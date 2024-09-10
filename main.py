from kivy.app import App 
from kivy.uix.widget import Widget 
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.properties import ListProperty
import sqlite3
import re
from functools import partial
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, Line, Ellipse, RoundedRectangle
from kivy.core.window import Window
from datetime import datetime


database = "database.db"
con = sqlite3.connect(database)
cur = con.cursor()


#Custom Line
class LineWidget(Widget):
    def __init__(self, **kwargs):
        super(LineWidget, self).__init__(**kwargs)
        with self.canvas:
            Color(0, 0, 0, 1)
            self.line = Line(points=[self.x, self.center_y, self.width, self.center_y], width=10)
        self.bind(pos=self.update_line, size=self.update_line)
    def update_line(self, *args):
        self.line.points = [self.x, self.center_y, self.right, self.center_y]
######################################################################

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
                Color(23/255, 156/255, 19/255, 1) 
                self.rrect = RoundedRectangle(
                    pos=self.pos, size=self.size, radius=[20] * 4
                )
        else:
            with self.canvas.before:
                Color(98/255, 0/255, 238/255, 1)  
                self.rrect = RoundedRectangle(
                    pos=self.pos, size=self.size, radius=[20] * 4
                )


################################################################################
class RoundToggleButton(RoundToggleButton2):
    
    def __init__(self, **kwargs):
        super(RoundToggleButton, self).__init__(**kwargs)
        self.size_hint = (0.3333, None)
        self.height =200 

##################################################################################
#                      submit and cance button


class RoundB(Button):
    def __init__(self, **kwargs):
        super(RoundB, self).__init__(**kwargs)
        
        self.background_color = (0, 0, 0, 0)  # Transparent background
        
        with self.canvas.before:
            Color(98/255, 0/255, 238/255, 1)  # Initial purple color
            self.rrect = RoundedRectangle(
                pos=self.pos, size=self.size, radius=[self.height / 2] * 4  # More rounded corners
            )
        
        # Bind to update the shape and handle button press/release
        self.bind(pos=self.update_rrect, size=self.update_rrect)
        self.bind(on_press=self.on_press, on_release=self.on_release)

    def update_rrect(self, *args):
        self.rrect.pos = self.pos
        self.rrect.size = self.size
        self.rrect.radius = [self.height / 2] * 4  # Update to keep rounded corners

    def on_press(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(23/255, 156/255, 19/255, 1)  # Green color when pressed
            self.rrect = RoundedRectangle(
                pos=self.pos, size=self.size, radius=[self.height / 2] * 4  # Rounded on press
            )

    def on_release(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(98/255, 0/255, 238/255, 1)  # Purple color when released
            self.rrect = RoundedRectangle(
                pos=self.pos, size=self.size, radius=[self.height / 2] * 4  # Rounded on release
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
            with open("current_s_t.txt","w") as f:
                f.write("EMPTY")

            
            # cur.execute("CREATE TABLE IF NOT EXISTS current_s_t(name text)")
            cur.execute("CREATE TABLE IF NOT EXISTS current_roll(roll INTEGER, status INTEGER)")
            cur.execute("CREATE TABLE IF NOT EXISTS latest_submit_table(name text, present INTEGER, absent INTEGER, date text)") 
            con.commit()

        except:
            print("Error!! 12")


    def table_name_validity_check(self, name):

        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cur.fetchall()
            
        for table in tables:
            table_name = table[0]
            if table_name=="current_roll" or table_name=="latest_submit_table":
                continue
            if table_name==name:
                return -1
        return 1


        

    def load_saved_classrooms(self):
        self.ids._scroll.scroll_y = 1
        self.ids._scroll2.scroll_y = 1

        try:
            # Query to get all table names
            cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cur.fetchall()
            
            for table in tables:
                table_name = table[0]
                if table_name=="current_roll" or table_name=="latest_submit_table":
                    continue
                cat = RoundToggleButton2(text=table_name, font_size=25, group="A")
                cat.bind(on_press=self.class_func)
                self.ids.cid.add_widget(cat)
                
            con.commit()
        except sqlite3.Error as e:
            print(f"An error occurred 21: {e}")
        
        finally:
            pass

    
    def add_class(self):
        #creating popup content
        content = BoxLayout(orientation='vertical',padding=10,spacing=10)
        input_name = TextInput(hint_text="Enter ClassRoom Name to Add", multiline=False,size_hint=(1,0.3), font_size=32, halign='center')
        content.add_widget(input_name)

        #start roll, end roll
        content2 = GridLayout(cols=2,padding=10,spacing=20,size_hint=(1,0.33))
        input_name2 = TextInput(hint_text="Start Roll", multiline=False,size_hint=(0.4,0.3), font_size=32, halign='center')
        input_name3 = TextInput(hint_text="End Roll", multiline=False,size_hint=(0.4,0.3), font_size=32, halign='center')
        content2.add_widget(input_name2)
        content2.add_widget(input_name3)
        content.add_widget(content2)

        def on_submit(instance):
            cn = input_name.text 
            cn_start = input_name2.text
            cn_end = input_name3.text

            ret = self.table_name_validity_check(cn)

            if ret==-1:
                self.error_popup("Class Already Exist")
                return

            if cn=="":
                self.error_popup("Enter a valid name!")
                return

            if not re.match(r'^\w+$', cn):
                # raise ValueError("Invalid classname. Use only letters, numbers, and underscores.")
                #Create A popup
                self.error_popup("Don't use space and special char!")
                return 

            try:
                int_va1 = int(cn_start)
                int_val = int(cn_end)
            except:
                self.error_popup("Please enter valid integer!")
                return

            if(int(cn_start)>int(cn_end)):
                self.error_popup("Start roll must be greater!")
                return
            

            if cn:
                #this line creates button(classroom) dynamically on id cid
                cat = RoundToggleButton2(text=cn, font_size=25, group="A")
                cat.bind(on_press=self.class_func)
                self.ids.cid.add_widget(cat)
                self.create_data_table(cn,cn_start,cn_end)
                self.ids.reg.clear_widgets()
                self.ids.jr.clear_widgets()
                
            popup.dismiss()

        #creating submit button
        sb = Button(text="Submit",font_size=32, size_hint=(1, 0.3))
        sb.bind(on_press=on_submit)
        content.add_widget(sb)

        #creating the popup
        popup = Popup(title='Add New ClassRoom', content=content, size_hint=(0.8,0.4))
        popup.open()


    def create_data_table(self, classname, startroll, endroll):        
        
        # Convert roll numbers to integers
        start_roll = int(startroll)
        end_roll = int(endroll)

        try:
            # Create the table if it doesn't exist
            cur.execute(f"CREATE TABLE IF NOT EXISTS {classname} (rollnumber INTEGER PRIMARY KEY, value INTEGER DEFAULT 0)")
            
            # Insert records
            records_to_insert = [(i, 0) for i in range(start_roll, end_roll + 1)]
            insert_query = f"INSERT OR IGNORE INTO {classname} (rollnumber, value) VALUES (?, ?)"
            cur.executemany(insert_query, records_to_insert)
            
            # Debugging: Print all rows in the table
            cur.execute(f"SELECT * FROM {classname}")
       
        
        except sqlite3.Error as e:
            print(f"Error occurred: {e}")
        
        finally:
            # Close the cursor and connection
            con.commit()

    def class_func(self,instance):
        #When pressing on a class_name(CSEA) this function executes
        #see datatable current_selected_table to get the selected table name

        if instance.state=='down':
            self.ids._scroll.scroll_y = 1
            self.ids._scroll2.scroll_y = 1
            cur.execute("DELETE FROM current_roll")

            with open("current_s_t.txt","w") as f:
                f.write(f"{instance.text}")
            

            self.update_register_page(instance.text)
            self.classDetails()
            
            
        else:
            self.ids._scroll.scroll_y = 1
            self.ids._scroll2.scroll_y = 1

            with open("current_s_t.txt","w") as f:
                f.write("EMPTY")
            cur.execute("DELETE FROM current_roll")


            self.ids.reg.clear_widgets()
            self.ids.jr.clear_widgets()

        

    
    def update_register_page(self,class_name):
        self.ids.reg.clear_widgets()

        cur.execute(f"SELECT * from {class_name}")
        row = cur.fetchone()
        while row:
            i = row[0]
            btn = RoundToggleButton(text=str(i),font_size=28)
            btn.bind(on_press =partial(self.on_toggle_button,roll=i))
            self.ids.reg.add_widget(btn)
            row = cur.fetchone()

    def clear_temp_data(self):
        cur.execute(f"DELETE FROM current_roll")
        self.insert_empty()
        con.commit()


    def delete_class(self):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        input_name = TextInput(hint_text="Enter ClassRoom Name to Delete", size_hint=(1,0.3),font_size=32, multiline=False, halign='center')
        content.add_widget(input_name)

        def on_delete(instance):

            class_name = input_name.text.strip()
            for child in self.ids.cid.children[:]:
                if isinstance(child, ToggleButton) and child.text == class_name:
                    #Removing classroom details

                    cur.execute(f"DROP TABLE IF EXISTS {class_name}")

                    con.commit()
    

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

        #roll value
        li = [(roll,value)]
        cur.executemany("INSERT INTO current_roll VALUES(?, ?)", li)
        con.commit()

    
    def error_popup(self,txt):
        
        content = BoxLayout(orientation='vertical',padding=10,spacing=10)
        lb = Label(text=txt, font_size=30)
        content.add_widget(lb)
        popup = Popup(title='Error Notice', content=content, size_hint=(0.8,0.3))
        popup.open()

    def final_submit(self):
        try:

            myflag = 0
            if self.ids._revbutton.state=="down":
                myflag = 1

            print(f"myflag:{myflag}")
          
            with open("current_s_t.txt","r") as f:
                data = f.read()


            class_name = data



            if class_name=='EMPTY':
                print("No Class Selected!")
                self.error_popup("NO  CLASSROOM  SELECTED")
                return


            d = {}
            cur.execute("SELECT * FROM current_roll")  #for today
            row = cur.fetchone()
            
            while row:
                # print(f"{row[0]} -- {row[1]}")
                d[row[0]]=row[1]
                row = cur.fetchone()

            counter = 0
            for roll,sta in d.items():
                if sta==1:
                    counter+=1

            

            
            total_st = 0

            d2 = {}
            table_name = data

            cur.execute(f"SELECT * FROM {table_name}")
            row = cur.fetchone()
            while row:
                total_st+=1
                d2[row[0]]=row[1]
                row = cur.fetchone()

            present = 0
            absent = 0

            low = min(d2.keys()) 
            high = max(d2.keys())

            total = high-low + 1


            if myflag == 0:
                for k, v in d.items():
                    if k in d2:
                        present+=1
                        d2[k] += v 
            else:           
                for i in range(low, high + 1):
                    if d.get(i) == 1: 
                        absent+=1
                        continue
                    d2[i] += 1  

                

                    
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


            #Working --- 
            

            
            cur.execute("DELETE FROM latest_submit_table")

            today = datetime.today()
            year = today.year
            month = today.month
            day = today.day

            today_date = str(day)+"-"+str(month)+"-"+str(year)

            qw = "INSERT INTO latest_submit_table (name,present,absent,date) VALUES (?,?,?,?)"
            cur.execute(qw, (class_name,counter,total_st-counter,today_date,))

            print(f"Class {class_name} -> Present: {counter} student. Absent: {total_st-counter} Date:{today_date}")


            if self.ids._revbutton.state=="normal":
                self.ids._date.text = "Date: " + today_date + "\n\n" + "Class: " + class_name + "\n" + "Present: " + str(present) + "\n"+"Absent: " + str(total-present)
            else:
                self.ids._date.text = "Date: " + today_date + "\n\n" + "Class: " + class_name + "\n" + "Present: " + str(total-absent) + "\n"+"Absent: " + str(absent)
            #############################


            self.classDetails()

            #clearing current_roll table
            cur.execute(f"DELETE FROM current_roll")
            self.insert_empty()

            con.commit()
            
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
        self.insert_empty()

    def insert_empty(self):
        with open("current_s_t.txt","w") as f:
            f.write("EMPTY")



    
    def view_table_details(self,name):

        # print(f"DataBase--{name}----***\n\n")

        cur.execute(f"SELECT * FROM {name}")
        row = cur.fetchone()
        while row:
            # print(row)
            row = cur.fetchone()
        # print("\nEnd Of DataBase")
        con.commit()


    def classDetails(self):
        #clear previous data/widgets
        self.ids.jr.clear_widgets()

        with open("current_s_t.txt","r") as f:
            tb = f.read()
        

        lab = Label(text="CLASS:  "+tb,font_size=40,bold=True,color=(0, 0, 0, 1),size_hint=(1,None), height=100)
        self.ids.jr.add_widget(lab)

        fgtext = "###################################################################################################"
        lab = Label(text=fgtext,color=(0,0,0, 1), size_hint=(1,None), height=100)
        self.ids.jr.add_widget(lab)

        print(f"\n\nTable name tb:{tb}")
        
                

        cur.execute(f"SELECT * FROM {tb}")
        row = cur.fetchone()
        while row:
            roll = row[0]
            state = row[1]

            pa = "Roll No: "+str(roll)+"    "+"Present Day: "+str(state)
            lab = Label(text=pa,font_size=32,bold=True,color=(0,0,0, 1),size_hint=(1,None), height=100)
            self.ids.jr.add_widget(lab)

            fgtext = "###################################################################################################"
            
            lab = Label(text=fgtext,color=(0,0,0, 1), size_hint=(1,None), height=100)
            self.ids.jr.add_widget(lab)


            row = cur.fetchone()


    def reverse(self):
        print(f"{self.ids._revbutton.state}")
        

###########################################################################

class AttendenceApp(App):
    def build(self):
        return MyLayout()
    
if __name__=="__main__":
    AttendenceApp().run()
    
