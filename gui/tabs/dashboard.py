from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from .base_tab import BaseTab
import json
from datetime import datetime, timedelta


class CleanCard(QWidget):
    """Ultra-clean card widget"""
    
    def __init__(self, title, value, icon, color):
        super().__init__()
        self.title = title
        self.value = value
        self.icon = icon
        self.color = color
        self.setup_ui()
        
    def setup_ui(self):
        self.setFixedSize(400, 160)
        self.setStyleSheet(f"""
            QWidget {{
                background: transparent;
                border: 2px solid {self.color};
                border-radius: 15px;
                border-left: 8px solid {self.color};
            }}
            QWidget:hover {{
                border-left: 8px solid {self.color};
                background: transparent;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(12)
        
        # Title
        title_label = QLabel(self.title)
        title_label.setStyleSheet("""
            QLabel {
                color: #f8fafc;
                font-size: 18px;
                font-weight: 600;
                padding: 0;
                margin: 0;
            }
        """)
        layout.addWidget(title_label)
        
        # Value and icon row
        value_layout = QHBoxLayout()
        value_layout.setContentsMargins(0, 0, 0, 0)
        value_layout.setSpacing(15)
        
        value_label = QLabel(self.value)
        value_label.setStyleSheet(f"""
            QLabel {{
                color: {self.color};
                font-size: 32px;
                font-weight: 700;
                padding: 0;
                margin: 0;
            }}
        """)
        value_layout.addWidget(value_label)
        
        value_layout.addStretch()
        
        icon_label = QLabel(self.icon)
        icon_label.setStyleSheet("""
            QLabel {
                color: #94a3b8;
                font-size: 28px;
                padding: 0;
                margin: 0;
            }
        """)
        value_layout.addWidget(icon_label)
        
        layout.addLayout(value_layout)


class DashboardTab(BaseTab):
    """Clean, modern dashboard tab"""
    
    def __init__(self, user_data, parent=None):
        super().__init__("Dashboard Overview", "Real-time analytics and insights", user_data)
        # Set proper margins for the main layout
        self.main_layout.setContentsMargins(0, 0, 0, 20)
        self.main_layout.setSpacing(0)
        # Set background to match main UI theme
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #1e293b, stop:1 #334155);
                color: #f8fafc;
            }
        """)
        
    def create_content(self):
        """Override create_content to add our dashboard content"""
        # Key metrics cards in a clean grid
        self.create_metrics_section()
        
        # Quick stats row
        self.create_quick_stats_section()
        
        # Load data after UI is created (with a small delay to ensure UI is ready)
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(100, self.refresh_data)
        
        self.main_layout.addStretch()
        
    def refresh_data(self):
        """Refresh dashboard data with clean cards"""
        print("🔄 Refreshing dashboard data...")
        
        try:
            # Get stats data
            stats_data = self.get_dashboard_stats()
            print(f"Dashboard data: Sales={stats_data[0][1]}, Orders={stats_data[1][1]}, Customers={stats_data[2][1]}, Inventory={stats_data[3][1]}")
            
            # Clear existing cards
            for card in self.cards:
                card.deleteLater()
            self.cards.clear()
            
            # Create new clean cards with proper data
            for i, (title, value, icon, color) in enumerate(stats_data):
                print(f"Creating card {i}: {title} = {value}")
                card = CleanCard(title, value, icon, color)
                row = i // 2
                col = i % 2
                self.metrics_layout.addWidget(card, row, col)
                self.cards.append(card)
                
            print("✅ Clean cards created successfully!")
            
        except Exception as e:
            print(f"❌ Error refreshing dashboard: {e}")
            import traceback
            traceback.print_exc()
    
    def get_dashboard_stats(self):
        """Get dashboard statistics from database"""
        try:
            # Total sales (all time)
            sales_query = """
                SELECT COALESCE(SUM(total_amount), 0) as total_sales
                FROM sales
            """
            sales_result = self.execute_query(sales_query)
            total_sales = sales_result[0]['total_sales'] if sales_result and sales_result[0] else 0
            
            # Total orders (all time)
            orders_query = "SELECT COUNT(*) as total_orders FROM sales"
            orders_result = self.execute_query(orders_query)
            total_orders = orders_result[0]['total_orders'] if orders_result and orders_result[0] else 0
            
            # Total customers
            customers_query = "SELECT COUNT(*) as total_customers FROM customers"
            customers_result = self.execute_query(customers_query)
            total_customers = customers_result[0]['total_customers'] if customers_result and customers_result[0] else 0
            
            # In stock items
            inventory_query = "SELECT COUNT(*) as in_stock FROM products WHERE stock_quantity > 0"
            inventory_result = self.execute_query(inventory_query)
            in_stock_items = inventory_result[0]['in_stock'] if inventory_result and inventory_result[0] else 0
            
            print(f"Dashboard stats: Sales={total_sales}, Orders={total_orders}, Customers={total_customers}, Stock={in_stock_items}")
            
            return [
                ("Total Sales", f"PKR {total_sales:,.2f}", "💰", "#10b981"),
                ("Total Orders", str(total_orders), "📦", "#3b82f6"),
                ("Customers", str(total_customers), "👥", "#8b5cf6"),
                ("In Stock", str(in_stock_items), "📦", "#f59e0b")
            ]
            
        except Exception as e:
            print(f"❌ Error getting dashboard stats: {e}")
            return [
                ("Total Sales", "PKR 0.00", "💰", "#10b981"),
                ("Total Orders", "0", "📦", "#3b82f6"),
                ("Customers", "0", "👥", "#8b5cf6"),
                ("In Stock", "0", "📦", "#f59e0b")
            ]
    
    
    def create_metrics_section(self):
        """Create key metrics cards section"""
        # Section title
        section_title = QLabel("Key Metrics")
        section_title.setStyleSheet("""
            QLabel {
                color: #f8fafc;
                font-size: 16px;
                font-weight: 600;
                padding: 8px 15px;
                margin: 0;
            }
        """)
        self.main_layout.addWidget(section_title)
        
        # Metrics container
        metrics_container = QWidget()
        metrics_container.setStyleSheet("""
            QWidget {
                background: transparent;
            }
        """)
        
        metrics_layout = QGridLayout(metrics_container)
        metrics_layout.setSpacing(50)
        metrics_layout.setContentsMargins(50, 40, 50, 50)
        # Set column stretch to prevent overlapping
        metrics_layout.setColumnStretch(0, 1)
        metrics_layout.setColumnStretch(1, 1)
        # Set row stretch to prevent overlapping
        metrics_layout.setRowStretch(0, 1)
        metrics_layout.setRowStretch(1, 1)
        
        # Create cards
        self.cards = []
        self.metrics_layout = metrics_layout
        self.metrics_container = metrics_container
        
        self.main_layout.addWidget(metrics_container)
    
    def create_quick_stats_section(self):
        """Create quick stats section"""
        # Section title
        section_title = QLabel("Quick Stats")
        section_title.setStyleSheet("""
            QLabel {
                color: #f8fafc;
                font-size: 16px;
                font-weight: 600;
                padding: 8px 15px;
                margin: 15px 0 8px 0;
            }
        """)
        self.main_layout.addWidget(section_title)
        
        # Stats container
        stats_container = QWidget()
        stats_container.setStyleSheet("""
            QWidget {
                background: transparent;
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 15px;
                margin: 0 30px;
            }
        """)
        
        stats_layout = QHBoxLayout(stats_container)
        stats_layout.setSpacing(50)
        stats_layout.setContentsMargins(40, 30, 40, 30)
        
        # Get quick stats
        quick_stats = self.get_quick_stats()
        for stat in quick_stats:
            stat_widget = QWidget()
            stat_widget.setStyleSheet("""
                QWidget {
                    background: transparent;
                    border: 2px solid rgba(255, 255, 255, 0.1);
                    border-radius: 12px;
                    padding: 15px;
                }
            """)
            
            stat_layout = QVBoxLayout(stat_widget)
            stat_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            stat_layout.setSpacing(5)
            
            # Value
            value_label = QLabel(stat['value'])
            value_label.setStyleSheet(f"""
                QLabel {{
                    color: {stat['color']};
                    font-size: 20px;
                    font-weight: 700;
                    padding: 0;
                    margin: 0;
                }}
            """)
            value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            stat_layout.addWidget(value_label)
            
            # Label
            label_label = QLabel(stat['label'])
            label_label.setStyleSheet("""
                QLabel {
                    color: #94a3b8;
                    font-size: 12px;
                    font-weight: 500;
                    padding: 0;
                    margin: 0;
                }
            """)
            label_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            stat_layout.addWidget(label_label)
            
            stats_layout.addWidget(stat_widget)
        
        self.main_layout.addWidget(stats_container)
    
    
    def get_quick_stats(self):
        """Get quick stats for the stats section"""
        try:
            # Low stock items
            low_stock_query = "SELECT COUNT(*) as low_stock FROM products WHERE stock_quantity < 10"
            low_stock_result = self.execute_query(low_stock_query)
            low_stock = low_stock_result[0]['low_stock'] if low_stock_result and low_stock_result[0] else 0
            
            # Pending purchases
            pending_purchases_query = "SELECT COUNT(*) as pending FROM purchases WHERE payment_status = 'Pending'"
            pending_result = self.execute_query(pending_purchases_query)
            pending_purchases = pending_result[0]['pending'] if pending_result and pending_result[0] else 0
            
            # This month's sales
            monthly_sales_query = """
                SELECT COALESCE(SUM(total_amount), 0) as monthly_sales FROM sales 
                WHERE MONTH(sale_date) = MONTH(CURRENT_DATE()) 
                AND YEAR(sale_date) = YEAR(CURRENT_DATE())
            """
            monthly_result = self.execute_query(monthly_sales_query)
            monthly_sales = monthly_result[0]['monthly_sales'] if monthly_result and monthly_result[0] else 0
            
            print(f"Quick stats: Low stock={low_stock}, Pending={pending_purchases}, Monthly={monthly_sales}")
            
            return [
                {"label": "Low Stock Items", "value": str(low_stock), "color": "#f59e0b"},
                {"label": "Pending Purchases", "value": str(pending_purchases), "color": "#ef4444"},
                {"label": "This Month", "value": f"PKR {monthly_sales:,.0f}", "color": "#10b981"}
            ]
        except Exception as e:
            print(f"❌ Error getting quick stats: {e}")
            return [
                {"label": "Low Stock Items", "value": "0", "color": "#f59e0b"},
                {"label": "Pending Purchases", "value": "0", "color": "#ef4444"},
                {"label": "This Month", "value": "PKR 0", "color": "#10b981"}
            ]
    
    def get_recent_sales(self):
        """Get recent sales for activity feed"""
        try:
            query = """
                SELECT s.customer_name, s.product_name, s.total_amount, s.sale_date
                FROM sales s
                ORDER BY s.sale_date DESC
                LIMIT 5
            """
            result = self.execute_query(query)
            print(f"Recent sales: {len(result) if result else 0} records")
            return result if result else []
        except Exception as e:
            print(f"❌ Error getting recent sales: {e}")
            return []