import datetime

class Invoice:
    def __init__(self, booking_id: str, room_id: str, customer_name: str, duration_days: int, total_amount: float, checkout_date: str = None):
        self.__booking_id = booking_id
        self.__room_id = room_id
        self.__customer_name = customer_name
        self.__duration_days = duration_days
        self.__total_amount = total_amount
        # Tự động lấy timestamp hiện tại nếu không truyền vào
        self.__checkout_date = checkout_date or datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # --- GETTERS ---
    def get_booking_id(self) -> str: return self.__booking_id
    def get_room_id(self) -> str: return self.__room_id
    def get_customer_name(self) -> str: return self.__customer_name
    def get_duration_days(self) -> int: return self.__duration_days
    def get_total_amount(self) -> float: return self.__total_amount
    def get_checkout_date(self) -> str: return self.__checkout_date
