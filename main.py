import os
import tkinter as tk
from infrastructure.repository import TextRoomRepository
from application.hotel_service import HotelService
from ui.dashboard import HotelApp

if __name__ == "__main__":
    # Tạo thư mục data nếu chưa có
    if not os.path.exists("data"):
        os.makedirs("data")

    # Khởi tạo Repository (có thể đổi sang JsonRoomRepository nếu muốn)
    repo = TextRoomRepository("data/rooms.txt")
    
    # Khởi tạo Service
    service = HotelService(repo)
    
    # Khởi tạo GUI
    root = tk.Tk()
    app = HotelApp(root, service)
    
    root.mainloop()