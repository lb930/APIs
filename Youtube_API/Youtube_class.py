import json
import requests
from datetime import date
from datetime import datetime
import csv
import os

class YTstats:

    def __init__(self, api_key, channel_id):
        self.api_key = api_key
        self.channel_id = channel_id
        self.channel_name = None
        self.channel_statistics = None

    def get_channel_title(self):
        """Get the channel name."""

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

    def to_csv(self, csv_directory):
        """Saves the channel statistics to a csv file.

        Args:
            csv_directory: file path and  file name
        """

        date_col = datetime.now()
        date_col = datetime.strftime(date_col, '%Y-%m-%d %H:%M:%S')
        channel = self.channel_name
        channel_id = self.channel_statistics['id']
        views = self.channel_statistics['statistics']['viewCount']
        subscribers = self.channel_statistics['statistics']['subscriberCount']
        videos = self.channel_statistics['statistics']['videoCount']

        file_exists = os.path.isfile(csv_directory)

        with open(csv_directory, 'a', newline='') as csvfile:
            fieldnames = ['date', 'channel_id', 'channel',
                          'views', 'subscribers', 'videos']
            writer = csv.DictWriter(csvfile, fieldnames = fieldnames)

            # Check if file exists and if not, create file with headers only
            if not file_exists:
                writer.writeheader()

            # Append data to existing csv file
            writer.writerow({'date': date_col, 'channel_id': channel_id, 'channel': channel,
                             'views': views, 'subscribers': subscribers, 'videos': videos})

    def dump(self, json_directory):
        """Save channel statistics in a json file. The file name is composed of today's date and the channel name.

        Args:
            json_directory: file path, requires \\ at the end on Windows
        """

        today_date = str(date.today())
        channel = self.channel_name.replace(' ', '')
        filename = channel + '_' + today_date + '.json'
        with open(json_directory + filename, 'w') as f:
            f.write(str(self.channel_statistics))