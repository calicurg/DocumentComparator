# -*- coding: cp1251 -*-
import Tkinter as TK
import LightLinter as LL
#import AccsView as AV
#import DIView as DV

Accs = {
        0:[],
        1:[]
        }
        
        
AI = {}

SynDI = {}
TargetDI = {0:[], ### found sentlines [seinx, ls]
            1:[]  ### document structure
            }

SeinxSectDI = {}
SectSeinxxDI = {}
HeaderLI = []
ParamDI = {'ls':'',
           'start':0,
           'end':0
           }



##AV.Accs = Accs

fna = 'C:\\Il\\Amorpha\\Comparator\\CSV\\DepleraSynopsis.csv'
fi = open(fna, 'r')
rl = fi.readlines()
fi.close()
#print len(rl)
LL.TKDI['sc'] = {}

def See():

    
    inx = LL.TKDI['en']['start'].get()
    LL.TKDI['tx'][1].see(inx)    
    

def Search_primer():

    primer = LL.TKDI['tx'][0].get('1.0', TK.END)
    primer = primer.strip()
    primer.encode('utf-8')
    
#    print 'primer:', primer
    Inx = LL.TKDI['tx'][1].search(primer, '1.0', nocase=1)
#    print type(Inx)
#    print 'Inx:', '[', Inx, ']'
    EndOfStartInx = int(Inx.split('.')[1])
    EndOfEndInx = EndOfStartInx + len(primer)
    LineStart = Inx.split('.')[0]
    EndPos = LineStart+'.'+str(EndOfEndInx)
    LL.TKDI['tx'][1].tag_add(0, Inx, EndPos)
    LL.TKDI['tx'][1].tag_configure(0, foreground='red') #font='Arial 14')
    LL.TKDI['tx'][1].see(Inx)


def Highlight():

    start_inx = LL.TKDI['en']['start'].get()
    end_inx = LL.TKDI['en']['end'].get()
#    LL.TKDI['tx'][1].tag_add(0, '1.100', '1.200')
    LL.TKDI['tx'][1].tag_add(0, start_inx, end_inx)
    LL.TKDI['tx'][1].tag_config(0, foreground='red')


    

def ShowContext():

    LL.TKDI['tx'][1].delete('1.0', TK.END)
    LL.TKDI['tx'][1]['fg'] = 'white'
    cs = int(LL.TKDI['lx']['target'].curselection()[0])   
    sent = TargetDI[0][cs]
    found_seinx = sent[0]
    SectInx = SeinxSectDI[found_seinx]
    Seinxx = SectSeinxxDI[SectInx]

    header_sl = HeaderLI[(SectInx-1)]
    SectionTitle = header_sl[1].decode('cp1251').encode('utf-8')
    header_line = str(header_sl[0]) +'  '+SectionTitle
    LL.TKDI['en']['start'].delete(0, TK.END)
    LL.TKDI['en']['start'].insert(0, header_line)
    
    
#    print 'found_seinx = ',found_seinx

    lena = 0
    for seinx in Seinxx:
        ls = Accs[1][seinx]
        len_ls = len(ls)
##        print seinx
##        print ls
        try:
            ls = ls.decode('cp1251').encode('utf-8')
        except:
            pass
        ls += '. '
        LL.TKDI['tx'][1].insert(TK.END, ls)
    
    Search_primer()    
    

def GetHeaderSeinxx():

    Start = 35
    for y in range(1, len(HeaderLI)):
        SectSeinxxDI[y] = []
        sl = HeaderLI[y]
        header = sl[1]

        
        for seinx in range(Start, len(Accs[1])):
            rs = Accs[1][seinx] ## raw sent
            if header in rs or header.lower() in rs.lower():
                HeaderLI[y][2] = seinx
                try:
                    header = header.decode('cp1251').encode('utf-8')
                except:
                    pass
                    
                line = sl[0] +'__'+header
                LL.TKDI['lx']['target_sections'].insert(TK.END, line)

                Start = seinx
                
##                print x
##                print sl[0]
##                print header
##                print ''
##                print '========='
                break
            else:
                SeinxSectDI[seinx] = y
                SectSeinxxDI[y].append(seinx)
                
    print 'GetHeaderSeinxx: done'           

        


def ReadStructure():

    fna = 'C:\\Il\\Amorpha\\Comparator\\TextFiles\\ProtStructure.txt'
    fi = open(fna, 'r')
    rl = fi.readlines()
    fi.close()

    for ls in rl:
        sl = ls.split('	')
        HeaderLI.append(sl)
##        print sl[0]
##        print sl[1]
##        print ''
##        print '============================'

    print 'ReadStructure: done'


    


def SetSynopsisInxx():

    for y in range(35, 146):
        SeinxSectDI[y] = 'Синопсис'
        


def Find__sent():

    LL.TKDI['tx'][1].delete('1.0', TK.END)
    primer = LL.TKDI['tx'][0].get('1.0', TK.END)
    primer = primer.strip()
    primer = primer.encode('cp1251')
    print 'primer:', primer
    
##    tu_cs = LL.TKDI['lx']['target'].curselection()
##    print tu_cs
##    cs = ''
##    if len(tu_cs) ==  1:
##        cs = int(tu_cs[0]) + 2
##    elif len(tu_cs) ==  0:
##        cs = 0

    en_line = LL.TKDI['en']['target'].get()
    en_line = en_line.strip()
    if en_line == '':
        start = 0
    else:
        seinx = int(en_line.split('__')[0])
        start = seinx + 1
        
        
    for y in range(start, len(Accs[1])):
        rs = Accs[1][y] ## raw sent
        if primer in rs or primer.lower() in rs.lower():
            #LL.TKDI['lx']['target'].select_set(y)
            
            try:
                rs = rs.decode('cp1251').encode('utf-8')
            except:
                pass

            rs = str(y) +':  '+rs    
            
            LL.TKDI['tx'][1].insert(TK.END, rs)
            LL.TKDI['en']['target'].delete(0, TK.END)
            entry_line = LL.TKDI['lx']['target'].get(y)
            LL.TKDI['en']['target'].insert(0, entry_line)
            break
    
    

def ShowDocStructure():

    LL.TKDI['tx'][0].delete('1.0', TK.END)
    LL.TKDI['lx']['target_sections'].delete(0, TK.END)
    for ls in TargetDI[1]:
        ls = ls.strip()
        
        ls += '\n'
       # print ls
        LL.TKDI['tx'][0].insert(TK.END, ls)
        LL.TKDI['lx']['target_sections'].insert(TK.END, ls)
        
        

def AcceptDocStructure():

    TargetDI[1] = []
    line = LL.TKDI['tx'][0].get('1.0', TK.END)
    sl = line.split('. ')
    for ls in sl:
        TargetDI[1].append(ls)
        
    
    print 'AcceptDocStructure: done'

        
 
def Show_target_doc():

    for y in range(len(Accs[1])):
        ls = Accs[1][y]
        try:
            ls = ls.decode('cp1251').encode('utf-8')
        except:
            pass
            
        lxline = str(y) +'__'+ls
        LL.TKDI['lx']['target'].insert(TK.END, lxline)
        


def ReadProt():

    fna = 'C:\\Il\\Amorpha\\Comparator\\TextFiles\\TheProtocol.txt'
    fi = open(fna, 'r')
    line = fi.read()
    line = line.replace('.\n', '. ')
    rl = line.split('. ')
    fi.close()
    Accs[1] = []
    for ls in rl:
        ls = ls.strip()
        Accs[1].append(ls)



def ParseSynopsis():
    
    for line in rl:
        sl = line.split(';')
        descr = sl[0]
        descr = descr.strip()
        ls = sl[1]
        if descr != '':            
            if descr[-1] == ':':
                descr = descr[:-1]
                current_descr = descr    
            SynDI[current_descr] = [ls]
        else:
            SynDI[current_descr].append(ls)       
        
    AI['Syn'] = SynDI
    

def Fill__descriptors():
    for y in range(len(rl)):
        ls = rl[y]
        sl = ls.split(';')
        descr = sl[0]
        descr = descr.strip()
        if descr != '':
            #print descr
            Accs[0].append(descr)




def reflect_section(event):

    lxname = 'sections'
    cs = int(LL.TKDI['lx'][lxname].curselection()[0])
    si = LL.TKDI['lx'][lxname].get(cs)
#    print si
    LL.TKDI['en'][lxname].delete(0, TK.END)
    LL.TKDI['en'][lxname].insert(0, si)        

     
    LL.TKDI['lx']['ls'].delete(0, TK.END)
    
    
    section = si.encode('utf-8')
    array = AI['Syn'][section]
    LL.TKDI['tx'][0].delete('1.0', TK.END)
    for ls in array:
        #ls = ls.decode('cp1251').encode('utf-8')
        if '***' in ls:
            ls = ls.replace('***', ';')
        ls += '\n'
        LL.TKDI['tx'][0].insert(TK.END, ls)
        LL.TKDI['lx']['ls'].insert(TK.END, ls)

    line = LL.TKDI['tx'][0].get('1.0', TK.END)
    ParamDI['ls'] = line
    

def Find__ls():

#    primer = LL.TKDI['en']['ls'].get()
    LL.TKDI['tx'][1].delete('1.0', TK.END)
    LL.TKDI['tx'][1]['fg'] = 'green'
    primer = LL.TKDI['tx'][0].get('1.0', TK.END)
    primer = primer.strip()
    
    primer = primer.encode('cp1251')
#    print 'primer:', primer
    LL.TKDI['tx'][1].delete('1.0', TK.END)
    LL.TKDI['lx']['target'].delete(0, TK.END)
    TargetDI[0] = []
    for y in range(len(Accs[1])):
        ls = Accs[1][y]
        
        try:
            if primer in ls:

                sent = [y, ls]
                TargetDI[0].append(sent) 
                
                ls = ls.decode('cp1251').encode('utf-8')
                LL.TKDI['lx']['target'].insert(TK.END, ls)
                ls = str(y)+':  '+ls+'\n\n==================================\n\n'
                LL.TKDI['tx'][1].insert(TK.END, ls)
##                print ls
##                print ''
##                print '=================================='
        except:
            
            print 'Exception:'
            print 'y:', y
            print ls
            
##    print 'TargetDI[0]'
##    for sent in TargetDI[0]:
##        print sent[0], sent[1]
##        
##    print 'Find__ls: done'
    

def reflect_ls(event):

    if LL.TKDI['lx']['ls'].size() > 0:
        lxname = 'ls'
        cs = int(LL.TKDI['lx'][lxname].curselection()[0])
        si = LL.TKDI['lx'][lxname].get(cs)
        si = si.strip()
        if si[-1] == '.':
            si = si[:-1]
            
    #    print si
        LL.TKDI['en'][lxname].delete(0, TK.END)
        LL.TKDI['en'][lxname].insert(0, si)        

        LL.TKDI['tx'][0].delete('1.0', TK.END)
        LL.TKDI['tx'][0].insert(TK.END, si)

        ParamDI['ls'] = si
        ParamDI['start'] = 0
        ParamDI['end'] = 0

        LL.TKDI['sc'][0].set(0)
        LL.TKDI['sc'][1].set(0)

        ls = si
        sl = ls.split()
        lena = len(sl)
        LL.TKDI['sc'][0]['to'] = lena
        LL.TKDI['sc'][1]['to'] = lena
        

        Find__ls()


    
def reflect_tarsect(event):

    if LL.TKDI['lx']['target_sections'].size() > 0:
        lxname = 'target_sections'
        cs = int(LL.TKDI['lx'][lxname].curselection()[0])
        si = LL.TKDI['lx'][lxname].get(cs)
    #    print si
        LL.TKDI['en'][lxname].delete(0, TK.END)
        LL.TKDI['en'][lxname].insert(0, si)        

        LL.TKDI['lx']['target'].delete(0, TK.END)
        Seinxx = SectSeinxxDI[(cs + 2)]

        txls = ''
        for seinx in Seinxx:
            rs = Accs[1][seinx]
            try:
                rs = rs.decode('cp1251').encode('utf-8')
            except:
                pass
                     
            lxline = str(seinx)+'__'+rs
            LL.TKDI['lx']['target'].insert(TK.END, lxline)
            rs += '\n'
            txls += rs
         
        LL.TKDI['tx'][0].delete('1.0', TK.END)
        LL.TKDI['tx'][0].insert(TK.END, txls)

        
def right__cut(event):
    
    ls = ParamDI['ls']
    sl = ls.split()

    pos = LL.TKDI['sc'][1].get()
    if pos == 0:
        line = ls
    if pos > 0:
        end = -1*pos
        ParamDI['end'] = end        
        start = ParamDI['start']
        
        if start == 0:
            slfr = sl[:end]
        else:
            slfr = sl[start:end]            
        
        line = ' '.join(slfr)
        
    LL.TKDI['tx'][0].delete('1.0', TK.END)
    LL.TKDI['tx'][0].insert(TK.END, line)

    Find__ls()

def left__cut(event):

    ls = ParamDI['ls']
    sl = ls.split()

    pos = LL.TKDI['sc'][0].get()
    if pos == 0:
        line = ls
    if pos > 0:
        start = pos
        ParamDI['start'] = start
        end = ParamDI['end']
        if end == 0:
            slfr = sl[start:]
        else:
            slfr = sl[start:end]     
            
        
        line = ' '.join(slfr)
    LL.TKDI['tx'][0].delete('1.0', TK.END)
    LL.TKDI['tx'][0].insert(TK.END, line)

    Find__ls()
    
def reflect_target(event):

    
    if LL.TKDI['lx']['target'].size() > 0:
        lxname = 'target'
        cs = int(LL.TKDI['lx'][lxname].curselection()[0])
        si = LL.TKDI['lx'][lxname].get(cs)
        LL.TKDI['en'][lxname].delete(0, TK.END)
        LL.TKDI['en'][lxname].insert(0, si)        
    
        ShowContext()    
    

def Create__forms():

    LL.Create__root('The Comparator')
    LL.Add__one__frame(0, 'root', 1, 1) ## lxx
    LL.Add__one__frame(1, 'root', 2, 1) ## Txx
    

    
    LL.Add__lx('sections', 0, 1, 1, 30, 7, 'Arial 10')
    array = []
    for k in AI['Syn'].keys():
        si = k #.decode('cp1251').encode('utf-8')
        array.append(si)
    array.sort()
    LL.Fill__lx(array, 'sections')    
    LL.TKDI['lx']['sections'].bind('<KeyRelease>', reflect_section)
    LL.TKDI['lx']['sections'].bind('<ButtonRelease>', reflect_section)


    LL.Add__lx('ls', 0, 1, 2, 30, 7, 'Verdana 10')
    LL.TKDI['en']['ls']['font'] = 'Verdana 10'
    LL.TKDI['lx']['ls'].bind('<KeyRelease>', reflect_ls)
    LL.TKDI['lx']['ls'].bind('<ButtonRelease>', reflect_ls)

    
    LL.Add__lx('target', 0, 1, 3, 30, 7, 'Verdana 10')
    LL.TKDI['en']['target']['font'] = 'Verdana 10'
    LL.TKDI['lx']['target'].bind('<KeyRelease>', reflect_target)
    LL.TKDI['lx']['target'].bind('<ButtonRelease>', reflect_target)

    LL.Add__lx('target_sections', 0, 1, 4, 25, 7, 'Arial 10')
    LL.TKDI['en']['target_sections']['font'] = 'Arial 10'
    LL.TKDI['lx']['target_sections'].bind('<KeyRelease>', reflect_tarsect)
    LL.TKDI['lx']['target_sections'].bind('<ButtonRelease>', reflect_tarsect)


    ###  ====================================================

    LL.TKDI['tx'][0] = LL.TK.Text(LL.TKDI['fr'][1])
    LL.TKDI['tx'][0].grid(row = 1, column = 1)
    LL.TKDI['tx'][0]['font'] = 'Courier 14'
    LL.TKDI['tx'][0]['height'] = 4#10
    LL.TKDI['tx'][0]['width'] = 90

    LL.Add__one__frame(2, 1, 2, 1) ## Txx


    LL.TKDI['sc'][0] = TK.Scale(LL.TKDI['fr'][2])
    LL.TKDI['sc'][0].grid(row = 1, column = 1)
    LL.TKDI['sc'][0]['from'] = 0
    LL.TKDI['sc'][0]['to'] = 10
    LL.TKDI['sc'][0]['tickinterval'] = 1    
    LL.TKDI['sc'][0]['orient'] = TK.HORIZONTAL
    LL.TKDI['sc'][0]['length'] = 400
    LL.TKDI['sc'][0].bind('<KeyRelease>', left__cut)
    LL.TKDI['sc'][0].bind('<ButtonRelease>', left__cut)
    
    LL.TKDI['en']['start'] = TK.Entry(LL.TKDI['fr'][2])
    LL.TKDI['en']['start'].grid(row = 1, column = 3)
    LL.TKDI['en']['start']['width'] = 30
    LL.TKDI['en']['start']['font'] = 'Arial 14'
    
    
    
##    LL.TKDI['en']['end'] = TK.Entry(LL.TKDI['fr'][2])
##    LL.TKDI['en']['end'].grid(row = 1, column = 4)
####    LL.TKDI['en']['start'].insert(0, '1.2')
####    LL.TKDI['en']['end'].insert(0, '1.9')
##    LL.TKDI['en']['end']['width'] = 4
    
    LL.TKDI['sc'][1] = TK.Scale(LL.TKDI['fr'][2])
    LL.TKDI['sc'][1].grid(row = 2, column = 1)
    LL.TKDI['sc'][1]['from'] = 0
    LL.TKDI['sc'][1]['to'] = 10
    LL.TKDI['sc'][1]['tickinterval'] = 1    
    LL.TKDI['sc'][1]['orient'] = TK.HORIZONTAL
    LL.TKDI['sc'][1]['length'] = 400
    LL.TKDI['sc'][1].bind('<KeyRelease>', right__cut)
    LL.TKDI['sc'][1].bind('<ButtonRelease>', right__cut)
   
    
    
    
    
    
    LL.TKDI['tx'][1] = LL.TK.Text(LL.TKDI['fr'][1])
    LL.TKDI['tx'][1].grid(row = 3, column = 1)
    LL.TKDI['tx'][1]['font'] = 'Courier 14'
    LL.TKDI['tx'][1]['height'] = 7 #10
    LL.TKDI['tx'][1]['width'] = 90
    LL.TKDI['tx'][1]['bg'] = 'black'
    LL.TKDI['tx'][1]['fg'] = 'green'    


    LL.Create__menu()
    LL.TKDI['me'][1].add_command(label = 'Find__ls', command = Find__ls)
    LL.TKDI['me'][1].add_command(label = 'ShowContext', command = ShowContext)
    
##    LL.TKDI['me'][1].add_command(label = 'AcceptDocStructure', command = AcceptDocStructure)
##    LL.TKDI['me'][1].add_command(label = 'ShowDocStructure', command = ShowDocStructure)
    LL.TKDI['me'][1].add_command(label = 'Find__sent', command = Find__sent)
    LL.TKDI['me'][1].add_command(label = 'Highlight', command = Highlight)
    LL.TKDI['me'][1].add_command(label = 'Search_primer', command = Search_primer)
    LL.TKDI['me'][1].add_command(label = 'See', command = See)



##    TKDI['me'][0] = TK.Menu(TKDI['fr']['root'])
##    TKDI['me'][1] = TK.Menu(TKDI['me'][0])
####TKDI['me'][1].add_command(label = 'Print_blocks', command = Print_blocks)
####TKDI['me'][1].add_command(label = 'Accept_block_content', command = Accept_block_content)









def Start():
    Fill__descriptors()    
    #AV.PrintAcc(0)
    ParseSynopsis()

    Create__forms()
    
    AI['name'] = 'Syn'
    ReadProt()
    Show_target_doc()

    SetSynopsisInxx()
    ReadStructure()
    GetHeaderSeinxx()
    
#    print SeinxSectDI[144]

    

    
#    DV.AllKeys()
##    arr =  AI['Syn'].keys()
##    fk = arr[6]
##    for ls in AI['Syn'][fk]:
##        print ls
##        print ''
##        print '===================='

    LL.TKDI['fr']['root'].mainloop()       

Start()


            

