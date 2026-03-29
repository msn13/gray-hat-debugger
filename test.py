import debugger


def test():
    dbg = debugger.debugger()
    
    dbg.load('C:\\Windows\\SysWOW64\\notepad.exe')
    
    pid_t = input('[+] Enter the desired process ID: ')
    
    print('[*] Attaching to given process ID...')
    dbg.attach(int(pid_t))
    print('Detaching from given process ID...')
    
    if dbg.detach():
        print('[*] Detached from given process ID successfully.')


if __name__ == "__main__":
    test()