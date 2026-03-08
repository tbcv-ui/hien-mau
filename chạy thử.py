import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QComboBox,
                             QSpinBox, QPushButton, QTableWidget, QTableWidgetItem,
                             QTabWidget, QMessageBox, QHeaderView)


# ==========================================
# PHẦN 1: CẤU TRÚC DỮ LIỆU & OOP
# ==========================================

class Donor:
    """Lớp đại diện cho một người hiến máu"""

    def __init__(self, name, gender, age, weight, blood_type, city, phone, conditions):
        self.name = name
        self.gender = gender
        self.age = age
        self.weight = weight
        self.blood_type = blood_type
        self.city = city
        self.phone = phone
        self.conditions = conditions  # Bệnh nền (nếu có)


class BloodBank:
    """Lớp quản lý danh sách người hiến máu và các thuật toán"""

    def __init__(self):
        self.donors_list = []  # Sử dụng List làm cấu trúc dữ liệu chính

    def add_donor(self, donor):
        self.donors_list.append(donor)

    def search_donors(self, target_blood_type, target_city):
        """Thuật toán tìm kiếm và lọc người hiến máu phù hợp"""
        results = []
        for donor in self.donors_list:
            # Lọc theo nhóm máu và ưu tiên cùng tỉnh/thành
            if donor.blood_type == target_blood_type and donor.city == target_city:
                results.append(donor)
        return results


# ==========================================
# PHẦN 2: GIAO DIỆN NGƯỜI DÙNG (PyQt6)
# ==========================================

class BloodBankApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.blood_bank = BloodBank()

        # Thêm một vài dữ liệu mẫu để bạn dễ kiểm tra
        self.blood_bank.add_donor(Donor("Nguyễn Văn A", "Nam", 25, 65, "O", "Hồ Chí Minh", "0123456789", "Không"))
        self.blood_bank.add_donor(Donor("Trần Thị B", "Nữ", 30, 50, "A", "Hà Nội", "0987654321", "Không"))
        self.blood_bank.add_donor(Donor("Lê Văn C", "Nam", 28, 70, "O", "Hồ Chí Minh", "0112233445", "Không"))

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Phần mềm Điều phối Nhóm máu (Blood Bank Coordinator)")
        self.setGeometry(100, 100, 800, 500)

        # Tạo Widget chính và Tab Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        # Khởi tạo 3 Tab
        self.tab_register = QWidget()
        self.tab_coordinate = QWidget()
        self.tab_list = QWidget()

        self.tabs.addTab(self.tab_register, "1. Đăng ký hiến máu")
        self.tabs.addTab(self.tab_coordinate, "2. Điều phối cấp cứu")
        self.tabs.addTab(self.tab_list, "3. Danh sách người hiến")

        self.setup_register_tab()
        self.setup_coordinate_tab()
        self.setup_list_tab()

    # --- THIẾT KẾ TAB 1: ĐĂNG KÝ ---
    def setup_register_tab(self):
        layout = QVBoxLayout()

        # Tạo các trường nhập liệu
        self.reg_name = QLineEdit()
        self.reg_gender = QComboBox()
        self.reg_gender.addItems(["Nam", "Nữ", "Khác"])
        self.reg_age = QSpinBox()
        self.reg_age.setRange(18, 60)  # Tuổi hiến máu tiêu chuẩn
        self.reg_weight = QSpinBox()
        self.reg_weight.setRange(45, 120)
        self.reg_blood = QComboBox()
        self.reg_blood.addItems(["A", "B", "AB", "O"])
        self.reg_city = QComboBox()
        self.reg_city.addItems(["Hồ Chí Minh", "Hà Nội", "Bình Dương", "Đà Nẵng", "Cần Thơ"])
        self.reg_phone = QLineEdit()
        self.reg_conditions = QLineEdit()
        self.reg_conditions.setPlaceholderText("Ghi 'Không' nếu khỏe mạnh")

        # Thêm vào layout dạng Form (Label + Input)
        def add_form_row(label_text, widget):
            row_layout = QHBoxLayout()
            row_layout.addWidget(QLabel(label_text))
            row_layout.addWidget(widget)
            layout.addLayout(row_layout)

        add_form_row("Họ và Tên:", self.reg_name)
        add_form_row("Giới tính:", self.reg_gender)
        add_form_row("Độ tuổi:", self.reg_age)
        add_form_row("Cân nặng (kg):", self.reg_weight)
        add_form_row("Nhóm máu:", self.reg_blood)
        add_form_row("Tỉnh/Thành phố:", self.reg_city)
        add_form_row("Số điện thoại:", self.reg_phone)
        add_form_row("Bệnh nền:", self.reg_conditions)

        # Nút Đăng ký
        self.btn_register = QPushButton("Lưu Thông Tin")
        self.btn_register.clicked.connect(self.handle_register)
        layout.addWidget(self.btn_register)

        self.tab_register.setLayout(layout)

    # --- THIẾT KẾ TAB 2: ĐIỀU PHỐI ---
    def setup_coordinate_tab(self):
        layout = QVBoxLayout()

        # Phần tìm kiếm
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Cần nhóm máu:"))
        self.search_blood = QComboBox()
        self.search_blood.addItems(["A", "B", "AB", "O"])
        search_layout.addWidget(self.search_blood)

        search_layout.addWidget(QLabel("Tại Tỉnh/Thành:"))
        self.search_city = QComboBox()
        self.search_city.addItems(["Hồ Chí Minh", "Hà Nội", "Bình Dương", "Đà Nẵng", "Cần Thơ"])
        search_layout.addWidget(self.search_city)

        self.btn_search = QPushButton("Tìm kiếm khẩn cấp")
        self.btn_search.clicked.connect(self.handle_search)
        search_layout.addWidget(self.btn_search)

        layout.addLayout(search_layout)

        # Bảng hiển thị kết quả điều phối
        self.coord_table = QTableWidget()
        self.coord_table.setColumnCount(4)
        self.coord_table.setHorizontalHeaderLabels(["Họ Tên", "SĐT", "Tỉnh Thành", "Nhóm Máu"])
        self.coord_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.coord_table)

        self.tab_coordinate.setLayout(layout)

    # --- THIẾT KẾ TAB 3: DANH SÁCH ---
    def setup_list_tab(self):
        layout = QVBoxLayout()

        self.list_table = QTableWidget()
        self.list_table.setColumnCount(8)
        self.list_table.setHorizontalHeaderLabels(
            ["Họ Tên", "Giới", "Tuổi", "Nặng(kg)", "Nhóm Máu", "Tỉnh Thành", "SĐT", "Bệnh nền"])
        layout.addWidget(self.list_table)

        self.btn_refresh = QPushButton("Làm mới danh sách")
        self.btn_refresh.clicked.connect(self.refresh_list_table)
        layout.addWidget(self.btn_refresh)

        self.tab_list.setLayout(layout)
        self.refresh_list_table()  # Hiển thị dữ liệu mẫu ngay từ đầu

    # ==========================================
    # PHẦN 3: XỬ LÝ SỰ KIỆN (LOGIC)
    # ==========================================

    def handle_register(self):
        """Xử lý khi bấm nút Lưu thông tin"""
        name = self.reg_name.text()
        phone = self.reg_phone.text()

        if not name or not phone:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập tên và số điện thoại!")
            return

        # Tạo đối tượng Donor mới
        new_donor = Donor(
            name=name,
            gender=self.reg_gender.currentText(),
            age=self.reg_age.value(),
            weight=self.reg_weight.value(),
            blood_type=self.reg_blood.currentText(),
            city=self.reg_city.currentText(),
            phone=phone,
            conditions=self.reg_conditions.text() or "Không"
        )

        # Thêm vào cấu trúc dữ liệu
        self.blood_bank.add_donor(new_donor)
        QMessageBox.information(self, "Thành công", f"Đã đăng ký thành công cho {name}!")

        # Cập nhật lại bảng danh sách
        self.refresh_list_table()

        # Xóa trắng form
        self.reg_name.clear()
        self.reg_phone.clear()
        self.reg_conditions.clear()

    def handle_search(self):
        """Xử lý khi bấm nút Tìm kiếm khẩn cấp"""
        b_type = self.search_blood.currentText()
        city = self.search_city.currentText()

        # Gọi thuật toán lọc từ backend
        results = self.blood_bank.search_donors(b_type, city)

        # Cập nhật bảng kết quả
        self.coord_table.setRowCount(len(results))
        for row, donor in enumerate(results):
            self.coord_table.setItem(row, 0, QTableWidgetItem(donor.name))
            self.coord_table.setItem(row, 1, QTableWidgetItem(donor.phone))
            self.coord_table.setItem(row, 2, QTableWidgetItem(donor.city))
            self.coord_table.setItem(row, 3, QTableWidgetItem(donor.blood_type))

        if not results:
            QMessageBox.information(self, "Kết quả", f"Không tìm thấy người hiến máu nhóm {b_type} tại {city}.")

    def refresh_list_table(self):
        """Cập nhật dữ liệu cho Tab 3"""
        donors = self.blood_bank.donors_list
        self.list_table.setRowCount(len(donors))
        for row, donor in enumerate(donors):
            self.list_table.setItem(row, 0, QTableWidgetItem(donor.name))
            self.list_table.setItem(row, 1, QTableWidgetItem(donor.gender))
            self.list_table.setItem(row, 2, QTableWidgetItem(str(donor.age)))
            self.list_table.setItem(row, 3, QTableWidgetItem(str(donor.weight)))
            self.list_table.setItem(row, 4, QTableWidgetItem(donor.blood_type))
            self.list_table.setItem(row, 5, QTableWidgetItem(donor.city))
            self.list_table.setItem(row, 6, QTableWidgetItem(donor.phone))
            self.list_table.setItem(row, 7, QTableWidgetItem(donor.conditions))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BloodBankApp()
    window.show()
    sys.exit(app.exec())

hi

