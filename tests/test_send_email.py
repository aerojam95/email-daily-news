# =============================================================================
# Modules
# =============================================================================

# Python modules
from email.message import EmailMessage
import smtplib
import ssl
import unittest
from unittest.mock import patch, MagicMock

# Third-party modules
import yaml

# Testing module
from send_email import format_gmail_message, send_gmail_from_ppw

# =============================================================================
# Tests
# =============================================================================

class TestFormatGmailMessage(unittest.TestCase):
    
    def test_valid_email_message(self):
        """Test creating a valid Gmail message object."""
        subject = "Test Subject"
        sender = "valid_sender@gmail.com"
        receiver = "valid_receiver@gmail.com"
        message = "This is a test email."
        
        msg = format_gmail_message(subject, sender, receiver, message)
        
        self.assertIsInstance(msg, EmailMessage)
        self.assertEqual(msg["Subject"], subject)
        self.assertEqual(msg["From"], sender)
        self.assertEqual(msg["To"], receiver)
        self.assertEqual(msg.get_content().strip(), message)

    def test_invalid_sender_email(self):
        """Test invalid sender email raises an assertion error."""
        with self.assertRaises(AssertionError):
            format_gmail_message("Test", "invalid_email", "receiver@gmail.com", "Message")

    def test_invalid_receiver_email(self):
        """Test invalid receiver email raises an assertion error."""
        with self.assertRaises(AssertionError):
            format_gmail_message("Test", "sender@gmail.com", "invalid_email", "Message")

class TestSendGmailFromPPW(unittest.TestCase):

    @patch("send_email.smtplib.SMTP_SSL")
    @patch("send_email.ssl.create_default_context")
    def test_send_email_success(self, mock_ssl_context, mock_smtp):
        """Test sending an email successfully with mocked SMTP."""
        mock_ssl_context.return_value = MagicMock()
        mock_server = mock_smtp.return_value.__enter__.return_value
        mock_server.login.return_value = None
        mock_server.send_message.return_value = None
        
        username = "valid_sender@gmail.com"
        password = "password"
        message = format_gmail_message("Test Subject", username, "valid_receiver@gmail.com", "Message")
        
        try:
            send_gmail_from_ppw(username, password, message)
        except Exception as e:
            self.fail(f"send_gmail_from_ppw raised an unexpected exception: {e}")

        mock_smtp.assert_called_once_with("smtp.gmail.com", 465, context=mock_ssl_context.return_value)
        mock_server.login.assert_called_once_with(username, password)
        mock_server.send_message.assert_called_once_with(message)

    def test_invalid_email_raises_assertion(self):
        """Test sending email with invalid username raises an assertion error."""
        with self.assertRaises(AssertionError):
            send_gmail_from_ppw("invalid_email", "password", "Message")

    @patch("send_email.smtplib.SMTP_SSL")
    @patch("send_email.ssl.create_default_context")
    def test_authentication_error(self, mock_ssl_context, mock_smtp):
        """Test SMTP authentication failure handling."""
        mock_ssl_context.return_value = MagicMock()
        mock_server = mock_smtp.return_value.__enter__.return_value
        mock_server.login.side_effect = smtplib.SMTPAuthenticationError(535, "Authentication failed")
        
        username = "valid_sender@gmail.com"
        password = "wrong_password"
        message = format_gmail_message("Test Subject", username, "valid_receiver@gmail.com", "Message")

        with self.assertRaises(smtplib.SMTPAuthenticationError):
            send_gmail_from_ppw(username, password, message)

    @patch("send_email.smtplib.SMTP_SSL")
    @patch("send_email.ssl.create_default_context")
    def test_connection_error(self, mock_ssl_context, mock_smtp):
        """Test SMTP connection failure handling."""
        mock_ssl_context.return_value = MagicMock()
        mock_smtp.side_effect = smtplib.SMTPConnectError(421, "Connection failed")

        username = "valid_sender@gmail.com"
        password = "password"
        message = format_gmail_message("Test Subject", username, "valid_receiver@gmail.com", "Message")

        with self.assertRaises(smtplib.SMTPConnectError):
            send_gmail_from_ppw(username, password, message)
            
    @patch("send_email.smtplib.SMTP_SSL")
    @patch("send_email.ssl.create_default_context")
    def test_smtp_exception(self, mock_ssl_context, mock_smtp):
        """Test handling of a general SMTPException."""
        mock_ssl_context.return_value = MagicMock()
        mock_server = mock_smtp.return_value.__enter__.return_value
        mock_server.send_message.side_effect = smtplib.SMTPException("SMTP error occurred")

        username = "valid_sender@gmail.com"
        password = "password"
        message = format_gmail_message("Test Subject", username, "valid_receiver@gmail.com", "Message")

        with self.assertRaises(smtplib.SMTPException):
            send_gmail_from_ppw(username, password, message)

if __name__ == "__main__":
    unittest.main()