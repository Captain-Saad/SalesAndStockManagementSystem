"""
Database Schema Setup for SSMS
Creates all necessary tables and initial data
"""

import sys
import os
from db_connection import DatabaseConnection


def create_database_schema():
    """Create complete database schema"""
    print("🗄️ Creating SSMS Database Schema...")
    print("=" * 50)
    
    try:
        db = DatabaseConnection()
        
        if not db.test_connection():
            print("❌ Database connection failed")
            return False
            
        print("✅ Database connected successfully")
        
        # Create tables
        tables_created = create_tables(db)
        
        if tables_created:
            print("✅ All tables created successfully")
            
            # Insert initial data
            insert_initial_data(db)
            
            print("✅ Initial data inserted successfully")
            print("🎉 Database schema setup completed!")
            return True
        else:
            print("❌ Failed to create tables")
            return False
            
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        return False


def create_tables(db):
    """Create all database tables"""
    tables = [
        # Users table
        """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            role ENUM('Admin', 'Manager', 'Employee') DEFAULT 'Employee',
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            phone VARCHAR(20),
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """,
        
        # Customers table
        """
        CREATE TABLE IF NOT EXISTS customers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE,
            phone VARCHAR(20),
            address TEXT,
            city VARCHAR(50),
            state VARCHAR(50),
            pincode VARCHAR(10),
            customer_type ENUM('Individual', 'Business', 'Wholesale', 'Retail') DEFAULT 'Individual',
            credit_limit DECIMAL(10,2) DEFAULT 0.00,
            notes TEXT,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """,
        
        # Categories table
        """
        CREATE TABLE IF NOT EXISTS categories (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL,
            description TEXT,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        
        # Products table
        """
        CREATE TABLE IF NOT EXISTS products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            sku VARCHAR(50) UNIQUE,
            category VARCHAR(50),
            description TEXT,
            purchase_price DECIMAL(10,2) DEFAULT 0.00,
            selling_price DECIMAL(10,2) DEFAULT 0.00,
            stock_quantity INT DEFAULT 0,
            min_stock_level INT DEFAULT 0,
            unit VARCHAR(20) DEFAULT 'Pieces',
            supplier VARCHAR(100),
            barcode VARCHAR(50),
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """,
        
        # Sales table
        """
        CREATE TABLE IF NOT EXISTS sales (
            id INT AUTO_INCREMENT PRIMARY KEY,
            customer_id INT,
            customer_name VARCHAR(100),
            product_id INT,
            product_name VARCHAR(100),
            quantity INT NOT NULL,
            unit_price DECIMAL(10,2) NOT NULL,
            total_amount DECIMAL(10,2) NOT NULL,
            discount_amount DECIMAL(10,2) DEFAULT 0.00,
            tax_amount DECIMAL(10,2) DEFAULT 0.00,
            payment_method ENUM('Cash', 'Card', 'UPI', 'Bank Transfer', 'Cheque') DEFAULT 'Cash',
            payment_status ENUM('Pending', 'Paid', 'Partially Paid', 'Refunded') DEFAULT 'Paid',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE SET NULL,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE SET NULL
        )
        """,
        
        # Purchases table
        """
        CREATE TABLE IF NOT EXISTS purchases (
            id INT AUTO_INCREMENT PRIMARY KEY,
            supplier_name VARCHAR(100) NOT NULL,
            product_id INT,
            product_name VARCHAR(100),
            quantity INT NOT NULL,
            unit_price DECIMAL(10,2) NOT NULL,
            total_amount DECIMAL(10,2) NOT NULL,
            purchase_date DATE NOT NULL,
            payment_method ENUM('Cash', 'Card', 'Bank Transfer', 'Cheque') DEFAULT 'Bank Transfer',
            payment_status ENUM('Pending', 'Paid', 'Partially Paid') DEFAULT 'Pending',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE SET NULL
        )
        """,
        
        # Stock movements table
        """
        CREATE TABLE IF NOT EXISTS stock_movements (
            id INT AUTO_INCREMENT PRIMARY KEY,
            product_id INT NOT NULL,
            movement_type ENUM('IN', 'OUT', 'ADJUSTMENT') NOT NULL,
            quantity INT NOT NULL,
            reference_type ENUM('SALE', 'PURCHASE', 'ADJUSTMENT', 'RETURN') NOT NULL,
            reference_id INT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
        )
        """,
        
        # Suppliers table
        """
        CREATE TABLE IF NOT EXISTS suppliers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            contact_person VARCHAR(50),
            email VARCHAR(100),
            phone VARCHAR(20),
            address TEXT,
            city VARCHAR(50),
            state VARCHAR(50),
            pincode VARCHAR(10),
            payment_terms VARCHAR(100),
            notes TEXT,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """,
        
        # Audit log table
        """
        CREATE TABLE IF NOT EXISTS audit_log (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            action VARCHAR(100) NOT NULL,
            table_name VARCHAR(50),
            record_id INT,
            old_values JSON,
            new_values JSON,
            ip_address VARCHAR(45),
            user_agent TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
        )
        """,
        
        # Settings table
        """
        CREATE TABLE IF NOT EXISTS settings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            setting_key VARCHAR(100) UNIQUE NOT NULL,
            setting_value TEXT,
            setting_type ENUM('STRING', 'NUMBER', 'BOOLEAN', 'JSON') DEFAULT 'STRING',
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
    ]
    
    try:
        for i, table_sql in enumerate(tables, 1):
            print(f"Creating table {i}/{len(tables)}...")
            db.execute_query(table_sql)
            
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False


def insert_initial_data(db):
    """Insert initial data into tables"""
    try:
        # Insert admin user
        admin_query = """
            INSERT IGNORE INTO users (username, password, email, role, first_name, last_name, is_active)
            VALUES ('admin', 'admin123', 'admin@ssms.com', 'Admin', 'System', 'Administrator', TRUE)
        """
        db.execute_query(admin_query)
        print("✅ Admin user created")
        
        # Insert sample categories
        categories = [
            ("Electronics", "Electronic devices and accessories"),
            ("Clothing", "Apparel and fashion items"),
            ("Food & Beverages", "Food and drink products"),
            ("Books", "Books and educational materials"),
            ("Home & Garden", "Home improvement and garden supplies"),
            ("Sports", "Sports equipment and accessories")
        ]
        
        for name, desc in categories:
            category_query = """
                INSERT IGNORE INTO categories (name, description)
                VALUES (%s, %s)
            """
            db.execute_query(category_query, (name, desc))
        print("✅ Sample categories created")
        
        # Insert sample products
        products = [
            ("Laptop", "LAP001", "Electronics", "High-performance laptop", 50000.00, 65000.00, 10, 2, "Pieces", "Tech Supplier"),
            ("T-Shirt", "TSH001", "Clothing", "Cotton t-shirt", 200.00, 500.00, 50, 10, "Pieces", "Fashion Supplier"),
            ("Coffee", "COF001", "Food & Beverages", "Premium coffee beans", 300.00, 450.00, 25, 5, "Kg", "Food Supplier"),
            ("Python Book", "BOK001", "Books", "Python programming guide", 400.00, 600.00, 15, 3, "Pieces", "Book Supplier"),
            ("Garden Tools", "GAR001", "Home & Garden", "Complete garden tool set", 1500.00, 2000.00, 8, 2, "Set", "Garden Supplier")
        ]
        
        for name, sku, category, desc, purchase_price, selling_price, stock, min_stock, unit, supplier in products:
            product_query = """
                INSERT IGNORE INTO products (name, sku, category, description, purchase_price, selling_price, stock_quantity, min_stock_level, unit, supplier)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            db.execute_query(product_query, (name, sku, category, desc, purchase_price, selling_price, stock, min_stock, unit, supplier))
        print("✅ Sample products created")
        
        # Insert sample customers
        customers = [
            ("John Doe", "john@example.com", "9876543210", "123 Main St", "Mumbai", "Maharashtra", "400001", "Individual", 10000.00),
            ("ABC Company", "contact@abc.com", "9876543211", "456 Business Ave", "Delhi", "Delhi", "110001", "Business", 50000.00),
            ("Jane Smith", "jane@example.com", "9876543212", "789 Residential Rd", "Bangalore", "Karnataka", "560001", "Individual", 5000.00)
        ]
        
        for name, email, phone, address, city, state, pincode, customer_type, credit_limit in customers:
            customer_query = """
                INSERT IGNORE INTO customers (name, email, phone, address, city, state, pincode, customer_type, credit_limit)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            db.execute_query(customer_query, (name, email, phone, address, city, state, pincode, customer_type, credit_limit))
        print("✅ Sample customers created")
        
        # Insert sample suppliers
        suppliers = [
            ("Tech Supplier", "Raj Kumar", "raj@techsupplier.com", "9876543213", "Tech Park", "Mumbai", "Maharashtra", "400002", "Net 30"),
            ("Fashion Supplier", "Priya Singh", "priya@fashionsupplier.com", "9876543214", "Fashion District", "Delhi", "Delhi", "110002", "Net 15"),
            ("Food Supplier", "Amit Patel", "amit@foodsupplier.com", "9876543215", "Food Market", "Bangalore", "Karnataka", "560002", "Net 7")
        ]
        
        for name, contact_person, email, phone, address, city, state, pincode, payment_terms in suppliers:
            supplier_query = """
                INSERT IGNORE INTO suppliers (name, contact_person, email, phone, address, city, state, pincode, payment_terms)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            db.execute_query(supplier_query, (name, contact_person, email, phone, address, city, state, pincode, payment_terms))
        print("✅ Sample suppliers created")
        
        # Insert sample sales
        sales = [
            (1, "John Doe", 1, "Laptop", 1, 65000.00, 65000.00, "Card", "Paid"),
            (2, "ABC Company", 2, "T-Shirt", 10, 500.00, 5000.00, "Bank Transfer", "Paid"),
            (3, "Jane Smith", 3, "Coffee", 2, 450.00, 900.00, "UPI", "Paid")
        ]
        
        for customer_id, customer_name, product_id, product_name, quantity, unit_price, total_amount, payment_method, payment_status in sales:
            sale_query = """
                INSERT IGNORE INTO sales (customer_id, customer_name, product_id, product_name, quantity, unit_price, total_amount, payment_method, payment_status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            db.execute_query(sale_query, (customer_id, customer_name, product_id, product_name, quantity, unit_price, total_amount, payment_method, payment_status))
        print("✅ Sample sales created")
        
        # Insert default settings
        settings = [
            ("company_name", "SSMS Solutions", "STRING", "Company name"),
            ("currency", "₹", "STRING", "Default currency symbol"),
            ("timezone", "Asia/Kolkata", "STRING", "Default timezone"),
            ("date_format", "DD/MM/YYYY", "STRING", "Date display format"),
            ("auto_backup", "true", "BOOLEAN", "Enable automatic backup"),
            ("session_timeout", "30", "NUMBER", "Session timeout in minutes")
        ]
        
        for key, value, value_type, description in settings:
            setting_query = """
                INSERT IGNORE INTO settings (setting_key, setting_value, setting_type, description)
                VALUES (%s, %s, %s, %s)
            """
            db.execute_query(setting_query, (key, value, value_type, description))
        print("✅ Default settings created")
        
        return True
        
    except Exception as e:
        print(f"❌ Error inserting initial data: {e}")
        return False


if __name__ == "__main__":
    success = create_database_schema()
    if success:
        print("\n🎉 Database setup completed successfully!")
        print("You can now run the SSMS application.")
    else:
        print("\n❌ Database setup failed!")
        sys.exit(1)
