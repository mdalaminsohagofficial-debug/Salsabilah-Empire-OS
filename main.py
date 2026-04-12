import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import datetime

"""
==========================================================
SALSABILAH AMIN EMPIRES LTD. - POS SYSTEM (OS v1.0)
Developed by: MD. AL AMIN SOHAG
GitHub: https://github.com/SalsabilahEmpires/Salsabilah-Empire-OS
==========================================================
"""

class SalsabilahOS:
    def __init__(self, root):
        self.root = root
        self.root.title("Salsabilah Empire OS - Business Suite")
        self.root.geometry("1100x700")
        self.root.configure(bg="#f0f2f5")

        # ১. ডাটা ফাইল কনফিগারেশন
        self.product_file = "Products - SALSABILAH AMIN EMPIRES LTD..csv"
        self.sales_db = "Salsabilah_Sales_Log.csv"
        
        self.cart = []
        self.load_inventory()
        self.setup_ui()

    def load_inventory(self):
        """আপনার CSV ফাইল থেকে মালের লিস্ট এবং দাম লোড করা"""
        if os.path.exists(self.product_file):
            try:
                # আপনার ফাইলের ফরম্যাট অনুযায়ী ডাটা লোড
                self.inventory_df = pd.read_csv(self.product_file)
                # টাকার সিম্বল (৳) এবং কমা সরিয়ে ফ্লোট নাম্বারে রূপান্তর
                self.inventory_df['Selling Price'] = self.inventory_df['Selling Price'].str.replace('৳', '').str.replace(',', '').astype(float)
            except Exception as e:
                messagebox.showerror("System Error", f"ডাটা লোড করতে সমস্যা হয়েছে: {e}")
        else:
            # ফাইল না থাকলে ব্ল্যাঙ্ক ডাটাফ্রেম
            self.inventory_df = pd.DataFrame(columns=['Product', 'Selling Price'])

    def setup_ui(self):
        # হেডার ব্যানার
        header = tk.Frame(self.root, bg="#1a237e", height=100)
        header.pack(fill=tk.X)
        tk.Label(header, text="SALSABILAH AMIN EMPIRES LTD.", font=("Helvetica", 22, "bold"), fg="white", bg="#1a237e").pack(pady=25)

        # মেইন কন্টেইনার
        container = tk.Frame(self.root, bg="#f0f2f5")
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # বাম সাইড: কন্ট্রোল প্যানেল
        left_frame = tk.LabelFrame(container, text=" Sales Management ", font=("Arial", 12, "bold"), bg="white", padx=15, pady=15)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, width=400)

        tk.Label(left_frame, text="কাস্টমার নাম:", bg="white").pack(anchor="w")
        self.cust_entry = tk.Entry(left_frame, font=("Arial", 12), bd=2)
        self.cust_entry.pack(fill=tk.X, pady=10)

        tk.Label(left_frame, text="পণ্য নির্বাচন করুন:", bg="white").pack(anchor="w")
        product_list = self.inventory_df['Product'].tolist() if not self.inventory_df.empty else []
        self.prod_combo = ttk.Combobox(left_frame, values=product_list, font=("Arial", 11))
        self.prod_combo.pack(fill=tk.X, pady=10)

        tk.Button(left_frame, text="কার্টে যোগ করুন", command=self.add_to_cart, bg="#2e7d32", fg="white", font=("Arial", 11, "bold"), height=2).pack(fill=tk.X, pady=20)

        # ডান সাইড: ইনভয়েস প্রিভিউ
        right_frame = tk.LabelFrame(container, text=" Live Invoice ", font=("Arial", 12, "bold"), bg="white")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(20, 0))

        self.bill_area = tk.Text(right_frame, font=("Consolas", 10), bg="#fafafa")
        self.bill_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # নিচের বাটন
        btn_save = tk.Button(self.root, text="বিক্রয় সম্পন্ন করুন (Save Transaction)", command=self.save_sale, bg="#c62828", fg="white", font=("Arial", 12, "bold"), pady=15)
        btn_save.pack(fill=tk.X, side=tk.BOTTOM)

    def add_to_cart(self):
        selected_prod = self.prod_combo.get()
        if selected_prod in self.inventory_df['Product'].values:
            price = self.inventory_df[self.inventory_df['Product'] == selected_prod]['Selling Price'].values[0]
            self.cart.append({"Product": selected_prod, "Price": price})
            self.bill_area.insert(tk.END, f"{selected_prod[:35]:<35} | {price:>10.2f} TK\n")
        else:
            messagebox.showwarning("Warning", "সঠিক পণ্য নির্বাচন করুন!")

    def save_sale(self):
        """সেলস ডেটাবেসে তথ্য সেভ করা"""
        if not self.cart:
            messagebox.showwarning("Empty", "কার্ট খালি!")
            return
            
        total = sum(item['Price'] for item in self.cart)
        customer = self.cust_entry.get() or "Walk-In Customer"
        date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # ডাটাবেসে লেখার জন্য ফরম্যাট
        sale_entry = pd.DataFrame([{
            "Timestamp": date_now,
            "Customer": customer,
            "Amount": total,
            "Items": ", ".join([i['Product'] for i in self.cart])
        }])

        # ফাইল না থাকলে হেডারসহ সেভ হবে, থাকলে নিচে যোগ হবে
        header_needed = not os.path.exists(self.sales_db)
        sale_entry.to_csv(self.sales_db, mode='a', index=False, header=header_needed)

        messagebox.showinfo("Success", f"বিক্রয় সফল! মোট: {total:.2f} TK\nতথ্য ডাটাবেসে সংরক্ষিত হয়েছে।")
        self.clear_all()

    def clear_all(self):
        self.cart = []
        self.bill_area.delete(1.0, tk.END)
        self.cust_entry.delete(0, tk.END)
        self.prod_combo.set('')

if __name__ == "__main__":
    root = tk.Tk()
    app = SalsabilahOS(root)
    root.mainloop()
    
