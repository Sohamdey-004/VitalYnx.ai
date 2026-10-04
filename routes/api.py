from flask import Blueprint,request,jsonify,current_app
from models import db,User,Reading
from services.ai_service import analyze_health
from services.simulation import generate
from .auth import current_user
from .dashboard import login_required
from services.device_status import device_is_connected, latest_device_reading
api_bp=Blueprint('api',__name__)
REQUIRED=('pulse','spo2','systolic','diastolic','heart_rate','ecg')
def save(data,user,source='demo'):
 previous=Reading.query.filter_by(user_id=user.id,source=source).order_by(Reading.created_at.desc()).limit(5).all()
 result=analyze_health(data,user,previous)
 r=Reading(user_id=user.id,pulse=int(data['pulse']),spo2=int(data['spo2']),systolic=int(data['systolic']),diastolic=int(data['diastolic']),heart_rate=int(data['heart_rate']),ecg_data=data.get('ecg',[]),signal_quality=data.get('signal_quality','good'),risk_level=result['risk_level'],risk_score=result['score'],ai_analysis=result['analysis'],source=source);db.session.add(r);db.session.commit();return r,result
@api_bp.route('/api/simulate',methods=['POST'])
@login_required
def simulate():
 name=(request.get_json(silent=True) or {}).get('scenario','NORMAL').upper();data=generate(name);r,result=save(data,current_user());return jsonify({'reading_id':r.id,'reading':data,'analysis':result})

@api_bp.route('/api/device-status')
@login_required
def device_status():
 reading=latest_device_reading(current_user().id)
 return jsonify({'connected':device_is_connected(reading),'last_seen':reading.created_at.isoformat() if reading else None})
@api_bp.route('/api/reading',methods=['POST'])
def reading():
 if request.headers.get('X-ESP32-API-Key') != current_app.config['ESP32_API_KEY']: return jsonify({'error':'Unauthorized device'}),401
 data=request.get_json(silent=True) or {}
 if any(k not in data for k in REQUIRED): return jsonify({'error':'Missing required fields'}),400
 try:
  for k in REQUIRED[:-1]: int(data[k])
 except (ValueError,TypeError): return jsonify({'error':'Vitals must be numeric'}),400
 user=db.session.get(User, data.get('user_id'))
 if not user:return jsonify({'error':'A valid user_id is required'}),400
 r,result=save(data,user,source='device');return jsonify({'id':r.id,'risk_level':result['risk_level'],'analysis':result['analysis']}),201
