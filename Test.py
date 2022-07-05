from sqlite3 import Time
import matplotlib.pyplot as plt
import tkinter as tk
import numpy as np
import pandas as pd

window = tk.Tk()

window.title('Graph of Temperature Data')
window.geometry("400x500")


label = tk.Label(text="Smart Park Capsule", fg="white", bg="black", width="50", height="3")
label.pack()

frame = tk.Frame(master=window, width="1000", height="1000", bg="white")
frame.pack()    



label1 = tk.Label(master=frame, text="Parking Spot 1", width="30", height="15", bg="red")
label1.place(x=70, y=20)
    
label4 = tk.Label(master=frame,text="In_Time",width="10", height="2", bg="blue")
label4.place(x=70,y=300)
entry = tk.Entry()
In_Time = entry.get()
In_Time
'Time'
entry.pack()
label7 = tk.Label(master=frame,text="Out_Time",width="10", height="2", bg="blue")
label7.place(x=200,y=300)
entry = tk.Entry()
Out_Time = entry.get()
Out_Time
'Time'
entry.pack()


label3 = tk.Label(master=frame, text="Parking Spot 2", width="30", height="15", bg="yellow")
label3.place(x=400, y=20)
label5 = tk.Label(master=frame,text="In_Time",width="10", height="2", bg="blue")
label5.place(x=400,y=300)
entry = tk.Entry()
In_Time = entry.get()
In_Time
'Time'
entry.pack()
label8 = tk.Label(master=frame,text="Out_Time",width="10", height="2", bg="blue")
label8.place(x=550,y=300)
entry = tk.Entry()
Out_Time = entry.get()
Out_Time
'Time'
entry.pack()

label2 = tk.Label(master=frame, text="Parking Spot 2", width="30", height="15", bg="red")
label2.place(x=740, y=20)
label6 = tk.Label(master=frame,text="In_Time",width="10", height="2", bg="blue")
label6.place(x=740,y=300)
entry = tk.Entry()
In_Time = entry.get()
In_Time
'Time'
entry.pack()
label9 = tk.Label(master=frame,text="Out_Time",width="10", height="2", bg="blue")
label9.place(x=875,y=300)
entry = tk.Entry()
Out_Time = entry.get()
Out_Time
'Time'
entry.pack()

label10 = tk.Label(master=frame,text="Gate_Open_Time",width="25", height="2", bg="Green")
label10.place(x=425,y=400)
entry = tk.Entry()
Gate_Open_Time = entry.get()
Gate_Open_Time
'Time'
entry.pack()

#dataFrame = pd.read_csv('Kumpula-June-2016-w-metadata.txt', skiprows=8)
#print(dataFrame.columns)
#x = dataFrame['YEARMODA']
#y = dataFrame['TEMP']
#plt.plot(x=120, y=500)
#plt.show()
#gasPrice = pd.read_csv('gas_prices.csv')
#plt.plot(gasPrice.Year, gasPrice.Canada,'b.-',label = 'Canada',color='green')
#plt.plot(gasPrice.Year, gasPrice.USA,'b.-',label = 'USA',color='red')
#plt.suptitle('Gas Price Comparison')
#plt.title('Canada', fontdict={'fontsize':15,'fontweight':'bold'})
#plt.xlabel('Year')
#plt.ylabel('Price in USD')
#plt.xticks([1990,1992,1994,1996,1998,2000,2002,2004,2006,2008])
#plt.yticks([1,1.5,2,2.5,3,3.5,4])
#plt.legend()
#plt.figure(figsize=(10,12), dpi=100)
      

window.mainloop()