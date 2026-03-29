from debugger_defines import *

kernel32 = windll.kernel32


class debugger:
    def __init__(self):
        self.h_process = None
        self.pid_t = None
        self.debugger_active = False
    
    def load(self, path_to_exe):
        
        # dwCreation flag determines how to create the process
        # set creation_flags = CREATE_NEW_CONSOLE if you want
        # to see the calculator GUI
        creation_flags = DEBUG_PROCESS
        
        # instantiate the structs
        startupinfo = STARTUPINFO()
        process_information = PROCESS_INFORMATION()
        
        # The following two options allow the started process
        # to be shown as a separate window. This also illustrates
        # how different settings in the STARTUPINFO struct can affect
        # the debuggee.
        startupinfo.dwFlags = 0x1
        startupinfo.wShowWindow = 0x0
        
        # We then initialize the cb variable in the STARTUPINFO struct
        # which is just the size of the struct itself
        startupinfo.cb = sizeof(startupinfo)
        
        # File could not be found w/out encoding
        exe_path = path_to_exe.encode('utf-8')
        
        print(f'[*] Attempting to launch: {exe_path}\n')
        
        if kernel32.CreateProcessA(exe_path,
                                   None,
                                   None,
                                   None,
                                   None,
                                   creation_flags,
                                   None,
                                   None,
                                   byref(startupinfo),
                                   byref(process_information)):
            
            print('[*] We have successfully launched the process!\n')
            print('[*] PID: %d' % process_information.dwProcessId)
            self.h_process = self.open_process(process_information.dwProcessId)
            return True
        
        else:
            err = kernel32.GetLastError()
            print(f'[*] Error creating process. Exit Code: {err}')
            return False
    
    def open_process(self, pid_t):
        """
        Takes in pid_t of a process and returns a handler to it.
        :param pid_t:
        :return: h_process
        """
        h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid_t)
        if h_process is not None:
            print('[*] We have successfully obtained a process handler!\n')
            return h_process
        
        else:
            print('[*] Unable to obtain process handler!.\n')
            return None
    
    def attach(self, pid_t):
        """
        Tries to attach to the process, if it fails it exits.
        :param pid_t:
        """
        self.h_process = self.open_process(pid_t)
        
        if kernel32.DebugActiveProcess(pid_t):
            self.debugger_active = True
            self.pid_t = int(pid_t)
            self.run()
        
        else:
            print('[*] Unable to attach to the process.\n')
    
    def run(self):
        """
        Poll for debugging events.
        """
        print('[*] Waiting for debug event from process ...\n')
        while self.debugger_active:
            self.get_debug_event()
    
    def get_debug_event(self):
        """
        Waits for a debugging event and handles debug events.
        """
        debug_event = DEBUG_EVENT()
        continue_status = DBG_CONTINUE
        
        if kernel32.WaitForDebugEvent(byref(debug_event), INFINITE):
            # TODO
            # input('[*] TODO: Event Handlers, press enter to continue...\n')
            # self.debugger_active = False
            
            kernel32.ContinueDebugEvent(
                debug_event.dwProcessId,
                debug_event.dwThreadId,
                continue_status)
        
        else:
            print('[*] Debug Event not found.\n')
    
    def detach(self):
        """
        Detaches from the process, if it fails it exits with last error code of that process.
        """
        if kernel32.DebugActiveProcessStop(self.pid_t):
            print('[*] Finished debugging. Exiting...\n')
            return True
        
        else:
            err = kernel32.GetLastError()
            print(f'[*] Error when detaching. Exit Code: {err}\n')
            return False