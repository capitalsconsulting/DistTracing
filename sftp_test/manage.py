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

def delete_files(directory):
    try:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path):
                    print(" file deleted ", file_path)
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error deleting file: {e}")
    except Exception as e:
        print(" Err on existing file delete ", str(e))

def track_1():
    print("> tracking for sftp1 startings...")
    while True:
        try:
            delete_files(settings.MEDIA_ROOT)
            email = EmailMessage(
                subject='OneSource',
                body='New File Received',
                from_email='pete@capitalsconsulting.com',
                to=['distributorsubmission@k-1c80vq6gka4vsdayfbc3rszgm8s46rwd2iyub7xcjmeakewsxj.46-zomweai.na210.apex.salesforce.com'],
            )
            
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None  # Disable host key verification
            with pysftp.Connection(
                settings.SFTP_HOST,
                username=settings.SFTP_USERNAME,
                password=settings.SFTP_PASSWORD,
                cnopts=cnopts
            ) as sftp:
                sftp.cwd(settings.SFTP_REMOTE_DIR)

                files = sftp.listdir()
                for filename in files:
                    if filename not in ['.', '..'] and filename.find('.csv') != -1:
                        try: 
                            print("> new file detection on sftp1: ", filename)
                            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            
                            local_filepath = os.path.join(settings.MEDIA_ROOT, filename)
                            remote_filepath = os.path.join(sftp.getcwd(), filename)
                            new_remote_filepath = os.path.join(sftp.getcwd()+"processed/", filename[:-4]+now+'.csv')
                            # print(" new_remote_filepath ", new_remote_filepath)
                            if not os.path.exists(local_filepath):  # Download only if the file doesn't exist locally
                                print("> file attaching from sftp1...")
                                sftp.get(remote_filepath, local_filepath)
                                data = []
                                with open(local_filepath, 'r', errors='ignore') as file:
                                    reader = csv.reader(file)

                                    for row in reader:
                                        try:
                                            updated_row = [
                                            strip_string(field).replace("\r\n", " ").replace("\n", "").replace('€', '\\u20AC').replace('á', '\\u00E1').replace('Ä', '').replace('¢','').replace('ì','').replace('*','').replace(';','').replace(':','').replace('~','').replace('°','').replace('ß','').replace('ö','').replace('ô','').replace('ó','').replace('ò','').replace('Ç','').replace('ü','').replace('é','').replace('â','').replace('ä','').replace('à','').replace('å','').replace('ç','').replace('ê','').replace('ë','').replace('è','').replace('ï','').replace('î','').replace('ì','').replace('æ','').replace('Æ','').replace('ö','').replace('ò','').replace('û','').replace('ù','').replace('ÿ','').replace('¢','').replace('£','').replace('¥','').replace('ƒ','').replace('á','').replace('í','').replace('ó','').replace('ú','').replace('ñ','').replace('Ñ','').replace('°','').replace('·','').replace('²','').replace('Ÿ','').replace('©','').replace('®','').replace('À','').replace('Á','').replace('Â','').replace('Ã','').replace('Ä','').replace('Å','').replace('È','').replace('É','').replace('Ê','').replace('Ë','').replace('Ì','').replace('Í','').replace('Î','').replace('Ï','').replace('Ð','').replace('Ò','').replace('Ó','').replace('Ô','').replace('Õ','').replace('Ö','').replace('×','').replace('Ø','').replace('Ù','').replace('Ú','').replace('Û','').replace('Ü','').replace('Ý','').replace('Þ','').replace('ã','').replace('ð','').replace('õ','').replace(']','').replace('*','').replace(',','') for field in row]
                                            data.append(updated_row)
                                        except UnicodeDecodeError:
                                            data.append(row)
                                            continue

                                with open(local_filepath, "w", newline='', errors='ignore') as myfile:

                                    writer = csv.writer(myfile)
                                    for row in data:
                                        writer.writerow(row)
                                
                                email.attach_file(local_filepath)
                                sftp.rename(remote_filepath, new_remote_filepath)
                                os.remove(local_filepath)
                                # Perform further processing on the downloaded file if needed
                        except Exception as e:
                            print(" Error on sftp1 file processing ", e)
                    # else:
                    #     print("> extra files ", filename)
                sftp.close()
            if len(email.attachments) > 0:
                email.send()
                print("> attached files ", len(email.attachments), " email for sftp1 sent")
            # Sleep for some time before checking for new files again
        except Exception as e:
            print("Err on sftp1 : ", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), " > ", str(e))
        time.sleep(10)  # Adjust the sleep time as per your requirements

def track_2():
    print("  > tracking for sftp2 starting")
    while True:
        try:
            delete_files(settings.MEDIA_ROOT2)
            email2 = EmailMessage(
                subject='Edwards',
                body='New File Received',
                from_email='pete@capitalsconsulting.com',
                to=['distributorsubmission@k-1c80vq6gka4vsdayfbc3rszgm8s46rwd2iyub7xcjmeakewsxj.46-zomweai.na210.apex.salesforce.com'],
            )
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None  # Disable host key verification
            with pysftp.Connection(
                settings.SFTP_HOST2,
                username=settings.SFTP_USERNAME2,
                password=settings.SFTP_PASSWORD2,
                cnopts=cnopts
            ) as sftp:
                sftp.cwd(settings.SFTP_REMOTE_DIR2)
                files = sftp.listdir()
                for filename in files:
                    
                    if filename not in ['.', '..'] and filename.find('.csv') != -1:
                        try:
                            print("  > new file detection on sftp2: ", filename)
                            local_filepath = os.path.join(settings.MEDIA_ROOT2, filename)
                            remote_filepath = os.path.join(sftp.getcwd(), filename)

                            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            
                            if not os.path.exists(local_filepath):  # Download only if the file doesn't exist locally
                                print("> file attaching from sftp2...")
                                sftp.get(remote_filepath, local_filepath)
                                

                                data = []
                                with open(local_filepath, "r", errors='ignore') as file:
                                    reader = csv.reader(file)
                                    for row in reader:
                                        try:
                                            updated_row = [
                                                strip_string(field).replace("\r\n", " ").replace("\n", "").replace('€', '\\u20AC').replace('á', '\\u00E1').replace('Ä', '').replace('¢','').replace('ì','').replace('*','').replace(';','').replace(':','').replace('~','').replace('°','').replace('ß','').replace('ö','').replace('ô','').replace('ó','').replace('ò','').replace('Ç','').replace('ü','').replace('é','').replace('â','').replace('ä','').replace('à','').replace('å','').replace('ç','').replace('ê','').replace('ë','').replace('è','').replace('ï','').replace('î','').replace('ì','').replace('æ','').replace('Æ','').replace('ö','').replace('ò','').replace('û','').replace('ù','').replace('ÿ','').replace('¢','').replace('£','').replace('¥','').replace('ƒ','').replace('á','').replace('í','').replace('ó','').replace('ú','').replace('ñ','').replace('Ñ','').replace('°','').replace('·','').replace('²','').replace('Ÿ','').replace('©','').replace('®','').replace('À','').replace('Á','').replace('Â','').replace('Ã','').replace('Ä','').replace('Å','').replace('È','').replace('É','').replace('Ê','').replace('Ë','').replace('Ì','').replace('Í','').replace('Î','').replace('Ï','').replace('Ð','').replace('Ò','').replace('Ó','').replace('Ô','').replace('Õ','').replace('Ö','').replace('×','').replace('Ø','').replace('Ù','').replace('Ú','').replace('Û','').replace('Ü','').replace('Ý','').replace('Þ','').replace('ã','').replace('ð','').replace('õ','').replace(']','').replace('*','').replace(',','') for field in row]

                                            data.append(updated_row)
                                        except UnicodeDecodeError:
                                            data.append(row)
                                            continue
                                
                                # with fileinput.FileInput(files=local_filepath, inplace=True, mode='rU') as file:
                                with open(local_filepath, "w", newline='', errors='ignore') as myfile:

                                    writer = csv.writer(myfile)
                                    for row in data:
                                        writer.writerow(row)

                                email2.attach_file(local_filepath)
                                sftp.remove(remote_filepath)
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
                                
                                os.remove(local_filepath)
                                sftp3.close()
                                # Perform further processing on the downloaded file if needed
                            # else:
                            #     print("  >> extra files ", filename)
                        except Exception as e:
                            print(" Error on sftp2 file processing ", e)
                sftp.close()
            if len(email2.attachments) > 0:
                email2.send()
                print("  > attached fles ", len(email2.attachments), " email for sftp2 sent")
                
        except Exception as e:
            print("Err on sftp2 : ", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), " > ", str(e))
        time.sleep(10)  # Adjust the sleep time as per your requirements

def track_3():
    print("    > tracking for sftp3 starting...")

    while True:
        try:
            delete_files(settings.MEDIA_ROOT3)
            email3 = EmailMessage(
                subject='Byram',
                body='New File Received',
                from_email='pete@capitalsconsulting.com',
                to=['distributorsubmission@k-1c80vq6gka4vsdayfbc3rszgm8s46rwd2iyub7xcjmeakewsxj.46-zomweai.na210.apex.salesforce.com'],
            )
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None  # Disable host key verification
            with pysftp.Connection(
                settings.SFTP_HOST3,
                username=settings.SFTP_USERNAME3,
                password=settings.SFTP_PASSWORD3,
                cnopts=cnopts
            ) as sftp:
                sftp.cwd(settings.SFTP_REMOTE_DIR3)
                files = sftp.listdir()

                for filename in files:
                    try:
                    
                        if filename not in ['.', '..'] and filename.find('.csv') != -1:
                            print("    >> new file detection on sftp3 : ", filename)

                            local_filepath = os.path.join(settings.MEDIA_ROOT3, filename)
                            remote_filepath = os.path.join(sftp.getcwd(), filename)

                            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            new_remote_filepath = os.path.join(sftp.getcwd()+"/../processed_byram/", filename[:-4]+" "+now+'.csv')
                            if not os.path.exists(local_filepath):
                                print("> file attaching from sftp3...")
                                sftp.get(remote_filepath, local_filepath)
                                data = []
                                with open(local_filepath, "r", errors='ignore') as file:
                                    reader = csv.reader(file)
                                    for row in reader:
                                        try:
                                            updated_row = [
                                                strip_string(field).replace("\r\n", " ").replace("\n", "").replace('€', '\\u20AC').replace('á', '\\u00E1').replace('Ä', '').replace('¢','').replace('ì','').replace('*','').replace(';','').replace(':','').replace('~','').replace('°','').replace('ß','').replace('ö','').replace('ô','').replace('ó','').replace('ò','').replace('Ç','').replace('ü','').replace('é','').replace('â','').replace('ä','').replace('à','').replace('å','').replace('ç','').replace('ê','').replace('ë','').replace('è','').replace('ï','').replace('î','').replace('ì','').replace('æ','').replace('Æ','').replace('ö','').replace('ò','').replace('û','').replace('ù','').replace('ÿ','').replace('¢','').replace('£','').replace('¥','').replace('ƒ','').replace('á','').replace('í','').replace('ó','').replace('ú','').replace('ñ','').replace('Ñ','').replace('°','').replace('·','').replace('²','').replace('Ÿ','').replace('©','').replace('®','').replace('À','').replace('Á','').replace('Â','').replace('Ã','').replace('Ä','').replace('Å','').replace('È','').replace('É','').replace('Ê','').replace('Ë','').replace('Ì','').replace('Í','').replace('Î','').replace('Ï','').replace('Ð','').replace('Ò','').replace('Ó','').replace('Ô','').replace('Õ','').replace('Ö','').replace('×','').replace('Ø','').replace('Ù','').replace('Ú','').replace('Û','').replace('Ü','').replace('Ý','').replace('Þ','').replace('ã','').replace('ð','').replace('õ','').replace(']','').replace('*','').replace(',','') for field in row]

                                            data.append(updated_row)
                                        except UnicodeDecodeError:
                                            data.append(row)
                                            continue
                                
                                # with fileinput.FileInput(files=local_filepath, inplace=True, mode='rU') as file:
                                with open(local_filepath, "w", newline='', errors='ignore') as myfile:

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
                                sftp.rename(remote_filepath, new_remote_filepath)
                                os.remove(local_filepath)
                                print(" new sftp path ", new_remote_filepath)
                                # Perform further processing on the downloaded file if needed
                        # else:
                        #     print("    >> extra files ", filename)
                    except Exception as e:
                        print(" Error on sftp3 file processing ", e)
                sftp.close()
            if len(email3.attachments) > 0:
                email3.send()
                print("      > attached files ", len(email3.attachments), " eamil for sftp3 sent")
        except Exception as e:
            print("Err on sftp3 : ", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), " > ", str(e))
        time.sleep(10)  # Adjust the sleep time as per your requirements

def track_4():
    print("      > tracking for sftp4 starting...")

    while True:
        try:
            delete_files(settings.MEDIA_ROOT4)
            email4 = EmailMessage(
                subject='Premier Kids',
                body='New File Received',
                from_email='pete@capitalsconsulting.com',
                to=['distributorsubmission@k-1c80vq6gka4vsdayfbc3rszgm8s46rwd2iyub7xcjmeakewsxj.46-zomweai.na210.apex.salesforce.com'],
            )
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None  # Disable host key verification
            with pysftp.Connection(
                settings.SFTP_HOST3,
                username=settings.SFTP_USERNAME3,
                password=settings.SFTP_PASSWORD3,
                cnopts=cnopts
            ) as sftp:
                sftp.cwd(settings.SFTP_REMOTE_DIR4)
                files = sftp.listdir()
                for filename in files:
                    try:
                        if filename not in ['.', '..'] and filename.find('.csv') != -1:
                            print("      >> new file detection for sftp4: ", filename)

                            local_filepath = os.path.join(settings.MEDIA_ROOT4, filename)
                            remote_filepath = os.path.join(sftp.getcwd(), filename)

                            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            new_remote_filepath = os.path.join(sftp.getcwd()+"/../processed_premierkids/", filename[:-4]+" "+now+'.csv')
                            if not os.path.exists(local_filepath):  # Download only if the file doesn't exist locally
                                print("> file attaching from sftp4...")
                                sftp.get(remote_filepath, local_filepath)
                                data = []
                                with open(local_filepath, "r", errors='ignore') as file:
                                    reader = csv.reader(file)
                                    for row in reader:
                                        try:
                                            updated_row = [
                                                strip_string(field).replace("\r\n", " ").replace("\n", "").replace('€', '\\u20AC').replace('á', '\\u00E1').replace('Ä', '').replace('¢','').replace('ì','').replace('*','').replace(';','').replace(':','').replace('~','').replace('°','').replace('ß','').replace('ö','').replace('ô','').replace('ó','').replace('ò','').replace('Ç','').replace('ü','').replace('é','').replace('â','').replace('ä','').replace('à','').replace('å','').replace('ç','').replace('ê','').replace('ë','').replace('è','').replace('ï','').replace('î','').replace('ì','').replace('æ','').replace('Æ','').replace('ö','').replace('ò','').replace('û','').replace('ù','').replace('ÿ','').replace('¢','').replace('£','').replace('¥','').replace('ƒ','').replace('á','').replace('í','').replace('ó','').replace('ú','').replace('ñ','').replace('Ñ','').replace('°','').replace('·','').replace('²','').replace('Ÿ','').replace('©','').replace('®','').replace('À','').replace('Á','').replace('Â','').replace('Ã','').replace('Ä','').replace('Å','').replace('È','').replace('É','').replace('Ê','').replace('Ë','').replace('Ì','').replace('Í','').replace('Î','').replace('Ï','').replace('Ð','').replace('Ò','').replace('Ó','').replace('Ô','').replace('Õ','').replace('Ö','').replace('×','').replace('Ø','').replace('Ù','').replace('Ú','').replace('Û','').replace('Ü','').replace('Ý','').replace('Þ','').replace('ã','').replace('ð','').replace('õ','').replace(']','').replace('*','').replace(',','') for field in row]

                                            data.append(updated_row)
                                        except UnicodeEncodeError:
                                            data.append(row)
                                            continue
                                
                                # with fileinput.FileInput(files=local_filepath, inplace=True, mode='rU') as file:
                                with open(local_filepath, "w", newline='', errors='ignore') as myfile:

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
                                sftp.rename(remote_filepath, new_remote_filepath)
                                os.remove(local_filepath)
                                print(" new sftp path ", new_remote_filepath)
                                # Perform further processing on the downloaded file if needed
                        # else:
                        #     print("    >> extra files ", filename)
                    except Exception as e:
                        print(" Error on sftp4 file processing ", e)
                sftp.close()
            if len(email4.attachments) > 0:
                email4.send()
                print("len(email4.attachments) ", len(email4.attachments))
            
        except Exception as e:
            print("Err on sftp4 : ", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), " > ", str(e))
        time.sleep(10)  # Adjust the sleep time as per your requirements


def track_5():
    print("        > tracking for sftp5 starting...")

    while True:
        try:
            delete_files(settings.MEDIA_ROOT5)
            email5 = EmailMessage(
                subject='CCS',
                body='New File Received',
                from_email='pete@capitalsconsulting.com',
                to=['distributorsubmission@k-1c80vq6gka4vsdayfbc3rszgm8s46rwd2iyub7xcjmeakewsxj.46-zomweai.na210.apex.salesforce.com'],
            )
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None  # Disable host key verification
            with pysftp.Connection(
                settings.SFTP_HOST3,
                username=settings.SFTP_USERNAME3,
                password=settings.SFTP_PASSWORD3,
                cnopts=cnopts
            ) as sftp:
                sftp.cwd(settings.SFTP_REMOTE_DIR5)
                files = sftp.listdir()
                for filename in files:
                    try:
                        if filename not in ['.', '..'] and filename.find('.csv') != -1:
                            print("        >> new file detection for sftp5: ", filename)

                            local_filepath = os.path.join(settings.MEDIA_ROOT5, filename)
                            remote_filepath = os.path.join(sftp.getcwd(), filename)

                            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            new_remote_filepath = os.path.join(sftp.getcwd()+"/../processed_ccs/", filename[:-4]+" "+now+'.csv')
                            if not os.path.exists(local_filepath):  # Download only if the file doesn't exist locally
                                print("> file attaching from sftp5...")
                                sftp.get(remote_filepath, local_filepath)
                                data = []
                                with open(local_filepath, "r", errors='ignore') as file:
                                    reader = csv.reader(file)
                                    for row in reader:
                                        try:
                                            updated_row = [
                                                strip_string(field).replace("\r\n", " ").replace("\n", "").replace('€', '\\u20AC').replace('á', '\\u00E1').replace('Ä', '').replace('¢','').replace('ì','').replace('*','').replace(';','').replace(':','').replace('~','').replace('°','').replace('ß','').replace('ö','').replace('ô','').replace('ó','').replace('ò','').replace('Ç','').replace('ü','').replace('é','').replace('â','').replace('ä','').replace('à','').replace('å','').replace('ç','').replace('ê','').replace('ë','').replace('è','').replace('ï','').replace('î','').replace('ì','').replace('æ','').replace('Æ','').replace('ö','').replace('ò','').replace('û','').replace('ù','').replace('ÿ','').replace('¢','').replace('£','').replace('¥','').replace('ƒ','').replace('á','').replace('í','').replace('ó','').replace('ú','').replace('ñ','').replace('Ñ','').replace('°','').replace('·','').replace('²','').replace('Ÿ','').replace('©','').replace('®','').replace('À','').replace('Á','').replace('Â','').replace('Ã','').replace('Ä','').replace('Å','').replace('È','').replace('É','').replace('Ê','').replace('Ë','').replace('Ì','').replace('Í','').replace('Î','').replace('Ï','').replace('Ð','').replace('Ò','').replace('Ó','').replace('Ô','').replace('Õ','').replace('Ö','').replace('×','').replace('Ø','').replace('Ù','').replace('Ú','').replace('Û','').replace('Ü','').replace('Ý','').replace('Þ','').replace('ã','').replace('ð','').replace('õ','').replace(']','').replace('*','').replace(',','') for field in row]

                                            data.append(updated_row)
                                        except UnicodeEncodeError:
                                            data.append(row)
                                            continue
                                
                                # with fileinput.FileInput(files=local_filepath, inplace=True, mode='rU') as file:
                                with open(local_filepath, "w", newline='', errors='ignore') as myfile:

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
                                email5.attach_file(local_filepath)
                                sftp.rename(remote_filepath, new_remote_filepath)
                                os.remove(local_filepath)
                                print(" new sftp path ", new_remote_filepath)
                                # Perform further processing on the downloaded file if needed
                        # else:
                        #     print("    >> extra files ", filename)
                    except Exception as e:
                        print(" Error on sftp5 file processing ", e)
                sftp.close()
            if len(email5.attachments) > 0:
                email5.send()
                print("len(email5.attachments) ", len(email5.attachments))
            
        except Exception as e:
            print("Err on sftp5 : ", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), " > ", str(e))
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
    t5 = threading.Thread(target=track_5)
    t5.start()
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
