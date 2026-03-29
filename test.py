import debugger


def test():
    dbg = debugger.debugger()
    
    #test: dbg.load("C:\\Windows\\SysWOW64\\notepad.exe")
    
    pid_t = input('[+] Enter the desired process ID: ')
    
    print(f'[*] Attaching to given process ID: {pid_t}\n')
    dbg.attach(int(pid_t))
    
    threads = dbg.enumerate_threads()
    # For each thread in the list we want to
    # grab the value of each of the registers
    for thread in threads:
        thread_context = dbg.get_thread_context(thread)
        # Outputs content of those registers
        print(f'[*] Dumping registers for thread ID: {thread}')
        print(f'[**] EIP: {thread_context.Eip}')
        print(f'[**] ESP: {thread_context.Esp}')
        print(f'[**] EBP: {thread_context.Ebp}')
        print(f'[**] EAX: {thread_context.Eax}')
        print(f'[**] EBX: {thread_context.Ebx}')
        print(f'[**] ECX: {thread_context.Ecx}')
        print(f'[**] EDX: {thread_context.Edx}')
        print('[*] END DUMP\n')
    
    print('[*] Detaching from given process ID...\n')
    dbg.detach()


if __name__ == '__main__':
    test()