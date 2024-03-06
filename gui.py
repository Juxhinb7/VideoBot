from tkinter import *
import customtkinter
import moviepy.editor as mpy
from generate_video import VideoGenerator


def start_gui_app() -> None:
    master = customtkinter.CTk()
    master.resizable(False, False)
    master.geometry("600x500")

    def button_pressed():
        print(prompt.get("1.0", "end-1c"))

    customtkinter.CTkLabel(master, text="Prompt:").grid(row=0)
    prompt = customtkinter.CTkTextbox(master, width=500, height=100)
    button = customtkinter.CTkButton(master, text="Generate video", corner_radius=5, command=button_pressed)

    prompt.grid(row=0, column=1, pady=6, padx=12)
    button.grid(row=3, column=1, pady=6, padx=12)
    master.mainloop()

