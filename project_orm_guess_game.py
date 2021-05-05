# -*- coding: utf-8 -*-
"""
Created on Tue May  4 16:38:51 2021

@author: QTVo
"""

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

#main code

class UserInput(Base):
    __tablename__ = "userinputs"
    
    id = Column(Integer, primary_key = True)
    firstname = Column(String)
    lastname = Column(String)
    no_of_guess = Column(Integer)
    date_win = Column(String)
    feedback = Column(String)
    rating= Column(Integer)
    
if __name__ == "__main__":
    engine = create_engine('sqlite:///guessnumber_game_db.sqlite')
    Base.metadata.create_all(engine)