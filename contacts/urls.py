from django.contrib import admin
from django.urls import path, include

from .views import *

from rest_framework import routers

router = routers.DefaultRouter()
router.register('contact', ContactViewSet, basename='contact')
router.register('company', CompanyViewSet)
router.register('mobile-phone', MobilePhoneViewSet)
router.register('text-template', TextTemplateViewSet, basename='text_template')
router.register('edit-text-template', TextTemplateViewSetWrite, basename='edit_text_template')
router.register('group', ContactGroupViewSet, basename='contact_group')



urlpatterns = [
    path('', include(router.urls)),
    path('add_contact_to_my/<pk>', AddContactToMyContactsViewSet.as_view(), name='add_contact_to_my'),
    path('add-contact-group/<title>', AddContactGroup.as_view(), name='add_contact_group'),
    path('add_new_contact/', AddContactViewSet.as_view(), name='add_new_contact'),
    path('edit-group/<pk>', ContactGroupEditViewSet.as_view(), name='edit_group'),
]