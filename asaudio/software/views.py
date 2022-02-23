from datetime import datetime, timedelta
from django.shortcuts import render
from django.views.generic.list import ListView
from django.db.models.functions import Lower
from .models import Category, Software


def home(request):
    categories = Category.objects.order_by("sequence")
    recent_updates = Software\
        .objects.select_related("developer", "category")\
        .filter(updated__gte=datetime.today()-timedelta(days=15))\
        .order_by("-updated")[:50]
    context = {
        "categories": categories,
        "recent_updates": recent_updates,
    }
    return render(request, 'home.html', context=context)


class SoftwareListView(ListView):
    model = Software

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs).select_related("developer").order_by(Lower("developer__name"), Lower("name")).filter(active=True)
        if "category" in self.kwargs:
            qs = qs.filter(category=self.kwargs["category"])
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "category" in self.kwargs:
            context["category"] = Category.objects.get(pk=self.kwargs["category"])
        return context


