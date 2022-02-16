from datetime import datetime, timedelta
import gspread
import plotly.graph_objects as go
import numpy
import streamlit as st
from PIL import Image
from random import randint
import stringStore


def show_match_page():
    # Function to create a trio of people if one list is bigger than the other
    def oddEven(listA, listB):
        if len(listA) > len(listB):
            double = listA[-1] + ' + ' + (listA[0])
            listA[-1] = double
            del listA[0]
        if len(listB) > len(listA):
            double = listB[-1] + ' + ' + (listB[0])
            listB[-1] = double
            del listB[0]

        return listA, listB

    # Split list of users who have opted in, into two groups
    def split_list(a_list):
        half = len(a_list) // 2
        return a_list[:half], a_list[half:]

    # Colour scheme variables
    primaryColor = stringStore.primaryColor
    secondaryBackgroundColor = stringStore.secondaryColor

    # Load and display banner
    image = Image.open(stringStore.banner)
    st.image(image, use_column_width=True)
    st.header(stringStore.matchHeader)

    # Get user and optIn/Out lists
    gc = gspread.service_account_from_dict(st.secrets[stringStore.googleServiceAccount])
    sh = gc.open_by_url(st.secrets[stringStore.googleSheetsURL])
    nameList = sh.sheet1.col_values(1)
    optArray = sh.sheet1.col_values(2)

    # Separate users who have opted in from out
    optedIn = []
    for choice in range(0, len(optArray)):
        if optArray[choice] == '1':
            optedIn.append(nameList[choice])

    # Split opted in users, into two groups
    a, b = split_list(optedIn)

    # Get max size of each opted in group
    listLength = int(len(optedIn) / 2)

    organiserAttendeeGroups = []

    for x in range(0, listLength):
        b.append(b.pop(b.index(b[0])))
        if (x % 2) == 0:
            organiserAttendeeGroups.append([a, b.copy()])
        else:
            organiserAttendeeGroups.append([b.copy(), a])

    week = int(datetime.date(datetime.today()).strftime("%V"))

    modTablePicker = week % listLength

    a, b = oddEven(organiserAttendeeGroups[modTablePicker][0], organiserAttendeeGroups[modTablePicker][1])

    fig = go.Figure(data=[go.Table(
        header=dict(values=[stringStore.matchFigureOrganiser, stringStore.matchFigureAttendee], fill_color=primaryColor,
                    font_color=stringStore.colorBlack),
        cells=dict(values=[a, b], fill_color=secondaryBackgroundColor))
    ])
    fig.update_layout()
    st.plotly_chart(fig)
