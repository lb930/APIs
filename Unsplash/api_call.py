import requests
import json
import os
from logger import logger

class UnsplashAPI:

    def prep(self):
        
        with open('config.json') as json_conf: 
            CONF = json.load(json_conf)
        self.log = logger()
        self.image_folder = CONF['image_location']
        self.access_key = os.environ['unsplash_access_key']

        return self.log, self.image_folder, self.access_key

    def get_images(self, orientation: str, *topics: list):

        try:
            t = ','.join(*topics)
            response = requests.get('https://api.unsplash.com/photos/random?client_id=' + self.access_key + '&orientation=' + orientation + '&topic=' + t)
            self.log.info(f'API status: {response}')
            # Only needed to investigate json structure
            # investigate = json.dumps(response.json(), sort_keys=True, indent=4)
            # print(investigate)
            self.data = response.json()
            return self.data
        
        except Exception as err:
            self.log.exception(err)
            self.log.info('\n')
            raise

    def download_image(self):

        try:
            image_url = requests.get(self.data['urls']['small'])
            self.log.info(f'Image URL status: {image_url}')
            
            image = image_url.content
            img_descr = self.data['alt_description']
            img_name = self.data['id']
            img_url = 'https://unsplash.com/photos/' + img_name
            
            with open(self.image_folder + img_name + '.jpg', 'wb') as handler:
                handler.write(image)
            print(img_descr)
            print(f'{img_name} downloaded: {img_url}')

            self.log.info(f'Image ID: {img_name}')
            self.log.info(f'Image URL: {img_url}')
            self.log.info(f'Image descr: {img_descr}')
            self.log.info('\n')
        
        except Exception as err:
            self.log.exception(err)
            self.log.info('\n')
            raise

if __name__ == '__main__':
    u = UnsplashAPI()
    u.prep()
    u.get_images('landscape', ['nature', 'ocean'])
    u.download_image()