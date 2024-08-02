import streamlit_authenticator as stauth
import streamlit as st
import yaml
from yaml.loader import SafeLoader
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#page configs
#st.set_page_config(layout="wide",initial_sidebar_state="collapsed")
hide_decoration_bar_style = '''<style>header {visibility: hidden;}
</style>'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)
#setting page background
page_bg = """
<style>
.stApp{
background-image: url("app/static/bg.png");
background-size: cover;
}
</style>
"""
st.markdown(page_bg,unsafe_allow_html=True)


#st.logo("https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=404,fit=crop,q=95/AGB32Jx3yetEQB4M/wallpapers-7-AoPGzq981wh4PLnV.png", link=None, icon_image=None)

# function for emailing the OTP fro new password creation
def forgotPasswordEmailer():
    # sender credentials
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    username = 'exhibitionease.auth@gmail.com'
    password = 'fvjw lsch ifqy faon'

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = email_of_forgotten_password
    msg['Subject'] = 'Your password has been reset'

    # Email body
    body = f"These are your new login credentials {username_of_forgotten_password}.Password  : {new_random_password},you can use this as your new password or create a new password after logging in using the provided password in the reset password tab"
    msg.attach(MIMEText(body, 'plain'))

        # Send the email
    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
        
        # Login to the SMTP server
        server.login(username, password)
        
        # Send the email
        server.sendmail(username, email_of_forgotten_password, msg.as_string())
        
        print("Email sent successfully!")
        
    except Exception as e:
        print(f"Failed to send email: {e}")

    finally:
        # Disconnect from the server
        server.quit()
#reset password -> function fro writing to the YAML file
# def writeToYaml():
#     with open('./credentials.yaml', 'w') as file:
#         data = yaml.safe_load(file)
#     data['Credentials']['usernames'] = "new_value"

# reading the YAML file
with open('./credentials.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# creating the authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)
#creating the login window
#filler
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")

#creating tabs
tab1, tab2 = st.tabs(["Login","SignUp"])
with tab1:
    authenticator.login()
with tab2:
    try:
        email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(pre_authorization=False)
        if email_of_registered_user:
            st.success('User registered successfully')
        with open('./credentials.yaml', 'w') as file:
            yaml.dump(config, file, default_flow_style=False)
    except Exception as e:
        st.error(e)
# with tab3:
#     try:
#         username_of_forgotten_password, email_of_forgotten_password, new_random_password = authenticator.forgot_password()
#         if username_of_forgotten_password:
#             st.success('New password to be sent securely')
#             forgotPasswordEmailer()
#             # The developer should securely transfer the new password to the user.
#         elif username_of_forgotten_password == False:
#             st.error('Username not found')
#         with open('./credentials.yaml', 'w') as file:
#             yaml.dump(config, file, default_flow_style=False)
#     except Exception as e:
#         st.error(e)
#     Otp = st.text_input("Enter the one time password received in mail")
#     new_pass = st.text_input("Enter your new password ")
    
#     if st.button("submit"):
# #        existing_pass = data['credentials']['usernames'][username_of_forgotten_password]['password']
        
#         if new_random_password == Otp:
#                     # Update the password
#             new_random_password = new_pass
#             with open('./credentials.yaml', 'w') as file:
#                 yaml.dump(config, file, default_flow_style=False)
#             st.success('Password has been reset, Login to continue')
#         else:
#             st.warning('Wrong OTP', icon="⚠️")

#authenticating
if st.session_state['authentication_status']:
    authenticator.logout()
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.title('Some content')
elif st.session_state['authentication_status'] is False:
    st.error('Username/password is incorrect')
#elif st.session_state['authentication_status'] is None:
#    st.warning('Please enter your username and password')

#updating the YAML file for any changes
with open('./credentials.yaml', 'w') as file:
    yaml.dump(config, file, default_flow_style=False)