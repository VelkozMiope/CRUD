class Book:
    def __init__(self, id, avaliable, title, timestamp):
        self.id = id
        self.title = title
        self.avaliable = avaliable
        self.timestamp = timestamp

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'avaliable': self.avaliable,
            'timestamp': self.timestamp
        }