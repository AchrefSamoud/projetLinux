import tkinter as tk
from multiprocessing import Process
import sys
import customtkinter
import os
from PIL import Image
import random
import ray
ray.init()
import subprocess
try:
    import thread
except ModuleNotFoundError:  # Python 3
    import _thread as thread
import time
from io import StringIO
clickable2=False
clickable1=False
class PrintLogger(object):  # create file like object

    def __init__(self, textbox):  # pass reference to text widget
        self.textbox = textbox  # keep ref

    def read(self, text):
        self.textbox.configure(state="disabled")  # make field readonly
        self.textbox.insert("end", text)  # write text to textbox
        self.textbox.see("end")  # scroll to end

    def flush(self):  # needed for file like object
        pass

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Linux_Project.py")
        self.geometry("700x450")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../test/manual_integration_tests/test_images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "serv.png")), size=(35, 35))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_test_image_cleanup.png")), size=(500, 150))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(25, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Client/Server App", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="", image=self.large_test_image)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        self.home_frame_button_1 = customtkinter.CTkButton(self.home_frame, text=" Run Client/Server Using Named Pipes", command=self.runProg1)
        self.home_frame_button_1.grid(row=1, column=0, padx=25, pady=12)
        self.home_frame_button_2 = customtkinter.CTkButton(self.home_frame, text=" Run Client/Server Using Sockets", compound="right", command=self.runProg2)
        self.home_frame_button_2.grid(row=2, column=0, padx=25, pady=12)
        self.home_frame_button_3 = customtkinter.CTkButton(self.home_frame, text="Quit", compound="top",command=self.close)
        self.home_frame_button_3.grid(row=4, column=0, padx=20, pady=10)
        self.home_frame_button_4= customtkinter.CTkButton(self.home_frame, text="Show Result", command=self.create_toplevel)
        self.home_frame_button_4.grid(row=3, column=0, padx=20, pady=10)

        # create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # create third frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # select default frame
        self.select_frame_by_name("home")


    def runProg1(self):
        global clickable1
        clickable1 = True
        @ray.remote    
        def serverTube():
            print ('start serverTube')
            os.system("./Serveur")
            print ('end serverTube')
        @ray.remote
        def clientTube():
            print ('start clientTube')
            time.sleep(2) # Sleep for 2 seconds
            os.system("./Client")
            print ('\n end clientTube')
        #Execute server and client in parellel:
        ray.get([serverTube.remote(),clientTube.remote()])
        
    
    
    def runProg2(self):
        global clickable2
        clickable2 = True
        @ray.remote
        def serverTCP():
            print ('start serverTCP')
            os.system("./serverTCP")
            print ('end serverTCP')
        @ray.remote
        def clientTCP():
            print ('start clientTCP')
            time.sleep(2) # Sleep for 5 seconds
            numb = random.randint(1,1000)
            print(numb)
            os.system("./clientTCP"+" "+str(numb))
            print ('end clientTCP')
        #Execute server and client in parellel:
        ray.get([serverTCP.remote(),clientTCP.remote()])
    def close(self):
        sys.exit()
    def create_toplevel(self):
        window = customtkinter.CTkToplevel(self)
        window.title("Communication Flow")
        window.geometry("500x250")

        # create label on CTkToplevel window
        label = customtkinter.CTkLabel(window, text="Console Result")
        label.pack(side="top", fill="both", expand=True, padx=5, pady=1)
        tabview = customtkinter.CTkTabview(label)
        tabview.grid(row=0, column=0,padx=10, pady=1)

        tab_1 = tabview.add("Client")  # add tab at the end
        tab_2 = tabview.add("Server")  # add tab at the end
        tabview.set("Server")  # set currently visible tab
        textbox1 = customtkinter.CTkTextbox(tab_1)
        textbox1.grid(row=0, column=0, columnspan=1, padx=10, pady=1)
        textbox2 = customtkinter.CTkTextbox(tab_2)
        textbox1.grid_rowconfigure(0, weight=1)
        textbox1.grid_columnconfigure((0, 0), weight=1)
        textbox2.grid_rowconfigure(0, weight=1)
        textbox2.grid_columnconfigure((0, 0), weight=1)
        textbox2.grid(row=0, column=0, columnspan=2, padx=10, pady=1)
        #textbox = customtkinter.CTkTextbox(label)
        #textbox.grid(row=0, column=0)
        filename="client.txt"
        try:
            global clickable1
            if clickable1:
                textbox1.delete('1.0',tk.END)
                the_file = open(filename)
                textbox1.insert(tk.END, the_file.read())
        except IOError:
            messagebox.showinfo("Error", "Could not open file")
        filename="server.txt"
        try:
            if clickable1:
                textbox2.delete('1.0',tk.END)
                the_file = open(filename)
                textbox2.insert(tk.END, the_file.read())
                clickable1=False
        except IOError:
            messagebox.showinfo("Error", "Could not open file")
        filename="result_TCP.txt"
        try:
            global clickable2
            if clickable2:
                textbox1.delete('1.0',tk.END)
                the_file = open(filename)
                textbox1.insert(tk.END, the_file.read())
        except IOError:
            messagebox.showinfo("Error", "Could not open file")
        filename="Client_TCP.txt"
        try:
            if clickable2:
                textbox2.delete('1.0',tk.END)
                the_file = open(filename)
                textbox2.insert(tk.END, the_file.read())
                clickable2=False
        except IOError:
            messagebox.showinfo("Error", "Could not open file")
    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=2, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=4, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")
    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)
class Display(tk.Frame):
    def __init__(self,parent=0):
       tk.Frame.__init__(self,parent)
       self.input = tk.Text(self, width=100, height=15)
       self.input.pack()
       self.doIt = tk.Button(self,text="URL to Hash", command=self.onEnter)
       self.doIt.pack()
       self.output = tk.Text(self, width=100, height=15)
       self.output.pack()
       sys.stdout = self
       self.pack()

    def onEnter(self):
        text_input = self.input.get(1.0,tk.END)
        product_url_list = text_input.split('\n')
        url_list_to_hash(product_url_list)

### I used the code below to somewhat successfully call the functions from another script
### but it did not solve my issue though.
        # p = subprocess.Popen(['python', './image_url_to_hash.py', self.input.get(1.0,"end-1c")],
        #              stdout=subprocess.PIPE,
        #              stderr=subprocess.STDOUT,
        #              )
        # for line in iter(p.stdout.readline, ''):
        #     print line

    def write(self, txt):
        self.output.insert(tk.END,str(txt))
#######This is the missing line!!!!:
        self.update_idletasks()

    def input_to_hash(text_input):
        product_url_list = text_input.split('\n')
        ### This is just some dummy code to simulate the output.
        ### There is a delay is processing each url, but I would like to capture output as it's running
        for link in product_url_list:
            time.sleep(1)
            print (link)

if __name__ == "__main__":
    app = App()
    app.mainloop()

