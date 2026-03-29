import debugger


def test():
    dbg = debugger.debugger()
    
    dbg.load('C:\\Windows\\SysWOW64\\notepad.exe')


if __name__ == "__main__":
    test()