import os, sqlite3
from pathlib import Path
from datetime import datetime,timezone
DB_PATH=os.getenv('SALIM_AI_DB',str(Path(__file__).resolve().parent/'salim_ai.db'))
def connect():
 c=sqlite3.connect(DB_PATH,timeout=15); c.row_factory=sqlite3.Row; return c
def now(): return datetime.now(timezone.utc).isoformat()
def init_db():
 Path(DB_PATH).parent.mkdir(parents=True,exist_ok=True)
 with connect() as db:
  db.execute("CREATE TABLE IF NOT EXISTS messages(id INTEGER PRIMARY KEY AUTOINCREMENT,role TEXT NOT NULL CHECK(role IN ('user','assistant')),content TEXT NOT NULL,created_at TEXT NOT NULL)")
  db.execute('CREATE TABLE IF NOT EXISTS tasks(id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT NOT NULL,completed INTEGER NOT NULL DEFAULT 0,created_at TEXT NOT NULL)')
def save_message(role,content):
 with connect() as db:
  db.execute('INSERT INTO messages(role,content,created_at) VALUES(?,?,?)',(role,content,now())); db.execute('DELETE FROM messages WHERE id NOT IN (SELECT id FROM messages ORDER BY id DESC LIMIT 300)')
def get_history(limit=100):
 with connect() as db: rows=db.execute('SELECT role,content,created_at FROM messages ORDER BY id DESC LIMIT ?',(int(limit),)).fetchall()
 return [dict(x) for x in reversed(rows)]
def clear_history():
 with connect() as db: db.execute('DELETE FROM messages')
def list_tasks():
 with connect() as db: rows=db.execute('SELECT id,title,completed,created_at FROM tasks ORDER BY id DESC LIMIT 100').fetchall()
 return [{'id':r['id'],'title':r['title'],'completed':bool(r['completed']),'created_at':r['created_at']} for r in rows]
def create_task(title):
 with connect() as db: cur=db.execute('INSERT INTO tasks(title,completed,created_at) VALUES(?,0,?)',(title,now())); tid=cur.lastrowid
 return next(t for t in list_tasks() if t['id']==tid)
def update_task(tid,completed):
 with connect() as db: cur=db.execute('UPDATE tasks SET completed=? WHERE id=?',(int(completed),tid))
 if not cur.rowcount: return None
 return next((t for t in list_tasks() if t['id']==tid),None)
def delete_task(tid):
 with connect() as db: cur=db.execute('DELETE FROM tasks WHERE id=?',(tid,)); return cur.rowcount>0
