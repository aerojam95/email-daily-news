# =============================================================================
# Modules
# =============================================================================

# Python
from email.message import EmailMessage
import re
import smtplib
import ssl

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

def format_gmail_message(subject:str, sender:str, receiver:str, message:str):
    """Create an Gmail message object reader to be sent as an email

    Args:
        subject (str): subject of email to be sent
        sender (str): Gmail address of sender 
        receiver (str): Gmail address of receiver
        message (str): Message content of email 

    Returns:
        object: EmailMessage object read for sending 
    """
    # Check valid gmail email addresses
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    assert re.match(pattern, sender), f"Invalid sender Gmail address: {sender}"
    assert re.match(pattern, receiver), f"Invalid sender Gmail address: {receiver}"
    
    # Logger function entry
    logger.info(f"Creating EmailMessage object...")
    
    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = receiver
        msg.set_content(message)
        logger.debug(f"EmailMessage object: {msg}")
        logger.info(f"Created EmailMessage object")
        return msg
    
    except Exception as e:
        logger.critical(f"Error: an unexpected error occurred: {e}")
        raise RuntimeError(
            f"RuntimeError: unexpected error occurred in format_gmail_message: {e}"
        ) from e

def send_gmail_from_ppw(username:str, password:str, message:str, host:str="smtp.gmail.com", port:int=465):
    """The function sends an email message from the sender to the receiver by SMTP gmail and SSL

    Args:
        username (str): Gmail address of sender
        password(str): password of sender Gmail address
        message (str): messgae to be emailed
        host (str, optional): host for SMTP server. Defaults to "smtp.gmail.com".
        port (int, optional): port for SMTP server. Defaults to 465.
    """
    # Check valid gmail email addresses
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    assert re.match(pattern, username), f"Invalid sender Gmail address: {username}"
    
    # Logger function entry
    logger.info(f"Sending email...")
    
    try:
        logger.info(f"Creating SSL context...")
        context = ssl.create_default_context()
        logger.debug(f"SSL context: {context}")
        logger.info(f"Createed SSL context")
        
    except ssl.SSLError as se:
        logger.critical(f"SSL error: encountered when created SSL context: {se}")
        raise
    
    except Exception as e:
        logger.critical(f"Error: an unexpected error occurred: {e}")
        raise RuntimeError(
            f"RuntimeError: unexpected error occurred in send_gmail_from_ppw: {e}"
        ) from e

    try:
        logger.info(f"Starting SMTP server {host}:{port}...")
        with smtplib.SMTP_SSL(host, port, context=context) as server:
            server.login(username, password)
            server.send_message(message)
            logger.info(f"Email sent")
    except smtplib.SMTPAuthenticationError as eauth:
        logger.critical(f"SMTPAuthenticationError: authentication failed. Check your username and password: {eauth}")
        raise
    except smtplib.SMTPConnectError as econn:
        logger.critical(f"SMTPConnectError: unable to connect to SMTP server {host}:{port}: {econn}")
        raise
    except smtplib.SMTPException as esmtp:
        logger.critical(f"SMTPException: SMTP error occurred: {esmtp}")
        raise
    except Exception as e:
        logger.critical(f"Error: an unexpected error occurred: {e}")
        raise RuntimeError(
            f"RuntimeError: unexpected error occurred in send_gmail_from_ppw: {e}"
        ) from e