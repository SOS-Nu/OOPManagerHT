class Booking:
    def __init__(self, booking_id: str, room_id: str, customer_name: str, num_people: int, duration_days: int):
        self.__booking_id = booking_id
        self.__room_id = room_id
        self.__customer_name = customer_name
        self.__num_people = int(num_people)
        self.__duration_days = int(duration_days)

    # --- GETTERS ---
    def get_booking_id(self) -> str: return self.__booking_id
    def get_room_id(self) -> str: return self.__room_id
    def get_customer_name(self) -> str: return self.__customer_name
    def get_num_people(self) -> int: return self.__num_people
    def get_duration_days(self) -> int: return self.__duration_days

    # --- SETTERS ---
    def set_customer_name(self, value: str): self.__customer_name = value
    def set_num_people(self, value: int): self.__num_people = int(value)
    def set_duration_days(self, value: int): self.__duration_days = int(value)
