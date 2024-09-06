from kivy.app import App 
from kivy.uix.widget import Widget 
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import sqlite3
import re
from functools import partial
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, Line, Ellipse, RoundedRectangle
from kivy.core.window import Window

#Window.size = (600, 800)



###########################################################################
#               Register Page Button
class RoundToggleButton(ToggleButton):
    
    def __init__(self, **kwargs):
        super(RoundToggleButton, self).__init__(**kwargs)
        self.size_hint = (0.3333, None)
        height =200 

############################################################################


class RoundToggleButton2(ToggleButton):
    def __init__(self, **kwargs):
        super(RoundToggleButton2, self).__init__(**kwargs)
        
        self.background_color = (0, 0, 0, 0)  # Transparent background
        
        with self.canvas.before:
            Color(98/255, 0/255, 238/255, 1) 
            self.rrect = RoundedRectangle(
                pos=self.pos, size=self.size, radius=[20] * 4
            )
        
        self.bind(pos=self.update_rrect, size=self.update_rrect)
        self.bind(state=self.on_state)

    def update_rrect(self, *args):
        self.rrect.pos = self.pos
        self.rrect.size = self.size

    def on_state(self, *args):
        self.canvas.before.clear()
        if self.state == 'down':
            with self.canvas.before:
                Color(23/255, 156/255, 19/255, 1)  # Green color when toggled on
                self.rrect = RoundedRectangle(
                    pos=self.pos, size=self.size, radius=[20] * 4
                )
        else:
            with self.canvas.before:
                Color(98/255, 0/255, 238/255, 1)   # Red color when toggled off
                self.rrect = RoundedRectangle(
                    pos=self.pos, size=self.size, radius=[20] * 4
                )

##################################################################################
#                      submit and cance button
class RoundB(Button):
    def __init__(self, **kwargs):
        super(RoundB, self).__init__(**kwargs)
        
        self.background_color = (0, 0, 0, 0)  # Transparent background
        
        with self.canvas.before:
            Color(98/255, 0/255, 238/255, 1) 
            self.rrect = RoundedRectangle(
                pos=self.pos, size=self.size, radius=[20] * 4
            )
        
        self.bind(pos=self.update_rrect, size=self.update_rrect)
        self.bind(on_press=self.on_press, on_release=self.on_release)

    def update_rrect(self, *args):
        self.rrect.pos = self.pos
        self.rrect.size = self.size

    def on_press(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(23/255, 156/255, 19/255, 1)  # Green color when pressed
            self.rrect = RoundedRectangle(
                pos=self.pos, size=self.size, radius=[20] * 4
            )

    def on_release(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(98/255, 0/255, 238/255, 1)    # Red color when released
            self.rrect = RoundedRectangle(
                pos=self.pos, size=self.size, radius=[20] * 4
            )
############################################################################################

class CustomLabel(Label):
    def __init__(self, **kwargs):
        super(CustomLabel, self).__init__(**kwargs)
        # Add default properties here
        self.border_color = (53/255, 56/255, 54/255, 1)  # RGBA format (red)
        self.border_width = 3


    def on_size(self, *args):
        self.update_canvas()


    def on_pos(self, *args):
        self.update_canvas()


    def update_canvas(self):
        self.canvas.before.clear()
        with self.canvas.before:
            # Draw background color
            Color(92/255, 94/255, 92/255, 1)  # RGBA format (green)
            Rectangle(pos=self.pos, size=self.size)
            # Draw border
            Color(*self.border_color)
            Line(rectangle=(self.x, self.y, self.width, self.height), width=self.border_width)

###########################################################################


class MyLayout(TabbedPanel):
    def __init__(self,**kwargs):
        super(MyLayout, self).__init__(**kwargs)
        self.load_saved_classrooms()

        try:
            database = "database.db"
            con = sqlite3.connect(database)
            cur = con.cursor()

            
            cur.execute("CREATE TABLE IF NOT EXISTS current_s_t(name text)")
            cur.execute("CREATE TABLE IF NOT EXISTS current_roll(roll INTEGER, status INTEGER)")
            

            cur.close()
            con.commit()
            con.close()
        except:
            print("Error!! 12")

        

    def load_saved_classrooms(self):
        database = "database.db"
        con = sqlite3.connect(database)
        cur = con.cursor()
        try:
            # Query to get all table names
            cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cur.fetchall()
            
            for table in tables:
                table_name = table[0]
                if table_name=="current_s_t" or table_name=="current_roll":
                    continue
                cat = RoundToggleButton2(text=table_name, font_size=24, group="A")
                cat.bind(on_press=self.class_func)
                self.ids.cid.add_widget(cat)
                
            con.commit()
        except sqlite3.Error as e:
            print(f"An error occurred 21: {e}")
        
        finally:
            cur.close()
            con.close()


    
    def add_class(self):
        #creating popup content
        content = BoxLayout(orientation='vertical',padding=10,spacing=10)
        input_name = TextInput(hint_text="Enter ClassRoom Name to Add", multiline=False,size_hint=(1,0.3), font_size=20, halign='center')
        content.add_widget(input_name)

        #start roll, end roll
        content2 = GridLayout(cols=2,padding=10,spacing=20,size_hint=(1,0.33))
        input_name2 = TextInput(hint_text="Start Roll", multiline=False,size_hint=(0.4,0.3), font_size=20, halign='center')
        input_name3 = TextInput(hint_text="End Roll", multiline=False,size_hint=(0.4,0.3), font_size=20, halign='center')
        content2.add_widget(input_name2)
        content2.add_widget(input_name3)
        content.add_widget(content2)

        def on_submit(instance):
            cn = input_name.text 
            cn_start = input_name2.text
            cn_end = input_name3.text

            try:
                int_va1 = int(cn_start)
                int_val = int(cn_end)
            except:
                self.error_popup("Please enter valid integer!")
                return

            if(int(cn_start)>int(cn_end)):
                self.error_popup("Start roll must be greater!")
                return
            if not re.match(r'^\w+$', cn):
                # raise ValueError("Invalid classname. Use only letters, numbers, and underscores.")
                #Create A popup
                self.error_popup("Don't use space and special char!")
                return 

            if cn:
                #this line creates button(classroom) dynamically on id cid
                cat = RoundToggleButton2(text=cn, font_size=24, group="A")
                cat.bind(on_press=self.class_func)
                self.ids.cid.add_widget(cat)
                self.create_data_table(cn,cn_start,cn_end)
                self.ids.reg.clear_widgets()
                self.ids.jr.clear_widgets()
                
            popup.dismiss()

        #creating submit button
        sb = Button(text="Submit",font_size=18, size_hint=(1, 0.3))
        sb.bind(on_press=on_submit)
        content.add_widget(sb)

        #creating the popup
        popup = Popup(title='Add New ClassRoom', content=content, size_hint=(0.8,0.4))
        popup.open()


    def create_data_table(self, classname, startroll, endroll):        
        
        # Convert roll numbers to integers
        start_roll = int(startroll)
        end_roll = int(endroll)
        
        con = sqlite3.connect("database.db")
        cur = con.cursor()

        try:
            # Create the table if it doesn't exist
            cur.execute(f"CREATE TABLE IF NOT EXISTS {classname} (rollnumber INTEGER PRIMARY KEY, value INTEGER DEFAULT 0)")
            
            # Insert records
            records_to_insert = [(i, 0) for i in range(start_roll, end_roll + 1)]
            insert_query = f"INSERT OR IGNORE INTO {classname} (rollnumber, value) VALUES (?, ?)"
            cur.executemany(insert_query, records_to_insert)
            
            # Debugging: Print all rows in the table
            cur.execute(f"SELECT * FROM {classname}")
            rows = cur.fetchall()
            for row in rows:
                print(row)
        
        except sqlite3.Error as e:
            print(f"Error occurred: {e}")
        
        finally:
            # Close the cursor and connection
            cur.close()
            con.commit()
            con.close()

    def class_func(self,instance):
        #When pressing on a class_name(CSEA) this function executes
        #see datatable current_selected_table to get the selected table name

        if instance.state=='down':
            database = "database.db"
            con = sqlite3.connect(database)
            cur = con.cursor()
            try:
                cur.execute(f"DELETE FROM current_s_t")
                cur.execute(f"DELETE FROM current_roll")
            except:
                print("F00000~")
            qw = "INSERT INTO current_s_t (name) VALUES (?)"
            cur.execute(qw, (instance.text,))
            cur.close()
            con.commit()
            con.close()

            self.update_register_page(instance.text)
            self.classDetails()
            
             
            #table details
            #DEBUG
            #self.view_table_details(instance.text)
        else:
            database = "database.db"
            con = sqlite3.connect(database)
            cur = con.cursor()
            try:
                cur.execute(f"DELETE FROM current_s_t")
            except:
                print("F000001~")
            qw = "INSERT INTO current_s_t (name) VALUES (?)"
            cur.execute(qw, ("EMPTY",))

            cur.close()
            con.commit()
            con.close()

            self.ids.reg.clear_widgets()
            self.ids.jr.clear_widgets()

    
    def update_register_page(self,class_name):
        self.ids.reg.clear_widgets()
        database = "database.db"
        con = sqlite3.connect(database)
        cur = con.cursor()
        cur.execute(f"SELECT * from {class_name}")
        row = cur.fetchone()
        while row:
            i = row[0]
            # btn = ToggleButton(text=str(i),font_size=32,size_hint_x=None, size_hint_y=None,height=100, width=180)
            btn = RoundToggleButton(text=str(i),font_size=20)
            btn.bind(on_press =partial(self.on_toggle_button,roll=i))
            self.ids.reg.add_widget(btn)
            row = cur.fetchone()

    def clear_temp_data(self):
        database = "database.db"
        con = sqlite3.connect(database)
        cur = con.cursor()
        cur.execute(f"DELETE FROM current_roll")
        cur.execute(f"DELETE FROM current_s_t")
        cur.close()
        con.commit()
        con.close()

    def delete_class(self):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        input_name = TextInput(hint_text="Enter ClassRoom Name to Delete", size_hint=(1,0.3),font_size=20, multiline=False, halign='center')
        content.add_widget(input_name)

        def on_delete(instance):

            class_name = input_name.text.strip()
            for child in self.ids.cid.children[:]:
                if isinstance(child, ToggleButton) and child.text == class_name:
                    #Removing classroom details
                    con = sqlite3.connect("database.db")
                    cur = con.cursor()

                    cur.execute(f"DROP TABLE IF EXISTS {class_name}")

                    cur.close()
                    con.commit()
                    con.close()

                    self.ids.cid.remove_widget(child)
                    self.ids.reg.clear_widgets()
                    self.ids.jr.clear_widgets()
                    break
            popup.dismiss()

        db = Button(text="Delete", size_hint=(1, 0.3))
        db.bind(on_press=on_delete)
        content.add_widget(db)

        popup = Popup(title='Delete ClassRoom', content=content, size_hint=(0.8, 0.3))
        popup.open()


    def on_toggle_button(self, instance, roll, *args):
        value = 1 if instance.state == 'down' else 0 

        database = "database.db"
        con = sqlite3.connect(database)
        cur = con.cursor()

        #roll value
        li = [(roll,value)]
        cur.executemany("INSERT INTO current_roll VALUES(?, ?)", li)

        
        cur.close()
        con.commit()
        con.close()
    
    def error_popup(self,txt):
        
        content = BoxLayout(orientation='vertical',padding=10,spacing=10)
        lb = Label(text=txt, font_size=20)
        content.add_widget(lb)
        popup = Popup(title='Error Notice', content=content, size_hint=(0.8,0.3))
        popup.open()

    def final_submit(self):
        try:
            con = sqlite3.connect("database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM current_s_t")
            row = cur.fetchone()
            if row[0]=='EMPTY':
                print("No Class Selected!")
                self.error_popup("NO  CLASSROOM  SELECTED")
                return

            d = {}
            cur.execute("SELECT * FROM current_roll")
            row = cur.fetchone()
            while row:
                # print(f"{row[0]} -- {row[1]}")
                d[row[0]]=row[1]
                row = cur.fetchone()


            d2 = {}
            cur.execute("SELECT * FROM current_s_t")
            row = cur.fetchone()
            table_name = row[0]

            cur.execute(f"SELECT * FROM {table_name}")
            row = cur.fetchone()
            while row:
                d2[row[0]]=row[1]
                row = cur.fetchone()

            
            for k,v in d.items():
                for u,h in d2.items():
                    if u==k:
                        h=h+v 
                        d2[u]=h
                        break
                    
            #delete previous records from table
            cur.execute(f"DELETE FROM {table_name}")

            cur.execute(f"SELECT * FROM {table_name}")
            li=[]
            for k,v in d2.items():
                li.append((k,v))

            cur.executemany(f"INSERT INTO {table_name} VALUES(?, ?)",li)


            #cur.close()
            con.commit()
            #con.close()

            self.classDetails()

            #clearing current_roll table
            cur.execute(f"DELETE FROM current_roll")
            cur.execute(f"DELETE FROM current_s_t")
            cur.execute("INSERT INTO current_s_t VALUES('EMPTY')")

            cur.close()
            con.commit()
            con.close()

            #Debug
            #self.view_table_details(table_name)
            
            self.reset_toggle_buttons()
            self.ids.reg.clear_widgets()
        except:
            pass

    def reset_toggle_buttons(self):
        for child in self.ids.reg.children:
            if isinstance(child, ToggleButton):
                child.state = 'normal'
        for child in self.ids.cid.children:
            if isinstance(child, ToggleButton):
                child.state = 'normal'

    def cancel_btn(self):
        #reset the temp files and toggle button
        self.clear_temp_data()


        self.reset_toggle_buttons()

        #remove the all  widgets from register as no class is selected
        self.ids.reg.clear_widgets()

        #clear previous data/widgets from details as no class is selected
        self.ids.jr.clear_widgets()



    
    def view_table_details(self,name):
        database = "database.db"
        con = sqlite3.connect(database)
        cur = con.cursor()

        # print(f"DataBase--{name}----***\n\n")

        cur.execute(f"SELECT * FROM {name}")
        row = cur.fetchone()
        while row:
            # print(row)
            row = cur.fetchone()
        # print("\nEnd Of DataBase")
        cur.close()
        con.commit()
        con.close()

    def classDetails(self):
        #clear previous data/widgets
        self.ids.jr.clear_widgets()

        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM current_s_t")
        row = cur.fetchone()
        tb = row[0]

        lab = CustomLabel(text="ClassRoom: "+tb,font_size=32,bold=True,color=(1, 1, 1, 1),size_hint=(1,None), height=100)
        self.ids.jr.add_widget(lab)

        # lab = CustomLabel(text="***************",font_size=32,bold=True,color=(1, 1, 1, 1),size_hint=(1,None), height=100)
        # self.ids.jr.add_widget(lab)
                

        cur.execute(f"SELECT * FROM {tb}")
        row = cur.fetchone()
        while row:
            roll = row[0]
            state = row[1]

            pa = "Roll No: "+str(roll)+"    "+"Present Day: "+str(state)
            lab = CustomLabel(text=pa,font_size=32,bold=False,color=(1, 1, 1, 1),size_hint=(1,None), height=100)
            self.ids.jr.add_widget(lab)

            row = cur.fetchone()

###########################################################################

class AttendenceApp(App):
    def build(self):
        return MyLayout()
    
if __name__=="__main__":
    AttendenceApp().run()
    
