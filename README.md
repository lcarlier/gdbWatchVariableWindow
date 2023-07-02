# GDB Watch Variable Window
This python script adds a new window containing variables to watch when debugging a program under GDB. 

![Alt text](images/screenshot.png)

# How to install
Clone this repository and add the following line into your ~/.gdbinit (or ~/.gdbrc) file

```
source <pathToThisRepo>/watchVariable.py
tui new-layout watchVariable {-horizontal src 2 watchVariable 1} 2 cmd 1 status 1
layout watchVariable
```

The python script is adding one new TUI window type and 2 user commands `add-variable-to-watch`, `remove-variable-to-watch` (see below)

# How to use
When starting GDB, the layout of the debugger should ressemble to the screenshot (unless you have omited the `layout watchVariable` line).

To add a new variable to watch, use the command `add-variable-to-watch`. The new variable will appear in the `Variables` window.

To remove a variable to watch, use the command `remove-variable-to-watch`.
