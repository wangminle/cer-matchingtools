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
    *   **布局:** `pack(fill=tk.BOTH, expand=False, padx=10, pady=5)` (填充可用空间，不随窗口扩展，内外边距)
2.  **`bottom_frame` (下半部分框架)**
    *   **类型:** `ttk.Frame`
    *   **父控件:** `root`
    *   **布局:** `pack(fill=tk.BOTH, expand=True, padx=10, pady=5)` (填充整个可用空间，随窗口扩展，内外边距)

**上半部分 (`top_frame`) 内的元素**

1.  **`file_area_frame` (文件区域框架)**
    *   **类型:** `ttk.Frame`
    *   **父控件:** `top_frame`
    *   **布局:** `pack(fill=tk.BOTH, expand=True, padx=5, pady=5)`
    *   **列配置:** 使用网格系统，两列等宽 `columnconfigure(0, weight=1, uniform="group1")` 和 `columnconfigure(1, weight=1, uniform="group1")`
2.  **`left_frame` (左侧框架 - ASR文件)**
    *   **类型:** `ttk.LabelFrame`
    *   **父控件:** `file_area_frame`
    *   **文本标签:** "ASR转换结果文件"
    *   **布局:** `grid(row=0, column=0, sticky="nsew", padx=5, pady=5)` (网格布局确保左右等宽)
3.  **`right_frame` (右侧框架 - 标注文件)**
    *   **类型:** `ttk.LabelFrame`
    *   **父控件:** `file_area_frame`
    *   **文本标签:** "标注文件"
    *   **布局:** `grid(row=0, column=1, sticky="nsew", padx=5, pady=5)` (网格布局确保左右等宽)
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
    *   **高度:** 160 (由120调整为160)
    *   **宽度:** 350 (固定宽度确保左右两侧一致)
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
    *   **高度:** 160 (由120调整为160)
    *   **宽度:** 350 (固定宽度确保左右两侧一致)
    *   **布局:** `pack(fill=tk.BOTH, expand=True)`
    *   **事件绑定:**
        *   `<ButtonPress-1>`: `self.on_press`
        *   `<B1-Motion>`: `self.on_drag`
        *   `<ButtonRelease-1>`: `self.on_release`
10. **`control_frame` (控制框架，包含按钮和过滤选项)**
    *   **类型:** `ttk.Frame`
    *   **父控件:** `top_frame`
    *   **布局:** `pack(fill=tk.X, pady=5)`
11. **`btn_container` (统计按钮容器框架)**
    *   **类型:** `ttk.Frame`
    *   **父控件:** `control_frame`
    *   **布局:** `pack(side=tk.TOP, fill=tk.X)`
12. **`calculate_btn` (开始统计按钮)**
    *   **类型:** `ttk.Button`
    *   **父控件:** `btn_container`
    *   **文本:** "开始统计"
    *   **命令:** `self.calculate_accuracy`
    *   **宽度:** 15
    *   **布局:** `pack(side=tk.TOP, pady=5)` (居中对齐)
13. **`filter_frame` (语气词过滤框架)**
    *   **类型:** `ttk.Frame`
    *   **父控件:** `control_frame`
    *   **布局:** `place(relx=1.0, rely=0.5, anchor=tk.E, x=-20)` (右侧绝对定位，垂直居中，与"开始统计"按钮在同一水平线上)
14. **`filter_check` (语气词过滤复选框)**
    *   **类型:** `ttk.Checkbutton`
    *   **父控件:** `filter_frame`
    *   **文本:** "语气词过滤"
    *   **变量:** `self.filter_fillers` (BooleanVar)
    *   **布局:** `pack(side=tk.LEFT)`
15. **语气词过滤提示标签**
    *   **类型:** `tk.Label`
    *   **父控件:** `filter_frame`
    *   **文本:** "?"
    *   **字体:** ("Arial", 9, "bold")
    *   **颜色:** "blue"
    *   **布局:** `pack(side=tk.LEFT, padx=3)`
    *   **事件绑定:** `<Enter>` 显示工具提示

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
    *   **列:** ("原始文件", "标注文件", "ASR字数", "标注字数", "字准确率", "过滤语气词")
    *   **显示模式:** "headings" (只显示表头，不显示索引列)
    *   **高度 (行数):** 8 (由12行减少到8行)
    *   **布局:** `pack(fill=tk.BOTH, expand=True)`
    *   **列属性 (循环设置):**
        *   `heading(col, text=col)` (设置每列的表头文本)
        *   `column(col, width=120, anchor="center")` (设置每列宽度120，内容居中)
4.  **`export_frame` (导出按钮容器框架)**
    *   **类型:** `ttk.Frame`
    *   **父控件:** `bottom_frame`
    *   **布局:** `pack(fill=tk.X, pady=10)`
5.  **`export_btn` (导出结果按钮)**
    *   **类型:** `ttk.Button`
    *   **父控件:** `export_frame`
    *   **文本:** "导出结果"
    *   **命令:** `self.export_results`
    *   **宽度:** 15
    *   **布局:** `pack(side=tk.TOP, pady=0)` (居中对齐)

**Canvas内部动态创建的元素** (通过 `update_canvas_items` 函数创建)

*   **文件矩形框:**
    *   **类型:** `canvas.create_rectangle`
    *   **坐标:** `(10, y_pos, 10 + item_width, y_pos+30)` (固定宽度确保两边一致)
    *   **填充色:** "lightblue"
    *   **标签:** `f"file_{i}"` 和 文件路径 `file_path` (用于标识和关联)
*   **文件名文本:**
    *   **类型:** `canvas.create_text`
    *   **坐标:** `(20, y_pos+15)`
    *   **文本:** `file_name` (从文件路径中提取)
    *   **锚点:** "w" (西，即左对齐)
    *   **标签:** `f"file_{i}"` (与对应矩形框关联)

**工具提示特性**

* **工具提示窗口:**
  * **类型:** `tk.Toplevel`
  * **无边框:** `wm_overrideredirect(True)`
  * **位置:** 根据鼠标位置动态计算
  * **内容:** 语气词过滤功能说明
  * **边界检测:** 使用30x30像素的虚拟边界框判断鼠标位置

**界面布局变更总结**

1. 文件显示区域高度从120像素增加到160像素
2. 使用网格布局确保左右两个文件区域宽度完全一致
3. 为Canvas设置固定宽度350像素，解决宽度不一致问题
4. 结果树视图高度从12行减少到8行
5. "开始统计"按钮和"导出结果"按钮使用居中对齐
6. "过滤语气词"勾选框使用place布局，垂直中点与"开始统计"按钮保持一致

这个列表涵盖了 `src/main.py` 中定义的所有主要UI组件及其关键属性和布局信息。Canvas 内部的元素是动态生成的，用于显示文件列表，并支持拖拽排序。布局已经优化，解决了宽度不一致问题，并使按钮居中显示，提升了用户体验。
