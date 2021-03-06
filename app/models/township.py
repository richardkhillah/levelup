from .. import db
from sqlalchemy import func

class BaseA(db.Model):
    __abstract__ = True
    __bind_key__ = 'township_data'
    name = db.Column(db.String(64))
    required_level = db.Column(db.Integer)
    time_to_make = db.Column(db.String(16))

class BaseB(db.Model):
    __abstract__ = True
    __bind_key__ = 'township_data'
    total_quantity = db.Column(db.Integer, default=1)
    # TODO: quantity_built is a property of the town - refactor.
    quantity_built = db.Column(db.Integer, default=0)
    required_population = db.Column(db.Integer)
    purchase_cost = db.Column(db.Integer)

class Source(BaseA, BaseB):
    __tablename__ = 'source'
    __bind_key__ = 'township_data'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    items = db.relationship('Item', back_populates='source')
    # source_stat
    __mapper_args__ = {
        'polymorphic_identity': 'source',
        'polymorphic_on': type}

class Farming(Source):
    __tablename__ = 'farming'
    __bind_key__ = 'township_data'
    id = db.Column(db.Integer, db.ForeignKey('source.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'farming'}

class Factory(Source):
    __tablename__ = 'factory'
    __bind_key__ = 'township_data'
    id = db.Column(db.Integer, db.ForeignKey('source.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'factory'}

class Island(Source):
    __tablename__ = 'island'
    __bind_key__ = 'township_data'
    id = db.Column(db.Integer, db.ForeignKey('source.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'island'}

class Locomotive(Source):
    __tablename__ = 'locomotive'
    __bind_key__ = 'township_data'
    id = db.Column(db.Integer, db.ForeignKey('source.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'locomotive'}

class House(Source):
    __tablename__ = 'house'
    __bind_key__ = 'township_data'
    id = db.Column(db.Integer, db.ForeignKey('source.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'house'}

class CommunityBuilding(Source):
    __tablename__ = 'community_building'
    __bind_key__ = 'township_data'
    id = db.Column(db.Integer, db.ForeignKey('source.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'community_building'}

class Special(Source):
    __tablename__ = 'special'
    __bind_key__ = 'township_data'
    id = db.Column(db.Integer, db.ForeignKey('source.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'special'}

source = {
    'source': Source,
    'farming': Farming,
    'factory': Factory,
    'island': Special,
    'locomotive': Locomotive,
    'house': House,
    'community_building': CommunityBuilding,
    'special': Special
}


class Item(BaseA):
    __tablename__ = 'item'
    __bind_key__ = 'township_data'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(32))
    source_id = db.Column(db.ForeignKey('source.id'))
    source = db.relationship('Source', back_populates='items')
    __mapper_args__ = {
        'polymorphic_identity': 'item',
        'polymorphic_on': type}

class Plant(Item):
    __tablename__ = 'plant'
    __bind_key__ = 'township_data'
    id = db.Column(db.Integer, db.ForeignKey(Item.id), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'plant'}

class Manufactured(Item):
    __tablename__ = 'manufactured'
    __bind_key__ = 'township_data'
    id = db.Column(db.Integer, db.ForeignKey(Item.id), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'manufactured'}

class Imported(Item):
    __tablename__ = 'imported'
    __bind_key__ = 'township_data'
    id = db.Column(db.Integer, db.ForeignKey(Item.id), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'imported'}

class Material(Item):
    __tablename__ = 'material'
    __bind_key__ = 'township_data'
    id = db.Column(db.Integer, db.ForeignKey(Item.id), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'material'}

class Foundry(Item):
    __tablename__ = 'foundry'
    __bind_key__ = 'township_data'
    id = db.Column(db.Integer, db.ForeignKey(Item.id), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'foundry'}

# class Ore(Item):
#     __tablename__ = 'ore'
# __bind_key__ = 'township_data'
#     id = db.Column(db.Integer, db.ForeignKey(Item.id), primary_key=True)
#     __mapper_args__ = {
#         'polymorphic_identity': 'ore'
#     }

# class Gem(Item):
#     __tablename__ = 'gem'
# __bind_key__ = 'township_data'
#     id = db.Column(db.Integer, db.ForeignKey(Item.id), primary_key=True)
#     __mapper_args__ = {
#         'polymorphic_identity': 'gem'
#     }

item = {
    'item': Item,
    'plant': Plant,
    'manufactured': Manufactured,
    'imported': Imported,
    'material': Material,
    'foundry': Foundry,
    # 'ore': Ore,
    # 'gem': Gem
}

class Unlock:
    def __init__(self, level=None, sources=None, items=None):
        self.level = level
        self.sources = sources
        self.items = items

    @property
    def construction_cost(self):
        cost = 0
        for source in self.sources:
            if source.purchase_cost:
                cost += source.purchase_cost
        return cost

    @construction_cost.setter
    def construction_cost(self):
        raise AttributeError("construction_cost is a computed value")


tm_dict = dict(
    db=db,
    Source=Source,
    Farming=Farming,
    Factory=Factory,
    Special=Special,
    House=House,
    CommunityBuilding=CommunityBuilding,

    Item=Item,
    Plant=Plant,
    Manufactured=Manufactured,
    Imported=Imported,
    Island=Island,
    Material=Material,
    Foundry=Foundry,
)
