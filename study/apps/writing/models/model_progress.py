# model_progress.py
# DBの「progress」テーブル1行分を表現するクラス（モデル）

from sqlalchemy import Boolean

class Progress:
    # コンストラクタ（初期化メソッド）
    def __init__(self, progress_id: int, phase_name: str,  stage_flag: Boolean, student_id: str):
        # 学習進捗ID（主キー）
        self.progress_id = progress_id
        # フェーズ名
        self.phase_name = phase_name
        # フェーズ完了フラグ
        self.stage_flag = stage_flag
        # 受講者ID（外部キー）
        self.student_id = student_id

    # オブジェクトを文字列に変換
    def __repr__(self) -> str:
        # デバッグ用に見やすい文字列表現
        # !rで文字列ならクォート''付きで表示
        return f"Category(progress_id={self.progress_id}, phase_name={self.phase_name!r}, stage_flag={self.stage_flag}, student_id={self.student_id})"