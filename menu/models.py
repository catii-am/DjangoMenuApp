from django.db import models
from django.urls import reverse

class Menu(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, related_name='items', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=200, blank=True)
    named_url = models.CharField(max_length=100, blank=True)

    def get_absolute_url(self):
        if self.named_url:
            return reverse(self.named_url)
        return self.url

    def __str__(self):
        return self.title
