import tkinter as tk

from screeninfo import get_monitors


class OverlayWindow:
    def __init__(self, main):
        self.main = main

    def open(self) -> None:
        monitors = get_monitors()

        # Compute combined geometry across all monitors (same idea as before)
        total_width = sum([monitor.width for monitor in monitors])
        max_height = max([monitor.height for monitor in monitors])
        min_x = min([monitor.x for monitor in monitors])
        min_y = min([monitor.y for monitor in monitors])

        # Size of the small overlay window
        overlay_width = 420
        overlay_height = 120

        # Center it horizontally, place it in the upper third vertically
        x = min_x + (total_width - overlay_width) // 2
        y = min_y + (max_height - overlay_height) // 4

        self.main.root = tk.Tk()
        self.main.root.overrideredirect(True)  # Remove window decorations
        self.main.root.geometry(f"{overlay_width}x{overlay_height}+{x}+{y}")
        self.main.root.attributes("-topmost", True)
        self.main.root.attributes("-alpha", self.main.config.opacity)

        # Main container
        frame = tk.Frame(self.main.root, bg="black")
        frame.pack(expand=True, fill="both")

        # Message for the user
        text = (
            "CatLock\n\n"
            "Keyboard is locked.\n"
            "Click this box to unlock."
        )
        label = tk.Label(
            frame,
            text=text,
            fg="white",
            bg="black",
            font=("Segoe UI", 11),
            justify="center",
        )
        label.pack(expand=True, fill="both")

        # Only clicks on this small window trigger unlock
        frame.bind("<Button-1>", self.main.unlock_keyboard)
        label.bind("<Button-1>", self.main.unlock_keyboard)

        # Keep your existing keyboard lock behavior
        self.main.lock_keyboard()

        self.main.root.mainloop()
