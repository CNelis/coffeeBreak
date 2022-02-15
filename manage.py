import itertools
import random
from datetime import datetime, timedelta

import gspread
import plotly.graph_objects as go
import numpy
import streamlit as st
from PIL import Image
from random import randint

import streamlit as st
import streamlit_authenticator as stauth


def show_admin_page():
    hashed_passwords = stauth.hasher(st.secrets["passwords"]).generate()

    authenticator = stauth.authenticate(st.secrets["names"], st.secrets["usernames"], hashed_passwords,
                                        'some_cookie_name', 'some_signature_key', cookie_expiry_days=0)

    name, authentication_status = authenticator.login('Login', 'main')

    if authentication_status:
        gc = gspread.service_account_from_dict(st.secrets["gcp_service_account"])

        sh = gc.open_by_url(st.secrets["private_gsheets_url"])

        nameList = sh.sheet1.col_values(1)

        addDel = ['Add Users', 'Delete Users']

        st.title('Manage users')
        st.subheader('Which task would you like to perform?')
        select = st.radio('', addDel, 0)
        if select == 'Add Users':
            st.subheader('Input new user name below')
            newUser = st.text_input('')
            if st.button('Add user'):
                sh.sheet1.append_row([newUser, 1])
                st.info('User added')
        else:
            st.subheader('Select user to be deleted')
            option = st.selectbox('', nameList)
            namePosition = nameList.index(option)
            if st.button('Delete user'):
                sh.sheet1.delete_row(namePosition + 1)
                st.info('User deleted')

    if authentication_status == False:
        st.error('Username/password is incorrect')
    if authentication_status == None:
        st.warning('Please enter your username and password')
