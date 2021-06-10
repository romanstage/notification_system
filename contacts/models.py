from django.db import models

from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import Group
# Create your models here.

# division - организация
# company - филиал
# department - отдел
# description - должность


class Contact(models.Model):
    sAMAccountName = models.CharField(max_length=150, null=True, blank=True, db_index=True,)
    cn = models.CharField(max_length=150, blank=True, db_index=True, )
    division = models.CharField(max_length=150, null=True, blank=True, db_index=True, )
    department = models.CharField(max_length=150, null=True, blank=True, db_index=True, )
    description = models.ManyToManyField('Position')
    mail = models.EmailField(max_length=150, blank=True, db_index=True, )
    manager = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, )
    objectGUID = models.CharField(max_length=150, blank=False, db_index=True, )
    company = models.ManyToManyField('CompanyMPTT')
    pager = models.CharField(max_length=150, blank=True, db_index=True, )
    physicalDeliveryOfficeName = models.CharField(max_length=150, blank=True, db_index=True, )
    postalCode = models.CharField(max_length=150, blank=True, db_index=True, )
    l = models.CharField(max_length=150, blank=True, db_index=True, )
    streetAddress = models.CharField(max_length=300, blank=True, db_index=True, )
    telephoneNumber = models.CharField(max_length=150, blank=True, db_index=True, )
    uSNChanged = models.BigIntegerField(blank=True, null=True, db_index=True, )
    jpegPhoto = models.CharField(max_length=150, blank=True, db_index=True, )
    jpegPhoto_hash = models.CharField(max_length=150, blank=True, db_index=True, )
    thumbnailPhoto = models.CharField(max_length=150, blank=True, db_index=True, )
    thumbnailPhoto_hash = models.CharField(max_length=150, blank=True, db_index=True, )
    date_create = models.DateTimeField(auto_now_add=True)
    date_change = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)
    contact_from_AD = models.BooleanField(default=False)
    available_to_groups = models.ManyToManyField(Group, blank=True,)

    def __str__(self):
        return f'{self.cn}'


class MobilePhone(models.Model):
    user = models.ForeignKey('Contact', on_delete=models.SET_NULL, null=True, blank=True, related_name='mobile_phone')
    mobile = models.BigIntegerField(blank=False, null=False)
    telegram_id = models.BigIntegerField(null=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.mobile}'


class CompanyMPTT(MPTTModel):
    company = models.CharField(max_length=150, blank=True, db_index=True, )
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                            related_name='children')
    date_create = models.DateTimeField(auto_now_add=True)
    date_change = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['company']


class Position(models.Model):
    description = models.CharField(max_length=150, blank=True, db_index=True, )
    date_create = models.DateTimeField(auto_now_add=True)
    date_change = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.description}'


class ContactGroup(models.Model):
    title = models.CharField(max_length=150, blank=False, db_index=True,)
    owner = models.ForeignKey(Group, null=True, blank=True, on_delete=models.SET_NULL, )
    contact = models.ManyToManyField(Contact, blank=True, related_name='contact_group')
    date_create = models.DateTimeField(auto_now_add=True)
    date_change = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'

class TextTemplate(models.Model):
    title = models.CharField(max_length=150, blank=False, db_index=True)
    body = models.TextField(max_length=720, blank=True)
    owner = models.ForeignKey(Group, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.title}'
