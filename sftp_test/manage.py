#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django.conf import settings
import pysftp
import time
from django.core.mail import EmailMessage
import threading
import csv
import fileinput
import io
import datetime

def strip_string(string):
    return ''.join(string.splitlines())

def track_1():
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
            email = EmailMessage(
                subject='OneSource',
                body='New File Received',
                from_email='pete@capitalsconsulting.com',
                to=['distributorsubmission@k-1c80vq6gka4vsdayfbc3rszgm8s46rwd2iyub7xcjmeakewsxj.46-zomweai.na210.apex.salesforce.com'],
            )
            files = sftp.listdir()
            for filename in files:
                
                if filename not in ['.', '..'] and filename.find('.csv') != -1:
                    print("> csv file ", filename)
                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    local_filepath = os.path.join(settings.MEDIA_ROOT, filename)
                    remote_filepath = os.path.join(sftp.getcwd(), filename)
                    new_remote_filepath = os.path.join(sftp.getcwd()+"/processed/", filename[:-4]+now+'.csv')

                    if not os.path.exists(local_filepath):  # Download only if the file doesn't exist locally
                        print("> email sending...")
                        sftp.get(remote_filepath, local_filepath)
                        
                        data = []
                        with open(local_filepath, 'r') as file:
                            reader = csv.reader(file)
                            for row in reader:
                                updated_row = [
                                    strip_string(field).replace("\r\n", " ").replace("\n", "").replace('€', '\\u20AC').replace('á', '\\u00E1').replace('Ä', '').replace('¢','').replace('ì','').replace('*','').replace(';','').replace(':','').replace('~','').replace('°','').replace('ß','').replace('ö','').replace('ô','').replace('ó','').replace('ò','').replace('Ç','').replace('ü','').replace('é','').replace('â','').replace('ä','').replace('à','').replace('å','').replace('ç','').replace('ê','').replace('ë','').replace('è','').replace('ï','').replace('î','').replace('ì','').replace('æ','').replace('Æ','').replace('ö','').replace('ò','').replace('û','').replace('ù','').replace('ÿ','').replace('¢','').replace('£','').replace('¥','').replace('ƒ','').replace('á','').replace('í','').replace('ó','').replace('ú','').replace('ñ','').replace('Ñ','').replace('°','').replace('·','').replace('²','').replace('Ÿ','').replace('©','').replace('®','').replace('À','').replace('Á','').replace('Â','').replace('Ã','').replace('Ä','').replace('Å','').replace('È','').replace('É','').replace('Ê','').replace('Ë','').replace('Ì','').replace('Í','').replace('Î','').replace('Ï','').replace('Ð','').replace('Ò','').replace('Ó','').replace('Ô','').replace('Õ','').replace('Ö','').replace('×','').replace('Ø','').replace('Ù','').replace('Ú','').replace('Û','').replace('Ü','').replace('Ý','').replace('Þ','').replace('ã','').replace('ð','').replace('õ','').replace(']','').replace('*','').replace(',','') for field in row]
                                data.append(updated_row)

                        with open(local_filepath, "w", newline='') as myfile:

                            writer = csv.writer(myfile)
                            for row in data:
                                writer.writerow(row)
                        
                        email.attach_file(local_filepath)
                        os.remove(local_filepath)
                        sftp.rename(remote_filepath, new_remote_filepath)
                        # Perform further processing on the downloaded file if needed
                else:
                    print("> extra files ", filename)
            if len(email.attachments) > 0:
                email.send()
            # Sleep for some time before checking for new files again
            time.sleep(10)  # Adjust the sleep time as per your requirements

def track_2():
    print(">>>>>>>>>> function 2 is running...")
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None  # Disable host key verification
    with pysftp.Connection(
        settings.SFTP_HOST2,
        username=settings.SFTP_USERNAME2,
        password=settings.SFTP_PASSWORD2,
        cnopts=cnopts
    ) as sftp:
        sftp.cwd(settings.SFTP_REMOTE_DIR2)

        while True:
            files = sftp.listdir()
            email2 = EmailMessage(
                subject='Edwards',
                body='New File Received',
                from_email='pete@capitalsconsulting.com',
                to=['distributorsubmission@k-1c80vq6gka4vsdayfbc3rszgm8s46rwd2iyub7xcjmeakewsxj.46-zomweai.na210.apex.salesforce.com'],
            )

            for filename in files:
                
                if filename not in ['.', '..'] and filename.find('.csv') != -1:
                    print("  >> csv file ", filename)
                    local_filepath = os.path.join(settings.MEDIA_ROOT2, filename)
                    remote_filepath = os.path.join(sftp.getcwd(), filename)

                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                   
                    if not os.path.exists(local_filepath):  # Download only if the file doesn't exist locally
                        print("  >> email sending...")
                        sftp.get(remote_filepath, local_filepath)
                        sftp.remove(remote_filepath)

                        data = []
                        with open(local_filepath, "r") as file:
                            reader = csv.reader(file)
                            for row in reader:
                                updated_row = [
                                    strip_string(field).replace("\r\n", " ").replace("\n", "").replace('€', '\\u20AC').replace('á', '\\u00E1').replace('Ä', '').replace('¢','').replace('ì','').replace('*','').replace(';','').replace(':','').replace('~','').replace('°','').replace('ß','').replace('ö','').replace('ô','').replace('ó','').replace('ò','').replace('Ç','').replace('ü','').replace('é','').replace('â','').replace('ä','').replace('à','').replace('å','').replace('ç','').replace('ê','').replace('ë','').replace('è','').replace('ï','').replace('î','').replace('ì','').replace('æ','').replace('Æ','').replace('ö','').replace('ò','').replace('û','').replace('ù','').replace('ÿ','').replace('¢','').replace('£','').replace('¥','').replace('ƒ','').replace('á','').replace('í','').replace('ó','').replace('ú','').replace('ñ','').replace('Ñ','').replace('°','').replace('·','').replace('²','').replace('Ÿ','').replace('©','').replace('®','').replace('À','').replace('Á','').replace('Â','').replace('Ã','').replace('Ä','').replace('Å','').replace('È','').replace('É','').replace('Ê','').replace('Ë','').replace('Ì','').replace('Í','').replace('Î','').replace('Ï','').replace('Ð','').replace('Ò','').replace('Ó','').replace('Ô','').replace('Õ','').replace('Ö','').replace('×','').replace('Ø','').replace('Ù','').replace('Ú','').replace('Û','').replace('Ü','').replace('Ý','').replace('Þ','').replace('ã','').replace('ð','').replace('õ','').replace(']','').replace('*','').replace(',','') for field in row]

                                data.append(updated_row)
                        
                        # with fileinput.FileInput(files=local_filepath, inplace=True, mode='rU') as file:
                        with open(local_filepath, "w", newline='') as myfile:

                            writer = csv.writer(myfile)
                            for row in data:
                                writer.writerow(row)

                        email2.attach_file(local_filepath)

                        
                        # sftp.remove(remote_filepath)
                        # sftp.rename(remote_filepath, new_remote_filepath)

                        with pysftp.Connection(
                            settings.SFTP_HOST3,
                            username=settings.SFTP_USERNAME3,
                            password=settings.SFTP_PASSWORD3,
                            cnopts=cnopts
                        ) as sftp3:
                            sftp3.cwd(settings.SFTP_REMOTE_TMP_DIR2)
                            new_remote_filepath = os.path.join(sftp3.getcwd(), filename[:-4]+now+'.csv')
                            sftp3.put(local_filepath, new_remote_filepath)
                        sftp3.close()
                        # Perform further processing on the downloaded file if needed
                        os.remove(local_filepath)
                else:
                    print("  >> extra files ", filename)
            
            if len(email2.attachments) > 0:
                email2.send()
            # Sleep for some time before checking for new files again
            time.sleep(10)  # Adjust the sleep time as per your requirements

def track_3():
    print(">>>>>>>>>> function 3 is running...")
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None  # Disable host key verification
    with pysftp.Connection(
        settings.SFTP_HOST3,
        username=settings.SFTP_USERNAME3,
        password=settings.SFTP_PASSWORD3,
        cnopts=cnopts
    ) as sftp:
        sftp.cwd(settings.SFTP_REMOTE_DIR3)

        while True:
            email3 = EmailMessage(
                subject='Byram',
                body='New File Received',
                from_email='pete@capitalsconsulting.com',
                to=['distributorsubmission@k-1c80vq6gka4vsdayfbc3rszgm8s46rwd2iyub7xcjmeakewsxj.46-zomweai.na210.apex.salesforce.com'],
            )
            files = sftp.listdir()
            for filename in files:
                
                if filename not in ['.', '..'] and filename.find('.csv') != -1:
                    print("    >> csv file ", filename)

                    local_filepath = os.path.join(settings.MEDIA_ROOT3, filename)
                    remote_filepath = os.path.join(sftp.getcwd(), filename)

                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    new_remote_filepath = os.path.join(sftp.getcwd()+"/../processed_byram/", filename[:-4]+" "+now+'.csv')
                    if not os.path.exists(local_filepath):  # Download only if the file doesn't exist locally
                        print("    >> email sending...")
                        sftp.get(remote_filepath, local_filepath)
                        
                        data = []
                        with open(local_filepath, "r") as file:
                            reader = csv.reader(file)
                            for row in reader:
                                updated_row = [
                                    strip_string(field).replace("\r\n", " ").replace("\n", "").replace('€', '\\u20AC').replace('á', '\\u00E1').replace('Ä', '').replace('¢','').replace('ì','').replace('*','').replace(';','').replace(':','').replace('~','').replace('°','').replace('ß','').replace('ö','').replace('ô','').replace('ó','').replace('ò','').replace('Ç','').replace('ü','').replace('é','').replace('â','').replace('ä','').replace('à','').replace('å','').replace('ç','').replace('ê','').replace('ë','').replace('è','').replace('ï','').replace('î','').replace('ì','').replace('æ','').replace('Æ','').replace('ö','').replace('ò','').replace('û','').replace('ù','').replace('ÿ','').replace('¢','').replace('£','').replace('¥','').replace('ƒ','').replace('á','').replace('í','').replace('ó','').replace('ú','').replace('ñ','').replace('Ñ','').replace('°','').replace('·','').replace('²','').replace('Ÿ','').replace('©','').replace('®','').replace('À','').replace('Á','').replace('Â','').replace('Ã','').replace('Ä','').replace('Å','').replace('È','').replace('É','').replace('Ê','').replace('Ë','').replace('Ì','').replace('Í','').replace('Î','').replace('Ï','').replace('Ð','').replace('Ò','').replace('Ó','').replace('Ô','').replace('Õ','').replace('Ö','').replace('×','').replace('Ø','').replace('Ù','').replace('Ú','').replace('Û','').replace('Ü','').replace('Ý','').replace('Þ','').replace('ã','').replace('ð','').replace('õ','').replace(']','').replace('*','').replace(',','') for field in row]

                                data.append(updated_row)
                        
                        # with fileinput.FileInput(files=local_filepath, inplace=True, mode='rU') as file:
                        with open(local_filepath, "w", newline='') as myfile:

                            writer = csv.writer(myfile)
                            for row in data:
                                writer.writerow(row)

                        # Opening our text file in write only
                        # mode to write the replaced content
                        # with open(local_filepath, 'w') as file:
                            # Writing the replaced data in our
                            # text file
                            # file.write(data)
                        # sftp.remove(remote_filepath)
                        email3.attach_file(local_filepath)
                        os.remove(local_filepath)
                        print(" new sftp path ", new_remote_filepath)
                        sftp.rename(remote_filepath, new_remote_filepath)
                        # Perform further processing on the downloaded file if needed
                else:
                    print("    >> extra files ", filename)
            print("len(email3.attachments) ", len(email3.attachments))
            if len(email3.attachments) > 0:
                print(" XXXX email sent XXXXX ")
                email3.send()
            # Sleep for some time before checking for new files again
            time.sleep(10)  # Adjust the sleep time as per your requirements

def track_4():
    print(">>>>>>>>>> function 3 is running...")
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None  # Disable host key verification
    with pysftp.Connection(
        settings.SFTP_HOST3,
        username=settings.SFTP_USERNAME3,
        password=settings.SFTP_PASSWORD3,
        cnopts=cnopts
    ) as sftp:
        sftp.cwd(settings.SFTP_REMOTE_DIR4)

        while True:
            email4 = EmailMessage(
                subject='Premier Kids',
                body='New File Received',
                from_email='pete@capitalsconsulting.com',
                to=['distributorsubmission@k-1c80vq6gka4vsdayfbc3rszgm8s46rwd2iyub7xcjmeakewsxj.46-zomweai.na210.apex.salesforce.com'],
            )
            files = sftp.listdir()
            for filename in files:
                
                if filename not in ['.', '..'] and filename.find('.csv') != -1:
                    print("    >> csv file ", filename)

                    local_filepath = os.path.join(settings.MEDIA_ROOT3, filename)
                    remote_filepath = os.path.join(sftp.getcwd(), filename)

                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    new_remote_filepath = os.path.join(sftp.getcwd()+"/../processed_premierkids/", filename[:-4]+" "+now+'.csv')
                    if not os.path.exists(local_filepath):  # Download only if the file doesn't exist locally
                        print("    >> email sending...")
                        sftp.get(remote_filepath, local_filepath)
                        
                        data = []
                        with open(local_filepath, "r") as file:
                            reader = csv.reader(file)
                            for row in reader:
                                updated_row = [
                                    strip_string(field).replace("\r\n", " ").replace("\n", "").replace('€', '\\u20AC').replace('á', '\\u00E1').replace('Ä', '').replace('¢','').replace('ì','').replace('*','').replace(';','').replace(':','').replace('~','').replace('°','').replace('ß','').replace('ö','').replace('ô','').replace('ó','').replace('ò','').replace('Ç','').replace('ü','').replace('é','').replace('â','').replace('ä','').replace('à','').replace('å','').replace('ç','').replace('ê','').replace('ë','').replace('è','').replace('ï','').replace('î','').replace('ì','').replace('æ','').replace('Æ','').replace('ö','').replace('ò','').replace('û','').replace('ù','').replace('ÿ','').replace('¢','').replace('£','').replace('¥','').replace('ƒ','').replace('á','').replace('í','').replace('ó','').replace('ú','').replace('ñ','').replace('Ñ','').replace('°','').replace('·','').replace('²','').replace('Ÿ','').replace('©','').replace('®','').replace('À','').replace('Á','').replace('Â','').replace('Ã','').replace('Ä','').replace('Å','').replace('È','').replace('É','').replace('Ê','').replace('Ë','').replace('Ì','').replace('Í','').replace('Î','').replace('Ï','').replace('Ð','').replace('Ò','').replace('Ó','').replace('Ô','').replace('Õ','').replace('Ö','').replace('×','').replace('Ø','').replace('Ù','').replace('Ú','').replace('Û','').replace('Ü','').replace('Ý','').replace('Þ','').replace('ã','').replace('ð','').replace('õ','').replace(']','').replace('*','').replace(',','') for field in row]

                                data.append(updated_row)
                        
                        # with fileinput.FileInput(files=local_filepath, inplace=True, mode='rU') as file:
                        with open(local_filepath, "w", newline='') as myfile:

                            writer = csv.writer(myfile)
                            for row in data:
                                writer.writerow(row)

                        # Opening our text file in write only
                        # mode to write the replaced content
                        # with open(local_filepath, 'w') as file:
                            # Writing the replaced data in our
                            # text file
                            # file.write(data)
                        # sftp.remove(remote_filepath)
                        email4.attach_file(local_filepath)
                        os.remove(local_filepath)
                        print(" new sftp path ", new_remote_filepath)
                        sftp.rename(remote_filepath, new_remote_filepath)
                        # Perform further processing on the downloaded file if needed
                else:
                    print("    >> extra files ", filename)
            print("len(email3.attachments) ", len(email4.attachments))
            if len(email4.attachments) > 0:
                print(" XXXX email sent XXXXX ")
                email4.send()
            # Sleep for some time before checking for new files again
            time.sleep(10)  # Adjust the sleep time as per your requirements

# @background(schedule=1)
def monitor_sftp_server():
    # SFTP connection credentials
   
    t1 = threading.Thread(target=track_1)
    t1.start()

    t2 = threading.Thread(target=track_2)
    t2.start()

    t3 = threading.Thread(target=track_3)
    t3.start()

    t4 = threading.Thread(target=track_4)
    t4.start()

    # tasks = []

    # task1 = asyncio.create_task(track_1())
    # tasks.append(task1)

    # task2 = asyncio.create_task(track_2())
    # tasks.append(task2)

    # # await asyncio.gather(task1, task2)
    # done, _ = await asyncio.wait([task1, task2], return_when=asyncio.FIRST_COMPLETED)

        
    

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
