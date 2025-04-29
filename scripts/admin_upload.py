import sqlite3
import csv

# Function to create database tables for storing MCQs
def create_mcq_table():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS mcqs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            option_1 TEXT NOT NULL,
            option_2 TEXT NOT NULL,
            option_3 TEXT NOT NULL,
            option_4 TEXT NOT NULL,
            answer TEXT NOT NULL,
            topic TEXT NOT NULL,
            bloom_level TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Function to add MCQs from CSV to the database
def add_mcqs_from_csv(csv_file):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            question = row['question']
            option_1 = row['option_1']
            option_2 = row['option_2']
            option_3 = row['option_3']
            option_4 = row['option_4']
            answer = row['answer']
            topic = row['topic']
            c.execute('''
                INSERT INTO mcqs (question, option_1, option_2, option_3, option_4, answer, topic)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (question, option_1, option_2, option_3, option_4, answer, topic))
    
    conn.commit()
    conn.close()
    print("MCQs added from CSV.")

if __name__ == "__main__":
    create_mcq_table()
    # Provide path to the CSV file
    add_mcqs_from_csv('data/admin_mcqs.csv')
