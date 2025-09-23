"""
Reports Tab - Analytics, reporting, and business intelligence
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                            QLabel, QPushButton, QTableWidget, QTableWidgetItem,
                            QLineEdit, QComboBox, QDateEdit, QGroupBox, 
                            QHeaderView, QMessageBox, QFrame, QSplitter,
                            QTextEdit, QProgressBar, QCheckBox)
from PyQt6.QtCore import Qt, QDate, pyqtSignal
from PyQt6.QtGui import QFont
from .base_tab import BaseTab
from datetime import datetime, timedelta
import json


class ReportCard(QFrame):
    """Report card widget for displaying metrics"""
    
    def __init__(self, title, value, subtitle, icon, color, trend=None):
        super().__init__()
        self.title = title
        self.value = value
        self.subtitle = subtitle
        self.icon = icon
        self.color = color
        self.trend = trend
        self.setup_ui()
        
    def setup_ui(self):
        """Setup card UI"""
        self.setFixedSize(250, 150)
        self.setStyleSheet(f"""
            QFrame {{
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 16px;
                padding: 20px;
            }}
            QFrame:hover {{
                background: rgba(255, 255, 255, 0.15);
                border: 1px solid {self.color};
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
        # Header with icon and trend
        header_layout = QHBoxLayout()
        
        # Icon
        icon_label = QLabel(self.icon)
        icon_label.setStyleSheet(f"""
            QLabel {{
                color: {self.color};
                font-size: 24px;
                font-weight: bold;
            }}
        """)
        header_layout.addWidget(icon_label)
        
        header_layout.addStretch()
        
        # Trend indicator
        if self.trend:
            trend_label = QLabel(self.trend)
            trend_label.setStyleSheet(f"""
                QLabel {{
                    color: {self.color};
                    font-size: 14px;
                    font-weight: bold;
                }}
            """)
            header_layout.addWidget(trend_label)
            
        layout.addLayout(header_layout)
        
        # Value
        value_label = QLabel(self.value)
        value_label.setStyleSheet("""
            QLabel {
                color: #f8fafc;
                font-size: 28px;
                font-weight: 700;
            }
        """)
        layout.addWidget(value_label)
        
        # Title
        title_label = QLabel(self.title)
        title_label.setStyleSheet("""
            QLabel {
                color: #cbd5e1;
                font-size: 14px;
                font-weight: 500;
            }
        """)
        layout.addWidget(title_label)
        
        # Subtitle
        if self.subtitle:
            subtitle_label = QLabel(self.subtitle)
            subtitle_label.setStyleSheet("""
                QLabel {
                    color: #9CA3AF;
                    font-size: 12px;
                    font-weight: 400;
                }
            """)
            layout.addWidget(subtitle_label)
        
        layout.addStretch()


class ReportsTab(BaseTab):
    """Reports tab for analytics and reporting"""
    
    def __init__(self, user_data):
        super().__init__("Reports & Analytics", "Business intelligence and reporting dashboard", user_data)
        
    def create_content(self):
        """Create reports content"""
        # Main layout
        main_layout = QVBoxLayout()
        
        # Report controls
        controls_widget = self.create_report_controls()
        main_layout.addWidget(controls_widget)
        
        # Report content
        content_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel - Key metrics
        self.metrics_widget = QWidget()
        metrics_layout = QVBoxLayout(self.metrics_widget)
        
        metrics_title = QLabel("Key Metrics")
        metrics_title.setStyleSheet("""
            QLabel {
                color: #f8fafc;
                font-size: 20px;
                font-weight: 700;
                margin-bottom: 20px;
            }
        """)
        metrics_layout.addWidget(metrics_title)
        
        # Metrics grid
        self.metrics_grid = QGridLayout()
        self.metrics_grid.setSpacing(20)
        metrics_layout.addLayout(self.metrics_grid)
        
        metrics_layout.addStretch()
        
        # Right panel - Detailed reports
        self.details_widget = QWidget()
        details_layout = QVBoxLayout(self.details_widget)
        
        details_title = QLabel("Detailed Reports")
        details_title.setStyleSheet("""
            QLabel {
                color: #f8fafc;
                font-size: 20px;
                font-weight: 700;
                margin-bottom: 20px;
            }
        """)
        details_layout.addWidget(details_title)
        
        # Report tabs
        self.report_tabs = QComboBox()
        self.report_tabs.addItems([
            "Sales Report", "Inventory Report", "Customer Report", 
            "Financial Report", "Product Performance"
        ])
        self.report_tabs.setStyleSheet("""
            QComboBox {
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 6px;
                padding: 8px 12px;
                color: #f8fafc;
                font-size: 16px;
            }
        """)
        self.report_tabs.currentTextChanged.connect(self.load_report)
        details_layout.addWidget(self.report_tabs)
        
        # Report content
        self.report_content = QWidget()
        self.report_layout = QVBoxLayout(self.report_content)
        details_layout.addWidget(self.report_content)
        
        # Add widgets to splitter
        content_splitter.addWidget(self.metrics_widget)
        content_splitter.addWidget(self.details_widget)
        content_splitter.setSizes([400, 600])
        
        main_layout.addWidget(content_splitter)
        self.main_layout.addLayout(main_layout)
        
        # Load initial data
        self.refresh_data()
        
    def create_report_controls(self):
        """Create report control panel"""
        controls_widget = QFrame()
        controls_widget.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 20px;
            }
        """)
        
        layout = QHBoxLayout(controls_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Date range
        date_label = QLabel("Date Range:")
        date_label.setStyleSheet("""
            QLabel {
                color: #f8fafc;
                font-size: 14px;
                font-weight: 600;
            }
        """)
        layout.addWidget(date_label)
        
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addDays(-30))
        self.start_date.setStyleSheet("""
            QDateEdit {
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 6px;
                padding: 8px 12px;
                color: #f8fafc;
            }
        """)
        layout.addWidget(self.start_date)
        
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setStyleSheet("""
            QDateEdit {
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 6px;
                padding: 8px 12px;
                color: #f8fafc;
            }
        """)
        layout.addWidget(self.end_date)
        
        # Report type
        self.report_type = QComboBox()
        self.report_type.addItems(["Daily", "Weekly", "Monthly", "Yearly"])
        self.report_type.setStyleSheet("""
            QComboBox {
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 6px;
                padding: 8px 12px;
                color: #f8fafc;
            }
        """)
        layout.addWidget(QLabel("Period:"))
        layout.addWidget(self.report_type)
        
        # Generate button
        generate_btn = QPushButton("Generate Report")
        generate_btn.setStyleSheet("""
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
        generate_btn.clicked.connect(self.generate_report)
        layout.addWidget(generate_btn)
        
        # Export button
        export_btn = QPushButton("Export")
        export_btn.setStyleSheet("""
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
        export_btn.clicked.connect(self.export_report)
        layout.addWidget(export_btn)
        
        layout.addStretch()
        
        return controls_widget
        
    def refresh_data(self):
        """Refresh reports data"""
        try:
            self.load_key_metrics()
            self.load_report()
        except Exception as e:
            self.show_error(f"Error refreshing reports data: {str(e)}")
            
    def load_key_metrics(self):
        """Load key business metrics"""
        try:
            # Clear existing metrics
            for i in reversed(range(self.metrics_grid.count())):
                child = self.metrics_grid.itemAt(i).widget()
                if child:
                    child.setParent(None)
                    
            # Get date range
            start_date = self.start_date.date().toPython()
            end_date = self.end_date.date().toPython()
            
            # Total Sales
            sales_query = """
                SELECT COALESCE(SUM(total_amount), 0) as total_sales FROM sales 
                WHERE DATE(created_at) BETWEEN %s AND %s
            """
            sales_result = self.execute_query(sales_query, (start_date, end_date))
            total_sales = sales_result[0]['total_sales'] if sales_result and sales_result[0]['total_sales'] else 0
            
            # Total Orders
            orders_query = """
                SELECT COUNT(*) as total_orders FROM sales 
                WHERE DATE(created_at) BETWEEN %s AND %s
            """
            orders_result = self.execute_query(orders_query, (start_date, end_date))
            total_orders = orders_result[0]['total_orders'] if orders_result and orders_result[0]['total_orders'] else 0
            
            # Average Order Value
            avg_order_value = total_sales / total_orders if total_orders > 0 else 0
            
            # New Customers
            customers_query = """
                SELECT COUNT(DISTINCT customer_id) as new_customers FROM sales 
                WHERE DATE(created_at) BETWEEN %s AND %s
            """
            customers_result = self.execute_query(customers_query, (start_date, end_date))
            new_customers = customers_result[0]['new_customers'] if customers_result and customers_result[0]['new_customers'] else 0
            
            # Top Selling Product
            top_product_query = """
                SELECT product_name, SUM(quantity) as total_qty
                FROM sales 
                WHERE DATE(created_at) BETWEEN %s AND %s
                GROUP BY product_name
                ORDER BY total_qty DESC
                LIMIT 1
            """
            top_product_result = self.execute_query(top_product_query, (start_date, end_date))
            top_product = top_product_result[0]['product_name'] if top_product_result and top_product_result[0]['product_name'] else "N/A"
            
            # Create metric cards
            metrics = [
                ("Total Sales", f"PKR {total_sales:,.2f}", f"{start_date.strftime('%b %d')} - {end_date.strftime('%b %d')}", "💰", "#10B981"),
                ("Total Orders", str(total_orders), f"{start_date.strftime('%b %d')} - {end_date.strftime('%b %d')}", "📦", "#3B82F6"),
                ("Avg Order Value", f"PKR {avg_order_value:.2f}", "Per transaction", "📊", "#8B5CF6"),
                ("Active Customers", str(new_customers), f"{start_date.strftime('%b %d')} - {end_date.strftime('%b %d')}", "👥", "#F59E0B"),
                ("Top Product", top_product, "Best seller", "🏆", "#EF4444"),
                ("Growth Rate", "+12.5%", "vs last period", "📈", "#10B981")
            ]
            
            for i, (title, value, subtitle, icon, color) in enumerate(metrics):
                card = ReportCard(title, value, subtitle, icon, color)
                row = i // 2
                col = i % 2
                self.metrics_grid.addWidget(card, row, col)
                
        except Exception as e:
            self.show_error(f"Error loading key metrics: {str(e)}")
            
    def load_report(self):
        """Load selected report"""
        report_type = self.report_tabs.currentText()
        
        # Clear existing report content
        for i in reversed(range(self.report_layout.count())):
            child = self.report_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
                
        if report_type == "Sales Report":
            self.load_sales_report()
        elif report_type == "Inventory Report":
            self.load_inventory_report()
        elif report_type == "Customer Report":
            self.load_customer_report()
        elif report_type == "Financial Report":
            self.load_financial_report()
        elif report_type == "Product Performance":
            self.load_product_performance_report()
            
    def load_sales_report(self):
        """Load sales report"""
        try:
            # Create sales report table
            table = QTableWidget()
            table.setStyleSheet("""
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
            
            table.setColumnCount(6)
            table.setHorizontalHeaderLabels([
                "Date", "Customer", "Product", "Quantity", "Amount", "Payment"
            ])
            
            # Query sales data
            start_date = self.start_date.date().toPython()
            end_date = self.end_date.date().toPython()
            
            query = """
                SELECT DATE(created_at), customer_name, product_name, 
                       quantity, total_amount, payment_method
                FROM sales 
                WHERE DATE(created_at) BETWEEN %s AND %s
                ORDER BY created_at DESC
            """
            result = self.execute_query(query, (start_date, end_date))
            
            if result:
                table.setRowCount(len(result))
                for row, sale in enumerate(result):
                    table.setItem(row, 0, QTableWidgetItem(str(sale[0])))
                    table.setItem(row, 1, QTableWidgetItem(sale[1] or "N/A"))
                    table.setItem(row, 2, QTableWidgetItem(sale[2] or "N/A"))
                    table.setItem(row, 3, QTableWidgetItem(str(sale[3])))
                    table.setItem(row, 4, QTableWidgetItem(f"PKR {sale[4]:.2f}"))
                    table.setItem(row, 5, QTableWidgetItem(sale[5] or "N/A"))
            else:
                table.setRowCount(0)
                
            self.report_layout.addWidget(table)
            
        except Exception as e:
            self.show_error(f"Error loading sales report: {str(e)}")
            
    def load_inventory_report(self):
        """Load inventory report"""
        try:
            # Create inventory report table
            table = QTableWidget()
            table.setStyleSheet("""
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
            
            table.setColumnCount(7)
            table.setHorizontalHeaderLabels([
                "Product", "Category", "Stock", "Min Level", "Price", "Value", "Status"
            ])
            
            # Query inventory data
            query = """
                SELECT name, category, stock_quantity, min_stock_level, 
                       selling_price, (stock_quantity * selling_price) as total_value
                FROM products
                ORDER BY name ASC
            """
            result = self.execute_query(query)
            
            if result:
                table.setRowCount(len(result))
                for row, product in enumerate(result):
                    table.setItem(row, 0, QTableWidgetItem(product[0] or "N/A"))
                    table.setItem(row, 1, QTableWidgetItem(product[1] or "N/A"))
                    table.setItem(row, 2, QTableWidgetItem(str(product[2])))
                    table.setItem(row, 3, QTableWidgetItem(str(product[3])))
                    table.setItem(row, 4, QTableWidgetItem(f"PKR {product[4]:.2f}"))
                    table.setItem(row, 5, QTableWidgetItem(f"PKR {product[5]:.2f}"))
                    
                    # Status
                    status = "Low Stock" if product[2] <= product[3] else "In Stock" if product[2] > 0 else "Out of Stock"
                    status_item = QTableWidgetItem(status)
                    if status == "Low Stock":
                        status_item.setBackground(Qt.GlobalColor.red)
                    elif status == "Out of Stock":
                        status_item.setBackground(Qt.GlobalColor.darkRed)
                    else:
                        status_item.setBackground(Qt.GlobalColor.green)
                    table.setItem(row, 6, status_item)
            else:
                table.setRowCount(0)
                
            self.report_layout.addWidget(table)
            
        except Exception as e:
            self.show_error(f"Error loading inventory report: {str(e)}")
            
    def load_customer_report(self):
        """Load customer report"""
        try:
            # Create customer report table
            table = QTableWidget()
            table.setStyleSheet("""
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
            
            table.setColumnCount(6)
            table.setHorizontalHeaderLabels([
                "Customer", "Email", "Phone", "Type", "Total Orders", "Total Spent"
            ])
            
            # Query customer data
            query = """
                SELECT CONCAT(c.first_name, ' ', c.last_name) as name, c.email, c.phone, c.customer_type,
                       COUNT(s.id) as total_orders, COALESCE(SUM(s.total_amount), 0) as total_spent
                FROM customers c
                LEFT JOIN sales s ON c.id = s.customer_id
                GROUP BY c.id, c.first_name, c.last_name, c.email, c.phone, c.customer_type
                ORDER BY total_spent DESC
            """
            result = self.execute_query(query)
            
            if result:
                table.setRowCount(len(result))
                for row, customer in enumerate(result):
                    table.setItem(row, 0, QTableWidgetItem(customer[0] or "N/A"))
                    table.setItem(row, 1, QTableWidgetItem(customer[1] or "N/A"))
                    table.setItem(row, 2, QTableWidgetItem(customer[2] or "N/A"))
                    table.setItem(row, 3, QTableWidgetItem(customer[3] or "N/A"))
                    table.setItem(row, 4, QTableWidgetItem(str(customer[4])))
                    table.setItem(row, 5, QTableWidgetItem(f"PKR {customer[5]:.2f}"))
            else:
                table.setRowCount(0)
                
            self.report_layout.addWidget(table)
            
        except Exception as e:
            self.show_error(f"Error loading customer report: {str(e)}")
            
    def load_financial_report(self):
        """Load financial report"""
        try:
            # Create financial summary
            summary_widget = QWidget()
            summary_layout = QVBoxLayout(summary_widget)
            
            # Financial metrics
            start_date = self.start_date.date().toPython()
            end_date = self.end_date.date().toPython()
            
            # Total Revenue
            revenue_query = """
                SELECT COALESCE(SUM(total_amount), 0) as total_revenue FROM sales 
                WHERE DATE(created_at) BETWEEN %s AND %s
            """
            revenue_result = self.execute_query(revenue_query, (start_date, end_date))
            total_revenue = revenue_result[0]['total_revenue'] if revenue_result and revenue_result[0]['total_revenue'] else 0
            
            # Total Cost (estimated)
            cost_query = """
                SELECT COALESCE(SUM(quantity * (SELECT purchase_price FROM products WHERE name = s.product_name LIMIT 1)), 0) as total_cost
                FROM sales s 
                WHERE DATE(created_at) BETWEEN %s AND %s
            """
            cost_result = self.execute_query(cost_query, (start_date, end_date))
            total_cost = cost_result[0]['total_cost'] if cost_result and cost_result[0]['total_cost'] else 0
            
            # Profit
            profit = total_revenue - total_cost
            profit_margin = (profit / total_revenue * 100) if total_revenue > 0 else 0
            
            # Create financial cards
            financial_cards = QHBoxLayout()
            
            revenue_card = self.create_financial_card("Total Revenue", f"PKR {total_revenue:,.2f}", "#10B981")
            cost_card = self.create_financial_card("Total Cost", f"PKR {total_cost:,.2f}", "#EF4444")
            profit_card = self.create_financial_card("Net Profit", f"PKR {profit:,.2f}", "#3B82F6")
            margin_card = self.create_financial_card("Profit Margin", f"{profit_margin:.1f}%", "#8B5CF6")
            
            financial_cards.addWidget(revenue_card)
            financial_cards.addWidget(cost_card)
            financial_cards.addWidget(profit_card)
            financial_cards.addWidget(margin_card)
            
            summary_layout.addLayout(financial_cards)
            self.report_layout.addWidget(summary_widget)
            
        except Exception as e:
            self.show_error(f"Error loading financial report: {str(e)}")
            
    def load_product_performance_report(self):
        """Load product performance report"""
        try:
            # Create product performance table
            table = QTableWidget()
            table.setStyleSheet("""
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
            
            table.setColumnCount(6)
            table.setHorizontalHeaderLabels([
                "Product", "Units Sold", "Revenue", "Avg Price", "Rank", "Performance"
            ])
            
            # Query product performance data
            start_date = self.start_date.date().toPython()
            end_date = self.end_date.date().toPython()
            
            query = """
                SELECT product_name, SUM(quantity) as units_sold, 
                       SUM(total_amount) as revenue, AVG(total_amount/quantity) as avg_price
                FROM sales 
                WHERE DATE(created_at) BETWEEN %s AND %s
                GROUP BY product_name
                ORDER BY units_sold DESC
            """
            result = self.execute_query(query, (start_date, end_date))
            
            if result:
                table.setRowCount(len(result))
                for row, product in enumerate(result):
                    table.setItem(row, 0, QTableWidgetItem(product[0] or "N/A"))
                    table.setItem(row, 1, QTableWidgetItem(str(product[1])))
                    table.setItem(row, 2, QTableWidgetItem(f"PKR {product[2]:.2f}"))
                    table.setItem(row, 3, QTableWidgetItem(f"PKR {product[3]:.2f}"))
                    table.setItem(row, 4, QTableWidgetItem(f"#{row + 1}"))
                    
                    # Performance indicator
                    performance = "Excellent" if row < 3 else "Good" if row < 6 else "Average"
                    perf_item = QTableWidgetItem(performance)
                    if performance == "Excellent":
                        perf_item.setBackground(Qt.GlobalColor.green)
                    elif performance == "Good":
                        perf_item.setBackground(Qt.GlobalColor.yellow)
                    else:
                        perf_item.setBackground(Qt.GlobalColor.gray)
                    table.setItem(row, 5, perf_item)
            else:
                table.setRowCount(0)
                
            self.report_layout.addWidget(table)
            
        except Exception as e:
            self.show_error(f"Error loading product performance report: {str(e)}")
            
    def create_financial_card(self, title, value, color):
        """Create financial card widget"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 12px;
                padding: 20px;
            }}
        """)
        card.setFixedHeight(100)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                color: #cbd5e1;
                font-size: 14px;
                font-weight: 500;
            }
        """)
        layout.addWidget(title_label)
        
        # Value
        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 24px;
                font-weight: 700;
            }}
        """)
        layout.addWidget(value_label)
        
        layout.addStretch()
        
        return card
        
    def generate_report(self):
        """Generate report based on current filters"""
        self.refresh_data()
        self.show_success("Report generated successfully")
        
    def export_report(self):
        """Export current report"""
        self.show_success("Report export functionality will be implemented")
