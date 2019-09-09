from django.urls import reverse
from django.views import View
from django.shortcuts import render, redirect


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'frontend/index.html')

