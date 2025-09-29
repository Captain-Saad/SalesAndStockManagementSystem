"""
Barcode Scanner Utility for SSMS
Supports barcode scanning, QR code generation, and product lookup
"""

import cv2
import numpy as np
from pyzbar import pyzbar
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QLineEdit, QTextEdit, QMessageBox,
                            QComboBox, QSpinBox, QFormLayout, QGroupBox)
from PyQt6.QtCore import QTimer, pyqtSignal, QThread
from PyQt6.QtGui import QPixmap, QImage
import qrcode
from io import BytesIO
import json
import time


class BarcodeScannerThread(QThread):
    """Thread for continuous barcode scanning"""
    barcode_detected = pyqtSignal(str, str)  # barcode_data, barcode_type
    error_occurred = pyqtSignal(str)
    
    def __init__(self, camera_index=0):
        super().__init__()
        self.camera_index = camera_index
        self.running = False
        self.cap = None
        
    def run(self):
        """Run barcode scanning loop"""
        try:
            self.cap = cv2.VideoCapture(self.camera_index)
            if not self.cap.isOpened():
                self.error_occurred.emit("Could not open camera")
                return
                
            self.running = True
            while self.running:
                ret, frame = self.cap.read()
                if not ret:
                    continue
                    
                # Decode barcodes
                barcodes = pyzbar.decode(frame)
                
                for barcode in barcodes:
                    barcode_data = barcode.data.decode('utf-8')
                    barcode_type = barcode.type
                    self.barcode_detected.emit(barcode_data, barcode_type)
                    break  # Process one barcode at a time
                    
                time.sleep(0.1)  # Small delay to prevent excessive CPU usage
                
        except Exception as e:
            self.error_occurred.emit(f"Scanner error: {str(e)}")
        finally:
            if self.cap:
                self.cap.release()
                
    def stop(self):
        """Stop scanning"""
        self.running = False
        self.wait()


class BarcodeScannerDialog(QDialog):
    """Barcode scanner dialog"""
    
    def __init__(self, parent=None, callback=None):
        super().__init__(parent)
        self.callback = callback
        self.scanner_thread = None
        self.setup_ui()
        
    def setup_ui(self):
        """Setup scanner UI"""
        self.setWindowTitle("Barcode Scanner")
        self.setFixedSize(600, 500)
        
        layout = QVBoxLayout(self)
        
        # Camera selection
        camera_group = QGroupBox("Camera Settings")
        camera_layout = QFormLayout(camera_group)
        
        self.camera_combo = QComboBox()
        self.camera_combo.addItems(["Camera 0", "Camera 1", "Camera 2"])
        camera_layout.addRow("Camera:", self.camera_combo)
        
        layout.addWidget(camera_group)
        
        # Scanner controls
        controls_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("Start Scanning")
        self.start_btn.clicked.connect(self.start_scanning)
        controls_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("Stop Scanning")
        self.stop_btn.clicked.connect(self.stop_scanning)
        self.stop_btn.setEnabled(False)
        controls_layout.addWidget(self.stop_btn)
        
        layout.addLayout(controls_layout)
        
        # Manual input
        manual_group = QGroupBox("Manual Input")
        manual_layout = QFormLayout(manual_group)
        
        self.manual_input = QLineEdit()
        self.manual_input.setPlaceholderText("Enter barcode manually...")
        self.manual_input.returnPressed.connect(self.process_manual_input)
        manual_layout.addRow("Barcode:", self.manual_input)
        
        layout.addWidget(manual_group)
        
        # Results
        results_group = QGroupBox("Scan Results")
        results_layout = QVBoxLayout(results_group)
        
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setMaximumHeight(150)
        results_layout.addWidget(self.results_text)
        
        layout.addWidget(results_group)
        
        # Action buttons
        action_layout = QHBoxLayout()
        
        self.use_btn = QPushButton("Use This Barcode")
        self.use_btn.clicked.connect(self.use_barcode)
        self.use_btn.setEnabled(False)
        action_layout.addWidget(self.use_btn)
        
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_results)
        action_layout.addWidget(self.clear_btn)
        
        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.close)
        action_layout.addWidget(self.close_btn)
        
        layout.addLayout(action_layout)
        
        self.current_barcode = None
        
    def start_scanning(self):
        """Start barcode scanning"""
        camera_index = self.camera_combo.currentIndex()
        
        self.scanner_thread = BarcodeScannerThread(camera_index)
        self.scanner_thread.barcode_detected.connect(self.on_barcode_detected)
        self.scanner_thread.error_occurred.connect(self.on_error)
        self.scanner_thread.start()
        
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.results_text.append("Scanner started... Point camera at barcode.")
        
    def stop_scanning(self):
        """Stop barcode scanning"""
        if self.scanner_thread:
            self.scanner_thread.stop()
            self.scanner_thread = None
            
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.results_text.append("Scanner stopped.")
        
    def on_barcode_detected(self, barcode_data, barcode_type):
        """Handle detected barcode"""
        self.current_barcode = barcode_data
        result_text = f"Detected: {barcode_type} - {barcode_data}"
        self.results_text.append(result_text)
        self.use_btn.setEnabled(True)
        
    def on_error(self, error_message):
        """Handle scanner error"""
        self.results_text.append(f"Error: {error_message}")
        self.stop_scanning()
        
    def process_manual_input(self):
        """Process manually entered barcode"""
        barcode_data = self.manual_input.text().strip()
        if barcode_data:
            self.current_barcode = barcode_data
            self.results_text.append(f"Manual input: {barcode_data}")
            self.use_btn.setEnabled(True)
            self.manual_input.clear()
            
    def use_barcode(self):
        """Use the current barcode"""
        if self.current_barcode and self.callback:
            self.callback(self.current_barcode)
            self.close()
        else:
            QMessageBox.warning(self, "No Barcode", "No barcode selected.")
            
    def clear_results(self):
        """Clear scan results"""
        self.results_text.clear()
        self.current_barcode = None
        self.use_btn.setEnabled(False)


class QRCodeGeneratorDialog(QDialog):
    """QR Code generator dialog"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup QR generator UI"""
        self.setWindowTitle("QR Code Generator")
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout(self)
        
        # Input form
        form_layout = QFormLayout()
        
        self.data_input = QLineEdit()
        self.data_input.setPlaceholderText("Enter data to encode...")
        form_layout.addRow("Data:", self.data_input)
        
        self.size_input = QSpinBox()
        self.size_input.setRange(100, 1000)
        self.size_input.setValue(200)
        form_layout.addRow("Size:", self.size_input)
        
        layout.addLayout(form_layout)
        
        # Generate button
        self.generate_btn = QPushButton("Generate QR Code")
        self.generate_btn.clicked.connect(self.generate_qr)
        layout.addWidget(self.generate_btn)
        
        # QR Code display
        self.qr_label = QLabel()
        self.qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.qr_label.setStyleSheet("border: 1px solid #ccc; background: white;")
        layout.addWidget(self.qr_label)
        
        # Action buttons
        action_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("Save QR Code")
        self.save_btn.clicked.connect(self.save_qr)
        self.save_btn.setEnabled(False)
        action_layout.addWidget(self.save_btn)
        
        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.close)
        action_layout.addWidget(self.close_btn)
        
        layout.addLayout(action_layout)
        
        self.qr_image = None
        
    def generate_qr(self):
        """Generate QR code"""
        data = self.data_input.text().strip()
        if not data:
            QMessageBox.warning(self, "No Data", "Please enter data to encode.")
            return
            
        try:
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)
            
            # Create image
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to QPixmap
            size = self.size_input.value()
            img = img.resize((size, size))
            
            # Convert PIL image to QPixmap
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            
            qimg = QImage.fromData(buffer.getvalue())
            pixmap = QPixmap.fromImage(qimg)
            
            self.qr_label.setPixmap(pixmap)
            self.qr_image = img
            self.save_btn.setEnabled(True)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate QR code: {str(e)}")
            
    def save_qr(self):
        """Save QR code to file"""
        if self.qr_image:
            from PyQt6.QtWidgets import QFileDialog
            filename, _ = QFileDialog.getSaveFileName(
                self, "Save QR Code", "qrcode.png", "PNG Files (*.png)"
            )
            if filename:
                self.qr_image.save(filename)
                QMessageBox.information(self, "Success", f"QR code saved to {filename}")


class BarcodeUtils:
    """Utility class for barcode operations"""
    
    @staticmethod
    def generate_product_barcode(product_id, product_name):
        """Generate a barcode for a product"""
        # Simple barcode generation (in real app, use proper barcode library)
        barcode_data = f"PROD{product_id:06d}"
        return barcode_data
        
    @staticmethod
    def parse_barcode(barcode_data):
        """Parse barcode data to extract information"""
        if barcode_data.startswith("PROD"):
            try:
                product_id = int(barcode_data[4:])
                return {"type": "product", "id": product_id}
            except ValueError:
                return {"type": "unknown", "data": barcode_data}
        else:
            return {"type": "unknown", "data": barcode_data}
            
    @staticmethod
    def validate_barcode(barcode_data):
        """Validate barcode format"""
        if not barcode_data or len(barcode_data) < 3:
            return False
        return True


# Example usage functions
def open_barcode_scanner(parent=None, callback=None):
    """Open barcode scanner dialog"""
    dialog = BarcodeScannerDialog(parent, callback)
    return dialog.exec()

def open_qr_generator(parent=None):
    """Open QR code generator dialog"""
    dialog = QRCodeGeneratorDialog(parent)
    return dialog.exec()
