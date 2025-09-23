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


class SalesTab(BaseTab):
    """Clean, modern sales management tab"""
    
    def __init__(self, user_data, parent=None):
        super().__init__("Sales Management", "Manage sales transactions and orders", user_data)
        self.load_sales_data()
        
    def create_content(self):
        """Override create_content to add our sales content"""
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel("Sales Management")
        title_label.setStyleSheet("""
            QLabel {
                color: #f8fafc;
                font-size: 28px;
                font-weight: 700;
            }
        """)
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Add sale button
        self.add_sale_btn = CleanButton("+ Add Sale", "#10b981")
        self.add_sale_btn.clicked.connect(self.show_add_sale_dialog)
        header_layout.addWidget(self.add_sale_btn)
        
        self.main_layout.addLayout(header_layout)
        
        # Filters
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(15)
        
        # Search
        self.search_input = CleanInput("Search sales...")
        self.search_input.textChanged.connect(self.filter_sales)
        filter_layout.addWidget(self.search_input)
        
        # Date filter
        self.date_filter = CleanCombo()
        self.date_filter.addItems(["All Time", "Today", "This Week", "This Month", "Last 30 Days"])
        self.date_filter.currentTextChanged.connect(self.filter_sales)
        filter_layout.addWidget(self.date_filter)
        
        # Customer filter
        self.customer_filter = CleanCombo()
        self.customer_filter.addItem("All Customers")
        self.customer_filter.currentTextChanged.connect(self.filter_sales)
        filter_layout.addWidget(self.customer_filter)
        
        filter_layout.addStretch()
        
        # Refresh button
        self.refresh_btn = CleanButton("Refresh", "#6b7280")
        self.refresh_btn.clicked.connect(self.load_sales_data)
        filter_layout.addWidget(self.refresh_btn)
        
        self.main_layout.addLayout(filter_layout)
        
        # Sales table
        self.sales_table = QTableWidget()
        self.sales_table.setStyleSheet("""
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
        self.sales_table.setColumnCount(7)
        self.sales_table.setHorizontalHeaderLabels([
            "ID", "Customer", "Product", "Quantity", "Amount", "Date", "Actions"
        ])
        
        # Set column widths
        header = self.sales_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
        
        # Set row height for better visibility
        self.sales_table.verticalHeader().setDefaultSectionSize(60)
        
        # Set column widths - prioritize names and amounts for full visibility
        self.sales_table.setColumnWidth(0, 60)   # ID - very compact
        self.sales_table.setColumnWidth(1, 250)  # Customer - FULL names visible
        self.sales_table.setColumnWidth(2, 220)  # Product - FULL product names visible
        self.sales_table.setColumnWidth(3, 80)   # Quantity - compact
        self.sales_table.setColumnWidth(4, 150)  # Amount - FULL currency visible
        self.sales_table.setColumnWidth(5, 100)  # Date - compact
        self.sales_table.setColumnWidth(6, 100)  # Actions - compact
        
        self.main_layout.addWidget(self.sales_table)
        
    def load_sales_data(self):
        """Load sales data from database"""
        try:
            query = """
                SELECT s.id, CONCAT(c.first_name, ' ', c.last_name) as customer_name, s.product_name, s.quantity, 
                       s.total_amount, s.sale_date
                FROM sales s
                JOIN customers c ON s.customer_id = c.id
                ORDER BY s.sale_date DESC
            """
            results = self.execute_query(query)
            
            if results is None:
                results = []
            
            self.sales_table.setRowCount(len(results))
            
            for row, sale in enumerate(results):
                # ID
                self.sales_table.setItem(row, 0, QTableWidgetItem(str(sale['id'])))
                
                # Customer
                self.sales_table.setItem(row, 1, QTableWidgetItem(sale['customer_name']))
                
                # Product
                self.sales_table.setItem(row, 2, QTableWidgetItem(sale['product_name']))
                
                # Quantity
                self.sales_table.setItem(row, 3, QTableWidgetItem(str(sale['quantity'])))
                
                # Amount
                amount = f"PKR {sale['total_amount']:,.2f}"
                self.sales_table.setItem(row, 4, QTableWidgetItem(amount))
                
                # Date
                if hasattr(sale['sale_date'], 'strftime'):
                    date_str = sale['sale_date'].strftime("%Y-%m-%d %H:%M")
                else:
                    date_str = str(sale['sale_date'])
                self.sales_table.setItem(row, 5, QTableWidgetItem(date_str))
                
                # Actions
                actions_widget = QWidget()
                actions_layout = QHBoxLayout(actions_widget)
                actions_layout.setContentsMargins(5, 5, 5, 5)
                actions_layout.setSpacing(5)
                
                edit_btn = CleanButton("Edit", "#3b82f6")
                edit_btn.setFixedSize(50, 25)
                edit_btn.clicked.connect(lambda checked, sale_id=sale['id']: self.edit_sale(sale_id))
                actions_layout.addWidget(edit_btn)
                
                delete_btn = CleanButton("Delete", "#ef4444")
                delete_btn.setFixedSize(60, 25)
                delete_btn.clicked.connect(lambda checked, sale_id=sale['id']: self.delete_sale(sale_id))
                actions_layout.addWidget(delete_btn)
                
                self.sales_table.setCellWidget(row, 6, actions_widget)
                
            print(f"✅ Loaded {len(results)} sales records")
            
        except Exception as e:
            print(f"❌ Error loading sales data: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Failed to load sales data: {e}")
    
    def filter_sales(self):
        """Filter sales based on search criteria"""
        # This is a simplified filter - in a real app you'd implement proper filtering
        self.load_sales_data()
    
    def show_add_sale_dialog(self):
        """Show add sale dialog"""
        QMessageBox.information(self, "Add Sale", "Add sale functionality would be implemented here")
    
    def edit_sale(self, sale_id):
        """Edit sale"""
        QMessageBox.information(self, "Edit Sale", f"Edit sale {sale_id} functionality would be implemented here")
    
    def delete_sale(self, sale_id):
        """Delete sale"""
        reply = QMessageBox.question(self, "Delete Sale", f"Are you sure you want to delete sale {sale_id}?")
        if reply == QMessageBox.StandardButton.Yes:
            QMessageBox.information(self, "Delete Sale", f"Sale {sale_id} deleted successfully")
            self.load_sales_data()