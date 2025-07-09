import tkinter as tk
from tkinter import *
from tkinter import font
from tkinter import ttk, messagebox, colorchooser
from tkinter import scrolledtext 
from tkinter import colorchooser
from tkinter.filedialog import askopenfilename

import textwrap
import json

import PIL
from PIL import Image, ImageTk, ImageDraw

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

# Hamdi addition
import tkinter.tix as tix

global size, var, pageNumber
size = 10
save_pdf_file_path = None
save_json_file_path = None

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

# Menu setup
# def setup_menu():
#     menubar = tk.Menu(main)
#     file_menu = tk.Menu(menubar, tearoff=0)
#     file_menu.add_command(label="New", command=lambda: new_project())
#     file_menu.add_command(label="Open", command=lambda: open_project())
#     file_menu.add_command(label="Help", command=lambda: help_page())
#     menubar.add_cascade(label="File", menu=file_menu)
#     main.config(menu=menubar)

# Nasa baba yung menu set-up - Bmae

def new_project():
    global pageNumber
    pageNumber = 1
    for widget in mainProject.winfo_children():
        widget.destroy()
    page_1()  # Assumed defined elsewhere

def open_project():

    global p1projecttitle, p1analysts, p1fontstyle, p1policyanalysis, p1fontsize
    global p2problematicsituation, p2undesirableeffects
    global p3efforts, p3accomplishments, p3assessments
    global p5rootcause, p5assessments
    global p6policyproblem, p6policyissue
    global p7policyGoalsandObjectives, p7indicators
    global p8stakeholders, p8actors
    global p9altnum, p9alternatives
    global p10spillovers, p10externalities, p10constraints, p10mitimeasures
    global p11BPAdescription, p11BPAreasonSelect
    global p12BPAspillover, p12BPAexternality, p12BPAconstraint, p12BPAmitigatingmeasure

    
    filename = tk.filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
    if filename:
        with open(filename, "r") as f:
            data = json.load(f)

        p1projecttitle = data.get("p1projecttitle", "")
        p1analysts = data.get("p1analysts", "")
        p1fontstyle = data.get("p1fontstyle", "")
        p1fontsize = data.get("p1fontsize", 12)
        p1policyanalysis = data.get("p1policyanalysis", "")
        p2problematicsituation = data.get("p2problematicsituation", "")
        p2undesirableeffects = data.get("p2undesirableeffects", "")
        p3efforts = data.get("p3efforts", [])
        p3accomplishments = data.get("p3accomplishments", [])
        p3assessments = data.get("p3assessments", [])
        p5rootcause = data.get("p5rootcause", "")
        p5assessments = data.get("p5assessments", ["", "", "", ""])
        p6policyproblem = data.get("p6policyproblem", "")
        p6policyissue = data.get("p6policyissue", "")
        p7policyGoalsandObjectives = data.get("p7policyGoalsandObjectives", [])
        p7indicators = data.get("p7indicators", [])
        p8stakeholders = data.get("p8stakeholders", [])
        p8actors = data.get("p8actors", [])
        p9altnum = data.get("p9altnum", [])
        p9alternatives = data.get("p9alternatives", [])
        p10spillovers = data.get("p10spillovers", "")
        p10externalities = data.get("p10externalities", "")
        p10constraints = data.get("p10constraints", "")
        p10mitimeasures = data.get("p10mitimeasures", "")
        p11BPAdescription = data.get("p11BPAdescription", "")
        p11BPAreasonSelect = data.get("p11BPAreasonSelect", "")
        p12BPAspillover = data.get("p12BPAspillover", "")
        p12BPAexternality = data.get("p12BPAexternality", "")
        p12BPAconstraint = data.get("p12BPAconstraint", "")
        p12BPAmitigatingmeasure = data.get("p12BPAmitigatingmeasure", "")

        createNewProject()

def help_page():
    help_window = tk.Toplevel(main)
    help_window.title("Help - Policy Analytics")
    help_window.geometry("800x600")
    help_text = scrolledtext.ScrolledText(help_window, height=30, width=80, wrap=tk.WORD)
    help_text.pack(padx=10, pady=10, fill="both", expand=True)
    help_content = """
    Policy Analytics Application Help
    ===============================
    This application guides you through a 15-page policy analysis process.

    Navigation:
    - Use 'Back' and 'Next' buttons to move between pages.
    - Progress is shown via a progress bar and workflow map at the top of each page.
    - Click workflow map rectangles to jump to specific pages.

    Features:
    - Add/Edit/Delete data in tables using buttons (Ctrl+Enter to add, Ctrl+Z to undo).
    - Zoom in/out using buttons for better visibility.
    - Use scrollbars for large tables.
    - Save data automatically when navigating with 'Next'.

    Page Descriptions:
    - Page 4: Select statistical methods (Linear/Multiple/Logistic Regression, Problem Tree Analysis).
    - Page 5: Enter root cause and assess existing policies.
    - Page 6: Define policy problem and issue statement.
    - Page 7: List policy goals and objectives with indicators.
    - Page 8: Identify stakeholders and actors.
    - Page 9: Assess policy alternatives with effectiveness, cost-efficiency, and acceptability.
    - Page 10: Evaluate spillovers, externalities, and constraints.
    - Page 11: Describe the best policy alternative and reasons for selection.
    - Page 12: Detail spillovers, externalities, constraints, and mitigating measures for the best alternative.
    - Page 13: Specify legislation, implementers, and funding for the best alternative.
    - Page 14: Create a policy implementation plan.
    - Page 15: Develop a monitoring and evaluation plan.

    Shortcuts:
    - Ctrl+Z: Undo last action (where applicable).
    - Ctrl+Enter: Add data to tables.
    - Tab: Cycle through input fields.
    """
    help_text.insert(tk.INSERT, help_content)
    help_text.config(state="disabled")

def wrap(string, length=40):
    return '\n'.join(textwrap.wrap(string, length))

def createNewProject():
    global pageNumber
    pageNumber = 0

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
    
    ##global p1projecttitle, p1analysts, p1fontstyle, p1policyanalysis, p1fontstyle, p1fontsize
    ##p1projecttitle = " "
    ##p1analysts = " "
    ##p1fontstyle = " "
    ##p1policyanalysis = " "
    ##p1fontstyle = " "
    ##p1fontsize = 12

    color = ("", "#000000")  # Default color for ShapeEditorApp
    interceptLR, coefficientLR = 0, 0
    interceptMR1, coefficientMR1 = 0, 0
    interceptMR2, coefficientMR2 = 0, 0
    interceptLogR, coefficientConstLogR, coefficientXLogR = 0, 0, 0
    discount = 0.05  # Default discount rate

    global p4summaryPDF
    p4summaryPDF = " "
    
    # Tooltip class
    class ToolTip:
        def __init__(self, widget, text):
            self.widget = widget
            self.text = text
            self.tip_window = None
            self.widget.bind("<Enter>", self.show_tip)
            self.widget.bind("<Leave>", self.hide_tip)

        def show_tip(self, event=None):
            if self.tip_window or not self.text:
                return
            x, y, _, _ = self.widget.bbox("insert")
            x += self.widget.winfo_rootx() + 25
            y += self.widget.winfo_rooty() + 25
            self.tip_window = tw = tk.Toplevel(self.widget)
            tw.wm_overrideredirect(True)
            tw.wm_geometry(f"+{x}+{y}")
            label = tk.Label(tw, text=self.text, justify="left", background="#ffffe0", relief="solid", borderwidth=1)
            label.pack()

        def hide_tip(self, event=None):
            if self.tip_window:
                self.tip_window.destroy()
                self.tip_window = None

    def setup_page_common(page_num, title, frame, widgets_to_destroy, back_func, next_func):
        mainProject.state('zoomed')
        style.configure('Treeview', rowheight=120)
        style.configure("TButton", foreground="black", font=("Arial", 10))

        # Canvas with scrollbars
        canvas = tk.Canvas(mainProject)
        scrollbar_y = ttk.Scrollbar(mainProject, orient="vertical", command=canvas.yview)
        scrollbar_x = ttk.Scrollbar(mainProject, orient="horizontal", command=canvas.xview)
        canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((0, 0), window=frame, anchor="nw")
        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Zoom functionality
        scale = 1.0
        def zoom_in():
            nonlocal scale
            scale *= 1.1
            canvas.scale("all", 0, 0, 1.1, 1.1)
            canvas.configure(scrollregion=canvas.bbox("all"))
        def zoom_out():
            nonlocal scale
            scale /= 1.1
            canvas.scale("all", 0, 0, 1/1.1, 1/1.1)
            canvas.configure(scrollregion=canvas.bbox("all"))
        zoom_in_button = ttk.Button(mainProject, text="Zoom In", command=zoom_in)
        zoom_out_button = ttk.Button(mainProject, text="Zoom Out", command=zoom_out)
        zoom_in_button.place(relx=0.01, rely=0.01)
        zoom_out_button.place(relx=0.08, rely=0.01)

        # Progress bar and workflow map
        progress = ttk.Progressbar(mainProject, length=200, maximum=15, value=page_num)
        progress.place(relx=0.01, rely=0.05)
        progress_label = tk.Label(mainProject, text=f"Page {page_num} of 15: {title}", font=("Arial", 12, "bold"))
        progress_label.place(relx=0.01, rely=0.08)
        workflow_canvas = tk.Canvas(mainProject, height=50, width=750)
        workflow_canvas.place(relx=0.01, rely=0.12)
        for i in range(1, 16):
            x = (i-1)*50
            workflow_canvas.create_rectangle(x, 10, x+40, 40, fill="lightblue" if i == page_num else "gray")
            workflow_canvas.create_text(x+20, 25, text=str(i))
            workflow_canvas.tag_bind(i, "<Button-1>", lambda e, p=i: jump_to_page(p))

        def jump_to_page(p):
            global pageNumber
            pageNumber = p
            for widget in mainProject.winfo_children():
                widget.destroy()
            globals()[f"page_{p}"]()

        # Navigation buttons
        btn_back = ttk.Button(mainProject, text="Back", command=back_func)
        btn_next = ttk.Button(mainProject, text="Next", command=next_func)
        ToolTip(btn_back, "Go to the previous page")
        ToolTip(btn_next, "Proceed to the next page")
        btn_back.place(relx=0.4, rely=0.95)
        btn_next.place(relx=0.5, rely=0.95)
        widgets_to_destroy.extend([canvas, scrollbar_y, scrollbar_x, zoom_in_button, zoom_out_button, progress, progress_label, workflow_canvas, btn_back, btn_next])

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

        projectTitle.insert(0, p1projecttitle)
        analystName.insert(0, p1analysts)
        polAnaTitle.insert(0, p1policyanalysis)
        fontsList.set(p1fontstyle)
        fontSize.insert(0, str(p1fontsize))

        def clear_page_1():
            projectTitle.config(bg="white")
            fontSize.config(bg="white")
            analystName.config(bg="white")
            polAnaTitle.config(bg="white")
            fontsList.set('')
            
            projectTitle.delete(0, END)
            polAnaTitle.delete(0, END)
            analystName.delete(0, END)
            fontSize.delete(0, END)
            indentation.delete(0, END)

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

    def page_2():                                                               # write problematic situation and undesirable effects

        status = Label(mainProject, text="")
        status.place(x=10, y=170)

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

        probSit.insert("1.0", p2problematicsituation)
        undeEff.insert("1.0", p2undesirableeffects)
        
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
        global p3efforts, p3accomplishments, p3assessments
        mainProject.geometry("1250x700")
        style = ttk.Style()
        style.configure('Treeview', rowheight=160)
        style.configure("TButton", foreground="black", font=("Arial", 10))  # Set button text to black

        # Undo stack
        undo_stack = []

        # Canvas with scrollbars
        canvas = tk.Canvas(mainProject)
        scrollbar_y = ttk.Scrollbar(mainProject, orient="vertical", command=canvas.yview)
        scrollbar_x = ttk.Scrollbar(mainProject, orient="horizontal", command=canvas.xview)
        canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        canvas.pack(side="left", fill="both", expand=True)
        frame3 = tk.LabelFrame(canvas)
        canvas.create_window((0, 0), window=frame3, anchor="nw")
        def configure_canvas(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        frame3.bind("<Configure>", configure_canvas)

        # Zoom functionality
        scale = 1.0
        def zoom_in():
            nonlocal scale
            scale *= 1.1
            canvas.scale("all", 0, 0, 1.1, 1.1)
            canvas.configure(scrollregion=canvas.bbox("all"))
        def zoom_out():
            nonlocal scale
            scale /= 1.1
            canvas.scale("all", 0, 0, 1/1.1, 1/1.1)
            canvas.configure(scrollregion=canvas.bbox("all"))
        zoom_in_button = ttk.Button(mainProject, text="Zoom In", command=zoom_in)
        zoom_out_button = ttk.Button(mainProject, text="Zoom Out", command=zoom_out)
        zoom_in_button.place(x=10, y=10)
        zoom_out_button.place(x=100, y=10)

        # Progress indicator
        progress_label = tk.Label(mainProject, text="Page 3 of 15: Current Efforts", font=("Arial", 12, "bold"))
        progress_label.place(x=10, y=50)

        # Treeview with scrollbars
        currEffLabel = tk.Label(frame3, text="Current Efforts/Measures of the Government to Solve the Situational Problem")
        effortsTable = ttk.Treeview(frame3, selectmode="browse", height=2)
        effortsTable["columns"] = ("1", "2", "3")
        effortsTable['show'] = 'headings'
        effortsTable.column("1", width=200, anchor='c', stretch=True)
        effortsTable.column("2", width=700, anchor='c', stretch=True)
        effortsTable.column("3", width=300, anchor='c', stretch=True)
        effortsTable.heading("1", text="Effort/Measure")
        effortsTable.heading("2", text="Accomplishments")
        effortsTable.heading("3", text="Assessment")
        sb_y = ttk.Scrollbar(frame3, orient="vertical", command=effortsTable.yview)
        sb_x = ttk.Scrollbar(frame3, orient="horizontal", command=effortsTable.xview)
        effortsTable.configure(yscrollcommand=sb_y.set, xscrollcommand=sb_x.set)
        currEffLabel.grid(row=0, column=0, columnspan=2)
        effortsTable.grid(row=1, column=0)
        sb_y.grid(row=1, column=1, sticky="ns")
        sb_x.grid(row=2, column=0, sticky="ew")

        # Input fields
        effoLabel = tk.Label(mainProject, text="Effort")
        accoLabel = tk.Label(mainProject, text="Accomplishment")
        asseLabel = tk.Label(mainProject, text="Assessment")
        effort = scrolledtext.ScrolledText(mainProject, height=9, width=40)
        accomplishment = scrolledtext.ScrolledText(mainProject, height=9, width=40)
        assessment = scrolledtext.ScrolledText(mainProject, height=9, width=40)
        effoLabel.place(x=195, y=390)
        effort.place(x=50, y=420)
        accoLabel.place(x=563, y=390)
        accomplishment.place(x=450, y=420)
        asseLabel.place(x=975, y=390)
        assessment.place(x=850, y=420)

        # Buttons with tooltips
        addButton = ttk.Button(mainProject, text="Add", style="TButton", command=lambda: add_data())
        ToolTip(addButton, "Add a new entry to the table")
        editButton = ttk.Button(mainProject, text="Edit", style="TButton", command=lambda: edit_data(), state="disabled")
        ToolTip(editButton, "Edit the selected table entry")
        deleteButton = ttk.Button(mainProject, text="Delete", style="TButton", command=lambda: delete_data(), state="disabled")
        ToolTip(deleteButton, "Delete the selected table entry")
        btnBack2 = ttk.Button(mainProject, text="Back", style="TButton", command=lambda: back_2())
        ToolTip(btnBack2, "Go to the previous page")
        btnNext2 = ttk.Button(mainProject, text="Next", style="TButton", command=lambda: next_2())
        ToolTip(btnNext2, "Proceed to the next page")
        addButton.place(x=490, y=590)
        editButton.place(x=680, y=590)
        deleteButton.place(x=870, y=590)
        btnBack2.place(x=490, y=650)
        btnNext2.place(x=680, y=650)

        if not effortsTable.get_children():
            for e, a, s in zip(p3efforts, p3accomplishments, p3assessments):
                effortsTable.insert("", "end", values=(wrap(e), wrap(a), wrap(s)))

        # Event handlers
        def show_data(a):
            effort.delete("1.0", tk.END)
            accomplishment.delete("1.0", tk.END)
            assessment.delete("1.0", tk.END)
            selectedItem = effortsTable.selection()
            if selectedItem:
                editButton.config(state="normal")
                deleteButton.config(state="normal")
                effort.insert(tk.INSERT, effortsTable.item(selectedItem[0])['values'][0])
                accomplishment.insert(tk.INSERT, effortsTable.item(selectedItem[0])['values'][1])
                assessment.insert(tk.INSERT, effortsTable.item(selectedItem[0])['values'][2])
            else:
                editButton.config(state="disabled")
                deleteButton.config(state="disabled")
        effortsTable.bind("<<TreeviewSelect>>", show_data)

        def add_data():
            effortText = effort.get("1.0", tk.END).strip()
            accomplishmentText = accomplishment.get("1.0", tk.END).strip()
            assessmentText = assessment.get("1.0", tk.END).strip()
            if not (effortText and accomplishmentText and assessmentText):
                messagebox.showerror("Error", "Please fill out all fields")
                return
            item_id = effortsTable.insert("", 'end', values=(wrap(effortText), wrap(accomplishmentText), wrap(assessmentText)))
            undo_stack.append(("add", item_id))
            p3efforts.append(effortText)
            p3accomplishments.append(accomplishmentText)
            p3assessments.append(assessmentText)
            effort.delete("1.0", tk.END)
            accomplishment.delete("1.0", tk.END)
            assessment.delete("1.0", tk.END)
            effort.focus()

        def edit_data():
            effortText = effort.get("1.0", tk.END).strip()
            accomplishmentText = accomplishment.get("1.0", tk.END).strip()
            assessmentText = assessment.get("1.0", tk.END).strip()
            if not (effortText and accomplishmentText and assessmentText):
                messagebox.showerror("Error", "Please fill out all fields")
                return
            selected_item = effortsTable.selection()[0]
            old_values = effortsTable.item(selected_item)['values']
            undo_stack.append(("edit", selected_item, old_values))
            effortsTable.item(selected_item, values=(effortText, accomplishmentText, assessmentText))
            p3efforts[effortsTable.index(selected_item)] = effortText
            p3accomplishments[effortsTable.index(selected_item)] = accomplishmentText
            p3assessments[effortsTable.index(selected_item)] = assessmentText

        def delete_data():
            selected_item = effortsTable.selection()
            if selected_item:
                item_id = selected_item[0]
                old_values = effortsTable.item(item_id)['values']
                index = effortsTable.index(item_id)
                undo_stack.append(("delete", item_id, old_values, index))
                effortsTable.delete(item_id)
                p3efforts.pop(index)
                p3accomplishments.pop(index)
                p3assessments.pop(index)
                effort.delete("1.0", tk.END)
                accomplishment.delete("1.0", tk.END)
                assessment.delete("1.0", tk.END)
                editButton.config(state="disabled")
                deleteButton.config(state="disabled")
            else:
                messagebox.showwarning("Warning", "Please select an item to delete")

        def undo():
            if not undo_stack:
                return
            action, *data = undo_stack.pop()
            if action == "add":
                item_id = data[0]
                effortsTable.delete(item_id)
                p3efforts.pop()
                p3accomplishments.pop()
                p3assessments.pop()
            elif action == "edit":
                item_id, old_values = data
                effortsTable.item(item_id, values=old_values)
                index = effortsTable.index(item_id)
                p3efforts[index] = old_values[0]
                p3accomplishments[index] = old_values[1]
                p3assessments[index] = old_values[2]
            elif action == "delete":
                item_id, old_values, index = data
                effortsTable.insert("", index, iid=item_id, values=old_values)
                p3efforts.insert(index, old_values[0])
                p3accomplishments.insert(index, old_values[1])
                p3assessments.insert(index, old_values[2])

        # Keyboard shortcuts
        mainProject.bind("<Control-z>", lambda event: undo())
        mainProject.bind("<Control-Return>", lambda event: add_data())
        effort.bind("<Tab>", lambda event: accomplishment.focus_set())
        accomplishment.bind("<Tab>", lambda event: assessment.focus_set())
        assessment.bind("<Tab>", lambda event: addButton.focus_set())

        def back_2():
            global pageNumber
            pageNumber -= 1
            for widget in mainProject.winfo_children():
                widget.destroy()
            page_2()

        def next_2():
            global pageNumber
            pageNumber += 1
            for widget in mainProject.winfo_children():
                widget.destroy()
            page_4()

    def page_4():
        global var
        var = tk.IntVar()
        mainProject.state('zoomed')
        style.configure("TButton", foreground="black", font=("Arial", 10))
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
        global p5rootcause, assessmentTuple
        frame5 = tk.LabelFrame(mainProject)
        widgets_to_destroy = [frame5]
        undo_stack = []

        root_cause_label = tk.Label(frame5, text="Root Cause of the Problem", font=("Arial", 12, "bold"))
        root_cause = tk.Entry(frame5, width=100)
        assessment_label = tk.Label(frame5, text="Assessment of Existing Policies that Address the Root Cause", font=("Arial", 12, "bold"))
        assessment_table = ttk.Treeview(frame5, selectmode="browse", height=2)
        assessment_table["columns"] = ("1", "2", "3", "4")
        assessment_table['show'] = 'headings'
        assessment_table.column("1", width=150, anchor='c')
        assessment_table.column("2", width=650, anchor='c')
        assessment_table.column("3", width=400, anchor='c')
        assessment_table.column("4", width=300, anchor='c')
        assessment_table.heading("1", text="Existing Policy")
        assessment_table.heading("2", text="Relevant Provision(s)")
        assessment_table.heading("3", text="Accomplishments")
        assessment_table.heading("4", text="Assessment")
        sb_y = ttk.Scrollbar(frame5, orient="vertical", command=assessment_table.yview)
        sb_x = ttk.Scrollbar(frame5, orient="horizontal", command=assessment_table.xview)
        assessment_table.configure(yscrollcommand=sb_y.set, xscrollcommand=sb_x.set)

        exist_label = tk.Label(mainProject, text="Existing Policy")
        rele_label = tk.Label(mainProject, text="Relevant Provision")
        accomp_label = tk.Label(mainProject, text="Accomplishment")
        assess_label = tk.Label(mainProject, text="Assessment")
        existing_policy = scrolledtext.ScrolledText(mainProject, height=9, width=40)
        relevant_provision = scrolledtext.ScrolledText(mainProject, height=9, width=40)
        accomplishment2 = scrolledtext.ScrolledText(mainProject, height=9, width=40)
        assessment2 = scrolledtext.ScrolledText(mainProject, height=9, width=40)
        add_button = ttk.Button(mainProject, text="Add", command=lambda: add_data2())
        edit_button = ttk.Button(mainProject, text="Edit", state="disabled", command=lambda: edit_data2())
        delete_button = ttk.Button(mainProject, text="Delete", state="disabled", command=lambda: delete_data2())
        ToolTip(add_button, "Add a new entry to the table")
        ToolTip(edit_button, "Edit the selected table entry")
        ToolTip(delete_button, "Delete the selected table entry")

        root_cause_label.grid(row=0, column=0, columnspan=2, pady=10)
        root_cause.grid(row=1, column=0, columnspan=2, padx=10)
        assessment_label.grid(row=2, column=0, columnspan=2, pady=10)
        assessment_table.grid(row=3, column=0)
        sb_y.grid(row=3, column=1, sticky="ns")
        sb_x.grid(row=4, column=0, sticky="ew")
        exist_label.place(relx=0.1, rely=0.6)
        existing_policy.place(relx=0.05, rely=0.65)
        rele_label.place(relx=0.3, rely=0.6)
        relevant_provision.place(relx=0.25, rely=0.65)
        accomp_label.place(relx=0.5, rely=0.6)
        accomplishment2.place(relx=0.45, rely=0.65)
        assess_label.place(relx=0.7, rely=0.6)
        assessment2.place(relx=0.65, rely=0.65)
        add_button.place(relx=0.4, rely=0.85)
        edit_button.place(relx=0.5, rely=0.85)
        delete_button.place(relx=0.6, rely=0.85)

        def show_data2(a):
            existing_policy.delete("1.0", tk.END)
            relevant_provision.delete("1.0", tk.END)
            accomplishment2.delete("1.0", tk.END)
            assessment2.delete("1.0", tk.END)
            selected_item = assessment_table.selection()
            if selected_item:
                edit_button.config(state="normal")
                delete_button.config(state="normal")
                values = assessment_table.item(selected_item[0])['values']
                existing_policy.insert("1.0", values[0])
                relevant_provision.insert("1.0", values[1])
                accomplishment2.insert("1.0", values[2])
                assessment2.insert("1.0", values[3])
            else:
                edit_button.config(state="disabled")
                delete_button.config(state="disabled")

        def add_data2():
            texts = [
                existing_policy.get("1.0", tk.END).strip(),
                relevant_provision.get("1.0", tk.END).strip(),
                accomplishment2.get("1.0", tk.END).strip(),
                assessment2.get("1.0", tk.END).strip()
            ]
            if not all(texts):
                messagebox.showerror("Error", "Please fill out all fields")
                return
            item_id = assessment_table.insert("", 'end', values=texts)
            undo_stack.append(("add", item_id))
            global assessmentTuple
            assessmentTuple = texts
            existing_policy.delete("1.0", tk.END)
            relevant_provision.delete("1.0", tk.END)
            accomplishment2.delete("1.0", tk.END)
            assessment2.delete("1.0", tk.END)
            existing_policy.focus()

        def edit_data2():
            texts = [
                existing_policy.get("1.0", tk.END).strip(),
                relevant_provision.get("1.0", tk.END).strip(),
                accomplishment2.get("1.0", tk.END).strip(),
                assessment2.get("1.0", tk.END).strip()
            ]
            if not all(texts):
                messagebox.showerror("Error", "Please fill out all fields")
                return
            selected_item = assessment_table.selection()[0]
            old_values = assessment_table.item(selected_item)['values']
            undo_stack.append(("edit", selected_item, old_values))
            assessment_table.item(selected_item, values=texts)
            global assessmentTuple
            assessmentTuple = texts

        def delete_data2():
            selected_item = assessment_table.selection()
            if selected_item:
                item_id = selected_item[0]
                old_values = assessment_table.item(item_id)['values']
                undo_stack.append(("delete", item_id, old_values))
                assessment_table.delete(item_id)
                existing_policy.delete("1.0", tk.END)
                relevant_provision.delete("1.0", tk.END)
                accomplishment2.delete("1.0", tk.END)
                assessment2.delete("1.0", tk.END)
                edit_button.config(state="disabled")
                delete_button.config(state="disabled")
            else:
                # Handle other statistical methods (Linear, Multiple, Logistic Regression)
                method_names = {1: "Linear Regression", 2: "Multiple Regression", 3: "Logistic Regression"}
                method = method_names.get(var.get(), "Unknown Method")
                result_label = tk.Label(content_frame, text=f"Results for {method} will be displayed here.", font=("Arial", 12))
                result_label.pack(pady=10)

        def back_4():
            global pageNumber
            pageNumber -= 1
            for widget in mainProject.winfo_children():
                widget.destroy()
            page_4()

        def next_4():
            global pageNumber, p5rootcause
            p5rootcause = root_cause.get().strip()
            if not p5rootcause:
                status.config(text="Enter root cause", foreground="red")
                status.place(relx=0.01, rely=0.9)
                return
            with open("page5_data.json", "w") as f:
                json.dump({"root_cause": p5rootcause, "assessments": [assessment_table.item(i)['values'] for i in assessment_table.get_children()]}, f)
            pageNumber += 1
            for widget in mainProject.winfo_children():
                widget.destroy()
            page_6()

        setup_page_common(5, "Root Cause and Policy Assessment", frame5, widgets_to_destroy, back_4, next_4)
        try:
            with open("page5_data.json", "r") as f:
                data = json.load(f)
                p5rootcause = data.get("root_cause", "")
                root_cause.insert(0, p5rootcause)
                for item in data.get("assessments", []):
                    assessment_table.insert("", "end", values=item)
        except FileNotFoundError:
            pass

    global p6policyproblem, p6policyissue
    p6policyproblem = " "
    p6policyissue = " "

    def page_6():
        global mainProject, pageNumber, p6policyproblem
        # Initialize p6policyproblem as a StringVar to store the policy problem text
        p6policyproblem = tk.StringVar(value="")  # Default to empty string
        mainProject.state('zoomed')
        style.configure("TButton", foreground="black", font=("Arial", 10))
        frame6 = tk.LabelFrame(mainProject, text="Policy Problem Definition", font=("Arial", 12, "bold"))
        widgets_to_destroy = [frame6]

        # UI Elements
        title_label = tk.Label(frame6, text="Define the Policy Problem", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)

        # Text input for policy problem
        policy_label = tk.Label(frame6, text="Enter the policy problem:", font=("Arial", 12))
        policy_label.pack(pady=5)
        policy_text = tk.Text(frame6, height=5, width=50, font=("Arial", 10))
        policy_text.pack(pady=5)

        # Bind the Text widget to p6policyproblem
        def update_policy_problem():
            p6policyproblem.set(policy_text.get("1.0", tk.END).strip())

        # Update p6policyproblem when the user types
        policy_text.bind("<KeyRelease>", lambda event: update_policy_problem())

        def back_5():
            global pageNumber
            pageNumber -= 1
            for widget in mainProject.winfo_children():
                widget.destroy()
            page_5()

        def next_5():
            global pageNumber
            if not p6policyproblem.get():
                messagebox.showwarning("Warning", "Please enter a policy problem before proceeding.")
                return
            if not p6policyissue:
                status.config(text="Enter policy issue statement", foreground="red")
                return
            with open("page6_data.json", "w") as f:
                json.dump({"policy_problem": p6policyproblem, "policy_issue": p6policyissue}, f)
            pageNumber += 1
            for widget in mainProject.winfo_children():
                widget.destroy()
            page_7()

        setup_page_common(6, "Policy Problem and Issue", frame6, widgets_to_destroy, back_5, next_5)
        try:
            with open("page6_data.json", "r") as f:
                data = json.load(f)
                policy_prob.insert("1.0", data.get("policy_problem", ""))
                policy_iss.insert("1.0", data.get("policy_issue", ""))
        except FileNotFoundError:
            pass

    p7policyGoalsandObjectives = []
    p7indicators = []

    def page_7():
        global p7policyGoalsandObjectives, p7indicators
        frame7 = tk.LabelFrame(mainProject)
        widgets_to_destroy = [frame7]
        undo_stack = []

        goals_obj_label = tk.Label(frame7, text="Goals and Objectives of the Proposal", font=("Arial", 12, "bold"))
        goals_and_obj_table = ttk.Treeview(frame7, selectmode="browse", height=5)
        goals_and_obj_table["columns"] = ("1", "2")
        goals_and_obj_table['show'] = 'headings'
        goals_and_obj_table.column("1", width=350, anchor='c')
        goals_and_obj_table.column("2", width=500, anchor='c')
        goals_and_obj_table.heading("1", text="Policy Goals and Objectives")
        goals_and_obj_table.heading("2", text="Indicators")
        sb_y = ttk.Scrollbar(frame7, orient="vertical", command=goals_and_obj_table.yview)
        sb_x = ttk.Scrollbar(frame7, orient="horizontal", command=goals_and_obj_table.xview)
        goals_and_obj_table.configure(yscrollcommand=sb_y.set, xscrollcommand=sb_x.set)

        pgo_label = tk.Label(mainProject, text="Policy Goals and Objectives")
        indi_label = tk.Label(mainProject, text="Indicators")
        pgo = tk.Entry(mainProject, width=40)
        indi = scrolledtext.ScrolledText(mainProject, height=3, width=55)
        add_button = ttk.Button(mainProject, text="Add", command=lambda: add_data3())
        edit_button = ttk.Button(mainProject, text="Edit", state="disabled", command=lambda: edit_data3())
        delete_button = ttk.Button(mainProject, text="Delete", state="disabled", command=lambda: delete_data3())
        ToolTip(add_button, "Add a new entry to the table")
        ToolTip(edit_button, "Edit the selected table entry")
        ToolTip(delete_button, "Delete the selected table entry")

        goals_obj_label.grid(row=0, column=0, columnspan=2, pady=10)
        goals_and_obj_table.grid(row=1, column=0)
        sb_y.grid(row=1, column=1, sticky="ns")
        sb_x.grid(row=2, column=0, sticky="ew")
        pgo_label.place(relx=0.1, rely=0.6)
        pgo.place(relx=0.05, rely=0.65)
        indi_label.place(relx=0.5, rely=0.6)
        indi.place(relx=0.45, rely=0.65)
        add_button.place(relx=0.4, rely=0.85)
        edit_button.place(relx=0.5, rely=0.85)
        delete_button.place(relx=0.6, rely=0.85)

        def show_data3(a):
            pgo.delete(0, tk.END)
            indi.delete("1.0", tk.END)
            selected_item = goals_and_obj_table.selection()
            if selected_item:
                edit_button.config(state="normal")
                delete_button.config(state="normal")
                values = goals_and_obj_table.item(selected_item[0])['values']
                pgo.insert(0, values[0])
                indi.insert("1.0", values[1])
            else:
                edit_button.config(state="disabled")
                delete_button.config(state="disabled")

        def add_data3():
            pgo_text = pgo.get().strip()
            indi_text = indi.get("1.0", tk.END).strip()
            if not (pgo_text and indi_text):
                messagebox.showerror("Error", "Please fill out all fields")
                return
            item_id = goals_and_obj_table.insert("", 'end', values=(pgo_text, indi_text))
            undo_stack.append(("add", item_id))
            p7policyGoalsandObjectives.append(pgo_text)
            p7indicators.append(indi_text)
            pgo.delete(0, tk.END)
            indi.delete("1.0", tk.END)
            pgo.focus()

        def edit_data3():
            pgo_text = pgo.get().strip()
            indi_text = indi.get("1.0", tk.END).strip()
            if not (pgo_text and indi_text):
                messagebox.showerror("Error", "Please fill out all fields")
                return
            selected_item = goals_and_obj_table.selection()[0]
            old_values = goals_and_obj_table.item(selected_item)['values']
            undo_stack.append(("edit", selected_item, old_values))
            goals_and_obj_table.item(selected_item, values=(pgo_text, indi_text))
            index = goals_and_obj_table.index(selected_item)
            p7policyGoalsandObjectives[index] = pgo_text
            p7indicators[index] = indi_text

        def delete_data3():
            selected_item = goals_and_obj_table.selection()
            if selected_item:
                item_id = selected_item[0]
                index = goals_and_obj_table.index(item_id)
                old_values = goals_and_obj_table.item(item_id)['values']
                undo_stack.append(("delete", item_id, old_values, index))
                goals_and_obj_table.delete(item_id)
                p7policyGoalsandObjectives.pop(index)
                p7indicators.pop(index)
                pgo.delete(0, tk.END)
                indi.delete("1.0", tk.END)
                edit_button.config(state="disabled")
                delete_button.config(state="disabled")
            else:
                messagebox.showwarning("Warning", "Please select an item to delete")

        def undo():
            if not undo_stack:
                return
            action, *data = undo_stack.pop()
            if action == "add":
                goals_and_obj_table.delete(data[0])
                p7policyGoalsandObjectives.pop()
                p7indicators.pop()
            elif action == "edit":
                item_id, old_values = data
                goals_and_obj_table.item(item_id, values=old_values)
                index = goals_and_obj_table.index(item_id)
                p7policyGoalsandObjectives[index] = old_values[0]
                p7indicators[index] = old_values[1]
            elif action == "delete":
                item_id, old_values, index = data
                goals_and_obj_table.insert("", index, iid=item_id, values=old_values)
                p7policyGoalsandObjectives.insert(index, old_values[0])
                p7indicators.insert(index, old_values[1])

        goals_and_obj_table.bind("<<TreeviewSelect>>", show_data3)
        mainProject.bind("<Control-z>", lambda e: undo())
        mainProject.bind("<Control-Return>", lambda e: add_data3())
        pgo.bind("<Tab>", lambda e: indi.focus_set())
        indi.bind("<Tab>", lambda e: add_button.focus_set())

        def back_6():
            global pageNumber
            pageNumber -= 1
            for widget in mainProject.winfo_children():
                widget.destroy()
            page_6()

        def next_6():
            global pageNumber
            ##with open("page7_data.json", "w") as f:
            ##    json.dump({"goals": p7policyGoalsandObjectives, "indicators": p7indicators}, f)
            ##pageNumber += 1
            for widget in mainProject.winfo_children():
                widget.destroy()
            page_8()

        setup_page_common(7, "Goals and Objectives", frame7, widgets_to_destroy, back_6, next_6)
        ##try:
        ##    with open("page7_data.json", "r") as f:
        ##        data = json.load(f)
        ##        for g, i in zip(data.get("goals", []), data.get("indicators", [])):
        ##            goals_and_obj_table.insert("", "end", values=(g, i))
        ##            p7policyGoalsandObjectives.append(g)
        ##            p7indicators.append(i)
        ##except FileNotFoundError:
        ##    pass

    def page_8():
        global p8stakeholders, p8actors
        frame8 = tk.LabelFrame(mainProject)
        widgets_to_destroy = [frame8]
        undo_stack = []

        sta_and_act_label = tk.Label(frame8, text="Stakeholders and Actors", font=("Arial", 12, "bold"))
        sta_and_act_table = ttk.Treeview(frame8, selectmode="browse", height=10)
        sta_and_act_table["columns"] = ("1", "2")
        sta_and_act_table['show'] = 'headings'
        sta_and_act_table.column("1", width=350, anchor='c')
        sta_and_act_table.column("2", width=350, anchor='c')
        sta_and_act_table.heading("1", text="Stakeholders")
        sta_and_act_table.heading("2", text="Actors")
        sb_y = ttk.Scrollbar(frame8, orient="vertical", command=sta_and_act_table.yview)
        sb_x = ttk.Scrollbar(frame8, orient="horizontal", command=sta_and_act_table.xview)
        sta_and_act_table.configure(yscrollcommand=sb_y.set, xscrollcommand=sb_x.set)

        stakeholders_label = tk.Label(mainProject, text="Stakeholders")
        actors_label = tk.Label(mainProject, text="Actors")
        stakeholders = tk.Entry(mainProject, width=40)
        actors = tk.Entry(mainProject, width=40)
        add_button = ttk.Button(mainProject, text="Add", command=lambda: add_data4())
        edit_button = ttk.Button(mainProject, text="Edit", state="disabled", command=lambda: edit_data4())
        delete_button = ttk.Button(mainProject, text="Delete", state="disabled", command=lambda: delete_data4())
        ToolTip(add_button, "Add a new entry to the table")
        ToolTip(edit_button, "Edit the selected table entry")
        ToolTip(delete_button, "Delete the selected table entry")

        sta_and_act_label.grid(row=0, column=0, columnspan=2, pady=10)
        sta_and_act_table.grid(row=1, column=0)
        sb_y.grid(row=1, column=1, sticky="ns")
        sb_x.grid(row=2, column=0, sticky="ew")
        stakeholders_label.place(relx=0.1, rely=0.6)
        stakeholders.place(relx=0.05, rely=0.65)
        actors_label.place(relx=0.5, rely=0.6)
        actors.place(relx=0.45, rely=0.65)
        add_button.place(relx=0.4, rely=0.85)
        edit_button.place(relx=0.5, rely=0.85)
        delete_button.place(relx=0.6, rely=0.85)

        def show_data4(a):
            stakeholders.delete(0, tk.END)
            actors.delete(0, tk.END)
            selected_item = sta_and_act_table.selection()
            if selected_item:
                edit_button.config(state="normal")
                delete_button.config(state="normal")
                values = sta_and_act_table.item(selected_item[0])['values']
                stakeholders.insert(0, values[0])
                actors.insert(0, values[1])
            else:
                edit_button.config(state="disabled")
                delete_button.config(state="disabled")

        def add_data4():
            stakeholders_text = stakeholders.get().strip()
            actors_text = actors.get().strip()
            if not (stakeholders_text and actors_text):
                messagebox.showerror("Error", "Please fill out all fields")
                return
            item_id = sta_and_act_table.insert("", 'end', values=(stakeholders_text, actors_text))
            undo_stack.append(("add", item_id))
            p8stakeholders.append(stakeholders_text)
            p8actors.append(actors_text)
            stakeholders.delete(0, tk.END)
            actors.delete(0, tk.END)
            stakeholders.focus()

        def edit_data4():
            stakeholders_text = stakeholders.get().strip()
            actors_text = actors.get().strip()
            if not (stakeholders_text and actors_text):
                messagebox.showerror("Error", "Please fill out all fields")
                return
            selected_item = sta_and_act_table.selection()[0]
            old_values = sta_and_act_table.item(selected_item)['values']
            undo_stack.append(("edit", selected_item, old_values))
            sta_and_act_table.item(selected_item, values=(stakeholders_text, actors_text))
            index = sta_and_act_table.index(selected_item)
            p8stakeholders[index] = stakeholders_text
            p8actors[index] = actors_text

        def delete_data4():
            selected_item = sta_and_act_table.selection()
            if selected_item:
                item_id = selected_item[0]
                index = sta_and_act_table.index(item_id)
                old_values = sta_and_act_table.item(item_id)['values']
                undo_stack.append(("delete", item_id, old_values, index))
                sta_and_act_table.delete(item_id)
                p8stakeholders.pop(index)
                p8actors.pop(index)
                stakeholders.delete(0, tk.END)
                actors.delete(0, tk.END)
                edit_button.config(state="disabled")
                delete_button.config(state="disabled")
            else:
                messagebox.showwarning("Warning", "Please select an item to delete")

        def undo():
            if not undo_stack:
                return
            action, *data = undo_stack.pop()
            if action == "add":
                sta_and_act_table.delete(data[0])
                p8stakeholders.pop()
                p8actors.pop()
            elif action == "edit":
                item_id, old_values = data
                sta_and_act_table.item(item_id, values=old_values)
                index = sta_and_act_table.index(item_id)
                p8stakeholders[index] = old_values[0]
                p8actors[index] = old_values[1]
            elif action == "delete":
                item_id, old_values, index = data
                sta_and_act_table.insert("", index, iid=item_id, values=old_values)
                p8stakeholders.insert(index, old_values[0])
                p8actors.insert(index, old_values[1])

        sta_and_act_table.bind("<<TreeviewSelect>>", show_data4)
        mainProject.bind("<Control-z>", lambda e: undo())
        mainProject.bind("<Control-Return>", lambda e: add_data4())
        stakeholders.bind("<Tab>", lambda e: actors.focus_set())
        actors.bind("<Tab>", lambda e: add_button.focus_set())

        def back_7():
            global pageNumber
            pageNumber -= 1
            for widget in mainProject.winfo_children():
                widget.destroy()
            page_7()

        def next_7():
            global pageNumber
            ##with open("page8_data.json", "w") as f:
            ##    json.dump({"stakeholders": p8stakeholders, "actors": p8actors}, f)
            ##pageNumber += 1
            for widget in mainProject.winfo_children():
                widget.destroy()
            page_9()

        setup_page_common(8, "Stakeholders and Actors", frame8, widgets_to_destroy, back_7, next_7)
        ##try:
        ##    with open("page8_data.json", "r") as f:
        ##        data = json.load(f)
        ##        for s, a in zip(data.get("stakeholders", []), data.get("actors", [])):
        ##            sta_and_act_table.insert("", "end", values=(s, a))
        ##            p8stakeholders.append(s)
        ##            p8actors.append(a)
        ##except FileNotFoundError:
        ##    pass

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
            policyAlternatives.focus()

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
        frame10 = tk.LabelFrame(mainProject)
        widgets_to_destroy = [frame10]
        undo_stack = []

        # UI Setup
        assessPALabel = tk.Label(frame10, text="Assessments of the Policy Alternatives: Spillovers, Externalities, and Constraints", font=("Arial", 12, "bold"))
        assessPATable = ttk.Treeview(frame10, selectmode="browse", height=3)
        assessPATable["columns"] = ("1", "2", "3", "4", "5")
        assessPATable['show'] = 'headings'
        assessPATable.column("1", width=300, anchor='c')
        assessPATable.column("2", width=250, anchor='c')
        assessPATable.column("3", width=180, anchor='c')
        assessPATable.column("4", width=140, anchor='c')
        assessPATable.column("5", width=180, anchor='c')
        assessPATable.heading("1", text="Alternative")
        assessPATable.heading("2", text="Spillovers")
        assessPATable.heading("3", text="Externalities")
        assessPATable.heading("4", text="Constraints")
        assessPATable.heading("5", text="Mitigating Measures")
        sb_y = ttk.Scrollbar(frame10, orient="vertical", command=assessPATable.yview)
        sb_x = ttk.Scrollbar(frame10, orient="horizontal", command=assessPATable.xview)
        assessPATable.configure(yscrollcommand=sb_y.set, xscrollcommand=sb_x.set)

        alternaLabel = tk.Label(mainProject, text="Alternative")
        spillovLabel = tk.Label(mainProject, text="Spillovers")
        externaLabel = tk.Label(mainProject, text="Externalities")
        constraLabel = tk.Label(mainProject, text="Constraints")
        mitmeasLabel = tk.Label(mainProject, text="Mitigating Measures")
        alternative = tk.Entry(mainProject, width=50)
        spillover = scrolledtext.ScrolledText(mainProject, height=4, width=25)
        externality = scrolledtext.ScrolledText(mainProject, height=4, width=25)
        constraint = scrolledtext.ScrolledText(mainProject, height=4, width=25)
        mitimeasure = scrolledtext.ScrolledText(mainProject, height=4, width=25)
        addButton10 = ttk.Button(mainProject, text="Add", command=lambda: add_data10())
        editButton10 = ttk.Button(mainProject, text="Edit", state="disabled", command=lambda: edit_data10())
        deleteButton10 = ttk.Button(mainProject, text="Delete", state="disabled", command=lambda: delete_data10())
        ToolTip(addButton10, "Add a new entry to the table")
        ToolTip(editButton10, "Edit the selected table entry")
        ToolTip(deleteButton10, "Delete the selected table entry")

        # Layout
        assessPALabel.grid(row=0, column=0, columnspan=2, pady=10)
        assessPATable.grid(row=1, column=0)
        sb_y.grid(row=1, column=1, sticky="ns")
        sb_x.grid(row=2, column=0, sticky="ew")
        alternaLabel.place(relx=0.05, rely=0.5)
        alternative.place(relx=0.05, rely=0.55)
        spillovLabel.place(relx=0.25, rely=0.5)
        spillover.place(relx=0.25, rely=0.55)
        externaLabel.place(relx=0.45, rely=0.5)
        externality.place(relx=0.45, rely=0.55)
        constraLabel.place(relx=0.65, rely=0.5)
        constraint.place(relx=0.65, rely=0.55)
        mitmeasLabel.place(relx=0.85, rely=0.5)
        mitimeasure.place(relx=0.85, rely=0.55)
        addButton10.place(relx=0.4, rely=0.85)
        editButton10.place(relx=0.5, rely=0.85)
        deleteButton10.place(relx=0.6, rely=0.85)

        # Populate table with p9alternatives
        for i, alt in enumerate(p9alternatives):
            assessPATable.insert("", 'end', values=(f"Alt {i+1}: {alt}", "", "", "", ""))

        def show_data10(a):
            alternative.delete(0, tk.END)
            spillover.delete("1.0", tk.END)
            externality.delete("1.0", tk.END)
            constraint.delete("1.0", tk.END)
            mitimeasure.delete("1.0", tk.END)
            selected_item = assessPATable.selection()
            if selected_item:
                editButton10.config(state="normal")
                deleteButton10.config(state="normal")
                values = assessPATable.item(selected_item[0])['values']
                alternative.insert(0, values[0])
                spillover.insert("1.0", values[1])
                externality.insert("1.0", values[2])
                constraint.insert("1.0", values[3])
                mitimeasure.insert("1.0", values[4])
            else:
                editButton10.config(state="disabled")
                deleteButton10.config(state="disabled")

        def add_data10():
            texts = [
                alternative.get().strip(),
                spillover.get("1.0", tk.END).strip(),
                externality.get("1.0", tk.END).strip(),
                constraint.get("1.0", tk.END).strip(),
                mitimeasure.get("1.0", tk.END).strip()
            ]
            if not all(texts):
                messagebox.showerror("Error", "Please fill out all fields")
                return
            item_id = assessPATable.insert("", 'end', values=texts)
            undo_stack.append(("add", item_id))
            alternative.delete(0, tk.END)
            spillover.delete("1.0", tk.END)
            externality.delete("1.0", tk.END)
            constraint.delete("1.0", tk.END)
            mitimeasure.delete("1.0", tk.END)
            alternative.focus()

        def edit_data10():
            texts = [
                alternative.get().strip(),
                spillover.get("1.0", tk.END).strip(),
                externality.get("1.0", tk.END).strip(),
                constraint.get("1.0", tk.END).strip(),
                mitimeasure.get("1.0", tk.END).strip()
            ]
            if not all(texts):
                messagebox.showerror("Error", "Please fill out all fields")
                return
            selected_item = assessPATable.selection()[0]
            old_values = assessPATable.item(selected_item)['values']
            undo_stack.append(("edit", selected_item, old_values))
            assessPATable.item(selected_item, values=texts)

        def delete_data10():
            selected_item = assessPATable.selection()
            if selected_item:
                item_id = selected_item[0]
                old_values = assessPATable.item(item_id)['values']
                undo_stack.append(("delete", item_id, old_values))
                assessPATable.delete(item_id)
                alternative.delete(0, tk.END)
                spillover.delete("1.0", tk.END)
                externality.delete("1.0", tk.END)
                constraint.delete("1.0", tk.END)
                mitimeasure.delete("1.0", tk.END)
                editButton10.config(state="disabled")
                deleteButton10.config(state="disabled")
            else:
                messagebox.showwarning("Warning", "Please select an item to delete")

        def undo():
            if not undo_stack:
                return
            action, *data = undo_stack.pop()
            if action == "add":
                assessPATable.delete(data[0])
            elif action == "edit":
                item_id, old_values = data
                assessPATable.item(item_id, values=old_values)
            elif action == "delete":
                item_id, old_values = data
                assessPATable.insert("", "end", iid=item_id, values=old_values)

        assessPATable.bind("<<TreeviewSelect>>", show_data10)
        mainProject.bind("<Control-z>", lambda e: undo())
        mainProject.bind("<Control-Return>", lambda e: add_data10())
        alternative.bind("<Tab>", lambda e: spillover.focus_set())
        spillover.bind("<Tab>", lambda e: externality.focus_set())
        externality.bind("<Tab>", lambda e: constraint.focus_set())
        constraint.bind("<Tab>", lambda e: mitimeasure.focus_set())
        mitimeasure.bind("<Tab>", lambda e: addButton10.focus_set())

        def back_9():
            global pageNumber
            pageNumber -= 1
            for widget in mainProject.winfo_children():
                widget.destroy()
            page_9()

        def next_9():
            global pageNumber
            ##with open("page10_data.json", "w") as f:
            ##    json.dump({"assessments": [assessPATable.item(i)['values'] for i in assessPATable.get_children()]}, f)
            pageNumber += 1
            for widget in mainProject.winfo_children():
                widget.destroy()
            page_11()

        setup_page_common(10, "Assessments of Policy Alternatives", frame10, widgets_to_destroy, back_9, next_9)
        ##try:
        ##    with open("page10_data.json", "r") as f:
        ##        data = json.load(f)
        ##        for item in data.get("assessments", []):
        ##            assessPATable.insert("", "end", values=item)
        ##except FileNotFoundError:
        ##    pass

    p11BPAdescription = " "
    p11BPAreasonSelect = " "

    def page_11():
        global p11BPAdescription, p11BPAreasonSelect
        frame11 = tk.LabelFrame(mainProject)
        widgets_to_destroy = [frame11]

        p11Label = tk.Label(mainProject, text="Description of the Best/Optimal Policy Alternative", font=("Arial", 12, "bold"))
        descrLabel = tk.Label(frame11, text="Description")
        descr = scrolledtext.ScrolledText(frame11, height=8, width=30)
        reaSelLabel = tk.Label(frame11, text="Reasons for Selection")
        reaSel = scrolledtext.ScrolledText(frame11, height=8, width=30)
        status.place(relx=0.01, rely=0.9)

        p11Label.grid(row=0, column=0, columnspan=2, pady=10)
        descrLabel.grid(row=1, column=0, sticky="w", padx=7)
        descr.grid(row=2, column=0, sticky="w", padx=7)
        reaSelLabel.grid(row=1, column=1, sticky="w", padx=7)
        reaSel.grid(row=2, column=1, sticky="w", padx=7)

        def back_10():
            global pageNumber
            pageNumber -= 1
            for widget in mainProject.winfo_children():
                widget.destroy()
            page_10()

        def next_10():
            global pageNumber, p11BPAdescription, p11BPAreasonSelect
            p11BPAdescription = descr.get("1.0", tk.END).strip()
            p11BPAreasonSelect = reaSel.get("1.0", tk.END).strip()
            if not p11BPAdescription:
                status.config(text="Enter description", foreground="red")
                return
            if not p11BPAreasonSelect:
                status.config(text="Enter reason for selection", foreground="red")
                return
            ##with open("page11_data.json", "w") as f:
            ##    json.dump({"description": p11BPAdescription, "reason": p11BPAreasonSelect}, f)
            save()
            pageNumber += 1
            for widget in mainProject.winfo_children():
                widget.destroy()
            page_12()

        setup_page_common(11, "Best Policy Alternative Description", frame11, widgets_to_destroy, back_10, next_10)
        ##try:
        ##    with open("page11_data.json", "r") as f:
        ##        data = json.load(f)
        ##        descr.insert("1.0", data.get("description", ""))
        ##        reaSel.insert("1.0", data.get("reason", ""))
        ##except FileNotFoundError:
        ##    pass

    p12BPAspillover = " "
    p12BPAexternality = " "
    p12BPAconstraint = " "
    p12BPAmitigatingmeasure = " "

    def page_12():
        global p12BPAspillover, p12BPAexternality, p12BPAconstraint, p12BPAmitigatingmeasure
        frame12 = tk.LabelFrame(mainProject)
        widgets_to_destroy = [frame12]

        p12Label = tk.Label(mainProject, text="Description of the Best/Optimal Policy Alternative", font=("Arial", 12, "bold"))
        spilloverLabel = tk.Label(frame12, text="Spillover")
        spillover = scrolledtext.ScrolledText(frame12, height=8, width=30)
        externalityLabel = tk.Label(frame12, text="Externalities")
        externality = scrolledtext.ScrolledText(frame12, height=8, width=30)
        constraintLabel = tk.Label(frame12, text="Constraints")
        constraint = scrolledtext.ScrolledText(frame12, height=8, width=30)
        mitiMeasureLabel = tk.Label(frame12, text="Mitigating Measures")
        mitiMeasure = scrolledtext.ScrolledText(frame12, height=8, width=30)
        status.place(relx=0.01, rely=0.9)

        p12Label.grid(row=0, column=0, columnspan=2, pady=10)
        spilloverLabel.grid(row=1, column=0, sticky="w", padx=7)
        spillover.grid(row=2, column=0, sticky="w", padx=7)
        externalityLabel.grid(row=1, column=1, sticky="w", padx=7)
        externality.grid(row=2, column=1, sticky="w", padx=7)
        constraintLabel.grid(row=3, column=0, sticky="w", padx=7)
        constraint.grid(row=4, column=0, sticky="w", padx=7)
        mitiMeasureLabel.grid(row=3, column=1, sticky="w", padx=7)
        mitiMeasure.grid(row=4, column=1, sticky="w", padx=7)

        def back_11():
            global pageNumber
            pageNumber -= 1
            for widget in mainProject.winfo_children():
                widget.destroy()
            page_11()

        def next_11():
            global pageNumber, p12BPAspillover, p12BPAexternality, p12BPAconstraint, p12BPAmitigatingmeasure
            p12BPAspillover = spillover.get("1.0", tk.END).strip()
            p12BPAexternality = externality.get("1.0", tk.END).strip()
            p12BPAconstraint = constraint.get("1.0", tk.END).strip()
            p12BPAmitigatingmeasure = mitiMeasure.get("1.0", tk.END).strip()
            if not p12BPAspillover:
                status.config(text="Enter spillover", foreground="red")
                return
            if not p12BPAexternality:
                status.config(text="Enter externality", foreground="red")
                return
            if not p12BPAconstraint:
                status.config(text="Enter constraint", foreground="red")
                return
            if not p12BPAmitigatingmeasure:
                status.config(text="Enter mitigating measure", foreground="red")
                return
            ##with open("page12_data.json", "w") as f:
            ##    json.dump({
            ##        "spillover": p12BPAspillover,
            ##        "externality": p12BPAexternality,
            ##        "constraint": p12BPAconstraint,
            ##        "mitigating_measure": p12BPAmitigatingmeasure
            ##    }, f)
            save()
            pageNumber += 1
            for widget in mainProject.winfo_children():
                widget.destroy()
            page_13()

        setup_page_common(12, "Best Policy Alternative Details", frame12, widgets_to_destroy, back_11, next_11)
        ##try:
        ##    with open("page12_data.json", "r") as f:
        ##        data = json.load(f)
        ##        spillover.insert("1.0", data.get("spillover", ""))
        ##        externality.insert("1.0", data.get("externality", ""))
        ##        constraint.insert("1.0", data.get("constraint", ""))
        ##        mitiMeasure.insert("1.0", data.get("mitigating_measure", ""))
        ##except FileNotFoundError:
        ##    pass

    p13BPAwhat = " "
    p13BPAwho = " "
    p13BPAhow = " "

    def page_13():
        global p13BPAwhat, p13BPAwho, p13BPAhow
        frame13 = tk.LabelFrame(mainProject)
        widgets_to_destroy = [frame13]

        p13Label = tk.Label(mainProject, text="Requirements for the Implementation of the Best/Optimal Policy Alternative", font=("Arial", 12, "bold"))
        p13whatLabel = tk.Label(frame13, text="What type of legislation is needed? Why?")
        p13what = scrolledtext.ScrolledText(frame13, height=8, width=30)
        p13whoLabel = tk.Label(frame13, text="Who will implement? Why?")
        p13who = scrolledtext.ScrolledText(frame13, height=8, width=30)
        p13howLabel = tk.Label(frame13, text="How much to implement and where to source funds?")
        p13how = scrolledtext.ScrolledText(frame13, height=8, width=30)
        status.place(relx=0.01, rely=0.9)

        p13Label.grid(row=0, column=0, columnspan=2, pady=10)
        p13whatLabel.grid(row=1, column=0, sticky="w", padx=7)
        p13what.grid(row=2, column=0, sticky="w", padx=7)
        p13whoLabel.grid(row=1, column=1, sticky="w", padx=7)
        p13who.grid(row=2, column=1, sticky="w", padx=7)
        p13howLabel.grid(row=3, column=0, sticky="w", padx=7)
        p13how.grid(row=4, column=0, sticky="w", padx=7)

        def back_12():
            global pageNumber
            pageNumber -= 1
            for widget in mainProject.winfo_children():
                widget.destroy()
            page_12()

        def next_12():
            global pageNumber, p13BPAwhat, p13BPAwho, p13BPAhow
            p13BPAwhat = p13what.get("1.0", tk.END).strip()
            p13BPAwho = p13who.get("1.0", tk.END).strip()
            p13BPAhow = p13how.get("1.0", tk.END).strip()
            if not p13BPAwhat:
                status.config(text="Enter the type of legislation needed", foreground="red")
                return
            if not p13BPAwho:
                status.config(text="Enter who will implement", foreground="red")
                return
            if not p13BPAhow:
                status.config(text="Enter how much to implement", foreground="red")
                return
            ##with open("page13_data.json", "w") as f:
            ##    json.dump({
            ##        "legislation": p13BPAwhat,
            ##        "implementers": p13BPAwho,
            ##        "funding": p13BPAhow
            ##    }, f)
            save()
            pageNumber += 1
            for widget in mainProject.winfo_children():
                widget.destroy()
            page_14()

        setup_page_common(13, "Implementation Requirements", frame13, widgets_to_destroy, back_12, next_12)
        ##try:
        ##    with open("page13_data.json", "r") as f:
        ##        data = json.load(f)
        ##        p13what.insert("1.0", data.get("legislation", ""))
        ##        p13who.insert("1.0", data.get("implementers", ""))
        ##        p13how.insert("1.0", data.get("funding", ""))
        ##except FileNotFoundError:
        ##    pass

    def page_14():
        frame14 = tk.LabelFrame(mainProject)
        widgets_to_destroy = [frame14]
        undo_stack = []

        implementationPlanLabel = tk.Label(frame14, text="Policy Implementation Plan", font=("Arial", 12, "bold"))
        implementationPlanTable = ttk.Treeview(frame14, selectmode="browse", height=3)
        implementationPlanTable["columns"] = ("1", "2", "3", "4", "5")
        implementationPlanTable['show'] = 'headings'
        implementationPlanTable.column("1", width=300, anchor='c')
        implementationPlanTable.column("2", width=250, anchor='c')
        implementationPlanTable.column("3", width=180, anchor='c')
        implementationPlanTable.column("4", width=140, anchor='c')
        implementationPlanTable.column("5", width=180, anchor='c')
        implementationPlanTable.heading("1", text="Critical Actions")
        implementationPlanTable.heading("2", text="Responsible/Accountable Units")
        implementationPlanTable.heading("3", text="Timeframes")
        implementationPlanTable.heading("4", text="Budgets")
        implementationPlanTable.heading("5", text="Budget Sources")
        sb_y = ttk.Scrollbar(frame14, orient="vertical", command=implementationPlanTable.yview)
        sb_x = ttk.Scrollbar(frame14, orient="horizontal", command=implementationPlanTable.xview)
        implementationPlanTable.configure(yscrollcommand=sb_y.set, xscrollcommand=sb_x.set)

        critALabel = tk.Label(mainProject, text="Critical Action")
        raUnitLabel = tk.Label(mainProject, text="Responsible/\nAccountable Unit")
        timeframeLabel = tk.Label(mainProject, text="Timeframe")
        budgetLabel = tk.Label(mainProject, text="Budget")
        budgSoLabel = tk.Label(mainProject, text="Budget Source")
        criticalAction = scrolledtext.ScrolledText(mainProject, height=4, width=30)
        respaccoUnit = scrolledtext.ScrolledText(mainProject, height=4, width=25)
        timeframe = scrolledtext.ScrolledText(mainProject, height=4, width=18)
        budget = scrolledtext.ScrolledText(mainProject, height=4, width=14)
        budgetSource = scrolledtext.ScrolledText(mainProject, height=4, width=17)
        addButton14 = ttk.Button(mainProject, text="Add", command=lambda: add_data14())
        editButton14 = ttk.Button(mainProject, text="Edit", state="disabled", command=lambda: edit_data14())
        deleteButton14 = ttk.Button(mainProject, text="Delete", state="disabled", command=lambda: delete_data14())
        ToolTip(addButton14, "Add a new entry to the table")
        ToolTip(editButton14, "Edit the selected table entry")
        ToolTip(deleteButton14, "Delete the selected table entry")

        implementationPlanLabel.grid(row=0, column=0, columnspan=2, pady=10)
        implementationPlanTable.grid(row=1, column=0)
        sb_y.grid(row=1, column=1, sticky="ns")
        sb_x.grid(row=2, column=0, sticky="ew")
        critALabel.place(relx=0.05, rely=0.5)
        criticalAction.place(relx=0.05, rely=0.55)
        raUnitLabel.place(relx=0.25, rely=0.5)
        respaccoUnit.place(relx=0.25, rely=0.55)
        timeframeLabel.place(relx=0.45, rely=0.5)
        timeframe.place(relx=0.45, rely=0.55)
        budgetLabel.place(relx=0.65, rely=0.5)
        budget.place(relx=0.65, rely=0.55)
        budgSoLabel.place(relx=0.85, rely=0.5)
        budgetSource.place(relx=0.85, rely=0.55)
        addButton14.place(relx=0.4, rely=0.85)
        editButton14.place(relx=0.5, rely=0.85)
        deleteButton14.place(relx=0.6, rely=0.85)

        def show_data14(a):
            criticalAction.delete("1.0", tk.END)
            respaccoUnit.delete("1.0", tk.END)
            timeframe.delete("1.0", tk.END)
            budget.delete("1.0", tk.END)
            budgetSource.delete("1.0", tk.END)
            selected_item = implementationPlanTable.selection()
            if selected_item:
                editButton14.config(state="normal")
                deleteButton14.config(state="normal")
                values = implementationPlanTable.item(selected_item[0])['values']
                criticalAction.insert("1.0", values[0])
                respaccoUnit.insert("1.0", values[1])
                timeframe.insert("1.0", values[2])
                budget.insert("1.0", values[3])
                budgetSource.insert("1.0", values[4])
            else:
                editButton14.config(state="disabled")
                deleteButton14.config(state="disabled")

        def add_data14():
            texts = [
                criticalAction.get("1.0", tk.END).strip(),
                respaccoUnit.get("1.0", tk.END).strip(),
                timeframe.get("1.0", tk.END).strip(),
                budget.get("1.0", tk.END).strip(),
                budgetSource.get("1.0", tk.END).strip()
            ]
            if not all(texts):
                messagebox.showerror("Error", "Please fill out all fields")
                return
            item_id = implementationPlanTable.insert("", 'end', values=texts)
            undo_stack.append(("add", item_id))
            criticalAction.delete("1.0", tk.END)
            respaccoUnit.delete("1.0", tk.END)
            timeframe.delete("1.0", tk.END)
            budget.delete("1.0", tk.END)
            budgetSource.delete("1.0", tk.END)
            criticalAction.focus()

        def edit_data14():
            texts = [
                criticalAction.get("1.0", tk.END).strip(),
                respaccoUnit.get("1.0", tk.END).strip(),
                timeframe.get("1.0", tk.END).strip(),
                budget.get("1.0", tk.END).strip(),
                budgetSource.get("1.0", tk.END).strip()
            ]
            if not all(texts):
                messagebox.showerror("Error", "Please fill out all fields")
                return
            selected_item = implementationPlanTable.selection()[0]
            old_values = implementationPlanTable.item(selected_item)['values']
            undo_stack.append(("edit", selected_item, old_values))
            implementationPlanTable.item(selected_item, values=texts)

        def delete_data14():
            selected_item = implementationPlanTable.selection()
            if selected_item:
                item_id = selected_item[0]
                old_values = implementationPlanTable.item(item_id)['values']
                undo_stack.append(("delete", item_id, old_values))
                implementationPlanTable.delete(item_id)
                criticalAction.delete("1.0", tk.END)
                respaccoUnit.delete("1.0", tk.END)
                timeframe.delete("1.0", tk.END)
                budget.delete("1.0", tk.END)
                budgetSource.delete("1.0", tk.END)
                editButton14.config(state="disabled")
                deleteButton14.config(state="disabled")
            else:
                messagebox.showwarning("Warning", "Please select an item to delete")

        def undo():
            if not undo_stack:
                return
            action, *data = undo_stack.pop()
            if action == "add":
                implementationPlanTable.delete(data[0])
            elif action == "edit":
                item_id, old_values = data
                implementationPlanTable.item(item_id, values=old_values)
            elif action == "delete":
                item_id, old_values = data
                implementationPlanTable.insert("", "end", iid=item_id, values=old_values)

        implementationPlanTable.bind("<<TreeviewSelect>>", show_data14)
        mainProject.bind("<Control-z>", lambda e: undo())
        mainProject.bind("<Control-Return>", lambda e: add_data14())
        criticalAction.bind("<Tab>", lambda e: respaccoUnit.focus_set())
        respaccoUnit.bind("<Tab>", lambda e: timeframe.focus_set())
        timeframe.bind("<Tab>", lambda e: budget.focus_set())
        budget.bind("<Tab>", lambda e: budgetSource.focus_set())
        budgetSource.bind("<Tab>", lambda e: addButton14.focus_set())

        def back_13():
            global pageNumber
            pageNumber -= 1
            for widget in mainProject.winfo_children():
                widget.destroy()
            page_13()

        def next_13():
            global pageNumber
            ##with open("page14_data.json", "w") as f:
            ##    json.dump({"plan": [implementationPlanTable.item(i)['values'] for i in implementationPlanTable.get_children()]}, f)
            pageNumber += 1
            for widget in mainProject.winfo_children():
                widget.destroy()
            page_15()

        setup_page_common(14, "Policy Implementation Plan", frame14, widgets_to_destroy, back_13, next_13)
        ##try:
        ##    with open("page14_data.json", "r") as f:
        ##        data = json.load(f)
        ##        for item in data.get("plan", []):
        ##            implementationPlanTable.insert("", "end", values=item)
        ##except FileNotFoundError:
        ##    pass

    def page_15():
        frame15 = tk.LabelFrame(mainProject)
        widgets_to_destroy = [frame15]
        undo_stack = []

        policyAssessmentLabel = tk.Label(frame15, text="Policy Assessment: Monitoring and Evaluation Plan", font=("Arial", 12, "bold"))
        policyAssessmentTable = ttk.Treeview(frame15, selectmode="browse", height=3)
        policyAssessmentTable["columns"] = ("1", "2", "3", "4", "5", "6", "7")
        policyAssessmentTable['show'] = 'headings'
        policyAssessmentTable.column("1", width=214, anchor='c')
        policyAssessmentTable.column("2", width=214, anchor='c')
        policyAssessmentTable.column("3", width=214, anchor='c')
        policyAssessmentTable.column("4", width=214, anchor='c')
        policyAssessmentTable.column("5", width=214, anchor='c')
        policyAssessmentTable.column("6", width=214, anchor='c')
        policyAssessmentTable.column("7", width=214, anchor='c')
        policyAssessmentTable.heading("1", text="Goals and Objectives")
        policyAssessmentTable.heading("2", text="SMART Indicators")
        policyAssessmentTable.heading("3", text="Sources of Data")
        policyAssessmentTable.heading("4", text="Data Collection Frequencies")
        policyAssessmentTable.heading("5", text="Unit-In-Charge of Data\nCollection and Analysis")
        policyAssessmentTable.heading("6", text="Outputs of M&E")
        policyAssessmentTable.heading("7", text="M&E Report Users")
        sb_y = ttk.Scrollbar(frame15, orient="vertical", command=policyAssessmentTable.yview)
        sb_x = ttk.Scrollbar(frame15, orient="horizontal", command=policyAssessmentTable.xview)
        policyAssessmentTable.configure(yscrollcommand=sb_y.set, xscrollcommand=sb_x.set)

        goalAndObjectiveLabel = tk.Label(mainProject, text="Goal and Objective")
        smartIndicatorLabel = tk.Label(mainProject, text="SMART Indicator")
        sourceofDataLabel = tk.Label(mainProject, text="Source of Data")
        dcfLabel = tk.Label(mainProject, text="Data Collection Frequency")
        uicLabel = tk.Label(mainProject, text="Unit-In-Charge of Data\nCollection and Analysis")
        MEoutputLabel = tk.Label(mainProject, text="Output of M&E")
        MEuserLabel = tk.Label(mainProject, text="M&E Report User")
        goalAndObjective = scrolledtext.ScrolledText(mainProject, height=4, width=22)
        smartIndicator = scrolledtext.ScrolledText(mainProject, height=4, width=22)
        sourceofData = scrolledtext.ScrolledText(mainProject, height=4, width=22)
        dcf = scrolledtext.ScrolledText(mainProject, height=4, width=22)
        uic = scrolledtext.ScrolledText(mainProject, height=4, width=22)
        MEoutput = scrolledtext.ScrolledText(mainProject, height=4, width=22)
        MEuser = scrolledtext.ScrolledText(mainProject, height=4, width=22)
        addButton15 = ttk.Button(mainProject, text="Add", command=lambda: add_data15())
        editButton15 = ttk.Button(mainProject, text="Edit", state="disabled", command=lambda: edit_data15())
        deleteButton15 = ttk.Button(mainProject, text="Delete", state="disabled", command=lambda: delete_data15())
        ToolTip(addButton15, "Add a new entry to the table")
        ToolTip(editButton15, "Edit the selected table entry")
        ToolTip(deleteButton15, "Delete the selected table entry")

        policyAssessmentLabel.grid(row=0, column=0, columnspan=2, pady=10)
        policyAssessmentTable.grid(row=1, column=0)
        sb_y.grid(row=1, column=1, sticky="ns")
        sb_x.grid(row=2, column=0, sticky="ew")
        goalAndObjectiveLabel.place(relx=0.05, rely=0.5)
        goalAndObjective.place(relx=0.05, rely=0.55)
        smartIndicatorLabel.place(relx=0.20, rely=0.5)
        smartIndicator.place(relx=0.20, rely=0.55)
        sourceofDataLabel.place(relx=0.35, rely=0.5)
        sourceofData.place(relx=0.35, rely=0.55)
        dcfLabel.place(relx=0.50, rely=0.5)
        dcf.place(relx=0.50, rely=0.55)
        uicLabel.place(relx=0.65, rely=0.5)
        uic.place(relx=0.65, rely=0.55)
        MEoutputLabel.place(relx=0.80, rely=0.5)
        MEoutput.place(relx=0.80, rely=0.55)
        MEuserLabel.place(relx=0.95, rely=0.5)
        MEuser.place(relx=0.95, rely=0.55)
        addButton15.place(relx=0.4, rely=0.85)
        editButton15.place(relx=0.5, rely=0.85)
        deleteButton15.place(relx=0.6, rely=0.85)

        for i, (goal, indicator) in enumerate(zip(p7policyGoalsandObjectives, p7indicators)):
            policyAssessmentTable.insert("", 'end', values=(goal, indicator, "", "", "", "", ""))

        def show_data15(a):
            goalAndObjective.delete("1.0", tk.END)
            smartIndicator.delete("1.0", tk.END)
            sourceofData.delete("1.0", tk.END)
            dcf.delete("1.0", tk.END)
            uic.delete("1.0", tk.END)
            MEoutput.delete("1.0", tk.END)
            MEuser.delete("1.0", tk.END)
            selected_item = policyAssessmentTable.selection()
            if selected_item:
                editButton15.config(state="normal")
                deleteButton15.config(state="normal")
                values = policyAssessmentTable.item(selected_item[0])['values']
                goalAndObjective.insert("1.0", values[0])
                smartIndicator.insert("1.0", values[1])
                sourceofData.insert("1.0", values[2])
                dcf.insert("1.0", values[3])
                uic.insert("1.0", values[4])
                MEoutput.insert("1.0", values[5])
                MEuser.insert("1.0", values[6])
            else:
                editButton15.config(state="disabled")
                deleteButton15.config(state="disabled")

        def add_data15():
            texts = [
                goalAndObjective.get("1.0", tk.END).strip(),
                smartIndicator.get("1.0", tk.END).strip(),
                sourceofData.get("1.0", tk.END).strip(),
                dcf.get("1.0", tk.END).strip(),
                uic.get("1.0", tk.END).strip(),
                MEoutput.get("1.0", tk.END).strip(),
                MEuser.get("1.0", tk.END).strip()
            ]
            if not all(texts):
                messagebox.showerror("Error", "Please fill out all fields")
                return
            item_id = policyAssessmentTable.insert("", 'end', values=texts)
            undo_stack.append(("add", item_id))
            goalAndObjective.delete("1.0", tk.END)
            smartIndicator.delete("1.0", tk.END)
            sourceofData.delete("1.0", tk.END)
            dcf.delete("1.0", tk.END)
            uic.delete("1.0", tk.END)
            MEoutput.delete("1.0", tk.END)
            MEuser.delete("1.0", tk.END)
            goalAndObjective.focus()

        def edit_data15():
            texts = [
                goalAndObjective.get("1.0", tk.END).strip(),
                smartIndicator.get("1.0", tk.END).strip(),
                sourceofData.get("1.0", tk.END).strip(),
                dcf.get("1.0", tk.END).strip(),
                uic.get("1.0", tk.END).strip(),
                MEoutput.get("1.0", tk.END).strip(),
                MEuser.get("1.0", tk.END).strip()
            ]
            if not all(texts):
                messagebox.showerror("Error", "Please fill out all fields")
                return
            selected_item = policyAssessmentTable.selection()[0]
            old_values = policyAssessmentTable.item(selected_item)['values']
            undo_stack.append(("edit", selected_item, old_values))
            policyAssessmentTable.item(selected_item, values=texts)

        def delete_data15():
            selected_item = policyAssessmentTable.selection()
            if selected_item:
                item_id = selected_item[0]
                old_values = policyAssessmentTable.item(item_id)['values']
                undo_stack.append(("delete", item_id, old_values))
                policyAssessmentTable.delete(item_id)
                goalAndObjective.delete("1.0", tk.END)
                smartIndicator.delete("1.0", tk.END)
                sourceofData.delete("1.0", tk.END)
                dcf.delete("1.0", tk.END)
                uic.delete("1.0", tk.END)
                MEoutput.delete("1.0", tk.END)
                MEuser.delete("1.0", tk.END)
                editButton15.config(state="disabled")
                deleteButton15.config(state="disabled")
            else:
                messagebox.showwarning("Warning", "Please select an item to delete")

        def undo():
            if not undo_stack:
                return
            action, *data = undo_stack.pop()
            if action == "add":
                policyAssessmentTable.delete(data[0])
            elif action == "edit":
                item_id, old_values = data
                policyAssessmentTable.item(item_id, values=old_values)
            elif action == "delete":
                item_id, old_values = data
                policyAssessmentTable.insert("", "end", iid=item_id, values=old_values)

        policyAssessmentTable.bind("<<TreeviewSelect>>", show_data15)
        mainProject.bind("<Control-z>", lambda e: undo())
        mainProject.bind("<Control-Return>", lambda e: add_data15())
        goalAndObjective.bind("<Tab>", lambda e: smartIndicator.focus_set())
        smartIndicator.bind("<Tab>", lambda e: sourceofData.focus_set())
        sourceofData.bind("<Tab>", lambda e: dcf.focus_set())
        dcf.bind("<Tab>", lambda e: uic.focus_set())
        uic.bind("<Tab>", lambda e: MEoutput.focus_set())
        MEoutput.bind("<Tab>", lambda e: MEuser.focus_set())
        MEuser.bind("<Tab>", lambda e: addButton15.focus_set())

        def back_14():
            global pageNumber
            pageNumber -= 1
            for widget in mainProject.winfo_children():
                widget.destroy()
            page_14()

        def next_14():
            global pageNumber
        ##    with open("page15_data.json", "w") as f:
        ##        json.dump({"assessment": [policyAssessmentTable.item(i)['values'] for i in policyAssessmentTable.get_children()]}, f)
            save()
            pageNumber += 1
            for widget in mainProject.winfo_children():
                widget.destroy()
            messagebox.showinfo("Completion", "Policy analysis completed! You can start a new project or open an existing one from the File menu.")
            new_project()  # Reset to page_1 or home page

        setup_page_common(15, "Monitoring and Evaluation Plan", frame15, widgets_to_destroy, back_14, next_14)
        try:
            with open("page15_data.json", "r") as f:
                data = json.load(f)
                for item in data.get("assessment", []):
                    policyAssessmentTable.insert("", "end", values=item)
        except FileNotFoundError:
            for i, (goal, indicator) in enumerate(zip(p7policyGoalsandObjectives, p7indicators)):
                policyAssessmentTable.insert("", 'end', values=(goal, indicator, "", "", "", "", ""))

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

root.config(menu=menubar)

root.mainloop()