import json

class TaskManager:
    def __init__(self, filename):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_tasks(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=4)

    def load_config(self):
        try:
            with open("config.json", 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"last_filter": "Tất cả", "last_sort": "Tiêu đề (A-Z)"}

    def save_config(self, config_data):
        with open("config.json", 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=4)

    def get_all_tasks(self):
        return self.tasks

    def add_task(self, task_data):
        if 'completed' not in task_data:
            task_data['completed'] = False
        self.tasks.append(task_data)

    def update_task(self, task_to_update, updated_data):
        if task_to_update in self.tasks:
            task_to_update.update(updated_data)

    def delete_task(self, task_to_delete):
        if task_to_delete in self.tasks:
            self.tasks.remove(task_to_delete)

    def update_task_completion(self, task_to_update, is_completed):
        if task_to_update in self.tasks:
            task_to_update['completed'] = is_completed

    def remove_completed_tasks(self):
        self.tasks = [task for task in self.tasks if not task.get('completed', False)]

    def sort_tasks(self, sort_key):
        reverse_order = False
        key_function = lambda task: task.get('title', '').lower()

        if sort_key == "Ngày hết hạn":
            key_function = lambda task: task.get('due_date', '9999-99-99')
        elif sort_key == "Mức độ ưu tiên":
            priority_map = {"Cao": 3, "Trung bình": 2, "Thấp": 1}
            key_function = lambda task: priority_map.get(task.get('priority', 'Thấp'), 1)
            reverse_order = True
        
        self.tasks.sort(key=key_function, reverse=reverse_order)
    
    def search_tasks(self, search_term):
        """Trả về một danh sách công việc có tiêu đề hoặc chi tiết chứa search_term."""
        if not search_term:
            return self.tasks
        
        search_term_lower = search_term.lower()
        results = []
        for task in self.tasks:
            title = task.get('title', '').lower()
            details = task.get('details', '').lower()
            if search_term_lower in title or search_term_lower in details:
                results.append(task)
        return results