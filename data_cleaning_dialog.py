from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QMessageBox
import pandas as pd

class DataCleaningDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Data Cleaning")
        self.setGeometry(200, 200, 400, 350)  # Adjust height to fit the new button

        # Layout for the data cleaning options
        layout = QVBoxLayout()

        # Add buttons for different outlier handling methods
        self.remove_outliers_button = QPushButton("Remove Outliers")
        self.remove_outliers_button.clicked.connect(self.remove_outliers)
        layout.addWidget(self.remove_outliers_button)

        self.replace_outliers_mean_button = QPushButton("Replace Outliers with Mean")
        self.replace_outliers_mean_button.clicked.connect(self.replace_outliers_with_mean)
        layout.addWidget(self.replace_outliers_mean_button)

        self.replace_outliers_median_button = QPushButton("Replace Outliers with Median")
        self.replace_outliers_median_button.clicked.connect(self.replace_outliers_with_median)
        layout.addWidget(self.replace_outliers_median_button)

        self.cap_outliers_button = QPushButton("Cap Outliers")
        self.cap_outliers_button.clicked.connect(self.cap_outliers)
        layout.addWidget(self.cap_outliers_button)

        # Add button to remove rows with NaN values
        self.remove_nan_button = QPushButton("Remove Rows with NaN")
        self.remove_nan_button.clicked.connect(self.remove_nan_rows)
        layout.addWidget(self.remove_nan_button)

        self.setLayout(layout)

    def calculate_outliers(self):
        """Calculate outliers based on IQR for each numeric column."""
        columns_to_check = self.parent.full_data.select_dtypes(include=['float64', 'int64']).columns
        Q1 = self.parent.full_data[columns_to_check].quantile(0.25)
        Q3 = self.parent.full_data[columns_to_check].quantile(0.75)
        IQR = Q3 - Q1
        outliers = (self.parent.full_data[columns_to_check] < (Q1 - 1.5 * IQR)) | (self.parent.full_data[columns_to_check] > (Q3 + 1.5 * IQR))
        return outliers

    def remove_outliers(self):
        """Removes rows with outliers based on IQR."""
        if self.parent.full_data is not None:
            outliers = self.calculate_outliers()
            self.parent.full_data = self.parent.full_data[~outliers.any(axis=1)]
            self.parent.current_page = 0
            self.parent.update_total_pages()
            self.parent.display_data()
            QMessageBox.information(self, "Outliers Removed", f"Outliers removed. Remaining rows: {len(self.parent.full_data)}.")
        else:
            QMessageBox.warning(self, "No Data", "Please import a dataset first.")

    def replace_outliers_with_mean(self):
        """Replaces outlier values with the column mean."""
        if self.parent.full_data is not None:
            outliers = self.calculate_outliers()
            for column in outliers.columns:
                mean_value = self.parent.full_data[column].mean()
                self.parent.full_data.loc[outliers[column], column] = mean_value

            self.parent.current_page = 0
            self.parent.update_total_pages()
            self.parent.display_data()
            QMessageBox.information(self, "Outliers Replaced", "Outliers have been replaced with the column mean.")
        else:
            QMessageBox.warning(self, "No Data", "Please import a dataset first.")

    def replace_outliers_with_median(self):
        """Replaces outlier values with the column median."""
        if self.parent.full_data is not None:
            outliers = self.calculate_outliers()
            for column in outliers.columns:
                median_value = self.parent.full_data[column].median()
                self.parent.full_data.loc[outliers[column], column] = median_value

            self.parent.current_page = 0
            self.parent.update_total_pages()
            self.parent.display_data()
            QMessageBox.information(self, "Outliers Replaced", "Outliers have been replaced with the column median.")
        else:
            QMessageBox.warning(self, "No Data", "Please import a dataset first.")

    def cap_outliers(self):
        """Caps outliers to the 5th and 95th percentiles."""
        if self.parent.full_data is not None:
            columns_to_check = self.parent.full_data.select_dtypes(include=['float64', 'int64']).columns
            lower_bound = self.parent.full_data[columns_to_check].quantile(0.05)
            upper_bound = self.parent.full_data[columns_to_check].quantile(0.95)

            for column in columns_to_check:
                self.parent.full_data[column] = self.parent.full_data[column].clip(lower=lower_bound[column], upper=upper_bound[column])

            self.parent.current_page = 0
            self.parent.update_total_pages()
            self.parent.display_data()
            QMessageBox.information(self, "Outliers Capped", "Outliers have been capped to the 5th and 95th percentiles.")
        else:
            QMessageBox.warning(self, "No Data", "Please import a dataset first.")

    def remove_nan_rows(self):
        """Removes rows containing NaN values."""
        if self.parent.full_data is not None:
            initial_rows = len(self.parent.full_data)
            self.parent.full_data = self.parent.full_data.dropna()
            final_rows = len(self.parent.full_data)
            removed_rows = initial_rows - final_rows

            self.parent.current_page = 0
            self.parent.update_total_pages()
            self.parent.display_data()
            QMessageBox.information(self, "NaN Rows Removed", f"{removed_rows} rows with NaN values have been removed.")
        else:
            QMessageBox.warning(self, "No Data", "Please import a dataset first.")
