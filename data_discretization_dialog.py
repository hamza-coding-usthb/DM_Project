import pandas as pd
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QMessageBox

class DataDiscretizationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Data Discretization")
        self.setGeometry(200, 200, 400, 200)

        # Layout for the data discretization options
        layout = QVBoxLayout()

        # Time-based discretization button
        self.time_discretization_button = QPushButton("Discretize by Time")
        self.time_discretization_button.clicked.connect(self.discretize_by_time)
        layout.addWidget(self.time_discretization_button)

        # Coordinate-based discretization button
        self.coord_discretization_button = QPushButton("Discretize by Coordinates")
        self.coord_discretization_button.clicked.connect(self.discretize_by_coordinates)
        layout.addWidget(self.coord_discretization_button)

        # Set dialog layout
        self.setLayout(layout)

    def ensure_datetime(self):
        """Ensure that the 'time' column is in datetime format."""
        if 'time' in self.parent.full_data.columns:
            self.parent.full_data['time'] = pd.to_datetime(self.parent.full_data['time'], errors='coerce')
            if self.parent.full_data['time'].isnull().any():
                QMessageBox.warning(self, "Date Conversion Error", "Some 'time' values could not be converted to datetime.")
                self.parent.full_data.dropna(subset=['time'], inplace=True)
            return True
        else:
            QMessageBox.warning(self, "Missing 'time' Column", "The data must have a 'time' column in datetime format.")
            return False

    def discretize_by_time(self):
        if self.parent.full_data is not None:
            # Ensure time column is in datetime format
            if not self.ensure_datetime():
                return

            # Example: Discretize by monthly and seasonal aggregation
            self.parent.full_data['year_month'] = self.parent.full_data['time'].dt.to_period('M')
            
            # Group by latitude, longitude, and year_month for monthly data
            monthly_data = self.parent.full_data.groupby(['latitude', 'longitude', 'year_month']).mean(numeric_only=True).reset_index()
            self.parent.full_data = monthly_data
            self.parent.current_page = 0
            self.parent.update_total_pages()
            self.parent.display_data()
            QMessageBox.information(self, "Discretization Complete", "Data has been discretized by monthly time intervals and displayed.")
        else:
            QMessageBox.warning(self, "No Data", "Please import a dataset first.")

    def discretize_by_coordinates(self):
        if self.parent.full_data is not None:
            # Example: Discretize by spatial coordinates into bins
            # Define latitude and longitude bins
            lat_bins = pd.interval_range(start=-90, end=90, freq=10)
            lon_bins = pd.interval_range(start=-180, end=180, freq=10)

            # Discretize latitude and longitude
            self.parent.full_data['lat_bin'] = pd.cut(self.parent.full_data['latitude'], bins=lat_bins)
            self.parent.full_data['lon_bin'] = pd.cut(self.parent.full_data['longitude'], bins=lon_bins)

            # Group by spatial bins and calculate mean for each bin
            spatial_data = self.parent.full_data.groupby(['lat_bin', 'lon_bin']).mean(numeric_only=True).reset_index()

            # Update the main data with discretized data
            self.parent.full_data = spatial_data
            self.parent.current_page = 0
            self.parent.update_total_pages()
            self.parent.display_data()
            QMessageBox.information(self, "Discretization Complete", "Data has been discretized by spatial coordinates and displayed.")
        else:
            QMessageBox.warning(self, "No Data", "Please import a dataset first.")
