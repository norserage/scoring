import threading

def start():
    thread = threading.Thread(target=thread_start)
    thread.start()

def thread_start():
    pass