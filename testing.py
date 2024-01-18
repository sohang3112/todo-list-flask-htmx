from typing import Any
from pprint import pprint
import sqlite3

import pandas as pd

import app

def row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
    return dict(zip(row.keys(), row))

# app.db_query("""
#     INSERT INTO todo_list(item, due_date) VALUES
#             ('dummy-1', "20-01-2024"),
#             ('dummy-2', "21-01-2024")    
# """)

# with app.db_connection() as conn:
#     df = pd.read_sql("SELECT * FROM todo_list", conn)
# print(df)

ans_rows = app.db_query("""
    SELECT ROWID, 
           IFNULL(item, "") AS item, 
           IFNULL(due_date, "") AS due_date
    FROM todo_list
""")
pprint([row_to_dict(row) for row in ans_rows])

# conn = app.db_connection()
# cursor = conn.cursor()
# cursor.execute("""
#     INSERT INTO todo_list(item, due_date) VALUES 
#         (NULL, NULL)   
# """)