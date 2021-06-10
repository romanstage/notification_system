from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField
from .models import CompanyMPTT, Position, Contact, MobilePhone, Group, ContactGroup, TextTemplate

class MobilePhoneSerializerReadOnly(serializers.ModelSerializer):

    class Meta:
        model = MobilePhone
        fields = (
            'id', 'mobile', 'status'
        )
        read_only_fields = fields


class MobilePhoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = MobilePhone
        fields = (
            'id', 'mobile', 'status', 'user', 'telegram_id'
        )


class PositionSerializerReadOnly(serializers.ModelSerializer):

    class Meta:
        model = Position
        fields = (
            # 'id',
            'description',
        )
        read_only_fields = fields


class CompanyMPTTSerializerReadOnly(serializers.ModelSerializer):

    class Meta:
        model = CompanyMPTT
        fields = (
            'id', 'company', 'level'
        )
        read_only_fields = fields


class ManagerSerializerReadOnly(serializers.ModelSerializer):
    company = CompanyMPTTSerializerReadOnly(many=True)
    description = PositionSerializerReadOnly(many=True)

    class Meta:
        model = Contact
        fields = (
            'id', 'cn', 'mail', 'company', 'description', 'pager'
        )
        read_only_fields = fields


class ContactSerializerReadOnly(serializers.ModelSerializer):
    company = CompanyMPTTSerializerReadOnly(many=True)
    description = PositionSerializerReadOnly(many=True)
    mobile_phone = MobilePhoneSerializerReadOnly(many=True)
    manager = ManagerSerializerReadOnly()

    class Meta:
        model = Contact
        fields = (
            'id', 'cn', 'mail', 'company', 'description', 'pager', 'manager', 'mobile_phone', 'jpegPhoto',
            'streetAddress',
        )
        read_only_fields = fields


class AddContactSerializer(serializers.ModelSerializer):
    company = CompanyMPTTSerializerReadOnly(many=True)
    description = PositionSerializerReadOnly(many=True)

    class Meta:
        model = Contact
        fields = (
            'id', 'cn', 'mail', 'company', 'description', 'division', 'department',
        )



class CompanyRecursiveModelSerializer(serializers.ModelSerializer):
    children = RecursiveField(allow_null=True, many=True)

    class Meta:
        model = CompanyMPTT
        fields = ('id', 'children', 'company')
        read_only_fields = fields


class AddContactToMyContacts(serializers.ModelSerializer):
    available_to_groups = serializers.PrimaryKeyRelatedField(many=True, queryset=Group.objects.all())

    class Meta:
        model = Contact
        fields = (
            'id', 'available_to_groups'
        )


class UserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class ContactGroupSerializer(serializers.ModelSerializer):
    contact = ContactSerializerReadOnly(many=True)
    owner = UserGroupSerializer()

    class Meta:
        model = ContactGroup
        fields = '__all__'


# Сериалайзер для правки
class ContactGroupSerializerWrite(serializers.ModelSerializer):
    class Meta:
        model = ContactGroup
        fields = '__all__'

class TextTemplateSerializer(serializers.ModelSerializer):
    owner = UserGroupSerializer()

    class Meta:
        model = TextTemplate
        fields = ('id', 'title', 'body', 'owner')
        read_only_fields = fields


# Сериалайзер для правки
class TextTemplateSerializerWrite(serializers.ModelSerializer):
    class Meta:
        model = TextTemplate
        fields = ('id', 'title', 'body' ,'owner')


