# **Fuseello**: an Arduino fuse editor

## Purpose

This small program, writte using `Python 3` and `GTK 3` is a tool to read and update the Arduino IDE *boards.txt* file contents.

Since I'm Italian and I love the "fusilli" pasta type, and this program edits the fuses values, I gave it the name "Fuseello"

## Requirements

* Python 3 >= 3.4
* Python GObject library ('gi')
* Python 'shutil' library
* Python regular expression library (re')

## Usage

The interface is organized into "slices" horizontally, based on the steps you wold normally perform using this tool:

1.  Select the *boards.txt* file from the ARduino IDE folder
2.  Choose a specific board with a specific MCU variant (if present)
3.  Check or change the values for the fuses
4.  Save a copy or overwrite the original file

## Known Issues

The following are the known problems with this early release:

- Some board variants have ther LOW fuses register not detected, because of its placement in the boards file (parsing problem)
- Unexpected behaviour when loading unsupported files (exception handling priblem)
- The entry boxes for fuse values accept any character (they do not have an hex-only allowing mask)