import pandas as pd
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QFileDialog, QMessageBox, QInputDialog

class DataManipulationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Data Manipulation")
        self.setGeometry(150, 150, 600, 400)

        layout = QVBoxLayout()
        self.import_button = QPushButton("Import Dataset")
        self.import_button.clicked.connect(self.import_data)
        layout.addWidget(self.import_button)

        self.description_button = QPushButton("Dataset Description")
        self.description_button.clicked.connect(self.show_description)
        layout.addWidget(self.description_button)

        self.update_button = QPushButton("Update an Instance")
        self.update_button.clicked.connect(self.update_instance)
        layout.addWidget(self.update_button)

        self.delete_button = QPushButton("Delete an Instance")
        self.delete_button.clicked.connect(self.delete_instance)
        layout.addWidget(self.delete_button)

        self.save_button = QPushButton("Save Dataset")
        self.save_button.clicked.connect(self.save_data)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def import_data(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)")
        if file_path:
            self.parent.file_path = file_path
            self.parent.full_data = pd.read_csv(file_path)
            self.parent.current_page = 0
            self.parent.update_total_pages()
            self.parent.display_data()
            QMessageBox.information(self, "Import Successful", "Dataset imported successfully.")

    def show_description(self):
        if self.parent.full_data is not None:
            description = self.parent.full_data.describe().to_string()
            QMessageBox.information(self, "Dataset Description", description)
        else:
            QMessageBox.warning(self, "No Data", "Please import a dataset first.")

    def update_instance(self):
        if self.parent.full_data is not None:
            row, ok = QInputDialog.getInt(self, "Update Row", "Enter row number to update:", 0, 0, len(self.parent.full_data) - 1)
            if ok:
                column, ok = QInputDialog.getItem(self, "Update Column", "Choose column:", self.parent.full_data.columns.tolist(), 0, False)
                if ok:
                    new_value, ok = QInputDialog.getText(self, "New Value", f"Enter new value for {column} at row {row}:")
                    if ok:
                        self.parent.full_data.at[row, column] = new_value
                        self.parent.display_data()
                        QMessageBox.information(self, "Update Successful", f"Row {row} updated successfully.")
        else:
            QMessageBox.warning(self, "No Data", "Please import a dataset first.")

    def delete_instance(self):
        if self.parent.full_data is not None:
            row, ok = QInputDialog.getInt(self, "Delete Row", "Enter row number to delete:", 0, 0, len(self.parent.full_data) - 1)
            if ok:
                self.parent.full_data.drop(row, inplace=True)
                self.parent.full_data.reset_index(drop=True, inplace=True)
                self.parent.display_data()
                QMessageBox.information(self, "Delete Successful", f"Row {row} deleted successfully.")
        else:
            QMessageBox.warning(self, "No Data", "Please import a dataset first.")

    def save_data(self):
        if self.parent.full_data is not None:
            save_path, _ = QFileDialog.getSaveFileName(self, "Save CSV File", "", "CSV Files (*.csv);;All Files (*)")
            if save_path:
                self.parent.full_data.to_csv(save_path, index=False)
                QMessageBox.information(self, "Save Successful", "Dataset saved successfully.")
        else:
            QMessageBox.warning(self, "No Data", "Please import a dataset first.")
