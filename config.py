"""
Configuration file for SSMS
Contains all configurable settings for the application
"""

import os
from pathlib import Path

# Application Information
APP_NAME = "Sales & Stock Management System"
APP_VERSION = "1.0.0"
APP_AUTHOR = "SSMS Team"

# Database Configuration
DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'SAh16ITU$530'),
    'database': os.getenv('DB_NAME', 'ssms_db'),
    'charset': 'utf8mb4',
    'connect_timeout': 10,
    'read_timeout': 30,
    'write_timeout': 30
}

# Application Settings
APP_SETTINGS = {
    'window_width': 1200,
    'window_height': 800,
    'theme': 'dark',  # 'dark' or 'light'
    'auto_refresh_interval': 30000,  # milliseconds
    'max_login_attempts': 3,
    'session_timeout': 3600,  # seconds
}

# UI Configuration
UI_CONFIG = {
    'primary_color': '#00C4B4',
    'secondary_color': '#2D3035',
    'background_color': '#1E2A44',
    'text_color': '#F5F7FA',
    'error_color': '#FF6B6B',
    'success_color': '#4CAF50',
    'warning_color': '#FF9800',
}

# File Paths
BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / 'logs'
REPORTS_DIR = BASE_DIR / 'reports'
BACKUP_DIR = BASE_DIR / 'backups'

# Create directories if they don't exist
for directory in [LOG_DIR, REPORTS_DIR, BACKUP_DIR]:
    directory.mkdir(exist_ok=True)

# Logging Configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': LOG_DIR / 'ssms.log',
    'max_size': 10 * 1024 * 1024,  # 10MB
    'backup_count': 5
}

# Security Settings
SECURITY_CONFIG = {
    'password_min_length': 6,
    'password_require_special': False,
    'session_encryption': True,
    'audit_logging': True
}

# Business Rules
BUSINESS_RULES = {
    'invoice_number_prefix': 'INV',
    'purchase_number_prefix': 'PUR',
    'credit_note_prefix': 'CN',
    'debit_note_prefix': 'DN',
    'default_tax_rate': 0.0,  # 0% default tax
    'low_stock_threshold': 10,
    'currency_symbol': '$',
    'date_format': '%Y-%m-%d',
    'datetime_format': '%Y-%m-%d %H:%M:%S'
}

def get_database_config():
    """Get database configuration"""
    return DATABASE_CONFIG.copy()

def get_app_settings():
    """Get application settings"""
    return APP_SETTINGS.copy()

def get_ui_config():
    """Get UI configuration"""
    return UI_CONFIG.copy()

def get_logging_config():
    """Get logging configuration"""
    return LOGGING_CONFIG.copy()

def get_security_config():
    """Get security configuration"""
    return SECURITY_CONFIG.copy()

def get_business_rules():
    """Get business rules"""
    return BUSINESS_RULES.copy()
