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
    