from tkinter import *
from PIL import ImageTk,Image

root = Tk()
root.title('Duplicate Finder')
root.iconbitmap('facicon.ico')


root.geometry('550x500')


img = Image.open('Amazon_logo.jpg')                        #The PIL Image Object which will be passed inside the .PhotoImage method

resized_img = img.resize((100, 100))                        #The object got resized and will be transferred into the .PhotoImage()


photo = ImageTk.PhotoImage(image=resized_img)               #Display Image using PIL Object

img_label = Label(root, image=photo)                        # Pass the Tkinter PhotoImage, not PIL image
img_label.pack(pady=(10,10))

# --------------- Text Box --------------- #

user_name = Entry(root,width=30,bg = 'white')
user_name.pack(pady = 100)





root.configure(background='#232f3e')
root.mainloop()






