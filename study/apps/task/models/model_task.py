# DBの「task」テーブル

from sqlalchemy import Text

class Task:
    def __init__(self, task_id: int, task_name: str, task_text: Text):
        # 課題ID(主キー)
        self.task_id = task_id 
        # 課題名
        self.task_name = task_name
        # 問題文
        self.task_text = task_text

    def __repr__(self) -> str:
        return f"Task(task_id={self.task_id}, task_name={self.task_name!r}, task_text={self.task_text!r})"