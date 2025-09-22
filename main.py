from frontend.cli import start_cli
from frontend.gui import start_gui

if __name__ == "__main__":
    print("🔒 Secure Notepad")
    print("=================")
    mode = input("Choose interface (1=CLI, 2=GUI): ")

    master_password = input("Enter master password: ")

    if mode == "1":
        start_cli(master_password)
    else:
        start_gui(master_password)
