import pandas as pd
from scipy.stats import zscore
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QMessageBox

class DataNormalizationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.data = None  # Local storage for the dataset
        self.setWindowTitle("Data Normalization")
        self.setGeometry(200, 200, 400, 200)

        # Layout for the data normalization options
        layout = QVBoxLayout()

        # Min-Max normalization button
        self.min_max_button = QPushButton("Min-Max Normalization")
        self.min_max_button.clicked.connect(self.apply_min_max_normalization)
        layout.addWidget(self.min_max_button)

        # Z-score normalization button
        self.zscore_button = QPushButton("Z-score Normalization")
        self.zscore_button.clicked.connect(self.apply_zscore_normalization)
        layout.addWidget(self.zscore_button)

        # Set dialog layout
        self.setLayout(layout)

    def set_data(self, data):
        """Set the dataset for the dialog."""
        self.data = data

    def apply_min_max_normalization(self):
        if self.data is not None:
            columns_to_normalize = self.data.columns.difference(['time', 'latitude', 'longitude', 'geometry'])
            non_normalized_columns = []
            for column in columns_to_normalize:
                min_value = self.data[column].min()
                max_value = self.data[column].max()
                if max_value - min_value > 1e-6:  # Ensure there's a significant range for normalization
                    self.data[column] = (self.data[column] - min_value) / (max_value - min_value)
                else:
                    non_normalized_columns.append(column)

            if non_normalized_columns:
                QMessageBox.warning(self, "Partial Normalization",
                                    f"Data has been normalized using Min-Max.\n"
                                    f"The following columns were not normalized due to insufficient range: {', '.join(non_normalized_columns)}")
            else:
                QMessageBox.information(self, "Normalization Complete", "Data has been normalized using Min-Max.")
        else:
            QMessageBox.warning(self, "No Data", "No dataset available for normalization.")

    def apply_zscore_normalization(self):
        if self.data is not None:
            columns_to_normalize = self.data.columns.difference(['time', 'latitude', 'longitude', 'geometry'])
            non_normalized_columns = []
            for column in columns_to_normalize:
                if self.data[column].std() > 1e-6:  # Check if std deviation is above threshold
                    self.data[column] = (self.data[column] - self.data[column].mean()) / self.data[column].std()
                else:
                    non_normalized_columns.append(column)

            if non_normalized_columns:
                QMessageBox.warning(self, "Partial Normalization",
                                    f"Data has been normalized using Z-score.\n"
                                    f"The following columns were not normalized due to low variance: {', '.join(non_normalized_columns)}")
            else:
                QMessageBox.information(self, "Normalization Complete", "Data has been normalized using Z-score.")
        else:
            QMessageBox.warning(self, "No Data", "No dataset available for normalization.")
