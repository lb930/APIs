from Youtube_class import YTstats

key = 'your_API_key'
directory = 'directory to store json files'

# Channels you would like to track
channel_ids = ['list of channel ids']

for id in channel_ids:
    yt = YTstats(key, id, directory)
    yt.get_channel_title()
    yt.get_channel_statistics()
    yt.dump()
    