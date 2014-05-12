#!/usr/bin/python

import os
import sys
import csv
import time
import re
import subprocess
import shutil

print time.ctime()

# Get path from ARGV, compute name of index file
path = "Papers/"
if (len(sys.argv) > 1):
    path = sys.argv[1]
index = "Files/"
if not os.path.exists(index):
    os.makedirs(index)
index += re.sub("/", ".", path)

modifieds    = {}
subjects     = {}
titles       = {}
authors      = {}
keywords     = {}

# Function to scrape metadata from a file

def get_meta(file):
    subject  = ""
    title    = ""
    author   = ""
    keywords = ""
    try:
        meta = subprocess.check_output(['pdftk', file, 'dump_data'])
        lines = meta.splitlines()
        for j, item in enumerate(lines):
            if (item.find("InfoKey: Subject") != -1):
                datum = lines[j+1]
                datum = re.sub(r".*InfoValue: ", "", datum)
                subject = datum.rstrip()
            if (item.find("InfoKey: Author") != -1):
                datum = lines[j+1]
                datum = re.sub(r".*InfoValue: ", "", datum)
                author = datum.rstrip()
            if (item.find("InfoKey: Title") != -1):
                datum = lines[j+1]
                datum = re.sub(r".*InfoValue: ", "", datum)
                title = datum.rstrip()
            if (item.find("InfoKey: Keywords") != -1):
                datum = lines[j+1]
                datum = re.sub(r".*InfoValue: ", "", datum)
                keywords = datum.rstrip()
    except:
        return ['.', '.', '.', "."]
    return [subject] + [title] + [author] + [keywords]

# Function to replace metadata in a file

def put_meta(file, row):
    subject  = row[0]
    title    = row[1]
    author   = row[2]
    keywords = row[3]
    try:
        meta = subprocess.check_output(['pdftk', file, 'dump_data'])
        lines = meta.splitlines()
        with open("Files/metadata.info", 'wb') as info:
            if (meta.find("InfoKey: Subject") == -1):
                info.write("InfoBegin" + os.linesep + "InfoKey: Subject" + os.linesep + "InfoValue: " + subject + os.linesep)
            if (meta.find("InfoKey: Author") == -1):
                info.write("InfoBegin" + os.linesep + "InfoKey: Author" + os.linesep + "InfoValue: " + author + os.linesep)
            if (meta.find("InfoKey: Title") == -1):
                info.write("InfoBegin" + os.linesep + "InfoKey: Title" + os.linesep + "InfoValue: " + title + os.linesep)
            if (meta.find("InfoKey: Keywords") == -1):
                info.write("InfoBegin" + os.linesep + "InfoKey: Keywords" + os.linesep + "InfoValue: " + title + os.linesep)
            for j, item in enumerate(lines):
                if (item.find("InfoKey: Subject") != -1):
                    lines[j+1] = "InfoValue: " + subject
                if (item.find("InfoKey: Author") != -1):
                    lines[j+1] = "InfoValue: " + author
                if (item.find("InfoKey: Title") != -1):
                    lines[j+1] = "InfoValue: " + title
                if (item.find("InfoKey: Keywords") != -1):
                    lines[j+1] = "InfoValue: " + keywords
                info.write(item + os.linesep)
        os.system('pdftk "' + file + '" cat output Files/noxmp.pdf')
        os.system('pdftk Files/noxmp.pdf update_info Files/metadata.info output "' + file + '"')
        os.system('rm Files/metadata.info Files/noxmp.pdf')
    except:
        print "Could not process file " + file

# Read in CSV file

try:
    with open(index + 'csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            file = row[0]
            while (len(row) < 6):
                row = row + ['']
            modifieds[file] = row[1]
            subjects[file]  = row[2]
            titles[file]    = row[3]
            authors[file]   = row[4]
            keywords[file]  = row[5]
except:
    print "Index not found, starting from scratch ..."

# Go find all files in the path ... collect metadata for those modified
# and Write back to CSV file

with open(index + 'new', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    for root, subFolders, files in os.walk(path):
        for item in files:
            file = os.path.join(root,item)
            if (file.find("pdf") == -1 and file.find("PDF") == -1):
                continue
            if (file.find("BOOKS") != -1):
                continue
            if (file.find("PHYSICS") != -1):
                continue
            if (file in modifieds.keys() and modifieds[file].find("rename") != -1):
                newfile = "[" + subjects[file] + "] " + titles[file] + ".pdf"
                newfile = newfile.replace("?","")
                newfile = newfile.replace("*","-star")
                newfile = newfile.replace("/","-")
                newfile = newfile.replace("/","-")
                newfile = newfile.replace(":"," -")
                newfile = newfile.replace("\"","'")
                newfile = newfile.replace("\\","'")
                newfile = newfile.replace("\t"," ")
                newfile = os.path.join(root, newfile)
                print "copying " + file + " to " + newfile
                shutil.copy(file, newfile)
                continue
            if (file in modifieds.keys() and modifieds[file].find("update") != -1):
                print "writing " + file
                row = [subjects[file]] + [titles[file]] + [authors[file]] + [keywords[file]]
                put_meta(file, row)
            mtime = os.path.getmtime(file)
            modified    = time.ctime(mtime)
            subject = ""
            title = ""
            author = ""
            keyword = ""
            if (file in modifieds.keys() and modified == modifieds[file]):
                subject  = subjects[file]
                title    = titles[file]
                author   = authors[file]
                keyword  = keywords[file]
            else:
                print "reading " + file
                row = get_meta(file)
                subject  = row[0]
                title    = row[1]
                author   = row[2]
                keyword  = row[3]
            spamwriter.writerow([file] + [modified] + [subject] + [title] + [author] + [keyword])

os.system('mv ' + index + 'csv ' + index + 'bak')
os.system('mv ' + index + 'new ' + index + 'csv')

print time.ctime()

