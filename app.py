import tkinter as tk
from tkinter import messagebox
import pickle
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import csv
import os
from datetime import datetime
import time

class SemanticContentClassifierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Semantic Content Classifier")
        self.root.geometry("900x650")
        self.root.resizable(False, False)
        
        # Load Model and Vectorizer
        try:
            with open('trained_model.pkl', 'rb') as f:
                self.model = pickle.load(f)
            with open('vectorizer.pkl', 'rb') as f:
                self.vectorizer = pickle.load(f)
        except Exception as e:
            messagebox.showerror("Error", "Model files not found! Please train the model first.")
            self.model = None
            self.vectorizer = None
            
        # Initialize NLP tools
        try:
            self.stop_words = set(stopwords.words('english'))
        except:
            nltk.download('stopwords')
            self.stop_words = set(stopwords.words('english'))
        self.port_stem = PorterStemmer()
        
        self.setup_ui()
        self.update_clock()
        
    def setup_ui(self):
        # Menu Bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.exit_app)
        menubar.add_cascade(label="File", menu=file_menu)
        
        tools_menu = tk.Menu(menubar, tearoff=0)
        tools_menu.add_command(label="Dataset Info", command=self.show_dataset_info)
        tools_menu.add_command(label="Model Info", command=self.show_model_info)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        # Main Layout
        header_frame = tk.Frame(self.root, bg="#2C3E50", pady=20)
        header_frame.pack(fill=tk.X)
        
        tk.Label(header_frame, text="Semantic Content Classifier", font=("Helvetica", 24, "bold"), fg="white", bg="#2C3E50").pack()
        tk.Label(header_frame, text="Natural Language Processing using Machine Learning", font=("Helvetica", 12), fg="#BDC3C7", bg="#2C3E50").pack()
        
        # Content Frame
        content_frame = tk.Frame(self.root, padx=40, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(content_frame, text="Enter News Article:", font=("Helvetica", 14, "bold")).pack(anchor="w")
        
        self.text_input = tk.Text(content_frame, height=10, width=90, font=("Helvetica", 12), wrap=tk.WORD, bd=2, relief=tk.GROOVE)
        self.text_input.pack(pady=10)
        
        # Buttons Frame
        btn_frame = tk.Frame(content_frame)
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Predict Category", font=("Helvetica", 12, "bold"), bg="#27AE60", fg="white", width=15, command=self.predict).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Clear", font=("Helvetica", 12, "bold"), bg="#F39C12", fg="white", width=15, command=self.clear).grid(row=0, column=1, padx=10)
        tk.Button(btn_frame, text="History", font=("Helvetica", 12, "bold"), bg="#2980B9", fg="white", width=15, command=self.show_history).grid(row=0, column=2, padx=10)
        tk.Button(btn_frame, text="Exit", font=("Helvetica", 12, "bold"), bg="#C0392B", fg="white", width=15, command=self.exit_app).grid(row=0, column=3, padx=10)
        
        # Result Frame
        result_frame = tk.Frame(content_frame, pady=20)
        result_frame.pack(fill=tk.X)
        
        tk.Label(result_frame, text="Predicted Category:", font=("Helvetica", 14, "bold")).pack()
        self.result_label = tk.Label(result_frame, text="---", font=("Helvetica", 20, "bold"), fg="#27AE60")
        self.result_label.pack(pady=10)
        
        # Status Bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W, bg="#ECF0F1", font=("Helvetica", 10))
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.clock_var = tk.StringVar()
        clock_label = tk.Label(self.root, textvariable=self.clock_var, bd=1, relief=tk.SUNKEN, anchor=tk.E, bg="#ECF0F1", font=("Helvetica", 10))
        clock_label.place(relx=1.0, rely=1.0, anchor="se", y=-2)
        
    def update_clock(self):
        now = time.strftime("%H:%M:%S")
        self.clock_var.set(now)
        self.root.after(1000, self.update_clock)
        
    def clean_text(self, text):
        clean = re.sub('[^a-zA-Z]', ' ', text)
        clean = clean.lower()
        clean = clean.split()
        clean = [self.port_stem.stem(word) for word in clean if word not in self.stop_words]
        return ' '.join(clean)
        
    def predict(self):
        if not self.model or not self.vectorizer:
            messagebox.showerror("Error", "Model not loaded.")
            return
            
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter some text to classify.")
            return
            
        self.status_var.set("Processing and Predicting...")
        self.root.update_idletasks()
        
        cleaned = self.clean_text(text)
        vectorized = self.vectorizer.transform([cleaned])
        prediction = self.model.predict(vectorized)[0]
        
        self.result_label.config(text=prediction)
        self.save_history(text, prediction)
        self.status_var.set("Prediction Complete")
        
    def save_history(self, text, prediction):
        file_exists = os.path.isfile('prediction_history.csv')
        
        with open('prediction_history.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['Date', 'Time', 'News', 'Prediction'])
            
            now = datetime.now()
            date = now.strftime("%d-%m-%Y")
            time_str = now.strftime("%H:%M:%S")
            writer.writerow([date, time_str, text, prediction])
            
    def clear(self):
        self.text_input.delete("1.0", tk.END)
        self.result_label.config(text="---")
        self.status_var.set("Ready")
        
    def show_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("Prediction History")
        history_window.geometry("600x400")
        
        text_area = tk.Text(history_window, font=("Helvetica", 10))
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        try:
            with open('prediction_history.csv', 'r', encoding='utf-8') as f:
                content = f.read()
                text_area.insert(tk.END, content)
        except:
            text_area.insert(tk.END, "No history found.")
        text_area.config(state=tk.DISABLED)
        
    def show_dataset_info(self):
        info = (
            "Dataset Information:\n\n"
            "- Source: Synthetic News Dataset\n"
            "- Total Articles: ~450\n"
            "- Categories (9): Business, Sports, Politics, Technology, Health, Crime, Education, Entertainment, Weather\n"
            "- Preprocessing: Lowercasing, Punctuation Removal, Stopword Removal, Stemming"
        )
        messagebox.showinfo("Dataset Info", info)
        
    def show_model_info(self):
        info = (
            "Model Information:\n\n"
            "- Algorithm: Multinomial Naive Bayes\n"
            "- Feature Extraction: TF-IDF Vectorizer\n"
            "- Max Features: 5000\n"
            "- Train/Test Split: 80/20\n"
            "- Check classification_report.txt for accuracy metrics."
        )
        messagebox.showinfo("Model Info", info)
        
    def show_about(self):
        info = (
            "Semantic Content Classifier\n\n"
            "An NLP and Machine Learning application that automatically classifies "
            "news articles into predefined categories.\n\n"
            "Developed for Internship Project."
        )
        messagebox.showinfo("About", info)
        
    def exit_app(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SemanticContentClassifierApp(root)
    root.mainloop()
