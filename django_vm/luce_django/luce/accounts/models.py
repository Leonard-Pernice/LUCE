# accounts.models.py

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, institution, ethereum_public_key=None, password=None, is_staff=False, is_admin=False):
        """
        Creates and saves a User with the given arguments and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not first_name:
            raise ValueError('Users must have a first_name')
        if not last_name:
            raise ValueError('Users must have a last_name')
        if not institution:
            raise ValueError('Users must have an institution')
        if not password:
        	raise ValueError('Users must have a password')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.first_name 	= first_name
        user.last_name 		= last_name
        user.institution 	= institution
        user.ethereum_public_key = ethereum_public_key
        user.staff = is_staff
        user.admin = is_admin
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, first_name, last_name, institution, password):
        """
        Creates and saves a staff user.
        """
        user = self.create_user(
            email,
            first_name,
            last_name,
            institution,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, institution, password):
        """
        Creates and saves a superuser.
        """
        user = self.create_user(
            email,
            first_name,
            last_name,
            institution,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


# Our custom user class
class User(AbstractBaseUser):
	# id, 
	# password and 
	# last_login are automatically inherited AbstractBaseUser
	# The other model fields we define ourselves
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    # Make these fields compulsory?
    first_name 	= 	models.CharField(max_length=255, blank=True, null=True)
    last_name 	= 	models.CharField(max_length=255, blank=True, null=True)
    institution =	models.CharField(max_length=255, blank=True, null=True)

    # Automatically obtain public_address from Metamask
    ethereum_public_key 	=	models.CharField(max_length=255, blank=True, null=True)

    # active user? -> can login
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    # notice the absence of a "Password field", that's built in.

    # Define which field should be the username for login
    USERNAME_FIELD = 'email'

    # USERNAME_FIELD & Password are required by default
    # Add additional required fields here:
    REQUIRED_FIELDS = ['first_name', 'last_name', 'institution'] 

    objects = UserManager()

    # The following methods are expected to be defined by Django
    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user an admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active