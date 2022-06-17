from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=30)
    sequence = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category-list', kwargs={'category': self.pk})

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["sequence", "name"]


class Developer(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField()
    notes = models.TextField(blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Software(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
    developer = models.ForeignKey(Developer, blank=True, null=True, on_delete=models.SET_NULL)
    url = models.URLField(blank=True, null=True)
    version = models.CharField(max_length=20, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    free = models.BooleanField(default=False, blank=True, null=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True, editable=True)
    active = models.BooleanField(default=True, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Software"

