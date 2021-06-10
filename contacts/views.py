from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .serializers import *
from rest_framework import viewsets, filters, generics
from rest_framework.views import APIView
from django.db.models import Count
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


class ContactViewSet(viewsets.ModelViewSet):

    """
        API
        сериализация контактов
        Фильтруем пользователей по принадлежности к МОЭК и ДЗО
        вершина дерева МОЭК имеет id 10 в БД
        вершина дерева ДЗО имеет id 170 в БД
    """
    # company = CompanyMPTT.objects.filter(id__in=[1, 2])
    # queryset = Contact.objects.filter(active=True,).order_by('cn')
    serializer_class = ContactSerializerReadOnly
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('cn', 'description__description', 'mail', 'manager__cn', 'company__company', 'company__id')
    ordering_fields = ('cn', 'description__description', 'mail', 'manager__cn')

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        '''my contacts флаг используется для отображения доступных пользователю контактов.'''
        my_contacts = self.request.query_params.get('my', False)
        if my_contacts and my_contacts !='false':
            user_group = self.request.user.groups.all()
            queryset = Contact.objects.filter(active=True, available_to_groups__in=user_group).order_by('cn')
        else:
            queryset = Contact.objects.filter(active=True,).order_by('cn')
        company = self.request.query_params.get('company', None)
        if company is not None and company != '':
            spliter = ',' if ',' in company else None
            company = company.split(spliter)
            '''поиск по всем отмеченым подразделениям'''
            queryset = queryset.filter(company__id__in=company)

            # queryset = queryset.filter(company__id__in=company)\
            #     .annotate(num_attr=Count('company'))\
            #     .filter(num_attr=len(company))
        return queryset


class AddContactViewSet(generics.UpdateAPIView):

    def patch(self, request, pk):
        return JsonResponse(data={'message': 'Not allow'}, status=400, )

    def put(self, request, pk):
        return JsonResponse(data={'message': 'Not allow'}, status=400, )

    def post(self, request):
        user_group = self.request.user.groups.all()[0]
        #serializer = AddContactSerializer(data=request.data, partial=True)

        #if serializer.is_valid():
        contact_object, created = Contact.objects.get_or_create(cn=request.data['cn'], mail=request.data['mail'],
                                                                division=request.data['division'],
                                                                department=request.data['department'],
                                                                active=True)
        contact_object.available_to_groups.add(user_group)
        if request.data['company']:
            company = CompanyMPTT.objects.get(id=request.data['company'][0]['id']).get_ancestors(ascending=True,
                                                                                                 include_self=True)
            for c in company:
                contact_object.company.add(c)
        if request.data['description']:
            description, created = Position.objects.get_or_create(description=request.data['description'],)
            contact_object.description.add(description)

        return JsonResponse(data={'id': contact_object.id}, status=201, )
        #return JsonResponse(data={'message': "wrong parameters"}, status=400, )

    queryset = Contact.objects.filter(active=True, )
    serializer_class = AddContactSerializer


class CompanyViewSet(viewsets.ModelViewSet):

    queryset = CompanyMPTT.objects.filter(id__in=(14, 38))
    serializer_class = CompanyRecursiveModelSerializer


class AddContactToMyContactsViewSet(generics.UpdateAPIView):

    def get_object(self, pk):
        return Contact.objects.get(pk=pk)

    def patch(self, request, pk):
        user_group = self.request.user.groups.all()[0]
        contact_object = self.get_object(pk)
        serializer = AddContactToMyContacts(contact_object, data=request.data,
                                         partial=True)  # set partial=True to update a data partially
        if serializer.is_valid():
            contact_object.available_to_groups.add(user_group)
            return JsonResponse(data=serializer.data, status=201,)
        return JsonResponse(data={'message': "wrong parameters"},  status=400, )

    def put(self, request, pk):
        return JsonResponse(data={'message': 'Not allow'}, status=400, )

    def delete(self, request, pk):
        user_group = self.request.user.groups.all()[0]
        contact_object = self.get_object(pk)
        serializer = AddContactToMyContacts(contact_object, data=request.data,
                                            partial=True)  # set partial=True to update a data partially
        if serializer.is_valid():
            contact_object.available_to_groups.remove(user_group)
            if not contact_object.contact_from_AD:
                contact_object.active = False
                contact_object.save()
            return JsonResponse(data=serializer.data, status=201, )
        return JsonResponse(data={'message': "wrong parameters"}, status=400, )

    queryset = Contact.objects.filter(active=True, )
    serializer_class = AddContactToMyContacts


class MobilePhoneViewSet(viewsets.ModelViewSet):

    queryset = MobilePhone.objects.all()
    serializer_class = MobilePhoneSerializer


class ContactGroupViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        if self.request.user:
            owner = self.request.user.groups.all()[0]
            queryset = ContactGroup.objects.filter(owner=owner).order_by('title')
            return queryset
    serializer_class = ContactGroupSerializer



class ContactGroupEditViewSet(APIView):

    def patch(self, request, pk):
        # serializer = ContactGroup(data=request.data)
        # if serializer.is_valid():
        contact_group = ContactGroup.objects.get(pk=pk)
        contact_to_add = Contact.objects.get(pk=request.data['contact_id'])
        contact_group.contact.add(contact_to_add)
        return JsonResponse(data={'message': "add success"},  status=201)

    def delete(self, request, pk):

        contact_group = ContactGroup.objects.get(pk=pk)
        contact_to_remove = Contact.objects.get(pk=request.data['contact_id'])
        contact_group.contact.remove(contact_to_remove)
        return JsonResponse(data={'message': "remove success"}, status=201)


class AddContactGroup(generics.CreateAPIView):
    def post(self, request, title):
        if self.request.user:
            user_group = self.request.user.groups.all()[0]
            contact_group = ContactGroup(title=title, owner=user_group)
            contact_group.save()
            return JsonResponse(data={'message': "success"}, status=200, )
        return JsonResponse(data={'message': "fail"}, status=500, )


class TextTemplateViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        if self.request.user:
            owner = self.request.user.groups.all()[0]
            queryset = TextTemplate.objects.filter(owner=owner).order_by('title')
            return queryset

    serializer_class = TextTemplateSerializer


class TextTemplateViewSetWrite(viewsets.ModelViewSet):

    def create(self, request):
        if self.request.user:
            user_group = self.request.user.groups.all()[0]
            new_text_template = TextTemplate(title=request.data['title'],
                                             body= request.data['body'],
                                             owner = user_group)
            new_text_template.save()
            return JsonResponse(data={'message': "success"}, status=200, )
        return JsonResponse(data={'message': "fail"}, status=500, )

    def patch(self, request,pk):
        if self.request.user:
            # user_group = self.request.user.groups.all()[0]
            TextTemplate.objects.filter(pk=pk).update(title=request.data['title'],
                                                      body=request.data['body'])
            # text_template_to_edit = TextTemplate.objects.get(pk=pk)

            # text_template_to_edit = TextTemplate(title=request.data['title'],
            #                                  body= request.data['body'],
            #                                  owner = user_group)
            # new_text_template.save()
            return JsonResponse(data={'message': "success"}, status=200, )
        return JsonResponse(data={'message': "fail"}, status=500, )

    queryset = TextTemplate.objects.all().order_by('id')
    serializer_class = TextTemplateSerializerWrite


