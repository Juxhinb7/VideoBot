from langchain_community.llms import Ollama
import logging

llm = Ollama(model="storyteller")


class ContentGenerator:
    __slots__ = ("__model", "__prompt", "__content")

    def __init__(self, model=Ollama(model="storyteller"), **kwargs):
        self.__model = model
        self.__prompt: str = kwargs["prompt"]
        self.__content: str = ""

    def generate_content(self) -> [str]:
        self.__content = llm.invoke(self.__prompt)
        data = self.__content.split("\n\n")
        parts_of_story = [line.strip().split("\n") for line in data]
        cleaned_data = []
        try:
            for part in parts_of_story:
                if not part[0].startswith("Part"):
                    continue
                cleaned_data.append(part)
        except IndexError:
            logging.error("""
            Index out of range. Sometimes this might happen if the content generated from the model either 
            too small or too large to process. Please try again.
            """)
        return cleaned_data
