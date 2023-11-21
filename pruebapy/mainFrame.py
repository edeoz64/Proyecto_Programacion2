from tkinter import Frame, Label, Button, Checkbutton, StringVar, IntVar
import serial, time, threading, mysql.connector, smtplib

db_config = {
    'host': 'localhost',
    'user': 'root',  # Usuario por defecto de XAMPP
    'database': 'sensado',
}
contracorreo = 'Miguel107._.'

class MainFrame(Frame):
    def __init__(self,master=None):
        super().__init__(master,width=500,height=300,background='#87CEEB')
        self.master = master
        self.master.protocol('WM_DELETE_WINDOW',self.askQuit)
        
        self.pack()
        self.hilo1 = threading.Thread(target=self.getSensorValues,daemon=True)
        self.esp = serial.Serial("COM3", 115200,timeout=1.0)
        time.sleep(1)
        self.value_hum = StringVar()
        self.value_temp = StringVar()
        self.value_ledr = IntVar()
        self.value_leda = IntVar()
        self.value_boc = IntVar()
        self.create_wifgets()
        self.isRun=True
        self.hilo1.start()
        
    def askQuit(self):
        self.isRun=False
        self.esp.write('led1:0'.encode('ascii'))
        time.sleep(1.5)
        self.esp.write('led2:0'.encode('ascii'))
        time.sleep(1.5)
        self.esp.write('bocina:0'.encode('ascii'))
        time.sleep(1.5)
        self.esp.close()
        self.hilo1.join(0.1)
        self.master.quit()
        self.master.destroy()
        print('***Finalizando...')
        
        
    def getSensorValues(self):
        while self.isRun:
            
            cad = self.esp.readline().decode('ascii')
            valores = cad.split(',')

            if len(valores) == 2:
                hum, temp = valores
                humedad = int(hum) 
                temperatura = float(temp)
                
                # Conectar a la base de datos
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor()
                sql = "INSERT INTO temphume (humedad, temperatura) VALUES (%s, %s)"
                data = (humedad, temperatura)                
                cursor.execute(sql, data)
                conn.commit()         
                #print(f"Datos insertados: Humedad={humedad}, Temperatura={temperatura}")    
                conn.close()
                
                if humedad < 60:
                    self.esp.write('led1:1'.encode('ascii'))
                    time.sleep(3)
                    self.esp.write('led1:0'.encode('ascii'))
                    time.sleep(2)
        
                elif humedad > 90:
                    self.esp.write('led2:1'.encode('ascii'))
                    time.sleep(3)
                    self.esp.write('bocina:1'.encode('ascii'))
                    time.sleep(3)
                    self.esp.write('led2:0'.encode('ascii'))
                    time.sleep(3)
                    self.esp.write('bocina:0'.encode('ascii'))
                    time.sleep(1)
                    message = 'Advertencia: Niveles de humedad elevados detectados. TOMAR PRECAUCIONES.'
                    subject = 'HUMEDAD ELEVADA'
                    message = 'Subject: {}\n\n{}'.format(subject, message)

                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login("u20211197757@usco.edu.co", contracorreo)
                    server.sendmail("u20211195575@usco.edu.co", "u20211196484@usco.edu.co", message)
                    server.quit()
 
                print(humedad)
                print(temperatura)   
                self.value_hum.set(humedad)
                self.value_temp.set(temperatura)
        
    
    def fnEnvialedr(self):
        cad = 'led1:'+ str(self.value_ledr.get())
        self.esp.write(cad.encode('ascii'))
        print(cad)
    
    def fnEnvialeda(self):
        cad = 'led2:'+ str(self.value_leda.get())
        self.esp.write(cad.encode('ascii'))
        print(cad)
        
    def fnEnviaboc(self):
        cad = 'bocina:'+ str(self.value_boc.get())
        self.esp.write(cad.encode('ascii'))
        print(cad)
    
    def create_wifgets(self):
        Label(self,text="Humedad:",bg="#87CEEB", fg="blue").place(x=20, y=20)
        Label(self,width=6, textvariable=self.value_hum).place(x=120, y=20)
        
        Label(self,text="Temperatura:",bg="#87CEEB", fg="blue").place(x=20, y=40)
        Label(self,width=6, textvariable=self.value_temp).place(x=120, y=40)
        
        Checkbutton(self,text = 'Probar led rojo',variable =self.value_ledr,onvalue=1,offvalue=0, command=self.fnEnvialedr,bg="lightgreen", fg="blue").place(x=30,y=120)
        
        
        Checkbutton(self,text = 'Probar led azul',variable =self.value_leda,onvalue=1,offvalue=0, command=self.fnEnvialeda,bg="lightgreen", fg="blue").place(x=30,y=150)
        
        
        Checkbutton(self,text = 'Probar bocina',variable =self.value_boc,onvalue=1,offvalue=0, command=self.fnEnviaboc,bg="lightgreen", fg="blue").place(x=30,y=180)