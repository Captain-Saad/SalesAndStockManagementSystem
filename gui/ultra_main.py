"""
Ultra-Modern Main Window with PyQt6
Beautiful dashboard with animations and modern design
"""

import sys
import os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db_connection import DatabaseConnection


class ModernSidebar(QWidget):
    """Modern sidebar with navigation"""
    page_changed = pyqtSignal(str)
    
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.current_page = "dashboard"
        self.setup_ui()
        
    def setup_ui(self):
        """Setup sidebar UI"""
        self.setFixedWidth(280)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #1F2937, stop:1 #111827);
                border-right: 1px solid #374151;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        self.create_header(layout)
        
        # Navigation
        self.create_navigation(layout)
        
        # User info
        self.create_user_section(layout)
        
    def create_header(self, parent_layout):
        """Create header section"""
        header = QWidget()
        header.setStyleSheet("background: transparent;")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(24, 32, 24, 32)
        header_layout.setSpacing(8)
        
        # Logo
        logo = QLabel("SSMS")
        logo.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 28px;
                font-weight: 900;
                letter-spacing: -1px;
            }
        """)
        header_layout.addWidget(logo)
        
        # Subtitle
        subtitle = QLabel("Management System")
        subtitle.setStyleSheet("""
            QLabel {
                color: #9CA3AF;
                font-size: 14px;
                font-weight: 400;
            }
        """)
        header_layout.addWidget(subtitle)
        
        parent_layout.addWidget(header)
        
    def create_navigation(self, parent_layout):
        """Create navigation menu"""
        nav_container = QWidget()
        nav_container.setStyleSheet("background: transparent;")
        nav_layout = QVBoxLayout(nav_container)
        nav_layout.setContentsMargins(16, 0, 16, 0)
        nav_layout.setSpacing(4)
        
        # Navigation items
        nav_items = [
            ("dashboard", "🏠", "Dashboard"),
            ("sales", "💰", "Sales"),
            ("purchases", "🛒", "Purchases"),
            ("inventory", "📦", "Inventory"),
            ("customers", "👥", "Customers"),
            ("reports", "📊", "Reports"),
            ("tools", "🔧", "Tools"),
            ("settings", "⚙️", "Settings")
        ]
        
        self.nav_buttons = {}
        
        for page_id, icon, text in nav_items:
            button = self.create_nav_button(page_id, icon, text)
            nav_layout.addWidget(button)
            self.nav_buttons[page_id] = button
            
        nav_layout.addStretch()
        parent_layout.addWidget(nav_container)
        
        # Set dashboard as active
        self.set_active_page("dashboard")
        
    def create_nav_button(self, page_id, icon, text):
        """Create navigation button"""
        button = QPushButton(f"  {icon}    {text}")
        button.setCheckable(True)
        button.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #D1D5DB;
                border: none;
                border-radius: 12px;
                padding: 16px 20px;
                text-align: left;
                font-size: 16px;
                font-weight: 500;
                min-height: 20px;
            }
            QPushButton:hover {
                background: rgba(55, 65, 81, 0.7);
                color: white;
            }
            QPushButton:checked {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #3B82F6, stop:1 #1E40AF);
                color: white;
                font-weight: 600;
            }
        """)
        
        button.clicked.connect(lambda: self.navigate_to(page_id))
        return button
        
    def navigate_to(self, page_id):
        """Navigate to page"""
        self.set_active_page(page_id)
        self.page_changed.emit(page_id)
        
    def set_active_page(self, page_id):
        """Set active page"""
        self.current_page = page_id
        for btn_id, button in self.nav_buttons.items():
            button.setChecked(btn_id == page_id)
            
    def create_user_section(self, parent_layout):
        """Create user section"""
        user_container = QWidget()
        user_container.setStyleSheet("""
            QWidget {
                background: rgba(55, 65, 81, 0.5);
                border-radius: 16px;
                margin: 16px;
                padding: 20px;
            }
        """)
        
        user_layout = QVBoxLayout(user_container)
        user_layout.setContentsMargins(0, 0, 0, 0)
        user_layout.setSpacing(12)
        
        # User name
        user_name = self.extract_username()
        name_label = QLabel(f"Welcome, {user_name}")
        name_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: 600;
            }
        """)
        user_layout.addWidget(name_label)
        
        # Role
        role_label = QLabel("Administrator")
        role_label.setStyleSheet("""
            QLabel {
                color: #9CA3AF;
                font-size: 14px;
                font-weight: 400;
            }
        """)
        user_layout.addWidget(role_label)
        
        # Logout button
        logout_btn = QPushButton("🚪  Logout")
        logout_btn.setStyleSheet("""
            QPushButton {
                background: #EF4444;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 14px;
                font-weight: 600;
                margin-top: 8px;
            }
            QPushButton:hover {
                background: #DC2626;
            }
        """)
        logout_btn.clicked.connect(self.logout)
        user_layout.addWidget(logout_btn)
        
        parent_layout.addWidget(user_container)
        
    def extract_username(self):
        """Extract username from user data"""
        try:
            if isinstance(self.user_data, dict):
                return self.user_data.get("username", "Admin")
            elif isinstance(self.user_data, (list, tuple)) and len(self.user_data) > 0:
                if isinstance(self.user_data[0], dict):
                    return self.user_data[0].get("username", "Admin")
                else:
                    return str(self.user_data[0])
            return "Admin"
        except:
            return "Admin"
            
    def logout(self):
        """Handle logout"""
        reply = QMessageBox.question(
            self, 
            "Logout", 
            "Are you sure you want to logout?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            print("🔄 Logging out...")
            # Close current main window
            self.close()
            
            # Create and show login window
            from gui.ultra_login import UltraModernLogin
            self.login_window = UltraModernLogin()
            self.login_window.show()
            print("✅ Redirected to login window")

class UltraModernMain(QMainWindow):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        
        # Force true fullscreen mode with aggressive approach
        self.setWindowTitle("SSMS - Sales & Stock Management System")
        
        # Set frameless window first
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        
        # Get screen geometry and force fullscreen
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(0, 0, screen.width(), screen.height())
        
        # Force fullscreen state with multiple attempts
        self.setWindowState(Qt.WindowState.WindowFullScreen)
        self.showFullScreen()
        
        # Additional fullscreen enforcement
        self.setWindowState(Qt.WindowState.WindowFullScreen)
        
        # Set size constraints to prevent shrinking
        self.setMinimumSize(screen.width(), screen.height())
        self.setMaximumSize(screen.width(), screen.height())
        
        # Force resize to screen size
        self.resize(screen.width(), screen.height())
        
        self.setup_ui()
        self.setup_shortcuts()
        self.setup_animations()
        
        # Ensure fullscreen after UI is set up
        QTimer.singleShot(100, self.enforce_fullscreen)
        
    def enforce_fullscreen(self):
        """Enforce fullscreen mode after window initialization"""
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(0, 0, screen.width(), screen.height())
        self.setMinimumSize(screen.width(), screen.height())
        self.setMaximumSize(screen.width(), screen.height())
        self.resize(screen.width(), screen.height())
        self.setWindowState(Qt.WindowState.WindowFullScreen)
        self.showFullScreen()
        
        # Additional enforcement after a short delay
        QTimer.singleShot(50, self.final_fullscreen_enforcement)
        
    def final_fullscreen_enforcement(self):
        """Final fullscreen enforcement"""
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(0, 0, screen.width(), screen.height())
        self.setWindowState(Qt.WindowState.WindowFullScreen)
        self.showFullScreen()
        
    def setup_ui(self):
        """Setup main UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #1e293b, stop:1 #334155);
                color: #f8fafc;
            }
        """)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = ModernSidebar(self.user_data)
        self.sidebar.page_changed.connect(self.navigate_to_page)
        main_layout.addWidget(self.sidebar)
        
        # Main content area
        self.content_area = QStackedWidget()
        self.content_area.setStyleSheet("""
            QStackedWidget {
                background: rgba(255, 255, 255, 0.05);
                margin: 20px;
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        main_layout.addWidget(self.content_area)
        
        # Create pages
        self.create_pages()
        
        # Show dashboard by default
        self.navigate_to_page("dashboard")
        
    def create_pages(self):
        """Create all pages"""
        # Import tab classes
        from gui.tabs import DashboardTab, SalesTab, InventoryTab, CustomersTab, ReportsTab, SettingsTab
        from gui.tabs.purchases import PurchasesTab
        from gui.tabs.tools import ToolsTab
        
        # Dashboard
        self.dashboard_page = DashboardTab(self.user_data)
        self.content_area.addWidget(self.dashboard_page)
        
        # Sales
        self.sales_page = SalesTab(self.user_data)
        self.content_area.addWidget(self.sales_page)
        
        # Purchases
        self.purchases_page = PurchasesTab(self.user_data)
        self.content_area.addWidget(self.purchases_page)
        
        # Inventory
        self.inventory_page = InventoryTab(self.user_data)
        self.content_area.addWidget(self.inventory_page)
        
        # Customers
        self.customers_page = CustomersTab(self.user_data)
        self.content_area.addWidget(self.customers_page)
        
        # Reports
        self.reports_page = ReportsTab(self.user_data)
        self.content_area.addWidget(self.reports_page)
        
        # Tools
        self.tools_page = ToolsTab(self.user_data)
        self.content_area.addWidget(self.tools_page)
        
        # Settings
        self.settings_page = SettingsTab(self.user_data)
        self.content_area.addWidget(self.settings_page)
            
    def create_dashboard_page(self):
        """Create dashboard page"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(30)
        
        # Header with fullscreen button
        header = self.create_page_header("Dashboard", "Overview of your business metrics")
        layout.addWidget(header)
        
        # Stats cards
        stats_container = QWidget()
        stats_layout = QGridLayout(stats_container)
        stats_layout.setSpacing(20)
        
        # Sample stats
        stats_data = [
            ("Total Sales", "₹1,25,000", "📈", "#10B981"),
            ("Total Orders", "342", "📦", "#3B82F6"),
            ("Active Customers", "1,234", "👥", "#8B5CF6"),
            ("Inventory Items", "567", "📊", "#F59E0B")
        ]
        
        for i, (title, value, icon, color) in enumerate(stats_data):
            # Simple placeholder for stats
            label = QLabel(f"{icon} {title}: {value}")
            label.setStyleSheet("""
                QLabel {
                    background: white;
                    border: 1px solid #e5e7eb;
                    border-radius: 8px;
                    padding: 20px;
                    font-size: 16px;
                    font-weight: 600;
                    color: #374151;
                }
            """)
            stats_layout.addWidget(label, 0, i)
            
        layout.addWidget(stats_container)
        
        # Chart placeholder
        chart_container = QWidget()
        chart_container.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 20px;
                padding: 30px;
            }
        """)
        chart_container.setMinimumHeight(300)
        
        chart_layout = QVBoxLayout(chart_container)
        
        chart_title = QLabel("Sales Analytics")
        chart_title.setStyleSheet("""
            QLabel {
                color: #f8fafc;
                font-size: 24px;
                font-weight: 700;
                margin-bottom: 20px;
            }
        """)
        chart_layout.addWidget(chart_title)
        
        chart_placeholder = QLabel("📊 Interactive charts will be displayed here\n\nSales trends, revenue analysis, and performance metrics")
        chart_placeholder.setStyleSheet("""
            QLabel {
                color: #cbd5e1;
                font-size: 18px;
                text-align: center;
                padding: 60px;
            }
        """)
        chart_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        chart_layout.addWidget(chart_placeholder)
        
        layout.addWidget(chart_container)
        return page
        
    def create_page_header(self, title, subtitle):
        """Create page header"""
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        # Title section
        title_container = QWidget()
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(8)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                color: #f8fafc;
                font-size: 36px;
                font-weight: 800;
                letter-spacing: -1px;
            }
        """)
        title_layout.addWidget(title_label)
        
        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet("""
            QLabel {
                color: #cbd5e1;
                font-size: 16px;
                font-weight: 400;
            }
        """)
        title_layout.addWidget(subtitle_label)
        
        header_layout.addWidget(title_container)
        header_layout.addStretch()
        
        # Status indicator (always fullscreen)
        status_label = QLabel("🖥️ Fullscreen Mode")
        status_label.setStyleSheet("""
            QLabel {
                background: rgba(34, 197, 94, 0.1);
                color: #059669;
                border: 1px solid rgba(34, 197, 94, 0.2);
                border-radius: 12px;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: 600;
            }
        """)
        header_layout.addWidget(status_label)
        
        return header
        
    def create_placeholder_page(self, title, icon, description):
        """Create placeholder page"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(30)
        
        # Icon
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("""
            QLabel {
                font-size: 120px;
                color: #64748b;
            }
        """)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                color: #f8fafc;
                font-size: 48px;
                font-weight: 800;
                letter-spacing: -2px;
            }
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel(description)
        desc_label.setStyleSheet("""
            QLabel {
                color: #cbd5e1;
                font-size: 20px;
                font-weight: 400;
                max-width: 600px;
            }
        """)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        return page
        
    def get_page_icon(self, page_name):
        """Get icon for page"""
        icons = {
            "sales": "💰",
            "inventory": "📦", 
            "customers": "👥",
            "reports": "📊",
            "settings": "⚙️"
        }
        return icons.get(page_name, "📄")
        
    def get_page_description(self, page_name):
        """Get description for page"""
        descriptions = {
            "sales": "Manage sales, invoices, and transactions",
            "inventory": "Track stock levels and manage products",
            "customers": "Manage customer information and relationships", 
            "reports": "Generate reports and view business insights",
            "settings": "Configure system settings and preferences"
        }
        return descriptions.get(page_name, "Coming soon...")
        
    def navigate_to_page(self, page_name):
        """Navigate to specific page"""
        page_map = {
            "dashboard": self.dashboard_page,
            "sales": self.sales_page,
            "purchases": self.purchases_page,
            "inventory": self.inventory_page,
            "customers": self.customers_page,
            "reports": self.reports_page,
            "tools": self.tools_page,
            "settings": self.settings_page
        }
        
        if page_name in page_map:
            self.content_area.setCurrentWidget(page_map[page_name])
            self.sidebar.set_active_page(page_name)
            # No automatic refresh - let showEvent handle it
        
    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        # Only Ctrl+Q to close (no escape or fullscreen toggle)
        QShortcut(QKeySequence("Ctrl+Q"), self, self.close)
        
        # Disable escape key completely
        QShortcut(QKeySequence("Escape"), self, lambda: None)
        
    def setup_animations(self):
        """Setup entrance animations"""
        self.fade_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.fade_effect)
        
        self.fade_animation = QPropertyAnimation(self.fade_effect, b"opacity")
        self.fade_animation.setDuration(800)
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        QTimer.singleShot(100, self.fade_animation.start)
        
    # Removed toggle_fullscreen - app stays in fullscreen only
            
    # Removed drag functionality since we're not using frameless windows

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Test user data
    user_data = {"username": "admin"}
    
    window = UltraModernMain(user_data)
    window.show()
    
    sys.exit(app.exec())
