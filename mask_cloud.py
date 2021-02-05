import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.ttk import Progressbar
from tkinter import filedialog
from tkinter import Menu
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import plot
from numpy import savetxt
import sys
import sklearn

class Tela():

    def __init__(self):
        self.menu_window = tk.Tk()
        self.menu_window.configure(background="#212121")
        self.perso(self.menu_window)

        logo_imag = tk.PhotoImage(file='nuuv.png')
        img_menu = ttk.Label(self.menu_window, image=logo_imag)
        img_menu.image = logo_imag
        img_menu.grid(row=0,column=0, pady=(0,20), padx=(20,20),rowspan = 1, columnspan = 3)

        style_help = ttk.Style()
        style_help.theme_use('clam')
        style_help.configure('help.TButton', borderwidth=0)
        help_img = tk.PhotoImage(file=r'help.png')
        self.help_button = ttk.Button(self.menu_window, width= 2, style='style_help.help.TButton', image=help_img, command = self.helpfunc)
        self.help_button.grid(row=0,pady=(20,0), padx=(320,20), column=0, sticky="N" )
        self.help_button.bind("<Enter>", self.dark)
        self.help_button.bind("<Leave>", self.light)

        self.var1 = tk.IntVar()
        self.check = ttk.Checkbutton(self.menu_window, text='CLOUD', onvalue = 1,command = self.abrir, variable=self.var1)
        self.check.grid(row=1,pady=(0,0), padx=(40,200), column=0)
        self.var2 = tk.IntVar()
        self.check1 = ttk.Checkbutton(self.menu_window, text='NDVI', onvalue = 2,command = self.abrir, variable=self.var2)
        self.check1.grid(row=1,pady=(0,0), padx=(80,100), column=0)
        self.var3 = tk.IntVar()
        self.check2 = ttk.Checkbutton(self.menu_window, text='CLOUD&NDVI', onvalue = 3,command = self.abrir, variable=self.var3)
        self.check2.grid(row=1,pady=(0,0), padx=(190,0), column=0)

        self.bottun_open = ttk.Button(self.menu_window, state=tk.DISABLED, command = self.open, text="Open")
        self.bottun_open.grid(row=4,column=0, pady=(30,10), padx=(30,190))
        self.bottun_send = ttk.Button(self.menu_window, state=tk.DISABLED, command = self.textoframe, text="Send")
        self.bottun_send.grid(row=4,column=0, pady=(30,10), padx=(190,10))

        valid = (self.menu_window.register(self.validar), "%S") 
        area_var = tk.IntVar()
        self.area = ttk.Entry(self.menu_window, textvariable=area_var, validate="key", validatecommand=valid, width = 20)
        self.area.grid(row=6, column=0, pady=(10,10), padx=(190,10))
        style_area = ttk.Style()
        style_area.theme_use('clam')
        style_area.configure('area.TLabel', font=('Source Code Pro Semibold', 10))
        area_label = ttk.Label(self.menu_window, text='Pixel area (km2)', style = 'style_area.area.TLabel')
        area_label.grid(row=6, column=0,pady=(10,10), padx=(35,190))

        bottom_label = ttk.Label(self.menu_window,text='script: www.github.com\\BSFernando', font="Source 10", foreground='black')
        bottom_label.grid(row=7, pady=(30,0), padx=(90,20),sticky="WE",columnspan = 3)
        bottom_label1 = ttk.Label(self.menu_window, text='email: bs_fernando@hotmail.com', font="Source 10", foreground='black')
        bottom_label1.grid(row=8, pady=(0,20), padx=(98,20),sticky="WE",columnspan = 3)

        self.menu_window.protocol("WM_DELETE_WINDOW", self.quit)
        self.menu_window.mainloop()

    def textoframe(self):
        plot_window = tk.Toplevel()

        menu_plot = Menu(plot_window)
        new_menu = Menu(menu_plot, tearoff=0)
        new_menu.add_command(label='Salvar', command = self.salvar)
        new_menu.add_separator()
        new_menu.add_command(label='Salvarcsv', command = self.salvarcsv)
        new_menu.add_separator()
        new_menu.add_command(label='Exit', command = self.quit)
        menu_plot.add_cascade(label='File', menu=new_menu)
        plot_window.config(menu=menu_plot)
        self.perso(plot_window)
        plot_window.configure(background="#212121")

        plot_bottum = ttk.Button(plot_window, command = self.salvar, text="Salvar")
        plot_bottum.pack(fill=tk.BOTH, anchor='nw')
        plot_bottum_csv = ttk.Button(plot_window, command = self.salvarcsv, text="SalvarCSV")
        plot_bottum_csv.pack(fill=tk.BOTH, anchor='nw', after=plot_bottum)

        self.figure_save, self.areas, self.lista_item  = plot.criar(self.path, self.area.get(), [self.var1.get(),self.var2.get(),self.var3.get()])
        figure = FigureCanvasTkAgg(self.figure_save, plot_window)
        figure.get_tk_widget().pack(fill=tk.Y, anchor='ne')

        plot_window.mainloop()

    def helpfunc(self):
        help_window = tk.Toplevel()
        self.perso(help_window)
        help_window.configure(background="#212121")

        help_imag1 = tk.PhotoImage(file='help_text.png')
        h = ttk.Label(help_window, image=help_imag1)
        h.image = help_imag1
        h.grid(row=0,column=0)

        help_window.mainloop()

    def perso(self, windo):
        style_func = ttk.Style(windo)
        style_func.theme_use('clam')
        style_func.configure('TButton',bordercolor="#b5b5b5",background="#212121", foreground='black', borderwidth=1, font=('Source Code Pro Semibold', 13))
        style_func.configure('TLabel', background="#212121", foreground='#e3dff5', font=('Source Code Pro Semibold', 13))
        style_func.configure('TNotebook', background="#212121", foreground='#e3dff5')
        style_func.configure('TEntry', background="black", foreground='black', font=('Source Code Pro Semibold', 13))
        style_func.configure('TCheckbutton', background="#212121", foreground='black', borderwidth=0.01, font=('Source Code Pro Semibold', 13))
    
    def abrir(self):
        if (self.check.instate(['selected']) == True or self.check1.instate(['selected']) == True or self.check2.instate(['selected']) == True):
            self.bottun_open['state'] = tk.NORMAL
        else:
            self.bottun_open['state'] = tk.DISABLED
            self.bottun_send['state'] = tk.DISABLED

    def open(self):
        self.path = filedialog.askopenfilename(filetypes = (("Image files","*.jpg"),("Image files","*.png")))
        if (self.path[len(self.path)-3:len(self.path)] == 'png' or self.path[len(self.path)-3:len(self.path)] == 'jpg'):
            self.bottun_send['state'] = tk.NORMAL
        else:
            self.bottun_send['state'] = tk.DISABLED

    def salvar(self):
        save = filedialog.asksaveasfile(title="Select An Image", defaultextension=".png", filetypes=(("jpeg files", ".jpg"),("png files", ".png")))
        self.figure_save.savefig(save.name)

    def salvarcsv(self):
        for item in (range(0,len(self.areas))):
            if self.lista_item[item] == 1:
                save = filedialog.asksaveasfile(title='CLOUD', mode='w', defaultextension=".csv")
                savetxt(save.name, self.areas[item], delimiter=',')
            elif self.lista_item[item] == 2:
                save = filedialog.asksaveasfile(title='NDVI', mode='w', defaultextension=".csv")
                savetxt(save.name, self.areas[item], delimiter=',')
            else:
                save = filedialog.asksaveasfile(title='CLOUD & NDVI', mode='w', defaultextension=".csv")
                savetxt(save.name, self.areas[item], delimiter=',')

    def validar(self,x):
        return x.isdigit()

    def quit(self):
        sys.exit()

    def dark(self, event):
        self.help = tk.PhotoImage(file=r'helpdark.png')
        self.help_button.configure(image=self.help)

    def light(self, event):
        self.help = tk.PhotoImage(file=r'help.png')
        self.help_button.configure(image=self.help)

if __name__ == '__main__':
	Tela()


    
