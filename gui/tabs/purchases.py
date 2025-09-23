"""
Purchases Tab - Purchase management, supplier management, and purchase reports
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                            QLabel, QPushButton, QTableWidget, QTableWidgetItem,
                            QLineEdit, QComboBox, QDateEdit, QSpinBox, QDoubleSpinBox,
                            QGroupBox, QHeaderView, QMessageBox, QDialog, QFormLayout,
                            QTextEdit, QFrame, QSplitter, QTabWidget, QCheckBox)
from PyQt6.QtCore import Qt, QDate, pyqtSignal
from PyQt6.QtGui import QFont
from .base_tab import BaseTab
from datetime import datetime, date


class PurchaseDialog(QDialog):
    """Dialog for creating/editing purchases"""
    
    def __init__(self, parent=None, purchase_data=None):
        super().__init__(parent)
        self.purchase_data = purchase_data
        self.setup_ui()
        
    def setup_ui(self):
        """Setup dialog UI"""
        self.setWindowTitle("Purchase Entry" if not self.purchase_data else "Edit Purchase")
        self.setModal(True)
        self.resize(700, 600)
        
        layout = QVBoxLayout(self)
        
        # Form
        form_group = QGroupBox("Purchase Information")
        form_layout = QFormLayout(form_group)
        
        # Supplier selection
        self.supplier_combo = QComboBox()
        self.supplier_combo.setEditable(True)
        form_layout.addRow("Supplier:", self.supplier_combo)
        
        # Purchase date
        self.purchase_date = QDateEdit()
        self.purchase_date.setDate(QDate.currentDate())
        form_layout.addRow("Purchase Date:", self.purchase_date)
        
        # Product selection
        self.product_combo = QComboBox()
        self.product_combo.setEditable(True)
        form_layout.addRow("Product:", self.product_combo)
        
        # Batch number
        self.batch_input = QLineEdit()
        self.batch_input.setPlaceholderText("Enter batch number")
        form_layout.addRow("Batch Number:", self.batch_input)
        
        # Quantity
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setMinimum(1)
        self.quantity_spin.setMaximum(99999)
        form_layout.addRow("Quantity:", self.quantity_spin)
        
        # Unit price
        self.unit_price_spin = QDoubleSpinBox()
        self.unit_price_spin.setMinimum(0.0)
        self.unit_price_spin.setMaximum(999999.99)
        self.unit_price_spin.setDecimals(2)
        form_layout.addRow("Unit Price:", self.unit_price_spin)
        
        # Total amount (calculated)
        self.total_amount_label = QLabel("PKR 0.00")
        self.total_amount_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        form_layout.addRow("Total Amount:", self.total_amount_label)
        
        # Payment method
        self.payment_combo = QComboBox()
        self.payment_combo.addItems(["Bank Transfer", "Cheque", "Cash", "Card"])
        form_layout.addRow("Payment Method:", self.payment_combo)
        
        # Payment status
        self.payment_status_combo = QComboBox()
        self.payment_status_combo.addItems(["Pending", "Paid", "Partially Paid"])
        form_layout.addRow("Payment Status:", self.payment_status_combo)
        
        # Expiry date
        self.expiry_date = QDateEdit()
        self.expiry_date.setDate(QDate.currentDate().addYears(1))
        form_layout.addRow("Expiry Date:", self.expiry_date)
        
        # Notes
        self.notes_text = QTextEdit()
        self.notes_text.setMaximumHeight(80)
        form_layout.addRow("Notes:", self.notes_text)
        
        layout.addWidget(form_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("Save")
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
        save_btn.clicked.connect(self.accept)
        
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
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        # Connect signals for calculation
        self.quantity_spin.valueChanged.connect(self.calculate_total)
        self.unit_price_spin.valueChanged.connect(self.calculate_total)
        
        # Load data if editing
        if self.purchase_data:
            self.load_data()
            
    def calculate_total(self):
        """Calculate total amount"""
        quantity = self.quantity_spin.value()
        unit_price = self.unit_price_spin.value()
        total = quantity * unit_price
        self.total_amount_label.setText(f"PKR {total:.2f}")
        
    def load_data(self):
        """Load existing purchase data"""
        if self.purchase_data:
            # Load existing data into form
            pass
            
    def get_data(self):
        """Get form data"""
        return {
            'supplier_name': self.supplier_combo.currentText(),
            'purchase_date': self.purchase_date.date().toPython(),
            'product_name': self.product_combo.currentText(),
            'batch_number': self.batch_input.text(),
            'quantity': self.quantity_spin.value(),
            'unit_price': self.unit_price_spin.value(),
            'total_amount': float(self.total_amount_label.text().replace('PKR', '').replace(',', '').strip()),
            'payment_method': self.payment_combo.currentText(),
            'payment_status': self.payment_status_combo.currentText(),
            'expiry_date': self.expiry_date.date().toPython(),
            'notes': self.notes_text.toPlainText()
        }


class PurchaseDemandDialog(QDialog):
    """Dialog for creating purchase demands"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup dialog UI"""
        self.setWindowTitle("Purchase Demand")
        self.setModal(True)
        self.resize(500, 400)
        
        layout = QVBoxLayout(self)
        
        # Form
        form_group = QGroupBox("Demand Information")
        form_layout = QFormLayout(form_group)
        
        # Product selection
        self.product_combo = QComboBox()
        self.product_combo.setEditable(True)
        form_layout.addRow("Product:", self.product_combo)
        
        # Quantity demanded
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setMinimum(1)
        self.quantity_spin.setMaximum(99999)
        form_layout.addRow("Quantity Demanded:", self.quantity_spin)
        
        # Priority
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["LOW", "MEDIUM", "HIGH", "URGENT"])
        form_layout.addRow("Priority:", self.priority_combo)
        
        # Reason
        self.reason_text = QTextEdit()
        self.reason_text.setMaximumHeight(80)
        form_layout.addRow("Reason:", self.reason_text)
        
        layout.addWidget(form_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("Create Demand")
        save_btn.setStyleSheet("""
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
        save_btn.clicked.connect(self.accept)
        
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
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
    def get_data(self):
        """Get form data"""
        return {
            'product_name': self.product_combo.currentText(),
            'quantity_demanded': self.quantity_spin.value(),
            'priority': self.priority_combo.currentText(),
            'reason': self.reason_text.toPlainText()
        }


class PurchasesTab(BaseTab):
    """Purchases tab for managing purchases and suppliers"""
    
    def __init__(self, user_data):
        super().__init__("Purchases Management", "Manage purchases, suppliers, and purchase demands", user_data)
        
    def create_content(self):
        """Create purchases content"""
        # Main tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                background: transparent;
            }
            QTabBar::tab {
                background: transparent;
                color: #f8fafc;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            QTabBar::tab:selected {
                background: transparent;
                border-bottom: 2px solid #3B82F6;
            }
            QTabBar::tab:hover {
                background: transparent;
            }
        """)
        
        # Purchase Transactions tab
        self.purchases_tab = self.create_purchases_tab()
        self.tab_widget.addTab(self.purchases_tab, "Purchase Transactions")
        
        # Purchase Demands tab
        self.demands_tab = self.create_demands_tab()
        self.tab_widget.addTab(self.demands_tab, "Purchase Demands")
        
        # Suppliers tab
        self.suppliers_tab = self.create_suppliers_tab()
        self.tab_widget.addTab(self.suppliers_tab, "Suppliers")
        
        # Purchase Reports tab
        self.reports_tab = self.create_reports_tab()
        self.tab_widget.addTab(self.reports_tab, "Purchase Reports")
        
        self.main_layout.addWidget(self.tab_widget)
        
        # Load initial data
        self.refresh_data()
        
    def create_purchases_tab(self):
        """Create purchases transactions tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("Purchase Transactions")
        title.setStyleSheet("""
            QLabel {
                color: #f8fafc;
                font-size: 24px;
                font-weight: 700;
            }
        """)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Add new purchase button
        add_purchase_btn = QPushButton("+ New Purchase")
        add_purchase_btn.setStyleSheet("""
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
        add_purchase_btn.clicked.connect(self.add_purchase)
        header_layout.addWidget(add_purchase_btn)
        
        layout.addLayout(header_layout)
        
        # Search and filter
        filter_layout = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search purchases...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background: transparent;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 6px;
                padding: 8px 12px;
                color: #f8fafc;
            }
            QLineEdit:focus {
                border-color: #3B82F6;
            }
        """)
        filter_layout.addWidget(self.search_input)
        
        self.supplier_filter = QComboBox()
        self.supplier_filter.addItem("All Suppliers")
        self.supplier_filter.setStyleSheet("""
            QComboBox {
                background: transparent;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 6px;
                padding: 8px 12px;
                color: #f8fafc;
            }
        """)
        filter_layout.addWidget(QLabel("Supplier:"))
        filter_layout.addWidget(self.supplier_filter)
        
        filter_btn = QPushButton("Filter")
        filter_btn.setStyleSheet("""
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
        filter_btn.clicked.connect(self.filter_purchases)
        filter_layout.addWidget(filter_btn)
        
        layout.addLayout(filter_layout)
        
        # Purchases table
        self.purchases_table = QTableWidget()
        self.purchases_table.setStyleSheet("""
            QTableWidget {
                background: transparent;
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 15px;
                gridline-color: rgba(255, 255, 255, 0.05);
                color: #f8fafc;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.05);
                background: transparent;
            }
            QTableWidget::item:selected {
                background-color: rgba(59, 130, 246, 0.2);
            }
            QHeaderView::section {
                background: transparent;
                color: #e2e8f0;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
        
        # Set table columns
        self.purchases_table.setColumnCount(10)
        self.purchases_table.setHorizontalHeaderLabels([
            "ID", "Supplier", "Product", "Batch", "Quantity", "Unit Price", "Total", "Date", "Status", "Actions"
        ])
        
        # Set column widths
        header = self.purchases_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)  # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Supplier
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # Product
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)  # Batch
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)  # Quantity
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)  # Unit Price
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)  # Total
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.Fixed)  # Date
        header.setSectionResizeMode(8, QHeaderView.ResizeMode.Fixed)  # Status
        header.setSectionResizeMode(9, QHeaderView.ResizeMode.Fixed)  # Actions
        
        # Set row height for better visibility
        self.purchases_table.verticalHeader().setDefaultSectionSize(60)
        
        # Set column widths - prioritize names and amounts for full visibility
        self.purchases_table.setColumnWidth(0, 60)   # ID - very compact
        self.purchases_table.setColumnWidth(1, 220)  # Supplier - FULL names visible
        self.purchases_table.setColumnWidth(2, 200)  # Product - FULL names visible
        self.purchases_table.setColumnWidth(3, 80)   # Batch - compact
        self.purchases_table.setColumnWidth(4, 60)   # Quantity - very compact
        self.purchases_table.setColumnWidth(5, 130)  # Unit Price - FULL currency visible
        self.purchases_table.setColumnWidth(6, 130)  # Total - FULL currency visible
        self.purchases_table.setColumnWidth(7, 100)  # Date - compact
        self.purchases_table.setColumnWidth(8, 80)   # Status - compact
        self.purchases_table.setColumnWidth(9, 100)  # Actions - compact
        
        layout.addWidget(self.purchases_table)
        
        return tab
        
    def create_demands_tab(self):
        """Create purchase demands tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("Purchase Demands")
        title.setStyleSheet("""
            QLabel {
                color: #f8fafc;
                font-size: 24px;
                font-weight: 700;
            }
        """)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Add new demand button
        add_demand_btn = QPushButton("+ New Demand")
        add_demand_btn.setStyleSheet("""
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
        add_demand_btn.clicked.connect(self.add_demand)
        header_layout.addWidget(add_demand_btn)
        
        layout.addLayout(header_layout)
        
        # Demands table
        self.demands_table = QTableWidget()
        self.demands_table.setStyleSheet("""
            QTableWidget {
                background: transparent;
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 15px;
                gridline-color: rgba(255, 255, 255, 0.05);
                color: #f8fafc;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.05);
                background: transparent;
            }
            QTableWidget::item:selected {
                background-color: rgba(59, 130, 246, 0.2);
            }
            QHeaderView::section {
                background: transparent;
                color: #e2e8f0;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
        
        # Set table columns
        self.demands_table.setColumnCount(7)
        self.demands_table.setHorizontalHeaderLabels([
            "ID", "Product", "Quantity", "Priority", "Status", "Requested By", "Actions"
        ])
        
        layout.addWidget(self.demands_table)
        
        return tab
        
    def create_suppliers_tab(self):
        """Create suppliers management tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("Suppliers")
        title.setStyleSheet("""
            QLabel {
                color: #f8fafc;
                font-size: 24px;
                font-weight: 700;
            }
        """)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Add new supplier button
        add_supplier_btn = QPushButton("+ Add Supplier")
        add_supplier_btn.setStyleSheet("""
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
        add_supplier_btn.clicked.connect(self.add_supplier)
        header_layout.addWidget(add_supplier_btn)
        
        layout.addLayout(header_layout)
        
        # Suppliers table
        self.suppliers_table = QTableWidget()
        self.suppliers_table.setStyleSheet("""
            QTableWidget {
                background: transparent;
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 15px;
                gridline-color: rgba(255, 255, 255, 0.05);
                color: #f8fafc;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.05);
                background: transparent;
            }
            QTableWidget::item:selected {
                background-color: rgba(59, 130, 246, 0.2);
            }
            QHeaderView::section {
                background: transparent;
                color: #e2e8f0;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
        
        # Set table columns
        self.suppliers_table.setColumnCount(8)
        self.suppliers_table.setHorizontalHeaderLabels([
            "ID", "Name", "Contact Person", "Email", "Phone", "City", "Payment Terms", "Actions"
        ])
        
        layout.addWidget(self.suppliers_table)
        
        return tab
        
    def create_reports_tab(self):
        """Create purchase reports tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Header
        title = QLabel("Purchase Reports")
        title.setStyleSheet("""
            QLabel {
                color: #f8fafc;
                font-size: 24px;
                font-weight: 700;
                margin-bottom: 20px;
            }
        """)
        layout.addWidget(title)
        
        # Report buttons
        reports_layout = QGridLayout()
        
        reports = [
            ("Purchase Summary", "📊", "View purchase summary report"),
            ("Supplier Analysis", "🏢", "Analyze supplier performance"),
            ("Product Analysis", "📦", "Analyze product purchases"),
            ("Payment Status", "💰", "View payment status report"),
            ("Expiry Report", "⏰", "View product expiry report"),
            ("Demand Report", "📋", "View purchase demands report")
        ]
        
        for i, (title, icon, description) in enumerate(reports):
            btn = QPushButton(f"{icon} {title}")
            btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 8px;
                    padding: 20px;
                    color: #f8fafc;
                    font-size: 14px;
                    font-weight: 600;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: rgba(59, 130, 246, 0.3);
                    border-color: #3B82F6;
                }
            """)
            btn.setToolTip(description)
            btn.clicked.connect(lambda checked, t=title: self.generate_report(t))
            
            row = i // 2
            col = i % 2
            reports_layout.addWidget(btn, row, col)
            
        layout.addLayout(reports_layout)
        layout.addStretch()
        
        return tab
        
    def refresh_data(self):
        """Refresh purchases data"""
        try:
            self.load_purchases_data()
            self.load_demands_data()
            self.load_suppliers_data()
        except Exception as e:
            self.show_error(f"Error refreshing purchases data: {str(e)}")
            
    def load_purchases_data(self):
        """Load purchases data from database"""
        try:
            # Query purchases data
            query = """
                SELECT p.id, p.supplier_name, p.product_name, p.quantity,
                       p.unit_price, p.total_amount, p.purchase_date,
                       p.payment_status, p.notes
                FROM purchases p
                ORDER BY p.purchase_date DESC
                LIMIT 100
            """
            result = self.execute_query(query)
            
            if result:
                self.purchases_table.setRowCount(len(result))
                
                for row, purchase in enumerate(result):
                    # ID
                    self.purchases_table.setItem(row, 0, QTableWidgetItem(str(purchase['id'])))
                    
                    # Supplier
                    self.purchases_table.setItem(row, 1, QTableWidgetItem(purchase['supplier_name'] or "N/A"))
                    
                    # Product
                    self.purchases_table.setItem(row, 2, QTableWidgetItem(purchase['product_name'] or "N/A"))
                    
                    # Batch (using quantity as batch for now)
                    self.purchases_table.setItem(row, 3, QTableWidgetItem(str(purchase['quantity'])))
                    
                    # Quantity
                    self.purchases_table.setItem(row, 4, QTableWidgetItem(str(purchase['quantity'])))
                    
                    # Unit Price
                    self.purchases_table.setItem(row, 5, QTableWidgetItem(f"PKR {purchase['unit_price']:.2f}"))
                    
                    # Total
                    self.purchases_table.setItem(row, 6, QTableWidgetItem(f"PKR {purchase['total_amount']:.2f}"))
                    
                    # Date
                    date_str = purchase['purchase_date'].strftime("%Y-%m-%d") if purchase['purchase_date'] else "N/A"
                    self.purchases_table.setItem(row, 7, QTableWidgetItem(date_str))
                    
                    # Status
                    status_item = QTableWidgetItem(purchase['payment_status'] or "N/A")
                    if purchase['payment_status'] == "Paid":
                        status_item.setBackground(Qt.GlobalColor.green)
                    elif purchase['payment_status'] == "Pending":
                        status_item.setBackground(Qt.GlobalColor.yellow)
                    else:
                        status_item.setBackground(Qt.GlobalColor.red)
                    self.purchases_table.setItem(row, 8, status_item)
                    
                    # Actions
                    actions_widget = QWidget()
                    actions_layout = QHBoxLayout(actions_widget)
                    actions_layout.setContentsMargins(0, 0, 0, 0)
                    
                    edit_btn = QPushButton("Edit")
                    edit_btn.setStyleSheet("""
                        QPushButton {
                            background-color: #3B82F6;
                            color: white;
                            border: none;
                            padding: 4px 8px;
                            border-radius: 4px;
                            font-size: 12px;
                        }
                        QPushButton:hover {
                            background-color: #2563EB;
                        }
                    """)
                    edit_btn.clicked.connect(lambda checked, purchase_id=purchase[0]: self.edit_purchase(purchase_id))
                    
                    delete_btn = QPushButton("Delete")
                    delete_btn.setStyleSheet("""
                        QPushButton {
                            background-color: #EF4444;
                            color: white;
                            border: none;
                            padding: 4px 8px;
                            border-radius: 4px;
                            font-size: 12px;
                        }
                        QPushButton:hover {
                            background-color: #DC2626;
                        }
                    """)
                    delete_btn.clicked.connect(lambda checked, purchase_id=purchase[0]: self.delete_purchase(purchase_id))
                    
                    actions_layout.addWidget(edit_btn)
                    actions_layout.addWidget(delete_btn)
                    
                    self.purchases_table.setCellWidget(row, 9, actions_widget)
                    
            else:
                self.purchases_table.setRowCount(0)
                
        except Exception as e:
            self.show_error(f"Error loading purchases data: {str(e)}")
            
    def load_demands_data(self):
        """Load purchase demands data"""
        # Implementation for loading demands data
        pass
        
    def load_suppliers_data(self):
        """Load suppliers data"""
        # Implementation for loading suppliers data
        pass
        
    def add_purchase(self):
        """Add new purchase"""
        dialog = PurchaseDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            self.save_purchase(data)
            
    def edit_purchase(self, purchase_id):
        """Edit existing purchase"""
        dialog = PurchaseDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            self.update_purchase(purchase_id, data)
            
    def delete_purchase(self, purchase_id):
        """Delete purchase"""
        reply = QMessageBox.question(
            self, "Delete Purchase", 
            "Are you sure you want to delete this purchase?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                query = "DELETE FROM purchases WHERE id = %s"
                self.execute_query(query, (purchase_id,))
                self.show_success("Purchase deleted successfully")
                self.refresh_data()
            except Exception as e:
                self.show_error(f"Error deleting purchase: {str(e)}")
                
    def save_purchase(self, data):
        """Save new purchase"""
        try:
            query = """
                INSERT INTO purchases (supplier_name, product_name, batch_number, quantity, 
                                     unit_price, total_amount, purchase_date, payment_method, 
                                     payment_status, notes, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
            """
            params = (
                data['supplier_name'],
                data['product_name'],
                data['batch_number'],
                data['quantity'],
                data['unit_price'],
                data['total_amount'],
                data['purchase_date'],
                data['payment_method'],
                data['payment_status'],
                data['notes']
            )
            self.execute_query(query, params)
            self.show_success("Purchase saved successfully")
            self.refresh_data()
        except Exception as e:
            self.show_error(f"Error saving purchase: {str(e)}")
            
    def update_purchase(self, purchase_id, data):
        """Update existing purchase"""
        try:
            query = """
                UPDATE purchases SET supplier_name = %s, product_name = %s, batch_number = %s,
                                   quantity = %s, unit_price = %s, total_amount = %s,
                                   purchase_date = %s, payment_method = %s, payment_status = %s,
                                   notes = %s, updated_at = NOW()
                WHERE id = %s
            """
            params = (
                data['supplier_name'],
                data['product_name'],
                data['batch_number'],
                data['quantity'],
                data['unit_price'],
                data['total_amount'],
                data['purchase_date'],
                data['payment_method'],
                data['payment_status'],
                data['notes'],
                purchase_id
            )
            self.execute_query(query, params)
            self.show_success("Purchase updated successfully")
            self.refresh_data()
        except Exception as e:
            self.show_error(f"Error updating purchase: {str(e)}")
            
    def add_demand(self):
        """Add new purchase demand"""
        dialog = PurchaseDemandDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            self.save_demand(data)
            
    def save_demand(self, data):
        """Save new purchase demand"""
        try:
            query = """
                INSERT INTO purchase_demands (product_id, quantity_demanded, priority, 
                                            reason, requested_by, created_at)
                VALUES ((SELECT id FROM products WHERE name = %s LIMIT 1), %s, %s, %s, %s, NOW())
            """
            params = (
                data['product_name'],
                data['quantity_demanded'],
                data['priority'],
                data['reason'],
                self.user_data['id']
            )
            self.execute_query(query, params)
            self.show_success("Purchase demand created successfully")
            self.refresh_data()
        except Exception as e:
            self.show_error(f"Error saving demand: {str(e)}")
            
    def add_supplier(self):
        """Add new supplier"""
        # Implementation for adding supplier
        pass
        
    def generate_report(self, report_type):
        """Generate purchase report"""
        self.show_success(f"Generating {report_type} report...")
        
    def filter_purchases(self):
        """Filter purchases based on search criteria"""
        self.refresh_data()
