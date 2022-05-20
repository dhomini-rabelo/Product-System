from abc import ABC

class AppAdmin(ABC):

    def register_admin(self, model_name: str):
        # use admin.site.empty_value_display = '(None)'
        model = model_name.title()
        admin_class = [
            f"\n\n@admin.register({model})\nclass {model}Admin(admin.ModelAdmin):",
            *self.spaces([
                "list_display = '',", "list_display_links = '',", "list_filter = '',",
                "list_per_page = 50", "list_select_related = False # use tuple, default is False",
                "ordering = '',", "actions = None", "prepopulated_fields = {'slug': 'title',}", 
                "search_fields = '', # ^ -> startswith, = -> iexact, @ ->	search, None -> icontains",
            ], 4)
        ]
        self.admin.add_in_end(admin_class)


    def create_abstract_user_admin(self):
        imports = [
            'from django.contrib.auth import admin as auth_admin',
            'from .forms import UserChangeForm, UserCreationForm',
            'from .models import User',
        ]
        user_admin = [
            '\n\n@admin.register(User)',
            'class UserAdmin(auth_admin.UserAdmin):',
            *self.spaces([
                'form = UserChangeForm',
                'add_form = UserCreationForm',
                'model = User',
                'fieldsets = auth_admin.UserAdmin.fieldsets + (',
                '("My fields", {"fields": ("img",)}),',
                ')',
                "list_display = 'first_name', 'username'",
                "list_display_links = 'first_name', 'username'",
            ], 4)
        ]
        self.admin.add_in_start(imports)
        self.admin.add_in_end(user_admin)
