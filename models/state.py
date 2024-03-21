#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
import models
from models.city import City
import shlex


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'

    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade='all, delete, delete-orphan',
                          backref="state")

    def __repr__(self):
        return f"<State(id='{self.id}', name='{self.name}')>"

    def __str__(self):
        return f"[State]({self.id}) {{'id': '{self.id}', " \
                f"'created_at': {self.created_at}, 'updated_at': " \
                f"{self.updated_at}, 'name': '{self.name}'}}"

    @property
    def cities(self):
        """attribute cities that returns the list
        of City instances with state_id equals to the current State.id
        """
        all_objects = models.storage.all()
        city_objects = []
        filtered_cities = []

        for key, obj in all_objects.items():
            if isinstance(obj, City):
                city_objects.append(obj)

        for city in city_objects:
            if city.state_id == self.id:
                filtered_cities.append(city)

        return filtered_cities
