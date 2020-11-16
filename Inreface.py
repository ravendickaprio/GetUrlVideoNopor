"""Proyecto Dickaprio
   Get Videos
   Interface Dickaprio
"""
#Importar Librerias
import tkinter as tk
from tkinter import ttk 
import matplotlib
matplotlib. use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.image as mpimg
from matplotlib.backend_bases import key_press_handler

from bs4 import BeautifulSoup
import urllib3
import io
#Clase Para Hacer El Frame Scrolleable 
class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        #Varibales de Color
        fondo      = "#191919"
        self.backgound = fondo
        #Estilos de botones y fondos
        styl = ttk.Style()
        styl.configure('new.TFrame', background=fondo)
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self,bg=fondo)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas, style='new.TFrame')

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

#Clase Para desplegar la UI
class App_Window(tk. Tk):
    def __init__(self,parent):
        tk.Tk.__init__(self,parent)
        self.parent = parent
        self.title(u"Get Video")
        self.inicializar()
        self.config(background = "#191919")
        

    def inicializar(self):
        #Varibales de Color
        primario   = "#f20000"
        secundario = "#69A1F4"
        fondo      = "#191919"
        fondo_diluido      = "#e5e5ff"
        self.backgound = fondo
        #Estilos de botones y fondos
        styl = ttk.Style()
        styl.configure('new.TFrame', background=fondo)
        styl2 = ttk.Style()
        styl2.configure('TButton', background=secundario)

        #declaracion de variables
        self.entrada          = tk.StringVar()
        self.conjunto_string  = tk.StringVar()
        self.tiporelacion     = tk.StringVar()


        #Definir el Frame con el que se trabajara

        miFrame = ScrollableFrame(self)
        # miFrame= ttk.Frame(self,padding="3 3 3 3",style='new.TFrame')
        miFrame. grid(columnspan=4, row=1, sticky=(tk. N, tk. W, tk. E, tk. S))

        #creamos un frame SUPERIOR para colocar la grafica
        frame_sup = ttk. Frame(self, padding="3 3 3 3")
        frame_sup. grid(columnspan=4, row=0)
        # Leer la imagen
        img = mpimg.imread("haker.jpg")
        # creamos la figura y el widget asociado
        f = Figure(figsize=(5, 4), dpi=100)
        f.patch.set_facecolor(fondo)
        self.ax1 = f.add_subplot(111)
        #Activamos el autoescalado del os ejes
        self.ax1.imshow(img)
        self.ax1.set_facecolor(fondo)
        self.ax1.axis('off')
        #Recalculamos los ejes
        self.ax1.relim()
        self.ax1.autoscale_view(True,True,True)
        #Inicializamos las dos graficas
        self.lineC, = self.ax1.plot([], [], color='b')
        self.canvas_fig = FigureCanvasTkAgg(f, master = frame_sup)
        self.canvas_fig. get_tk_widget().grid(column=0, row=0,rowspan=2)
        #Numero de Linea
        numero_grid   = 0
        #Definir Las etiquetas
        lrelacion     = tk.Label(miFrame.scrollable_frame , text = "URL-")
        lrelacion    .  config(background = fondo)
        lrelacion    .  grid(row = numero_grid , column = 0 , padx = 10 , pady = 10)

        #Funcion para agregar el evento enter 
        def on_key_press(event):
            if event.keycode == 13 :
                self.funcionGetB()

        #Definir las entitis(cajas de texto) , Botones Labels por renglon del grid
        etexto        = tk.Entry(miFrame.scrollable_frame, textvariable=self.entrada)
        etexto       .  bind('<Return>', on_key_press)
        etexto       .  grid(row =numero_grid, column=1,padx=10,pady=10)
        econjuntor    = tk.Entry(miFrame.scrollable_frame, textvariable=self.conjunto_string , state=tk.DISABLED)

        self.botonadd = ttk.Button (miFrame.scrollable_frame , text="Get Video" , command = self.funcionGetB)
        self.botonadd.  grid(row = numero_grid, column = 3 , padx = 10 , pady = 10)
        botonlimpiar = ttk.Button (miFrame.scrollable_frame, text="Clear" , command = self.clear)
        botonlimpiar.  grid(sticky = (tk. N, tk. W, tk. E, tk. S) , row = numero_grid , column = 2 , padx = 10 , pady = 10 , columnspan = 1)
        numero_grid   = numero_grid + 1
        #--------------------------------------------------------------------
        econjuntor   .  grid(sticky=(tk. N, tk. W, tk. E, tk. S) , row = numero_grid , column = 0 , padx = 10 , pady = 10 , columnspan = 5)
        econjuntor   .  config(disabledbackground = primario , disabledforeground = fondo)
        numero_grid   = numero_grid + 1
        #--------------------------------------------------------------------
        self.texbox   = tk.Text(miFrame.scrollable_frame , height = 10 , width = 30, bg = fondo_diluido)
        self.texbox.    grid(sticky = (tk. N, tk. W, tk. E, tk. S), row = numero_grid , column = 0 , padx = 10 , pady = 10 , columnspan = 4)
        self.texbox.    config(state="disabled", foreground='gray31')
        self.conjunto_string.set("enjoy/*/*/*/*/*/enjoy/*/*/*/*/*/enjoy/*/*/*/*/*/")  


    #Funcion Para LLenar datos
    #Input  string pareja  Pareja formada por 2 caracteres separados por una ,(aun no validado)
    #Output bool
    def llenado_datos (self , pareja):
        pareja = pareja.strip()
        if(pareja!=''):
            val = pareja.find("https://www.")
            if val > -1 :
                self.clear()
                http = urllib3.PoolManager()
                r = http.request('GET',pareja , preload_content=False)
                r.auto_close = False
                f = open ('Series.txt','a+')
                encontrado = 0
                for line in io.TextIOWrapper(r):
                    if encontrado == 0:
                        tittle = line.find("title")
                        if tittle > 0 :
                            encontrado = 1
                            web = line.find("title>")
                            web2 = line.find("XVIDEOS.COM")
                            letrirtas = line[web + 6: web2] # &comma
                            letrirtas = self.eliminaCaracteres(letrirtas)
                            self.texbox.config(state='normal')
                            self.texbox.insert(tk.END, letrirtas) 
                            self.texbox.insert(tk.END, "\n") 
                            self.texbox.config(state='disabled')
                            f.write('\n' +letrirtas)

                    # url
                    locc = line.find("html5video_base")
                    if locc > 0 :
                        web = line.find("https://")
                        web2 = line.find("><img")
                        letrirtas = line[web: web2-1]
                        self.texbox.config(state='normal')
                        self.texbox.insert(tk.END, letrirtas) 
                        self.texbox.insert(tk.END, "\n") 
                        self.texbox.config(state='disabled')
                        f.write('\n' +letrirtas)
                    
                # soup = BeautifulSoup(i)
                f.close()
            else :
                return False
        else :
            return False
        return True

    #Funcion para Llenar la matriz de entradas por Entity
    #Input 
    #Output 
    def funcionGetB (self):
        var1 = self.entrada.get()
        llenado = self.llenado_datos(var1)
        if llenado :    
            self.conjunto_string.set( "(" + var1 + ")")
        else:
            self.texbox.config(state='normal')
            self.texbox.insert(tk.END, "URL FAIL") 
            self.texbox.config(state='disabled')
        self.entrada.set("")
        
    #Funcion para limpiar string
    #Input 
    #Output 
    def eliminaCaracteres (self, string_row ):
        string_row = string_row.replace("&comma" , "")
        string_row = string_row.replace("&lpar"  , "")
        string_row = string_row.replace("&rpar"  , "")
        string_row = string_row.replace("&ntilde", "ñ")
        string_row = string_row.replace("&Ntilde", "Ñ")
        string_row = string_row.replace("&aacute", "á")
        string_row = string_row.replace("&eacute", "é")
        string_row = string_row.replace("&iacute", "í")
        string_row = string_row.replace("&oacute", "ó")
        string_row = string_row.replace("&uacute", "ú")
        string_row = string_row.replace("&Aacute", "Á")
        string_row = string_row.replace("&Eacute", "É")
        string_row = string_row.replace("&Iacute", "Í")
        string_row = string_row.replace("&Oacute", "Ó")
        string_row = string_row.replace("&Uacute", "Ú")
        string_row = string_row.replace("&euro"  , "€")
        string_row = string_row.replace("&lt"    , "<")
        string_row = string_row.replace("&gt"    , ">")
        string_row = string_row.replace("&amp"   , "&")
        string_row = string_row.replace("&quot"  , "\"")
        string_row = string_row.replace("&nbsp"  , "_")
        string_row = string_row.replace("&apos"  , "'")
        string_row = string_row.replace("."      , "")
        string_row = string_row.replace(";"      , "")
        string_row = string_row.replace("COM"    , "")
        string_row = string_row.replace("CO"     , "")
        string_row = string_row.replace(" "      , "_")
        string_row = string_row.replace("</t"    , "")
        string_row = string_row.replace("</ti"   , "")
        string_row = string_row.replace("</tit"  , "")
        string_row = string_row.replace("</titl" , "")
        string_row = string_row.replace("</title", "")
        string_row = string_row.replace("</t>"   , "")
        string_row = string_row.replace("</p>"   , "")
        string_row = string_row.replace("</p"    , "")
        string_row = string_row.replace("</"     , "")
        string_row = string_row[0:50]
        return string_row
    #Funcion para Limpiar las variables
    #Input 
    #Output 
    def clear (self):
        self.botonadd.config(state='normal')
        self.texbox.config(state='normal')
        self.texbox.delete('1.0', "end") 
        self.texbox.config(state='disabled')


if __name__ == "__main__":
    MainWindow = App_Window(None)
    MainWindow.mainloop()
