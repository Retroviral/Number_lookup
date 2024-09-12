from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from sqlite3 import *

ws = Tk()
ws.title("Supplier Search")
ws.geometry("600x600+300+50")
ws.resizable(0, 0)

conn = None

conn = connect("IMEI.db")

curs = conn.cursor()

def show():
    ws_ent.delete(0, END)
    ws_ent.focus()
    treeview.selection()
    conn = None
    try:
        conn = connect("IMEI.db")
        cursor = conn.cursor()
        db = "select * from IMEI"
        cursor.execute(db)

        fetchdata = treeview.get_children()
        for elements in fetchdata:
            treeview.delete(elements)

        data = cursor.fetchall()
        for d in data:
            treeview.insert("", END, values=d)

        conn.commit()
    except Exception as e:
        showerror("Fail", e)
        conn.rollback()
    finally:
        if conn is not None:
            conn.close()


def search():
    treeview.selection()
    fetchdata = treeview.get_children()
    for f in fetchdata:
        treeview.delete(f)
    conn = None
    try:
        conn = connect("IMEI.db")
        core = conn.cursor()
        db = "select * from IMEI where imei = '%s'"
        imei = ws_ent.get()
        ##if str(imei) > str(15) or (not imei.isalnum()):
          ##  showerror("fail", "Invalid IMEI")
        ##else:
        core.execute(db % imei)
        data = core.fetchall()
        for d in data:
            treeview.insert("", END, values=d)

    except Exception as e:
        showerror("issue", e)

    finally:
        if conn is not None:
            conn.close()


def reset():
    show()


scrollbarx = Scrollbar(ws, orient=HORIZONTAL)
scrollbary = Scrollbar(ws, orient=VERTICAL)
treeview = ttk.Treeview(ws, columns=("RNO", "IMEI", "Supplier", "Description"), show='headings', height=22)
treeview.pack()
treeview["displaycolumns"]=("2", "3")
treeview.heading('RNO', text="RNO", anchor=CENTER)
treeview.column("RNO", stretch=NO, width=100)
treeview.heading('IMEI', text="IMEI", anchor=CENTER)
treeview.column("IMEI", stretch=NO, width=100)
treeview.heading('Supplier', text="Supplier", anchor=CENTER)
treeview.column("Supplier", stretch=NO)
treeview.heading('Description', text="Description", anchor=CENTER)
treeview.column("Description", stretch=NO)
scrollbary.config(command=treeview.yview)
scrollbary.place(x=526, y=7)
scrollbarx.config(command=treeview.xview)
scrollbarx.place(x=220, y=460)
style = ttk.Style()
style.theme_use("default")
style.map("Treeview")

ws_lbl = Label(ws, text="IMEI", font=('calibri', 12, 'normal'))
ws_lbl.place(x=90, y=540)
ws_ent = Entry(ws, width=20, font=('Arial', 15, 'bold'))
ws_ent.place(x=155, y=540)
ws_btn1 = Button(ws, text='Search', width=8, font=('calibri', 12, 'normal'), command=search)
ws_btn1.place(x=395, y=540)
ws_btn2 = Button(ws, text='Reset', width=8, font=('calibri', 12, 'normal'), command=reset)
ws_btn2.place(x=505, y=540)

show()
ws.mainloop()
