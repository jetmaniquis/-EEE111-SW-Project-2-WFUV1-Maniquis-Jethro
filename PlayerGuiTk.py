import customtkinter
import tkinter as tk
import csv
import json
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk, ImageFilter
from PlayerDbSqlite import PlayerDbSqlite
from PlayerDbEntry import PlayerDbEntry  # Import PlayerDbEntry class

class PlayerGuiCtk(customtkinter.CTk):
    def __init__(self, dataBase=PlayerDbSqlite('BasketballPlayer_Id.db')):
        super().__init__()
        self.db = dataBase

        # Load background image
        bg_image = Image.open("C:\\Users\\Jethro\\Desktop\\SW\\bballbg.jpg")
        bg_image = bg_image.resize((1500, 1000), Image.Resampling.LANCZOS)  # Use LANCZOS for antialiasing
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        # Create a label to hold the background image
        self.bg_label = tk.Label(self, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)

        # Create an instance of PlayerDbEntry with default values
        self.player_entry = PlayerDbEntry()

        self.title('Basketball Player Management System')
        self.geometry('1500x1000')
        self.config(bg='#FFA500')  # Orange background
        self.resizable(False, False)

        self.font1 = ('Comic Sans MS', 25, 'bold')  # Public Sans font
        self.font2 = ('Public Sans', 15, 'bold')  # Public Sans font

        
 # Styling enhancements
        self.style = ttk.Style(self)
        self.style.theme_use('clam')

        # Configure styles for Label, Entry, Combobox, and Button widgets
        
        self.style.configure('TEntry', font=self.font1, foreground='#000', background='#FCC981', bordercolor='#000', borderwidth=2)
        self.style.configure('TCombobox', font=self.font1, foreground='#000', background='#0C9295', bordercolor='#000', borderwidth=5)
        self.style.configure('TButton', font=self.font1, foreground='#000', cursor='hand2', borderwidth=2)

        # Data Entry Form
        # 'Player_Id' Label and Entry Widgets
        self.id_label = self.newCtkLabel('Player ID')
        self.id_label.place(x=145, y=80)
        self.id_entry = StringVar()
        self.id_entry = self.newCtkEntry(entryiable=self.id_entry)
        self.id_entry.place(x=100, y=130)
        

        # 'Player Name' Label and Entry Widgets
        self.name_label = self.newCtkLabel('Player Name')
        self.name_label.place(x=130, y=180)
        self.name_entry = StringVar()
        self.name_entry = self.newCtkEntry(entryiable=self.name_entry)
        self.name_entry.place(x=100, y=230)


        # 'Position' Label and Combo Box Widgets
        self.position_label = self.newCtkLabel('Position')
        self.position_label.place(x=160, y=280)
        self.position_cboxVar = StringVar()
        self.position_cboxOptions = ['Point Guard', 'Shooting Guard', 'Small Forward', 'Power Forward', 'Center']
        self.position_cbox = self.newCtkComboBox(options=self.position_cboxOptions,
                                    entryiable=self.position_cboxVar)
        self.position_cbox.place(x=100, y=330)
        # Set initial value from PlayerDbEntry
        self.position_cboxVar.set(self.player_entry.position)

        # 'Height' Label and Entry Widgets
        self.height_label = self.newCtkLabel('Height (cm)')
        self.height_label.place(x=150, y=380)
        self.height_entry = StringVar()
        self.height_entry = self.newCtkEntry(entryiable=self.height_entry)
        self.height_entry.place(x=100, y=430)
    

        # 'Jersey Number' Label and Entry Widgets
        self.jersey_label = self.newCtkLabel('Jersey Number')
        self.jersey_label.place(x=120, y=480)
        self.jersey_entry = StringVar()
        self.jersey_entry = self.newCtkEntry(entryiable=self.jersey_entry)
        self.jersey_entry.place(x=100, y=530)
    

        # Rest of your GUI code
        self.add_button = self.newCtkButton(text='Add Player',
                                onClickHandler=self.add_entry,
                                fgColor='#90EE90',  # Black text
                                hoverColor='#008000',  # Lighter orange on hover
                                borderColor='#FFA500')  # Orange border
        self.add_button.place(x=80, y=600)

        self.new_button = self.newCtkButton(text='New Player',
                                onClickHandler=lambda:self.clear_form(True), fgColor='#FCC981')
        self.new_button.place(x=80, y=650)

        self.update_button = self.newCtkButton(text='Update Player',
                                    onClickHandler=self.update_entry, fgColor='#FCC981')
        self.update_button.place(x=80, y=700)

        self.delete_button = self.newCtkButton(text='Delete Player',
                                    onClickHandler=self.delete_entry,
                                    fgColor='#FF7276',
                                    hoverColor='#8b0000',
                                    borderColor='#FFA500')
        self.delete_button.place(x=80, y=750)

        self.export_button = self.newCtkButton(text='Export to CSV',
                                    onClickHandler=self.export_to_csv, fgColor='#FCC981')
        self.export_button.place(x=80, y=800)

        self.import_button = self.newCtkButton(text='Import from CSV',
                                onClickHandler=self.import_from_csv, fgColor='#FCC981')
        self.import_button.place(x=80, y=850)

        self.export_to_json_button = self.newCtkButton(text='Export Entries to JSON',
                                                        onClickHandler=self.export_entries_to_json,
                                                        fgColor='#FCC981')
        self.export_to_json_button.place(x=70, y=900)

        

        # Tree View for Database Entries
        
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure(style='Treeview', 
                        font=self.font2, 
                        foreground='#000',  # Black text
                        background='#FCC981',  # Orange background
                        fieldlbackground='systemTransparent')  # Orange field background
        self.style.configure('Transparent.Treeview', background='systemTransparent', foreground='#000', fieldbackground='#FCC981')

        self.style.map('Treeview', background=[('selected', '#FDB44E')])  # Lighter orange on selection

        self.tree = ttk.Treeview(self, height=15)
        self.tree['columns'] = ('Player_Id', 'Player Name', 'Position', 'Height', 'Jersey Number')
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('Player_Id', anchor='center', width=10)
        self.tree.column('Player Name', anchor='center', width=150)
        self.tree.column('Position', anchor='center', width=150)
        self.tree.column('Height', anchor='center', width=10)
        self.tree.column('Jersey Number', anchor='center', width=150)

        self.tree.heading('Player_Id', text='Player_Id')
        self.tree.heading('Player Name', text='Player Name')
        self.tree.heading('Position', text='Position')
        self.tree.heading('Height', text='Height')
        self.tree.heading('Jersey Number', text='Jersey Number')

        self.tree.place(x=460, y=80, width=1000, height=750)
        self.tree.bind('<ButtonRelease>', self.read_display_data)

        self.add_to_treeview()

    # new Label Widget
    def newCtkLabel(self, text = 'CTK Label'):
        widget_Font=self.font1
        widget_TextColor='#Ffffff'
        
        widget_CornerRadius=5
        
        widget = customtkinter.CTkLabel(self, 
                                    text=text,
                                    font=widget_Font, 
                                    text_color=widget_TextColor,
                                  corner_radius=widget_CornerRadius,
                                
                                    padx=10,  # Adjust the padding
                                    pady=5)   # Adjust the padding
        return widget

    # new Entry Widget
    def newCtkEntry(self, text = 'CTK Label', entryiable=None):
        widget_Font=self.font1
        widget_TextColor='#000'
        widget_FgColor='#FFF'
        widget_BorderColor='#0C9295'
        widget_BorderWidth=2
        widget_Width=250

        widget = customtkinter.CTkEntry(self,
                                    font=widget_Font,
                                    text_color=widget_TextColor,
                                    fg_color=widget_FgColor,
                                    border_color=widget_BorderColor,
                                    border_width=widget_BorderWidth,
                                    width=widget_Width)
        return widget

    # new Combo Box Widget
    def newCtkComboBox(self, options=['DEFAULT', 'OTHER'], entryiable=None):
        widget_Font=self.font1
        widget_TextColor='#000'
        widget_FgColor='#FFF'
        widget_DropdownHoverColor='#0C9295'
        widget_ButtonColor='#0C9295'
        widget_ButtonHoverColor='#0C9295'
        widget_BorderColor='#0C9295'
        widget_BorderWidth=2
        widget_Width=250
        widget_Options=options

        widget = customtkinter.CTkComboBox(self,
                                        font=widget_Font,
                                        text_color=widget_TextColor,
                                        fg_color=widget_FgColor,
                                        border_color=widget_BorderColor,
                                        width=widget_Width,
                                        variable=entryiable,
                                        values=options,
                                        state='readonly')
        
        # get default value to 1st option
        widget.set(options[0])

        return widget

    # new Button Widget
    def newCtkButton(self, text = 'CTK Button', onClickHandler=None, fgColor='#FFFFFF', hoverColor='#FF5002', borderColor='#F15704'):
        widget_Font=self.font1
        widget_TextColor='#000'
        widget_FgColor=fgColor
        widget_HoverColor=hoverColor
        widget_BorderColor=borderColor
        widget_BorderWidth=2
        widget_Cursor='hand2'
        
        widget_Width=300
        widget_Function=onClickHandler

        widget = customtkinter.CTkButton(self,
                                        text=text,
                                        command=widget_Function,
                                        font=widget_Font,
                                        text_color=widget_TextColor,
                                        fg_color=widget_FgColor,
                                        hover_color=widget_HoverColor,
                    
                                        border_color=widget_BorderColor,
                                        border_width=widget_BorderWidth,
                                        cursor=widget_Cursor,
                                       
                                        width=widget_Width)
       
        return widget

    # Handles
    def add_to_treeview(self):
        players = self.db.fetch_players()
        self.tree.delete(*self.tree.get_children())
        for player in players:
            print(player)
            self.tree.insert('', END, values=player)
            

    def clear_form(self, *clicked):
        if clicked:
            self.tree.selection_remove(self.tree.focus())
            self.tree.focus('')
        self.id_entry.delete(0, END)
        self.name_entry.delete(0, END)
        self.position_cboxVar.set('Point Guard')
        self.height_entry.delete(0, END)
        self.jersey_entry.delete(0, END)

    def read_display_data(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            row = self.tree.item(selected_item)['values']
            self.clear_form()
            self.id_entry.insert(0, row[0])
            self.name_entry.insert(0, row[1])
            self.position_cboxVar.set(row[2])
            self.height_entry.insert(0,row[3])
            self.jersey_entry.insert(0,row[4])
        else:
            pass

    def add_entry(self):
        Player_Id = self.id_entry.get()
        player_name = self.name_entry.get()
        position = self.position_cboxVar.get()
        height = self.height_entry.get()
        jersey_number = self.jersey_entry.get()

        if not (Player_Id and player_name and position and height and jersey_number):
            messagebox.showerror('Error', 'Enter all fields.')
        elif self.db.id_exists(Player_Id):
            messagebox.showerror('Error', 'Player_Id already exists')
        else:
            self.db.insert_player(Player_Id, player_name, position, height, jersey_number)

            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been inserted')

    def delete_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose a player to delete')
        else:
            player_id = self.id_entry.get()
            self.db.delete_player(player_id)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been deleted')

    def update_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose a player to update')
        else:
        # Get the correct 'id' from the database using the 'Player_Id' from the treeview
            selected_item = self.tree.focus()
            row = self.tree.item(selected_item)['values']
            player_id = row[0]  # Assuming the player_id is in the first column
            actual_player_id = self.db.fetch_players()[int(player_id) - 1][0]

            player_name = self.name_entry.get()
            position = self.position_cboxVar.get()
            height = self.height_entry.get()
            jersey_number = self.jersey_entry.get()

            print(f"Updating player with ID: {actual_player_id}")
            print(f"New data: {player_name}, {position}, {height}, {jersey_number}")

            self.db.update_player(actual_player_id, player_name, position, height, jersey_number)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been updated')



    def export_to_csv(self):
        self.db.export_csv()
        messagebox.showinfo('Success', f'Data exported to {self.db.dbName}')


    def import_from_csv(self):

        file_path = filedialog.askopenfilename(title="Open CSV File", filetypes=[("CSV files", ".csv")])

        if not file_path:
            messagebox.showinfo('Info', 'No file selected.')
            return

        if self.db.import_csv(file_path):
            messagebox.showinfo('Success', f'Data imported from {file_path}')
            # Optionally, update the displayed data in your GUI after importing
            self.add_to_treeview()
        else:
            messagebox.showerror('Error', f'Failed to import data from {file_path}')

    def export_entries_to_json(self):
        players = self.db.fetch_players()
        json_data = []

        for player in players:
            player_dict = {
                'Player_Id': player[0],
                'Player_Name': player[1],
                'Position': player[2],
                'Height': player[3],
                'Jersey_Number': player[4]
            }
            json_data.append(player_dict)

        # Export to JSON file
        with open('basketball_players.json', 'w') as json_file:
            json.dump(json_data, json_file, indent=4)

        messagebox.showinfo('Success', 'Entries exported to basketball_players.json')
            

    
if __name__ == "__main__":
    app = PlayerGuiCtk()
    app.mainloop()
