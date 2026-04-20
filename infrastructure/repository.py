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

class BaseRepository:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def read_lines(self):
        if not os.path.exists(self.file_path): 
            return []
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return [line.strip().split('|') for line in f if line.strip()]
        except Exception as e:
            print(f"Lỗi đọc file {self.file_path}: {e}")
            return []

    def write_lines(self, lines):
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                for p in lines:
                    f.write('|'.join(map(str, p)) + '\n')
        except Exception as e:
            print(f"Lỗi ghi file {self.file_path}: {e}")

    def append_line(self, line):
        try:
            with open(self.file_path, 'a', encoding='utf-8') as f:
                f.write('|'.join(map(str, line)) + '\n')
        except Exception as e:
            print(f"Lỗi thêm vào file {self.file_path}: {e}")

class TextRoomRepository(BaseRepository):
    def load_all(self) -> List[Room]:
        return [
            VipRoom(p[0], float(p[2]), int(p[3])) if p[1].lower() == "vip" 
            else StandardRoom(p[0], float(p[2]), int(p[3])) 
            for p in self.read_lines() if len(p) == 4
        ]

    def save_all(self, rooms: List[Room]) -> None:
        self.write_lines([[r.get_room_id(), r.get_room_type(), r.get_price(), r.get_capacity()] for r in rooms])

class BookingRepository(BaseRepository):
    def load_all(self) -> List[Booking]:
        return [Booking(p[0], p[1], p[2], int(p[3]), int(p[4])) for p in self.read_lines() if len(p) == 5]

    def save_all(self, bookings: List[Booking]) -> None:
        self.write_lines([[b.get_booking_id(), b.get_room_id(), b.get_customer_name(), b.get_num_people(), b.get_duration_days()] for b in bookings])

class InvoiceRepository(BaseRepository):
    def load_all(self) -> List[Invoice]:
        return [Invoice(p[0], p[1], p[2], int(p[3]), float(p[4]), p[5]) for p in self.read_lines() if len(p) == 6]

    def save(self, invoice: Invoice) -> None:
        self.append_line([invoice.get_booking_id(), invoice.get_room_id(), invoice.get_customer_name(), invoice.get_duration_days(), invoice.get_total_amount(), invoice.get_checkout_date()])