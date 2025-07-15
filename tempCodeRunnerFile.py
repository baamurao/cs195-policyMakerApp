    global pageNumber
    pageNumber = 1
    for widget in mainProject.winfo_children():
        widget.destroy()