import tkinter
import tkinter.messagebox
import customtkinter
from analyze import  Analyzer
from tkinter import filedialog
import numpy as np
from math import sqrt

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.tmp = "KNeighbors"
        # configure window
        self.title("ResortsFinder")
        self.geometry(f"{700}x{500}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="WeatherAnalyzation", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event, text = "Load data")
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        #self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        #self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        #self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        #self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=2, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                        command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=3, column=0, padx=20, pady=(0, 0))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="Classifier type:", anchor="w")
        self.scaling_label.grid(row=4, column=0, padx=20, pady=(5, 10))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["KNeighbors","GaussianNB","DecisionTree"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=5, column=0, padx=20, pady=(0, 270))
        self.textbox = customtkinter.CTkTextbox(self, width=900,height=500)
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0))
        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Enter weather")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Search", command=self.start_analyze)
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")


    def start_analyze(self):
        self.textbox.delete('1.0',"end")

        try:
            self.ent = self.entry.get()
            txt = (self.ent.strip()).split(" ")
            txt = [float(i) for i in txt]
            print(2)
            cols = ["precipitation", "max_temperature", "min_temperature", "wind"]
            self.textbox.insert("end", "You've entered next weather data:\n")
            print(3)
            for i in range(0, len(txt)):
                self.textbox.insert("end", f"{cols[i]}: {txt[i]}\n")
            print(4)
            print(np.array([txt]))
            #print(self.tmp)
            if self.tmp == "KNeighbors":
                self.result = self.analizator.predict_KNN(np.array([txt]))
            elif self.tmp == "GaussianNB":
                self.result = self.analizator.predict_GNB(np.array([txt]))
            elif self.tmp == "DecisionTree":
                self.result = self.analizator.predict_CART(np.array([txt]))
            print(self.result)
            found_row = self.analizator.data[self.analizator.data.resort == self.result[0]]
            r_vec = sqrt(sum([i**2 for i in (np.array(found_row.values[0][1:]) - np.array(txt))]))
            if r_vec <= 5:
                self.textbox.insert("end", f"\nFounded resort: {found_row.values[0][0]}\n")
                for i in range(0, len(txt)):
                    self.textbox.insert("end", f"{cols[i]}: {found_row.values[0][1:][i]}\n")
            else:
                self.textbox.insert("end", f"\nNot found\n")
        except:
            self.textbox.delete('1.0', "end")
            self.textbox.insert("end", "Error. Incorrect entered data or weather dataset")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        self.tmp = new_scaling


    def sidebar_button_event(self):
        tkinter.Tk().withdraw()  # prevents an empty tkinter window from appearing
        csv_path = filedialog.askopenfilename()
        self.analizator = Analyzer(csv_path)

if __name__ == "__main__":
    app = App()
    app.mainloop()


