# -*- coding: utf-8 -*-
"""
Created on Mon May  3 12:04:42 2021

@author: QTVo
"""

""" 
#%% # DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data
#%% Password hashing

import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False


#%% sidebar form decor

st.sidebar.header("Login Form")
menu = ["Login", "SignUp"]
choice = st.sidebar.selectbox("Menu", menu)
if choice == "Login":
    user = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type = "password")
    if st.sidebar.checkbox('Login') :
        create_usertable()
        hashed_pswd = make_hashes(password)
        result = login_user(user,check_hashes(password,hashed_pswd))
        if result:
            st.success("Logged In as {}".format(user))
elif choice == "SignUp":
    first =st.sidebar.text_input("First Name")
    last = st.sidebar.text_input("Last Name")
    email, user = st.sidebar.beta_columns(2)
    email.text_input("Email (Optional")
    user.text_input("Username")
    password = st.sidebar.text_input("Password", type = "password")
    retypepassword = st.sidebar.text_input("Retype Password", type = "password")
    if password != retypepassword:
        st.sidebar.error("Password and Retype Password are different")
    else:
        if st.sidebar.button('SignUp'):          
            create_usertable()
            add_userdata(user,make_hashes(password))
            st.success("You have successfully created an account.Go to the Login Menu to login")
"""