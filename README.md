![alt text](logos/tubeShorty3.png "Title")
# TubeShorty
This is a user interface-driven software I developed specifically for easily generating YouTube Shorts stories. It utilizes a graphical user interface (GUI) where, upon providing input prompts, you can describe and generate the story along with accompanying video footage, images, and audio through a single button.

### On Linux Platforms
Download the Ollama Platform that makes it easy to host LLMs locally and provides built-in GPU acceleration out of the box
``curl -fsSL https://ollama.com/install.sh | sh``

### On Mac Platforms
Visit the official Ollama page to download the platform on Mac:
``https://ollama.com/download/mac``


### Guide
 Occasionally, an "Index error" may occur when generating story chunks from the AI model, where these chunks are larger than what can be effectively processed. In such instances, you have the option to retry generation by clicking on the "Generate" button again. The project's organization encompasses several folders, including 'audio', 
'images', 'logos', 'logs', and 'samples'.


Within the designated 'audio' directory, will be stored the mp3 files corresponding to each paragraph and the combined audioclip utilized for the final video output.
Inside the 'images' folder, upload your preferred images manually (a total of 6 images with jpg extension are required) since the program only handles text, audio, and video generation, not image 
generation.
Located within the 'logos' directory is the logo file for the desktop application.
Lastly, inside the 'logs' folder resides the program.log file which serves to log essential information aiding in debugging efforts.
In the 'samples' directory, you can find both videos - the first without audio and the second as an audio-included copy 
of the former.
Lastly there is a special file called Modelfile that aids in creating a custom representation of the Ollama Model. After the installation and configuation of Ollama and an LLM Model for it. What is left to do is, to type this command at the terminal:
``ollama create delfini -f Modelfile``.
Make sure to installed all required dependencies in the directory path with: ``pip install -r requirements.txt``.
After this step you are ready to execute the program.
