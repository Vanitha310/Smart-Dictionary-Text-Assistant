import tkinter as tk
import threading
from api import fetch_word_data
from database import save_word, get_top_words

typing_delay = 600
typing_timer = None


class SmartDictionaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Dictionary Text Assistant")
        self.root.geometry("750x550")
        self.root.config(bg="#f3f4f6")

        self.setup_ui()

    def setup_ui(self):
        input_frame = tk.LabelFrame(self.root, text=" Start Typing ", font=('Segoe UI', 12, 'bold'))
        input_frame.pack(padx=20, pady=10, fill="both")

        self.text_widget = tk.Text(input_frame, height=5, font=('Segoe UI', 13))
        self.text_widget.pack(fill="both", expand=True)
        self.text_widget.bind("<KeyRelease>", self.on_key_release)

        output_frame = tk.LabelFrame(self.root, text=" Word Insights ", font=('Segoe UI', 12, 'bold'))
        output_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.output_widget = tk.Text(output_frame, wrap="word", state="disabled", font=('Consolas', 11))
        self.output_widget.pack(fill="both", expand=True)

        stats_frame = tk.LabelFrame(self.root, text=" Top Searched Words ", font=('Segoe UI', 11, 'bold'))
        stats_frame.pack(padx=20, pady=10, fill="both")

        self.stats_label = tk.Label(stats_frame, font=('Segoe UI', 10))
        self.stats_label.pack()

        self.update_stats()

    def extract_last_word(self):
        text = self.text_widget.get("1.0", tk.END).strip()
        words = text.split()
        return words[-1] if words else ""

    def on_key_release(self, event):
        global typing_timer
        if typing_timer:
            self.root.after_cancel(typing_timer)
        typing_timer = self.root.after(typing_delay, self.start_search)

    def start_search(self):
        word = self.extract_last_word()
        if word:
            threading.Thread(target=self.process_word, args=(word,), daemon=True).start()

    def process_word(self, word):
        data = fetch_word_data(word)
        if data:
            save_word(word, data["definition"])
            self.root.after(0, lambda: self.display_result(word, data))

    def display_result(self, word, data):
        current_word = self.extract_last_word()
        if word.lower() != current_word.lower():
            return

        self.output_widget.config(state="normal")
        self.output_widget.delete("1.0", tk.END)

        content = f"""
WORD: {word.upper()}

Definition:
{data['definition']}

Synonyms:
{', '.join(data['synonyms']) if data['synonyms'] else "None"}

Example:
{data['example']}
"""
        self.output_widget.insert("1.0", content)
        self.output_widget.config(state="disabled")

        self.update_stats()

    def update_stats(self):
        top_words = get_top_words()
        text = " | ".join([f"{word} ({count})" for word, count in top_words])
        self.stats_label.config(text=text if text else "No data yet.")


def run_app():
    root = tk.Tk()
    app = SmartDictionaryApp(root)
    root.mainloop()