import tkinter

import customtkinter
import logging
from video_generator import VideoGenerator, ArrayLengthMismatchException
from datetime import datetime
from content_generator import ContentGenerator
import glob


def start_gui_app() -> None:
    master = customtkinter.CTk()
    photo = tkinter.PhotoImage(file="logos/tubeShorty3.png")
    master.wm_iconphoto(False, photo)
    master.resizable(False, False)
    master.geometry("600x200")
    master.title("VideoBot")

    logging.info("Program started!")

    def on_generate_video() -> None:
        user_input = prompt.get("1.0", "end-1c")

        logging.info("Initializing the ContentGenerator Object...")
        cg = ContentGenerator(prompt=user_input)
        logging.info("ContentGenerator Object initialized!")

        logging.info("Generating story...")
        generated_content = cg.generate_content()
        logging.info("Story generated!")

        logging.info("Initializing the VideoGenerator Object...")
        vg = VideoGenerator(images=[file for file in glob.glob("images/*.jpg")],
                            display_size=(1080, 1920),
                            video_duration=60)
        logging.info("VideoGenerator Object initialized!")

        logging.info("Applying images...")
        vg.apply_images()
        logging.info("Images applied!")

        logging.info("Generating video...")
        try:
            vg.generate(imageclip_start=[0, 10, 20, 30, 40, 50], with_subtitles=True, font="Arial",
                        font_size=24, color="white", textclip_start=[0, 25],
                        textclip_duration=[25, 50],
                        paragraphs=generated_content)
        except ArrayLengthMismatchException as e:
            logging.error("The program responded with the following error: %s", str(e))
        logging.info("Video generated!")

        logging.info("Saving video...")
        vg.save(f"samples/sample{datetime.now()}.mp4", 10)
        vg.add_audio_to_video_and_save(generated_content)
        logging.info("Video saved!")

    def on_quit() -> None:
        logging.info("Exiting program...")
        master.destroy()
        logging.info("Program exited!")

    customtkinter.CTkLabel(master, text="Prompt:").grid(row=0)
    prompt = customtkinter.CTkTextbox(master, width=500, height=100)

    generate_button = customtkinter.CTkButton(master, text="Generate video", corner_radius=5, command=on_generate_video)
    quit_button = customtkinter.CTkButton(master, text="Quit", corner_radius=5, command=on_quit)
    master.protocol("WM_DELETE_WINDOW", on_quit)

    prompt.grid(row=0, column=1, pady=6, padx=12)
    generate_button.grid(row=3, column=1, pady=6, padx=12)
    quit_button.grid(row=4, column=1, pady=6, padx=12)
    master.mainloop()
