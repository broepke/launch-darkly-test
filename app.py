from flask import Flask, render_template
import os
import ldclient
from ldclient import Context
from ldclient.config import Config


# Set sdk_key to your LaunchDarkly SDK key.
sdk_key = os.getenv("LAUNCHDARKLY_SDK_KEY")
ldclient.set_config(Config(sdk_key))


app = Flask(__name__)

# Define a feature flag key
FEATURE_FLAG_KEY = "new-homepage"


@app.route("/")
def index():
    # Get the user's context. This could be based on session data,
    # user ID, or other identifying information.
    user = {
        "key": "user123",  # Unique identifier for the user
        "firstName": "Jane",
        "lastName": "Doe",
        "email": "jane.doe@example.com",
    }

    context = Context.builder("example-user-key").kind("user").name("Sandy").build()

    # Evaluate the feature flag for the user
    # show_new_homepage = ldclient.variation(FEATURE_FLAG_KEY, user, False)
    show_new_homepage = ldclient.get().variation(FEATURE_FLAG_KEY, context, False)
    print(show_new_homepage)

    if show_new_homepage:
        # Render the new homepage
        return render_template("new_homepage.html")
    else:
        # Render the old homepage
        return render_template("old_homepage.html")


if __name__ == "__main__":
    app.run(debug=True)
