from backend import storage
from backend.auth import derive_key, generate_salt

def start_cli(password: str):
    # For now, fixed salt (better: store salt securely)
    salt = b'secure_salt_1234'
    key = derive_key(password, salt)

    storage.init_db()

    while True:
        print("\n1. Add Note\n2. View Notes\n3. Exit")
        choice = input("Choose: ")

        if choice == "1":
            title = input("Title: ")
            content = input("Content: ")
            storage.save_note(title, content, key)
            print("Note saved securely.")
        elif choice == "2":
            notes = storage.load_notes(key)
            for n in notes:
                print(f"[{n[0]}] {n[1]} -> {n[2]}")
        elif choice == "3":
            break
        else:
            print("Invalid choice.")
