#!/usr/bin/env python3
'''
This module is used to define a class that will handle the boards.txt file parsing,
discovering each combination of board + MCU, and finding out the bindings with the fuses
'''
import re

REGEX_FIND_BOARDS_CPU = '(?<=\.cpu\.)[a-zA-Z0-9]*(?=\=)'

class BoardList:
    '''
    This class should be instanced by passing the full absolute path to a valid,
    Arduino IDE compatible,  boards.txt file
    '''
    def __init__(self, boardsFile):
        '''
        When the constructor is run, it will poulate the instance dictionary boards
        with each combination of board + MCU as key, and the line number at which was
        found in the file as value
        '''
        # Initialize the instance boards dictionary
        self.boards = {}
        # Keep the file as an instance variable
        self.boardsFile = boardsFile
        # Use the globally defined regular expression string
        global REGEX_FIND_BOARDS_CPU

        lines = []
        with open(boardsFile, "r") as file:
            # Read all file lines into a list
            lines = file.readlines()

        # Used as a line number cursor
        currentLineNumber = 0
        # Currently read board name
        boardName = ""
        # Line number at wich a board name was found
        boardLineNumber = 0
        # Name of the last board found (used to know if a new board is found)
        oldBoardName = ""
        # List of CPUs associated with one board (it is reset whan a new board is found)
        cpuNames = []
        
        def putFoundBoardsToDict():
            '''
            Helper function that will actually populate the boards dictionary,
            adding the board names as keys
            '''
            #print("[%d]" % (boardLineNumber) + '\t' + oldBoardName)
            if len(cpuNames) > 0:
                for cpu in cpuNames:
                    self.boards[oldBoardName + " @ " + cpu[0]] = cpu[1]
                    #print("[%d]" % (cpu[1]) + '\t\t=> ' + cpu[0])
            else:
                self.boards[oldBoardName] = boardLineNumber

        for line in lines:
            if ".name=" in line:
                boardName = line[line.find("=") + 1:-1]
                if boardName != oldBoardName and boardLineNumber > 0:
                    putFoundBoardsToDict()
                oldBoardName = boardName
                boardLineNumber = currentLineNumber
                cpuNames = []
            # Regexp-Foo: find a line wich contains only a word (a-z chars,
            # 0-9 numbers) between .cpu. and =
            elif re.search(REGEX_FIND_BOARDS_CPU, line) is not None:
                cpu = line[line.find("=") + 1:-1]
                cpuNames.append((cpu, currentLineNumber))
            currentLineNumber += 1
        # Run the helper one more time, to add the last found board: this
        # wont trigger in the for loop because boardName == oldBoardName
        putFoundBoardsToDict()

    def getBoardNames(self):
        '''
        Parameters: none

        Returns: a list of board names, from the boards dictionary keys; if the
        dictionary is empty, an empty list is returned
        '''
        if len(self.boards.keys()) > 0:
            return [*self.boards]
        else:
            return []
    
    def getBoardLine(self, boardName):
        '''
        Parameters: String boardName - the name of a board, shoud be a key of the
        boards dictionary

        Returns: the line number at which that board name occurs in the boards file;
        if the parameter does not correspond to a key in the dictionary, -1 is returned
        '''
        if boardName in self.boards:
            return self.boards[boardName]
        else:
            return -1

    def getBoardFuses(self, boardName):
        '''
        Parameters: String boardName - the name of a board, shoud be a key of the
        boards dictionary

        Returns: in order, the three values for the LOW, HIGH and EXTENDED fuses
        (in this order) as tuples of (String value, int lineNumber)
        '''
        global REGEX_FIND_BOARDS_CPU
        lowFuses = ("", )
        highFuses = ("", )
        extendedFuses = ("", )
        currentLineNumber = 0

        lines = []
        with open(self.boardsFile, "r") as file:
            lines = file.readlines()
        startLine = self.getBoardLine(boardName) + 1

        for line in lines[startLine:]:
            if ".name=" in line or re.search(REGEX_FIND_BOARDS_CPU, line) is not None:
                break
            elif ".low_fuses=" in line:
                lowFuses = (line[line.find("=0x") + 3:-1], currentLineNumber + startLine)
            elif ".high_fuses=" in line:
                highFuses = (line[line.find("=0x") + 3:-1], currentLineNumber + startLine)
            elif ".extended_fuses=" in line:
                extendedFuses = (line[line.find("=0x") + 3:-1], currentLineNumber + startLine)
            currentLineNumber += 1

        return lowFuses, highFuses, extendedFuses

    def setBoardFuses(self, boardName, fuseTuple):
        '''
        Parameters: 
        String boardName - the name of a board, shoud be a key of the
        boards dictionary
        fuseTuple = (String lowFuses, String highFuses, String extendedFuses) - tuple
        of the vaulues for the three fuses, as strings

        Returns: none
        '''
        fuses = self.getBoardFuses(boardName)   # ((lowFuses, line), (highFuses, line),
                                                # (extendedFuse, line))
        
        lines = []
        with open(self.boardsFile, "r") as file:
            lines = file.readlines()

        line = lines[fuses[0][1]] # LOW fuses line
        lines[fuses[0][1]] = line[:line.find("=0x") + 3] + fuseTuple[0] + '\n'

        line = lines[fuses[1][1]] # HIGH fuses line
        lines[fuses[1][1]] = line[:line.find("=0x") + 3] + fuseTuple[1] + '\n'

        line = lines[fuses[2][1]] # EXTENDED fuses line
        lines[fuses[2][1]] = line[:line.find("=0x") + 3] + fuseTuple[2] + '\n'

        with open(self.boardsFile, "w") as file:
            file.writelines(lines)