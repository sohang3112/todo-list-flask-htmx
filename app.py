from typing import Any, Mapping
from pprint import pprint
import logging
import sqlite3

from flask import Flask, request, render_template
import pandas as pd


#region helper-funcitons

def db_connection():
    conn = sqlite3.connect(
        'todo-list.db', 
        isolation_level=None,   # auto-commit: https://stackoverflow.com/a/23634805/12947681
    )

    # By default, cursor.fetchall() returns list of tuples
    # This instead makes it return list of sqlite.Row() objects
    # row = sqlite.Row() acts like a dict -
    # row["database_column"] will give the corresponding value
    # Source: https://docs.python.org/3/library/sqlite3.html?highlight=lastrowid#sqlite3.Cursor.row_factory
    conn.row_factory = sqlite3.Row

    return conn

def db_query(query: str, *args) -> list[Mapping[str, Any]] | int:
    """Run database query
    SELECT query: return fetched data as list of rows.
       Each row is a dict whose keys are database columns.
    INSERT, UPDATE, etc. query: return last inserted row's ROWID.
    """
    with db_connection() as conn:
        cursor = conn.cursor()
        res = cursor.execute(query, *args)
        ans_rows = res.fetchall()
        # cursor.description=None in case of
        # Insert, Update, Delete, etc. queries
        if not cursor.description:
            return cursor.lastrowid    # last inserted row
        # columns = [x[0] for x in cursor.description]
        # return [dict(zip(columns, row)) for row in ans_rows]
        return ans_rows

def mk_db_table():
    db_query("""
        CREATE TABLE IF NOT EXISTS todo_list(id integer primary key, item, due_date)
    """)

#endregion helper-funcitons

#region flask-api
    
app = Flask(__name__)
app.logger.setLevel(level=logging.INFO)

@app.before_request
def log_request():
    request_line = f"{request.method} {request.path}"
    headers = "\n".join([f"{key}: {value}" for key, value in request.headers.items()])
    body = request.get_data(as_text=True)
    app.logger.debug(f"{request_line}\n{headers}\n\n{body}")

@app.after_request
def disable_caching(response):
    response.headers['Cache-Control'] = 'no-store'
    return response

@app.get('/')
def index():
    todo_list = db_query("""
        SELECT id, 
               IFNULL(item, "") AS item, 
               IFNULL(due_date, "") AS due_date
        FROM todo_list
    """)
    return render_template('index.html', todo_list=todo_list)

@app.post('/row/new')
def new_row():
    inserted_rowid = db_query("INSERT INTO todo_list(item, due_date) VALUES (NULL, NULL)")
    inserted_id = db_query("SELECT id FROM todo_list WHERE rowid = ?", (inserted_rowid,))[0]['id']
    return render_template('new_row.html', id=inserted_id)

# MAYBE TODO: use PUT http method instead of POST ??
@app.post('/row/<id>/edit')
def edit_row(id: int):
    pass

# MAYBE TODO: use DELETE http method instead of POST ??
@app.post('/row/<id>/delete')
def delete_row(id: int):
    # TODO: raise error if sql query raises error (i.e., id doesn't exist)
    db_query("DELETE FROM todo_list WHERE id = ?", (id,))
    return ""

#endregion flask-api

if __name__ == '__main__':
    mk_db_table()
    app.logger.debug('Starting app')
    app.run(debug=True)