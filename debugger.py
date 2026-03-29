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
            self.print_err(self.load)
            return False
    
    def open_process(self, pid_t):
        """
        Takes in pid_t of a process and returns a handler to it.
        :param pid_t:
        :return: h_process
        """
        h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, None, pid_t)
        
        if h_process is not None:
            print(f'[*] Successfully obtained process handle for pid: {pid_t}!\n')
            return h_process
        
        else:
            print(f'[*] Unable to obtain process handle for pid: {pid_t}!.\n')
            return False
    
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
            self.print_err(self.attach)
    
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
            self.debugger_active = False
            
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
            self.print_err(self.detach)
            return False
    
    def open_thread(self, tid_t):
        """
        Opens and returns a thread handle for the given thread id.
        :param tid_t:
        :return: h_thread
        """
        h_thread = kernel32.OpenThread(THREAD_ALL_ACCESS, None, tid_t)
        
        if h_thread is not None:
            print(f'[*] Successfully obtained thread handle for tid: {tid_t}!\n')
            return h_thread
        else:
            print(f'[*] Unable to obtain thread handle for tid: {tid_t}!.\n')
            return False
    
    def enumerate_threads(self):
        """
        Creates and returns a list of threads that match the current process id.
        :return: threads
        """
        thread_entry = THREADENTRY32()
        threads = []
        snapshot = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, self.pid_t)
        
        if snapshot is not None:
            thread_entry.dwSize = sizeof(thread_entry)
            success = kernel32.Thread32First(snapshot, byref(thread_entry))
            
            while success:
                if thread_entry.th32OwnerProcessID == self.pid_t:
                    threads.append(thread_entry.th32ThreadID)
                
                success = kernel32.Thread32Next(snapshot, byref(thread_entry))
            
            if kernel32.CloseHandle(snapshot):
                print(f'[*] Successfully gathered threads info into a list!')
                return threads
            else:
                self.print_err(self.enumerate_threads)
                return False
        else:
            self.print_err(self.enumerate_threads)
            return False
    
    def get_thread_context(self, tid_t):
        """
        Populates the thread context with cpu registers for a given thread id.
        :param tid_t:
        :return: context
        """
        context = CONTEXT()
        context.ContextFlags = CONTEXT_FULL | CONTEXT_DEBUG_REGISTERS
        
        h_thread = self.open_thread(tid_t)
        
        if kernel32.GetThreadContext(h_thread, byref(context)):
            kernel32.CloseHandle(h_thread)
            return context
        
        else:
            self.print_err(self.get_thread_context)
            return False
    
    def print_err(self, errored_fun):
        err = kernel32.GetLastError()
        print(f'[*] Error occurred during {errored_fun.__name__} function. Exit Code: {err}\n')