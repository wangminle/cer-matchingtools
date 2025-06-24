好的，我们来分析一下 `src/main_with_tokenizers.py` 这个新版本文件中的前端UI元素及其属性。

这个文件使用 `tkinter` 构建了一个支持多分词器切换的图形用户界面。主要包含以下元素：

**主窗口 (`root`)**

*   **类型:** `tk.Tk`
*   **标题:** "ASR字准确率对比工具 - 多分词器版本"
*   **初始尺寸:** 800x650 (相比旧版本增加了50像素高度以容纳分词器选择区域)
*   **可调整大小:** 允许水平和垂直调整 (`resizable(True, True)`)
*   **最小尺寸:** 800x650 (`minsize(800, 650)`)

**主框架**

1.  **`top_frame` (上半部分框架)**
    *   **类型:** `ttk.Frame`
    *   **父控件:** `root`
    *   **布局:** `pack(fill=tk.BOTH, expand=False, padx=10, pady=5)` (填充可用空间，不随窗口扩展，内外边距)
2.  **`bottom_frame` (下半部分框架)**
    *   **类型:** `ttk.Frame`
    *   **父控件:** `root`
    *   **布局:** `pack(fill=tk.BOTH, expand=True, padx=10, pady=5)` (填充整个可用空间，随窗口扩展，内外边距)

## 第一层：分词器选择区域 (新增核心功能)

1.  **`tokenizer_frame` (分词器选择框架)**
    *   **类型:** `ttk.LabelFrame`
    *   **父控件:** `top_frame`
    *   **文本标签:** "分词器选择"
    *   **布局:** `pack(fill=tk.X, padx=5, pady=5)` (水平填充)

2.  **`tokenizer_selection_frame` (分词器选择容器框架)**
    *   **类型:** `ttk.Frame`
    *   **父控件:** `tokenizer_frame`
    *   **布局:** `pack(fill=tk.X, padx=10, pady=10)`

3.  **`tokenizer_label` (分词器标签)**
    *   **类型:** `ttk.Label`
    *   **父控件:** `tokenizer_selection_frame`
    *   **文本:** "选择分词器:"
    *   **布局:** `pack(side=tk.LEFT, padx=(0, 10))`

4.  **`tokenizer_combobox` (分词器下拉选择框)**
    *   **类型:** `ttk.Combobox`
    *   **父控件:** `tokenizer_selection_frame`
    *   **文本变量:** `self.selected_tokenizer` (StringVar，默认值："jieba")
    *   **值列表:** `self.available_tokenizers` (动态检测可用分词器)
    *   **状态:** "readonly" (只读)
    *   **宽度:** 15
    *   **布局:** `pack(side=tk.LEFT, padx=(0, 10))`
    *   **事件绑定:** `<<ComboboxSelected>>`: `self.on_tokenizer_change`

5.  **`tokenizer_status_label` (分词器状态标签)**
    *   **类型:** `ttk.Label`
    *   **父控件:** `tokenizer_selection_frame`
    *   **文本:** 动态显示 (例如："✓ jieba (v0.42.1)" 或 "✗ thulac - 未安装")
    *   **前景色:** "green" (可用) 或 "red" (不可用)
    *   **布局:** `pack(side=tk.LEFT, padx=(0, 10))`

6.  **`tokenizer_info_btn` (分词器信息按钮)**
    *   **类型:** `ttk.Button`
    *   **父控件:** `tokenizer_selection_frame`
    *   **文本:** "分词器信息"
    *   **命令:** `self.show_tokenizer_info`
    *   **宽度:** 10
    *   **布局:** `pack(side=tk.LEFT, padx=(0, 10))`

## 第二层：文件选择区域

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
    *   **高度:** 120 (优化为紧凑布局)
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
    *   **高度:** 120 (优化为紧凑布局)
    *   **宽度:** 350 (固定宽度确保左右两侧一致)
    *   **布局:** `pack(fill=tk.BOTH, expand=True)`
    *   **事件绑定:**
        *   `<ButtonPress-1>`: `self.on_press`
        *   `<B1-Motion>`: `self.on_drag`
        *   `<ButtonRelease-1>`: `self.on_release`

## 第三层：控制区域

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
    *   **值:** `onvalue=True, offvalue=False`
    *   **布局:** `pack(side=tk.LEFT)`

15. **语气词过滤提示标签**
    *   **类型:** `tk.Label`
    *   **父控件:** `filter_frame`
    *   **文本:** "?"
    *   **字体:** ("Arial", 9, "bold")
    *   **颜色:** "blue"
    *   **布局:** `pack(side=tk.LEFT, padx=3)`
    *   **事件绑定:** `<Enter>` 显示工具提示

## 第四层：结果显示区域

1.  **`result_frame` (结果显示框架)**
    *   **类型:** `ttk.LabelFrame`
    *   **父控件:** `bottom_frame`
    *   **文本标签:** "字准确率统计结果"
    *   **布局:** `pack(fill=tk.BOTH, expand=True, padx=5, pady=5)`

2.  **`result_tree_frame` (结果表格Treeview容器框架)**
    *   **类型:** `ttk.Frame`
    *   **父控件:** `result_frame`
    *   **布局:** `pack(fill=tk.BOTH, expand=True, padx=5, pady=5)`

3.  **`result_tree` (结果显示表格) - 新增分词器列**
    *   **类型:** `ttk.Treeview`
    *   **父控件:** `result_tree_frame`
    *   **列:** ("原始文件", "标注文件", "ASR字数", "标注字数", "字准确率", "过滤语气词", "分词器")
    *   **显示模式:** "headings" (只显示表头，不显示索引列)
    *   **高度 (行数):** 8
    *   **布局:** `pack(fill=tk.BOTH, expand=True)`
    *   **列属性:**
        *   前6列: `column(col, width=100, anchor="center")` (宽度100，内容居中)
        *   "分词器"列: `column(col, width=80, anchor="center")` (宽度80，内容居中)

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

## 动态创建的UI元素

**Canvas内部动态创建的元素** (通过 `update_canvas_items` 函数创建)

*   **文件名文本:**
    *   **类型:** `canvas.create_text`
    *   **坐标:** `(20, y_pos)`
    *   **文本:** 文件名 (从文件路径中提取)
    *   **锚点:** "w" (西，即左对齐)
    *   **标签:** `f"file_{i}"` 和 完整文件路径 (用于标识和关联)
    *   **间距:** 垂直间距40像素

**分词器信息弹窗** (通过 `show_tokenizer_info` 函数创建)

*   **信息窗口:**
    *   **类型:** `tk.Toplevel`
    *   **标题:** "{tokenizer_name} 分词器信息"
    *   **尺寸:** 400x300
    *   **可调整大小:** 否 (`resizable(False, False)`)
    *   **模态:** 是 (`transient` 和 `grab_set`)

*   **文本显示区域:**
    *   **类型:** `tk.Text`
    *   **父控件:** `text_frame`
    *   **换行:** `wrap=tk.WORD`
    *   **尺寸:** 宽度50，高度15
    *   **状态:** 只读 (`state=tk.DISABLED`)
    *   **滚动条:** 垂直滚动条 (`ttk.Scrollbar`)

*   **信息内容包含:**
    *   分词器名称、类名、版本
    *   初始化状态、可用性
    *   描述、支持功能、依赖库
    *   性能、准确度、注意事项
    *   错误信息 (如果不可用)

**工具提示特性**

* **工具提示窗口:**
  * **类型:** `tk.Toplevel`
  * **无边框:** `wm_overrideredirect(True)`
  * **位置:** 根据鼠标位置动态计算
  * **背景色:** "#FFFFCC" (淡黄色)
  * **边框:** `relief=tk.SOLID, borderwidth=1`
  * **内容:** 语气词过滤功能说明
  * **边界检测:** 使用30x30像素的虚拟边界框判断鼠标位置

## 新版本界面布局特性

### 📊 分层架构设计
1. **第一层 - 分词器选择**: 新增核心功能，支持jieba/THULAC/HanLP切换
2. **第二层 - 文件选择**: 保持原有拖拽功能，优化布局紧凑性
3. **第三层 - 控制选项**: 统计按钮和语气词过滤选项
4. **第四层 - 结果展示**: 新增分词器列，显示更详细的统计信息

### 🎯 核心新功能
1. **智能分词器检测**: 启动时自动检测可用分词器
2. **实时状态显示**: 绿色✓表示可用，红色✗表示不可用
3. **详细信息展示**: 弹窗显示分词器详细信息
4. **性能优化缓存**: 避免重复初始化分词器
5. **优雅降级机制**: 分词器不可用时自动回退到jieba

### 🔧 布局优化改进
1. **紧凑的分词器选择区域**: 水平排列所有分词器相关控件
2. **优化的文件显示区域**: Canvas高度调整为120像素
3. **增强的结果表格**: 新增"分词器"列，显示使用的分词器类型
4. **统一的布局风格**: 所有按钮居中对齐，提升视觉一致性

这个新版本的UI设计文档涵盖了 `src/main_with_tokenizers.py` 中定义的所有主要UI组件，特别突出了多分词器支持这一核心新功能。界面布局经过优化，既保持了原有功能的完整性，又新增了强大的分词器切换能力。
