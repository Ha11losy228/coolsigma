import os
import tkinter as tk
from tkinter import ttk
import itertools
import subprocess
import threading
import time

class RainbowText:
    def __init__(self, canvas, text, x, y):
        self.canvas = canvas
        self.text = text
        self.x = x
        self.y = y
        self.colors = itertools.cycle(['#FF0000', '#FF7F00', '#FFFF00', '#00FF00', '#0000FF', '#4B0082', '#8B00FF'])
        self.text_id = self.canvas.create_text(self.x, self.y, text=self.text, font=('Consolas', 12), fill=next(self.colors))
        self.animate()

    def animate(self):
        self.canvas.itemconfig(self.text_id, fill=next(self.colors))
        self.canvas.after(100, self.animate)

def search_usertg(usertg):
    base_path = './Base'
    results = []

    for root, dirs, files in os.walk(base_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if usertg in content:
                        results.append((file, content))
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")

    return results

def search_thread(usertg):
    global searching
    searching = True
    search_label.config(text="Поиск")
    dots = itertools.cycle(['.', '..', '...', '....', '.....'])

    while searching:
        search_label.config(text=f"Поиск{next(dots)}")
        time.sleep(0.5)

    results = search_usertg(usertg)

    if results:
        result_text = "Результаты:\n\n"
        for file, content in results:
            result_text += f"Файл: {file}\n{content}\n\n"
        result_label.config(text=result_text, justify='left', wraplength=600)
    else:
        result_label.config(text="Ничего не найдено.", justify='left')

    search_label.config(text="Поиск завершен")

def on_search():
    usertg = usertg_entry.get()
    if not usertg:
        result_label.config(text="Введите username Telegram.", justify='left')
        return

    global searching
    searching = False
    search_label.config(text="Поиск...")

    search_thread_instance = threading.Thread(target=search_thread, args=(usertg,))
    search_thread_instance.start()

def show_menu():
    root.destroy()
    subprocess.Popen(['python', 'main.py'])

def main():
    global root, canvas
    root = tk.Tk()
    root.title("Пробив по username Telegram")
    root.configure(bg='black')

    canvas = tk.Canvas(root, width=800, height=400, bg='black', highlightthickness=0)
    canvas.pack()

    rainbow_text = RainbowText(canvas, "██████╗░██████╗░░█████╗░██████╗░██╗██╗░░░██╗\n"
                                       "██╔══██╗██╔══██╗██╔══██╗██╔══██╗██║██║░░░██║\n"
                                       "██████╔╝██████╔╝██║░░██║██████╦╝██║╚██╗░██╔╝\n"
                                       "██╔═══╝░██╔══██╗██║░░██║██╔══██╗██║░╚████╔╝░\n"
                                       "██║░░░░░██║░░██║╚█████╔╝██████╦╝██║░░╚██╔╝░░\n"
                                       "╚═╝░░░░░╚═╝░░╚═╝░╚════╝░╚═════╝░╚═╝░░░╚═╝░░░ po useru tg", 400, 100)

    usertg_label = ttk.Label(root, text="Введите username Telegram:", font=("Consolas", 14), background='black', foreground='white')
    usertg_label.pack(pady=10)

    global usertg_entry
    usertg_entry = ttk.Entry(root, font=("Consolas", 14), width=30)
    usertg_entry.pack(pady=10)

    search_button = ttk.Button(root, text="Искать", command=on_search)
    search_button.pack(pady=10)

    global result_label
    result_label = ttk.Label(root, text="", font=("Consolas", 12), background='black', foreground='white', anchor='w')
    result_label.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    global search_label
    search_label = ttk.Label(root, text="", font=("Consolas", 12), background='black', foreground='white', anchor='w')
    search_label.pack(pady=10, padx=10)

    back_button = ttk.Button(root, text="Назад", command=show_menu)
    back_button.pack(side=tk.LEFT, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
