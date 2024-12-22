import streamlit as st
import ldclient
from ldclient import Context
from ldclient.config import Config

# Get the LaunchDarkly SDK key from Streamlit Secrets
sdk_key = st.secrets["other"]["launchdarkly_sdk_key"]
ldclient.set_config(Config(sdk_key))

# Define a feature flag key
FEATURE_FLAG_KEY = "new-homepage"

# Define the user context
user_key = "532169c2-a050-4210-841c-9ecc95a22cc8"
user_name = "Jane Doe"
context = Context.builder(user_key).kind("user").name(user_name).build()

# Evaluate the feature flag for the user
show_new_homepage = ldclient.get().variation(FEATURE_FLAG_KEY, context, False)

st.title("Hello, Streamlit!")

if show_new_homepage:
    # Render the new homepage
    st.write("**User Key:**", user_key)
    st.write("**User Name:**", user_name)
    st.write("🆕 This is the new homepage 🆕")
    left, right = st.columns(2)
    if left.button("Left button", icon="😁"):
        left.write("You clicked the left button!")
    if right.button("Right button", icon="😢"):
        right.write("You clicked the right button!")
else:
    # Render the old homepage
    st.write("**User Key:**", user_key)
    st.write("**User Name:**", user_name)
    st.write("📠 This is the old homepage 📠")
    left, right = st.columns(2)
    if left.button("Left button", icon="😁"):
        left.write("You clicked the left button!")
    if right.button("Right button", icon="😢"):
        right.write("You clicked the right button!")
