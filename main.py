import streamlit as st

from manage import show_admin_page
from matchPage import show_match_page
from optPage import show_opt_page

page = st.sidebar.selectbox("Select an Option:", ('Coffee Chat Matches', 'Opt In/Out', 'Admin'))

if page == 'Coffee Chat Matches':
    show_match_page()
if page == 'Opt In/Out':
    show_opt_page()
if page == 'Admin':
    show_admin_page()
