# middleware/tier_check.py

from functools import wraps
from flask import request, jsonify

def require_tier(min_tier):
    """Decorator to enforce tier-based access"""
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            user_tier = get_current_user_tier()
            
            tier_levels = {
                'unregistered': 0,
                'unpaid': 1,
                'paid': 2
            }
            
            if tier_levels[user_tier] < tier_levels[min_tier]:
                return jsonify({
                    'error': 'Insufficient access level',
                    'required_tier': min_tier,
                    'current_tier': user_tier
                }), 403
            
            return f(*args, **kwargs)
        return wrapped
    return decorator

# Usage in routes
@app.route('/api/cases/<id>/full')
@require_tier('paid')
def get_full_case(id):
    # Only paid users can access
    pass