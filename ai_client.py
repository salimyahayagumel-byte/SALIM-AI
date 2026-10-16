import os, requests
API_URL='https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent'
class GeminiError(Exception):
 def __init__(self,message,status_code=502): super().__init__(message); self.status_code=status_code
SYSTEM_PROMPT="""Kai ne SALIM AI, mataimakin AI mai ladabi da gaskiya. Ka fi amfani da Hausa idan mai amfani ya yi Hausa; ka iya Turanci idan ya yi Turanci. Ka ba da amsa mai amfani, bayyananniya kuma mai tsari. Kada ka ƙirƙiri hujjoji ko ka ce ka aiwatar da aiki idan ba ka yi ba. Idan ba ka da tabbaci, ka faɗi haka. Ka taimaka da coding, bayani, rubutu, shiri da tunani. Kada ka nemi sirrin mai amfani ko API key."""
def ask_gemini(message,history=None):
 key=os.getenv('GEMINI_API_KEY','').strip()
 if not key: raise GeminiError('Ba a saita GEMINI_API_KEY ba. Ƙara shi a Render Environment ko cikin .env na Termux.',503)
 model=os.getenv('GEMINI_MODEL','gemini-2.5-flash').strip() or 'gemini-2.5-flash'; contents=[]
 for item in (history or [])[-12:]:
  role=item.get('role'); text=str(item.get('content','')).strip()
  if role in ('user','assistant') and text: contents.append({'role':'user' if role=='user' else 'model','parts':[{'text':text[:12000]}]})
 contents.append({'role':'user','parts':[{'text':message}]})
 payload={'systemInstruction':{'parts':[{'text':SYSTEM_PROMPT}]},'contents':contents,'generationConfig':{'temperature':0.7,'topP':0.9,'maxOutputTokens':2048}}
 try: r=requests.post(API_URL.format(model=model),params={'key':key},json=payload,timeout=45)
 except requests.Timeout: raise GeminiError('Gemini ya ɗauki lokaci fiye da kima. Ka sake gwadawa.',504)
 except requests.RequestException: raise GeminiError('Ba a iya haɗuwa da sabis ɗin Gemini ba. Duba intanet ko sake gwadawa.',502)
 if r.status_code in (401,403): raise GeminiError('Gemini ya ƙi API key ko izini. Duba GEMINI_API_KEY a Render Environment.',502)
 if r.status_code==404: raise GeminiError(f"Ba a sami Gemini model '{model}' ba. Saita GEMINI_MODEL zuwa model da AI Studio ya nuna yana samuwa.",502)
 if r.status_code==429: raise GeminiError('An kai iyakar Gemini API (quota/rate limit). Jira quota ta sabunta ko duba AI Studio.',429)
 if r.status_code>=500: raise GeminiError('Sabis ɗin Gemini yana da matsala na ɗan lokaci. Ka sake gwadawa daga baya.',502)
 if not r.ok:
  try: detail=r.json().get('error',{}).get('message','')[:220]
  except Exception: detail=''
  raise GeminiError(f'Gemini API ya dawo da HTTP {r.status_code}: {detail or "Duba API key, model da Google AI Studio."}',502)
 try:
  data=r.json(); candidates=data.get('candidates') or []; parts=candidates[0].get('content',{}).get('parts',[]) if candidates else []; answer='\n'.join(p.get('text','') for p in parts if p.get('text'))
  if not answer.strip():
   reason=(data.get('promptFeedback') or {}).get('blockReason')
   if reason: raise GeminiError(f'Gemini bai amsa ba saboda safety filter ({reason}). Ka sake tsara tambayar.',400)
   raise GeminiError('Gemini bai dawo da amsa ba. Ka sake gwadawa.',502)
  return answer.strip()
 except (ValueError,KeyError,IndexError,TypeError): raise GeminiError('Ba a iya karanta amsar Gemini ba. Ka duba Render Logs.',502)
