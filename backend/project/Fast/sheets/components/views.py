from abc import ABC

class AppViews(ABC):

    def create_view(self, name_view, logged=False):
        login = '@login_required\n' if logged else ''
        new_view = [
            f"{login}def {name_view}(request):",
            *self.spaces([
                "# initial flow", 
                "context = dict()", 
                "# main flow",  
                "# end flow",  
                f"return render(request, 'apps/{self.app}/{name_view}.html', context)"
            ], 4),
        ]
        self.views.add_in_end(new_view)
        self.response(f'view {name_view} criada')
            