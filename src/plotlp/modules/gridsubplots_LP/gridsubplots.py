#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Date          : 2026-03-11
# Author        : Lancelot PINCET
# GitHub        : https://github.com/LancelotPincet
# Library       : plotLP
# Module        : gridsubplots

"""
Subplots functions that creates a grid of axis (typically for images plots).
"""



# %% Libraries
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker
import numpy as np
from plotlp import figure



# %% Function
def gridsubplots(nrows, ncols, yticks=None, xticks=None, figsize_ratio=None, **kwargs) :
    '''
    Subplots functions that creates a grid of axis (typically for images plots).
    
    Parameters
    ----------
    nrows : int
        Number of rows in grid.
    ncols : int
        Number of columns in grid.
    yticks : list
        List of string corresponding to y labels.
    xticks : list
        List of string corresponding to x labels.
    figsize_ratio : int
        (x / y) ratio to apply to default figure, if None will use (ncols / nrows).
    **kwargs : dict
        key-ward arguments to pass to plotlp.figure function.

    Returns
    -------
    fig : StyledFigure
        figure object.
    axes : np.array(StyledAxes)
        axes array.

    Examples
    --------
    >>> from plotlp import gridsubplots
    ...
    >>> fig, axes = gridsubplots(2, 3, yticks=['1', '2'], xticks=['1', '2', '3'])
    '''

    figsize_ratio = ncols * 0.93 / nrows if figsize_ratio is None else figsize_ratio
    fig = figure(figsize_ratio=figsize_ratio, **kwargs)
    gs = gridspec.GridSpec(nrows, ncols, hspace=0, wspace=0)  # no space between axes
    axes = np.array([[fig.add_subplot(gs[i, j]) for j in range(ncols)] for i in range(nrows)])
    if xticks is not None and len(xticks) != ncols : raise SyntaxError('xticks do not have the length of ncols')
    if yticks is not None and len(yticks) != nrows : raise SyntaxError('yticks do not have the length of nrows')

    for i in range(nrows):
        for j in range(ncols):
            ax = axes[i, j]
            ax.polish_noborders = False

            # remove ticks everywhere
            ax.xaxis.set_major_locator(ticker.NullLocator())
            ax.yaxis.set_major_locator(ticker.NullLocator())
            ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
            
            # bottom border row
            if i == nrows - 1 and xticks is not None:
                ax.tick_params(bottom=True, labelbottom=True)
                ax.xaxis.set_major_locator(MidpointLocator())
                ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos, label=str(xticks[j]): label))

            # left border column  
            if j == 0 and yticks is not None:
                ax.tick_params(left=True, labelleft=True)
                ax.yaxis.set_major_locator(MidpointLocator())
                ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos, label=str(yticks[i]): label))
        
    return fig, axes



class MidpointLocator(ticker.Locator):
    """Always places a single tick at the midpoint of the current axis limits."""
    def __call__(self):
        vmin, vmax = self.axis.get_view_interval()
        return [(vmin + vmax) / 2]



# %% Test function run
if __name__ == "__main__":
    from corelp import test
    test(__file__)