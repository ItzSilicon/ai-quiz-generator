from google import genai
from google.genai import types
import tkinter as tk
import pathlib
from tkinter.filedialog import askopenfilename
from pydantic import BaseModel

class Question(BaseModel):
    question: str
    Choices: list[str]
    answer: str

difficulty_levels = {
    "1": "stupid",
    "2": "easy",
    "3": "medium",
    "4": "hard",
    "5": "insane"
}
###Input###
def get_info():
    quiz_name = input("Enter the name of the quiz: \n(If name is repeated, it will be overwritten)\n")
    if not quiz_name:
        print("No name entered. Do you want to cancel? (y/n)")
        if input().lower() == 'y':
            exit()
        else:
            return get_info()
    print("Which resource do you want to use to generate questions?")
    print("1. PDF file")
    print("2. Pure text")
    print("3. Cancel")
    resource= input("Enter the number corresponding to your choice: ")
    if resource == "3":
        print("Cancelled.")
        exit()
    elif resource == "1":
        tk.Tk().withdraw() # part of the import if you are not using other tkinter functions
        filepath=None
        while not filepath:
            filepath = askopenfilename(filetypes=[("Text files","*.pdf")],title="Select a file you want to use.")
            if not filepath:
                print("No file selected. Do you want to cancel? (y/n)")
                if input().lower() == 'y':
                    exit()
                else:
                    continue
        input_content = filepath
    elif resource == "2":
        text = None
        while not text:
            text = input("Enter the text:")
            if not text:
                print("No text entered. Do you want to cancel? (y/n)")
                if input().lower() == 'y':
                    exit()
                else:
                    continue
        input_content = text
    question_amount = 0
    while question_amount <= 0:
        question_amount = int(input("How many questions do you want to ask? \n(Too many questions may cause the program to crash, so be careful!)\n"))
        if question_amount <= 0:
            print("Invalid number of questions. Do you want to cancel? (y/n)")
            if input().lower() == 'y':
                exit()
            else:
                continue
    difficulty=""
    while difficulty not in difficulty_levels:
        print("Select a difficulty level:")
        for key, value in difficulty_levels.items():
            print(f"{key}: {value}")
        difficulty = input("Enter the number corresponding to your choice: ")
        if difficulty not in difficulty_levels:
            print("Invalid choice. Do you want to cancel? (y/n)")
            if input().lower() == 'y':
                exit()
            else:
                continue
        language = input("Enter the language you want to use (e.g. English, Chinese(Traditional)): ")
        if not language:
            print("No language selected. Do you want to cancel? (y/n)")
            if input().lower() == 'y':
                exit()
            else:
                continue
        prompt = f"""
        Request: Generate {question_amount} quiz questions based on the following content.
        Content: {input_content}
        Please provide the questions in the following format:
        Question: <question text> 
        Choices: <list of choices> (4 choices, A, B, C, D)
        Answer: <correct answer> (Only one correct answer is allowed, stored as a single letter, e.g. A, B, C, D)
        The questions should be in {language} and the difficulty level is {difficulty_levels[difficulty]}.
        the questions should be clear and concise, suitable for a quiz.
        """
    return quiz_name,resource,input_content,prompt

    
###Handler###
def generate_questions(api_key, name, resource, input_content, prompt):
    client = genai.Client(api_key=api_key)
    filepath_lib = pathlib.Path(input_content)
    print(f"Generating questions for {filepath_lib.name}...")
    if resource == "1":
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Part.from_bytes(
                    data=filepath_lib.read_bytes(),
                    mime_type='application/pdf',
                ),
                prompt],
            config = {
                "response_mime_type": "application/json",
                "response_schema":list[Question]
            }
        )
    elif resource == "2":
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                prompt+"\nContent:\n"+input_content],
            config = {
                "response_mime_type": "application/json",
                "response_schema":list[Question]
            }
        )
    print("Questions generated successfully!")
    with open(f"./Quizes/{name}.json", "w",encoding="UTF-8") as f:
        f.write(response.text)