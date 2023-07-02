import re

variable_to_watch=[]

class watch_variable_window:
    def __init__(self, tui_window):
        self._tui_window = tui_window
        self._tui_window.title = 'Variables'
        self._before_prompt_listener = lambda : self._before_prompt()
        gdb.events.before_prompt.connect(self._before_prompt_listener)
        self.whatisRE = re.compile(r"type = (.*)")

    def printVar(self, varName):
        typeStr = ""
        addrOf = None
        try:
            varValue = gdb.parse_and_eval(varName);
            typeStr = gdb.execute(f"whatis {varName}", from_tty=False, to_string=True)
            result = self.whatisRE.match(typeStr)
            typeStr = result[1]
        except gdb.error as gdbError:
            self._tui_window.write(f"{varName} = {gdbError}\n");
            return

        code = varValue.type.code
        if(code == gdb.TYPE_CODE_PTR or code == gdb.TYPE_CODE_REF):
            addrOf = varValue
            varValue = varValue.referenced_value()
            typeStr = f"{typeStr} ({addrOf})"
        
        try:
            self._tui_window.write(f"{typeStr}: {varName} = {varValue}\n");
        except gdb.MemoryError as memoryError:
            self._tui_window.write(f"{typeStr}: {varName} = {memoryError}")

    def render(self):
        self._tui_window.erase();
        for varToWatch in variable_to_watch:
            self.printVar(varToWatch)

    def _before_prompt(self):
        self.render()

gdb.register_window_type('watchVariable', watch_variable_window)

class AddVarToWatch(gdb.Command):
    def __init__(self):
        super(AddVarToWatch, self).__init__("add-variable-to-watch", gdb.COMMAND_USER)

    def complete(self, text, word):
        return gdb.COMPLETE_SYMBOL

    def invoke(self, args, from_tty):
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
        if len(args.split(" ")) != 1:
            print(f"Expected 1 parameter only {args}")
            return
        try:
            variable_to_watch.remove(args)
        except ValueError:
            print(f"{args} does not exists")

RemoveVarToWatch()
