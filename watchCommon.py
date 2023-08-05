import gdb 

class tui_scrollable_window:
    def __init__(self, tui_window, title):
        self._tui_window = tui_window
        self._tui_window.title = title

        self._before_prompt_listener = lambda : self._before_prompt()
        gdb.events.before_prompt.connect(self._before_prompt_listener)

        self.vpos = 0
        self.hpos = 0

    def _before_prompt(self):
        self.render()

    def close(self):
        gdb.events.before_prompt.disconnect(self._before_prompt_listener)

    def vscroll(self, offset):
        self.vpos = max(0, self.vpos + offset)
        self._tui_window.erase()
        self.rendercb(True)

    def hscroll(self, offset):
        self.hpos = max(0, self.hpos + offset)
        self._tui_window.erase()
        self.rendercb(True)

    def render(self):
        self._tui_window.erase()
        self.rendercb(False)

    def printview(self, allLines):
        winWidth = self._tui_window.width
        winHeight = self._tui_window.height
        win = self._tui_window

        maxWidth = 0
        for line in allLines:
            maxWidth = max(maxWidth, len(line))

        hOffset = 0
        if(maxWidth > winWidth):
            hOffset = self.hpos
        else:
            self.hpos = 0

        vOffset = 0
        if(len(allLines) > winHeight):
            vOffset = self.vpos
        else:
            self.vpos = 0

        for line in allLines[vOffset:vOffset + winHeight]:
            if len(line) == 0:
                self._tui_window.write("\n")
                continue
            line = line.replace("\u001b[0m","")
            colorMarkup = ""
            finalOffset = hOffset
            if line[0] == "\u001b":
                markupPos = line.find("m")
                colorMarkup = line[0: markupPos + 1]
                finalOffset = hOffset + markupPos + 1
            self._tui_window.write(f"{colorMarkup}{line[finalOffset:finalOffset + winWidth - 1]}\u001b[0m\n")
