import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import pandas as pd
import VietnameseTextPreprocessor
import re
from pyvi import ViTokenizer, ViPosTagger


# Function to preprocess text
def text_preprocess(input_path, text):
    # output_path_not_stopwords = '../Dataset/Root/data_preprocessing_not_stopwords.csv'
    # vietnameseTextPreprocessorNotStopwords = VietnameseTextPreprocessor(remove_np=False)
    # vietnameseTextPreprocessorNotStopwords.process_file(input_path, output_path_not_stopwords)
    #
    # path_stopwords_vietnamese = '../Dataset/Stopwords/vietnamese-stopwords-dash.txt'
    # output_path_stopwords_vietnamese = '../Dataset/Root/data_preprocessing_stopwords_vietnamese.csv'
    # vietnameseTextPreprocessorStopwordsVietnamese = VietnameseTextPreprocessor(
    #     path_stopwords=path_stopwords_vietnamese, remove_np=False
    # )
    # vietnameseTextPreprocessorStopwordsVietnamese.process_file(input_path, output_path_stopwords_vietnamese)
    #
    # path_stopwords_project = '../Dataset/Stopwords/stopwords_project.txt'
    # output_path_stopwords_project = '../Dataset/Root/data_preprocessing_stopwords_project.csv'
    # vietnameseTextPreprocessorStopwordsProject = VietnameseTextPreprocessor(
    #     path_stopwords=path_stopwords_project
    # )
    # vietnameseTextPreprocessorStopwordsProject.process_file(input_path, output_path_stopwords_project)

    # Return filtered text
    # You might need to adjust this to return the processed text
    return text.lower()  # Adjust as necessary for your actual preprocessing result


# Function to filter and display VAT numbers
def filter_and_display_vat_nbr(input_path, output_file_path):
    df = pd.read_excel(input_path)
    df['input'] = df['text'].apply(lambda x: text_preprocess(input_path, x))
    df.to_excel(output_file_path, index=False)
    return df


# Tkinter GUI class
class VATNumberApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Preprocessor")

        self.frame = ttk.Frame(root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Helvetica", 13))
        self.style.configure("TEntry", font=("Helvetica", 13))
        self.style.configure("TButton", font=("Helvetica", 13))

        self.file_label = ttk.Label(self.frame, text="Chọn file đầu vào:")
        self.file_label.grid(row=0, column=0, sticky=tk.W)

        self.file_entry = ttk.Entry(self.frame, width=50)
        self.file_entry.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E))

        self.browse_button = ttk.Button(self.frame, text="Browse", command=self.browse_file, width=15)
        self.browse_button.grid(row=0, column=3, sticky=tk.W)

        self.input_column_label = ttk.Label(self.frame, text="Input:")
        self.input_column_label.grid(row=1, column=0, sticky=tk.W, pady=(10, 0))

        self.input_column_entry = ttk.Entry(self.frame, width=23)
        self.input_column_entry.grid(row=1, column=1, sticky=tk.W, pady=(10, 0))

        self.target_column_label = ttk.Label(self.frame, text="Target:")
        self.target_column_label.grid(row=1, column=2, sticky=tk.W, padx=(10, 0), pady=(10, 0))

        self.target_column_entry = ttk.Entry(self.frame, width=23)
        self.target_column_entry.grid(row=1, column=3, sticky=tk.W, pady=(10, 0))

        self.output_label = ttk.Label(self.frame, text="Chọn file lưu kết quả:")
        self.output_label.grid(row=2, column=0, sticky=tk.W)

        self.output_entry = ttk.Entry(self.frame, width=50)
        self.output_entry.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E))

        self.browse_output_button = ttk.Button(self.frame, text="Browse", command=self.browse_output_file, width=15)
        self.browse_output_button.grid(row=2, column=3, sticky=tk.W)

        self.text_widget = tk.Text(self.frame, height=5, width=70)
        self.text_widget.grid(row=3, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(10, 0))

        self.filter_button = ttk.Button(self.frame, text="Start", command=self.filter_vat_nbr)
        self.filter_button.grid(row=4, column=3, sticky=tk.E, pady=(10, 0))

        for child in self.frame.winfo_children():
            child.grid_configure(padx=5, pady=5)

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)

    def browse_output_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx *.xls")])
        if file_path:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, file_path)

    def filter_vat_nbr(self):
        input_file = self.file_entry.get()
        output_file = self.output_entry.get()

        if not input_file or not output_file:
            messagebox.showwarning("Warning", "Vui lòng chọn cả file đầu vào và file lưu kết quả.")
            return

        try:
            df = filter_and_display_vat_nbr(input_file, output_file)
            self.result_label.config(text=f"Đã xử lý thành công. Số lượng dòng: {len(df)}")
        except Exception as e:
            messagebox.showerror("Error", f"Có lỗi xảy ra: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = VATNumberApp(root)
    root.mainloop()
