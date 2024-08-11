import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import pandas as pd
import os
import re
import threading
import datetime
import logging
import configparser

from SVM import SVM
from Vectorization import Vectorization
from VietnameseTextPreprocessor import VietnameseTextPreprocessor

def read_config_general():
    # Create a ConfigParser object
    config = configparser.ConfigParser()

    # Read the configuration file
    config.read('config.ini', encoding='utf-8')

    # Access values from the configuration file
    log_file_name = config.get('General', 'log_file_name')
    input_df_name = config.get('General', 'input_df_name')
    label_df_name = config.get('General', 'label_df_name')
    return log_file_name, input_df_name, label_df_name

def read_config_preprocessing():
    # Create a ConfigParser object
    config = configparser.ConfigParser()

    # Read the configuration file
    config.read('config.ini', encoding='utf-8')

    # Access values from the configuration file
    multi_label = config.getboolean('Preprocessing', 'multi_label')
    stopword_path = config.get('Preprocessing', 'stopword_path')
    is_remove_np = config.getboolean('Preprocessing', 'is_remove_np')
    required_columns_str = config.get('Preprocessing', 'required_columns')
    required_columns = [column.strip() for column in required_columns_str.split(';')]
    input_column_name = config.get('Preprocessing', 'input_column_name')
    label_column_name = config.get('Preprocessing', 'label_column_name')

    return multi_label, stopword_path, is_remove_np, required_columns, input_column_name, label_column_name

def read_config_vectoration():
    # Create a ConfigParser object
    config = configparser.ConfigParser()

    # Read the configuration file
    config.read('config.ini', encoding='utf-8')

    # Access values from the configuration file
    data_vector_file_name = config.get('Vectorization', 'data_vector_file_name')
    vectorizer_file_name = config.get('Vectorization', 'vectorizer_file_name')
    min_tf = config.getint('Vectorization', 'min_tf')

    return data_vector_file_name, vectorizer_file_name, min_tf

def read_config_svm():
    # Create a ConfigParser object
    config = configparser.ConfigParser()

    # Read the configuration file
    config.read('config.ini')

    # Access values from the configuration file
    svm_file_name = config.get('SVM', 'svm_file_name')
    C = config.getfloat('SVM', 'C')
    kernel = config.get('SVM', 'kernel')
    gamma = config.get('SVM', 'gamma')
    probability = config.getboolean('SVM', 'probability')

    return svm_file_name, C, kernel, gamma, probability



# Tkinter GUI class
class DataPreprocessor:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Preprocessor")

        self.initial_width = 800
        self.initial_height = 300

        self.root.geometry(f"{self.initial_width}x{self.initial_height}")
        self.root.minsize(self.initial_width, self.initial_height)

        self.frame = ttk.Frame(root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure row and column weights for dynamic resizing
        self.frame.grid_rowconfigure(0, weight=0)
        self.frame.grid_rowconfigure(1, weight=0)
        self.frame.grid_rowconfigure(2, weight=0)
        self.frame.grid_rowconfigure(3, weight=1)

        self.frame.grid_columnconfigure(0, weight=0)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(2, weight=1)
        self.frame.grid_columnconfigure(3, weight=0)

        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Helvetica", 13))
        self.style.configure("TEntry", font=("Helvetica", 13))
        self.style.configure("TButton", font=("Helvetica", 13))

        self.file_label = ttk.Label(self.frame, text="Select the data folder for preprocess:")
        self.file_label.grid(row=0, column=0, sticky=tk.W)

        self.input_entry = ttk.Entry(self.frame)
        self.input_entry.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E))

        self.browse_button = ttk.Button(self.frame, text="Browse", command=self.browse_folder_input, width=15)
        self.browse_button.grid(row=0, column=3, sticky=tk.W)

        self.output_label = ttk.Label(self.frame, text="Select the folder to save:")
        self.output_label.grid(row=1, column=0, sticky=tk.W)

        self.output_entry = ttk.Entry(self.frame)
        self.output_entry.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E))

        self.browse_output_button = ttk.Button(self.frame, text="Browse", command=self.browse_folder_output, width=15)
        self.browse_output_button.grid(row=1, column=3, sticky=tk.W)

        self.text_widget = tk.Text(self.frame, font=("Helvetica", 13), state=tk.DISABLED)
        self.text_widget.grid(row=3, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))

        self.scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.text_widget.yview)
        self.scrollbar.grid(row=3, column=3, sticky=(tk.N, tk.S, tk.E), pady=(10, 0))
        self.text_widget.config(yscrollcommand=self.scrollbar.set)

        self.start_button = tk.Button(self.frame, text="Start", command=self.toggle_processing, width=15,
                                      bg='light green', font=("Helvetica", 13))
        self.start_button.grid(row=2, column=3, sticky=tk.E, pady=(10, 0))

        for child in self.frame.winfo_children():
            child.grid_configure(padx=5, pady=5)

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self.text_widget.tag_configure("error", foreground="red")
        self.text_widget.tag_configure("success", foreground="green")
        self.text_widget.tag_configure("info", foreground="black")
        self.text_widget.tag_configure("warning", foreground="yellow")

        self.processing = False
        self.processing_thread = None
        self.stop_event = threading.Event()
        self.app_closing = False

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.logger = logging.getLogger("DataPreprocessorLogger")
        self.logger.setLevel(logging.DEBUG)
        self.log_file_handler = None

        self.log_file_name, self.input_df_name, self.label_df_name = read_config_general()

    def set_log_file(self, output_folder):
        if self.log_file_handler:
            self.logger.removeHandler(self.log_file_handler)

        log_file_path = os.path.join(output_folder, self.log_file_name)
        self.log_file_handler = logging.FileHandler(log_file_path)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%H:%M:%S %d-%m-%Y')
        self.log_file_handler.setFormatter(formatter)
        self.logger.addHandler(self.log_file_handler)

    def on_close(self):
        self.app_closing = True
        self.root.destroy()

    def browse_folder_input(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, folder_path)

    def browse_folder_output(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, folder_path)

    def log_message(self, message, msg_type="info"):
        """Log a message to the text_widget with a timestamp and color-coding."""
        if not self.app_closing:
            timestamp = datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")
            full_message = f"{timestamp} - {message}"
            self.text_widget.config(state=tk.NORMAL)
            self.text_widget.insert(tk.END, full_message + '\n', (msg_type,))
            self.text_widget.see(tk.END)
            self.text_widget.config(state=tk.DISABLED)

            # Log to file
            if msg_type == "info":
                self.logger.info(message)
            elif msg_type == "success":
                self.logger.info(message)
            elif msg_type == "warning":
                self.logger.warning(message)
            elif msg_type == "error":
                self.logger.error(message)

    def toggle_processing(self):
        if self.processing:
            self.stop_event.set()
            self.processing = False
            self.start_button.config(text="Start", bg="light green")
            self.log_message("Stopping process...", "info")
        else:
            self.log_message("Process started...", "info")
            self.processing = True
            self.start_button.config(text="Stop", bg="red")
            self.stop_event.clear()
            self.processing_thread = threading.Thread(target=self.process_data)
            self.processing_thread.start()

    def process_data(self):
        try:
            input_folder = self.input_entry.get()
            output_folder = self.output_entry.get()

            if not input_folder:
                self.log_message("Error: Please select input folder.", "error")
                return

            if not output_folder:
                self.log_message("Error: Please select output folder.", "error")
                return

            if not os.path.isdir(input_folder):
                self.log_message(f"Error: The input directory '{input_folder}' does not exist or is not a directory.",
                                 "error")
                return

            if not os.path.isdir(output_folder):
                self.log_message(f"Error: The output directory '{output_folder}' does not exist or is not a directory.",
                                 "error")
                return

            self.set_log_file(output_folder)

            multi_label, stopword_path, is_remove_np, required_columns, input_column_name, label_column_name = read_config_preprocessing()

            xlsx_files = [f for f in os.listdir(input_folder) if f.endswith('.xlsx')]
            if not xlsx_files:
                self.log_message(f"No .xlsx files found in the input directory '{input_folder}'.", "error")
                return

            self.log_message("Loading data... [STARTED]", "info")
            self.log_message(f"Found {len(xlsx_files)} files .xlsx in the input directory.", "info")

            combined_data = []

            for xlsx_file in xlsx_files:
                if self.stop_event.is_set() or self.app_closing:
                    self.log_message("Processing stopped by user.", "error")
                    return

                self.log_message(f"Processing file: {xlsx_file}", "info")
                file_path = os.path.join(input_folder, xlsx_file)

                id_match = re.match(r'^(\d+)', xlsx_file)
                if not id_match:
                    self.log_message(f"Warning: The file '{xlsx_file}' does not have a valid ID in its name.",
                                     "warning")
                    continue

                room_id = id_match.group(1)

                try:
                    dataframe = pd.read_excel(file_path, sheet_name=0)

                    self.log_message(
                        f"File '{xlsx_file}' loaded with {dataframe.shape[0]} rows and {dataframe.shape[1]} columns.",
                        "info")

                    missing_columns = [col for col in required_columns if col not in dataframe.columns]
                    if missing_columns:
                        self.log_message(
                            f"Warning: The file '{xlsx_file}' is missing the following required columns: {', '.join(missing_columns)}.",
                            "warning")
                    else:
                        dataframe[label_column_name] = room_id
                        combined_data.append(dataframe[[input_column_name, label_column_name]])
                        self.log_message(f"File '{xlsx_file}' processed successfully with {dataframe.shape[0]} rows.",
                                         "success")
                except Exception as e:
                    self.log_message(f"Error processing file '{xlsx_file}': {str(e)}", "error")

                if self.stop_event.is_set() or self.app_closing:
                    self.log_message("Processing stopped by user.", "error")
                    return

            if combined_data:
                combined_df = pd.concat(combined_data, ignore_index=True)
                self.log_message(f"Combined Dataframe created with {len(combined_df)} entries.", "success")
                self.log_message("Loading data... [COMPLETED]", "success")
                self.log_message("Preprocessing data... [STARTED]", "info")

                vietnameseTextPreprocessor = VietnameseTextPreprocessor(path_stopwords=stopword_path,
                                                                        multi_label=multi_label, is_remove_np=is_remove_np)
                df_preprocess = vietnameseTextPreprocessor.process_df(combined_df, input_column_name, label_column_name, self.input_df_name, self.label_df_name)

                if self.stop_event.is_set() or self.app_closing:
                    self.log_message("Processing stopped by user.", "error")
                    return

                self.log_message("Preprocessing data... [COMPLETED]", "success")
                self.log_message("Vectorizing data... [STARTED]", "info")

                X = df_preprocess[self.input_df_name]
                y = df_preprocess[self.label_df_name]

                data_vector_file_name, vectorizer_file_name, min_tf = read_config_vectoration()

                vectorization = Vectorization()
                X_vector = vectorization.fit_transform(X, min_tf)

                #Lưu lại model vector
                vectorizer_model_path = f'{self.output_entry.get()}/{vectorizer_file_name}'
                vectorization.save_model(vectorizer_model_path)
                self.log_message("Vectorizing data... [COMPLETED]", "success")
                self.log_message(f"Vectorizer model saved to '{vectorizer_model_path}'", "success")

                # lưu lại file csv vector hoá
                preprocess_output_path = f'{self.output_entry.get()}/{data_vector_file_name}'
                df = pd.DataFrame(X_vector.toarray(), columns=vectorization.get_feature_names_out())
                df[self.label_df_name] = y
                df.to_csv(preprocess_output_path, index=False)
                self.log_message(f"Vectorizer data saved to '{preprocess_output_path}'", "success")

                if self.stop_event.is_set() or self.app_closing:
                    self.log_message("Processing stopped by user.", "error")
                    return

                svm_file_name, C, kernel, gamma, probability = read_config_svm()

                self.log_message("Training SVM model... [STARTED]", "info")
                model_svm = SVM(kernel = kernel, C = C, gamma = gamma, probability = probability)
                model_svm.fit(X_vector, y)
                svm_model_path = f'{self.output_entry.get()}/{svm_file_name}'
                model_svm.save_model(svm_model_path)
                self.log_message("Training SVM model... [COMPLETED]", "success")
                self.log_message(f"SVM model saved to '{svm_model_path}'", "success")

                if self.stop_event.is_set() or self.app_closing:
                    self.log_message("Processing stopped by user.", "error")
                    return

                self.log_message("Process completed successfully!", "success")
                self.root.after(0, lambda: messagebox.showinfo("Success", "Processed successfully!!!"))
            else:
                self.log_message("No valid files found for preprocessing.", "error")
                return
        except Exception as e:
            self.log_message(f"Error: An error occurred: {e}", "error")
        finally:
            self.processing = False
            if not self.app_closing:
                self.start_button.config(text="Start", bg="light green")


if __name__ == "__main__":
    root = tk.Tk()
    app = DataPreprocessor(root)
    root.mainloop()
