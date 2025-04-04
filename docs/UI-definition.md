好的，我们来分析一下 `src/main.py` 这个文件中的前端UI元素及其属性。

这个文件使用 `tkinter` 构建了一个图形用户界面。主要包含以下元素：

**主窗口 (`root`)**

*   **类型:** `tk.Tk`
*   **标题:** "ASR字准确率对比工具"
*   **初始尺寸:** 800x600
*   **可调整大小:** 允许水平和垂直调整 (`resizable(True, True)`)
*   **最小尺寸:** 800x600 (`minsize(800, 600)`)

**主框架**

1.  **`top_frame` (上半部分框架)**
    *   **类型:** `ttk.Frame`
    *   **父控件:** `root`
    *   **布局:** `pack(fill=tk.BOTH, expand=True, padx=10, pady=5)` (填充整个可用空间，随窗口扩展，内外边距)
2.  **`bottom_frame` (下半部分框架)**
    *   **类型:** `ttk.Frame`
    *   **父控件:** `root`
    *   **布局:** `pack(fill=tk.BOTH, expand=True, padx=10, pady=5)` (填充整个可用空间，随窗口扩展，内外边距)

**上半部分 (`top_frame`) 内的元素**

1.  **`file_area_frame` (文件区域框架)**
    *   **类型:** `ttk.Frame`
    *   **父控件:** `top_frame`
    *   **布局:** `pack(fill=tk.BOTH, expand=True, padx=5, pady=5)`
2.  **`left_frame` (左侧框架 - ASR文件)**
    *   **类型:** `ttk.LabelFrame`
    *   **父控件:** `file_area_frame`
    *   **文本标签:** "ASR转换结果文件"
    *   **布局:** `pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)` (靠左停靠，填充并扩展)
3.  **`right_frame` (右侧框架 - 标注文件)**
    *   **类型:** `ttk.LabelFrame`
    *   **父控件:** `file_area_frame`
    *   **文本标签:** "标注文件"
    *   **布局:** `pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)` (靠右停靠，填充并扩展)
4.  **`asr_btn` (选择ASR文件按钮)**
    *   **类型:** `ttk.Button`
    *   **父控件:** `left_frame`
    *   **文本:** "选择ASR文件"
    *   **命令:** `self.select_asr_files`
    *   **布局:** `pack(pady=5)` (垂直内边距)
5.  **`asr_canvas_frame` (ASR文件列表Canvas容器框架)**
    *   **类型:** `ttk.Frame`
    *   **父控件:** `left_frame`
    *   **布局:** `pack(fill=tk.BOTH, expand=True, padx=5, pady=5)`
6.  **`asr_canvas` (ASR文件列表显示区域)**
    *   **类型:** `tk.Canvas`
    *   **父控件:** `asr_canvas_frame`
    *   **背景色:** "white"
    *   **高度:** 150
    *   **布局:** `pack(fill=tk.BOTH, expand=True)`
    *   **事件绑定:**
        *   `<ButtonPress-1>`: `self.on_press`
        *   `<B1-Motion>`: `self.on_drag`
        *   `<ButtonRelease-1>`: `self.on_release`
7.  **`ref_btn` (选择标注文件按钮)**
    *   **类型:** `ttk.Button`
    *   **父控件:** `right_frame`
    *   **文本:** "选择标注文件"
    *   **命令:** `self.select_ref_files`
    *   **布局:** `pack(pady=5)`
8.  **`ref_canvas_frame` (标注文件列表Canvas容器框架)**
    *   **类型:** `ttk.Frame`
    *   **父控件:** `right_frame`
    *   **布局:** `pack(fill=tk.BOTH, expand=True, padx=5, pady=5)`
9.  **`ref_canvas` (标注文件列表显示区域)**
    *   **类型:** `tk.Canvas`
    *   **父控件:** `ref_canvas_frame`
    *   **背景色:** "white"
    *   **高度:** 150
    *   **布局:** `pack(fill=tk.BOTH, expand=True)`
    *   **事件绑定:**
        *   `<ButtonPress-1>`: `self.on_press`
        *   `<B1-Motion>`: `self.on_drag`
        *   `<ButtonRelease-1>`: `self.on_release`
10. **`calculate_btn` (开始统计按钮)**
    *   **类型:** `ttk.Button`
    *   **父控件:** `top_frame` (直接位于top\_frame，在file\_area\_frame下方)
    *   **文本:** "开始统计"
    *   **命令:** `self.calculate_accuracy`
    *   **宽度:** 15
    *   **布局:** `pack(pady=10)`

**下半部分 (`bottom_frame`) 内的元素**

1.  **`result_frame` (结果显示框架)**
    *   **类型:** `ttk.LabelFrame`
    *   **父控件:** `bottom_frame`
    *   **文本标签:** "字准确率统计结果"
    *   **布局:** `pack(fill=tk.BOTH, expand=True, padx=5, pady=5)`
2.  **`result_tree_frame` (结果表格Treeview容器框架)**
    *   **类型:** `ttk.Frame`
    *   **父控件:** `result_frame`
    *   **布局:** `pack(fill=tk.BOTH, expand=True, padx=5, pady=5)`
3.  **`result_tree` (结果显示表格)**
    *   **类型:** `ttk.Treeview`
    *   **父控件:** `result_tree_frame`
    *   **列:** ("原始文件", "标注文件", "ASR字数", "标注字数", "字准确率")
    *   **显示模式:** "headings" (只显示表头，不显示索引列)
    *   **高度 (行数):** 8
    *   **布局:** `pack(fill=tk.BOTH, expand=True)`
    *   **列属性 (循环设置):**
        *   `heading(col, text=col)` (设置每列的表头文本)
        *   `column(col, width=150, anchor="center")` (设置每列宽度150，内容居中)
4.  **`export_btn` (导出结果按钮)**
    *   **类型:** `ttk.Button`
    *   **父控件:** `bottom_frame` (直接位于bottom\_frame，在result\_frame下方)
    *   **文本:** "导出结果"
    *   **命令:** `self.export_results`
    *   **宽度:** 15
    *   **布局:** `pack(pady=10)`

**Canvas内部动态创建的元素** (通过 `update_canvas_items` 函数创建)

*   **文件矩形框:**
    *   **类型:** `canvas.create_rectangle`
    *   **坐标:** `(10, y_pos, canvas.winfo_width()-10, y_pos+30)` (根据canvas宽度动态调整)
    *   **填充色:** "lightblue"
    *   **标签:** `f"file_{i}"` 和 文件路径 `file_path` (用于标识和关联)
*   **文件名文本:**
    *   **类型:** `canvas.create_text`
    *   **坐标:** `(20, y_pos+15)`
    *   **文本:** `file_name` (从文件路径中提取)
    *   **锚点:** "w" (西，即左对齐)
    *   **标签:** `f"file_{i}"` (与对应矩形框关联)

这个列表涵盖了 `src/main.py` 中定义的所有主要UI组件及其关键属性和布局信息。 Canvas 内部的元素是动态生成的，用于显示文件列表，并支持拖拽排序。
