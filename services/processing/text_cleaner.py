import re

class TextCleaner:

    @staticmethod
    def clean(text:str)-> str:

        if not text:
            return ""
        # Line Endings
        text = text.replace("\r\n","\n")
        text = text.replace("\r","\n")

        # Space TabSpace 
        text = re.sub(r"[ \t]+", " ", text)
        # Space TabSpace 
        text = re.sub(r"\n{3,}", "\n\n", text)

        text = text.strip()


        return text
