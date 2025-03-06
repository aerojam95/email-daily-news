# **Email daily news**
Code sends an email via Gmail as a host to desired receiver with the latest news articles on a topic from [News API](https://newsapi.org/).

## Table of Contents
- [News API](#news-api)
    - [How to Get a News API Key](#get-news-api-key)
- [Email via Gmail](#email)
    - [How to Get a Gmail App Password](#gmail-password)
- [Code](#code)
    - [Python virtual environment](#python-venv)
    - [Environment variables](#env-var)
    - [Programme execution](#execution)
        - [Arguments](#arguments)
        - [Example](#example)

## News API
[News API](https://newsapi.org/) provides access to news articles from various sources. This programme fetches the latest articles based on a specified topic. Further doicumentation on constructing the API endpoint can be in the [documentation](https://newsapi.org/docs).

The default API endpoint used in the code base is: `https://newsapi.org/v2/everything?q=<TOPIC>&from=2025-02-06&sortBy=publishedAt&language=en&apiKey=<API_KEY>`

### How to Get a News API Key
1. Go to [News API](https://newsapi.org/)
2. Sign up for a free account
3. Navigate to the "API Keys" section and generate a key
4. Save this API key as an environment variable (`NEWS_API_KEY`)

## Email via Gmail
The programme works by using a SMTP protocol which uses a Gmail host and needs a Gmail app password to run the programme such that it emails the news articles to a receiver via a Gmail account.

### How to Get a Gmail App Password
1. Go to Google Account Security
2. Enable 2-Step Verification
2. Navigate to App passwords and generate one for "Mail"
4. Copy and save the password securely as an environment variable (`GMAIL_PASSWORD`)

## Code

The code retrieves and emails relevant news articles based on user-defined parameters. The code for this programme can be found in the directory: [src](src/).

### Python virtual environment

Before using the code it is best to setup and start a Python virtual environment in order to avoid potential package clashes using the [requirements](requirements.txt) file:

```
# Navigate into the data project directory

# Create a virtual environment
python3 -m venv email-daily-news

# Activate virtual environment
source email-daily-news/bin/activate

# Install dependencies for code
pip3 install -r requirements.txt

# When finished with virtual environment
deactivate
```


### Environment variables

Before running the script, set up these environment variables:

1. GMAIL_USERNAME: Your Gmail address (sender, i.e. the gmail address of the account for the Gmail app password)
2. GMAIL_PASSWORD: Your Gmail app password

If not using the full endpoint argument to the programme the following environment variable is needed too:

3. NEWS_API_KEY: Your API key from News API

Setting the environment variables:

```
export GMAIL_USERNAME="your_email@gmail.com"
export GMAIL_PASSWORD="your_app_password"
export NEWS_API_KEY="your_news_api_key" # if required
```


### Programme execution

Run the programme using:

```
python main.py [-e ENDPOINT] [-t TOPIC] [-n NUMBER_ARTICLES]

```

#### Arguments

- **`-e, --endpoint`** (optional): Manually specify the News API endpoint (e.g., `https://newsapi.org/v2/everything?q=tesla>&from=2025-02-06&sortBy=publishedAt&language=en&apiKey=<API_KEY>`)
- **`-t, --topic`** (optional): Specify a topic (e.g., *"tesla"*, *"climate"*)
- **`-n, --number_articles`** (optional): Number of articles to retrieve (default: **20**)

#### Example

This fetches the latest 5 news articles about technology and sends them via email:

```
python main.py -t "technology" -n 5
```