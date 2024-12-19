from django.urls import path, include
from .views import StoreInitialCsvView, StoreSingleEntryView, DataView #,getview,postview

urlpatterns = [
    path('transformandstorecsv/', StoreInitialCsvView().as_view(), name='transformandstorecsv'),
    path('storesingleentry/', StoreSingleEntryView.as_view(), name='storesingleentry'),
    path('run/', DataView.as_view(), name='runcompanyavailability'),
]
