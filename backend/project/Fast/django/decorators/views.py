from django.http import Http404



def only_get(view_function):
    
    def exec_view_function(*args, **kwargs):
        request = args[0]
        if request.method != 'GET':
            raise Http404    
        return view_function(*args, **kwargs)  
    
    return exec_view_function