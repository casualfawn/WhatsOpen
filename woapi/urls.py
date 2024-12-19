from django.urls import path, include
from .views import StoreInitialCsvView, StoreSingleEntryView, GetOpenCompaniesView, GetAllView #,getview,postview

urlpatterns = [
    path('transformandstorecsv/', StoreInitialCsvView().as_view(), name='transformandstorecsv'),
    path('storesingleentry/', StoreSingleEntryView.as_view(), name='storesingleentry'),
    path('getall/', GetAllView.as_view(), name='getall'),
    path('getcompanyavailability/', GetOpenCompaniesView.as_view(), name='getcompanyavailability'),

]
