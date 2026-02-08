#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Date          : 2026-02-08
# Author        : Lancelot PINCET
# GitHub        : https://github.com/LancelotPincet
# Library       : template_[library]
# Module        : make_animation

"""
This file allows to test make_animation

make_animation : This module allows to create animations from plots
"""



# %% Libraries
from corelp import print, debug
import pytest
from template_[lowerlib] import make_animation
debug_folder = debug(__file__)



# %% Function test
def test_function() :
    '''
    Test make_animation function
    '''
    print('Hello world!')



# %% Instance fixture
@pytest.fixture()
def instance() :
    '''
    Create a new instance at each test function
    '''
    return make_animation()

def test_instance(instance) :
    '''
    Test on fixture
    '''
    pass


# %% Returns test
@pytest.mark.parametrize("args, kwargs, expected, message", [
    #([], {}, None, ""),
    ([], {}, None, ""),
])
def test_returns(args, kwargs, expected, message) :
    '''
    Test make_animation return values
    '''
    assert make_animation(*args, **kwargs) == expected, message



# %% Error test
@pytest.mark.parametrize("args, kwargs, error, error_message", [
    #([], {}, None, ""),
    ([], {}, None, ""),
])
def test_errors(args, kwargs, error, error_message) :
    '''
    Test make_animation error values
    '''
    with pytest.raises(error, match=error_message) :
        make_animation(*args, **kwargs)



# %% Test function run
if __name__ == "__main__":
    from corelp import test
    test(__file__)