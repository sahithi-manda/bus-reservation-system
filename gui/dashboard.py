import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import Calendar
import datetime

CITIES = [
    {"city": "Hyderabad", "state": "Telangana"},
    {"city": "Bangalore", "state": "Karnataka"},
    {"city": "Chennai", "state": "Tamil Nadu"},
    {"city": "Goa", "state": "Goa"},
    {"city": "Vijayawada", "state": "Andhra Pradesh"},
    {"city": "Nellore", "state": "Andhra Pradesh"}
]

class CityDropdown(ctk.CTkToplevel):
    def __init__(self, master, target_entry):
        super().__init__(master)
        self.target_entry = target_entry
        self.overrideredirect(True)
        self.configure(fg_color="white")
        
        self.border_frame = ctk.CTkFrame(self, fg_color="white", border_width=1, border_color="gray80", corner_radius=5)
        self.border_frame.pack(fill="both", expand=True)
        
        title = ctk.CTkLabel(self.border_frame, text="POPULAR CITIES", text_color="gray50", font=ctk.CTkFont(size=11, weight="bold"))
        title.pack(anchor="w", padx=15, pady=(10, 5))
        
        for data in CITIES:
            row = ctk.CTkFrame(self.border_frame, fg_color="white", corner_radius=0, cursor="hand2")
            row.pack(fill="x", pady=0)
            
            def on_enter(e, r=row): r.configure(fg_color="gray90")
            def on_leave(e, r=row): r.configure(fg_color="white")
            def on_click(e, city=data["city"]):
                self.target_entry.delete(0, 'end')
                self.target_entry.insert(0, city)
                self.destroy()
                
            icon = ctk.CTkLabel(row, text="🚌", font=ctk.CTkFont(size=18))
            icon.pack(side="left", padx=(15, 10), pady=10)
            
            text_frame = ctk.CTkFrame(row, fg_color="transparent")
            text_frame.pack(side="left", fill="both", expand=True, pady=10)
            
            city_lbl = ctk.CTkLabel(text_frame, text=data["city"], font=ctk.CTkFont(size=14, weight="bold"), text_color="black")
            city_lbl.pack(anchor="w")
            state_lbl = ctk.CTkLabel(text_frame, text=data["state"], font=ctk.CTkFont(size=11), text_color="gray60")
            state_lbl.pack(anchor="w")
            
            for widget in [row, icon, text_frame, city_lbl, state_lbl]:
                widget.bind("<Enter>", on_enter)
                widget.bind("<Leave>", on_leave)
                widget.bind("<Button-1>", on_click)
                
        self.target_entry.update_idletasks()
        x = self.target_entry.winfo_rootx()
        y = self.target_entry.winfo_rooty() + self.target_entry.winfo_height() + 5
        width = self.target_entry.winfo_width()
        self.geometry(f"{width}x330+{x}+{y}")
        
        self.focus_set()
        self.bind("<FocusOut>", self.check_focus_loss)

    def check_focus_loss(self, event):
        self.after(50, getattr(self, "_execute_focus_check"))
        
    def _execute_focus_check(self):
        fw = self.focus_get()
        if not fw or str(fw).startswith(str(self)) == False:
            self.destroy()

class DashboardWindow(ctk.CTkToplevel):
    def __init__(self, master, username, logout_callback):
        super().__init__(master)
        self.username = username
        self.logout_callback = logout_callback

        self.title("Bus Reservation System - AbhiBus Mode")
        self.geometry("1400x800")
        self.minsize(1200, 600)
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Top Bar
        self.nav_frame = ctk.CTkFrame(self, height=60, corner_radius=0, fg_color=("gray95", "gray17"))
        self.nav_frame.grid(row=0, column=0, sticky="ew")
        
        from core.utils import get_logo_image
        self.nav_logo_img = get_logo_image(size=(160, 55))
        
        if self.nav_logo_img:
            self.nav_title = ctk.CTkLabel(self.nav_frame, text="", image=self.nav_logo_img)
            self.nav_title.grid(row=0, column=0, padx=30, pady=5, sticky="w")
            self.nav_frame.grid_columnconfigure(1, weight=1)
        else:
            self.nav_frame.grid_columnconfigure(1, weight=1)
            self.nav_left = ctk.CTkLabel(self.nav_frame, text="", width=150)
            self.nav_left.grid(row=0, column=0, padx=20, pady=15)
            self.nav_title = ctk.CTkLabel(self.nav_frame, text="Bus Reservation System", font=ctk.CTkFont(size=22, weight="bold"), text_color="#e21a22")
            self.nav_title.grid(row=0, column=1, pady=15)
        
        self.nav_right = ctk.CTkFrame(self.nav_frame, fg_color="transparent")
        self.nav_right.grid(row=0, column=2, padx=20, pady=15, sticky="e")
        
        self.home_btn = ctk.CTkButton(self.nav_right, text="🏠 Home", width=100, fg_color="transparent", hover_color=("gray90", "gray30"), text_color=("black", "white"), font=ctk.CTkFont(size=14, weight="bold"), command=self.rebuild_search_dashboard)
        self.home_btn.pack(side="left", padx=5)
        
        self.bookings_btn = ctk.CTkButton(self.nav_right, text="🎟️ My Bookings", width=140, fg_color="transparent", hover_color=("gray90", "gray30"), text_color=("black", "white"), font=ctk.CTkFont(size=14, weight="bold"), command=self.show_bookings_history)
        self.bookings_btn.pack(side="left", padx=5)
        
        self.cancel_nav_btn = ctk.CTkButton(self.nav_right, text="❌ Cancel Ticket", width=140, fg_color="transparent", hover_color=("#ffcccc", "#660000"), text_color="#e21a22", font=ctk.CTkFont(size=14, weight="bold"), command=self.show_bookings_history)
        self.cancel_nav_btn.pack(side="left", padx=5)

        self.user_menu_var = ctk.StringVar(value=f"👤 {self.username}")
        self.user_menu = ctk.CTkOptionMenu(self.nav_right, variable=self.user_menu_var, 
                                           values=["My Profile", "Logout"],
                                           command=self.handle_user_menu, width=130,
                                           fg_color=("gray90", "gray25"), text_color=("black", "white"),
                                           button_color=("gray90", "gray25"), button_hover_color=("gray85", "gray30"))
        self.user_menu.pack(side="left", padx=5)

        # Main Layout
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.content_frame.grid_rowconfigure(0, weight=0) # Search Card
        self.content_frame.grid_rowconfigure(1, weight=1) # The Dual Pane splits here!
        self.content_frame.grid_columnconfigure(0, weight=1)

        # Search Box
        self.search_card = ctk.CTkFrame(self.content_frame, corner_radius=15, fg_color=("white", "gray14"))
        self.search_card.grid(row=0, column=0, padx=20, pady=(0, 20), sticky="ew")
        for i in range(6): self.search_card.grid_columnconfigure(i, weight=1)
        
        # Central Dashboard Logo
        self.home_logo_img = get_logo_image(size=(300, 100))
        if self.home_logo_img:
            logo_lbl = ctk.CTkLabel(self.search_card, text="", image=self.home_logo_img)
            logo_lbl.grid(row=0, column=0, columnspan=6, pady=(20, 0))
            input_row = 1
        else:
            input_row = 0

        self.leaving_entry = ctk.CTkEntry(self.search_card, placeholder_text="📍 Leaving From", height=45, font=ctk.CTkFont(size=14))
        self.leaving_entry.grid(row=input_row, column=0, padx=(20, 10), pady=20, sticky="ew")
        self.leaving_entry.bind("<FocusIn>", lambda e: self.open_city_dropdown(self.leaving_entry))
        self.leaving_entry.bind("<Button-1>", lambda e: self.open_city_dropdown(self.leaving_entry))

        self.going_entry = ctk.CTkEntry(self.search_card, placeholder_text="🏁 Going To", height=45, font=ctk.CTkFont(size=14))
        self.going_entry.grid(row=input_row, column=1, padx=10, pady=20, sticky="ew")
        self.going_entry.bind("<FocusIn>", lambda e: self.open_city_dropdown(self.going_entry))
        self.going_entry.bind("<Button-1>", lambda e: self.open_city_dropdown(self.going_entry))

        self.selected_date = ctk.StringVar()
        self.set_date(0)
        
        self.date_btn = ctk.CTkButton(self.search_card, textvariable=self.selected_date, height=45,
                                      fg_color=("gray95", "gray20"), text_color=("black", "white"), hover_color=("gray85", "gray30"),
                                      command=self.open_calendar_popup)
        self.date_btn.grid(row=input_row, column=2, padx=10, pady=20, sticky="ew")

        self.today_btn = ctk.CTkButton(self.search_card, text="Today", height=45, width=80, fg_color="transparent", border_width=1, text_color=("black", "white"), hover_color=("gray90", "gray30"), border_color="gray80", command=lambda: self.set_date(0))
        self.today_btn.grid(row=input_row, column=3, padx=5, pady=20, sticky="ew")

        self.tomorrow_btn = ctk.CTkButton(self.search_card, text="Tomorrow", height=45, width=80, fg_color="transparent", border_width=1, text_color=("black", "white"), hover_color=("gray90", "gray30"), border_color="gray80", command=lambda: self.set_date(1))
        self.tomorrow_btn.grid(row=input_row, column=4, padx=(5, 10), pady=20, sticky="ew")

        self.search_btn = ctk.CTkButton(self.search_card, text="🔍 Search", height=45, width=120, font=ctk.CTkFont(size=15, weight="bold"), fg_color="#e21a22", hover_color="#c1181e", command=self.handle_search)
        self.search_btn.grid(row=input_row, column=5, padx=(10, 20), pady=20, sticky="ew")

        self.active_dropdown = None
        self.all_buses = [] # In-memory hold

        # Holder for the Dual Pane
        self.dual_pane = None
        
        # Central routing var
        self.flow_frame = None

    def open_city_dropdown(self, entry_widget):
        if self.active_dropdown and self.active_dropdown.winfo_exists():
            if getattr(self.active_dropdown, 'target_entry', None) == entry_widget: return
            else: self.active_dropdown.destroy()
        self.active_dropdown = CityDropdown(self, entry_widget)

    def set_date(self, days_ahead):
        date = datetime.date.today() + datetime.timedelta(days=days_ahead)
        self.selected_date.set(f"📅 {date.strftime('%Y-%m-%d')}")

    def open_calendar_popup(self):
        top = ctk.CTkToplevel(self)
        top.title("Select Date")
        top.geometry("300x300")
        top.resizable(False, False)
        top.grab_set() 
        top.focus()
        x, y = self.winfo_x() + (self.winfo_width() // 2) - 150, self.winfo_y() + (self.winfo_height() // 2) - 150
        top.geometry(f"+{x}+{y}")

        cal = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd', background='white', foreground='black', bordercolor='gray', headersbackground='light gray', headersforeground='black', selectbackground='#e21a22', selectforeground='white')
        cal.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkButton(top, text="Confirm", fg_color="#e21a22", hover_color="#c1181e", command=lambda: [self.selected_date.set(f"📅 {cal.get_date()}"), top.destroy()]).pack(pady=(0, 20))

    def handle_user_menu(self, choice):
        self.user_menu_var.set(f"👤 {self.username}")
        if choice == "Logout":
            self.destroy()
            self.logout_callback()
        elif choice == "My Profile":
            from core.auth_manager import get_user_profile
            success, data = get_user_profile(self.username)
            if success:
                msg = f"User Profile Details\n" + "━" * 25 + "\n\n"
                msg += f"👤 Username:\t{data['username']}\n"
                msg += f"📧 Email ID:\t{data['email']}\n"
                msg += f"📱 Phone No:\t{data['phone']}\n"
                messagebox.showinfo("My Profile", msg)
            else:
                messagebox.showerror("Error", "Could not fetch user profile details.")

    def show_bookings_history(self):
        # Wipe the screen safely
        self.clear_flow_frame()
        if self.dual_pane:
            self.dual_pane.grid_remove()
        self.search_card.grid_remove() # Hide search bar safely
        
        self.bookings_pane = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.bookings_pane.grid(row=1, column=0, sticky="nsew")
        self.bookings_pane.grid_rowconfigure(1, weight=1)
        self.bookings_pane.grid_columnconfigure(0, weight=1)
        
        # Header
        hdr = ctk.CTkFrame(self.bookings_pane, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        ctk.CTkLabel(hdr, text="My Ticket History", font=ctk.CTkFont(size=24, weight="bold")).pack(side="left", padx=20)
        ctk.CTkButton(hdr, text="Back to Search", fg_color="gray30", hover_color="gray20", command=self.rebuild_search_dashboard).pack(side="right", padx=20)
        
        # Area
        scroll = ctk.CTkScrollableFrame(self.bookings_pane, fg_color="transparent")
        scroll.grid(row=1, column=0, sticky="nsew", padx=20)
        
        from core.booking_manager import get_user_bookings
        success, tickets = get_user_bookings(self.username)
        
        if not tickets:
            ctk.CTkLabel(scroll, text="You have no active or historical bookings.", font=ctk.CTkFont(size=18), text_color="gray50").pack(pady=100)
            return
            
        for t in tickets:
            card = ctk.CTkFrame(scroll, fg_color=("white", "gray17"), corner_radius=15, border_width=1, border_color="gray80")
            card.pack(fill="x", pady=10)
            
            top_bar = ctk.CTkFrame(card, fg_color="gray90", corner_radius=15)
            top_bar.pack(fill="x", padx=2, pady=2)
            ctk.CTkLabel(top_bar, text=f"Booking ID: {t['booking_id']}", text_color="black", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=15, pady=5)
            ctk.CTkLabel(top_bar, text=f"Travel Date: {t['travel_date']}", text_color="black").pack(side="right", padx=15, pady=5)
            
            body = ctk.CTkFrame(card, fg_color="transparent")
            body.pack(fill="x", padx=15, pady=15)
            
            ctk.CTkLabel(body, text=f"{t['operator']} | {t['route_from']}  ➔  {t['route_to']}", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w")
            ctk.CTkLabel(body, text=f"{t['departure_time']} - {t['arrival_time']} ({t['duration']})", text_color="gray60").pack(anchor="w", pady=(2,10))
            
            ctk.CTkLabel(body, text=f"Seats: {t['seat_numbers']}", font=ctk.CTkFont(size=14)).pack(anchor="w")
            ctk.CTkLabel(body, text=f"Total Amount Paid: ₹{t['total_amount']}", font=ctk.CTkFont(size=16, weight="bold"), text_color="#e21a22").pack(anchor="w", pady=(5,0))
            
            ctk.CTkButton(card, text="Cancel Ticket", width=120, height=35, font=ctk.CTkFont(weight="bold"), fg_color="transparent", text_color="#e21a22", border_width=2, border_color="#e21a22", hover_color=("gray90", "gray20"), command=lambda bk=t['booking_id']: self.cancel_ticket(bk)).pack(anchor="e", padx=15, pady=(0, 15))

    def cancel_ticket(self, booking_id):
        if messagebox.askyesno("Confirm Cancellation", f"Are you completely sure you want to cancel Ticket {booking_id}?"):
            from core.booking_manager import cancel_booking
            success, msg = cancel_booking(self.username, booking_id)
            if success:
                messagebox.showinfo("Success", f"Ticket {booking_id} successfully cancelled!\n\nYour money (₹0) has been refunded.")
                self.show_bookings_history()
            else:
                messagebox.showerror("Error", msg)

    def clear_flow_frame(self):
        if getattr(self, "flow_frame", None) and self.flow_frame.winfo_exists():
            self.flow_frame.destroy()
            self.flow_frame = None

    def rebuild_search_dashboard(self):
        self.clear_flow_frame()
        if getattr(self, "bookings_pane", None) and self.bookings_pane.winfo_exists():
            self.bookings_pane.destroy()
            
        self.search_card.grid() # Reveal search bar
        if getattr(self, "dual_pane", None) and self.dual_pane.winfo_exists():
            self.dual_pane.grid()
        elif hasattr(self, "all_buses") and self.all_buses:
            self.handle_search()
            
    def handle_search(self):
        leaving = self.leaving_entry.get().strip()
        going = self.going_entry.get().strip()
        date_str = self.selected_date.get()
        if not leaving or not going:
            messagebox.showwarning("Warning", "Please select locations!")
            return
            
        from core.booking_manager import search_buses
        success, buses = search_buses(leaving, going, date_str)
        self.all_buses = buses if success else []
        self.current_date_str = date_str.replace("📅 ", "")

        # Always wipe dual pane completely to rebuild
        if self.dual_pane: self.dual_pane.destroy()
        
        if not self.all_buses:
            self.dual_pane = ctk.CTkFrame(self.content_frame, fg_color="transparent")
            self.dual_pane.grid(row=1, column=0, sticky="nsew")
            ctk.CTkLabel(self.dual_pane, text=f"No buses currently running for {leaving} to {going}.", font=ctk.CTkFont(size=20, weight="bold"), text_color="gray50").pack(pady=100)
            return

        self.dual_pane = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.dual_pane.grid(row=1, column=0, sticky="nsew")
        self.dual_pane.grid_columnconfigure(0, weight=0, minsize=290) # Left Filters Pane
        self.dual_pane.grid_columnconfigure(1, weight=1) # Right Results Pane
        self.dual_pane.grid_rowconfigure(0, weight=1)

        self.build_filters_panel()
        
        self.results_holder = ctk.CTkFrame(self.dual_pane, fg_color="transparent")
        self.results_holder.grid(row=0, column=1, sticky="nsew", padx=(15, 0))
        self.results_holder.grid_rowconfigure(1, weight=1)
        self.results_holder.grid_columnconfigure(0, weight=1)

        # Header for Results
        self.res_header = ctk.CTkFrame(self.results_holder, fg_color="transparent", height=40)
        self.res_header.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.res_title = ctk.CTkLabel(self.res_header, text=f"{len(self.all_buses)} Buses Found", font=ctk.CTkFont(size=18, weight="bold"))
        self.res_title.pack(side="left")

        self.sort_var = ctk.StringVar(value="Sort: Default")
        self.sort_opts = ctk.CTkOptionMenu(self.res_header, variable=self.sort_var, values=["Sort: Default", "Price: Low to High", "Price: High to Low"], command=self.apply_filters, fg_color=("gray90", "gray25"), text_color=("black", "white"), button_color=("gray90", "gray25"))
        self.sort_opts.pack(side="right")

        self.scroll_results = ctk.CTkScrollableFrame(self.results_holder, fg_color="transparent")
        self.scroll_results.grid(row=1, column=0, sticky="nsew")

        # Initial Render
        self.apply_filters()

    def build_filters_panel(self):
        f_panel = ctk.CTkFrame(self.dual_pane, fg_color=("white", "gray14"), corner_radius=15)
        f_panel.grid(row=0, column=0, sticky="nsew", padx=10, pady=(0, 10))

        # Title / Clear
        top_bar = ctk.CTkFrame(f_panel, fg_color="transparent")
        top_bar.pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(top_bar, text="FILTERS", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left")
        ctk.CTkButton(top_bar, text="CLEAR ALL", width=70, fg_color="transparent", text_color="#e21a22", hover_color=("gray90", "gray20"), command=self.clear_all_filters).pack(side="right")

        # Price Sliders
        ctk.CTkLabel(f_panel, text="Price Range", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=20, pady=(10, 5))
        
        self.min_price_var = ctk.DoubleVar(value=300)
        self.max_price_var = ctk.DoubleVar(value=3000)
        
        self.price_lbl_min = ctk.CTkLabel(f_panel, text="Min: ₹300", font=ctk.CTkFont(size=12))
        self.price_lbl_min.pack(anchor="w", padx=20)
        self.min_slider = ctk.CTkSlider(f_panel, from_=300, to=3000, variable=self.min_price_var, button_color="#e21a22", button_hover_color="#c1181e", command=self.slider_update)
        self.min_slider.pack(fill="x", padx=20, pady=(0, 10))

        self.price_lbl_max = ctk.CTkLabel(f_panel, text="Max: ₹3000", font=ctk.CTkFont(size=12))
        self.price_lbl_max.pack(anchor="w", padx=20)
        self.max_slider = ctk.CTkSlider(f_panel, from_=300, to=3000, variable=self.max_price_var, button_color="#e21a22", button_hover_color="#c1181e", command=self.slider_update)
        self.max_slider.pack(fill="x", padx=20, pady=(0, 20))

        # Dep Time
        ctk.CTkLabel(f_panel, text="Departure Time", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=20, pady=(10, 5))
        self.chk_morning = ctk.CTkCheckBox(f_panel, text="Before 10 AM", fg_color="#e21a22", hover_color="#c1181e", command=self.apply_filters)
        self.chk_morning.pack(anchor="w", padx=20, pady=5)
        self.chk_afternoon = ctk.CTkCheckBox(f_panel, text="10 AM - 5 PM", fg_color="#e21a22", hover_color="#c1181e", command=self.apply_filters)
        self.chk_afternoon.pack(anchor="w", padx=20, pady=5)
        self.chk_evening = ctk.CTkCheckBox(f_panel, text="5 PM - 11 PM", fg_color="#e21a22", hover_color="#c1181e", command=self.apply_filters)
        self.chk_evening.pack(anchor="w", padx=20, pady=5)
        self.chk_night = ctk.CTkCheckBox(f_panel, text="After 11 PM", fg_color="#e21a22", hover_color="#c1181e", command=self.apply_filters)
        self.chk_night.pack(anchor="w", padx=20, pady=(5, 20))

        # Boarding/Dropping dynamic extraction
        b_pts, d_pts = set(), set()
        for b in self.all_buses:
            for bp in b['boarding_points']: b_pts.add(bp)
            for dp in b['dropping_points']: d_pts.add(dp)

        ctk.CTkLabel(f_panel, text="Boarding Point", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=20, pady=(10, 5))
        self.board_var = ctk.StringVar(value="All")
        self.board_menu = ctk.CTkOptionMenu(f_panel, variable=self.board_var, values=["All"] + list(b_pts), command=self.apply_filters, fg_color=("gray90", "gray25"), text_color=("black", "white"), button_color=("gray90", "gray25"))
        self.board_menu.pack(fill="x", padx=20, pady=(0, 15))

        ctk.CTkLabel(f_panel, text="Dropping Point", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=20, pady=(10, 5))
        self.drop_var = ctk.StringVar(value="All")
        self.drop_menu = ctk.CTkOptionMenu(f_panel, variable=self.drop_var, values=["All"] + list(d_pts), command=self.apply_filters, fg_color=("gray90", "gray25"), text_color=("black", "white"), button_color=("gray90", "gray25"))
        self.drop_menu.pack(fill="x", padx=20, pady=(0, 20))

    def slider_update(self, val):
        self.price_lbl_min.configure(text=f"Min: ₹{int(self.min_price_var.get())}")
        self.price_lbl_max.configure(text=f"Max: ₹{int(self.max_price_var.get())}")
        self.apply_filters()

    def clear_all_filters(self):
        self.min_price_var.set(300)
        self.max_price_var.set(3000)
        self.slider_update(0)
        self.chk_morning.deselect()
        self.chk_afternoon.deselect()
        self.chk_evening.deselect()
        self.chk_night.deselect()
        self.board_var.set("All")
        self.drop_var.set("All")
        self.apply_filters()

    def apply_filters(self, *args):
        for w in self.scroll_results.winfo_children(): w.destroy()
        
        filtered = []
        min_p = int(self.min_price_var.get())
        max_p = int(self.max_price_var.get())
        board = self.board_var.get()
        drop = self.drop_var.get()
        
        want_mor = self.chk_morning.get() == 1
        want_aft = self.chk_afternoon.get() == 1
        want_eve = self.chk_evening.get() == 1
        want_nig = self.chk_night.get() == 1
        any_time_selected = want_mor or want_aft or want_eve or want_nig

        for b in self.all_buses:
            if b['price'] < min_p or b['price'] > max_p: continue
            if board != "All" and board not in b['boarding_points']: continue
            if drop != "All" and drop not in b['dropping_points']: continue
            
            if any_time_selected:
                hr = b['departure_hour']
                match_time = False
                if want_mor and hr < 10: match_time = True
                if want_aft and 10 <= hr < 17: match_time = True
                if want_eve and 17 <= hr < 23: match_time = True
                if want_nig and hr >= 23: match_time = True
                if not match_time: continue

            filtered.append(b)

        # Sorting logic
        st = self.sort_var.get()
        if st == "Price: Low to High":
            filtered.sort(key=lambda x: x['price'])
        elif st == "Price: High to Low":
            filtered.sort(key=lambda x: x['price'], reverse=True)

        self.res_title.configure(text=f"{len(filtered)} Buses Found")

        if not filtered:
            ctk.CTkLabel(self.scroll_results, text="No buses match those exact filters.", font=ctk.CTkFont(size=15)).pack(pady=40)
            return

        for bus in filtered:
            self.draw_bus_card(bus, self.current_date_str)

    def draw_bus_card(self, bus, date_str):
        card = ctk.CTkFrame(self.scroll_results, fg_color=("white", "gray17"), corner_radius=10, border_width=1, border_color="gray80")
        card.pack(fill="x", padx=5, pady=8)
        
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", padx=20, pady=15, fill="y")
        operator_lbl = ctk.CTkLabel(info_frame, text=bus["operator"], font=ctk.CTkFont(size=18, weight="bold"))
        operator_lbl.pack(anchor="w")
        type_lbl = ctk.CTkLabel(info_frame, text=bus["bus_type"], font=ctk.CTkFont(size=12), text_color="gray60")
        type_lbl.pack(anchor="w", pady=(2, 0))
        
        time_frame = ctk.CTkFrame(card, fg_color="transparent")
        time_frame.pack(side="left", padx=30, pady=15, fill="y")
        dep_lbl = ctk.CTkLabel(time_frame, text=bus["departure_time"], font=ctk.CTkFont(size=18, weight="bold"))
        dep_lbl.pack(anchor="w")
        
        mid_frame = ctk.CTkFrame(card, fg_color="transparent")
        mid_frame.pack(side="left", padx=5, pady=25)
        arrow_lbl = ctk.CTkLabel(mid_frame, text=f"── {bus['duration']} ──➔", font=ctk.CTkFont(size=13), text_color="gray60")
        arrow_lbl.pack()
        
        arr_frame = ctk.CTkFrame(card, fg_color="transparent")
        arr_frame.pack(side="left", padx=(5, 20), pady=15, fill="y")
        arr_lbl = ctk.CTkLabel(arr_frame, text=bus["arrival_time"], font=ctk.CTkFont(size=18, weight="bold"))
        arr_lbl.pack(anchor="w")
        
        action_frame = ctk.CTkFrame(card, fg_color="transparent")
        action_frame.pack(side="right", padx=20, pady=15, fill="y")
        price_lbl = ctk.CTkLabel(action_frame, text=f"₹ {bus['price']}", font=ctk.CTkFont(size=22, weight="bold"))
        price_lbl.pack(anchor="e", pady=(0, 5))
        seat_btn = ctk.CTkButton(action_frame, text="Select Seats", font=ctk.CTkFont(size=14, weight="bold"), fg_color="#e21a22", hover_color="#c1181e", width=120, height=35, command=lambda b=bus: self.open_seat_selection(b, date_str))
        seat_btn.pack(anchor="e")

    def open_seat_selection(self, bus_data, date_str):
        self.search_card.grid_remove()
        if getattr(self, "dual_pane", None):
            self.dual_pane.grid_remove()
            
        self.clear_flow_frame()
        
        from gui.booking_flows import SeatSelectionFrame
        self.flow_frame = SeatSelectionFrame(self.content_frame, self.username, bus_data, date_str,
                                             on_back=self.back_to_search_results,
                                             on_proceed=lambda seats, price: self.open_checkout(bus_data, seats, date_str, price))
        self.flow_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        
    def back_to_search_results(self):
        self.clear_flow_frame()
        self.search_card.grid()
        if getattr(self, "dual_pane", None):
            self.dual_pane.grid()
            
    def open_checkout(self, bus_data, selected_seats, date_str, total_price):
        self.clear_flow_frame()
        
        from gui.booking_flows import CheckoutFrame
        self.flow_frame = CheckoutFrame(self.content_frame, self.username, bus_data, selected_seats, date_str, total_price,
                                           on_back=lambda: self.open_seat_selection(bus_data, date_str),
                                           on_success=lambda bid, bdata, seats, price: self.show_booking_confirmation(bid, bdata, seats, price))
        self.flow_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")

    def show_booking_confirmation(self, booking_id, bus_data, selected_seats, total_price):
        self.clear_flow_frame()
        from gui.booking_flows import ConfirmationFrame
        self.flow_frame = ConfirmationFrame(self.content_frame, booking_id, bus_data, selected_seats, total_price,
                                            on_home=self.rebuild_search_dashboard)
        self.flow_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
