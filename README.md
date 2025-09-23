# Sales and Stock Management System (SSMS)

A modern, ultra-sleek Sales and Stock Management System built with Python and PyQt6, featuring a beautiful glass-morphism UI design.

## ✨ Features

### 🎨 **Ultra-Modern UI Design**
- **Glass-morphism Design**: Transparent, glossy glass effect throughout the application
- **Purple Gradient Theme**: Consistent purple gradient background matching the login window
- **Clean Card Layout**: Modern card-based interface with transparent backgrounds
- **Responsive Design**: Optimized for different screen sizes

### 📊 **Core Functionality**
- **Dashboard**: Real-time metrics and key performance indicators
- **Sales Management**: Complete sales tracking and management
- **Customer Management**: Customer database and relationship management
- **Inventory Management**: Product stock tracking and management
- **Purchase Management**: Purchase orders and supplier management
- **Reports**: Comprehensive reporting system
- **Settings**: System configuration and user preferences
- **Tools**: Additional utilities and maintenance tools

### 🔧 **Technical Features**
- **Database Integration**: MySQL/MariaDB database support
- **User Authentication**: Secure login system with role-based access
- **Real-time Updates**: Live data refresh and synchronization
- **Error Handling**: Comprehensive error handling and logging
- **Modular Architecture**: Clean, maintainable code structure

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- MySQL/MariaDB database
- Required Python packages (see requirements.txt)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/saadk/SalesAndStockManagementSystem.git
   cd SalesAndStockManagementSystem
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Database Setup**
   - Create a MySQL/MariaDB database
   - Update database configuration in `config.py`
   - Run the application to auto-create tables

4. **Launch the Application**
   ```bash
   python main.py
   ```
   
   Or use the batch file:
   ```bash
   launch_ssms.bat
   ```

### Default Login Credentials
- **Username**: `admin`
- **Password**: `admin123`

## 📁 Project Structure

```
SalesAndStockManagementSystem/
├── gui/                    # GUI components
│   ├── tabs/              # Application tabs
│   │   ├── dashboard.py   # Dashboard with metrics
│   │   ├── sales.py       # Sales management
│   │   ├── customers.py   # Customer management
│   │   ├── inventory.py   # Inventory management
│   │   ├── purchases.py   # Purchase management
│   │   ├── reports.py     # Reporting system
│   │   ├── settings.py    # Settings and configuration
│   │   ├── tools.py       # Additional tools
│   │   └── base_tab.py    # Base tab class
│   ├── ultra_login.py     # Modern login window
│   └── ultra_main.py      # Main application window
├── config.py              # Configuration settings
├── database_schema.py     # Database schema definitions
├── db_connection.py       # Database connection handler
├── main.py               # Application entry point
├── requirements.txt      # Python dependencies
├── settings.json         # Application settings
├── launch_ssms.bat      # Windows batch launcher
└── README.md            # This file
```

## 🎯 Key Features

### Dashboard
- **Key Metrics**: Total sales, orders, customers, and inventory
- **Quick Stats**: Low stock alerts, pending orders, monthly revenue
- **Real-time Updates**: Live data refresh every few seconds
- **Clean Cards**: Transparent glass-effect cards with hover animations

### Sales Management
- **Sales Tracking**: Complete sales transaction management
- **Customer Integration**: Link sales to customer records
- **Product Integration**: Track product sales and inventory
- **Date Filtering**: Filter sales by date ranges

### Customer Management
- **Customer Database**: Complete customer information management
- **Contact Details**: Phone, email, and address tracking
- **Sales History**: View customer purchase history
- **Search & Filter**: Advanced customer search capabilities

### Inventory Management
- **Product Catalog**: Complete product database
- **Stock Tracking**: Real-time inventory levels
- **Supplier Information**: Track product suppliers
- **Low Stock Alerts**: Automatic low stock notifications

### Purchase Management
- **Purchase Orders**: Create and manage purchase orders
- **Supplier Management**: Supplier database and tracking
- **Demand Tracking**: Track product demand and reorder points
- **Multi-tab Interface**: Organized purchase workflow

## 🎨 UI Design Philosophy

The application features a **glass-morphism design** with:
- **Transparent Backgrounds**: All cards and tables use transparent backgrounds
- **Subtle Borders**: Minimal borders with low opacity for definition
- **Purple Gradient**: Consistent purple gradient theme throughout
- **Clean Typography**: Modern, readable fonts with proper spacing
- **Hover Effects**: Subtle animations and hover states
- **Responsive Layout**: Adapts to different screen sizes

## 🔧 Configuration

### Database Configuration
Update `config.py` with your database settings:
```python
DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'ssms_database'
}
```

### Application Settings
Modify `settings.json` for application preferences:
```json
{
    "theme": "purple",
    "auto_refresh": true,
    "refresh_interval": 5000
}
```

## 📊 Database Schema

The application uses the following main tables:
- `users` - User authentication and roles
- `customers` - Customer information
- `products` - Product catalog
- `sales` - Sales transactions
- `purchases` - Purchase orders
- `suppliers` - Supplier information

## 🚀 Performance Features

- **Efficient Database Queries**: Optimized SQL queries for fast data retrieval
- **Lazy Loading**: Load data only when needed
- **Caching**: Smart caching for frequently accessed data
- **Background Processing**: Non-blocking UI operations

## 🛠️ Development

### Adding New Features
1. Create new tab classes inheriting from `BaseTab`
2. Add database schema changes to `database_schema.py`
3. Update the main window to include new tabs
4. Test thoroughly with sample data

### Code Style
- Follow PEP 8 guidelines
- Use type hints where appropriate
- Document functions and classes
- Maintain consistent naming conventions

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review the code comments

## 🎉 Acknowledgments

- Built with Python and PyQt6
- Glass-morphism design inspiration from modern UI trends
- Database integration with MySQL/MariaDB
- Modern Python development practices

---

**Sales and Stock Management System** - A modern, efficient, and beautiful business management solution.
