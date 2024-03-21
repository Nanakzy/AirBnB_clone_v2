#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table
from sqlalchemy.orm import relationship
import models
import shlex
from os import getenv
from sqlalchemy.ext.declarative import declarative_base

place_amenity = Table("place_amenity", Base.metadata,
                      Column("place_id", String(60),
                             ForeignKey("places.id"),
                             primary_key=True,
                             nullable=False),
                      Column("amenity_id", String(60),
                             ForeignKey("amenities.id"),
                             primary_key=True,
                             nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    name = Column(String(128), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    def __repr__(self):
        return f"<Place(id='{self.id}', name='{self.name}')>"

    def __str__(self):
        return (f"(hbnb) [[Place] ({self.id}) "
                f"{{'number_bathrooms': {self.number_bathrooms}, "
                f"'longitude': {self.longitude}, "
                f"'city_id': '{self.city_id}', "
                f"'user_id': '{self.user_id}', "
                f"'latitude': {self.latitude}, "
                f"'price_by_night': {self.price_by_night}, "
                f"'name': '{self.name}', "
                f"'id': '{self.id}', "
                f"'max_guest': {self.max_guest}, "
                f"'number_rooms': {self.number_rooms}, "
                f"'updated_at': {self.updated_at}, "
                f"'created_at': {self.created_at}}}]")

    if getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship("Review", cascade="all, delete,delete-orphan",
                               backref="place")
        amenities = relationship("Amenity", secondary=place_amenity,
                                 viewonly=False,
                                 back_populates="place_amenities")
    else:
        @property
        def reviews(self):
            """getter attribute reviews that returns the list of
            Review instances
            with place_id equals to the current Place.id
            """
            all_objects = models.storage.all()
            review_list = []
            result = []
            for key in all_objects:
                review = key.replace('.', ' ')
                review = shlex.split(review)
                if review[0] == 'Review':
                    review_list.append(all_objects[key])
            for elem in review_list:
                if elem.place_id == self.id:
                    result.append(elem)
            return result

        @property
        def amenities(self):
            """ Returns list of amenity ids """
            return self.amenity_ids

        @amenities.setter
        def amenities(self, obj=None):
            """ Appends amenity ids to the attribute """
            if isinstance(obj, Amenity) and obj.id not in self.amenity_ids:
                self.amenity_ids.append(obj.id)
