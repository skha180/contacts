from django.urls import path
from .views import (
    upload_csv,
    list_contacts,
    export_csv,
    add_contact,
    edit_contact,      # <-- make sure this is imported
    delete_contact     # <-- also import delete if you use it
)

urlpatterns = [
    path('', upload_csv, name='upload_csv'),
    path('list/', list_contacts, name='list_contacts'),
    path('export/', export_csv, name='export_csv'),
    path('add/', add_contact, name='add_contact'),
    path('edit/<int:pk>/', edit_contact, name='edit_contact'),
    path('delete/<int:pk>/', delete_contact, name='delete_contact'),
]
