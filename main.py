import tkinter as tk
import time
import threading
import random

class TypeSpeedGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Typing Test")
        self.root.geometry("800x600")

        # Read the text from file and split by newlines
        self.texts = open("texts.txt", "r").read().split("\n")

        # Create the UI
        self.frame = tk.Frame(self.root)
        
        # Sample text label
        self.sample_label = tk.Label(self.frame, text=random.choice(self.texts), font=("Helvetica", 18))
        self.sample_label.grid(row=0, column=0, columnspan=2, padx=5, pady=10)

        # Input field
        self.input_entry = tk.Entry(self.frame, width=40, font=("Helvetica", 24))
        self.input_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=10)
        self.input_entry.bind("<KeyRelease>", self.start)  # Bind key release to start typing check

        # Speed label
        self.speed_label = tk.Label(self.frame, text="Speed: \n0.00 CPS\n0.00 CPM\n0.00 WPS\n0.00 WPM", font=("Helvetica", 18))
        self.speed_label.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

        # Reset button
        self.reset_button = tk.Button(self.frame, text="Reset", command=self.reset, font=("Helvetica", 24))
        self.reset_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

        self.frame.pack(expand=True)

        self.counter = 0
        self.running = False
        self.start_time = 0
        self.root.mainloop()

    def start(self, event):
        if not self.running:
            if not event.keysym in ["Shift", "Control", "Alt"]:  # Don't count modifier keys
                self.running = True
                self.start_time = time.time()
                t = threading.Thread(target=self.time_thread)
                t.daemon = True  # Allow thread to exit when the main program exits
                t.start()
                
        # Check if the input matches the sample text
        if not self.sample_label.cget("text").startswith(self.input_entry.get()):
            self.input_entry.config(fg="red")
        else:
            self.input_entry.config(fg="black")
        
        # If text is completely typed, stop
        if self.input_entry.get() == self.sample_label.cget("text")[:-1]:
            self.running = False
            self.input_entry.config(fg="green")

    def time_thread(self):
        while self.running:
            time.sleep(0.1)  # Update every 0.1 seconds
            self.counter += 0.1
            cps = len(self.input_entry.get()) / self.counter
            cpm = cps * 60
            wps = len(self.input_entry.get().split()) / self.counter
            wpm = wps * 60

            # Update the speed label (use after to ensure it's updated on the main thread)
            self.root.after(0, self.update_speed_label, cps, cpm, wps, wpm)

    def update_speed_label(self, cps, cpm, wps, wpm):
        self.speed_label.config(text=f"Speed: \n{cps:.2f} CPS\n{cpm:.2f} CPM\n{wps:.2f} WPS\n{wpm:.2f} WPM")

    def reset(self):
        self.running = False
        self.counter = 0
        self.speed_label.config(text="Speed: \n0.00 CPS\n0.00 CPM\n0.00 WPS\n0.00 WPM")
        self.sample_label.config(text=random.choice(self.texts))
        self.input_entry.delete(0, tk.END)


# Run the GUI
TypeSpeedGUI()
