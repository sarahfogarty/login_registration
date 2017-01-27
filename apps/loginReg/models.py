from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
import re
import bcrypt
# EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')  ===================CLEANED UP VERSION============

class UserManager(models.Manager):

    def validateReg(self, request):

        # Check to see if  from validate input is greater than 0. If so, there were  and you cannot register.
        error = self.validateInput(request)
# above -  use self rather than User - pulling from self
        # if statement to check above variable. Also dpesn't need objects

        if len(error) > 0:
            return (False, error)

        # Else -> there are no  (no "else" needed in code. Start the password bcrypt hash thing.)

        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

        # Creates the new user because PW is all good
        user = self.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], pw_hash=pw_hash)

        return (True, user)


    def validateLogin(self, request):
        try:
            user = User.objects.get(email=request.POST['email'])
            # The email matched a record in the database, now test passwords
            password = request.POST['password'].encode()
            if bcrypt.hashpw(password, user.pw_hash.encode()):
                return (True, user)
        except ObjectDoesNotExist:
            pass
        return (False, ["Email/password don't match."])


    def validateInput(self, request):
        error = []
        email_list = User.objects.filter(email = request.POST['email'])
        if email_list:
            error.append('Email already has account accociated')
        # hashed = bcrypt.hashpw('password', bcrypt.gensalt())

        # use request.POST tp [u;; the data in for usability]
        if len(request.POST['first_name']) < 2:
            error.append('First name must be greater than 2 characters.')
        if len(request.POST['last_name']) < 2:
            error.append('Last name must be greater than 2 characters.')
        elif not (request.POST['first_name']).isalpha():
            error.append('First name must be letters.')
        elif not (request.POST['last_name']).isalpha():
            error.append('Last name must be letters.')
# should this be match or compile?
        if not EMAIL_REGEX.match(request.POST['email']):
            error.append('Must enter a valid email.')
        if len(request.POST['password']) < 8:
            error.append('Password must be at least 8 characters.')
        elif request.POST['password'] != request.POST['passwordconf']:
            error.append('Passwords do not match.')

        return error


#
#
#
class User(models.Model):
    first_name = models.CharField(max_length = 45)
    last_name = models.CharField(max_length = 45)
    email = models.CharField(max_length = 45)
# ADD PW_HASH
    pw_hash = models.CharField(max_length = 255, default='pw_hash')

    # DONT NEED CREATED AT, UPDATED AT, PASSWORD.
    # password = models.CharField(max_length = 45)
    # created_at = models.DateTimeField(auto_now_add = True)
    # updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
