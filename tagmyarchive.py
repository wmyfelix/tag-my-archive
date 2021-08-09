#!/usr/bin/env python3
import os,re,sys,stat,getopt,datetime,shutil
dlfolder="/opt/Download"
ext="/opt/extract"
noask=0
mvdir=0
def start():
    edit=0
    mv=0
    print("ExtractTarget Dir:\t",ext)
    print("Resource Dir:\t",dlfolder)
    p7zip,zip_only,rar_only=0,0,0
    _7z,_un=0,0
    os.environ['ext']=ext
    if os.path.isdir(ext):os.chdir(ext)
    else: os.makedirs(ext),os.chdir(ext)
    if os.name=='nt':  
        os.system('echo $(which 7z unzip unrar | grep -E -o "7z$|unzip$|unrar$") > %ext%/available_ext')
    else:
        os.system('echo $(which 7z unzip unrar | grep -E -o "7z$|unzip$|unrar$") > $ext/available_ext')
    with open("available_ext",'r') as avl:
        avlstr=avl.read()
        print( "Current Dir:\t",os.getcwd(),"\nShell:\tavailable extract method:",avlstr)
        if '7z' in avlstr:
            p7zip='7z'
            print("Shell:\t7z detected.")
        elif 'unzip' in avlstr: 
            zip_only='zip'
            print("Shell:\tunzip detected.")
            if 'unrar' in avlstr: 
                rar_only='rar'
                print("Shell:\tunrar detected.")
        else: 
            shellNone=1
            print("Shell:\tNone of shell way extract method available.\a")
            sys.exit()
        if noask!=1:
            y=input("Continue?\n[y/n]:")
            print(y)
            if y!="y":sys.exit()
    for root,dirs,files in os.walk(dlfolder):
        for name in files:
            if os.path.isfile(ext+'/done')==False:
                f=open(ext+'/done','x')
                f.close
            f=open(ext+'/done','r+')
            frs=f.readlines()
            skip=1
            for fr in frs:
                if name+'\n'==fr:
                    print(f"Skip:Recorded File:{name},Skipping.")
                    f.close
                    break
            else:skip=0
            if skip!=0:
                print("Skipped.")
                continue
            fullpath=os.path.join(root,name)
            frontname=re.search('.+(?=\.)',name)
            if frontname: 
                fname=frontname.group()
                print("archive found.",fname)
            else: 
                print("archive not found.")
                continue
            extname=re.search('[^.]+$',name)
            if extname: 
                ename=extname.group()
                print("Extentions Found:",ename)
                if ename not in ['rar','zip','7z']:
                    print("Skip:\tNot an archive format.")
                    if ename in ['jpg','png','mp4','avi']:
                        print(ename,"detected.")
                        if os.path.isdir(root) and mvdir==1 and root!=dlfolder:
                            mv=1
                            edit=1
                    else:continue
            else: 
                print("Skip:\tExtentions Not Found,Skipped.")
                continue
            if (ename=='zip' and zip_only=="zip") or (ename=='rar' and rar_only=='rar') and mv!=1:
                _un=ename
                print(f"Extract {fname} using un{ename}.")
            elif p7zip=='7z':
                print(f'Extract {fname} using p7zip.')
                _7z=1
            else: 
                print("Shell:\tUnsupported Extention.")
                continue
            print("Shell:\tenvironment checked.")
            if mv==1:
                fname=re.search("[^/]*$",root).group()
                print("fname changed to:",fname)
            e2=re.split(" +",fname,1)
            e1=re.split("-+",fname,1)
            e=""
            _match=0
            if len(e1)!=1:
                print("Using fitter='-'")
                e=e1
                n1=e[0]
                n2=e[1]
                _match=1
            elif len(e2)!=1:
                print("Using fitter=' '")
                e=e2
                n1=e[0]
                n2=e[1]
                _match=1
            ns=re.search("(?<=\[)[^PMGB]*?(?=\])|(?<=【)[^PMGB]*?(?=】)",fname)
            n3=re.search("(?<=[(]).*?(?=[)])",fname)
            if ns: 
                print("Special Matching triggered,Overwrite.",ns.group())
                n1=ns.group()
                n2=fname.replace(f"[{n1}]","")
                n2=n2.replace(f"【{n1}】","")
                _match=1
            for by in (" by "," By "):
                if by in fname:
                    print("by_string detected,Overwrite.")
                    n1=re.split(by,fname,1)[1]
                    n2=re.split(by,fname,1)[0]
                    _match=1
            if n3 and _match==1:
                print("Extended Matching triggered.")
                n3=n3.group(0)
                n2=n2.replace(f"({n3})","")
                n1=n1.replace(f"({n3})","")
                n3=re.sub("^(\s*_*)*|(\s*_*)*$","",n3)
            n1=re.sub("^(\s*_*)*|(\s*_*)*$","",n1)
            n2=re.sub("^(\s*_*)*|(\s*_*)*$","",n2)
            print("Author:",n1)
            print("Name:",n2)
            if n3 and _match==1:extdir=f"{ext}/{n1}/{n2}/{n3}"
            else: extdir=f"{ext}/{n1}/{n2}"
            if _match==0:
                print ("No Author/Name Detected ,Skipped.")
                continue
            if n3:print('Extented String=',n3)
            if os.path.isdir(extdir):print("dir already exists.")
            else:os.makedirs(extdir),print("mkdir:",extdir)
            if mv==1:
                print(f"MvDir:\t--mvdir given,move directory:{fullpath} to {extdir}")
                shutil.move(fullpath,extdir)
                continue
            print(f"Extracting {name} to {extdir}")
            os.environ['n1']=n1
            os.environ['n2']=n2
            os.environ['fullpath']=fullpath
            os.environ['extdir']=extdir
            edit=1
            if os.name=='nt':
                if _7z==1: osret=os.system('7z x "%fullpath%" -o"%extdir%" -y %arg%')
                if _un=='zip': osret=os.system('unzip "%fullpath%" -d "%extdir%" -o %arg%')
                if _un=='rar': osret=os.system('unrar x "%fullpath%" "%extdir%" y %arg%')
                os.system('chmod -R 775 "%extdir%"')
            else:
                if _7z==1: osret=os.system('7z x "$fullpath" -o"$extdir" -mmt1 -y $arg')
                if _un=='zip': osret=os.system('unzip "$fullpath" -d "$extdir" -o $arg')
                if _un=='rar': osret=os.system('unrar x "$fullpath" "$extdir" y $arg')
                os.system('chmod -R 775 "$extdir"')
            if osret==0:
                f.write(name+'\n')
                print("History Recorded.")
            else:print("Encountered with error:",osret)
            f.close
    f.close
    if os.path.isfile('available_ext'):os.remove('available_ext')
    
help="""
Usages:
\t-h|help\tDisplay this message.
\t-x<ResourceDir>\tSpecify your Resource Dir.
\t-o<ExtractTargetDir>\tSpecify the Output Dir.
\t-s\tSignal to run.
\t--noask\tDont Ask [y/n].
\t--mvdir\tMove uncompressed Image/Video to OutputDir. 
\t--exec<Addtional Args>\t Exec Addtional Args in Shell prompt.
Sample:\tpython tagmyarchive.py -s -x <ResourceDir> -o <ExtractTargetDir>
"""
print(datetime.datetime.now(),"Start.")
try:
    options,otheropts=getopt.getopt(sys.argv[1:],"sx:o:h",['noask','mvdir','exec'])
except getopt.GetoptError:
    print("Type 'python tagmyarchive.py -h' for usages.")
    sys.exit(2)
for option,argument in options:
    if option=='-h':print(help),sys.exit()
    if option=='-x':
        dlfolder=argument
        _x=1
    if option=='-o':
        ext=argument
        _o=1
    if option=='--noask':
        print("NoAsking...")
        noask=1
    if option=='--mvdir':
        print("Warning:\t--mvdir given,this may cause system impact.")
        mvdir=1
    if option=='-s':sta=1
    if option=='--exec':os.environ['arg']=argument
    else:os.environ['arg']=''
for otheropt in otheropts:
    if otheropt=='help':print(help),sys.exit()
    else:print("Type 'python tagmyarchive.py -h' for usages.") 
if os.name=='nt':
    print("System:\t",os.name)
try:
    if sta==1 or (_x==1 and _o==1):start()
except NameError:print("Type 'python tagmyarchive.py -h' for usages.")