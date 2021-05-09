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
# from datetime import date
#import pandas as pd
#import SessionState
import bcrypt
from streamlit import caching
from streamlit.script_runner import StopException, RerunException
from sqlalchemy.orm import sessionmaker
from project_orm_guess_game import UserInput, UserHistory
from sqlalchemy import create_engine

#%% session state :
    
from session_state import get_state
class MyState:
    a: int
    b: int
    reward: int
    trivia: int
    
    def __init__(self, a: int, b: int,trivia: int,reward: int):
        self.a = a
        self.b = b
        self.trivia = trivia
        self.reward = reward

def setup(a: int, b: int,trivia: int,reward: int) -> MyState:
    return MyState(a,b,trivia,reward)




#%%
st.title('Guess the Number Game')

#---------------------------------#
# About
expander_bar = st.beta_expander("About the App")

expander_bar.markdown("""
* **Guess the Number Game** is a simple Web-App to demonstrate Python, SQL and Data Science streamlit framework
* **Python libraries:**  streamlit, numpy, bcrypt, functools, random, matplotlib, sqlalchemy
* **Version 2.2:** App written by [Quoc Thinh Vo](https://quoctvo.com). 
    Please open the Navigation bar and choose Game Versions for more information                                                                                                                                        

    
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
    
#st.subheader("*************************************")
menu = ["Home", "Game Statistics", "Game Versions"]
choice = st.selectbox("Navigation", menu)   
 	
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

salt = b'$2b$12$qGA7Ps7wsWagoMz8nQQDYu'
#%% Section 1: header and number interval picking
if choice == "Home":
        
    st.subheader('Ready to find the secret number?')
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
    state = get_state(setup, a=1, b=1,reward=0,trivia=0)
    menu2 = ["Easy","Medium","Hard"] #"Custom"
    st.write("The more difficult level, the better rewards!")
    level = st.selectbox("Please choose a difficult level and start playing:",menu2)
    min_num = 0
    max_num = 0
    if level == "Easy":
        max_num = 30
        state.reward = 1
    elif level == "Medium":
        max_num = 100
        state.reward = 3
    elif level == "Hard":
        max_num = 500
        state.reward = 6
    # elif level == "Custom":
    #     min_num=st.number_input("Minimum Number (0 - 10000):",
    #                     max_value = 10000,
    #                     min_value= 0,
    #                     value =500)
    #     max_num=st.number_input("Maximum Number (0 - 10000):",
    #                     max_value = 10000,
    #                     min_value= 0,
    #                     value =600)
    #     if min_num > max_num:
    #         st.error("Max number cannot be smaller than Min number")
    #         st.write("Please adjust the interval and try again")
    #         st.stop().Exception()
        
        
    min_num= int(min_num)
    max_num= int(max_num)
    
    #initialize random number, play counter and timer:
    #ss = SessionState.get(x=1)
    
    
   # timer = SessionState.get(t=0)
    #current=time.time()
    #start_time = get_state(setup, a= current)
    rand_num = play(min_num,max_num)

    #%% Section 2: Generating random number and guessing
    with st.form(key='guess'):
        st.write("The generated random number is between: ",min_num,"and",max_num)        
        st.subheader('Please enter your guess here:')
        guess= st.number_input("Guessing number:",min_value = 0,max_value=500)
        
    #%% Section 3: Authenticate guess vs random num
          
       # if authenticate(str(rand_num), (guess)):
        submit_button2 = st.form_submit_button(label='Guess')
        
    if submit_button2:
        if int(rand_num)== int(guess):
            if guess == "":
                st.text("Please enter a number before pressing Guess button!")  
            st.write("Random number is: ",rand_num)
            st.success('Congratulations, your guess is right!')
            st.write("You win the game with",state.a, "guessing play(s)")
            state.a = 1
        else: 
            #For debugging print out rand_num
            #st.write(rand_num)
            state.a +=1
            state.b += 1
            if guess != "":        
                if int(rand_num) < int(guess):
                    st.warning('Random number is SMALLER than your guess')            
                elif int(rand_num) > int(guess):
                    st.error('Random number is GREATER than your guess')    
            else:

                state.a -=1
                state.b -= 1
                st.error("Please enter a valid number")
            st.stop().Exception()
    
    #%% Section 4: Submit records for rewards
    
    with st.form(key ='record_play'):
        #SQL data base generating:
        engine = create_engine('sqlite:///web_game4_db.sqlite')
        Session = sessionmaker(bind=engine)
        sess_1= Session()
        
        engine2 = create_engine('sqlite:///web_game4_db.sqlite')
        Session2 = sessionmaker(bind=engine2)
        sess_2= Session2()
        
        # Form header and form generating:
        st.subheader("Submit your winning records for rewards")
        st.write("* Already have an account?")
        st.write("Submit records using your created Username and Password to earn accumluated rewards")
        st.write("* Or simply type in new Username and Password to create an account and start earning")
        username1 , passcode1 = st.beta_columns(2)
        with username1:
            U_name = st.text_input("Username")
        with passcode1:
            U_code = st.text_input("Password",type="password")
        
        
        this_reward = state.reward
        now_local = time.localtime()
        now = str(time.strftime("%c",now_local))
        
        
        if st.checkbox("Not a spamming bot? Please check here"):
            state.trivia = 1
            st.write("Great, thank you!")
            
            
        col2,col3 = st.beta_columns([3,3])    
        with col2:
            st.write("Winning Rewards:")
            st.write(this_reward,"candy tokens +🍭+")
            
        with col3:
            st.write("Winning Date:")
            st.write(now)
    
        submit_button = st.form_submit_button(label='Submit')
        
    if submit_button :
        
        if not state.trivia:
            st.error("Make sure to check the trivia box")
            
        else:
            
            if int(rand_num)!= int(guess):
                st.error("Oops! Only winner can submit records")
          
            else:
                try:
                    if U_name =="" or U_code=="":
                        st.error("Please fill in all the required fields")
                    else:
                        x = sess_1.query(UserInput).get(U_name)
                        my_pw = bcrypt.hashpw(U_code.encode(), salt)
                        if x is None :         # New user         
                            entry = UserInput(username=U_name, passcode=my_pw, rewards=state.reward,\
                                              playing_time = 1)
                            sess_1.add(entry)
                            sess_1.commit()
                            st.balloons()
                            
                            # Doing the same thing for UserHistory table:
                            entry2 = UserHistory(username=U_name, passcode=my_pw,\
                                               guess_numbers=state.b, this_rewards=state.reward,\
                                                   date_win = now)
                            sess_2.add(entry2)
                            sess_2.commit()
                            state.b = 1
                            state.trivia=0
                            
                            st.success("Thank you for submitting your playing records!")                             
                            st.write("⏳ Submitting your records now...")
                            
                            my_bar = st.progress(0)
                            for percent in range(100):               
                                my_bar.progress(percent+1)
                                time.sleep(0.025)
                                            
                            st.success('✅ Records successfully submitted. The game will automatically reset shortly!')
                            time.sleep(4.5)
                            caching.clear_cache()
                            raise st.script_runner.RerunException(st.script_request_queue.RerunData(None))
                        
                    # There's user already but wrong passcode
                        elif x.passcode != my_pw:
                            st.error("Username already exists! Please use a different Username or make sure Password is correct")
                    
                    # Matched user and passcode:
                        elif x.passcode == my_pw:
                            x.rewards += state.reward
                            x.playing_time += 1
                            sess_1.commit()
                            entry3 = UserHistory(username=U_name, passcode=my_pw,\
                                               guess_numbers=state.b, this_rewards=this_reward,\
                                                   date_win = now)
                            sess_2.add(entry3)
                            sess_2.commit()
                            state.b = 1
                            state.trivia=0
                            
                            st.success("Thank you for submitting your playing records!")                             
                            st.write("⏳ Submitting your records now...")
                            
                            my_bar = st.progress(0)
                            for percent in range(100):               
                                my_bar.progress(percent+1)
                                time.sleep(0.025)
                                            
                            st.success('✅ Records successfully submitted. The game will automatically reset shortly!')
                            time.sleep(4.5)
                            caching.clear_cache()
                            raise st.script_runner.RerunException(st.script_request_queue.RerunData(None))
            
                except Exception as e:
                    st.error(f"❌ Some error occured : {e}")
                    st.error('The page will reset shortly')
                    time.sleep(4.5) 
                    caching.clear_cache()
                    raise st.script_runner.RerunException(st.script_request_queue.RerunData(None))
#%% choice == GAME STATISTICs
import matplotlib.pyplot as plt

if choice == "Game Statistics":
    engine = create_engine('sqlite:///web_game4_db.sqlite')
    Session = sessionmaker(bind=engine)
    sess= Session()
    
    
    st.text(" ")
    st.subheader("Guess the Number Game Statistics:")
    st.text("+ Data for demonstration purposes only +")
    st.write("This current development sprint is upgraded with live update scraping data version")
   
    
    unique=0
    unique_dict = {}
    reward_list =[]
    # Query for all user in the USERINPUT database:
    results = sess.query(UserInput).all()
    
    for item in results:   
        unique+=1
        unique_dict[item.username]=(item.rewards,item.playing_time)
        reward_list.append(item.rewards)
    
    # Query for all user in the USER HISTORY database:
    results2 = sess.query(UserHistory).all()
    num_guess=[]
    no_ID = []
    player_username =[]
    player=0
    
    for item in results2:   
        player+=1
        num_guess.append(item.guess_numbers)
        no_ID.append(item.id)
        player_username.append(item.username)
    # Print number of winner and average guess per player:  
    st.write("🏆 Registered winners:",player)
    average = float("{:.1f}".format(sum(num_guess) / len(num_guess)) )
    print_average = st.write("  🏁  Average guess per player:",average)
    x_axis = [(x+1) for x in range(player)]        
  
    
    # make dict of User ID : number of guess
    ID_dict = {}
    for U_ID,no_guess in zip(no_ID,num_guess):
        ID_dict[U_ID] = no_guess 
    
    # make dict of User Nick Name: number of guess 
    player_ID_dict = {}
    for i,p in zip(no_ID,player_username):
        player_ID_dict[i] = p
    
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
          print_out_winner.append(player_ID_dict[index_value])
        
    best_record= st.write("⭐ Best record:", total_winner, " winner(s) won with", best,"guess(es)")
    
    
   
    if st.checkbox("Check here to see Best Record Winner(s)"):
        #st.write(" 🔥 🔥 🔥 Username ")
        Id = 0
        # control_anonymous = 0
        for player_out in print_out_winner:
            Id+=1                                 
            st.write("🔥 Username:",player_out)
            # else:              
            #     registed_ID = find_winner_ID[control_anonymous]
            #     st.write(Id,":","Anonymous registered ID",registed_ID)
            # control_anonymous+=1   
            
    
    output_uni = []
    if st.checkbox("Check here to see Token Leader(s)"):
        reward_list.sort(reverse = True)
        i =0
        for key,item in unique_dict.items():
                if item[0] == reward_list[0]:
                    i+=1
                    st.write(i,"💰 Username:",key,"--- Total tokens won:",item[0],"--- Played: ",item[1],"times")
                if item[0] == reward_list[1]:
                    i+=1
                    st.write(i,"💰 Username:",key,"--- Total tokens won:",item[0],"--- Played: ",item[1],"times")
                if item[0] == reward_list[2]:
                    i+=1
                    st.write(i,"💰  Username:",key,"--- Total tokens won:",item[0],"--- Played: ",item[1],"times")
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
    
   
## fig2 power of 2 graph

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
            y_candy_list ,label="Generated Tokens per Winner"
        )
    ax2.plot(
        x_axis2,
          total_list ,label="Total Candy Tokens"
        )
    if max(x_axis2) < 25:
        ax2.xaxis.set_ticks(np.arange(min(x_axis2), max(x_axis2)+1, 1))
    ax2.legend()
    ax2.set_ylabel("Number of candy tokens")
    ax2.set_xlabel("Registered Winner ID")  
    # 🔥 fire icon     
    st.subheader("The Community Power")
    st.write("Imagine the number of candy tokens generated is doubled each time there's a new winner")  
    st.write("Wonder how many tokens our community would receive?")
    current_h5= sum(y_candy_list)
    st.write("🍭 Total candy tokens generated:",current_h5)
    st.write(" 💖 Thank everyone for parcitipating, supporting, sending sweetness and having fun together")
    st.write(" ✨ Cheers!")
    st.write(fig2)
 
    st.text(" ")
    st.write("**Note**: Live time scraping data needs some time to update depending on the network")
    st.text(" ")
#     #--------------------------------------------#
#     # Testing form
#     #---------------------------------------------#
    # Retrieve data form
    #a=st.selectbox("Would you like to check your playing records?",["General Information","In Details"])
    #if a == "General Information":\
    if 1:
        with st.form('records_form'):
            st.subheader("Would you like to check your playing records?")
            firstname2 , usercode2 = st.beta_columns(2)
            with firstname2:
                F_name2 = st.text_input("Userame")
            with usercode2:
                code2 = st.text_input("Password",type="password")
            
            col1,col2 = st.beta_columns([1,1])
            with col1:
                view_data_button = st.form_submit_button(label='View Account Tokens')
            with col2:
                view_data_button2 = st.form_submit_button(label='View Account Playing History')
               
        if view_data_button:
            
            x = sess.query(UserInput).get(F_name2)
            
            if x:
                my_retrieving_pw = bcrypt.hashpw(code2.encode(), salt)
                if x.passcode == my_retrieving_pw:
                    st.write("Username:",x.username)
                    st.write("Total tokens won:",x.rewards)                
                    st.write("Total playing times:",x.playing_time)
                else:
                    st.error("Wrong password")
            else:
                st.error("No records found for this user")
                
            if st.button("Close Displays"):
                caching.clear_cache()
                raise st.script_runner.RerunException(st.script_request_queue.RerunData(None))
    #if a == "In Details":
    # if 1:
    #     with st.form('records_form2'):
      
    #         firstname2 , usercode2 = st.beta_columns(2)
    #         with firstname2:
    #             F_name2 = st.text_input("Userame")
    #         with usercode2:
    #             code2 = st.text_input("Password",type="password")
                
            
      
                
        if view_data_button2:
            list_x = sess.query(UserHistory).filter_by(username=F_name2)
            count = sess.query(UserHistory).filter_by(username=F_name2).count()
           
            if list_x:
                y = count
                for x in list_x:
                    y -=1
                    my_retrieving_pw = bcrypt.hashpw(code2.encode(), salt)
                    if x.passcode == my_retrieving_pw:
                        
                        st.write("--------------------")
                        st.write("Username:",x.username)
                        st.write("Tokens won:",x.this_rewards)                
                        st.write("Winner with:",x.guess_numbers,"guess(es)")
                        st.write("Winning Date:",x.date_win)
                    else:
                        if y == 0:
                            st.error("Wrong password")
            if count == 0:
                st.error("No records found for this user")
                
            if st.button("Close History"):
                caching.clear_cache()
                raise st.script_runner.RerunException(st.script_request_queue.RerunData(None))
        


#%% Version update

if choice == "Game Versions":
    
    st.subheader("Upcoming Updates")
    st.write("* Updating base script and css")
    st.write("* Updating data seperately for each difficult level")
    st.write("* Updating widget showing the most favorite choice of difficult level")
    
    st.subheader("Potential Updates")
    st.write("* Building a Machine Learning model to study user's strategy and replicate performance")
    
    st.subheader("Version 2.2 - 05/08/2021")
    st.write("* Updated username and password sign-in to retrieve personal records")
    st.write("* Added hashed function for password security purposes")
    st.write("* Added user's accumulated rewards and playing times")
  
    
    st.subheader("Version 2.1 - 05/05/2021")
    st.write("* Added SQL data base for game experience recording")
    st.write("* Updated live web scraping data")
    st.write("* Changed: GUI - Removed Custom range - Added pre-designed difficult level")
    st.write("* Changed: GUI - Removed Sidebar - Added Navigation bar")
    st.write("* Added: Best record player list")
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
    
    
    
    

    












