import tkinter as tk
from tinydb import TinyDB
import datetime
import time
import os
import sys
from tkinter import messagebox
import json
import uuid
import re
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tinydb import TinyDB, Query
import subprocess
from tkinter import simpledialog, messagebox
import math
from tkinter import font
from tkcolorpicker import askcolor
#from datetime import datetime, timedelta
from tkcalendar import Calendar



class window_biweekly(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.title("Budget App")
        self.every_two_weeks_btn = None
        self.configure(bg=f"{self.parent.get_settings('bg_color')}")
        #self.geometry(f"150x700")
        #self.resizable(True, False)
        self.options_buttons()
        self.check_previous_start_date()

    def options_buttons(self):
        if not os.path.exists("start_date.txt") and not os.path.exists("start_date_month.txt"):
            self.select_type_label = tk.Label(self, foreground=f"{self.parent.get_settings('other_txt_color')}", text= "Select Budget Type", font=("Arial", 16))
            self.select_type_label.pack()
            self.every_two_weeks_btn = tk.Button(self, text="Every two weeks", command=lambda: (self.select_type_label.destroy(), self.every_month_btn.destroy(), self.every_two_weeks_btn.destroy(), self.open_two_weeks_window()))
            self.every_two_weeks_btn.pack()
            self.every_month_btn = tk.Button(self, text="Every month", command=lambda: (self.every_month_btn.destroy(), self.every_two_weeks_btn.destroy(), self.open_monthly_window(), self.select_type_label.destroy()))
            self.every_month_btn.pack()

    def check_previous_start_date(self):
        if os.path.exists("start_date.txt"):
            self.display_reset_button()
            with open("start_date.txt", "r") as file:
                start_date = file.read()
                self.create_week_buttons(start_date)
    
        if os.path.exists("start_date_month.txt"):
            self.display_reset_button()
            with open("start_date_month.txt", "r") as file:
                start_date = file.read()
                self.create_month_buttons(start_date)
        
    def display_reset_button(self):
        self.confirm_btn = tk.Button(text= "CNF")
        self.select_type_label = tk.Button(text= "CNF")
        self.every_two_weeks_btn = tk.Button(text= "CNF")
        self.every_month_btn = tk.Button(text= "CNF")
        self.format_label = tk.Button(text= "CNF")
        self.start_date_entry = tk.Button(text= "CNF")
        self.select_type_label.destroy()
        self.every_two_weeks_btn.destroy()
        self.every_month_btn.destroy()
        self.confirm_btn.destroy()
        self.format_label.destroy()
        self.start_date_entry.destroy()
        self.select_budget_label = tk.Label(self, background=f"{self.parent.get_settings('bg_color')}", foreground=f"{self.parent.get_settings('other_txt_color')}", text= "Select Budget", font=("Arial", 16))
        self.select_budget_label.pack()
        self.reset_btn = tk.Button(self, text="RESET APP", command=self.reset_app)
        self.reset_btn.configure(bg=f"{self.parent.get_settings('btn_color')}", fg=f"{self.parent.get_settings('btn_txt_color')}")
        self.reset_btn.pack()

    def open_two_weeks_window(self):
        self.format_label = tk.Label(self, text="Enter Start date in MM-DD-YY format")
        self.format_label.pack()
        self.start_date_entry = tk.Entry(self)
        self.start_date_entry.pack()
        self.confirm_btn = tk.Button(self, text="Confirm", command=lambda: (self.create_week_buttons(self.start_date_entry.get()), self.display_reset_button))
        self.confirm_btn.pack()

    def create_week_buttons(self, start_date):
        self.add_year_button = tk.Button(self, text = "Add year", command= lambda: (self.add_buttons()))
        self.add_year_button.configure(bg=f"{self.parent.get_settings('btn_color')}", fg=f"{self.parent.get_settings('btn_txt_color')}")
        self.add_year_button.pack(side='bottom', anchor='center')
        _master = TinyDB("master_db.json")
        master_button_table = _master.table('button')
        years = master_button_table.all()[-1]["add_year"] * 27

        try:
            start_date = datetime.datetime.strptime(start_date, "%m-%d-%y")
            counter = 0
            current_frame = tk.Frame(self)
            current_frame.pack(side='left', padx=15, pady=15)
            for week in range(1, years):
                counter += 1
                if counter == 28:
                    counter = 1
                    current_frame = tk.Frame(self)
                    current_frame.configure(bg=f"{self.parent.get_settings('bg_color')}")
                    current_frame.pack(side='left', padx=15, pady=15)
                week_start_date = start_date + datetime.timedelta(days=(week - 1) * 14)
                week_end_date = week_start_date + datetime.timedelta(days=13)
                self.week_btn = tk.Button(
                    current_frame,
                    text=f"{week_start_date.strftime('%m-%d')} to {week_end_date.strftime('%m-%d-%y')}",
                    command=lambda w=week, ws=week_start_date, we=week_end_date: self.handle_week_selection(w, start_date, ws, we),
                )
                self.week_btn.configure(bg=f"{self.parent.get_settings('btn_color')}", fg=f"{self.parent.get_settings('btn_txt_color')}")
                self.week_btn.pack()

            self.save_start_date(start_date)
        except ValueError:
            messagebox.showerror(
                "Error",
                "Invalid date format. Please enter the date in MM-DD-YY format."
            )
        
    def handle_week_selection(self, week, start_date, week_start_date, week_end_date):
        filetxt = f"week{week}.json"
        with open("active_week.txt", "w") as file:
            file.write(filetxt)

        start_date_str = week_start_date.strftime("%m/%d")
        end_date_str = week_end_date.strftime("%m/%d/%y")
        selected_week = f"{start_date_str} to {end_date_str}"
        with open("title.txt", "w") as file:
            file.write(selected_week)

        self.parent.window.destroy()
        self.parent.__init__()
        self.parent.load_data()

    def open_monthly_window(self):
        self.format_label = tk.Label(self, text="Enter Start date in MM-DD-YY format")
        self.format_label.pack()
        self.start_date_entry = tk.Entry(self)
        self.start_date_entry.pack()
        self.confirm_btn = tk.Button(self, text="Confirm", command=lambda: (self.create_month_buttons(self.start_date_entry.get()), self.display_reset_button))
        self.confirm_btn.pack()

    def create_month_buttons(self, start_date):
        self.add_year_button = tk.Button(self, text = "Add year", command= lambda: (self.add_buttons()))
        self.add_year_button.configure(bg=f"{self.parent.get_settings('btn_color')}", fg=f"{self.parent.get_settings('btn_txt_color')}")
        self.add_year_button.pack(side='bottom', anchor='center')
        _master = TinyDB("master_db.json")
        master_button_table = _master.table('button')
        years = master_button_table.all()[-1]["add_year"] * 12
        try:
            start_date = datetime.datetime.strptime(start_date, "%m-%d-%y")
            counter = 0
            current_frame = tk.Frame(self)
            current_frame.pack(side='left', padx=15, pady=15)
            current_date = start_date
            for _ in range(years):  # Limit to 24 months
                counter += 1
                if counter == 13:
                    counter = 1
                    current_frame = tk.Frame(self)
                    current_frame.configure(bg=f"{self.parent.get_settings('bg_color')}")
                    current_frame.pack(side='left', padx=15, pady=15)
                month_end_date = current_date.replace(day=1) + datetime.timedelta(days=32)
                month_end_date = month_end_date.replace(day=1) - datetime.timedelta(days=1)

                self.month_btn = tk.Button(
                    current_frame,
                    text=f"{current_date.strftime('%B %y')}",
                    width=10, height=1,
                    command=lambda c_date=current_date: self.handle_month_selection(c_date, start_date),
                )
                self.month_btn.configure(bg=f"{self.parent.get_settings('btn_color')}", fg=f"{self.parent.get_settings('btn_txt_color')}")
                self.month_btn.pack()

                current_date += datetime.timedelta(days=32)
                current_date = current_date.replace(day=1)

            self.save_start_date_month(start_date)
        except ValueError:
            messagebox.showerror(
                "Error",
                "Invalid date format. Please enter the date in MM-DD-YY format.", parent=self.window
            )

    def handle_month_selection(self, selected_date, start_date):
        month = selected_date.month
        year = selected_date.year
        filetxt = f"month{month}_{year}.json"
        with open("active_week.txt", "w") as file:
            file.write(filetxt)
        month = selected_date.strftime("%B")
        year = selected_date.year
        selected_month = f"{month} {year}"
        with open("title.txt", "w") as file:
            file.write(selected_month)
        self.parent.window.destroy()
        self.parent.__init__()   
        self.parent.load_data()

    def save_start_date(self, start_date):
        with open("start_date.txt", "w") as file:
            file.write(start_date.strftime("%m-%d-%y"))

    def save_start_date_month(self, start_date):
        with open("start_date_month.txt", "w") as file:
            file.write(start_date.strftime("%m-%d-%y"))

    def reset_app(self):
        confirmation = messagebox.askyesno(
            "Reset App", "Are you sure you want to reset the app and clear the start date?"
        )
        if confirmation:
            try:
                os.remove("start_date.txt")
            except FileNotFoundError:
                pass
            try:
                os.remove("start_date_month.txt")
            except FileNotFoundError:
                pass
            try:
                os.remove("title.txt")
            except FileNotFoundError:
                pass
            with open("active_week.txt", "w") as file:
                file.write("test_database")
            self.parent.window.destroy()
            self.parent.__init__()
            directory = os.getcwd()
            for filename in os.listdir(directory):
                if (
                    filename.startswith(("week", "month", "Recurring"))
                    and filename.endswith(".json")
                ):
                    file_path = os.path.join(directory, filename)
                    os.remove(file_path)
                    print(f"Deleted file: {file_path}") 
            TinyDB("goals.json").drop_table('goals')
            self.clear_master_db("master_db.json")
            self.clear_master_db("change_master.json")
        
    def add_buttons(self):
        _master = TinyDB("master_db.json")
        master_button_table = _master.table('button')
        count = master_button_table.all()[-1]["add_year"]
        x = int(count) + 1
        master_button_table.insert({'add_year': x})
        self.destroy()
        self.parent.window_biweekly()

    def clear_master_db(self, db):
        dbc = TinyDB(db)
        income_table = dbc.table('income')
        expense_table = dbc.table('expense')
        savings_table = dbc.table('savings')
        button_table = dbc.table('button')
        settings_table = dbc.table ('settings')
        try:
            dbc.drop_table('savings')
            dbc.drop_table('income')
            dbc.drop_table('expense')
        except: pass
        try:
            dbc.drop_table('button')
            dbc.drop_table('settings')
        except: pass
        if 'income' not in dbc.tables():
            income_table.insert({'name': "123", 'amount': "123", 'date': "123"})
            income_table.remove(doc_ids=[1])
        if 'expense' not in dbc.tables():
            expense_table.insert({'name': "123", 'amount': "123", 'date': "123"})
            expense_table.remove(doc_ids=[1])
        if 'savings' not in dbc.tables():
            savings_table.insert({'name': "123", 'amount': "123", 'date': "123"})
            savings_table.remove(doc_ids=[1]) 
        if "settings" not in dbc.tables():
            settings_table.insert({'bg_color': "#DCEEFB"})
            settings_table.insert({'btn_txt_color': "#FBF5F5"})
            settings_table.insert({'btn_color': "#837979"})
            settings_table.insert({'other_txt_color': "#211D1D"})
            print("master.db updated")
        if "button" not in dbc.tables():
            button_table.insert({'add_year': 1})
        print("master.db updated")

        
class SecondWindow(tk.Toplevel):
    def __init__(self, parent, data):
        super().__init__(parent.window)
        self.title("Edit Window")
        self.top_level = parent.window
        self.parent = parent
        self.data = data 
        self.configure(bg=f"{self.parent.get_settings('bg_color')}")
        self.setup_gui()
        self.insert_data(self.split_data(data))
        self.protocol("WM_DELETE_WINDOW", self.on_window_close)

    def on_window_close(self):
            self.parent.add_item(self.split_data(self.data)["type"],self.entry_edit_name, self.entry_edit_amount, self.entry_edit_date)    
            self.parent.save_data()
            self.destroy()
            self.top_level.attributes('-alpha', 1.0)

    
    def setup_gui(self):
        self.edit_frame = tk.Frame(self)
        self.edit_frame.configure(bg=f"{self.parent.get_settings('bg_color')}")
        self.edit_frame.pack(side=tk.LEFT, padx=10, pady=10)
        self.label_edit_name = tk.Label(self.edit_frame, background=f"{self.parent.get_settings('bg_color')}", foreground=f"{self.parent.get_settings('other_txt_color')}", text="Name:")
        self.label_edit_name.pack(padx=3)
        self.entry_edit_name = tk.Entry(self.edit_frame)
        self.entry_edit_name.pack()
        self.label_edit_amount = tk.Label(self.edit_frame, background=f"{self.parent.get_settings('bg_color')}", foreground=f"{self.parent.get_settings('other_txt_color')}", text="Amount:")
        self.label_edit_amount.pack()
        self.entry_edit_amount = tk.Entry(self.edit_frame)
        self.entry_edit_amount.pack()
        self.label_edit_date = tk.Label(self.edit_frame, background=f"{self.parent.get_settings('bg_color')}", foreground=f"{self.parent.get_settings('other_txt_color')}", text="Date:")
        self.label_edit_date.pack()
        self.entry_edit_date = tk.Entry(self.edit_frame)
        self.entry_edit_date.pack()
        self.save_button = tk.Button(self.edit_frame, text="Save", command=lambda: (self.on_window_close()))
        self.save_button.configure(bg=f"{self.parent.get_settings('btn_color')}", fg=f"{self.parent.get_settings('btn_txt_color')}")
        self.save_button.pack()
        self.close_button = tk.Button(self.edit_frame, text="Close", command=self.on_window_close)
        self.close_button.configure(bg=f"{self.parent.get_settings('btn_color')}", fg=f"{self.parent.get_settings('btn_txt_color')}")
        self.close_button.pack()
        
        
    def split_data(self,data):
        type = (data[0])
        name = (data[1].split(",")[0].split(":")[0])
        amount = (data[1].split(",")[0].split(": $")[1].split(".")[0])
        date= (data[1].split(",")[1].split(": ")[1].split(", Date: ")[0])
        return {"type":type, "name":name, "amount":amount, "date":date}   
    
    def insert_data(self, data):
        self.entry_edit_name.insert(tk.END, data["name"])
        self.entry_edit_amount.insert(tk.END, data["amount"])
        self.entry_edit_date.insert(tk.END, data["date"])
        #self.parent.delete_items()


class Query_masterdb(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent.window)
        #self.main = FinancialManager() 
        self.master = TinyDB("master_db.json")
        self.master_income_table = self.master.table('income')
        self.master_expense_table = self.master.table('expense')
        self.master_savings_table = self.master.table('savings')
        self.parent = parent
        #self = self       

    def calculate_total_amount(self, data, start_date, end_date):
        total_amount = 0
        # Convert start and end dates to datetime objects for comparison
        start_date = datetime.datetime.strptime(start_date, "%m-%d-%y")
        end_date = datetime.datetime.strptime(end_date, "%m-%d-%y")

        for transaction in data:
            transaction_date = datetime.datetime.strptime(transaction["date"], "%m-%d-%y")

            # Check if the transaction date is within the specified range
            if start_date <= transaction_date <= end_date:
                total_amount += int(transaction["amount"])
        return total_amount 
    
    def calculate_total_financials(self, trans_type, start_date, end_date):
        income_table = self.master_income_table
        income_data = income_table.all()

        expense_table = self.master_expense_table
        expense_data = expense_table.all()

        savings_table = self.master_savings_table
        savings_data = savings_table.all()
        if trans_type == "total_income":
            trans_type = self.calculate_total_amount(income_data, start_date, end_date)
        if trans_type == "total_expense":
            trans_type = self.calculate_total_amount(expense_data, start_date, end_date)
        if trans_type == "total_savings":
            trans_type = self.calculate_total_amount(savings_data, start_date, end_date)

        return trans_type   


class LayoutEditor():
    def __init__(self, main_class):
        super().__init__()
        self.parent = main_class
        self.mdb_ = TinyDB("master_db.json")
        self.master_settings_table = self.mdb_.table('settings')
        self.new_window = tk.Toplevel(self.parent.window) 
        self.new_window.attributes("-topmost", True)
        self.gui_layout()
        #self.after(1000, self.parent.bring_to_top(self.new_window))

    def gui_layout(self):
        self.new_window.title("Layout Editor")
        width = 300
        height = 200
        screen_width = self.new_window.winfo_screenwidth()
        screen_height = self.new_window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 1)
        self.new_window.geometry(f"{width}x{height}+{x}+{y}")
        self.new_window.configure(bg=f"{self.parent.get_settings('bg_color')}")

        # Create buttons for layout editing
        self.button_color_ = tk.Button(self.new_window, text="Change Button Color", command=lambda: (self.open_color_picker("btn_color")))
        self.button_color_.configure(bg=f"{self.parent.get_settings('btn_color')}", fg=f"{self.parent.get_settings('btn_txt_color')}")
        self.button_color_.pack()
        self.button_text_color_ = tk.Button(self.new_window, text="Change Button text Color", command=lambda: self.open_color_picker('btn_txt_color'))
        self.button_text_color_.configure(bg=f"{self.parent.get_settings('btn_color')}", fg=f"{self.parent.get_settings('btn_txt_color')}")
        self.button_text_color_.pack()
        self.other_txt_color_ = tk.Button(self.new_window, text="Change Other Text Color", command=lambda: self.open_color_picker('other_txt_color'))
        self.other_txt_color_.configure(bg=f"{self.parent.get_settings('btn_color')}", fg=f"{self.parent.get_settings('btn_txt_color')}")
        self.other_txt_color_.pack()
        self.background_color_ = tk.Button(self.new_window, text="Change Background Color", command=lambda: self.open_color_picker('bg_color'))
        self.background_color_.configure(bg=f"{self.parent.get_settings('btn_color')}", fg=f"{self.parent.get_settings('btn_txt_color')}")
        self.background_color_.pack()

        
        
        #self.parent.bring_to_top(self)

    def open_color_picker(self, setting_key):
        color = askcolor()
        if color:
            selected_color = color[1]
            print(selected_color)
        query = Query()
        result = self.master_settings_table.get(query[setting_key] != None)
        if result:
            doc_id = result.doc_id
            new_setting = {setting_key: selected_color}
            self.master_settings_table.remove(doc_ids=[doc_id])
            self.master_settings_table.insert(new_setting)
            self.parent.window.destroy()
            self.parent.__init__()
            self.parent.load_data()
            self.parent.layoutwindow()
    
            
            
class FinancialManager:
    
    def __init__(self):
        self.active_database = self.get_active_database()
        self.db = TinyDB(self.active_database)
        self.income_table = self.db.table('income')
        self.expense_table = self.db.table('expense')
        self.savings_table = self.db.table('savings')
        self.resize_in_progress = False
        self.window = tk.Tk()
        self.qmdb = Query_masterdb
        self.master = TinyDB("master_db.json")
        self.master_income_table = self.master.table('income')
        self.master_expense_table = self.master.table('expense')
        self.master_savings_table = self.master.table('savings')
        self.master_settings_table = self.master.table('settings')
        if not os.path.exists("start_date.txt") and not os.path.exists("start_date_month.txt"):
            window_biweekly.clear_master_db(self, "master_db.json")
        self.bg_color = self.get_settings('bg_color')
        self.bg_color = self.get_settings('btn_txt_color')
        self.bg_color = self.get_settings('btn_color')
        self.force_start_date()
        self.check_and_create_tables()
        self.checkbox_var = tk.BooleanVar()
        self.checkbox_var.set(False)
        self.checkbox_goals_var = tk.BooleanVar()
        self.checkbox_goals_var.set(False)
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        if os.path.exists("start_date_month.txt") or os.path.exists("start_date.txt"):
            self.window.title(self.window_title())
            self.window.configure(bg=f"{self.get_settings('bg_color')}")
            self.window.geometry("1100x500")
            self.windowsize_count = 1
            self.window.bind("<Configure>", self.resize_handler)
            self.window.state("zoomed")
            self.setup_ui()
            self.resize_handler("")
            self.load_data()
            self.bind_buttons()
            self.goals_db = TinyDB("goals.json")  
            self.goals_table = self.goals_db.table('goals')

            
        self.income_ids = []
        self.expense_ids = []
        self.savings_ids= []

    def resize_handler(self, event):
        if self.window.state() == "zoomed" and self.resize_in_progress == False:
            self.resize_in_progress = True
            self.windowsize_count = 1
            print("large")
            self.large_window_ui()  
            
            
        if self.window.state() == "normal" and self.windowsize_count <= 1:
            self.resize_in_progress = False
            self.windowsize_count +=1
            print("small")
            try:
                self.checkbox_var.set(False)
                self.close_chart()
                self.pie_chart_frame.destroy()
            except:pass
            try:
                self.checkbox_goals_var.set(False)
                self.window_frame_goals.destroy()
            except:pass
            self.large_window_ui()
    
    def large_window_ui(self):
        if self.window.state() == "zoomed":
            font_size = ("Arial", 22)
            label_font = ("Arial", 18) 
            button_font = ("Arial", 18)
            text_font = ("Arial", 18)
            listbox_font = ("Arial", 16)
            smaller_text = ("Arial", 12)
            self.checkbox = tk.Checkbutton(self.window_frame, text="Pie Chart", variable=self.checkbox_var, command=self.checkbox_changed, foreground=self.get_settings('other_txt_color'), font=button_font)
            self.checkbox_goals = tk.Checkbutton(self.window_frame, text="Show Goals", variable=self.checkbox_goals_var, command=self.toggle_goals_listbox, foreground=self.get_settings('other_txt_color'), font=button_font)
            self.checkbox.pack(side='top')#place(x=585, y=125)
            self.checkbox_goals.pack(side='bottom')#place(x=675, y=125)
            self.window_frame.place(relx=0.638, rely=0.2)
            self.checkbox.configure(bg=self.get_settings('bg_color'), font=button_font)
            self.checkbox_goals.configure(bg=self.get_settings('bg_color'), font=button_font)
        else:
            font_size = ("Arial", 12)
            label_font = ("Arial", 10) 
            button_font = ("Arial", 10)
            text_font = ("Arial", 10)
            listbox_font = ("Arial", 10)
            smaller_text = ("Arial", 8)
            try:
                self.checkbox.destroy()
                self.checkbox_goals.destroy()
            except:pass
        self.font_size = font_size
        self.label_font = label_font
        self.button_font = button_font
        self.text_font = text_font
        self.listbox_font = listbox_font
        # Income
        self.income_frame.configure(bg=self.get_settings('bg_color'))
        self.income_label.configure(bg=self.get_settings('bg_color'), font=label_font)
        self.label_income_name.configure(bg=self.get_settings('bg_color'), font=label_font)
        self.label_income_amount.configure(bg=self.get_settings('bg_color'), font=label_font)
        self.label_income_date.configure(bg=self.get_settings('bg_color'), font=label_font)
        self.add_income_button.configure(bg=self.get_settings('btn_color'), fg=self.get_settings('btn_txt_color'), font=button_font)
        self.income_label.configure(fg=self.get_settings('other_txt_color'), font=label_font)
        self.entry_income_name.configure(font=text_font)
        self.entry_income_amount.configure(font=text_font)
        self.entry_income_date.configure(font=text_font)
        self.income_listbox.configure(font=listbox_font)

        # Expense
        self.expense_frame.configure(bg=self.get_settings('bg_color'))
        self.expense_label.configure(bg=self.get_settings('bg_color'), font=label_font)
        self.label_expense_name.configure(bg=self.get_settings('bg_color'), font=label_font)
        self.label_expense_amount.configure(bg=self.get_settings('bg_color'), font=label_font)
        self.label_expense_date.configure(bg=self.get_settings('bg_color'), font=label_font)
        self.add_expense_button.configure(bg=self.get_settings('btn_color'), fg=self.get_settings('btn_txt_color'), font=button_font)
        self.delete_selected_button.configure(bg=self.get_settings('btn_color'), fg=self.get_settings('btn_txt_color'), font=button_font)
        self.expense_label.configure(fg=self.get_settings('other_txt_color'), font=label_font)
        self.entry_expense_name.configure(font=text_font)
        self.entry_expense_amount.configure(font=text_font)
        self.entry_expense_date.configure(font=text_font)
        self.expense_listbox.configure(font=listbox_font)

        # Savings
        self.savings_frame.configure(bg=self.get_settings('bg_color'))
        self.savings_label.configure(bg=self.get_settings('bg_color'), font=label_font)
        self.label_savings_name.configure(bg=self.get_settings('bg_color'), font=label_font)
        self.label_savings_amount.configure(bg=self.get_settings('bg_color'), font=label_font)
        self.label_savings_date.configure(bg=self.get_settings('bg_color'), font=label_font)
        self.add_savings_button.configure(bg=self.get_settings('btn_color'), fg=self.get_settings('btn_txt_color'), font=button_font)
        self.delete_edit_button.configure(bg=self.get_settings('btn_color'), fg=self.get_settings('btn_txt_color'), font=button_font)
        self.savings_label.configure(fg=self.get_settings('other_txt_color'), font=label_font)
        self.entry_savings_name.configure(font=text_font)
        self.entry_savings_amount.configure(font=text_font)
        self.entry_savings_date.configure(font=text_font)
        self.savings_listbox.configure(font=listbox_font)

        # Totals
        self.total_frame.configure(bg=self.get_settings('bg_color'))
        self.total_income_label.configure(bg=self.get_settings('bg_color'), fg=self.get_settings('other_txt_color'), font=label_font)
        self.total_expense_label.configure(bg=self.get_settings('bg_color'), fg=self.get_settings('other_txt_color'), font=label_font)
        self.total_savings_label.configure(bg=self.get_settings('bg_color'), fg=self.get_settings('other_txt_color'), font=label_font)
        self.remaining_amount_label.configure(bg=self.get_settings('bg_color'), fg=self.get_settings('other_txt_color'), font=label_font)

        # Misc Buttons
        self.misc_left_frame.configure(bg=self.get_settings('bg_color'))
        self.misc_right_frame.configure(bg=self.get_settings('bg_color'))
        self.window_frame.configure(bg=self.get_settings('bg_color'))
        self.recurring_one_button.configure(bg=self.get_settings('btn_color'), fg=self.get_settings('btn_txt_color'), font=button_font)
        self.edit_recurring_one_button.configure(bg=self.get_settings('btn_color'), fg=self.get_settings('btn_txt_color'), font=button_font)
        self.recurring_two_button.configure(bg=self.get_settings('btn_color'), fg=self.get_settings('btn_txt_color'), font=button_font)
        self.edit_recurring_two_button.configure(bg=self.get_settings('btn_color'), fg=self.get_settings('btn_txt_color'), font=button_font)
        self.two_week_button.configure(bg=self.get_settings('btn_color'), fg=self.get_settings('btn_txt_color'), font=font_size)
        self.save_button.configure(bg=self.get_settings('btn_color'), fg=self.get_settings('btn_txt_color'), font=button_font)
        self.layout_button.configure(bg=self.get_settings('btn_color'), fg=self.get_settings('btn_txt_color'), font=smaller_text)

    def setup_ui(self):
     
        font_size = ("Arial", 12)
        label_font = ("Arial", 10) 
        button_font = ("Arial", 10)
        text_font = ("Arial", 10)
        listbox_font = ("Arial", 10)
        self.income_frame = tk.Frame(self.window)
        self.window_frame = tk.Frame(self.window)
        self.income_label = tk.Label(self.income_frame, text="Income", foreground=self.get_settings('other_txt_color'), font=label_font)
        self.label_income_name = tk.Label(self.income_frame, text="Name:", foreground=self.get_settings('other_txt_color'), font=label_font)
        self.entry_income_name = tk.Entry(self.income_frame, font=text_font)
        self.label_income_amount = tk.Label(self.income_frame, text="Amount:", foreground=self.get_settings('other_txt_color'), font=label_font)
        self.entry_income_amount = tk.Entry(self.income_frame, font=text_font)
        self.label_income_date = tk.Label(self.income_frame, text="Date:", foreground=self.get_settings('other_txt_color'), font=label_font)
        self.entry_income_date = tk.Entry(self.income_frame, font=text_font)
        self.add_income_button = tk.Button(self.income_frame, text="Add Income", command=lambda: (self.add_item('income', self.entry_income_name, self.entry_income_amount, self.entry_income_date), self.load_data()), font=button_font)
        self.income_listbox = tk.Listbox(self.income_frame, selectmode='extended', width=33, height=9, font=listbox_font)

        self.expense_frame = tk.Frame(self.window)
        self.expense_label = tk.Label(self.expense_frame, text="Expenses", foreground=self.get_settings('other_txt_color'), font=label_font)
        self.label_expense_name = tk.Label(self.expense_frame, text="Name:", foreground=self.get_settings('other_txt_color'), font=label_font)
        self.entry_expense_name = tk.Entry(self.expense_frame, font=text_font)
        self.label_expense_amount = tk.Label(self.expense_frame, text="Amount:", foreground=self.get_settings('other_txt_color'), font=label_font)
        self.entry_expense_amount = tk.Entry(self.expense_frame, font=text_font)
        self.label_expense_date = tk.Label(self.expense_frame, text="Date:", foreground=self.get_settings('other_txt_color'), font=label_font)
        self.entry_expense_date = tk.Entry(self.expense_frame, font=text_font)
        self.add_expense_button = tk.Button(self.expense_frame, text="Add Expense", command=lambda: (self.add_item('expense', self.entry_expense_name, self.entry_expense_amount, self.entry_expense_date), self.load_data()), font=button_font)
        self.expense_listbox = tk.Listbox(self.expense_frame, selectmode='extended', width=33, height=15, font=listbox_font)

        self.savings_frame = tk.Frame(self.window)
        self.savings_label = tk.Label(self.savings_frame, text="Savings", foreground=self.get_settings('other_txt_color'), font=label_font)
        self.label_savings_name = tk.Label(self.savings_frame, text="Name:", foreground=self.get_settings('other_txt_color'), font=label_font)
        self.entry_savings_name = tk.Entry(self.savings_frame, font=text_font)
        self.label_savings_amount = tk.Label(self.savings_frame, text="Amount:", foreground=self.get_settings('other_txt_color'), font=label_font)
        self.entry_savings_amount = tk.Entry(self.savings_frame, font=text_font)
        self.label_savings_date = tk.Label(self.savings_frame, text="Date:", foreground=self.get_settings('other_txt_color'), font=label_font)
        self.entry_savings_date = tk.Entry(self.savings_frame, font=text_font)
        self.add_savings_button = tk.Button(self.savings_frame, text="Add Savings", command=lambda: (self.add_savings_goal(), self.add_item('savings', self.entry_savings_name, self.entry_savings_amount, self.entry_savings_date), self.load_data()), font=button_font)
        self.savings_listbox = tk.Listbox(self.savings_frame, selectmode='extended', width=33, height=9, font=listbox_font)

        self.total_frame = tk.Frame(self.savings_frame)
        self.total_income_label = tk.Label(self.total_frame, text="Total Income: $0.00", foreground=self.get_settings('other_txt_color'), font=label_font)
        self.total_expense_label = tk.Label(self.total_frame, text="Total Expenses: $0.00", foreground=self.get_settings('other_txt_color'), font=label_font)
        self.total_savings_label = tk.Label(self.total_frame, text="Total Savings: $0.00", foreground=self.get_settings('other_txt_color'), font=label_font)
        self.remaining_amount_label = tk.Label(self.total_frame, text="Remaining Amount: $0.00", foreground=self.get_settings('other_txt_color'), font=label_font)

        self.delete_selected_button = tk.Button(self.income_frame, text="Delete Selected", command=lambda: (self.delete_items(), self.load_data()), font=button_font)
        self.delete_edit_button = tk.Button(self.income_frame, text="Edit Selected", command=lambda: (self.open_second_window(), self.delete_items()), font=button_font)
        self.save_button = tk.Button(self.income_frame, text="Save Data", command=self.save_data, font=button_font)
        self.misc_right_frame = tk.Frame(self.window)
        self.misc_left_frame = tk.Frame(self.window)
        self.recurring_one_button = tk.Button(self.misc_right_frame, text="Add Recurring One", command=lambda: self.recurring_add("Recurring_One.json"), font=button_font)
        self.edit_recurring_one_button = tk.Button(self.misc_left_frame, text="Edit Recurring One", command=lambda: self.recurring_edit("Recurring_One"), font=button_font)
        self.recurring_two_button = tk.Button(self.misc_right_frame, text="Add Recurring Two", command=lambda: self.recurring_add("Recurring_Two.json"), font=button_font)
        self.edit_recurring_two_button = tk.Button(self.misc_left_frame, text="Edit Recurring Two", command=lambda: self.recurring_edit("Recurring_Two"), font=button_font)
        self.two_week_button = tk.Button(self.window, text=self.window_title(), command=self.window_biweekly, font=font_size, width=30)
        self.layout_button = tk.Button(self.window, text="Edit Window Layout", command=lambda: LayoutEditor(self), font=("Arial", 12))


        self.two_week_button.pack(side='top', anchor='center')#place(x=585, y=10, width=95, height=25)
        self.income_frame.pack(side="left", padx=5, pady=5, anchor='n')#(x=10, y=10)
        self.income_label.pack()
        self.label_income_name.pack()
        self.entry_income_name.pack()
        self.label_income_amount.pack()
        self.entry_income_amount.pack()
        self.label_income_date.pack()
        self.entry_income_date.pack()
        self.add_income_button.pack(pady=5)
        self.income_listbox.pack(fill="both", expand=True)
        self.delete_edit_button.pack(pady=5)#place(x=63, y=365, width=90, height=25)
        self.delete_selected_button.pack(pady=5)#place(x=63, y=335, width=90, height=25)
        self.save_button.pack(padx=5)#place(x=63, y=395, width=90, height=25)

        self.expense_frame.pack(side="left", padx=5, pady=5, anchor='n')#(x=200, y=10)
        self.expense_label.pack()
        self.label_expense_name.pack()
        self.entry_expense_name.pack()
        self.label_expense_amount.pack()
        self.entry_expense_amount.pack()
        self.label_expense_date.pack()
        self.entry_expense_date.pack()
        self.add_expense_button.pack(pady=5)
        self.expense_listbox.pack(fill="both", expand=True)

        self.savings_frame.pack(side="left", padx=5, pady=5, anchor='n')#(x=390, y=10)
        self.savings_label.pack()
        self.label_savings_name.pack()
        self.entry_savings_name.pack()
        self.label_savings_amount.pack()
        self.entry_savings_amount.pack()
        self.label_savings_date.pack()
        self.entry_savings_date.pack()
        self.add_savings_button.pack(pady=5)
        self.savings_listbox.pack(fill="both", expand=True)

        self.total_frame.pack(anchor='s')#place(x=392, y=340, width=180, height=90)
        self.total_income_label.pack()
        self.total_expense_label.pack()
        self.total_savings_label.pack()
        self.remaining_amount_label.pack()
        self.update_total_labels()
        self.misc_right_frame.pack(side='left', anchor='n', pady=50)
        self.misc_left_frame.pack(side='left', anchor='n', pady=50)
        self.recurring_one_button.pack(padx=2, pady=2)#place(x=585, y=65)
        self.edit_recurring_one_button.pack(padx=2, pady=2)#place(x=715, y=65)
        self.recurring_two_button.pack(padx=2, pady=2)#place(x=585, y=95)
        self.edit_recurring_two_button.pack(padx=2, pady=2)#place(x=715, y=95)
        self.layout_button.place(relx=0.99, y=10,anchor="ne")
        #tk.Label(self.window_frame_goals, text="Hello World").pack()
        date_to_pop = datetime.datetime.now().strftime("%m-%d-%y")
        if len(self.entry_income_date.get()) < 1:
            self.entry_income_date.insert(0 ,date_to_pop)
        if len(self.entry_expense_date.get()) < 1:
            self.entry_expense_date.insert(0 ,date_to_pop)
        if len(self.entry_savings_date.get()) < 1:
            self.entry_savings_date.insert(0 ,date_to_pop)

    def layoutwindow(self):
        
        LayoutEditor(self)

    def get_settings(self, section):
        query = Query()
        result = self.master_settings_table.search(query[section].exists())

        if result:
            section_value = result[0].get(section)
            return f"{section_value}"
        else:
            print("Section not found in settings table.")

    def qmdb_total_by_type_date_start_end(self, trans_type, start_date, end_date):
        #total_income, total_expense,
        trans_type = self.qmdb().calculate_total_financials(trans_type, start_date, end_date)
        return trans_type
    
    def toggle_goals_listbox(self, *args):
        if self.checkbox_goals_var.get():
            self.populate_goals_listbox()
        else:
            self.goals_listbox.destroy()
            self.goals_label.destroy()
            self.window_frame_goals.destroy()
            #self.window.geometry("986x444")

    def populate_goals_listbox(self):
        self.window_frame_goals = tk.Frame(self.window)
        self.window_frame_goals.place(relx=.633, rely=.95, anchor='se')
        self.goals_frame = tk.Frame(self.window_frame_goals)
        self.goals_frame.configure(bg=f"{self.get_settings('bg_color')}")
        self.goals_frame.pack()#place(x=585, y=175)
        self.goals_listbox = tk.Listbox(self.goals_frame)
        width = self.goals_listbox.size()
        height = self.goals_listbox.size()
        self.goals_listbox.config(width=width, height=height)
        self.goals_label = tk.Label(self.goals_frame, background=f"{self.get_settings('bg_color')}" ,foreground=f"{self.get_settings('other_txt_color')}", text="Goals", font=self.text_font)
        self.goals_label.pack(pady=1)
        self.goals_listbox.pack()
        self.goals_listbox.configure(font=self.listbox_font)
        self.goals_listbox.delete(0, tk.END)
   
        for goal in self.goals_table.all():
            name = goal['name']
            total_amount = round(int(goal['total_amount']))#goal['total_amount']
            already_saved = round(int(float(goal['already_saved'])))#goal['already_saved']
            amount_saved = self.get_total_savings_amount(name) + already_saved
            amount_in_budget = self.get_total_savings_amount(name)
            remaining_amount = total_amount - amount_saved
            first_date = self.get_first_date(name)
            current_date = datetime.datetime.now().strftime("%m-%d-%y")
            days_passed = self.calculate_time_passed("day", first_date, current_date)
            months_passed = self.calculate_time_passed("month", first_date, current_date)
            average = amount_in_budget / days_passed
            average_month = amount_in_budget / months_passed
            average_per_month = int(round(average_month))
            days_to_complete = remaining_amount / average
            rounded_number = int(round(days_to_complete))
            estimated_completion_date = datetime.datetime.now().date() + datetime.timedelta(days=int(rounded_number))
            formatted_completion_date = estimated_completion_date.strftime("%m-%d-%y")
            self.goals_listbox.insert(tk.END, f"{name}, Target: ${total_amount}, Saved: ${amount_saved}, Completion: {formatted_completion_date}, Average per Month:${average_per_month}, Remaining: ${remaining_amount}")
            self.goals_listbox.insert(tk.END, "") 

    def get_total_savings_amount(self, goal_name):
        self.master = TinyDB("master_db.json")
        self.master_income_table = self.master.table('income')
        self.master_expense_table = self.master.table('expense')
        self.master_savings_table = self.master.table('savings')
        query = Query()
        pattern = re.compile(re.escape(goal_name), re.IGNORECASE)
        entries = self.master_savings_table.search(query.name.matches(pattern))
        total_amount = sum(int(entry['amount']) for entry in entries)
        return total_amount

    def get_first_date(self, goal_name):
        with open('master_db.json', 'r') as json_file:
            data = json.load(json_file)
        earliest_date = None
        earliest_item = None
        for key, item in data["savings"].items():
            name = item["name"].lower() 
            if name == goal_name.lower():
                item_date = datetime.datetime.strptime(item["date"], "%m-%d-%y")
                if earliest_date is None or item_date < earliest_date:
                    earliest_date = item_date
                    earliest_item = item
        if earliest_item:
            return(earliest_item["date"])
        else:
            return

    def calculate_time_passed(self, day_week_month, first_date, current_date):
        first_date_obj = datetime.datetime.strptime(first_date, "%m-%d-%y")
        second_date_obj = datetime.datetime.strptime(current_date, "%m-%d-%y")
        date_difference = second_date_obj - first_date_obj
        if day_week_month == "day":
            day_week_month = date_difference.days 
        if day_week_month== "week":
            day_week_month = date_difference.days // 7
        if day_week_month== "month":
            day_week_month = date_difference.days / 30
        day_week_month = math.ceil(day_week_month)
        return day_week_month
    
    def add_savings_goal(self):
        savings_goal_name = self.entry_savings_name.get()
        if self.check_savings_goal_exists(savings_goal_name):
                return
        result = messagebox.askquestion("Savings Goal", "Is this a savings goal?", parent=self.window)
        if result == "yes":
            savings_goal_name = self.entry_savings_name.get()
            if self.check_savings_goal_exists(savings_goal_name):
                messagebox.showinfo("Savings Goal", "Savings goal already exists!", parent=self.window)
                return
            pre_saved_amount = simpledialog.askfloat("pre_saved_amount", f"Amount already saved for {savings_goal_name} not entered into Budget App:")
            time.sleep(.01)
            #self.window.attributes("-topmost", False)
            ask_frame = tk.Toplevel(self.window_frame)
            ask_frame.title("Total Amount")
            width = 300
            height = 100
            screen_width = ask_frame.winfo_screenwidth()
            screen_height = ask_frame.winfo_screenheight()
            x = (screen_width // 2) - (width // 2)
            y = (screen_height // 2) - (height // 2)
            ask_frame.geometry(f"{width}x{height}+{x}+{y}")
            test_test = tk.Frame(ask_frame)
            label_ask = tk.Label(test_test, text=f"Total amount to be saved for {savings_goal_name}:")
            entry_ask = tk.Entry(test_test)
            button_ask = tk.Button(ask_frame, text= "Confirm", command=lambda: (self.add_savings_goal_to_database(savings_goal_name, entry_ask.get(), pre_saved_amount), ask_frame.destroy()))
            cancel_button = tk.Button(ask_frame, text= "Cancel", command=lambda: (ask_frame.destroy()))
            test_test.pack(padx=5, pady=5)
            label_ask.pack(padx=5, pady=5)
            entry_ask.pack(padx=5, pady=5)
            total_amount= entry_ask.get()
            button_ask.configure(bg=f"{self.get_settings('btn_color')}", fg=f"{self.get_settings('btn_txt_color')}")
            cancel_button.configure(bg=f"{self.get_settings('btn_color')}", fg=f"{self.get_settings('btn_txt_color')}")
            button_ask.place(x=85, y=70)
            cancel_button.place(x=155, y=70)
        else:
            try:
                ask_frame.destroy()
            except: return

    def check_savings_goal_exists(self, savings_goal_name):
        pattern = re.compile(re.escape(savings_goal_name), re.IGNORECASE)
        Goal = Query()
        result = self.goals_table.search(Goal.name.matches(pattern))
        return bool(result)
    
    def add_savings_goal_to_database(self, savings_goal_name, total_amount, pre_saved_amount):
        if len(total_amount) >= 1:
            self.goals_table.insert({'name': savings_goal_name, 'total_amount': total_amount, 'already_saved': pre_saved_amount})

    def on_close(self):
        try:
            self.close_chart()
        except:
            pass
        self.window.destroy()
       
    def checkbox_changed(self):
        if self.checkbox_var.get():
            self.pie_chart_frame = tk.Frame(self.window_frame)
            current_pie_chart = tk.Button(self.pie_chart_frame, text="Current Budget", command= lambda: (self.close_chart(), self.display_pie_chart()))
            pie_chart_three = tk.Button(self.pie_chart_frame, text="Last Three Months", command= lambda: (self.close_chart(), self.display_pie_chart_date(3, 1, 1)))
            pie_chart_six = tk.Button(self.pie_chart_frame, text="Last Six Months", command= lambda: (self.close_chart(), self.display_pie_chart_date(6, 1, 1)))
            pie_chart_year = tk.Button(self.pie_chart_frame, text="Last Year", command= lambda: (self.close_chart(), self.display_pie_chart_date(12, 1, 1)))
            pie_chart_custom = tk.Button(self.pie_chart_frame, text="Custom Date Range", command= lambda: (self.close_chart(), self.start_end_date()))
            self.pie_chart_frame.configure(bg=f"{self.get_settings('bg_color')}")
            self.pie_chart_frame.pack()
            current_pie_chart.configure(bg=f"{self.get_settings('btn_color')}", font=("Arial", 10), fg=f"{self.get_settings('btn_txt_color')}")
            pie_chart_three.configure(bg=f"{self.get_settings('btn_color')}", font=("Arial", 10), fg=f"{self.get_settings('btn_txt_color')}")
            pie_chart_six.configure(bg=f"{self.get_settings('btn_color')}", font=("Arial", 10), fg=f"{self.get_settings('btn_txt_color')}")
            pie_chart_year.configure(bg=f"{self.get_settings('btn_color')}", font=("Arial", 10), fg=f"{self.get_settings('btn_txt_color')}")
            pie_chart_custom.configure(bg=f"{self.get_settings('btn_color')}", font=("Arial", 10), fg=f"{self.get_settings('btn_txt_color')}")
            current_pie_chart.pack(anchor="nw", side ="left", padx=5, pady=2)
            pie_chart_three.pack(anchor="nw", side ="left", padx=5, pady=2)
            pie_chart_six.pack(anchor="nw", side ="left", padx=5, pady=2)
            pie_chart_year.pack(anchor="nw", side ="left", padx=5, pady=2)
            pie_chart_custom.pack(anchor="nw", side ="left", padx=5, pady=2)
        else:
            self.pie_chart_frame.destroy()
            self.close_chart()

        try:
            self.start_end_frame.destroy()
        except:
            pass

    def start_end_date(self):
        self.start_end_frame = tk.Frame(self.window_frame)
        self.start_end_frame.pack()#place(y=200, x=780)
        pie_start_date_l = tk.Label(self.start_end_frame, text="Enter start date(MM-DD-YY)", font=("Arial", 14))
        pie_start_date_l.pack(padx=2, pady=2)
        self.pie_start_date = tk.Entry(self.start_end_frame)
        self.pie_start_date.pack(padx=2, pady=2)
        pie_end_date_l = tk.Label(self.start_end_frame, text="Enter end date(MM-DD-YY)", font=("Arial", 14))
        pie_end_date_l.pack(padx=2, pady=2)
        self.pie_end_date = tk.Entry(self.start_end_frame, text="Enter end date(MM-DD-YY)", font=("Arial", 14))
        self.pie_end_date.pack(padx=2, pady=2)
        create_chart_btn = tk.Button(self.start_end_frame, text="Create Chart", command= lambda: (self.btn_create_chart()))
        create_chart_btn.configure(bg=f"{self.get_settings('btn_color')}", fg=f"{self.get_settings('btn_txt_color')}", font=("Arial", 14))
        create_chart_btn.pack(padx=2, pady=2)

    def btn_create_chart(self):
        try:
            self.display_pie_chart_date(1, self.pie_start_date.get(), self.pie_end_date.get()) 
            self.start_end_frame.destroy()    
        except:  
            messagebox.showinfo("ERROR", "Date must be it MM-DD-YY format", parent=self.window)
            
    def display_pie_chart_date(self, number_of_months, start_date, end_date):
        # Step 1: Parse the JSON data
        with open('master_db.json', 'r') as file:
            data = json.load(file)
        #number_of_months = 3
        plt.interactive(False)
        n = number_of_months *30
        try:
            nstart_date = datetime.datetime.strptime(start_date, "%m-%d-%y")
            nend_date = datetime.datetime.strptime(end_date, "%m-%d-%y")
            tend_date = nend_date.strftime("%m-%d-%y")
            tstart_date = nstart_date.strftime("%m-%d-%y")
        except: 
            pass
        current_date = datetime.datetime.now()
        new_month = current_date.replace(day=15) - datetime.timedelta(days=n)
        __months_ago = new_month.replace(day=current_date.day)
        formatted_date = __months_ago.strftime("%m-%d-%y")
        formatted_start = current_date.strftime("%m-%d-%y")
        if number_of_months != 1:
            filtered_income = {
                key: value
                for key, value in data['income'].items()
                if value['date'] != 'NA' and datetime.datetime.strptime(value['date'], "%m-%d-%y") >= __months_ago
            }
        if start_date != 1:
            filtered_income = {
                key: value
                for key, value in data['income'].items()
                if value['date'] != 'NA' and datetime.datetime.strptime(value['date'], "%m-%d-%y") >= nstart_date and datetime.datetime.strptime(value['date'], "%m-%d-%y") <= nend_date
            }
        if number_of_months != 1:
            filtered_expense = {
                key: value
                for key, value in data['expense'].items()
                if value['date'] != 'NA' and datetime.datetime.strptime(value['date'], "%m-%d-%y") >= __months_ago
            }
        if start_date != 1:
            filtered_expense = {
                key: value
                for key, value in data['expense'].items()
                if value['date'] != 'NA' and datetime.datetime.strptime(value['date'], "%m-%d-%y") >= nstart_date and datetime.datetime.strptime(value['date'], "%m-%d-%y") <= nend_date
            }
        if number_of_months != 1:
            filtered_savings = {
                key: value
                for key, value in data['savings'].items()
                if value['date'] != 'NA' and datetime.datetime.strptime(value['date'], "%m-%d-%y") >= __months_ago
            }
        if start_date != 1:
            filtered_savings = {
                key: value
                for key, value in data['savings'].items()
                if value['date'] != 'NA' and datetime.datetime.strptime(value['date'], "%m-%d-%y") >= nstart_date and datetime.datetime.strptime(value['date'], "%m-%d-%y") <= nend_date
            }
        combined_income = {}
        for key, value in filtered_income.items():
            name = value['name']
            amount = float(value['amount'])
            if name in combined_income:
                combined_income[name] += amount
            else:
                combined_income[name] = amount
        combined_expense = {}
        for key, value in filtered_expense.items():
            name = value['name']
            amount = float(value['amount'])
            if name in combined_expense:
                combined_expense[name] += amount
            else:
                combined_expense[name] = amount
        combined_savings = {}
        for key, value in filtered_savings.items():
            name = value['name']
            amount = float(value['amount'])
            if name in combined_savings:
                combined_savings[name] += amount
            else:
                combined_savings[name] = amount
        income_names = list(combined_income.keys())
        income_amounts = list(combined_income.values())
        
        expense_names = list(combined_expense.keys())
        expense_amounts = list(combined_expense.values())
        
        savings_names = list(combined_savings.keys())
        savings_amounts = list(combined_savings.values())
        
        total_income = sum(income_amounts)
        total_expense = sum(expense_amounts)
        total_savings = sum(savings_amounts)
        total = total_expense + total_savings
        remaining = total_income - total
        remaining_name = ("Remaining")
       
        income_percentages = [amount / total_income * 100 for amount in income_amounts]
        expense_percentages = [amount / total_income * 100 for amount in expense_amounts]
        savings_percentages = [amount / total_income * 100 for amount in savings_amounts]
        all_names = expense_names + savings_names + [remaining_name]
        all_amounts = expense_amounts + savings_amounts + [remaining]
        all_percentages = expense_percentages + savings_percentages
        label_texts = all_names
        amount_texts = [f'${amount:.2f}' for amount in all_amounts]
        combined_texts = [f'{label}\n{amount}' for label, amount in zip(label_texts, amount_texts)]
        self.fig = plt.figure(figsize=(7, 7))
        ax = self.fig.add_subplot(111)
        wedges, text_labels, autotexts = ax.pie(all_amounts, labels=combined_texts, autopct='%1.1f%%', startangle=90, counterclock=False, textprops={'color': f"{self.get_settings('other_txt_color')}"}, wedgeprops={'linewidth': .5, 'edgecolor': 'black'})
        if number_of_months != 1:
            title = f"{formatted_date} to {formatted_start}"
        if start_date != 1:
            title = f"{tstart_date} to {tend_date}"
        ax.axis('equal')
        ax.set_aspect('1.1')
        ax.set_title(title, color=f"{self.get_settings('other_txt_color')}", y=1.08)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window_frame)
        self.canvas.draw()
        plt.gcf().set_facecolor(f"{self.get_settings('bg_color')}")
        self.canvas.get_tk_widget().pack()#place(x=585, y=195)
        self.pie_chart_summery_frame = tk.Frame(self.window_frame)
        self.pie_chart_summery_frame.configure(bg=f"{self.get_settings('bg_color')}")
        total_sav_label = tk.Label(self.pie_chart_summery_frame, background=f"{self.get_settings('bg_color')}", foreground=f"{self.get_settings('other_txt_color')}", font=font.Font(size=11), text =f"Savings: ${total_savings:.2f} ({total_savings / total_income * 100:.1f}%)")
        total_exp_label = tk.Label(self.pie_chart_summery_frame, background=f"{self.get_settings('bg_color')}", foreground=f"{self.get_settings('other_txt_color')}", font=font.Font(size=11), text =f"Expense: ${total_expense:.2f} ({total_expense / total_income * 100:.1f}%)")
        total_inc_label = tk.Label(self.pie_chart_summery_frame, background=f"{self.get_settings('bg_color')}", foreground=f"{self.get_settings('other_txt_color')}", font=font.Font(size=11), text =f"Total Income: ${total_income:.2f}")
        total_rem_label = tk.Label(self.pie_chart_summery_frame, background=f"{self.get_settings('bg_color')}", foreground=f"{self.get_settings('other_txt_color')}", font=font.Font(size=11), text =f"Remaining: ${remaining:.2f} ({remaining / total_income * 100:.1f}%)")
        self.pie_chart_summery_frame.place(relx=.01, rely=.085, anchor='nw')#place(x=1040, y=195)   
        total_inc_label.pack(padx=2, pady=2)
        total_sav_label.pack(padx=2, pady=2)
        total_exp_label.pack(padx=2, pady=2)
        #total_rem_label.pack(padx=2, pady=2)
        #self.window.geometry("1250x700")

    def display_pie_chart(self):
        with open(self.get_active_database()) as file:
            data = json.load(file)
        plt.interactive(False)
        savings = data['savings']
        expense = data['expense']
        income = data['income']
        savings_labels = [savings[item]['name'] for item in savings]
        savings_values = [float(savings[item]['amount']) for item in savings]
        expense_labels = [expense[item]['name'] for item in expense]
        expense_values = [float(expense[item]['amount']) for item in expense]
        income_values = [float(income[item]['amount']) for item in income]
        remaining_label = 'Remaining'
        remaining_value = self.remaining_amount
        if remaining_value < 0:
            messagebox.showinfo("Negative Remaining Amount", "Budget has a negative remaining amount. Pie Chart cannot open.")
            self.checkbox_var.set(False)
            self.checkbox_changed()
        total_savings = sum(savings_values)
        total_expense = sum(expense_values)
        total_income = sum(income_values)
        combined_labels = savings_labels + expense_labels + [remaining_label]
        combined_values = savings_values + expense_values + [remaining_value]
        combined_texts = [f'{label}\n{amount}' for label, amount in zip(combined_labels, combined_values)]
        self.fig = plt.figure(figsize=(7, 7))
        ax = self.fig.add_subplot(111)
        ax.pie(combined_values, labels=combined_texts, autopct='%1.1f%%', startangle=140, textprops={'color': f"{self.get_settings('other_txt_color')}"}, wedgeprops={'linewidth': .5, 'edgecolor': 'black'})
        ax.axis('equal')
        ax.set_aspect('1.1')
        ax.set_title('Savings and Expenses', y=1.08, color=f"{self.get_settings('other_txt_color')}")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window_frame)
        self.canvas.draw()
        plt.gcf().set_facecolor(f"{self.get_settings('bg_color')}")
        self.canvas.get_tk_widget().pack()#place(x=585, y=195) 
        self.pie_chart_summery_frame = tk.Frame(self.window_frame)
        self.pie_chart_summery_frame.configure(bg=f"{self.get_settings('bg_color')}")
        self.pie_chart_summery_frame.place(relx=.01, rely=.085, anchor='nw')#place(x=1040, y=195)
        total_sav_label = tk.Label(self.pie_chart_summery_frame, background=f"{self.get_settings('bg_color')}", foreground=f"{self.get_settings('other_txt_color')}", font=font.Font(size=11), text =f"Savings: ${total_savings:.2f} ({total_savings / total_income * 100:.1f}%)")
        total_exp_label = tk.Label(self.pie_chart_summery_frame, background=f"{self.get_settings('bg_color')}", foreground=f"{self.get_settings('other_txt_color')}", font=font.Font(size=11), text =f"Expense: ${total_expense:.2f} ({total_expense / total_income * 100:.1f}%)")
        total_inc_label = tk.Label(self.pie_chart_summery_frame, background=f"{self.get_settings('bg_color')}", foreground=f"{self.get_settings('other_txt_color')}", font=font.Font(size=11), text =f"Total Income: ${total_income:.2f}")
        total_rem_label = tk.Label(self.pie_chart_summery_frame, background=f"{self.get_settings('bg_color')}", foreground=f"{self.get_settings('other_txt_color')}", font=font.Font(size=11), text =f"Remaining: ${self.remaining_amount:.2f} ({self.remaining_amount / total_income * 100:.1f}%)")      
        total_inc_label.pack(padx=2, pady=2)
        total_sav_label.pack(padx=2, pady=2)
        total_exp_label.pack(padx=2, pady=2)
        #total_rem_label.pack(padx=2, pady=2)
        #self.window.geometry("1240x700")
        
    def close_chart(self):
        try:
            self.start_end_frame.destroy()
        except:
            pass
        plt.interactive(True)
        try:
            self.canvas.get_tk_widget().destroy()
            plt.close(self.fig)
        except:pass    
        try:
            self.pie_chart_summery_frame.destroy()
        except:pass

        

    def check_and_create_tables(self):
        if 'income' not in self.db.tables():
            self.income_table.insert({'name': "123", 'amount': "123", 'date': "123"})
            self.income_table.remove(doc_ids=[1])
        if 'expense' not in self.db.tables():
            self.expense_table.insert({'name': "123", 'amount': "123", 'date': "123"})
            self.expense_table.remove(doc_ids=[1])
        if 'savings' not in self.db.tables():
            self.savings_table.insert({'name': "123", 'amount': "123", 'date': "123"})
            self.savings_table.remove(doc_ids=[1])

    def force_start_date(self):
        if not os.path.exists("start_date.txt") and not os.path.exists("start_date_month.txt"):
            self.window.geometry("986x444")
            self.two_week_button = tk.Button(self.window, text="Budget Selection", command=self.window_biweekly)
            self.two_week_button.configure(bg="grey", fg="white")
            self.two_week_button.place(x=440, y=205)
    
    def bind_buttons(self):
        self.add_income_button.bind('<Return>', lambda event: self.add_item('income', self.entry_income_name, self.entry_income_amount, self.entry_income_date))
        self.add_expense_button.bind('<Return>', lambda event: self.add_item('expense', self.entry_expense_name, self.entry_expense_amount, self.entry_expense_date))
        self.add_savings_button.bind('<Return>', lambda event: (self.add_savings_goal(), self.add_item('savings', self.entry_savings_name, self.entry_savings_amount, self.entry_savings_date)))
        self.delete_selected_button.bind('<Return>', lambda event: self.delete_items())
        self.delete_edit_button.bind('<Return>', lambda event: self.open_second_window())
        self.save_button.bind('<Return>', lambda event: self.save_data())

    def execute_button_command(self):
        current_widget = self.window.focus_get()
        if isinstance(current_widget, tk.Button) and current_widget['command']:
            current_widget['command']()

    def generate_numeric_uuid(self):
        uuid_value = str(uuid.uuid4().int)
        return uuid_value

    def recurring_add(self, number):
        source_file = number  
        destination_file = self.get_active_database()

        try:
            with open(source_file, 'r') as source:
                source_data = json.load(source)
        except FileNotFoundError:
            pass
            return
        try:
            with open(destination_file, 'r') as destination:
                destination_data = json.load(destination)
        except FileNotFoundError:
            destination_data = {}  
        except json.JSONDecodeError:
            destination_data = {
            "income": {},
            "savings": {},
            "expense": {}
        }

        for section in ["income", "savings", "expense"]:
            section_data = source_data.get(section, {})
            new_date = self.add_budget_date()
            for key, value in section_data.items():
                unique_id = self.generate_numeric_uuid()  
                destination_data[section][unique_id] = value
                section_data[key]['UUID'] = unique_id
                value['date'] = new_date

        try:
            with open(destination_file, 'w') as destination:
                json.dump(destination_data, destination, indent=4)
        except Exception as e:
            print("Error writing to destination file:", e)
        change = "no"
        self.update_master_db(change)
        self.window.destroy()
        self.__init__()
        self.load_data()

    def recurring_edit(self, number):
        filetxt = f"{number}.json"
        with open("active_week.txt", "w") as file:
            file.write(filetxt)
        with open("title.txt", "w") as file:
            file.write(number)    
        self.window.destroy()
        self.__init__()
        self.load_data()

    def window_title(self):
        try:
            with open("title.txt", "r") as file:
                title = file.readline().strip()
                if len(title) == 0:
                    return "Press Me"
                return title
        except FileNotFoundError:
            return "Press me"
    
    def get_active_database(self):
        try:
            with open("active_week.txt", "r") as file:
                active_database = file.readline().strip()
                if len(active_database) == 0:
                    return "test1234.json"
                return active_database
        except FileNotFoundError:
            return "Press_Budget_Selection"
    
    def add_budget_date(self):
        if os.path.exists("start_date_month.txt"):
            filename = self.get_active_database()
            match = re.search(r"month(\d+)_(\d{4})", filename)
            if match:
                month = match.group(1)
                year = match.group(2)
            date = f"{month.zfill(2)}-01-{year[-2:]}"
            return date
        if os.path.exists("start_date.txt"):
            with open("start_date.txt", "r") as file:
                start_date = file.read()
            filename = self.get_active_database()
            if filename == "week0.json":
                return start_date
            string = filename
            number = int(re.findall(r'\d+', string)[0])
            result = number * 14 - 14
            known_date = datetime.datetime.strptime(start_date, "%m-%d-%y")
            new_date = known_date + datetime.timedelta(days=result)
            formatted_date = new_date.strftime("%m-%d-%y")
            return(formatted_date)
  
    def update_total_labels(self):
        values = self.load_total()
        self.total_income_label.config(text=f"Total Income: ${values['income']}")
        self.total_expense_label.config(text=f"Total Expense: ${values['expense']}")
        self.total_savings_label.config(text=f"Total Savings: ${values['savings']}")
        self.remaining_amount_label.config(text=f"Remaining Amount: ${values['remaining']}")

    def load_total(self):
        added_income = self.update_register('add', 0, self.income_table) 
        subtracted_expense = self.update_register('add', 0, self.expense_table)         
        subtracted_savings = self.update_register('add', 0, self.savings_table) 
        self.remaining_amount = round(0 + added_income - subtracted_expense - subtracted_savings, 2)
        return {'income': added_income, 'expense':subtracted_expense, 'savings':subtracted_savings, 'remaining':self.remaining_amount}
            
    def update_register(self, type, reg, table):
            for x in table.all():
                if(type == 'sub'):
                    reg -= float(x['amount'])
                if(type == 'add'):
                    reg += float(x['amount'])
            return reg
    
    def update_master_db(self, change_mdb):    
        source_file = self.get_active_database()
        destination_file = "master_db.json"
        if change_mdb == "change":
            destination_file = "change_master.json"
            self.master = TinyDB("change_master.json")
        if not os.path.exists(destination_file):
            with open(destination_file, 'w') as file:
                initial_data ={}
                if 'income' not in self.db.tables():
                        self.income_table.insert({'name': "123", 'amount': "123", 'date': "123"})
                        self.income_table.remove(doc_ids=[1])
                if 'expense' not in self.db.tables():
                        self.expense_table.insert({'name': "123", 'amount': "123", 'date': "123"})
                        self.expense_table.remove(doc_ids=[1])
                if 'savings' not in self.db.tables():
                        self.savings_table.insert({'name': "123", 'amount': "123", 'date': "123"})
                        self.savings_table.remove(doc_ids=[1])
        try:
            with open(source_file, 'r') as source:
                source_data = json.load(source)
        except FileNotFoundError:
            return

        try:
            with open(destination_file, 'r') as destination:
                destination_data = json.load(destination)
        except FileNotFoundError:
            destination_data = {}
        except json.JSONDecodeError:
            destination_data = {
                "income": {},
                "savings": {},
                "expense": {}
            }

        for section in ["income", "savings", "expense"]:
            section_data = source_data.get(section, {})
            for key, value in section_data.items():
                unique_id = value.get("UUID")
                if unique_id not in destination_data[section]:
                    destination_data[section][unique_id] = value

        try:
            with open(destination_file, 'w') as destination:
                json.dump(destination_data, destination, indent=4)
        except Exception as e:
            print("Error writing to destination file:", e)

    def add_item(self, transaction_type, entry_name, entry_amount, entry_date):
        table_map = {
            "income": self.income_table,
            "expense": self.expense_table,
            "savings": self.savings_table,
        }
        listbox_map = {
            "income": self.income_listbox,
            "expense": self.expense_listbox,
            "savings": self.savings_listbox,
        }
        name = entry_name.get()
        amount = (re.sub(r'[^0-9.]', '', entry_amount.get()))
        if len(entry_date.get()) == 0:
            date = datetime.datetime.now().strftime("%m-%d-%y")
        if len(entry_date.get()) != 0:
            date = entry_date.get()
        if name and amount and date and len(entry_amount.get()) != 0:
            key = self.generate_numeric_uuid()
            table_map[transaction_type].insert({'UUID': key, 'name': name, 'amount': amount, 'date': date})
            json_file = self.get_active_database()
            with open(json_file, 'r') as file:    
                data = json.load(file)
            updated_info = {}
            for uuid, transaction in data[transaction_type].items():
                doc_id = transaction.pop('UUID')
                transaction['UUID'] = doc_id  
                updated_info[doc_id] = transaction
            data[transaction_type] = updated_info
            with open(json_file, 'w') as file:
                json.dump(data, file, indent=4)
            if not self.get_active_database() in ["Recurring_One.json", "Recurring_Two.json"]:
                change = "no"
                self.update_master_db(change)
            if self.get_active_database() in ["Recurring_One.json", "Recurring_Two.json"]:
                change = "change"
                self.update_master_db(change)
            listbox_map[transaction_type].insert(tk.END, (key, f"{name} (${amount}), Date: {date}"))
            entry_name.delete(0, tk.END)
            entry_amount.delete(0, tk.END)
            entry_date.delete(0, tk.END)
            entry_date.insert(0, date)
            entry_name.focus_set()
            entry_date.pack()
            self.load_data()
            if self.checkbox_var.get():
                self.checkbox_var.set(False)
                self.checkbox_changed()
                self.checkbox_var.set(True)
                self.checkbox_changed()
            if self.checkbox_goals_var.get():
                self.checkbox_goals_var.set(False)
                self.toggle_goals_listbox()
                self.checkbox_goals_var.set(True)
                self.toggle_goals_listbox()

    def delete_items(self):
        if self.savings_listbox.curselection():
            self.delete_selected(self.savings_table, self.savings_listbox)
        if self.expense_listbox.curselection():
            self.delete_selected(self.expense_table, self.expense_listbox)
        if self.income_listbox.curselection():
            self.delete_selected(self.income_table, self.income_listbox)
        try:
            if self.goals_listbox.curselection():
                self.delete_selected(self.goals_table, self.goals_listbox)
        except:
            pass
           
    def delete_selected(self, dataset, listbox):
        master = TinyDB("master_db.json")
        master_income_table = master.table('income')
        master_expense_table = master.table('expense')
        master_savings_table = master.table('savings')
        selected_items = listbox.curselection()
        for index in selected_items[::-1]: 
            doc_ids=[dataset.all()[index].doc_id]
            try:
                if dataset == self.income_table:
                    master_income_table.remove(doc_ids=doc_ids)
                if dataset == self.expense_table:
                    master_expense_table.remove(doc_ids=doc_ids)
                if dataset == self.savings_table:
                    master_savings_table.remove(doc_ids=doc_ids)
                if self.checkbox_var.get():
                    self.checkbox_var.set(False)
                    self.checkbox_changed()
                    self.checkbox_var.set(True)
                    self.checkbox_changed()
                if self.checkbox_goals_var.get():
                    self.checkbox_goals_var.set(False)
                    self.toggle_goals_listbox()
                    self.checkbox_goals_var.set(True)
            except:
                pass
            dataset.remove(doc_ids=[dataset.all()[index].doc_id])
        try:
            self.toggle_goals_listbox()
        except:
            pass
        self.load_data()
            
    def load_data(self):
        self.income_ids = []
        self.expense_ids = []
        self.savings_ids= []

        self.income_listbox.delete(0, tk.END)
        self.expense_listbox.delete(0, tk.END)
        self.savings_listbox.delete(0, tk.END)
        self.income_data = self.income_table.all()
        self.total_income = 0
        for income in self.income_data:
            self.income_listbox.insert(tk.END, f"{income['name']}: ${income['amount']}, Date: {income['date']}")
        self.expense_data = self.expense_table.all()
        self.total_expense = 0
        for expense in self.expense_data:
            self.expense_listbox.insert(tk.END, f"{expense['name']}: ${expense['amount']}, Date: {expense['date']}")
        self.savings_data = self.savings_table.all()
        for savings in self.savings_data:
            self.savings_listbox.insert(tk.END, f"{savings['name']}: ${savings['amount']}, Date: {savings['date']}")
        self.check_and_create_tables
        self.update_total_labels()

    def save_data(self):
        self.income_data = self.income_table.all()
        self.expense_data = self.expense_table.all()
        self.savings_data = self.savings_table.all()
        self.expense_list = self.expense_listbox.curselection()
        for index in self.expense_list[::-1]:  
            self.expense_table.remove(doc_ids=[self.expense_data[index].doc_id])
        self.savings_list = self.savings_listbox.curselection()
        for index in self.savings_list[::-1]: 
            self.savings_table.remove(doc_ids=[self.savings_data[index].doc_id])
        self.income_table.truncate()
        self.expense_table.truncate()
        self.savings_table.truncate()
        for income in self.income_data:
            self.income_table.insert(income)
        for expense in self.expense_data:
            self.expense_table.insert(expense)
        for savings in self.savings_data:
            self.savings_table.insert(savings)
        self.update_total_labels()
        self.load_data()

    def check_selected_listbox(self, data):
        if(self.data.curselection()):
            return data
        else:
            return "false"

    def window_biweekly(self):
        window_biweekly(self).grab_set() 

    def open_second_window(self):
        if self.savings_listbox.curselection():
            selected_index = self.savings_listbox.curselection()[0]
            selected_item = self.savings_listbox.get(selected_index)
            data = "savings", selected_item
            second_window = SecondWindow(self, data)
            self.window.attributes('-alpha', .5)
            second_window.grab_set() 
        elif self.expense_listbox.curselection():
            selected_index = self.expense_listbox.curselection()[0]
            selected_item = self.expense_listbox.get(selected_index)
            data = "expense", selected_item
            second_window = SecondWindow(self, data)
            self.window.attributes('-alpha', .5)
            second_window.grab_set() 
        elif self.income_listbox.curselection():
            selected_index = self.income_listbox.curselection()[0]
            selected_item = self.income_listbox.get(selected_index)
            data = "income", selected_item
            second_window = SecondWindow(self, data)
            self.window.attributes('-alpha', .5)
            second_window.grab_set() 
        else: pass
            
    def run(self):
        self.check_and_create_tables()
        self.window.mainloop()
        

if __name__ == '__main__':
    manager = FinancialManager()
    manager.run()
    
