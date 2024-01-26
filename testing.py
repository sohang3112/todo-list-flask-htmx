from typing import Any
from pprint import pprint
import sqlite3

import pandas as pd
import requests

import app

def row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
    return dict(zip(row.keys(), row))

# app.mk_db_table()
# app.db_query("""
#     INSERT INTO todo_list(item, due_date) VALUES
#             ('dummy-1', "20-01-2024"),
#             ('dummy-2', "21-01-2024")    
# """)

# app.db_query("DROP TABLE todo_list")

response = requests.post('http://127.0.0.1:5000/row/new')
print(response)
print(response.text)
