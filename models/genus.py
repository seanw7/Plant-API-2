# copied from store.py
from db import db

class GenusModel(db.Model):
    __tablename__ = "genus_model"

    #__table_args__ = (db.ForeignKeyConstraint(['name'],['plants.genus_name']),)

    id = db.Column(db.Integer)#, primary_key=True)
    name = db.Column(db.String(80), primary_key=True)

    #db.Index('ix_genus_name', db.func.lower(db.metadata.tables['genus_model.name']))
    plants = db.relationship('PlantModel', lazy='dynamic')#, backref='GenusModel')

    def __repr__(self):
        return '<GenusModel %r>' % self.name

    def __init__(self, name):#, plants):
        self.name = name
        #self.plants


    def json(self):
        return {"genus": self.name, "species": [plant.json() for plant in self.plants.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
