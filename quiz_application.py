import mysql.connector
from collections import deque
import os
from dotenv import load_dotenv

load_dotenv()

class Question:
    def __init__(self, question_id, question, answer):
        self.question_id = question_id
        self.question = question
        self.answer = answer

class Quiz:
    def __init__(self):
        self.db_connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database="quiz_db"
        )

        self.cursor = self.db_connection.cursor()

        self.questions = self.fetch_questions()
        self.count = len(self.questions) + 1

    def fetch_questions(self):
        self.cursor.execute("SELECT * FROM questions")
        rows = self.cursor.fetchall()
        questions = [Question(row[0], row[1], row[2]) for row in rows]
        return deque(questions)

    def add_question(self, question_text, answer):
        insert_query = "INSERT INTO questions (question_text, answer) VALUES (%s, %s)"
        data = (question_text, answer)
        self.cursor.execute(insert_query, data)
        self.db_connection.commit()
        self.update_ids_and_reset_counter()
        self.questions = self.fetch_questions()
        self.count = len(self.questions) + 1

    def delete_question(self):
        self.view_questions()
        try:
            question_num = int(input("Enter the question number you'd like to delete: "))
            if 1 <= question_num <= len(self.questions):
                self.delete_question_from_db(question_num)
                self.update_ids_and_reset_counter()
                self.questions = self.fetch_questions()
                self.count = len(self.questions) + 1
                print(f"Question {question_num} deleted successfully.")
            else:
                print("Invalid question number. Please enter a valid question number.")
        except ValueError:
            print("Invalid input. Please enter a valid question number.")

    def delete_question_from_db(self, question_num):
        delete_query = "DELETE FROM questions WHERE id = %s"
        data = (question_num,)
        self.cursor.execute(delete_query, data)
        self.db_connection.commit()

    def update_ids_and_reset_counter(self):
        self.reset_auto_increment_counter()
        self.update_existing_ids()

    def reset_auto_increment_counter(self):
        self.cursor.execute("ALTER TABLE questions AUTO_INCREMENT = 1;")
        self.db_connection.commit()

    def update_existing_ids(self):
        set_new_id_query = "SET @new_id := 0;"
        update_id_query = "UPDATE questions SET id = @new_id := @new_id + 1;"
        self.cursor.execute(set_new_id_query)
        self.cursor.execute(update_id_query)
        self.db_connection.commit()

    def view_questions(self):
        if not self.questions:
            print("No questions available.")
        else:
            print("Existing Questions:")
            for index, question in enumerate(self.questions, start=1):
                print(f"({index}.) {question.question}")
            print("-" * 35)

    def get_results(self, correct_num, question_num):
        return (correct_num / question_num) * 100

    def quiz_session(self):
        correct_num = 0
        num_of_questions = 0
        for i, question in enumerate(self.questions, start=1):
            print(question.question)
            user_answer = input("Enter answer: ")
            if user_answer.lower() == question.answer.lower():
                correct_num += 1
            num_of_questions += 1
        score = self.get_results(correct_num, num_of_questions)
        print(f"You got {score:.2f}%!")

        if score > 75:
            print("Congratulations!")
        else:
            print("You can do better next time!")

    def clear_all_questions(self):
        confirmation = input("Are you sure you want to clear all questions? (yes/no): ").lower()
        if confirmation == "yes":
            self.cursor.execute("TRUNCATE TABLE questions;")
            self.db_connection.commit()
            print("All questions cleared successfully.")
            self.update_ids_and_reset_counter()
            self.questions = self.fetch_questions()
            self.count = len(self.questions) + 1
        else:
            print("Operation canceled.")

    def run_quiz(self):
        while True:
            try:
                menu_choice = int(input("1. Add a question\n"
                                        "2. Delete a question\n"
                                        "3. View questions\n"
                                        "4. Take a quiz\n"
                                        "5. Clear all questions\n"
                                        "6. Exit\n"))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue

            if menu_choice == 1:
                question_text = input("Enter a question to add to the quiz: ")
                answer = input("Enter the answer to the question: ")
                self.add_question(question_text, answer)
            elif menu_choice == 2:
                if not self.questions:
                    print("Error: Cannot delete questions without any questions. Please add questions first.")
                else:
                    self.delete_question()
                continue
            elif menu_choice == 3:
                self.view_questions()
            elif menu_choice == 4:
                if not self.questions:
                    print("Error: Cannot start the quiz without any questions. Please add questions first.")
                else:
                    self.quiz_session()
                    break
            elif menu_choice == 5:
                self.clear_all_questions()
            elif menu_choice == 6:
                exit()
            else:
                print("Invalid Input")

    def close_connection(self):
        self.db_connection.close()


# Instantiate the Quiz class
quiz_instance = Quiz()

# Run the quiz
quiz_instance.run_quiz()

# Close the database connection when done
quiz_instance.close_connection()
