from PIL import Image
import easyocr


def extract_text_from_image(image_path):

    reader = easyocr.Reader(['en'])

    results = reader.readtext(image_path)

    text = " ".join(
        [result[1] for result in results]
    )

    return text


def load_image(image_path):
    return Image.open(image_path)