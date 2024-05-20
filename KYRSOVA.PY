import tkinter as tk
from tkinter import ttk, messagebox
import csv

class EconomicTaskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Economic Task Application")
        
        self.data_files = ["sales.txt", "products.txt", "categories.txt"]
        self.sales_data = []
        self.product_data = []
        self.category_data = []
        
        self.read_files()
        self.create_widgets()

    def read_files(self):
        for file in self.data_files:
            with open(file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=' ')
                if file == "sales.txt":
                    self.sales_data = list(reader)
                elif file == "products.txt":
                    self.product_data = list(reader)
                elif file == "categories.txt":
                    self.category_data = list(reader)
    
    def create_widgets(self):
        self.tab_control = ttk.Notebook(self.root)

        self.tab1 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab1, text="Visualize Data")
        
        self.tab2 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab2, text="Summarize Data")
        
        self.tab3 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab3, text="Search Data")
        
        self.tab4 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab4, text="Filter Data")
        
        self.tab5 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab5, text="Save Data")
        
        self.tab6 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab6, text="Add Data")

        self.tab_control.pack(expand=1, fill="both")
        
        self.visualize_data(self.tab1)
        self.summarize_data(self.tab2)
        self.search_data(self.tab3)
        self.filter_data(self.tab4)
        self.save_data(self.tab5)
        self.add_data(self.tab6)

    def visualize_data(self, tab):
        sales_label = tk.Label(tab, text="Sales Data")
        sales_label.pack()
        
        sales_text = tk.Text(tab, height=10, width=50)
        sales_text.pack()
        for row in self.sales_data:
            sales_text.insert(tk.END, f"{row}\n")

        products_label = tk.Label(tab, text="Products Data")
        products_label.pack()
        
        products_text = tk.Text(tab, height=10, width=50)
        products_text.pack()
        for row in self.product_data:
            products_text.insert(tk.END, f"{row}\n")
            
        categories_label = tk.Label(tab, text="Categories Data")
        categories_label.pack()
        
        categories_text = tk.Text(tab, height=10, width=50)
        categories_text.pack()
        for row in self.category_data:
            categories_text.insert(tk.END, f"{row}\n")

    def summarize_data(self, tab):
        summary = self.get_summary()
        summary_label = tk.Label(tab, text="Summary")
        summary_label.pack()
        
        summary_text = tk.Text(tab, height=20, width=50)
        summary_text.pack()
        for key, value in summary.items():
            summary_text.insert(tk.END, f"{key}: {value}\n")
    
    def get_summary(self):
        summary = {}
        for row in self.sales_data:
            code = row[0]
            group = self.get_group_by_code(code)
            total = float(row[2]) * int(row[3])
            if group in summary:
                summary[group] += total
            else:
                summary[group] = total
        return summary

    def get_group_by_code(self, code):
        for row in self.product_data:
            if row[0] == code:
                group_code = row[2]
                for category in self.category_data:
                    if category[0] == group_code:
                        return category[1]
        return None
    
    def search_data(self, tab):
        search_label = tk.Label(tab, text="Enter Date (dd.mm.yyyy):")
        search_label.pack()
        
        self.search_entry = tk.Entry(tab)
        self.search_entry.pack()
        
        search_button = tk.Button(tab, text="Search", command=self.search)
        search_button.pack()
        
        self.search_text = tk.Text(tab, height=20, width=50)
        self.search_text.pack()
        
    def search(self):
        date = self.search_entry.get()
        results = []
        for row in self.sales_data:
            if row[1] == date:
                results.append(row)
        self.search_text.delete(1.0, tk.END)
        for result in results:
            self.search_text.insert(tk.END, f"{result}\n")
    
    def filter_data(self, tab):
        filter_label = tk.Label(tab, text="Enter Minimum Amount:")
        filter_label.pack()
        
        self.filter_entry = tk.Entry(tab)
        self.filter_entry.pack()
        
        filter_button = tk.Button(tab, text="Filter", command=self.filter)
        filter_button.pack()
        
        self.filter_text = tk.Text(tab, height=20, width=50)
        self.filter_text.pack()
    
    def filter(self):
        amount = float(self.filter_entry.get())
        results = []
        for row in self.sales_data:
            total = float(row[2]) * int(row[3])
            if total >= amount:
                results.append(row)
        self.filter_text.delete(1.0, tk.END)
        for result in results:
            self.filter_text.insert(tk.END, f"{result}\n")
    
    def save_data(self, tab):
        save_button = tk.Button(tab, text="Save Summary to File", command=self.save_to_file)
        save_button.pack()
    
    def save_to_file(self):
        summary = self.get_summary()
        with open("summary.txt", 'w', encoding='utf-8') as f:
            for key, value in summary.items():
                f.write(f"{key}: {value}\n")
        messagebox.showinfo("Info", "Summary saved to summary.txt")
    
    def add_data(self, tab):
        add_label = tk.Label(tab, text="Add Sale (code date price quantity):")
        add_label.pack()
        
        self.add_entry = tk.Entry(tab)
        self.add_entry.pack()
        
        add_button = tk.Button(tab, text="Add", command=self.add_sale)
        add_button.pack()
        
    def add_sale(self):
        sale = self.add_entry.get().split()
        self.sales_data.append(sale)
        messagebox.showinfo("Info", "Sale added")

if __name__ == "__main__":
    root = tk.Tk()
    app = EconomicTaskApp(root)
    root.mainloop()
