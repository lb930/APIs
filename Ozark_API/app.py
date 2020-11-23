from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, marshal_with, fields, abort

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:<pw>@localhost/<db>'
db = SQLAlchemy(app)

# Define the tables in the database
class Season(db.Model):
    season_id = db.Column(db.VARCHAR, primary_key=True)
    season = db.Column(db.Integer, unique=True, nullable=False)
    # one-to-many relationship to Episode class
    episodes = db.relationship('Episode', backref='season', lazy=True)


# intermediary
actor_episode = db.Table('actor_episode',
                         db.Column('actor_id', db.String, db.ForeignKey('actor.actor_id'), primary_key=True),
                         db.Column('episode_id', db.String, db.ForeignKey('episode.episode_id'), primary_key=True))


class Actor(db.Model):
    actor_id = db.Column(db.String(3), primary_key=True)
    first_name = db.Column(db.VARCHAR)
    last_name = db.Column(db.VARCHAR)
    middle_name = db.Column(db.VARCHAR)
    characters = db.relationship('Character', backref='actor', lazy=True)
    actor_episode_rel = db.relationship('Episode', secondary=actor_episode, backref =db.backref('actors', lazy = 'dynamic'))

class Episode(db.Model):
    episode_id = db.Column(db.VARCHAR, primary_key=True)
    episode_num = db.Column(db.Integer)
    title = db.Column(db.VARCHAR)
    release_date = db.Column(db.DateTime)
    imdb_rating = db.Column(db.Float)
    director = db.Column(db.VARCHAR)
    synopsis = db.Column(db.VARCHAR)
    # foreign key
    season_id = db.Column(db.String(2), db.ForeignKey('season.season_id'), nullable=False)

class Character(db.Model):
    char_id = db.Column(db.String(3), primary_key=True)
    first_name = db.Column(db.VARCHAR)
    last_name = db.Column(db.VARCHAR)
    actor_id = db.Column(db.String(3), db.ForeignKey(
        'actor.actor_id'), nullable=False)

# API output format
episode_fields = {'episode_id': fields.String,
                  'episode_num': fields.Integer,
                  'title': fields.String,
                  'release_date': fields.DateTime,
                  'imdb_rating': fields.Float,
                  'director': fields.String,
                  'synopsis': fields.String,
                  'season_id': fields.String
                  }

# Seasons
season_fields = {'season_id': fields.String, 'season': fields.Integer}

# Characters
character_fields = {}
character_fields['character'] = {}
character_fields['character']['char_id'] = fields.String(attribute='char_id')
character_fields['character']['first_name'] = fields.String(attribute='first_name')
character_fields['character']['last_name'] = fields.String(attribute='last_name')
character_fields['character']['actor_first_name'] = fields.String(attribute='actor.first_name')
character_fields['character']['actor_middle_name'] = fields.String(attribute='actor.middle_name')
character_fields['character']['actor_last_name'] = fields.String(attribute='actor.last_name')

# Actors and episodes
actor_episode_fields = {'episode_id': fields.String, 'actor_id': fields.String}

# Define get methods
class Ozark(Resource):

    @marshal_with(episode_fields)
    def get(self):
        """Fetches all episodes"""
        episodes = Episode.query.all()
        return episodes


class OzarkEpisode(Resource):
    @marshal_with(episode_fields)
    def get(self, ep_id):
        """Fetches a specific episode"""
        episodes = Episode.query.filter_by(episode_id=ep_id).first()
        if not episodes:
            abort(404, message='Could not find episode with that id')
        return episodes


class OzarkSeasons(Resource):
    @marshal_with(season_fields)
    def get(self):
        """Fetches all seasons"""
        seasons = Season.query.all()
        return seasons


class OzarkCharacters(Resource):
    @marshal_with(character_fields)
    def get(self):
        chars = Character.query.all()
        return chars


class OzarkFirstLast(Resource):
    @marshal_with(character_fields)
    def get(self, fn, ln):
        """Fetches a specific character"""
        characters = Character.query.filter_by(
            first_name=fn).filter_by(last_name=ln).first()
        if not characters:
            abort(404, message='Could not find character')
        return characters


class OzarkFirst(Resource):
    @marshal_with(character_fields)
    def get(self, fn):
        """Fetches a specific character"""
        characters = Character.query.filter_by(first_name=fn).first()
        if not characters:
            abort(404, message='Could not find character')
        return characters


api.add_resource(Ozark, '/episodes')
api.add_resource(OzarkEpisode, '/episodes&episode_id=<string:ep_id>')
api.add_resource(OzarkSeasons, '/seasons')
api.add_resource(OzarkCharacters, '/characters')
api.add_resource(OzarkFirstLast, '/characters&first_name=<string:fn>&last_name=<string:ln>')
api.add_resource(OzarkFirst, '/characters&first_name=<string:fn>')

if __name__ == "__main__":
    app.run(debug=True)
