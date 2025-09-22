import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
from backend import storage
from backend.auth import derive_key

class SecureNotepadApp:
    def __init__(self, root, key):
        self.root = root
        self.key = key
        self.root.title("🔒 Secure Notepad")
        self.root.geometry("700x500")

        # Button bar
        button_frame = ttk.Frame(self.root, padding=10)
        button_frame.pack(fill="x")

        self.add_btn = ttk.Button(button_frame, text="➕ Add Note", command=self.add_note)
        self.add_btn.pack(side="left", padx=5)

        self.view_btn = ttk.Button(button_frame, text="📂 Refresh Notes", command=self.load_notes)
        self.view_btn.pack(side="left", padx=5)

        # Notes list with delete column
        self.notes_list = ttk.Treeview(
            self.root,
            columns=("id", "title", "delete"),
            show="headings",
            height=15
        )
        self.notes_list.heading("id", text="ID")
        self.notes_list.heading("title", text="Title")
        self.notes_list.heading("delete", text="🗑️")

        self.notes_list.column("id", width=50, anchor="center")
        self.notes_list.column("title", width=500, anchor="w")
        self.notes_list.column("delete", width=50, anchor="center")

        self.notes_list.pack(fill="both", expand=True, pady=10)

        # Bind double-click for opening a note
        self.notes_list.bind("<Double-1>", self.open_note)

        # Bind single-click for delete icon
        self.notes_list.bind("<Button-1>", self.check_delete_click)

        # Load notes
        self.load_notes()

    def add_note(self):
        self.open_editor(note_id=None, title="", content="")

    def load_notes(self):
        for i in self.notes_list.get_children():
            self.notes_list.delete(i)
        notes = storage.load_notes(self.key)
        for n in notes:
            self.notes_list.insert("", "end", values=(n[0], n[1], "❌"))

    def check_delete_click(self, event):
        region = self.notes_list.identify_region(event.x, event.y)
        if region != "cell":
            return

        column = self.notes_list.identify_column(event.x)
        if column != "#3":  # delete column
            return

        item = self.notes_list.identify_row(event.y)
        if not item:
            return

        note_id = self.notes_list.item(item)["values"][0]
        confirm = messagebox.askyesno("Confirm Delete", f"Delete note {note_id}?")
        if confirm:
            storage.delete_note(note_id)
            self.load_notes()

    def open_note(self, event):
        selected = self.notes_list.selection()
        if not selected:
            return
        note_id = self.notes_list.item(selected[0])["values"][0]
        note = storage.get_note(note_id, self.key)
        if note:
            self.open_editor(note_id=note[0], title=note[1], content=note[2])
    def open_editor(self, note_id=None, title="", content=""):
        editor = tk.Toplevel(self.root)
        editor.title("📝 Edit Note" if note_id else "📝 New Note")
        editor.geometry("500x400")

        # --- Title frame ---
        title_frame = ttk.Frame(editor, padding=10)
        title_frame.pack(fill="x")
        ttk.Label(title_frame, text="Title:").pack(anchor="w")
        title_entry = ttk.Entry(title_frame)
        title_entry.pack(fill="x", pady=5)
        title_entry.insert(0, title)

        # --- Content frame ---
        content_frame = ttk.Frame(editor, padding=10)
        content_frame.pack(fill="both", expand=True)
        ttk.Label(content_frame, text="Content:").pack(anchor="w")
        text_area = tk.Text(content_frame, wrap="word")
        text_area.pack(fill="both", expand=True, pady=5)
        text_area.insert("1.0", content)

        # --- Buttons frame ---
        button_frame = ttk.Frame(editor, padding=10)
        button_frame.pack(fill="x", side="bottom")

        def save_note():
            new_title = title_entry.get().strip()
            new_content = text_area.get("1.0", "end-1c").strip()
            if not new_title or not new_content:
                messagebox.showwarning("Invalid", "Title and content cannot be empty.")
                return
            if note_id:  # update existing
                storage.update_note(note_id, new_title, new_content, self.key)
                messagebox.showinfo("Updated", "Note updated successfully.")
            else:  # new note
                storage.save_note(new_title, new_content, self.key)
                messagebox.showinfo("Saved", "Note saved successfully.")
            editor.destroy()
            self.load_notes()

        save_btn = ttk.Button(button_frame, text="💾 Save", bootstyle="success", command=save_note)
        save_btn.pack(side="right", padx=5)

        cancel_btn = ttk.Button(button_frame, text="✖ Cancel", bootstyle="secondary", command=editor.destroy)
        cancel_btn.pack(side="right", padx=5)

def start_gui(password):
    salt = b'secure_salt_1234'
    key = derive_key(password, salt)
    storage.init_db()

    root = ttk.Window(themename="cosmo")
    app = SecureNotepadApp(root, key)
    root.mainloop()
