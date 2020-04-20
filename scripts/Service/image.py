import requests
import shutil
import os
import datetime
import PIL
import imagehash
from os import listdir
from os.path import isfile, join

class Image():

    IMGFOLDER = '/home/dzanardo/github/apartamento/images/'
    FILES = ''
    __IMAGES = {}

    def __init__(self):
        self.FILES = [f for f in listdir(self.IMGFOLDER) if isfile(join(self.IMGFOLDER, f))]
        self.__load_images()

    def __load_images(self):
        for file in self.FILES:
            self.__IMAGES[str(file.split('_')[1:2][0])] = str(file)
        
    def download(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        url = url.replace('{action}', 'crop').replace('{width}', '360').replace('{height}', '240')
        file_name = url.split('/')[-1]

        if file_name in self.__IMAGES:
            return str(self.__IMAGES[file_name])
            
        r = requests.get(url, stream=True, headers=headers)

        img_name = datetime.datetime.today().strftime('%Y%m%d') + '_' + file_name
        if r.status_code == 200:
            print('Downloading images')
            with open(self.IMGFOLDER + img_name, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
                return img_name

    def get_images_hash(self):
        print('Loading Images hash')
        files = [f for f in listdir(self.IMGFOLDER) if isfile(join(self.IMGFOLDER, f))]
        images = {'key': 'value'}
        for file in files:
            file_name = self.IMGFOLDER + str(file)
            try:
                img = PIL.Image.open(file_name)
            except OSError as ex:
                print('Cannot load ' + file_name, ex)
            img_hash = imagehash.average_hash(img)
            images[str(file)] = img_hash

        print('Images loaded %s from %s' % (len(files), len(images)))
        
        return images
