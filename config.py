import os
from dotenv import load_dotenv

load_dotenv()

# WhatsApp Configuration
WHATSAPP_GROUP_NAME = os.getenv("WHATSAPP_GROUP_NAME", "Paris group 2")
TARGET_MESSAGE = "good news: we have approval from sbib and liberty for tonights deploy"

# Email Configuration
GMAIL_USER = os.getenv("GMAIL_USER", "neomwabii@gmail.com")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "iwbk muwz pdgw jptq")
NOTIFICATION_EMAIL = os.getenv("NOTIFICATION_EMAIL", "neomwabii@gmail.com")

# Azure Configuration
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING", "")

# Monitoring Configuration
CHECK_INTERVAL_MINUTES = 5  # Check every 5 minutes when active
MAX_RETRIES = 3
TIMEOUT_SECONDS = 30
