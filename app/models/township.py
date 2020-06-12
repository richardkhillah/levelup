from .. import db
from sqlalchemy import func

class BaseA(db.Model):
    __abstract__ = True
    name = db.Column(db.String(64))
    required_level = db.Column(db.Integer)
    time_to_make = db.Column(db.String(16))

class BaseB(db.Model):
    __abstract__ = True
    total_quantity = db.Column(db.Integer, default=1)
    # TODO: quantity_built is a property of the town - refactor.
    quantity_built = db.Column(db.Integer, default=0)
    required_population = db.Column(db.Integer)
    # purchase_cost = db.Column(db.Integer)

class Source(BaseA, BaseB):
    __tablename__ = 'source'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    items = db.relationship('Item', back_populates='source')
    # source_stat
    __mapper_args__ = {
        'polymorphic_identity': 'source',
        'polymorphic_on': type}

class Farming(Source):
    __tablename__ = 'farming'
    id = db.Column(db.Integer, db.ForeignKey('source.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'farming'}

class Factory(Source):
    __tablename__ = 'factory'
    id = db.Column(db.Integer, db.ForeignKey('source.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'factory'}

class Island(Source):
    __tablename__ = 'island'
    id = db.Column(db.Integer, db.ForeignKey('source.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'island'}

class Locomotive(Source):
    __tablename__ = 'locomotive'
    id = db.Column(db.Integer, db.ForeignKey('source.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'locomotive'}

class House(Source):
    __tablename__ = 'house'
    id = db.Column(db.Integer, db.ForeignKey('source.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'house'}

class CommunityBuilding(Source):
    __tablename__ = 'community_building'
    id = db.Column(db.Integer, db.ForeignKey('source.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'community_building'}

class Special(Source):
    __tablename__ = 'special'
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
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(32))
    source_id = db.Column(db.ForeignKey('source.id'))
    source = db.relationship('Source', back_populates='items')
    __mapper_args__ = {
        'polymorphic_identity': 'item',
        'polymorphic_on': type}

class Plant(Item):
    __tablename__ = 'plant'
    id = db.Column(db.Integer, db.ForeignKey(Item.id), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'plant'}

class Manufactured(Item):
    __tablename__ = 'manufactured'
    id = db.Column(db.Integer, db.ForeignKey(Item.id), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'manufactured'}

class Imported(Item):
    __tablename__ = 'imported'
    id = db.Column(db.Integer, db.ForeignKey(Item.id), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'imported'}

class Material(Item):
    __tablename__ = 'material'
    id = db.Column(db.Integer, db.ForeignKey(Item.id), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'material'}

class Foundry(Item):
    __tablename__ = 'foundry'
    id = db.Column(db.Integer, db.ForeignKey(Item.id), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'foundry'}

# class Ore(Item):
#     __tablename__ = 'ore'
#     id = db.Column(db.Integer, db.ForeignKey(Item.id), primary_key=True)
#     __mapper_args__ = {
#         'polymorphic_identity': 'ore'
#     }

# class Gem(Item):
#     __tablename__ = 'gem'
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


class Town(db.Model):
    __tablename__ = 'town'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    level = db.Column(db.Integer, default=1)
    population = db.Column(db.Integer)
    population_cap = db.Column(db.Integer)
    coins = db.Column(db.Integer)
    township_cash = db.Column(db.Integer)

    # sources = db.relationship('Source', backref='town')
    source_stats = db.relationship('SourceStat', backref='town')

    def available_sources(self):
        return Source.query.filter(self.level >= Source.required_level)

    def purchase_source(self, source):
        pass

class SourceStat(db.Model):
    __tablename__ = 'source_stats'
    id = db.Column(db.Integer, primary_key=True)

    source_id = db.Column(db.Integer, db.ForeignKey('source.id'))
    source = db.relationship('Source', backref='source_stat', uselist=False)

    quantity = db.Column(db.Integer, nullable=False, default=1)

    town_id = db.Column(db.Integer, db.ForeignKey('town.id'))
    level = db.Column(db.Integer, default=1)

    @property
    def source_name(self):
        return self.source.name

    def upgrade_requirements():
        pass

    def upgrade():
        pass

    def _downgrade():
        pass

class FactoryStats(SourceStat):
    shelf_count = db.Column(db.Integer, default=6)
    crate_count = db.Column(db.Integer, default=2)
    production_time_reduction_fraction = db.Column(db.Float, default=0.0)
    exp_point_increase_fraction = db.Column(db.Float, default=0.0)

    def upgrade():
        pass

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
    Island=Island,
    Material=Material,
    Foundry=Foundry,

    Town=Town,
    SourceStat=SourceStat,
    FactoryStats=FactoryStats,

    # add_dummies=add_dummies,
    # add_towns=add_towns,
    # remove_towns=remove_towns,
    # remove_dummies=remove_dummies
)
