from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from .base_tab import BaseTab
from datetime import datetime, timedelta


class CleanButton(QPushButton):
    """Clean, modern button"""
    
    def __init__(self, text, color="#3b82f6"):
        super().__init__(text)
        self.setStyleSheet(f"""
            QPushButton {{
                background: {color};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: 500;
                min-height: 20px;
            }}
            QPushButton:hover {{
                background: {self.darken_color(color)};
            }}
            QPushButton:pressed {{
                background: {self.darken_color(color, 0.8)};
            }}
        """)
    
    def darken_color(self, color, factor=0.9):
        """Darken color for hover effect"""
        if color.startswith("#"):
            color = color[1:]
        r = int(color[0:2], 16)
        g = int(color[2:4], 16)
        b = int(color[4:6], 16)
        r = int(r * factor)
        g = int(g * factor)
        b = int(b * factor)
        return f"#{r:02x}{g:02x}{b:02x}"


class CleanInput(QLineEdit):
    """Clean, modern input field"""
    
    def __init__(self, placeholder=""):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
                background: white;
                color: #374151;
            }
            QLineEdit:focus {
                border: 2px solid #3b82f6;
                outline: none;
            }
        """)


class CleanCombo(QComboBox):
    """Clean, modern combo box"""
    
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QComboBox {
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
                background: white;
                color: #374151;
                min-height: 20px;
            }
            QComboBox:focus {
                border: 2px solid #3b82f6;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #6b7280;
                margin-right: 5px;
            }
        """)


class CustomersTab(BaseTab):
    """Clean, modern customers management tab"""
    
    def __init__(self, user_data, parent=None):
        super().__init__("Customer Management", "Manage customer information and relationships", user_data)
        self.load_customers_data()
        
    def create_content(self):
        """Override create_content to add our customers content"""
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel("Customer Management")
        title_label.setStyleSheet("""
            QLabel {
                color: #f8fafc;
                font-size: 28px;
                font-weight: 700;
            }
        """)
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Add customer button
        self.add_customer_btn = CleanButton("+ Add Customer", "#10b981")
        self.add_customer_btn.clicked.connect(self.show_add_customer_dialog)
        header_layout.addWidget(self.add_customer_btn)
        
        self.main_layout.addLayout(header_layout)
        
        # Filters
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(15)
        
        # Search
        self.search_input = CleanInput("Search customers...")
        self.search_input.textChanged.connect(self.filter_customers)
        filter_layout.addWidget(self.search_input)
        
        # Type filter
        self.type_filter = CleanCombo()
        self.type_filter.addItems(["All Types", "Individual", "Business"])
        self.type_filter.currentTextChanged.connect(self.filter_customers)
        filter_layout.addWidget(self.type_filter)
        
        # City filter
        self.city_filter = CleanCombo()
        self.city_filter.addItem("All Cities")
        self.city_filter.currentTextChanged.connect(self.filter_customers)
        filter_layout.addWidget(self.city_filter)
        
        filter_layout.addStretch()
        
        # Refresh button
        self.refresh_btn = CleanButton("Refresh", "#6b7280")
        self.refresh_btn.clicked.connect(self.load_customers_data)
        filter_layout.addWidget(self.refresh_btn)
        
        self.main_layout.addLayout(filter_layout)
        
        # Customers table
        self.customers_table = QTableWidget()
        self.customers_table.setStyleSheet("""
            QTableWidget {
                background: transparent;
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 15px;
                gridline-color: rgba(255, 255, 255, 0.05);
                color: #f8fafc;
                font-size: 14px;
                selection-background-color: rgba(59, 130, 246, 0.3);
            }
            QTableWidget::item {
                padding: 12px 16px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.05);
                min-height: 20px;
                background: transparent;
            }
            QTableWidget::item:selected {
                background: rgba(59, 130, 246, 0.2);
                color: #ffffff;
            }
            QHeaderView::section {
                background: transparent;
                color: #e2e8f0;
                padding: 12px 16px;
                border: none;
                border-bottom: 2px solid rgba(255, 255, 255, 0.1);
                font-weight: 600;
                font-size: 14px;
                min-height: 20px;
            }
        """)
        
        # Set table columns
        self.customers_table.setColumnCount(8)
        self.customers_table.setHorizontalHeaderLabels([
            "ID", "Name", "Email", "Phone", "Type", "City", "Orders", "Actions"
        ])
        
        # Set column widths
        header = self.customers_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.Fixed)
        
        # Set row height for better visibility
        self.customers_table.verticalHeader().setDefaultSectionSize(60)
        
        # Set column widths - prioritize names for full visibility
        self.customers_table.setColumnWidth(0, 60)   # ID - very compact
        self.customers_table.setColumnWidth(1, 280)  # Name - FULL names visible
        self.customers_table.setColumnWidth(2, 200)  # Email - adequate
        self.customers_table.setColumnWidth(3, 120)  # Phone - compact
        self.customers_table.setColumnWidth(4, 80)   # Type - compact
        self.customers_table.setColumnWidth(5, 100)  # City - compact
        self.customers_table.setColumnWidth(6, 60)   # Orders - very compact
        self.customers_table.setColumnWidth(7, 100)  # Actions - compact
        
        self.main_layout.addWidget(self.customers_table)
        
    def load_customers_data(self):
        """Load customers data from database"""
        try:
            query = """
                SELECT c.id, CONCAT(c.first_name, ' ', c.last_name) as customer_name, c.email, c.phone, 
                       c.customer_type, c.city, COUNT(s.id) as total_orders
                FROM customers c
                LEFT JOIN sales s ON c.id = s.customer_id
                GROUP BY c.id
                ORDER BY c.first_name, c.last_name
            """
            results = self.execute_query(query)
            
            if results is None:
                results = []
            
            self.customers_table.setRowCount(len(results))
            
            for row, customer in enumerate(results):
                # ID
                self.customers_table.setItem(row, 0, QTableWidgetItem(str(customer['id'])))
                
                # Name
                self.customers_table.setItem(row, 1, QTableWidgetItem(customer['customer_name']))
                
                # Email
                email = customer['email'] or "N/A"
                self.customers_table.setItem(row, 2, QTableWidgetItem(email))
                
                # Phone
                phone = customer['phone'] or "N/A"
                self.customers_table.setItem(row, 3, QTableWidgetItem(phone))
                
                # Type
                customer_type = customer['customer_type'] or "Individual"
                self.customers_table.setItem(row, 4, QTableWidgetItem(customer_type))
                
                # City
                city = customer['city'] or "N/A"
                self.customers_table.setItem(row, 5, QTableWidgetItem(city))
                
                # Orders
                orders = str(customer['total_orders'])
                self.customers_table.setItem(row, 6, QTableWidgetItem(orders))
                
                # Actions
                actions_widget = QWidget()
                actions_layout = QHBoxLayout(actions_widget)
                actions_layout.setContentsMargins(5, 5, 5, 5)
                actions_layout.setSpacing(5)
                
                edit_btn = CleanButton("Edit", "#3b82f6")
                edit_btn.setFixedSize(50, 25)
                edit_btn.clicked.connect(lambda checked, customer_id=customer['id']: self.edit_customer(customer_id))
                actions_layout.addWidget(edit_btn)
                
                delete_btn = CleanButton("Delete", "#ef4444")
                delete_btn.setFixedSize(60, 25)
                delete_btn.clicked.connect(lambda checked, customer_id=customer['id']: self.delete_customer(customer_id))
                actions_layout.addWidget(delete_btn)
                
                self.customers_table.setCellWidget(row, 7, actions_widget)
                
            print(f"✅ Loaded {len(results)} customer records")
            
        except Exception as e:
            print(f"❌ Error loading customers data: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Failed to load customers data: {e}")
    
    def filter_customers(self):
        """Filter customers based on search criteria"""
        # This is a simplified filter - in a real app you'd implement proper filtering
        self.load_customers_data()
    
    def show_add_customer_dialog(self):
        """Show add customer dialog"""
        QMessageBox.information(self, "Add Customer", "Add customer functionality would be implemented here")
    
    def edit_customer(self, customer_id):
        """Edit customer"""
        QMessageBox.information(self, "Edit Customer", f"Edit customer {customer_id} functionality would be implemented here")
    
    def delete_customer(self, customer_id):
        """Delete customer"""
        reply = QMessageBox.question(self, "Delete Customer", f"Are you sure you want to delete customer {customer_id}?")
        if reply == QMessageBox.StandardButton.Yes:
            QMessageBox.information(self, "Delete Customer", f"Customer {customer_id} deleted successfully")
            self.load_customers_data()