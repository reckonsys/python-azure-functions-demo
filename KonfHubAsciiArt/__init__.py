# Thanks to: https://github.com/uvipen/ASCII-generator/blob/master/img2txt.py
import logging
from urllib import request

import azure.functions as func
import cv2
import numpy as np

PRINTABLE = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/()1{}[]?-_+~<>i!lI;:,\"^`'. "  # noqa: E501
NUM_CHARS = len(PRINTABLE)
NUM_COLS = 150


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Ascii Generator triggered')
    src = req.params.get('src')
    if not src:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            src = req_body.get('src')

    if src is None:
        return func.HttpResponse('Please provide a `src` query parameter')

    url_response = request.urlopen(src)
    img_array = np.array(bytearray(url_response.read()), dtype=np.uint8)
    image = cv2.imdecode(img_array, -1)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height, width = image.shape
    cell_width = width / NUM_COLS
    cell_height = 2 * cell_width
    num_rows = int(height / cell_height)
    num_cols = NUM_COLS
    output = ""
    for i in range(num_rows):
        for j in range(num_cols):
            output += PRINTABLE[min(int(np.mean(image[
                int(i * cell_height):min(int((i + 1) * cell_height), height),
                int(j * cell_width):min(int((j + 1) * cell_width), width)])
                * NUM_CHARS / 255), NUM_CHARS - 1)]
        output += "\n"
    return func.HttpResponse(output)
