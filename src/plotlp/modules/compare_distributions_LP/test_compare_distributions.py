#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Date          : 2026-05-28
# Author        : Lancelot PINCET
# GitHub        : https://github.com/LancelotPincet
# Library       : plotLP
# Module        : compare_distributions

"""
This file allows to test compare_distributions

compare_distributions : This function create a figure which compares distributions via histograms and scatterplots.
"""



# %% Libraries
import numpy as np
import pytest
from plotlp import compare_distributions



# %% Function test
def test_two_vectors_returns_figure():
    """Two vectors should return a figure."""
    x = np.arange(20, dtype=np.float32)
    y = x + 1
    figure = compare_distributions(x, y)
    assert figure is not None


def test_multiple_vectors_returns_figure():
    """Three vectors should return a pairwise-plot figure."""
    x = np.arange(30, dtype=np.float32)
    y = x * 2
    z = x * 3
    figure = compare_distributions(x, y, z, bissectrice=True)
    assert figure is not None


def test_requires_at_least_two_vectors():
    """One vector should raise an error."""
    with pytest.raises(ValueError, match="at least two vectors"):
        compare_distributions(np.arange(10))



# %% Test function run
if __name__ == "__main__":
    from corelp import test
    test(__file__)
