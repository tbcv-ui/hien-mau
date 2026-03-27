# cnguoihien.py

class NguoiHien:
    """Lớp đại diện cho một người hiến máu."""
    def __init__(self, ho_ten, tuoi, gioi_tinh, can_nang, cccd, nhom_mau, tinh_thanh, so_dien_thoai, benh_nen, so_lan_hien, lan_hien_gan_nhat):
        self.ho_ten = ho_ten
        self.tuoi = tuoi
        self.gioi_tinh = gioi_tinh
        self.can_nang = can_nang
        self.cccd = cccd
        self.nhom_mau = nhom_mau
        self.tinh_thanh = tinh_thanh
        self.so_dien_thoai = so_dien_thoai
        self.benh_nen = benh_nen
        self.so_lan_hien = so_lan_hien
        self.lan_hien_gan_nhat = lan_hien_gan_nhat

    def to_dict(self):
        """Chuyển đổi đối tượng NguoiHien thành Dictionary để lưu vào JSON."""
        return {
            'ho_ten': self.ho_ten,
            'tuoi': self.tuoi,
            'gioi_tinh': self.gioi_tinh,
            'can_nang': self.can_nang,
            'cccd': self.cccd,
            'nhom_mau': self.nhom_mau,
            'tinh_thanh': self.tinh_thanh,
            'so_dien_thoai': self.so_dien_thoai,
            'benh_nen': self.benh_nen,
            'so_lan_hien': self.so_lan_hien,
            'lan_hien_gan_nhat': self.lan_hien_gan_nhat
        }

    @classmethod
    def from_dict(cls, data):
        """Tạo đối tượng NguoiHien từ Dictionary (khi đọc từ JSON)."""
        return cls(**data)