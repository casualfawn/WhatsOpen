from django.urls import path, include
from .views import StoreInitialCsvView, StoreSingleEntryView, GetAllView #,getview,postview

urlpatterns = [
    path('transformandstorecsv/', StoreInitialCsvView().as_view(), name='transformandstorecsv'),
    path('storesingleentry/', StoreSingleEntryView.as_view(), name='storesingleentry'),
    path('run/', GetAllView.as_view(), name='runcompanyavailability'),
]
