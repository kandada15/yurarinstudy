# DBの「streamed」テーブル
from datetime import datetime

class Streamed:
  def __init__(self, streamed_id: int, streamed_limit: datetime, task_id: int, group_id: int):
      # 配信済み課題ID(主キー)
      self.streamed_id = streamed_id
      # 課題提出期限 
      self.streamed_limit = streamed_limit
      # 課題ID(外部キー)
      self.task_id = task_id
      # グループID(外部キー)
      self.group_id = group_id

  def __repr__(self) -> str:
     return f"Task_Streamed(task_streamed_id={self.streamed_id}, task_streamed_limit={self.streamed_limit!r}, task_id={self.task_id!r}, group_id={self.group_id!r})"