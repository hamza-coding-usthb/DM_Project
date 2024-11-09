import pandas as pd
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QMessageBox

class DataAggregationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Data Aggregation")
        self.setGeometry(200, 200, 400, 200)

        # Layout for the data aggregation options
        layout = QVBoxLayout()

        # Monthly aggregation button
        self.monthly_button = QPushButton("Aggregate Monthly")
        self.monthly_button.clicked.connect(self.aggregate_monthly)
        layout.addWidget(self.monthly_button)

        # Seasonal aggregation button
        self.seasonal_button = QPushButton("Aggregate Seasonally")
        self.seasonal_button.clicked.connect(self.aggregate_seasonally)
        layout.addWidget(self.seasonal_button)

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

    def aggregate_monthly(self):
        if self.parent.full_data is not None:
            # Check if required columns are present
            if not {'time', 'latitude', 'longitude'}.issubset(self.parent.full_data.columns):
                QMessageBox.warning(self, "Missing Columns", "Data must contain 'time', 'latitude', and 'longitude' columns for aggregation.")
                return

            if not self.ensure_datetime():
                return
            
            # Extract year-month for monthly grouping
            self.parent.full_data['year_month'] = self.parent.full_data['time'].dt.to_period('M')

            # Perform monthly aggregation
            monthly_data = self.parent.full_data.groupby(['latitude', 'longitude', 'year_month']).mean(numeric_only=True).reset_index()

            # Update the parent data with the aggregated data
            self.parent.full_data = monthly_data
            self.parent.current_page = 0
            self.parent.update_total_pages()
            self.parent.display_data()

            QMessageBox.information(self, "Aggregation Complete", "Data has been aggregated monthly and displayed.")

    def aggregate_seasonally(self):
        if self.parent.full_data is not None:
            # Check if required columns are present
            if not {'time', 'latitude', 'longitude'}.issubset(self.parent.full_data.columns):
                QMessageBox.warning(self, "Missing Columns", "Data must contain 'time', 'latitude', and 'longitude' columns for aggregation.")
                return

            if not self.ensure_datetime():
                return

            # Define a function to map months to seasons
            def get_season(month):
                if month in [12, 1, 2]:
                    return 'Winter'
                elif month in [3, 4, 5]:
                    return 'Spring'
                elif month in [6, 7, 8]:
                    return 'Summer'
                elif month in [9, 10, 11]:
                    return 'Fall'

            # Map months to seasons and add a 'season' column
            self.parent.full_data['season'] = self.parent.full_data['time'].dt.month.map(get_season)

            # Perform seasonal aggregation
            seasonal_data = self.parent.full_data.groupby(['latitude', 'longitude', 'season']).mean(numeric_only=True).reset_index()

            # Update the parent data with the aggregated data
            self.parent.full_data = seasonal_data
            self.parent.current_page = 0
            self.parent.update_total_pages()
            self.parent.display_data()

            QMessageBox.information(self, "Aggregation Complete", "Data has been aggregated seasonally and displayed.")
