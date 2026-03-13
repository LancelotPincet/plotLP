#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author        : Lancelot PINCET
# GitHub        : https://github.com/LancelotPincet



# %% Libraries
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Scalebar
def scalebar(self, pixel=1., unit=None, length=None, *, loc='lower right', bar_height_frac=0.015, pad_frac=0.05, color="white", fontsize=10, zorder=5, label_pad=4, **kwargs) :

    ax = self

    # Get image dimensions
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    img_w = abs(xlim[1] - xlim[0]) # width in pixels
    img_h = abs(ylim[1] - ylim[0]) # height in pixels
    x_min, x_max = min(xlim), max(xlim)
    y_min, y_max = min(ylim), max(ylim)

    # Autoselect bar width
    if length is None:
        target_px = img_w * 0.15
        magnitude = 10 ** np.floor(np.log10(target_px * pixel))
        for step in [1, 2, 5, 10]:
            candidate = step * magnitude
            if candidate / pixel <= target_px * 1.5:
                length = candidate
                break
        else:
            length = magnitude
    bar_px = length / pixel # bar length in pixels

    # Bar height
    bar_h  = img_h * bar_height_frac # bar thickness in pixels

    # Bar padding from barder
    pad = min(img_w, img_h) * pad_frac

    # Anchor position
    loc = loc.lower()
    x0 = x_max - pad - bar_px  if "right" in loc else x_min + pad
    y0 = y_max - pad - bar_h   if "lower" in loc else y_min + pad

    # Scale bar rectangle
    bar_rect = mpatches.Rectangle((x0, y0), bar_px, bar_h, linewidth=0, facecolor=color, zorder=zorder)
    ax.add_patch(bar_rect)

    # Label
    label_x = x0 + bar_px / 2
    pt_to_data = (y_max - y_min) / ax.get_window_extent().height * 72 / ax.figure.dpi
    inverted = ax.yaxis_inverted()
    if inverted:
        label_y = y0 - label_pad * pt_to_data   # above bar visually (smaller y)
        va = "top"
    else:
        label_y = y0 + bar_h + label_pad * pt_to_data
        va = "bottom"

    ax.text(label_x, label_y, f"{length:g} {unit}", color=color, fontsize=fontsize, ha="center", va="bottom", zorder=zorder, fontweight="bold")
