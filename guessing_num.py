# -*- coding: utf-8 -*-
"""
Created on Sun May  2 14:59:05 2021

@author: QTVo
"""


import streamlit as st
import random
import functools
import time
import pandas as pd
import SessionState
from streamlit import caching
from streamlit.script_runner import StopException, RerunException
st.title('Guess the Number Game')

#---------------------------------#
# About
expander_bar = st.beta_expander("About")
expander_bar.markdown("""
* **Guess the Number Game** is a simple Web-App to demonstrate Python and Data Science framework
* **Python libraries:**  streamlit, numpy, functools, random, matplotlib
* **Credit:** app written by [Quoc Thinh Vo](https://site.quoctvo.com)
""")


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

#%% Side bar
st.sidebar.header("Please choose an option")
menu = ["Play Game", "View Data", "Version Update"]
choice = st.sidebar.selectbox("Menu", menu)    	
#%% function declarations

@cache_on_button_press("Guess")
def authenticate(rand,gue):
    return rand==gue  

@cache_on_button_press("Let's play")
def play(min_num,max_num):
    return random.randint(min_num,max_num)
 
#%% Section 1: header and number interval picking
if choice == "Play Game":
    ss = SessionState.get(x=1)
    st.header('Please choose a number range:')
    st.text("  ")
    min_num=st.slider("Minimum:",0,9999,1000)
    max_num=st.slider("Maximum:",0,9999,3000)
    
    if min_num > max_num:
        st.error("Max number cannot be smaller than Min number")
        st.text("Please adjust the interval and try again")
        st.stop().Exception()
    min_num= int(min_num)
    max_num= int(max_num)
    rand_num = play(min_num,max_num)
    
    #%% Section 2: Generating random number and guessing
    
    st.write("The generated random number is between: ",min_num,"and",max_num)
    st.header('Please enter your guess here:')
    guess= st.text_input("Guess number:")
    
    #%% Authenticate guess vs random num
     
    
     
    if authenticate(str(rand_num), (guess)):
        if guess == "":
            st.text("Please enter a number before pressing Guess button!")  
        st.write("Random number is: ",rand_num)
        st.success('Congratulations, your guess is right!')
        st.write("You win the game with",ss.x, "guessing plays")
        ss.x = 1     
    else: 
        ss.x +=1
        if guess != "":        
            if(rand_num) < int(guess):
                st.warning('Random number is smaller than your guess')            
            elif (rand_num) > int(guess):
                st.error('Random number is greater than your guess')    
        else:
            st.text("Please enter a valid number")
        st.stop().Exception()
    
    
    #%% Footer + Rating the app
           
    st.header('Did you win or have fun playing?')
    answer = st.slider("Rate this app",0,10,5)
    
    if st.button("Rate"):
        link = """ <a href="http://quoctvo.com">Thank you! Click here to go back to my website</a> """
        st.markdown(link, unsafe_allow_html=True)
        st.balloons()
    
#%% choice == View data
import matplotlib.pyplot as plt

if choice == "View Data":
    st.text(" ")
    st.write("Data for demonstration purposes only")
    st.write("Live update scraping data will be coming soon in the next version")
    player = 59
    winner = 55
    number_of_players = st.write("Players:",player)
    player_win= st.write("Winners:",winner)
    
   
    y_data=[]
    for y in range(int(winner)):
        y_data.append(random.randint(1,12))
    x_data=[]
    for x in range(int(winner)):
        x_data.append(x+1)
    average = int(sum(y_data) / len(y_data) )
    best= min(y_data)
    best_record= st.write("Best record: Player won with ", best, "guess(es)")
    print_average = st.write("Average guess per play:",average)
    st.text("  ")
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    
    ax.plot(
        x_data,
            y_data,
        )
    
    ax.set_ylabel("Number of guess per Winner")
    ax.set_xlabel("Number of Winner")
    
    st.write(fig)
    st.text(" ")
    st.write("Live time scraping data is being worked on and will be updated soon.")


#%% Version update

if choice == "Version Update":
    
    st.header("Upcoming Updates")
    st.text("* Adding SQL data base for game experience recording")
    st.text("* Updating live web scraping data")
    st.header("Potential Updates")
    st.text("* Adding user sign up for personal records")
    st.text("* Building a Machine Learning model to study player's strategy and replicate performance")
    
    st.header("Version 2.0 - 05/03/2021")
    st.text("* Rebuilt constructions for mobile version")
    st.text("* Updated sidebar, added Version Update Option")
    
    st.header("Version 1.2 - 04/30/2021")
    st.text("* User choices: Updated Minimum and Maximum range")
    st.text("* Updated sidebar, added View Data Option")
    st.text("* Added number of guess counter")
    
    st.header("Version 1.0 - 04/28/2021")
    st.text("* Fixed bugs cache auto-refreshing")
    st.text("* Fixed bugs overflow from user's input")
    
    st.header("Version 1.0 - 04/20/2021")
    st.text("* Uploaded Web-beta version")
    st.text("* Tested Gameplay and Data Flow")
    
    
    
    

    












