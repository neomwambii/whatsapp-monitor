import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import config

logger = logging.getLogger(__name__)

class EmailNotifier:
    def __init__(self):
        self.gmail_user = config.GMAIL_USER
        self.gmail_password = config.GMAIL_APP_PASSWORD
        self.notification_email = config.NOTIFICATION_EMAIL
        
    def send_approval_notification(self, original_message, group_name):
        """Send email notification when approval message is detected"""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.gmail_user
            msg['To'] = self.notification_email
            msg['Subject'] = f"🚀 DEPLOY APPROVAL DETECTED - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            
            # Email body
            body = f"""
            <html>
            <body>
                <h2>🎉 Deploy Approval Notification</h2>
                <p><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><strong>Group:</strong> {group_name}</p>
                <p><strong>Status:</strong> ✅ APPROVAL RECEIVED</p>
                
                <h3>Original Message:</h3>
                <div style="background-color: #f0f0f0; padding: 10px; border-left: 4px solid #4CAF50;">
                    <p><strong>"{original_message}"</strong></p>
                </div>
                
                <p><em>This notification was sent automatically by your WhatsApp monitoring system.</em></p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            # Send email
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.gmail_user, self.gmail_password)
            text = msg.as_string()
            server.sendmail(self.gmail_user, self.notification_email, text)
            server.quit()
            
            logger.info(f"Approval notification sent to {self.notification_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email notification: {str(e)}")
            return False
    
    def send_error_notification(self, error_message):
        """Send error notification if monitoring fails"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.gmail_user
            msg['To'] = self.notification_email
            msg['Subject'] = f"⚠️ WhatsApp Monitor Error - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            
            body = f"""
            <html>
            <body>
                <h2>⚠️ Monitoring System Error</h2>
                <p><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><strong>Error:</strong> {error_message}</p>
                <p><em>Please check the monitoring system logs.</em></p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.gmail_user, self.gmail_password)
            text = msg.as_string()
            server.sendmail(self.gmail_user, self.notification_email, text)
            server.quit()
            
            logger.info("Error notification sent")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send error notification: {str(e)}")
            return False
