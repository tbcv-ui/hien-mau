class BloodBank:
    """Lớp quản lý danh sách người hiến máu"""
    def __init__(self):
        self.donors_list = [] # Cấu trúc dữ liệu List

    def add_donor(self, donor):
        """Thêm người hiến vào danh sách"""
        self.donors_list.append(donor)

    def get_all_donors(self):
        """Lấy toàn bộ danh sách hiện có"""
        return self.donors_list