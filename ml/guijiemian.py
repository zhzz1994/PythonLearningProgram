import tkinter as tk

window = tk.Tk()
window.title('my window')
window.geometry('500x300')  #中间是字母x

# var = tk.StringVar()
# lab = tk.Label(window,textvariable=var,bg = 'green',font=('Arial',12),width = 15,height = 2)
# lab.pack()
# on_hit = False
# def hitme():
#     global on_hit
#     if on_hit == False:
#         on_hit = True
#         var.set('you hit me')
#     else:
#         on_hit = False
#         var.set('')
# buttun = tk.Button(window,text='hit it',width=15,height = 2,command=hitme)
# buttun.pack()

# ent = tk.Entry(window,show = 'z') #show=None
# ent.pack()
# def insertpoint():
#     var = ent.get()
#     text.insert('insert',var)
# def insertend():
#     var = ent.get()
#     text.insert('end',var)  #insert(1.1,var)
#
# buttun1 = tk.Button(window,text='insert point',width=15,height = 2,command=insertpoint)
# buttun1.pack()
# buttun2 = tk.Button(window,text='insert end',width=15,height = 2,command=insertend)
# buttun2.pack()
# text = tk.Text(window,height=2)
# text.pack()

# var1 = tk.StringVar()
# lab = tk.Label(window,textvariable=var1,bg = 'yellow',font=('Arial',12),width = 15,height = 4)
# lab.pack()

# def printselect():
#     value = listb.get(listb.curselection())
#     var1.set(value)
#
# butprit = tk.Button(window,text='print select',width=15,height = 2,command=printselect)
# butprit.pack()
#
# var2 = tk.StringVar()
# var2.set((11,22,33,44))
# listb = tk.Listbox(window,listvariable = var2)
# listitems = [1,2,3,4]
# for item in listitems:
#     listb.insert('end',item)
# listb.insert(1,'first')
# listb.pack()

def hit_me():

    tk.messagebox.showinfo(title='Hi', message='hahahaha')

    #tk.messagebox.showwarning(title='Hi', message='nononono')

    #tk.messagebox.showerror(title='Hi', message='No!! never')

    # print(tk.messagebox.askquestion(title='Hi', message='hahahaha'))   # return 'yes' , 'no'
    #
    # print(tk.messagebox.askyesno(title='Hi', message='hahahaha'))   # return True, False
    #
    # print(tk.messagebox.asktrycancel(title='Hi', message='hahahaha'))   # return True, False
    #
    # print(tk.messagebox.askokcancel(title='Hi', message='hahahaha'))   # return True, False
    #
    # print(tk.messagebox.askyesnocancel(title="Hi", message="haha"))     # return, True, False, None



tk.Button(window, text='hit me', command=hit_me).pack()

window.mainloop()