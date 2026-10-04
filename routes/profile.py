from flask import Blueprint,render_template,request,redirect,url_for,flash
from models import db
from .auth import current_user
from .dashboard import login_required
profile_bp=Blueprint('profile',__name__)
@profile_bp.route('/profile',methods=['GET','POST'])
@login_required
def profile():
 u=current_user()
 if request.method=='POST':
  for key in ('name','phone','gender','emergency_contact_name','emergency_contact_phone','emergency_contact_relationship'): setattr(u,key,request.form.get(key,''))
  try:u.age=int(request.form['age']);u.height=float(request.form['height']);u.weight=float(request.form['weight'])
  except ValueError:flash('Please use valid numbers for age, height, and weight.','error');return render_template('profile.html',user=u)
  u.hereditary_conditions=request.form.getlist('hereditary');u.current_health_issues=request.form.getlist('issues');u.wellness_preferences=request.form.getlist('wellness');db.session.commit();flash('Profile saved.','success');return redirect(url_for('profile.profile'))
 return render_template('profile.html',user=u)
