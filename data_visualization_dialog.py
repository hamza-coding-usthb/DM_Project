import pandas as pd
import matplotlib
matplotlib.use('QtAgg')

import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QInputDialog, QMessageBox

class DataVisualizationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Data Visualization")
        self.setGeometry(200, 200, 400, 200)

        # Layout for the data visualization options
        layout = QVBoxLayout()

        # Buttons for different types of plots
        self.boxplot_button = QPushButton("Boxplot")
        self.boxplot_button.clicked.connect(self.plot_boxplot)
        layout.addWidget(self.boxplot_button)

        self.scatter_button = QPushButton("Scatter Plot")
        self.scatter_button.clicked.connect(self.plot_scatter)
        layout.addWidget(self.scatter_button)

        self.histogram_button = QPushButton("Histogram")
        self.histogram_button.clicked.connect(self.plot_histogram)
        layout.addWidget(self.histogram_button)

        # Set dialog layout
        self.setLayout(layout)

    def plot_boxplot(self):
        if self.parent.full_data is not None:
            columns = self.parent.full_data.select_dtypes(include=['float64', 'int64']).columns.tolist()
            if columns:
                column, ok = QInputDialog.getItem(self, "Select Column", "Choose column for boxplot:", columns, 0, False)
                if ok:
                    plt.figure(figsize=(8, 6))
                    self.parent.full_data.boxplot(column=column)
                    plt.title(f'Boxplot of {column}')
                    plt.ylabel(column)
                    plt.show()
            else:
                QMessageBox.warning(self, "No Numeric Columns", "No numeric columns available for boxplot.")
        else:
            QMessageBox.warning(self, "No Data", "Please import a dataset first.")

    def plot_scatter(self):
        if self.parent.full_data is not None:
            columns = self.parent.full_data.select_dtypes(include=['float64', 'int64']).columns.tolist()
            if len(columns) >= 2:
                col_x, ok_x = QInputDialog.getItem(self, "Select X Column", "Choose X column for scatter plot:", columns, 0, False)
                if ok_x:
                    col_y, ok_y = QInputDialog.getItem(self, "Select Y Column", "Choose Y column for scatter plot:", columns, 1, False)
                    if ok_y:
                        # Calculate Pearson correlation coefficient
                        correlation = self.parent.full_data[[col_x, col_y]].corr().iloc[0, 1]

                        # Create scatter plot
                        plt.figure(figsize=(8, 6))
                        plt.scatter(self.parent.full_data[col_x], self.parent.full_data[col_y], alpha=0.5)
                        plt.title(f'Scatter Plot of {col_x} vs {col_y}')
                        plt.xlabel(col_x)
                        plt.ylabel(col_y)

                        # Display Pearson correlation coefficient on the plot
                        plt.annotate(f'Pearson Correlation: {correlation:.2f}', 
                                     xy=(0.05, 0.95), xycoords='axes fraction', 
                                     fontsize=12, color='red', 
                                     bbox=dict(boxstyle="round,pad=0.3", edgecolor='red', facecolor='white'))

                        plt.show()
            else:
                QMessageBox.warning(self, "Insufficient Columns", "Need at least two numeric columns for scatter plot.")
        else:
            QMessageBox.warning(self, "No Data", "Please import a dataset first.")

    def plot_histogram(self):
        if self.parent.full_data is not None:
            # Check for numeric columns
            columns = self.parent.full_data.select_dtypes(include=['float64', 'int64']).columns.tolist()
            if not columns:
                QMessageBox.warning(self, "No Numeric Columns", "No numeric columns available for histogram.")
                return
            
            # Check for discretized columns
            discretized_columns = self.parent.full_data.select_dtypes(include=['category', 'object']).columns.tolist()
            column, ok_col = QInputDialog.getItem(self, "Select Column", "Choose column for histogram:", columns, 0, False)
            if ok_col:
                if discretized_columns:
                    # Optional selection for discretization
                    discretize_column, ok_discretize = QInputDialog.getItem(
                        self, "Select Discretized Column", "Choose discretized column (optional):", discretized_columns, 0, True)
                    if ok_discretize:
                        plt.figure(figsize=(8, 6))
                        self.parent.full_data.groupby(discretize_column)[column].plot.hist(alpha=0.5, legend=True)
                        plt.title(f'Histogram of {column} grouped by {discretize_column}')
                        plt.xlabel(column)
                        plt.show()
                    else:
                        # Standard histogram without discretization
                        plt.figure(figsize=(8, 6))
                        self.parent.full_data[column].plot.hist(bins=20, alpha=0.7)
                        plt.title(f'Histogram of {column}')
                        plt.xlabel(column)
                        plt.ylabel('Frequency')
                        plt.show()
                else:
                    # No discretized columns available; plot a simple histogram
                    plt.figure(figsize=(8, 6))
                    self.parent.full_data[column].plot.hist(bins=20, alpha=0.7)
                    plt.title(f'Histogram of {column}')
                    plt.xlabel(column)
                    plt.ylabel('Frequency')
                    plt.show()
        else:
            QMessageBox.warning(self, "No Data", "Please import a dataset first.")
