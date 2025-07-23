import subprocess
import os
import sys
import json
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def create_config_gui():
    def save_config():
        config = {
            "personal_info": {
                "nie": nie_entry.get(),
                "name": name_entry.get(),
                "surname": surname_entry.get(),
                "nationality": nationality_entry.get()
            }
        }
        
        try:
            with open("config.json", "w") as f:
                json.dump(config, f, indent=4)
            window.destroy()
            print("Configuration saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {e}")

    # Create main window
    window = tk.Tk()
    window.title("AppointmentChecker Configuration")
    window.geometry("400x350")
    
    # Create and pack a frame
    frame = ttk.Frame(window, padding="20")
    frame.pack(fill=tk.BOTH, expand=True)

    # NIE
    ttk.Label(frame, text="NIE:").pack(fill=tk.X, pady=5)
    nie_entry = ttk.Entry(frame)
    nie_entry.pack(fill=tk.X, pady=5)

    # Name
    ttk.Label(frame, text="Name:").pack(fill=tk.X, pady=5)
    name_entry = ttk.Entry(frame)
    name_entry.pack(fill=tk.X, pady=5)

    # Surname
    ttk.Label(frame, text="Surname:").pack(fill=tk.X, pady=5)
    surname_entry = ttk.Entry(frame)
    surname_entry.pack(fill=tk.X, pady=5)

    # Nationality
    ttk.Label(frame, text="Nationality:").pack(fill=tk.X, pady=5)
    nationality_entry = ttk.Entry(frame)
    nationality_entry.pack(fill=tk.X, pady=5)

    # Save button
    ttk.Button(frame, text="Save Configuration", command=save_config).pack(pady=20)

    window.mainloop()

def build_exe():
    print("Checking configuration...")
    
    # Check if config.json exists
    if not os.path.exists("config.json"):
        print("No configuration file found. Launching configuration GUI...")
        create_config_gui()
    
    if not os.path.exists("config.json"):
        print("Configuration file is required to build the executable.")
        sys.exit(1)

    print("Building executable...")
    try:
        # Install PyInstaller if not already installed
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        
        # Build the executable
        subprocess.run([
            "pyinstaller",
            "--onefile",
            "--clean",
            "--collect-all", "selenium",
            "--collect-all", "undetected_chromedriver",
            "main.py"
        ], check=True)
        
        # Copy config.json to dist folder
        os.makedirs("dist", exist_ok=True)
        import shutil
        shutil.copy2("config.json", "dist/config.json")
        
        print("\nBuild successful!")
        print("The executable and config.json are in the 'dist' folder")
        print("IMPORTANT: Keep config.json in the same folder as the executable when running it!")
        
    except subprocess.CalledProcessError as e:
        print(f"Error during build: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build_exe()
