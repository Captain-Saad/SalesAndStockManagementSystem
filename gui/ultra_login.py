"""
Ultra-Modern Login Window with PyQt6
Beautiful gradients, animations, and professional design
"""

import sys
import os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import threading

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db_connection import DatabaseConnection

class GradientWidget(QWidget):
    """Widget with gradient background"""
    def __init__(self, colors, direction="vertical"):
        super().__init__()
        self.colors = colors
        self.direction = direction
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        gradient = QLinearGradient()
        if self.direction == "vertical":
            gradient = QLinearGradient(0, 0, 0, self.height())
        else:
            gradient = QLinearGradient(0, 0, self.width(), 0)
            
        for i, color in enumerate(self.colors):
            gradient.setColorAt(i / (len(self.colors) - 1), QColor(color))
            
        painter.fillRect(self.rect(), gradient)

class ModernButton(QPushButton):
    """Modern button with hover effects"""
    def __init__(self, text, style="primary"):
        super().__init__(text)
        self.style_type = style
        self.setup_style()
        
    def setup_style(self):
        if self.style_type == "primary":
            self.setStyleSheet("""
                QPushButton {
                    background-color: #1E40AF;
                    color: #FFFFFF;
                    border: 3px solid #1E40AF;
                    border-radius: 8px;
                    font-size: 18px;
                    font-weight: 700;
                    padding: 16px 30px;
                    min-height: 20px;
                    text-align: center;
                }
                QPushButton:hover {
                    background-color: #1D4ED8;
                    border-color: #1D4ED8;
                }
                QPushButton:pressed {
                    background-color: #1E3A8A;
                    border-color: #1E3A8A;
                }
                QPushButton:disabled {
                    background-color: #9CA3AF;
                    border-color: #9CA3AF;
                    color: #6B7280;
                }
            """)
        elif self.style_type == "ghost":
            self.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    color: #3B82F6;
                    border: none;
                    font-size: 14px;
                    font-weight: 500;
                    padding: 8px 12px;
                    text-decoration: underline;
                    min-height: 16px;
                }
                QPushButton:hover {
                    color: #1D4ED8;
                    background-color: rgba(59, 130, 246, 0.08);
                    border-radius: 6px;
                    text-decoration: none;
                }
                QPushButton:pressed {
                    color: #1E3A8A;
                    background-color: rgba(59, 130, 246, 0.15);
                }
            """)

class ModernInput(QLineEdit):
    """Modern input field with floating label effect"""
    def __init__(self, placeholder="", is_password=False):
        super().__init__()
        self.setPlaceholderText(placeholder)
        if is_password:
            self.setEchoMode(QLineEdit.EchoMode.Password)
        self.setup_style()
        
    def setup_style(self):
        self.setStyleSheet("""
            QLineEdit {
                background-color: #FFFFFF;
                border: 3px solid #374151;
                border-radius: 8px;
                padding: 16px 20px;
                font-size: 16px;
                color: #000000;
                min-height: 20px;
                font-weight: 600;
            }
            QLineEdit:focus {
                border-color: #1E40AF;
                background-color: #FFFFFF;
            }
            QLineEdit:hover {
                border-color: #1F2937;
                background-color: #FFFFFF;
            }
            QLineEdit::placeholder {
                color: #6B7280;
                font-weight: 400;
            }
        """)

class UltraModernLogin(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Force true fullscreen mode
        self.setWindowTitle("SSMS - Sales & Stock Management System")
        
        # Set frameless window first
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        
        # Get screen geometry and force fullscreen
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(0, 0, screen.width(), screen.height())
        
        # Force fullscreen state
        self.setWindowState(Qt.WindowState.WindowFullScreen)
        self.showFullScreen()
        
        # Setup UI
        self.setup_ui()
        self.setup_shortcuts()
        
        # Animation setup
        self.setup_animations()
        
    def setup_ui(self):
        """Setup the main UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Left panel (branding)
        self.create_left_panel(main_layout)
        
        # Right panel (login form)
        self.create_right_panel(main_layout)
        
    def create_left_panel(self, parent_layout):
        """Create stunning left branding panel"""
        # Gradient background
        left_panel = GradientWidget(["#667eea", "#764ba2"], "diagonal")
        # Make width responsive - 40% of screen width, min 500px, max 700px
        screen_width = QApplication.primaryScreen().availableGeometry().width()
        panel_width = max(500, min(700, int(screen_width * 0.4)))
        left_panel.setFixedWidth(panel_width)
        
        layout = QVBoxLayout(left_panel)
        # Responsive margins based on panel width
        margin_h = max(40, int(panel_width * 0.08))
        margin_v = max(60, int(panel_width * 0.12))
        layout.setContentsMargins(margin_h, margin_v, margin_h, margin_v)
        layout.setSpacing(30)
        
        # Logo section
        logo_container = QWidget()
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Main logo - responsive font size
        logo_label = QLabel("SSMS")
        logo_size = max(60, min(100, int(panel_width * 0.15)))
        logo_label.setStyleSheet(f"""
            QLabel {{
                color: white;
                font-size: {logo_size}px;
                font-weight: 900;
                letter-spacing: -2px;
            }}
        """)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(logo_label)
        
        # Subtitle
        subtitle = QLabel("Sales & Stock Management System")
        subtitle.setStyleSheet("""
            QLabel {
                color: rgba(255,255,255,0.9);
                font-size: 22px;
                font-weight: 300;
                letter-spacing: 1px;
                margin-top: -10px;
            }
        """)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(subtitle)
        
        layout.addWidget(logo_container)
        
        # Features list
        features_container = QWidget()
        features_layout = QVBoxLayout(features_container)
        features_layout.setSpacing(20)
        
        features = [
            ("📊", "Real-time Analytics", "Monitor your business performance instantly"),
            ("📦", "Inventory Management", "Track stock levels and manage products"),
            ("💰", "Sales Tracking", "Comprehensive sales and revenue monitoring"),
            ("👥", "Customer Management", "Build stronger customer relationships"),
            ("📈", "Business Intelligence", "Data-driven insights for growth")
        ]
        
        for icon, title, desc in features:
            feature_widget = self.create_feature_item(icon, title, desc)
            features_layout.addWidget(feature_widget)
            
        layout.addWidget(features_container)
        
        # Footer
        footer = QLabel("© 2024 SSMS • Crafted with ❤️ for Business Excellence")
        footer.setStyleSheet("""
            QLabel {
                color: rgba(255,255,255,0.7);
                font-size: 14px;
                font-weight: 300;
                padding: 20px 0;
            }
        """)
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(footer)
        
        parent_layout.addWidget(left_panel)
        
    def create_feature_item(self, icon, title, description):
        """Create a feature item widget"""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)
        
        # Icon
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("""
            QLabel {
                font-size: 32px;
                min-width: 40px;
                max-width: 40px;
            }
        """)
        layout.addWidget(icon_label)
        
        # Text container
        text_container = QWidget()
        text_layout = QVBoxLayout(text_container)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(4)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: 600;
            }
        """)
        text_layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel(description)
        desc_label.setStyleSheet("""
            QLabel {
                color: rgba(255,255,255,0.8);
                font-size: 14px;
                font-weight: 300;
                line-height: 1.4;
            }
        """)
        desc_label.setWordWrap(True)
        text_layout.addWidget(desc_label)
        
        layout.addWidget(text_container)
        return container
        
    def create_right_panel(self, parent_layout):
        """Create modern right login panel"""
        right_panel = QWidget()
        right_panel.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #fdfbfb, stop:1 #ebedee);
            }
        """)
        
        layout = QVBoxLayout(right_panel)
        # Responsive margins for right panel
        screen = QApplication.primaryScreen().availableGeometry()
        screen_width = screen.width()
        screen_height = screen.height()
        
        # Calculate panel width the same way as left panel
        panel_width = max(500, min(700, int(screen_width * 0.4)))
        right_width = screen_width - panel_width
        
        # Calculate responsive margins
        margin_h = max(40, min(120, int(right_width * 0.12)))
        margin_v = max(40, min(100, int(screen_height * 0.08)))
        
        layout.setContentsMargins(margin_h, margin_v, margin_h, margin_v)
        layout.setSpacing(28)
        
        # Header section
        header_container = QWidget()
        header_layout = QVBoxLayout(header_container)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.setSpacing(16)
        
        # Welcome text - responsive font size
        welcome_label = QLabel("Welcome Back!")
        welcome_size = max(32, min(48, int(right_width * 0.06)))
        welcome_label.setStyleSheet(f"""
            QLabel {{
                color: #1F2937;
                font-size: {welcome_size}px;
                font-weight: 700;
                letter-spacing: -1px;
            }}
        """)
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(welcome_label)
        
        # Subtitle
        subtitle_label = QLabel("Sign in to access your dashboard")
        subtitle_label.setStyleSheet("""
            QLabel {
                color: #6B7280;
                font-size: 18px;
                font-weight: 400;
            }
        """)
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(subtitle_label)
        
        layout.addWidget(header_container)
        
        # Login form
        self.create_login_form(layout)
        
        # Add some spacing
        spacer = QWidget()
        spacer.setFixedHeight(16)
        layout.addWidget(spacer)
        
        # Demo credentials card
        self.create_demo_card(layout)
        
        # Add stretch to center content vertically
        layout.addStretch()
        
        parent_layout.addWidget(right_panel)
        
    def create_login_form(self, parent_layout):
        """Create the login form"""
        form_container = QWidget()
        # Remove width constraints to prevent clipping
        form_layout = QVBoxLayout(form_container)
        form_layout.setContentsMargins(0, 0, 0, 0)  # No margins to prevent clipping
        form_layout.setSpacing(20)  # Standard spacing
        
        # Username field
        username_label = QLabel("Username")
        username_label.setStyleSheet("""
            QLabel {
                color: #374151;
                font-size: 16px;
                font-weight: 600;
                margin-bottom: 8px;
                padding-left: 4px;
            }
        """)
        form_layout.addWidget(username_label)
        
        self.username_input = ModernInput("Enter your username")
        form_layout.addWidget(self.username_input)
        
        # Add spacing between fields
        field_spacer = QWidget()
        field_spacer.setFixedHeight(12)
        form_layout.addWidget(field_spacer)
        
        # Password field
        password_label = QLabel("Password")
        password_label.setStyleSheet("""
            QLabel {
                color: #374151;
                font-size: 16px;
                font-weight: 600;
                margin-bottom: 8px;
                padding-left: 4px;
            }
        """)
        form_layout.addWidget(password_label)
        
        self.password_input = ModernInput("Enter your password", is_password=True)
        form_layout.addWidget(self.password_input)
        
        # Options row
        options_container = QWidget()
        options_layout = QHBoxLayout(options_container)
        options_layout.setContentsMargins(0, 16, 0, 16)
        
        # Remember me checkbox with better visibility
        self.remember_checkbox = QCheckBox("Remember me")
        self.remember_checkbox.setStyleSheet("""
            QCheckBox {
                color: #4B5563;
                font-size: 14px;
                font-weight: 500;
                spacing: 10px;
                padding: 6px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 3px;
                border: 2px solid #9CA3AF;
                background-color: white;
                margin-right: 8px;
            }
            QCheckBox::indicator:hover {
                border-color: #3B82F6;
                background-color: #F8FAFC;
            }
            QCheckBox::indicator:checked {
                background-color: #3B82F6;
                border-color: #3B82F6;
                image: none;
            }
            QCheckBox::indicator:checked:hover {
                background-color: #2563EB;
                border-color: #2563EB;
            }
        """)
        options_layout.addWidget(self.remember_checkbox)
        
        options_layout.addStretch()
        
        # Forgot password
        forgot_btn = ModernButton("Forgot Password?", "ghost")
        forgot_btn.clicked.connect(self.forgot_password)
        options_layout.addWidget(forgot_btn)
        
        form_layout.addWidget(options_container)
        
        # Login button
        self.login_button = ModernButton("Sign In")
        self.login_button.clicked.connect(self.handle_login)
        form_layout.addWidget(self.login_button)
        
        # Add form directly without wrapper to prevent clipping
        parent_layout.addWidget(form_container)
        
    def create_demo_card(self, parent_layout):
        """Create demo credentials card"""
        demo_card = QWidget()
        demo_card.setStyleSheet("""
            QWidget {
                background-color: rgba(59, 130, 246, 0.06);
                border: 1px solid rgba(59, 130, 246, 0.12);
                border-radius: 12px;
            }
        """)
        demo_card.setFixedHeight(130)
        
        layout = QVBoxLayout(demo_card)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(14)
        
        # Title
        title = QLabel("🔑 Demo Credentials")
        title.setStyleSheet("""
            QLabel {
                color: #1F2937;
                font-size: 16px;
                font-weight: 700;
                margin-bottom: 4px;
            }
        """)
        layout.addWidget(title)
        
        # Credentials container
        creds_container = QWidget()
        creds_layout = QVBoxLayout(creds_container)
        creds_layout.setContentsMargins(0, 0, 0, 0)
        creds_layout.setSpacing(8)
        
        # Username row
        username_container = QWidget()
        username_layout = QHBoxLayout(username_container)
        username_layout.setContentsMargins(0, 0, 0, 0)
        username_layout.setSpacing(8)
        
        username_key = QLabel("Username:")
        username_key.setStyleSheet("""
            QLabel {
                color: #6B7280;
                font-size: 14px;
                font-weight: 500;
                min-width: 70px;
            }
        """)
        username_layout.addWidget(username_key)
        
        username_value = QLabel("admin")
        username_value.setStyleSheet("""
            QLabel {
                color: #1F2937;
                font-size: 13px;
                font-family: 'Consolas', 'Courier New', monospace;
                font-weight: 600;
                background-color: rgba(255, 255, 255, 0.7);
                padding: 3px 8px;
                border-radius: 5px;
                border: 1px solid rgba(59, 130, 246, 0.1);
            }
        """)
        username_layout.addWidget(username_value)
        username_layout.addStretch()
        
        creds_layout.addWidget(username_container)
        
        # Password row
        password_container = QWidget()
        password_layout = QHBoxLayout(password_container)
        password_layout.setContentsMargins(0, 0, 0, 0)
        password_layout.setSpacing(8)
        
        password_key = QLabel("Password:")
        password_key.setStyleSheet("""
            QLabel {
                color: #6B7280;
                font-size: 14px;
                font-weight: 500;
                min-width: 70px;
            }
        """)
        password_layout.addWidget(password_key)
        
        password_value = QLabel("admin123")
        password_value.setStyleSheet("""
            QLabel {
                color: #1F2937;
                font-size: 13px;
                font-family: 'Consolas', 'Courier New', monospace;
                font-weight: 600;
                background-color: rgba(255, 255, 255, 0.7);
                padding: 3px 8px;
                border-radius: 5px;
                border: 1px solid rgba(59, 130, 246, 0.1);
            }
        """)
        password_layout.addWidget(password_value)
        password_layout.addStretch()
        
        creds_layout.addWidget(password_container)
        
        layout.addWidget(creds_container)
        
        # Add demo card directly without wrapper
        parent_layout.addWidget(demo_card)
        
    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        # Enter to login
        self.username_input.returnPressed.connect(self.handle_login)
        self.password_input.returnPressed.connect(self.handle_login)
        
        # Only Ctrl+Q to close (no escape or fullscreen toggle)
        QShortcut(QKeySequence("Ctrl+Q"), self, self.close)
        
        # Disable escape key completely
        QShortcut(QKeySequence("Escape"), self, lambda: None)
        
    def setup_animations(self):
        """Setup entrance animations"""
        # Fade in effect
        self.fade_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.fade_effect)
        
        self.fade_animation = QPropertyAnimation(self.fade_effect, b"opacity")
        self.fade_animation.setDuration(800)
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # Start animation
        QTimer.singleShot(100, self.fade_animation.start)
        
    def handle_login(self):
        """Handle login button click"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        print(f"🔑 Login attempt: username='{username}', password='{password}'")
        
        if not username or not password:
            print("❌ Empty credentials")
            self.show_error("Please enter both username and password")
            return
            
        # Show loading state
        self.login_button.setText("Signing In...")
        self.login_button.setEnabled(False)
        
        print("🔄 Starting login thread...")
        
        # Perform login in background thread
        self.login_thread = threading.Thread(
            target=self.perform_login, 
            args=(username, password), 
            daemon=True
        )
        self.login_thread.start()
        
    def perform_login(self, username, password):
        """Perform actual login"""
        try:
            print("🔌 Testing database connection...")
            # Test database connection
            db = DatabaseConnection()
            if not db.test_connection():
                print("❌ Database connection failed")
                QTimer.singleShot(0, lambda: self.show_error("Database connection failed"))
                return
                
            print("✅ Database connected, checking credentials...")
            # Check credentials
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            result = db.execute_query(query, (username, password))
            
            print(f"🔍 Query result: {result}")
            
            if result and len(result) > 0:
                user = result[0]
                print(f"✅ Login successful for user: {user}")
                # Store user data and call login_successful directly
                self.current_user = user
                QTimer.singleShot(0, self.on_login_success)
            else:
                print("❌ Invalid credentials")
                QTimer.singleShot(0, self.on_login_failure)
                
        except Exception as e:
            error_msg = f"Login error: {str(e)}"
            print(f"💥 Exception: {error_msg}")
            self.error_message = error_msg
            QTimer.singleShot(0, self.on_login_error)
        finally:
            QTimer.singleShot(0, self.reset_login_button)
    
    def on_login_success(self):
        """Handle successful login callback"""
        print("🎉 Login success callback triggered!")
        self.login_successful(self.current_user)
    
    def on_login_failure(self):
        """Handle login failure callback"""
        print("❌ Login failure callback triggered!")
        self.show_error("Invalid username or password")
    
    def on_login_error(self):
        """Handle login error callback"""
        print(f"💥 Login error callback triggered: {self.error_message}")
        self.show_error(self.error_message)
            
    def login_successful(self, user):
        """Handle successful login"""
        print("🎉 Login successful, starting transition...")
        # Skip animation for now and go directly to main window
        self.open_main_window(user)
        
    def open_main_window(self, user):
        """Open main window"""
        print("🚀 Opening main window...")
        from gui.ultra_main import UltraModernMain
        self.main_window = UltraModernMain(user)
        
        # Ensure fullscreen for main window
        self.main_window.setWindowState(Qt.WindowState.WindowFullScreen)
        self.main_window.showFullScreen()
        
        # Close login window after main window is shown
        self.close()
        print("✅ Main window opened!")
        
    def show_error(self, message):
        """Show error message"""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setWindowTitle("Login Error")
        msg_box.setText(message)
        msg_box.setStyleSheet("""
            QMessageBox {
                background: white;
                color: #1F2937;
                font-size: 14px;
            }
            QMessageBox QPushButton {
                background: #3B82F6;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 600;
            }
            QMessageBox QPushButton:hover {
                background: #2563EB;
            }
        """)
        msg_box.exec()
        
    def reset_login_button(self):
        """Reset login button state"""
        self.login_button.setText("Sign In")
        self.login_button.setEnabled(True)
        
    def forgot_password(self):
        """Handle forgot password"""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle("Forgot Password")
        msg_box.setText("Please contact your system administrator to reset your password.")
        msg_box.exec()
        
    # Removed toggle_fullscreen - app stays in fullscreen only
            
    # Removed drag functionality since we're not using frameless windows

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern style
    
    # Set application properties
    app.setApplicationName("SSMS")
    app.setApplicationVersion("4.0")
    app.setOrganizationName("SSMS Solutions")
    
    window = UltraModernLogin()
    window.show()
    
    sys.exit(app.exec())
