import time



def get_time(view_function):

    def run_view_function(*args, **kwargs):
        start = time.time()
        response = view_function(*args, **kwargs)
        end = time.time()
        print(end-start)
        return response

    return run_view_function
