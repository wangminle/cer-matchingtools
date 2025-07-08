import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import pandas as pd
import jiwer
from functools import partial

# 导入重构后的ASRMetrics类和分词器模块
from asr_metrics_refactored import ASRMetrics
from text_tokenizers import get_available_tokenizers, get_tokenizer_info, get_cached_tokenizer_info


class ASRComparisonTool:
    def __init__(self, root):
        self.root = root
        self.root.title("ASR字准确率对比工具 - 多分词器版本")
        self.root.geometry("800x650")  # 增加一些高度以容纳分词器选择
        # 设置窗口大小不可调整，但支持最大化
        self.root.resizable(True, True)
        # 设置minsize，确保窗口不会小于800x650
        self.root.minsize(800, 650)
        
        # 存储文件列表和配对信息
        self.asr_files = []
        self.ref_files = []
        self.file_pairs = []
        self.results = []
        
        # 性能优化：缓存ASRMetrics实例，避免重复创建
        self.asr_metrics_cache = {}
        
        # 创建主框架分为上下两部分
        self.top_frame = ttk.Frame(root)
        self.top_frame.pack(fill=tk.BOTH, expand=False, padx=10, pady=5)  # 不再扩展，固定上部区域高度
        
        self.bottom_frame = ttk.Frame(root)
        self.bottom_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)  # 让下部结果区域自动扩展
        
        # 语气词过滤设置
        self.filter_fillers = tk.BooleanVar(value=False)
        
        # 分词器设置
        self.selected_tokenizer = tk.StringVar(value="jieba")  # 默认选择jieba
        self.available_tokenizers = []
        
        # 提示框变量
        self.tooltip_window = None
        
        # 初始化分词器列表
        self._init_tokenizers()
        
        # 初始化UI组件
        self._init_ui()
    
    def _init_tokenizers(self):
        """初始化可用的分词器列表"""
        try:
            self.available_tokenizers = get_available_tokenizers()
            if not self.available_tokenizers:
                self.available_tokenizers = ["jieba"]  # 确保至少有jieba
            
            # 如果jieba可用，设为默认值
            if "jieba" in self.available_tokenizers:
                self.selected_tokenizer.set("jieba")
            else:
                # 如果jieba不可用，选择第一个可用的分词器
                self.selected_tokenizer.set(self.available_tokenizers[0])
                
        except Exception as e:
            print(f"警告: 初始化分词器列表失败: {str(e)}")
            self.available_tokenizers = ["jieba"]
            self.selected_tokenizer.set("jieba")
    
    def _init_ui(self):
        # 上半部分 - 分词器选择区域（新增）
        self.tokenizer_frame = ttk.LabelFrame(self.top_frame, text="分词器选择")
        self.tokenizer_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 分词器选择容器
        self.tokenizer_selection_frame = ttk.Frame(self.tokenizer_frame)
        self.tokenizer_selection_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 分词器标签
        self.tokenizer_label = ttk.Label(self.tokenizer_selection_frame, text="选择分词器:")
        self.tokenizer_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # 分词器下拉框
        self.tokenizer_combobox = ttk.Combobox(
            self.tokenizer_selection_frame, 
            textvariable=self.selected_tokenizer,
            values=self.available_tokenizers,
            state="readonly",
            width=15
        )
        self.tokenizer_combobox.pack(side=tk.LEFT, padx=(0, 10))
        self.tokenizer_combobox.bind("<<ComboboxSelected>>", self.on_tokenizer_change)
        
        # 分词器状态标签
        self.tokenizer_status_label = ttk.Label(
            self.tokenizer_selection_frame, 
            text="", 
            foreground="green"
        )
        self.tokenizer_status_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # 分词器信息按钮
        self.tokenizer_info_btn = ttk.Button(
            self.tokenizer_selection_frame,
            text="分词器信息",
            command=self.show_tokenizer_info,
            width=10
        )
        self.tokenizer_info_btn.pack(side=tk.LEFT, padx=(10, 10))
        
        # 更新分词器状态
        self.update_tokenizer_status()
        
        # 文件选择区域
        # 创建包含左右两帧和底部按钮的上半部分框架
        self.file_area_frame = ttk.Frame(self.top_frame)
        self.file_area_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建一个固定比例的网格系统，确保左右框架宽度一致
        self.file_area_frame.columnconfigure(0, weight=1, uniform="group1")  # 左侧列
        self.file_area_frame.columnconfigure(1, weight=1, uniform="group1")  # 右侧列
        
        self.left_frame = ttk.LabelFrame(self.file_area_frame, text="ASR转换结果文件")
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        self.right_frame = ttk.LabelFrame(self.file_area_frame, text="标注文件")
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # ASR文件选择按钮和列表
        self.asr_btn = ttk.Button(self.left_frame, text="选择ASR文件", command=self.select_asr_files)
        self.asr_btn.pack(pady=5)
        
        # 创建一个frame来容纳canvas，以便控制高度
        self.asr_canvas_frame = ttk.Frame(self.left_frame)
        self.asr_canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 设置canvas的高度和宽度
        self.asr_canvas = tk.Canvas(self.asr_canvas_frame, bg="white", height=120, width=350)  # 减少高度
        self.asr_canvas.pack(fill=tk.BOTH, expand=True)
        self.asr_canvas.bind("<ButtonPress-1>", self.on_press)
        self.asr_canvas.bind("<B1-Motion>", self.on_drag)
        self.asr_canvas.bind("<ButtonRelease-1>", self.on_release)
        
        # 标注文件选择按钮和列表
        self.ref_btn = ttk.Button(self.right_frame, text="选择标注文件", command=self.select_ref_files)
        self.ref_btn.pack(pady=5)
        
        # 创建一个frame来容纳canvas，以便控制高度
        self.ref_canvas_frame = ttk.Frame(self.right_frame)
        self.ref_canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 设置canvas的高度和宽度，确保与左侧一致
        self.ref_canvas = tk.Canvas(self.ref_canvas_frame, bg="white", height=120, width=350)  # 减少高度
        self.ref_canvas.pack(fill=tk.BOTH, expand=True)
        self.ref_canvas.bind("<ButtonPress-1>", self.on_press)
        self.ref_canvas.bind("<B1-Motion>", self.on_drag)
        self.ref_canvas.bind("<ButtonRelease-1>", self.on_release)
        
        # 创建单一控制框架，将统计按钮和过滤勾选框放在同一行
        self.control_frame = ttk.Frame(self.top_frame)
        self.control_frame.pack(fill=tk.X, pady=5)
        
        # 创建按钮容器框架
        self.btn_container = ttk.Frame(self.control_frame)
        self.btn_container.pack(side=tk.TOP, fill=tk.X)
        
        # 统计按钮 - 居中对齐
        self.calculate_btn = ttk.Button(self.btn_container, text="开始统计", command=self.calculate_accuracy, width=15)
        self.calculate_btn.pack(side=tk.TOP, pady=5)
        
        # 语气词过滤开关 - 调整位置到右侧，并与"开始统计"按钮垂直居中对齐
        self.filter_frame = ttk.Frame(self.control_frame)
        # 使用place布局，设置rely=0.5使其垂直居中，anchor=E使其靠右对齐
        self.filter_frame.place(relx=1.0, rely=0.5, anchor=tk.E, x=-20)
        
        self.filter_check = ttk.Checkbutton(
            self.filter_frame, 
            text="语气词过滤", 
            variable=self.filter_fillers,
            onvalue=True,
            offvalue=False
        )
        self.filter_check.pack(side=tk.LEFT)
        
        # 为语气词过滤开关添加提示信息
        filter_tooltip = tk.Label(self.filter_frame, text="?", font=("Arial", 9, "bold"), fg="blue")
        filter_tooltip.pack(side=tk.LEFT, padx=3)
        
        # 鼠标悬停显示提示信息
        def show_tooltip(event):
            # 避免多个提示框出现，如果已存在则不创建新的
            if self.tooltip_window:
                return
                
            # 创建提示框
            self.tooltip_window = tk.Toplevel(self.root)
            self.tooltip_window.wm_overrideredirect(True)  # 无边框窗口
            self.tooltip_window.geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            tooltip_text = '开启此选项后，计算字准确率时将会过滤掉"嗯"、"啊"、"呢"等语气词。\n这可以使CER计算更准确地反映实际语义内容。'
            label = tk.Label(self.tooltip_window, text=tooltip_text, justify=tk.LEFT, 
                             background="#FFFFCC", relief=tk.SOLID, borderwidth=1, padx=5, pady=5)
            label.pack()
            
            # 构建虚拟边界框（30x30像素的区域）
            # 获取问号标签的位置和尺寸
            x = filter_tooltip.winfo_rootx()
            y = filter_tooltip.winfo_rooty()
            w = filter_tooltip.winfo_width()
            h = filter_tooltip.winfo_height()
            
            # 计算中心点
            center_x = x + w/2
            center_y = y + h/2
            
            # 边界框的边界
            self.tooltip_boundary = {
                'x1': center_x - 15,  # 左边界
                'y1': center_y - 15,  # 上边界
                'x2': center_x + 15,  # 右边界
                'y2': center_y + 15   # 下边界
            }
            
            # 绑定鼠标移动事件
            self.root.bind("<Motion>", check_tooltip_boundary)
            
        def check_tooltip_boundary(event):
            """检查鼠标是否在提示框边界内"""
            if self.tooltip_window:
                # 获取鼠标当前位置
                x, y = event.x_root, event.y_root
                
                # 检查是否在30x30的边界框内
                if (x < self.tooltip_boundary['x1'] or 
                    x > self.tooltip_boundary['x2'] or 
                    y < self.tooltip_boundary['y1'] or 
                    y > self.tooltip_boundary['y2']):
                    # 如果鼠标移出边界框，销毁提示框
                    self.tooltip_window.destroy()
                    self.tooltip_window = None
                    self.root.unbind("<Motion>")
        
        filter_tooltip.bind("<Enter>", show_tooltip)
        
        # 下半部分 - 结果显示区域
        self.result_frame = ttk.LabelFrame(self.bottom_frame, text="字准确率统计结果")
        self.result_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建一个frame来容纳treeview，以便控制高度
        self.result_tree_frame = ttk.Frame(self.result_frame)
        self.result_tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 结果展示表格，设置高度 - 增加分词器列
        columns = ("原始文件", "标注文件", "ASR字数", "标注字数", "字准确率", "过滤语气词", "分词器")
        self.result_tree = ttk.Treeview(self.result_tree_frame, columns=columns, show="headings", height=8)  
        for col in columns:
            self.result_tree.heading(col, text=col)
            if col == "分词器":
                self.result_tree.column(col, width=80, anchor="center")
            else:
                self.result_tree.column(col, width=100, anchor="center")
        
        self.result_tree.pack(fill=tk.BOTH, expand=True)
        
        # 创建导出按钮的容器框架用于居中对齐
        self.export_frame = ttk.Frame(self.bottom_frame)
        self.export_frame.pack(fill=tk.X, pady=10)
        
        # 导出按钮 - 居中对齐
        self.export_btn = ttk.Button(self.export_frame, text="导出结果", command=self.export_results, width=15)
        self.export_btn.pack(side=tk.TOP, pady=0)
        
        # 设置拖拽变量
        self.drag_data = {"x": 0, "y": 0, "item": None, "canvas": None}
    
    def on_tokenizer_change(self, event=None):
        """分词器选择变化时的回调函数"""
        self.update_tokenizer_status()
    
    def update_tokenizer_status(self):
        """更新分词器状态显示"""
        tokenizer_name = self.selected_tokenizer.get()
        try:
            # 性能优化：使用缓存的信息
            info = get_tokenizer_info(tokenizer_name)
            if info.get('available', False):
                version = info.get('version', 'unknown')
                status_text = f"✓ {tokenizer_name} (v{version})"
                if tokenizer_name in self.asr_metrics_cache:
                    status_text += " [已缓存]"
                self.tokenizer_status_label.config(
                    text=status_text,
                    foreground="green"
                )
            else:
                error_msg = info.get('error', '未知错误')
                self.tokenizer_status_label.config(
                    text=f"✗ {tokenizer_name} - {error_msg[:20]}...",
                    foreground="red"
                )
        except Exception as e:
            self.tokenizer_status_label.config(
                text=f"✗ {tokenizer_name} - 获取信息失败",
                foreground="red"
            )
    
    def clear_tokenizer_cache(self):
        """清理分词器缓存"""
        print("正在清理分词器缓存...")
        
        # 清理ASRMetrics缓存
        self.asr_metrics_cache.clear()
        
        # 清理工厂类缓存
        try:
            from text_tokenizers.tokenizers.factory import TokenizerFactory
            TokenizerFactory.clear_cache()
            print("工厂类缓存已清理")
        except Exception as e:
            print(f"清理工厂类缓存失败: {str(e)}")
        
        # 更新分词器状态显示
        self.update_tokenizer_status()
        print("缓存清理完成，状态已更新")
    
    def show_tokenizer_info(self):
        """显示分词器详细信息"""
        tokenizer_name = self.selected_tokenizer.get()
        try:
            # 🔧 修复: 优先使用工厂类的缓存信息获取方法
            info = get_cached_tokenizer_info(tokenizer_name)
            
            # 如果工厂类缓存中没有，再检查ASRMetrics缓存
            if info is None and tokenizer_name in self.asr_metrics_cache:
                try:
                    cached_metrics = self.asr_metrics_cache[tokenizer_name]
                    info = cached_metrics.get_tokenizer_info()
                    info['initialized'] = True
                    info['available'] = True
                    info['cached'] = True
                    print(f"从ASRMetrics缓存获取{tokenizer_name}分词器信息")
                except Exception as e:
                    print(f"从ASRMetrics缓存获取信息失败: {str(e)}")
                    info = None
            
            # 如果都没有缓存，则从工厂类获取（可能会触发初始化）
            if info is None:
                info = get_tokenizer_info(tokenizer_name)
                print(f"从工厂类重新获取{tokenizer_name}分词器信息")
            else:
                print(f"使用缓存的{tokenizer_name}分词器信息")
            
            # 创建信息窗口
            info_window = tk.Toplevel(self.root)
            info_window.title(f"{tokenizer_name} 分词器信息")
            info_window.geometry("400x300")
            info_window.resizable(False, False)
            
            # 使窗口居中
            info_window.transient(self.root)
            info_window.grab_set()
            
            # 创建滚动文本框
            text_frame = ttk.Frame(info_window)
            text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            text_widget = tk.Text(text_frame, wrap=tk.WORD, width=50, height=15)
            scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
            text_widget.configure(yscrollcommand=scrollbar.set)
            
            text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # 格式化信息文本
            info_text = f"分词器名称: {info.get('name', 'N/A')}\n"
            info_text += f"类名: {info.get('class_name', 'N/A')}\n"
            info_text += f"版本: {info.get('version', 'N/A')}\n"
            
            # 🔧 修复: 更准确的缓存状态显示
            init_status = "成功" if info.get('initialized', False) else "失败"
            if info.get('cached', False):
                init_status += " [已缓存]"
            elif tokenizer_name in self.asr_metrics_cache:
                init_status += " [ASR已缓存]"
            info_text += f"初始化状态: {init_status}\n"
            
            info_text += f"可用性: {'可用' if info.get('available', False) else '不可用'}\n\n"
            
            if 'description' in info:
                info_text += f"描述: {info['description']}\n\n"
            
            if 'features' in info:
                info_text += f"支持功能: {', '.join(info['features'])}\n\n"
            
            if 'dependencies' in info:
                info_text += f"依赖库: {', '.join(info['dependencies'])}\n\n"
            
            if 'performance' in info:
                info_text += f"性能: {info['performance']}\n"
            
            if 'accuracy' in info:
                info_text += f"准确度: {info['accuracy']}\n\n"
            
            if 'note' in info:
                info_text += f"注意事项: {info['note']}\n\n"
            
            # 🔧 修复: HanLP特有信息显示
            if tokenizer_name == 'hanlp':
                if 'tok_model' in info:
                    info_text += f"分词模型: {info['tok_model']}\n"
                if 'pos_model' in info:
                    info_text += f"词性标注模型: {info['pos_model']}\n"
                info_text += "\n"
            
            if not info.get('available', False) and 'error' in info:
                info_text += f"错误信息: {info['error']}\n"
            
            text_widget.insert(tk.END, info_text)
            text_widget.config(state=tk.DISABLED)
            
            # 关闭按钮
            close_btn = ttk.Button(info_window, text="关闭", command=info_window.destroy)
            close_btn.pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("错误", f"获取分词器信息失败: {str(e)}")

    def select_asr_files(self):
        files = filedialog.askopenfilenames(filetypes=[("文本文件", "*.txt")])
        self.asr_files = list(files)
        self.update_canvas_items(self.asr_canvas, self.asr_files)

    def select_ref_files(self):
        files = filedialog.askopenfilenames(filetypes=[("文本文件", "*.txt")])
        self.ref_files = list(files)
        self.update_canvas_items(self.ref_canvas, self.ref_files)

    def update_canvas_items(self, canvas, file_list):
        canvas.delete("all")
        y_pos = 20
        for i, file_path in enumerate(file_list):
            filename = os.path.basename(file_path)
            item_id = canvas.create_text(20, y_pos, text=filename, anchor="w", tags=(f"file_{i}", file_path))
            canvas.itemconfig(item_id, tags=(f"file_{i}", file_path))
            y_pos += 40

    def on_press(self, event):
        canvas = event.widget
        closest = canvas.find_closest(event.x, event.y)
        if closest:
            tags = canvas.gettags(closest)
            if tags and tags[0].startswith("file_"):
                self.drag_data["item"] = closest
                self.drag_data["x"] = event.x
                self.drag_data["y"] = event.y
                self.drag_data["canvas"] = canvas

    def on_drag(self, event):
        if self.drag_data["item"]:
            dx = event.x - self.drag_data["x"]
            dy = event.y - self.drag_data["y"]
            
            canvas = self.drag_data["canvas"]
            item = self.drag_data["item"]
            
            canvas.move(item, 0, dy)
            # 同时移动文本标签
            tags = canvas.gettags(item)
            for tag in tags:
                if tag.startswith("file_"):
                    text_items = canvas.find_withtag(tag)
                    for text_item in text_items:
                        if text_item != item:
                            canvas.move(text_item, 0, dy)
            
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

    def on_release(self, event):
        self.drag_data["item"] = None
        self.drag_data["canvas"] = None

    def get_file_order(self, canvas):
        items = canvas.find_all()
        file_items = {}
        
        for item in items:
            tags = canvas.gettags(item)
            if tags and tags[0].startswith("file_"):
                coords = canvas.coords(item)
                if len(coords) >= 2:  # 确保有足够的坐标信息
                    y_pos = coords[1]  # 获取y坐标
                    file_path = tags[1] if len(tags) > 1 else None
                    if file_path:
                        file_items[y_pos] = file_path
        
        # 按y坐标排序
        return [file_items[y] for y in sorted(file_items.keys())]

    def calculate_accuracy(self):
        # 清空结果
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
        
        self.results = []
        
        # 获取排序后的文件列表
        sorted_asr_files = self.get_file_order(self.asr_canvas)
        sorted_ref_files = self.get_file_order(self.ref_canvas)
        
        # 检查文件数量是否匹配
        if len(sorted_asr_files) != len(sorted_ref_files):
            messagebox.showerror("错误", "ASR文件和标注文件数量不匹配！")
            return
        
        # 获取语气词过滤设置
        filter_fillers = self.filter_fillers.get()
        
        # 获取选择的分词器
        tokenizer_name = self.selected_tokenizer.get()
        
        try:
            # 性能优化：使用缓存的ASRMetrics实例，避免重复创建
            if tokenizer_name not in self.asr_metrics_cache:
                print(f"初始化{tokenizer_name}分词器...")
                self.asr_metrics_cache[tokenizer_name] = ASRMetrics(tokenizer_name=tokenizer_name)
            
            asr_metrics = self.asr_metrics_cache[tokenizer_name]
            
            # 逐对计算字准确率
            for asr_file, ref_file in zip(sorted_asr_files, sorted_ref_files):
                try:
                    # 读取文件内容
                    asr_text = self.read_file_with_multiple_encodings(asr_file)
                    ref_text = self.read_file_with_multiple_encodings(ref_file)
                    
                    # 使用ASRMetrics计算各项指标，传入语气词过滤设置
                    metrics = asr_metrics.calculate_detailed_metrics(ref_text, asr_text, filter_fillers)
                    
                    # 获取结果
                    accuracy = metrics['accuracy']
                    ref_chars = metrics['ref_length']
                    asr_chars = metrics['hyp_length']
                    used_tokenizer = metrics.get('tokenizer', tokenizer_name)
                    
                    result = {
                        "asr_file": os.path.basename(asr_file),
                        "ref_file": os.path.basename(ref_file),
                        "asr_chars": asr_chars,
                        "ref_chars": ref_chars,
                        "accuracy": accuracy,
                        "details": metrics,  # 保存详细指标供后续使用
                        "filter_fillers": filter_fillers,  # 记录是否应用了语气词过滤
                        "tokenizer": used_tokenizer  # 记录使用的分词器
                    }
                    
                    self.results.append(result)
                    
                    # 添加到结果表格
                    self.result_tree.insert("", "end", values=(
                        result["asr_file"],
                        result["ref_file"],
                        result["asr_chars"],
                        result["ref_chars"],
                        f"{result['accuracy']:.4f}",
                        "是" if filter_fillers else "否",
                        used_tokenizer
                    ))
                    
                except Exception as e:
                    messagebox.showerror("错误", f"处理文件时出错: {str(e)}")
                    
        except Exception as e:
            messagebox.showerror("错误", f"初始化分词器失败: {str(e)}")

    def read_file_with_multiple_encodings(self, file_path):
        """
        尝试使用多种编码方式读取文件内容
        
        Args:
            file_path (str): 文件路径
            
        Returns:
            str: 文件内容
            
        Raises:
            Exception: 如果所有编码方式都失败则抛出异常
        """
        # 尝试的编码格式列表
        encodings = ['utf-8', 'gbk', 'gb2312', 'gb18030', 'ansi']
        
        # 存储可能的异常
        errors = []
        
        # 依次尝试不同的编码
        for encoding in encodings:
            try:
                # 对于 'ansi'，我们使用系统默认编码
                if encoding == 'ansi':
                    with open(file_path, 'r') as f:
                        content = f.read().strip()
                else:
                    with open(file_path, 'r', encoding=encoding) as f:
                        content = f.read().strip()
                return content
            except UnicodeDecodeError as e:
                # 记录错误但继续尝试其他编码
                errors.append((encoding, str(e)))
                continue
        
        # 如果所有编码都失败，抛出异常
        error_msg = "无法解码文件，尝试了以下编码：\n"
        for encoding, error in errors:
            error_msg += f"- {encoding}: {error}\n"
        raise Exception(error_msg)

    def export_results(self):
        if not self.results:
            messagebox.showinfo("提示", "没有可导出的结果！")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt"), ("CSV文件", "*.csv")],
            title="导出结果"
        )
        
        if not file_path:
            return
            
        try:
            if file_path.endswith('.csv'):
                # 导出为CSV格式
                df = pd.DataFrame(self.results)
                # 只保留基本字段和过滤状态以及分词器信息
                df = df[['asr_file', 'ref_file', 'asr_chars', 'ref_chars', 'accuracy', 'filter_fillers', 'tokenizer']]
                # 将过滤状态标记为更易读的文本
                df['filter_fillers'] = df['filter_fillers'].apply(lambda x: "是" if x else "否")
                # 重命名列名
                df.columns = ['ASR文件', '标注文件', 'ASR字数', '标注字数', '字准确率', '是否过滤语气词', '分词器']
                df.to_csv(file_path, index=False, encoding='utf-8')
            else:
                # 导出为TXT格式
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("原始文件\t标注文件\tASR字数\t标注字数\t字准确率\t是否过滤语气词\t分词器\n")
                    for result in self.results:
                        filter_status = "是" if result.get('filter_fillers', False) else "否"
                        tokenizer_used = result.get('tokenizer', 'unknown')
                        f.write(f"{result['asr_file']}\t{result['ref_file']}\t"
                                f"{result['asr_chars']}\t{result['ref_chars']}\t"
                                f"{result['accuracy']:.4f}\t{filter_status}\t{tokenizer_used}\n")
            
            messagebox.showinfo("成功", f"结果已导出到 {file_path}")
        
        except Exception as e:
            messagebox.showerror("错误", f"导出结果时出错: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ASRComparisonTool(root)
    root.mainloop()