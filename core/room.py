class Room:
    def __init__(self, room_id: str, room_type: str, price: float, capacity: int):
        self.__room_id = room_id
        self.__room_type = room_type
        self.__price = float(price)
        self.__capacity = int(capacity)

    # --- GETTERS ---
    def get_room_id(self) -> str: return self.__room_id
    def get_room_type(self) -> str: return self.__room_type
    def get_price(self) -> float: return self.__price
    def get_capacity(self) -> int: return self.__capacity

    # --- SETTERS ---
    def set_room_type(self, value: str) -> None: self.__room_type = value
    def set_price(self, value: float) -> None: self.__price = float(value)
    def set_capacity(self, value: int) -> None: self.__capacity = int(value)

    def calculate_checkout_price(self, days: int) -> float:
        """Phương thức tính tổng tiền lưu trú (Đa hình)"""
        return self.__price * days

class StandardRoom(Room):
    def __init__(self, room_id: str, price: float, capacity: int = 2):
        super().__init__(room_id, "Standard", price, capacity)

class VipRoom(Room):
    def __init__(self, room_id: str, price: float, capacity: int = 4):
        super().__init__(room_id, "VIP", price, capacity)

    def calculate_checkout_price(self, days: int) -> float:
        """Ghi đè: Phòng VIP có thêm phụ thu dịch vụ 20%"""
        base_price = super().calculate_checkout_price(days)
        return base_price * 1.2