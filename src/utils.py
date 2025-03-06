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

# =============================================================================
# Functions
# =============================================================================

def get_env_var(env_var:str):
    """Import arument environment variables

    Args:
        env_var (str): environment variable to import

    Raises:
        ValueError: no ENV variable found

    Returns:
        str: imported environment variable
    """
    try:
        logger.info(f"Getting ENV variable {env_var}...")
        env_var_import = os.getenv(env_var)
        logger.info("Have ENV variable")
        logger.debug(f"ENV variable {env_var}: {env_var_import}")
        return env_var_import
            
    except ValueError as ve:
        logger.error(f"ValueError: {ve}")
        raise

    except Exception as e:
        logger.critical(f"Error: {e}")
        raise
    

def get_news_api_endpoint(api_key:str, topic="tesla") -> str:
    """Get URL which contains URL and API key to access endpoint URL

    Args:
        topic (str): string to give type of news from endpoint
        api_key (str): API key string to access endpoint of input URL

    Returns:
        str: augmented URL with API key
    """
    # Set news api endpoint constants
    BASE_URL = "https://newsapi.org/v2/everything?q="
    CONDITIONS_URL = "&from=2025-02-06&sortBy=publishedAt&language=en"
    try:
        endpoint = f"{BASE_URL}{topic}{CONDITIONS_URL}&apiKey={api_key}"
        logger.debug(f"Endpoint: {endpoint}")
        return endpoint

    except Exception as e:
        logger.critical(f"Error: {e}")
        raise
        

def get_http_response(url:str, headers:str={
    "User-Agent": 
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }) -> dict:
    """_Get HTTP response from endpoint and return JSON of response

    Args:
        url (str): URL of the endpoint to send HTTP request
        headers (str, optional): Headers for senfind HTTP request. Defaults to HEADERS.

    Raises:
        HTTPError: 4xx, client networking error
        ConnectionError: connection error with endpoint
        TimeOutError: time out error at endpoint
        RequestException: request error at endpoint

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
        logger.error(f"HTTP error: {http_err}")
        raise

    except requests.exceptions.ConnectionError as conn_err:
        logger.error(f"Connection error: {conn_err}")
        raise

    except requests.exceptions.Timeout as timeout_err:
        logger.error(f"Timeout error: {timeout_err}")
        raise

    except requests.exceptions.RequestException as req_err:
        logger.error(f"General Request error: {req_err}")
        raise
        
    except Exception as e:
        logger.critical(f"Error: {e}")
        raise
    
def get_article_title_description_link(content:dict, number_articles:int=20) -> str:
    """Get the title and description of the articles contained in the content dictionary

    Args:
        content (dict): Dictionary containing article title and description values
                        Expected structure:
                        {
                            "article": [
                                {
                                    "title": "Breaking News",
                                    "description": "This is the latest news update.",
                                    ...
                                },
                                ...
                            ],
                            ...
                        }
        number_articles (int): the first number of articles to include in message for SMTP email

    Returns:
        str: A formatted string of titles, descriptions, and links ready for parsing in an SMTP email

    Raises:
        ValueError: If required keys are missing
        TypeError: If values are not in the expected format
    """
    logger.info("Generating string with titles, descriptions, and urls of articles...")
    try:
        # Check if "article" key exists and is a list
        if "articles" not in content:
            raise ValueError("Key 'articles' is missing from argument")
        if not isinstance(content["articles"], list):
            raise TypeError("Value of 'articles' must be a list of dictionaries")

        articles = content["articles"][:number_articles]
        message = ""

        for i, article in enumerate(articles):
            # Check article is a dict
            if not isinstance(article, dict):
                raise TypeError("Each article must be a dictionary")
            # Check title, description, and url keys exist
            if "title" not in article or "description" not in article or "url" not in article:
                raise ValueError("Each article must contain 'title', 'description', and 'url' keys")
            # Do not add empty values to message
            if article["title"] is None and article["description"] is None and article["url"] is None:
                pass
            elif not isinstance(article["title"], str) or not isinstance(article["description"], str) or not isinstance(article["url"], str):
                raise TypeError("'title', 'description', 'url' must be strings.")
            else:
                message += f"[{i+1}]\nTitle: {article['title']}\nDescription: {article['description']}\nLink: {article['url']}\n\n"

        logger.info("Generated string with titles, descriptions, and urls of articles")
        return message.strip()

    except ValueError as e:
        logger.error(f"ValueError: {e}")
        raise
    
    except TypeError as e:
        logger.error(f"TypeError: {e}")
        raise
    
    except Exception as e:
        logger.critical(f"Error: {e}")
        raise 