#!/usr/bin/env python

from __future__ import print_function

import argparse
import glob
import os
import os.path as osp
import sys

import imgviz
import numpy as np

import labelme


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("input_dir", help="input annotated directory")
    parser.add_argument("output_dir", default='outputs', help="output dataset directory")
    parser.add_argument("--labels", help="labels file")
    parser.add_argument(
        "--noviz", help="no visualization", action="store_true"
    )
    args = parser.parse_args()

    out_dir = osp.join(args.input_dir, args.output_dir)
    out_mask = osp.join(out_dir, 'Mask')
    out_overlap = osp.join(out_dir, 'Overlap')

    if osp.exists(out_dir):
        print("Output directory already exists:", out_dir)
        sys.exit(1)

    if not args.noviz:
        os.makedirs(
            out_overlap
        )
    print("Creating dataset:", args.output_dir)

    class_names = ['none', 'building', 'road', 'street', 'plastic_house', 'farmland', 'forest', 'waterside']
    class_name_to_id = {'none': 0, 'building': 1, 'road': 2, 'street': 3, 'plastic_house': 4, 'farmland': 5,
                        'forest': 6, 'waterside': 7}

    for filename in glob.glob(osp.join(args.input_dir, "*.json")):
        print("Generating dataset from:", filename)

        label_file = labelme.LabelFile(filename=filename)

        base = osp.splitext(osp.basename(filename))[0]
        out_png_file = osp.join(
            out_mask, base + ".png"
        )
        if not args.noviz:
            out_viz_file = osp.join(
                out_overlap,
                base + ".png",
            )

        img = labelme.utils.img_data_to_arr(label_file.imageData)

        lbl, _ = labelme.utils.shapes_to_label(
            img_shape=img.shape,
            shapes=label_file.shapes,
            label_name_to_value=class_name_to_id,
        )
        lbl_pil = labelme.utils.lblreturn(lbl)
        lbl_pil.save(out_png_file)

        colormap = [[0, 0, 0],
                    [255, 0, 0],
                    [255, 255, 0],
                    [150, 150, 0],
                    [255, 150, 0],
                    [0, 0, 255],
                    [0, 255, 0],
                    [0, 255, 255]]

        if not args.noviz:
            viz = imgviz.label2rgb(
                label=lbl,
                img=img,
                font_size=15,
                label_names=class_names,
                colormap=np.array(colormap),
                loc="rb",
            )
            imgviz.io.imsave(out_viz_file, viz)


if __name__ == "__main__":
    main()
