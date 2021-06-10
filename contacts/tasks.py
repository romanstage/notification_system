import base64
import hashlib
import json
import os
import re

from celery import shared_task
from ldap3 import Server, Connection, SUBTREE

from main.celery import app
from main.settings import AD_SERVER, AD_USER, AD_PASSWORD, AD_SEARCH_TREE
from main.settings import VPN_USER_PHOTO_DIRS
from .models import *


# task for update users from AD
# @app.task
@shared_task
def update_ad_users():
    """
        TO DO:
        Добавить поле "активный" и синхронизировать всех пользователей.

        Снхронизация пользователей AD с базой Contact
        Получем всех активных пользователей из AD.

        Работает через генератор.
        выгружает по 5 пользователей и обрабатывает.

    """
    server = Server(AD_SERVER)
    conn = Connection(server, user=AD_USER, password=AD_PASSWORD)
    """conn.bind() Установка соединения с AD """
    conn.bind()
    """entry_generator генератор поиска пользователей и их атрибутов по фильтру """
    entry_generator = conn.extend.standard.paged_search(AD_SEARCH_TREE,
                                                        '(&(objectCategory=Person) (!(UserAccountControl:1.2.840.113556.1.4.803:=2))(givenName=*)(sn=*))',
                                                        SUBTREE,
                                                        attributes=['cn', 'division', 'company', 'department',
                                                                    'description', 'distinguishedName', 'employeeID',
                                                                    'homeMDB', 'mail', 'manager', 'memberOf', 'mobile',
                                                                    'msExchRBACPolicyLink', 'objectGUID', 'pager', 'l',
                                                                    'physicalDeliveryOfficeName', 'postalCode',
                                                                    'streetAddress', 'sAMAccountName',
                                                                    'telephoneNumber', 'uSNChanged', 'mobile',
                                                                    'lastLogon'],
                                                        paged_size=5,
                                                        generator=True)
    for entry in entry_generator:
        if 'attributes' in entry:
            ent = entry['attributes']
            update = False
            update_fields = ['cn', 'sAMAccountName']
            contact, created = Contact.objects.get_or_create(objectGUID=ent['objectGUID'])
            """Берем пользователя из БД или создаем нового, если нет пользователя с таким id"""
            if not created:
                """Если пользоваетль существует, проверяем изменение его атрибутов по полю uSNChanged"""
                if contact.uSNChanged:
                    if contact.uSNChanged != ent['uSNChanged']:
                        update_fields.append('uSNChanged')
                        contact.uSNChanged = ent['uSNChanged']
                        update = True
                else:
                    update_fields.append('uSNChanged')
                    contact.uSNChanged = ent['uSNChanged']
                    update = True
            else:
                update = True
            """Если это новый пользоваетль или изменились атрибуты уже существующего юзера, переменная update = True"""
            if update:
                """Далее разбираем все атрибуты и сохраняем изменения"""
                if ent['distinguishedName']:
                    try:
                        company_list = ent['distinguishedName'].split(',')
                        company_list.reverse()
                        now_company = False
                        for c in company_list:
                            if c[0:2] != 'CN' and c[0:2] != 'DC':
                                if now_company:
                                    company, created_com = CompanyMPTT.objects.get_or_create(company=c[3:],
                                                                                             parent=now_company, )
                                else:
                                    company, created_com = CompanyMPTT.objects.get_or_create(company=c[3:],
                                                                                             parent__isnull=True, )
                                if company not in contact.company.all():
                                    contact.company.add(company)
                                now_company = company
                    except:
                        print('Can`t create company')

                if ent['manager']:
                    try:
                        manager_list = ent['manager'].split(',')
                        manager_company_list = []
                        for c in manager_list:
                            if c[0:2] != 'CN' and c[0:2] != 'DC':
                                manager_company_list.append(c[3:])
                        manager_company = CompanyMPTT.objects.get(company=manager_company_list[0],
                                                                  parent__company=manager_company_list[1])
                        manager = Contact.objects.get(cn=manager_list[0][3:], company=manager_company)
                        contact.manager = manager
                        update_fields.append('manager')
                    except:
                        print('Can`t get manager')
                if ent['description']:
                    for p in ent['description']:
                        position, created_positon = Position.objects.get_or_create(description=p)
                        if position not in contact.description.all():
                            contact.description.add(position)
                if ent['mobile']:
                    if type(ent['mobile']) == list:
                        for m_phone in ent['mobile']:
                            mobile, created_mobile = MobilePhone.objects.get_or_create(user=contact, mobile=int(
                                re.sub("\D", "", m_phone)))
                    else:
                        print(int(re.sub("\D", "", ent['mobile'])))
                        mobile, created_mobile = MobilePhone.objects.get_or_create(user=contact, mobile=int(
                            re.sub("\D", "", ent['mobile'])))
                if ent['department']:
                    update_fields.append('department')
                    contact.department = ent['department']
                if ent['division']:
                    update_fields.append('division')
                    contact.division = ent['division']
                if ent['mail']:
                    update_fields.append('mail')
                    contact.mail = ent['mail']
                if ent['pager']:
                    update_fields.append('pager')
                    contact.pager = ent['pager']
                if ent['physicalDeliveryOfficeName']:
                    update_fields.append('physicalDeliveryOfficeName')
                    contact.physicalDeliveryOfficeName = ent['physicalDeliveryOfficeName']
                if ent['postalCode']:
                    update_fields.append('postalCode')
                    contact.postalCode = ent['postalCode']
                if ent['l']:
                    update_fields.append('l')
                    contact.l = ent['l']
                if ent['streetAddress']:
                    update_fields.append('streetAddress')
                    contact.streetAddress = ent['streetAddress']
                if ent['telephoneNumber']:
                    update_fields.append('telephoneNumber')
                    contact.telephoneNumber = ent['telephoneNumber']
                contact.cn = ent['cn']
                contact.sAMAccountName = ent['sAMAccountName']
                contact.active = True
                contact.contact_from_AD = True
                update_fields += ['active', 'contact_from_AD']
                contact.save(update_fields=update_fields)
    return True


@app.task
def update_manager():
    """
        Снхронизация пользователей AD для установки связай пользователь -> руководитель

    """
    server = Server(AD_SERVER)
    conn = Connection(server, user=AD_USER, password=AD_PASSWORD)
    """conn.bind() Установка соединения с AD """
    conn.bind()
    """entry_generator генератор поиска пользователей и их атрибутов по фильтру """
    entry_generator = conn.extend.standard.paged_search(AD_SEARCH_TREE,
                                                        '(&(objectCategory=Person) (!(UserAccountControl:1.2.840.113556.1.4.803:=2))(givenName=*)(sn=*))',
                                                        SUBTREE,
                                                        attributes=['cn', 'division', 'company', 'department',
                                                                    'description', 'distinguishedName', 'employeeID',
                                                                    'homeMDB', 'mail', 'manager', 'memberOf', 'mobile',
                                                                    'msExchRBACPolicyLink', 'objectGUID', 'pager', 'l',
                                                                    'physicalDeliveryOfficeName', 'postalCode',
                                                                    'streetAddress', 'sAMAccountName',
                                                                    'telephoneNumber', 'uSNChanged',
                                                                    'lastLogon'],
                                                        paged_size=5,
                                                        generator=True)
    for entry in entry_generator:
        if 'attributes' in entry:
            ent = entry['attributes']
            update_fields = []
            contact, created = Contact.objects.get_or_create(objectGUID=ent['objectGUID'])
            if not created:
                """Если пользоваетль существует, проверяем изменение его атрибутов по полю uSNChanged"""
                if contact.uSNChanged:
                    if contact.uSNChanged != ent['uSNChanged']:
                        update_fields.append('uSNChanged')
                        contact.uSNChanged = ent['uSNChanged']
                else:
                    update_fields.append('uSNChanged')
                    contact.uSNChanged = ent['uSNChanged']
                """проверяем наличие атрибута manager, при наличии пытаемся найти его в БД и привязать к пользователю"""
                if ent['manager']:
                    try:
                        manager_list = ent['manager'].split(',')
                        manager_company_list = []
                        for c in manager_list:
                            if c[0:2] != 'CN' and c[0:2] != 'DC':
                                manager_company_list.append(c[3:])
                        manager_company = CompanyMPTT.objects.get(company=manager_company_list[0],
                                                                  parent__company=manager_company_list[1])
                        manager = Contact.objects.get(cn=manager_list[0][3:], company=manager_company)
                        contact.manager = manager
                        update_fields.append('manager')
                    except:
                        print('Can`t get manager')
                contact.save(update_fields=update_fields)
    return True


@shared_task
def update_photo():
    """
        Снхронизация пользователей AD для получения/обновления фото пользователей

    """
    server = Server(AD_SERVER)
    conn = Connection(server, user=AD_USER, password=AD_PASSWORD)
    """conn.bind() Установка соединения с AD """
    conn.bind()
    for user in Contact.objects.filter(active=True, contact_from_AD=True):
        """Для всех пользователей из БД делаем поиск по AD с атрибутами  jpegPhoto - фото и  thumbnailPhoto - аватар"""
        conn.search(AD_SEARCH_TREE,
                    f'(&(objectCategory=Person)(objectGUID={user.objectGUID}))',
                    SUBTREE,
                    attributes=['objectGUID', 'cn', 'jpegPhoto', 'thumbnailPhoto']
                    )
        if conn.entries:
            j = json.loads(conn.entries[0].entry_to_json())
            update = False
            update_fields = []
            """При наличии атрибута jpegPhoto
                Если у пользователя не сохранено фото на сервер, то обробатываем и сохраняем.
                Если есть фото, сравниваем хэш фото из AD и имеющеесеся фото. При их отличии обновляем фото"""
            if 'jpegPhoto' in j['attributes']:
                if len(j['attributes']['jpegPhoto']) > 0:
                    photo = str.encode(j['attributes']['jpegPhoto'][0]['encoded'])
                    photo_hash = hashlib.md5(photo).hexdigest()
                    if user.jpegPhoto_hash:
                        if user.jpegPhoto_hash != photo_hash:
                            update = True
                    else:
                        update = True
                    if update:
                        path = os.path.join(VPN_USER_PHOTO_DIRS, f'{user.objectGUID}.jpg')
                        with open(path, "wb") as fh:
                            fh.write(base64.decodebytes(photo))
                        user.jpegPhoto_hash = photo_hash
                        user.jpegPhoto = f'{user.objectGUID}.jpg'
                        update_fields += ['jpegPhoto_hash', 'jpegPhoto']
            update = False
            """При наличии атрибута thumbnailPhoto
                Если у пользователя не сохранено фото на сервер, то обробатываем и сохраняем.
                Если есть фото, сравниваем хэш фото из AD и имеющеесеся фото. При их отличии обновляем фото"""
            if 'thumbnailPhoto' in j['attributes']:
                if len(j['attributes']['thumbnailPhoto']) > 0:
                    photo = str.encode(j['attributes']['thumbnailPhoto'][0]['encoded'])
                    photo_hash = hashlib.md5(photo).hexdigest()
                    if user.jpegPhoto_hash:

                        if user.thumbnailPhoto_hash != photo_hash:
                            update = True
                    else:
                        update = True
                    if update:
                        path = os.path.join(VPN_USER_PHOTO_DIRS, f't{user.objectGUID}.jpg')
                        with open(path, "wb") as fh:
                            fh.write(base64.decodebytes(photo))
                        user.thumbnailPhoto_hash = photo_hash
                        user.thumbnailPhoto = f't{user.objectGUID}.jpg'
                        update_fields += ['thumbnailPhoto_hash', 'thumbnailPhoto']
            if update_fields:
                user.save(update_fields=update_fields)
    return True