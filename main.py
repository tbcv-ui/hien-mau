import sys
import json
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from PyQt6 import uic

# Nhập các lớp từ 3 file backend của chúng ta
from Cnguoihien import Donor
from Cdsnguoihien import BloodBank
from Dieuphoi import Coordinator


class BloodBankApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # 1. TẢI FILE GIAO DIỆN TỪ QT DESIGNER
        uic.loadUi("hienmaumoi.ui", self)

        # 2. Khởi tạo dữ liệu
        self.blood_bank = BloodBank()
        self.coordinator = Coordinator()

        # 3. KẾT NỐI CÁC NÚT BẤM VỚI HÀM XỬ LÝ
        # Tên các nút (ptb_luuthongtin, btn_lammoi, timkhancap) lấy chính xác từ file .ui của bạn
        self.ptb_luuthongtin.clicked.connect(self.handle_register)
        self.btn_lammoi.clicked.connect(self.refresh_list_table)
        self.timkhancap.clicked.connect(self.handle_search)

    # ==========================================
    # CÁC HÀM XỬ LÝ LOGIC
    # ==========================================
    def handle_register(self):
        """Xử lý khi bấm nút LƯU THÔNG TIN"""
        # Lấy dữ liệu từ các ô nhập liệu của bạn
        name = self.ted_hvt.toPlainText().strip()  # Chú ý: bạn dùng QTextEdit cho Họ Tên
        age = self.led_tuoi.text().strip()
        weight = self.led_cannang.text().strip()
        phone = self.led_sdt.text().strip()
        conditions = self.led_benhnen.text().strip()

        gender = self.cbb_gioitinh.currentText()
        blood_type = self.cbb_nhommau.currentText()
        city = self.cbb_tinh.currentText()

        cccd = self.led_cccd.text().strip()
        lan_hien = self.led_lanhien.text().strip()
        ngay_hien = self.date.date().toString("dd/MM/yyyy")

        # Kiểm tra tất cả các trường phải được điền
        missing = []
        if not name:
            missing.append("Họ và tên")
        if not age:
            missing.append("Độ tuổi")
        if not weight:
            missing.append("Cân nặng")
        if not cccd:
            missing.append("CCCD/CMND")
        if not phone:
            missing.append("Số điện thoại")
        if not conditions:
            missing.append("Bệnh nền")
        if not lan_hien:
            missing.append("Số lần hiến máu")

        if missing:
            QMessageBox.warning(self, "Lỗi", "Vui lòng điền đầy đủ thông tin!\n\nCòn thiếu:\n- " + "\n- ".join(missing))
            return

        # Lưu vào danh sách
        new_donor = Donor(name, gender, age, weight, blood_type, city, phone, conditions)
        self.blood_bank.add_donor(new_donor)

        # Lưu vào file JSON
        donor_data = {
            "ho_ten": name,
            "gioi_tinh": gender,
            "tuoi": age,
            "can_nang": weight,
            "nhom_mau": blood_type,
            "tinh_thanh": city,
            "so_dien_thoai": phone,
            "cccd": cccd,
            "benh_nen": conditions,
            "so_lan_hien": lan_hien,
            "ngay_hien_gan_nhat": ngay_hien
        }
        self.save_to_json(donor_data)

        QMessageBox.information(self, "Thành công", f"Đã đăng ký thành công cho {name}!")

        # Xóa trắng form để nhập người tiếp theo
        self.ted_hvt.clear()
        self.led_tuoi.clear()
        self.led_cannang.clear()
        self.led_sdt.clear()
        self.led_benhnen.clear()
        self.led_cccd.clear()
        self.led_lanhien.clear()

    def save_to_json(self, donor_data):
        """Lưu thông tin người hiến vào file data.json (thêm mới, không ghi đè)"""
        data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")

        # Đọc dữ liệu cũ nếu có
        if os.path.exists(data_file) and os.path.getsize(data_file) > 0:
            with open(data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = []

        # Thêm người mới vào danh sách
        data.append(donor_data)

        # Ghi lại toàn bộ danh sách
        with open(data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def refresh_list_table(self):
        """Cập nhật dữ liệu cho Bảng Danh sách (Tab 2) từ file data.json"""
        data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")

        if os.path.exists(data_file) and os.path.getsize(data_file) > 0:
            with open(data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = []

        self.table_danhsach.setRowCount(len(data))

        for row, donor in enumerate(data):
            self.table_danhsach.setItem(row, 0, QTableWidgetItem(str(row + 1)))
            self.table_danhsach.setItem(row, 1, QTableWidgetItem(donor.get("ho_ten", "")))
            self.table_danhsach.setItem(row, 2, QTableWidgetItem(donor.get("tuoi", "")))
            self.table_danhsach.setItem(row, 3, QTableWidgetItem(donor.get("gioi_tinh", "")))
            self.table_danhsach.setItem(row, 4, QTableWidgetItem(donor.get("can_nang", "")))
            self.table_danhsach.setItem(row, 5, QTableWidgetItem(donor.get("benh_nen", "")))
            self.table_danhsach.setItem(row, 6, QTableWidgetItem(donor.get("tinh_thanh", "")))
            self.table_danhsach.setItem(row, 7, QTableWidgetItem(donor.get("nhom_mau", "")))
            self.table_danhsach.setItem(row, 8, QTableWidgetItem(donor.get("so_dien_thoai", "")))

    def handle_search(self):
        """Xử lý khi bấm nút TÌM KHẨN CẤP (Tab 3)"""
        b_type = self.nhommau.currentText()  # Lấy từ combobox nhóm máu
        city = self.tinhthanh.currentText()  # Lấy từ combobox tỉnh thành

        results = self.coordinator.search_donors(self.blood_bank, b_type, city)

        # Cập nhật bảng kết quả (tableWidget)
        self.tableWidget.setRowCount(len(results))
        for row, donor in enumerate(results):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(donor.name))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(str(donor.age)))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(donor.gender))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(str(donor.weight)))
            self.tableWidget.setItem(row, 4, QTableWidgetItem(donor.conditions))
            self.tableWidget.setItem(row, 5, QTableWidgetItem(donor.city))
            self.tableWidget.setItem(row, 6, QTableWidgetItem(donor.blood_type))
            self.tableWidget.setItem(row, 7, QTableWidgetItem(donor.phone))

        if not results:
            QMessageBox.information(self, "Kết quả", f"Không tìm thấy người hiến máu nhóm {b_type} tại {city}.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BloodBankApp()
    window.show()
    sys.exit(app.exec())