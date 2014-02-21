Register Map Viewer
=============

*A python-based tool for reading and writing to registers in ARM Cortex-A running Linux*

This tool is a command-line utility to read and write to registers that are in the system memory map and provides auto-completion features for the field and values you want to write to.

## SVD
ARM defines an SVD (System View Description) file format in its CMSIS
standard as a means for Cortex-M-based chip manufacturers to provide a
common description of peripherals, registers, and register fields. You
can download SVD files for different manufacturers

## Installation instructions

Make sure you have python3 installed with lxml. This tool will not work with python2.

    sudo apt-get install python3-pip
    sudo pip install lxml
    
    cd regmap_viewer
    make all    


    
## Running instructions

    python regmapview.py

## Bugs
There are still some issues with some svd files which are not formatted correctly 

Auto-complete feature is still a bit fidgety. 
