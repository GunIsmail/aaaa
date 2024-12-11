import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap, QIcon, QStandardItemModel, QStandardItem
import csv


class Mainform(QMainWindow):
    def __init__(self):
        super(Mainform, self).__init__()

        self.setWindowTitle('Ders Programı Oluşturucu')
        self.setGeometry(200, 200, 600, 600)
        self.initUI()

    def initUI(self):
        # Main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # File select button
        self.file_button = QPushButton("CSV Dosyası Seç", self)
        self.file_button.clicked.connect(self.select_file)
        self.layout.addWidget(self.file_button)

        # Label to show selected file
        self.file_label = QLabel("Seçilen dosya: Henüz bir dosya seçilmedi.", self)
        self.layout.addWidget(self.file_label)

        # Submit button
        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.submit_file)
        self.submit_button.setEnabled(False)  # Not active until a file is selected
        self.layout.addWidget(self.submit_button)

        # Result label for showing messages
        self.result_label = QLabel("", self)
        self.layout.addWidget(self.result_label)

        # Edit data button
        self.edit_button = QPushButton("Verileri Düzenle", self)
        self.edit_button.clicked.connect(self.edit_data)
        self.edit_button.setEnabled(False)
        self.layout.addWidget(self.edit_button)

        # # Show classrooms button
        self.show_classrooms_button = QPushButton("Derslikleri Göster", self)
        # self.show_classrooms_button.clicked.connect(self.show_classrooms)
        self.show_classrooms_button.setEnabled(False)
        self.layout.addWidget(self.show_classrooms_button)

        # Generate schedule button
        self.generate_button = QPushButton("Ders Programı Oluştur", self)
        self.generate_button.clicked.connect(self.generator)
        self.generate_button.setEnabled(False)
        self.layout.addWidget(self.generate_button)

        self.selected_file = None  # Path to selected file
        self.data = None  # Data from CSV file

    def select_file(self):
        # Open file dialog to select a CSV file
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "CSV Dosyası Seç", "", "CSV Files (*.csv);;All Files (*)", options=options
        )
        if file_path:
            self.selected_file = file_path
            self.file_label.setText(f"Seçilen dosya: {file_path}")
            self.submit_button.setEnabled(True)

    def submit_file(self):
        if self.selected_file:
            try:
                # Read the CSV file and process it
                with open(self.selected_file, mode='r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    self.data = list(reader)  # Store data

                self.result_label.setText(f"{len(self.data)} satır başarıyla yüklendi.")
                self.edit_button.setEnabled(True)
                self.show_classrooms_button.setEnabled(True)
                self.generate_button.setEnabled(True)
            except Exception as e:
                self.result_label.setText(f"Hata: {str(e)}")

    def edit_data(self):
        if self.data:
            self.show_edit_window()

    def show_edit_window(self):
        self.edit_window = QDialog(self)
        self.edit_window.setWindowTitle("Verileri Düzenle")
        self.edit_window.setGeometry(300, 300, 800, 600)

        layout = QVBoxLayout(self.edit_window)

        # Table view for data
        self.table_view = QTableView(self.edit_window)
        self.table_model = QStandardItemModel(len(self.data), len(self.data[0]))
        self.table_model.setHorizontalHeaderLabels(self.data[0].keys())

        # Populate the table
        for row_index, row in enumerate(self.data):
            for col_index, (key, value) in enumerate(row.items()):
                item = QStandardItem(value)
                self.table_model.setItem(row_index, col_index, item)

        self.table_view.setModel(self.table_model)
        layout.addWidget(self.table_view)

        # Add, Edit, Delete buttons
        button_layout = QHBoxLayout()

        add_button = QPushButton("Ekle", self.edit_window)
        add_button.clicked.connect(self.add_row)
        button_layout.addWidget(add_button)

        delete_button = QPushButton("Sil", self.edit_window)
        delete_button.clicked.connect(self.delete_row)
        button_layout.addWidget(delete_button)

        layout.addLayout(button_layout)

        # Save button
        save_button = QPushButton("Kaydet", self.edit_window)
        save_button.clicked.connect(self.save_data)
        layout.addWidget(save_button)

        self.edit_window.setLayout(layout)
        self.edit_window.exec_()

    def add_row(self):
        new_row = [QStandardItem("") for _ in range(self.table_model.columnCount())]
        self.table_model.appendRow(new_row)

    def delete_row(self):
        selected_indexes = self.table_view.selectionModel().selectedRows()
        for index in sorted(selected_indexes, reverse=True):
            self.table_model.removeRow(index.row())

    def edit_derslik(self):
        self.derslik_window = QDialog(self)
        self.derslik_window.setWindowTitle("Derslik Düzenle")
        self.derslik_window.setGeometry(300, 300, 400, 300)

        layout = QVBoxLayout(self.derslik_window)

        # List view for derslik
        self.derslik_list_view = QListView(self.derslik_window)
        self.derslik_model = QStringListModel()

        # Filter out NULL or empty ("") values from the data
        derslik_list = [row.get("Derslik", "") for row in self.data if row.get("Derslik", "") not in [None, ""]]

        # Set the filtered list to the model
        self.derslik_model.setStringList(derslik_list)

        self.derslik_list_view.setModel(self.derslik_model)
        layout.addWidget(self.derslik_list_view)

        # Add, Edit, Delete buttons for derslik
        button_layout = QHBoxLayout()

        add_derslik_button = QPushButton("Ekle", self.derslik_window)
        add_derslik_button.clicked.connect(self.add_derslik)
        button_layout.addWidget(add_derslik_button)

        delete_derslik_button = QPushButton("Sil", self.derslik_window)
        delete_derslik_button.clicked.connect(self.delete_derslik)
        button_layout.addWidget(delete_derslik_button)

        layout.addLayout(button_layout)

        self.derslik_window.setLayout(layout)
        self.derslik_window.exec_()

    def add_derslik(self):
        # Input dialog to add new classroom
        text, ok = QInputDialog.getText(self, "Yeni Derslik Ekle", "Derslik adı girin:")

        if ok and text:
            # If the entered text is "Unknown" or empty, do not add it to the list
            if text.lower() == "unknown" or text == "":
                self.result_label.setText("Geçersiz derslik adı. 'Unknown' veya boş derslik eklenemez.")
                return
            
            # Update the model with the new classroom
            self.derslik_model.insertRow(self.derslik_model.rowCount())
            self.derslik_model.setData(self.derslik_model.index(self.derslik_model.rowCount() - 1), text)

            # Add the new classroom to the data
            new_classroom = {"Derslik": text}
            for key in self.data[0].keys():
                if key != "Derslik":
                    new_classroom[key] = ""  # Fill empty data for other columns
            self.data.append(new_classroom)

            # Save the updated data to the CSV
            self.save_updated_data()

    def delete_derslik(self):
        selected_indexes = self.derslik_list_view.selectedIndexes()
        for index in selected_indexes:
            # Use the correct 'role' argument to fetch the classroom name
            classroom_name = self.derslik_model.data(index, Qt.DisplayRole)
            
            # Remove selected classroom from the list
            self.derslik_model.removeRow(index.row())

            # Remove classroom from the data as well
            self.data = [row for row in self.data if row.get("Derslik") != classroom_name]

    def save_data(self):
        self.data = []
        for row_index in range(self.table_model.rowCount()):
            row_data = {}
            for col_index in range(self.table_model.columnCount()):
                header = self.table_model.horizontalHeaderItem(col_index).text()
                item = self.table_model.item(row_index, col_index)
                row_data[header] = item.text() if item else ""
            self.data.append(row_data)

        self.save_updated_data()
        self.result_label.setText("Veriler başarıyla kaydedildi.")
        self.edit_window.close()

    def save_updated_data(self):
        if self.selected_file:
            try:
                with open(self.selected_file, mode='w', newline='', encoding='utf-8') as file:
                    fieldnames = self.data[0].keys()
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(self.data)
            except Exception as e:
                self.result_label.setText(f"Veri kaydedilirken hata oluştu: {str(e)}")

    def show_classrooms(self):
        self.result_label.setText("Derslikler gösteriliyor...")
        # Open the Derslik editing window
        self.edit_derslik()

    def generator(self):
        self.result_label.setText("Ders programı oluşturuluyor...")


def app():
    application = QApplication(sys.argv)
    app_icon = QIcon("Ankara_University_Logo.png")  # Ensure the path is correct
    application.setWindowIcon(app_icon)

    win = Mainform()
    win.show()

    sys.exit(application.exec_())


if __name__ == "__main__":
    app()
