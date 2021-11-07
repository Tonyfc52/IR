from tkinter import *
from tkinter.ttk import *
#from tkinterweb import HtmlFrame
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


def analysis():
    ana = pd.read_csv('analysis.csv')
    for i in range(len(ana)):
        mytable.insert("", index=END, values=[
                       ana.iloc[i][0], ana.iloc[i][1], ana.iloc[i][2]])


def loadto(csvfile, numbername, textname, framename):
    dataread = pd.read_csv(csvfile)

    number = 'Number of tokens: '+str(len(dataread))
    numbername.insert('1.0', number)
    textname.insert('1.0', 'Top 5000 Words \t\t\t\tFreq \n')
    textname.insert(END, '-------------- \t\t\t\t---- \n')
    for i in range(5000):
        textname.insert(
            END, str(dataread.iloc[i][1])+'\t\t\t\t'+str(dataread.iloc[i][2])+'\n')
    # drawing
    fig = Figure(figsize=(6, 4), dpi=100)

    a = fig.add_subplot(111)
    a.set_title('Frequency distribution of All words')
    X = dataread.index
    Y = dataread['freq']
    a.plot(X, Y)
    canvas = FigureCanvasTkAgg(fig, master=framename)
    canvas.draw()
    canvas.get_tk_widget().pack(side=RIGHT, fill=BOTH, expand=YES)


root = Tk()
root.title('Frequency and stemming')
root.geometry("800x600+100+100")

notebook = Notebook(root)
frame1 = Frame()
frame2 = Frame()
frame3 = Frame()
frame4 = Frame()
notebook.add(frame1, text='Normal')
notebook.add(frame2, text='No stopwords')
notebook.add(frame3, text='PorterStem')
notebook.add(frame4, text='Analysis')
notebook.pack(padx=10, pady=10, fill=BOTH, expand=True)

# frame1內容
number1 = Text(frame1, height=1, width=45, font=('Calibri', 12))
content1 = Text(frame1, width=40, height=50, font=('Calibri', 12))
pic1 = Canvas(frame1, width=600, height=400)
number1.pack()
content1.pack(fill=BOTH, side=LEFT)
scroll1y = Scrollbar(frame1, command=content1.yview)
content1.configure(yscrollcommand=scroll1y.set)
scroll1y.pack(side=LEFT, fill=Y)

# frame2內容
number2 = Text(frame2, height=1, width=45, font=('Calibri', 12))
content2 = Text(frame2, width=40, height=50, font=('Calibri', 12))
pic2 = Canvas(frame2, width=600, height=400)
number2.pack()
content2.pack(fill=BOTH, side=LEFT)
scroll2y = Scrollbar(frame2, command=content2.yview)
content2.configure(yscrollcommand=scroll2y.set)
scroll2y.pack(side=LEFT, fill=Y)


# frame3內容
number3 = Text(frame3, height=1, width=45, font=('Calibri', 12))
content3 = Text(frame3, width=40, height=50, font=('Calibri', 12))
pic3 = Canvas(frame3, width=600, height=400)
number3.pack()
content3.pack(fill=BOTH, side=LEFT)
scroll3y = Scrollbar(frame3, command=content3.yview)
content3.configure(yscrollcommand=scroll3y.set)
scroll3y.pack(side=LEFT, fill=Y)


# frame4內容
Style().configure("Treeview.Heading", font=('Calibri', 12))
mytable = Treeview(
    frame4, columns=['A', 'B', 'C'], selectmode=NONE, show='headings', height=2, style="Treeview.Heading")

mytable.heading('#1', text='Stemmed')
mytable.heading('#2', text='Times')
mytable.heading('#3', text='Original Words')
mytable.column('#1', width=200, stretch=False)
mytable.column('#2', width=70, stretch=False)
mytable.column('#3', width=600)
mytable.pack(fill=BOTH, expand=True)

scroll4y = Scrollbar(mytable, orient='vertical', command=mytable.yview)
mytable.configure(yscrollcommand=scroll4y.set)
scroll4y.pack(side=RIGHT, fill=Y)


loadto('freq_normal.csv', number1, content1, frame1)
loadto('freq_nostop.csv', number2, content2, frame2)
loadto('freq_afterstem.csv', number3, content3, frame3)
analysis()

root.mainloop()
