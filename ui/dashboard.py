import tkinter as tk
from tkinter import ttk, messagebox
import random
from core.room import VipRoom, StandardRoom
from core.booking import Booking

class HotelApp:
    def __init__(self, root, service):
        self.root = root
        self.service = service
        self.root.title("QUẢN LÝ KHÁCH SẠN (ROOMS, BOOKINGS & INVOICES)")
        self.root.geometry("1100x700")
        self.create_widgets()
        self.refresh_table()

    def create_widgets(self):
        # Tạo Notebook (Chia 2 Tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        #tab1 quan ly va dat phong
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="Quản lý Hiện Tại")

        # pannel
        top_frame = tk.Frame(self.tab1)
        top_frame.pack(fill="x", padx=10, pady=5)
        
        # info room
        f_room = tk.LabelFrame(top_frame, text="Thông tin Phòng (rooms.txt)", padx=10, pady=10)
        f_room.pack(side="left", fill="both", expand=True, padx=5)

        tk.Label(f_room, text="Mã Phòng:").grid(row=0, column=0, pady=5, sticky="e")
        self.e_room_id = tk.Entry(f_room, width=12)
        self.e_room_id.grid(row=0, column=1, padx=5)

        tk.Label(f_room, text="Loại:").grid(row=0, column=2, pady=5, sticky="e")
        self.e_type = ttk.Combobox(f_room, values=["VIP", "Standard"], width=10)
        self.e_type.current(1)
        self.e_type.grid(row=0, column=3, padx=5)

        tk.Label(f_room, text="Giá/Đêm:").grid(row=1, column=0, pady=5, sticky="e")
        self.e_price = tk.Entry(f_room, width=12)
        self.e_price.grid(row=1, column=1, padx=5)

        tk.Label(f_room, text="Sức chứa:").grid(row=1, column=2, pady=5, sticky="e")
        self.e_capacity = tk.Entry(f_room, width=12)
        self.e_capacity.grid(row=1, column=3, padx=5)

        btn_room_f = tk.Frame(f_room)
        btn_room_f.grid(row=2, column=0, columnspan=4, pady=10)
        tk.Button(btn_room_f, text="Lưu Phòng", bg="#28a745", fg="white", command=self.save_room, width=10).pack(side="left", padx=5)
        tk.Button(btn_room_f, text="Xóa Phòng", bg="#dc3545", fg="white", command=self.delete_room, width=10).pack(side="left", padx=5)

        # infor booking room
        f_book = tk.LabelFrame(top_frame, text="Thông tin Đặt Phòng (bookings.txt)", padx=10, pady=10)
        f_book.pack(side="right", fill="both", expand=True, padx=5)

        tk.Label(f_book, text="Mã Đặt:").grid(row=0, column=0, pady=5, sticky="e")
        self.e_booking_id = tk.Entry(f_book, width=15)
        self.e_booking_id.grid(row=0, column=1, padx=5)

        tk.Label(f_book, text="Tên Khách:").grid(row=0, column=2, pady=5, sticky="e")
        self.e_cust = tk.Entry(f_book, width=15)
        self.e_cust.grid(row=0, column=3, padx=5)

        tk.Label(f_book, text="Số Khách:").grid(row=1, column=0, pady=5, sticky="e")
        self.e_num_guests = tk.Entry(f_book, width=15)
        self.e_num_guests.grid(row=1, column=1, padx=5)

        tk.Label(f_book, text="Số Đêm:").grid(row=1, column=2, pady=5, sticky="e")
        self.e_duration = tk.Entry(f_book, width=15)
        self.e_duration.grid(row=1, column=3, padx=5)

        btn_book_f = tk.Frame(f_book)
        btn_book_f.grid(row=2, column=0, columnspan=4, pady=10)
        tk.Button(btn_book_f, text="Đặt Phòng", bg="#007bff", fg="white", command=self.book_room, width=10).pack(side="left", padx=5)
        tk.Button(btn_book_f, text="Trả Phòng (Tính HĐ)", bg="#ffc107", command=self.checkout, width=18).pack(side="left", padx=5)

        # view table
        self.tree = ttk.Treeview(self.tab1, columns=(1,2,3,4,5,6,7,8,9), show="headings", height=15)
        cols = ["Mã Phòng", "Loại", "Giá", "Sức Chứa", "Trạng Thái", "Mã Đặt", "Tên Khách", "Số Khách", "Số Đêm"]
        widths = [80, 80, 100, 80, 100, 80, 120, 80, 80]
        for i, (c, w) in enumerate(zip(cols, widths), 1):
            self.tree.heading(i, text=c)
            self.tree.column(i, width=w, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        #event dobule click
        self.tree.bind('<Double-1>', self.on_double_click)


        # history invoice
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="Danh sách Hóa Đơn")

        f_inv_btn = tk.Frame(self.tab2)
        f_inv_btn.pack(fill="x", padx=10, pady=5)
        tk.Button(f_inv_btn, text="Làm mới", bg="#17a2b8", fg="white", command=self.refresh_invoices).pack(side="left")

        self.tree_inv = ttk.Treeview(self.tab2, columns=(1,2,3,4,5,6), show="headings", height=20)
        inv_cols = ["Mã Đặt", "Mã Phòng", "Tên Khách Hàng", "Số Đêm", "Tổng Tiền (VNĐ)", "Thời Gian Thanh Toán"]
        inv_widths = [100, 100, 200, 100, 150, 200]
        for i, (c, w) in enumerate(zip(inv_cols, inv_widths), 1):
            self.tree_inv.heading(i, text=c)
            self.tree_inv.column(i, width=w, anchor="center")
        self.tree_inv.pack(fill="both", expand=True, padx=10, pady=10)

        # Bind event when changing tabs to auto refresh invoices
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)


    # logic tab 1
    def on_double_click(self, event):
        try:
            selected = self.tree.selection()
            if not selected: return
            item = self.tree.item(selected[0])['values']
            
            for e in (self.e_room_id, self.e_price, self.e_capacity, self.e_booking_id, self.e_cust, self.e_num_guests, self.e_duration):
                e.delete(0, tk.END)

            self.e_room_id.insert(0, str(item[0]))
            self.e_type.set(str(item[1]))
            price_clean = str(item[2]).replace(',', '')
            self.e_price.insert(0, price_clean)
            self.e_capacity.insert(0, str(item[3]))

            if str(item[4]) != "Trống":
                self.e_booking_id.insert(0, str(item[5]))
                self.e_cust.insert(0, str(item[6]))
                self.e_num_guests.insert(0, str(item[7]))
                self.e_duration.insert(0, str(item[8]))
            else:
                self.e_booking_id.insert(0, f"BK{random.randint(100,999)}")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def refresh_table(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        rooms = self.service.get_all_rooms
        
        for r in rooms:
            status = self.service.get_room_status(r.get_room_id())
            booking = self.service.get_booking_for_room(r.get_room_id())
            
            b_id = booking.get_booking_id() if booking else ""
            b_cust = booking.get_customer_name() if booking else ""
            b_num = booking.get_num_people() if booking else ""
            b_dur = booking.get_duration_days() if booking else ""
            
            self.tree.insert("", "end", values=(
                r.get_room_id(), 
                r.get_room_type(), 
                f"{r.get_price():,.0f}", 
                r.get_capacity(),
                status,
                b_id, b_cust, b_num, b_dur
            ))

    def save_room(self):
        try:
            r_type = self.e_type.get()
            price = float(self.e_price.get())
            cap = int(self.e_capacity.get())
            r_id = self.e_room_id.get().strip()

            if not r_id: raise ValueError("Vui lòng nhập Mã phòng")

            room_obj = VipRoom(r_id, price, cap) if r_type.lower() == "vip" else StandardRoom(r_id, price, cap)
            
            if self.service.get_room(r_id):
                self.service.update_room(r_id, {'type': r_type, 'price': price, 'capacity': cap})
                messagebox.showinfo("Thông báo", "Sửa thành công!")
            else:
                self.service.add_room(room_obj)
                messagebox.showinfo("Thông báo", "Thêm thành công!")
                
            self.refresh_table()
        except Exception as e: 
            messagebox.showerror("Lỗi", str(e))

    def delete_room(self):
        try:
            r_id = self.e_room_id.get()
            if messagebox.askyesno("Xác nhận", f"Xóa phòng {r_id}?"):
                self.service.delete_room(r_id)
                self.refresh_table()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def book_room(self):
        try:
            bk = Booking(
                self.e_booking_id.get(),
                self.e_room_id.get(),
                self.e_cust.get(),
                int(self.e_num_guests.get()),
                int(self.e_duration.get())
            )
            self.service.book_room(bk)
            self.refresh_table()
            messagebox.showinfo("Thông báo", "Đặt phòng thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def checkout(self):
        try:
            b_id = self.e_booking_id.get().strip()
            if not b_id:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn hoặc nhập mã đặt phòng (Booking ID) để thanh toán!")
                return
                
            if messagebox.askyesno("Xác nhận", f"Xác nhận xuất hóa đơn và trả phòng cho mã đặt: {b_id}?"):
                invoice = self.service.checkout_and_generate_invoice(b_id)
                self.refresh_table()
                
                msg = (
                    f"---- HÓA ĐƠN ({invoice.get_checkout_date()}) ----\n"
                    f"Mã phòng: {invoice.get_room_id()}\n"
                    f"Khách hàng: {invoice.get_customer_name()}\n"
                    f"Thời gian lưu trú: {invoice.get_duration_days()} đêm\n"
                    f"TỔNG TIỀN: {invoice.get_total_amount():,.0f} VNĐ\n\n"
                    f"(Hóa đơn đã được lưu vào hệ thống)"
                )
                messagebox.showinfo("Trả phòng thành công!", msg)
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    # logic tab 2
    def on_tab_changed(self, event):
        """Khi bấm sang Tab 2, tự động tải lại danh sách hóa đơn"""
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")
        if tab_text == "Danh sách Hóa Đơn":
            self.refresh_invoices()

    def refresh_invoices(self):
        for i in self.tree_inv.get_children(): self.tree_inv.delete(i)
        invoices = self.service.get_all_invoices()
        for inv in invoices:
            self.tree_inv.insert("", "end", values=(
                inv.get_booking_id(),
                inv.get_room_id(),
                inv.get_customer_name(),
                inv.get_duration_days(),
                f"{inv.get_total_amount():,.0f}",
                inv.get_checkout_date()
            ))