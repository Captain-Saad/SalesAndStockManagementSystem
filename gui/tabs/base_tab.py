"""
Base Tab Class for SSMS
Provides common functionality for all tabs
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import pyqtSignal, QTimer
from PyQt6.QtGui import QFont
from db_connection import DatabaseConnection


class BaseTab(QWidget):
    """Base class for all SSMS tabs"""
    
    # Signals
    data_updated = pyqtSignal()
    error_occurred = pyqtSignal(str)
    
    def __init__(self, title, description, user_data):
        super().__init__()
        self.title = title
        self.description = description
        self.user_data = user_data
        self.db = DatabaseConnection()
        self.setup_ui()
        
    def setup_ui(self):
        """Setup base UI structure"""
        # Set background to match main UI theme
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #1e293b, stop:1 #334155);
                color: #f8fafc;
            }
        """)
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(50, 40, 50, 40)
        self.main_layout.setSpacing(35)
        
        # Header
        self.create_header()
        
        # Content area (to be implemented by subclasses)
        self.create_content()
        
    def create_header(self):
        """Create tab header"""
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 20)
        header_layout.setSpacing(12)
        
        # Title
        title_label = QLabel(self.title)
        title_label.setStyleSheet("""
            QLabel {
                color: #f8fafc;
                font-size: 36px;
                font-weight: 700;
                margin-bottom: 12px;
            }
        """)
        header_layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel(self.description)
        desc_label.setStyleSheet("""
            QLabel {
                color: #cbd5e1;
                font-size: 18px;
                font-weight: 400;
            }
        """)
        header_layout.addWidget(desc_label)
        
        self.main_layout.addWidget(header_widget)
        
    def create_content(self):
        """Create content area - to be overridden by subclasses"""
        pass
        
    def refresh_data(self):
        """Refresh tab data - to be overridden by subclasses"""
        pass
        
    def show_error(self, message):
        """Show error message"""
        self.error_occurred.emit(message)
        
    def show_success(self, message):
        """Show success message"""
        # This could be implemented with a notification system
        print(f"✅ {message}")
        
    def get_database_connection(self):
        """Get database connection"""
        return self.db
        
    def execute_query(self, query, params=None):
        """Execute database query"""
        try:
            return self.db.execute_query(query, params)
        except Exception as e:
            self.show_error(f"Database error: {str(e)}")
            return None
