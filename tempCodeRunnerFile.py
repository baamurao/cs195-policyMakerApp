            elif(int(var.get()) == 4):
                analysis = Toplevel(main)
                analysis.title("Analysis - Problem Tree Analysis")
                analysis.geometry("830x480")

                # Ensure it's in front
                analysis.transient(root)
                analysis.grab_set()
                analysis.lift()
                analysis.focus_force()
                analysis.attributes("-topmost", 1)
                analysis.after(10, lambda: analysis.attributes("-topmost", 0))

                class ShapeEditorApp:
                    def __init__(self, root):
                        global textValue
                        textValue = StringVar()
                        italic_font = font.Font(family="Arial", size=10, slant="italic")

                        self.root = root
                        self.root.title("Problem Tree Analysis")

                        # Create Canvas widget with scrollbars
                        self.canvas_frame = tk.Frame(root)
                        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
                        
                        self.scroll_x = tk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL)
                        self.scroll_y = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL)
                        self.canvas = tk.Canvas(self.canvas_frame, bg="white", 
                                            xscrollcommand=self.scroll_x.set, 
                                            yscrollcommand=self.scroll_y.set)
                        self.scroll_x.config(command=self.canvas.xview)
                        self.scroll_y.config(command=self.canvas.yview)
                        self.scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
                        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
                        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

                        # Initialize variables
                        self.current_shape = None
                        self.start_x = None
                        self.start_y = None
                        self.current_shape_item = None
                        self.pen_active = False
                        self.eraser_active = False
                        self.color = "black"
                        self.undo_stack = []
                        self.redo_stack = []
                        self.zoom_level = 1.0
                        self.max_undo = 50  # Limit to prevent excessive memory use

                        # Create buttons
                        self.color_button = tk.Button(root, text="Color", command=self.choose_color)
                        self.pen_button = tk.Button(root, text='Pen', command=self.use_pen)
                        self.eraser_button = tk.Button(root, text="Eraser", command=self.use_eraser)
                        self.rect_button = tk.Button(root, text="Rectangle", command=self.create_rectangle)
                        self.circle_button = tk.Button(root, text="Arrow", command=self.create_arrow)
                        self.clear_button = tk.Button(root, text="Clear", command=self.clear_canvas)
                        self.undo_button = tk.Button(root, text="Undo", command=self.undo)
                        self.redo_button = tk.Button(root, text="Redo", command=self.redo)
                        self.zoom_in_button = tk.Button(root, text="Zoom In", command=self.zoom_in)
                        self.zoom_out_button = tk.Button(root, text="Zoom Out", command=self.zoom_out)
                        self.save_button = tk.Button(root, text="Save", command=self.save_canvas)
                        self.text_frame = tk.Frame(root, height=100, width=200, relief=tk.SUNKEN, borderwidth=3)
                        self.text_entry = tk.Entry(self.text_frame, textvariable=textValue, bg="white", width=20)
                        self.text_note = tk.Label(root, text="* Right click on canvas to paste text", font=italic_font, fg="gray")
                        
                        # Pack buttons
                        self.pen_button.pack(side=tk.LEFT)
                        self.eraser_button.pack(side=tk.LEFT)
                        self.clear_button.pack(side=tk.LEFT)
                        self.color_button.pack(side=tk.LEFT)
                        self.rect_button.pack(side=tk.LEFT)
                        self.circle_button.pack(side=tk.LEFT)
                        self.undo_button.pack(side=tk.LEFT)
                        self.redo_button.pack(side=tk.LEFT)
                        self.zoom_in_button.pack(side=tk.LEFT)
                        self.zoom_out_button.pack(side=tk.LEFT)
                        self.save_button.pack(side=tk.LEFT)
                        self.text_frame.pack(side=tk.LEFT)                         
                        self.text_entry.pack(side=tk.LEFT)
                        self.text_note.pack(side=tk.LEFT)

                        # Bind mouse events
                        self.canvas.bind("<Button-1>", self.start_draw)
                        self.canvas.bind("<B1-Motion>", self.draw_shape)
                        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)
                        self.canvas.bind("<Button-2>", self.add_text)
                        self.canvas.bind("<Button-3>", self.add_text)
                        self.canvas.bind("<MouseWheel>", self.zoom)

                        # Initial scroll region
                        self.canvas.config(scrollregion=(0, 0, 1000, 1000))  # Large initial region

                    def add_text(self, event):
                        item = self.canvas.create_text(event.x, event.y, text=textValue.get() or "", fill=self.color)
                        self.save_state()
                        self.redo_stack.clear()
                        print(f"Added text, undo_stack size: {len(self.undo_stack)}")

                    def use_pen(self):
                        self.pen_active = True
                        self.eraser_active = False
                        self.current_shape = None

                    def use_eraser(self):
                        self.pen_active = False
                        self.eraser_active = True
                        self.current_shape = None

                    def choose_color(self):
                        color_tuple = colorchooser.askcolor(title="Choose color")
                        if color_tuple[1]:
                            self.color = color_tuple[1]

                    def create_rectangle(self):
                        self.pen_active = False
                        self.eraser_active = False
                        self.current_shape = "rectangle"

                    def create_arrow(self):
                        self.pen_active = False
                        self.eraser_active = False
                        self.current_shape = "arrow"

                    def start_draw(self, event):
                        self.start_x = event.x
                        self.start_y = event.y
                        if self.pen_active or self.eraser_active:
                            return
                        if self.current_shape == "rectangle":
                            self.current_shape_item = self.canvas.create_rectangle(
                                self.start_x, self.start_y, self.start_x, self.start_y, outline=self.color
                            )
                        elif self.current_shape == "arrow":
                            self.current_shape_item = self.canvas.create_line(
                                self.start_x, self.start_y, self.start_x, self.start_y, fill=self.color, arrow="last", width=5
                            )

                    def draw_shape(self, event):
                        if self.pen_active or self.eraser_active:
                            item = self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, 
                                                        fill=self.color if self.pen_active else "white", 
                                                        width=2 if self.pen_active else 10)
                            self.save_state_for_stroke(item)  # Save state for each stroke
                            self.redo_stack.clear()
                            self.start_x, self.start_y = event.x, event.y
                        elif self.current_shape_item:
                            x, y = event.x, event.y
                            self.canvas.coords(self.current_shape_item, self.start_x, self.start_y, x, y)

                    def stop_draw(self, event):
                        if self.current_shape_item or self.pen_active or self.eraser_active:
                            self.save_state()  # Save final state for non-pen/eraser actions
                            self.redo_stack.clear()
                            print(f"Stopped draw, undo_stack size: {len(self.undo_stack)}")
                        self.current_shape_item = None
                        self.pen_active = False
                        self.eraser_active = False

                    def clear_canvas(self):
                        self.save_state()
                        self.canvas.delete("all")
                        self.redo_stack.clear()
                        self.update_scroll_region()
                        print(f"Cleared canvas, undo_stack size: {len(self.undo_stack)}")

                    def save_state(self):
                        items = []
                        for item in self.canvas.find_all():
                            item_type = self.canvas.type(item)
                            coords = self.canvas.coords(item)
                            config = {k: v[-1] for k, v in self.canvas.itemconfig(item).items() if k in ["fill", "outline", "text", "width", "arrow"]}
                            if item_type == "line":
                                items.append(("line", coords, {"fill": config.get("fill", "black"), "width": config.get("width", 2), "arrow": config.get("arrow", "none")}))
                            elif item_type == "rectangle":
                                items.append(("rectangle", coords, {"outline": config.get("outline", "black")}))
                            elif item_type == "text":
                                items.append(("text", coords, {"text": config.get("text", ""), "fill": config.get("fill", "black")}))
                        if items:
                            if len(self.undo_stack) >= self.max_undo:
                                self.undo_stack.pop(0)  # Remove oldest state if limit reached
                            self.undo_stack.append(items)
                        self.update_scroll_region()

                    def save_state_for_stroke(self, item):
                        item_type = self.canvas.type(item)
                        coords = self.canvas.coords(item)
                        config = {k: v[-1] for k, v in self.canvas.itemconfig(item).items() if k in ["fill", "width"]}
                        if item_type == "line" and len(self.undo_stack) < self.max_undo:
                            self.undo_stack.append([("line", coords, {"fill": config.get("fill", "black"), "width": config.get("width", 2)})])
                        self.update_scroll_region()

                    def undo(self):
                        if self.undo_stack:
                            state = self.undo_stack.pop()
                            self.redo_stack.append([(self.canvas.type(item), self.canvas.coords(item), {k: v[-1] for k, v in self.canvas.itemconfig(item).items() if k in ["fill", "outline", "text", "width", "arrow"]}) for item in self.canvas.find_all()])
                            self.canvas.delete("all")
                            for item_type, coords, config in state:
                                if item_type == "line":
                                    self.canvas.create_line(*coords, fill=config["fill"], width=config.get("width", 2), arrow=config.get("arrow", "none"))
                                elif item_type == "rectangle":
                                    self.canvas.create_rectangle(*coords, outline=config["outline"])
                                elif item_type == "text":
                                    self.canvas.create_text(coords[0], coords[1], text=config["text"], fill=config["fill"])
                            self.update_scroll_region()
                            print(f"Undo performed, undo_stack size: {len(self.undo_stack)}, redo_stack size: {len(self.redo_stack)}")

                    def redo(self):
                        if self.redo_stack:
                            state = self.redo_stack.pop()
                            self.undo_stack.append([(self.canvas.type(item), self.canvas.coords(item), {k: v[-1] for k, v in self.canvas.itemconfig(item).items() if k in ["fill", "outline", "text", "width", "arrow"]}) for item in self.canvas.find_all()])
                            self.canvas.delete("all")
                            for item_type, coords, config in state:
                                if item_type == "line":
                                    self.canvas.create_line(*coords, fill=config["fill"], width=config.get("width", 2), arrow=config.get("arrow", "none"))
                                elif item_type == "rectangle":
                                    self.canvas.create_rectangle(*coords, outline=config["outline"])
                                elif item_type == "text":
                                    self.canvas.create_text(coords[0], coords[1], text=config["text"], fill=config["fill"])
                            self.update_scroll_region()
                            print(f"Redo performed, undo_stack size: {len(self.undo_stack)}, redo_stack size: {len(self.redo_stack)}")

                    def zoom_in(self):
                        self.zoom_level *= 1.2
                        self.canvas.scale("all", self.canvas.canvasx(0), self.canvas.canvasy(0), 1.2, 1.2)
                        self.update_scroll_region()

                    def zoom_out(self):
                        self.zoom_level /= 1.2
                        if self.zoom_level > 0.1:
                            self.canvas.scale("all", self.canvas.canvasx(0), self.canvas.canvasy(0), 1/1.2, 1/1.2)
                            self.update_scroll_region()

                    def zoom(self, event):
                        if event.delta > 0:
                            self.zoom_in()
                        else:
                            self.zoom_out()

                    def save_canvas(self):
                        self.canvas.postscript(file="temp.ps", colormode="color")
                        from PIL import Image
                        img = Image.open("temp.ps")
                        img.save("image.png", "PNG")
                        os.remove("temp.ps")
                        messagebox.showinfo("Success", "Canvas saved as image.png")

                    def update_scroll_region(self):
                        region = self.canvas.bbox("all")
                        if region:
                            self.canvas.config(scrollregion=region)
                        else:
                            self.canvas.config(scrollregion=(0, 0, 1000, 1000))

                app = ShapeEditorApp(analysis)