import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import os

def open_main_gui():
    root.destroy()
    subprocess.Popen(["python", "nfa_gui.py"])

root = tk.Tk()
root.title("Regex to NFA Visualizer - Welcome")
root.geometry("700x500")
root.configure(bg="#ffe6f0")  

# Welcome logo
logo_label = tk.Label(root, text="Welcome 🌸", 
                      font=("Helvetica", 30, "bold"), 
                      fg="#a64ca6", bg="#ffe6f0")  
logo_label.pack(pady=(30, 10))
# Logo image
img_path = "C:/Users/DELL/Downloads/RegexToNfa/RegexToNfa/Regx.png"

if os.path.exists(img_path):
    image = Image.open(img_path)
    image = image.resize((250, 250), Image.Resampling.LANCZOS)

    photo = ImageTk.PhotoImage(image)
    label_img = tk.Label(root, image=photo, bg="#ffe6f0")
    label_img.image = photo
    label_img.pack(pady=10)
else:
    tk.Label(root, text="(Image not found)", fg="red", bg="#ffe6f0").pack(pady=10)
# Supported operators description
description_text = """
Supported operators:
  |  : Union (OR)
  .  : Concatenation (implicit, but added automatically)
  *  : Kleene Star (0 or more repetitions)
  +  : Kleene Plus (1 or more repetitions)
  ?  : Optional (0 or 1 repetition)
 [ ] : Character class (e.g., [a-z], [0-9])
  () : Grouping

"""
description_label = tk.Label(root, text=description_text, 
                             font=("Helvetica", 18), 
                             fg="#4b0082", bg="#ffe6f0", justify=tk.LEFT)
description_label.pack(pady=10)

# Start button
tk.Button(root, text="Start Exploring", 
          font=("Helvetica", 15, "bold"),
          bg="#f2ccff", fg="#4b0082", padx=20, pady=8,
          command=open_main_gui).pack(pady=30)
root.state("zoomed")  # Maximize window
root.mainloop()
