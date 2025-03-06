# =============================================================================
# Modules
# =============================================================================

# Python
import argparse
import os

# Third-party
import requests

# Custom
from custom_logger import get_custom_logger
from utils import get_api_url, get_http_response

# =============================================================================
# Variables
# =============================================================================

# Logging
logger = get_custom_logger("data/configurations/logger.yaml")

# Requests
HEADERS = {
"User-Agent": 
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}
DEFAULT_URL = "https://newsapi.org/v2/everything?q=tesla&from=2025-02-06&sortBy=publishedAt"

# =============================================================================
# Programme exectuion
# =============================================================================

if __name__ == "__main__":
    
    # =========================================================================
    # Argument parsing
    # =========================================================================

    parser = argparse.ArgumentParser(description="url from which to request API data")
    parser.add_argument("-u", "--url", type=str, required=False, help="url address")
    args = parser.parse_args()
    url = args.url
    
    # =========================================================================
    # Programme
    # =========================================================================
    
    # Logger entry
    logger.info(f"Sending daily news email...")
    
    # If no URL parsed
    if url is None:
        url = get_api_url(url=DEFAULT_URL)

    # Get content of HTTP response
    content = get_http_response(url=url, headers=HEADERS)
    
    #logger exit
    logger.info(f"Sent daily news email")