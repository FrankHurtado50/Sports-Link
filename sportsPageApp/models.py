from django.db import models
import bcrypt
import re

class UserManager(models.Manager):
    def register_validator(self, post_data):
        errors = {}

        if len(post_data['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters."
        if len(post_data['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters."
        if len(post_data['password']) < 4:
            errors['password'] = "Password must be at least 4 characters."
        if post_data['password'] != post_data['confirm_password']:
            errors['confirm_password'] = "Password does not match Confirm Password"

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        return errors


    def login_validator(self, post_data):
        errors = {}
        user_list = User.objects.filter(email = post_data['email'])
        if len(user_list) > 0:
            user = user_list[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors['password'] = "Invalid Credentials"
        else:
            errors['email'] = "Invalid Credentials"

        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    create_at = models.DateTimeField(auto_now_add = True)
    update_at = models.DateTimeField(auto_now = True)
    objects = UserManager()


# Create your models here.
