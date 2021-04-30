from django.shortcuts import render

from django.views.generic import TemplateView

class ExtrasView(TemplateView):
    template_name = 'index.html'

    # Context Variables (dictionary)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_statement'] = 'Nice to see you!' # accedemos con {{my_statement}} en el template
        return context

    def say_bye(self): # add this line
        return 'Goodbye' # and this line too!

