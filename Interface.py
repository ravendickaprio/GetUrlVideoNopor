"""Proyecto Dickaprio
   Get Videos
   Interface Dickaprio
"""
#Importar Librerias
# Para Modo Grafico
import tkinter as tk
from tkinter import ttk 
#  Para Pintar Imagen (Inesesaria para funcionamiento)
import matplotlib
matplotlib. use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.image as mpimg
from matplotlib.backend_bases import key_press_handler
# Para Obtener HTML de Web
import urllib3
import io
# Para descargar el Video
import requests
#new
from threading import Thread
from urllib.request import urlretrieve, urlcleanup
#Clase Para Hacer El Frame Scrolleable 
class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        #Varibales de Color
        self.fondo = "#191919"
        self.backgound = self.fondo
        #Estilos de botones y self.fondos
        styl = ttk.Style()
        styl.configure('new.TFrame', background=self.fondo)
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self,bg=self.fondo)
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
        self.primario   = "#f20000"
        self.secundario = "#69A1F4"
        self.fondo      = "#191919"
        self.fondo_diluido      = "#e5e5ff"
        self.exito      = "#00b300"
        self.backgound = self.fondo
        #Estilos de botones y fondos
        styl = ttk.Style()
        styl.configure('new.TFrame', background=self.fondo)
        styl2 = ttk.Style()
        styl2.configure('TButton', background=self.secundario)

        #declaracion de variables
        self.entrada          = tk.StringVar()
        self.conjunto_string  = tk.StringVar()
        self.url_video = ""
        self.filename = ""
        #Definir el Frame con el que se trabajara
        miFrame = ScrollableFrame(self)
        # miFrame= ttk.Frame(self,padding="3 3 3 3",style='new.TFrame')
        miFrame. grid(columnspan=4, row=1, sticky=(tk. N, tk. W, tk. E, tk. S))
        #creamos un frame SUPERIOR para colocar la imagen
        frame_sup = ttk. Frame(self, padding="3 3 3 3")
        frame_sup. grid(columnspan=4, row=0)

        # Leer la imagen
        img = mpimg.imread("haker.jpg")#Puedes poner la que gustes 
        # creamos la figura y el widget asociado
        f = Figure(figsize=(5, 4), dpi=100)
        f.patch.set_facecolor(self.fondo)
        self.ax1 = f.add_subplot(111)
        #Activamos el autoescalado del os ejes
        self.ax1.imshow(img)
        self.ax1.set_facecolor(self.fondo)
        self.ax1.axis('off')
        #Recalculamos los ejes
        self.ax1.relim()
        self.ax1.autoscale_view(True,True,True)
        #Inicializamos las cambas
        self.canvas_fig = FigureCanvasTkAgg(f, master = frame_sup)
        self.canvas_fig. get_tk_widget().grid(column=0, row=0,rowspan=2)
        #Numero de Linea (row)
        numero_grid   = 0
        #Definir Las etiquetas
        lrelacion     = tk.Label(miFrame.scrollable_frame , text = "URL-")
        lrelacion    .  config(background = self.fondo)
        lrelacion    .  grid(row = numero_grid , column = 0 , padx = 10 , pady = 10)
        #Funcion para agregar el evento enter 
        def on_key_press(event):
            if event.keycode == 13 :
                self.obtenerURL()

        #Definir las entitis(cajas de texto) , Botones Labels por renglon del grid
        self.etexto        = tk.Entry(miFrame.scrollable_frame, textvariable=self.entrada)
        self.etexto       .  bind('<Return>', on_key_press)
        self.etexto       .  grid(row =numero_grid, column=1,padx=10,pady=10)
        self.botonadd = ttk.Button (miFrame.scrollable_frame , text="Get Video" , command = self.obtenerURL)
        self.botonadd.  grid(row = numero_grid, column = 3 , padx = 10 , pady = 10)
        botonlimpiar = ttk.Button (miFrame.scrollable_frame, text="Clear" , command = self.clear)
        botonlimpiar.  grid(sticky = (tk. N, tk. W, tk. E, tk. S) , row = numero_grid , column = 2 , padx = 10 , pady = 10 , columnspan = 1)
        numero_grid   = numero_grid + 1
        #--------------------------------------------------------------------
        self.progressbar = ttk.Progressbar(self)
        self.progressbar.place(x=70, y=60, width=385)
        numero_grid   = numero_grid + 1
        self.econjuntor    = tk.Entry(miFrame.scrollable_frame, textvariable=self.conjunto_string , state=tk.DISABLED)
        self.econjuntor   .  grid(sticky=(tk. N, tk. W, tk. E, tk. S) , row = numero_grid , column = 0 , padx = 10 , pady = 10 , columnspan = 5)
        self.econjuntor   .  config(disabledbackground = self.primario , disabledforeground = self.fondo)
        numero_grid   = numero_grid + 1
        #--------------------------------------------------------------------
        self.texbox   = tk.Text(miFrame.scrollable_frame , height = 10 , width = 30, bg = self.fondo_diluido)
        self.texbox.    grid(sticky = (tk. N, tk. W, tk. E, tk. S), row = numero_grid , column = 0 , padx = 10 , pady = 10 , columnspan = 4)
        self.texbox.    config(state="disabled", foreground='gray31')
        self.botonsdescargar = ttk.Button (miFrame.scrollable_frame, text="Download" , command = self.downloadClick)
        self.botonsdescargar.  grid(sticky = (tk. N, tk. W, tk. E, tk. S) , row = numero_grid , column = 5 , padx = 10 , pady = 10 , columnspan = 1)
        self.botonsdescargar.config(state='disabled')
        self.conjunto_string.set("enjoy/*/*/*/*/*/enjoy/*/*/*/*/*/enjoy/*/*/*/*/*/")  

    #Funcion Para Obtener el filename del video y la url del mismo para descargar
    #Input  string url_raw  Direccion URL Ingresada por el usuario
    #Output bool true|false Indica si la funcion se ejecuto correctamente
    def procesarURL (self , url_raw):
        url_raw = url_raw.strip()#Eliminar espacios
        if(url_raw!=''):
            val = url_raw.find("https://www.")#Validar el formato http
            if val > -1 :
                self.clear() #Limpiar Cajas de texto
                # Traer todo el cuerpo de la pagina
                http = urllib3.PoolManager()
                r = http.request('GET', url_raw , preload_content=False)
                r.auto_close = False
                f = open ('Series.txt','a+')# Abrir el archivo txt para guardar un registo (opcional)
                encontrado = 0
                for line in io.TextIOWrapper(r): #iteramos toda la web para buscar el video
                    if encontrado == 0:
                        tittle = line.find("title") #Solo para saber el file name
                        if tittle > 0 :
                            encontrado = 1
                            #Extraemos el File name
                            inicio = line.find("title>")
                            fin = line.find("XVIDEOS.COM")
                            self.filename = line[inicio + 6: fin] # Sacamos el filename
                            self.filename = self.eliminaCaracteres(self.filename)
                            self.texbox.config(state='normal')
                            self.texbox.insert(tk.END, self.filename) 
                            self.texbox.insert(tk.END, "\n") 
                            self.texbox.config(state='disabled')
                            f.write('\n' +self.filename)#Colocamos en archivo (opcional)
                    # url del video, aqui se localiza el video, desconozco la resolucion
                    locc = line.find("html5video_base")
                    if locc > 0 :
                        inicio = line.find("https://")
                        fin = line.find("><img")
                        url_video_tmp = line[inicio: fin-1]
                        self.texbox.config(state='normal')
                        self.texbox.insert(tk.END, url_video_tmp) 
                        self.texbox.insert(tk.END, "\n") 
                        self.texbox.config(state='disabled')
                        f.write('\n' +url_video_tmp)#Colocamos en archivo (opcional)
                        if url_video_tmp != '': #Hotfix de cosas curiosas de la vida
                            self.url_video = url_video_tmp
                f.close()#cerramos el archivo (opcional)
                self.botonsdescargar.config(state='normal')
                self.econjuntor   .  config(disabledbackground = self.primario , disabledforeground = self.fondo)
                return True
        return False

    #Funcion para Llenar la matriz de entradas por Entity
    #Input 
    #Output 
    def obtenerURL (self):
        url_raw = self.entrada.get()
        llenado = self.procesarURL(url_raw)
        if llenado :    
            self.conjunto_string.set( "(" + url_raw + ")")
        else:
            self.texbox.config(state='normal')
            self.texbox.insert(tk.END, "URL FAIL") 
            self.texbox.config(state='disabled')
        self.entrada.set("") #Eliminar contenido del url
        
    #Funcion para limpiar file name de caracteres html
    #Input  string  string_row filename raw
    #Output string  string_row filename sin caracteres html a 50 caracteres max
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
        string_row = string_row.replace("</title>"    , "")
        string_row = string_row.replace("itle>"    , "")
        string_row = string_row.replace("</"     , "")
        string_row = string_row[0:50]
        return string_row

    #Funcion para Limpiar las cajas de texto
    #Input 
    #Output 
    def clear (self):
        self.botonadd.config(state='normal')
        self.texbox.config(state='normal')
        self.texbox.delete('1.0', "end") 
        self.texbox.config(state='disabled')
        self.botonsdescargar.config(state='disabled')
        self.econjuntor   .  config(disabledbackground = self.primario , disabledforeground = self.fondo)

    #Funcion para descargar
    #Input 
    #Output Video descargado con el filname
    def download (self):
        self.texbox.config(state='disabled')
        self.botonsdescargar.config(state='disabled')
        self.botonadd.config(state='disabled')
        self.etexto.config(state='disabled')
        #Proceso disque con la barra
        urlretrieve(self.url_video, self.filename+ '.mp4', self.download_status)
        urlcleanup()
        #Fin Proceso
        self.botonadd.config(state='normal')
        self.etexto.config(state='normal')
        self.econjuntor   .  config(disabledbackground = self.exito , disabledforeground = self.fondo)

    #Funcion para mandar el threath de descargar para que no se congele la app
    #Input 
    #Output Video descargado con el filname
    def downloadClick(self):
        Thread(target=self.download).start()

    #Funcion para mostrar en la barra el proceso de descarga
    #Input 
    #Output Video descargado con el filname
    def download_status(self, count, data_size, total_data):
        if count == 0:
            # Establecer el máximo valor para la barra de progreso.
            self.progressbar.configure(maximum=total_data)
        else:
            # Aumentar el progreso.
            self.progressbar.step(data_size)

if __name__ == "__main__":
    MainWindow = App_Window(None)
    MainWindow.mainloop()
