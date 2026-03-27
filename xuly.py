class Coordinator:
    """Lớp xử lý thuật toán tìm kiếm và điều phối"""

    def search_donors(self, blood_bank, target_blood_type, target_city):
        """Lọc người phù hợp từ kho dữ liệu (BloodBank)"""
        results = []
        all_donors = blood_bank.get_all_donors()

        # 1. CHUẨN HÓA TỪ KHÓA TÌM KIẾM
        # Xóa mọi dấu cách ở nhóm máu và in hoa (VD: " o - " -> "O-")
        search_blood = target_blood_type.replace(" ", "").upper()
        # Xóa dấu cách ở hai đầu chữ của tỉnh thành và in thường (VD: " Hà Nội " -> "hà nội")
        search_city = target_city.strip().lower()

        for donor in all_donors:
            # 2. CHUẨN HÓA DỮ LIỆU CỦA NGƯỜI HIẾN TRONG KHO
            donor_blood = donor.blood_type.replace(" ", "").upper()
            donor_city = donor.city.strip().lower()

            # 3. SO SÁNH SAU KHI ĐÃ LÀM SẠCH
            if donor_blood == search_blood and donor_city == search_city:
                results.append(donor)

        return results