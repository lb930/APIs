# Ozark API

After loading the .tar file into a database, the API can be queried.

### Endpoints

* /episodes: returns a list of all episodes<br>
* /episodes&episode_id=2_1: returns information on the first episode in season 2<br>
* /seasons: returns a list of all seasons<br>
* /characters: returns a list of all characters and actors<br>
* /characters&first_name=Martin&last_name=Byrde: return information on a specific character<br>

### Example query

```python
import requests

BASE = 'http://127.0.0.1:5000/'
response = requests.get(BASE + 'characters')
print(response.json())
```



