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
        self.equal_width_button = QPushButton("Equal Width Discretization (Very Low - Very High)")
        self.equal_width_button.clicked.connect(self.equal_width_discretization)
        layout.addWidget(self.equal_width_button)

        self.equal_frequency_button = QPushButton("Equal Frequency Discretization (Very Low - Very High)")
        self.equal_frequency_button.clicked.connect(self.equal_frequency_discretization)
        layout.addWidget(self.equal_frequency_button)

        # Set dialog layout
        self.setLayout(layout)

    def get_column_options(self):
        """
        Generate a list of columns for discretization.
        Excludes 'latitude', 'longitude', and 'geometry' columns, but includes an 'All Numerical Columns' option.
        """
        if self.parent.full_data is not None:
            numerical_columns = self.parent.full_data.select_dtypes(include=['number']).columns.tolist()
            # Exclude specific columns
            excluded_columns = {'latitude', 'longitude', 'geometry'}
            valid_columns = [col for col in numerical_columns if col not in excluded_columns]
            return ["All Numerical Columns"] + valid_columns
        return []

    def apply_discretization(self, column, method, bins, labels):
        """
        Apply the specified discretization method to the given column(s).
        """
        updated_data = self.parent.full_data.copy()  # Copy the existing DataFrame for modifications

        if column == "All Numerical Columns":
            # Apply discretization to all numerical columns (excluding latitude, longitude, geometry)
            for col in self.get_column_options()[1:]:
                try:
                    if method == "equal_width":
                        updated_data[col] = pd.cut(updated_data[col], bins=bins, labels=labels)
                    elif method == "equal_frequency":
                        updated_data[col] = pd.qcut(updated_data[col], q=bins, labels=labels)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"An error occurred while discretizing '{col}': {e}")
        else:
            # Apply discretization to a single column
            try:
                if method == "equal_width":
                    updated_data[column] = pd.cut(updated_data[column], bins=bins, labels=labels)
                elif method == "equal_frequency":
                    updated_data[column] = pd.qcut(updated_data[column], q=bins, labels=labels)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred while discretizing '{column}': {e}")

        # Update the parent table display with the modified data
        self.parent.full_data = updated_data  # Replace the full_data with the updated one
        self.parent.display_data()  # Refresh the displayed data to show the new table

    def equal_width_discretization(self):
        if self.parent.full_data is not None:
            column, ok = QInputDialog.getItem(
                self,
                "Select Column",
                "Choose column for equal width discretization:",
                self.get_column_options(),
                0,
                False
            )
            if ok:
                # Perform equal-width discretization into 5 fixed bins
                try:
                    bins = 5  # Fixed number of bins
                    labels = ["Very Low", "Low", "Average", "High", "Very High"]
                    self.apply_discretization(column, method="equal_width", bins=bins, labels=labels)
                    QMessageBox.information(self, "Discretization Complete", "Equal width discretization applied.")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"An error occurred during discretization: {e}")
        else:
            QMessageBox.warning(self, "No Data", "Please import a dataset first.")

    def equal_frequency_discretization(self):
        if self.parent.full_data is not None:
            column, ok = QInputDialog.getItem(
                self,
                "Select Column",
                "Choose column for equal frequency discretization:",
                self.get_column_options(),
                0,
                False
            )
            if ok:
                # Perform equal-frequency discretization into 5 fixed bins
                try:
                    bins = 5  # Fixed number of bins
                    labels = ["Very Low", "Low", "Average", "High", "Very High"]
                    self.apply_discretization(column, method="equal_frequency", bins=bins, labels=labels)
                    QMessageBox.information(self, "Discretization Complete", "Equal frequency discretization applied.")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"An error occurred during discretization: {e}")
        else:
            QMessageBox.warning(self, "No Data", "Please import a dataset first.")
