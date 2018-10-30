'''
Some utilities like file upload handler
Created by Qinyu Liu
Created at 2018-10-15
'''
import os
import time
import zipfile
import nltk
from django.conf import settings
from .models import ResultFile, QueryItem, Directory, Profile, File, SentenceItem
from IFN702.utils import byte_to_string

def handle_file_upload(request):
    f = request.FILES['file_field']
    username = request.user.username
    original_name, file_extension = os.path.splitext(f.name)
    accepted_file_ext = ['.txt', '.zip']
    sent_in_total = 100 # If 100 then save to file
    sent_count = 0
    sentence_list = []

    # File extension checks
    file_check_results = {}
    file_check_results['file_not_accepted'] = []
    file_check_results['file_accepted'] = []

    if file_extension == ".zip":

        unzipped = zipfile.ZipFile(f)
        for innerfile in unzipped.namelist():
            # Generate Path & Validate file contents
            if innerfile.startswith('__MAC'):
                continue
            else:
                name, ext = os.path.splitext(innerfile)
                if ext not in accepted_file_ext:
                    file_check_results['file_not_accepted'].append(innerfile)
                    continue

                file_check_results['file_accepted'].append(innerfile)
                # Open the accepted file
                content_byte = unzipped.open(innerfile).read()
                content_str = byte_to_string(content_byte)

                # Using tokenizer to see how many sentences
                sentences = nltk.sent_tokenize(content_str)
                for sentence in sentences:
                    # Check at least 3 words in a sentence
                    words = nltk.word_tokenize(sentence)
                    if len(words) < 3:
                        continue

                    # Save this sentence
                    sentence_list.append(sentence)
                    sent_count += 1

                    if sent_count == sent_in_total:
                        # Save to file
                        filename = "%s_%s_%s%s" % (original_name, time.time(), username, ".txt")
                        path = "%s%s" % (settings.MEDIA_ROOT, "/" + username + "_" + original_name + "/")
                        if not os.path.exists(path):
                            os.makedirs(path)
                        upload_path = "%s%s" % (path, filename)

                        # Create user profile if it doesn't exist
                        if Profile.objects.filter(owner=username).count() == 0:
                            profile = Profile()
                            profile.owner = username
                            profile.save()
                        profile = Profile.objects.get(owner=username)

                        # Create directory if it doesn't exist
                        # Zip file name as directory_name
                        if Directory.objects.filter(directory_name=original_name, owner=username).count() == 0:
                            directory = Directory()
                            directory.directory_name = original_name
                            directory.owner = username
                            directory.save()
                        directory = Directory.objects.get(directory_name=original_name, owner=username)

                        file = File()
                        file.file_name = filename
                        file.file_path = upload_path
                        file.file_content = []
                        with open(upload_path, 'wb+') as destination:
                            for s in sentence_list:
                                destination.write(s.encode('utf-8'))
                                sent_item = SentenceItem()
                                sent_item.sentence = s
                                file.file_content.append(sent_item)
                            destination.close()
                            file.save()
                            directory.file.add(file)
                            directory.save()
                            profile.directory.add(directory)
                            profile.save()
                        # Initialize variables
                        sentence_list = []
                        sent_count = 0
        # All files are processed
        if sent_count != 0:
            # Save to file
            filename = "%s_%s_%s%s" % (original_name, time.time(), username, ".txt")
            path = "%s%s" % (settings.MEDIA_ROOT, "/" + username + "_" + original_name + "/")
            if not os.path.exists(path):
                os.makedirs(path)
            upload_path = "%s%s" % (path, filename)

            # Create user profile if it doesn't exist
            if Profile.objects.filter(owner=username).count() == 0:
                profile = Profile()
                profile.owner = username
                profile.save()
            profile = Profile.objects.get(owner=username)

            # Create directory if it doesn't exist
            # Zip file name as directory_name
            if Directory.objects.filter(directory_name=original_name, owner=username).count() == 0:
                directory = Directory()
                directory.directory_name = original_name
                directory.owner = username
                directory.save()
            directory = Directory.objects.get(directory_name=original_name, owner=username)

            file = File()
            file.file_name = filename
            file.file_path = upload_path
            file.file_content = []
            with open(upload_path, 'wb+') as destination:
                for s in sentence_list:
                    destination.write(s.encode('utf-8'))
                    sent_item = SentenceItem()
                    sent_item.sentence = s
                    file.file_content.append(sent_item)
                destination.close()
                file.save()
                directory.file.add(file)
                directory.save()
                profile.directory.add(directory)
                profile.save()
        return file_check_results
    elif file_extension == ".txt":

        content_byte = f.read()
        content_str = byte_to_string(content_byte)

        # Using tokenizer to see how many sentences
        sentences = nltk.sent_tokenize(content_str)
        for sentence in sentences:
            # Check at least 3 words in a sentence
            words = nltk.word_tokenize(sentence)
            if len(words) < 3:
                continue

            # Save this sentence
            sentence_list.append(sentence)
            sent_count += 1

            if sent_count == sent_in_total:
                # Save to file
                filename = "%s_%s_%s%s" % (original_name, time.time(), username, ".txt")
                path = "%s%s" % (settings.MEDIA_ROOT, "/" + username + "_Default/")
                if not os.path.exists(path):
                    os.makedirs(path)
                upload_path = "%s%s" % (path, filename)

                # Create user profile if it doesn't exist
                if Profile.objects.filter(owner=username).count() == 0:
                    profile = Profile()
                    profile.owner = username
                    profile.save()
                profile = Profile.objects.get(owner=username)

                # Create directory if it doesn't exist
                dir_name = "Default"
                # Zip file name as directory_name
                if Directory.objects.filter(directory_name=dir_name, owner=username).count() == 0:
                    directory = Directory()
                    directory.directory_name = dir_name
                    directory.owner = username
                    directory.save()
                directory = Directory.objects.get(directory_name=dir_name, owner=username)

                file = File()
                file.file_name = filename
                file.file_path = upload_path
                file.file_content = []
                with open(upload_path, 'wb+') as destination:
                    for s in sentence_list:
                        destination.write(s.encode('utf-8'))
                        sent_item = SentenceItem()
                        sent_item.sentence = s
                        file.file_content.append(sent_item)
                    destination.close()
                    file.save()
                    directory.file.add(file)
                    directory.save()
                    profile.directory.add(directory)
                    profile.save()
                # Initialize variables
                sentence_list = []
                sent_count = 0
                file_check_results['file_accepted'].append(filename)

        # Save rest if existed
        if sent_count != 0:
            # Save to file
            filename = "%s_%s_%s%s" % (original_name, time.time(), username, ".txt")
            path = "%s%s" % (settings.MEDIA_ROOT, "/" + username + "_Default/")
            if not os.path.exists(path):
                os.makedirs(path)
            upload_path = "%s%s" % (path, filename)

            # Create user profile if it doesn't exist
            if Profile.objects.filter(owner=username).count() == 0:
                profile = Profile()
                profile.owner = username
                profile.save()
            profile = Profile.objects.get(owner=username)

            # Create directory if it doesn't exist
            dir_name = "Default"
            # Zip file name as directory_name
            if Directory.objects.filter(directory_name=dir_name, owner=username).count() == 0:
                directory = Directory()
                directory.directory_name = dir_name
                directory.owner = username
                directory.save()
            directory = Directory.objects.get(directory_name=dir_name, owner=username)

            file = File()
            file.file_name = filename
            file.file_path = upload_path
            file.file_content = []
            with open(upload_path, 'wb+') as destination:
                for s in sentence_list:
                    destination.write(s.encode('utf-8'))
                    sent_item = SentenceItem()
                    sent_item.sentence = s
                    file.file_content.append(sent_item)
                destination.close()
                file.save()
                directory.file.add(file)
                directory.save()
                profile.directory.add(directory)
                profile.save()
            # Initialize variables
            sentence_list = []
            sent_count = 0

        return file_check_results
    else:
        raise Exception("Extension not accepted.")



def handle_result_file(request):
    f = request.FILES['file_field']
    original_name, file_extension = os.path.splitext(f.name)
    # 拼接新的文件名
    filename = "%s_%s%s" % (original_name, time.time(), file_extension)
    # 拼接文件上传目录
    path = "%s%s" % (settings.MEDIA_ROOT, "/Results/")
    # 如果目录不存在，创建此目录
    if not os.path.exists(path):
        os.makedirs(path)
    # 拼接文件上传存放文件路径
    upload_path = "%s%s" % (path, filename)
    if not os.path.isfile:
        raise Exception("Must be a single file!")
    
    # For bootstrap-table
    file_obj = {}
    file_obj['filename'] = filename
    file_obj['data'] = []

    # Save files
    file = ResultFile()
    file.file_name = filename
    file.file_path = path
    file.owner = request.user.username
    file.file_content = []
    with open(upload_path, 'wb+') as destination:
        start = 0;
        for line in f:
            destination.write(line)
            if start != 0:
                items = byte_to_string(line).splitlines()[0].strip().split( )
                if len(items) == 2:
                    q = QueryItem()
                    q.items = items[0]
                    q.support = items[1]
                    q.weight = 0
                    file.file_content.append(q)

                     # For bootstrap-table
                    file_obj['data'].append({
                        'words': items[0],
                        'support': items[1]
                        })
                if len(items) == 3:
                    q = QueryItem()
                    q.items = items[0]
                    q.weight = items[1]
                    q.support = items[2]
                    file.file_content.append(q)

                     # For bootstrap-table
                    file_obj['data'].append({
                        'words': items[0],
                        'weight': items[1],
                        'support': items[2]
                        })
            start += 1;
        destination.close()
    file.save()
    return file_obj