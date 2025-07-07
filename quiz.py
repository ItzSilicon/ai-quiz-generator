import json
import random
quiz_file = "test.json"
with open(quiz_file, "r", encoding="UTF-8") as f:
    quiz_data = json.load(f)

correct_answers = 0
total_questions = len(quiz_data)
question_number = 1
# Shuffle the questions to randomize the quiz order
random.shuffle(quiz_data)
for question in quiz_data:
    print(f"\nQuestion {question_number}/{total_questions}:")
    print(f"Q: {question['question']}")
    for option in question['Choices']:
        print(option)
    reply = input("Your answer: (A/B/C/D) :")
    if reply.upper() == question['answer']:
        print("Correct!")
        correct_answers += 1
    else:
        print(f"Wrong! The correct answer is {question['answer']}")
    question_number += 1