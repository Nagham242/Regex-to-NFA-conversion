import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageGrab
from regex_to_nfa import regex_to_nfa

def draw_nfa(nfa, canvas, state_ids):
    canvas.delete("all")
    coords = {}
    radius = 25
    spacing_x = 140
    spacing_y = 160
    base_y = 160
    x_start = 80

    sorted_states = sorted(state_ids.items(), key=lambda x: int(x[1][1:]))
    for i, (state, sid) in enumerate(sorted_states):
        coords[sid] = (x_start + i * spacing_x, base_y)

    # Dynamically update the canvas scroll region to fit everything
    canvas.config(scrollregion=(0, 0, x_start + len(coords) * spacing_x, base_y + 400))

    for sid, (cx, cy) in coords.items():
        if sid == state_ids[nfa.accept]:
            color = "#fff9c4"  # pastel yellow
            outline = "#fdd835"
        elif sid == state_ids[nfa.start]:
            color = "#4caf50"
            outline = "#2e7d32"
        else:
            color = "#f3e5f5"
            outline = "#8e24aa"

        canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius,
                           fill=color, outline=outline, width=3)
        canvas.create_text(cx, cy, text=sid, font=("Helvetica", 11, "bold"), fill="#212121")

    visited = set()
    epsilon_offset = 0

    def draw_edges(state):
        nonlocal epsilon_offset
        sid = state_ids[state]
        if state in visited:
            return
        visited.add(state)

        for symbol, targets in state.transitions.items():
            for t in targets:
                tid = state_ids[t]
                x1, y1 = coords[sid]
                x2, y2 = coords[tid]
                mx, my = (x1 + x2) // 2, (y1 + y2) // 2 - 20
                canvas.create_line(x1, y1, mx, my, x2, y2, smooth=True, arrow=tk.LAST,
                                   fill="#6a1b9a", width=2)
                canvas.create_text(mx, my - 10, text=symbol, font=("Helvetica", 9, "bold"), fill="#6a1b9a")
                draw_edges(t)

        for t in state.epsilon:
            tid = state_ids[t]
            x1, y1 = coords[sid]
            x2, y2 = coords[tid]
            level = epsilon_offset % 4 + 1
            offset = level * 25 + 30
            mx, my = (x1 + x2) // 2, base_y - offset
            canvas.create_line(x1, y1, mx, my, x2, y2, smooth=True, arrow=tk.LAST,
                               dash=(4, 2), fill="#ab47bc", width=2)
            canvas.create_text(mx, my - 10, text='ε', font=("Helvetica", 9, "bold"), fill="#ab47bc")
            epsilon_offset += 1
            draw_edges(t)

    draw_edges(nfa.start)

def export_as_png(canvas):
    try:
        # Get the full canvas size (manually calculated)
        width = canvas.winfo_width()
        height = canvas.winfo_height()

        # Get the canvas coordinates and ensure everything is visible
        x = canvas.winfo_rootx()
        y = canvas.winfo_rooty()

        # Ensure that the canvas is big enough to capture everything
        canvas.update_idletasks()  # Make sure everything is rendered

        # Capture the entire content of the canvas
        filepath = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")])
        if filepath:
            image = ImageGrab.grab((x, y, x + width, y + height))
            image.save(filepath)
            messagebox.showinfo("Success", f"NFA image saved as {filepath}")
    except Exception as e:
        messagebox.showerror("Export Failed", f"Failed to export image:\n{e}")


def main():
    def convert():
        regex = entry.get()
        try:
            nfa = regex_to_nfa(regex)
            state_ids = {}
            state_count = [0]

            def get_id(state):
                if state not in state_ids:
                    state_ids[state] = f"S{state_count[0]}"
                    state_count[0] += 1
                return state_ids[state]

            visited = set()
            def assign_ids(state):
                if state in visited:
                    return
                visited.add(state)
                get_id(state)
                for t in state.transitions.values():
                    for next_state in t:
                        assign_ids(next_state)
                for next_state in state.epsilon:
                    assign_ids(next_state)

            assign_ids(nfa.start)

            text.delete("1.0", tk.END)
            text.insert(tk.END, f"NFA for regex: {regex}\nStates: {list(state_ids.values())}\nStart: {state_ids[nfa.start]}\nAccept: {state_ids[nfa.accept]}\n")
            draw_nfa(nfa, canvas, state_ids)
        except Exception as e:
            messagebox.showerror("Error", f"Invalid regular expression!\n\n{str(e)}")

    root = tk.Tk()
    root.title("Regex to NFA - Thompson Construction")
    root.configure(bg="#fff0f5")
    root.state("zoomed")  # Maximize window

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TFrame", background="#e1bee7")
    style.configure("TLabel", background="#e1bee7", font=("Helvetica", 11, "bold"))
    style.configure("TButton", background="#d1c4e9", foreground="black", font=("Helvetica", 10, "bold"))
    style.configure("TEntry", padding=6)

    # Root layout
    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)

    frame = ttk.Frame(root, padding="15")
    frame.grid(row=0, column=0, sticky="ew")
    frame.columnconfigure(1, weight=1)

    # Row with input, convert, export buttons
    ttk.Label(frame, text="Enter Regular Expression:").grid(row=0, column=0, sticky="w", padx=5)
    entry = ttk.Entry(frame, font=("Helvetica", 11))
    entry.grid(row=0, column=1, sticky="ew", padx=5)
    
    convert_btn = ttk.Button(frame, text="Convert to NFA", command=convert)
    convert_btn.grid(row=0, column=2, sticky="ew", padx=5)
    
    export_btn = ttk.Button(frame, text="Export as PNG", command=lambda: export_as_png(canvas))
    export_btn.grid(row=0, column=3, sticky="ew", padx=5)

    # Output text area
    text = tk.Text(root, height=6, font=("Courier", 10), bg="#f3e5f5", wrap=tk.WORD)
    text.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 10))

    # Canvas Frame with scroll
    canvas_frame = ttk.Frame(root)
    canvas_frame.grid(row=2, column=0, sticky="nsew", padx=15)
    root.rowconfigure(2, weight=1)

    canvas = tk.Canvas(canvas_frame, bg="#ede7f6", height=400)
    canvas.grid(row=0, column=0, sticky="nsew")

    h_scroll = ttk.Scrollbar(canvas_frame, orient="horizontal", command=canvas.xview)
    h_scroll.grid(row=1, column=0, sticky="ew")
    canvas.configure(xscrollcommand=h_scroll.set)

    canvas_frame.columnconfigure(0, weight=1)
    canvas_frame.rowconfigure(0, weight=1)

    root.mainloop()

if __name__ == '__main__':
    main()
