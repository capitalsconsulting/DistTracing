# Detecting new files from Sftp
This is a repository for receiving new csv file detection from Sftp store

## Prequisites
python 3.8 & django
```
python -m venv venv
source ./venv/bin/activate
python -m pip install -r ./sftp_test/requirement.txt
```

## Run Server

```
python mamage.py runserver
```

## Custom setting

./sftp_test/sftp_test/settings.py contains config info

### Here are config settings for sftp connection
```
SFTP_HOST = 'bbonesource.blob.core.windows.net'
SFTP_USERNAME = 'bbonesource.sftponesource'
SFTP_PASSWORD = 'K12X06IzJucyBqpfi76GgdV3v4fSZQHi'
SFTP_REMOTE_DIR = '/'
```

### Here is sftp file storing directory
```
MEDIA_ROOT='sftp-files/'
```

### Here are smtp email transfer config settings
```
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'devilprogrammer090@gmail.com'
EMAIL_HOST_PASSWORD = 'xpaenpqxdeuzchlp'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
```
For custom email transfer, app password should be generated with your google account like the following
![google-generate-app-specific-password](https://github.com/edzavier/sftp-smtp-transfer/assets/135173998/1a1c7452-3e03-4fa3-8b7f-08d4cee89ca5)

### Sending email content( title & description ) and destination & source could be customized in ./sftp_test/manage.py line 11
```
email = EmailMessage(
    subject='File Received',
    body='New File Received',
    from_email='devilprogrammer090@gmail.com',
    to=['distributorsubmission@k-1c80vq6gka4vsdayfbc3rszgm8s46rwd2iyub7xcjmeakewsxj.46-zomweai.na210.apex.salesforce.com'],
)
```
