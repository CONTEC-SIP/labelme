import os.path as osp

import numpy as np
import PIL.Image
import imgviz


def lblsave(filename, lbl):
    if osp.splitext(filename)[1] != ".png":
        filename += ".png"
    # Assume label ranses [-1, 254] for int32,
    # and [0, 255] for uint8 as VOC.
    if lbl.min() >= -1 and lbl.max() < 255:
        lbl_pil = PIL.Image.fromarray(lbl.astype(np.uint8), mode="P")
        colormap = imgviz.label_colormap()
        lbl_pil.putpalette(colormap.flatten())
        lbl_pil.save(filename)
    else:
        raise ValueError(
            "[%s] Cannot save the pixel-wise class label as PNG. "
            "Please consider using the .npy format." % filename
        )


def lblreturn(lbl):
    lbl_pil = PIL.Image.fromarray(lbl.astype(np.uint8), mode="P")
    colormap = [[0, 0, 0],
                [255, 0, 0],
                [255, 255, 0],
                [255, 150, 0],
                [0, 0, 255],
                [0, 255, 0],
                [0, 255, 255]]
    lbl_pil.putpalette(np.array(colormap, np.uint8).flatten())

    return lbl_pil
