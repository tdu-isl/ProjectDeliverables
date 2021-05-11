import sqlite3
from fastapi import APIRouter

router = APIRouter()

@router.get('/users/{user}')
def get_userID(user: str):
    usersDB = 'backend/db/TEST.db'
    conn = sqlite3.connect(usersDB)
    cur = conn.cursor()
    cur.execute('SELECT id,name from persons WHERE name=\'' + user + '\'')
    id = cur.fetchall()
    cur.close()
    conn.close()
    
    if len(id) >= 1:
        return {
            'status': 'succeeded',
            user: id[0][0]
        }
    else:
        return {
            'status': 'failed'
        }
