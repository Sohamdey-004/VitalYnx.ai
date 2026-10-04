from functools import wraps
from flask import Blueprint, render_template, redirect, url_for
from .auth import current_user
from models import Reading
from services.wellness_recommendations import recommendations
from services.device_status import device_is_connected, latest_device_reading
dashboard_bp=Blueprint('dashboard',__name__)
def login_required(f):
 @wraps(f)
 def wrapped(*a,**k):
  u=current_user()
  if not u:return redirect(url_for('auth.login'))
  if not u.profile_completed:return redirect(url_for('auth.onboarding'))
  return f(*a,**k)
 return wrapped
@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
@login_required
def index():
 u=current_user()
 latest=latest_device_reading(u.id)
 if not device_is_connected(latest):
  return render_template('dashboard_disconnected.html',user=u)
 recent=Reading.query.filter_by(user_id=u.id,source='device').order_by(Reading.created_at.desc()).limit(5).all()
 return render_template('dashboard.html',user=u,latest=latest,recent=recent)
@dashboard_bp.route('/health-check')
@login_required
def health_check():
 latest=latest_device_reading(current_user().id)
 if not device_is_connected(latest): return redirect(url_for('dashboard.index'))
 return render_template('health_check.html',user=current_user(),latest=latest)
@dashboard_bp.route('/connect-device', methods=['POST'])
@login_required
def connect_device():
 return redirect(url_for('dashboard.index'))
@dashboard_bp.route('/consultation')
@login_required
def consultation():
 u=current_user();latest=latest_device_reading(u.id)
 connected=device_is_connected(latest)
 return render_template(
  'consultation.html', user=u,
  recommendations=recommendations(u,latest if connected else None),
  device_connected=connected,
 )
@dashboard_bp.route('/exercises')
@login_required
def exercises(): return render_template('exercises.html',user=current_user())
