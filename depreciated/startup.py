import tkinter as tk
from playsound3 import playsound

def startup():
    root = tk.Tk()

    def center_window(root, width, height):
        # Get the screen width and height of the primary monitor
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Calculate the x and y coordinates for the window
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        # Set the geometry of the window
        root.geometry(f"{width}x{height}+{x}+{y}")

    center_window(root, 128, 128)

    root.overrideredirect(True)

    image = tk.PhotoImage(file="bkd.png")
    label = tk.Label(root, image=image)
    label.pack()

    # This is needed to have the sound play and the image display at the same time
    root.after(100, lambda: playsound("jingle.wav"))

    root.after(3000, root.destroy)
    root.mainloop()