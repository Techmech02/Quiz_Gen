import sqlite3
import csv
# Function to upload MCQs from CSV (same as admin upload functionality)
def upload_mcqs_from_csv(csv_file):
    # Reusing the same function as before
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
    print("MCQs added successfully.")

# Function to view performance trends
def view_student_performance():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # Get performance data: number of correct/incorrect answers per student
    c.execute('''
        SELECT student_id, COUNT(CASE WHEN correct = 1 THEN 1 END) AS correct, 
               COUNT(CASE WHEN correct = 0 THEN 1 END) AS incorrect
        FROM student_progress
        GROUP BY student_id
    ''')
    performance_data = c.fetchall()
    
    for data in performance_data:
        student_id, correct, incorrect = data
        print(f"Student {student_id}: Correct Answers = {correct}, Incorrect Answers = {incorrect}")
    
    conn.close()

# Function to classify MCQs into Bloom Levels
def classify_bloom_levels():
    # Placeholder for the logic to classify Bloom levels using your pre-trained model
    pass

# Function to manage the admin panel interface
def admin_panel():
    while True:
        print("\nAdmin Panel")
        print("1. Upload MCQs from CSV")
        print("2. View Student Performance")
        print("3. Classify Bloom Levels for MCQs")
        print("4. Exit")
        
        choice = input("Enter choice: ")
        
        if choice == '1':
            csv_file = input("Enter CSV file path: ")
            upload_mcqs_from_csv(csv_file)
        elif choice == '2':
            view_student_performance()
        elif choice == '3':
            classify_bloom_levels()  # This should trigger Bloom level classification
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    admin_panel()
