# DBの「submission」テーブル
from sqlalchemy import Text
from datetime import datetime

class Submission:
  def __init__(self, submission_id: int, answer_text: Text,  submit_date: datetime, task_id: int, student_id: int, q_t: Text | None=None, submit_flag: bool = False, checked_flag: bool = False, returned_flag: bool = False):
      # 提出物ID(主キー)
      self.submission_id = submission_id
      # 解答文
      self.answer_text = answer_text
      # 質問文
      self.q_t = q_t
      # 課題提出フラグ
      self.submit_flag = submit_flag
      # 提出日時
      self.submit_date = submit_date
      # 提出課題添削フラグ
      self.checked_flag = checked_flag
      # 提出課題返却フラグ
      self.returned_flag = returned_flag
      # 課題ID(外部キー)
      self.task_id = task_id
      # 受講者ID(外部キー)
      self.student_id = student_id

  def __repr__(self) -> str:
     return f"Task_Submission(task_submission_id={self.submission_id}, answer_text={self.answer_text!r}, question_text={self.q_t!r}, task_streamed_flag={self.submit_flag!r}, task_submission_date={self.submit_date!r}, task_checked_flag={self.checked_flag!r}, task_returned_flag={self.returned_flag!r}, task_id={self.task_id!r}, student_id={self.student_id!r})"
