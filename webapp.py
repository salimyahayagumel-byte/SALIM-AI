import os
from datetime import datetime, timezone
from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
from ai_client import ask_gemini, GeminiError
from database import init_db, save_message, get_history, clear_history, list_tasks, create_task, update_task, delete_task
load_dotenv()
app=Flask(__name__)
init_db()
@app.get('/')
def home(): return render_template('index.html', app_name=os.getenv('APP_NAME','SALIM AI'))
@app.get('/health')
def health():
 return jsonify({'service':'SALIM AI','status':'healthy','version':'5.0.0','ai_provider':'Google Gemini','api_key_configured':bool(os.getenv('GEMINI_API_KEY','').strip()),'model':os.getenv('GEMINI_MODEL','gemini-2.5-flash'),'timestamp':datetime.now(timezone.utc).isoformat()})
@app.post('/api/chat')
def chat():
 data=request.get_json(silent=True) or {}; message=str(data.get('message','')).strip()
 if not message: return jsonify({'error':'Rubuta tambaya kafin ka aika.'}),400
 if len(message)>12000: return jsonify({'error':'Saƙon ya yi tsawo. Ka rage shi.'}),413
 try:
  history=get_history(limit=12); save_message('user',message); reply=ask_gemini(message,history=history); save_message('assistant',reply); return jsonify({'reply':reply,'provider':'Gemini'})
 except GeminiError as exc:
  app.logger.warning('Gemini request failed: %s',exc); return jsonify({'error':str(exc),'reply':None}),exc.status_code
 except Exception:
  app.logger.exception('Unexpected chat failure'); return jsonify({'error':'An samu matsala a server. Duba Render Logs ko Termux terminal.'}),500
@app.get('/api/history')
def history(): return jsonify({'messages':get_history(limit=100)})
@app.delete('/api/history')
def history_clear(): clear_history(); return jsonify({'ok':True,'message':'An share tarihin tattaunawa.'})
@app.get('/api/tasks')
def tasks_get(): return jsonify({'tasks':list_tasks()})
@app.post('/api/tasks')
def tasks_post():
 data=request.get_json(silent=True) or {}; title=str(data.get('title','')).strip()
 if not title: return jsonify({'error':'Rubuta sunan aikin.'}),400
 if len(title)>240: return jsonify({'error':'Sunan aikin ya yi tsawo.'}),400
 return jsonify({'task':create_task(title)}),201
@app.patch('/api/tasks/<int:task_id>')
def tasks_patch(task_id):
 completed=(request.get_json(silent=True) or {}).get('completed')
 if not isinstance(completed,bool): return jsonify({'error':'completed dole ya zama true ko false.'}),400
 task=update_task(task_id,completed)
 if not task: return jsonify({'error':'Ba a sami aikin ba.'}),404
 return jsonify({'task':task})
@app.delete('/api/tasks/<int:task_id>')
def tasks_delete(task_id):
 if not delete_task(task_id): return jsonify({'error':'Ba a sami aikin ba.'}),404
 return jsonify({'ok':True})
if __name__=='__main__': app.run(host='0.0.0.0',port=int(os.getenv('PORT','8080')),debug=False)
