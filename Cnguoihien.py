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
        self.conditions = conditions
