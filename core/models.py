from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user"""
        if not email:
            raise ValueError('User must have valid email address.')
        user = self.model(email=self.normalize_email(email),
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create, save, and return a superuser"""
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.role = "Admin"
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    email = models.EmailField(max_length=255, unique=True)
    fullname = models.CharField(max_length=255)
    phone_regex = RegexValidator(regex=r'^\d{10}',
                            message='Phone number must be entered in the formated 9876543210.'
    )
    phone = models.CharField(validators=[phone_regex], max_length=10, 
                             unique=True, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    pincode = models.IntegerField(validators=[MinValueValidator(000000), MaxValueValidator(999999)], null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    class UserTypes(models.TextChoices):
        ADMIN = "Admin", "ADMIN"
        AUTHOR = "Author", "AUTHOR"

    role = models.CharField(max_length=10, choices=UserTypes.choices,
                            blank=True,
                            null=True,
                            default=UserTypes.AUTHOR
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
