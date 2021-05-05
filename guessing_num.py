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
import numpy as np

#import pandas as pd
#import SessionState
from streamlit import caching
from streamlit.script_runner import StopException, RerunException
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
expander_bar = st.beta_expander("About the App")

expander_bar.markdown("""
* **Guess the Number Game** is a simple Web-App to demonstrate Python, SQL and Data Science streamlit framework
* **Python libraries:**  streamlit, numpy, functools, random, matplotlib, sqlalchemy
* **Version 2.1:** App written by [Quoc Thinh Vo](https://quoctvo.com). 
    Please open the Navigation menu and choose Version Update for more information                                                                                                                                        

    
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

@cache_on_button_press("Click here to reset")
def play_2(min_num,max_num):
    return random.randint(min_num,max_num)
#%% Section 1: header and number interval picking
if choice == "Play Game":
    
    st.subheader('Please choose a difficult level:')
    # min_num=st.number_input("Minimum Number (0-10000):",
    #                    max_value = 10000,
    #                    min_value= 0,
    #                    value =500)
    # max_num=st.number_input("Maximum Number (0-10000):",
    #                    max_value = 10000,
    #                    min_value= 0,
    #                    value =600)
    # if min_num > max_num:
    #     st.error("Max number cannot be smaller than Min number")
    #     st.text("Please adjust the interval and try again")
    #     st.stop().Exception()
    
    menu2 = ["Easy","Medium","Hard", "Custom"]
    level = st.selectbox("Level:",menu2)
    min_num = 0
    max_num = 0
    if level == "Easy":
        max_num = 30
    elif level == "Medium":
        max_num = 100
    elif level == "Hard":
        max_num = 500
    elif level == "Custom":
        min_num=st.number_input("Minimum Number (0 - 10000):",
                        max_value = 10000,
                        min_value= 0,
                        value =500)
        max_num=st.number_input("Maximum Number (0 - 10000):",
                        max_value = 10000,
                        min_value= 0,
                        value =600)
        if min_num > max_num:
            st.error("Max number cannot be smaller than Min number")
            st.write("Please adjust the interval and try again")
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
            #st.write(rand_num)
            state.a +=1
            state.b += 1
            if guess != "":        
                if(rand_num) < int(guess):
                    st.warning('Random number is smaller than your guess')            
                elif (rand_num) > int(guess):
                    st.error('Random number is greater than your guess')    
            else:
                state.a -=1
                state.b -= 1
                st.error("Please enter a valid number")
            st.stop().Exception()
    
    
    #%% Footer + Rating the app
    
    @st.cache(suppress_st_warning = True)
    def form(suppress_st_warning = True):
        my_bar = st.progress(0)
        for percent in range(100):
            time.sleep(0.1)
            my_bar.progress(percent+1)
        st.spinner()
        with st.spinner(text=''):
            time.sleep(5)
            st.success('Done')     
           
    with st.form(key ='record_play'):
        #SQL data base generating:
        engine = create_engine('sqlite:///number_game2_db.sqlite')
        Session = sessionmaker(bind=engine)
        sess= Session()
        
        # Form header and form generating:
        st.subheader("Would you like to submit your records?")
        firstname , lastname = st.beta_columns(2)
        with firstname:
            F_name = st.text_input("Name")
        with lastname:
            L_name = st.text_input("Nickname (will be publicly displayed)")
        
        note, date = st.beta_columns([3,1])
        notefeed = note.text_input("Feedback (Optional)")
        datewin = str(date.date_input("Winning date"))
        rate = int(st.slider("Rate this App:",0,10,6))
        
        submit_button = st.form_submit_button(label='Submit')
    if submit_button :
        if str(rand_num)!= (guess):
            st.error("Oops! Only winner can submit records")
            
        else:
            try:
                
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
       
                    if F_name == "" :
                        if L_name == "":
                            st.error("Please enter your Name")
                            st.error("To stay Anonymous: Leave Name blank and input letter 'A' or 'a' in Nickname ")
                        else:                                
                            if L_name == "A" or L_name == "a":
                                L_name='a'
                                entry = UserInput(firstname=F_name,
                                                          lastname=L_name,
                                                          no_of_guess=state.b,
                                                          date_win=datewin,
                                                          feedback = notefeed,
                                                          rating = rate)
                                sess.add(entry)
                                sess.commit()
                                st.balloons()
                                state.b = 1
                                st.success("Thank you for submitting your playing records!")
                                
                                st.write("⏳ Submitting your form now...")
                                my_bar = st.progress(0)
                                for percent in range(100):               
                                    my_bar.progress(percent+1)
                                    time.sleep(0.04)
                                    
                                st.success('✅ Your form has been submitted. The game will automatically reset shortly')
                                time.sleep(5)
                                caching.clear_cache()
                                raise st.script_runner.RerunException(st.script_request_queue.RerunData(None))
                            else:
                                st.error("Anonymous registration only accepts 'A' or 'a' in Nickname")
                    else:
                        entry = UserInput(firstname=F_name,
                                                          lastname=L_name,
                                                          no_of_guess=state.b,
                                                          date_win=datewin,
                                                          feedback = notefeed,
                                                          rating = rate)
                        sess.add(entry)
                        sess.commit()
                        st.balloons()
                        state.b = 1
                        
                        st.success("Thank you {} for submitting your playing records!".format(F_name))
    
                        st.write("⏳ Submitting your form now...")
                        my_bar = st.progress(0)
                        for percent in range(100):               
                            my_bar.progress(percent+1)
                            time.sleep(0.04)
                            
                        st.success('✅ Your form has been submitted. The game will automatically reset shortly')
                        time.sleep(5)
                        caching.clear_cache()
                        raise st.script_runner.RerunException(st.script_request_queue.RerunData(None))
                else:
                       st.error("Please do not resubmit an existing record")      
            
             
            
            except Exception as e:
                st.error(f"Some error occured : {e}")
                st.error('❌ The page will reset shortly')
                time.sleep(6)
        
            
            
    # if st.button("Reset Page and Play again"):
    #     caching.clear_cache()
    #     raise st.script_runner.RerunException(st.script_request_queue.RerunData(None))
        
 
              
#%% choice == View data
import matplotlib.pyplot as plt

if choice == "View Data":
    engine = create_engine('sqlite:///number_game2_db.sqlite')
    Session = sessionmaker(bind=engine)
    sess= Session()
    
    st.text(" ")
    st.subheader("Guess the Number Game Statistics:")
    st.text("+ Data for demonstration purposes only +")
    st.write("This current development sprint is upgraded with live update scraping data version")
   
    player=0
    num_guess=[]
    player_ID=[]
    no_ID = []
    
    # Qeury for all user in the database:
    results = sess.query(UserInput).all()
    
    for item in results:   
        player+=1
        num_guess.append(item.no_of_guess)
        player_ID.append(item.lastname)
        no_ID.append(item.id)
    
     
    # Print number of winner and average guess per player:  
    st.write("🏆 Registered winners:",player)
    average = float("{:.2f}".format(sum(num_guess) / len(num_guess)) )
    print_average = st.write("  🔥   Average guess per player:",average)
    x_axis = [(x+1) for x in range(player)]        
    # y_data=[]
    # for y in range(int(winner)):
    #     y_data.append(random.randint(1,12))
    # x_data=[]
    # for x in range(int(winner)):
    #     x_data.append(x+1)
    
    
    # make dict of User ID : number of guess
    ID_dict = {}
    for ano,ano_guess in zip(no_ID,num_guess):
        ID_dict[ano] = ano_guess
    
    # make dict of User Nick Name: number of guess 
    Player_ID_dict = {}
    for i,p in zip(no_ID,player_ID):
        Player_ID_dict[i] = p
    
    # Find best winner and corresponding ID:
    best= min(num_guess)     
    find_winner_ID = []
    
    for ID,guess_item in ID_dict.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
        if guess_item == best:
            find_winner_ID .append(ID)           
            
    total_winner = len(find_winner_ID)
    print_out_winner=[]
    for i in range(total_winner):
         index_value = find_winner_ID [i]
         print_out_winner.append(Player_ID_dict[index_value])
        
    best_record= st.write("⭐ Best record:", total_winner, " winner(s) won with", best,"guess(es)")
    
    if st.checkbox("Check to see best record winner list"):
        st.write(" 🏁 Player's Nickname:")
        Id = 0
        control_anonymous = 0
        for player_out in print_out_winner:
            Id+=1           
            if (player_out != "a"):              
                st.write(Id,":",player_out)
            else:              
                registed_ID = find_winner_ID[control_anonymous]
                st.write(Id,":","Anonymous registered ID",registed_ID)
            control_anonymous+=1   
    
    # Graph players vs guesses
    st.subheader("Winner Registration ID vs Number of guess per Winner ID")
    fig = plt.figure(1)
    ax = fig.add_subplot(1,1,1)
    
    if max(x_axis) < 25:
        ax.xaxis.set_ticks(np.arange(min(x_axis), max(x_axis)+1, 1))
    ax.plot(
        x_axis,
            num_guess,
        )
    
    ax.grid()
    ax.set_ylabel("Number of guess")
    ax.set_xlabel("Winner Registration ID")
    st.write(fig)
    
    # Retrieve data form
    with st.form('records_form'):
        st.subheader("Would you like to check your personal records?")
        firstname2 , lastname2 = st.beta_columns(2)
        with firstname2:
            F_name2 = st.text_input("Name")
        with lastname2:
            L_name2 = st.text_input("Nickname")
            
        view_data_button = st.form_submit_button(label='Click to view records')
        if L_name2 == 'A':
            L_name2='a'
    if view_data_button:
        results = sess.query(UserInput).filter_by(firstname=F_name2)\
            .filter_by(lastname=L_name2)
            
        count_item = 0
        for item in results:   
            st.header("Player information:")
            
            firstname3 = item.firstname
            lastname3 = item.lastname
            
            if lastname3 =='A':
                lastname3= 'a'
            f = ""
            l = ""
           
            if  ( firstname3 == "" and lastname3 =="a" ):
                f = "---"
                l = "Anonymous player"
            else: 
                f = firstname3
                l = lastname3
                
            st.write("Name:",f)
            st.write("Nick name:",l )
            count_item +=1
            st.write("Winner with",item.no_of_guess ,"guess(es)")
            st.write("On Date:",item.date_win)
            
        if count_item == 0:
            st.error("No records found for this user")
            
        if st.button("Clear Displays"):
            caching.clear_cache()
            raise st.script_runner.RerunException(st.script_request_queue.RerunData(None))
    
    # fig2 pwer of 2
    fig2 = plt.figure(2)
    ax2 = fig2.add_subplot(2,1,1)
    
    x_axis2 = [(x+1) for x in range(player)]
    y_candy = 0
    y_candy_list=[]
    y_candy_total=0
    total_list=[]
    for i in range(player):
        if y_candy == 0:
            y_candy= 1
            y_candy_list.append(y_candy)
            y_candy_total += y_candy
            total_list.append(y_candy_total)
        else:
            y_candy= y_candy*2
            y_candy_list.append(y_candy)
            y_candy_total += y_candy
            total_list.append(y_candy_total)
          
    ax2.plot(
        x_axis2,
           y_candy_list ,label="Candies per Winner"
        )
    ax2.plot(
        x_axis2,
          total_list ,label="Total Candies"
        )
    if max(x_axis2) < 25:
        ax2.xaxis.set_ticks(np.arange(min(x_axis2), max(x_axis2)+1, 1))
    ax2.legend()
    ax2.set_ylabel("Number of candies")
    ax2.set_xlabel("Registered Winner ID")  
    # 🔥 fire icon     
    st.subheader("The power of two")
    st.write("Imagine we double the number of candies I would receive after each time we got a new registered winner")  
    st.write("Assuming that all registered  winners would send me some candies")
    current_h5= sum(y_candy_list)
    st.write("🍭 Total candies received:",current_h5)
    st.write(" 💖 Thank everyone for parcitipating, supporting, sending sweetness and having fun together")
    st.write(" ✨ Cheers!")
    st.write(fig2)
 
    st.text(" ")
    st.write("**Note**: Live time scraping data needs some time to update depending on the network")


#%% Version update

if choice == "Version Update":
    
    st.subheader("Upcoming Updates")
    st.write("* Updating base script and css")
    st.write("* Updating data seperately for each difficult level")
    st.write("* Updating widget showing the most favorite choice of difficult level")
    
    st.subheader("Potential Updates")
    st.write("* Adding user sign up with hashed password for personal records")
    st.write("* Building a Machine Learning model to study user's strategy and replicate performance")
    
    st.subheader("Version 2.1 - 05/05/2021")
    st.write("* Added SQL data base for game experience recording")
    st.write("* Updated live web scraping data")
    st.write("* Changed: GUI - Minimum and Maximum number: from slider to input box")
    st.write("* Changed: GUI - Removed Sidebar - Added Navigation bar")
    st.write("* Added: Best record player nickname")
    st.write("* Added: Retrieving personal records functionality")
    
    
    st.subheader("Version 2.0 - 05/02/2021")
    st.write("* Re-constructed for mobile version")
    st.write("* Updated sidebar, added Version Update Option")
    
    st.subheader("Version 1.2 - 04/30/2021")
    st.write("* User choices: Updated Minimum and Maximum range")
    st.write("* Updated sidebar, added View Data Option")
    st.write("* Added number of guess counter")
    
    st.subheader("Version 1.1 - 04/28/2021")
    st.write("* Fixed bugs cache auto-refreshing")
    st.write("* Fixed bugs overflow from user's input")
    
    st.subheader("Version 1.0 - 04/20/2021")
    st.write("* Uploaded Web-beta version")
    st.write("* Tested Gameplay and Data Flow")
    
    
    
    

    












