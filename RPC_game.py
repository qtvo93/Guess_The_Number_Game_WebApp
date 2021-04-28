# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 15:49:22 2021

@author: QTVo
"""

import streamlit as st
import random


def strategy(history):
    if not history: return random.choice(['R','P','S'])
        
    else:
        
        Play = [game for game in history]
        
        rP,rS,rR= Play.count('P'),Play.count('S'),Play.count('R')
        fP, fS,fR = rP/ len(Play), rS/ len(Play), rR/ len(Play)
        
        if len(history) > 2:
            if history[-1]=='R'and history[-2]=='R':
                if history[-3] == 'R':
                    if fS > fP :
                        return 'R'
                    else:
                        return 'S'
                elif history[-3]=='S':
                    if fS - fP <= 0:
                        return 'S'
                elif history[-3]=='P':
                    if fP - fS <= 0:
                        return 'P'
                        
            if history[-1]=='S'and history[-2]=='S':
                if history[-3] == 'S':
                    if fR > fP :
                        return 'P'
                    else:
                        return 'R'
                elif history[-3]=='P':
                    if fP - fR <= 0:
                        return 'P'
                elif history[-3]=='R':
                    if fR - fP <= 0:
                        return 'S'
            if history[-1]=='P'and history[-2]=='P':
                if history[-3] == 'P':
                    if fS > fR :
                        return 'S'
                    else:
                        return 'R'
                elif history[-3]=='R':
                    if fR - fS <= 0:
                        return 'R'
                elif history[-3]=='S':
                    if fS - fR <= 0:
                        return 'P'
                
        if fP >= 0.62 : 
            return 'S'
        elif fS >= 0.62 : 
            return 'R'
        elif fR >= 0.62 : 
            return 'P'
        else:
            return random.choices(['P', 'S', 'R'], [fR, fP, fS])[0]
        


st.title('Beat The Rock Paper Scissors Robot App')

#---------------------------------#
# About
expander_bar = st.beta_expander("About")
expander_bar.markdown("""
* **Python libraries:**  streamlit, numpy, random, json, time
* **Credit:** app written by [Quoc Thinh Vo](https://site.quoctvo.com).
""")


#---------------------------------#

history=[]
st.header('Enter your next play (R-P-S):')
play="  "
play = st.text_area("Next play:", play, height=50)

history.append(play)
output= strategy(history)
tracker=0
st.header('Check the box to view the robot play after you input your next play')
st.header('     ')

if st.checkbox('view_robot_play'):
    st.write(output)
    

    
final=" "
if len(history) > 0:
    if (output == 'R' and play =='P') or (output == 'S' and play =='R') or (output == 'P' and play =='S'):
            final = 'Congrats! you win the game'
    elif (output == 'P' and play =='R') or (output == 'R' and play =='S') or (output == 'S' and play =='P'):
            final = "Don't be discouraged. You will win next time"
    else:
            final = "Tie!!!"
else:
    final = "N/A"
if len(history)>tracker:    
    st.write(final)
    tracker+=1
st.header('     ')
st.header('Did you win or have fun playing?')
answer = st.slider("rate this app",0,10,5)