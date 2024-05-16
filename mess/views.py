from django.db.models.query import QuerySet
from django.shortcuts import render
from django.contrib.auth import decorators, mixins
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import MessageInfo
from .forms import CreateMessageForm
from pytils.translit import slugify
# Create your views here.


class MessagesListView(mixins.LoginRequiredMixin, ListView):
    model = MessageInfo
    paginate_by = 4
    context_object_name = 'messages'
    template_name = 'messages/messages_list.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('employee')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'messages'
        context['catg_selected'] = 2
        return context
    

class MessageCreateView(mixins.LoginRequiredMixin, CreateView):
    model = MessageInfo
    form_class = CreateMessageForm
    template_name = 'messages/messageinfo_form.html'
    success_url = reverse_lazy('mess:list')
    extra_context = {'title': 'create', 'catg_selected': 2}

    def form_valid(self, form):
        form.instance.employee = self.request.user
        form.instance.slug = f'{slugify(form.instance.employee.pk)}-{slugify(form.instance.title_message)}'
        return super().form_valid(form)
    
class MessageUpdateView(mixins.LoginRequiredMixin, UpdateView):
    model = MessageInfo
    form_class = CreateMessageForm
    template_name = 'messages/messageinfo_form.html'
    context_object_name = 'message'
    success_url = reverse_lazy('mess:list')
    extra_context = {'title': 'update', 'catg_selected': 2}
    
    def form_valid(self, form):
        form.instance.slug = f'{slugify(form.instance.employee.pk)}-{slugify(form.instance.title_message)}'
        return super().form_valid(form)


class MessageDeleteView(mixins.LoginRequiredMixin, DeleteView):
    model = MessageInfo
    template_name = 'messages/message_delete.html'
    context_object_name = 'message'
    success_url = reverse_lazy('mess:list')
    extra_context = {'title': 'update', 'catg_selected': 2}

  
@decorators.login_required
def main_list(request):
    return render(request, 'messages/main.html', {'title': 'main', 'catg_selected': 1})
