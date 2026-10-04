import pytest
from app import create_app
from models import db,User,Reading
@pytest.fixture
def client():
 app=create_app({'TESTING':True,'SQLALCHEMY_DATABASE_URI':'sqlite:///:memory:','SECRET_KEY':'test','ESP32_API_KEY':'device'})
 with app.app_context():db.create_all()
 with app.test_client() as c:yield c
def register(c):
 c.post('/register',data={'name':'Asha Rao','email':'asha@example.com','phone':'9999999999','password':'securepass','latitude':'19.076','longitude':'72.877','location_label':'Mumbai'},follow_redirects=False)
 with c.session_transaction() as s: email_code=s['dev_email_code'];phone_code=s['dev_phone_code']
 return c.post('/verify-contact',data={'email_code':email_code,'phone_code':phone_code},follow_redirects=True)
def onboard(c): return c.post('/onboarding',data={'gender':'Female','age':'22','height':'165','weight':'60','contact_name':'Sam','contact_phone':'8888888888','relationship':'Friend'},follow_redirects=True)
def test_registration_login_onboarding_and_logout(client):
 assert b'Build your health profile' in register(client).data
 assert b'Good morning' in onboard(client).data
 assert client.post('/logout',follow_redirects=True).status_code==200
 assert b'Good morning' in client.post('/login',data={'identity':'asha@example.com','password':'securepass'},follow_redirects=True).data
 with client.application.app_context():
  user=User.query.first();assert user.email_verified and user.phone_verified and user.location_label=='Mumbai'
def test_dashboard_requires_login(client): assert client.get('/dashboard').status_code==302
def test_disconnected_dashboard_hides_results_and_blocks_simulation(client):
 register(client);onboard(client)
 assert b'DEVICE NOT CONNECTED' in client.get('/dashboard').data
 assert client.post('/api/simulate',json={'scenario':'NORMAL'}).status_code==409
 assert client.post('/connect-device',follow_redirects=True).status_code==200
def test_simulation_storage_and_device_api(client):
 register(client);onboard(client)
 client.post('/connect-device')
 r=client.post('/api/simulate',json={'scenario':'EMERGENCY'});assert r.status_code==200 and r.json['analysis']['risk_level']=='HIGH_RISK'
 with client.application.app_context(): u=User.query.first();assert Reading.query.count()==1;uid=u.id
 payload={'user_id':uid,'pulse':75,'spo2':98,'systolic':120,'diastolic':80,'heart_rate':75,'ecg':[0,.1],'signal_quality':'good'}
 assert client.post('/api/reading',json=payload,headers={'X-ESP32-API-Key':'device'}).status_code==201
 assert client.post('/api/reading',json=payload).status_code==401
