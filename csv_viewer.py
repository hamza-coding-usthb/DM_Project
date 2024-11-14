import sys
import pandas as pd
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QTableWidget,
                             QTableWidgetItem, QLabel, QHBoxLayout, QInputDialog, QMessageBox, QSplitter)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from data_manipulation_dialog import DataManipulationDialog
from data_cleaning_dialog import DataCleaningDialog
from data_normalization_dialog import DataNormalizationDialog
from data_aggregation_dialog import DataAggregationDialog
from data_discretization_dialog import DataDiscretizationDialog
from data_visualization_dialog import DataVisualizationDialog
from data_merger_dialog import DataMergerDialog


class CsvViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Mining Utility")
        self.setGeometry(100, 100, 1000, 600)
        self.setWindowIcon(QIcon("Cloud.jpeg"))  # Replace "Cloud.jpeg" with the path to your logo file

        # Initialize variables for pagination
        self.full_data = None
        self.chunk_size = 1000
        self.current_page = 0
        self.total_pages = 0

        # Initialize UI
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()
        splitter = QSplitter(Qt.Horizontal)

        # Left sidebar for buttons
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout()
        buttons = [
            ("Data Manipulation", self.open_data_manipulation),
            ("Data Cleaning", self.open_data_cleaning),
            ("Data Normalization", self.open_data_normalization),
            ("Data Aggregation", self.open_data_aggregation),
            ("Data Merger", self.open_data_merger),
            ("Data Discretization", self.open_data_discretization),
            ("Data Visualization", self.open_data_visualization),
            ("Copy Selection", self.copy_selection),  
        ]
        for text, func in buttons:
            button = QPushButton(text)
            button.clicked.connect(func)
            button.setFixedHeight(40)
            sidebar_layout.addWidget(button)
        sidebar.setLayout(sidebar_layout)
        sidebar.setFixedWidth(200)
        sidebar_layout.addStretch()

        # Data display area
        data_display_area = QWidget()
        data_layout = QVBoxLayout(data_display_area)
        self.table = QTableWidget()
        self.table.setSelectionBehavior(QTableWidget.SelectItems)  # Allows cell-by-cell selection
        self.table.setSelectionMode(QTableWidget.ExtendedSelection)  # Allows multi-cell selection
        data_layout.addWidget(self.table)

        # Pagination controls
        nav_layout = QHBoxLayout()
        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.load_previous_page)
        self.prev_button.setEnabled(False)
        nav_layout.addWidget(self.prev_button)

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.load_next_page)
        self.next_button.setEnabled(False)
        nav_layout.addWidget(self.next_button)

        # Go-to-page button
        self.jump_button = QPushButton("Go to Page")
        self.jump_button.clicked.connect(self.go_to_page)
        nav_layout.addWidget(self.jump_button)

        self.page_label = QLabel("Page: 0/0")
        nav_layout.addWidget(self.page_label)
        data_layout.addLayout(nav_layout)

        # Setup splitter and central widget
        splitter.addWidget(sidebar)
        splitter.addWidget(data_display_area)
        main_layout.addWidget(splitter)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        self.apply_styles()
    def copy_selection(self):
        """Copies selected cells to the clipboard."""
        selected_ranges = self.table.selectedRanges()
        if not selected_ranges:
            QMessageBox.warning(self, "No Selection", "Please select a section of the data to copy.")
            return

        selected_data = ""
        for range_ in selected_ranges:
            for row in range(range_.topRow(), range_.bottomRow() + 1):
                row_data = []
                for col in range(range_.leftColumn(), range_.rightColumn() + 1):
                    item = self.table.item(row, col)
                    row_data.append(item.text() if item else "")
                selected_data += "\t".join(row_data) + "\n"

        # Copy to clipboard
        clipboard = QApplication.clipboard()
        clipboard.setText(selected_data)
        QMessageBox.information(self, "Copy Complete", "Selected data has been copied to the clipboard.")

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #1a1a1a;
                color: white;
            }
            QPushButton {
                background-color: #2a1e33;
                color: #ffffff;
                border-radius: 8px;
                font-size: 14px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3b2a4e;
            }
            QTableWidget {
                background-color: #1a1a1a;
                color: #ffffff;
                font-size: 13px;
                gridline-color: #333333;
            }
            QLabel {
                font-size: 14px;
                color: #ffffff;
            }
            QMainWindow {
                border-radius: 15px;
            }
        """)
        font = QFont("Verdana", 10, QFont.Bold)
        self.setFont(font)

    # New function to go to a specific page
    def go_to_page(self):
        if self.full_data is not None:
            page_num, ok = QInputDialog.getInt(self, "Go to Page", f"Enter page number (1-{self.total_pages}):", min=1, max=self.total_pages)
            if ok:
                self.current_page = page_num - 1
                self.display_data()

    def open_data_visualization(self):
        dialog = DataVisualizationDialog(self)
        dialog.exec_()

    def open_data_discretization(self):
        dialog = DataDiscretizationDialog(self)
        dialog.exec_()

    def open_data_merger(self):
        dialog = DataMergerDialog(self)
        dialog.exec_()

    def open_data_aggregation(self):
        dialog = DataAggregationDialog(self)
        dialog.exec_()

    def open_data_manipulation(self):
        dialog = DataManipulationDialog(self)
        dialog.exec_()

    def open_data_cleaning(self):
        dialog = DataCleaningDialog(self)
        dialog.exec_()

    def open_data_normalization(self):
        dialog = DataNormalizationDialog(self)
        dialog.exec_()

    def update_total_pages(self):
        if self.full_data is not None:
            self.total_pages = (len(self.full_data) // self.chunk_size) + (1 if len(self.full_data) % self.chunk_size != 0 else 0)
            self.page_label.setText(f"Page: {self.current_page + 1}/{self.total_pages}")

    def display_data(self):
        if self.full_data is None:
            return

        # Define start and end row indices for the current page
        start_row = self.current_page * self.chunk_size
        end_row = min(start_row + self.chunk_size, len(self.full_data))
        chunk = self.full_data.iloc[start_row:end_row]

        # Update table with continuous row indices
        self.table.setRowCount(chunk.shape[0])
        self.table.setColumnCount(chunk.shape[1])
        self.table.setHorizontalHeaderLabels(chunk.columns)

        for i, (index, row) in enumerate(chunk.iterrows()):
            for j, value in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))
            self.table.setVerticalHeaderItem(i, QTableWidgetItem(str(index + 1)))  # Set continuous row index

        self.update_total_pages()
        self.prev_button.setEnabled(self.current_page > 0)
        self.next_button.setEnabled(self.current_page < self.total_pages - 1)

    def load_previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.display_data()

    def load_next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.display_data()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = CsvViewer()
    viewer.show()
    sys.exit(app.exec_())
