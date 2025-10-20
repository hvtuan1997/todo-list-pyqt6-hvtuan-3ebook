from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton)
from PyQt6.QtCore import Qt

class TaskDetailDialog(QDialog):
    EDIT_REQUESTED_CODE = 2

    def __init__(self, task_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Chi tiết Công việc")
        self.setMinimumWidth(350)

        main_layout = QVBoxLayout()
        
        title = task_data.get('title', 'N/A')
        details = task_data.get('details', 'Không có chi tiết.')
        priority = task_data.get('priority', 'Thấp')
        due_date = task_data.get('due_date', 'N/A')
        
        if priority == "Cao": priority_html = f'<font color="#e74c3c"><b>{priority}</b></font>'
        elif priority == "Trung bình": priority_html = f'<font color="#f39c12"><b>{priority}</b></font>'
        else: priority_html = f'<font color="#2ecc71"><b>{priority}</b></font>'
            
        content_text = f"""
        <h2 style="color: #3498db;">{title}</h2>
        <p><b>Chi tiết:</b><br>{details.replace('\n', '<br>')}</p>
        <p><b>Mức độ ưu tiên:</b> {priority_html}</p>
        <p><b>Ngày hết hạn:</b> {due_date}</p>
        """
        content_label = QLabel(content_text)
        content_label.setWordWrap(True)

        close_button, edit_button = QPushButton("Đóng"), QPushButton("Sửa")
        close_button.clicked.connect(self.accept)
        edit_button.clicked.connect(self.request_edit)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(edit_button)
        button_layout.addWidget(close_button)

        main_layout.addWidget(content_label)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def request_edit(self):
        self.done(self.EDIT_REQUESTED_CODE)