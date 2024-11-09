import pandas as pd
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QFileDialog, QMessageBox

class DataMergerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Data Merger")
        self.setGeometry(200, 200, 400, 200)

        # Layout for the data merger options
        layout = QVBoxLayout()

        # Button to merge data
        self.merge_button = QPushButton("Select CSV to Merge")
        self.merge_button.clicked.connect(self.merge_data)
        layout.addWidget(self.merge_button)

        # Set dialog layout
        self.setLayout(layout)

    def merge_data(self):
        if self.parent.full_data is not None:
            # Open a file dialog to select the second CSV file
            file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File to Merge", "", "CSV Files (*.csv);;All Files (*)")
            if not file_path:
                return

            # Load the second CSV file
            try:
                secondary_data = pd.read_csv(file_path)
            except Exception as e:
                QMessageBox.warning(self, "File Error", f"Could not load CSV file: {e}")
                return

            # Check if both files have 'latitude' and 'longitude' columns
            required_columns = {'latitude', 'longitude'}
            if not required_columns.issubset(self.parent.full_data.columns) or not required_columns.issubset(secondary_data.columns):
                QMessageBox.warning(self, "Missing Columns", "Both files must have 'latitude' and 'longitude' columns for merging.")
                return

            # Perform the merge on 'latitude' and 'longitude' columns
            merged_data = pd.merge(self.parent.full_data, secondary_data, on=['latitude', 'longitude'], how='inner')

            # Update the main data with merged data
            self.parent.full_data = merged_data
            self.parent.current_page = 0
            self.parent.update_total_pages()
            self.parent.display_data()

            QMessageBox.information(self, "Merge Complete", "Data has been successfully merged and displayed.")
        else:
            QMessageBox.warning(self, "No Data", "Please import a primary dataset first.")
