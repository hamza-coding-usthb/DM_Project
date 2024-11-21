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
         # Add a button for the new reduction option
        self.reduction_button = QPushButton("Reduce Data by Season")
        self.reduction_button.clicked.connect(self.reduce_data_by_season)
        layout.addWidget(self.reduction_button)
        # Set dialog layout
        self.setLayout(layout)
    def reduce_data_by_season(self):
        if self.parent.full_data is not None:
            try:
                # Pivot the data based on 'latitude', 'longitude', and 'season'
                pivot_df = self.parent.full_data.pivot(index=['latitude', 'longitude'], 
                                                       columns='season',
                                                       values=['PSurf', 'Qair', 'Rainf', 'Snowf', 'Tair', 'Wind'])

                # Flatten the MultiIndex columns
                pivot_df.columns = [f"{var}{season}" for var, season in pivot_df.columns]
                
                # Reset index to make it compatible with the main data frame
                pivot_df.reset_index(inplace=True)

                # Update the main data with the reduced form
                self.parent.full_data = pivot_df
                self.parent.current_page = 0
                self.parent.update_total_pages()
                self.parent.display_data()

                QMessageBox.information(self, "Reduction Complete", "Data has been reduced by season and displayed.")
            except Exception as e:
                QMessageBox.warning(self, "Reduction Error", f"An error occurred during data reduction: {e}")
        else:
            QMessageBox.warning(self, "No Data", "Please import a dataset first.")
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

            # Define the official seasonal boundaries
            def get_season(date):
                if date >= pd.Timestamp(f"{date.year}-12-21") or date < pd.Timestamp(f"{date.year}-03-21"):
                    return 'Winter'
                elif pd.Timestamp(f"{date.year}-03-21") <= date < pd.Timestamp(f"{date.year}-06-21"):
                    return 'Spring'
                elif pd.Timestamp(f"{date.year}-06-21") <= date < pd.Timestamp(f"{date.year}-09-23"):
                    return 'Summer'
                elif pd.Timestamp(f"{date.year}-09-23") <= date < pd.Timestamp(f"{date.year}-12-21"):
                    return 'Fall'

            # Map precise date ranges to seasons and add a 'season' column
            self.parent.full_data['season'] = self.parent.full_data['time'].apply(get_season)

            # Perform seasonal aggregation
            seasonal_data = self.parent.full_data.groupby(['latitude', 'longitude', 'season']).mean(numeric_only=True).reset_index()

            # Update the parent data with the aggregated data
            self.parent.full_data = seasonal_data
            self.parent.current_page = 0
            self.parent.update_total_pages()
            self.parent.display_data()

            QMessageBox.information(self, "Aggregation Complete", "Data has been aggregated seasonally based on precise boundaries and displayed.")
