import os
import threading
import tkinter as tk
import time
from tkinter import ttk
from tkinter import filedialog
from tkinter.ttk import Progressbar
from tkinter.scrolledtext import ScrolledText

def browse_folder():
    folder_path = filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder_path)

def find_files():
    folder_path = folder_entry.get()
    keyword = keyword_entry.get()
    found_files = []

    progress_window = tk.Toplevel(root)
    progress_window.geometry('300x85')
    progress_window.title('Taranıyor...')
    progress_window.resizable(False, False)

    progress_label = tk.Label(progress_window, text='Dosyalar taranıyor...', font=("Helvetica", 10))
    progress_label.pack(pady=10)

    progress_bar = Progressbar(progress_window, orient=tk.HORIZONTAL, length=200, mode='indeterminate')
    progress_bar.pack()

    def search():
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if keyword.lower() in file.lower():
                    found_files.append(os.path.join(root, file))

        progress_window.destroy()

        if len(found_files) > 0:
            result_text.delete(1.0, tk.END)
            for file_path in found_files:
                result_text.insert(tk.END, file_path + '\n')
        else:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, 'Aranan kelimeyi içeren dosya bulunamadı.')

    progress_bar.start()
    threading.Thread(target=search).start()

# Create the tkinter GUI
root = tk.Tk()
root.title('Öğe Bulucu - emmod V1.2')
root.geometry('500x580')
root.resizable(False, False)

#Create and place the widgets
header_label = tk.Label(root, text='Öğe Bulucu by emmod', font=("Helvetica", 20, "bold"))
header_label.pack(pady=20)

#Folder frame
folder_frame = tk.Frame(root)
folder_frame.pack()

folder_label = tk.Label(folder_frame, text='Taranacak klasör:', font=("Helvetica", 10))
folder_label.pack(side=tk.LEFT)

folder_entry = ttk.Entry(folder_frame, width=30, font=("Helvetica", 10))
folder_entry.pack(side=tk.LEFT,)

folder_button = ttk.Button(folder_frame, text='Klasör', style='My.TButton', command=browse_folder)
folder_button.pack(side=tk.RIGHT, padx=10)

#Keyword frame
keyword_frame = tk.Frame(root)
keyword_frame.pack(pady=15)

keyword_label = tk.Label(keyword_frame, text='Taranacak öğelerde geçen isim:', font=("Helvetica", 10))
keyword_label.pack(side=tk.LEFT)

keyword_entry = ttk.Entry(keyword_frame, width=30, font=("Helvetica", 10))
keyword_entry.pack(side=tk.LEFT)

#Search button
search_button = ttk.Button(root, text='Taramayı başlat', style='My.TButton', command=find_files)
search_button.pack(pady=0)

#Results
result_label = tk.Label(root, text='Sonuçlar:', font=("Helvetica", 10))
result_label.pack()

result_frame = tk.Frame(root)
result_frame.pack(pady=10)

result_text = tk.Text(result_frame, width=70, height=24, font=("Helvetica", 8))
result_text.pack(side=tk.LEFT)

scrollbar = tk.Scrollbar(result_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

result_text.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=result_text.yview)

root.mainloop()
