# LaunchDarkly Feature Flag Demo

This project demonstrates the implementation of LaunchDarkly feature flags in both a basic Python application and a Streamlit web application. It showcases user authentication, context-based feature flagging, and different implementation approaches.

## Features

- User authentication using Streamlit Authenticator
- LaunchDarkly feature flag integration
- Toggle between old and new homepage versions
- User context-based feature flag evaluation
- Interactive UI elements with Streamlit
- Example implementations in both pure Python and Streamlit

## Project Structure

```
├── Home.py                 # Streamlit web application
├── config.yaml             # User configuration and credentials
├── requirements.txt        # Project dependencies
```

## Prerequisites

- Python 3.x
- LaunchDarkly account and SDK key
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd launch-darkly-test
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your LaunchDarkly SDK key:
```toml
# .streamlit/secrets.toml
[other]
launchdarkly_sdk_key = "your-sdk-key"
```

## Usage

### Streamlit Web Application
Run the Streamlit web application:
```bash
streamlit run Home.py
```

The Streamlit application includes:
- User authentication (default credentials: username: brian/chris, password: brian/chris)
- Feature flag demonstration with homepage variants
- User context information display
- Interactive UI elements

## Feature Flags

The project demonstrates two types of feature flag implementations:

1. Homepage Toggle (Home.py):
   - Flag Key: "new-homepage"
   - User context-based evaluation
   - Includes user attributes (email, gender, etc.)

## Dependencies
- streamlit
- streamlit-authenticator
- launchdarkly-server-sdk

## Additional Resources

- [Google Material Button Icons](https://fonts.google.com/icons)
- [LaunchDarkly Documentation](https://docs.launchdarkly.com/sdk/server-side/python)
- [Streamlit Documentation](https://docs.streamlit.io)
