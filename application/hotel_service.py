from typing import Dict, List, Optional
from core.room import Room
from core.booking import Booking
from core.invoice import Invoice
from infrastructure.repository import RoomRepository, BookingRepository, InvoiceRepository

class HotelService:
    def __init__(self, room_repo: RoomRepository, booking_repo: BookingRepository, invoice_repo: InvoiceRepository):
        self.room_repo = room_repo
        self.booking_repo = booking_repo
        self.invoice_repo = invoice_repo
        
        self.rooms_dict: Dict[str, Room] = {r.get_room_id(): r for r in self.room_repo.load_all()}
        self.bookings_dict: Dict[str, Booking] = {b.get_booking_id(): b for b in self.booking_repo.load_all()}

    def _sync_rooms(self) -> None:
        self.room_repo.save_all(list(self.rooms_dict.values()))

    def _sync_bookings(self) -> None:
        self.booking_repo.save_all(list(self.bookings_dict.values()))

    # ================= QUẢN LÝ PHÒNG =================
    def get_room(self, room_id: str) -> Optional[Room]:
        return self.rooms_dict.get(room_id)

    @property
    def get_all_rooms(self) -> List[Room]:
        return list(self.rooms_dict.values())

    def add_room(self, room: Room) -> None:
        if room.get_room_id() in self.rooms_dict:
            raise ValueError("Mã phòng đã tồn tại!")
        self.rooms_dict[room.get_room_id()] = room
        self._sync_rooms()

    def update_room(self, room_id: str, data: dict) -> bool:
        room = self.get_room(room_id)
        if room:
            room.set_room_type(data['type'])
            room.set_price(data['price'])
            room.set_capacity(data['capacity'])
            self._sync_rooms()
            return True
        return False

    def delete_room(self, room_id: str) -> None:
        if room_id in self.rooms_dict:
            is_booked = any(b.get_room_id() == room_id for b in self.bookings_dict.values())
            if is_booked:
                raise ValueError("Không thể xóa phòng đang có người đặt!")
            del self.rooms_dict[room_id]
            self._sync_rooms()

    # ================= QUẢN LÝ ĐẶT PHÒNG & HÓA ĐƠN =================
    def get_all_bookings(self) -> List[Booking]:
        return list(self.bookings_dict.values())

    def book_room(self, booking: Booking) -> None:
        if booking.get_booking_id() in self.bookings_dict:
            raise ValueError("Mã đặt phòng đã tồn tại!")
        if booking.get_room_id() not in self.rooms_dict:
            raise ValueError("Phòng không tồn tại!")
        
        is_booked = any(b.get_room_id() == booking.get_room_id() for b in self.bookings_dict.values())
        if is_booked:
            raise ValueError("Phòng này đã có người đặt!")
            
        self.bookings_dict[booking.get_booking_id()] = booking
        self._sync_bookings()

    def checkout_and_generate_invoice(self, booking_id: str) -> Invoice:
        if booking_id not in self.bookings_dict:
            raise ValueError("Không tìm thấy mã đặt phòng!")
            
        booking = self.bookings_dict[booking_id]
        room = self.get_room(booking.get_room_id())
        
        if not room:
            raise ValueError("Lỗi dữ liệu: Không tìm thấy phòng của hóa đơn!")
            
        total = room.calculate_checkout_price(booking.get_duration_days())
        
        invoice = Invoice(
            booking_id=booking.get_booking_id(),
            room_id=room.get_room_id(),
            customer_name=booking.get_customer_name(),
            duration_days=booking.get_duration_days(),
            total_amount=total
        )
        
        self.invoice_repo.save(invoice)
        del self.bookings_dict[booking_id]
        self._sync_bookings()
        
        return invoice

    def get_all_invoices(self) -> List[Invoice]:
        """Tải toàn bộ hóa đơn cho giao diện UI"""
        return self.invoice_repo.load_all()

    # ================= TIỆN ÍCH =================
    def get_room_status(self, room_id: str) -> str:
        is_booked = any(b.get_room_id() == room_id for b in self.bookings_dict.values())
        return "Đã thuê" if is_booked else "Trống"

    def get_booking_for_room(self, room_id: str) -> Optional[Booking]:
        for b in self.bookings_dict.values():
            if b.get_room_id() == room_id:
                return b
        return None

    def search_rooms(self, keyword: str) -> List[Room]:
        k = keyword.lower()
        return [r for r in self.rooms_dict.values() if k in r.get_room_id().lower()]