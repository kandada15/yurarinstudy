from datetime import date
# DB内の「student」

class Student:
    def __init__(self, student_id: int, student_name: str, password: str, entry_year: date, birthday: date, entry_date: date, is_alert: bool, group_id: int):
        self.student_id = student_id
        self.student_name = student_name
        self.password = password
        self.entry_year = entry_year
        self.birthday = birthday
        self.entry_date = entry_date
        self.is_alert = is_alert
        self.group_id = group_id

    def __repr__(self) -> str:
        return f"Student(student_id={self.student_id}, student_name={self.student_name!r}, password={self.password!r}, entry_year,)"

    # # passwordという直接アクセスできない属性を定義
    # @property
    # def password(self):
    #     raise AttributeError("読み取り不可") # passwordにアクセスするとエラーになる
    
    # ## passwordに値を代入する処理
    # # passwordに値を入れようとすると以下の関数が実行される
    # @password.setter 

    # # パスワードをハッシュ化するメソッドを定義
    # def password(self, password): 
    #     # パスワードをハッシュ化してpassword_hashに保存
    #     self.password_hash = generate_password_hash(password) 

    # # パスワードの検証
    # def verify_password(self, password): 
    #     return check_password_hash(self.password_hash, password)