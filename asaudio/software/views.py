from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.db.models.functions import Lower
from django.utils import timezone as tz
from django.http import JsonResponse
from django.urls import reverse_lazy
from django import forms
from django.conf import settings
from .models import Category, Software, Developer


def home(request):
    recent_updates = Software\
        .objects.select_related("developer", "category")\
        .filter(created__gte=tz.now()-tz.timedelta(days=settings.ASA_RECENT_UPDATES_DAYS))\
        .filter(active=True)\
        .order_by("-created")[:settings.ASA_RECENT_UPDATES_MAX]
    context = {
        "recent_updates": recent_updates,
    }
    return render(request, 'home.html', context=context)


class SoftwareListView(ListView):
    model = Software

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset().select_related("developer").order_by(Lower("developer__name"), Lower("name")).filter(active=True)
        if "category" in self.kwargs:
            qs = qs.filter(category=self.kwargs["category"])
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "category" in self.kwargs:
            context["category"] = Category.objects.get(pk=self.kwargs["category"])
        return context


# For retrieving data with autocomplete.js
def get_developers():
    result = Developer.objects.order_by(Lower("name")).values_list("name", flat=True).distinct()
    return JsonResponse({"status": 200, "data": result})


class SearchForm(forms.Form):
    developer = forms.CharField(label="developer", max_length=50, required=False)
    title = forms.CharField(label="software", max_length=50, required=False)


class SearchView(FormView):
    template_name = "software/search.html"
    form_class = SearchForm
    success_url = reverse_lazy("search")

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            cleaned_data = form.cleaned_data
            if cleaned_data["developer"] or cleaned_data["title"]:
                software = Software.objects.filter(active=True)
                if cleaned_data["developer"]:
                    software = software.filter(developer__name__icontains=cleaned_data["developer"])
                if cleaned_data["title"]:
                    software = software.filter(name__icontains=cleaned_data["title"])
                if software.count():
                    software = software.order_by(Lower("developer__name"), "category__sequence", Lower("name"))
                else:
                    software = None
            else:
                software = None

            self.extra_context = {"software": software, "search": True}
        return super().get(request, *args, **kwargs)


class DeveloperView(DetailView):
    model = Developer
    template_name = "software/developer.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["software_list"] = self.object.software_set.all().order_by("category", "name")
        return context


class DeveloperListView(ListView):
    model = Developer
