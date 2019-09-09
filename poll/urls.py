from django.urls import re_path
from poll.views import IndexView

urlpatterns = [
    re_path('$', IndexView.as_view(), name='index_view'),
]
