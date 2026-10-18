from src.datamosh import doDatamosh, doMelt
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

def browse_file(entry):
    path = filedialog.askopenfilename(filetypes=[
        ("Video Files", "*.mp4 *.avi *.mov"),
        ("All Files", "*.*")
    ])
    if path:
        entry.delete(0, tk.END)
        entry.insert(0, path)

def browse_save(entry):
    path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 Video", "*.mp4")])
    if path:
        entry.delete(0, tk.END)
        entry.insert(0, path)

def mode_changed(*_):
    mode = mode_var.get()

    for frame in (frame_transition, frame_melt):
        frame.grid_remove()
    
    if mode == "Transition":
        frame_transition.grid(row=3, column=0, padx=10, pady=5, sticky="ew")
    
    else:
        frame_melt.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

def start_processing():
    mode = mode_var.get()
    
    try:
        if mode == "Transition":
            clip1 = entry_clip1.get()
            clip2 = entry_clip2.get()
        
            output = entry_output.get()
            iframe_skip = int(entry_iframe_skip.get())
        
            quality = int(entry_transition_quality.get())
        
            status_var.set("Running Transition Datamosh...")

            root.update_idletasks()
            doDatamosh(clip1, clip2, output, iframe_skip=iframe_skip, quality=quality)
    
        else:
            clip = entry_clip1.get()
            output = entry_output.get()
        
            extend_frames = int(entry_melt_extend.get())
            quality = int(entry_melt_quality.get())
        
            status_var.set("Running Melt Effect...")
        
            root.update_idletasks()
            doMelt(clip, output, extend_frames=extend_frames, quality=quality)
        
        status_var.set("Done!")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        
        status_var.set("Error occurred")

root = tk.Tk()
root.title("MagicJump")
# universal clip 1 (clip2 is selectable only in transition mode and is defined there)
ttk.Label(root, text="Input Clip 1:").grid(row=0, column=0, sticky="w", padx=10)
entry_clip1 = ttk.Entry(root, width=40)
entry_clip1.grid(row=0, column=1)
ttk.Button(root, text="Browse", command=lambda: browse_file(entry_clip1)).grid(row=0, column=2)
# output file selection
ttk.Label(root, text="Output File:").grid(row=1, column=0, sticky="w", padx=10)
entry_output = ttk.Entry(root, width=40)
entry_output.grid(row=1, column=1)
ttk.Button(root, text="Browse", command=lambda: browse_save(entry_output)).grid(row=1, column=2)
# transition header and mode selector
mode_var = tk.StringVar(value="Transition")
ttk.Label(root, text="Mode:").grid(row=2, column=0, sticky="w", padx=10)
mode_menu = ttk.OptionMenu(root, mode_var, "Transition", "Transition", "Melt", command=mode_changed)
mode_menu.grid(row=2, column=1, sticky="w")
# transition settings
frame_transition = ttk.LabelFrame(root, text="Transition Settings")
ttk.Label(frame_transition, text="Clip 2:").grid(row=0, column=0, sticky="w")
entry_clip2 = ttk.Entry(frame_transition, width=40)
entry_clip2.grid(row=0, column=1)
ttk.Button(frame_transition, text="Browse", command=lambda: browse_file(entry_clip2)).grid(row=0, column=2)
ttk.Label(frame_transition, text="I-frame Skip:").grid(row=1, column=0, sticky="w")
entry_iframe_skip = ttk.Entry(frame_transition, width=10)
entry_iframe_skip.insert(0, "5")
entry_iframe_skip.grid(row=1, column=1)
ttk.Label(frame_transition, text="Quality:").grid(row=2, column=0, sticky="w")
entry_transition_quality = ttk.Entry(frame_transition, width=10)
entry_transition_quality.insert(0, "5")
entry_transition_quality.grid(row=2, column=1)
# melt settings
frame_melt = ttk.LabelFrame(root, text="Melt Settings")
ttk.Label(frame_melt, text="Extend Frames:").grid(row=0, column=0, sticky="w")
entry_melt_extend = ttk.Entry(frame_melt, width=10)
entry_melt_extend.insert(0, "40")
entry_melt_extend.grid(row=0, column=1)
ttk.Label(frame_melt, text="Quality:").grid(row=1, column=0, sticky="w")
entry_melt_quality = ttk.Entry(frame_melt, width=10)
entry_melt_quality.insert(0, "5")
entry_melt_quality.grid(row=1, column=1)
# start amd job section
ttk.Button(root, text="Start", command=start_processing).grid(row=4, column=0, columnspan=3, pady=10)
status_var = tk.StringVar(value="nojobs")
ttk.Label(root, textvariable=status_var).grid(row=5, column=0, columnspan=3, pady=5)

def main():
    mode_changed()
    root.mainloop()

if __name__ == "__main__":
    main()