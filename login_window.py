import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QGridLayout, QHBoxLayout, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal 

class LoginWindow(QWidget):
    show_register_signal = pyqtSignal()
    login_success_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        form_layout = QGridLayout()
        button_layout = QHBoxLayout()

        title_label = QLabel("Đăng nhập")
        title_label.setObjectName("TitleLabel")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nhập tài khoản admin")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Nhập mật khẩu 123")

        register_button = QPushButton("Chưa có tài khoản? Đăng ký")
        register_button.setObjectName("LinkButton")
        login_button = QPushButton("Đăng nhập")

        form_layout.addWidget(QLabel("Tên đăng nhập:"), 0, 0)
        form_layout.addWidget(self.username_input, 0, 1)
        form_layout.addWidget(QLabel("Mật khẩu:"), 1, 0)
        form_layout.addWidget(self.password_input, 1, 1)

        button_layout.addWidget(register_button)
        button_layout.addStretch()
        button_layout.addWidget(login_button)
        
        main_layout.addWidget(title_label)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)

        login_button.clicked.connect(self.handle_login)
        register_button.clicked.connect(self.show_register_signal.emit)
        self.password_input.returnPressed.connect(self.handle_login)

    def handle_login(self):
        if self.username_input.text() == "admin" and self.password_input.text() == "123":
            self.login_success_signal.emit()
        else:
            QMessageBox.warning(self, "Thất bại", "Sai tên đăng nhập hoặc mật khẩu!")
            self.password_input.clear()