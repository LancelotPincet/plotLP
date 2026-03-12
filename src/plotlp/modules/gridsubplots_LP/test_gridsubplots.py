#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Date          : 2026-03-11
# Author        : Lancelot PINCET
# GitHub        : https://github.com/LancelotPincet
# Library       : plotLP
# Module        : gridsubplots

"""
This file allows to test gridsubplots

gridsubplots : Subplots functions that creates a grid of axis (typically for images plots).
"""



# %% Libraries
from corelp import debug
import pytest
from plotlp import gridsubplots
debug_folder = debug(__file__)



# %% Function test
def test_function() :
    '''
    Test gridsubplots function
    '''
    print('Hello world!')



# %% Instance fixture
@pytest.fixture()
def instance() :
    '''
    Create a new instance at each test function
    '''
    return gridsubplots()

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
    Test gridsubplots return values
    '''
    assert gridsubplots(*args, **kwargs) == expected, message



# %% Error test
@pytest.mark.parametrize("args, kwargs, error, error_message", [
    #([], {}, None, ""),
    ([], {}, None, ""),
])
def test_errors(args, kwargs, error, error_message) :
    '''
    Test gridsubplots error values
    '''
    with pytest.raises(error, match=error_message) :
        gridsubplots(*args, **kwargs)



# %% Test function run
if __name__ == "__main__":
    from corelp import test
    test(__file__)