import numpy
import streamlit as st
from PIL import Image
from google.oauth2 import service_account
from gsheetsdb import connect
import gspread
import datetime


def show_opt_page():
    image = Image.open('banner/CGI_LinkedIn_banner_modern_office.jpg')
    st.image(image, use_column_width=True)

    st.header('Opt In/Out of Coffee Chats')

    optOptions()


def optOptions():
    gc = gspread.service_account_from_dict(st.secrets["gcp_service_account"])

    sh = gc.open_by_url(st.secrets["private_gsheets_url"])

    nameList = sh.sheet1.col_values(1)

    optArray = sh.sheet1.col_values(2)

    inOut = ['Im In!', 'Im Out!']

    option = st.selectbox('Select your name', nameList)

    namePosition = nameList.index(option)

    if datetime.datetime.today().weekday() == 0:
        if optArray[namePosition] == '1':
            select = st.radio('Are you free for a chat?', inOut, 0)
            if select == 'Im In!':
                sh.sheet1.update_cell(namePosition + 1, 2, '1')
            else:
                sh.sheet1.update_cell(namePosition + 1, 2, '0')
        else:
            select = st.radio('Select one ' + option, inOut, 1)
            if select == 'Im In!':
                sh.sheet1.update_cell(namePosition + 1, 2, '1')
            else:
                sh.sheet1.update_cell(namePosition + 1, 2, '0')
    else:
        st.warning("Opt in and opt out available on Mondays")
