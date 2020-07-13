from tkinter import *
import os
import cv2
import numpy as np
from PIL import Image
import sqlite3
import mysql.connector
import tkinter as tk
import tkinter.simpledialog
from tkinter import messagebox

faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
cam=cv2.VideoCapture(0);
def takeatt():
    rec=cv2.face.LBPHFaceRecognizer_create();
    rec.read("recognizer\\trainningData.yml")
    id=0
    font=cv2.FONT_HERSHEY_SIMPLEX
    checkset=set([0,0])
    mydb=mysql.connector.connect(host="sql12.freesqldatabase.com",user="sql12353604",passwd="nRAijBtRk2",database="sql12353604")
    conn=mydb.cursor()
    count=0;
    detail=""
    totalcases=0
    while(True):
        ret,img=cam.read();
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces=faceDetect.detectMultiScale(gray,1.3,5);
        temp=0
        for(x,y,w,h) in faces:
            cv2.rectangle(img, (x,y),(x+w,y+h),(0,0,255),2)
            id,conf=rec.predict(gray[y:y+h,x:x+w])
            profile=getProfile(id)
            #print(id)
            conn.execute("SELECT COUNT(Aadhar) from Murder where Aadhar="+str(id))
            for row in conn:
                murdercnt=row[0]
                totalcases=totalcases+murdercnt
                if(murdercnt>0):
                    detail=detail+"Murder:\n"
                    conn.execute("SELECT * from Details INNER JOIN Murder where Details.id=Murder.aadhar and Details.id="+str(id))
                    for row in conn:
                        detail=detail+str(row[7])+"\n"

            conn.execute("SELECT COUNT(Aadhar) from Kidnapping where Aadhar="+str(id))
            for row in conn:
                kidnapcnt=row[0]
                totalcases=totalcases+kidnapcnt
                if(kidnapcnt>0):
                    detail=detail+"Kidnapping:\n"
                    conn.execute("SELECT * from Details INNER JOIN Kidnapping where Details.id=Kidnapping.aadhar and Details.id="+str(id))
                    for row in conn:
                        detail=detail+str(row[7])+"\n"

            conn.execute("SELECT COUNT(Aadhar) from Robbery where Aadhar="+str(id))
            for row in conn:
                robcnt=row[0]
                totalcases=totalcases+robcnt
                if(robcnt>0):
                    detail=detail+"Robbery:\n"
                    conn.execute("SELECT * from Details INNER JOIN Robbery where Details.id=Robbery.aadhar and Details.id="+str(id))
                    for row in conn:
                        detail=detail+str(row[7])+"\n"

            conn.execute("SELECT COUNT(Aadhar) from Cybercrime where Aadhar="+str(id))
            for row in conn:
                cccnt=row[0]
                totalcases=totalcases+cccnt
                if(cccnt>0):
                    detail=detail+"CyberCrime:\n"
                    conn.execute("SELECT * from Details INNER JOIN Cybercrime where Details.id=Cybercrime.aadhar and Details.id="+str(id))
                    for row in conn:
                        detail=detail+str(row[7])+"\n"

            conn.execute("SELECT COUNT(Aadhar) from Terrorist where Aadhar="+str(id))
            for row in conn:
                tecnt=row[0]
                totalcases=totalcases+tecnt
                if(tecnt>0):
                    detail=detail+"Robbery:\n"
                    conn.execute("SELECT * from Details INNER JOIN Terrorist where Details.id=Terrorist.aadhar and Details.id="+str(id))
                    for row in conn:
                        detail=detail+str(row[7])+"\n"
            print(totalcases)
            conn.execute("UPDATE Details SET total="+str(totalcases)+" where id="+str(id))
            mydb.commit()
            conn.execute("SELECT total FROM Details where id="+str(id))
            for row in conn:
                totalcases=row[0]
            if(profile!=None):
                print("Record Found")
                temp=1
                cv2.putText(img,str(profile[1]),(x,y+h),font,1,255,2);
        cv2.imshow("Face",img);
        if(temp==1):
            messagebox.showinfo("Details", "Name= "+str(profile[1])+"\nGender= "+str(profile[2])+"\nAge= "+str(profile[3])+"\nAadhar No= "+str(profile[0])+"\nAddress="+str(profile[4])+"\nTotal Case="+str(totalcases)+"\nDetails=\n"+str(detail))
            break;
        if(cv2.waitKey(1)==ord('q')):
            break;
        count=count+1
        if(count==300):
            messagebox.showinfo("Ooppss","No Record Found")
            break;
    cam.release()
    cv2.destroyAllWindows()
    

def insertOrUpdate(Id,Name,Gender,Age,Crime,Desc,Address):
    mydb=mysql.connector.connect(host="sql12.freesqldatabase.com",user="sql12353604",passwd="nRAijBtRk2",database="sql12353604")
    conn=mydb.cursor(buffered=True)
    cmd="SELECT * FROM Details WHERE ID="+str(Id)
    conn.execute(cmd)
    mydb.commit()
    isRecordExist=0
    for row in conn:
        isRecordExist=1
    if(isRecordExist==1):
        messagebox.showinfo("Ooppss","record already present")
    else:
        cmd="INSERT INTO Details(ID,Name,Gender,Age,Address) Values("+str(Id)+","+str(Name)+","+str(Gender)+","+str(Age)+","+str(Address)+")"
        if(Crime.find("Murder")!=-1):
            cmd2="Insert into Murder (aadhar,description) Values("+str(Id)+","+str(Desc)+")"
            conn.execute(cmd2)
            mydb.commit()
        if(Crime.find("Robbery")!=-1):
            cmd2="Insert into Robbery (aadhar,description) Values("+str(Id)+","+str(Desc)+")"
            conn.execute(cmd2)
            mydb.commit()
        if(Crime.find("Kidnapping")!=-1):
            cmd2="Insert into Kidnapping (aadhar,description) Values("+str(Id)+","+str(Desc)+")"
            conn.execute(cmd2)
            mydb.commit()
        if(Crime.find("Terrorist")!=-1):
            cmd2="Insert into Terrorist (aadhar,description) Values("+str(Id)+","+str(Desc)+")"
            conn.execute(cmd2)
            mydb.commit()
        if(Crime.find("Cybercrime")!=-1):
            cmd2="Insert into Cybercrime (aadhar,description) Values("+str(Id)+","+str(Desc)+")"
            conn.execute(cmd2)
            mydb.commit()
    conn.execute(cmd)
    mydb.commit();

def getProfile(id):
    mydb=mysql.connector.connect(host="sql12.freesqldatabase.com",user="sql12353604",passwd="nRAijBtRk2",database="sql12353604")
    conn=mydb.cursor()
    cmd="SELECT * FROM Details WHERE ID="+str(id)
    conn.execute(cmd)
    profile=None
    for row in conn:
        profile=row
    return profile
    

def add_stu():
    myText1=tkinter.simpledialog.askstring("Details","Enter Name:")
    myText2=tkinter.simpledialog.askstring("Details","Enter Aadhar Card Number:")
    myText3=tkinter.simpledialog.askstring("Details","Enter the Gender:")
    myText4=tkinter.simpledialog.askstring("Details","Enter the Age(in years):")
    myText7=tkinter.simpledialog.askstring("Details","Enter the Address:")
    myText5=tkinter.simpledialog.askstring("Details","Crime Committed(Murder,Robbery,CyberCrime,Terrorist,Kidnapping):")
    myText6=tkinter.simpledialog.askstring("Details","Enter thre description of crime:")
    fn=StringVar()
    window=Tk()
    window.title("Add the Records")
    window.geometry("600x400")
    label2=Label(window,text="Records Updated Successfully",fg='blue',font=("arial",16,"bold")).place(x=190,y=60)
    id=myText2
    name='"'+myText1+'"'
    gender='"'+myText3+'"'
    age=myText4
    crime=str(myText5)
    desc='"'+myText6+'"'
    add='"'+myText7+'"'
    insertOrUpdate(id,name,gender,age,crime,desc,add)
    sampleNum=0;
    while(True):
        ret,img=cam.read();
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces=faceDetect.detectMultiScale(gray,1.3,5);
        for(x,y,w,h) in faces:
            sampleNum=sampleNum+1;
            cv2.imwrite("dataSet/User."+str(id)+"."+str(sampleNum)+".jpg",gray[y:y+h,x:x+w])
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
            cv2.waitKey(100);
        cv2.imshow("Face",img);
        cv2.waitKey(1);
        if(sampleNum>150):
            break;
    cam.release()
    cv2.destroyAllWindows()

def FindUsingAadhar():
    id=tkinter.simpledialog.askstring("Details","Enter the Aadhar Number:")
    profile=getProfile(id)
    mydb=mysql.connector.connect(host="sql12.freesqldatabase.com",user="sql12353604",passwd="nRAijBtRk2",database="sql12353604")
    conn=mydb.cursor()
    detail=""
    totalcases=0
    conn.execute("SELECT COUNT(Aadhar) from Murder where Aadhar="+str(id))
    for row in conn:
        murdercnt=row[0]
        totalcases=totalcases+murdercnt
        if(murdercnt>0):
            detail=detail+"Murder:\n"
            conn.execute("SELECT * from Details INNER JOIN Murder where Details.id=Murder.aadhar and Details.id="+str(id))
            for row in conn:
                detail=detail+str(row[7])+"\n"

    conn.execute("SELECT COUNT(Aadhar) from Kidnapping where Aadhar="+str(id))
    for row in conn:
        kidnapcnt=row[0]
        totalcases=totalcases+kidnapcnt
        if(kidnapcnt>0):
            detail=detail+"Kidnapping:\n"
            conn.execute("SELECT * from Details INNER JOIN Kidnapping where Details.id=Kidnapping.aadhar and Details.id="+str(id))
            for row in conn:
                detail=detail+str(row[7])+"\n"

    conn.execute("SELECT COUNT(Aadhar) from Robbery where Aadhar="+str(id))
    for row in conn:
        robcnt=row[0]
        totalcases=totalcases+robcnt
        if(robcnt>0):
            detail=detail+"Robbery:\n"
            conn.execute("SELECT * from Details INNER JOIN Robbery where Details.id=Robbery.aadhar and Details.id="+str(id))
            for row in conn:
                detail=detail+str(row[7])+"\n"

    conn.execute("SELECT COUNT(Aadhar) from Cybercrime where Aadhar="+str(id))
    for row in conn:
        cccnt=row[0]
        totalcases=totalcases+cccnt
        if(cccnt>0):
            detail=detail+"CyberCrime:\n"
            conn.execute("SELECT * from Details INNER JOIN Cybercrime where Details.id=Cybercrime.aadhar and Details.id="+str(id))
            for row in conn:
                detail=detail+str(row[7])+"\n"

    conn.execute("SELECT COUNT(Aadhar) from Terrorist where Aadhar="+str(id))
    for row in conn:
        tecnt=row[0]
        totalcases=totalcases+tecnt
        if(tecnt>0):
            detail=detail+"Robbery:\n"
            conn.execute("SELECT * from Details INNER JOIN Terrorist where Details.id=Terrorist.aadhar and Details.id="+str(id))
            for row in conn:
                detail=detail+str(row[7])+"\n"
    conn.execute("UPDATE Details SET total="+str(totalcases)+" where id="+str(id))
    mydb.commit()
    conn.execute("SELECT total FROM Details where id="+str(id))
    temp=0
    for row in conn:
        totalcases=row[0]
    if(profile!=None):
        print("Record Found")
        temp=1
    if(temp==1):
        messagebox.showinfo("Details", "Name= "+str(profile[1])+"\nGender= "+str(profile[2])+"\nAge= "+str(profile[3])+"\nAadhar No= "+str(profile[0])+"\nAddress="+str(profile[4])+"\nTotal Case="+str(totalcases)+"\nDetails=\n"+str(detail))
    else:
        messagebox.showinfo("Ooppss","No Record Found")
    cv2.destroyAllWindows()

    
def take_att():
    window=Tk()
    window.title("Find Records")
    window.geometry("600x400")
    label2=Label(window,text="Find Records",fg='blue',font=("arial",16,"bold")).place(x=190,y=30)
    button_s=Button(window,text="Find using Aadhar",fg='White',command=FindUsingAadhar,bg='brown',relief=GROOVE,font=("arial",12,"bold"))
    button_s.place(x=200,y=150)
    button_ta=Button(window,text="Find using Face",fg='White',command=takeatt,bg='brown',relief=GROOVE,font=("arial",12,"bold"))
    button_ta.place(x=200,y=200)
    window.mainloop()

def tabify(s, tabsize = 19):
    ln = ((len(s)//tabsize)+1)*tabsize
    return s.ljust(ln)
def tab(s, tabsize = 16):
    ln = ((len(s)//tabsize)+1)*tabsize
    return s.ljust(ln)

def all():
    window=Tk()
    window.title("View Attendance")
    window.geometry("600x400")
    label2=Label(window,text="View Criminal Records",fg='blue',font=("arial",16,"bold")).place(x=190,y=30)
    listbox=Listbox(window,height=15,width=80)
    listbox.place(x=70,y=100)
    mydb=mysql.connector.connect(host="sql12.freesqldatabase.com",user="sql12353604",passwd="nRAijBtRk2",database="sql12353604")
    conn=mydb.cursor()
    cmd="SELECT * FROM Details INNER JOIN Murder where Details.id=Murder.aadhar"
    conn.execute(cmd)
    listbox.insert(END,tab("Aadhar")+tab("Name")+tab("Gender")+tab("Age")+tab("Address")+tab("Total Cases")+tab("Description\n"))
    li=(conn.fetchall()).copy()
    if len(li) !=0:
        listbox.insert(END,"                                                               Murder")
    for row in li:
        aadh=row[0]
        name = row[1]
        gen = row[2]
        ag=row[3]
        add=row[4]
        tc=row[5]
        desc=row[7]
        text=tabify(str(aadh))+tabify(str(name))+tabify(str(gen))+tabify(str(ag))+tabify(str(add))+tabify(str(tc))+tabify(str(desc))
        listbox.insert(END,text)
        
    cmd="SELECT * FROM Details INNER JOIN Kidnapping where Details.id=Kidnapping.aadhar"
    conn.execute(cmd)
    li=(conn.fetchall()).copy()
    if len(li)>0:
        listbox.insert(END,"                                                               Kidnapping")
    for row in li:
        aadh=row[0]
        name = row[1]
        gen = row[2]
        ag=row[3]
        add=row[4]
        tc=row[5]
        desc=row[7]
        text=tabify(str(aadh))+tabify(str(name))+tabify(str(gen))+tabify(str(ag))+tabify(str(add))+tabify(str(tc))+tabify(str(desc))
        listbox.insert(END,text)

    cmd="SELECT * FROM Details INNER JOIN Robbery where Details.id=Robbery.aadhar"
    conn.execute(cmd)
    li=(conn.fetchall()).copy()
    if len(li) !=0:
        listbox.insert(END,"                                                               Robbery")
    for row in li:
        aadh=row[0]
        name = row[1]
        gen = row[2]
        ag=row[3]
        add=row[4]
        tc=row[5]
        desc=row[7]
        text=tabify(str(aadh))+tabify(str(name))+tabify(str(gen))+tabify(str(ag))+tabify(str(add))+tabify(str(tc))+tabify(str(desc))
        listbox.insert(END,text)

    cmd="SELECT * FROM Details INNER JOIN Cybercrime where Details.id=Cybercrime.aadhar"
    conn.execute(cmd)
    li=(conn.fetchall()).copy()
    if len(li) !=0:
        listbox.insert(END,"                                                               Cyber Crime")
    for row in li:
        aadh=row[0]
        name = row[1]
        gen = row[2]
        ag=row[3]
        add=row[4]
        tc=row[5]
        desc=row[7]
        text=tabify(str(aadh))+tabify(str(name))+tabify(str(gen))+tabify(str(ag))+tabify(str(add))+tabify(str(tc))+tabify(str(desc))
        listbox.insert(END,text)

    cmd="SELECT * FROM Details INNER JOIN Terrorist where Details.id=Terrorist.aadhar"
    conn.execute(cmd)
    li=(conn.fetchall()).copy()
    if len(li) !=0:
        listbox.insert(END,"                                                               Terrorist")
    for row in li:
        aadh=row[0]
        name = row[1]
        gen = row[2]
        ag=row[3]
        add=row[4]
        tc=row[5]
        desc=row[7]
        text=tabify(str(aadh))+tabify(str(name))+tabify(str(gen))+tabify(str(ag))+tabify(str(add))+tabify(str(tc))+tabify(str(desc))
        listbox.insert(END,text)
    

def cmd(crime):
    window=Tk()
    window.title("List of Criminals")
    window.geometry("600x400")
    print(crime)
    label2=Label(window,text=crime,fg='blue',font=("arial",16,"bold")).place(x=270,y=30)
    listbox=Listbox(window,height=15,width=80)
    listbox.place(x=70,y=100)
    mydb=mysql.connector.connect(host="sql12.freesqldatabase.com",user="sql12353604",passwd="nRAijBtRk2",database="sql12353604")
    conn=mydb.cursor()
    cmd="SELECT * FROM Details INNER JOIN "+str(crime)+" where Details.id="+str(crime)+".aadhar"
    conn.execute(cmd)
    listbox.insert(END,tab("Aadhar")+tab("Name")+tab("Gender")+tab("Age")+tab("Address")+tab("Total Cases")+tab("Description\n"))
    for row in conn:
        aadh=row[0]
        name = row[1]
        gen = row[2]
        ag=row[3]
        add=row[4]
        tc=row[5]
        desc=row[7]
        text=tabify(str(aadh))+tabify(str(name))+tabify(str(gen))+tabify(str(ag))+tabify(str(add))+tabify(str(tc))+tabify(str(desc))
        listbox.insert(END,text)


def view_att():
    window=Tk()
    window.title("View Attendance")
    window.geometry("600x400")
    label2=Label(window,text="View Criminal Records",fg='blue',font=("arial",16,"bold")).place(x=190,y=30)

    buttonm=Button(window,text="Murder Case",fg='White',command=lambda:cmd("Murder"),bg='brown',relief=GROOVE,font=("arial",10,"bold"))
    buttonm.place(x=175,y=150)
    
    buttonk=Button(window,text="Kidnapping Case",fg='White',command=lambda:cmd("Kidnapping"),bg='brown',relief=GROOVE,font=("arial",10,"bold"))
    buttonk.place(x=375,y=150)
    
    buttonr=Button(window,text="Robbery Case",fg='White',command=lambda:cmd("Robbery"),bg='brown',relief=GROOVE,font=("arial",10,"bold"))
    buttonr.place(x=175,y=250)
    
    buttonc=Button(window,text="Cyber Crime Case",fg='White',command=lambda:cmd("Cybercrime"),bg='brown',relief=GROOVE,font=("arial",10,"bold"))
    buttonc.place(x=375,y=250)
    
    buttont=Button(window,text="Terrorist Case",fg='White',command=lambda:cmd("Terrorist"),bg='brown',relief=GROOVE,font=("arial",10,"bold"))
    buttont.place(x=175,y=350)
    
    buttona=Button(window,text="All the Cases",fg='White',command=all,bg='brown',relief=GROOVE,font=("arial",10,"bold"))
    buttona.place(x=375,y=350)
    window.mainloop()

def getImagesWithID(path):
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
    faces=[]
    IDs=[]
    for imagePath in imagePaths:
        faceImg=Image.open(imagePath).convert('L');
        faceNp=np.array(faceImg,'uint8')
        ID=int(os.path.split(imagePath)[-1].split('.')[1])
        faces.append(faceNp)
        print(ID)
        IDs.append(ID)
        cv2.imshow("training",faceNp)
        cv2.waitKey(10)
    return IDs, faces


def train_data():
    print("Machine Trained Successfully")
    recognizer=cv2.face.LBPHFaceRecognizer_create();
    path='dataSet'
    Ids,faces=getImagesWithID(path)
    recognizer.train(faces,np.array(Ids))
    recognizer.save('recognizer/trainningData.yml')
    cv2.destroyAllWindows()
    

window=Tk()
window.geometry("800x600")
window.title("Criminal Records Management")

label1=Label(window,text="Criminal Records",fg='blue',font=("arial",20,"bold")).place(x=290,y=30)

button1=Button(window,text="Add Records",fg='White',command=add_stu,bg='brown',relief=GROOVE,font=("arial",12,"bold"))
button1.place(x=335,y=100)

button2=Button(window,text="Find Records",fg='White',command=take_att,bg='brown',relief=GROOVE,font=("arial",12,"bold"))
button2.place(x=335,y=180)

button3=Button(window,text="View Records",fg='White',command=view_att,bg='brown',relief=GROOVE,font=("arial",12,"bold"))
button3.place(x=335,y=260)

button4=Button(window,text="Train Machine",fg='White',command=train_data,bg='brown',relief=GROOVE,font=("arial",12,"bold"))
button4.place(x=335,y=340)


window.mainloop()
