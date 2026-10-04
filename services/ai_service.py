"""Safe AI boundary; network failures always fall back to deterministic screening."""
import json, os
from urllib.request import Request, urlopen
from .health_analysis import assess
def analyze_health(data, user=None, previous=None):
    result = assess(data, user, previous)
    summary = f"{result['risk_level'].replace('_',' ')}: " + ' '.join(result['reasons']) + ' ' + result['recommended_action']
    safe_suffix = ' This is prototype screening, not a diagnosis or medical advice.'
    result['analysis'], result['source'] = summary + safe_suffix, 'deterministic safety rules'
    # Optional OpenAI-compatible endpoint. Classification always stays rule-based.
    key = os.getenv('AI_API_KEY')
    if key:
        try:
            prompt = ('Rewrite this safety screening summary in clear, supportive language. Do not diagnose, '
                      'prescribe, claim certainty, or remove the disclaimer: ' + result['analysis'])
            payload = json.dumps({'model': os.getenv('AI_MODEL','gpt-4o-mini'),'messages':[{'role':'user','content':prompt}],'temperature':0.2,'max_tokens':160}).encode()
            req = Request(os.getenv('AI_API_BASE','https://api.openai.com/v1').rstrip('/') + '/chat/completions', payload, {'Authorization':'Bearer '+key,'Content-Type':'application/json'})
            with urlopen(req, timeout=5) as response: text = json.loads(response.read())['choices'][0]['message']['content'].strip()
            if text: result['analysis'], result['source'] = text + safe_suffix, 'optional LLM explanation'
        except Exception: pass
    return result
