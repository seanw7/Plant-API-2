# copied from item.py
from db import db


class PlantModel(db.Model):
    __tablename__ = "plants"

    __table_args__ = (db.ForeignKeyConstraint(['genus_name'],['genus.name']),)# {ondelete:cascade},)#,{'mysql_engine':'InnoDB'})

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    quantity = db.Column(db.Float(precision=2))
    price = db.Column(db.Float(precision=2))

    genus_name = db.Column(db.String(80))#, db.ForeignKey('genus.name'), nullable=False)
    genera = db.relationship('GenusModel', backref='PlantModel')#, lazy=True)#, cascade="delete-orphan")#backref=db.backref('plants', lazy=True))

    def __repr__(self):
        return '<PlantModel %r>' % self.name

    def __init__(self, name, quantity, price, genus_name):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.genus_name = genus_name
        #url = "http://www.palmpedia.net/wiki/{}_{}".format(genus_name, name)

    def json(self):
        return {"name": self.name, "price": self.price, "quantity": self.quantity, "value": self.quantity * self.price, \
        "url": self.make_url()}

    def make_url(self):
        return "https://www.google.com/webhp#q={}+{}".format(self.genus_name, self.name)

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
