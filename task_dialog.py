from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QComboBox, QDateEdit, QPushButton, QMessageBox)
from PyQt6.QtCore import QDate

class TaskDialog(QDialog):
    def __init__(self, task_data=None, parent=None):
        super().__init__(parent)
        self.is_edit_mode = task_data is not None
        self.setWindowTitle("Chỉnh sửa công việc" if self.is_edit_mode else "Thêm công việc mới")
        self.setMinimumWidth(400)

        main_layout = QVBoxLayout()
        form_layout = QGridLayout()

        self.title_input = QLineEdit()
        self.details_input = QTextEdit()
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["Thấp", "Trung bình", "Cao"])
        self.due_date_input = QDateEdit(calendarPopup=True, date=QDate.currentDate())

        form_layout.addWidget(QLabel("Tiêu đề:"), 0, 0)
        form_layout.addWidget(self.title_input, 0, 1)
        form_layout.addWidget(QLabel("Chi tiết:"), 1, 0)
        form_layout.addWidget(self.details_input, 1, 1)
        form_layout.addWidget(QLabel("Mức độ ưu tiên:"), 2, 0)
        form_layout.addWidget(self.priority_combo, 2, 1)
        form_layout.addWidget(QLabel("Ngày hết hạn:"), 3, 0)
        form_layout.addWidget(self.due_date_input, 3, 1)

        if self.is_edit_mode:
            self.title_input.setText(task_data.get('title', ''))
            self.details_input.setText(task_data.get('details', ''))
            self.priority_combo.setCurrentText(task_data.get('priority', 'Thấp'))
            if due_date := task_data.get('due_date'):
                self.due_date_input.setDate(QDate.fromString(due_date, "yyyy-MM-dd"))
        
        ok_button, cancel_button = QPushButton("OK"), QPushButton("Hủy")
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)

        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def get_task_data(self):
        return {
            'title': self.title_input.text(),
            'details': self.details_input.toPlainText(),
            'priority': self.priority_combo.currentText(),
            'due_date': self.due_date_input.date().toString("yyyy-MM-dd")
        }

    def accept(self):
        if not self.title_input.text().strip():
            QMessageBox.warning(self, "Thiếu thông tin", "Tiêu đề công việc không được để trống!")
            return 
        super().accept()