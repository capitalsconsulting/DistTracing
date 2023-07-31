#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django.conf import settings
from background_task import background
import pysftp
import time
from django.core.mail import EmailMessage

email = EmailMessage(
    subject='File Received',
    body='New File Received',
    from_email='devilprogrammer090@gmail.com',
    to=['distributorsubmission@k-1c80vq6gka4vsdayfbc3rszgm8s46rwd2iyub7xcjmeakewsxj.46-zomweai.na210.apex.salesforce.com'],
)

# @background(schedule=1)
def monitor_sftp_server():
    # SFTP connection credentials
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None  # Disable host key verification

    with pysftp.Connection(
        settings.SFTP_HOST,
        username=settings.SFTP_USERNAME,
        password=settings.SFTP_PASSWORD,
        cnopts=cnopts
    ) as sftp:
        sftp.cwd(settings.SFTP_REMOTE_DIR)

        while True:
            files = sftp.listdir()
            for filename in files:
                
                if filename not in ['.', '..'] and filename.find('.csv') != -1:
                    print("csv file ", filename)
                    local_filepath = os.path.join(settings.MEDIA_ROOT, filename)
                    remote_filepath = os.path.join(sftp.getcwd(), filename)
                    if not os.path.exists(local_filepath):  # Download only if the file doesn't exist locally
                        print("   email sending...")
                        sftp.get(remote_filepath, local_filepath)
                        email.attach_file(local_filepath)
                        email.send()
                        # Perform further processing on the downloaded file if needed
                else:
                    print(" extra files ", filename)

            # Sleep for some time before checking for new files again
            time.sleep(10)  # Adjust the sleep time as per your requirements

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sftp_test.settings')
    try:
        from django.core.management import execute_from_command_line
        monitor_sftp_server()
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
