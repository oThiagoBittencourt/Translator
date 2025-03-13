import mss
import pyautogui
import cv2 as cv
import numpy as np

from pytesseract import pytesseract
from googletrans import Translator

# Definição da rota do tesseract.exe
file_tesseract = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
pytesseract.tesseract_cmd = file_tesseract

# API google tradutor
def translate_text(text, dest_lang="pt"):
    translator = Translator()
    return translator.translate(text, dest=dest_lang).text

# Transcrição da imagem e tratamento
def image_to_text(image, monitor):
    tamanho_minimo = (monitor['height'] / 100) * 5

    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

    # Filtrar palavras com base no tamanho da altura da caixa delimitadora
    texto_filtrado = []
    for i, palavra in enumerate(data['text']):
        if len(palavra.strip()) > 0:  # Ignorar palavras vazias
            altura = data['height'][i]
            if altura > tamanho_minimo:
                texto_filtrado.append(palavra)

    text = ' '.join(texto_filtrado)
    return text

# Processo de captura de tela e tratamento de imagem
def get_image():
    w, h = pyautogui.size()
    monitor = {"top": 0, "left": 0, "width": w, "height": h}

    img = None

    with mss.mss() as sct:
        image = sct.grab(monitor)
        image = np.array(image)
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        _, img_thresh = cv.threshold(gray, 150, 255, cv.THRESH_BINARY)
        return {'image': img_thresh, 'monitor': monitor}
    
def translate():
    image = get_image()
    text = image_to_text(image['image'], image['monitor'])
    result = translate_text(text)
    return result