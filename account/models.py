from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from about.models import ClubModel


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, id, name, phone, password=None, **extra_fields):
        if not id:
            raise ValueError("User must have ID")
        if not name:
            raise ValueError("User must have name")
        if not phone:
            raise ValueError("User must have phone")
        if not password:
            raise ValueError("User must have password")

        user = self.model(
            id=id,
            name=name,
            phone=phone,
            **extra_fields
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, id, name, phone, password, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff = True')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser = True')

        return self.create_user(id, name, phone, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.PositiveIntegerField(primary_key=True, unique=True, null=False, blank=False)
    name = models.CharField(max_length=5, null=False, blank=False)
    phone = PhoneNumberField(null=False, blank=False)

    leader_of = models.ForeignKey(ClubModel,  related_name='leader_of+', on_delete=models.SET_NULL, null=True, blank=True)
    member_of = models.ForeignKey(ClubModel,  related_name='member_of+', on_delete=models.SET_NULL, null=True, blank=True)

    end = models.BooleanField(default=False, null=False, blank=False)

    username = None
    first_name = None
    last_name = None
    email = None
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['name', 'phone']
    objects = UserManager()

    def __str__(self):
        return str(self.id)

    # def has_perm(self, perm, obj=None):
    #     print('has_perm', perm, obj)
    #     return self.is_admin
    #
    # def has_module_perms(self, app_label):
    #     print('has_module_perms', app_label)
    #     return self.is_admin

