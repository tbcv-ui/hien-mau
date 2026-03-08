class Coordinator:
    """Lớp xử lý thuật toán tìm kiếm và điều phối"""

    def search_donors(self, blood_bank, target_blood_type, target_city):
        """Lọc người phù hợp từ kho dữ liệu (BloodBank)"""
        results = []
        # Lấy danh sách từ kho
        all_donors = blood_bank.get_all_donors()

        for donor in all_donors:
            # Thuật toán lọc theo nhóm máu và vị trí
            if donor.blood_type == target_blood_type and donor.city == target_city:
                results.append(donor)

        return results