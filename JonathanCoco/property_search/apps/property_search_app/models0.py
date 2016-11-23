from __future__ import unicode_literals
from django.db import models
import re
#import bcrypt
from django.contrib import messages
import bcrypt
import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')


# Create your models here.

#Our new manager!
  #No methods in our new manager should ever catch the whole request object with a parameter!!! (just parts, like request.POST)
class UserManager(models.Manager):
    def Login(self, email, password, request):
        bLoginSuccessful = True;

        users = User.objects.filter(email = email)
        if len(users) == 0:
            messages.error(request, "User does not exists", extra_tags = "Login")
            return 0
        else:

            if (users[0].password != bcrypt.hashpw(password.encode('utf-8'), users[0].password.encode('utf-8'))):
                messages.error(request, "Invalid Password", extra_tags = "Login")

                return 0

        return users[0]

    def EncryptPassword(self, password):

        password = password.encode('utf-8')
        return bcrypt.hashpw(password, bcrypt.gensalt())


    def IsRegistrationValid(self, first_name, last_name, alias, email, birth_date, password, confirm_password, request):

        bOK = True

        if ((len(first_name) <=2) or not NAME_REGEX.match(first_name)):
            messages.error(request, "First Name - Alpha characters only and at least 2 characters", extra_tags="Registration")
            bOK = False
        if len(last_name) <=2:
            messages.error(request, "Last Name - Alpha characters only and at least 2 characters", extra_tags="Registration")
            bOK = False
        if len(email) < 1:
            messages.error(request, "Email cannot be blank!", extra_tags="Registration")
            bOK = False
        elif not EMAIL_REGEX.match(email):
            messages.error(request, "Invalid Email Address!", extra_tags="Registration")
            bOK = False

        if self.IsValidDate(birth_date) == False:
            messages.error(request, "Invalid Birth Date Format", extra_tags="Registration")
            bOK = False
        else:
            birthdate = datetime.datetime.strptime(birth_date, '%Y-%m-%d')

            if (datetime.datetime.now().year - birthdate.year) < 13:
                messages.error(request, "You must be at least 13 to register", extra_tags="Registration")
                bOK = False
            elif (birthdate.year < 1900):
                messages.error(request, "Please enter  a year > 1900", extra_tags="Registration")
                bOK = False



        if (password <> confirm_password ):
            messages.error(request, "Passwords do not match", extra_tags="Registration")
            bOK = False

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters", extra_tags="Registration")
            bOK = False

        users = User.objects.filter(email = email)
        if len(users) > 0:
            messages.error(request, "User already exists")
            bOK = False

        return bOK

    def IsValidDate(self, datestring):
        try:
            datetime.datetime.strptime(datestring, '%Y-%m-%d')
            return True
        except ValueError:
            pass

        try:
            datetime.datetime.strptime(datestring, '%m/%d/%Y')
            return True
        except ValueError:
            pass

        return False;





class User(models.Model):
    email = models.CharField(max_length=45)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    alias = models.CharField(max_length=45)
    password = models.CharField(max_length=60)
    birth_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    # *************************
    # Connect an instance of UserManager to our User model overwriting
    # the old hidden objects key with a new one with extra properties!!!
    objects = UserManager()

class Property(models.Model):
    prop_id = models.IntegerField()
    geo_id = models.CharField(max_length=50, null=True)
    file_as_name = models.CharField(max_length=70, null=True)
    pct_ownership = models.DecimalField(decimal_places=0, max_digits=14, null=True)
    dba_name = models.CharField(max_length=50, null=True)
    addr_line1 = models.CharField(max_length=60, null=True)
    addr_line2 = models.CharField(max_length=60, null=True)
    addr_line3 = models.CharField(max_length=60, null=True)
    addr_city = models.CharField(max_length=50, null=True)
    addr_state = models.CharField(max_length=50, null=True)
    addr_zip = models.CharField(max_length=10, null=True)
    ml_deliverable = models.CharField(max_length=1, null=True)
    abs_subdv_cd = models.CharField(max_length=10, null=True)
    abs_subdv_ref = models.CharField(max_length=50, null=True)
    abs_subdv_desc = models.CharField(max_length=60, null=True)
    block = models.CharField(max_length=50, null=True)
    tract_or_lot = models.CharField(max_length=50, null=True)
    legal_desc = models.CharField(max_length=255, null=True)
    legal_desc_2 = models.CharField(max_length=255, null=True)
    mapsco = models.CharField(max_length=20, null=True)
    condo_pct = models.DecimalField(decimal_places=10, max_digits=13, null=True)
    situs_num = models.CharField(max_length=15, null=True)
    situs_street_prefx = models.CharField(max_length=10, null=True)
    situs_street = models.CharField(max_length=50, null=True)
    situs_street_sufix = models.CharField(max_length=10, null=True)
    situs_city = models.CharField(max_length=30, null=True)
    situs_state = models.CharField(max_length=2, null=True)
    situs_zip = models.CharField(max_length=10, null=True)
    situs_display = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=5, null=True)
    school = models.CharField(max_length=5, null=True)
    tif = models.CharField(max_length=5, null=True)
    exemptions = models.CharField(max_length=100, null=True)
    all_entities = models.CharField(max_length=100, null=True)
    deed_book_id = models.CharField(max_length=20, null=True)
    deed_book_page = models.CharField(max_length=20, null=True)
    deed_num = models.CharField(max_length=50, null=True)
    deed_dt = models.DateTimeField()
    deed_type_cd = models.CharField(max_length=10, null=True)
    legal_acreage = models.DecimalField(decimal_places=4, max_digits=14, null=True)
    eff_size_acres = models.DecimalField(decimal_places=4, max_digits=14, null=True)
    land_sqft = models.DecimalField(decimal_places=2, max_digits=18, null=True)
    land_total_sqft = models.DecimalField(decimal_places=2, max_digits=18, null=True)
    living_area = models.DecimalField(decimal_places=0, max_digits=14, null=True)
    state_cd = models.CharField(max_length=10, null=True)
    class_cd = models.CharField(max_length=10, null=True)
    property_use_cd = models.CharField(max_length=10, null=True)
    prop_type_cd = models.CharField(max_length=5, null=True)
    commercial_flag = models.CharField(max_length=1, null=True)
    eff_yr_blt = models.DecimalField(decimal_places=0, max_digits=4, null=True)
    yr_blt = models.DecimalField(decimal_places=0, max_digits=4, null=True)
    zoning = models.CharField(max_length=50, null=True)
    land_type_cd = models.CharField(max_length=10, null=True)
    beds = models.CharField(max_length=20, null=True)
    baths = models.CharField(max_length=20, null=True)
    stories = models.IntegerField()
    units = models.IntegerField()
    percent_complete = models.DecimalField(decimal_places=2, max_digits=5, null=True)
    pool = models.CharField(max_length=1)
    prop_create_dt = models.DateTimeField()
    property_status = models.CharField(max_length=50, null=True)
    curr_val_yr = models.DecimalField(decimal_places=0, max_digits=4, null=True)
    curr_imprv_hstd_val = models.DecimalField(decimal_places=0, max_digits=14, null=True)
    curr_imprv_non_hstd_val = models.DecimalField(decimal_places=0, max_digits=14, null=True)
    curr_land_hstd_val = models.DecimalField(decimal_places=0, max_digits=14, null=True)
    curr_land_non_hstd_val = models.DecimalField(decimal_places=0, max_digits=14, null=True)
    curr_ag_use_val = models.DecimalField(decimal_places=0, max_digits=14, null=True)
    curr_ag_market = models.DecimalField(decimal_places=0, max_digits=14, null=True)
    curr_market = models.DecimalField(decimal_places=0, max_digits=14, null=True)
    curr_ag_loss = models.DecimalField(decimal_places=0, max_digits=14, null=True)
    curr_appraised_val = models.DecimalField(decimal_places=0, max_digits=14, null=True)
    curr_ten_percent_cap = models.DecimalField(decimal_places=0, max_digits=14, null=True)
    curr_assessed_val = models.DecimalField(decimal_places=0, max_digits=14, null=True)
    cert_val_yr = models.DecimalField(decimal_places=0, max_digits=4, null=True)
    cert_imprv_hstd_val = models.DecimalField(decimal_places=0, max_digits=14, null=True)
    cert_imprv_non_hstd_val = models.DecimalField(decimal_places=0, max_digits=14, null=True)
    cert_land_hstd_val = models.DecimalField(decimal_places=0, max_digits=14, null=True)
    cert_land_non_hstd_val = models.DecimalField(decimal_places=0, max_digits=14, null=True)
    cert_ag_use_val = models.DecimalField(decimal_places=0, max_digits=14, null=True)
    cert_ag_market = models.DecimalField(decimal_places=0, max_digits=14, null=True)
    cert_market = models.DecimalField(decimal_places=0, max_digits=14, null=True)
    cert_ag_loss = models.DecimalField(decimal_places=0, max_digits=14, null=True)
    cert_appraised_val = models.DecimalField(decimal_places=0, max_digits=14, null=True)
    cert_ten_percent_cap = models.DecimalField(decimal_places=0, max_digits=14, null=True)
    cert_assessed_val = models.DecimalField(decimal_places=0, max_digits=14, null=True)
    parent_year = models.DecimalField(decimal_places=0, max_digits=4, null=True)
    parent_id = models.IntegerField()
    parent_block = models.CharField(max_length=50, null=True)
    parent_tract = models.CharField(max_length=50, null=True)
    parent_acres = models.DecimalField(decimal_places=4, max_digits=14)

    class Meta:
        managed = False
        db_table = 'ad_public'
