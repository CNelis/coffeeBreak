from datetime import datetime, timedelta
import gspread
import plotly.graph_objects as go
import numpy
import streamlit as st
from PIL import Image
from random import randint
import stringStore


def show_match_page():
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

    primaryColor = stringStore.primaryColor
    secondaryBackgroundColor = stringStore.secondaryColor

    image = Image.open(stringStore.banner)
    st.image(image, use_column_width=True)

    st.header(stringStore.matchHeader)

    gc = gspread.service_account_from_dict(st.secrets[stringStore.googleServiceAccount])

    sh = gc.open_by_url(st.secrets[stringStore.googleSheetsURL])

    nameList = sh.sheet1.col_values(1)

    optArray = sh.sheet1.col_values(2)
    optedIn = []

    for choice in range(0, len(optArray)):
        if optArray[choice] == '1':
            optedIn.append(nameList[choice])

    def split_list(a_list):
        half = len(a_list) // 2
        return a_list[:half], a_list[half:]

    listLength = int(len(optedIn) / 2)
    organiserAttendeeGroups = []
    a, b = split_list(optedIn)

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
