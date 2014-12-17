__author__ = 'sid'

import subprocess
import os
import time

imgdir = raw_input('Enter the directory name containing Images:')
metadataDir = "/home/sid/Desktop/MS/MongoDbDev/meta"
    # raw_input('Enter the directory name to store metadata files:')
tagsdirectory = raw_input('Enter the directory name of tag files:')

def read_file_names(directory_path):
    files = []
    for each_file in os.listdir(directory_path):
        files.append(each_file)

    return files


def generatemeta():
    # imgdir = raw_input('Enter the directory name containing Images:')
    # metadataDir = raw_input('Enter the directory name to store metadata files')
    imgnames = read_file_names(imgdir)
    for img in imgnames:
        subprocess.Popen(["./metagenerate.sh", str(imgdir + "/" + img), str(metadataDir + "/" + img.rstrip(".jpeg"))])


def formatJSON(filename, url, tagsfilename):
    filecontents = open(filename, "r")
    tagsfilecontent = open(tagsfilename, "r")
    metaJs = "{"
    for lines in filecontents.readlines():
        ind = lines.find(":")
        entityname = lines[:ind].rstrip(" ")
        entityvalue = lines[ind + 2:len(lines)].rstrip("\n")

        # get the file name
        if entityname == "File Name":
            fname = entityvalue
        if entityname == "Directory":
            entityvalue = url + fname
            entityname = "URL"

        metaJs += str('"') + str(entityname) + str('"') + ":" + str('"') + str(entityvalue) + str('"') + str(',')
    tags = ""
    for tag in tagsfilecontent:
        tags += tag.rstrip("\r\n") + ","
    tags = tags.rstrip(",")
    metaJs += str('"') + "Tags" + str('"') + ":" + str('"') + tags + str('"') + "}"

    return metaJs


def uploadDatatoMongo(metadata):
    time.sleep(3)
    subprocess.call(['curl', '-H', 'Content-Type: application/json', '-X', 'POST', '-d', metadata, 'http://localhost:3000/items'])

    print "Successfully Uploaded to MongoDB"

def createJSON():
    url = "https://github.com/iamsidshetty/Multimedia/blob/master/img/"
    metafilenames = sorted(read_file_names(metadataDir))
    tagsfilenames = sorted(read_file_names(tagsdirectory))
    metadataInJson = []

    # format the metadata in JSON format
    for i, metafiles in enumerate(metafilenames):
        metadataInJson.append(formatJSON(str(metadataDir + "/" + metafiles), url, str(tagsdirectory + "/" + tagsfilenames[i])))

    print "Metadata Creation Done!"
    return metadataInJson


def main():
    generatemeta()
    metadataInJson = createJSON()

    for meta in metadataInJson:
        uploadDatatoMongo(meta)


if __name__ == "__main__":
    main()
