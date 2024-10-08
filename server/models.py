from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates

from config import db, bcrypt

class Region(db.Model, SerializerMixin):
    __tablename__ = 'regions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    habitats = db.relationship('Habitat', back_populates='region')

    serialize_rules = ('-habitats.region',)

    @validates('name')
    def validate_name(self, key, name):
        regions = ["Kanto", "Johto", "Hoenn", "Sinnoh", "Unova", "Kalos", "Alola", "Galar", "Paldea", "Orre", "Ultra Space", "Kitakami", "Almia", "Oblivia", "Lental", "Uncharted"]
        if name not in regions:
            raise ValueError('Region not recognized. Please select from available options or confirm uncharted territory.')
        return name
    
class Biome(db.Model, SerializerMixin):
    __tablename__ = 'biomes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    trainers = db.relationship('Trainer', back_populates='biome')

    serialize_rules = ('-trainers.biome',)

    @validates('name')
    def validate_name(self, key, name):
        biomes = ['Coastal', 'Polar', 'Taiga', 'Mires', 'Forest (conif.)', 'Forest (decid.)', 'Forest (tropical rain)', 'Forest (temperate rain)', 'Grasslands', 'Shrublands', 'Desert', 'Savanna', 'Wetland', 'River and Stream', 'Lake', 'Intertidal', 'Reef', 'Sea', 'Ocean', 'Deep Ocean', 'Cavern', 'Mountain', 'Ruins', 'City', 'No Preference']
        if name not in biomes:
            raise ValueError('Biome not recognized. Please select from available options. If no preference, select "No Preference"')
        return name
    
class Habitat(db.Model, SerializerMixin):
    __tablename__ = 'habitats'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    image = db.Column(db.String, nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('regions.id'))

    reviews = db.relationship('Review', back_populates='habitat', cascade='all, delete-orphan')

    sightings = db.relationship('Sighting', back_populates='habitat', cascade='all, delete-orphan')

    region = db.relationship('Region', back_populates='habitats')

    serialize_rules = ('-reviews.habitat', '-region.habitats', '-sightings.habitat', )

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError('Habitat must be named.')
        elif 25 < len(name) < 2:
            raise ValueError('Habitat names must be between 2-25 characters long')
        return name

    def __repr__(self):
        return f'<Habitat {self.id}: {self.name}>'
    
class Trainer(db.Model, SerializerMixin):
    __tablename__ = 'trainers'

    serialize_rules = ('-reviews.trainer', '-sightings.trainer', '-biome.trainers', '-_password_hash', '-reviews.habitat', '-sightings.habitat')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    age = db.Column(db.Integer)
    image = db.Column(db.String)
    _password_hash = db.Column(db.String, nullable=False)
    biome_id = db.Column(db.Integer, db.ForeignKey('biomes.id'))

    reviews = db.relationship('Review', back_populates='trainer', cascade='all, delete-orphan')

    sightings = db.relationship('Sighting', back_populates='trainer', cascade='all, delete-orphan')

    biome = db.relationship('Biome', back_populates='trainers')

    @hybrid_property
    def password_hash(self):
        raise AttributeError('Password hashes may not be viewed.')
    
    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError('Please enter a name.')
        return name
    
    @validates('age')
    def validate_age(self, key, age):
        if age < 10:
            raise ValueError('Trainers must be at least 10 years old.')
        return age

    def __repr__(self):
        return f'<Trainer {self.id}: {self.name}, age: {self.age}>'
    
class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'
    __table_args__ = (db.CheckConstraint('length(content) >= 50'),)

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    danger = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    habitat_id = db.Column(db.Integer, db.ForeignKey('habitats.id'))
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainers.id'))

    habitat = db.relationship('Habitat', back_populates='reviews')
    trainer = db.relationship('Trainer', back_populates='reviews')

    serialize_rules = ('-habitat.reviews', '-trainer.reviews',)

    @validates('danger')
    def validate_danger(self, key, danger):
        if not danger:
            raise ValueError('Please enter the observed danger levels of this habitat.')
        return danger

    def __repr__(self):
        return f'<Review {self.id}>'
    
class Sighting(db.Model, SerializerMixin):
    __tablename__ = 'sightings'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    blurb = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    habitat_id = db.Column(db.Integer, db.ForeignKey('habitats.id'))
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainers.id'))

    habitat = db.relationship('Habitat', back_populates='sightings')
    trainer = db.relationship('Trainer', back_populates='sightings')

    serialize_rules = ('-habitat.sightings', '-trainer.sightings',)

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError('Please enter the name of the sighting. If not known, please enter "Pokémon Unknown" instead.')
        return name
    
    @validates('blurb')
    def validate_blurb(self, key, blurb):
        if len(blurb) > 200:
            raise ValueError('Please keep blurbs on rare sightings to 200 characters or less. You are free to go into much greater depths on an encounter in your review of the habitat!')
        return blurb

    def __repr__(self):
        return f'<Rare sighting {self.id}: {self.name} at habitat #{self.habitat_id}>'
