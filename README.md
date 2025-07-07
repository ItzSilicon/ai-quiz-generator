# AI Quiz Generator
<img width="600" alt="Snipaste_2025-07-07_16-13-32" src="https://github.com/user-attachments/assets/7990dc88-fc13-45cd-9a96-3eff6267adfe" />
<img width="451" alt="Snipaste_2025-07-07_16-14-14" src="https://github.com/user-attachments/assets/fec54014-71c0-486d-9a9b-11dce6de39d8" />

A Python-based application for generating and taking quizzes using AI, featuring a modern Tkinter GUI.

## Features

- Generate quiz questions from PDF or text using the Google Gemini API.
- Save and load quizzes in JSON format.
- User-friendly GUI for selecting, answering, and reviewing quizzes.
- Supports multiple quiz files and summary export.
- High-DPI display support.

## Requirements

- Windows 10/11
- [Google Gemini API key](https://ai.google.dev/api)

## Installation

1. **Download the Release:**
   - Download `generator_main.exe` and `quiz_gui.exe` from the [Releases](https://github.com/ItzSilicon/ai-quiz-generator/releases) page.
   - Place both `.exe` files in the same folder.

2. **Get your Google Gemini API key:**
   - Visit [https://ai.google.dev/api](https://ai.google.dev/api) and follow the instructions.
   - Save your API key in a file named `apikey.txt` in the same folder as the `.exe` files.

## Usage

### 1. Generate a Quiz

- Double-click `generator_main.exe` to start the quiz generator.
- If this is your first time running the program, make sure `apikey.txt` with your Google Gemini API key is present in the same folder. If not, you will be prompted to enter your API key, which will be saved for future use.
- Follow the on-screen prompts:
  1. **Quiz Name:** Enter a name for your quiz.
  2. **Resource Selection:** Choose whether to use a PDF file or input text as your quiz source.
  3. **Input Content:** Provide the path to your PDF or text file.
  4. **Prompt:** You will be asked to enter a prompt instructions for the AI.
- Review the quiz details shown in the console. Confirm by typing `yes` to proceed, or any other input to cancel and start over.
- The application will generate quiz questions using the Google Gemini API and save the quiz as a `.json` file in the `Quiz` folder.
- After completion, you can choose to generate another quiz or exit the program.

### 2. Take a Quiz

- Double-click `quiz_gui.exe`.
- Select a quiz file from the dropdown menu.
- Click "Start" to begin.
- Answer questions, navigate with Previous/Next, and finish to see your results and a detailed summary.

### 3. Quiz Summaries

- After finishing a quiz, a summary will be displayed and saved in the `Quiz_Summaries` folder.

## Project Structure

```
AI Quiz Generator/
├── generator_main.exe
├── quiz_gui.exe
├── Quiz/
│   └── (your .json quiz files)
├── Quiz_Summaries/
│   └── (auto-saved summaries)
├── apikey.txt
└── README.md
```

## Notes

- Make sure your quiz files are in the `Quiz` directory.
- The project supports high-DPI screens and multiple languages.
- For best results, use clear and concise source material when generating quizzes.

## License

MIT License

---

**Enjoy your AI-powered quiz experience!**
