import streamlit as st
import stringStore
from manage import show_admin_page
from matchPage import show_match_page
from optPage import show_opt_page


# Create SideBar
page = st.sidebar.selectbox(stringStore.sideBarSelect, (stringStore.sideBarCoffeePage,
                                                        stringStore.sideBarOptPage,
                                                        stringStore.sideBarAdminPage))

# Switch between pages using the sidebar
if page == stringStore.sideBarCoffeePage:
    show_match_page()
if page == stringStore.sideBarOptPage:
    show_opt_page()
if page == stringStore.sideBarAdminPage:
    show_admin_page()
