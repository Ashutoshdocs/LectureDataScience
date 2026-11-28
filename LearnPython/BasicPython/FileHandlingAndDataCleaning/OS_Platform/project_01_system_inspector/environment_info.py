import os


def collect_selected_environment(keys):
    """
    Return only requested environment variables.

    Avoid printing or saving the entire environment because it may contain
    passwords, API keys, access tokens, or other sensitive configuration.
    """
    return {key: os.getenv(key, "<not set>") for key in keys}
