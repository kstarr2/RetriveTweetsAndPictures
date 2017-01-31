#!/usr/bin/env python
# encoding: utf-8

import urllib.request
import shutil
import os
import errno
import sys
import csv
import tweet_dumper

def get_urls(listObjofPics, userName):
    """Retrives URLs from the csv file generated from tweet_dumper.py"""

    with open('%s_pic_tweets.csv' %userName, newline='') as csvfile:
        # skipinitialspace=True in order to avoid ',' delimiter issues in row[2] from tweet text
        reader = csv.reader(csvfile, delimiter=',', quotechar='"', skipinitialspace=True)
        
        for row in reader:
            listObjofPics.append(row[3])
      
    return listObjofPics


def create_directory():
    """Creates a new directory for all the images retrieved."""
    try:
        if os.path.isdir("./imagesFromTweets") != True:
            os.makedirs("./imagesFromTweets")

    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def download_images(urlList):
    """retrieves urls from get_urls(), then uses urllib and shutil to download them."""
    fileNumber = 1;
    fileName = ""

    # urlList[0] is just titles, so we start at 1
    for url in urlList[1:]:
        sys.stdout.write("\rFile number %i of %i " % (fileNumber+1, len(urlList)))

        sys.stdout.flush()

        try:
            fileName = str(fileNumber) + ".png"
            # Download the file from `url` and save it locally under `fileName`:
            # I append png to the end of the file to "make it" png, but there's definitely a better way
            with urllib.request.urlopen(url) as response, open(fileName, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
        except urllib.error.HTTPError:
            sys.stdout.flush()
            print("\r %s is not a downloadable image. Skipping to next url..." % url)
        
        fileNumber +=  1;

    sys.stdout.write("\r\nDone!")
    sys.stdout.flush()
    sys.stdout.write("\r\n")
    

if __name__ == '__main__':
    # Enter your username in place of mine! 
    userName = "kathy_starr"

    tweet_dumper.get_all_tweets(userName)

    listOfPictureUrls = []

    get_urls(listOfPictureUrls, userName)

    create_directory()
    os.chdir("./imagesFromTweets")

    print("downloading!")
    download_images(listOfPictureUrls)

 


