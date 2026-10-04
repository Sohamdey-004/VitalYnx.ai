from datetime import datetime, timedelta, timezone

from flask import Blueprint, render_template, jsonify, request
from sqlalchemy import func

from .auth import current_user
from .dashboard import login_required
from models import Reading

records_bp=Blueprint('records',__name__)
HISTORY_DAYS = 30
PAGE_SIZE = 25


def monthly_readings(user_id):
 cutoff = datetime.now(timezone.utc) - timedelta(days=HISTORY_DAYS)
 return Reading.query.filter(
  Reading.user_id == user_id,
  Reading.source == 'device',
  Reading.created_at >= cutoff,
 )


@records_bp.route('/records')
@login_required
def records():
 user = current_user()
 query = monthly_readings(user.id)
 total = query.count()
 page = max(request.args.get('page', 1, type=int), 1)
 pages = max((total + PAGE_SIZE - 1) // PAGE_SIZE, 1)
 page = min(page, pages)
 readings = query.order_by(Reading.created_at.desc()).offset((page - 1) * PAGE_SIZE).limit(PAGE_SIZE).all()
 stats = query.with_entities(
  func.count(Reading.id),
  func.avg(Reading.pulse),
  func.count(func.distinct(func.date(Reading.created_at))),
 ).one()
 return render_template(
  'records.html', user=user, readings=readings, total=total, page=page,
  pages=pages, avg_pulse=round(stats[1]) if stats[1] is not None else None,
  active_days=stats[2], history_days=HISTORY_DAYS,
 )


@records_bp.route('/api/trends')
@login_required
def trends():
 rows = monthly_readings(current_user().id).with_entities(
  func.date(Reading.created_at).label('day'),
  func.avg(Reading.pulse).label('pulse'),
  func.avg(Reading.spo2).label('spo2'),
  func.avg(Reading.systolic).label('systolic'),
  func.avg(Reading.diastolic).label('diastolic'),
 ).group_by(func.date(Reading.created_at)).order_by(func.date(Reading.created_at)).all()
 return jsonify({
  'labels': [row.day for row in rows],
  'pulse': [round(row.pulse, 1) for row in rows],
  'spo2': [round(row.spo2, 1) for row in rows],
  'systolic': [round(row.systolic, 1) for row in rows],
  'diastolic': [round(row.diastolic, 1) for row in rows],
 })
