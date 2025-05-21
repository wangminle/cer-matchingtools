Okay, let's analyze the frontend UI elements and their attributes in the `src/main.py` file.

This file uses `tkinter` to build a graphical user interface. It mainly includes the following elements:

**Main Window (`root`)**

*   **Type:** `tk.Tk`
*   **Title:** "ASR Character Accuracy Comparison Tool"
*   **Initial Size:** 800x600
*   **Resizable:** Allows horizontal and vertical resizing (`resizable(True, True)`)
*   **Minimum Size:** 800x600 (`minsize(800, 600)`)

**Main Frames**

1.  **`top_frame` (Upper part frame)**
    *   **Type:** `ttk.Frame`
    *   **Parent:** `root`
    *   **Layout:** `pack(fill=tk.BOTH, expand=False, padx=10, pady=5)` (Fills available space, does not expand with window, internal/external padding)
2.  **`bottom_frame` (Lower part frame)**
    *   **Type:** `ttk.Frame`
    *   **Parent:** `root`
    *   **Layout:** `pack(fill=tk.BOTH, expand=True, padx=10, pady=5)` (Fills entire available space, expands with window, internal/external padding)

**Elements within the Upper Part (`top_frame`)**

1.  **`file_area_frame` (File area frame)**
    *   **Type:** `ttk.Frame`
    *   **Parent:** `top_frame`
    *   **Layout:** `pack(fill=tk.BOTH, expand=True, padx=5, pady=5)`
    *   **Column Configuration:** Uses a grid system, two columns of equal width `columnconfigure(0, weight=1, uniform="group1")` and `columnconfigure(1, weight=1, uniform="group1")`
2.  **`left_frame` (Left frame - ASR files)**
    *   **Type:** `ttk.LabelFrame`
    *   **Parent:** `file_area_frame`
    *   **Text Label:** "ASR Transcription Result Files"
    *   **Layout:** `grid(row=0, column=0, sticky="nsew", padx=5, pady=5)` (Grid layout ensures equal width for left and right)
3.  **`right_frame` (Right frame - Annotation files)**
    *   **Type:** `ttk.LabelFrame`
    *   **Parent:** `file_area_frame`
    *   **Text Label:** "Annotation Files"
    *   **Layout:** `grid(row=0, column=1, sticky="nsew", padx=5, pady=5)` (Grid layout ensures equal width for left and right)
4.  **`asr_btn` (Select ASR Files button)**
    *   **Type:** `ttk.Button`
    *   **Parent:** `left_frame`
    *   **Text:** "Select ASR Files"
    *   **Command:** `self.select_asr_files`
    *   **Layout:** `pack(pady=5)` (Vertical internal padding)
5.  **`asr_canvas_frame` (ASR file list Canvas container frame)**
    *   **Type:** `ttk.Frame`
    *   **Parent:** `left_frame`
    *   **Layout:** `pack(fill=tk.BOTH, expand=True, padx=5, pady=5)`
6.  **`asr_canvas` (ASR file list display area)**
    *   **Type:** `tk.Canvas`
    *   **Parent:** `asr_canvas_frame`
    *   **Background Color:** "white"
    *   **Height:** 160 (Adjusted from 120 to 160)
    *   **Width:** 350 (Fixed width to ensure consistency on both sides)
    *   **Layout:** `pack(fill=tk.BOTH, expand=True)`
    *   **Event Bindings:**
        *   `<ButtonPress-1>`: `self.on_press`
        *   `<B1-Motion>`: `self.on_drag`
        *   `<ButtonRelease-1>`: `self.on_release`
7.  **`ref_btn` (Select Annotation Files button)**
    *   **Type:** `ttk.Button`
    *   **Parent:** `right_frame`
    *   **Text:** "Select Annotation Files"
    *   **Command:** `self.select_ref_files`
    *   **Layout:** `pack(pady=5)`
8.  **`ref_canvas_frame` (Annotation file list Canvas container frame)**
    *   **Type:** `ttk.Frame`
    *   **Parent:** `right_frame`
    *   **Layout:** `pack(fill=tk.BOTH, expand=True, padx=5, pady=5)`
9.  **`ref_canvas` (Annotation file list display area)**
    *   **Type:** `tk.Canvas`
    *   **Parent:** `ref_canvas_frame`
    *   **Background Color:** "white"
    *   **Height:** 160 (Adjusted from 120 to 160)
    *   **Width:** 350 (Fixed width to ensure consistency on both sides)
    *   **Layout:** `pack(fill=tk.BOTH, expand=True)`
    *   **Event Bindings:**
        *   `<ButtonPress-1>`: `self.on_press`
        *   `<B1-Motion>`: `self.on_drag`
        *   `<ButtonRelease-1>`: `self.on_release`
10. **`control_frame` (Control frame, includes button and filter option)**
    *   **Type:** `ttk.Frame`
    *   **Parent:** `top_frame`
    *   **Layout:** `pack(fill=tk.X, pady=5)`
11. **`btn_container` (Statistics button container frame)**
    *   **Type:** `ttk.Frame`
    *   **Parent:** `control_frame`
    *   **Layout:** `pack(side=tk.TOP, fill=tk.X)`
12. **`calculate_btn` (Start Calculation button)**
    *   **Type:** `ttk.Button`
    *   **Parent:** `btn_container`
    *   **Text:** "Start Calculation"
    *   **Command:** `self.calculate_accuracy`
    *   **Width:** 15
    *   **Layout:** `pack(side=tk.TOP, pady=5)` (Center aligned)
13. **`filter_frame` (Filler word filter frame)**
    *   **Type:** `ttk.Frame`
    *   **Parent:** `control_frame`
    *   **Layout:** `place(relx=1.0, rely=0.5, anchor=tk.E, x=-20)` (Absolute positioning on the right, vertically centered, on the same horizontal line as the "Start Calculation" button)
14. **`filter_check` (Filler word filter checkbox)**
    *   **Type:** `ttk.Checkbutton`
    *   **Parent:** `filter_frame`
    *   **Text:** "Filter Filler Words"
    *   **Variable:** `self.filter_fillers` (BooleanVar)
    *   **Layout:** `pack(side=tk.LEFT)`
15. **Filler word filter hint label**
    *   **Type:** `tk.Label`
    *   **Parent:** `filter_frame`
    *   **Text:** "?"
    *   **Font:** ("Arial", 9, "bold")
    *   **Color:** "blue"
    *   **Layout:** `pack(side=tk.LEFT, padx=3)`
    *   **Event Binding:** `<Enter>` to show tooltip

**Elements within the Lower Part (`bottom_frame`)**

1.  **`result_frame` (Result display frame)**
    *   **Type:** `ttk.LabelFrame`
    *   **Parent:** `bottom_frame`
    *   **Text Label:** "Character Accuracy Statistics Results"
    *   **Layout:** `pack(fill=tk.BOTH, expand=True, padx=5, pady=5)`
2.  **`result_tree_frame` (Result table Treeview container frame)**
    *   **Type:** `ttk.Frame`
    *   **Parent:** `result_frame`
    *   **Layout:** `pack(fill=tk.BOTH, expand=True, padx=5, pady=5)`
3.  **`result_tree` (Result display table)**
    *   **Type:** `ttk.Treeview`
    *   **Parent:** `result_tree_frame`
    *   **Columns:** ("Original File", "Annotation File", "ASR Char Count", "Ref Char Count", "Char Accuracy", "Filter Filler Words")
    *   **Display Mode:** "headings" (Only show headers, not index column)
    *   **Height (rows):** 8 (Reduced from 12 rows to 8 rows)
    *   **Layout:** `pack(fill=tk.BOTH, expand=True)`
    *   **Column Attributes (set in a loop):**
        *   `heading(col, text=col)` (Set header text for each column)
        *   `column(col, width=120, anchor="center")` (Set column width to 120, content centered)
4.  **`export_frame` (Export button container frame)**
    *   **Type:** `ttk.Frame`
    *   **Parent:** `bottom_frame`
    *   **Layout:** `pack(fill=tk.X, pady=10)`
5.  **`export_btn` (Export Results button)**
    *   **Type:** `ttk.Button`
    *   **Parent:** `export_frame`
    *   **Text:** "Export Results"
    *   **Command:** `self.export_results`
    *   **Width:** 15
    *   **Layout:** `pack(side=tk.TOP, pady=0)` (Center aligned)

**Dynamically Created Elements inside Canvas** (created by `update_canvas_items` function)

*   **File Rectangle:**
    *   **Type:** `canvas.create_rectangle`
    *   **Coordinates:** `(10, y_pos, 10 + item_width, y_pos+30)` (Fixed width ensures consistency on both sides)
    *   **Fill Color:** "lightblue"
    *   **Tags:** `f"file_{i}"` and file path `file_path` (For identification and association)
*   **File Name Text:**
    *   **Type:** `canvas.create_text`
    *   **Coordinates:** `(20, y_pos+15)`
    *   **Text:** `file_name` (Extracted from file path)
    *   **Anchor:** "w" (West, i.e., left-aligned)
    *   **Tags:** `f"file_{i}"` (Associated with the corresponding rectangle)

**Tooltip Feature**

* **Tooltip Window:**
  * **Type:** `tk.Toplevel`
  * **Borderless:** `wm_overrideredirect(True)`
  * **Position:** Dynamically calculated based on mouse position
  * **Content:** Explanation of the filler word filtering function
  * **Boundary Detection:** Uses a 30x30 pixel virtual bounding box to determine mouse position

**UI Layout Change Summary**

1. File display area height increased from 120 pixels to 160 pixels
2. Grid layout used to ensure the two file areas (left and right) have exactly the same width
3. Canvas set to a fixed width of 350 pixels to resolve width inconsistency issues
4. Result tree view height reduced from 12 rows to 8 rows
5. "Start Calculation" and "Export Results" buttons are center-aligned
6. "Filter Filler Words" checkbox uses `place` layout, vertically centered with the "Start Calculation" button

This list covers all major UI components defined in `src/main.py` and their key attributes and layout information. Elements inside the Canvas are dynamically generated to display the file list and support drag-and-drop sorting. The layout has been optimized to resolve width inconsistency issues and center buttons, improving the user experience. 