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

    key = 'your_API_key'
    directory = 'directory to store json files'

    # Channels you would like to track
    channel_ids = ['UC4JX40jDee_tINbkjycV4Sg']

    for id in channel_ids:
        yt = YTstats(key, id, directory)
        yt.get_channel_title()
        yt.get_channel_statistics()
        yt.dump()    
```
        
This will create output a json file with the channel name and today's date as file name.
