from django.shortcuts import render
from django.views.generic import ListView, DetailView

from apps.portal.models import Blog


# Create your views here.
class BlogList(ListView):
    model = Blog
    template_name = 'portal/item_list.html'
    context_object_name = 'items'
    paginate_by = 5

class BlogDetail(DetailView):
    model = Blog
    template_name = 'portal/item_detail.html'
    context_object_name = 'item'
