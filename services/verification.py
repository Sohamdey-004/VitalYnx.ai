"""Contact verification with optional SMTP delivery and safe development fallback."""
import base64, os, secrets, smtplib
from email.message import EmailMessage
from urllib.parse import urlencode
from urllib.request import Request, urlopen

def code():
    return f"{secrets.randbelow(1_000_000):06d}"

def deliver_email(address, value):
    host = os.getenv('SMTP_HOST')
    if not host:
        return False
    message = EmailMessage()
    message['Subject'] = 'Your Vitalynx AI verification code'
    message['From'] = os.getenv('SMTP_FROM', os.getenv('SMTP_USERNAME', 'no-reply@vitalynx.local'))
    message['To'] = address
    message.set_content(f'Your Vitalynx AI verification code is {value}. It expires shortly. Do not share it.')
    with smtplib.SMTP(host, int(os.getenv('SMTP_PORT', '587')), timeout=10) as client:
        if os.getenv('SMTP_TLS', 'true').lower() == 'true': client.starttls()
        if os.getenv('SMTP_USERNAME'): client.login(os.getenv('SMTP_USERNAME'), os.getenv('SMTP_PASSWORD', ''))
        client.send_message(message)
    return True

def phone_delivery_configured():
    return bool(os.getenv('TWILIO_ACCOUNT_SID') and os.getenv('TWILIO_AUTH_TOKEN') and os.getenv('TWILIO_FROM_PHONE'))

def deliver_phone(number, value):
    if not phone_delivery_configured(): return False
    sid, token = os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN']
    payload = urlencode({'To': number, 'From': os.environ['TWILIO_FROM_PHONE'], 'Body': f'Your Vitalynx AI verification code is {value}. Do not share it.'}).encode()
    auth = base64.b64encode(f'{sid}:{token}'.encode()).decode()
    req = Request(f'https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json', payload, {'Authorization':f'Basic {auth}','Content-Type':'application/x-www-form-urlencoded'})
    with urlopen(req, timeout=10): pass
    return True
