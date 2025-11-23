"""Visit tracking routes."""

from flask import Blueprint, request, jsonify, g
import datetime

from src.models import Visit, Subscription, Plan
from src.config.database import db
from src.controllers.auth import auth_required

visits_bp = Blueprint('visits', __name__)


@visits_bp.route('/visits', methods=['POST'])
@auth_required
def record_visit():
    """
    Record a healthcare visit.
    Automatically calculates cost based on plan limits.
    """
    data = request.get_json() or {}
    subscription_id = data.get('subscription_id')
    notes = data.get('notes', '')
    
    if not subscription_id:
        return jsonify({'message': 'subscription_id is required'}), 400
    
    # Verify subscription exists and belongs to user
    subscription = Subscription.query.get(subscription_id)
    if not subscription:
        return jsonify({'message': 'Subscription not found'}), 404
    
    if subscription.user_id != g.user_id:
        return jsonify({'message': 'Unauthorized - not your subscription'}), 403
    
    # Check if subscription is active
    if subscription.end_date < datetime.date.today():
        return jsonify({'message': 'Subscription has expired'}), 400
    
    # Get the plan details
    plan = Plan.query.get(subscription.plan_id)
    if not plan:
        return jsonify({'message': 'Plan not found'}), 404
    
    # Calculate cost for this visit
    cost = subscription.calculate_visit_cost()
    visits_this_month = subscription.get_visits_this_month()
    
    # Create visit record
    visit = Visit(
        user_id=g.user_id,
        subscription_id=subscription_id,
        visit_date=datetime.datetime.utcnow(),
        cost=cost,
        notes=notes
    )
    
    db.session.add(visit)
    db.session.commit()
    
    # Determine if this was a free or paid visit
    is_included = cost == 0
    remaining_free = 0
    
    if plan.included_visits != float('inf'):
        remaining_free = max(0, plan.included_visits - visits_this_month - 1)
    else:
        remaining_free = 'unlimited'
    
    return jsonify({
        'message': 'Visit recorded successfully',
        'visit_id': visit.id,
        'visit_date': visit.visit_date.isoformat(),
        'cost': cost,
        'charged': cost > 0,
        'visits_used_this_month': visits_this_month + 1,
        'remaining_free_visits': remaining_free,
        'plan_name': plan.name
    }), 201


@visits_bp.route('/visits/summary', methods=['GET'])
@auth_required
def get_visit_summary():
    """
    Get summary of visit usage for active subscriptions.
    Shows visits used, remaining, and total charges.
    """
    # Get user's active subscriptions
    active_subs = Subscription.query.filter_by(user_id=g.user_id).filter(
        Subscription.end_date >= datetime.date.today()
    ).all()
    
    if not active_subs:
        return jsonify({
            'message': 'No active subscriptions',
            'subscriptions': []
        })
    
    summary = []
    total_charges = 0
    
    for sub in active_subs:
        plan = Plan.query.get(sub.plan_id)
        if not plan:
            continue
        
        visits_this_month = sub.get_visits_this_month()
        total_visits = sub.get_visits_count()
        
        # Calculate charges for extra visits
        visits_charged = Visit.query.filter(
            Visit.subscription_id == sub.id,
            Visit.cost > 0
        ).all()
        
        charges_this_month = sum(v.cost for v in visits_charged if v.visit_date.month == datetime.datetime.utcnow().month)
        total_charges += charges_this_month
        
        # Calculate remaining visits
        if plan.included_visits == float('inf'):
            remaining = 'unlimited'
            status = 'unlimited'
        else:
            remaining = max(0, plan.included_visits - visits_this_month)
            status = 'within_limit' if visits_this_month <= plan.included_visits else 'exceeded'
        
        summary.append({
            'subscription_id': sub.id,
            'plan_name': plan.name,
            'plan_price': plan.price,
            'included_visits': 'unlimited' if plan.included_visits == float('inf') else plan.included_visits,
            'visits_used_this_month': visits_this_month,
            'total_visits_all_time': total_visits,
            'remaining_free_visits': remaining,
            'extra_visit_price': plan.extra_visit_price,
            'charges_this_month': charges_this_month,
            'status': status,
            'active_until': sub.end_date.isoformat()
        })
    
    return jsonify({
        'subscriptions': summary,
        'total_extra_charges': total_charges,
        'month': datetime.datetime.utcnow().strftime('%B %Y')
    })


@visits_bp.route('/visits', methods=['GET'])
@auth_required
def get_visit_history():
    """
    Get detailed visit history for the user.
    """
    # Get all visits for user
    visits = Visit.query.filter_by(user_id=g.user_id).order_by(Visit.visit_date.desc()).all()
    
    history = []
    for visit in visits:
        subscription = Subscription.query.get(visit.subscription_id)
        plan = Plan.query.get(subscription.plan_id) if subscription else None
        
        history.append({
            'visit_id': visit.id,
            'visit_date': visit.visit_date.isoformat(),
            'subscription_id': visit.subscription_id,
            'plan_name': plan.name if plan else 'Unknown',
            'cost': visit.cost,
            'was_charged': visit.cost > 0,
            'notes': visit.notes
        })
    
    return jsonify({
        'visits': history,
        'total_visits': len(history)
    })
