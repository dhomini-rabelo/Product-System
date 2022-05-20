from Support.Code.actions.Support.django.views import BaseView
from Support.Code.actions.Support.forms.main import validate_form
from Support.Code.actions.shortcuts.form.main import get_form, save_form
from django.shortcuts import render, redirect




class FormView(BaseView):

    def get(self, request):
        if hasattr(self, 'get_every'): self.get_every(request)
        self.tc['form'] = get_form(request, self.form_nickname, self.form_data)
        return render(request, self.template_path, self.tc)

    def post(self, request):
        if hasattr(self, 'post_every'): self.post_every(request)
        validation = validate_form(request.POST, self.form_validation)

        if validation['status'] == 'valid':
            return self.actions(request)

        save_form(request, self.form_nickname, validation['fields'], validation['errors'])
        return redirect(request.path)
        