import random
class FontSpoofer:
    def get_fonts(self):
        fonts = ["Arial", "Helvetica", "Times New Roman", "Courier New", "Verdana"]
        random.shuffle(fonts)
        return fonts[:3]
