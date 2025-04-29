import sqlite3
import random

# Function to track student's progress and update question difficulty
def track_student_answer(student_id, mcq_id, answer_provided, correct, bloom_level, topic):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO student_progress (student_id, mcq_id, answer_provided, correct, bloom_level, topic)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (student_id, mcq_id, answer_provided, correct, bloom_level, topic))
    conn.commit()
    conn.close()

# Function to dynamically select the next question based on student's progress
def select_next_question(student_id, num_questions=1):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # Get all questions answered by the student
    c.execute('SELECT mcq_id, correct FROM student_progress WHERE student_id = ?', (student_id,))
    student_answers = c.fetchall()

    # Track student's correct/incorrect answers to determine weak areas
    incorrect_answers = [mcq_id for mcq_id, correct in student_answers if not correct]
    
    # If the student has incorrect answers, try to target those topics/Bloom levels
    if incorrect_answers:
        # Get the MCQs related to the incorrect questions
        c.execute('''
            SELECT mcq_id, question, bloom_level, topic FROM mcqs WHERE id IN (?)
        ''', (",".join(map(str, incorrect_answers)),))
        weak_mcqs = c.fetchall()
        selected_mcqs = weak_mcqs
    else:
        # No incorrect answers, choose randomly or based on Bloom level preference
        c.execute('SELECT question, bloom_level, topic FROM mcqs')
        all_mcqs = c.fetchall()
        selected_mcqs = random.sample(all_mcqs, num_questions)
    
    conn.close()
    return selected_mcqs

# Function to generate and assess the next question
def generate_and_assess_next_question(student_id, num_questions=1):
    questions = select_next_question(student_id, num_questions)
    for question in questions:
        mcq_id, question_text, bloom_level, topic = question
        print(f"Question: {question_text} (Bloom Level: {bloom_level}, Topic: {topic})")
        
        # Assuming we get student's answer (from a real UI, for example)
        student_answer = input("Your answer: ")
        
        # Check if the student's answer is correct
        correct_answer = get_correct_answer(mcq_id)
        correct = student_answer.strip().lower() == correct_answer.strip().lower()
        
        # Track student's answer
        track_student_answer(student_id, mcq_id, student_answer, correct, bloom_level, topic)
        
        if correct:
            print("Correct!")
        else:
            print(f"Incorrect. Correct answer: {correct_answer}")
    
def get_correct_answer(mcq_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT answer FROM mcqs WHERE id = ?', (mcq_id,))
    answer = c.fetchone()[0]
    conn.close()
    return answer

# Example: Start quiz for student with ID 1
if __name__ == "__main__":
    student_id = 1
    generate_and_assess_next_question(student_id, num_questions=3)
