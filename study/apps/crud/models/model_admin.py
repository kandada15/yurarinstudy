from datetime import date, datetime
# DB内の「admin」

class Admin:
    def __init__(self, admin_id: str, admin_name: str, password: str, birthday: date, entry_date: datetime = None):
        self.admin_id = admin_id
        self.admin_name = admin_name
        self.password = password
        self.birthday = birthday
        self.entry_date = entry_date

    def __repr__(self) -> str:
        return f"Admin(admin_id={self.admin_id!r}, admin_name={self.admin_name!r}, password={self.password!r}, birthday={self.birthday}, entry_date={self.entry_date})"

 # # passwordという直接アクセスできない属性を定義（生パスワードを隠蔽）
    # @property
    # def password(self):
    #     raise AttributeError("パスワードは読み取り不可です")
    
    # # passwordに値を代入する際の処理（ハッシュ化）
    # @password.setter
    # def password(self, password):
    #     # パスワードをハッシュ化して password_hash などの別フィールドに保存する想定
    #     # self.password_hash = generate_password_hash(password)
    #     pass

    # # パスワードの検証メソッド
    # def verify_password(self, password):
    #     # return check_password_hash(self.password_hash, password)
    #     return False
    
    # # 生年月日を初期パスワードとして設定するメソッド
    # def reset_password_to_birthday(self):
    #     # YYYYMMDD形式の文字列に変換してセットする例
    #     birthday_str = self.birthday.strftime('%Y%m%d')
    #     self.password = birthday_str