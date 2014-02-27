from Tkinter import Tk, Frame, BOTH, Label, Canvas
from cgitb import text
import threading
import time
# from flight import flightcontroller
import controls
import flight


class Gui(Frame, threading.Thread):
  
    def __init__(self, parent):
        threading.Thread.__init__(self)
        Frame.__init__(self, parent)   
        self.parent = parent
        self.closeRequest = False
        
        self.initUI()
        self.start()
        
    
    def initUI(self):
        self.parent.title("Crazyflie Client")

        Label(self, text="Pitch").place(x=5, y=5)
        self.label_pitch = Label(self, text="0.00")
        self.label_pitch.place(x=60, y=5)
        
        Label(self, text="Roll").place(x=5, y=25)
        self.label_roll = Label(self, text="0.00")
        self.label_roll.place(x=60, y=25)
        
        Label(self, text="Yaw").place(x=5, y=50)
        self.label_yaw = Label(self, text="0.00")
        self.label_yaw.place(x=60, y=50)
        
        Label(self, text="Throttle").place(x=5, y=70)
        self.label_thrust = Label(self, text="0.00")
        self.label_thrust.place(x=60, y=70)
        
        self.canvas1 = Canvas(self, bg="#ddd", width=150, height=150)
        self.canvas1.place(x=395, y=25)
        
        self.canvas2 = Canvas(self, bg="#eee", width=340, height=280)
        self.canvas2.place(x=300, y=200)
        
        self.pack(fill=BOTH, expand=1)
        
    def onClose(self):
        self.closeRequest = True
        
    def drawCanvas1(self, status):
        self.canvas1.delete("all")
        
        max = 30.
        x = (status.roll / max) * 75 + 76
        y = (status.pitch / max) * 75 + 76
        
        w0 = 2
        w10 = 75 * 1 / 3.
        w20 = 75 * 2 / 3. 
        w30 = 75 * 3 / 3.
        self.canvas1.create_line(76, 0, 76, 150, fill="#bbb")
        self.canvas1.create_line(0, 76, 150, 76, fill="#bbb")
        self.canvas1.create_oval(76 - w0, 76 - w0, 76 + w0, 76 + w0, outline="#bbb")
        self.canvas1.create_oval(76 - w10, 76 - w10, 76 + w10, 76 + w10, outline="#bbb")
        self.canvas1.create_oval(76 - w20, 76 - w20, 76 + w20, 76 + w20, outline="#bbb")
        self.canvas1.create_oval(76 - w30, 76 - w30, 76 + w30, 76 + w30, outline="#bbb")
        
        self.canvas1.create_oval(x - 4, y - 4, x + 4, y + 4, fill="#000")
        
    
    def drawCanvas2(self, status):
        self.canvas2.delete("all")
        
        w = 40
        w2 = 80
        self.canvas2.create_rectangle(0 * w2, 0, w + 0 * w2, 200, outline="#aaa")
        self.canvas2.create_rectangle(1 * w2, 0, w + 1 * w2, 200, outline="#aaa")
        self.canvas2.create_rectangle(2 * w2, 0, w + 2 * w2, 200, outline="#aaa")
        self.canvas2.create_rectangle(3 * w2, 0, w + 3 * w2, 200, outline="#aaa")
        
        pixel_M1 = (status.motor_1 / 60000.) * 200
        pixel_M2 = (status.motor_2 / 60000.) * 200
        pixel_M3 = (status.motor_3 / 60000.) * 200
        pixel_M4 = (status.motor_4 / 60000.) * 200
        
        self.canvas2.create_rectangle(0 * w2, 200 - pixel_M1, w + 0 * w2, 200, fill="#0f0", outline="#0f0")
        self.canvas2.create_rectangle(1 * w2, 200 - pixel_M2, w + 1 * w2, 200, fill="#0f0", outline="#0f0")
        self.canvas2.create_rectangle(2 * w2, 200 - pixel_M3, w + 2 * w2, 200, fill="#0f0", outline="#0f0")
        self.canvas2.create_rectangle(3 * w2, 200 - pixel_M4, w + 3 * w2, 200, fill="#0f0", outline="#0f0")
    
        self.canvas2.create_rectangle(75, 230, 275, 270, outline="#aaa")
        pixel_bat = (status.bat / 4.) * 200
        self.canvas2.create_rectangle(75, 230, 75 + pixel_bat, 270, fill="#0f0", outline="#0f0")

    
    def run(self):
        while self.closeRequest == False:
            fc = flight.getFlightController()
            
            self.label_pitch.config(text="%2.2f" % fc.pitch)
            self.label_roll.config(text="%2.2f" % fc.roll)
            self.label_yaw.config(text="%2.2f" % fc.yawrate)
            self.label_thrust.config(text="%2.2f" % fc.throttle)
            
            self.drawCanvas1(flight.getCFStatus())
            self.drawCanvas2(flight.getCFStatus())
            
            time.sleep(0.05)
            
        self.quit()
        
def main():
    root = Tk()
    root.geometry("640x480-2500+50")
    app = Gui(root)
    root.protocol("WM_DELETE_WINDOW", app.onClose)
    root.mainloop()  


if __name__ == '__main__':
    controls.start()
    flight.init()
    
    main()  


#         canvas2 = Canvas(self)
#         canvas2.create_rectangle(30, 10, 120, 80, 
#             outline="#fb0", fill="#fb0")
#         canvas2.create_rectangle(150, 10, 240, 80, 
#             outline="#f50", fill="#f50")
#         canvas2.create_rectangle(270, 10, 370, 80, 
#             outline="#05f", fill="#05f")            
#         canvas2.pack(fill=BOTH, expand=1)
