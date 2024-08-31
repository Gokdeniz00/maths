import sqlite3
import pandas as pd

conn = sqlite3.connection('words.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS words (
            word TEXT PRIMARY KEY,
            spam_count INTEGER DEFAULT 0,
            spam_probability DOUBLE,
            ham_count INTEGER DEFAULT 0,
            ham_probability DOUBLE
)''')

def read_emails
conn.close()