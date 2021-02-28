from pdf2image import convert_from_path
from tkinter import *
from tkinter import messagebox, filedialog
import os
import tkinter as tk
import json


settings = dict()
#
#persistence in s/w


def load_settings():
    print("ld set")
    settings_file_path = r"C:\Users\Sumit\Onedrive\Desktop\PDFtoImage"
    if not os.path.exists(settings_file_path):
        os.mkdir(settings_file_path)

    with open(settings_file_path+'\\settings.txt', 'r') as file:
        content = file.read()
        settings = json.loads(content)
    return settings


settings = load_settings()
print(settings)


def save_settings(settings):
    settings_file_path = r"C:\Users\Sumit\Onedrive\Desktop\PDFtoImage"
    if not os.path.exists(settings_file_path):
        os.mkdir(settings_file_path)

    with open(settings_file_path+'\\settings.txt', 'w+') as file:
        file.write(json.dumps(settings))
#


def extractor():
    path_to_pdf = e1.get()
    pdf2img(path_to_pdf)


def select_file():
    master.filename = filedialog.askopenfilename(
        initialdir=settings["initialdir"], title="Select file", filetypes=(("pdf files", "*.pdf"), ("all files", "*.*")))
    # initialdir='C:\\' for eg. sets default select dir .. here we are getting this from previously opened folder
    path_to_pdf = master.filename  # r'{}'.format(master.filename)

    # by default askopenfilename uses linux like '/' for win we have to use '\'
    path_to_pdf = path_to_pdf.replace('/', '\\')
    settings["initialdir"] = path_to_pdf
    entry_text.set(path_to_pdf)


def extract_filename(path):
    l = len(path)
    reversed_path = path[::-1]
    found_bs = False
    found_dot = False

    for index, chr in enumerate(reversed_path):
        if chr == '\\':
            index_bs = index
            found_bs = True
        elif chr == '.':
            index_dot = index
            found_dot = True
        elif found_bs and found_dot:
            if index_bs != -1:
                index_bs = l - index_bs
                index_dot = l - index_dot
                return path[index_bs:index_dot-1]
            else:
                return "filename"
    return path


def pdf2img(loc):
    out_path = r"C:\Users\Sumit\Onedrive\Desktop\PDFtoImage"
    if not os.path.exists(out_path):
        os.mkdir(out_path)
    file_name = extract_filename(loc)
    try:
        print(loc)
        images = convert_from_path(
            pdf_path=loc, poppler_path=r"C:\Users\Sumit\OneDrive\Desktop\professor\py3\pdf to img\poppler-21.02.0\Library\bin")
        print("gt here")
        for i in range(len(images)):
            # Save pages as images in the pdf
            images[i].save(out_path+'\\'+file_name +
                           'page' + str(i) + '.jpg', 'JPEG')

    except:
        Results = "❌ wrong PDF !!"
        messagebox.showinfo("Result", Results)
    else:
        Results = "✔ success"
        messagebox.showinfo("Result", Results)


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        print("saving settings..")
        save_settings(settings)
        master.destroy()


if __name__ == "__main__":
    master = Tk()
    Label(master, text="File Location").grid(row=0, sticky=W)
    entry_text = tk.StringVar()

    e1 = Entry(master, textvariable=entry_text)
    e1.grid(row=0, column=1)

    select_file_button = Button(
        master, text='choose file', command=select_file)
    select_file_button.grid(row=0, column=2, columnspan=2,
                            rowspan=2, padx=5, pady=5)

    convert_button = Button(master, text="Convert", command=extractor)
    convert_button.grid(row=0, column=5, columnspan=2,
                        rowspan=2, padx=5, pady=5)

    master.protocol("WM_DELETE_WINDOW", on_closing)

    mainloop()
