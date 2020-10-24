# Youtube API

A script for downloading information on Youtube channels and storing the results in a json file.

The script is intended to run every day and track the number of subscribers, views and videos for any given Youtube channel. The result can then be analysed.

## Prerequisites

* API key from https://console.developers.google.com/apis/

## Example

Download and save Youtube_class.py. Create a script similar to main.py and store your API key and directory where you would like to save the JSON files in the respective variables.
Channel IDs can be found in the Youtube channel URL, eg https://www.youtube.com/channel/UC4JX40jDee_tINbkjycV4Sg.

```python
from Youtube_class import YTstats

key = 'you_API_key'

# Channel IDs can be found in the URL of each Youtube channel
channel_ids = ['some_channel', 'another_channel']

for id in channel_ids:
    yt = YTstats(key, id)
    yt.get_channel_title()
    yt.get_channel_statistics()
    yt.dump('Filepath for jsons')
    yt.to_csv('File path for csv file')   
```
        
This will create output a json file with the channel name and today's date as file name as well as a CSV file:

| date | channel_id | channel | views | subscribers | videos |
| --- | --- | --- | --- | --- | --- |
