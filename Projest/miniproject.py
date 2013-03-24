import os
import re
def menu(response):
    print "*"*80
    print "%s %60s"%("* PDB FILE ANALYZER","*")
    print "*"*80
    print "%s %49s"%("* Select an option from below:","*")
    print "*%79s"% "*"
    print "*      %s %25s %28s"% ("1) Open a PDB File","(O)","*")
    print "*      %s %28s"%("2) Information                           (I)","*")
    print "*      %s %28s"%("3) Show histogram of amino acids         (H)","*")
    print "*      %s %28s"%("4) Display Secondary Structure           (S)","*")
    print "*      %s %28s"%("5) Manipulate Helix or Sheet             (M)","*")
    print "*      %s %28s"%("6) Export PDB File                       (X)","*")
    print "*      %s %28s"%("7) Exit                                  (Q)","*")
    print "*%79s"%("*")
    print "*", "Current PDB:%s *".rjust(78," ") % (response)
    print "*"*80

def validatepath():
    flag = True
    while flag:
        paths = raw_input("Enter a valid PATH for a PDB file: ")
        if os.path.exists(paths)and os.path.isfile(paths):
          flag = False
    else:
        return paths

def validatePDB(paths):
    PDBfile=open(paths,"r")
    header = PDBfile.read(6)
    while header!="HEADER":
        paths = validatepath()
        PDBfile=open(paths,"r")
        header = PDBfile.read(6)
    else:
        return PDBfile
def optionO(currentPDB = None):
    if currentPDB != validatepath():
        currentPDB = validatepath()
        PDBfile=validatePDB(currentPDB)
        print "The File %s has been successfully loaded" %currentPDB
    else:
        ans = raw_input("Do you want to replace ? y or n ")
        if ans.lower == "y":
            currentPDB = validatepath()
            PDBfile=validatePDB(currentPDB)
            print "The File %s has been successfully loaded" %currentPDB
        else:
            currentPDB = currentPDB
            PDBfile=validatePDB(currentPDB)
            print "The File %s has been successfully loaded" %currentPDB
    return currentPDB
##need to solve the problem of availability of variables
#pending:   confirmng replacement of present file
#################INFORMATION DSPLAY########################################             
def add_to_PDBdict(PDB,key,seq):
    PDB[key]=seq
    return PDB
#
def parselen(string,noperline,indentation=0):
    seq = ""
    i = 0
    while i <len(string):
        seq+= " "*indentation+string[i:i+noperline]+"\n"
        i += noperline
    return seq

def extractTitle(PDBfile):
    PDBfile.seek(0)
    title = "Title: "
    for line in PDBfile:
        if line.startswith("TITLE"):
            title += line[10:80].rstrip()
    return title

def extractHelix(PDBfile):
    title = "Title: "
    for line in PDBfile:
        if line.startswith("TITLE"):
            title += line[10:80].rstrip()
    return title

def countHelix(PDBfile,char):
    PDBfile.seek(0)
    count = 0
    for line in PDBfile:
        if line.startswith("HELIX")and line[31]==char:
            count+=1
    return count
def countSheet(PDBfile,char):
    PDBfile.seek(0)
    count = 0
    for line in PDBfile:
        if line.startswith("SHEET")and line[32]==char:
            count+=1
    return count
def extractSeq(PDBfile,char):
    PDBfile.seek(0)
    seq=""
    for line in PDBfile:
        if line.startswith("SEQRES")and line[11]==char:
            seq+=line[18:70]
    return seq
def oneto3(seq,dict):
    oneaa = ""
    for i in seq:
        if i !="":
            oneaa+=dict[i]
    return oneaa
def parseSequence(sequence,numberperline,indentation=0):
	seq=""
	index=0
	while index<len(sequence):
		seq += " "*indentation +sequence[index:index+numberperline] + "\n"
		index +=numberperline
	return seq
def ectractSheetInfo():
    PDBfile.seek(0)
    sheetLists =[]
    for line in PDBfile:
        if line.startswith("SHEET"):
            sheetLists +=[[["strand:",line[8:10].strip()],["sheetID:",line[12:14].strip()],
                       ["numStrands",int(line[15:16])],["initResName:",line[17:20].strip()],
                       ["initChainID:",line[21:22].strip()],
                      ["initSeqNum:",int(line[23:26].strip())],["initICode:",line[26:27].strip()],
                      ["endResName:",line[27:31].strip()],["endChainID:",line[32:33].strip()],
                      ["endSeqNum:",int(line[34:37].strip())],["endICode:",line[37:38].strip()],
                      ["sense:",line[39:40].strip()],["curAtom:",line[42:45].strip()],
                       ["curResName:",line[45:48].strip()],["curChainId:",line[49:50].strip()],
                    ["curResSeq:",line[51:54].strip()],["curIcode:",line[54:55].strip()],
                      ["prevAtom:",line[57:60].strip()],["prevResName:",line[60:63].strip()],
                       ["prevChainId:",line[64:65].strip()],["prevResSeq:",line[66:69].strip()],
                       ["prevICode:",line[69:70].strip()]],]
    return sheetLists
def extractHelixInfo():
    PDBfile.seek(0)
    helixLists =[]
    for line in PDBfile:
        if line.startswith("HELIX"):
            helixLists +=[[["serNum:",int(line[8:10].strip())],["helixID:",int(line[12:14].strip())],
                      ["initResName:",line[15:18].strip()],["initChainID:",line[19:20].strip()],
                      ["initSeqNum:",int(line[22:25].strip())],["initICode:",line[25:26].strip()],
                      ["endResName:",line[27:30].strip()],["endChainID:",line[31:32].strip()],
                      ["endSeqNum:",int(line[34:37].strip())],["endICode:",line[37:38].strip()],
                      ["helixClass:",int(line[39:40].strip())],["comment:",line[41:70].strip()],
                      ["length:",int(line[72:76].strip())]],]
    return helixLists

def optionI():
    print "PDB file: %s"% currentPDB
    title = extractTitle(PDBfile)
    seq= parseSequence(title,80).rstrip()
    print seq
    print "CHAINS: A and B"
    print " - chain A"
    PDB ={}
    PDB =add_to_PDBdict(PDB,"Title",seq)
    seqA= extractSeq(PDBfile,"A")
    PDB =add_to_PDBdict(PDB,"ThreeSeqA",seqA.rstrip())
    seqA = oneto3(seqA.split(" "),threeTO1)
    print "   Number of Amino acids:  ",len(seqA)
    print "   Number of helix:          ",countHelix(PDBfile,"A")
    print "   Number of sheet:          ",countSheet(PDBfile,"A")
    print "   Sequence:  ",parseSequence(seqA,50,14)
    print " - chain B"
    seqB= extractSeq(PDBfile,"B")
    PDB =add_to_PDBdict(PDB,"ThreeSeqB",seqB.rstrip())
    seqB = oneto3(seqB.split(" "),threeTO1)
    print "   Number of Amino acids:  ",len(seqB)
    print "   Number of helix:         ",countHelix(PDBfile,"B")
    print "   Number of sheet:         ",countSheet(PDBfile,"B")
    print "   Sequence:  ",parseSequence(seqB,50)
    PDB =add_to_PDBdict(PDB,"SequenceA",seqA)
    PDB =add_to_PDBdict(PDB,"SequenceB",seqB)
    #return PDB
def PDBDict():
    #print "PDB file: %s"% currentPDB
    title = extractTitle(PDBfile)
    seq= parseSequence(title,80).rstrip()
    #print seq
    #print "CHAINS: A and B"
    #print " - chain A"
    PDB ={}
    PDB =add_to_PDBdict(PDB,"Title",seq)
    seqA= extractSeq(PDBfile,"A")
    PDB =add_to_PDBdict(PDB,"ThreeSeqA",seqA.rstrip())
    seqA = oneto3(seqA.split(" "),threeTO1)
    #print "   Number of Amino acids:  ",len(seqA)
    #print "   Number of helix:          ",countHelix(PDBfile,"A")
    #print "   Number of sheet:          ",countSheet(PDBfile,"A")
    #print "   Sequence:  ",parseSequence(seqA,50,14)
    #print " - chain B"
    seqB= extractSeq(PDBfile,"B")
    PDB =add_to_PDBdict(PDB,"ThreeSeqB",seqB.rstrip())
    seqB = oneto3(seqB.split(" "),threeTO1)
    #print "   Number of Amino acids:  ",len(seqB)
    #print "   Number of helix:         ",countHelix(PDBfile,"B")
    #print "   Number of sheet:         ",countSheet(PDBfile,"B")
    #print "   Sequence:  ",parseSequence(seqB,50)
    PDB =add_to_PDBdict(PDB,"SequenceA",seqA)
    PDB =add_to_PDBdict(PDB,"SequenceB",seqB)
    return PDB                       

##########################HISTOGRAM OF AMINO ACIDS###########################
def sort_by(seq,i,sort):
        seq = sorted(seq, key=lambda x: x[i], reverse = sort)            
        for i in seq:
            if i[1] !=0:
                print "%s (%3i) : %s"% (i[0],i[1],"*"*i[1])
def optionH():
    print '''Choose an option to order by: 
      number of amino acids - ascending  (an)
      number of amino acids - descending (dn)
      alphabetically - ascending         (aa)
      alphabetically - descending        (da)'''
    count_of_aa=[]
    List_of_aa= ["Ala","Arg","Asn","Asp","Asx","Cys","Gln","Glu","Glx","Gly","His",
          "Ile","Leu","Lys","Met","Phe","Pro","Ser","Thr","Trp","Tyr","Val"]
    sequence = PDB['ThreeSeqA']+PDB['ThreeSeqB']
    for i in List_of_aa:
        count=sequence.count(i.upper())
        count_of_aa+=[(i,count)] # list of tuple to store count of aa
    response =raw_input("order by: ")
    while response !="":
        if response.lower() == "an":
            sort_by(count_of_aa,0,False)
            response =raw_input("order by: ")
        if response.lower() == "dn":
            sort_by(count_of_aa,0,True)
            response =raw_input("order by: ")
        if response.lower() == "aa":
            sort_by(count_of_aa,1,False)
            response =raw_input("order by: ")
        if response.lower() == "da":
            sort_by(count_of_aa,0,True)
            response =raw_input("order by: ")

############################DISPLAY SECONDARY STRUCTURE####################

def extractSrtA():
    chainA = {}
    HelixA =[]
    SheetA = []
    for i in helixSheets["Helix"]:
        if i[3][1]=="A":
            HelixA += [[str(i[1][1]),i[4][1],i[8][1]]]
    for i in helixSheets["Sheet"]:
        if i[4][1]=="A":        
            SheetA += [[str(i[0][1])+str(i[1][1]),i[5][1],i[9][1]]]
        chainA["HelixA"]=HelixA
        chainA["SheetA"]=SheetA
    return chainA

def extractSrtB():
    chainB = {}
    HelixB =[]
    SheetB = []
    for i in helixSheets["Helix"]:
        if i[3][1]=="B":
            HelixB += [[str(i[1][1]),i[4][1],i[8][1]]]
    for i in helixSheets["Sheet"]:
        if i[4][1]=="B":        
            SheetB += [[str(i[0][1])+str(i[1][1]),i[5][1],i[9][1]]]
        chainB["HelixB"]=HelixB
        chainB["SheetB"]=SheetB
    return chainB
def parselen2(string,noperline,indentation=0):
    seq = ()
    i = 0
    while i <len(string):
        seq+= (" "*indentation+string[i:i+noperline]+"\n",)
        i += noperline
    return seq
def chain(Chain,Helix,Sheet,seq):
    s = "|"
    h = "/"
    helix =[]
    sheet =[]
    secStructure = ""
    tagid = ""
    taglist=[' ']*len(seq)
    structure=["-"]*len(seq)
    for i in Chain[Sheet]:
        a=(i[1]-1)
        b=i[2]
        structure[a:b] = s*((b-a))
    for i in Chain[Helix]:
        a=(i[1]-1)
        b=i[2]
        structure[a:b] = h*((b-a))
    for i in Chain[Sheet]:
        a=(i[1]-1)
        b=i[2]
        taglist[a:a+2] = i[0]
    for i in Chain[Helix]:
        a=(i[1]-1)
        taglist[a:a+1] = i[0]
    for i in structure:
        secStructure += i.strip()
    for i in taglist:
        tagid += i
    labels =parselen2(tagid,80,indentation=0)
    structure=parselen2(secStructure,80,indentation=0)
    sequences=parselen2(seq,80,indentation=0)
    for i, j, k in zip(sequences,structure,labels):
        print i,j,k
def optionS():
    print "Secondary structure of the PDB id %s " % currentPDB[:4] 
    print "Chain A"
    print "(1)"
    ChainB=extractSrtB()
    SequenceB =PDB["SequenceB"]
    ChainA = extractSrtA()
    SequenceA =PDB["SequenceA"]
    chain(ChainA,"HelixA","SheetA",SequenceA)
    print "(%s)" %len(SequenceA)
    print
    print "Chain B"
    print "(1)"
    chain(ChainB,"HelixB","SheetB",SequenceB)
    print "(%s)" %len(SequenceB)


#####################################MANIPULATE HELIX OR SHEET########################
def countHelix(PDBfile,char): #use this to save the count of helix 
    PDBfile.seek(0)
    count = 0
    for line in PDBfile:
        if line.startswith("HELIX")and line[31]==char:
            count+=1
    return count
def countSheet(PDBfile,char):
    PDBfile.seek(0)
    count = 0
    for line in PDBfile:
        if line.startswith("SHEET")and line[32]==char:
            count+=1
    return count
def edit(response,feature,action="edited"):
    if int(response)==int(response): #convert this as a function
        n= int(response)-1
        Helix= helixSheets[feature][n] #exraxt lists for Helix
        Helix[3][1]=raw_input(Helix[3][0]+str(Helix[3][1])) #chainID
        Helix[4][1]=int(raw_input(Helix[4][0][:-1]+"["+str(Helix[4][1])+"]: "))#initSeqqNo
        Helix[2][1]=oneTo3[sequence[(int(Helix[4][1])-1)]]#extract sequence name from dictionary
        print "The position corresponds to amino acid",Helix[2][1]
        Helix[8][1]=int(raw_input(Helix[8][0][:-1]+"["+str(Helix[8][1])+"]: "))
        Helix[6][1]=oneTo3[sequence[(int(Helix[8][1])-1)]]
        print "The position corresponds to amino acid",Helix[6][1]
        Helix[12][1]=(Helix[8][1])-(Helix[4][1])
        Helix[10][1]=int(raw_input(Helix[10][0][:-1]+"["+str(Helix[10][1])+"]: "))
        n=Helix[10][1]
        print "The selected class was:",helixClass[n] #work on function to change the class and insert here
        Helix[11][1]=raw_input(Helix[11][0][:-1]+"["+str(Helix[11][1])+"]: ")
        print "The helix", int(response)," has been successfully", action
    return Helix
def editsheet(response,feature,action="edited"):
    if int(response)==int(response): #convert this as a function
        n= int(response)-1
        Sheet= helixSheets[feature][n] #exraxt lists for Helix
        Sheet[4][1]=raw_input(Sheet[4][0]+str(Sheet[4][1])) #chainID
        Sheet[5][1]=int(raw_input(Sheet[5][0][:-1]+"["+str(Sheet[5][1])+"]: "))#initSeqqNo
        Sheet[3][1]=oneTo3[sequence[(int(Sheet[5][1])-1)]]#extract sequence name from dictionary
        print "The position corresponds to amino acid",Sheet[3][1]
        Sheet[9][1]=int(raw_input(Sheet[9][0][:-1]+"["+str(Sheet[9][1])+"]: "))
        Sheet[7][1]=oneTo3[sequence[(int(Sheet[9][1])-1)]]
        print "The position corresponds to amino acid",Sheet[7][1]
        print "The Sheet", int(response)," has been successfully", action
    return Sheet
def confirmS(n):
    PDBfile.seek(0)
    for line in PDBfile:
        if line.startswith("SHEET") and line[9]==str(n) and (line[13]=="B" or line[13]=="C"):
            return line
def confirmH(n):
    PDBfile.seek(0)
    for line in PDBfile:
        if line.startswith("HELIX") and line[9]==str(n):
            return line

def optionL():
    response =raw_input("Do you want to list the Helix (H) or the Sheet (S): ")
    while response!="":
        if response.upper() == "S":
            n = 1
            l=len(sheetLists)
            for i in sheetLists:
                print "Helix"+str(n)+"of"+str(l)+":"
                for j in i:
                    print "  %-13s %s"% (j[0],str(j[1]).strip())
                n +=1
            response =raw_input("Do you want to list the Helix (H) or the Sheet (S): ")
        elif response.upper() == "H":
            n = 1
            l=len(helixLists)
            for i in range(len(helixLists)):
                print "Helix"+str(n)+"of"+str(l)+":"
                #if helixLists[i][10][1]=='1':
                    #helixLists[i][10][1]="Right-handed alpha" #incororate the
                for j in helixLists[i]:
                    if j[0] =="helixClass:":
                        j[1]=helixClass[int(j[1])] #this changes the value at printing-sort it
                    print "  %-13s %s"% (j[0],str(j[1]).strip())
                n +=1
            response =raw_input("Do you want to list the Helix (H) or the Sheet (S): ")
    else:
        print "Choose one of the Manipulation Options:\nList(L) Edit(E) New(N) Remove(R) Main Menu(M)"
##        return helixSheets
def optionE():
    feature=raw_input("Do you want to edit a Helix (H) or a Sheet (S): ")
    while feature!="":
        if feature.upper()=="H":
            feature="Helix"
            response=raw_input("Which Helix do you want to edit 1-"+str(len(helixSheets["Helix"])))
            while response!="":
                Helix=edit(response,feature)
                response=raw_input("Which Helix do you want to edit (1-"+str(len(helixSheets["Helix"])))
            else:
                feature=raw_input("Do you want to edit a Helix (H) or a Sheet (S): ")
        elif feature.upper()=="S":
            feature="Sheet"
            response=raw_input("Which Sheet do you want to edit 1-"+str(len(helixSheets["Sheet"])))
            while response!="":
                Sheet=editsheet(response,feature)
                response=raw_input("Which sheet do you want to edit (1-"+str(len(helixSheets["Sheet"]))+"): ")
    else:
            #feature=raw_input("Do you want to edit a Helix (H) or a Sheet (S): ")
        print "Choose one of the Manipulation Options:"
        return helixSheets

def optionN():
    response=raw_input("Do you want to add a Helix (H) or a Sheet (S): ")
    while response!="":
        if response.upper()=="H":
            n=len(helixSheets["Helix"])+1
            helixSheets["Helix"]+=[[["serNum:",int(n)],["helixID:",int()],
                                  ["initResName:",""],["initChainID:","A"],
                                  ["initSeqNum:",int(1)],["initICode:",None],
                                  ["endResName:",None],["endChainID:",None],
                                  ["endSeqNum:",None],["endICode:",None],
                                  ["helixClass:",int(1)],["comment:",""],
                                  ["length:",int(1)]]]
            response=len(helixSheets["Helix"])
            feature= "Helix"
            Helix=edit(response,feature,"created")
            response=raw_input("Do you want to add a Helix (H) or a Sheet (S): ")
            #return helixSheets
        elif response.upper()=="S":
            helixSheets["Sheet"] +=[[["strand:",None],["sheetID:",None],
                                       ["numStrands",None],["initResName:",None],
                                       ["initChainID:",None],
                                      ["initSeqNum:",int(1)],["initICode:",None],
                                      ["endResName:",None],["endChainID:",None],
                                      ["endSeqNum:",int(1)],["endICode:",None],
                                      ["sense:",None],["curAtom:",None],
                                       ["curResName:",None],["curChainId:",None],
                                    ["curResSeq:",None],["curIcode:",None],
                                      ["prevAtom:",None],["prevResName:",None],
                                       ["prevChainId:",None],["prevResSeq:",None],
                                       ["prevICode:",None]]]
            response=len(helixSheets["Sheet"])
            feature= "Sheet"
            Helix=editsheet(response,feature,"created")
            response=raw_input("Do you want to add a Helix (H) or a Sheet (S): ")
            
    else:
        print "Choose one of the Manipulation Options:\nList(L) Edit(E) New(N) Remove(R) Main Menu(M)"
        return helixSheets
         
def optionR():
    response=raw_input("Do you want to remove a Helix (H) or a Sheet (S): ")
    while response!="":
        if response.upper()=="H":
            response=raw_input("Which Helix do you want to delete (1-"+str(len(helixSheets["Helix"]))+"): ")
            n=int(response)-1
            a=confirmH(n)
            while response!="":
                response=raw_input("Are you sure do you want to delete the helix? \n"+str(a)+"\n Y/N? ")
                if response.upper()=="Y":
                    helixSheets["Helix"].remove(helixSheets["Helix"][n])
                    print "Helix",int(n)+1,"successfully removed"
                    print "All serial numbers have been updated"
                    response=raw_input("Which Helix do you want to delete (1-"+str(len(helixSheets["Helix"]))+"): ")
            response=raw_input("Do you want to remove a Helix (H) or a Sheet (S): ")
        elif response.upper() =="S":
            response=raw_input("Which Sheet do you want to delete (1-"+str(len(helixSheets["Sheet"]))+"): ")
            while response!="":
                if int(response)==int(response):
                    n=int(response)-1
                    a=confirmS(n)
                    print a
                    response=raw_input("Y/N? ")
                    if response.upper()=="Y":
                        helixSheets["Sheet"].remove(helixSheets["Sheet"][n])
                        response=response=raw_input("Which Sheet do you want to delete (1-"+str(len(helixSheets["Sheet"]))+"): ")
            response=raw_input("Do you want to remove a Helix (H) or a Sheet (S): ")
    else:
        print "Choose one of the Manipulation Options: "
        return helixSheets

def writeToFile():
    PDBfile.seek(0)
    path = raw_input("Filepath: ")
    new = open(path, "w")
    n=1  
    for line in PDBfile:
        if line.startswith("HEADER"):
            line = line[1:51]+"23/3/2013"+line[60:]
            new.write(line)
        elif line.startswith("HELIX") and line[9]==str(n):
            if n<len(helixSheets["Helix"])+1:
                line = "HELIX %4s %3s %1s %1s %2s %s %s %s %s %2s %2s %34s %s \n"%(str(helixSheets["Helix"][n-1][0][1]),str(helixSheets["Helix"][n-1][1][1]),
                                                                             str(helixSheets["Helix"][n-1][2][1]),str(helixSheets["Helix"][n-1][3][1]),
                                                                             str(helixSheets["Helix"][n-1][4][1]),str(helixSheets["Helix"][n-1][5][1]),
                                                                             str(helixSheets["Helix"][n-1][6][1]),str(helixSheets["Helix"][n-1][7][1]),
                                                                             str(helixSheets["Helix"][n-1][8][1]),str(helixSheets["Helix"][n-1][9][1]),
                                                                            str(helixSheets["Helix"][n-1][10][1]),str(helixSheets["Helix"][n-1][11][1]),
                                                                            str(helixSheets["Helix"][n-1][12][1]))
                new.write(line)
                n+=1
        elif line.startswith("SHEET") and line[9]==str(n):
            if n<len(helixSheets["Sheet"]):
                line = "SHEET    %4s %3s %1s %1s %2s %s %s %s %s %s %s %2s %2s  %s %s %2s %s %s %s %2s %2s %s \n"%(str(helixSheets["Sheet"][0][0][1]),str(helixSheets["Sheet"][n][1][1]),
                                    str(helixSheets["Sheet"][n][2][1]),str(helixSheets["Sheet"][n-1][3][1]),str(helixSheets["Sheet"][n-1][4][1]),
                                    str(helixSheets["Sheet"][n-1][5][1]),str(helixSheets["Sheet"][n-1][6][1]),str(helixSheets["Sheet"][n-1][7][1]),
                                    str(helixSheets["Sheet"][n-1][8][1]),str(helixSheets["Sheet"][n-1][9][1]),str(helixSheets["Sheet"][n-1][10][1]),
                                    str(helixSheets["Sheet"][n-1][11][1]),str(helixSheets["Sheet"][n-1][12][1]),str(helixSheets["Sheet"][n-1][13][1]),
                                    str(helixSheets["Sheet"][n-1][14][1]),str(helixSheets["Sheet"][n-1][15][1]),str(helixSheets["Sheet"][n-1][16][1]),
                                    str(helixSheets["Sheet"][n-1][17][1]),str(helixSheets["Sheet"][n-1][18][1]),str(helixSheets["Sheet"][n-1][19][1]),
                                    str(helixSheets["Sheet"][n-1][20][1]),str(helixSheets["Sheet"][n-1][21][1]))
                new.write(line)
                n+=1
        else:
            line=line
            new.write(line)

##############CORE PROGRAM##################################
currentPDB = None
menu(currentPDB)
response = raw_input(":")
while response!="":
    if response.upper() =="O":
        currentPDB=optionO()
        PDBfile=validatePDB(validatepath())
        menu(currentPDB)
        response = raw_input(":")
        helixSheets ={}
        helixLists=extractHelixInfo()
        sheetLists=ectractSheetInfo()
        helixSheets["Helix"]=helixLists
        helixSheets["Sheet"]=sheetLists
        threeTO1 ={'VAL':'V', 'ILE':'I', 'LEU':'L', 'GLU':'E', 'GLN':'Q',
                 'ASP':'D', 'ASN':'N', 'HIS':'H', 'TRP':'W', 'PHE':'F', 'TYR':'Y',
                'ARG':'R', 'LYS':'K', 'SER':'S', 'THR':'T', 'MET':'M', 'ALA':'A',
                'GLY':'G', 'PRO':'P', 'CYS':'C'}
        sequence='YNFFPRKPKWDKNQITYRIIGYTPDLDPETVDDAFARAFQVWSDVTPLRFSRIHDGEADIMINFGRWEHGDGYPFDGKDGLLAHAFAPGTGVGGDSHFDDDELWTLGKGVGYSLFLVAAHAFGHAMGLEHSQDPGALMAPIYTYTKNFRLSQDDIKGIQELYGASPD'
        oneTo3={'A': 'ALA', 'C': 'CYS', 'E': 'GLU', 'D': 'ASP', 'G': 'GLY', 'F': 'PHE', 'I': 'ILE', 'H': 'HIS',
            'K': 'LYS', 'M': 'MET', 'L': 'LEU', 'N': 'ASN', 'Q': 'GLN', 'P': 'PRO', 'S': 'SER', 'R': 'ARG',
            'T': 'THR', 'W': 'TRP', 'V': 'VAL', 'Y': 'TYR'}
        helixClass={1:"Right-handed alpha",2:"Right-handed omega",3:"Right-handed pi",4:"Right-handed gamma",
                5:"Right-handed 3 - 10",6:"Left-handed alpha",7:"Left-handed omega",8:"Left-handed gamma",
                9:"2 - 7 ribbon/helix",10:"Polyproline"}
        PDB=PDBDict()

    elif response.upper() == "I":
        optionI()
        menu(currentPDB)
        response = raw_input(":")

    elif response.upper() =="H":
        optionH()
        menu(currentPDB)    
        response = raw_input(":")

    elif response.upper() == "S":
        optionS()
        menu(currentPDB)    
        response = raw_input(":")

    elif response.upper()=="M":
        print "Choose one of the Manipulation Options: "
        print "List(L)  Edit(E)  New(N)  Remove(R)  Main Menu(M)"
        response = raw_input(":")
        while response!="":
            if response.upper() == "L":
                optionL()
                response =raw_input(":")#insert after calling the above function
            elif response.upper()=="E":
                helixSheets=optionE()
                response=raw_input("List(L) Edit(E) New(N) Remove(R) Main Menu(M")
            elif response.upper()=="N":
                helixSheets=optionN()
                response =raw_input(":")
            elif response.upper()=="R":
                helixSheets=optionR()
                response = raw_input("List(L) Edit(E) New(N) Remove(R) Main Menu(M):  ")

        else:
            menu(currentPDB)
            response=raw_input(":")
    elif response.upper()=="X":
        writeToFile()
        menu(currentPDB)    
        response = raw_input(":")

##    else:
##        menu(currentPDB)

        














"""if response.upper()=="M":
    print "Choose one of the Manipulation Options: "
    print "List(L)  Edit(E)  New(N)  Remove(R)  Main Menu(M)"
    response = raw_input(":")
    while response!="":
        if response.upper() == "L":
            response =raw_input("Do you want to list the Helix (H) or the Sheet (S): ")
            if response.upper() == "S":
                n = 1
                l=len(sheetLists)
                for i in sheetLists:
                    print "Helix"+str(n)+"of"+str(l)+":"
                    for j in i:
                        print "  %-13s %s"% (j[0],str(j[1]).strip())
                    n +=1
                    response =raw_input("Do you want to list the Helix (H) or the Sheet (S): ")
            elif response.upper() == "H":
                n = 1
                l=len(helixLists)
                for i in range(len(helixLists)):
                    print "Helix"+str(n)+"of"+str(l)+":"
                    if helixLists[i][10][1]=='1':
                        helixLists[i][10][1]="Right-handed alpha"
                    for j in helixLists[i]:
                        if j[0] =="helixClass:" and j[1]==1:
                            j[1]="Right-handed alpha"
                        print "  %-13s %s"% (j[0],str(j[1]).strip())
                    n +=1
            else:
                print "Choose one of the Manipulation Options:\nList(L) Edit(E) New(N) Remove(R) Main Menu(M)"
                response =raw_input(":")
        elif response.upper()=="E":
            feature=raw_input("Do you want to edit a Helix (H) or a Sheet (S): ")
            while feature!="":
                if feature.upper()=="H":
                    feature="Helix"
                    response=raw_input("Which Helix do you want to edit 1-"+str(len(helixSheets["Helix"])))
                    while response!="":
                        Helix=edit(response,feature)
                        response=raw_input("Which Helix do you want to edit (1-"+str(len(helixSheets["Helix"])))
                    else:
                        feature=raw_input("Do you want to edit a Helix (H) or a Sheet (S): ")
                elif feature.upper()=="S":
                    feature="Sheet"
                    response=raw_input("Which Sheet do you want to edit 1-"+str(len(helixSheets["Sheet"])))
                    while response!="":
                        Sheet=editsheet(response,feature)
                        response=raw_input("Which sheet do you want to edit (1-"+str(len(helixSheets["Sheet"]))+"): ")
                else:
                    #feature=raw_input("Do you want to edit a Helix (H) or a Sheet (S): ")
                    print "Choose one of the Manipulation Options:"
                    response=raw_input("List(L) Edit(E) New(N) Remove(R) Main Menu(M")
        elif response.upper()=="N":
            response=raw_input("Do you want to add a Helix (H) or a Sheet (S): ")
            while response!="":
                if response.upper()=="H":
                    n=len(helixSheets["Helix"])+1
                    helixSheets["Helix"]+=[[["serNum:",int(n)],["helixID:",int()],
                                          ["initResName:",""],["initChainID:","A"],
                                          ["initSeqNum:",int(1)],["initICode:",None],
                                          ["endResName:",None],["endChainID:",None],
                                          ["endSeqNum:",None],["endICode:",None],
                                          ["helixClass:",int(1)],["comment:",""],
                                          ["length:",int(1)]]]
                    response=len(helixSheets["Helix"])
                    feature= "Helix"
                    Helix=edit(response,feature,"created")
                    response=raw_input("Do you want to add a Helix (H) or a Sheet (S): ")
                elif response.upper()=="S":
                    helixSheets["Sheet"] +=[[["strand:",None],["sheetID:",None],
                                               ["numStrands",None],["initResName:",None],
                                               ["initChainID:",None],
                                              ["initSeqNum:",int(1)],["initICode:",None],
                                              ["endResName:",None],["endChainID:",None],
                                              ["endSeqNum:",int(1)],["endICode:",None],
                                              ["sense:",None],["curAtom:",None],
                                               ["curResName:",None],["curChainId:",None],
                                            ["curResSeq:",None],["curIcode:",None],
                                              ["prevAtom:",None],["prevResName:",None],
                                               ["prevChainId:",None],["prevResSeq:",None],
                                               ["prevICode:",None]]]
                    response=len(helixSheets["Sheet"])
                    feature= "Sheet"
                    Helix=editsheet(response,feature,"created")
                    response=raw_input("Do you want to edit a Helix (H) or a Sheet (S): ")
                else:
                    print "Choose one of the Manipulation Options:\nList(L) Edit(E) New(N) Remove(R) Main Menu(M)"
                    response =raw_input(":")
        elif response.upper()=="R":
            response=raw_input("Do you want to remove a Helix (H) or a Sheet (S): ")
            while response!="":
                if response.upper()=="H":
                    response=raw_input("Which Helix do you want to delete (1-"+str(len(helixSheets["Helix"]))+"): ")
                    n=int(response)-1
                    a=confirmH()
                    while response!="":
                        response=raw_input("Are you sure do you want to delete the helix? \n"+str(a)+"\n Y/N? ")
                        if response.upper()=="Y":
                            helixSheets["Helix"].remove(helixSheets["Helix"][n])
                            print "Helix",int(n)+1,"successfully removed"
                            print "All serial numbers have been updated"
                            response=raw_input("Which Helix do you want to delete (1-"+str(len(helixSheets["Helix"]))+"): ")
                    response=raw_input("Do you want to remove a Helix (H) or a Sheet (S): ")
                elif response.upper() =="S":
                    response=raw_input("Which Sheet do you want to delete (1-"+str(len(helixSheets["Sheet"]))+"): ")
                    while response!="":
                        if int(response)==int(response):
                            n=int(response)-1
                            a=confirmS()
                            print a
                            response=raw_input("Y/N? ")
                            if response.upper()=="Y":
                                helixSheets["Sheet"].remove(helixSheets["Sheet"][n])
                                response=response=raw_input("Which Sheet do you want to delete (1-"+str(len(helixSheets["Sheet"]))+"): ")
            else:
                print "Choose one of the Manipulation Options:"
                response = raw_input("List(L) Edit(E) New(N) Remove(R) Main Menu(M) ")
        elif response.upper()=="M":
            menu(currentPDB)
            response=raw_input(":")
        else:
            menu(currentPDB)
if response.upper()=="S":
    draw_structure()"""
                        
                               
                                                                       
                                                                           

 
