from django.urls import path
from .views import StoreView, DataView

urlpatterns = [
    path('transformandstore/', StoreView.as_view(), name='transformandstore'),
    path('run/', DataView.as_view(), name='runcompanyavailability'),
]
