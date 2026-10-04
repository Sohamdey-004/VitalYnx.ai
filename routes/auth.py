from datetime import datetime, timedelta, timezone
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from models import db, User, VerificationChallenge
from services.verification import code, deliver_email, deliver_phone
from werkzeug.security import generate_password_hash, check_password_hash
auth_bp=Blueprint('auth',__name__)
@auth_bp.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        email=request.form.get('email','').strip().lower(); phone=request.form.get('phone','').strip(); name=request.form.get('name','').strip(); password=request.form.get('password','')
        if not all([email,phone,name]) or len(password)<8: flash('Enter name, a valid email/phone, and a password of at least 8 characters.','error')
        elif User.query.filter((User.email==email)|(User.phone==phone)).first(): flash('An account with that email or phone already exists.','error')
        else:
            try:
                latitude=float(request.form['latitude']) if request.form.get('latitude') else None; longitude=float(request.form['longitude']) if request.form.get('longitude') else None
            except ValueError: latitude=longitude=None
            u=User(email=email,phone=phone,name=name,location_label=request.form.get('location_label','').strip()[:180],location_latitude=latitude,location_longitude=longitude);u.set_password(password);db.session.add(u);db.session.flush()
            email_code, phone_code = code(), code()
            challenge=VerificationChallenge(user_id=u.id,email_code_hash=generate_password_hash(email_code),phone_code_hash=generate_password_hash(phone_code),expires_at=datetime.now(timezone.utc)+timedelta(minutes=10));db.session.add(challenge);db.session.commit()
            sent_email=sent_phone=False
            try: sent_email=deliver_email(email,email_code)
            except Exception: pass
            try: sent_phone=deliver_phone(phone,phone_code)
            except Exception: pass
            session.clear();session['verification_user_id']=u.id
            if current_app.config['DEV_VERIFICATION_MODE']:
                session['dev_email_code']=email_code;session['dev_phone_code']=phone_code
            elif not (sent_email and sent_phone):
                flash('Verification delivery is not configured. Add SMTP and Twilio credentials or enable development mode.','error');return redirect(url_for('auth.register'))
            return redirect(url_for('auth.verify_contact'))
    return render_template('register.html')
@auth_bp.route('/verify-contact', methods=['GET','POST'])
def verify_contact():
    user_id=session.get('verification_user_id'); u=db.session.get(User,user_id) if user_id else None
    if not u:return redirect(url_for('auth.register'))
    if request.method=='POST':
        challenge=VerificationChallenge.query.filter_by(user_id=u.id).first()
        now=datetime.now(timezone.utc)
        if not challenge or challenge.expires_at.replace(tzinfo=timezone.utc) < now: flash('Your code expired. Register again to request a new one.','error')
        elif not (check_password_hash(challenge.email_code_hash,request.form.get('email_code','')) and check_password_hash(challenge.phone_code_hash,request.form.get('phone_code',''))): flash('Those verification codes do not match. Please try again.','error')
        else:
            u.email_verified=True;u.phone_verified=True;db.session.delete(challenge);db.session.commit();session.clear();session['user_id']=u.id;return redirect(url_for('auth.onboarding'))
    return render_template('verify_contact.html',user=None, email=u.email, phone=u.phone, dev_email_code=session.get('dev_email_code'), dev_phone_code=session.get('dev_phone_code'))
@auth_bp.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        identity=request.form.get('identity','').strip().lower();u=User.query.filter((User.email==identity)|(User.phone==identity)).first()
        if u and u.check_password(request.form.get('password','')):
            session.clear()
            if not (u.email_verified and u.phone_verified): session['verification_user_id']=u.id;return redirect(url_for('auth.verify_contact'))
            session['user_id']=u.id;return redirect(url_for('dashboard.index') if u.profile_completed else url_for('auth.onboarding'))
        flash('Invalid login details.','error')
    return render_template('login.html')
@auth_bp.route('/onboarding',methods=['GET','POST'])
def onboarding():
    u=current_user()
    if not u:return redirect(url_for('auth.login'))
    if request.method=='POST':
        try: u.age=int(request.form['age']);u.height=float(request.form['height']);u.weight=float(request.form['weight'])
        except (KeyError,ValueError): flash('Age, height, and weight must be valid numbers.','error');return render_template('onboarding.html',user=u)
        u.gender=request.form.get('gender');u.hereditary_conditions=request.form.getlist('hereditary');u.current_health_issues=request.form.getlist('issues');u.wellness_preferences=request.form.getlist('wellness');u.emergency_contact_name=request.form.get('contact_name');u.emergency_contact_phone=request.form.get('contact_phone');u.emergency_contact_relationship=request.form.get('relationship');u.profile_completed=True;db.session.commit();return redirect(url_for('dashboard.index'))
    return render_template('onboarding.html',user=u)
@auth_bp.route('/logout',methods=['POST'])
def logout(): session.clear();return redirect(url_for('auth.login'))
def current_user(): return db.session.get(User, session.get('user_id')) if session.get('user_id') else None
