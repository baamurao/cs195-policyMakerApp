import tkinter as tk
from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter import scrolledtext 
from tkinter import colorchooser
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename

import textwrap

import PIL
from PIL import Image, ImageTk

import fpdf
from fpdf import FPDF

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
import scipy as sp

import sys
import os

import statsmodels.api as sm
import sklearn as skl

from sklearn.linear_model import LinearRegression, LogisticRegression

global size, var, pageNumber

save_file_path = None
size = 10

root = Tk()
root.title("Policy Analytics 1.0")
root.geometry("1300x700")
root.state('zoomed')

# getting screen's width in pixels
height = root.winfo_screenheight()
width = root.winfo_screenwidth() 
print("\n width x height = %d x %d (in pixels)\n" %(width, height))

main = tk.PanedWindow(root, background="#ffffff")

main.pack(side="top", fill="both", expand=True)

left_pane = tk.Frame(main, background="#76090c", width=200)
middle_pane = tk.Frame(main, background="#ffffff", width=1520)
right_pane = tk.PanedWindow(main, background="#76090c", width=200)

main.add(left_pane, stretch="never", minsize=150)
main.add(middle_pane, stretch="always", minsize=500)
main.add(right_pane, stretch="never", minsize=150)

introLabel = Label(middle_pane, background="#ffffff", foreground="#76090c", font=("Franklin Gothic Heavy", 14), wraplength=1000, justify="center", text = "Welcome to Policy Analytics 1.0")
aboutLabel = Label(middle_pane, background="#ffffff", foreground="#76090c", font=("Franklin ", 10), wraplength=1000, justify="center", text = "Policy Analytics 1.0 is a tool for learning policy analysis. This software can be used in training programs and classroom learning. It provides a step-by-step procedure that allows users to input and process basic essential data for problem structuring, forecasting and assessment of policy alternatives, recommending or prescribing the best/optimal policy alternative, designing an implementation plan, and building a monitoring and evaluation plan. Its outputs can be used in writing a complete policy issue paper. It is based on the “Elements of the Policy Issue Paper” in Annex 1 of Public Policy Analysis: An Integrated Approach by William N. Dunn (2018) with modifications based on the teaching and training experiences of its creator, Dr. Ebinezer R. Florano, Professor of Public Policy at the University of the Philippines, National College of Public Administration and Governance and Convenor of the UPCIDS Data Science for Public Policy Program (DSPPP).")
arrLabel = Label(middle_pane, background="#ffffff", foreground="#76090c", font=("Franklin ", 10), wraplength=1400, justify="center", text = "All rights reserved@2024 – UPCIDS-DSPPP")
creatorLabel = Label(middle_pane, background="#ffffff", foreground="#76090c", font=("Franklin ", 10), wraplength=1400, justify="left", text = "Creator: Dr. Ebinezer R. Florano")
programmerLabel = Label(middle_pane, background="#ffffff", foreground="#76090c", font=("Franklin ", 10), wraplength=1400, justify="left", text = "Programmers: Emmerson Isip, Gabriel Ramos, and Raphael Justin Portuguez")
reveiwerLabel = Label(middle_pane, background="#ffffff", foreground="#76090c", font=("Franklin ", 10), wraplength=1400, justify="left", text = "Reviewers: Colin Rosales, Danne Nicole Pinpin, and Jean Phoebe Yao")
adminLabel = Label(middle_pane, background="#ffffff", foreground="#76090c", font=("Franklin ", 10), wraplength=1400, justify="left", text = "Administrative Assistance: Lilian J. Marfil, Pedro J. Madarang, and Zhelly Ann Linsangan")

dspppLogo = (Image.open("logo_DSPPP.png"))
cidsLogo = (Image.open("logo_UP_CIDS.png"))
upLogo = (Image.open("logo_UP.png"))

up = upLogo.resize((100, 100))
dsppp = dspppLogo.resize((100, 100))

up = ImageTk.PhotoImage(up)
dsppp = ImageTk.PhotoImage(dsppp)
cids = ImageTk.PhotoImage(cidsLogo)

def update_wraplength(event):
    # Subtract some padding (e.g., 100px) to prevent edge crowding
    new_width = event.width - 100
    for label in resizable_labels:
        label.config(wraplength=new_width)

resizable_labels = [introLabel, aboutLabel, arrLabel, creatorLabel, programmerLabel, reveiwerLabel, adminLabel]

middle_pane.bind("<Configure>", update_wraplength)

main.columnconfigure(0, weight=1)
main.columnconfigure(1, weight=1)
main.columnconfigure(2, weight=1)
main.columnconfigure(3, weight=1)
main.columnconfigure(4, weight=1)
main.columnconfigure(5, weight=1)

# introLabel.place(x=800, y=23)
# aboutLabel.place(x=240, y=63)
# arrLabel.place(x=805, y=200)

introLabel.pack(pady=(20, 5), anchor="center")     
aboutLabel.pack(pady=(20, 5), anchor="center")    
arrLabel.pack(pady=(20, 5), anchor="center")     

logo_frame = tk.Frame(middle_pane, background="#ffffff")  
logo_frame.pack(pady=20, anchor="center") 

upLabel = Label(logo_frame, image=up, background="#ffffff")
upLabel.pack(side=tk.LEFT, padx=20)  

dspppLabel = Label(logo_frame, image=dsppp, background="#ffffff")
dspppLabel.pack(side=tk.LEFT, padx=20)

cidsLabel = Label(logo_frame, image=cids, background="#ffffff")
cidsLabel.pack(side=tk.LEFT, padx=20)

creatorLabel.pack(pady=(20,5), padx=50, anchor="w")
programmerLabel.pack(pady=5, padx=50, anchor="w")
reveiwerLabel.pack(pady=5, padx=50, anchor="w")
adminLabel.pack(pady=5, padx=50, anchor="w")
style = ttk.Style()

def wrap(string, length=40):
    return '\n'.join(textwrap.wrap(string, length))

def createNewProject():
    global pageNumber
    pageNumber = 0

    global p3efforts, p3accomplishments, p3assessments
    p3efforts = []
    p3accomplishments = []
    p3assessments = []

    global filename, fileobject

    mainProject = Toplevel(root)
    
    varRoot1 = tk.IntVar()
    varRoot2 = tk.IntVar()
    varRoot3 = tk.IntVar()
    varRoot4 = tk.IntVar()
    varRoot5 = tk.IntVar()
    varRoot6 = tk.IntVar()
    varRoot7 = tk.IntVar()

    status = ttk.Label(mainProject, text="")
    
    global p1projecttitle, p1analysts, p1fontstyle, p1policyanalysis, p1fontstyle, p1fontsize
    p1projecttitle = " "
    p1analysts = " "
    p1fontstyle = " "
    p1policyanalysis = " "
    p1fontstyle = " "
    p1fontsize = 12

    global p4summaryPDF
    p4summaryPDF = " "

    def page_1():
        global pageNumber
        pageNumber += 1
        print(pageNumber)
        mainProject.title("Create New Project")
        mainProject.geometry("660x210")

        frame1 = tk.LabelFrame(mainProject)

        blank = Label(mainProject, text = "  ")

        projectTitleLabel1 = Label(frame1, text = "Project Title")
        projectTitle = Entry(frame1, width=30)

        settingsLabel = Label(frame1, text = "Settings")
        fontStyleLabel = Label(frame1, text = "Choose font style: ")
        fontSizeLabel = Label(frame1, text = "Choose font size: ")
        indentationLabel = Label(frame1, text = "Choose indentation: ")
        
        font.families()
        fonts = list(font.families())
        fonts.sort()

        fontsList = ttk.Combobox(frame1, width=30, values=fonts)
        fontSize = Entry(frame1, width=10)
        indentation = Entry(frame1, width=10)

        analystNameLabel1 = Label(frame1, text = "Analyst")
        analystName = Entry(frame1, width=30)

        levelsLabel1 = Label(frame1, text = "Levels of Analysis ")

        varNat = tk.IntVar()
        varLoc = tk.IntVar()
        varOrg = tk.IntVar()

        national = tk.Checkbutton(frame1, text='National',variable=varNat, onvalue=1, offvalue=0)
        local = tk.Checkbutton(frame1, text='Local',variable=varLoc, onvalue=1, offvalue=0)
        organizational = tk.Checkbutton(frame1, text='Organizational',variable=varOrg, onvalue=1, offvalue=0)

        polAnaTitleLabel1 = Label(frame1, text = "Policy Analysis Title")
        polAnaTitle = Entry(frame1, width=30)

        frame1.place(x=10, y=10)
        projectTitleLabel1.grid(row=2, column=0, padx=7)
        projectTitle.grid(row=3, column=0, padx=7)
        analystNameLabel1.grid(row=2, column=1, padx=7)
        analystName.grid(row=3, column=1, padx=7)
        polAnaTitleLabel1.grid(row=2, column=2, padx=7)
        polAnaTitle.grid(row=3, column=2, padx=7)
        settingsLabel.grid(row=5, column=0)
        fontStyleLabel.grid(row=6, column=0, sticky = W, padx=7)
        fontsList.grid(row=6, column=1, sticky = W, padx=7)
        fontSizeLabel.grid(row=7, column=0, sticky = W, padx=7)
        fontSize.grid(row=7, column=1, sticky = W, padx=7)
        indentationLabel.grid(row=8, column=0, sticky = W, padx=7)
        indentation.grid(row=8, column=1, sticky = W, padx=7)
        levelsLabel1.grid(row=5, column=2, padx=7)
        national.grid(row=6, column=2, sticky = W, padx=56)
        local.grid(row=7, column=2, sticky = W, padx=56)
        organizational.grid(row=8, column=2, sticky = W, padx=56)
    
        def clear_page_1():
            projectTitle.config(bg="white")
            fontSize.config(bg="white")
            analystName.config(bg="white")
            polAnaTitle.config(bg="white")
            fontsList.set('')
            # probSit.config(bg="white")
            # undeEff.config(bg="white")
            
            projectTitle.delete(0, END)
            polAnaTitle.delete(0, END)
            analystName.delete(0, END)
            fontSize.delete(0, END)
            indentation.delete(0, END)
            # probSit.delete("1.0", tk.END)
            # undeEff.delete("1.0", tk.END)

        def create_project():    
            global p1projecttitle, p1analysts, p1fontstyle, p1policyanalysis, p1fontstyle, p1fontsize
            p1projecttitle = projectTitle.get()
            if not p1projecttitle.strip():
                status.config(
                    text="Enter project title",
                    foreground="red",
                )
                return
            
            p1fontstyle = fontsList.get()

            p1fontsize = fontSize.get()
            if p1fontsize.isnumeric() == False:
                status.config(
                    text="Enter font size",
                    foreground="red",
                )
                return

            p1fontsize = int(p1fontsize)

            p1analysts = analystName.get()
            if not p1analysts.strip():
                status.config(
                    text="Enter analyst name",
                    foreground="red",
                )
                return
                    
            p1policyanalysis = polAnaTitle.get()
            if not p1policyanalysis.strip():
                status.config(
                    text="Enter policy analysis title",
                    foreground="red",
                )
                return
            
            save()
            
            global pageNumber
            pageNumber += 1
            print(pageNumber)
            frame1.destroy()
            btnCreate.destroy() 
            btnClear1.destroy()  
            page_2()
            
        btnCreate = Button(mainProject, text = "Create", width=10, command = lambda: create_project())
        btnClear1 = Button(mainProject, text = "Clear", width=10, command = lambda: clear_page_1())

        btnCreate.place(x=380, y=170)
        btnClear1.place(x=190, y=170)
        status.place(x=10, y=170)

    page_1()

    global p2problematicsituation, p2undesirableeffects
    p2problematicsituation = "problematic situation"
    p2undesirableeffects = "undesirable effects"

    def page_2():                                                               # write problematic situation and undesirable effects
        mainProject.geometry("660x210")
        frame2 = tk.LabelFrame(mainProject)

        status.config(text="")

        probSitLabel = Label(frame2, text = "Problematic Situation")
        probSit = scrolledtext.ScrolledText(frame2, height = 8, width=30)
        
        undeEffLabel = Label(frame2, text = "Undesirable Effects")
        undeEff = scrolledtext.ScrolledText(frame2, height = 8, width=30)
        
        frame2.place(x=40, y=10)
        probSitLabel.grid(row=1, column=0, sticky = W, padx=7)
        probSit.grid(row=2, column=0, sticky = W, padx=7)
        undeEffLabel.grid(row=1, column=1, sticky = W, padx=7)
        undeEff.grid(row=2, column=1, sticky = W, padx=7)
        
        def back_1():
            global pageNumber
            pageNumber -= 1
            print(pageNumber)
            frame2.destroy() 
            btnBack1.destroy()
            btnNext1.destroy() 
            page_1()
        
        def next_1():
            global pageNumber
            pageNumber += 1
            print(pageNumber)

            global p2problematicsituation, p2undesirableeffects
            p2problematicsituation = probSit.get("1.0", tk.END)
            if not p2problematicsituation.strip():
                status.config(
                text="Enter problematic\nsituation",
                foreground="red",
            )
                return
                    
            p2undesirableeffects = undeEff.get("1.0", tk.END)
            if not p2undesirableeffects.strip():
                status.config(
                text="Enter undesirable\neffects",
                foreground="red",
            )
                return
        
            # fileobject.writelines(problematicsituation+"\n"+undesirableeffects+"\n")
            save()

            frame2.destroy() 
            btnBack1.destroy()
            btnNext1.destroy() 
            page_3()

        btnBack1 = Button(mainProject, text = "Back", width=10, command = lambda: back_1())
        btnNext1 = Button(mainProject, text = "Next", width=10, command = lambda: next_1())
        btnBack1.place(x=140, y=170)
        btnNext1.place(x=400, y=170)
    
    def page_3():
        mainProject.geometry("1250x700")
        style.configure('Treeview', rowheight=160)

        status.config(text="")

        # mainFrame3 = tk.Frame(mainProject)
        # mainFrame3.place(x=10, y=10)
        # mainFrame1_3 = tk.Frame(mainFrame3, height=600, width = 1200)
        # mainFrame1_3.pack(fill=BOTH,expand=1)
        # mainFrame2_3 = tk.LabelFrame(mainFrame1_3, height=600, width = 1200)
        # mainFrame2_3.pack(fill=X,side=BOTTOM)
        # canvas3 = Canvas(mainFrame1_3, height=600, width = 1200)
        # canvas3.pack(side=LEFT,fill=BOTH,expand=1)

        # sbx3 = ttk.Scrollbar(mainFrame2_3,orient=HORIZONTAL,command=canvas3.xview)
        # sbx3.pack(side=BOTTOM,fill=X)
        # sby3 = ttk.Scrollbar(mainFrame1_3,orient=VERTICAL,command=canvas3.yview)
        # sby3.pack(side=RIGHT,fill=Y)
        # canvas3.configure(xscrollcommand=sbx3.set)
        # canvas3.configure(yscrollcommand=sby3.set)
        # canvas3.bind("<Configure>",lambda e: canvas3.config(scrollregion= canvas3.bbox(ALL))) 

        frame3 = tk.LabelFrame(mainProject)
        # canvas3.create_window((0,0),window= frame3, anchor="nw")
            # enumerate current effort
        currEffLabel = Label(frame3, text = "Current Efforts/Measures of the Government to Solve the Situational Problem")
        effortsTable=ttk.Treeview(frame3, selectmode="browse", height=2)
        effortsTable["columns"]=("1","2","3")
        effortsTable['show']='headings'
        effortsTable.column("1",width=200,anchor='c', stretch=TRUE)
        effortsTable.column("2",width=700,anchor='c', stretch=TRUE)
        effortsTable.column("3",width=300,anchor='c', stretch=TRUE)
        effortsTable.heading("1",text="Effort/Measure")
        effortsTable.heading("2",text="Accomplishments")
        effortsTable.heading("3",text="Assessment")

        sb = Scrollbar(frame3, orient=VERTICAL)

        effortsTable.configure(yscrollcommand=sb.set)  # connect to Treeview
        sb.config(command=effortsTable.yview)
        
        effoLabel = Label(mainProject, text = "Effort")
        accoLabel = Label(mainProject, text = "Accomplishment")
        asseLabel = Label(mainProject, text = "Assessment")

        effort = scrolledtext.ScrolledText(mainProject, height = 9, width=40)
        accomplishment = scrolledtext.ScrolledText(mainProject, height = 9, width=40)
        assessment = scrolledtext.ScrolledText(mainProject, height = 9, width=40)

        addButton = tk.Button(mainProject, text='Add', width=10, command=lambda: add_data())  
        editButton = tk.Button(mainProject, text="Edit", width=10, command=lambda: edit_data())

        def show_data(a):
            effort.delete("1.0", tk.END)   
            accomplishment.delete("1.0", tk.END) 
            assessment.delete("1.0", tk.END) 

            selectedItem = effortsTable.selection()[0]
            effort.insert(tk.INSERT, effortsTable.item(selectedItem)['values'][0])
            accomplishment.insert(tk.INSERT, effortsTable.item(selectedItem)['values'][1])
            assessment.insert(tk.INSERT, effortsTable.item(selectedItem)['values'][2])

        effortsTable.bind("<<TreeviewSelect>>", show_data)

        def edit_data():
            effortText = effort.get("1.0", tk.END)                          # read effort
            accomplishmentText = accomplishment.get("1.0", tk.END)          # read accomplishment
            assessmentText = assessment.get("1.0", tk.END)                  # read assessment

            selected_item = effortsTable.selection()[0]

            effortsTable.item(selected_item, text="blub", values=(effortText, accomplishmentText, assessmentText))

            print(effortsTable.index(selected_item))

            p3efforts[effortsTable.index(selected_item)] = effortText
            p3accomplishments[effortsTable.index(selected_item)] = accomplishmentText
            p3assessments[effortsTable.index(selected_item)] = assessmentText

        def add_data():
            global p3efforts, p3accomplishments, p3assessments
            effortText = effort.get("1.0", tk.END)                          # read effort
            accomplishmentText = accomplishment.get("1.0", tk.END)          # read accomplishment
            assessmentText = assessment.get("1.0", tk.END)                  # read assessment

            effortsTable.insert("",'end', values=(wrap(effortText), wrap(accomplishmentText), wrap(assessmentText)))
            effort.delete("1.0", tk.END)            # reset the text entry box
            accomplishment.delete("1.0", tk.END)    # reset the text entry box
            assessment.delete("1.0", tk.END)
            effort.focus() 

            p3efforts.append(effortText)
            p3accomplishments.append(accomplishmentText)
            p3assessments.append(assessmentText)

        frame3.place(x=10, y=10)
        currEffLabel.grid(row=0, column=0, columnspan=2)
        effortsTable.grid(row=1, column=0)
        # sb.grid(row=0, column=1, rowspan=2)
        effoLabel.place(x=195, y=390)
        effort.place(x=50, y=420)
        accoLabel.place(x=563, y=390)
        accomplishment.place(x=450, y=420)
        asseLabel.place(x=975, y=390)
        assessment.place(x=850, y=420)
        addButton.place(x=490, y=590)
        editButton.place(x=680, y=590)

        def back_2():
            global pageNumber
            pageNumber -= 1
            print(pageNumber)

            sb.destroy()
            frame3.destroy() 
            effoLabel.destroy()
            effort.destroy()
            effort.place_forget()
            accoLabel.destroy()
            accomplishment.destroy()
            accomplishment.place_forget()
            asseLabel.destroy()
            assessment.destroy()
            assessment.place_forget()
            addButton.destroy()
            editButton.destroy()
            btnBack2.destroy()
            btnNext2.destroy() 
            page_2()
        
        def next_2():
            global pageNumber
            pageNumber += 1
            print(pageNumber)

            save()
            sb.destroy()
            frame3.destroy() 
            effoLabel.destroy()
            effort.destroy()
            effort.place_forget()
            accoLabel.destroy()
            accomplishment.destroy()
            accomplishment.place_forget()
            asseLabel.destroy()
            assessment.destroy()
            assessment.place_forget()
            addButton.destroy()
            editButton.destroy()
            btnBack2.destroy()
            btnNext2.destroy() 
            page_4()

        btnBack2 = Button(mainProject, text = "Back", width=10, command = lambda: back_2())
        btnNext2 = Button(mainProject, text = "Next", width=10, command = lambda: next_2())
        btnBack2.place(x=490, y=650)
        btnNext2.place(x=680, y=650)

    def page_4():
        mainProject.geometry("660x210")

        frame4 = tk.LabelFrame(mainProject)

        global var
        var = IntVar()
            
        StatisticalMethod = Label(frame4, text = "Statistical Method")
        Qualita = Label(frame4, text = "Qualitative")
        Quantita = Label(frame4, text = "Quantitative")
        R1 = Radiobutton(frame4, text="Linear Regression", variable=var, value=1)
        R2 = Radiobutton(frame4, text="Multiple Regression", variable=var, value=2)
        R3 = Radiobutton(frame4, text="Logistic Regression", variable=var, value=3)
        R4 = Radiobutton(frame4, text="Problem Tree Analysis", variable=var, value=4)

        StatisticalMethod.place(x = 275, y=10)
        frame4.place(x=190, y=50)
        Quantita.grid(row=1, column=0)
        Qualita.grid(row=1, column=1)
        R1.grid(row=2, column=0)
        R2.grid(row=3, column=0)
        R3.grid(row=4, column=0)
        R4.grid(row=2, column=1)

        def analyses():                    
            if (int(var.get()) == 1):
                analysis = Toplevel(main)
                analysis.title("Analysis - Linear Regression")
                analysis.geometry("1000x680")

                filename = askopenfilename(filetypes=[("CSV Files", "*.csv")])

                if filename == "":
                    page_4()
                df = pd.read_csv(filename, usecols=[0,1])
                X_train = df.iloc[:, [0]]
                y_train = df.iloc[:, [1]]

                print(df)

                column_names = list(df.columns)

                model = sm.OLS(y_train, sm.add_constant(X_train)).fit()

                lb1 = Label(analysis,text=model.summary(), font="Consolas", justify="left")
                lb1.pack()

                reg = skl.linear_model.LinearRegression().fit(X_train[:], y_train[:])

                divider  = "\n******************************************************************************\n"
                regTitle = "                       skLearn Linear Regression Results                        \n"
                lb2 = Label(analysis,text=divider+regTitle, font="Consolas", justify="left")
                lb2.pack()

                score = "Score:        " + str(round(float(reg.score(X_train, y_train)), 5))
                global interceptLR, coefficientLR, interceptLRDisplay, coefficientLRDisplay
                interceptLRDisplay = "\nIntercept:    " + str(round(float(reg.intercept_), 5))
                interceptLR = float(reg.intercept_)
                coefficientLRDisplay = "\nCoefficient:  " + str(round(float(reg.coef_), 5))
                coefficientLR = float(reg.coef_)

                summary = score + interceptLRDisplay + coefficientLRDisplay
                lb3 = Label(analysis,text=summary, font="Consolas", justify="left")
                lb3.pack()

                global p4summaryPDF
                p4summaryPDF = divider + regTitle + summary
                
                plt.scatter(X_train, y_train, color = "m", marker = "o", s = 30)

                # plotting the regression line
                plt.plot(X_train, reg.predict(X_train), color = "g")

                # putting labels
                plt.xlabel(column_names[0])
                plt.ylabel(column_names[1])
                plt.show()

            elif(int(var.get()) == 2):
                analysis = Toplevel(main)
                analysis.title("Analysis - Multiple Regression Summary 1")
                analysis.geometry("1200x680")

                analysis2 = Toplevel(main)
                analysis2.title("Analysis - Multiple Regression Summary 2")
                analysis2.geometry("1200x680")

                filename = askopenfilename(filetypes=[("CSV Files", "*.csv")])
                df = pd.read_csv(filename)

                data_x = df.iloc[:, 0:2]
                data_x1 = df.iloc[:, [0]]
                data_x2 = df.iloc[:, [1]]
                data_y = df.iloc[:, [2]]

                data_x = sm.add_constant(data_x)

                ks = sm.OLS(data_y, data_x)
                ks_res =ks.fit()
                ks_res.summary()
                
                print(ks_res.summary())

                lb1 = Label(analysis, text=ks_res.summary(), font="Consolas", justify="left")
                lb1.pack()

                column_headers = list(df.columns.values)

                dividerA  = "******************************************************************************\n"
                regTitleA = "          skLearn Multiple Regression Results - "+column_headers[0]+"           \n"
                lb2 = Label(analysis2, text=dividerA+regTitleA, font="Consolas", justify="left")
                lb2.pack()

                reg1 = skl.linear_model.LinearRegression().fit(data_x1, data_y)

                score = "Score:        " + str(reg1.score(data_x1, data_y))
                global interceptMR1, coefficientMR1
                interceptMR1Display = "\nIntercept:    " + str(reg1.intercept_)
                coefficientMR1Display = "\nCoefficient:  " + str(reg1.coef_)
                interceptMR1 = float(reg1.intercept_)
                coefficientMR1 = float(reg1.coef_)

                summary3 = score + interceptMR1Display + coefficientMR1Display 
                lb3 = Label(analysis2, text=summary3, font="Consolas", justify="left")
                lb3.pack()

                dividerB  = "******************************************************************************\n"
                regTitleB = "          skLearn Multiple Regression Results - "+column_headers[1]+"            \n"
                lb4 = Label(analysis2, text=dividerB+regTitleB, font="Consolas", justify="left")
                lb4.pack()

                reg2 = skl.linear_model.LinearRegression().fit(data_x2, data_y)

                score = "Score:        " + str(reg2.score(data_x2, data_y))
                global interceptMR2, coefficientMR2
                interceptMR2Display = "\nIntercept:    " + str(reg2.intercept_)
                coefficientMR2Display = "\nCoefficient:  " + str(reg2.coef_)
                interceptMR2 = float(reg2.intercept_)
                coefficientMR2 = float(reg2.coef_)

                summary4 = score + interceptMR2Display + coefficientMR2Display
                lb5 = Label(analysis2, text=summary4, font="Consolas", justify="left")
                lb5.pack()


                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
                ax.scatter(data_x1, data_x2, data_y, c='blue', marker='o')

                # set your labels
                ax.set_xlabel(column_headers[0])
                ax.set_ylabel(column_headers[1])
                ax.set_zlabel(column_headers[2])

                plt.savefig('regplot.png')
                plt.show()

                # l = tk.Label(frame, text="Hello", font="-size 50")
                # l.pack()

                # l = tk.Label(frame, text="World", font="-size 50")
                # l.pack()

                # l = tk.Label(frame, text="Test text 1\nTest text 2\nTest text 3\nTest text 4\nTest text 5\nTest text 6\nTest text 7\nTest text 8\nTest text 9", font="-size 20")
                # l.pack()

            elif(int(var.get()) == 3):
                analysis = Toplevel(main)
                analysis.title("Analysis - Logistic Regression Summary 1")
                analysis.geometry("830x480")

                analysis2 = Toplevel(main)
                analysis2.title("Analysis - Logistic Regression Summary 2")
                analysis2.geometry("830x480")

                filename = askopenfilename(filetypes=[("CSV Files", "*.csv")])
                df = pd.read_csv(filename)
                X_train = df.iloc[:, [0]]
                y_train = df.iloc[:, [1]]

                X_train = sm.add_constant(X_train)
                print("111")
                print(X_train.max()[1])
                print("111")

                column_names = list(df.columns)

                logit_model = sm.Logit(y_train, X_train).fit()

                lb1 = Label(analysis,text=logit_model.summary(), font="Consolas", justify="left")
                lb1.pack()

                reg = skl.linear_model.LogisticRegression().fit(X_train[:], y_train[:])

                divider  = "\n******************************************************************************\n"
                regTitle = "                       skLearn Logistic Regression Results                        "
                lb2 = Label(analysis,text=divider+regTitle, font="Consolas", justify="left")
                lb2.pack()

                score = "Score:        " + str(round(float(reg.score(X_train, y_train)), 5))
                global interceptLogR, coefficientConstLogR, coefficientXLogR, interceptLogRDisplay, coefficientLogRDisplay
                interceptLogRDisplay = "\nIntercept:    " + str(reg.intercept_)
                print(interceptLogRDisplay)
                coefficientLogRDisplay = "\nCoefficient:  " + str(reg.coef_)
                print(coefficientLogRDisplay)
                interceptLogR = float(reg.intercept_)
                coefficientConstLogR = float(reg.coef_[0][0])
                coefficientXLogR = float(reg.coef_[0][1])

                summary2 = score + interceptLogRDisplay + coefficientLogRDisplay
                lb3 = Label(analysis,text=summary2, font="Consolas", justify="left")
                lb3.pack()

                lb4 = Label(analysis2,text=logit_model.summary2(), font="Consolas", justify="left")
                lb4.pack()
                
                X_train = df.iloc[:, [0]]
                plt.scatter(X_train, y_train, color = "m", marker = "o", s = 30)

                X_train = sm.add_constant(X_train)
                X_test = np.arange(0, int(X_train.max()[1]), 0.1)
                y_test = sp.special.expit(X_test * reg.coef_[0][1] + reg.intercept_[0])
                plt.plot(X_test, y_test, label="Logistic Regression Model", color="red", linewidth=3)
                plt.savefig('regplot.png')
                plt.show() 

            
            elif(int(var.get()) == 4):
                analysis = Toplevel(main)
                analysis.title("Analysis - Problem Tree Analysis")
                analysis.geometry("830x480")

                class ShapeEditorApp:

                    def __init__(self, root):
                        global textValue
                        textValue = StringVar()

                        self.root = root
                        self.root.title("Problem Tree Analysis")

                        # Create Canvas widget
                        self.canvas = tk.Canvas(analysis, bg="white")
                        self.canvas.pack(fill=tk.BOTH, expand=True)

                        # Initialize shape variables
                        self.current_shape = None
                        self.start_x = None
                        self.start_y = None
                        self.current_shape_item = None

                        # Create buttons
                        self.color_button = tk.Button(root, text="Color", command=self.choose_color)
                        self.pen_button = Button(root, text='Pen', command=self.use_pen)
                        self.rect_button = tk.Button(root, text="Rectangle", command=self.create_rectangle)
                        self.circle_button = tk.Button(root, text="Arrow", command=self.create_arrow)
                        self.clear_button = tk.Button(root, text="Clear", command=self.clear_canvas)
                        self.text_frame = Frame(root, height=100, width=200, relief=SUNKEN, borderwidth=3)
                        self.text_entry = Entry(self.text_frame, textvariable=textValue, bg="white" , width=20)
                        self.pen_button.pack(side=tk.LEFT)
                        self.clear_button.pack(side=tk.LEFT)
                        self.color_button.pack(side=tk.LEFT)
                        self.rect_button.pack(side=tk.LEFT)
                        self.circle_button.pack(side=tk.LEFT)
                        self.text_frame.pack(side=tk.LEFT)                         
                        self.text_entry.pack(side=tk.LEFT)

                        # Bind mouse events
                        self.canvas.bind("<Button-1>", self.start_draw)
                        self.canvas.bind("<B1-Motion>", self.draw_shape)
                        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)
                        self.canvas.bind("<Button-2>", self.add_text)
                        self.canvas.bind("<Button-3>", self.add_text)

                    def add_text(self, event):
                        self.canvas.create_text(event.x, event.y, text=textValue.get())
                    
                    def use_pen(self):
                        self.activate_button(self.pen_button)

                    def choose_color(self):
                        global color 
                        color = colorchooser.askcolor(title="Choose color")

                    def create_rectangle(self):
                        self.current_shape = "rectangle"

                    def create_arrow(self):
                        self.current_shape = "arrow"

                    def start_draw(self, event):
                        self.start_x = event.x
                        self.start_y = event.y
                        if self.current_shape == "rectangle":
                            self.current_shape_item = self.canvas.create_rectangle(
                                self.start_x, self.start_y, self.start_x, self.start_y, outline=color[1]
                            )
                        elif self.current_shape == "arrow":
                            self.current_shape_item = self.canvas.create_line(
                                self.start_x, self.start_y, self.start_x, self.start_y, fill=color[1], arrow="last", width=5
                            )

                    def draw_shape(self, event):
                        if self.current_shape_item:
                            x, y = event.x, event.y
                            self.canvas.coords(self.current_shape_item, self.start_x, self.start_y, x, y)

                    def stop_draw(self, event):
                        self.current_shape_item = None

                    def clear_canvas(self):
                        self.canvas.delete("all")

                app = ShapeEditorApp(analysis)
        
        def back_3():
            global pageNumber
            pageNumber -= 1
            print(pageNumber)
            frame4.destroy() 
            frame4.forget() 
            btnBack3.destroy()
            btnNext3.destroy() 
            page_3()
        
        def next_3():
            global pageNumber
            pageNumber += 1
            print(pageNumber)
            frame4.destroy()
            frame4.forget()
            btnBack3.destroy()
            btnNext3.destroy() 
            analyses()
            page_5()

        btnBack3 = Button(mainProject, text = "Back", width=10, command = lambda: back_3())
        btnNext3 = Button(mainProject, text = "Next", width=10, command = lambda: next_3())
        btnBack3.place(x=190, y=170)
        btnNext3.place(x=380, y=170)

    global p5rootcause
    p5rootcause = " "
    
    def page_5(): 
        mainProject.state('zoomed')
        style.configure('Treeview', rowheight=320)

        frame5 = tk.LabelFrame(mainProject)

        status.config(text="")
        
        rootCauseLabel = Label(frame5, text = "Root Cause of the Problem")
        rootCause = Entry(frame5, width=200)

        assessmentLabel = Label(frame5, text = "Assessment of Existing Policies that Address the Root Cause")
        assessmentTable=ttk.Treeview(frame5, selectmode="browse", height=1)
        assessmentTable["columns"]=("1","2","3","4")
        assessmentTable['show']='headings'
        assessmentTable.column("1",width=150,anchor='c')
        assessmentTable.column("2",width=650,anchor='c')
        assessmentTable.column("3",width=400,anchor='c')
        assessmentTable.column("4",width=300,anchor='c')
        assessmentTable.heading("1",text="Existing Policy")
        assessmentTable.heading("2",text="Relevant Provision(s)")
        assessmentTable.heading("3",text="Accomplishments")
        assessmentTable.heading("4",text="Assessment")

        existLabel = Label(mainProject, text = "Existing Policy")
        releLabel = Label(mainProject, text = "Relevant Provision")
        accompLabel2 = Label(mainProject, text = "Accomplishment")
        assessLabel2 = Label(mainProject, text = "Assessment")

        existingPolicy = scrolledtext.ScrolledText(mainProject, height = 9, width=40)
        relevantProvision = scrolledtext.ScrolledText(mainProject, height = 9, width=40)
        accomplishment2 = scrolledtext.ScrolledText(mainProject, height = 9, width=40)
        assessment2 = scrolledtext.ScrolledText(mainProject, height = 9, width=40)

        addButton2 = tk.Button(mainProject, text='Add', width=10, command=lambda: add_data2())  
        editButton2 = tk.Button(mainProject, text="Edit", width=10, command=lambda: edit_data2())

        def show_data2(a):
            existingPolicy.delete(0,END)
            relevantProvision.delete(0,END)
            accomplishment2.delete(0,END)
            assessment2.delete(0,END)

            selectedItem = assessmentTable.selection()[0]
            existingPolicy.insert(0, assessmentTable.item(selectedItem)['values'][0])
            relevantProvision.insert(0, assessmentTable.item(selectedItem)['values'][1])
            accomplishment2.insert(0, assessmentTable.item(selectedItem)['values'][2])
            assessment2.insert(0, assessmentTable.item(selectedItem)['values'][3])

        assessmentTable.bind("<<TreeviewSelect>>", show_data2)

        def edit_data2():
            existingPolicyText = existingPolicy.get("1.0", tk.END)               # read existing policy
            relevantProvisionText = relevantProvision.get("1.0", tk.END)         # read relevant provision
            accomplishment2Text = accomplishment2.get("1.0", tk.END)             # read accomplishment 
            assessment2Text = assessment2.get("1.0", tk.END)                     # read assessment                 
                                    
            selected_item = assessmentTable.selection()[0]
            assessmentTable.item(selected_item, text="blub", values=(existingPolicyText, relevantProvisionText, accomplishment2Text, assessment2Text))

        def add_data2():
            existingPolicyText = existingPolicy.get("1.0", tk.END)               # read existing policy
            relevantProvisionText = relevantProvision.get("1.0", tk.END)         # read relevant provision
            accomplishment2Text = accomplishment2.get("1.0", tk.END)             # read accomplishment 
            assessment2Text = assessment2.get("1.0", tk.END)                     # read assessment      

            global assessmentTuple
            assessmentTuple = [existingPolicyText, relevantProvisionText, accomplishment2Text, assessment2Text]

            # effortList.append(efforttuple)

            assessmentTable.insert("",'end', values=(existingPolicyText, relevantProvisionText, accomplishment2Text, assessment2Text))
            existingPolicyText.delete('1.0',END)                    # reset the text entry box
            relevantProvisionText.delete('1.0',END)                 # reset the text entry box
            accomplishment2Text.delete('1.0',END)                   # reset the text entry box
            assessment2Text.delete('1.0',END)                       # reset the text entry box
            existingPolicyText.focus() 

        frame5.place(x=10, y=10)
        rootCauseLabel.grid(row=0, column=1)
        rootCause.grid(row=1, column=1)
        assessmentLabel.grid(row=2, column=1)
        assessmentTable.grid(row=3, column=1)
        existLabel.place(x=150, y=480)
        existingPolicy.place(x=40, y=510)
        releLabel.place(x=520, y=480)
        relevantProvision.place(x=410, y=510)
        accompLabel2.place(x=900, y=480)
        accomplishment2.place(x=780, y=510)
        assessLabel2.place(x=1280, y=480)
        assessment2.place(x=1150, y=510)
        addButton2.place(x=640, y=690)
        editButton2.place(x=790, y=690)

        def back_4():
            global pageNumber
            pageNumber -= 1
            print(pageNumber)
            mainProject.state('normal')
            frame5.destroy() 
            existLabel.destroy()
            existingPolicy.destroy()
            existingPolicy.place_forget()
            releLabel.destroy()
            relevantProvision.destroy()
            relevantProvision.place_forget()
            accompLabel2.destroy()
            accomplishment2.destroy()
            accomplishment2.place_forget()
            assessLabel2.destroy()
            assessment2.destroy()
            assessment2.place_forget()
            btnBack4.destroy()
            btnNext4.destroy() 
            addButton2.destroy()
            editButton2.destroy()
            page_4()
            

        def next_4():
            global pageNumber
            pageNumber += 1
            print(pageNumber)
            global p5rootcause
            p5rootcause = rootCause.get()
            if not p5rootcause.strip():
                status.config(
                    text="Enter root cause",
                    foreground="red",
                )
                return
            
            mainProject.state('normal')
            frame5.destroy() 
            existLabel.destroy()
            existingPolicy.destroy()
            existingPolicy.place_forget()
            releLabel.destroy()
            relevantProvision.destroy()
            relevantProvision.place_forget()
            accompLabel2.destroy()
            accomplishment2.destroy()
            accomplishment2.place_forget()
            assessLabel2.destroy()
            assessment2.destroy()
            assessment2.place_forget()
            btnBack4.destroy()
            btnNext4.destroy() 
            addButton2.destroy()
            editButton2.destroy()
            page_6()

        btnBack4 = Button(mainProject, text = "Back", width=10, command = lambda: back_4())
        btnNext4 = Button(mainProject, text = "Next", width=10, command = lambda: next_4())
        btnBack4.place(x=640, y=750)
        btnNext4.place(x=790, y=750)
        status.place(x=10, y=700)

    global p6policyproblem, p6policyissue
    p6policyproblem = " "
    p6policyissue = " "

    def page_6():                                                   # write problematic situation and undesirable effects
        mainProject.geometry("660x210")

        frame6 = tk.LabelFrame(mainProject)

        status.config(text="")

        policyProbLabel = Label(frame6, text = "Policy Problem")
        policyProb = scrolledtext.ScrolledText(frame6, height = 8, width=30)
        
        policyIssueLabel = Label(frame6, text = "Policy Issue Statement")
        policyIss = scrolledtext.ScrolledText(frame6, height = 8, width=30)
        
        frame6.place(x=40, y=10)
        status.place(x=10, y=170)
        policyProbLabel.grid(row=1, column=0, sticky = W, padx=7)
        policyProb.grid(row=2, column=0, sticky = W, padx=7)
        policyIssueLabel.grid(row=1, column=1, sticky = W, padx=7)
        policyIss.grid(row=2, column=1, sticky = W, padx=7)

        def back_5():
            global pageNumber
            pageNumber -= 1
            print(pageNumber)
            frame6.destroy() 
            btnBack5.destroy()
            btnNext5.destroy() 
            page_5()
        
        def next_5():
            global p6policyproblem, p6policyissue
            p6policyproblem = policyProb.get("1.0", tk.END)
            if not p6policyproblem.strip():
                status.config(
                text="Enter policy\nproblem",
                foreground="red",
            )
                return
                    
            p6policyissue = policyIss.get("1.0", tk.END)
            if not p6policyissue.strip():
                status.config(
                text="Enter policy\nissue statement",
                foreground="red",
            )
                return
            global pageNumber
            pageNumber += 1
            print(pageNumber)
            frame6.destroy() 
            btnBack5.destroy()
            btnNext5.destroy() 
            page_7()

        btnBack5 = Button(mainProject, text = "Back", width=10, command = lambda: back_5())
        btnNext5 = Button(mainProject, text = "Next", width=10, command = lambda: next_5())
        btnBack5.place(x=140, y=170)
        btnNext5.place(x=400, y=170)

    p7policyGoalsandObjectives = []
    p7indicators = []

    def page_7():
        mainProject.geometry("880x500")
        style.configure('Treeview', rowheight=40)

        # write problematic situation and undesirable effects

        frame7 = tk.LabelFrame(mainProject)

        goalsObjLabel = Label(frame7, text = "Goals and Objectives of the Proposal")
        
        goalsandObjTable=ttk.Treeview(frame7, height=5)
        goalsandObjTable["columns"]=("1","2")
        goalsandObjTable['show']='headings'
        goalsandObjTable.column("1",width=350,anchor='c')
        goalsandObjTable.column("2",width=500,anchor='c')
        goalsandObjTable.heading("1",text="Policy Goals and Objectives")
        goalsandObjTable.heading("2",text="Indicators")

        for i in range(0, len(p7indicators)):
            goalsandObjTable.insert("",'end', values=(p7policyGoalsandObjectives[i], p7indicators[i]))

        pgoLabel = Label(mainProject, text = "Policy Goals and Objectives")
        indiLabel = Label(mainProject, text = "Indicators")

        pgo = tk.Entry(mainProject, width=40) 
        indi = scrolledtext.ScrolledText(mainProject, height = 3, width=55) 

        addButton3 = tk.Button(mainProject, text='Add', width=10, command=lambda: add_data3())  
        editButton3 = tk.Button(mainProject, text="Edit", width=10, command=lambda: edit_data3())

        def show_data3(a):
            pgo.delete(0,END)
            indi.delete("1.0", tk.END)

            selectedItem = goalsandObjTable.selection()[0]
            pgo.insert(0, goalsandObjTable.item(selectedItem)['values'][0])
            indi.insert("1.0", goalsandObjTable.item(selectedItem)['values'][1])

        goalsandObjTable.bind("<<TreeviewSelect>>", show_data3)

        def edit_data3():
            pgoText = pgo.get()                                         # read policy goal and objective
            indiText = indi.get("1.0", tk.END)                          # read indicator

            selected_item = goalsandObjTable.selection()[0]
            goalsandObjTable.item(selected_item, text="blub", values=(pgoText, indiText))

            p7policyGoalsandObjectives.pop(goalsandObjTable.index(selected_item))
            p7policyGoalsandObjectives.insert(goalsandObjTable.index(selected_item), pgoText)
            p7indicators.pop(goalsandObjTable.index(selected_item))
            p7indicators.insert(goalsandObjTable.index(selected_item), indiText)

        def add_data3():
            pgoText = pgo.get()                                         # read policy goal and objective
            indiText = indi.get("1.0", tk.END)                          # read indicator

            p7policyGoalsandObjectives.append(pgoText)
            p7indicators.append(indiText)

            goalsandObjTable.insert("",'end', values=(pgoText, indiText))
            pgo.delete(0,END)  # reset the text entry box
            indi.delete('1.0',END)  # reset the text entry box
            pgo.focus() 

        frame7.place(x=10, y=10)
        goalsObjLabel.grid(row=0, column=1)
        goalsandObjTable.grid(row=1, column=1)
        pgoLabel.place(x=110, y=270)
        pgo.place(x=60, y=300)
        indiLabel.place(x=590, y=270)
        indi.place(x=390, y=290)
        addButton3.place(x=260, y=380)
        editButton3.place(x=520, y=380)

        def back_6():
            global pageNumber
            pageNumber -= 1
            print(pageNumber)
            frame7.destroy() 
            pgoLabel.destroy()
            pgo.destroy()
            indiLabel.destroy()
            indi.destroy()
            addButton3.destroy()
            editButton3.destroy()
            btnBack6.destroy()
            btnNext6.destroy() 
            page_6()
        
        def next_6():
            frame7.destroy() 
            pgoLabel.destroy()
            pgo.destroy()
            indiLabel.destroy()
            indi.place_forget()
            addButton3.destroy()
            editButton3.destroy()
            btnBack6.destroy()
            btnNext6.destroy() 
            page_8()

        btnBack6 = Button(mainProject, text = "Back", width=10, command = lambda: back_6())
        btnNext6 = Button(mainProject, text = "Next", width=10, command = lambda: next_6())
        btnBack6.place(x=260, y=440)
        btnNext6.place(x=520, y=440)

    p8stakeholders = []
    p8actors = []

    def page_8():
        style.configure('Treeview', rowheight=20)
        mainProject.geometry("740x500")

        frame8 = tk.LabelFrame(mainProject)

        staAndActLabel = Label(frame8, text = "Stakeholders and Actors")
        
        staAndActTable=ttk.Treeview(frame8, height=10)
        staAndActTable["columns"]=("1","2")
        staAndActTable['show']='headings'
        staAndActTable.column("1",width=350,anchor='c')
        staAndActTable.column("2",width=350,anchor='c')
        staAndActTable.heading("1",text="Stakeholders")
        staAndActTable.heading("2",text="Actors")

        for i in range(0, len(p8stakeholders)):
            staAndActTable.insert("",'end', values=(p8stakeholders[i], p8actors[i]))

        sb = Scrollbar(frame8, orient=VERTICAL)

        staAndActTable.configure(yscrollcommand=sb.set)  # connect to Treeview
        sb.config(command=staAndActTable.yview)

        global stakeholders, actors, addButton4, editButton4
        stakeholdersLabel = Label(mainProject, text = "Stakeholders")
        actorsLabel = Label(mainProject, text = "Actors")

        stakeholders = tk.Entry(mainProject, width=40) 
        actors = tk.Entry(mainProject, width=40) 

        addButton4 = tk.Button(mainProject, text='Add', width=10, command=lambda: add_data4())  
        editButton4 = tk.Button(mainProject, text="Edit", width=10, command=lambda: edit_data4())

        def show_data4(a):
            stakeholders.delete(0,END)
            actors.delete(0,END)

            selectedItem = staAndActTable.selection()[0]
            stakeholders.insert(0, staAndActTable.item(selectedItem)['values'][0])
            actors.insert(0, staAndActTable.item(selectedItem)['values'][1])

        staAndActTable.bind("<<TreeviewSelect>>", show_data4)

        def edit_data4():
            stakeholdersText = stakeholders.get()           # read stakeholders
            actorsText = actors.get()                       # read actors

            selected_item = staAndActTable.selection()[0]
            staAndActTable.item(selected_item, text="blub", values=(stakeholdersText, actorsText))

            p8stakeholders.pop(staAndActTable.index(selected_item))
            p8stakeholders.insert(staAndActTable.index(selected_item), stakeholdersText)
            p8actors.pop(staAndActTable.index(selected_item))
            p8actors.insert(staAndActTable.index(selected_item), actorsText)

        def add_data4():
            stakeholdersText = stakeholders.get()           # read stakeholders
            actorsText = actors.get()                       # read actors

            staAndActTable.insert("",'end', values=(stakeholdersText, actorsText))
            stakeholders.delete('1.0',END)  # reset the text entry box
            actors.delete('1.0',END)  # reset the text entry box
            stakeholders.focus() 

            p8stakeholders.append(stakeholdersText)
            p8actors.append(actorsText)
        
        frame8.place(x=10, y=10)
        staAndActLabel.grid(row=0, column=0, columnspan=2)
        staAndActTable.grid(row=1, column=0)
        sb.grid(row=0, column=1, rowspan=2)
        stakeholdersLabel.place(x=140, y=270)
        stakeholders.place(x=60, y=300)
        actorsLabel.place(x=520, y=270)
        actors.place(x=420, y=300)
        addButton4.place(x=185, y=360)
        editButton4.place(x=445, y=360)

        def back_7():
            global pageNumber
            pageNumber -= 1
            print(pageNumber)
            global stakeholders, actors, addButton4, editButton4
            frame8.destroy()      
            btnNext7.destroy()    
            stakeholdersLabel.destroy()
            stakeholders.destroy()
            actorsLabel.destroy()
            actors.destroy()
            addButton4.destroy()
            editButton4.destroy()   
            btnBack7.destroy()
            btnNext7.destroy() 
            page_7()
        
        def next_7():
            global stakeholders, actors, addButton4, editButton4
            frame8.destroy()      
            btnNext7.destroy()    
            stakeholdersLabel.destroy()
            stakeholders.destroy()
            actorsLabel.destroy()
            actors.destroy()
            addButton4.destroy()
            editButton4.destroy() 
            btnBack7.destroy()
            btnNext7.destroy() 
            page_9()

        btnBack7 = Button(mainProject, text = "Back", width=10, command = lambda: back_7())
        btnNext7 = Button(mainProject, text = "Next", width=10, command = lambda: next_7())
        btnBack7.place(x=185, y=420)
        btnNext7.place(x=445, y=420)

    global p9alternatives
    p9alternatives = []
    
    def page_9():               
        mainProject.geometry("870x545")

        style.configure('Treeview', rowheight=15)

        frame9 = tk.LabelFrame(mainProject)
        frame9.columnconfigure(0, weight=2)
        frame9.columnconfigure(1, weight=2)
        frame9.columnconfigure(2, weight=2)
        frame9.columnconfigure(3, weight=2)
        frame9.columnconfigure(4, weight=2)
        frame9.rowconfigure(0, weight=1)
        frame9.rowconfigure(1, weight=1)
        frame9.rowconfigure(2, weight=1)
        frame9.rowconfigure(3, weight=1)
        frame9.rowconfigure(4, weight=1)
        frame9.rowconfigure(5, weight=1)
        frame9.rowconfigure(6, weight=1)
        frame9.rowconfigure(7, weight=1)
        frame9.rowconfigure(8, weight=1)
        frame9.rowconfigure(9, weight=1)

        assessAlterLabel = Label(frame9, text = "Assessment of the Policy Alternatives")
        assessAlterLabel.grid(row=0, column=0, columnspan=2)

        assessAlterTable=ttk.Treeview(frame9, height=10)
        assessAlterTable["columns"]=("1", "2")  
        assessAlterTable['show']='headings'  
        assessAlterTable.column("1", width=140, anchor='c')
        assessAlterTable.column("2", width=300, anchor='c')
        assessAlterTable.heading("1",text="Policy Alternative No.")
        assessAlterTable.heading("2",text="Policy Alternative")

        polAltNoLabel = Label(mainProject, text = "Policy Alternative No.\n")
        policyAlternativeNo = tk.Entry(mainProject, width=20) 
        polAltLabel = Label(mainProject, text = "Policy Alternative\n")
        policyAlternatives = tk.Entry(mainProject, width=50) 

        addButton5 = tk.Button(mainProject, text='Add', width=10, command=lambda: add_data5())  
        editButton5 = tk.Button(mainProject, text="Edit", width=10, command=lambda: edit_data5())
        computeButton = tk.Button(mainProject, text="Compute", width=10, command=lambda: compute())

        def show_data5(a):
            policyAlternativeNo.delete(0,END)
            policyAlternatives.delete(0,END)

            selectedItem = assessAlterTable.selection()[0]
            policyAlternativeNo.insert(0, assessAlterTable.item(selectedItem)['values'][0])
            policyAlternatives.insert(0, assessAlterTable.item(selectedItem)['values'][1])

        assessAlterTable.bind("<<TreeviewSelect>>", show_data5)

        def edit_data5():
            policyAlternativeNoText = policyAlternativeNo.get()           # read stakeholders
            policyAlternativesText = policyAlternatives.get()             # read actors

            selected_item = assessAlterTable.selection()[0]
            assessAlterTable.item(selected_item, text="blub", values=(policyAlternativeNoText, policyAlternativesText))
            
            p9alternatives.pop(assessAlterTable.index(selected_item))
            p9alternatives.insert(assessAlterTable.index(selected_item), policyAlternativesText)

        def add_data5():
            policyAlternativeNoText = policyAlternativeNo.get()           # read stakeholders
            policyAlternativesText = policyAlternatives.get()             # read actors

            p9alternatives.append(policyAlternativesText)

            assessAlterTable.insert("",'end', values=(policyAlternativeNoText, policyAlternativesText))
            policyAlternativeNo.delete('1.0',END)  # reset the text entry box
            policyAlternatives.delete('1.0',END)  # reset the text entry box
            stakeholders.focus() 

        frame9.place(x=10, y=10)

        column3 = Label(frame9, text="Effectiveness")
        column3.grid(row=1, column=2)

        column4 = Label(frame9, text="Cost-efficiency")
        column4.grid(row=1, column=3)

        column5 = Label(frame9, text="Acceptability")
        column5.grid(row=1, column=4)

        column6 = Label(frame9, text="Criteria")
        column6.grid(row=0, column=2, columnspan=3)

        assessAlterTable.grid(row=1, rowspan=7, column=0, columnspan=2)

        polAltNoLabel.place(x=139, y=300)
        policyAlternativeNo.place(x=135, y=330)
        polAltLabel.place(x=520, y=300)
        policyAlternatives.place(x=420, y=330)
        addButton5.place(x=265, y=400)
        editButton5.place(x=550, y=400)
        computeButton.place(x=590, y=250)

        varEffec = IntVar(value=0)
        varCostEff = IntVar(value=0)
        varAccept = IntVar(value=0)
    
        R1_2 = Radiobutton(frame9, text="SLR", variable=varEffec, value=1)
        R2_2 = Radiobutton(frame9, text="MR", variable=varEffec, value=2)
        R3_2 = Radiobutton(frame9, text="LogR", variable=varEffec, value=3)
        R4_2 = Radiobutton(frame9, text="FGD", variable=varEffec, value=4)
        R5_2 = Radiobutton(frame9, text="Tangible Cost-Benefit Analysis\nw/ Discounting", variable=varCostEff, value=1)
        R6_2 = Radiobutton(frame9, text="Tangible Cost-Benefit Analysis\nw/o Discounting", variable=varCostEff, value=2)
        R7_2 = Radiobutton(frame9, text="Intangible Cost-Benefit Analysis", variable=varCostEff, value=3)
        R8_2 = Radiobutton(frame9, text="PRINCE Method", variable=varAccept, value=1)
        R9_2 = Radiobutton(frame9, text="Stakeholder Analysis", variable=varAccept, value=2)

        R1_2.grid(row=3, column=2)
        R2_2.grid(row=4, column=2)
        R3_2.grid(row=5, column=2)
        R4_2.grid(row=8, column=2)
        R5_2.grid(row=4, column=3)
        R6_2.grid(row=5, column=3)
        R7_2.grid(row=8, column=3)
        R8_2.grid(row=4, column=4)
        R9_2.grid(row=8, column=4)

        def back_8():
            global pageNumber
            pageNumber -= 1
            print(pageNumber)
            frame9.destroy()       
            polAltLabel.destroy()
            policyAlternatives.destroy()
            polAltNoLabel.destroy()
            policyAlternativeNo.destroy()
            addButton5.destroy()
            editButton5.destroy()   
            computeButton.destroy()   
            btnBack8.destroy()
            btnNext8.destroy()
            page_8()

        def next_8():
            frame9.destroy()       
            polAltLabel.destroy()
            policyAlternatives.destroy()
            polAltNoLabel.destroy()
            policyAlternativeNo.destroy()
            addButton5.destroy()
            editButton5.destroy()   
            computeButton.destroy()   
            btnBack8.destroy()
            btnNext8.destroy()
            page_10()

        def compute():
            print(p9alternatives)
            netBenefitWithout = []
            netBenefitWith = []
            
            crite = [int(varEffec.get()), int(varCostEff.get()), int(varAccept.get())]
            print(crite)

            if int(varEffec.get()) == 1: 
                def windowPerAlt(a, policyAlt):
                    effectiveness1 = Toplevel(main)
                    effectiveness1.title("Effectiveness: Simple LR")
                    effectiveness1.geometry("830x480")
                    
                    equation = "y = "+str(coefficientLR)+"x + "+str(interceptLR)+"\n"
                    equationWithLabel = Label(effectiveness1, text="\nEquation  :  "+equation, font="Consolas", justify="left")
                    equationWithLabel.pack()

                    simpleLRLabel = Label(effectiveness1, text = "Alternative " + str(a+1) + " - " + policyAlt)
                    simpleLRTable=ttk.Treeview(effectiveness1)
                    simpleLRTable["columns"]=("1","2","3")
                    simpleLRTable['show']='headings'
                    simpleLRTable.column("1",width=130,anchor='c')
                    simpleLRTable.column("2",width=130,anchor='c')
                    simpleLRTable.column("3",width=130,anchor='c')
                    simpleLRTable.heading("1",text="Year")
                    simpleLRTable.heading("2",text="X")
                    simpleLRTable.heading("3",text="Y")

                    yearLabel = Label(effectiveness1, text = "Year")
                    inputXLabel = Label(effectiveness1, text = "X")

                    year = tk.Entry(effectiveness1, width=30)
                    inputX = tk.Entry(effectiveness1, width=30) 

                    addButton = tk.Button(effectiveness1, text='Add', width=10, command=lambda: add_data())  
                    editButton = tk.Button(effectiveness1, text="Edit", width=10, command=lambda: edit_data())

                    years = []

                    def show_data(a):
                        year.delete(0,END)
                        inputX.delete(0,END)

                        selectedItem = simpleLRTable.selection()[0]
                        year.insert(0, simpleLRTable.item(selectedItem)['values'][0])
                        inputX.insert(0, simpleLRTable.item(selectedItem)['values'][1])

                    simpleLRTable.bind("<<TreeviewSelect>>", show_data)    

                    am = 0
                    def edit_data():
                        yearText = year.get()                                   # get year

                        selected_item = simpleLRTable.selection()[0]

                        years.pop(simpleLRTable.index(selected_item))
                        years.insert(simpleLRTable.index(selected_item), int(yearText))

                        inputXText = float(inputX.get())                                                    # get X
                        outputYText = float(inputX.get())*float(coefficientLR) + float(interceptLR)         # compute for Y
                        
                        simpleLRTable.item(selected_item, text="blub", values=(yearText, inputXText, outputYText))

                    def add_data():
                        yearText = year.get()                                   # get year
                        inputXText = int(inputX.get())                        # get benefit
                        outputYText = float(inputX.get())*float(coefficientLR) + float(interceptLR)         # compute for Y

                        years.append(int(yearText))

                        year.delete(0,END)
                        inputX.delete(0,END)

                        global assessmentTuple
                        assessmentTuple = [yearText, inputXText, outputYText]

                        # effortList.append(efforttuple)

                        simpleLRTable.insert("",'end', values=(yearText, inputXText, outputYText))
                        yearText.delete('1.0',END)                      # reset the text entry box
                        inputX.delete('1.0',END)                        # reset the text entry box
                        yearText.focus() 
                    
                    simpleLRLabel.pack()
                    simpleLRTable.pack()
                    yearLabel.place(x=210, y=360)
                    year.place(x=300, y=360)
                    inputXLabel.place(x=210, y=420)
                    inputX.place(x=300, y=420)
                    addButton.place(x=540, y=360)
                    editButton.place(x=540, y=420)

                a = 0

                while (a < len(p9alternatives)):
                    windowPerAlt(a, p9alternatives[a])
                    a += 1

            elif int(varEffec.get()) == 2: 
                def window1PerAlt(a, policyAlt):
                    effectivenessMR1 = Toplevel(main)
                    effectivenessMR1.title("Effectiveness: MR1")
                    effectivenessMR1.geometry("830x480")
                    
                    equation = "y = "+str(coefficientMR1)+"x + "+str(interceptMR1)+"\n"
                    equationWithLabel = Label(effectivenessMR1, text="\nEquation  :  "+equation, font="Consolas", justify="left")
                    equationWithLabel.pack()

                    MR1Label = Label(effectivenessMR1, text = "Alternative " + str(a+1) + " - " + policyAlt)
                    MR1Table=ttk.Treeview(effectivenessMR1)
                    MR1Table["columns"]=("1","2","3")
                    MR1Table['show']='headings'
                    MR1Table.column("1",width=130,anchor='c')
                    MR1Table.column("2",width=130,anchor='c')
                    MR1Table.column("3",width=130,anchor='c')
                    MR1Table.heading("1",text="Year")
                    MR1Table.heading("2",text="X")
                    MR1Table.heading("3",text="Y")

                    yearLabel = Label(effectivenessMR1, text = "Year")
                    inputXLabel = Label(effectivenessMR1, text = "X")

                    year = tk.Entry(effectivenessMR1, width=30)
                    inputX = tk.Entry(effectivenessMR1, width=30) 

                    addButton = tk.Button(effectivenessMR1, text='Add', width=10, command=lambda: add_data())  
                    editButton = tk.Button(effectivenessMR1, text="Edit", width=10, command=lambda: edit_data())

                    years = []

                    def show_data(a):
                        year.delete(0,END)
                        inputX.delete(0,END)

                        selectedItem = MR1Table.selection()[0]
                        year.insert(0, MR1Table.item(selectedItem)['values'][0])
                        inputX.insert(0, MR1Table.item(selectedItem)['values'][1])

                    MR1Table.bind("<<TreeviewSelect>>", show_data)    

                    am = 0
                    def edit_data():
                        yearText = year.get()                                   # get year

                        selected_item = MR1Table.selection()[0]

                        years.pop(MR1Table.index(selected_item))
                        years.insert(MR1Table.index(selected_item), int(yearText))

                        inputXText = float(inputX.get())                                                    # get X
                        outputYText = float(inputX.get())*float(coefficientMR1) + float(interceptMR1)         # compute for Y
                        
                        MR1Table.item(selected_item, text="blub", values=(yearText, inputXText, outputYText))

                    def add_data():
                        yearText = year.get()                                   # get year
                        inputXText = int(inputX.get())                        # get benefit
                        outputYText = float(inputX.get())*float(coefficientMR1) + float(interceptMR2)         # compute for Y

                        years.append(int(yearText))

                        year.delete(0,END)
                        inputX.delete(0,END)

                        global assessmentTuple
                        assessmentTuple = [yearText, inputXText, outputYText]

                        # effortList.append(efforttuple)

                        MR1Table.insert("",'end', values=(yearText, inputXText, outputYText))
                        yearText.delete('1.0',END)                      # reset the text entry box
                        inputX.delete('1.0',END)                        # reset the text entry box
                        yearText.focus() 
                    
                    MR1Label.pack()
                    MR1Table.pack()
                    yearLabel.place(x=210, y=360)
                    year.place(x=300, y=360)
                    inputXLabel.place(x=210, y=420)
                    inputX.place(x=300, y=420)
                    addButton.place(x=540, y=360)
                    editButton.place(x=540, y=420)

                def window2PerAlt(a, policyAlt):
                    effectivenessMR2 = Toplevel(main)
                    effectivenessMR2.title("Effectiveness: MR2")
                    effectivenessMR2.geometry("830x480")
                    
                    equation = "y = "+str(coefficientMR2)+"x + "+str(interceptMR2)+"\n"
                    equationWithLabel = Label(effectivenessMR2, text="\nEquation  :  "+equation, font="Consolas", justify="left")
                    equationWithLabel.pack()

                    MR2Label = Label(effectivenessMR2, text = "Alternative " + str(a+1) + " - " + policyAlt)
                    MR2Table=ttk.Treeview(effectivenessMR2)
                    MR2Table["columns"]=("1","2","3")
                    MR2Table['show']='headings'
                    MR2Table.column("1",width=130,anchor='c')
                    MR2Table.column("2",width=130,anchor='c')
                    MR2Table.column("3",width=130,anchor='c')
                    MR2Table.heading("1",text="Year")
                    MR2Table.heading("2",text="X")
                    MR2Table.heading("3",text="Y")

                    yearLabel = Label(effectivenessMR2, text = "Year")
                    inputXLabel = Label(effectivenessMR2, text = "X")

                    year = tk.Entry(effectivenessMR2, width=30)
                    inputX = tk.Entry(effectivenessMR2, width=30) 

                    addButton = tk.Button(effectivenessMR2, text='Add', width=10, command=lambda: add_data())  
                    editButton = tk.Button(effectivenessMR2, text="Edit", width=10, command=lambda: edit_data())

                    years = []

                    def show_data(a):
                        year.delete(0,END)
                        inputX.delete(0,END)

                        selectedItem = MR2Table.selection()[0]
                        year.insert(0, MR2Table.item(selectedItem)['values'][0])
                        inputX.insert(0, MR2Table.item(selectedItem)['values'][1])

                    MR2Table.bind("<<TreeviewSelect>>", show_data)    

                    am = 0
                    def edit_data():
                        yearText = year.get()                                   # get year

                        selected_item = MR2Table.selection()[0]

                        years.pop(MR2Table.index(selected_item))
                        years.insert(MR2Table.index(selected_item), int(yearText))

                        inputXText = float(inputX.get())                                                    # get X
                        outputYText = float(inputX.get())*float(coefficientMR2) + float(interceptMR2)         # compute for Y
                        
                        MR2Table.item(selected_item, text="blub", values=(yearText, inputXText, outputYText))

                    def add_data():
                        yearText = year.get()                                   # get year
                        inputXText = int(inputX.get())                        # get benefit
                        outputYText = float(inputX.get())*float(coefficientMR2) + float(interceptMR2)         # compute for Y

                        years.append(int(yearText))

                        year.delete(0,END)
                        inputX.delete(0,END)

                        global assessmentTuple
                        assessmentTuple = [yearText, inputXText, outputYText]

                        # effortList.append(efforttuple)

                        MR2Table.insert("",'end', values=(yearText, inputXText, outputYText))
                        yearText.delete('1.0',END)                      # reset the text entry box
                        inputX.delete('1.0',END)                        # reset the text entry box
                        yearText.focus() 
                    
                    MR2Label.pack()
                    MR2Table.pack()
                    yearLabel.place(x=210, y=360)
                    year.place(x=300, y=360)
                    inputXLabel.place(x=210, y=420)
                    inputX.place(x=300, y=420)
                    addButton.place(x=540, y=360)
                    editButton.place(x=540, y=420)

                a = 0

                while (a < len(p9alternatives)):
                    window1PerAlt(a, p9alternatives[a])
                    window2PerAlt(a, p9alternatives[a])
                    a += 1

            elif int(varEffec.get()) == 3: 
                def windowPerAlt(a, policyAlt):
                    effectivenessLogR = Toplevel(main)
                    effectivenessLogR.title("Effectiveness: LogR")
                    effectivenessLogR.geometry("830x480")
                    
                    equation = "y = "+str(coefficientXLogR)+"x + "+str(interceptLogR+coefficientConstLogR)+"\n"
                    equationWithLabel = Label(effectivenessLogR, text="\nEquation  :  "+equation, font="Consolas", justify="left")
                    equationWithLabel.pack()

                    LogRLabel = Label(effectivenessLogR, text = "Alternative " + str(a+1) + " - " + policyAlt)
                    LogRTable=ttk.Treeview(effectivenessLogR)
                    LogRTable["columns"]=("1","2","3")
                    LogRTable['show']='headings'
                    LogRTable.column("1",width=130,anchor='c')
                    LogRTable.column("2",width=130,anchor='c')
                    LogRTable.column("3",width=130,anchor='c')
                    LogRTable.heading("1",text="Year")
                    LogRTable.heading("2",text="X")
                    LogRTable.heading("3",text="Y")

                    yearLabel = Label(effectivenessLogR, text = "Year")
                    inputXLabel = Label(effectivenessLogR, text = "X")

                    year = tk.Entry(effectivenessLogR, width=30)
                    inputX = tk.Entry(effectivenessLogR, width=30) 

                    addButton = tk.Button(effectivenessLogR, text='Add', width=10, command=lambda: add_data())  
                    editButton = tk.Button(effectivenessLogR, text="Edit", width=10, command=lambda: edit_data())

                    years = []

                    def show_data(a):
                        year.delete(0,END)
                        inputX.delete(0,END)

                        selectedItem = LogRTable.selection()[0]
                        year.insert(0, LogRTable.item(selectedItem)['values'][0])
                        inputX.insert(0, LogRTable.item(selectedItem)['values'][1])

                    LogRTable.bind("<<TreeviewSelect>>", show_data)    

                    am = 0
                    def edit_data():
                        yearText = year.get()                                   # get year

                        selected_item = LogRTable.selection()[0]

                        years.pop(LogRTable.index(selected_item))
                        years.insert(LogRTable.index(selected_item), int(yearText))

                        inputXText = float(inputX.get())                                                                            # get X
                        log_odds = float(inputX.get())*float(coefficientXLogR) + float(interceptLogR+coefficientConstLogR)          # compute for Y
                        odds = np.exp(log_odds)
                        outputYText = odds / (1 + odds)
                        
                        LogRTable.item(selected_item, text="blub", values=(yearText, inputXText, outputYText))

                    def add_data():
                        yearText = year.get()                                   # get year
                        
                        years.append(int(yearText))

                        inputXText = float(inputX.get())                                                                            # get X
                        log_odds = float(inputX.get())*float(coefficientXLogR) + float(interceptLogR+coefficientConstLogR)          # compute for Y
                        odds = np.exp(log_odds)
                        outputYText = odds / (1 + odds)

                        year.delete(0,END)
                        inputX.delete(0,END)

                        global assessmentTuple
                        assessmentTuple = [yearText, inputXText, outputYText]

                        # effortList.append(efforttuple)

                        LogRTable.insert("",'end', values=(yearText, inputXText, outputYText))
                        year.delete(0,END)                      # reset the text entry box
                        inputX.delete(0,END)                        # reset the text entry box
                        yearText.focus() 
                    
                    LogRLabel.pack()
                    LogRTable.pack()
                    yearLabel.place(x=210, y=360)
                    year.place(x=300, y=360)
                    inputXLabel.place(x=210, y=420)
                    inputX.place(x=300, y=420)
                    addButton.place(x=540, y=360)
                    editButton.place(x=540, y=420)

                a = 0

                while (a < len(p9alternatives)):
                    windowPerAlt(a, p9alternatives[a])
                    a += 1

            elif int(varEffec.get()) == 4: 
                effectiveness4 = Toplevel(main)
                effectiveness4.title("Effectiveness: FGD")
                effectiveness4.geometry("830x480")

            if int(varCostEff.get()) == 1: 
                popup = Toplevel(root)
                popup.geometry("200x200")
                popup.title("Enter Discount Rate")

                discountLabel = Label(popup, text = "Enter discount rate (1-100): ")
                discountEntry = Entry(popup, width=10)
                discountButton = tk.Button(popup, text='Set', width=10, command=lambda: enter_discount())

                def enter_discount():
                    global discount
                    discount = int(discountEntry.get())/100
                    print(discount)
                    popup.update()
                    popup.destroy()
                
                def windowPerAlt(a, policyAlt):
                    nu = 0
                    tangiblePerAlternative = Toplevel(main)
                    tangiblePerAlternative.title("Tangible BCA with Discounting: Alternative " + str(a+1) + " - " + policyAlt)
                    tangiblePerAlternative.geometry("810x600")

                    totalDiscBenefit = 0
                    totalDiscCost = 0

                    analysisFrame = tk.LabelFrame(tangiblePerAlternative)

                    yearlytangibleCBAwithLabel = Label(analysisFrame, text = "Alternative " + str(a+1) + " - " + policyAlt)
                    yearlytangibleCBAwithTable=ttk.Treeview(analysisFrame)
                    yearlytangibleCBAwithTable["columns"]=("1","2","3","4","5","6")
                    yearlytangibleCBAwithTable['show']='headings'
                    yearlytangibleCBAwithTable.column("1",width=130,anchor='c')
                    yearlytangibleCBAwithTable.column("2",width=130,anchor='c')
                    yearlytangibleCBAwithTable.column("3",width=130,anchor='c')
                    yearlytangibleCBAwithTable.column("4",width=130,anchor='c')
                    yearlytangibleCBAwithTable.column("5",width=130,anchor='c')
                    yearlytangibleCBAwithTable.column("6",width=130,anchor='c')
                    yearlytangibleCBAwithTable.heading("1",text="Year")
                    yearlytangibleCBAwithTable.heading("2",text="Benefit")
                    yearlytangibleCBAwithTable.heading("3",text="Cost")
                    yearlytangibleCBAwithTable.heading("4",text="df")
                    yearlytangibleCBAwithTable.heading("5",text="Discounted Benefit")
                    yearlytangibleCBAwithTable.heading("6",text="Discounted Cost")

                    yearLabel = Label(tangiblePerAlternative, text = "Year")
                    benefLabel = Label(tangiblePerAlternative, text = "Benefit")
                    costLabel = Label(tangiblePerAlternative, text = "Cost")
                    totalLabel = Label(tangiblePerAlternative, text = "Total: ")

                    year = tk.Entry(tangiblePerAlternative, width=30)
                    benefit = tk.Entry(tangiblePerAlternative, width=30) 
                    cost = tk.Entry(tangiblePerAlternative, width=30) 

                    addButton = tk.Button(tangiblePerAlternative, text='Add', width=10, command=lambda: add_data())  
                    editButton = tk.Button(tangiblePerAlternative, text="Edit", width=10, command=lambda: edit_data())
                    computeTotalButton = tk.Button(tangiblePerAlternative, text="Compute Total", width=50, command=lambda: compute_total())

                    years = []

                    def show_data(a):
                        year.delete(0,END)
                        benefit.delete(0,END)
                        cost.delete(0,END)

                        selectedItem = yearlytangibleCBAwithTable.selection()[0]
                        year.insert(0, yearlytangibleCBAwithTable.item(selectedItem)['values'][0])
                        benefit.insert(0, yearlytangibleCBAwithTable.item(selectedItem)['values'][1])
                        cost.insert(0, yearlytangibleCBAwithTable.item(selectedItem)['values'][2])

                    yearlytangibleCBAwithTable.bind("<<TreeviewSelect>>", show_data)    

                    am = 0
                    def edit_data():
                        nonlocal nu, totalDiscBenefit, totalDiscCost
                        yearText = year.get()                                   # get year


                        selected_item = yearlytangibleCBAwithTable.selection()[0]
                        
                        totalDiscBenefit -= round(float(yearlytangibleCBAwithTable.item(selected_item)['values'][4]), 2)
                        totalDiscCost -= round(float(yearlytangibleCBAwithTable.item(selected_item)['values'][5]), 2)

                        years.pop(yearlytangibleCBAwithTable.index(selected_item))
                        years.insert(yearlytangibleCBAwithTable.index(selected_item), int(yearText))

                        benefitText = float(benefit.get())                        # get benefit
                        costText = float(cost.get())                              # get cost
                        df = round(1/((1+discount)**(int(yearText) - int(years[0]))), 5)
                        discountedBenefit = round(float(benefitText)*df, 2)                 # compute for and set discountedBenefit 
                        discountedCost = round(float(costText)*df, 2)                       # compute for and set discountedCost

                        totalDiscBenefit += discountedBenefit
                        totalDiscCost += discountedCost
                        print(totalDiscBenefit, totalDiscCost)

                        yearlytangibleCBAwithTable.item(selected_item, text="blub", values=(yearText, benefitText, costText, df, discountedBenefit, discountedCost))

                    def add_data():
                        nonlocal nu, totalDiscBenefit, totalDiscCost
                        print(year.get())
                        print(benefit.get())
                        print(cost.get())

                        yearText = year.get()                                   # get year
                        benefitText = float(benefit.get())                        # get benefit
                        costText = float(cost.get())                              # get cost

                        years.append(int(yearText))

                        year.delete(0,END)
                        benefit.delete(0,END)
                        cost.delete(0,END)
                        df = round(1/((1+discount)**nu), 5)                               # set df to discount function
                        discountedBenefit = round(float(benefitText)*df, 2)                 # compute for and set discountedBenefit 
                        discountedCost = round(float(costText)*df, 2)                       # compute for and set discountedCost
                        nu += 1

                        totalDiscBenefit += discountedBenefit
                        totalDiscCost += discountedCost
                        print(totalDiscBenefit, totalDiscCost)

                        global assessmentTuple
                        assessmentTuple = [yearText, benefitText, costText, df, discountedBenefit, discountedCost]

                        # effortList.append(efforttuple)

                        yearlytangibleCBAwithTable.insert("",'end', values=(yearText, benefitText, costText, df, discountedBenefit, discountedCost))
                        yearText.delete('1.0',END)               # reset the text entry box
                        benefitText.delete('1.0',END)                   # reset the text entry box
                        costText.delete('1.0',END)                      # reset the text entry box
                        yearText.focus() 

                    def compute_total():
                        popupTotal = Toplevel(tangiblePerAlternative)
                        popupTotal.geometry("400x280")
                        popupTotal.title("Totals")

                        totDBLabel = Label(popupTotal, text = "Total Discounted Benefits:   ")
                        totDCLabel = Label(popupTotal, text = "Total Discounted Costs:    ")
                        BCRatioLabel = Label(popupTotal, text = "Benefit-Cost Ratio:   ")

                        BCRatio = round(float(totalDiscBenefit/totalDiscCost), 2)
                        
                        totDBLabel2 = Label(popupTotal, text = str(totalDiscBenefit))
                        totDCLabel2 = Label(popupTotal, text = str(totalDiscCost))
                        BCRatioLabel2 = Label(popupTotal, text = str(BCRatio))

                        totDBLabel.place(x=70, y=40)
                        totDCLabel.place(x=70, y=100)
                        BCRatioLabel.place(x=70, y=160)
                        totDBLabel2.place(x=260, y=40)
                        totDCLabel2.place(x=260, y=100)
                        BCRatioLabel2.place(x=260, y=160)
                    
                    analysisFrame.place(x=10, y=10)
                    yearlytangibleCBAwithLabel.grid(row=0, column=1)
                    yearlytangibleCBAwithTable.grid(row=1, column=1)
                    yearLabel.place(x=100, y=330)
                    year.place(x=260, y=330)
                    benefLabel.place(x=100, y=390)
                    benefit.place(x=260, y=390)
                    costLabel.place(x=100, y=450)
                    cost.place(x=260, y=450)
                    addButton.place(x=550, y=390)
                    editButton.place(x=550, y=450)
                    computeTotalButton.place(x=220, y=540)

                a = 0

                while (a < len(p9alternatives)):
                    windowPerAlt(a, p9alternatives[a])
                    a += 1

                discountLabel.place(x = 25, y = 10)
                discountEntry.place(x = 70, y = 50)
                discountButton.place(x = 63, y = 100)

            elif int(varCostEff.get()) == 2: 
                def windowPerAlt(a, policyAlt):
                    nu = 0
                    tangibleWithoutPerAlternative = Toplevel(main)
                    tangibleWithoutPerAlternative.title("Tangible BCA without Discounting: Alternative " + str(a+1) + " - " + policyAlt)
                    tangibleWithoutPerAlternative.geometry("620x600")
                    
                    analysisFrame = tk.LabelFrame(tangibleWithoutPerAlternative)

                    yearlytangibleCBAwithoutLabel = Label(analysisFrame, text = "Alternative " + str(a+1) + " - " + policyAlt)
                    yearlytangibleCBAwithoutTable=ttk.Treeview(analysisFrame)
                    yearlytangibleCBAwithoutTable["columns"]=("1","2","3")
                    yearlytangibleCBAwithoutTable['show']='headings'
                    yearlytangibleCBAwithoutTable.column("1",width=200,anchor='c')
                    yearlytangibleCBAwithoutTable.column("2",width=200,anchor='c')
                    yearlytangibleCBAwithoutTable.column("3",width=200,anchor='c')
                    yearlytangibleCBAwithoutTable.heading("1",text="Year")
                    yearlytangibleCBAwithoutTable.heading("2",text="Benefit")
                    yearlytangibleCBAwithoutTable.heading("3",text="Cost")

                    yearLabel = Label(tangibleWithoutPerAlternative, text = "Year")
                    benefLabel = Label(tangibleWithoutPerAlternative, text = "Benefit")
                    costLabel = Label(tangibleWithoutPerAlternative, text = "Cost")

                    year = tk.Entry(tangibleWithoutPerAlternative, width=30)
                    benefit = tk.Entry(tangibleWithoutPerAlternative, width=30) 
                    cost = tk.Entry(tangibleWithoutPerAlternative, width=30) 

                    addButton = tk.Button(tangibleWithoutPerAlternative, text='Add', width=10, command=lambda: add_data())  
                    editButton = tk.Button(tangibleWithoutPerAlternative, text="Edit", width=10, command=lambda: edit_data())

                    def show_data(a):
                        year.delete(0,END)
                        benefit.delete(0,END)
                        cost.delete(0,END)

                        selectedItem = yearlytangibleCBAwithoutTable.selection()[0]
                        year.insert(0, yearlytangibleCBAwithoutTable.item(selectedItem)['values'][0])
                        benefit.insert(0, yearlytangibleCBAwithoutTable.item(selectedItem)['values'][1])
                        cost.insert(0, yearlytangibleCBAwithoutTable.item(selectedItem)['values'][2])

                    yearlytangibleCBAwithoutTable.bind("<<TreeviewSelect>>", show_data)    

                    def edit_data():
                        yearText = year.get()                                   # get year
                        benefitText = int(benefit.get())                        # get benefit
                        costText = int(cost.get())                              # get cost

                        selected_item = yearlytangibleCBAwithoutTable.selection()[0]
                        yearlytangibleCBAwithoutTable.item(selected_item, text="blub", values=(yearText, benefitText, costText))

                    def add_data():
                        nonlocal nu

                        yearText = year.get()                                   # get year
                        benefitText = int(benefit.get())                        # get benefit
                        costText = int(cost.get())                              # get cost

                        year.delete(0,END)
                        benefit.delete(0,END)
                        cost.delete(0,END)
                        nu += 1
                        global assessmentTuple
                        assessmentTuple = [yearText, benefitText, costText]

                        # effortList.append(efforttuple)

                        yearlytangibleCBAwithoutTable.insert("",'end', values=(yearText, benefitText, costText))
                        yearText.delete('1.0',END)               # reset the text entry box
                        benefitText.delete('1.0',END)                   # reset the text entry box
                        costText.delete('1.0',END)                      # reset the text entry box
                        yearText.focus() 
                    
                    analysisFrame.place(x=10, y=10)
                    yearlytangibleCBAwithoutLabel.grid(row=0, column=1)
                    yearlytangibleCBAwithoutTable.grid(row=1, column=1)
                    yearLabel.place(x=40, y=330)
                    year.place(x=200, y=330)
                    benefLabel.place(x=40, y=390)
                    benefit.place(x=200, y=390)
                    costLabel.place(x=40, y=450)
                    cost.place(x=200, y=450)
                    addButton.place(x=450, y=390)
                    editButton.place(x=450, y=450)

                a = 0

                while (a < len(p9alternatives)):
                    windowPerAlt(a, p9alternatives[a])
                    a += 1

            elif int(varCostEff.get()) == 3:
                def windowPerAlt(a, policyAlt):
                    nu = 0
                    intangiblePerAlternative = Toplevel(main)
                    intangiblePerAlternative.title("Intangible BCA: Alternative " + str(a+1) + " - " + policyAlt)
                    intangiblePerAlternative.geometry("830x600")
                
                a = 0

                while (a < len(p9alternatives)):
                    windowPerAlt(a, p9alternatives[a])
                    a += 1

            if int(varAccept.get()) == 1:
                def windowPerAlt(a, policyAlt):
                    princeMethod = Toplevel(main)
                    princeMethod.title("PRINCE Method: Alternative " + str(a+1) + " - " + policyAlt)
                    princeMethod.geometry("670x600")

                    analysisFrame = tk.LabelFrame(princeMethod)

                    princeLabel = Label(analysisFrame, text = "PRINCE Method")
                    princeTable=ttk.Treeview(analysisFrame)
                    princeTable["columns"]=("1","2","3","4","5")
                    princeTable['show']='headings'
                    princeTable.column("1",width=130,anchor='c')
                    princeTable.column("2",width=130,anchor='c')
                    princeTable.column("3",width=130,anchor='c')
                    princeTable.column("4",width=130,anchor='c')
                    princeTable.column("5",width=130,anchor='c')
                    princeTable.heading("1",text="Player")
                    princeTable.heading("2",text="Issue Position")
                    princeTable.heading("3",text="Power")
                    princeTable.heading("4",text="Priority")
                    princeTable.heading("5",text="PRINCE Score")

                    playerLabel = Label(princeMethod, text = "Player")
                    issueposLabel = Label(princeMethod, text = "Issue\nPosition")
                    powerLabel = Label(princeMethod, text = "Power")
                    prioLabel = Label(princeMethod, text = "Priority")

                    player = tk.Entry(princeMethod, width=30)
                    issuepos = tk.Entry(princeMethod, width=30) 
                    power = tk.Entry(princeMethod, width=30) 
                    prio = tk.Entry(princeMethod, width=30) 

                    addButton = tk.Button(princeMethod, text='Add', width=10, command=lambda: add_data())  
                    editButton = tk.Button(princeMethod, text="Edit", width=10, command=lambda: edit_data())

                    def show_data(a):
                        player.delete(0,END)
                        issuepos.delete(0,END)
                        power.delete(0,END)
                        prio.delete(0,END)

                        selectedItem = princeTable.selection()[0]
                        player.insert(0, princeTable.item(selectedItem)['values'][0])
                        issuepos.insert(0, princeTable.item(selectedItem)['values'][1])
                        power.insert(0, princeTable.item(selectedItem)['values'][2])
                        prio.insert(0, princeTable.item(selectedItem)['values'][3])

                    princeTable.bind("<<TreeviewSelect>>", show_data)

                    def edit_data():
                        playerText = player.get()                               # read player textbox
                        issueposText = int(issuepos.get())                      # read issue position textbox
                        powerText = int(power.get())                            # read power textbox        
                        prioText = int(prio.get())                              # read priority textbox     

                        grades = [issueposText, powerText, prioText]
                        pc = 1
                        for g in grades:
                            if g != 0:
                                pc *= g       
                                                
                        selected_item = princeTable.selection()[0]
                        princeTable.item(selected_item, text="blub", values=(playerText, issueposText, powerText, prioText, pc))

                    def add_data():
                        playerText = player.get()                               # read player textbox
                        issueposText = int(issuepos.get())                      # read issue position textbox
                        powerText = int(power.get())                            # read power textbox        
                        prioText = int(prio.get())                              # read priority textbox 

                        grades = [issueposText, powerText, prioText]
                        pc = 1
                        for g in grades:
                            if g != 0:
                                pc *= g 

                        global assessmentTuple
                        assessmentTuple = [playerText, issueposText, powerText, prioText]

                        # effortList.append(efforttuple)

                        princeTable.insert("",'end', values=(playerText, issueposText, powerText, prioText, pc))
                        player.delete(0,END)
                        issuepos.delete(0,END)
                        power.delete(0,END)
                        prio.delete(0,END)
                        player.focus() 

                    analysisFrame.place(x=10, y=10)
                    princeLabel.grid(row=0, column=1)
                    princeTable.grid(row=1, column=1)
                    playerLabel.place(x=40, y=330)
                    player.place(x=200, y=330)
                    issueposLabel.place(x=40, y=390)
                    issuepos.place(x=200, y=390)
                    powerLabel.place(x=40, y=450)
                    power.place(x=200, y=450)
                    prioLabel.place(x=40, y=510)
                    prio.place(x=200, y=510)
                    addButton.place(x=450, y=390)
                    editButton.place(x=450, y=450)

                a = 0

                while (a < len(p9alternatives)):
                    windowPerAlt(a, p9alternatives[a])
                    a += 1    

            elif int(varAccept.get()) == 2:
                def windowPerAlt(a, policyAlt):
                    stakeholderWindow = Toplevel(main)
                    stakeholderWindow.title("Stakeholder Analysis: Alternative " + str(a+1) + " - " + policyAlt)
                    stakeholderWindow.geometry("790x600")

                    analysisFrame = tk.LabelFrame(stakeholderWindow)

                    stakeholderLabel = Label(analysisFrame, text = "Stakeholder Analysis")
                    stakeholderTable=ttk.Treeview(analysisFrame)
                    stakeholderTable["columns"]=("1","2","3","4")
                    stakeholderTable['show']='headings'
                    stakeholderTable.column("1",width=190,anchor='c')
                    stakeholderTable.column("2",width=190,anchor='c')
                    stakeholderTable.column("3",width=190,anchor='c')
                    stakeholderTable.column("4",width=190,anchor='c')
                    stakeholderTable.heading("1",text="Players (Stakeholder + Actor)")
                    stakeholderTable.heading("2",text="Positions/Stands")
                    stakeholderTable.heading("3",text="Motivations/Values/Beliefs")
                    stakeholderTable.heading("4",text="Sources of Power")

                    player_stakeactorLabel = Label(stakeholderWindow, text = "Player (Stakeholder + Actor)")
                    positionLabel = Label(stakeholderWindow, text = "Position/Stand")
                    motivationLabel = Label(stakeholderWindow, text = "Motivation/Value/Belief")
                    sourceLabel = Label(stakeholderWindow, text = "Source")

                    player_stakeactor = tk.Entry(stakeholderWindow, width=30)
                    position = tk.Entry(stakeholderWindow, width=30) 
                    motivation = tk.Entry(stakeholderWindow, width=30) 
                    source = tk.Entry(stakeholderWindow, width=30) 

                    addButton = tk.Button(stakeholderWindow, text='Add', width=10, command=lambda: add_data())  
                    editButton = tk.Button(stakeholderWindow, text="Edit", width=10, command=lambda: edit_data())

                    def show_data(a):
                        player_stakeactor.delete(0,END)
                        position.delete(0,END)
                        motivation.delete(0,END)
                        source.delete(0,END)

                        selectedItem = stakeholderTable.selection()[0]
                        player_stakeactor.insert(0, stakeholderTable.item(selectedItem)['values'][0])
                        position.insert(0, stakeholderTable.item(selectedItem)['values'][1])
                        motivation.insert(0, stakeholderTable.item(selectedItem)['values'][2])
                        source.insert(0, stakeholderTable.item(selectedItem)['values'][3])


                    stakeholderTable.bind("<<TreeviewSelect>>", show_data)

                    def edit_data():
                        player_stakeactorText = player_stakeactor.get()     # read player(s + a) textbox
                        positionText = position.get()                       # read position textbox
                        motivationText = motivation.get()                   # read motivation textbox        
                        sourceText = source.get()                           # read source textbox     
    
                        selected_item = stakeholderTable.selection()[0]
                        stakeholderTable.item(selected_item, text="blub", values=(player_stakeactorText, positionText, motivationText, sourceText))

                    def add_data():
                        player_stakeactorText = player_stakeactor.get()     # read player(s + a) textbox
                        positionText = position.get()                       # read position textbox
                        motivationText = motivation.get()                   # read motivation textbox        
                        sourceText = source.get()                           # read source textbox   

                        global assessmentTuple
                        assessmentTuple = [player_stakeactorText, positionText, motivationText, sourceText]

                        # effortList.append(efforttuple)

                        stakeholderTable.insert("",'end', values=(player_stakeactorText, positionText, motivationText, sourceText))
                        player_stakeactor.delete(0,END)
                        position.delete(0,END)
                        motivation.delete(0,END)
                        source.delete(0,END)
                        player_stakeactor.focus() 

                    analysisFrame.place(x=10, y=10)
                    stakeholderLabel.grid(row=0, column=1)
                    stakeholderTable.grid(row=1, column=1)
                    player_stakeactorLabel.place(x=40, y=330)
                    player_stakeactor.place(x=200, y=330)
                    positionLabel.place(x=40, y=390)
                    position.place(x=200, y=390)
                    motivationLabel.place(x=40, y=450)
                    motivation.place(x=200, y=450)
                    sourceLabel.place(x=40, y=510)
                    source.place(x=200, y=510)
                    addButton.place(x=450, y=390)
                    editButton.place(x=450, y=450)

                a = 0

                while (a < len(p9alternatives)):
                    windowPerAlt(a, p9alternatives[a])
                    a += 1    


        btnNext8 = Button(mainProject, text = "Next", width=10, command = lambda: next_8())
        btnNext8.place(x=550, y=440)         
        btnBack8 = Button(mainProject, text = "Back", width=10, command = lambda: back_8())
        btnBack8.place(x=265, y=440)      

    def page_10():
        style.configure('Treeview', rowheight=60)
        mainProject.geometry("1090x540")

        frame10 = tk.LabelFrame(mainProject)

        assessPALabel = Label(frame10, text = "Assessments of the Policy Alternatives: Spillovers, Externalities, and Constraints")
        assessPATable=ttk.Treeview(frame10, selectmode="browse", height=3)
        assessPATable["columns"]=("1","2","3","4","5")
        assessPATable['show']='headings'
        assessPATable.column("1",width=300,anchor='c')
        assessPATable.column("2",width=250,anchor='c')
        assessPATable.column("3",width=180,anchor='c')
        assessPATable.column("4",width=140,anchor='c')
        assessPATable.column("5",width=180,anchor='c')
        assessPATable.heading("1",text="Alternative")
        assessPATable.heading("2",text="Spillovers")
        assessPATable.heading("3",text="Externalities")
        assessPATable.heading("4",text="Constraints")
        assessPATable.heading("5",text="Mitigating Measures")

        for i in range(0, len(p9alternatives)):
            numb = str(i+1)+":"
            altText = ["Alt", numb, p9alternatives[i]]
            alter = " ".join(altText)
            assessPATable.insert("",'end', values=(alter.replace(" ", "\ ")))

        
        alternaLabel = Label(mainProject, text = "Alternative")
        spillovLabel = Label(mainProject, text = "Spillovers")
        externaLabel = Label(mainProject, text = "Externalities")
        constraLabel = Label(mainProject, text = "Constraints")
        mitmeasLabel = Label(mainProject, text = "Mitigating Measures")

        alternative = Entry(mainProject, width=150)
        spillover = scrolledtext.ScrolledText(mainProject, height = 4, width=25)
        externality = scrolledtext.ScrolledText(mainProject, height = 4, width=25)
        constraint = scrolledtext.ScrolledText(mainProject, height = 4, width=25)
        mitimeasure = scrolledtext.ScrolledText(mainProject, height = 4, width=25)

        addButton10 = tk.Button(mainProject, text='Add', width=10, command=lambda: add_data10())  
        editButton10 = tk.Button(mainProject, text="Edit", width=10, command=lambda: edit_data10())

        def show_data10(a):
            alternative.delete(0, END)
            spillover.delete("1.0", tk.END)
            externality.delete("1.0", tk.END)
            constraint.delete("1.0", tk.END)
            mitimeasure.delete("1.0", tk.END)

            selectedItem = assessPATable.selection()[0]
            
            alternative.insert(0, assessPATable.item(selectedItem)['values'][0])
            spillover.insert("1.0", assessPATable.item(selectedItem)['values'][1])
            externality.insert("1.0", assessPATable.item(selectedItem)['values'][2])
            constraint.insert("1.0", assessPATable.item(selectedItem)['values'][3])
            mitimeasure.insert("1.0", assessPATable.item(selectedItem)['values'][4])

        assessPATable.bind("<<TreeviewSelect>>", show_data10)

        def edit_data10():
            alternativeText = alternative.get()                                     # read alternative
            spilloverText = spillover.get("1.0", tk.END)                            # read spillover
            externalityText = externality.get("1.0", tk.END)                        # read externality 
            constraintText = constraint.get("1.0", tk.END)                          # read constraint         
            mitimeasureText = mitimeasure.get("1.0", tk.END)                        # read mitimeasure                  
                                    
            selected_item = assessPATable.selection()[0]
            assessPATable.item(selected_item, text="blub", values=(alternativeText, spilloverText, externalityText, constraintText, mitimeasureText))

        def add_data10():
            alternativeText = alternative.get()                                     # read alternative
            spilloverText = spillover.get("1.0", tk.END)                            # read spillover
            externalityText = externality.get("1.0", tk.END)                        # read externality 
            constraintText = constraint.get("1.0", tk.END)                          # read constraint         
            mitimeasureText = mitimeasure.get("1.0", tk.END)                        # read mitimeasure 

            # global assessmentTuple
            # assessmentTuple = [existingPolicyText, relevantProvisionText, accomplishment2Text, assessment2Text]

            # effortList.append(efforttuple)

            assessPATable.insert("",'end', values=(alternativeText, spilloverText, externalityText, constraintText, mitimeasureText))
            
            alternative.delete(0, END)                              # reset text entry boxes
            spillover.delete('1.0',tk.END)                          
            externality.delete('1.0',tk.END)                        
            constraint.delete('1.0',tk.END)                   
            mitimeasure.delete('1.0',tk.END)                  
            mitimeasure.focus() 

        frame10.place(x=10, y=10)
        assessPALabel.grid(row=2, column=1)
        assessPATable.grid(row=3, column=1)
        alternaLabel.place(x=540, y=250)
        alternative.place(x=100, y=270)
        spillovLabel.place(x=100, y=310)
        spillover.place(x=20, y=350)
        externaLabel.place(x=370, y=310)
        externality.place(x=290, y=350)
        constraLabel.place(x=640, y=310)
        constraint.place(x=560, y=350)
        mitmeasLabel.place(x=880, y=310)
        mitimeasure.place(x=830, y=350)
        addButton10.place(x=370, y=430)
        editButton10.place(x=620, y=430)

        def back_9():
            global pageNumber
            pageNumber -= 1
            print(pageNumber)
            frame10.destroy() 
            alternaLabel.destroy()
            alternative.destroy()
            spillovLabel.destroy()
            spillover.destroy()
            spillover.place_forget()
            externaLabel.destroy()
            externality.destroy()
            externality.place_forget()
            constraLabel.destroy()
            constraint.destroy()
            constraint.place_forget()
            mitmeasLabel.destroy()
            mitimeasure.destroy()
            mitimeasure.place_forget()
            btnBack9.destroy()
            btnNext9.destroy() 
            addButton10.destroy()
            editButton10.destroy()
            page_9()
        
        def next_9():
            frame10.destroy()            
            alternaLabel.destroy()
            alternative.destroy()
            spillovLabel.destroy()
            spillover.destroy()
            spillover.place_forget()
            externaLabel.destroy()
            externality.destroy()
            externality.place_forget()
            constraLabel.destroy()
            constraint.destroy()
            constraint.place_forget()
            mitmeasLabel.destroy()
            mitimeasure.destroy()
            mitimeasure.place_forget()
            btnBack9.destroy()
            btnNext9.destroy() 
            addButton10.destroy()
            editButton10.destroy()
            page_11()

        btnBack9 = Button(mainProject, text = "Back", width=10, command = lambda: back_9())
        btnNext9 = Button(mainProject, text = "Next", width=10, command = lambda: next_9())
        btnBack9.place(x=370, y=500)
        btnNext9.place(x=620, y=500)

    def page_11():
        mainProject.geometry("660x290")
        frame11 = tk.LabelFrame(mainProject)

        status.config(text="")
        status.place(x=10, y=210)
        
        p11Label = Label(mainProject, text = "Description of the Best/Optimal Policy Alternative")

        descrLabel = Label(frame11, text = "Description")
        descr = scrolledtext.ScrolledText(frame11, height = 8, width=30)
        
        reaSelLabel = Label(frame11, text = "Reasons for Selection")
        reaSel = scrolledtext.ScrolledText(frame11, height = 8, width=30)
        
        frame11.place(x=40, y=40)
        p11Label.place(x=170, y=10)
        descrLabel.grid(row=1, column=0, sticky = W, padx=7)
        descr.grid(row=2, column=0, sticky = W, padx=7)
        reaSelLabel.grid(row=1, column=1, sticky = W, padx=7)
        reaSel.grid(row=2, column=1, sticky = W, padx=7)
        
        def back_10():
            global pageNumber
            frame11.destroy() 
            p11Label.destroy() 
            btnBack10.destroy()
            btnNext10.destroy() 

            pageNumber -= 1
            print(pageNumber)
            page_10()
        
        def next_10():
            global pageNumber

            global p11BPAdescription, p11BPAreasonSelect
            p11BPAdescription = descr.get("1.0", tk.END)
            if not p11BPAdescription.strip():
                status.config(
                text="Enter description",
                foreground="red",
            )
                return
                    
            p11BPAreasonSelect = reaSel.get("1.0", tk.END)
            if not p11BPAreasonSelect.strip():
                status.config(
                text="Enter reason\nfor selection",
                foreground="red",
            )
                return
        
            # fileobject.writelines(problematicsituation+"\n"+undesirableeffects+"\n")
            save()

            frame11.destroy() 
            p11Label.destroy()
            btnBack10.destroy()
            btnNext10.destroy()

            pageNumber += 1
            print(pageNumber)
            page_12()

        btnBack10 = Button(mainProject, text = "Back", width=10, command = lambda: back_10())
        btnNext10 = Button(mainProject, text = "Next", width=10, command = lambda: next_10())
        btnBack10.place(x=140, y=210)
        btnNext10.place(x=400, y=210)

    def page_12():
        mainProject.geometry("660x500")
        frame12 = tk.LabelFrame(mainProject)

        status.config(text="")
        status.place(x=10, y=370)

        p12Label = Label(mainProject, text = "Description of the Best/Optimal Policy Alternative")

        spilloverLabel = Label(frame12, text = "Spillover")
        spillover = scrolledtext.ScrolledText(frame12, height = 8, width=30)
        
        externalityLabel = Label(frame12, text = "Externalities")
        externality = scrolledtext.ScrolledText(frame12, height = 8, width=30)

        constraintLabel = Label(frame12, text = "Constraints")
        constraint = scrolledtext.ScrolledText(frame12, height = 8, width=30)
        
        mitiMeasureLabel = Label(frame12, text = "Mitigating Measures")
        mitiMeasure = scrolledtext.ScrolledText(frame12, height = 8, width=30)
        
        frame12.place(x=40, y=40)
        p12Label.place(x=170, y=10)
        spilloverLabel.grid(row=1, column=0, sticky = W, padx=7)
        spillover.grid(row=2, column=0, sticky = W, padx=7)
        externalityLabel.grid(row=1, column=1, sticky = W, padx=7)
        externality.grid(row=2, column=1, sticky = W, padx=7)
        constraintLabel.grid(row=3, column=0, sticky = W, padx=7)
        constraint.grid(row=4, column=0, sticky = W, padx=7)
        mitiMeasureLabel.grid(row=3, column=1, sticky = W, padx=7)
        mitiMeasure.grid(row=4, column=1, sticky = W, padx=7)
        
        def back_11():
            global pageNumber
            frame12.destroy() 
            p12Label.destroy()
            btnBack11.destroy()
            btnNext11.destroy() 

            pageNumber -= 1
            print(pageNumber)
            page_11()
        
        def next_11():
            global pageNumber

            global p12BPAspillover, p12BPAexternality, p12BPAconstraint, p12BPAmitigatingmeasure
            p12BPAspillover = spillover.get("1.0", tk.END)
            if not p12BPAspillover.strip():
                status.config(
                text="Enter spillover",
                foreground="red",
            )
                return
                    
            p12BPAexternality = externality.get("1.0", tk.END)
            if not p12BPAexternality.strip():
                status.config(
                text="Enter externality",
                foreground="red",
            )
                return
            
            p12BPAconstraint = constraint.get("1.0", tk.END)
            if not p12BPAconstraint.strip():
                status.config(
                text="Enter constraint",
                foreground="red",
            )
                return
                    
            p12BPAmitigatingmeasure = mitiMeasure.get("1.0", tk.END)
            if not p12BPAmitigatingmeasure.strip():
                status.config(
                text="Enter mitigating\nmeasure",
                foreground="red",
            )
                return
        
            # fileobject.writelines(problematicsituation+"\n"+undesirableeffects+"\n")
            save()

            frame12.destroy() 
            p12Label.destroy()
            btnBack11.destroy()
            btnNext11.destroy() 
            
            pageNumber += 1
            print(pageNumber)
            page_13()

        btnBack11 = Button(mainProject, text = "Back", width=10, command = lambda: back_11())
        btnNext11 = Button(mainProject, text = "Next", width=10, command = lambda: next_11())
        btnBack11.place(x=140, y=370)
        btnNext11.place(x=400, y=370)


    def page_13():
        mainProject.geometry("660x500")
        frame13 = tk.LabelFrame(mainProject)

        status.config(text="")

        p13Label = Label(mainProject, text = "Requirements for the Implementation of the Best/Optimal Policy Alternative")

        p13whatLabel = Label(frame13, text = "What type of legislation is needed? Why?")
        p13what = scrolledtext.ScrolledText(frame13, height = 8, width=30)
        
        p13whoLabel = Label(frame13, text = "Who will implement? Why?")
        p13who = scrolledtext.ScrolledText(frame13, height = 8, width=30)

        p13howLabel = Label(frame13, text = "How much to implement and where to source funds?")
        p13how = scrolledtext.ScrolledText(frame13, height = 8, width=30)
        
        frame13.place(x=40, y=40)
        p13Label.place(x=150, y=10)
        p13whatLabel.grid(row=1, column=0, sticky = W, padx=7)
        p13what.grid(row=2, column=0, sticky = W, padx=7)
        p13whoLabel.grid(row=1, column=1, sticky = W, padx=7)
        p13who.grid(row=2, column=1, sticky = W, padx=7)
        p13howLabel.grid(row=3, column=0, sticky = W, padx=7)
        p13how.grid(row=4, column=0, sticky = W, padx=7)
        
        def back_12():
            global pageNumber
            frame13.destroy() 
            p13Label.destroy()
            btnBack12.destroy()
            btnNext12.destroy() 
            
            pageNumber -= 1
            print(pageNumber)
            page_12()
        
        def next_12():
            global pageNumber

            global p13BPAwhat, p13BPAwho, p13BPAhow
            p13BPAwhat = p13what.get("1.0", tk.END)
            if not p13BPAwhat.strip():
                status.config(
                text="Enter the type\nof legislation needed",
                foreground="red",
            )
                return
                    
            p13BPAwho = p13who.get("1.0", tk.END)
            if not p13BPAwho.strip():
                status.config(
                text="Enter who will\nimplement",
                foreground="red",
            )
                return
            
            p13BPAhow = p13how.get("1.0", tk.END)
            if not p13BPAhow.strip():
                status.config(
                text="Enter how much\nto implement",
                foreground="red",
            )
                return
    
            # fileobject.writelines(problematicsituation+"\n"+undesirableeffects+"\n")
            save()

            frame13.destroy() 
            p13Label.destroy()
            btnBack12.destroy()
            btnNext12.destroy() 
            
            pageNumber += 1
            print(pageNumber)
            page_14()

        btnBack12 = Button(mainProject, text = "Back", width=10, command = lambda: back_12())
        btnNext12 = Button(mainProject, text = "Next", width=10, command = lambda: next_12())
        btnBack12.place(x=140, y=370)
        btnNext12.place(x=400, y=370)

    def page_14():
        style.configure('Treeview', rowheight=60)
        mainProject.geometry("1090x530")

        frame14 = tk.LabelFrame(mainProject)

        implementationPlanLabel = Label(frame14, text = "Policy Implementation Plan")
        implementationPlanTable=ttk.Treeview(frame14, selectmode="browse", height=3)
        implementationPlanTable["columns"]=("1","2","3","4","5")
        implementationPlanTable['show']='headings'
        implementationPlanTable.column("1",width=300,anchor='c')
        implementationPlanTable.column("2",width=250,anchor='c')
        implementationPlanTable.column("3",width=180,anchor='c')
        implementationPlanTable.column("4",width=140,anchor='c')
        implementationPlanTable.column("5",width=180,anchor='c')
        implementationPlanTable.heading("1",text="Critical Actions")
        implementationPlanTable.heading("2",text="Responsible/Accountable Units")
        implementationPlanTable.heading("3",text="Timeframes")
        implementationPlanTable.heading("4",text="Budgets")
        implementationPlanTable.heading("5",text="Budget Sources")

        critALabel = Label(mainProject, text = "Critical Action")
        raUnitLabel = Label(mainProject, text = "Responsible/\nAccountable Unit")
        timeframeLabel = Label(mainProject, text = "Timeframe")
        budgetLabel = Label(mainProject, text = "Budget")
        budgSoLabel = Label(mainProject, text = "Budget Source")

        criticalAction = scrolledtext.ScrolledText(mainProject, height = 4, width=30)
        respaccoUnit = scrolledtext.ScrolledText(mainProject, height = 4, width=25)
        timeframe = scrolledtext.ScrolledText(mainProject, height = 4, width=18)
        budget = scrolledtext.ScrolledText(mainProject, height = 4, width=14)
        budgetSource = scrolledtext.ScrolledText(mainProject, height = 4, width=17)

        addButton14 = tk.Button(mainProject, text='Add', width=10, command=lambda: add_data14())  
        editButton14 = tk.Button(mainProject, text="Edit", width=10, command=lambda: edit_data14())

        def show_data14(a):
            criticalAction.delete("1.0", tk.END)
            respaccoUnit.delete("1.0", tk.END)
            timeframe.delete("1.0", tk.END)
            budget.delete("1.0", tk.END)
            budgetSource.delete("1.0", tk.END)

            selectedItem = implementationPlanTable.selection()[0]
            criticalAction.insert("1.0", implementationPlanTable.item(selectedItem)['values'][0])
            respaccoUnit.insert("1.0", implementationPlanTable.item(selectedItem)['values'][1])
            timeframe.insert("1.0", implementationPlanTable.item(selectedItem)['values'][2])
            budget.insert("1.0", implementationPlanTable.item(selectedItem)['values'][3])
            budgetSource.insert("1.0", implementationPlanTable.item(selectedItem)['values'][4])

        implementationPlanTable.bind("<<TreeviewSelect>>", show_data14)

        def edit_data14():
            criticalActionText = criticalAction.get("1.0", tk.END)                  # read existing policy
            respaccoUnitText = respaccoUnit.get("1.0", tk.END)                      # read relevant provision
            timeframeText = timeframe.get("1.0", tk.END)                            # read accomplishment 
            budgetText = budget.get("1.0", tk.END)                                  # read assessment          
            budgetSourceText = budgetSource.get("1.0", tk.END)                      # read assessment                  
                                    
            selected_item = implementationPlanTable.selection()[0]
            implementationPlanTable.item(selected_item, text="blub", values=(criticalActionText, respaccoUnitText, timeframeText, budgetText, budgetSourceText))

        def add_data14():
            criticalActionText = criticalAction.get("1.0", tk.END)                  # read existing policy
            respaccoUnitText = respaccoUnit.get("1.0", tk.END)                      # read relevant provision
            timeframeText = timeframe.get("1.0", tk.END)                            # read accomplishment 
            budgetText = budget.get("1.0", tk.END)                                  # read assessment          
            budgetSourceText = budgetSource.get("1.0", tk.END)                      # read assessment      

            # global assessmentTuple
            # assessmentTuple = [existingPolicyText, relevantProvisionText, accomplishment2Text, assessment2Text]

            # effortList.append(efforttuple)

            implementationPlanTable.insert("",'end', values=(criticalActionText, respaccoUnitText, timeframeText, budgetText, budgetSourceText))
            criticalAction.delete('1.0',tk.END)                    # reset the text entry box
            respaccoUnit.delete('1.0',tk.END)                 # reset the text entry box
            timeframe.delete('1.0',tk.END)                   # reset the text entry box
            budget.delete('1.0',tk.END)                       # reset the text entry box
            budgetSource.focus() 

        frame14.place(x=10, y=10)
        implementationPlanLabel.grid(row=2, column=1)
        implementationPlanTable.grid(row=3, column=1)
        critALabel.place(x=120, y=250)
        criticalAction.place(x=38, y=300)
        raUnitLabel.place(x=390, y=250)
        respaccoUnit.place(x=330, y=300)
        timeframeLabel.place(x=620, y=250)
        timeframe.place(x=570, y=300)
        budgetLabel.place(x=790, y=250)
        budget.place(x=750, y=300)
        budgSoLabel.place(x=925, y=250)
        budgetSource.place(x=900, y=300)
        addButton14.place(x=370, y=400)
        editButton14.place(x=620, y=400)

        def back_13():
            global pageNumber
            frame14.destroy() 
            critALabel.destroy()
            criticalAction.destroy()
            criticalAction.place_forget()
            raUnitLabel.destroy()
            respaccoUnit.destroy()
            respaccoUnit.place_forget()
            timeframeLabel.destroy()
            timeframe.destroy()
            timeframe.place_forget()
            budgetLabel.destroy()
            budget.destroy()
            budget.place_forget()
            budgSoLabel.destroy()
            budgetSource.destroy()
            budgetSource.place_forget()
            btnBack13.destroy()
            btnNext13.destroy() 
            addButton14.destroy()
            editButton14.destroy()

            pageNumber -= 1
            print(pageNumber)
            page_13()
        
        def next_13():
            global pageNumber
            frame14.destroy() 
            critALabel.destroy()
            criticalAction.destroy()
            criticalAction.place_forget()
            raUnitLabel.destroy()
            respaccoUnit.destroy()
            respaccoUnit.place_forget()
            timeframeLabel.destroy()
            timeframe.destroy()
            timeframe.place_forget()
            budgetLabel.destroy()
            budget.destroy()
            budget.place_forget()
            budgSoLabel.destroy()
            budgetSource.destroy()
            budgetSource.place_forget()
            btnBack13.destroy()
            btnNext13.destroy() 
            addButton14.destroy()
            editButton14.destroy()

            pageNumber += 1
            print(pageNumber)
            page_15()

        btnBack13 = Button(mainProject, text = "Back", width=10, command = lambda: back_13())
        btnNext13 = Button(mainProject, text = "Next", width=10, command = lambda: next_13())
        btnBack13.place(x=370, y=460)
        btnNext13.place(x=620, y=460)

    def page_15():
        style.configure('Treeview', rowheight=120)
        mainProject.state('zoomed')

        frame15 = tk.LabelFrame(mainProject)

        policyAssessmentLabel = Label(frame15, text = "Policy Assessment: Monitoring and Evaluation Plan")
        policyAssessmentTable=ttk.Treeview(frame15, selectmode="browse", height=3)
        policyAssessmentTable["columns"]=("1","2","3","4","5","6","7")
        policyAssessmentTable['show']='headings'
        policyAssessmentTable.column("1",width=214,anchor='c')
        policyAssessmentTable.column("2",width=214,anchor='c')
        policyAssessmentTable.column("3",width=214,anchor='c')
        policyAssessmentTable.column("4",width=214,anchor='c')
        policyAssessmentTable.column("5",width=214,anchor='c')
        policyAssessmentTable.column("6",width=214,anchor='c')
        policyAssessmentTable.column("7",width=214,anchor='c')
        policyAssessmentTable.heading("1",text="Goals and Objectives")
        policyAssessmentTable.heading("2",text="SMART Indicators")
        policyAssessmentTable.heading("3",text="Sources of Data")
        policyAssessmentTable.heading("4",text="Data Collection Frequencies")
        policyAssessmentTable.heading("5",text="Unit-In-Charge of Data\nCollection and Analysis")
        policyAssessmentTable.heading("6",text="Outputs of M&E")
        policyAssessmentTable.heading("7",text="M&E Report Users")

        for i in range(0, len(p7policyGoalsandObjectives)):
            policyAssessmentTable.insert("",'end', values=(p7policyGoalsandObjectives[i], p7indicators[i]))

        goalAndObjectiveLabel = Label(mainProject, text = "Goal and Objective")
        smartIndicatorLabel = Label(mainProject, text = "SMART Indicator")
        sourceofDataLabel = Label(mainProject, text = "Source of Data")
        dcfLabel = Label(mainProject, text = "Data Collection Frequency")
        uicLabel = Label(mainProject, text = "Unit-In-Charge of Data\nCollection and Analysis")
        MEoutputLabel = Label(mainProject, text = "Output of M&E")
        MEuserLabel = Label(mainProject, text = "M&E Report User")

        goalAndObjective = scrolledtext.ScrolledText(mainProject, height = 4, width=22)
        smartIndicator = scrolledtext.ScrolledText(mainProject, height = 4, width=22)
        sourceofData = scrolledtext.ScrolledText(mainProject, height = 4, width=22)
        dcf = scrolledtext.ScrolledText(mainProject, height = 4, width=22)
        uic = scrolledtext.ScrolledText(mainProject, height = 4, width=22)
        MEoutput = scrolledtext.ScrolledText(mainProject, height = 4, width=22)
        MEuser = scrolledtext.ScrolledText(mainProject, height = 4, width=22)

        addButton15 = tk.Button(mainProject, text='Add', width=10, command=lambda: add_data15())  
        editButton15 = tk.Button(mainProject, text="Edit", width=10, command=lambda: edit_data15())

        def show_data15(a):
            goalAndObjective.delete("1.0", tk.END)
            smartIndicator.delete("1.0", tk.END)
            sourceofData.delete("1.0", tk.END)
            dcf.delete("1.0", tk.END)
            uic.delete("1.0", tk.END)
            MEoutput.delete("1.0", tk.END)
            MEuser.delete("1.0", tk.END)

            selectedItem = policyAssessmentTable.selection()[0]
            goalAndObjective.insert("1.0", policyAssessmentTable.item(selectedItem)['values'][0])
            smartIndicator.insert("1.0", policyAssessmentTable.item(selectedItem)['values'][1])
            sourceofData.insert("1.0", policyAssessmentTable.item(selectedItem)['values'][2])
            dcf.insert("1.0", policyAssessmentTable.item(selectedItem)['values'][3])
            uic.insert("1.0", policyAssessmentTable.item(selectedItem)['values'][4])
            MEoutput.insert("1.0", policyAssessmentTable.item(selectedItem)['values'][5])
            MEuser.insert("1.0", policyAssessmentTable.item(selectedItem)['values'][6])

        policyAssessmentTable.bind("<<TreeviewSelect>>", show_data15)

        def edit_data15():
            goalAndObjectiveText = goalAndObjective.get("1.0", tk.END)                          # read existing policy
            smartIndicatorText = smartIndicator.get("1.0", tk.END)                              # read relevant provision
            sourceofDataText = sourceofData.get("1.0", tk.END)                                  # read accomplishment 
            dcfText = dcf.get("1.0", tk.END)                                                    # read assessment          
            uicText = uic.get("1.0", tk.END)                                                    # read assessment      
            MEoutputText = MEoutput.get("1.0", tk.END)                                          # read assessment          
            MEuserText = MEuser.get("1.0", tk.END)                                              # read assessment                     
                                    
            selected_item = policyAssessmentTable.selection()[0]
            policyAssessmentTable.item(selected_item, text="blub", values=(goalAndObjectiveText, smartIndicatorText, sourceofDataText, dcfText, uicText, MEoutputText, MEuserText))

        def add_data15():
            goalAndObjectiveText = goalAndObjective.get("1.0", tk.END)                          # read existing policy
            smartIndicatorText = smartIndicator.get("1.0", tk.END)                              # read relevant provision
            sourceofDataText = sourceofData.get("1.0", tk.END)                                  # read accomplishment 
            dcfText = dcf.get("1.0", tk.END)                                                    # read assessment          
            uicText = uic.get("1.0", tk.END)                                                    # read assessment      
            MEoutputText = MEoutput.get("1.0", tk.END)                                          # read assessment          
            MEuserText = MEuser.get("1.0", tk.END)                                              # read assessment       

            # global assessmentTuple
            # assessmentTuple = [existingPolicyText, relevantProvisionText, accomplishment2Text, assessment2Text]

            # effortList.append(efforttuple)
            policyAssessmentTable.insert("",'end', values=(goalAndObjectiveText, smartIndicatorText, sourceofDataText, dcfText, uicText, MEoutputText, MEuserText))
            goalAndObjective.delete("1.0", tk.END)
            smartIndicator.delete("1.0", tk.END)
            sourceofData.delete("1.0", tk.END)
            dcf.delete("1.0", tk.END)
            uic.delete("1.0", tk.END)
            MEoutput.delete("1.0", tk.END)
            MEuser.delete("1.0", tk.END)

        frame15.place(x=10, y=10)
        policyAssessmentLabel.grid(row=2, column=1)
        policyAssessmentTable.grid(row=3, column=1)
        goalAndObjectiveLabel.place(x=70, y=450)
        goalAndObjective.place(x=20, y=490)
        smartIndicatorLabel.place(x=290, y=450)
        smartIndicator.place(x=237, y=490)
        sourceofDataLabel.place(x=510, y=450)
        sourceofData.place(x=453, y=490)
        dcfLabel.place(x=700, y=450)
        dcf.place(x=670, y=490)
        uicLabel.place(x=925, y=440)
        uic.place(x=886, y=490)
        MEoutputLabel.place(x=1160, y=450)
        MEoutput.place(x=1103, y=490)
        MEuserLabel.place(x=1350, y=450)
        MEuser.place(x=1320, y=490)
        addButton15.place(x=590, y=580)
        editButton15.place(x=840, y=580)

        def back_14():
            global pageNumber
            mainProject.state("normal")
            frame15.destroy() 
            goalAndObjectiveLabel.destroy()
            goalAndObjective.destroy()
            goalAndObjective.place_forget()
            smartIndicatorLabel.destroy()
            smartIndicator.destroy()
            smartIndicator.place_forget()
            sourceofDataLabel.destroy()
            sourceofData.destroy()
            sourceofData.place_forget()
            dcfLabel.destroy()
            dcf.destroy()
            dcf.place_forget()
            uicLabel.destroy()
            uic.destroy()
            uic.place_forget()
            MEoutputLabel.destroy()
            MEoutput.destroy()
            MEoutput.place_forget()
            MEuserLabel.destroy()
            MEuser.destroy()
            MEuser.place_forget()
            btnBack14.destroy()
            btnNext14.destroy() 
            addButton15.destroy()
            editButton15.destroy()

            pageNumber -= 1
            print(pageNumber)
            page_14()
        
        def next_14():
            # global pageNumber
            # pageNumber += 1
            # print(pageNumber)
            mainProject.state("normal")
            frame15.destroy() 
            goalAndObjectiveLabel.destroy()
            goalAndObjective.destroy()
            goalAndObjective.place_forget()
            smartIndicatorLabel.destroy()
            smartIndicator.destroy()
            smartIndicator.place_forget()
            sourceofDataLabel.destroy()
            sourceofData.destroy()
            sourceofData.place_forget()
            dcfLabel.destroy()
            dcf.destroy()
            dcf.place_forget()
            uicLabel.destroy()
            uic.destroy()
            uic.place_forget()
            MEoutputLabel.destroy()
            MEoutput.destroy()
            MEoutput.place_forget()
            MEuserLabel.destroy()
            MEuser.destroy()
            MEuser.place_forget()
            btnBack14.destroy()
            btnNext14.destroy() 
            addButton15.destroy()
            editButton15.destroy()

        btnBack14 = Button(mainProject, text = "Back", width=10, command = lambda: back_14())
        btnNext14 = Button(mainProject, text = "Next", width=10, command = lambda: next_14())
        btnBack14.place(x=590, y=640)
        btnNext14.place(x=840, y=640)

    # projectTitle.config(bg="white")
    # fontSize.config(bg="white")
    # polAnaTitle.config(bg="white")
    # probSit.config(bg="white")
    # undeEff.config(bg="white")

    # n = varNat.get()
    # l = varLoc.get()
    # o = varOrg.get()

    # quan = varRoot1.get()
    # regLi = varRoot2.get()
    # regMu = varRoot3.get()
    # regLo = varRoot4.get()
    # qual = varRoot5.get()
    # prob = varRoot6.get()
    # delp = varRoot7.get()

    # data = [projecttitle, policyanalysis, fontstyle, fontsize, n, l, o]

    # filename = projecttitle
    # fileobject = open(filename + '.pol', 'w')
    # json.dump(data, fileobject)
    # fileobject.close()

def helpPage():
    helpWindow = Toplevel(root)
    helpWindow.title("Help")
    helpWindow.geometry("600x300")

    # Create Canvas and Scrollbar
    canvas = tk.Canvas(helpWindow, borderwidth=0, background="#ffffff")
    scrollbar = tk.Scrollbar(helpWindow, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, background="#ffffff")

    # Configure scrolling
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Pack canvas and scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Your labels go in the scrollable_frame
    aboutLabel = Label(scrollable_frame, foreground="#76090c", background="#ffffff",
                       font=("Franklin Gothic Heavy", 12), wraplength=500, justify="left", text="About")
    
    descLabel = Label(scrollable_frame, foreground="#000000", background="#ffffff",
                      font=("Franklin", 10), wraplength=500, justify="left",
                      text="The Policy Analytics 1.0 application is a step-by-step desktop tool designed to help students, policy analysts, and public administration professionals perform comprehensive policy analysis and development. It is based on William N. Dunn’s policy paper structure, with enhancements by Dr. Ebinezer R. Florano. The application guides users through a structured process to: Define a policy problem, analyze current government efforts, perform statistical or qualitative analysis, evaluate policy alternatives, and design a policy implementation and monitoring plan. The final output is a detailed draft suited for a Policy Issue Paper.")

    guideLabel = Label(scrollable_frame, foreground="#76090c", background="#ffffff",
                       font=("Franklin Gothic Heavy", 12), wraplength=500, justify="left", text="Step-by-Step Guide")

    stepsLabel = Label(scrollable_frame, foreground="#000000", background="#ffffff",
                        font=("Franklin", 10), wraplength=500, justify="left",
                        text=
                        "Upon creating a new project, you will be guided through the following steps:\n\n"
                        "Page 1: Project Setup\n"
                        "  •  Enter project title, analyst name, font style and size, etc.\n"
                        "  •  Choose level(s) of policy analysis (National, Local, Organizational)\n\n"
                        "Page 2: Problematic Situation\n"
                        "  •  Describe the problematic situation and its undesirable effects\n\n"
                        "Page 3: Current Government Efforts\n"
                        "  •  Describe current government efforts, accomplishments, and assessments\n\n"
                        "Page 4: Statistical or Qualitative Analysis\n"
                        "  •  Choose a method for analysis: Linear/Multiple/Logistic Regression or Problem Tree\n"
                        "  •  If a statistical analysis method is chosen, upload a CSV file. The program will output plots and regression results based on the analysis in separate windows.\n"
                        "  •  If Problem Tree is chosen, a window will appear \n\n"
                        
                        )
        

    # Pack labels into the scrollable frame
    aboutLabel.pack(pady=5, padx=10, anchor="w") 
    descLabel.pack(pady=5, padx=10, anchor="w")
    guideLabel.pack(pady=5, padx=10, anchor="w") 
    stepsLabel.pack(pady=5, padx=10, anchor="w")

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    canvas.bind_all("<MouseWheel>", _on_mousewheel)  # For Windows

def save():
    global pageNumber, save_file_path
    
    if save_file_path is None:
        save_file_path = asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=p1projecttitle + ".pdf",
            title="Save PDF As"
        )
    if not save_file_path:
        return  # User canceled save


    pdf = FPDF()   

    pdf.add_page()
    
    pdf.set_font(family="Arial", style='B', size=int(p1fontsize))
    
    pdf.cell(0, 8, txt = p1projecttitle, ln = 2, border = 0, align = 'C', fill = FALSE)
    pdf.set_font(family="Arial", style='I', size=int(p1fontsize))
    pdf.cell(0, 8, txt = p1analysts, ln = 2, border = 0, align = 'C', fill = FALSE)
    pdf.cell(0, 8, txt = p1policyanalysis, ln = 2, border = 0, align = 'C', fill = FALSE)
    pdf.set_font(family="Arial", style='I', size=int(p1fontsize))
    pdf.cell(0, 8, txt = "\nProblematic Situation: ", ln = 2, border = 0, align = 'J', fill = FALSE)
    pdf.set_font(family="Arial", style='', size=int(p1fontsize))
    pdf.multi_cell(0, 10, txt = p2problematicsituation, border = 0, align = 'J', fill = FALSE)
    pdf.set_font(family="Arial", style='I', size=int(p1fontsize))
    pdf.cell(0, 8, txt = "\nUndesirable Effects: ", ln = 2, border = 0, align = 'J', fill = FALSE)
    pdf.set_font(family="Arial", style='', size=int(p1fontsize))
    pdf.multi_cell(0, 10, txt = p2undesirableeffects, border = 0, align = 'J', fill = FALSE)
    pdf.set_font(family="Arial", style='I', size=int(p1fontsize))
    pdf.cell(0, 8, txt = "\nRoot Cause: ", ln = 2, border = 0, align = 'J', fill = FALSE)
    pdf.set_font(family="Arial", style='', size=int(p1fontsize))
    pdf.multi_cell(0, 10, txt = p5rootcause, border = 0, align = 'J', fill = FALSE)
    pdf.set_font(family="Arial", style='I', size=int(p1fontsize))
    pdf.cell(0, 8, txt = "\nPolicy Problem: ", ln = 2, border = 0, align = 'J', fill = FALSE)
    pdf.set_font(family="Arial", style='', size=int(p1fontsize))
    pdf.multi_cell(0, 10, txt = p6policyproblem, border = 0, align = 'J', fill = FALSE)
    pdf.set_font(family="Arial", style='I', size=int(p1fontsize))
    pdf.cell(0, 8, txt = "\nPolicy Issue Statement: ", ln = 2, border = 0, align = 'J', fill = FALSE)
    pdf.set_font(family="Arial", style='', size=int(p1fontsize))
    pdf.multi_cell(0, 10, txt = p6policyissue, border = 0, align = 'J', fill = FALSE)
  
    pdf.add_page()

    if int(pageNumber) == 5:
        pdf.multi_cell(0, 10, txt ="Regression Analysis\n", border = 0, align = 'C', fill = FALSE)
        pdf.multi_cell(0, 10, txt = p4summaryPDF, border = 0, align = 'C', fill = FALSE)
        pdf.image('regplot.png', x=20, y=100, w=160)

    # save the pdf with name .pdf
    
    pdf.output(save_file_path, 'F')

def print_file():

    pdffilename = p1projecttitle+".pdf"
    print(pdffilename)

    # Open input PDF file
    os.startfile(pdffilename, 'Print')

def quit():
    
    global pageNumber
    pageNumber = 0
    print(pageNumber)
    sys.exit()

menubar = Menu(root) 

file1 = Menu(menubar, tearoff = 0) 
menubar.add_cascade(label ='File', menu = file1) 
file1.add_command(label ='Create New', command = lambda: createNewProject())
file1.add_command(label ='Save', command = lambda: save()) 
file1.add_command(label ='Print', command = lambda: print_file()) 
file1.add_separator() 
file1.add_command(label ='Exit', command = lambda: quit())
file1.add_command(label ='Help', command = lambda: helpPage())

root.config(menu=menubar)

root.mainloop()