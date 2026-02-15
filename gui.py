import tkinter as tk
import crypt, startup, re

# Variables
version = "0.0"

# startup.startup()

root = tk.Tk()
root.title(f"bmsg {version}")
root.geometry("500x500")

# Functions
def clipboard(input):
    root.clipboard_clear()
    root.clipboard_append(input)

def get_keys(length):
    keys = str(crypt.generate_keys(length))
    re_output = re.findall(r'\w+\((.*?)\)', keys)
    public_key = re_output[0]
    private_key = re_output[1]
    key_label.configure(text=f"Public Key: {public_key}\nPrivate Key: {private_key}", wraplength=300, font=("default", 5))
    public_copy_button = tk.Button(root, text="Copy Public", command=clipboard(public_key))
    private_copy_button = tk.Button(root, text="Copy Private", command=clipboard(private_key))
    public_copy_button.grid(column=0, row=2)
    private_copy_button.grid(column=0, row=3)

# GUI
frame = tk.Frame(root)
frame.grid()
generate_keys_button = tk.Button(frame, text="Generate Keys", command=lambda: get_keys(1024))
generate_keys_button.grid(column=0, row=0)
key_label = tk.Label(frame, text="No keys generated yet.")
key_label.grid(column=0, row=1)


tk.mainloop()