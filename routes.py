"""Main routes blueprint for subscription plans."""

from flask import Blueprint, request, jsonify, g
import datetime

from models import db, Plan, Subscription
from auth import auth_required

plans_bp = Blueprint('plans', __name__)


@plans_bp.route('/plans', methods=['GET'])
@auth_required
def get_plans():
    """Get all available subscription plans."""
    plans = Plan.query.all()
    out = []

    for p in plans:
        out.append({
            'id': p.id,
            'name': p.name,
            'price': p.price,
            'included_visits': 'Unlimited' if p.included_visits == float('inf') else p.included_visits,
            'extra_visit_price': p.extra_visit_price,
            'services': p.services()
        })

    return jsonify(out)


@plans_bp.route('/subscriptions', methods=['GET'])
@auth_required
def get_user_subscriptions():
    """Get current user's subscriptions."""
    subscriptions = Subscription.query.filter_by(user_id=g.user_id).all()
    out = []

    for sub in subscriptions:
        plan = Plan.query.get(sub.plan_id)
        out.append({
            'id': sub.id,
            'plan_name': plan.name if plan else 'Unknown',
            'plan_id': sub.plan_id,
            'start_date': sub.start_date.isoformat(),
            'end_date': sub.end_date.isoformat(),
            'active': sub.end_date >= datetime.date.today()
        })

    return jsonify(out)


@plans_bp.route('/subscriptions', methods=['POST'])
@auth_required
def create_subscription():
    """Subscribe to a plan."""
    data = request.get_json() or {}
    plan_id = data.get('plan_id')
    duration_days = data.get('duration_days', 30)  # Default 30 days

    if not plan_id:
        return jsonify({'message': 'plan_id is required'}), 400

    plan = Plan.query.get(plan_id)
    if not plan:
        return jsonify({'message': 'Plan not found'}), 404

    # Check for existing active subscription
    active_sub = Subscription.query.filter_by(user_id=g.user_id).filter(
        Subscription.end_date >= datetime.date.today()
    ).first()

    if active_sub:
        return jsonify({'message': 'You already have an active subscription'}), 400

    # Create new subscription
    start_date = datetime.date.today()
    end_date = start_date + datetime.timedelta(days=duration_days)

    subscription = Subscription(
        user_id=g.user_id,
        plan_id=plan_id,
        start_date=start_date,
        end_date=end_date
    )

    db.session.add(subscription)
    db.session.commit()

    return jsonify({
        'message': 'Subscription created successfully',
        'subscription_id': subscription.id,
        'plan_name': plan.name,
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat()
    }), 201


@plans_bp.route('/subscriptions/<int:subscription_id>', methods=['DELETE'])
@auth_required
def cancel_subscription(subscription_id):
    """Cancel a subscription."""
    subscription = Subscription.query.get(subscription_id)

    if not subscription:
        return jsonify({'message': 'Subscription not found'}), 404

    if subscription.user_id != g.user_id:
        return jsonify({'message': 'Unauthorized'}), 403

    db.session.delete(subscription)
    db.session.commit()

    return jsonify({'message': 'Subscription cancelled successfully'})
