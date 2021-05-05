# -*- coding: utf-8 -*-
"""
Created on Sun May  2 14:59:05 2021

@author: QTVo
"""

#%% Libraries

import streamlit as st
import random
import functools
import time
#import pandas as pd
#import SessionState
#from streamlit import caching
#from streamlit.script_runner import StopException, RerunException
from sqlalchemy.orm import sessionmaker
from project_orm_guess_game import UserInput  
from sqlalchemy import create_engine

#%% session state :
    
from session_state import get_state
class MyState:
    a: int
    b: int
    def __init__(self, a: int, b: int):
        self.a = a
        self.b = b


def setup(a: int, b: int) -> MyState:
    return MyState(a,b)




#%%
st.title('Guess the Number Game')

#---------------------------------#
# About
expander_bar = st.beta_expander("About the App",expanded=True)

expander_bar.markdown("""
* **Guess the Number Game** is a simple Web-App to demonstrate Python, SQL and Data Science streamlit framework
* **Python libraries:**  streamlit, numpy, functools, random, matplotlib, sqlalchemy
* **Version 2.0:** App written by [Quoc Thinh Vo](https://quoctvo.com). 
    Please open the Navigation bar and choose Version Update for more information                                                                                                                                        

    
""" )

#---------------------------------#
#### prevent cahce refreshing from button click
def cache_on_button_press(label, **cache_kwargs):
   
    internal_cache_kwargs = dict(cache_kwargs)
    internal_cache_kwargs['allow_output_mutation'] = True
    internal_cache_kwargs['show_spinner'] = False
    
    def function_decorator(func):
        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            @st.cache(**internal_cache_kwargs)
            def get_cache_entry(func, args, kwargs):
                class ButtonCacheEntry:
                    def __init__(self):
                        self.evaluated = False
                        self.return_value = None
                    def evaluate(self):
                        self.evaluated = True
                        self.return_value = func(*args, **kwargs)
                return ButtonCacheEntry()
            cache_entry = get_cache_entry(func, args, kwargs)
            if not cache_entry.evaluated:
                if st.button(label):
                    cache_entry.evaluate()
                else:
                    raise st.stop().StopException
            return cache_entry.return_value
        return wrapped_func
    return function_decorator
#### 

#%% Navigation bar:
    
st.subheader("Navigation")
menu = ["Play Game", "View Data", "Version Update"]
choice = st.selectbox("Menu", menu)   
 	
#%% function declarations

@cache_on_button_press("Guess")
def authenticate(rand,gue):
    return rand==gue  

@cache_on_button_press("Let's play")
def play(min_num,max_num):
    return random.randint(min_num,max_num)
 
#%% Section 1: header and number interval picking
if choice == "Play Game":
    
    st.subheader('Please choose a number range:')
    st.text("  ")
    min_num=st.number_input("Minimum Number (0-10000):",
                       max_value = 10000,
                       min_value= 0,
                       value =500)
    max_num=st.number_input("Maximum Number (0-10000):",
                       max_value = 10000,
                       min_value= 0,
                       value =600)
    if min_num > max_num:
        st.error("Max number cannot be smaller than Min number")
        st.text("Please adjust the interval and try again")
        st.stop().Exception()
    min_num= int(min_num)
    max_num= int(max_num)
    
    #initialize random number, play counter and timer:
    #ss = SessionState.get(x=1)
    state = get_state(setup, a=1, b=1)
    
   # timer = SessionState.get(t=0)
    #current=time.time()
    #start_time = get_state(setup, a= current)
    rand_num = play(min_num,max_num)

    #%% Section 2: Generating random number and guessing
    with st.form(key='guess'):
        st.write("The generated random number is between: ",min_num,"and",max_num)        
        st.subheader('Please enter your guess here:')
        guess= st.text_input("Guessing number:")
       
        #%% Authenticate guess vs random num
          
       # if authenticate(str(rand_num), (guess)):
        submit_button2 = st.form_submit_button(label='Guess')
    if submit_button2:
        if str(rand_num)== (guess):
            if guess == "":
                st.text("Please enter a number before pressing Guess button!")  
            st.write("Random number is: ",rand_num)
            st.success('Congratulations, your guess is right!')
            st.write("You win the game with",state.a, "guessing play(s)")
            state.a = 1
        else: 
            state.a +=1
            state.b += 1
            if guess != "":        
                if(rand_num) < int(guess):
                    st.warning('Random number is smaller than your guess')            
                elif (rand_num) > int(guess):
                    st.error('Random number is greater than your guess')    
            else:
                st.text("Please enter a valid number")
            st.stop().Exception()
    
    
    #%% Footer + Rating the app
           
    with st.form(key ='record_play'):
        #SQL data base generating:
        engine = create_engine('sqlite:///guessnumber_game_db.sqlite')
        Session = sessionmaker(bind=engine)
        sess= Session()
        
        # Form header and form generating:
        st.subheader("Would you like to submit your records?")
        firstname , lastname = st.beta_columns(2)
        with firstname:
            F_name = st.text_input("Firstname")
        with lastname:
            L_name = st.text_input("Lastname")
        
        note, date = st.beta_columns([3,1])
        notefeed = note.text_input("Feedback (Optional)")
        datewin = str(date.date_input("Winning date"))
        rate = int(st.slider("Rate this App:",0,10,6))
        
        submit_button = st.form_submit_button(label='Submit')
    if submit_button:
        try:
            
            entry = UserInput(firstname=F_name,
                              lastname=L_name,
                              no_of_guess=state.b,
                              date_win=datewin,
                              feedback = notefeed,
                              rating = rate)
          #  user_query = sess.query(UserInput).filter_by(firstname=F_name)\
             #   .filter_by(lastname=L_name).filter_by(no_of_guess=ss.x)\
                # .filter_by(date_win=datewin).filter_by(feedback = notefeed)
            add_logic = True
            results = sess.query(UserInput).all()
            for item in results:
                if item.firstname == F_name:
                    if item.lastname == L_name:
                        if item.no_of_guess==state.b:
                            if item.date_win ==datewin:        
                                add_logic=False
                                
            if add_logic == True:
                sess.add(entry)
                sess.commit()
                st.balloons()
                if F_name != "":
                    st.success("Thank you {} for submitting your playing records!".format(F_name))
                else:
                    st.success("Thank you for submitting your playing records!")
            else:
                if F_name == "" and L_name == "":
                    st.error("Please enter your name")   
                else:
                    st.error("Please do not resubmit an existing record")
        except Exception as e:
            st.error(f"Some error occured : {e}")
    
    with st.form('records_form'):
        st.subheader("Please input your first and last name to see your records")
        firstname2 , lastname2 = st.beta_columns(2)
        with firstname2:
            F_name2 = st.text_input("Firstname")
        with lastname2:
            L_name2 = st.text_input("Lastname")
            
        view_data_button = st.form_submit_button(label='Click to view records')
       
    if view_data_button:
        results = sess.query(UserInput).filter_by(firstname=F_name2)\
            .filter_by(lastname=L_name2)
        
        for item in results:   
            st.header("Player information:")
            firstname3 , lastname3 = st.beta_columns([1,9])
            firstname3.subheader(item.firstname)
            lastname3.subheader(item.lastname)

            st.write("Winner with",item.no_of_guess ,"guess(es)")
            st.write("On Date:",item.date_win)
            
            
#%% choice == View data
import matplotlib.pyplot as plt

if choice == "View Data":
    engine = create_engine('sqlite:///guessnumber_game_db.sqlite')
    Session = sessionmaker(bind=engine)
    sess= Session()
    
    st.text(" ")
    st.subheader("Guess the Number Game Statistics")
    st.write("Data for demonstration purposes only")
    st.write("This current development sprint is using live update scraping data version")
   
    player=0
    num_guess=[]
    results = sess.query(UserInput).all()
    for item in results:   
        player+=1
        num_guess.append(item.no_of_guess)
        
    st.write("Registered winners:",player)
    x_axis = [(x+1) for x in range(player)]        
    # y_data=[]
    # for y in range(int(winner)):
    #     y_data.append(random.randint(1,12))
    # x_data=[]
    # for x in range(int(winner)):
    #     x_data.append(x+1)
    average = int(sum(num_guess) / len(num_guess) )
    best= min(num_guess)
    best_record= st.write("Best record: Player won with ", best, "guess(es)")
    print_average = st.write("Average guess per player:",average)
    st.text("  ")
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    
    ax.plot(
        x_axis,
            num_guess,
        )
    
    ax.set_ylabel("Number of guess per Winner")
    ax.set_xlabel("Number of Winner")
    
    st.write(fig)
   
 
    st.text(" ")
    st.write("Live time scraping data needs some time to update")


#%% Version update

if choice == "Version Update":
    
    st.header("Upcoming Updates")
    st.text("* Updating base script and css")
    
    st.header("Potential Updates")
    st.text("* Adding user sign up with hashed password for personal records")
    st.text("* Building a Machine Learning model to study player's strategy and replicate performance")
    
    st.header("Version 2.1 - 05/04/2021")
    st.text("* Added SQL data base for game experience recording")
    st.text("* Updated live web scraping data")
    st.text("* Changed: GUI - from slider interval input box")
    st.text("* Changed: GUI - removed Sidebar - Added Navigation bar")
    
    st.header("Version 2.0 - 05/02/2021")
    st.text("* Rebuilt constructions for mobile version")
    st.text("* Updated sidebar, added Version Update Option")
    
    st.header("Version 1.2 - 04/30/2021")
    st.text("* User choices: Updated Minimum and Maximum range")
    st.text("* Updated sidebar, added View Data Option")
    st.text("* Added number of guess counter")
    
    st.header("Version 1.1 - 04/28/2021")
    st.text("* Fixed bugs cache auto-refreshing")
    st.text("* Fixed bugs overflow from user's input")
    
    st.header("Version 1.0 - 04/20/2021")
    st.text("* Uploaded Web-beta version")
    st.text("* Tested Gameplay and Data Flow")
    
    
    
    

    












