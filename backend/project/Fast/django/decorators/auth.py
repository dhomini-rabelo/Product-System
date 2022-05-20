from ...forms.checks import check_is_logged
from django.shortcuts import redirect



def no_login_required(view_function):
    
    def exec_view_function(*args, **kwargs):
        request = args[0]
        if check_is_logged(request):
            return redirect('/')     
        return view_function(*args, **kwargs)  
    
    return exec_view_function
