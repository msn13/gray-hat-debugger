import debugger


def test():
    dbg = debugger.debugger()
    
    dbg.load('C:\\Windows\\System32\\calc.exe')


if __name__ == "__main__":
    test()