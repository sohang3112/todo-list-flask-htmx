from typing import Any, Mapping
from pprint import pprint
import sqlite3

from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

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
        CREATE TABLE IF NOT EXISTS todo_list(item, due_date)
    """)

@app.get('/')
def index():
    # Sqlite automatically provides column ROWID for every table
    # Source: https://stackoverflow.com/a/7906029/12947681
    todo_list = db_query("""
        SELECT ROWID, 
               IFNULL(item, "") AS item, 
               IFNULL(due_date, "") AS due_date
        FROM todo_list
    """)
    return render_template('index.html', todo_list=todo_list)

@app.get('/row/new')
def new_row():
    inserted_row_id = db_query("""
        INSERT INTO todo_list(item, due_date) VALUES 
            (NULL, NULL)   
    """)
    return render_template('new_row.html', rowid=inserted_row_id)

if __name__ == '__main__':
    mk_db_table()
    app.run(debug=True)