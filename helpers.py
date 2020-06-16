from flask import redirect, render_template, request, session
from functools import wraps
import sqlite3


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

class DB_Handler:
    def __init__(self, database):
        self.db_name = database
    
    def execute(self, query, *args):
        
        with sqlite3.connect(self.db_name) as con:
            cur = con.cursor()
            res = cur.execute(query, args)
            con.commit()
            return res
        