# DBの「return」テーブル

from sqlalchemy import Text

class Returned:
  def __init__(self, returned_id: int, check_text: Text, submission_id: int, q_a_t: Text | None=None):
        # 課題返却ID(主キー)
        self.returned_id = returned_id
        # 添削文
        self.check_text = check_text
        # 回答文
        self.q_a_t = q_a_t
        # 提出物ID(外部キー)
        self.submission_id = submission_id

  def __repr__(self) -> str:
     return f"Task_Submission(task_returned_id={self.returned_id}, check_text={self.check_text!r}, q_a_t={self.q_a_t!r}, task_submission_id={self.submission_id!r})"