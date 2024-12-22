import random
import streamlit as st
import ldclient
from ldclient import Context
from ldclient.config import Config

# Get the LaunchDarkly SDK key from Streamlit Secrets
sdk_key = st.secrets["other"]["launchdarkly_sdk_key"]
ldclient.set_config(Config(sdk_key))

# Define a feature flag key
FEATURE_FLAG_KEY = "new-homepage"

cohort = random.choice(["A", "B"])
if cohort == "A":
    # Define the user context for cohort A
    user_key = "532169c2-a050-4210-841c-9ecc95a22cc8"
    user_name = "Jane Doe"
    user_email = "jane.doe@example.com"
    user_gender = "Female"
else:
    # Define the user context for cohort B
    user_key = "b2e0c2b4-5e0e-4f2b-8c2f-8f0e4e2b5f2b"
    user_name = "John Doberman"
    user_email = "john.dobs@meglocorp.com"
    user_gender = "Male"

# Build the user context
builder = Context.builder(user_key)
builder.kind("user")
builder.name(user_name)
builder.set("email", user_email)
builder.set("gender", user_gender)
context = builder.build()

# Evaluate the feature flag for the user
show_new_homepage = ldclient.get().variation(FEATURE_FLAG_KEY, context, False)

st.title("Hello, Streamlit!")
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