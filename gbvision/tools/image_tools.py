def crop(im, x, y, w, h):
    return im[y:y + h, x:x + w, :]
