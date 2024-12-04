from tkinter import *

root = Tk()

#test = Label(root, text="hello")
#test.pack()

width = root.winfo_screenwidth()
height = root.winfo_screenheight()-40
root.attributes("-alpha", 0.3)

root.overrideredirect(True)
root.geometry(str(width)+"x"+str(height))

root.mainloop()