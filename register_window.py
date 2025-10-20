import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QGridLayout, QHBoxLayout, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal

class RegisterWindow(QWidget):
    show_login_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        form_layout = QGridLayout()
        button_layout = QHBoxLayout()

        title_label = QLabel("Tạo tài khoản mới")
        title_label.setObjectName("TitleLabel")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.display_name_input = QLineEdit()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #e74c3c;")
        self.error_label.hide()

        register_button = QPushButton("Đăng ký")
        back_to_login_button = QPushButton("Quay lại Đăng nhập")
        back_to_login_button.setObjectName("LinkButton")

        form_layout.addWidget(QLabel("Tên hiển thị:"), 0, 0)
        form_layout.addWidget(self.display_name_input, 0, 1)
        form_layout.addWidget(QLabel("Tên đăng nhập:"), 1, 0)
        form_layout.addWidget(self.username_input, 1, 1)
        form_layout.addWidget(QLabel("Mật khẩu:"), 2, 0)
        form_layout.addWidget(self.password_input, 2, 1)
        form_layout.addWidget(QLabel("Nhập lại mật khẩu:"), 3, 0)
        form_layout.addWidget(self.confirm_password_input, 3, 1)
        form_layout.addWidget(self.error_label, 4, 0, 1, 2)

        button_layout.addWidget(back_to_login_button)
        button_layout.addStretch()
        button_layout.addWidget(register_button)

        main_layout.addWidget(title_label)
        main_layout.addLayout(form_layout)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)

        register_button.clicked.connect(self.handle_register)
        back_to_login_button.clicked.connect(self.show_login_signal.emit)
        self.password_input.textChanged.connect(self.error_label.hide)
        self.confirm_password_input.textChanged.connect(self.error_label.hide)

    def handle_register(self):
        password = self.password_input.text()
        if not all([self.display_name_input.text(), self.username_input.text(), password, self.confirm_password_input.text()]):
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin.")
            return
        if len(self.username_input.text()) < 5:
            QMessageBox.warning(self, "Lỗi", "Tên đăng nhập phải có ít nhất 5 ký tự.")
            return
        if len(password) < 6:
            QMessageBox.warning(self, "Lỗi", "Mật khẩu phải có ít nhất 6 ký tự.")
            return
        if password != self.confirm_password_input.text():
            self.error_label.setText("Mật khẩu nhập lại không khớp!")
            self.error_label.show()
            return
        
        QMessageBox.information(self, "Thành công", f"Đăng ký tài khoản '{self.username_input.text()}' thành công!")
        self.show_login_signal.emit()