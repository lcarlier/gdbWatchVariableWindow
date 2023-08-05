import re

import sys, os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

from watchCommon import tui_scrollable_window

variable_to_watch=[]

class watch_variable_window(tui_scrollable_window):

    def __init__(self, tui_window):
        super(watch_variable_window, self).__init__(tui_window, "Variables")
        self.whatisRE = re.compile(r"type = (.*)")

    def getPrintVar(self, varName):
        typeStr = ""
        addrOf = None
        try:
            varValue = gdb.parse_and_eval(varName);
            typeStr = gdb.execute(f"whatis {varName}", from_tty=False, to_string=True)
            result = self.whatisRE.match(typeStr)
            typeStr = result[1]
        except gdb.error as gdbError:
            return f" {varName} = {gdbError}"

        code = varValue.type.code
        if(code == gdb.TYPE_CODE_PTR or code == gdb.TYPE_CODE_REF):
            addrOf = varValue
            varValue = varValue.referenced_value()
            typeStr = f"{typeStr} ({addrOf})"
        
        try:
            return f" {typeStr}: {varName} = {varValue}"
        except gdb.MemoryError as memoryError:
            return f" {typeStr}: {varName} = {memoryError}"

    def formatVar(self, varStr):
        finalStr = ""
        indentStr = "  "
        curIdent = 0
        for c in varStr:
            if c == "{":
                curIdent += 1
                finalStr += f"{{\n {curIdent * indentStr}"
            elif c == "}":
                curIdent -= 1
                finalStr += f"\n {curIdent * indentStr}}}"
            elif c == ",":
                # Don't add the ' ' character after the carriage return because the
                # representation from GDB already has it
                finalStr += f",\n{curIdent * indentStr}"
            else:
                finalStr += c
        return finalStr

    def rendercb(self, fromScroll):
        allLines = []

        for varToWatch in variable_to_watch:
            formatedVar = self.formatVar(self.getPrintVar(varToWatch))
            lines = formatedVar.split("\n")
            for line in lines:
                allLines.append(line)

        self.printview(allLines)

gdb.register_window_type('watchVariable', watch_variable_window)

class AddVarToWatch(gdb.Command):
    def __init__(self):
        super(AddVarToWatch, self).__init__("add-variable-to-watch", gdb.COMMAND_USER)

    def complete(self, text, word):
        return gdb.COMPLETE_SYMBOL

    def invoke(self, args, from_tty):
        if len(args) == 0:
            print(f"One argument is needed")
            return
        if len(args.split(" ")) != 1:
            print(f"Expected 1 parameter only {args}")
            return
        variable_to_watch.append(args)

AddVarToWatch()

class RemoveVarToWatch(gdb.Command):
    def __init__(self):
        super(RemoveVarToWatch, self).__init__("remove-variable-to-watch", gdb.COMMAND_USER)

    def complete(self, text, word):
        return gdb.COMPLETE_SYMBOL

    def invoke(self, args, from_tty):
        if len(args) == 0:
            print(f"One argument is needed")
            return
        if len(args.split(" ")) != 1:
            print(f"Expected 1 parameter only {args}")
            return
        try:
            variable_to_watch.remove(args)
        except ValueError:
            print(f"{args} does not exists")

RemoveVarToWatch()
