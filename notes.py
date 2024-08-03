import tkinter as tk
import customtkinter
import sqlite3

import time
import os
import zipfile

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

# if __name__ == '__main__':
#     zipf = zipfile.ZipFile('Python.zip', 'w', zipfile.ZIP_DEFLATED)
#     zipdir('tmp/', zipf)
#     zipf.close()

def db_start():
    global conn, cur

    conn = sqlite3.connect('notes_db')
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, note TEXT)""")

def save_note():
    note = note_entry.get()
    cur.execute("INSERT INTO notes (note) VALUES (?)", (note,))
    conn.commit()
    update_notes_list()
    note_entry.delete(0, customtkinter.END)

def delete_note():
    index = notes_list.curselection()
    if index:
        selected_note = notes_list.get(index)
        cur.execute("DELETE FROM notes WHERE note=?", (selected_note,))
        conn.commit()
        update_notes_list()

def update_notes_list():
    notes_list.delete(0, customtkinter.END)
    cur.execute("SELECT * FROM notes")
    notes = cur.fetchall()
    for note in notes:
        note_text = note[1]
        notes_list.insert(customtkinter.END, note_text)

root = customtkinter.CTk()
root.title("Приложение для заметок")
root.geometry("300x400")
root.resizable(0, 0)

note_label = customtkinter.CTkLabel(root, text="Заметка:")
note_label.pack(pady=5)

note_entry = customtkinter.CTkEntry(root)
note_entry.pack(pady=5)

save_button = customtkinter.CTkButton(root, text="Добавить заметку", command=save_note)
save_button.pack(pady=5)

delete_button = customtkinter.CTkButton(root, text="Удалить заметку", command=delete_note)
delete_button.pack(pady=5)

notes_list = tk.Listbox(root, width=45, height=15)
notes_list.pack(pady=5)

db_start()
update_notes_list()
root.mainloop()
conn.close()
