import tkinter as tk
from tkinter import ttk, messagebox
from core.room import Room

class HotelApp:
    def __init__(self, root, service):
        self.root = root
        self.service = service
        self.root.title("QUẢN LÝ KHÁCH SẠN")
        self.root.geometry("900x550")
        self.create_widgets()
        self.refresh_table(self.service.rooms)

    def create_widgets(self):
        # Frame Nhập liệu
        f = tk.LabelFrame(self.root, text="Thao tác dữ liệu", padx=10, pady=10)
        f.pack(fill="x", padx=10, pady=5)

        tk.Label(f, text="Mã:").grid(row=0, column=0)
        self.e_id = tk.Entry(f, width=10)
        self.e_id.grid(row=0, column=1, padx=5)

        tk.Label(f, text="Loại:").grid(row=0, column=2)
        self.e_type = tk.Entry(f, width=10)
        self.e_type.grid(row=0, column=3, padx=5)

        tk.Label(f, text="Giá:").grid(row=0, column=4)
        self.e_price = tk.Entry(f, width=10)
        self.e_price.grid(row=0, column=5, padx=5)

        tk.Label(f, text="Khách:").grid(row=0, column=6)
        self.e_cust = tk.Entry(f, width=15)
        self.e_cust.grid(row=0, column=7, padx=5)

        # Nút bấm
        btn_f = tk.Frame(self.root)
        btn_f.pack(fill="x", padx=10)
        tk.Button(btn_f, text="Thêm", bg="#28a745", fg="white", width=8, command=self.add).pack(side="left", padx=2)
        tk.Button(btn_f, text="Sửa", bg="#007bff", fg="white", width=8, command=self.update).pack(side="left", padx=2)
        tk.Button(btn_f, text="Xóa", bg="#dc3545", fg="white", width=8, command=self.delete).pack(side="left", padx=2)
        tk.Button(btn_f, text="Sắp xếp", width=8, command=self.sort).pack(side="left", padx=2)

        self.s_entry = tk.Entry(btn_f)
        self.s_entry.pack(side="right", padx=5)
        tk.Button(btn_f, text="Tìm kiếm", command=self.search).pack(side="right")

        # Table
        self.tree = ttk.Treeview(self.root, columns=(1,2,3,4,5), show="headings")
        cols = ["Mã Phòng", "Loại", "Giá", "Trạng thái", "Khách hàng"]
        for i, c in enumerate(cols, 1):
            self.tree.heading(i, text=c)
            self.tree.column(i, width=150, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    def refresh_table(self, data):
        for i in self.tree.get_children(): self.tree.delete(i)
        for r in data: 
            self.tree.insert("", "end", values=(
                r.get_room_id(), 
                r.get_room_type(), 
                f"{r.get_price():,.0f}", 
                r.get_status(), 
                r.get_customer_name()
            ))

    def add(self):
        try:
            # Đã sửa lỗi: dùng self.e_cust Thay vì self.e_entry
            r = Room(
                self.e_id.get(), 
                self.e_type.get(), 
                float(self.e_price.get()), 
                "Còn trống", 
                self.e_cust.get() or "N/A"
            )
            self.service.add_room(r)
            self.refresh_table(self.service.rooms)
            messagebox.showinfo("Thông báo", "Thêm thành công!")
        except Exception as e: 
            messagebox.showerror("Lỗi", f"Dữ liệu không hợp lệ: {e}")

    def update(self):
        try:
            data = {
                'type': self.e_type.get(),
                'price': float(self.e_price.get()),
                'status': "Đã đặt",
                'cust': self.e_cust.get()
            }
            if self.service.update_room(self.e_id.get(), data):
                self.refresh_table(self.service.rooms)
                messagebox.showinfo("Thông báo", "Cập nhật thành công!")
            else:
                messagebox.showwarning("Lỗi", "Không tìm thấy mã phòng")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def delete(self):
        try:
            selected = self.tree.selection()
            if not selected: return
            sid = self.tree.item(selected[0])['values'][0]
            if messagebox.askyesno("Xác nhận", f"Xóa phòng {sid}?"):
                self.service.delete_room(str(sid))
                self.refresh_table(self.service.rooms)
        except:
            messagebox.showwarning("Chú ý", "Hãy chọn một dòng để xóa")

    def search(self):
        results = self.service.search_by_keyword(self.s_entry.get())
        self.refresh_table(results)

    def sort(self):
        results = self.service.sort_by_price()
        self.refresh_table(results)