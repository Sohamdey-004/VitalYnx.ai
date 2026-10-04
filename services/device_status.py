from datetime import datetime, timedelta, timezone

from models import Reading


DEVICE_ONLINE_WINDOW = timedelta(seconds=120)


def latest_device_reading(user_id):
    return Reading.query.filter_by(user_id=user_id, source='device').order_by(
        Reading.created_at.desc()
    ).first()


def device_is_connected(reading, now=None):
    if reading is None or reading.created_at is None:
        return False

    now = now or datetime.now(timezone.utc)
    created_at = reading.created_at
    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=timezone.utc)

    age = now - created_at
    return timedelta(0) <= age <= DEVICE_ONLINE_WINDOW
