import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from PyQt6 import uic

# Nhập các lớp từ 3 file backend của chúng ta
from donor import Donor
from blood_bank import BloodBank
from coordinator import Coordinator


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

        if not name or not phone:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập họ tên và số điện thoại!")
            return

        # Lưu vào danh sách
        new_donor = Donor(name, gender, age, weight, blood_type, city, phone, conditions)
        self.blood_bank.add_donor(new_donor)

        QMessageBox.information(self, "Thành công", f"Đã đăng ký thành công cho {name}!")

        # Xóa trắng form để nhập người tiếp theo
        self.ted_hvt.clear()
        self.led_tuoi.clear()
        self.led_cannang.clear()
        self.led_sdt.clear()
        self.led_benhnen.clear()
        self.led_cccd.clear()  # Ô CCCD bạn tạo trong giao diện

    def refresh_list_table(self):
        """Cập nhật dữ liệu cho Bảng Danh sách (Tab 2)"""
        donors = self.blood_bank.get_all_donors()
        self.table_danhsach.setRowCount(len(donors))  # table_danhsach là tên bảng trong UI của bạn

        for row, donor in enumerate(donors):
            self.table_danhsach.setItem(row, 0, QTableWidgetItem(str(row + 1)))  # Cột STT
            self.table_danhsach.setItem(row, 1, QTableWidgetItem(donor.name))
            self.table_danhsach.setItem(row, 2, QTableWidgetItem(str(donor.age)))
            self.table_danhsach.setItem(row, 3, QTableWidgetItem(donor.gender))
            self.table_danhsach.setItem(row, 4, QTableWidgetItem(str(donor.weight)))
            self.table_danhsach.setItem(row, 5, QTableWidgetItem(donor.conditions))
            self.table_danhsach.setItem(row, 6, QTableWidgetItem(donor.city))
            self.table_danhsach.setItem(row, 7, QTableWidgetItem(donor.blood_type))
            self.table_danhsach.setItem(row, 8, QTableWidgetItem(donor.phone))

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