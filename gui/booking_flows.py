import customtkinter as ctk
from tkinter import messagebox
from core.booking_manager import get_booked_seats, create_booking

class CheckoutFrame(ctk.CTkFrame):
    def __init__(self, master, username, bus_data, selected_seats, travel_date, total_price, on_back, on_success):
        super().__init__(master, fg_color="transparent")
        self.username = username
        self.bus_data = bus_data
        self.selected_seats = selected_seats
        self.travel_date = travel_date
        self.total_price = total_price
        self.on_back = on_back
        self.on_success = on_success
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Center Box
        center = ctk.CTkFrame(self, fg_color="transparent")
        center.grid(row=0, column=0)
        
        # Header
        hdr = ctk.CTkFrame(center, fg_color="#e21a22", corner_radius=10)
        hdr.pack(fill="x")
        
        btn_back = ctk.CTkButton(hdr, text="⬅ Back", width=60, fg_color="transparent", hover_color="#c1181e", font=ctk.CTkFont(size=14, weight="bold"), command=self.on_back)
        btn_back.pack(side="left", padx=15, pady=15)
        ctk.CTkLabel(hdr, text="Payment Portal", text_color="white", font=ctk.CTkFont(size=20, weight="bold")).pack(side="left", padx=(100, 160), pady=15)
        
        # Main Body
        body = ctk.CTkFrame(center, fg_color="transparent", width=600)
        body.pack(fill="both", expand=True, pady=20)
        
        # Summary Card (Left/Top)
        sum_card = ctk.CTkFrame(body, fg_color=("white", "gray14"))
        sum_card.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(sum_card, text=f"{self.bus_data['operator']} | {self.bus_data['bus_type']}", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=15, pady=(15, 5))
        ctk.CTkLabel(sum_card, text=f"{self.bus_data['route_from']}  ➔  {self.bus_data['route_to']}", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=15)
        ctk.CTkLabel(sum_card, text=f"Travel Date: {self.travel_date}", text_color="gray60", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=15)
        ctk.CTkLabel(sum_card, text=f"Seats: {', '.join(self.selected_seats)}", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=15)
        
        price_lbl = ctk.CTkLabel(sum_card, text=f"Amount carefully calculated: ₹{self.total_price}", font=ctk.CTkFont(size=20, weight="bold"), text_color="#e21a22")
        price_lbl.pack(anchor="e", padx=15, pady=(20, 15))
        
        # Payment Methods
        pay_card = ctk.CTkFrame(body, fg_color=("gray95", "gray17"))
        pay_card.pack(fill="both", expand=True)
        ctk.CTkLabel(pay_card, text="Select Mock Payment Method", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=15, pady=15)
        
        self.pay_var = ctk.StringVar(value="upi")
        ctk.CTkRadioButton(pay_card, text="UPI ID", variable=self.pay_var, value="upi", fg_color="#e21a22", command=self.update_fields).pack(anchor="w", padx=30, pady=10)
        ctk.CTkRadioButton(pay_card, text="Credit / Debit Card", variable=self.pay_var, value="card", fg_color="#e21a22", command=self.update_fields).pack(anchor="w", padx=30, pady=10)
        
        self.input_frame = ctk.CTkFrame(pay_card, fg_color="transparent")
        self.input_frame.pack(fill="x", padx=30, pady=(20, 0))
        self.payment_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Enter UPI ID (e.g. user@bank)", height=45, font=ctk.CTkFont(size=14))
        self.payment_entry.pack(fill="x")
        
        # Checkout Button
        btn = ctk.CTkButton(center, text=f"PAY ₹{self.total_price} NOW", font=ctk.CTkFont(size=18, weight="bold"), height=55, fg_color="#e21a22", hover_color="#c1181e", command=self.process_payment)
        btn.pack(fill="x", pady=20)
        
    def update_fields(self):
        v = self.pay_var.get()
        if v == "upi":
            self.payment_entry.configure(placeholder_text="Enter UPI ID (e.g. user@bank)")
        else:
            self.payment_entry.configure(placeholder_text="Enter Card Number (16 Digits)")
            
    def process_payment(self):
        val = self.payment_entry.get().strip()
        if not val:
            messagebox.showwarning("Payment Failed", "Please enter dummy payment details to proceed!")
            return
            
        success, booking_id = create_booking(self.username, self.bus_data, self.selected_seats, self.travel_date, self.total_price)
        if success:
            self.on_success(booking_id, self.bus_data, self.selected_seats, self.total_price)
        else:
            messagebox.showerror("Error", f"Failed to book: {booking_id}")


class ConfirmationFrame(ctk.CTkFrame):
    def __init__(self, master, booking_id, bus_data, selected_seats, total_price, on_home):
        super().__init__(master, fg_color="transparent")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        center = ctk.CTkFrame(self, fg_color=("white", "gray14"), corner_radius=15, border_width=1, border_color="gray80")
        center.grid(row=0, column=0, pady=40)
        
        ctk.CTkLabel(center, text="🎉 Booking Confirmed!", text_color="#28a745", font=ctk.CTkFont(size=28, weight="bold")).pack(pady=(30, 10))
        ctk.CTkLabel(center, text=f"Your Ticket ID: {booking_id}", font=ctk.CTkFont(size=18)).pack(pady=(0, 20))
        
        tk_frame = ctk.CTkFrame(center, fg_color=("gray95", "gray17"), corner_radius=10)
        tk_frame.pack(fill="x", padx=30, pady=10)
        
        ctk.CTkLabel(tk_frame, text=f"{bus_data['operator']} | {bus_data['bus_type']}", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", padx=15, pady=(15, 5))
        ctk.CTkLabel(tk_frame, text=f"{bus_data['route_from']}  ➔  {bus_data['route_to']}", font=ctk.CTkFont(size=15)).pack(anchor="w", padx=15)
        ctk.CTkLabel(tk_frame, text=f"Timings: {bus_data['departure_time']} - {bus_data['arrival_time']}", font=ctk.CTkFont(size=14), text_color="gray60").pack(anchor="w", padx=15, pady=(0, 10))
        ctk.CTkLabel(tk_frame, text=f"Seats Booked: {', '.join(selected_seats)}", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=15)
        ctk.CTkLabel(tk_frame, text=f"Total Amount Paid: ₹{total_price}", font=ctk.CTkFont(size=16, weight="bold"), text_color="#e21a22").pack(anchor="w", padx=15, pady=(5, 15))
        
        ctk.CTkButton(center, text="Return to Home Dashboard", font=ctk.CTkFont(size=16, weight="bold"), height=50, fg_color="#e21a22", hover_color="#c1181e", command=on_home).pack(fill="x", padx=30, pady=30)


class SeatSelectionFrame(ctk.CTkFrame):
    def __init__(self, master, username, bus_data, travel_date, on_back, on_proceed):
        super().__init__(master, fg_color="transparent")
        self.username = username
        self.bus_data = bus_data
        self.travel_date = travel_date
        self.base_price = int(bus_data["price"])
        self.on_back = on_back
        self.on_proceed = on_proceed
        
        self.selected_seats = set()
        _, self.booked_seats = get_booked_seats(self.bus_data["id"], self.travel_date)
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Header Nav
        hdr = ctk.CTkFrame(self, fg_color="transparent", height=50)
        hdr.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        ctk.CTkButton(hdr, text="⬅ Back to Search", width=140, height=45, font=ctk.CTkFont(size=15, weight="bold"), fg_color="gray30", command=self.on_back).pack(side="left", padx=20)
        ctk.CTkLabel(hdr, text=f"Seat Selection - {bus_data['operator']} ({bus_data['bus_type']})", font=ctk.CTkFont(size=24, weight="bold")).pack(side="left", padx=20)

        # Left Panel (Graphical Layout)
        self.layout_panel = ctk.CTkScrollableFrame(self, fg_color=("gray90", "gray14"), border_width=1, border_color="gray80", corner_radius=15)
        self.layout_panel.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
        hdr_driver = ctk.CTkLabel(self.layout_panel, text="Front of Bus  [ Driver ] 🪑", font=ctk.CTkFont(size=18, weight="bold"), text_color="gray50")
        hdr_driver.pack(pady=(20, 10))
        
        self.grid_frame = ctk.CTkFrame(self.layout_panel, fg_color="transparent")
        self.grid_frame.pack(anchor="center", pady=10)
        
        self.build_grid()
        
        # Legend attached at bottom of left panel
        leg = ctk.CTkFrame(self.layout_panel, fg_color="transparent")
        leg.pack(pady=40)
        ctk.CTkButton(leg, text="Available", state="disabled", fg_color="white", text_color="black", corner_radius=5, width=80, height=35).pack(side="left", padx=5)
        ctk.CTkButton(leg, text="Selected", state="disabled", fg_color="#e21a22", text_color="white", width=80, height=35, corner_radius=5).pack(side="left", padx=15)
        ctk.CTkButton(leg, text="Booked", state="disabled", fg_color=("gray40", "gray30"), text_color="gray70", width=80, height=35, corner_radius=5).pack(side="left", padx=5)

        # Right Panel (Checkout Cart)
        self.cart_panel = ctk.CTkFrame(self, fg_color=("white", "gray17"), corner_radius=15)
        self.cart_panel.grid(row=1, column=1, sticky="nsew", padx=(0, 20), pady=(0, 20))
        
        ctk.CTkLabel(self.cart_panel, text="Booking Summary", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", padx=30, pady=30)
        
        self.summary_lbl = ctk.CTkLabel(self.cart_panel, text="Seats: None\n\nTotal Fare: ₹0", font=ctk.CTkFont(size=20), justify="left")
        self.summary_lbl.pack(anchor="w", padx=30, pady=20)
        
        self.proceed_btn = ctk.CTkButton(self.cart_panel, text="Proceed to Payment", fg_color="#e21a22", hover_color="#c1181e", font=ctk.CTkFont(size=18, weight="bold"), height=55, state="disabled", command=self.trigger_proceed)
        self.proceed_btn.pack(side="bottom", fill="x", padx=30, pady=30)
        
    def build_grid(self):
        rows = 12
        seat_counter = 1
        
        # 3 + 2 layout => 5 seats per row
        for r in range(rows):
            for c in range(5):
                seat_num = str(seat_counter)
                
                # Columns 0, 1, 2 are Left block
                # Column 3 is Aisle spacer
                # Columns 4, 5 are Right block
                actual_col = c if c < 3 else c + 1
                
                if c == 3:
                    self.grid_frame.columnconfigure(3, minsize=60) # Aisle separator
                
                btn = ctk.CTkButton(self.grid_frame, text=seat_num, width=50, height=50, font=ctk.CTkFont(size=14, weight="bold"))
                btn.grid(row=r, column=actual_col, padx=6, pady=6)
                
                if seat_num in self.booked_seats:
                    btn.configure(fg_color=("gray60", "gray30"), hover_color=("gray60", "gray30"), text_color="gray20", state="disabled")
                else:
                    btn.configure(fg_color="white", text_color="black", hover_color=("gray90", "gray80"), border_width=1, border_color="gray80",
                                  command=lambda s=seat_num, b=btn: self.toggle_seat(s, b))
                                  
                seat_counter += 1

    def toggle_seat(self, seat_num, btn):
        if seat_num in self.selected_seats:
            self.selected_seats.remove(seat_num)
            btn.configure(fg_color="white", text_color="black")
        else:
            if len(self.selected_seats) >= 6:
                messagebox.showwarning("Limit Reached", "You can only legitimately book max 6 seats at once per transaction!")
                return
            self.selected_seats.add(seat_num)
            btn.configure(fg_color="#e21a22", hover_color="#c1181e", text_color="white")
            
        self.update_summary()
        
    def update_summary(self):
        tot = len(self.selected_seats) * self.base_price
        c = ', '.join(sorted(self.selected_seats, key=lambda x: int(x))) if self.selected_seats else "None"
        self.summary_lbl.configure(text=f"Seats: {c}\n\nTotal Fare: ₹{tot}")
        if self.selected_seats:
            self.proceed_btn.configure(state="normal")
        else:
            self.proceed_btn.configure(state="disabled")
            
    def trigger_proceed(self):
        tot = len(self.selected_seats) * self.base_price
        self.on_proceed(sorted(self.selected_seats, key=lambda x: int(x)), tot)
