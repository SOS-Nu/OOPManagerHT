class HotelService:
    def __init__(self, repository):
        self.repository = repository
        self.rooms = self.repository.load_all()

    def add_room(self, room):
        if any(r.get_room_id() == room.get_room_id() for r in self.rooms):
            raise ValueError("Mã phòng đã tồn tại!")
        self.rooms.append(room)
        self.repository.save_all(self.rooms)

    def update_room(self, room_id, data):
        for r in self.rooms:
            if r.get_room_id() == room_id:
                r.set_room_type(data['type'])
                r.set_price(data['price'])
                r.set_status(data['status'])
                r.set_customer_name(data['cust'])
                self.repository.save_all(self.rooms)
                return True
        return False

    def delete_room(self, room_id):
        self.rooms = [r for r in self.rooms if r.get_room_id() != room_id]
        self.repository.save_all(self.rooms)

    def search_by_keyword(self, keyword):
        k = keyword.lower()
        return [r for r in self.rooms if k in r.get_room_id().lower() or k in r.get_customer_name().lower()]

    def sort_by_price(self):
        return sorted(self.rooms, key=lambda x: x.get_price())