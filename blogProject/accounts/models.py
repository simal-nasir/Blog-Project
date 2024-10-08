from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserAccountManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self._db)  # Use the database defined in the manager
        return user

    def create_superuser(self, email, name, password=None):
        """Create and return a superuser with an email, name, and password."""
        if not email:
            raise ValueError("Superusers must have an email address")
        if password is None:
            raise ValueError("Superusers must have a password")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, is_staff=True, is_superuser=True)

        user.set_password(password)
        user.save(using=self._db)
        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email