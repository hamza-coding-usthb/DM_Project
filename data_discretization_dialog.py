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

        # Existing buttons
        self.time_discretization_button = QPushButton("Discretize by Time")
        self.time_discretization_button.clicked.connect(self.discretize_by_time)
        layout.addWidget(self.time_discretization_button)

        self.coord_discretization_button = QPushButton("Discretize by Coordinates")
        self.coord_discretization_button.clicked.connect(self.discretize_by_coordinates)
        layout.addWidget(self.coord_discretization_button)

        # Set dialog layout
        self.setLayout(layout)

    def equal_width_discretization(self):
        if self.parent.full_data is not None:
            column, ok = QInputDialog.getItem(self, "Select Column", "Choose column for equal width discretization:", 
                                              self.parent.full_data.columns.tolist(), 0, False)
            if ok:
                bins, ok = QInputDialog.getInt(self, "Number of Bins", "Enter the number of bins:", 5, 2, 100)
                if ok:
                    self.parent.full_data[column + "_width_bin"] = pd.cut(self.parent.full_data[column], bins=bins)
                    self.parent.display_data()
                    QMessageBox.information(self, "Discretization Complete", "Equal width discretization applied.")
        else:
            QMessageBox.warning(self, "No Data", "Please import a dataset first.")

    def equal_frequency_discretization(self):
        if self.parent.full_data is not None:
            column, ok = QInputDialog.getItem(self, "Select Column", "Choose column for equal frequency discretization:", 
                                              self.parent.full_data.columns.tolist(), 0, False)
            if ok:
                bins, ok = QInputDialog.getInt(self, "Number of Bins", "Enter the number of bins:", 5, 2, 100)
                if ok:
                    self.parent.full_data[column + "_freq_bin"] = pd.qcut(self.parent.full_data[column], q=bins)
                    self.parent.display_data()
                    QMessageBox.information(self, "Discretization Complete", "Equal frequency discretization applied.")
        else:
            QMessageBox.warning(self, "No Data", "Please import a dataset first.")
    def discretize_by_time(self):
        if self.parent.full_data is not None:
            if 'time' in self.parent.full_data.columns:
                # Convert 'time' column to datetime if it isn't already
                self.parent.full_data['time'] = pd.to_datetime(self.parent.full_data['time'], errors='coerce')
                # Discretize time into monthly intervals
                self.parent.full_data['year_month'] = self.parent.full_data['time'].dt.to_period('M')
                self.parent.display_data()
                QMessageBox.information(self, "Discretization Complete", "Data has been discretized by monthly time intervals.")
            else:
                QMessageBox.warning(self, "Missing 'time' Column", "The data must have a 'time' column.")
        else:
            QMessageBox.warning(self, "No Data", "Please import a dataset first.")
    def discretize_by_coordinates(self):
        if self.parent.full_data is not None:
            # Define latitude and longitude bins (adjust intervals as needed)
            lat_bins = pd.interval_range(start=-90, end=90, freq=10)
            lon_bins = pd.interval_range(start=-180, end=180, freq=10)

            # Discretize latitude and longitude
            self.parent.full_data['lat_bin'] = pd.cut(self.parent.full_data['latitude'], bins=lat_bins)
            self.parent.full_data['lon_bin'] = pd.cut(self.parent.full_data['longitude'], bins=lon_bins)

            # Update the table display
            self.parent.display_data()
            QMessageBox.information(self, "Discretization Complete", "Data has been discretized by spatial coordinates.")
        else:
            QMessageBox.warning(self, "No Data", "Please import a dataset first.")

