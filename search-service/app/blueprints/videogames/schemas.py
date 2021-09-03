from marshmallow import Schema, fields


class VideoGameSchema(Schema):
    aliases = fields.List(fields.String())
    name = fields.List(fields.String())
    number_of_platforms = fields.Integer()


videogame_schema = VideoGameSchema()
videogames_schema = VideoGameSchema(many=True)
