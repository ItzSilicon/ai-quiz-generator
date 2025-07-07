# AI Quiz Generator

A Python project for generating and taking quizzes using AI and a modern Tkinter GUI.

## Features

- Generate quiz questions from PDF or text using Google Gemini API.
- Save and load quizzes in JSON format.
- User-friendly GUI for selecting, answering, and reviewing quizzes.
- Supports multiple quiz files and summary export.
- High-DPI support.

## Requirements

- Python 3.10+
- [google-generativeai](https://pypi.org/project/google-generativeai/)
- tkinter (usually included with Python)
- A Google Gemini API key ([get one here](https://ai.google.dev/api))

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/ai-quiz-generator.git
    cd ai-quiz-generator
    ```

2. **Install dependencies:**
    ```bash
    pip install google-generativeai
    ```

3. **Get your Google Gemini API key:**
    - Visit [https://ai.google.dev/api](https://ai.google.dev/api) and follow the instructions.
    - Save your API key in a file named `apikey.txt` in the project root.

## Usage

### 1. Generate a Quiz

Run the generator script to create a quiz from a PDF or text:

```bash
python generator_main.py
```

- Follow the prompts to enter quiz name, select resource, and set quiz parameters.
- The generated quiz will be saved as a `.json` file in the `./Quizes` directory.

### 2. Take a Quiz

Run the GUI quiz app:

```bash
python quiz_gui.py
```

- Select a quiz file from the dropdown.
- Click "Start" to start.
- Answer questions, navigate with Previous/Next, and finish to see your results and a detailed summary.

### 3. Quiz Summaries

- After finishing a quiz, a summary will be shown and saved in the `Quiz_Summaries` folder.

## Project Structure

```
AI Quiz Generator/
├── generator_main.py
├── generator.py
├── quiz_gui.py
├── Quizes/
│   └── (your .json quiz files)
├── Quiz_Summaries/
│   └── (auto-saved summaries)
├── apikey.txt
└── README.md
```

## Notes

- Make sure your quiz files are in the `./Quizes` directory.
- The project supports high-DPI screens and multiple languages.
- For best results, use clear and concise source material when generating quizzes.

## License

MIT License

---

**Enjoy your AI-powered quiz experience!**