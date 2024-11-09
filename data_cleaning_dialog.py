import pandas as pd
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QMessageBox

class DataCleaningDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Data Cleaning")
        self.setGeometry(200, 200, 400, 200)

        # Layout for the data cleaning options
        layout = QVBoxLayout()

        # Outlier removal button
        self.remove_outliers_button = QPushButton("Remove Outliers")
        self.remove_outliers_button.clicked.connect(self.remove_outliers)
        layout.addWidget(self.remove_outliers_button)

        # Set dialog layout
        self.setLayout(layout)

    def remove_outliers(self):
        if self.parent.full_data is not None:
            # Exclude columns named 'time', 'latitude', 'longitude' for outlier removal
            columns_to_check = self.parent.full_data.columns.difference(['time', 'latitude', 'longitude'])

            # Calculate Q1 and Q3 for each specified column
            Q1 = self.parent.full_data[columns_to_check].quantile(0.25)
            Q3 = self.parent.full_data[columns_to_check].quantile(0.75)
            IQR = Q3 - Q1

            # Filter out rows where any column has outliers
            outliers = (self.parent.full_data[columns_to_check] < (Q1 - 1.5 * IQR)) | (self.parent.full_data[columns_to_check] > (Q3 + 1.5 * IQR))
            self.parent.full_data = self.parent.full_data[~outliers.any(axis=1)]
            
            # Refresh the data display
            self.parent.current_page = 0
            self.parent.update_total_pages()
            self.parent.display_data()

            QMessageBox.information(self, "Outliers Removed", f"Outliers removed. Remaining rows: {len(self.parent.full_data)}.")
        else:
            QMessageBox.warning(self, "No Data", "Please import a dataset first.")
