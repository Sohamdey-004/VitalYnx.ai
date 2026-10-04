"""Transparent prototype screening rules; this is not diagnostic software."""
def assess(data, user=None, previous=None):
    p, o, s, d = [int(data[k]) for k in ('pulse','spo2','systolic','diastolic')]
    score, reasons = 0, []
    def add(points, reason):
        nonlocal score
        score += points; reasons.append(reason)
    if o < 90: add(60, 'Oxygen saturation is very low in this prototype reading.')
    elif o < 95: add(25, 'Oxygen saturation is below the configured monitoring range.')
    if p >= 130 or p <= 40: add(45, 'Pulse is substantially outside the configured range.')
    elif p >= 101 or p < 55: add(18, 'Pulse is outside the usual resting range.')
    if s >= 180 or d >= 120: add(55, 'Blood pressure is in a severely elevated configured range.')
    elif s >= 140 or d >= 90: add(28, 'Blood pressure is elevated in this screening.')
    symptoms = (user.current_health_issues if user else []) or []
    if any(x in symptoms for x in ('Chest discomfort','Breathing difficulty','Dizziness')) and score >= 18:
        add(20, 'Reported symptoms increase the need for caution.')
    if score >= 55:
        level, action, emergency = 'HIGH_RISK', 'Stop strenuous activity and seek urgent professional medical evaluation. If severe symptoms are present, use the emergency workflow.', True
    elif score >= 18:
        level, action, emergency = 'CAUTION', 'Rest, repeat the measurement correctly, and consider medical evaluation if readings persist or symptoms are present.', False
    else:
        level, action, emergency = 'STABLE', 'No immediate warning was found by the prototype rules. Continue monitoring and follow routine care advice.', False
    return {'risk_level': level, 'score': min(score,100), 'reasons': reasons or ['Readings are within the configured prototype monitoring ranges.'], 'recommended_action': action, 'emergency_required': emergency}
