#!/usr/bin/env python3
'''
This module contains the main window callback handlers and global definitions
'''

#pylint: disable=wrong-import-position
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
#pylint: enable=wrong-import-position
from BoardList import BoardList
from shutil import copy
from time import time

# Define global variables
BOARDS_FILE = ""
BOARDS = None
SELECTED_BOARD = ""

# Define handlers
class FuseelloHandler():

    def __init__(self, guiObjects):
        self.guiObjects = guiObjects

    def on_boardsFile_set(self, fileButton):
        '''
        Handler called when a file is chosen using the ChooseFileButton
        '''
        global BOARDS_FILE
        global BOARDS
        # Get involved objects references
        _PATH_LABEL = self.guiObjects.get_object("main_window-lbl_filePath")
        _FILE_BUTTON = self.guiObjects.get_object("main-window-btn_chooseBoardsFile")
        _COMBO_BOARDS = self.guiObjects.get_object("comboBox_boards_list")
        # Obtain selected file name
        BOARDS_FILE = _FILE_BUTTON.get_filename()
        # Update the label text
        _PATH_LABEL.set_text("  File path: " + BOARDS_FILE)
        # Load the boards into a BoardList object
        BOARDS = BoardList(BOARDS_FILE)
        # Then add all the boards names to the ComboBox
        _COMBO_BOARDS.remove_all()
        for board in BOARDS.getBoardNames():
            _COMBO_BOARDS.append_text(board)

    def on_comboBox_boards_list_changed(self, comboBox):
        '''
        Handler called when the selection of the CheckBoxText is changed
        '''
        global BOARDS
        global SELECTED_BOARD
        # Update selected board text
        SELECTED_BOARD = comboBox.get_active_text()
        # Get the selected board fuses
        _LOW_FUSE, _HIGH_FUSE, _EXTENDED_FUSE = BOARDS.getBoardFuses(SELECTED_BOARD)
        # Get involved objects references
        _ENTRY_LOW_FUSES = self.guiObjects.get_object("entry_low_fuses")
        _ENTRY_HIGH_FUSES = self.guiObjects.get_object("entry_high_fuses")
        _ENTRY_EXTENDED_FUSES = self.guiObjects.get_object("entry_extended_fuses")
        # Set the text in the fuse entries
        _ENTRY_LOW_FUSES.set_text(_LOW_FUSE[0])
        _ENTRY_HIGH_FUSES.set_text(_HIGH_FUSE[0])
        _ENTRY_EXTENDED_FUSES.set_text(_EXTENDED_FUSE[0])

    def on_btn_overwrite_clicked(self, button):
        '''
        Handler called when the 'Overwrite' button is clicked
        '''
        global BOARDS
        global SELECTED_BOARD
        if SELECTED_BOARD is not "":
            # Get involved objects references
            _ENTRY_LOW_FUSES = self.guiObjects.get_object("entry_low_fuses")
            _ENTRY_HIGH_FUSES = self.guiObjects.get_object("entry_high_fuses")
            _ENTRY_EXTENDED_FUSES = self.guiObjects.get_object("entry_extended_fuses")
            # Create a tuple of fuse values from the entry boxes
            _ENTRY_FUSES = (_ENTRY_LOW_FUSES.get_text(), _ENTRY_HIGH_FUSES.get_text(),
                            _ENTRY_EXTENDED_FUSES.get_text())
            # Write fuse values to file
            BOARDS.setBoardFuses(SELECTED_BOARD, _ENTRY_FUSES)

    def on_btn_save_copy_clicked(self, button):
        '''
        Handler called when the 'Save copy' button is clicked
        '''
        global BOARDS_FILE
        global SELECTED_BOARD
        if SELECTED_BOARD is not "":
            # Get current time in milliseconds
            currMillis = str(int(round(time() * 1000)))
            # Copy the original file, appending the timestamp to its name
            copy(BOARDS_FILE, BOARDS_FILE + '_' + currMillis)
            # Call the handler which will write the file
            self.on_btn_overwrite_clicked(button)

if __name__ == "__main__":
    # Load GLADE interface file
    _BUILDER = Gtk.Builder()
    _BUILDER.add_from_file("main_window.glade")
    # Create Instance of main window
    _GUI_MAIN = _BUILDER.get_object("main_window")
    _GUI_MAIN.connect("destroy", Gtk.main_quit)
    _GUI_MAIN.show_all()
    # Connect handlers to GUI
    _BUILDER.connect_signals(FuseelloHandler(_BUILDER))
    # Run GTK main loop
    Gtk.main()