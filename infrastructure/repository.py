import os
from typing import List
from core.room import Room, StandardRoom, VipRoom
from core.booking import Booking
from core.invoice import Invoice

class RoomRepository:
    def load_all(self) -> List[Room]:
        raise NotImplementedError

    def save_all(self, rooms: List[Room]) -> None:
        raise NotImplementedError

class TextRoomRepository(RoomRepository):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_all(self) -> List[Room]:
        rooms: List[Room] = []
        if not os.path.exists(self.file_path): 
            return []
            
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    p = line.strip().split('|')
                    if len(p) == 4:
                        r_id, r_type, price, capacity = p[0], p[1], float(p[2]), int(p[3])
                        
                        if r_type.lower() == "vip":
                            rooms.append(VipRoom(r_id, price, capacity))
                        else:
                            rooms.append(StandardRoom(r_id, price, capacity))
            return rooms
        except Exception as e:
            print(f"Lỗi đọc file rooms.txt: {e}")
            return []

    def save_all(self, rooms: List[Room]) -> None:
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                for r in rooms:
                    line = f"{r.get_room_id()}|{r.get_room_type()}|{r.get_price()}|{r.get_capacity()}\n"
                    f.write(line)
        except Exception as e:
            print(f"Lỗi ghi file rooms.txt: {e}")

class BookingRepository:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_all(self) -> List[Booking]:
        bookings: List[Booking] = []
        if not os.path.exists(self.file_path): 
            return []
            
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    p = line.strip().split('|')
                    if len(p) == 5:
                        bookings.append(Booking(p[0], p[1], p[2], int(p[3]), int(p[4])))
            return bookings
        except Exception as e:
            print(f"Lỗi đọc file bookings.txt: {e}")
            return []

    def save_all(self, bookings: List[Booking]) -> None:
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                for b in bookings:
                    line = f"{b.get_booking_id()}|{b.get_room_id()}|{b.get_customer_name()}|{b.get_num_people()}|{b.get_duration_days()}\n"
                    f.write(line)
        except Exception as e:
            print(f"Lỗi ghi file bookings.txt: {e}")

class InvoiceRepository:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_all(self) -> List[Invoice]:
        """Tải toàn bộ hóa đơn từ file lên danh sách"""
        invoices = []
        if not os.path.exists(self.file_path): 
            return []
            
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    p = line.strip().split('|')
                    if len(p) == 6:
                        # p = [booking_id, room_id, cus_name, duration, total, date]
                        invoices.append(Invoice(p[0], p[1], p[2], int(p[3]), float(p[4]), p[5]))
            return invoices
        except Exception as e:
            print(f"Lỗi đọc file invoices.txt: {e}")
            return []

    def save(self, invoice: Invoice) -> None:
        """Sử dụng mode 'a' (append) để nối thêm hóa đơn vào cuối file"""
        try:
            with open(self.file_path, 'a', encoding='utf-8') as f:
                line = f"{invoice.get_booking_id()}|{invoice.get_room_id()}|{invoice.get_customer_name()}|{invoice.get_duration_days()}|{invoice.get_total_amount()}|{invoice.get_checkout_date()}\n"
                f.write(line)
        except Exception as e:
            print(f"Lỗi ghi file invoices.txt: {e}")