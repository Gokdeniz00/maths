import sqlite3
import pandas as pd
import  re
from typing import List
import tkinter as tk

#main training function that reads emails and collects word data
def train():
    conn = sqlite3.Connection('maths\\bayesian-analysis\\data\\words.db')
    cur=create_cursor(conn)
    create_words_table(cur)
    init_info_table()
    data=load_data()
    print(data.head())


#creates an sqlite3 database cursor
def create_cursor(conn: sqlite3.Connection)->sqlite3.Connection.cursor:
    cur=conn.cursor()
    return cur


#creates the words table that will store words and associated data
def create_words_table(cur: sqlite3.Connection.cursor):
    cur.execute('''CREATE TABLE IF NOT EXISTS words (
            word TEXT PRIMARY KEY,
            spam_count INTEGER DEFAULT 0,
            spam_probability DOUBLE,
            ham_count INTEGER DEFAULT 0,
            ham_probability DOUBLE
)''')
    

def init_info_table(cur: sqlite3.Connection.cursor):
    cur.execute('''CREATE TABLE IF NOT EXISTS info(
                data_label TEXT PRIMARY KEY,
                data INTEGER DEFAULT 0 )''')    
    cur.execute('INSERT INTO info (data_label,data) VALUES(?,0)',("spammails"))
    cur.execute('INSERT INTO info (data_label,data) VALUES(?,0)',("hammails"))


#reads email data from emails.csv file with pandas
def load_data()->pd.DataFrame:
    file_path='maths\\bayesian-analysis\\data\\emails.csv'
    data= pd.read_csv(file_path)
    return data


def process_emails(cur:sqlite3.Connection.cursor,data:pd.DataFrame):
    for index,row in data.iterrows():
        process_email(cur,row)

def update_info_table(cur:sqlite3.Connection.cursor,row:pd.Series):
    if row[1]:
        cur.execute('UPDATE info SET data=data+1 WHERE data_label=?',('spammails'))
    else:
        cur.execute('UPDATE info SET data=data+1 WHERE data_label=?',('hammails'))

def process_email(cur:sqlite3.Connection.cursor,row:pd.Series):
    words=tokenize_email(row)
    is_spam=bool(row["spam"])
    process_words(cur,words,is_spam)


def tokenize_email(row:pd.Series)->List[str]:
    words=re.findall(r'\b\w+\b',row["text"].lower())
    return words


def process_words(cur:sqlite3.Connection.cursor,words:List[str],is_spam:bool):
    for word in words:
        update_word(cur,word,is_spam)


def update_word(cur:sqlite3.Connection.cursor,word:str,is_spam:bool):
        result=check_word(cur,word)
        if result:
            if is_spam:
                cur.execute('UPDATE words SET spam_count=spam_count+1 WHERE word=?',(word))
            else:
                cur.execute('UPDATE words SET ham_count=ham_count+1 WHERE word=?',(word))
        else:
            if is_spam:
                cur.execute('INSERT INTO words VALUES(?,1,0,0,0)',(word))
            else:
                cur.execute('INSERT INTO words VALUES(?,0,0,1,0)',(word))

#checks if the word is present in the database
def check_word(cur:sqlite3.Connection.cursor, word:str)->bool:
    cur.execute('''SELECT * FROM words WHERE word = ?''',(word,))
    result = cur.fetchone()
    return result


def update_probability(cur:sqlite3.Connection.cursor):   
    cur.execute("SELECT * FROM words")
    words = cur.fetchall()
    for word in words:
        (spam_probability,ham_probability)=calculate_probability(cur,word)
        cur.execute("UPDATE words SET spam_probability=?,ham_probability=?",(spam_probability,ham_probability))
def calculate_probability(cur:sqlite3.Connection.cursor,word:tuple)->tuple:
    spam_probability=(word[2]+2)/get_spam_count()
    ham_probability=(word[3]+2)/get_ham_count()
    return (spam_probability,ham_probability)
    
def get_spam_count(cur:sqlite3.Connection.cursor)->int:
    cur.execute("SELECT * FROM info WHERE data_label=?",('spammails'))
    spam_data=cur.fetchone()
    return spam_data[1]

def get_ham_count(cur:sqlite3.Connection.cursor)->int:
    cur.execute("SELECT * FROM info WHERE data_label=?",('hammails'))
    ham_data=cur.fetchone()
    return ham_data[1]

#part two gui

def gui():
    window =tk.Tk()
    title=tk.Label(text="Spam! detector:")
    input = tk.Text()
    button=tk.Button(text="Detect",command=detect(input.get()))
    title.pack()
    input.pack()
    button.pack()
    window.mainloop()
def detect(email:str):

gui()

