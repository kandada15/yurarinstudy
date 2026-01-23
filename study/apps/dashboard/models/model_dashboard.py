# models/model_dashboard.py
# dashboard テーブル1行分を表現するモデルクラス

# Dashboard テーブルモデル作成
class Dashboard:
    def __init__(self, dashboard_id: int, admin_id: str, group_id: int, submission_id: int, task_id: int, progress_id: int):
        # ダッシュボードID（主キー）
        self.dashboard_id = dashboard_id
        # 管理者ID（外部キー）
        self.admin_id = admin_id
        # グループID（外部キー）
        self.group_id = group_id
        # 提出物ID（外部キー）
        self.submission_id = submission_id
        # 課題ID（外部キー）
        self.task_id = task_id
        # 学習進捗ID（外部キー）
        self.progress_id = progress_id