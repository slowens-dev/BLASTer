import warnings
warnings.simplefilter('ignore')
import tkinter as tk
from tkinter import ttk, Text
from Bio.Blast import NCBIWWW,NCBIXML
from Bio import SearchIO
FONT = ('verdana', 16)

BOXquery = None
BOXstring = ''

####GUI####
class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, 'BLASTer')
        container = tk.Frame(self)
        container.pack(side='top',fill='both',expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0,weight=1)

        self.frames= {}
        
        PAGES = (StartPage, FastaPage, SeqIDPage)
        for F in PAGES:           
            frame = F(container,self)
            self.frames[F] = frame
            frame.grid(row=1,column=0,sticky='nsew')
        self.show_frame(StartPage)
        
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

        
class FastaPage(tk.Frame):
    
    def __init__(self, parent, controller):
        filepath = tk.StringVar()
        database = tk.StringVar()
        database.set('nr')
        eVal = tk.StringVar()
        eVal.set(10.0)
        numHits = tk.StringVar()
        numHits.set(30)
        
        resultvar = ("A complete list of databases can be found at: \n ftp://ftp.ncbi.nlm.nih.gov/blast/db/")
        
        tk.Frame.__init__(self,parent)
        self.configure(background= 'blue')
        welcome = tk.Label(self, text = 'Enter a .FASTA filepath: ',font=FONT,background='yellow')
        welcome.grid(row = 0, column = 0)
        enterFilePath= tk.Entry(self, width = 20, background = 'yellow', textvariable= filepath)
        enterFilePath.grid(row = 0, column = 1,columnspan=2) 
        dbLabel = tk.Label(self,text='enter your database name: ', font=FONT,background='yellow')
        dbLabel.grid(row=0, column=3)
        dbEnter = tk.Entry(self, width = 20, background = 'yellow', textvariable = database)
        dbEnter.grid(row =0, column=4)
        eValEnter = tk.Entry(self, width=20, background='yellow',textvariable=eVal)
        eValLabel = tk.Label(self, text='Enter max E Value: ', font=FONT,background='yellow')

        numHitsLabel = tk.Label(self,text='Number of Hits to Display: ',font=FONT,background='yellow')
        numHitsEnter = tk.Entry(self, width =20, background = 'yellow', textvariable = numHits)

            
        eValEnter.grid(row=1,column=4)
        eValLabel.grid(row=1,column=3)
        numHitsEnter.grid(row=2,column=4)
        numHitsLabel.grid(row=2,column=3)

        result = Text(self, width = 100, height = 40,background='yellow')
        result.insert(0.0,resultvar)
    
        result.grid(row = 1, columnspan=3, rowspan = 4)
        result.grid_rowconfigure(2, weight=1)
        search = ttk.Button(self, text='Run BLAST search',
                        command= lambda: result.insert( '0.0', str( fastaFileBlast( self, parent, controller,filepath.get(), database.get(), eVal.get(), numHits.get()   ))+('\n'*10)    )  )
        search.grid(row=4, column = 3, columnspan = 2)

        allignButton = ttk.Button(self, text='show allignment',
                          command= lambda: self.result.insert('0.0', ('\n\n\n',allignShow(self, parent, controller,blastRecords[int(text)]) ) ) )

        #UTILS
        self.grid_rowconfigure(4,weight=1)
        gohome = ttk.Button(self, text="Return to Home Page",
                           command=lambda: controller.show_frame(StartPage))
        gohome.grid(row=5, column =0)

        goseqid = ttk.Button(self, text='Run BLAST using an NCBI GeneID',
                             command= lambda:controller.show_frame(SeqIDPage))
        goseqid.grid(row=5, column=1)
                   
        poweredby = tk.Label(self, text = 'Powered by BioPython, NCBI, TKinter', font=('verdana',12),background='yellow')
        poweredby.grid(row = 5, column = 4)

    
        
        

        
class SeqIDPage(tk.Frame):
    
    def __init__(self, parent, controller):
        
        seqID = tk.StringVar()
        database = tk.StringVar()
        database.set('nr')
        eVal = tk.StringVar()
        eVal.set(10.0)
        numHits = tk.StringVar()
        numHits.set(30)
        alignNum = tk.StringVar()
        alignNum.set('')
        
        resultvar = ("A complete list of databases can be found at: \n ftp://ftp.ncbi.nlm.nih.gov/blast/db/")
        
        tk.Frame.__init__(self,parent)
        self.configure(background= 'blue')

        result = Text(self, width = 100, height = 40,background='yellow')
        result.grid(row = 1, columnspan=3, rowspan = 5)
        result.grid_rowconfigure(2, weight=1)
        result.insert(0.0,resultvar)

        welcome = tk.Label(self, text = 'Enter an NCBI geneID #: ',font=FONT,background='yellow')
        welcome.grid(row = 0, column = 0)
        
        enterID= tk.Entry(self, width = 20, background = 'yellow', textvariable= seqID)
        enterID.grid(row = 0, column = 1,columnspan=2)
        
        dbLabel = tk.Label(self,text='enter your database name: ', font=FONT,background='yellow')
        dbLabel.grid(row=0, column=3)
        
        dbEnter = tk.Entry(self, width = 20, background = 'yellow', textvariable = database)
        dbEnter.grid(row =0, column=4)
        
        eValEnter = tk.Entry(self, width=20, background='yellow',textvariable=eVal)
        eValEnter.grid(row=1,column=4)

        eValLabel = tk.Label(self, text='Enter max E Value: ', font=FONT,background='yellow')
        eValLabel.grid(row=1,column=3)

        numHitsEnter = tk.Entry(self, width =20, background = 'yellow', textvariable = numHits)
        numHitsEnter.grid(row=2,column=4)
        
        numHitsLabel = tk.Label(self,text='Number of Hits to Display: ',font=FONT,background='yellow')
        numHitsLabel.grid(row=2,column=3)


        search = ttk.Button(self, text='Run BLAST search', 
                        command= lambda: result.insert( '0.0', str( seqIDBlast( self, parent, controller,seqID.get(), database.get(), eVal.get(), numHits.get()   ))+('\n'*10)    )  )
        search.grid(row=3, column = 3, columnspan = 2,pady=5)
        
        alignAllButton = ttk.Button(self, text='Show All Returned Alignments', 
                              command= lambda: result.insert('0.0', ('\n\n\n' + alignShow(self, parent, controller) + '\n\n\n' ) ) )               
        alignAllButton.grid(row=4, column = 3 ,sticky='n', columnspan= 2  )
        
        alignEntry = tk.Entry(self,width=20, background='yellow', textvariable = alignNum)
        alignEntry.grid(row=4, column=4,)

        alignLabel = tk.Label(self,text='Enter a Result# for full allignment', background = 'yellow', font=FONT)
        alignLabel.grid(row = 4,column=3)

        alignLabelButton = ttk.Button(self, text='Show Alignment', 
                                       command= lambda: result.insert('0.0', alignShowSpecific(self, parent, controller)) )
        alignLabelButton.grid(pady=(50,0),row=4, column=3, columnspan = 2)


            

       
 

        #UTILS
        self.grid_rowconfigure(4,weight=1)
        gohome = ttk.Button(self, text="Return to Home Page",
                           command=lambda: controller.show_frame(StartPage))
        gohome.grid(row=8, column =0)

        goseqid = ttk.Button(self, text='Run BLAST using a .FASTA file',
                             command= lambda:controller.show_frame(FastaPage))
        goseqid.grid(row= 8, column=1)
                   
        poweredby = tk.Label(self, text = 'Powered by BioPython, NCBI, TKinter', font=('verdana',12),background='yellow')
        poweredby.grid(row = 8, column = 4)

    
        
        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self,parent)
        tk.Frame.configure(self,background = 'blue')
        welcome = tk.Label(self, text = 'Welcome to \nBLASTer',font=FONT, background='yellow')
        welcome.pack(pady=10,padx=10)
        button = ttk.Button(self, text='Submit a .FASTA file',
                           command=lambda: controller.show_frame(FastaPage))
        button.pack()
        button2 = ttk.Button(self, text='Submit an NCBI Gene Sequence ID',
                            command=lambda: controller.show_frame(SeqIDPage))
        button2.pack()
        
        poweredby = ttk.Label(self, text = 'Powered by BioPython', font=('verdana',12))
        poweredby.pack()

####DATA####

    
def fastaFileBlast(self, parent, controller, filepath, db, eVal, hits):

    fasta = open(filepath).read()#get fasta from the file
    resultHandle = NCBIWWW.qblast('blastn',db,fasta,hitlist_size = hits,expect = eVal)#get the results

    with open('blastData.xml', 'w') as writer:
        writer.write(resultHandle.read()) #writes to the file and empties resultHandle
    resultHandle.close()

    
    resultHandle = open('blastData.xml')#reloads resultHandle 
    blastRecords = NCBIXML.parse(resultHandle)#get the blast records in Record form
    blastRecords = list(blastRecords)

    blastQR = SearchIO.read('blastData.xml', 'blast-xml')#blast QueryResult object

    global BOX
    BOX = blastQR
    return BOX


def alignShow(self, parent, controller):
    global BOXstring
    count = 0
    resultHandle = open('blastData.xml')#reloads resultHandle 
    blastRecords = NCBIXML.parse(resultHandle)#get the blast records in Record form

    for record in blastRecords:
        for align in record.alignments:
            for hsp in align.hsps:
                   BOXstring += ('\n*****ALIGNMENT***** '+'\nResult#: '+str(count)+ '\nSequence: '+ str(align.title)+'\nLength: '+ str(align.length)+ '\nE Value: '+ str(hsp.expect)+'\n'+str(hsp.query[0:100])+'\n'+ str(hsp.match[0:100])+'\n'+str(hsp.sbjct[0:100]))
                   count += 1
    return( BOXstring)

def alignShowSpecific(self, parent, controller):
    resultHandle = open('blastData.xml')#reloads resultHandle 
    blastRecords = NCBIXML.parse(resultHandle)#get the blast records in Record form
    blastQR = SearchIO.read('blastData.xml', 'blast-xml')
    

    
def seqIDBlast(self, parent, controller, seqID, db, eVal, hits):

    resultHandle = NCBIWWW.qblast('blastn',db,str(seqID),hitlist_size = hits,expect = eVal)#get the results

    with open('blastData.xml', 'w') as writer:
        writer.write(resultHandle.read()) #writes to the file and empties resultHandle
    resultHandle.close()


    blastQR = SearchIO.read('blastData.xml', 'blast-xml')#blast QueryResult object
    global BOX
    BOX = blastQR
    return BOX
    
    


#MAIN#
app = App()
app.mainloop()
