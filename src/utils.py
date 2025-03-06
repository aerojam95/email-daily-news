# =============================================================================
# Modules
# =============================================================================

# Python
import os

# Third-party
import requests

# Custom
from custom_logger import get_custom_logger

# =============================================================================
# Variables
# =============================================================================

# Logging
logger = get_custom_logger("data/configurations/logger.yaml")

# Requests
DEFAULT_URL = "https://newsapi.org/v2/everything?q=tesla&from=2025-02-06&sortBy=publishedAt"

# =============================================================================
# Functions
# =============================================================================

def get_api_url(url:str):
    """Get URL which contains URL API key to access endpoint URL

    Args:
        url (str): Endpoint URL

    Raises:
        ValueError: no API key found in ENV variable NEWS_API_KEY
        RuntimeError: unexpected error

    Returns:
        str: augmented URL with API key
    """
    try:
        logger.info("Getinng API key from ENV variable...")
        api_key = os.getenv("NEWS_API_KEY")
        logger.info("Have API key from ENV variable")
        endpoint = f"{url}&apiKey={api_key}"
        logger.debug(f"Endpoint: {endpoint}")
        return endpoint
            
    except ValueError as ve:
        logger.critical(f"ValueError: {ve}")
        raise

    except Exception as e:
        logger.critical(f"Error: {e}")
        raise RuntimeError(f"RuntimeError: {e}") from e
        

def get_http_response(url:str, headers:str):
    """_Get HTTP response from endpoint and return JSON of response

    Args:
        url (str): URL of the endpoint to send HTTP request
        headers (str, optional): Headers for senfind HTTP request. Defaults to HEADERS.

    Raises:
        HTTPError: 4xx, client networking error
        ConnectionError: connection error with endpoint
        TimeOutError: time out error at endpoint
        RuntimeError: unexpected error

    Returns:
        object: JSON object of the HTTP response
    """
    try:
        logger.info("Sending HTTP request...")
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()
        logger.info("Received HTTP response")
        content = response.json()
        logger.debug(f"HTTP response from {url}: {content}")
        return content
        
    except requests.exceptions.HTTPError as http_err:
        logger.critical(f"HTTP error: {http_err}")
        # Rate limit
        if response.status_code == 429:
            logger.critical("Rate limit exceeded. Waiting before retrying...")
        raise

    except requests.exceptions.ConnectionError as conn_err:
        logger.critical(f"Connection error: {conn_err}")
        raise

    except requests.exceptions.Timeout as timeout_err:
        logger.critical(f"Timeout error: {timeout_err}")
        raise

    except requests.exceptions.RequestException as req_err:
        logger.critical(f"General Request error: {req_err}")
        raise
        
    except Exception as e:
        logger.critical(f"Error: {e}")
        raise RuntimeError(f"RuntimeError: {e}") from e