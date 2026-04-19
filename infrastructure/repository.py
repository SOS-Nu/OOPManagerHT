import os
from core.room import Room

class TextRoomRepository:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_all(self):
        rooms = []
        if not os.path.exists(self.file_path): return []
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    p = line.strip().split('|')
                    if len(p) == 5:
                        rooms.append(Room(p[0], p[1], p[2], p[3], p[4]))
            return rooms
        except Exception as e:
            print(f"Lỗi đọc file: {e}")
            return []

    def save_all(self, rooms):
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                for r in rooms:
                    # Truy xuất qua các hàm Getter
                    line = f"{r.get_room_id()}|{r.get_room_type()}|{r.get_price()}|{r.get_status()}|{r.get_customer_name()}\n"
                    f.write(line)
        except Exception as e:
            print(f"Lỗi ghi file: {e}")