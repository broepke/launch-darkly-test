import streamlit as st
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities import LoginError
import yaml
from yaml.loader import SafeLoader
import ldclient
from ldclient import Context
from ldclient.config import Config

st.title("Hello, Streamlit!")
st.code("Username: brian \ chris \nPassword: brian \ chris")

# Get the LaunchDarkly SDK key from Streamlit Secrets
sdk_key = st.secrets["other"]["launchdarkly_sdk_key"]
ldclient.set_config(Config(sdk_key))

# Load credentials from the YAML file
with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

# Uncomment this plus the file write at the end of this script
# stauth.Hasher.hash_passwords(config['credentials'])

# Initialize the authenticator
authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
)

# Store the authenticator object in the session state
st.session_state["authenticator"] = authenticator
# Store the config in the session state so it can be updated later
st.session_state["config"] = config

# Authentication logic
try:
    authenticator.login(location="main", key="launch-darkly-test-app-home")
except LoginError as e:
    st.error(e)

if st.session_state["authentication_status"]:
    authenticator.logout(location="sidebar", key="launch-darkly-test-app-home")

    # Define a feature flag key
    FEATURE_FLAG_KEY = "new-homepage"

    # Get the user's information from Streamlit Authenticator
    app_username = st.session_state.username
    user_email = st.session_state.email
    user_name = st.session_state.name
    user_key = st.session_state["config"]["credentials"]["usernames"][app_username][
        "id"
    ]
    user_gender = st.session_state["config"]["credentials"]["usernames"][app_username][
        "gender"
    ]

    # Build the user context for LaunchDarkly
    builder = Context.builder(user_key)
    builder.kind("user")
    builder.name(user_name)
    builder.set("email", user_email)
    builder.set("gender", user_gender)
    context = builder.build()

    # Evaluate the feature flag for the user
    show_new_homepage = ldclient.get().variation(FEATURE_FLAG_KEY, context, False)

    st.write("**User Key:**", user_key)
    st.write("**User Name:**", user_name)
    st.write("**User Email:**", user_email)
    st.write("**User Geneder:**", user_gender)

    if show_new_homepage:
        # Render the new homepage
        st.write("🆕 This is the new homepage 🆕")

    else:
        # Render the old homepage
        st.write("📠 This is the old homepage 📠")

    left, right = st.columns(2)
    if left.button("Left button", icon="😁", key="left-button", type="secondary"):
        left.write("You clicked the left button!")
    if right.button("Right button", icon="😢", key="right-button", type="primary"):
        right.write("You clicked the right button!")


elif st.session_state["authentication_status"] is False:
    st.error("Username/password is incorrect")
elif st.session_state["authentication_status"] is None:
    st.warning("Please enter your username and password")


with st.expander("Session State for Debugging", icon="💾"):
    st.session_state

# with open('config.yaml', 'w') as file:
#     yaml.dump(config, file, default_flow_style=False)
