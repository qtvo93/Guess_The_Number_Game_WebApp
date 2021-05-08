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
    
    id = Column(Integer)
    username = Column(String, primary_key = True)
    passcode = Column(String)   
    rewards = Column(Integer)
    playing_time = Column(Integer)


class UserHistory(Base):
    __tablename__ = "userhistory"
    
    id = Column(Integer, primary_key = True)
    username = Column(String)
    passcode = Column(String) 
    guess_numbers = Column(Integer)
    this_rewards = Column(Integer)
    date_win = Column(String)
    
    
if __name__ == "__main__":
    engine = create_engine('sqlite:///web_game4_db.sqlite')
    Base.metadata.create_all(engine)