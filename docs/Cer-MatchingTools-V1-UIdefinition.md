Okay, let's analyze the frontend UI elements and their attributes in the `src/main_with_tokenizers.py` new version file.

This file uses `tkinter` to build a graphical user interface with multi-tokenizer switching support. It mainly includes the following elements:

**Main Window (`root`)**

*   **Type:** `tk.Tk`
*   **Title:** "ASR Character Accuracy Comparison Tool - Multi-Tokenizer Version"
*   **Initial Size:** 800x650 (increased by 50 pixels height compared to old version to accommodate tokenizer selection area)
*   **Resizable:** Allows horizontal and vertical resizing (`resizable(True, True)`)
*   **Minimum Size:** 800x650 (`minsize(800, 650)`)

**Main Frames**

1.  **`top_frame` (Upper part frame)**
    *   **Type:** `ttk.Frame`
    *   **Parent:** `root`
    *   **Layout:** `pack(fill=tk.BOTH, expand=False, padx=10, pady=5)` (Fills available space, does not expand with window, internal/external padding)
2.  **`bottom_frame` (Lower part frame)**
    *   **Type:** `ttk.Frame`
    *   **Parent:** `root`
    *   **Layout:** `pack(fill=tk.BOTH, expand=True, padx=10, pady=5)` (Fills entire available space, expands with window, internal/external padding)

## Layer 1: Tokenizer Selection Area (New Core Feature)

1.  **`tokenizer_frame` (Tokenizer selection frame)**
    *   **Type:** `ttk.LabelFrame`
    *   **Parent:** `top_frame`
    *   **Text Label:** "Tokenizer Selection"
    *   **Layout:** `pack(fill=tk.X, padx=5, pady=5)` (Horizontal fill)

2.  **`tokenizer_selection_frame` (Tokenizer selection container frame)**
    *   **Type:** `ttk.Frame`
    *   **Parent:** `tokenizer_frame`
    *   **Layout:** `pack(fill=tk.X, padx=10, pady=10)`

3.  **`tokenizer_label` (Tokenizer label)**
    *   **Type:** `ttk.Label`
    *   **Parent:** `tokenizer_selection_frame`
    *   **Text:** "Select Tokenizer:"
    *   **Layout:** `pack(side=tk.LEFT, padx=(0, 10))`

4.  **`tokenizer_combobox` (Tokenizer dropdown selection box)**
    *   **Type:** `ttk.Combobox`
    *   **Parent:** `tokenizer_selection_frame`
    *   **Text Variable:** `self.selected_tokenizer` (StringVar, default value: "jieba")
    *   **Values List:** `self.available_tokenizers` (dynamically detected available tokenizers)
    *   **State:** "readonly"
    *   **Width:** 15
    *   **Layout:** `pack(side=tk.LEFT, padx=(0, 10))`
    *   **Event Binding:** `<<ComboboxSelected>>`: `self.on_tokenizer_change`

5.  **`tokenizer_status_label` (Tokenizer status label)**
    *   **Type:** `ttk.Label`
    *   **Parent:** `tokenizer_selection_frame`
    *   **Text:** Dynamic display (e.g., "✓ jieba (v0.42.1)" or "✗ thulac - Not installed")
    *   **Foreground Color:** "green" (available) or "red" (unavailable)
    *   **Layout:** `pack(side=tk.LEFT, padx=(0, 10))`

6.  **`tokenizer_info_btn` (Tokenizer info button)**
    *   **Type:** `ttk.Button`
    *   **Parent:** `tokenizer_selection_frame`
    *   **Text:** "Tokenizer Info"
    *   **Command:** `self.show_tokenizer_info`
    *   **Width:** 10
    *   **Layout:** `pack(side=tk.LEFT, padx=(0, 10))`

## Layer 2: File Selection Area

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
    *   **Height:** 120 (optimized for compact layout)
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
    *   **Height:** 120 (optimized for compact layout)
    *   **Width:** 350 (Fixed width to ensure consistency on both sides)
    *   **Layout:** `pack(fill=tk.BOTH, expand=True)`
    *   **Event Bindings:**
        *   `<ButtonPress-1>`: `self.on_press`
        *   `<B1-Motion>`: `self.on_drag`
        *   `<ButtonRelease-1>`: `self.on_release`

## Layer 3: Control Area

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
    *   **Values:** `onvalue=True, offvalue=False`
    *   **Layout:** `pack(side=tk.LEFT)`

15. **Filler word filter hint label**
    *   **Type:** `tk.Label`
    *   **Parent:** `filter_frame`
    *   **Text:** "?"
    *   **Font:** ("Arial", 9, "bold")
    *   **Color:** "blue"
    *   **Layout:** `pack(side=tk.LEFT, padx=3)`
    *   **Event Binding:** `<Enter>` to show tooltip

## Layer 4: Result Display Area

1.  **`result_frame` (Result display frame)**
    *   **Type:** `ttk.LabelFrame`
    *   **Parent:** `bottom_frame`
    *   **Text Label:** "Character Accuracy Statistics Results"
    *   **Layout:** `pack(fill=tk.BOTH, expand=True, padx=5, pady=5)`

2.  **`result_tree_frame` (Result table Treeview container frame)**
    *   **Type:** `ttk.Frame`
    *   **Parent:** `result_frame`
    *   **Layout:** `pack(fill=tk.BOTH, expand=True, padx=5, pady=5)`

3.  **`result_tree` (Result display table) - Added Tokenizer Column**
    *   **Type:** `ttk.Treeview`
    *   **Parent:** `result_tree_frame`
    *   **Columns:** ("Original File", "Annotation File", "ASR Char Count", "Ref Char Count", "Char Accuracy", "Filter Filler Words", "Tokenizer")
    *   **Display Mode:** "headings" (Only show headers, not index column)
    *   **Height (rows):** 8
    *   **Layout:** `pack(fill=tk.BOTH, expand=True)`
    *   **Column Attributes:**
        *   First 6 columns: `column(col, width=100, anchor="center")` (width 100, content centered)
        *   "Tokenizer" column: `column(col, width=80, anchor="center")` (width 80, content centered)

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

## Dynamically Created UI Elements

**Dynamically Created Elements inside Canvas** (created by `update_canvas_items` function)

*   **File Name Text:**
    *   **Type:** `canvas.create_text`
    *   **Coordinates:** `(20, y_pos)`
    *   **Text:** Filename (extracted from file path)
    *   **Anchor:** "w" (West, i.e., left-aligned)
    *   **Tags:** `f"file_{i}"` and full file path (for identification and association)
    *   **Spacing:** 40 pixels vertical spacing

**Tokenizer Info Dialog** (created by `show_tokenizer_info` function)

*   **Info Window:**
    *   **Type:** `tk.Toplevel`
    *   **Title:** "{tokenizer_name} Tokenizer Information"
    *   **Size:** 400x300
    *   **Resizable:** No (`resizable(False, False)`)
    *   **Modal:** Yes (`transient` and `grab_set`)

*   **Text Display Area:**
    *   **Type:** `tk.Text`
    *   **Parent:** `text_frame`
    *   **Wrap:** `wrap=tk.WORD`
    *   **Size:** width 50, height 15
    *   **State:** Read-only (`state=tk.DISABLED`)
    *   **Scrollbar:** Vertical scrollbar (`ttk.Scrollbar`)

*   **Information Content Includes:**
    *   Tokenizer name, class name, version
    *   Initialization status, availability
    *   Description, supported features, dependencies
    *   Performance, accuracy, notes
    *   Error information (if unavailable)

**Tooltip Feature**

* **Tooltip Window:**
  * **Type:** `tk.Toplevel`
  * **Borderless:** `wm_overrideredirect(True)`
  * **Position:** Dynamically calculated based on mouse position
  * **Background Color:** "#FFFFCC" (light yellow)
  * **Border:** `relief=tk.SOLID, borderwidth=1`
  * **Content:** Explanation of the filler word filtering function
  * **Boundary Detection:** Uses a 30x30 pixel virtual bounding box to determine mouse position

## New Version Interface Layout Features

### 📊 Layered Architecture Design
1. **Layer 1 - Tokenizer Selection**: New core feature supporting jieba/THULAC/HanLP switching
2. **Layer 2 - File Selection**: Maintains original drag-and-drop functionality, optimized layout compactness
3. **Layer 3 - Control Options**: Statistics button and filler word filtering options
4. **Layer 4 - Result Display**: Added tokenizer column, showing more detailed statistical information

### 🎯 Core New Features
1. **Intelligent Tokenizer Detection**: Automatically detects available tokenizers at startup
2. **Real-time Status Display**: Green ✓ indicates available, red ✗ indicates unavailable
3. **Detailed Information Display**: Dialog shows detailed tokenizer information
4. **Performance Optimization Caching**: Avoids repeated tokenizer initialization
5. **Graceful Degradation Mechanism**: Automatically fallback to jieba when tokenizers are unavailable

### 🔧 Layout Optimization Improvements
1. **Compact Tokenizer Selection Area**: Horizontally arranged all tokenizer-related controls
2. **Optimized File Display Area**: Canvas height adjusted to 120 pixels
3. **Enhanced Result Table**: Added "Tokenizer" column showing the tokenizer type used
4. **Unified Layout Style**: All buttons center-aligned, improving visual consistency

This new version UI design document covers all major UI components defined in `src/main_with_tokenizers.py`, particularly highlighting the multi-tokenizer support as the core new feature. The interface layout has been optimized to maintain the completeness of original functionality while adding powerful tokenizer switching capabilities. 