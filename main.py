import os
import tkinter as tk
from infrastructure.repository import TextRoomRepository, BookingRepository, InvoiceRepository
from application.hotel_service import HotelService
from ui.dashboard import HotelApp

if __name__ == "__main__":
    if not os.path.exists("data"):
        os.makedirs("data")

    #crud 3 file 
    room_repo = TextRoomRepository("data/rooms.txt")
    booking_repo = BookingRepository("data/bookings.txt")
    invoice_repo = InvoiceRepository("data/invoices.txt")
    
    # Inject dependencies
    service = HotelService(room_repo, booking_repo, invoice_repo)
    
    # init tạo GUI
    root = tk.Tk()
    app = HotelApp(root, service)
    
    root.mainloop()