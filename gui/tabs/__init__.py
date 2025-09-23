"""
SSMS Tabs Module
Contains all tab implementations for the Sales & Stock Management System
"""

from .dashboard import DashboardTab
from .sales import SalesTab
from .inventory import InventoryTab
from .customers import CustomersTab
from .reports import ReportsTab
from .settings import SettingsTab
from .purchases import PurchasesTab
from .tools import ToolsTab

__all__ = [
    'DashboardTab',
    'SalesTab', 
    'InventoryTab',
    'CustomersTab',
    'ReportsTab',
    'SettingsTab',
    'PurchasesTab',
    'ToolsTab'
]
