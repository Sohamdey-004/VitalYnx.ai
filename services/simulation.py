import math, random
SCENARIOS = {
 'NORMAL': (78,98,120,78), 'HIGH_HEART_RATE': (122,97,128,82), 'LOW_SPO2': (92,91,126,80),
 'HIGH_BLOOD_PRESSURE': (84,97,158,98), 'ABNORMAL_COMBINATION': (128,92,165,104), 'EMERGENCY': (142,87,186,122)}
def ecg_waveform(rate, points=180):
    out=[]; beat=max(18, round(3600/rate))
    for i in range(points):
        phase=i%beat; v=0.03*math.sin(i*.32)+random.uniform(-.025,.025)
        if phase in range(3,6): v += .16
        if phase == 9: v -= .28
        if phase == 10: v += .95
        if phase == 11: v -= .38
        if phase in range(17,22): v += .19*math.sin((phase-17)/5*math.pi)
        out.append(round(v,3))
    return out
def generate(name='NORMAL'):
    p,o,s,d=SCENARIOS.get(name, SCENARIOS['NORMAL'])
    jitter=lambda x,n: x+random.randint(-n,n)
    pulse=jitter(p,3); return {'pulse':pulse,'spo2':max(80,jitter(o,1)),'systolic':jitter(s,4),'diastolic':jitter(d,3),'heart_rate':pulse,'ecg':ecg_waveform(pulse),'signal_quality':'good','scenario':name}
