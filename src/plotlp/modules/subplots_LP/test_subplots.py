#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Date          : 2025-12-11
# Author        : Lancelot PINCET
# GitHub        : https://github.com/LancelotPincet
# Library       : plotLP
# Module        : subplots

"""
This file allows to test subplots

subplots : Wrapper function defining subplots in a StyledFigure.
"""



# %% Libraries
from corelp import print, debug
from plotlp import subplots, plt
import numpy as np
debug_folder = debug(__file__)



# %% Function test
def test_subplot() :
    '''
    Test subplot function
    '''
    x = np.linspace(-10,10,50)
    y = x**2
    v = np.linspace(-10,10,100)
    X, Y = np.meshgrid(v,v)
    R = np.sqrt(X**2+Y**2)
    img = np.exp(-R**2/2/4**2)

    fig = figure(figsize_fact=(0.5,0.5), darkmode=True)
    fig.axis.plot(x, -y)
    plt.plot(x, y)
    plt.xlabel('x [ua]')
    fig.axis.set_ylabel('y [ua]')
    fig.title = 'test title'
    plt.savefig(path_png = debug_folder / 'plot_png', close=False)
    plt.savefig(path_pdf = debug_folder / 'plot_pdf', close=False)
    plt.savefig(debug_folder / 'plot_all')



# %% Test function run
if __name__ == "__main__":
    from corelp import test
    test(__file__)