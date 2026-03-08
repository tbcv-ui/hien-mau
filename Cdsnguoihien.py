# Tên file: ds_nguoi_hien.py

class BloodBank:
    """Lớp quản lý danh sách và các thuật toán điều phối"""
    def __init__(self):
        self.donors_list = [] # Cấu trúc dữ liệu chính

    def add_donor(self, donor):
        self.donors_list.append(donor)

    def search_donors(self, target_blood_type, target_city):
        """Thuật toán lọc người theo nhóm máu và khu vực"""
        results = []
        for donor in self.donors_list:
            if donor.blood_type == target_blood_type and donor.city == target_city:
                results.append(donor)
        return results