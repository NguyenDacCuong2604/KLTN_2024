import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import pandas as pd
import os
import threading
import datetime

from Code.Model_SVM import Model_SVM
from Code.Vectorization import Vectorization
from Code.VietnameseTextPreprocessor import VietnameseTextPreprocessor


# Tkinter GUI class
class DataPreprocessor:
    name_file_datapreprocess = 'data_preprocess.csv'
    min_df = 6
    name_file_vectorizer = 'tfidf.model'
    name_file_svm = 'svm.model'

    def __init__(self, root):
        self.root = root
        self.root.title("Data Preprocessor")

        # Define initial width and height for the frame
        self.initial_width = 600
        self.initial_height = 300

        # Set initial size of the window
        self.root.geometry(f"{self.initial_width}x{self.initial_height}")
        self.root.minsize(self.initial_width, self.initial_height)

        # Create a frame that will expand with the window
        self.frame = ttk.Frame(root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure row and column weights for dynamic resizing
        self.frame.grid_rowconfigure(0, weight=0)
        self.frame.grid_rowconfigure(1, weight=0)
        self.frame.grid_rowconfigure(2, weight=0)
        self.frame.grid_rowconfigure(3, weight=0)
        self.frame.grid_rowconfigure(4, weight=1)  # Expandable row

        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(2, weight=1)
        self.frame.grid_columnconfigure(3, weight=0)

        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Helvetica", 13))
        self.style.configure("TEntry", font=("Helvetica", 13))
        self.style.configure("TButton", font=("Helvetica", 13))

        self.file_label = ttk.Label(self.frame, text="Select input file:")
        self.file_label.grid(row=0, column=0, sticky=tk.W)

        self.file_entry = ttk.Entry(self.frame)
        self.file_entry.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E))

        self.browse_button = ttk.Button(self.frame, text="Browse", command=self.browse_file_input, width=15)
        self.browse_button.grid(row=0, column=3, sticky=tk.W)

        self.input_column_label = ttk.Label(self.frame, text="Input:")
        self.input_column_label.grid(row=1, column=0, sticky=tk.E, pady=(10, 0))

        self.input_column_entry = ttk.Entry(self.frame)
        self.input_column_entry.grid(row=1, column=1,  sticky=tk.W, pady=(10, 0))

        self.target_column_label = ttk.Label(self.frame, text="Target:")
        self.target_column_label.grid(row=1, column=2, sticky=tk.E, padx=(10, 0), pady=(10, 0))

        self.target_column_entry = ttk.Entry(self.frame)
        self.target_column_entry.grid(row=1, column=3, sticky=tk.W, pady=(10, 0))

        self.output_label = ttk.Label(self.frame, text="Select the folder to save:")
        self.output_label.grid(row=2, column=0, sticky=tk.W)

        self.output_entry = ttk.Entry(self.frame)
        self.output_entry.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E))

        self.browse_output_button = ttk.Button(self.frame, text="Browse", command=self.browse_folder_output, width=15)
        self.browse_output_button.grid(row=2, column=3, sticky=tk.W)

        self.text_widget = tk.Text(self.frame, font=("Helvetica", 13), state=tk.DISABLED)
        self.text_widget.grid(row=4, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))

        self.scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.text_widget.yview)
        self.scrollbar.grid(row=4, column=3, sticky=(tk.N, tk.S, tk.E), pady=(10, 0))
        self.text_widget.config(yscrollcommand=self.scrollbar.set)

        self.start_button = tk.Button(self.frame, text="Start", command=self.toggle_processing, width=15, bg='light green', font=("Helvetica", 13))
        self.start_button.grid(row=3, column=3, sticky=tk.E, pady=(10, 0))

        for child in self.frame.winfo_children():
            child.grid_configure(padx=5, pady=5)

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self.text_widget.tag_configure("error", foreground="red")
        self.text_widget.tag_configure("success", foreground="green")
        self.text_widget.tag_configure("info", foreground="black")

        self.processing = False
        self.processing_thread = None
        self.stop_event = threading.Event()

    def browse_file_input(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls *.csv")])
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)

    def browse_folder_output(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, folder_path)

    def log_message(self, message, msg_type="info"):
        """Log a message to the text_widget with a timestamp and color-coding."""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")
        full_message = f"{timestamp} - {message}"
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.insert(tk.END, full_message + '\n', (msg_type,))
        self.text_widget.see(tk.END)  # Scroll to the end
        self.text_widget.config(state=tk.DISABLED)

    def toggle_processing(self):
        if self.processing:
            self.stop_event.set()  # Signal the thread to stop
            self.processing = False
            self.start_button.config(text="Start", bg="light green")
            self.log_message("Stopping process...", "info")
        else:
            self.log_message("Process started...", "info")
            self.processing = True
            self.start_button.config(text="Stop", bg="red")
            self.stop_event.clear()  # Clear the stop event
            self.processing_thread = threading.Thread(target=self.process_data)
            self.processing_thread.start()

    def process_data(self):
        try:
            input_file = self.file_entry.get()
            output_folder = self.output_entry.get()

            if not input_file or not output_folder:
                self.log_message("Error: Please select both the input file and the output folder.", "error")
                return

            column_input = self.input_column_entry.get()
            column_target = self.target_column_entry.get()

            if not column_input or not column_target:
                self.log_message("Error: Please enter the names of the Input and Target columns.", "error")
                return

            if not os.path.exists(output_folder):
                self.log_message(f"Error: The output directory '{output_folder}' does not exist.", "error")
                return

            self.log_message("Loading data... [STARTED]", "info")

            # Check if stop event is set
            if self.stop_event.is_set():
                return

            try:
                df = None
                if input_file.endswith('.xlsx') or input_file.endswith('.xls'):
                    df = pd.read_excel(input_file)
                elif input_file.endswith('.csv'):
                    df = pd.read_csv(input_file)

                # Check if stop event is set
                if self.stop_event.is_set():
                    return

                columns_df = df.columns

                if column_input not in columns_df:
                    self.log_message(f"Error: The Input column '{column_input}' does not exist in the file.", "error")
                    return

                if column_target not in columns_df:
                    self.log_message(f"Error: The Target column '{column_target}' does not exist in the file.", "error")
                    return

                self.log_message("Loading data... [COMPLETED]", "success")
                self.log_message("Preprocessing data... [STARTED]", "info")

                # Data preprocessing
                output_path_stopword = '../Dataset/Root/data_preprocessing_stopwords_project.csv'
                vietnameseTextPreprocessor = VietnameseTextPreprocessor(output_path_stopword)
                df_preprocess = vietnameseTextPreprocessor.process_df(df, self.input_column_entry.get(),
                                                                      self.target_column_entry.get())

                # Check if stop event is set
                if self.stop_event.is_set():
                    return
                preprocess_output_path = f'{self.output_entry.get()}/{self.name_file_datapreprocess}'
                df_preprocess.to_csv(preprocess_output_path, index=False)
                self.log_message("Preprocessing data... [COMPLETED]", "success")
                self.log_message(f"Data preprocessing saved to '{preprocess_output_path}'", "success")
                self.log_message("Vectorizing data... [STARTED]", "info")

                # Vectorization
                X = df_preprocess['input']
                y = df_preprocess['label']

                vectorization = Vectorization()
                X_vector = vectorization.fit_transform(X, self.min_df)
                vectorizer_model_path = f'{self.output_entry.get()}/{self.name_file_vectorizer}'
                vectorization.save_model(vectorizer_model_path)
                self.log_message("Vectorizing data... [COMPLETED]", "success")
                self.log_message(f"Vectorizer model saved to '{vectorizer_model_path}'", "success")
                # Train model
                self.log_message("Training SVM model... [STARTED]", "info")
                model_svm = Model_SVM()
                model_svm.fit(X_vector, y)
                svm_model_path = f'{self.output_entry.get()}/{self.name_file_svm}'
                model_svm.save_model(svm_model_path)
                self.log_message("Training SVM model... [COMPLETED]", "success")
                self.log_message(f"SVM model saved to '{svm_model_path}'", "success")
                self.log_message("Process completed successfully!", "success")
                self.root.after(0, lambda: messagebox.showinfo("Success", "Processed successfully!!!"))
            except FileNotFoundError:
                self.log_message("Error: File not found. Please check the file path.", "error")
            except Exception as e:
                self.log_message(f"Error: An error occurred: {e}", "error")
        finally:
            self.processing = False
            self.start_button.config(text="Start", bg="light green")


if __name__ == "__main__":
    root = tk.Tk()
    app = DataPreprocessor(root)
    root.mainloop()
