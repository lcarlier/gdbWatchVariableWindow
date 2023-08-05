import copy

import sys, os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

from watchCommon import tui_scrollable_window

class fg:
  black = "\u001b[30m"
  red = "\u001b[31m"
  green = "\u001b[32m"
  yellow = "\u001b[33m"
  blue = "\u001b[34m"
  magenta = "\u001b[35m"
  cyan = "\u001b[36m"
  white = "\u001b[37m"

class util:
  reset = "\u001b[0m"
  bold = "\u001b[1m"

class watch_registers_window(tui_scrollable_window):
    def __init__(self, tui_window):
        super(watch_registers_window, self).__init__(tui_window, "registers")
        self.previousScreen = None
        self.allLinesColors = None

    def rendercb(self, fromScroll):
        allLines = []

        if fromScroll and self.allLinesColors is not None and self.previousScreen:
            for lineIdx in range(len(self.previousScreen)):
                if self.allLinesColors[lineIdx]:
                    allLines.append(f"{fg.green}{self.previousScreen[lineIdx]}{util.reset}")
                else:
                    allLines.append(self.previousScreen[lineIdx])
        else:
            try:
                self.allLinesColors = []
                infoRegisterStr = gdb.execute(f"info registers", from_tty=False, to_string=True)
                allLines = infoRegisterStr.split("\n")
                copyAllLine = copy.deepcopy(allLines)
                if self.previousScreen is not None and len(self.previousScreen) == len(allLines):
                    for lineIdx in  range(len(allLines)):
                        prevLine = self.previousScreen[lineIdx]
                        newLine = allLines[lineIdx]
                        if prevLine != newLine:
                            allLines[lineIdx] = f"{fg.green}{newLine}{util.reset}"
                            self.allLinesColors.append(True)
                        else:
                            self.allLinesColors.append(False)
                self.previousScreen = copyAllLine
            except gdb.error as gdbError:
                allLines.append(" Couldn't execute 'info registers'")

        self.printview(allLines)

gdb.register_window_type('watchRegisters', watch_registers_window)
