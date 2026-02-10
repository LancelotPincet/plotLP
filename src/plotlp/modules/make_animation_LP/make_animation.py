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
from corelp import Path
from matplotlib import pyplot as plt
import imageio
import io
import numpy as np



# %% Function
def make_animation(export_path:str, name=None, fps:float=24., loop:bool=True, pingpong:bool=False, extension:str='.gif', iterator=range, *, extension2animate='.png', array2animate=None, function2animate=None, parameter2animate=None, value2animate=None, dpi:int=300, **kwargs) :
    '''
    This module allows to create animations from plots, chose from animating images from a folder or through live generation with a function
    
    Parameters
    ----------
    export_path : str or pathlib.Path
        Path where to save animation.
    name : str
        name of animation file.
    fps : float
        Animation Frames Per Second.
    loop : bool
        True to loop animation.
    pingpong : bool
        True to make animation back and forth.
    extension2animate : str
        Extension of animated function in folder.
    array2animate : function
        Array to animate.
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
    >>> make_animation(saving_path, "myanimation", function2animate=myplottingfunction, parameter2animate=""myparameter", value2animate=np.linspace(mini,maxi,1000), **kwargs) # from function
    >>> make_animation(saving_path, "myanimation", extension2animate='.tif') # from folder
    '''

    # Path
    export_path = Path(export_path)
    if name is not None : export_path = export_path / name
    export_path = export_path.with_suffix(extension)

    # Animation modalities
    if function2animate is not None :
        function_animation(export_path, fps, loop, pingpong, function2animate, parameter2animate, value2animate, dpi, iterator, **kwargs)
    elif array2animate is not None :
        array_animation(export_path, fps, loop, pingpong, array2animate, iterator)
    else :
        folder_animation(export_path, fps, loop, pingpong, extension2animate, iterator)



def folder_animation(export_path, fps, loop, pingpong, extension2animate, iterator) :
    folder_path = export_path.with_suffix('')

    # List and naturally sort all PNG files
    image_files = [img for img in folder_path.iterdir() if img.suffix == extension2animate]
    if not image_files:
        raise ValueError("No PNG images found in the folder.")
    image_files.sort()
    if pingpong:
        image_files = image_files + image_files[-2:0:-1]

    # Stream images one at a time and save to GIF
    with get_writer(export_path, fps, loop) as writer :
        for file in iterator(image_files):
            frame = imageio.imread(file)
            writer.append_data(frame)



def array_animation(export_path, fps, loop, pingpong, array2animate, iterator) :
    folder_path = export_path.with_suffix('')
    array2animate = np.asarray(array2animate)
    if pingpong:
        array2animate = np.concatenate(
            (array2animate, array2animate[-2:0:-1]),
            axis=0
        )
    

    # Normalize floats → uint8
    if np.issubdtype(array2animate.dtype, np.floating):
        array2animate = np.clip(array2animate, 0, 1)
        array2animate = (array2animate * 255).astype(np.uint8)
    elif array2animate.dtype != np.uint8:
        array2animate = array2animate.astype(np.uint8)

    # Write frames directly
    with get_writer(export_path, fps, loop) as writer:
        for frame in iterator(array2animate):
            writer.append_data(frame)



def function_animation(export_path, fps, loop, pingpong, function2animate, parameter2animate, value2animate, dpi, iterator, **kwargs) :

    # List of parameter
    if parameter2animate is None:
        raise ValueError("parameter2animate must be provided when function2animate is used")
    if pingpong:
        value2animate = np.hstack((value2animate, value2animate[-2:0:-1]))

    # Stream images one at a time and save to GIF
    with get_writer(export_path, fps, loop) as writer :
        for value in iterator(value2animate):
            kwargs[parameter2animate] = value
            fig = function2animate(**kwargs)
            fig.set_dpi(dpi)
            buf = io.BytesIO()
            fig.savefig(buf, format="png", dpi=dpi)
            buf.seek(0)
            frame = imageio.imread(buf)
            writer.append_data(frame)
            plt.close(fig)



def get_writer(export_path, fps, loop) :
    match export_path.suffix :
        case '.mp4' :
           return imageio.get_writer(export_path, fps=fps, codec='libx264', quality=8, format='ffmpeg')
        case '.gif' :
            return imageio.get_writer(export_path, mode='I', fps=fps, loop=0 if loop else 1)
        case _ :
            raise SyntaxError(f'Animation extension not recognized: -->{export_path.suffix}<--')



# %% Test function run
if __name__ == "__main__":
    from corelp import test
    test(__file__)