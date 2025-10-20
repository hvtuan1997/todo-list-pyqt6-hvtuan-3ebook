import sys
import json
from PyQt6.QtWidgets import (QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QToolBar, QListWidget, QListWidgetItem, QMessageBox, QComboBox, QLineEdit, QPushButton, QProgressBar)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QAction, QCloseEvent, QKeyEvent, QFont, QColor

from task_manager import TaskManager
from login_window import LoginWindow
from register_window import RegisterWindow
from task_dialog import TaskDialog
from task_detail_dialog import TaskDetailDialog

stylesheet = """
    QWidget { background-color: #2c3e50; color: #ecf0f1; font-size: 14px; }
    QMainWindow, QDialog { background-color: #2c3e50; }
    QPushButton { background-color: #3498db; color: white; border: none; padding: 8px 16px; border-radius: 4px; font-weight: bold; }
    QPushButton:hover { background-color: #2980b9; }
    QPushButton:pressed { background-color: #1a5276; }
    QPushButton#LinkButton { background-color: transparent; border: none; color: #3498db; text-align: left; font-weight: normal; }
    QPushButton#LinkButton:hover { color: #5dade2; }
    QLineEdit, QTextEdit, QComboBox, QDateEdit { background-color: #34495e; border: 1px solid #7f8c8d; border-radius: 4px; padding: 5px; }
    QListWidget { border: 1px solid #7f8c8d; border-radius: 4px; }
    QListWidget::item:hover { background-color: #34495e; }
    QListWidget::item:selected { background-color: #3498db; }
    QToolBar { background-color: #34495e; border: none; padding: 5px; }
    QToolBar QToolButton { padding: 5px; border-radius: 4px; }
    QToolBar QToolButton:hover { background-color: #2c3e50; }
    QStatusBar { color: #bdc3c7; }
    QLabel#TitleLabel { font-size: 24px; font-weight: bold; color: #ecf0f1; margin-bottom: 10px; }
    QProgressBar { border: 1px solid #7f8c8d; border-radius: 4px; text-align: center; }
    QProgressBar::chunk { background-color: #2ecc71; }
    QPushButton#ClearSearchButton {
        font-size: 16px;
        font-weight: bold;
        padding: 0px; /* Loại bỏ padding để chữ "X" không bị đẩy đi */
        border-radius: 14px; /* Làm cho nút tròn (1/2 kích thước 28px) */
    }
    QPushButton#ClearSearchButton:hover {
        background-color: #c0392b; /* Đổi sang màu đỏ khi di chuột vào */
    }
"""

class MainScreen(QWidget):
    item_selected_signal = pyqtSignal(str)
    view_details_signal = pyqtSignal(QListWidgetItem)
    task_state_changed_signal = pyqtSignal(QListWidgetItem, bool)
    filter_changed_signal = pyqtSignal(str)
    sort_changed_signal = pyqtSignal(str)
    search_text_changed_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout()
        controls_layout = QHBoxLayout()

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Tất cả", "Chưa hoàn thành", "Đã hoàn thành"])
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Tiêu đề (A-Z)", "Ngày hết hạn", "Mức độ ưu tiên"])
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Tìm kiếm...")
        clear_search_button = QPushButton("X")
        clear_search_button.setObjectName("ClearSearchButton")
        clear_search_button.setFixedSize(28, 28)
        clear_search_button.setToolTip("Xóa nội dung tìm kiếm")

        controls_layout.addWidget(QLabel("Lọc:"))
        controls_layout.addWidget(self.filter_combo)
        controls_layout.addSpacing(15)
        controls_layout.addWidget(QLabel("Sắp xếp:"))
        controls_layout.addWidget(self.sort_combo)
        controls_layout.addStretch()
        controls_layout.addWidget(self.search_input)
        controls_layout.addWidget(clear_search_button)
        
        main_layout.addLayout(controls_layout)
        self.todo_list = QListWidget()
        main_layout.addWidget(self.todo_list)
        self.setLayout(main_layout)

        self.filter_combo.currentTextChanged.connect(self.filter_changed_signal.emit)
        self.sort_combo.currentTextChanged.connect(self.sort_changed_signal.emit)
        self.search_input.textChanged.connect(self.search_text_changed_signal.emit)
        clear_search_button.clicked.connect(self.search_input.clear)
        self.todo_list.itemClicked.connect(self.on_item_clicked)
        self.todo_list.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.todo_list.itemChanged.connect(self.on_item_changed)
        
    def load_tasks(self, tasks):
        current_selection = self.todo_list.currentItem().text() if self.todo_list.currentItem() else None
        self.todo_list.blockSignals(True)
        self.todo_list.clear()
        for task in tasks:
            item = QListWidgetItem(task['title'])
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            is_completed = task.get('completed', False)
            item.setCheckState(Qt.CheckState.Checked if is_completed else Qt.CheckState.Unchecked)
            
            self.apply_completed_style(item, is_completed)
            
            tooltip_text = f"Ưu tiên: {task.get('priority', 'N/A')}\nHết hạn: {task.get('due_date', 'N/A')}"
            item.setToolTip(tooltip_text)
            self.todo_list.addItem(item)
            if task['title'] == current_selection:
                self.todo_list.setCurrentItem(item)
        self.todo_list.blockSignals(False)
    
    def apply_completed_style(self, item, is_completed):
        """Hàm trợ giúp để áp dụng hiệu ứng gạch ngang/đổi màu."""
        font = item.font()
        font.setStrikeOut(is_completed)
        item.setFont(font)
        item.setForeground(QColor('#7f8c8d') if is_completed else QColor('#ecf0f1'))

    def on_item_clicked(self, item): self.item_selected_signal.emit(item.text())
    def on_item_double_clicked(self, item): self.view_details_signal.emit(item)
    def on_item_changed(self, item): self.task_state_changed_signal.emit(item, item.checkState() == Qt.CheckState.Checked)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ứng dụng To-Do List")
        self.setGeometry(200, 200, 800, 600)
        self.progress_bar = QProgressBar()
        self.statusBar().addPermanentWidget(self.progress_bar)
        
        self.task_manager = TaskManager("tasks.json")
        config = self.task_manager.load_config()
        self.current_filter = config.get("last_filter", "Tất cả")
        self.current_sort_key = config.get("last_sort", "Tiêu đề (A-Z)")
        self.current_search_term = ""

        self.init_ui()
        self.main_page.filter_combo.setCurrentText(self.current_filter)
        self.main_page.sort_combo.setCurrentText(self.current_sort_key)
        
        self.setup_connections()
        self.refresh_ui()

    def init_ui(self):
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)
        actions = {
            "add": QAction(QIcon("icons/add.png"), "Thêm mới (Ctrl+N)", self),
            "edit": QAction(QIcon("icons/edit.png"), "Sửa (F2)", self),
            "delete": QAction(QIcon("icons/delete.png"), "Xóa (Delete)", self),
            "toggle": QAction(QIcon("icons/toggle.png"), "Hoàn thành/Chưa xong", self),
            "cleanup": QAction(QIcon("icons/cleanup.png"), "Dọn dẹp", self),
            "sort": QAction(QIcon("icons/sort.png"), "Sắp xếp", self)
        }
        actions["add"].setShortcut("Ctrl+N")
        actions["edit"].setShortcut("F2")
        actions["delete"].setShortcut("Delete")

        toolbar.addAction(actions["add"])
        toolbar.addAction(actions["edit"])
        toolbar.addAction(actions["delete"])
        toolbar.addAction(actions["toggle"])
        toolbar.addSeparator()
        toolbar.addAction(actions["cleanup"])
        
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        self.login_page, self.register_page, self.main_page = LoginWindow(), RegisterWindow(), MainScreen()
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.register_page)
        self.stacked_widget.addWidget(self.main_page)
        self.go_to_login_page()

    def setup_connections(self):
        self.login_page.show_register_signal.connect(self.go_to_register_page)
        self.register_page.show_login_signal.connect(self.go_to_login_page)
        self.login_page.login_success_signal.connect(self.go_to_main_page)
        
        self.main_page.item_selected_signal.connect(self.update_status_bar)
        self.main_page.view_details_signal.connect(self.show_task_details)
        self.main_page.task_state_changed_signal.connect(self.update_task_completion)
        self.main_page.filter_changed_signal.connect(self.apply_filter)
        self.main_page.sort_changed_signal.connect(self.apply_sort)
        self.main_page.search_text_changed_signal.connect(self.handle_search)

        actions = self.findChild(QToolBar).actions()
        actions[0].triggered.connect(self.add_todo)
        actions[1].triggered.connect(self.edit_todo)
        actions[2].triggered.connect(self.delete_todo)
        actions[3].triggered.connect(self.toggle_task_completion)
        actions[5].triggered.connect(self.delete_completed_tasks)
        
    def closeEvent(self, event: QCloseEvent):
        config_data = {"last_filter": self.current_filter, "last_sort": self.current_sort_key}
        self.task_manager.save_config(config_data)
        self.task_manager.save_tasks()
        event.accept()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Delete and self.stacked_widget.currentWidget() == self.main_page:
            self.delete_todo()
        else:
            super().keyPressEvent(event)

    def refresh_ui(self):
        self.task_manager.sort_tasks(self.current_sort_key)
        tasks_to_show = self.task_manager.search_tasks(self.current_search_term)
        
        if self.current_filter == "Chưa hoàn thành":
            tasks_to_show = [t for t in tasks_to_show if not t.get('completed', False)]
        elif self.current_filter == "Đã hoàn thành":
            tasks_to_show = [t for t in tasks_to_show if t.get('completed', False)]
            
        self.main_page.load_tasks(tasks_to_show)
        self.update_progress_bar()

    def find_task_by_item(self, item):
        return next((task for task in self.task_manager.get_all_tasks() if task['title'] == item.text()), None) if item else None

    def add_todo(self):
        dialog = TaskDialog(parent=self)
        if dialog.exec():
            self.task_manager.add_task(dialog.get_task_data())
            self.refresh_ui()

    def edit_todo(self):
        current_item = self.main_page.todo_list.currentItem()
        if not current_item: return
        task_data = self.find_task_by_item(current_item)
        if not task_data: return
        dialog = TaskDialog(task_data=task_data, parent=self)
        if dialog.exec():
            self.task_manager.update_task(task_data, dialog.get_task_data())
            self.refresh_ui()

    def delete_todo(self):
        current_item = self.main_page.todo_list.currentItem()
        if not current_item: return
        reply = QMessageBox.question(self, "Xác nhận", f"Xóa công việc:\n'{current_item.text()}'?")
        if reply == QMessageBox.StandardButton.Yes:
            task_to_delete = self.find_task_by_item(current_item)
            if task_to_delete:
                self.task_manager.delete_task(task_to_delete)
                self.refresh_ui()

    def show_task_details(self, item):
        task_data = self.find_task_by_item(item)
        if task_data:
            dialog = TaskDetailDialog(task_data, self)
            if dialog.exec() == TaskDetailDialog.EDIT_REQUESTED_CODE:
                self.edit_todo()

    def toggle_task_completion(self):
        if current_item := self.main_page.todo_list.currentItem():
            current_state = current_item.checkState()
            current_item.setCheckState(Qt.CheckState.Unchecked if current_state == Qt.CheckState.Checked else Qt.CheckState.Checked)

    def delete_completed_tasks(self):
        if QMessageBox.question(self, "Xác nhận", "Xóa tất cả các công việc đã hoàn thành?") == QMessageBox.StandardButton.Yes:
            self.task_manager.remove_completed_tasks()
            self.refresh_ui()

    def update_task_completion(self, item, is_completed):
        task_data = self.find_task_by_item(item)
        if task_data:
            self.task_manager.update_task_completion(task_data, is_completed)
            self.main_page.apply_completed_style(item, is_completed)
            if self.current_filter != "Tất cả": self.refresh_ui()
            else: self.update_progress_bar()

    def update_progress_bar(self):
        all_tasks = self.task_manager.get_all_tasks()
        if not all_tasks:
            self.progress_bar.setValue(0)
            return
        completed_count = sum(1 for t in all_tasks if t.get('completed', False))
        total_count = len(all_tasks)
        percentage = int((completed_count / total_count) * 100)
        self.progress_bar.setValue(percentage)
        self.progress_bar.setFormat(f"{completed_count}/{total_count}")

    def apply_filter(self, text): self.current_filter = text; self.refresh_ui()
    def apply_sort(self, text): self.current_sort_key = text; self.refresh_ui()
    def handle_search(self, text): self.current_search_term = text; self.refresh_ui()
    def update_status_bar(self, text): self.statusBar().showMessage(f"Đã chọn: {text}")
    def go_to_register_page(self): self.stacked_widget.setCurrentIndex(1)
    def go_to_login_page(self): self.stacked_widget.setCurrentIndex(0)
    def go_to_main_page(self): self.stacked_widget.setCurrentIndex(2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())