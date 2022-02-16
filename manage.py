import gspread
import streamlit as st
import streamlit_authenticator as stauth
import stringStore


def show_admin_page():

    # Create passwords, load login area
    hashed_passwords = stauth.hasher(st.secrets["passwords"]).generate()
    authenticator = stauth.authenticate(st.secrets["names"], st.secrets["usernames"], hashed_passwords,
                                        'some_cookie_name', 'some_signature_key', cookie_expiry_days=0)
    name, authentication_status = authenticator.login('Login', 'main')

    # User login successful
    if authentication_status:

        # Get list of user from Google sheets
        gc = gspread.service_account_from_dict(st.secrets[stringStore.googleServiceAccount])
        sh = gc.open_by_url(st.secrets[stringStore.googleSheetsURL])
        nameList = sh.sheet1.col_values(1)

        # Header and subheader
        st.title(stringStore.adminManageUsers)
        st.subheader(stringStore.adminWhichTask)

        # radio button options
        addDel = [stringStore.adminAddUsers, stringStore.adminDeleteUsers]
        select = st.radio('', addDel, 0)

        # default option - add users
        if select == stringStore.adminAddUsers:

            # Get user input
            st.subheader(stringStore.adminInputName)
            newUser = st.text_input('')

            # add user on button click
            if st.button(stringStore.adminAddUser):
                sh.sheet1.append_row([newUser, 1])
                st.info(stringStore.adminUserAdded)

        # other option - delete users
        else:

            # Select user to be deleted
            st.subheader(stringStore.adminDeleteSelect)
            option = st.selectbox('', nameList)

            # Get username position in array, convert to row number
            namePosition = nameList.index(option) + 1

            # Delete user onclick
            if st.button(stringStore.adminDeleteUser):
                sh.sheet1.delete_row(namePosition)
                st.info(stringStore.adminUserDeleted)

    # User auth fails
    if authentication_status == False:
        st.error(stringStore.adminIncorrectPassOrUser)

    # User has not attempted login
    if authentication_status == None:
        st.warning(stringStore.adminEnterCredentials)
