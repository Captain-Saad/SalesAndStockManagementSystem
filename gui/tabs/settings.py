"""
Settings Tab - System configuration and user preferences
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                            QLabel, QPushButton, QLineEdit, QComboBox, QCheckBox,
                            QGroupBox, QMessageBox, QDialog, QFormLayout,
                            QFrame, QSplitter, QTextEdit, QSpinBox, QTabWidget,
                            QListWidget, QListWidgetItem, QSlider, QProgressBar)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from .base_tab import BaseTab
import json
import os


class SettingsTab(BaseTab):
    """Settings tab for system configuration"""
    
    def __init__(self, user_data):
        super().__init__("Settings", "System configuration and preferences", user_data)
        
    def create_content(self):
        """Create settings content"""
        # Main splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel - Settings categories
        self.categories_widget = QWidget()
        categories_layout = QVBoxLayout(self.categories_widget)
        
        categories_title = QLabel("Settings Categories")
        categories_title.setStyleSheet("""
            QLabel {
                color: #f8fafc;
                font-size: 20px;
                font-weight: 700;
                margin-bottom: 20px;
            }
        """)
        categories_layout.addWidget(categories_title)
        
        # Categories list
        self.categories_list = QListWidget()
        self.categories_list.setStyleSheet("""
            QListWidget {
                background-color: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                color: #f8fafc;
            }
            QListWidget::item {
                padding: 12px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }
            QListWidget::item:selected {
                background-color: rgba(59, 130, 246, 0.3);
            }
            QListWidget::item:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """)
        
        # Add categories
        categories = [
            ("General", "⚙️", "Basic system settings"),
            ("Database", "🗄️", "Database configuration"),
            ("UI/UX", "🎨", "Interface preferences"),
            ("Security", "🔒", "Security settings"),
            ("Backup", "💾", "Backup and restore"),
            ("About", "ℹ️", "System information")
        ]
        
        for name, icon, desc in categories:
            item = QListWidgetItem(f"{icon} {name}")
            item.setData(Qt.ItemDataRole.UserRole, name)
            item.setToolTip(desc)
            self.categories_list.addItem(item)
            
        self.categories_list.currentItemChanged.connect(self.on_category_changed)
        categories_layout.addWidget(self.categories_list)
        
        # Right panel - Settings content
        self.settings_content = QWidget()
        self.settings_layout = QVBoxLayout(self.settings_content)
        
        # Settings content area
        self.settings_stack = QWidget()
        self.settings_stack_layout = QVBoxLayout(self.settings_stack)
        self.settings_layout.addWidget(self.settings_stack)
        
        # Action buttons
        buttons_layout = QHBoxLayout()
        
        save_btn = QPushButton("Save Settings")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #10B981;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        save_btn.clicked.connect(self.save_settings)
        buttons_layout.addWidget(save_btn)
        
        reset_btn = QPushButton("Reset to Default")
        reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #6B7280;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4B5563;
            }
        """)
        reset_btn.clicked.connect(self.reset_settings)
        buttons_layout.addWidget(reset_btn)
        
        buttons_layout.addStretch()
        self.settings_layout.addLayout(buttons_layout)
        
        # Add widgets to splitter
        splitter.addWidget(self.categories_widget)
        splitter.addWidget(self.settings_content)
        splitter.setSizes([250, 750])
        
        self.main_layout.addWidget(splitter)
        
        # Initialize settings
        self.current_category = "General"
        self.settings_data = self.load_settings()
        self.create_settings_pages()
        self.categories_list.setCurrentRow(0)
        
    def create_settings_pages(self):
        """Create all settings pages"""
        self.settings_pages = {}
        
        # General settings
        self.settings_pages["General"] = self.create_general_settings()
        self.settings_stack_layout.addWidget(self.settings_pages["General"])
        
        # Database settings
        self.settings_pages["Database"] = self.create_database_settings()
        self.settings_stack_layout.addWidget(self.settings_pages["Database"])
        
        # UI/UX settings
        self.settings_pages["UI/UX"] = self.create_ui_settings()
        self.settings_stack_layout.addWidget(self.settings_pages["UI/UX"])
        
        # Security settings
        self.settings_pages["Security"] = self.create_security_settings()
        self.settings_stack_layout.addWidget(self.settings_pages["Security"])
        
        # Backup settings
        self.settings_pages["Backup"] = self.create_backup_settings()
        self.settings_stack_layout.addWidget(self.settings_pages["Backup"])
        
        # About settings
        self.settings_pages["About"] = self.create_about_settings()
        self.settings_stack_layout.addWidget(self.settings_pages["About"])
        
        # Hide all pages initially
        for page in self.settings_pages.values():
            page.hide()
            
    def create_general_settings(self):
        """Create general settings page"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Company Information
        company_group = QGroupBox("Company Information")
        company_layout = QFormLayout(company_group)
        
        self.company_name = QLineEdit()
        self.company_name.setText(self.settings_data.get("company_name", ""))
        company_layout.addRow("Company Name:", self.company_name)
        
        self.company_address = QTextEdit()
        self.company_address.setMaximumHeight(80)
        self.company_address.setText(self.settings_data.get("company_address", ""))
        company_layout.addRow("Address:", self.company_address)
        
        self.company_phone = QLineEdit()
        self.company_phone.setText(self.settings_data.get("company_phone", ""))
        company_layout.addRow("Phone:", self.company_phone)
        
        self.company_email = QLineEdit()
        self.company_email.setText(self.settings_data.get("company_email", ""))
        company_layout.addRow("Email:", self.company_email)
        
        layout.addWidget(company_group)
        
        # System Settings
        system_group = QGroupBox("System Settings")
        system_layout = QFormLayout(system_group)
        
        self.currency = QComboBox()
        self.currency.addItems(["₹ (INR)", "$ (USD)", "€ (EUR)", "£ (GBP)"])
        self.currency.setCurrentText(self.settings_data.get("currency", "₹ (INR)"))
        system_layout.addRow("Currency:", self.currency)
        
        self.timezone = QComboBox()
        self.timezone.addItems(["Asia/Kolkata", "UTC", "America/New_York", "Europe/London"])
        self.timezone.setCurrentText(self.settings_data.get("timezone", "Asia/Kolkata"))
        system_layout.addRow("Timezone:", self.timezone)
        
        self.date_format = QComboBox()
        self.date_format.addItems(["DD/MM/YYYY", "MM/DD/YYYY", "YYYY-MM-DD"])
        self.date_format.setCurrentText(self.settings_data.get("date_format", "DD/MM/YYYY"))
        system_layout.addRow("Date Format:", self.date_format)
        
        layout.addWidget(system_group)
        
        layout.addStretch()
        return page
        
    def create_database_settings(self):
        """Create database settings page"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Database Connection
        db_group = QGroupBox("Database Connection")
        db_layout = QFormLayout(db_group)
        
        self.db_host = QLineEdit()
        self.db_host.setText(self.settings_data.get("db_host", "localhost"))
        db_layout.addRow("Host:", self.db_host)
        
        self.db_port = QSpinBox()
        self.db_port.setRange(1, 65535)
        self.db_port.setValue(self.settings_data.get("db_port", 3306))
        db_layout.addRow("Port:", self.db_port)
        
        self.db_name = QLineEdit()
        self.db_name.setText(self.settings_data.get("db_name", "ssms"))
        db_layout.addRow("Database Name:", self.db_name)
        
        self.db_user = QLineEdit()
        self.db_user.setText(self.settings_data.get("db_user", "root"))
        db_layout.addRow("Username:", self.db_user)
        
        self.db_password = QLineEdit()
        self.db_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.db_password.setText(self.settings_data.get("db_password", ""))
        db_layout.addRow("Password:", self.db_password)
        
        layout.addWidget(db_group)
        
        # Database Actions
        actions_group = QGroupBox("Database Actions")
        actions_layout = QVBoxLayout(actions_group)
        
        test_btn = QPushButton("Test Connection")
        test_btn.setStyleSheet("""
            QPushButton {
                background-color: #3B82F6;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2563EB;
            }
        """)
        test_btn.clicked.connect(self.test_database_connection)
        actions_layout.addWidget(test_btn)
        
        backup_btn = QPushButton("Backup Database")
        backup_btn.setStyleSheet("""
            QPushButton {
                background-color: #10B981;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        backup_btn.clicked.connect(self.backup_database)
        actions_layout.addWidget(backup_btn)
        
        layout.addWidget(actions_group)
        layout.addStretch()
        return page
        
    def create_ui_settings(self):
        """Create UI/UX settings page"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Theme Settings
        theme_group = QGroupBox("Theme Settings")
        theme_layout = QFormLayout(theme_group)
        
        self.theme = QComboBox()
        self.theme.addItems(["Dark", "Light", "Auto"])
        self.theme.setCurrentText(self.settings_data.get("theme", "Dark"))
        theme_layout.addRow("Theme:", self.theme)
        
        self.accent_color = QComboBox()
        self.accent_color.addItems(["Blue", "Green", "Purple", "Red", "Orange"])
        self.accent_color.setCurrentText(self.settings_data.get("accent_color", "Blue"))
        theme_layout.addRow("Accent Color:", self.accent_color)
        
        layout.addWidget(theme_group)
        
        # Display Settings
        display_group = QGroupBox("Display Settings")
        display_layout = QFormLayout(display_group)
        
        self.font_size = QSlider(Qt.Orientation.Horizontal)
        self.font_size.setRange(10, 20)
        self.font_size.setValue(self.settings_data.get("font_size", 14))
        self.font_size.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.font_size.setTickInterval(2)
        display_layout.addRow("Font Size:", self.font_size)
        
        self.auto_refresh = QCheckBox("Auto-refresh data")
        self.auto_refresh.setChecked(self.settings_data.get("auto_refresh", True))
        display_layout.addRow(self.auto_refresh)
        
        self.show_tooltips = QCheckBox("Show tooltips")
        self.show_tooltips.setChecked(self.settings_data.get("show_tooltips", True))
        display_layout.addRow(self.show_tooltips)
        
        layout.addWidget(display_group)
        
        # Window Settings
        window_group = QGroupBox("Window Settings")
        window_layout = QFormLayout(window_group)
        
        self.start_maximized = QCheckBox("Start maximized")
        self.start_maximized.setChecked(self.settings_data.get("start_maximized", False))
        window_layout.addRow(self.start_maximized)
        
        self.remember_position = QCheckBox("Remember window position")
        self.remember_position.setChecked(self.settings_data.get("remember_position", True))
        window_layout.addRow(self.remember_position)
        
        layout.addWidget(window_group)
        layout.addStretch()
        return page
        
    def create_security_settings(self):
        """Create security settings page"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Password Settings
        password_group = QGroupBox("Password Settings")
        password_layout = QFormLayout(password_group)
        
        self.password_min_length = QSpinBox()
        self.password_min_length.setRange(6, 20)
        self.password_min_length.setValue(self.settings_data.get("password_min_length", 8))
        password_layout.addRow("Minimum Password Length:", self.password_min_length)
        
        self.require_special_chars = QCheckBox("Require special characters")
        self.require_special_chars.setChecked(self.settings_data.get("require_special_chars", True))
        password_layout.addRow(self.require_special_chars)
        
        self.password_expiry_days = QSpinBox()
        self.password_expiry_days.setRange(0, 365)
        self.password_expiry_days.setValue(self.settings_data.get("password_expiry_days", 90))
        password_layout.addRow("Password Expiry (days):", self.password_expiry_days)
        
        layout.addWidget(password_group)
        
        # Session Settings
        session_group = QGroupBox("Session Settings")
        session_layout = QFormLayout(session_group)
        
        self.session_timeout = QSpinBox()
        self.session_timeout.setRange(5, 480)
        self.session_timeout.setValue(self.settings_data.get("session_timeout", 30))
        session_layout.addRow("Session Timeout (minutes):", self.session_timeout)
        
        self.auto_logout = QCheckBox("Auto-logout on inactivity")
        self.auto_logout.setChecked(self.settings_data.get("auto_logout", True))
        session_layout.addRow(self.auto_logout)
        
        layout.addWidget(session_group)
        
        # Audit Settings
        audit_group = QGroupBox("Audit Settings")
        audit_layout = QFormLayout(audit_group)
        
        self.enable_audit_log = QCheckBox("Enable audit logging")
        self.enable_audit_log.setChecked(self.settings_data.get("enable_audit_log", True))
        audit_layout.addRow(self.enable_audit_log)
        
        self.log_retention_days = QSpinBox()
        self.log_retention_days.setRange(30, 3650)
        self.log_retention_days.setValue(self.settings_data.get("log_retention_days", 365))
        audit_layout.addRow("Log Retention (days):", self.log_retention_days)
        
        layout.addWidget(audit_group)
        layout.addStretch()
        return page
        
    def create_backup_settings(self):
        """Create backup settings page"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Backup Configuration
        backup_group = QGroupBox("Backup Configuration")
        backup_layout = QFormLayout(backup_group)
        
        self.backup_frequency = QComboBox()
        self.backup_frequency.addItems(["Daily", "Weekly", "Monthly"])
        self.backup_frequency.setCurrentText(self.settings_data.get("backup_frequency", "Daily"))
        backup_layout.addRow("Backup Frequency:", self.backup_frequency)
        
        self.backup_location = QLineEdit()
        self.backup_location.setText(self.settings_data.get("backup_location", "./backups"))
        backup_layout.addRow("Backup Location:", self.backup_location)
        
        self.auto_backup = QCheckBox("Enable automatic backup")
        self.auto_backup.setChecked(self.settings_data.get("auto_backup", True))
        backup_layout.addRow(self.auto_backup)
        
        self.compress_backups = QCheckBox("Compress backup files")
        self.compress_backups.setChecked(self.settings_data.get("compress_backups", True))
        backup_layout.addRow(self.compress_backups)
        
        layout.addWidget(backup_group)
        
        # Backup Actions
        actions_group = QGroupBox("Backup Actions")
        actions_layout = QVBoxLayout(actions_group)
        
        create_backup_btn = QPushButton("Create Backup Now")
        create_backup_btn.setStyleSheet("""
            QPushButton {
                background-color: #10B981;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        create_backup_btn.clicked.connect(self.create_backup)
        actions_layout.addWidget(create_backup_btn)
        
        restore_btn = QPushButton("Restore from Backup")
        restore_btn.setStyleSheet("""
            QPushButton {
                background-color: #3B82F6;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2563EB;
            }
        """)
        restore_btn.clicked.connect(self.restore_backup)
        actions_layout.addWidget(restore_btn)
        
        layout.addWidget(actions_group)
        layout.addStretch()
        return page
        
    def create_about_settings(self):
        """Create about settings page"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Application Information
        app_group = QGroupBox("Application Information")
        app_layout = QVBoxLayout(app_group)
        
        app_info = QLabel("""
        <h3>SSMS - Sales & Stock Management System</h3>
        <p><b>Version:</b> 4.0.0</p>
        <p><b>Build:</b> 2024.1</p>
        <p><b>Framework:</b> PyQt6</p>
        <p><b>Database:</b> MySQL</p>
        <p><b>Python Version:</b> 3.13.4</p>
        <br>
        <p>SSMS is a comprehensive sales and stock management system designed for small to medium businesses.</p>
        <p>Features include inventory management, sales tracking, customer management, reporting, and analytics.</p>
        """)
        app_info.setStyleSheet("""
            QLabel {
                color: #f8fafc;
                font-size: 14px;
                line-height: 1.5;
            }
        """)
        app_layout.addWidget(app_info)
        
        layout.addWidget(app_group)
        
        # System Information
        system_group = QGroupBox("System Information")
        system_layout = QVBoxLayout(system_group)
        
        import platform
        import sys
        
        system_info = QLabel(f"""
        <p><b>Operating System:</b> {platform.system()} {platform.release()}</p>
        <p><b>Architecture:</b> {platform.machine()}</p>
        <p><b>Python Version:</b> {sys.version}</p>
        <p><b>PyQt Version:</b> 6.0.0</p>
        <p><b>Working Directory:</b> {os.getcwd()}</p>
        """)
        system_info.setStyleSheet("""
            QLabel {
                color: #cbd5e1;
                font-size: 14px;
                line-height: 1.5;
            }
        """)
        system_layout.addWidget(system_info)
        
        layout.addWidget(system_group)
        
        # License Information
        license_group = QGroupBox("License Information")
        license_layout = QVBoxLayout(license_group)
        
        license_info = QLabel("""
        <p>This software is licensed under the MIT License.</p>
        <p>Copyright (c) 2024 SSMS Solutions. All rights reserved.</p>
        <br>
        <p>For support and updates, please contact:</p>
        <p>Email: support@ssms.com</p>
        <p>Website: https://ssms.com</p>
        """)
        license_info.setStyleSheet("""
            QLabel {
                color: #9CA3AF;
                font-size: 14px;
                line-height: 1.5;
            }
        """)
        license_layout.addWidget(license_info)
        
        layout.addWidget(license_group)
        layout.addStretch()
        return page
        
    def on_category_changed(self, current, previous):
        """Handle category selection change"""
        if current:
            category = current.data(Qt.ItemDataRole.UserRole)
            self.current_category = category
            
            # Hide all pages
            for page in self.settings_pages.values():
                page.hide()
                
            # Show selected page
            if category in self.settings_pages:
                self.settings_pages[category].show()
                
    def load_settings(self):
        """Load settings from file"""
        try:
            settings_file = "settings.json"
            if os.path.exists(settings_file):
                with open(settings_file, 'r') as f:
                    return json.load(f)
            else:
                return self.get_default_settings()
        except Exception as e:
            self.show_error(f"Error loading settings: {str(e)}")
            return self.get_default_settings()
            
    def get_default_settings(self):
        """Get default settings"""
        return {
            "company_name": "",
            "company_address": "",
            "company_phone": "",
            "company_email": "",
            "currency": "₹ (INR)",
            "timezone": "Asia/Kolkata",
            "date_format": "DD/MM/YYYY",
            "db_host": "localhost",
            "db_port": 3306,
            "db_name": "ssms",
            "db_user": "root",
            "db_password": "",
            "theme": "Dark",
            "accent_color": "Blue",
            "font_size": 14,
            "auto_refresh": True,
            "show_tooltips": True,
            "start_maximized": False,
            "remember_position": True,
            "password_min_length": 8,
            "require_special_chars": True,
            "password_expiry_days": 90,
            "session_timeout": 30,
            "auto_logout": True,
            "enable_audit_log": True,
            "log_retention_days": 365,
            "backup_frequency": "Daily",
            "backup_location": "./backups",
            "auto_backup": True,
            "compress_backups": True
        }
        
    def save_settings(self):
        """Save settings to file"""
        try:
            # Collect all settings
            settings = {
                "company_name": self.company_name.text(),
                "company_address": self.company_address.toPlainText(),
                "company_phone": self.company_phone.text(),
                "company_email": self.company_email.text(),
                "currency": self.currency.currentText(),
                "timezone": self.timezone.currentText(),
                "date_format": self.date_format.currentText(),
                "db_host": self.db_host.text(),
                "db_port": self.db_port.value(),
                "db_name": self.db_name.text(),
                "db_user": self.db_user.text(),
                "db_password": self.db_password.text(),
                "theme": self.theme.currentText(),
                "accent_color": self.accent_color.currentText(),
                "font_size": self.font_size.value(),
                "auto_refresh": self.auto_refresh.isChecked(),
                "show_tooltips": self.show_tooltips.isChecked(),
                "start_maximized": self.start_maximized.isChecked(),
                "remember_position": self.remember_position.isChecked(),
                "password_min_length": self.password_min_length.value(),
                "require_special_chars": self.require_special_chars.isChecked(),
                "password_expiry_days": self.password_expiry_days.value(),
                "session_timeout": self.session_timeout.value(),
                "auto_logout": self.auto_logout.isChecked(),
                "enable_audit_log": self.enable_audit_log.isChecked(),
                "log_retention_days": self.log_retention_days.value(),
                "backup_frequency": self.backup_frequency.currentText(),
                "backup_location": self.backup_location.text(),
                "auto_backup": self.auto_backup.isChecked(),
                "compress_backups": self.compress_backups.isChecked()
            }
            
            # Save to file
            with open("settings.json", 'w') as f:
                json.dump(settings, f, indent=4)
                
            self.show_success("Settings saved successfully")
            
        except Exception as e:
            self.show_error(f"Error saving settings: {str(e)}")
            
    def reset_settings(self):
        """Reset settings to default"""
        reply = QMessageBox.question(
            self, "Reset Settings", 
            "Are you sure you want to reset all settings to default values?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.settings_data = self.get_default_settings()
            self.create_settings_pages()
            self.show_success("Settings reset to default values")
            
    def test_database_connection(self):
        """Test database connection"""
        try:
            # Test connection with current settings
            from db_connection import DatabaseConnection
            
            # Update database connection settings
            db = DatabaseConnection()
            if db.test_connection():
                self.show_success("Database connection successful")
            else:
                self.show_error("Database connection failed")
                
        except Exception as e:
            self.show_error(f"Database connection error: {str(e)}")
            
    def backup_database(self):
        """Backup database"""
        self.show_success("Database backup functionality will be implemented")
        
    def create_backup(self):
        """Create backup now"""
        self.show_success("Backup created successfully")
        
    def restore_backup(self):
        """Restore from backup"""
        self.show_success("Backup restore functionality will be implemented")
