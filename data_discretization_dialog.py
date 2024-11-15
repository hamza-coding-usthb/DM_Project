from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QMessageBox, QInputDialog
import pandas as pd

class DataDiscretizationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Data Discretization")
        self.setGeometry(200, 200, 400, 200)

        # Layout for the data discretization options
        layout = QVBoxLayout()

        # Buttons for different discretization methods
        self.equal_width_button = QPushButton("Equal Width Discretization")
        self.equal_width_button.clicked.connect(self.equal_width_discretization)
        layout.addWidget(self.equal_width_button)

        self.equal_frequency_button = QPushButton("Equal Frequency Discretization")
        self.equal_frequency_button.clicked.connect(self.equal_frequency_discretization)
        layout.addWidget(self.equal_frequency_button)

        # Button for discretizing by coordinates
        self.coord_discretization_button = QPushButton("Discretize by Coordinates")
        self.coord_discretization_button.clicked.connect(self.discretize_by_coordinates)
        layout.addWidget(self.coord_discretization_button)

        # Set dialog layout
        self.setLayout(layout)

    def equal_width_discretization(self):
        if self.parent.full_data is not None:
            column, ok = QInputDialog.getItem(
                self, "Select Column", "Choose column for equal width discretization:", 
                self.parent.full_data.columns.tolist(), 0, False
            )
            if ok:
                bins, ok = QInputDialog.getInt(self, "Number of Bins", "Enter the number of bins:", 5, 2, 100)
                if ok:
                    # Perform equal-width discretization
                    self.parent.full_data[column + "_width_bin"] = pd.cut(self.parent.full_data[column], bins=bins)
                    self.parent.display_data()
                    QMessageBox.information(self, "Discretization Complete", "Equal width discretization applied.")
        else:
            QMessageBox.warning(self, "No Data", "Please import a dataset first.")

    def equal_frequency_discretization(self):
        if self.parent.full_data is not None:
            column, ok = QInputDialog.getItem(
                self, "Select Column", "Choose column for equal frequency discretization:", 
                self.parent.full_data.columns.tolist(), 0, False
            )
            if ok:
                bins, ok = QInputDialog.getInt(self, "Number of Bins", "Enter the number of bins:", 5, 2, 100)
                if ok:
                    # Perform equal-frequency discretization
                    self.parent.full_data[column + "_freq_bin"] = pd.qcut(self.parent.full_data[column], q=bins)
                    self.parent.display_data()
                    QMessageBox.information(self, "Discretization Complete", "Equal frequency discretization applied.")
        else:
            QMessageBox.warning(self, "No Data", "Please import a dataset first.")

    def discretize_by_coordinates(self):
        if self.parent.full_data is not None:
            # Ensure 'latitude' and 'longitude' columns exist
            if 'latitude' in self.parent.full_data.columns and 'longitude' in self.parent.full_data.columns:
                
                # Determine min and max for latitude and longitude from the dataset
                min_lat, max_lat = self.parent.full_data['latitude'].min(), self.parent.full_data['latitude'].max()
                min_lon, max_lon = self.parent.full_data['longitude'].min(), self.parent.full_data['longitude'].max()

                # Prompt user for the number of intervals (bins)
                num_bins, ok = QInputDialog.getInt(self, "Number of Bins", "Enter the number of bins:", 5, 2, 100)
                if not ok:
                    return
                
                # Define latitude and longitude bins within dataset-specific ranges
                lat_bins = pd.interval_range(start=min_lat, end=max_lat, freq=(max_lat - min_lat) / num_bins)
                lon_bins = pd.interval_range(start=min_lon, end=max_lon, freq=(max_lon - min_lon) / num_bins)

                # Discretize latitude and longitude columns based on calculated intervals
                self.parent.full_data['lat_bin'] = pd.cut(self.parent.full_data['latitude'], bins=lat_bins)
                self.parent.full_data['lon_bin'] = pd.cut(self.parent.full_data['longitude'], bins=lon_bins)

                # Group by the new lat_bin and lon_bin intervals and calculate the mean of other columns
                grouped_data = self.parent.full_data.groupby(['lat_bin', 'lon_bin']).mean(numeric_only=True).reset_index()

                # Update the main data with the aggregated data
                self.parent.full_data = grouped_data
                self.parent.current_page = 0
                self.parent.update_total_pages()
                self.parent.display_data()

                QMessageBox.information(self, "Discretization Complete", "Data has been discretized by spatial coordinates and aggregated.")
            else:
                QMessageBox.warning(self, "Missing Columns", "The dataset must contain 'latitude' and 'longitude' columns.")
        else:
            QMessageBox.warning(self, "No Data", "Please import a dataset first.")
