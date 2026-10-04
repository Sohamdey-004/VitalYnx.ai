"""Conservative educational wellness suggestions; never treatment or diagnosis."""
def recommendations(user, latest=None):
    history=set((user.hereditary_conditions or []) + (user.current_health_issues or []))
    items=[]
    def add(title, trigger, food, movement, note):
        if trigger:
            items.append({'title':title,'food':food,'movement':movement,'note':note})
    add('Heart and blood-pressure aware basics', bool(history & {'Heart disease','High blood pressure','Family cardiac history'}) or (latest and latest.systolic >= 140), 'Choose vegetables, fruit, pulses, whole grains and less packaged salty food. Prefer water over sugary drinks.', 'Try comfortable-paced walking and gentle breathing. Avoid strenuous activity until a clinician says it is suitable.', 'If you have chest discomfort, severe headache, breathlessness, or a concerning reading, seek professional care instead of exercising.')
    add('Breathing comfort basics', 'Asthma' in history or 'Breathing difficulty' in history or (latest and latest.spo2 < 95), 'Stay hydrated and choose regular balanced meals; avoid any known personal food triggers.', 'Use calm seated breathing only when comfortable. Avoid breath-holds, intense exercise, or yoga during breathing difficulty.', 'Breathing trouble needs professional assessment, especially if sudden, severe, or worsening.')
    add('Blood-sugar supportive habits', 'Diabetes' in history, 'Favor high-fibre vegetables, beans, lentils and whole grains; pair carbohydrates with protein and follow your clinician’s nutrition plan.', 'A short walk after meals may be appropriate for many people; check with your care team if you use glucose-lowering medicine.', 'Food and exercise do not replace prescribed diabetes care or glucose monitoring.')
    add('Energy and gentle recovery', bool(history & {'Fatigue','Dizziness','Thyroid condition'}), 'Eat regular balanced meals and include iron/protein sources that suit your diet. Do not self-treat deficiencies.', 'Choose seated stretches, relaxed mobility, or a brief easy walk if you feel steady. Stop with dizziness.', 'Persistent fatigue or dizziness deserves medical discussion, particularly when new or severe.')
    if not items:
        items.append({'title':'Everyday wellness foundation','food':'Build meals around vegetables, fruit, pulses or lean protein, whole grains, and water.','movement':'Choose enjoyable, low-impact movement such as walking, gentle stretching, or beginner yoga.','note':'These are general wellbeing ideas—not treatment. Personal conditions and medicines may change what is appropriate.'})
    return items
