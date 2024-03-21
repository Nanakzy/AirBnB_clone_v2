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
        created_at_repr = f"datetime.datetime({self.created_at.year}, {self.created_at.month}, {self.created_at.day}, {self.created_at.hour}, {self.created_at.minute}, {self.created_at.second}, {self.created_at.microsecond})"
        updated_at_repr = f"datetime.datetime({self.updated_at.year}, {self.updated_at.month}, {self.updated_at.day}, {self.updated_at.hour}, {self.updated_at.minute}, {self.updated_at.second}, {self.updated_at.microsecond})"

        return (f"[State]({self.id}) "
                f"{{'id': '{self.id}', "
                f"'created_at': {created_at_repr}, 'updated_at': "
                f"{updated_at_repr}, 'name': '{self.name}'}}")

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
