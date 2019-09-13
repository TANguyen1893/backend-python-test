from alayatodo import database

class Users(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(255), nullable=False)
    password = database.Column(database.String(255), nullable=False)

    def serialize(self):
        return dict(id=self.id, username=self.username, password=self.password)

class Todos(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    user_id = database.Column(database.Integer, database.ForeignKey('users.id'), nullable=False)
    description = database.Column(database.String(255))
    complete = database.Column(database.Integer, default=False) # Can use Boolean type here but insertion would need to convert Integer to SQL Boolean

    def serialize(self):
        return dict(id=self.id, user_id=self.user_id, description=self.description, complete=self.complete)