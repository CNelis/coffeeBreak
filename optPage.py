import numpy
import streamlit as st
from PIL import Image
from google.oauth2 import service_account
from gsheetsdb import connect
import gspread
import datetime

import stringStore


def show_opt_page():
    # load image and display as header
    image = Image.open(stringStore.banner)
    st.image(image, use_column_width=True)
    st.header(stringStore.optHeader)

    optOptions()


def optOptions():

    # Get array of users and opt in/out info
    gc = gspread.service_account_from_dict(st.secrets[stringStore.googleServiceAccount])
    sh = gc.open_by_url(st.secrets[stringStore.googleSheetsURL])
    nameList = sh.sheet1.col_values(1)
    optArray = sh.sheet1.col_values(2)

    # Radio button options
    inOut = [stringStore.optImIn, stringStore.optImOut]

    # Select dropdown, populated with usernames
    option = st.selectbox(stringStore.optSelectName, nameList)

    # Stores selected user index
    namePosition = nameList.index(option)

    # Only true on a Monday
    if datetime.datetime.today().weekday() == 0:

        # true if selected user has opted in
        if optArray[namePosition] == '1':

            # radio button update users preference, default in
            select = st.radio(stringStore.optFreeForChat, inOut, 0)
            if select == stringStore.optImIn:
                sh.sheet1.update_cell(namePosition + 1, 2, '1')
            else:
                sh.sheet1.update_cell(namePosition + 1, 2, '0')

        # true if selected user has opted out
        else:

            # radio button update users preference, default out
            select = st.radio(stringStore.optSelectOne + option, inOut, 1)
            if select == stringStore.optImIn:
                sh.sheet1.update_cell(namePosition + 1, 2, '1')
            else:
                sh.sheet1.update_cell(namePosition + 1, 2, '0')
    else:
        st.warning(stringStore.optAvailabilityMessage)
