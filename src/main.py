import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import pandas as pd
import jiwer
from functools import partial
from utils import ASRMetrics

class ASRComparisonTool:
    def __init__(self, root):
        self.root = root
        self.root.title("ASR字准确率对比工具")
        self.root.geometry("800x600")
        # 设置窗口大小不可调整，但支持最大化
        self.root.resizable(True, True)
        # 设置minsize，确保窗口不会小于800x600
        self.root.minsize(800, 600)
        
        # 存储文件列表和配对信息
        self.asr_files = []
        self.ref_files = []
        self.file_pairs = []
        self.results = []
        
        # 创建主框架分为上下两部分
        self.top_frame = ttk.Frame(root)
        self.top_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.bottom_frame = ttk.Frame(root)
        self.bottom_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 初始化UI组件
        self._init_ui()
    
    def _init_ui(self):
        # 上半部分 - 文件选择区域
        # 创建包含左右两帧和底部按钮的上半部分框架
        self.file_area_frame = ttk.Frame(self.top_frame)
        self.file_area_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.left_frame = ttk.LabelFrame(self.file_area_frame, text="ASR转换结果文件")
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.right_frame = ttk.LabelFrame(self.file_area_frame, text="标注文件")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # ASR文件选择按钮和列表
        self.asr_btn = ttk.Button(self.left_frame, text="选择ASR文件", command=self.select_asr_files)
        self.asr_btn.pack(pady=5)
        
        # 创建一个frame来容纳canvas，以便控制高度
        self.asr_canvas_frame = ttk.Frame(self.left_frame)
        self.asr_canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 设置canvas的高度
        self.asr_canvas = tk.Canvas(self.asr_canvas_frame, bg="white", height=150)
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
        
        # 设置canvas的高度
        self.ref_canvas = tk.Canvas(self.ref_canvas_frame, bg="white", height=150)
        self.ref_canvas.pack(fill=tk.BOTH, expand=True)
        self.ref_canvas.bind("<ButtonPress-1>", self.on_press)
        self.ref_canvas.bind("<B1-Motion>", self.on_drag)
        self.ref_canvas.bind("<ButtonRelease-1>", self.on_release)
        
        # 统计按钮 - 单独放置在顶部框架内，与文件区域分开
        self.calculate_btn = ttk.Button(self.top_frame, text="开始统计", command=self.calculate_accuracy, width=15)
        self.calculate_btn.pack(pady=10)
        
        # 下半部分 - 结果显示区域
        self.result_frame = ttk.LabelFrame(self.bottom_frame, text="字准确率统计结果")
        self.result_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建一个frame来容纳treeview，以便控制高度
        self.result_tree_frame = ttk.Frame(self.result_frame)
        self.result_tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 结果展示表格，设置高度
        columns = ("原始文件", "标注文件", "ASR字数", "标注字数", "字准确率")
        self.result_tree = ttk.Treeview(self.result_tree_frame, columns=columns, show="headings", height=8)
        for col in columns:
            self.result_tree.heading(col, text=col)
            self.result_tree.column(col, width=150, anchor="center")
        
        self.result_tree.pack(fill=tk.BOTH, expand=True)
        
        # 导出按钮
        self.export_btn = ttk.Button(self.bottom_frame, text="导出结果", command=self.export_results, width=15)
        self.export_btn.pack(pady=10)
        
        # 设置拖拽变量
        self.drag_data = {"x": 0, "y": 0, "item": None, "canvas": None}
    
    def select_asr_files(self):
        files = filedialog.askopenfilenames(title="选择ASR文件", filetypes=[("文本文件", "*.txt")])
        if files:
            self.asr_files = list(files)
            self.update_canvas_items(self.asr_canvas, self.asr_files)
    
    def select_ref_files(self):
        files = filedialog.askopenfilenames(title="选择标注文件", filetypes=[("文本文件", "*.txt")])
        if files:
            self.ref_files = list(files)
            self.update_canvas_items(self.ref_canvas, self.ref_files)
    
    def update_canvas_items(self, canvas, file_list):
        canvas.delete("all")
        y_pos = 10
        for i, file_path in enumerate(file_list):
            file_name = os.path.basename(file_path)
            item_id = canvas.create_rectangle(10, y_pos, canvas.winfo_width()-10, y_pos+30, 
                                            fill="lightblue", tags=f"file_{i}")
            canvas.create_text(20, y_pos+15, text=file_name, anchor="w", tags=f"file_{i}")
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
        
        # 逐对计算字准确率
        for asr_file, ref_file in zip(sorted_asr_files, sorted_ref_files):
            try:
                # 读取文件内容
                asr_text = self.read_file_with_multiple_encodings(asr_file)
                ref_text = self.read_file_with_multiple_encodings(ref_file)
                
                # 使用ASRMetrics计算各项指标
                metrics = ASRMetrics.calculate_detailed_metrics(ref_text, asr_text)
                
                # 获取结果
                accuracy = metrics['accuracy']
                ref_chars = metrics['ref_length']
                asr_chars = metrics['hyp_length']
                
                result = {
                    "asr_file": os.path.basename(asr_file),
                    "ref_file": os.path.basename(ref_file),
                    "asr_chars": asr_chars,
                    "ref_chars": ref_chars,
                    "accuracy": accuracy,
                    "details": metrics  # 保存详细指标供后续使用
                }
                
                self.results.append(result)
                
                # 添加到结果表格
                self.result_tree.insert("", "end", values=(
                    result["asr_file"],
                    result["ref_file"],
                    result["asr_chars"],
                    result["ref_chars"],
                    f"{result['accuracy']:.4f}"
                ))
                
            except Exception as e:
                messagebox.showerror("错误", f"处理文件时出错: {str(e)}")
    
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
                # 只保留基本字段
                df = df[['asr_file', 'ref_file', 'asr_chars', 'ref_chars', 'accuracy']]
                df.to_csv(file_path, index=False, encoding='utf-8')
            else:
                # 导出为TXT格式
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("原始文件\t标注文件\tASR字数\t标注字数\t字准确率\n")
                    for result in self.results:
                        f.write(f"{result['asr_file']}\t{result['ref_file']}\t"
                                f"{result['asr_chars']}\t{result['ref_chars']}\t"
                                f"{result['accuracy']:.4f}\n")
            
            messagebox.showinfo("成功", f"结果已导出到 {file_path}")
        
        except Exception as e:
            messagebox.showerror("错误", f"导出结果时出错: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ASRComparisonTool(root)
    root.mainloop() 