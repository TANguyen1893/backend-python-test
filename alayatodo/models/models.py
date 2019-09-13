from alayatodo import database
from passlib.hash import bcrypt


class Users(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(255), nullable=False)
    password = database.Column(database.String(255), nullable=False)

    def does_password_match(self, password):
        return bcrypt.verify(password, self.password)

    def serialize(self):
        return dict(id=self.id, username=self.username, password=self.password)


class Todos(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    user_id = database.Column(
        database.Integer,
        database.ForeignKey('users.id'),
        nullable=False)
    description = database.Column(database.String(255))
    # Can use Boolean type here but insertion would need to convert Integer to
    # SQL Boolean
    complete = database.Column(database.Integer, default=False)

    def serialize(self):
        return dict(id=self.id, user_id=self.user_id,
                    description=self.description, complete=self.complete)
