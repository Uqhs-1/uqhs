#python 
def users(x):
  if x == 'gen':
    users = User.objects.all()
    data = [[i.profile.title, i.profile.last_name, i.profile.first_name, i.username, i.profile.department] for i in users]
  else:
    if not User.objects.filter(username__exact=request.GET.get('username')):
      userObj = User.objects.create_user(username=request.GET.get('username'), email=request.GET.get('username').lower()+'@uqhs.herokuapp.com', password='Ll0183111@$')
      userObj.is_active = True
      userObj.is_staff = True
      userObj.save()
      pro = userObj.profile
      pro.title, pro.last_name, pro.first_name, pro.department = [request.GET.get('title'), request.GET.get('last_name'), request.GET.get('first_name'), request.GET.get('department')]
      pro.email_confirmed = True
      pro.save()
    data = {'status':request.GET.get('username'),'sn':request.GET.get('sn'), 'len':request.GET.get('len')}
  return JsonResponse(data)


import boto3

# constants
BUCKET_NAME = 'uqhs’
S3_FILE = 'pdfs3'
LOCAL_NAME = 'pdflc'

s3 = boto3.resource('s3')

# test listing
bucket = s3.Bucket(BUCKET_NAME)
for f in bucket.objects.all():
    print(f.key)

# test downloading
bucket.download_file(S3_FILE, LOCAL_NAME)

# test uploading
data = open('storage/emulated/0/uqs/uqi/result/static/result/pdf/marksheets/1/1st/ARB_1_1_21_0.pdf', 'rb')
bucket.put_object(Key='ARB1.pdf', Body=data)
#Notice how we didn’t have to explicitly

export AWS_ACCESS_KEY_ID='AKIAZXDZRFQVP24YW7UU'
export AWS_SECRET_ACCESS_KEY='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'
export AWS_STORAGE_BUCKET_NAME='uqhs'
export AWS_UR='AWS_URL='https://uqhs.s3.amazonaws.com'

heroku config:set AWS_SECRET_ACCESS_KEY= '32hOmVzUovuSW89PjoSYS2WNBm3IE/JKyosYehQh'
heroku config:set AWS_ACCESS_KEY_ID='AKIAZXDZRFQVP24YW7UU'
heroku config:set AWS_STORAGE_BUCKET_NAME='uqhs'
heroku config:set AWS_URL='https://uqhs##.s3.amazonaws.com/'

AWS_ACCESS_KEY_ID='AKIAZXDZRFQVP24YW7UU'
AWS_SECRET_ACCESS_KEY='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'
AWS_STORAGE_BUCKET_NAME = 'uqhs'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'

STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


Storing Django Static and Media Files on Amazon S3
Posted byMichael HermanMichael Herman
Last updated February 10th, 2020
Share this tutorial
Amazon's Simple Storage System (S3) provides a simple, cost-effective way to store static files. This tutorial shows how to configure Django to load and serve up static and user uploaded media files, public and private, via an Amazon S3 bucket.

Main dependencies:

Django v3.0.3
Docker v19.03.4
Python v3.8.1
Contents
S3 Bucket
IAM Access
Django Project
Django Storages
Static Files
Public Media Files
Private Media Files
Conclusion
S3 Bucket
Before beginning, you will need an AWS account. If you’re new to AWS, Amazon provides a free tier with 5GB of S3 storage.

To create an S3 bucket, navigate to the S3 page and click "Create bucket":

aws s3

Give the bucket a unique, DNS-compliant name and select a region:

aws s3

Click "Next". Don't make any changes on the "Configure options" page. Then, on the "Set permissions" page, turn off "Block all public access":

aws s3

Click "Next" again and create the bucket. You should now see your bucket back on the main S3 page:

aws s3

IAM Access
Although you could use the AWS root user, it's best for security to create an IAM user that only has access to S3 or to a specific S3 bucket. What's more, by setting up a group, it makes it much easier to assign (and remove) access to the bucket. So, we'll start by setting up a group with limited permissions and then create a user and assign that user to the group.

IAM Group
Within the AWS Console, navigate to the main IAM page and click "Groups" on the sidebar. Then, click the "Create New Group" button, provide a name for the group and then search for and select the built-in policy "AmazonS3FullAccess":

aws iam

Click the "Next Step" button and then "Create Group" to finish setting up the group:

aws iam

If you'd like to limit access even more, to the specific bucket we just created, create a new policy with the following permissions:

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "s3:*",
            "Resource": [
                "arn:aws:s3:::your-bucket-name",
                "arn:aws:s3:::your-bucket-name/*"
            ]
        }
    ]
}
Be sure to replace your-bucket-name with the actual name. Then, detach the "AmazonS3FullAccess" policy from the group and attach the new policy.

IAM User
Back on the main IAM page, click "Users" and then "Add user". Define a user name and select "Programmatic access" under the "Access type":

aws iam

Click the next button to move on to the "Permissions" step. Select the group we just created:

aws iam

Click next again and then click "Create user" to create the new user. You should now see the user's access key ID and secret access key:

aws iam

Take note of the keys.

Django Project
Clone down the django-docker-s3 repo, and then check out the v1 tag to the master branch:

$ git clone https://github.com/testdrivenio/django-docker-s3 --branch v1 --single-branch
$ cd django-docker-s3
$ git checkout tags/v1 -b master
From the project root, create the images and spin up the Docker containers:

$ docker-compose up -d --build
Once the build is complete, navigate to http://localhost:1337:

app

You should be able to upload an image, and then view the image at http://localhost:1337/mediafiles/IMAGE_FILE_NAME.

The radio buttons, for public vs. private, do not work. We will be adding this functionality later in this tutorial. Ignore them for now.

Take a quick look at the project structure before moving on:

├── .gitignore
├── LICENSE
├── README.md
├── app
│   ├── Dockerfile
│   ├── entrypoint.sh
│   ├── hello_django
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── manage.py
│   ├── mediafiles
│   ├── requirements.txt
│   ├── static
│   │   └── bulma.min.css
│   ├── staticfiles
│   └── upload
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── migrations
│       │   └── __init__.py
│       ├── models.py
│       ├── templates
│       │   └── upload.html
│       ├── tests.py
│       └── views.py
├── docker-compose.yml
└── nginx
    ├── Dockerfile
    └── nginx.conf
Want to learn how to build this project? Check out the Dockerizing Django with Postgres, Gunicorn, and Nginx blog post.

Django Storages
Next, install django-storages, to use S3 as the main Django storage backend, and boto3, to interact with the AWS API.

Update the requirements file:

boto3==1.11.12
Django==3.0.3
django-storages==1.9.1
gunicorn==20.0.4
Add storages to the INSTALLED_APPS in settings.py:

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'upload',
    'storages',
]
Update the images and spin up the new containers:

$ docker-compose up -d --build
Static Files
Moving along, we need to update the handling of static files in settings.py:

STATIC_URL = '/staticfiles/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)


MEDIA_URL = '/mediafiles/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')
Replace those settings with the following:

USE_S3 = os.getenv('USE_S3') == 'TRUE'

if USE_S3:
    # aws settings
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    # s3 static settings
    AWS_LOCATION = 'static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
else:
    STATIC_URL = '/staticfiles/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

MEDIA_URL = '/mediafiles/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')
Take note of USE_S3 and STATICFILES_STORAGE:

The USE_S3 environment variable is used to turn the S3 storage on (value is TRUE) and off (value is FALSE). So, you could configure two Docker compose files: one for development with S3 off and the other for production with S3 on.
The STATICFILES_STORAGE setting configures Django to automatically add static files to the S3 bucket when the collectstatic command is run.
Review the official django-storages documentation for more info on the above settings and config.

Add the appropriate environment variables to the web service in the docker-compose.yml file:

web:
  build: ./app
  command: gunicorn hello_django.wsgi:application --bind 0.0.0.0:8000
  volumes:
    - ./app/:/usr/src/app/
    - static_volume:/usr/src/app/staticfiles
    - media_volume:/usr/src/app/mediafiles
  expose:
    - 8000
  environment:
    - SECRET_KEY=please_change_me
    - SQL_ENGINE=django.db.backends.postgresql
    - SQL_DATABASE=postgres
    - SQL_USER=postgres
    - SQL_PASSWORD=postgres
    - SQL_HOST=db
    - SQL_PORT=5432
    - DATABASE=postgres
    - USE_S3=TRUE
    - AWS_ACCESS_KEY_ID=UPDATE_ME
    - AWS_SECRET_ACCESS_KEY=UPDATE_ME
    - AWS_STORAGE_BUCKET_NAME=UPDATE_ME
  depends_on:
    - db
Don't forget to update AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY with the user keys that you just created along with the AWS_STORAGE_BUCKET_NAME.

To test, re-build and run the containers:

$ docker-compose down -v
$ docker-compose up -d --build
This will automatically collect the static files (via the entrypoint.sh file). It should take much longer than usual since it is uploading them to the S3 bucket.

http://localhost:1337 should still render correctly:

app

View the page source to ensure the CSS stylesheet is pulled in from the S3 bucket:

app

Verify that the static files can be seen on the AWS console within the "static" subfolder of the S3 bucket:

aws s3

Media uploads will still hit the local filesystem since we've only configured S3 for static files. We'll work with media uploads shortly.

Finally, update the value of USE_S3 to FALSE and re-build the images to make sure that Django uses the local filesystem for static files. Once done, change USE_S3 back to TRUE.

Public Media Files
To prevent users from overwriting existing static files, media file uploads should be placed in a different subfolder in the bucket. We'll handle this by creating custom storage classes for each type of storage.

Add a new file called storage_backends.py to the "app/hello_django" folder:

from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class StaticStorage(S3Boto3Storage):
    location = 'static'
    default_acl = 'public-read'


class PublicMediaStorage(S3Boto3Storage):
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False
Make the following changes to settings.py:

USE_S3 = os.getenv('USE_S3') == 'TRUE'


#STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
#AUTH_USER_MODEL = 'score_log.User'
# The URL to use when referring to static files (where they will be served from)
#STATIC_URL = '/static/'
#STATICFILES_DIRS = (
    #os.path.join(BASE_DIR, 'result/static'),
#)###
admin
#668122295338
AWS_ACCESS_KEY_ID='AKIAZXDZRFQVP24YW7UU'
AWS_SECRET_ACCESS_KEY='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'
AWS_STORAGE_BUCKET_NAME = 'uqhs'
AWS_S3_SECURE_URLS = False 
AWS_S3_URL_PROTOCOL = 'http' 
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
#AWS_S3_HOST = "s3.amazonaws.com" 
#AWS_S3_URL = 'https://{bucker_name}.s3.amazonaws.com/'.format(bucker_name=AWS_STORAGE_BUCKET_NAME) 

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'

STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

