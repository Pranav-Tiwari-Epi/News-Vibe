from marshmallow import Schema, fields 


class NewsRequestSchema(Schema):
    start_date=fields.Date(required=True)
    end_date=fields.Date(required=True)
    type=fields.Str()
    topic=fields.Str(required=True)
    
class NewsResponseSchema(Schema):
    index=fields.Int()
    source=fields.Str()
    author=fields.Str()
    url=fields.URL()
    time=fields.Time()
    date=fields.Date()
    title=fields.Str()
    # analysisContent=fields.Str()
    sentimentAnalysis=fields.Str()
    