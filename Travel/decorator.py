from functools import wraps
from flask import redirect, url_for, flash, session

def admin_required(f):
    """Decorator to ensure the user is logged in as an admin."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:  
            flash("You must be logged in as an admin to access this page.", "warning")
            return redirect(url_for('travel.admin_login'))  
        return f(*args, **kwargs)
    return decorated_function
