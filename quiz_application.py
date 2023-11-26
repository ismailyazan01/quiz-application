from collections import deque

class Question:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

class Quiz:
    def __init__(self, questions=None):
        self.questions = deque(questions) if questions else deque()
        self.count = 1

    def add_question(self):
        self.count = len(self.questions) + 1
        while True:
            question_text = input("Enter a question to add to the quiz (Enter \"done\" if done): ")
            if question_text.lower() == "done":
                break
            answer = input("Enter the answer to the question: ")
            question = Question(f"({self.count}.) {question_text}", answer)
            self.questions.append(question)
            self.count += 1

    def delete_question(self, question_num=None):
        """
        Deletes a question from the quiz based on the question number.

        Parameters:
        - question_num (int): The question number to delete.
        """
        if not self.questions:
            print("No questions available for deletion.")
            return

        if question_num is None:
            try:
                question_num = int(input("Enter the question number you'd like to delete: "))
            except ValueError:
                print("Invalid input. Please enter a valid question number.")
                return

        if 1 <= question_num <= len(self.questions):
            deleted_question = self.questions[question_num - 1]
            self.questions.remove(deleted_question)
            print(f"Question {question_num} deleted successfully.")
        else:
            print("Invalid question number. Please enter a valid question number.")
            return

        # Update question numbers
        for i, question in enumerate(self.questions, start=1):
            question.question = f"({i}.) {question.question.split(' ', 1)[1]}"

        self.count = len(self.questions) + 1

    def view_questions(self):
        if not self.questions:
            print("No questions available.")
        else:
            print("Existing Questions:")
            for question in self.questions:
                print(question.question)

    def get_results(self, correct_num, question_num):
        """
        Calculates the percentage of correct answers.

        Parameters:
        - correct_num (int): Number of correctly answered questions.
        - question_num (int): Total number of questions.

        Returns:
        - float: Percentage of correct answers.
        """
        return (correct_num / question_num) * 100

    def quiz_session(self):
        """
        Conducts the quiz session, allowing the user to answer questions and displays the results.
        """
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

    def run_quiz(self):
        """
        Initiates the quiz, allowing the user to add questions, delete questions, view questions, start the quiz, or
        quit the application.
        """
        while True:
            try:
                menu_choice = int(input("Would you like to add more questions (Enter 1), delete questions (Enter 2), "
                                        "view questions (Enter 3), start the quiz (Enter 4), or quit the application "
                                        "(Enter 5)? "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue

            if menu_choice == 1:
                self.add_question()
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
                exit()
            else:
                print("Invalid Input")


quiz_instance = Quiz()
quiz_instance.run_quiz()
