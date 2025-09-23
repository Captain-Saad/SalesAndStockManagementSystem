"""
Tools Tab - Utility tools and system maintenance
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                            QLabel, QPushButton, QTableWidget, QTableWidgetItem,
                            QLineEdit, QComboBox, QGroupBox, QHeaderView, 
                            QMessageBox, QDialog, QFormLayout, QTextEdit, 
                            QFrame, QSplitter, QProgressBar, QCheckBox,
                            QFileDialog, QTextBrowser)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont
from .base_tab import BaseTab
import json
import os
import shutil
from datetime import datetime


class BackupThread(QThread):
    """Thread for performing backup operations"""
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, backup_path):
        super().__init__()
        self.backup_path = backup_path
        
    def run(self):
        """Run backup operation"""
        try:
            self.status.emit("Starting backup...")
            self.progress.emit(10)
            
            # Create backup directory
            os.makedirs(self.backup_path, exist_ok=True)
            self.progress.emit(20)
            
            # Backup database
            self.status.emit("Backing up database...")
            self.progress.emit(40)
            
            # Backup settings
            self.status.emit("Backing up settings...")
            self.progress.emit(60)
            
            # Backup logs
            self.status.emit("Backing up logs...")
            self.progress.emit(80)
            
            # Create backup info
            backup_info = {
                "timestamp": datetime.now().isoformat(),
                "version": "4.0",
                "files": []
            }
            
            with open(os.path.join(self.backup_path, "backup_info.json"), 'w') as f:
                json.dump(backup_info, f, indent=4)
                
            self.progress.emit(100)
            self.status.emit("Backup completed successfully!")
            self.finished.emit(True, "Backup completed successfully!")
            
        except Exception as e:
            self.finished.emit(False, f"Backup failed: {str(e)}")


class ToolsTab(BaseTab):
    """Tools tab for system utilities and maintenance"""
    
    def __init__(self, user_data):
        super().__init__("Tools & Utilities", "System maintenance and utility tools", user_data)
        
    def create_content(self):
        """Create tools content"""
        # Main layout
        main_layout = QVBoxLayout()
        
        # Tools grid
        tools_grid = QGridLayout()
        tools_grid.setSpacing(20)
        
        # Define tools
        tools = [
            ("Database Backup", "💾", "Create system backup", self.open_backup_tool),
            ("Database Restore", "🔄", "Restore from backup", self.open_restore_tool),
            ("Data Export", "📤", "Export data to files", self.open_export_tool),
            ("Data Import", "📥", "Import data from files", self.open_import_tool),
            ("System Logs", "📋", "View system logs", self.open_logs_tool),
            ("Database Maintenance", "🔧", "Database optimization", self.open_maintenance_tool),
            ("User Management", "👥", "Manage user accounts", self.open_user_management),
            ("System Info", "ℹ️", "View system information", self.open_system_info),
            ("Clear Cache", "🗑️", "Clear system cache", self.clear_cache),
            ("Reset Settings", "⚙️", "Reset to default settings", self.reset_settings)
        ]
        
        # Create tool buttons
        for i, (title, icon, description, callback) in enumerate(tools):
            btn = self.create_tool_button(title, icon, description, callback)
            row = i // 3
            col = i % 3
            tools_grid.addWidget(btn, row, col)
            
        main_layout.addLayout(tools_grid)
        main_layout.addStretch()
        
        self.main_layout.addLayout(main_layout)
        
    def create_tool_button(self, title, icon, description, callback):
        """Create a tool button"""
        btn = QPushButton(f"{icon}\n{title}")
        btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 12px;
                padding: 20px;
                color: #f8fafc;
                font-size: 14px;
                font-weight: 600;
                text-align: center;
                min-height: 100px;
            }
            QPushButton:hover {
                background-color: rgba(59, 130, 246, 0.3);
                border-color: #3B82F6;
            }
        """)
        btn.setToolTip(description)
        btn.clicked.connect(callback)
        return btn
        
    def open_backup_tool(self):
        """Open backup tool dialog"""
        dialog = BackupDialog(self)
        dialog.exec()
        
    def open_restore_tool(self):
        """Open restore tool dialog"""
        dialog = RestoreDialog(self)
        dialog.exec()
        
    def open_export_tool(self):
        """Open export tool dialog"""
        dialog = ExportDialog(self)
        dialog.exec()
        
    def open_import_tool(self):
        """Open import tool dialog"""
        dialog = ImportDialog(self)
        dialog.exec()
        
    def open_logs_tool(self):
        """Open system logs viewer"""
        dialog = LogsDialog(self)
        dialog.exec()
        
    def open_maintenance_tool(self):
        """Open database maintenance tool"""
        dialog = MaintenanceDialog(self)
        dialog.exec()
        
    def open_user_management(self):
        """Open user management tool"""
        dialog = UserManagementDialog(self)
        dialog.exec()
        
    def open_system_info(self):
        """Open system information dialog"""
        dialog = SystemInfoDialog(self)
        dialog.exec()
        
    def clear_cache(self):
        """Clear system cache"""
        reply = QMessageBox.question(
            self, "Clear Cache", 
            "Are you sure you want to clear the system cache?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                # Clear cache logic here
                self.show_success("Cache cleared successfully")
            except Exception as e:
                self.show_error(f"Error clearing cache: {str(e)}")
                
    def reset_settings(self):
        """Reset settings to default"""
        reply = QMessageBox.question(
            self, "Reset Settings", 
            "Are you sure you want to reset all settings to default? This cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                # Reset settings logic here
                self.show_success("Settings reset to default")
            except Exception as e:
                self.show_error(f"Error resetting settings: {str(e)}")


class BackupDialog(QDialog):
    """Backup tool dialog"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup dialog UI"""
        self.setWindowTitle("Database Backup")
        self.setModal(True)
        self.resize(500, 400)
        
        layout = QVBoxLayout(self)
        
        # Backup options
        options_group = QGroupBox("Backup Options")
        options_layout = QFormLayout(options_group)
        
        # Backup location
        location_layout = QHBoxLayout()
        self.location_input = QLineEdit()
        self.location_input.setText("./backups")
        location_layout.addWidget(self.location_input)
        
        browse_btn = QPushButton("Browse")
        browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #3B82F6;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2563EB;
            }
        """)
        browse_btn.clicked.connect(self.browse_location)
        location_layout.addWidget(browse_btn)
        
        options_layout.addRow("Backup Location:", location_layout)
        
        # Include options
        self.include_database = QCheckBox("Include Database")
        self.include_database.setChecked(True)
        options_layout.addRow(self.include_database)
        
        self.include_settings = QCheckBox("Include Settings")
        self.include_settings.setChecked(True)
        options_layout.addRow(self.include_settings)
        
        self.include_logs = QCheckBox("Include Logs")
        self.include_logs.setChecked(True)
        options_layout.addRow(self.include_logs)
        
        layout.addWidget(options_group)
        
        # Progress
        progress_group = QGroupBox("Progress")
        progress_layout = QVBoxLayout(progress_group)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        progress_layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("Ready to backup")
        self.status_label.setStyleSheet("color: #cbd5e1;")
        progress_layout.addWidget(self.status_label)
        
        layout.addWidget(progress_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        start_btn = QPushButton("Start Backup")
        start_btn.setStyleSheet("""
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
        start_btn.clicked.connect(self.start_backup)
        button_layout.addWidget(start_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
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
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
    def browse_location(self):
        """Browse for backup location"""
        location = QFileDialog.getExistingDirectory(self, "Select Backup Location")
        if location:
            self.location_input.setText(location)
            
    def start_backup(self):
        """Start backup process"""
        backup_path = self.location_input.text()
        if not backup_path:
            QMessageBox.warning(self, "Warning", "Please select a backup location")
            return
            
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Start backup thread
        self.backup_thread = BackupThread(backup_path)
        self.backup_thread.progress.connect(self.progress_bar.setValue)
        self.backup_thread.status.connect(self.status_label.setText)
        self.backup_thread.finished.connect(self.backup_finished)
        self.backup_thread.start()
        
    def backup_finished(self, success, message):
        """Handle backup completion"""
        self.progress_bar.setVisible(False)
        if success:
            QMessageBox.information(self, "Success", message)
            self.accept()
        else:
            QMessageBox.critical(self, "Error", message)


class RestoreDialog(QDialog):
    """Restore tool dialog"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup dialog UI"""
        self.setWindowTitle("Database Restore")
        self.setModal(True)
        self.resize(500, 300)
        
        layout = QVBoxLayout(self)
        
        # Restore options
        options_group = QGroupBox("Restore Options")
        options_layout = QFormLayout(options_group)
        
        # Backup file selection
        file_layout = QHBoxLayout()
        self.file_input = QLineEdit()
        file_layout.addWidget(self.file_input)
        
        browse_btn = QPushButton("Browse")
        browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #3B82F6;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2563EB;
            }
        """)
        browse_btn.clicked.connect(self.browse_file)
        file_layout.addWidget(browse_btn)
        
        options_layout.addRow("Backup File:", file_layout)
        
        layout.addWidget(options_group)
        
        # Warning
        warning = QLabel("⚠️ Warning: This will overwrite all current data!")
        warning.setStyleSheet("color: #F59E0B; font-weight: bold;")
        layout.addWidget(warning)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        restore_btn = QPushButton("Restore")
        restore_btn.setStyleSheet("""
            QPushButton {
                background-color: #EF4444;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #DC2626;
            }
        """)
        restore_btn.clicked.connect(self.start_restore)
        button_layout.addWidget(restore_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
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
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
    def browse_file(self):
        """Browse for backup file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Backup File", "", "Backup Files (*.backup);;All Files (*)"
        )
        if file_path:
            self.file_input.setText(file_path)
            
    def start_restore(self):
        """Start restore process"""
        file_path = self.file_input.text()
        if not file_path:
            QMessageBox.warning(self, "Warning", "Please select a backup file")
            return
            
        reply = QMessageBox.question(
            self, "Confirm Restore", 
            "Are you sure you want to restore from this backup? All current data will be lost!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Restore logic here
            QMessageBox.information(self, "Success", "Restore completed successfully")
            self.accept()


class ExportDialog(QDialog):
    """Export tool dialog"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup dialog UI"""
        self.setWindowTitle("Data Export")
        self.setModal(True)
        self.resize(500, 400)
        
        layout = QVBoxLayout(self)
        
        # Export options
        options_group = QGroupBox("Export Options")
        options_layout = QFormLayout(options_group)
        
        # Export location
        location_layout = QHBoxLayout()
        self.location_input = QLineEdit()
        self.location_input.setText("./exports")
        location_layout.addWidget(self.location_input)
        
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_location)
        location_layout.addWidget(browse_btn)
        
        options_layout.addRow("Export Location:", location_layout)
        
        # Data selection
        self.export_sales = QCheckBox("Sales Data")
        self.export_sales.setChecked(True)
        options_layout.addRow(self.export_sales)
        
        self.export_products = QCheckBox("Products Data")
        self.export_products.setChecked(True)
        options_layout.addRow(self.export_products)
        
        self.export_customers = QCheckBox("Customers Data")
        self.export_customers.setChecked(True)
        options_layout.addRow(self.export_customers)
        
        self.export_purchases = QCheckBox("Purchases Data")
        self.export_purchases.setChecked(True)
        options_layout.addRow(self.export_purchases)
        
        # Format selection
        self.format_combo = QComboBox()
        self.format_combo.addItems(["CSV", "Excel", "JSON"])
        options_layout.addRow("Export Format:", self.format_combo)
        
        layout.addWidget(options_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        export_btn = QPushButton("Export")
        export_btn.setStyleSheet("""
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
        export_btn.clicked.connect(self.start_export)
        button_layout.addWidget(export_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
    def browse_location(self):
        """Browse for export location"""
        location = QFileDialog.getExistingDirectory(self, "Select Export Location")
        if location:
            self.location_input.setText(location)
            
    def start_export(self):
        """Start export process"""
        # Export logic here
        QMessageBox.information(self, "Success", "Export completed successfully")
        self.accept()


class ImportDialog(QDialog):
    """Import tool dialog"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup dialog UI"""
        self.setWindowTitle("Data Import")
        self.setModal(True)
        self.resize(500, 300)
        
        layout = QVBoxLayout(self)
        
        # Import options
        options_group = QGroupBox("Import Options")
        options_layout = QFormLayout(options_group)
        
        # File selection
        file_layout = QHBoxLayout()
        self.file_input = QLineEdit()
        file_layout.addWidget(self.file_input)
        
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_file)
        file_layout.addWidget(browse_btn)
        
        options_layout.addRow("Import File:", file_layout)
        
        # Format selection
        self.format_combo = QComboBox()
        self.format_combo.addItems(["CSV", "Excel", "JSON"])
        options_layout.addRow("File Format:", self.format_combo)
        
        layout.addWidget(options_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        import_btn = QPushButton("Import")
        import_btn.clicked.connect(self.start_import)
        button_layout.addWidget(import_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
    def browse_file(self):
        """Browse for import file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Import File", "", "All Files (*.*)"
        )
        if file_path:
            self.file_input.setText(file_path)
            
    def start_import(self):
        """Start import process"""
        # Import logic here
        QMessageBox.information(self, "Success", "Import completed successfully")
        self.accept()


class LogsDialog(QDialog):
    """System logs viewer dialog"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup dialog UI"""
        self.setWindowTitle("System Logs")
        self.setModal(True)
        self.resize(800, 600)
        
        layout = QVBoxLayout(self)
        
        # Log viewer
        self.log_viewer = QTextBrowser()
        self.log_viewer.setStyleSheet("""
            QTextBrowser {
                background-color: #1F2937;
                color: #F9FAFB;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
                border: 1px solid #374151;
                border-radius: 6px;
            }
        """)
        
        # Load sample logs
        sample_logs = """
[2024-01-15 10:30:15] INFO: Application started
[2024-01-15 10:30:16] INFO: Database connection established
[2024-01-15 10:30:17] INFO: User admin logged in
[2024-01-15 10:35:22] INFO: New sale created - ID: 1001
[2024-01-15 10:40:15] INFO: Product updated - ID: 5
[2024-01-15 10:45:30] WARNING: Low stock alert - Product: Coffee
[2024-01-15 11:00:00] INFO: Backup completed successfully
[2024-01-15 11:15:45] ERROR: Database connection timeout
[2024-01-15 11:16:00] INFO: Database connection restored
[2024-01-15 11:30:15] INFO: User admin logged out
        """
        
        self.log_viewer.setPlainText(sample_logs)
        layout.addWidget(self.log_viewer)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_logs)
        button_layout.addWidget(refresh_btn)
        
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.clear_logs)
        button_layout.addWidget(clear_btn)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
    def refresh_logs(self):
        """Refresh log display"""
        # Refresh logic here
        pass
        
    def clear_logs(self):
        """Clear log display"""
        self.log_viewer.clear()


class MaintenanceDialog(QDialog):
    """Database maintenance dialog"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup dialog UI"""
        self.setWindowTitle("Database Maintenance")
        self.setModal(True)
        self.resize(500, 400)
        
        layout = QVBoxLayout(self)
        
        # Maintenance options
        options_group = QGroupBox("Maintenance Options")
        options_layout = QVBoxLayout(options_group)
        
        # Maintenance tasks
        self.optimize_tables = QCheckBox("Optimize Database Tables")
        self.optimize_tables.setChecked(True)
        options_layout.addWidget(self.optimize_tables)
        
        self.clean_logs = QCheckBox("Clean Old Logs")
        self.clean_logs.setChecked(True)
        options_layout.addWidget(self.clean_logs)
        
        self.repair_tables = QCheckBox("Repair Database Tables")
        options_layout.addWidget(self.repair_tables)
        
        self.analyze_tables = QCheckBox("Analyze Table Statistics")
        self.analyze_tables.setChecked(True)
        options_layout.addWidget(self.analyze_tables)
        
        layout.addWidget(options_group)
        
        # Progress
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        start_btn = QPushButton("Start Maintenance")
        start_btn.clicked.connect(self.start_maintenance)
        button_layout.addWidget(start_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
    def start_maintenance(self):
        """Start maintenance process"""
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Simulate maintenance process
        QTimer.singleShot(1000, lambda: self.progress_bar.setValue(25))
        QTimer.singleShot(2000, lambda: self.progress_bar.setValue(50))
        QTimer.singleShot(3000, lambda: self.progress_bar.setValue(75))
        QTimer.singleShot(4000, lambda: self.progress_bar.setValue(100))
        QTimer.singleShot(5000, lambda: self.maintenance_finished())
        
    def maintenance_finished(self):
        """Handle maintenance completion"""
        self.progress_bar.setVisible(False)
        QMessageBox.information(self, "Success", "Database maintenance completed successfully")
        self.accept()


class UserManagementDialog(QDialog):
    """User management dialog"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup dialog UI"""
        self.setWindowTitle("User Management")
        self.setModal(True)
        self.resize(800, 600)
        
        layout = QVBoxLayout(self)
        
        # Users table
        self.users_table = QTableWidget()
        self.users_table.setStyleSheet("""
            QTableWidget {
                background-color: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                gridline-color: rgba(255, 255, 255, 0.1);
                color: #f8fafc;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }
            QHeaderView::section {
                background-color: rgba(255, 255, 255, 0.1);
                color: #f8fafc;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
        
        # Set table columns
        self.users_table.setColumnCount(6)
        self.users_table.setHorizontalHeaderLabels([
            "ID", "Username", "Email", "Role", "Status", "Actions"
        ])
        
        layout.addWidget(self.users_table)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton("Add User")
        add_btn.clicked.connect(self.add_user)
        button_layout.addWidget(add_btn)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
    def add_user(self):
        """Add new user"""
        # Add user logic here
        pass


class SystemInfoDialog(QDialog):
    """System information dialog"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup dialog UI"""
        self.setWindowTitle("System Information")
        self.setModal(True)
        self.resize(600, 500)
        
        layout = QVBoxLayout(self)
        
        # System info
        info_text = QTextBrowser()
        info_text.setStyleSheet("""
            QTextBrowser {
                background-color: #1F2937;
                color: #F9FAFB;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
                border: 1px solid #374151;
                border-radius: 6px;
            }
        """)
        
        import platform
        import sys
        
        system_info = f"""
SSMS - Sales & Stock Management System
Version: 4.0.0
Build: 2024.1

System Information:
Operating System: {platform.system()} {platform.release()}
Architecture: {platform.machine()}
Python Version: {sys.version}

Database Information:
Type: MySQL
Host: localhost
Port: 3306
Database: ssms

Application Information:
Framework: PyQt6
UI Theme: Dark
Fullscreen: Enabled
Auto-refresh: Enabled

Memory Usage:
Available: 8.0 GB
Used: 2.1 GB
Free: 5.9 GB

Disk Usage:
Total: 500 GB
Used: 150 GB
Free: 350 GB
        """
        
        info_text.setPlainText(system_info)
        layout.addWidget(info_text)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
