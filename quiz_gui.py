import json
import random
import tkinter as tk
from tkinter import messagebox
from tkinter import font
import ctypes
import time
import os
from tkinter import ttk

# Set DPI awareness for high DPI displays
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

QUIZ_DIR = "./Quiz"

def get_quiz_files():
    return [f for f in os.listdir(QUIZ_DIR) if f.endswith(".json")]

def load_selected_quiz():
    global quiz_file, quiz_data, user_answers, current_question
    selected_file = quiz_select.get()
    if not selected_file:
        messagebox.showwarning("No file", "請選擇一個題庫檔案")
        return
    quiz_file = os.path.join(QUIZ_DIR, selected_file)
    with open(quiz_file, "r", encoding="UTF-8") as f:
        quiz_data = json.load(f)
    random.shuffle(quiz_data)
    current_question = 0
    user_answers = [None] * len(quiz_data)
    show_question()
    # 啟用按鈕
    for rb in option_buttons:
        rb.config(state=tk.NORMAL)
    prev_btn.config(state=tk.NORMAL)
    next_btn.config(state=tk.NORMAL)
    finish_btn.config(state=tk.NORMAL)
    # Freeze quiz selection after starting
    quiz_select.config(state="disabled")
    start_btn.config(state="disabled")


# --- Fancy Colors and Styles ---
BG_COLOR = "#f0f4fa"
FRAME_COLOR = "#ffffff"
ACCENT_COLOR = "#4f8cff"
BTN_COLOR = "#e3eefd"
BTN_HOVER = "#c7e0ff"
CORRECT_COLOR = "#b6e6bd"
WRONG_COLOR = "#f7b6b6"
FONT = ("Segoe UI", 16)
TITLE_FONT = ("Segoe UI", 20, "bold")
QUESTION_FONT = ("Segoe UI", 20, "bold")
OPTION_FONT = ("Segoe UI", 16)
OPTION_FONT_BOLD = ("Segoe UI", 16, "bold")  # Add this line
BTN_FONT = ("Segoe UI", 16, "bold")

CHOICE_COLORS = ["#b6e6bd", "#b6d6f7", "#f7e6b6", "#dab6f7"]  # A, B, C, D

def show_question():
    if not quiz_data:  # 如果 quiz_data 為空，則不顯示題目
        question_label.config(text="")
        return
    q = quiz_data[current_question]
    progress_label.config(text=f"Question {current_question+1} of {len(quiz_data)}")
    question_label.config(text=f"{q['question']}")
    for i, opt in enumerate(q['Choices']):
        option_vars[i].set(opt)
        option_buttons[i].config(bg=FRAME_COLOR)
    if user_answers[current_question]:
        selected.set(user_answers[current_question])
    else:
        selected.set(None)
    prev_btn.config(state=tk.NORMAL if current_question > 0 else tk.DISABLED)
    next_btn.config(state=tk.NORMAL if current_question < len(quiz_data)-1 else tk.DISABLED)
    update_option_colors()  # <-- Add this line

def record_answer(*args):
    answer = selected.get()
    if answer:
        user_answers[current_question] = answer

def next_question():
    global current_question
    record_answer()
    if current_question < len(quiz_data) - 1:
        current_question += 1
        show_question()

def prev_question():
    global current_question
    record_answer()
    if current_question > 0:
        current_question -= 1
        show_question()

def finish_quiz():
    record_answer()
    unanswered = user_answers.count(None)
    if unanswered > 0:
        if not messagebox.askyesno("Unanswered", f"You have {unanswered} unanswered questions. Finish anyway?"):
            return
    correct = 0
    summary = ""
    for idx, (q, user_ans) in enumerate(zip(quiz_data, user_answers)):
        is_correct = user_ans == q['answer']
        if is_correct:
            correct += 1
        options_text = ""
        for opt in q['Choices']:
            opt_letter = opt.split('.')[0].strip()  # "A", "B", etc.
            mark = ""
            if user_ans == opt_letter:
                mark = " ← Your choice"
            if q['answer'] == opt_letter:
                mark += " (Correct)"
            options_text += f"    {opt}{mark}\n"
        summary += (
            f"Q{idx+1}: {q['question']}\n"
            f"{options_text}"
            f"{'✔️ Correct' if is_correct else '❌ Wrong'}\n\n"
        )
    messagebox.showinfo("Quiz Finished", f"You got {correct} out of {len(quiz_data)} correct!")

    filename= f"quiz_summary_{int(time.time())}.txt"
    # Save summary to file
    with open(f"./Quiz_Summaries/{filename}", "w", encoding="utf-8") as f:
        f.write(f"Score: {correct} / {len(quiz_data)}\n\n")
        f.write(summary)

    # Show summary window
    result_window = tk.Toplevel(root)
    result_window.title("Quiz Summary")
    result_window.geometry("900x700")

    # Add a frame for text and scrollbar
    summary_frame = tk.Frame(result_window, bg=BG_COLOR)
    summary_frame.pack(expand=True, fill="both", padx=20, pady=20)

    scrollbar = tk.Scrollbar(summary_frame)
    scrollbar.pack(side="right", fill="y")

    text = tk.Text(
        summary_frame,
        wrap="word",
        font=OPTION_FONT,
        bg=BG_COLOR,
        yscrollcommand=scrollbar.set
    )
    text.insert("1.0", summary)
    text.config(state="normal")  # Enable editing for tagging

    # Tag and color correct options
    start = "1.0"
    while True:
        pos = text.search("(Correct)", start, stopindex="end")
        if not pos:
            break
        line_start = pos.split('.')[0] + ".0"
        line_end = pos.split('.')[0] + ".end"
        text.tag_add("correct", line_start, line_end)
        start = pos + "+1c"
    text.tag_config("correct", foreground="#228B22", font=OPTION_FONT_BOLD)  # Green and bold

    text.config(state="disabled")
    text.pack(side="left", expand=True, fill="both")

    scrollbar.config(command=text.yview)

    # Disable navigation and finish buttons after quiz is finished
    prev_btn.config(state=tk.DISABLED)
    next_btn.config(state=tk.DISABLED)
    finish_btn.config(state=tk.DISABLED)

    # Quit after closing the summary window
    def quit_app():
        root.destroy()
    result_window.protocol("WM_DELETE_WINDOW", quit_app)

def update_option_colors(*args):
    selected_value = selected.get()
    for i, rb in enumerate(option_buttons):
        if selected_value == chr(65+i):
            rb.config(bg=CHOICE_COLORS[i], font=OPTION_FONT_BOLD, fg=ACCENT_COLOR)  # Bold and colored text
        else:
            rb.config(bg=FRAME_COLOR, font=OPTION_FONT, fg="black")  # Normal

def on_enter(e):
    e.widget['background'] = BTN_HOVER

def on_leave(e):
    e.widget['background'] = BTN_COLOR

root = tk.Tk()
root.title("Quiz")
root.geometry("1200x800")
root.state('zoomed')
root.configure(bg=BG_COLOR)

# Title
title_label = tk.Label(root, text="Quiz", font=TITLE_FONT, bg=BG_COLOR, fg=ACCENT_COLOR)
title_label.pack(pady=(30, 10))

# Main frame for quiz content
main_frame = tk.Frame(root, bg=FRAME_COLOR, bd=2, relief="groove")
main_frame.pack(pady=20, padx=60, fill="both", expand=True)

progress_label = tk.Label(main_frame, text="", font=FONT, bg=FRAME_COLOR, fg=ACCENT_COLOR)
progress_label.pack(pady=(20, 0))

question_label = tk.Label(main_frame, text="", wraplength=1400, font=QUESTION_FONT, bg=FRAME_COLOR)
question_label.pack(pady=24)

selected = tk.StringVar()
selected.trace_add("write", record_answer)
selected.trace_add("write", update_option_colors)  # Add this line

option_vars = [tk.StringVar() for _ in range(4)]
option_buttons = []
for i in range(4):
    rb = tk.Radiobutton(
        main_frame,
        textvariable=option_vars[i],
        variable=selected,
        value=chr(65+i),
        font=("Segoe UI", 18),
        anchor="w",
        padx=24,
        pady=8,
        bg=FRAME_COLOR,
        activebackground=FRAME_COLOR,
        highlightthickness=0,
        indicatoron=0,
        width=20,
        state=tk.DISABLED  # <-- Add this line
    )
    rb.pack(anchor="w", padx=40, pady=6, fill="x")
    option_buttons.append(rb)

button_frame = tk.Frame(main_frame, bg=FRAME_COLOR)
button_frame.pack(pady=30)

prev_btn = tk.Button(button_frame, text="Previous", command=prev_question, font=BTN_FONT, width=12, bg=BTN_COLOR, fg=ACCENT_COLOR, bd=0, relief="ridge", activebackground=BTN_HOVER, state=tk.DISABLED)
prev_btn.grid(row=0, column=0, padx=20)
prev_btn.bind("<Enter>", on_enter)
prev_btn.bind("<Leave>", on_leave)

next_btn = tk.Button(button_frame, text="Next", command=next_question, font=BTN_FONT, width=12, bg=BTN_COLOR, fg=ACCENT_COLOR, bd=0, relief="ridge", activebackground=BTN_HOVER, state=tk.DISABLED)
next_btn.grid(row=0, column=1, padx=20)
next_btn.bind("<Enter>", on_enter)
next_btn.bind("<Leave>", on_leave)

finish_btn = tk.Button(main_frame, text="Finish Quiz", command=finish_quiz, font=BTN_FONT, width=18, bg=ACCENT_COLOR, fg="white", bd=0, relief="ridge", activebackground="#2d6fd2", state=tk.DISABLED)
finish_btn.pack(pady=10)
finish_btn.bind("<Enter>", lambda e: finish_btn.config(bg="#2d6fd2"))
finish_btn.bind("<Leave>", lambda e: finish_btn.config(bg=ACCENT_COLOR))

# --- GUI for quiz selection ---
quiz_files = get_quiz_files()
quiz_select_frame = tk.Frame(root, bg=BG_COLOR)
quiz_select_frame.pack(pady=(10, 0))

tk.Label(quiz_select_frame, text="Select Quiz:", font=FONT, bg=BG_COLOR).pack(side="left", padx=(0, 10))
quiz_select = ttk.Combobox(quiz_select_frame, values=quiz_files, font=FONT, state="readonly", width=30)
quiz_select.pack(side="left")
if quiz_files:
    quiz_select.current(0)

start_btn = tk.Button(quiz_select_frame, text="Start", font=BTN_FONT, bg=ACCENT_COLOR, fg="white", command=load_selected_quiz)
start_btn.pack(side="left", padx=10)

# 預設 quiz_data 為空直到選擇題庫

root.mainloop()