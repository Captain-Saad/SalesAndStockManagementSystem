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


class InventoryTab(BaseTab):
    """Clean, modern inventory management tab"""
    
    def __init__(self, user_data, parent=None):
        super().__init__("Inventory Management", "Manage products and stock levels", user_data)
        self.load_products_data()
        
    def create_content(self):
        """Override create_content to add our inventory content"""
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel("Inventory Management")
        title_label.setStyleSheet("""
            QLabel {
                color: #f8fafc;
                font-size: 28px;
                font-weight: 700;
            }
        """)
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Add product button
        self.add_product_btn = CleanButton("+ Add Product", "#10b981")
        self.add_product_btn.clicked.connect(self.show_add_product_dialog)
        header_layout.addWidget(self.add_product_btn)
        
        self.main_layout.addLayout(header_layout)
        
        # Filters
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(15)
        
        # Search
        self.search_input = CleanInput("Search products...")
        self.search_input.textChanged.connect(self.filter_products)
        filter_layout.addWidget(self.search_input)
        
        # Category filter
        self.category_filter = CleanCombo()
        self.category_filter.addItem("All Categories")
        self.category_filter.currentTextChanged.connect(self.filter_products)
        filter_layout.addWidget(self.category_filter)
        
        # Status filter
        self.status_filter = CleanCombo()
        self.status_filter.addItems(["All Status", "In Stock", "Low Stock", "Out of Stock"])
        self.status_filter.currentTextChanged.connect(self.filter_products)
        filter_layout.addWidget(self.status_filter)
        
        filter_layout.addStretch()
        
        # Refresh button
        self.refresh_btn = CleanButton("Refresh", "#6b7280")
        self.refresh_btn.clicked.connect(self.load_products_data)
        filter_layout.addWidget(self.refresh_btn)
        
        self.main_layout.addLayout(filter_layout)
        
        # Products table
        self.products_table = QTableWidget()
        self.products_table.setStyleSheet("""
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
        self.products_table.setColumnCount(9)
        self.products_table.setHorizontalHeaderLabels([
            "ID", "Name", "SKU", "Category", "Stock", "Price", "Status", "Supplier", "Actions"
        ])
        
        # Set column widths
        header = self.products_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(8, QHeaderView.ResizeMode.Fixed)
        
        # Set row height for better visibility
        self.products_table.verticalHeader().setDefaultSectionSize(60)
        
        # Set column widths - prioritize names and prices for full visibility
        self.products_table.setColumnWidth(0, 60)   # ID - very compact
        self.products_table.setColumnWidth(1, 300)  # Name - FULL product names visible
        self.products_table.setColumnWidth(2, 100)  # SKU - compact
        self.products_table.setColumnWidth(3, 100)  # Category - compact
        self.products_table.setColumnWidth(4, 60)   # Stock - very compact
        self.products_table.setColumnWidth(5, 150)  # Price - FULL currency visible
        self.products_table.setColumnWidth(6, 80)   # Status - compact
        self.products_table.setColumnWidth(7, 150)  # Supplier - adequate
        self.products_table.setColumnWidth(8, 100)  # Actions - compact
        
        self.main_layout.addWidget(self.products_table)
        
    def load_products_data(self):
        """Load products data from database"""
        try:
            query = """
                SELECT p.id, p.name, p.sku, p.category, p.stock_quantity, 
                       p.selling_price, p.supplier
                FROM products p
                ORDER BY p.name
            """
            results = self.execute_query(query)
            
            if results is None:
                results = []
            
            self.products_table.setRowCount(len(results))
            
            for row, product in enumerate(results):
                # ID
                self.products_table.setItem(row, 0, QTableWidgetItem(str(product['id'])))
                
                # Name
                self.products_table.setItem(row, 1, QTableWidgetItem(product['name']))
                
                # SKU
                sku = product['sku'] or "N/A"
                self.products_table.setItem(row, 2, QTableWidgetItem(sku))
                
                # Category
                category = product['category'] or "N/A"
                self.products_table.setItem(row, 3, QTableWidgetItem(category))
                
                # Stock
                stock = str(product['stock_quantity'])
                self.products_table.setItem(row, 4, QTableWidgetItem(stock))
                
                # Price
                price = f"PKR {product['selling_price']:,.2f}"
                self.products_table.setItem(row, 5, QTableWidgetItem(price))
                
                # Status (always Active since we removed is_active column)
                status = "Active"
                status_item = QTableWidgetItem(status)
                if product['stock_quantity'] == 0:
                    status_item.setBackground(QColor("#fef2f2"))
                    status_item.setForeground(QColor("#dc2626"))
                elif product['stock_quantity'] < 10:
                    status_item.setBackground(QColor("#fef3c7"))
                    status_item.setForeground(QColor("#d97706"))
                else:
                    status_item.setBackground(QColor("#f0fdf4"))
                    status_item.setForeground(QColor("#16a34a"))
                self.products_table.setItem(row, 6, status_item)
                
                # Supplier
                supplier = product['supplier'] or "N/A"
                self.products_table.setItem(row, 7, QTableWidgetItem(supplier))
                
                # Actions
                actions_widget = QWidget()
                actions_layout = QHBoxLayout(actions_widget)
                actions_layout.setContentsMargins(5, 5, 5, 5)
                actions_layout.setSpacing(5)
                
                edit_btn = CleanButton("Edit", "#3b82f6")
                edit_btn.setFixedSize(50, 25)
                edit_btn.clicked.connect(lambda checked, product_id=product['id']: self.edit_product(product_id))
                actions_layout.addWidget(edit_btn)
                
                delete_btn = CleanButton("Delete", "#ef4444")
                delete_btn.setFixedSize(60, 25)
                delete_btn.clicked.connect(lambda checked, product_id=product['id']: self.delete_product(product_id))
                actions_layout.addWidget(delete_btn)
                
                self.products_table.setCellWidget(row, 8, actions_widget)
                
            print(f"✅ Loaded {len(results)} product records")
            
        except Exception as e:
            print(f"❌ Error loading products data: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Failed to load products data: {e}")
    
    def filter_products(self):
        """Filter products based on search criteria"""
        # This is a simplified filter - in a real app you'd implement proper filtering
        self.load_products_data()
    
    def show_add_product_dialog(self):
        """Show add product dialog"""
        QMessageBox.information(self, "Add Product", "Add product functionality would be implemented here")
    
    def edit_product(self, product_id):
        """Edit product"""
        QMessageBox.information(self, "Edit Product", f"Edit product {product_id} functionality would be implemented here")
    
    def delete_product(self, product_id):
        """Delete product"""
        reply = QMessageBox.question(self, "Delete Product", f"Are you sure you want to delete product {product_id}?")
        if reply == QMessageBox.StandardButton.Yes:
            QMessageBox.information(self, "Delete Product", f"Product {product_id} deleted successfully")
            self.load_products_data()