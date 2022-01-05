import time
from tkinter import *
from PIL import ImageTk, Image
from tkPDFViewer import tkPDFViewer as pdf
import os


class Question:

    def __init__(self, question, answer_yes, answer_no, end=False):
        self.question = question
        self.answer_yes = answer_yes
        self.answer_no = answer_no
        self.end = end


class SolutionPDF:

    def __init__(self, pdf_location, plant):
        self.pdf_location = pdf_location
        self.plant = plant


class App(Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.attributes("-fullscreen", True)
        self.title("Planten vragen")
        # Determineer tabel
        # Questions
        self.questions = [
            Question("Is uw plant een boom of een heester?", "Is het een aarde plant?", "Is het een waterplant?"),
            Question("Is het een waterplant?", "Dan is het plant 1.", "Dan is het plant 2.", True),
            Question("Is het een aarde plant?", "Dan is het plant 3.", "Dan is het plant 4.", True)
        ]
        # PDFs
        self.solutions = [
            SolutionPDF("/pdfs/waterplant.pdf", "Dan is het plant 1.")
        ]
        self.showing = ""
        # Font
        self.font = ("Times bold", 14)
        # Visual elements
        self.question_label = Label(self, text="", font=self.font)
        self.question_yes_button = Button(self, text="Ja", height=5, width=15)
        self.question_no_button = Button(self, text="Nee", height=5, width=15)
        self.determineer_button = Button(self, text="Determineertabel", height=5, width=15)
        self.exit_button = Button(self, text="Exit", height=5, width=15)
        self.home_button = Button(self, text="Home", height=5, width=15)

    def show_menu(self):
        # Toon het hoofdmenu
        self.determineer_button.grid(row=1, column=0, padx=10, pady=10)
        self.exit_button.grid(row=0, column=0, padx=10, pady=10)
        self.showing = "menu"

    def hide_menu(self):
        App.hide_element(self.determineer_button)
        App.hide_element(self.exit_button)

    def show_questions(self):
        self.home_button.grid(row=0, column=1, padx=10, pady=10)
        self.question_label.grid(row=1, column=1, padx=10, pady=10)
        self.question_yes_button.grid(row=2, column=0, padx=10, pady=10)
        self.question_no_button.grid(row=2, column=2, padx=10, pady=10)
        # Set text to first question.
        self.question_label["text"] = self.questions[0].question
        # Set showing
        self.showing = "questions"

    def hide_questions(self):
        App.hide_element(self.home_button)
        App.hide_element(self.question_label)
        App.hide_element(self.question_yes_button)
        App.hide_element(self.question_no_button)

    def hide_other(self):
        # Hide all other elements
        if self.showing == "":
            pass
        elif self.showing == "menu":
            # Hide the menu
            self.hide_menu()
        elif self.showing == "questions":
            self.hide_questions()

    def clicked_yes_or_no(self, option):
        # You clicked yes or no.
        # Show the next question
        current_question = [question for question in self.questions if question.question == self.question_label["text"]][0]
        if current_question.end:
            # This is an ending question
            # Just show the answer and show the corresponding pdf.
            self.question_label["text"] = current_question.answer_yes if option == "yes" else current_question.answer_no
            # Hide the yes or no buttons since we don't need those anymore. It was the last question
            App.hide_element(self.question_yes_button)
            App.hide_element(self.question_no_button)
        else:
            # This a question with a follow up.
            # Show the question depending on yes or no
            self.question_label["text"] = current_question.answer_yes if option == "yes" else current_question.answer_no

    def clicked_button(self, name):
        print(f"Clicked the {name} button.")
        if name == "yes":
            self.clicked_yes_or_no("yes")
        elif name == "no":
            self.clicked_yes_or_no("no")
        elif name == "home":
            self.hide_other()
            self.show_menu()
        elif name == "exit":
            exit(0)
        elif name == "determineertabel":
            self.hide_other()
            self.show_questions()
        elif name == "other":
            pass

    def register_button_callbacks(self):
        self.question_yes_button["command"] = lambda: self.clicked_button("yes")
        self.question_no_button["command"] = lambda: self.clicked_button("no")
        self.determineer_button["command"] = lambda: self.clicked_button("determineertabel")
        self.exit_button["command"] = lambda: self.clicked_button("exit")
        self.home_button["command"] = lambda: self.clicked_button("home")

    @staticmethod
    def show_element(e):
        e.grid()

    @staticmethod
    def hide_element(e):
        e.grid_forget()

    def set_size(self, size):
        self.geometry(f"{size[0]}x{size[1]}")


if __name__ == "__main__":
    app = App()
    app.register_button_callbacks()
    app.show_menu()
    app.set_size((750, 500))
    mainloop()
