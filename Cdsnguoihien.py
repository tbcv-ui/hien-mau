# Cdsnguoihien.py
import json
import os
from Cnguoihien import NguoiHien

class Node:
    """Một nút trong danh sách liên kết."""
    def __init__(self, nguoi_hien):
        self.data = nguoi_hien
        self.next = None

class DanhSachNguoiHien:
    """Quản lý danh sách người hiến bằng Danh sách liên kết đơn và kết nối với JSON."""
    def __init__(self, file_path="du_lieu_nguoi_hien.json"):
        self.head = None
        self.file_path = file_path
        self.doc_tu_file_json()

    def luu_xuong_file_json(self):
        danh_sach_dict = []
        temp = self.head
        while temp:
            danh_sach_dict.append(temp.data.to_dict())
            temp = temp.next

        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(danh_sach_dict, f, ensure_ascii=False, indent=4)

    def doc_tu_file_json(self):
        if not os.path.exists(self.file_path):
            return
        with open(self.file_path, 'r', encoding='utf-8') as f:
            try:
                danh_sach_dict = json.load(f)
                for item in danh_sach_dict:
                    nguoi = NguoiHien.from_dict(item)
                    self.them_nguoi_hien(nguoi, ghi_file=False)
            except json.JSONDecodeError:
                pass

    def them_nguoi_hien(self, nguoi_hien, ghi_file=True):
        new_node = Node(nguoi_hien)
        if not self.head:
            self.head = new_node
            if ghi_file: self.luu_xuong_file_json()
            return True

        temp = self.head
        while temp:
            if temp.data.cccd == nguoi_hien.cccd:
                return False
            if temp.next is None:
                break
            temp = temp.next

        temp.next = new_node
        if ghi_file: self.luu_xuong_file_json()
        return True

    def cap_nhat_nguoi_hien(self, cccd, nguoi_hien_moi):
        """Tìm Node có CCCD tương ứng và cập nhật dữ liệu (Dành cho chức năng Sửa)."""
        temp = self.head
        while temp:
            if temp.data.cccd == cccd:
                temp.data = nguoi_hien_moi # Ghi đè dữ liệu
                self.luu_xuong_file_json() # Lưu lại xuống file
                return True
            temp = temp.next
        return False

    def xoa_theo_cccd(self, cccd):
        temp = self.head
        prev = None

        if temp is not None and temp.data.cccd == cccd:
            self.head = temp.next
            temp = None
            self.luu_xuong_file_json()
            return True

        while temp is not None and temp.data.cccd != cccd:
            prev = temp
            temp = temp.next

        if temp is None:
            return False

        prev.next = temp.next
        temp = None
        self.luu_xuong_file_json()
        return True

    def lay_danh_sach(self):
        danh_sach = []
        temp = self.head
        while temp:
            danh_sach.append(temp.data)
            temp = temp.next
        return danh_sach

    def tim_kiem_cap_cuu(self, nhom_mau, tinh_thanh):
        ket_qua = []
        temp = self.head
        while temp:
            if temp.data.nhom_mau == nhom_mau and temp.data.tinh_thanh == tinh_thanh:
                ket_qua.append(temp.data)
            temp = temp.next
        return ket_qua