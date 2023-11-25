class Question:
    def __init__(self, question, answer):
        """
        Represents a single question in the quiz.

        Parameters:
        - question (str): The text of the question.
        - answer (str): The correct answer to the question.
        """
        self.question = question
        self.answer = answer


class Quiz:
    def __init__(self, questions=None):
        """
        Represents a quiz containing a collection of questions.

        Parameters:
        - questions (dict): A dictionary of questions where the keys are question numbers and the values are Question objects.
        """
        self.questions = questions or {}
        self.count = 1

    def add_question(self):
        """
        Allows the user to add questions to the quiz interactively.
        """
        self.count = len(self.questions) + 1
        while True:
            question = input("Enter a question to add to the quiz (Enter \"done\" if done): ")
            if question.lower() == "done":
                break
            answer = input("Enter the answer to the question: ")
            self.questions[self.count] = [question, answer]
            self.count += 1

    def delete_question(self):
        """
        Allows the user to delete a question from the quiz based on the question number.
        """
        question_num = input("Enter the question number of the question you'd like to delete from the quiz: ")

        try:
            del self.questions[int(question_num)]
        except KeyError:
            print("Invalid question number. Please enter a valid question number.")
            return
        self.count = max(self.questions.keys(), default=0)

        print("Question deleted successfully.")

    def view_questions(self):
        """
        Displays the existing questions in the quiz.
        """
        if not self.questions:
            print("No questions available.")
        else:
            print("Existing Questions:")
            for i in self.questions:
                print(f"({i}.) {self.questions[i][0]}")

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
        for i in self.questions:
            print(f"({i}.) {self.questions[i][0]}")
            user_answer = input("Enter answer: ")
            if user_answer.lower() == self.questions.get(i)[1].lower():
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
