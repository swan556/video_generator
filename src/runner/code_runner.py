import tkinter as tk
from tkinter import scrolledtext, simpledialog
import os
import subprocess
from time import sleep

root = tk.Tk()
root.title("Dark Themed UI")
root.geometry("1920x1080")

# ------------------------ COLORS ------------------------
bg_color = "#121212"
entry_bg = "#1E1E1E"
text_bg = "#1E1E1E"
fg_color = "#FFFFFF"
placeholder_color = "#555555"
button_color = "#4CAF50"

root.configure(bg=bg_color)

# ------------------------ LANGUAGE OPTIONS ------------------------
LANGUAGES = ["python", "c++", "c", "java", "html", "css", "javascript", "bash",
             "go", "rust", "typescript", "kotlin", "swift", "php", "sql"]
selected_language = tk.StringVar()
selected_language.set(LANGUAGES[0])  # default

def run_manim(title):
    with open("./temp_files/cwf.txt", "w", encoding="utf-8") as f:
        f.write("_".join(title.split()))
    
    status_label_2.config(text="Running Manim...")
    root.update()
    python_path = "./venv/bin/python"
    script_path = "./src/generator/main.py"
    subprocess.run([python_path, script_path])
    status_label_2.config(text="Manim Finished.")

def sanitize_title(title):
    return title.strip().lower().replace(" ", "_")

def create_files(hook, hook_code, title, body, main_code, lang_ext):
    session_id = sanitize_title(title)
    base_path = f"./temp_files/{session_id}/"
    os.makedirs(base_path, exist_ok=True)

    with open(base_path + "hook.txt", "w", encoding="utf-8") as f:
        f.write(hook)

    with open(base_path + f"hook_code.{lang_ext}", "w", encoding="utf-8") as f:
        f.write(hook_code)

    with open(base_path + "title.txt", "w", encoding="utf-8") as f:
        f.write(title)

    with open(base_path + "body.txt", "w", encoding="utf-8") as f:
        f.write(body)

    with open(base_path + f"main_code.{lang_ext}", "w", encoding="utf-8") as f:
        f.write(main_code)

    with open(base_path + f"file_extension.txt", "w", encoding="utf-8") as f:
        f.write(lang_ext)

def load_session():
    try:
        folders = os.listdir("./temp_files")
        folders = [f for f in folders if os.path.isdir(f"./temp_files/{f}")]
        if not folders:
            status_label.config(text="No saved sessions found.", fg="red")
            return

        session = simpledialog.askstring("Load Session", f"Available sessions:\n{', '.join(folders)}\n\nEnter session ID to load:")
        if not session:
            return

        session = sanitize_title(session)
        path = f"./temp_files/{session}/"

        def try_read(file):
            try:
                with open(path + file, "r", encoding="utf-8") as f:
                    return f.read()
            except:
                return None

        title = try_read("title.txt")
        body = try_read("body.txt")
        hook = try_read("hook.txt")
        ext = try_read("file_extension.txt")
        main_code = try_read(f"main_code.{ext}")
        hook_code = try_read(f"hook_code.{ext}")

        if not all([title, body, hook, main_code, hook_code]):
            status_label.config(text="Failed to load: missing files.", fg="red")
            return

        reset_fields(skip_placeholders=True)
        title_entry.insert(0, title)
        selected_language.set(ext)
        hook_text.insert("1.0", hook)
        body_text.insert("1.0", body)
        hook_code_text.insert("1.0", hook_code)
        main_code_text.insert("1.0", main_code)

        status_label.config(text="Session loaded.", fg="green")

    except Exception as e:
        status_label.config(text=f"Error: {str(e)}", fg="red")

def add_placeholder(widget, placeholder_text, is_text=False):
    def on_focus_in(event):
        current = widget.get("1.0", tk.END).strip() if is_text else widget.get()
        if current == placeholder_text:
            if is_text:
                widget.delete("1.0", tk.END)
            else:
                widget.delete(0, tk.END)
            widget.config(fg=fg_color)

    def on_focus_out(event):
        current = widget.get("1.0", tk.END).strip() if is_text else widget.get()
        if current == '':
            if is_text:
                widget.insert("1.0", placeholder_text)
            else:
                widget.insert(0, placeholder_text)
            widget.config(fg=placeholder_color)

    if is_text:
        widget.insert("1.0", placeholder_text)
    else:
        widget.insert(0, placeholder_text)
    widget.config(fg=placeholder_color)

    widget.bind("<FocusIn>", on_focus_in)
    widget.bind("<FocusOut>", on_focus_out)

def setup_code_box_behavior(textbox):
    def handle_tab(event):
        textbox.insert(tk.INSERT, "    ")
        return "break"

    def handle_return(event):
        cursor_index = textbox.index(tk.INSERT)
        line_number = cursor_index.split('.')[0]
        line_start = f"{line_number}.0"
        line_end = f"{line_number}.end"
        current_line = textbox.get(line_start, line_end)

        indent = ''
        for char in current_line:
            if char in (' ', '\t'):
                indent += char
            else:
                break

        textbox.insert(tk.INSERT, f"\n{indent}")
        return "break"

    def handle_backspace(event):
        cursor_index = textbox.index(tk.INSERT)
        line_number, column = map(int, cursor_index.split('.'))
        if column >= 4:
            start_index = f"{line_number}.{column - 4}"
            end_index = cursor_index
            chars_to_check = textbox.get(start_index, end_index)
            if chars_to_check == "    ":
                textbox.delete(start_index, end_index)
                return "break"
        return

    textbox.bind("<Tab>", handle_tab)
    textbox.bind("<Return>", handle_return)
    textbox.bind("<BackSpace>", handle_backspace)

def reset_fields(skip_placeholders=False):
    widgets = [
        (title_entry, "title", False),
        (hook_text, "hook", True),
        (body_text, "body", True),
        (hook_code_text, "hook code", True),
        (main_code_text, "main code", True)
    ]
    for widget, placeholder, is_text in widgets:
        if is_text:
            widget.delete("1.0", tk.END)
        else:
            widget.delete(0, tk.END)
        if not skip_placeholders:
            add_placeholder(widget, placeholder, is_text)

    status_label.config(text="", fg="green")
    status_label_2.config(text="")

# ------------------------ WIDGETS ------------------------

title_entry = tk.Entry(root, font=("Arial", 16), bg=entry_bg, fg=fg_color, insertbackground=fg_color)
title_entry.place(x=20, y=20, width=700, height=50)
add_placeholder(title_entry, "title")

lang_menu = tk.OptionMenu(root, selected_language, *LANGUAGES)
lang_menu.configure(bg=button_color, fg="white", font=("Arial", 12))
lang_menu.place(x=740, y=20, width=180, height=50)

hook_text = scrolledtext.ScrolledText(root, font=("Arial", 28), bg=text_bg, fg=fg_color, insertbackground=fg_color)
hook_text.place(x=20, y=90, width=900, height=200)
add_placeholder(hook_text, "hook", is_text=True)
setup_code_box_behavior(hook_text)

body_text = scrolledtext.ScrolledText(root, font=("Arial", 42), bg=text_bg, fg=fg_color, insertbackground=fg_color)
body_text.place(x=20, y=310, width=900, height=600)
add_placeholder(body_text, "body", is_text=True)
setup_code_box_behavior(body_text)

hook_code_text = scrolledtext.ScrolledText(root, font=("Courier", 14), bg=text_bg, fg=fg_color, insertbackground=fg_color)
hook_code_text.place(x=950, y=90, width=900, height=200)
add_placeholder(hook_code_text, "hook code", is_text=True)
setup_code_box_behavior(hook_code_text)

main_code_text = scrolledtext.ScrolledText(root, font=("Courier", 14), bg=text_bg, fg=fg_color, insertbackground=fg_color)
main_code_text.place(x=950, y=310, width=900, height=600)
add_placeholder(main_code_text, "main code", is_text=True)
setup_code_box_behavior(main_code_text)

# ------------------------ STATUS LABELS ------------------------
status_label = tk.Label(root, text="", font=("Arial", 14), bg=bg_color, fg="green")
status_label.place(x=950, y=980, width=900, height=30)

status_label_2 = tk.Label(root, text="", font=("Arial", 14), bg=bg_color, fg="#FFA500")
status_label_2.place(x=950, y=1015, width=900, height=30)

# ------------------------ ACTIONS ------------------------

def submit_action():
    title = title_entry.get().strip()
    hook = hook_text.get("1.0", tk.END).strip()
    body = body_text.get("1.0", tk.END).strip()
    hook_code = hook_code_text.get("1.0", tk.END).strip()
    main_code = main_code_text.get("1.0", tk.END).strip()
    lang_ext = selected_language.get()

    if title == "" or title == "title":
        status_label.config(text="Please enter a valid title.", fg="red")
        return

    create_files(hook, hook_code, title, body, main_code, lang_ext)
    status_label.config(text="Files created successfully.", fg="green")

    sleep(2)
    run_manim(title)

# ------------------------ BUTTONS ------------------------

submit_btn = tk.Button(root, text="SUBMIT", font=("Arial", 16), bg=button_color, fg="white", command=submit_action)
submit_btn.place(x=950, y=920, width=290, height=50)

reset_btn = tk.Button(root, text="RESET", font=("Arial", 16), bg="#f44336", fg="white", command=reset_fields)
reset_btn.place(x=1260, y=920, width=290, height=50)

load_btn = tk.Button(root, text="LOAD", font=("Arial", 16), bg="#2196F3", fg="white", command=load_session)
load_btn.place(x=1570, y=920, width=280, height=50)

root.mainloop()
