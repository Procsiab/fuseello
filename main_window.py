#!/usr/bin/env python3
'''
This module contains the main window callback handlers and global definitions
'''

from shutil import copy
from time import time
#pylint: disable=wrong-import-position
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
#pylint: enable=wrong-import-position
from BoardList import BoardList

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
        pathLabel = self.guiObjects.get_object("main_window-lbl_filePath")
        fileButton = self.guiObjects.get_object("main-window-btn_chooseBoardsFile")
        comboBoards = self.guiObjects.get_object("comboBox_boards_list")
        # Obtain selected file name
        BOARDS_FILE = fileButton.get_filename()
        # Update the label text
        pathLabel.set_text("  File path: " + BOARDS_FILE)
        # Load the boards into a BoardList object
        BOARDS = BoardList(BOARDS_FILE)
        # Then add all the boards names to the ComboBox
        comboBoards.remove_all()
        for board in BOARDS.getBoardNames():
            comboBoards.append_text(board)

    def on_comboBox_boards_list_changed(self, comboBox):
        '''
        Handler called when the selection of the CheckBoxText is changed
        '''
        global BOARDS
        global SELECTED_BOARD
        # Update selected board text
        SELECTED_BOARD = comboBox.get_active_text()
        # Get the selected board fuses
        lowFuse, highFuse, extendedFuse = BOARDS.getBoardFuses(SELECTED_BOARD)
        # Get involved objects references
        entryLowFuse = self.guiObjects.get_object("entry_low_fuses")
        entryHighFuse = self.guiObjects.get_object("entry_high_fuses")
        entryExtendedFuse = self.guiObjects.get_object("entry_extended_fuses")
        # Set the text in the fuse entries
        entryLowFuse.set_text(lowFuse[0])
        entryHighFuse.set_text(highFuse[0])
        entryExtendedFuse.set_text(extendedFuse[0])

    def __writeEntryValuesToFile__(self):
        '''
        Helper to save fuses values from the entries into the boards file
        '''
        # Get involved objects references
        entryLowFuse = self.guiObjects.get_object("entry_low_fuses")
        entryHighFuse = self.guiObjects.get_object("entry_high_fuses")
        entryExtendedFuse = self.guiObjects.get_object("entry_extended_fuses")
        # Create a tuple of fuse values from the entry boxes
        entryFuses = (entryLowFuse.get_text(), entryHighFuse.get_text(),
                        entryExtendedFuse.get_text())
        # Write fuse values to file
        BOARDS.setBoardFuses(SELECTED_BOARD, entryFuses)

    def on_btn_overwrite_clicked(self, button):
        '''
        Handler called when the 'Overwrite' button is clicked
        '''
        global BOARDS
        global SELECTED_BOARD
        # If a board was selected from the dropdown
        if SELECTED_BOARD is not "":
            # Define and show a warning dialog
            warnDialog = Gtk.MessageDialog(parent=self.guiObjects.get_object("main_window"),
                flags=0, message_type=Gtk.MessageType.WARNING,
                buttons=Gtk.ButtonsType.OK_CANCEL,
                text="You may loose your data!")
            warnDialog.format_secondary_text(
                "You clicked: " + button.get_label() + "\n"
                + "Are you sure you want to overwrite the selected 'boards.txt' file?")
            userChoice = warnDialog.run()
            if userChoice == Gtk.ResponseType.OK:
                self.__writeEntryValuesToFile__()
            # Close the dialog
            Gtk.Widget.destroy(warnDialog);

    def on_btn_save_copy_clicked(self, button):
        '''
        Handler called when the 'Save copy' button is clicked
        '''
        global BOARDS_FILE
        global SELECTED_BOARD
        # If a board was selected from the dropdown
        if SELECTED_BOARD is not "":
            # Get current time in milliseconds
            currMillis = str(int(round(time() * 1000)))
            # Copy the original file, appending the timestamp to its name
            copy(BOARDS_FILE, BOARDS_FILE + '_' + currMillis)
            # Write the original file
            self.__writeEntryValuesToFile__()


if __name__ == "__main__":
    # Load GLADE interface file
    builder = Gtk.Builder()
    builder.add_from_file("main_window.glade")
    # Create Instance of main window
    guiMain = builder.get_object("main_window")
    guiMain.connect("destroy", Gtk.main_quit)
    guiMain.show_all()
    # Connect handlers to GUI
    builder.connect_signals(FuseelloHandler(builder))
    # Run GTK main loop
    Gtk.main()