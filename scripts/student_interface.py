import sqlite3
import random

# Function to fetch the next question based on student progress
def get_next_question(student_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # Fetch all MCQs answered by the student
    c.execute('SELECT mcq_id, correct FROM student_progress WHERE student_id = ?', (student_id,))
    student_answers = c.fetchall()

    # Identify weak areas (incorrect answers)
    incorrect_answers = [mcq_id for mcq_id, correct in student_answers if not correct]

    # Select next question based on weak areas or random if no incorrect answers
    if incorrect_answers:
        # Fetch questions related to the incorrect answers
        c.execute('''
            SELECT mcq_id, question, option_1, option_2, option_3, option_4 FROM mcqs WHERE id IN (?)
        ''', (",".join(map(str, incorrect_answers)),))
        next_question = random.choice(c.fetchall())
    else:
        # If no incorrect answers, pick a random question
        c.execute('SELECT mcq_id, question, option_1, option_2, option_3, option_4 FROM mcqs')
        next_question = random.choice(c.fetchall())
    
    conn.close()
    return next_question

# Function to display a question to the student and get their answer
def display_question(question_data):
    mcq_id, question, option_1, option_2, option_3, option_4 = question_data
    
    print(f"Question: {question}")
    print(f"1. {option_1}")
    print(f"2. {option_2}")
    print(f"3. {option_3}")
    print(f"4. {option_4}")
    
    student_answer = input("Please select an option (1-4): ")
    return int(student_answer)

# Function to check if the student's answer is correct
def check_answer(mcq_id, student_answer):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT answer FROM mcqs WHERE id = ?', (mcq_id,))
    correct_answer = c.fetchone()[0]
    conn.close()
    
    # Return True if the answer is correct, otherwise False
    if student_answer == correct_answer:
        return True
    return False

# Function to track student's progress (store answers)
def track_progress(student_id, mcq_id, answer_provided, correct):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO student_progress (student_id, mcq_id, answer_provided, correct)
        VALUES (?, ?, ?, ?)
    ''', (student_id, mcq_id, answer_provided, correct))
    conn.commit()
    conn.close()

# Main function to run the student quiz
def start_quiz(student_id):
    i=0
    while(i<100):
        next_question = get_next_question(student_id)
        mcq_id, question, option_1, option_2, option_3, option_4 = next_question
        
        # Display question and get student's answer
        student_answer = display_question(next_question)
        
        # Check if the answer is correct
        correct = check_answer(mcq_id, student_answer)
        
        # Track student's progress
        track_progress(student_id, mcq_id, student_answer, correct)
        


if __name__ == "__main__":
    student_id = 1 
    start_quiz(student_id)
