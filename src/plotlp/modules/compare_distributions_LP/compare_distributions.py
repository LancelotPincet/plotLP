#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Date          : 2026-05-28
# Author        : Lancelot PINCET
# GitHub        : https://github.com/LancelotPincet
# Library       : plotLP
# Module        : compare_distributions

"""
This function create a figure which compares distributions via histograms and scatterplots.
"""



# %% Libraries
import numpy as np
from plotlp import subplots



# %% Function
def compare_distributions(
    *vectors,
    labels=None,
    hue=None,
    npoints=1000,
    bins=64,
    percentile=99,
    bissectrice=False,
    title=None,
):
    """Compare distributions with pairwise scatterplots and diagonal histograms."""
    if len(vectors) < 2:
        raise ValueError("compare_distributions requires at least two vectors")

    vectors = [np.asarray(vector, dtype=np.float32).ravel() for vector in vectors]
    n = len(vectors)

    if labels is None:
        labels = [f"Vector {index + 1}" for index in range(n)]
    labels = list(labels)
    if len(labels) != n:
        raise ValueError("labels length must match the number of vectors")

    if hue is not None:
        hue = np.asarray(hue).ravel()
        expected_size = vectors[0].size
        if any(vector.size != expected_size for vector in vectors):
            raise ValueError("all vectors must have the same size when hue is provided")
        if hue.size != expected_size:
            raise ValueError("hue length must match vector length")
        categories = list(dict.fromkeys(hue.tolist()))
    else:
        categories = [None]

    npoints = int(npoints)
    if npoints < 1:
        raise ValueError("npoints must be >= 1")

    percentile = float(percentile)
    if percentile <= 0 or percentile > 100:
        raise ValueError("percentile must be in (0, 100]")
    q_low = (100 - percentile) / 2
    q_high = 100 - q_low

    global_scatter_limits = None
    if bissectrice:
        finite_all = [values[np.isfinite(values)] for values in vectors]
        finite_all = [values for values in finite_all if values.size]
        if finite_all:
            limits_values = np.concatenate(finite_all)
            low = float(np.nanpercentile(limits_values, q_low))
            high = float(np.nanpercentile(limits_values, q_high))
            if high <= low:
                high = low + 1.0
            global_scatter_limits = (low, high)

    color_map = {category: f"C{index % 10}" for index, category in enumerate(categories)}

    if n == 2:
        figure, axes = subplots(
            2,
            2,
            figsize_ratio=1,
            dpi=100,
            sharex="col",
            gridspec_kw={"width_ratios": [3, 1], "height_ratios": [1, 3]},
        )
        ax_hist_x = axes[0, 0]
        ax_scatter = axes[1, 0]
        ax_hist_y = axes[1, 1]
        axes[0, 1].axis("off")

        x_values, y_values = vectors
        pair_mask = np.isfinite(x_values) & np.isfinite(y_values)
        if hue is None:
            category_masks = [(None, pair_mask)]
        else:
            category_masks = [
                (category, pair_mask & (hue == category)) for category in categories
            ]

        x_finite = x_values[np.isfinite(x_values)]
        y_finite = y_values[np.isfinite(y_values)]
        if x_finite.size:
            if bissectrice and global_scatter_limits is not None:
                _low, _high = global_scatter_limits
                x_bins = np.linspace(_low, _high, int(bins) + 1, dtype=np.float32)
            else:
                x_bins = np.histogram_bin_edges(x_finite, bins=bins)
            for category, mask in category_masks:
                x_mask = mask if hue is None else np.isfinite(x_values) & (hue == category)
                x_cat = x_values[x_mask]
                x_cat = x_cat[np.isfinite(x_cat)]
                if x_cat.size:
                    ax_hist_x.hist(
                        x_cat,
                        bins=x_bins,
                        alpha=0.45,
                        edgecolor=color_map[category],
                        linewidth=0.8,
                        color=color_map[category],
                    )

        if y_finite.size:
            if bissectrice and global_scatter_limits is not None:
                _low, _high = global_scatter_limits
                y_bins = np.linspace(_low, _high, int(bins) + 1, dtype=np.float32)
            else:
                y_bins = np.histogram_bin_edges(y_finite, bins=bins)
            for category, mask in category_masks:
                y_mask = mask if hue is None else np.isfinite(y_values) & (hue == category)
                y_cat = y_values[y_mask]
                y_cat = y_cat[np.isfinite(y_cat)]
                if y_cat.size:
                    ax_hist_y.hist(
                        y_cat,
                        bins=y_bins,
                        alpha=0.45,
                        edgecolor=color_map[category],
                        linewidth=0.8,
                        color=color_map[category],
                        orientation="horizontal",
                    )

        rng = np.random.default_rng(0)
        points_drawn = 0
        for category, mask in category_masks:
            indices = np.flatnonzero(mask)
            if indices.size == 0:
                continue
            sample_size = min(npoints, indices.size)
            sample_indices = rng.choice(indices, size=sample_size, replace=False)
            points_drawn += sample_size
            ax_scatter.scatter(
                x_values[sample_indices],
                y_values[sample_indices],
                s=6,
                alpha=0.35,
                color=color_map[category],
            )

        if points_drawn == 0:
            ax_scatter.text(0.5, 0.5, "No finite paired values", ha="center", va="center")

        ax_scatter.set_xlabel(labels[0])
        ax_scatter.set_ylabel(labels[1])
        ax_scatter.polish_equiscale = True
        ax_hist_x.set_ylabel("Counts")
        ax_hist_y.set_xlabel("Counts")
        ax_hist_x.tick_params(axis="x", labelbottom=False)
        ax_hist_y.tick_params(axis="y", labelleft=False)
        ax_hist_x.polish_grids = True
        ax_hist_y.polish_grids = True

        if bissectrice and np.any(pair_mask):
            low, high = global_scatter_limits
            ax_scatter.plot([low, high], [low, high], "k--", linewidth=1.2)
            ax_scatter.set_xlim(low, high)
            ax_scatter.set_ylim(low, high)
            ax_hist_x.set_xlim(low, high)
            ax_hist_y.set_ylim(low, high)
        elif np.any(pair_mask):
            x_pair = x_values[pair_mask]
            y_pair = y_values[pair_mask]
            x_low = float(np.nanpercentile(x_pair, q_low))
            x_high = float(np.nanpercentile(x_pair, q_high))
            y_low = float(np.nanpercentile(y_pair, q_low))
            y_high = float(np.nanpercentile(y_pair, q_high))
            if x_high <= x_low:
                x_high = x_low + 1.0
            if y_high <= y_low:
                y_high = y_low + 1.0
            ax_scatter.set_xlim(x_low, x_high)
            ax_scatter.set_ylim(y_low, y_high)

        if title is not None:
            figure.title = title
        return figure

    figure, axes = subplots(
        n,
        n,
        figsize_fact=(n / 2, n / 2),
        figsize_ratio=1,
        dpi=100,
        sharex="col",
    )
    rng = np.random.default_rng(0)

    for i in range(n):
        for j in range(n):
            axis = axes[i, j]
            if i < j:
                axis.axis("off")
                continue

            if i == j:
                values = vectors[i]
                finite = values[np.isfinite(values)]
                axis.set_box_aspect(1)
                if finite.size == 0:
                    axis.text(0.5, 0.5, "No finite values", ha="center", va="center")
                else:
                    if bissectrice and global_scatter_limits is not None:
                        _low, _high = global_scatter_limits
                        edges = np.linspace(_low, _high, int(bins) + 1, dtype=np.float32)
                    else:
                        edges = np.histogram_bin_edges(finite, bins=bins)
                    for category in categories:
                        if hue is None:
                            category_values = finite
                        else:
                            category_mask = np.isfinite(values) & (hue == category)
                            category_values = values[category_mask]
                        if category_values.size:
                            axis.hist(
                                category_values,
                                bins=edges,
                                alpha=0.45,
                                edgecolor=color_map[category],
                                linewidth=0.8,
                                color=color_map[category],
                            )
                axis.set_ylabel("Counts")
                axis.polish_grids = True
                if bissectrice and global_scatter_limits is not None:
                    _low, _high = global_scatter_limits
                    axis.set_xlim(_low, _high)
                if i == n - 1:
                    axis.set_xlabel(labels[j])
                else:
                    axis.set_xlabel("")
                    axis.tick_params(axis="x", labelbottom=False)
                continue

            x_values = vectors[j]
            y_values = vectors[i]
            pair_mask = np.isfinite(x_values) & np.isfinite(y_values)
            if hue is None:
                category_masks = [(None, pair_mask)]
            else:
                category_masks = [
                    (category, pair_mask & (hue == category)) for category in categories
                ]

            points_drawn = 0
            for category, mask in category_masks:
                indices = np.flatnonzero(mask)
                if indices.size == 0:
                    continue
                sample_size = min(npoints, indices.size)
                sample_indices = rng.choice(indices, size=sample_size, replace=False)
                points_drawn += sample_size
                axis.scatter(
                    x_values[sample_indices],
                    y_values[sample_indices],
                    s=5,
                    alpha=0.35,
                    color=color_map[category],
                )

            if points_drawn == 0:
                axis.text(0.5, 0.5, "No finite paired values", ha="center", va="center")

            axis.polish_equiscale = True
            if i == n - 1:
                axis.set_xlabel(labels[j])
            else:
                axis.set_xlabel("")
                axis.tick_params(axis="x", labelbottom=False)
            if j == 0:
                axis.set_ylabel(labels[i])
            else:
                axis.set_ylabel("")
                axis.tick_params(axis="y", labelleft=False)

            if bissectrice and np.any(pair_mask):
                low, high = global_scatter_limits
                axis.plot([low, high], [low, high], "k--", linewidth=1.0)
                axis.set_xlim(low, high)
                axis.set_ylim(low, high)
            elif np.any(pair_mask):
                x_pair = x_values[pair_mask]
                y_pair = y_values[pair_mask]
                x_low = float(np.nanpercentile(x_pair, q_low))
                x_high = float(np.nanpercentile(x_pair, q_high))
                y_low = float(np.nanpercentile(y_pair, q_low))
                y_high = float(np.nanpercentile(y_pair, q_high))
                if x_high <= x_low:
                    x_high = x_low + 1.0
                if y_high <= y_low:
                    y_high = y_low + 1.0
                axis.set_xlim(x_low, x_high)
                axis.set_ylim(y_low, y_high)

    if title is not None:
        figure.title = title
    return figure



# %% Test function run
if __name__ == "__main__":
    from corelp import test
    test(__file__)
