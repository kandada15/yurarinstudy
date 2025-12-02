# DB内の「group」

class Group:
    def __init__(self, group_id: int, group_name: str, admin_id: str):
        """
        :param group_id: グループID (PK, int(10)) - AUTO_INCREMENT
        :param group_name: グループ名 (nvarchar(50)) - クラス、学部、部署など
        :param admin_id: 管理者ID (FK, varchar(10)) - グループ管理者
        """
        self.group_id = group_id
        self.group_name = group_name
        self.admin_id = admin_id

    def __repr__(self) -> str:
        return f"Group(group_id={self.group_id}, group_name={self.group_name!r}, admin_id={self.admin_id!r})"