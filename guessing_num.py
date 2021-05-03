# -*- coding: utf-8 -*-
"""
Created on Sun May  2 14:59:05 2021

@author: QTVo
"""


import streamlit as st
import random
import functools
import time


st.title('Guessing the random number')

#---------------------------------#
# About
expander_bar = st.beta_expander("About")
expander_bar.markdown("""
* **Python libraries:**  streamlit, numpy, functools, random 
* **Credit:** app written by [Quoc Thinh Vo](https://site.quoctvo.com).
""")


#---------------------------------#
####
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


@cache_on_button_press("Guess")
def authenticate(rand,gue):
    return rand==gue  

@cache_on_button_press("Let's play")
def play(min_num,max_num):
    return random.randint(min_num,max_num)
   
st.header('Please choose your number interval:')
min_num=st.slider("From:",0,10,9999)
max_num=st.slider("To:",0,10,9999)

if min_num > max_num:
    st.text("First number cannot be smaller than second number! Please choose again")
    st.stop().Exception()
min_num= int(min_num)
max_num= int(max_num)
rand_num = play(min_num,max_num)

st.write("The generated random number is between: ",min_num,"and",max_num)
st.header('Please enter your guess here:')
guess= st.text_input("Guess number:")



   


#Authenticate guess
      
if authenticate(str(rand_num), (guess)):
    if guess == "":
        st.text("Please enter a number before pressing Guess button!")  
    st.write("Random number is: ",rand_num)
    st.success('Congratulations, your guess is right!')
    #st.write("You win the game with",t1, "guessing plays")
   
       
else:   
    if guess != "":        
        if(rand_num) < int(guess):
            st.warning('Random number is smaller than your guess')            
        elif (rand_num) > int(guess):
            st.error('Random number is greater than your guess')    
    else:
        st.text("Please enter a valid number")
    st.stop().Exception()
        
st.header('Did you win or have fun playing?')
answer = st.slider("Rate this app",0,10,5)

if st.button("Rate"):
    link = """ <a href="http://quoctvo.com">Thank you! Click here to go back to my website</a> """
    st.markdown(link, unsafe_allow_html=True)
    st.balloons()

























