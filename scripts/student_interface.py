import sqlite3
from models.quiz_selector import select_next_question, track_student_answer

# Function to fetch the next question based on student progress using quiz_selector
def get_next_question(student_id):
    questions = select_next_question(student_id, num_questions=1)
    if questions:
        question = questions[0]
        mcq_id, question_text, bloom_level, topic = question
        return mcq_id, question_text, bloom_level, topic
    else:
        return None

# Function to display a question to the student and get their answer
def display_question(mcq_id, question_text):
    print(f"Question: {question_text}")
    student_answer = input("Please enter your answer: ")
    return student_answer

# Function to check if the student's answer is correct
def check_answer(mcq_id, student_answer):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT answer FROM mcqs WHERE id = ?', (mcq_id,))
    correct_answer = c.fetchone()[0]
    conn.close()
    
    # Return True if the answer is correct, otherwise False
    return student_answer.strip().lower() == correct_answer.strip().lower()

# Function to track student's progress (store answers) using quiz_selector
def track_progress(student_id, mcq_id, answer_provided, correct, bloom_level, topic):
    track_student_answer(student_id, mcq_id, answer_provided, correct, bloom_level, topic)

# Main function to run the student quiz
def start_quiz(student_id):
    i = 0
    while i < 100:
        next_question = get_next_question(student_id)
        if not next_question:
            print("No more questions available.")
            break
        mcq_id, question_text, bloom_level, topic = next_question
        
        # Display question and get student's answer
        student_answer = display_question(mcq_id, question_text)
        
        # Check if the answer is correct
        correct = check_answer(mcq_id, student_answer)
        
        # Track student's progress
        track_progress(student_id, mcq_id, student_answer, correct, bloom_level, topic)
        
        i += 1

if __name__ == "__main__":
    student_id = 1 
    start_quiz(student_id)
