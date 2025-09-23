import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main entry point for Ultra-Modern SSMS"""
    print("🚀 Starting Ultra-Modern SSMS v4.0")
    print("=" * 50)
    print(f"Python version: {sys.version}")
    
    try:
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import Qt
        from gui.ultra_login import UltraModernLogin
        
        # Create application
        app = QApplication(sys.argv)
        app.setStyle('Fusion')  # Modern style
        
        # Set application properties
        app.setApplicationName("SSMS")
        app.setApplicationVersion("4.0")
        app.setOrganizationName("SSMS Solutions")
        
        # High DPI support is handled automatically in PyQt6
        # No need to set attributes manually
        
        print("✨ Launching Ultra-Modern Login...")
        
        # Create and show login window
        login_window = UltraModernLogin()
        login_window.show()
        
        print("✅ Application started successfully!")
        print("🔑 Login with: admin / admin123")
        print("🎮 Controls: Ctrl+Q = Quit (Always Fullscreen)")
        print("=" * 50)
        
        # Run application
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()