from flask import Flask, render_template, redirect, request, session
from sqlalchemy import inspect, text
from werkzeug.middleware.proxy_fix import ProxyFix
from config import Config
from models import db
from routes.auth import current_user
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.api import api_bp
from routes.profile import profile_bp
from routes.records import records_bp
from routes.emergency import emergency_bp
from services.device_status import device_is_connected, latest_device_reading
def create_app(test_config=None):
 app=Flask(__name__);app.config.from_object(Config)
 if test_config:app.config.update(test_config)
 secret_key=app.config['SECRET_KEY']
 if app.config['APP_ENV'] == 'production' and (not secret_key or secret_key == 'dev-only-change-me' or len(secret_key) < 32):
  raise RuntimeError('Set a unique SECRET_KEY with at least 32 characters before starting in production.')
 proxy_count=app.config['TRUST_PROXY_COUNT']
 if proxy_count:
  app.wsgi_app=ProxyFix(app.wsgi_app,x_for=proxy_count,x_proto=proxy_count,x_host=proxy_count,x_port=proxy_count)
 db.init_app(app)
 app.register_blueprint(auth_bp);app.register_blueprint(dashboard_bp);app.register_blueprint(api_bp);app.register_blueprint(profile_bp);app.register_blueprint(records_bp);app.register_blueprint(emergency_bp)
 @app.context_processor
 def inject_device_status():
  user=current_user()
  reading=latest_device_reading(user.id) if user else None
  return {'device_connected':device_is_connected(reading)}
 @app.before_request
 def require_https():
  if app.config['FORCE_HTTPS'] and not request.is_secure:
   if request.path.startswith('/api/'):
    return 'HTTPS is required for API requests.', 426
   return redirect(request.url.replace('http://', 'https://', 1), code=308)
 @app.after_request
 def security_headers(response):
  response.headers.setdefault('X-Content-Type-Options', 'nosniff')
  response.headers.setdefault('X-Frame-Options', 'DENY')
  response.headers.setdefault('Referrer-Policy', 'strict-origin-when-cross-origin')
  response.headers.setdefault('Permissions-Policy', 'camera=(), microphone=(), geolocation=(self)')
  if session.get('user_id'):
   response.headers.setdefault('Cache-Control', 'no-store')
  if app.config['ENABLE_HSTS'] and request.is_secure:
   response.headers.setdefault('Strict-Transport-Security', f"max-age={app.config['HSTS_MAX_AGE']}")
  return response
 @app.errorhandler(404)
 def missing(_):return render_template('404.html'),404
 with app.app_context():
  db.create_all()
  reading_columns = {column['name'] for column in inspect(db.engine).get_columns('reading')}
  if 'source' not in reading_columns:
   db.session.execute(text("ALTER TABLE reading ADD COLUMN source VARCHAR(16) NOT NULL DEFAULT 'demo'"))
   db.session.commit()
 return app
app=create_app()
if __name__=='__main__': app.run(host='127.0.0.1',debug=app.config['DEBUG'],port=5000)
