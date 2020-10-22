import json
import requests
from datetime import date

class YTstats:

    def __init__(self, api_key, channel_id, directory):
        self.api_key = api_key
        self.channel_id = channel_id
        self.directory = directory
        self.channel_name = None
        self.channel_statistics = None

    def get_channel_title(self):

        """Get the channel name"""

        url_title = f'https://www.googleapis.com/youtube/v3/channels?part=snippet&id={self.channel_id}&key={self.api_key}'

        json_url_title = requests.get(url_title)
        channel_name_json = json.loads(json_url_title.text)
        channel_name_json = channel_name_json['items'][0]['snippet']['title']
        
        self.channel_name = channel_name_json
        return channel_name_json

    def get_channel_statistics(self):

        """Extract the channel statistics"""

        url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={self.channel_id}&key={self.api_key}'

        json_url = requests.get(url)
        statistics = json.loads(json_url.text)
        statistics = statistics['items'][0]
        
        self.channel_statistics = statistics
        return statistics

    def dump(self):

        """Save channel statistics in a json file"""

        today_date = str(date.today())
        channel = self.channel_name.replace(' ', '')
        filename = channel + '_' + today_date + '.json'
        with open(self.directory + filename, 'w') as f:
            f.write(str(self.channel_statistics))