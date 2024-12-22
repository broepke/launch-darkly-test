import os
from flask import Flask, request, render_template_string
import ldclient
from ldclient import Context
from ldclient.config import Config

# Initialize LaunchDarkly client with your SDK key
sdk_key = os.getenv("LAUNCHDARKLY_SDK_KEY")
if not sdk_key:
    raise ValueError("LaunchDarkly SDK key is not set in environment variables.")

ldclient.set_config(Config(sdk_key))
ld_client = ldclient.get()

app = Flask(__name__)

# HTML templates
BASE_HTML = """
<!DOCTYPE html>
<html>
    <head>
        <title>Feature Rollout</title>
    </head>
    <body>
        <h1>Welcome, {{ user_name }}</h1>
        <p>User Key: {{ user_key }}</p>
        {% if new_feature %}
            <p><b>🎉 New Feature is Enabled for You! 🎉</b></p>
        {% else %}
            <p><b>🚧 New Feature is Not Available for You Yet. 🚧</b></p>
        {% endif %}
    </body>
</html>
"""


@app.route("/")
def index():
    # Get user context from query parameters
    user_key = request.args.get("user_key", "user123")  # Default to "user123"
    user_name = request.args.get("user_name", "Jane Doe")  # Default to "Jane Doe"

    # Build the user context
    user_context = Context.builder(user_key).kind("user").name(user_name).build()

    # Evaluate feature flag
    new_feature = ld_client.variation("new-homepage", user_context, False)

    # Log the evaluation for debugging
    app.logger.info(f"User context: {user_context}")
    app.logger.info(f"Feature flag 'new-homepage': {new_feature}")

    # Render response
    return render_template_string(
        BASE_HTML, user_name=user_name, user_key=user_key, new_feature=new_feature
    )


if __name__ == "__main__":
    try:
        app.run(debug=True)
    finally:
        # Ensure the LaunchDarkly client is closed
        ld_client.close()