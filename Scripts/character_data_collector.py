import os
import tkinter as tk
from tkinter import scrolledtext, messagebox

class ToolTip(object):
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.id = None
        self.x = self.y = 0
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
    
    def enter(self, event=None):
        self.schedule()
    
    def leave(self, event=None):
        self.unschedule()
        self.hidetip()
    
    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(500, self.showtip)
    
    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)
    
    def showtip(self, event=None):
        x, y, _cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + cy + self.widget.winfo_rooty() + 25
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()

def save_content(character_name, section, content):
    directory = "character_data"
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_name = os.path.join(directory, f"{character_name}_{section}.txt")
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Content for {character_name} ({section}) saved to {file_name}")

def process_content(character_name, content_dict):
    for section, content in content_dict.items():
        save_content(character_name, section, content.strip())

def on_submit():
    character_name = entry_character_name.get().strip()
    content_dict = {
        "Overview": text_overview.get("1.0", tk.END).strip(),
        "Starter_Guide": text_starter_guide.get("1.0", tk.END).strip(),
        "Combos": text_combos.get("1.0", tk.END).strip(),
        "Strategy_Guide": text_strategy.get("1.0", tk.END).strip()
    }

    if not character_name:
        messagebox.showerror("Error", "Character name cannot be empty")
        return

    if not any(content_dict.values()):
        messagebox.showerror("Error", "All content fields are empty. Please provide some content.")
        return

    process_content(character_name, content_dict)
    messagebox.showinfo("Success", f"Content for {character_name} has been processed and saved.")
    entry_character_name.delete(0, tk.END)
    text_overview.delete("1.0", tk.END)
    text_starter_guide.delete("1.0", tk.END)
    text_combos.delete("1.0", tk.END)
    text_strategy.delete("1.0", tk.END)

# Set up the GUI
root = tk.Tk()
root.title("Character Data Collector")

# Character name input
label_character_name = tk.Label(root, text="Character Name:")
label_character_name.pack()

entry_character_name = tk.Entry(root, width=50)
entry_character_name.pack()
ToolTip(entry_character_name, "Enter the name of the character (e.g., Johnny).")

# Overview input
label_overview = tk.Label(root, text="Overview:")
label_overview.pack()

text_overview = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=10)
text_overview.pack()
ToolTip(text_overview, "Paste the overview content here.")

# Starter Guide input
label_starter_guide = tk.Label(root, text="Starter Guide:")
label_starter_guide.pack()

text_starter_guide = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=10)
text_starter_guide.pack()
ToolTip(text_starter_guide, "Paste the starter guide content here.")

# Combos input
label_combos = tk.Label(root, text="Combos:")
label_combos.pack()

text_combos = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=10)
text_combos.pack()
ToolTip(text_combos, "Paste the combos content here.")

# Strategy Guide input
label_strategy = tk.Label(root, text="Strategy Guide:")
label_strategy.pack()

text_strategy = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=10)
text_strategy.pack()
ToolTip(text_strategy, "Paste the strategy guide content here.")

# Submit button
button_submit = tk.Button(root, text="Submit", command=on_submit)
button_submit.pack()
ToolTip(button_submit, "Click to process and save the content.")

# Run the GUI
root.mainloop()
