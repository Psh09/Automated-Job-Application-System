import tkinter as tk
from tkinter import filedialog, messagebox
#import yapiipml
from easy_apply_bot import EasyApplyBot  # Assuming the main bot code is in easyapplybot.py

class EasyApplyBotGUI:
    def __init__(self, master):
        self.master = master
        master.title("LinkedIn EasyApplyBot")
        master.geometry("400x500")

        # Username
        tk.Label(master, text="LinkedIn Username:").pack()
        self.username_entry = tk.Entry(master)
        self.username_entry.pack()

        # Password
        tk.Label(master, text="LinkedIn Password:").pack()
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.pack()

        # Phone Number
        tk.Label(master, text="Phone Number:").pack()
        self.phone_entry = tk.Entry(master)
        self.phone_entry.pack()

        # Salary
        tk.Label(master, text="Desired Salary:").pack()
        self.salary_entry = tk.Entry(master)
        self.salary_entry.pack()

        # Rate
        tk.Label(master, text="Desired Rate:").pack()
        self.rate_entry = tk.Entry(master)
        self.rate_entry.pack()

        # Positions
        tk.Label(master, text="Positions (comma-separated):").pack()
        self.positions_entry = tk.Entry(master)
        self.positions_entry.pack()

        # Locations
        tk.Label(master, text="Locations (comma-separated):").pack()
        self.locations_entry = tk.Entry(master)
        self.locations_entry.pack()

        # Resume Upload
        tk.Button(master, text="Upload Resume", command=self.upload_resume).pack()
        self.resume_label = tk.Label(master, text="No file selected")
        self.resume_label.pack()

        # Cover Letter Upload
        tk.Button(master, text="Upload Cover Letter", command=self.upload_cover_letter).pack()
        self.cover_letter_label = tk.Label(master, text="No file selected")
        self.cover_letter_label.pack()

        # Start Button
        tk.Button(master, text="Start Bot", command=self.start_bot).pack()

    def upload_resume(self):
        filename = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if filename:
            self.resume_path = filename
            self.resume_label.config(text=f"Selected: {filename}")

    def upload_cover_letter(self):
        filename = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if filename:
            self.cover_letter_path = filename
            self.cover_letter_label.config(text=f"Selected: {filename}")

    def start_bot(self):
        config = {
            'username': self.username_entry.get(),
            'password': self.password_entry.get(),
            'phone_number': self.phone_entry.get(),
            'salary': self.salary_entry.get(),
            'rate': self.rate_entry.get(),
            'positions': [pos.strip() for pos in self.positions_entry.get().split(',')],
            'locations': [loc.strip() for loc in self.locations_entry.get().split(',')],
            'uploads': {
                'Resume': getattr(self, 'resume_path', ''),
                'Cover Letter': getattr(self, 'cover_letter_path', '')
            }
        }

        try:
            bot = EasyApplyBot(
                config['username'],
                config['password'],
                config['phone_number'],
                config['salary'],
                config['rate'],
                uploads=config['uploads']
            )
            bot.start_apply(config['positions'], config['locations'])
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    gui = EasyApplyBotGUI(root)
    root.mainloop()