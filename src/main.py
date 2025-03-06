# =============================================================================
# Modules
# =============================================================================

# Python
import argparse

# Custom
from custom_logger import get_custom_logger
from send_email import format_gmail_message, send_gmail_from_ppw
from utils import get_env_var, get_news_api_endpoint, get_http_response, get_article_title_description_link

# =============================================================================
# Variables
# =============================================================================

# Logging
logger = get_custom_logger("data/configurations/logger.yaml")

# SMTP email elements
SUBJECT = "Daily news email"
BASE_MESSAGE = "To whom it may concern,\n\n Please find below the titles and descriptions of articles from the news that are of interest to you:\n\n"

# =============================================================================
# Programme exectuion
# =============================================================================

if __name__ == "__main__":
    
    # Parsed values
    parser = argparse.ArgumentParser(description="endpoint from which to request API data")
    parser.add_argument("-e", "--endpoint", type=str, required=False, help="endpoint URL address")
    parser.add_argument("-t", "--topic", type=str, required=False, help="topic of news to be sent")
    parser.add_argument("-n", "--number_articles", type=int, required=False, help="number of articles to be emailed")
    args = parser.parse_args()
    endpoint = args.endpoint
    topic = args.topic
    number_articles = args.number_articles
    
    # Get ENV vars
    username = get_env_var("GMAIL_USERNAME")
    password = get_env_var("GMAIL_PASSWORD")
    
    # If no URL or topic parsed
    if endpoint is None:
        api_key = get_env_var("NEWS_API_KEY")
        if topic is not None:
            endpoint = get_news_api_endpoint(api_key=api_key, topic=topic)
        else:
            endpoint = get_news_api_endpoint(api_key=api_key)

    # Get content of HTTP response
    content = get_http_response(url=endpoint)
    # If no number_articles parsed
    if number_articles is not None:
        raw_message = f"{BASE_MESSAGE}{get_article_title_description_link(content=content, number_articles=number_articles)}"
    else:
        raw_message = f"{BASE_MESSAGE}{get_article_title_description_link(content=content)}"
    
    # Email
    if raw_message != BASE_MESSAGE:
        logger.info(f"Sending news articles email...")
        message = format_gmail_message(subject=SUBJECT, sender=username, receiver=username,message=raw_message )
        send_gmail_from_ppw(username=username, password=password, message=message)
        logger.info(f"Sent news articles email")
    else:
        logger.info(f"No news articles to send in email")