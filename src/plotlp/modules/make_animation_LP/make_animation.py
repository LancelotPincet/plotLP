#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Date          : 2026-02-08
# Author        : Lancelot PINCET
# GitHub        : https://github.com/LancelotPincet
# Library       : plotLP
# Module        : make_animation

"""
This module allows to create animations from plots
"""



# %% Libraries
from pathlib import Path



# %% Function
def make_animation(saving_path:str, animation_file=None, fps:float=24., loop:bool=True, pingpong:bool=False, extension:str='.gif', *, folder2animate=None, extension2animate=None, function2animate=None, parameter2animate=None, value2animate=None, **kwargs) :
    '''
    This module allows to create animations from plots, chose from animating images from a folder or through live generation with a function
    
    Parameters
    ----------
    saving_path : str or pathlib.Path
        Path where to save animation.
    fps : float
        Animation Frames Per Second.
    loop : bool
        True to loop animation.
    pingpong : bool
        True to make animation back and forth.
    folder2animate : str
        name of folder filled of images to animate
    extension2animate : str
        Extension of animated function in folder.
    function2animate : function
        Function to animate.
    parameter2animate : str
        Name of parameter to animate.
    **kwargs : dict
        Other fixed parameter for function, the animated parameter will be ignored.

    Examples
    --------
    >>> from plotlp import make_animation
    ...
    >>> make_animation(saving_path, function2animate=myplottingfunction, parameter2animate=""myparameter", value2animate=np.linspace(mini,maxi,1000), **kwargs) # from function
    >>> make_animation(saving_path, folder2animate=myfolder, extension2animate='.png') # from folder
    '''

    # Path
    saving_path = Path(saving_path)
    if animation_file is not None : saving_path = saving_path / animation_file
    saving_path = saving_path.with_suffix(extension)

    # Animation modes
    if folder2animate is not None :
        folder_animation(saving_path, fps, loop, pingpong, extension)
    elif function2animate is not None :

    return None




# %% Test function run
if __name__ == "__main__":
    from corelp import test
    test(__file__)