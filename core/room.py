class Room:
    def __init__(self, room_id, room_type, price, status, customer_name):
        self.__room_id = room_id
        self.__room_type = room_type
        self.__price = float(price)
        self.__status = status
        self.__customer_name = customer_name

    # --- GETTERS ---
    def get_room_id(self): return self.__room_id
    def get_room_type(self): return self.__room_type
    def get_price(self): return self.__price
    def get_status(self): return self.__status
    def get_customer_name(self): return self.__customer_name

    # --- SETTERS ---
    def set_room_type(self, value): self.__room_type = value
    def set_price(self, value): self.__price = float(value)
    def set_status(self, value): self.__status = value
    def set_customer_name(self, value): self.__customer_name = value