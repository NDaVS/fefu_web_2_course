import threading

threads = []


def run_in_threads(*functions):
    for function in functions:
        thread = threading.Thread(target=function)
        thread.daemon = True
        thread.start()
        threads.append(thread)

    # for thread in threads:
    #     thread.join()
