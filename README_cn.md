# ASR字准确率对比工具

基于Python的ASR（自动语音识别）字准确率批量对比工具，支持多种中文分词器切换。

## ✨ 核心特性

### 🎯 多分词器支持
- **Jieba分词器**：默认选择，高速分词，适合日常使用
- **THULAC分词器**：清华大学开发，高精度分词，适合专业分析
- **HanLP分词器**：深度学习模型，最高精度，适合科研环境

### 🚀 智能特性
- ✅ **自动检测分词器可用性**：启动时检测已安装的分词器
- ✅ **智能降级机制**：分词器不可用时自动回退到jieba
- ✅ **实时状态显示**：GUI界面显示分词器状态和版本信息
- ✅ **无依赖演示**：提供完整的架构演示程序，无需安装额外依赖

### 📊 高级功能
- 批量导入ASR转写结果文档和标准标注文档
- 拖拽建立ASR结果和标注文件的一一对应关系
- 自动计算字准确率（Character Accuracy Rate）
- 统计文档字数信息
- 支持导出统计结果为TXT或CSV格式
- 支持多种文本编码（UTF-8、GBK、GB2312、GB18030、ANSI）
- **语气词过滤功能**：可选择过滤"嗯"、"啊"等语气词
- **优化的用户界面**：更大的结果展示区域，更友好的操作体验

## 📦 安装与依赖

### 安装依赖
```bash
# 安装核心依赖
pip install -r dev/src/requirements.txt

# 可选：安装其他分词器
pip install thulac    # 安装THULAC分词器
pip install hanlp     # 安装HanLP分词器（较大，首次使用需下载模型）
```

#### 依赖说明
**核心依赖（必需）：**
- `jieba>=0.42.1`：默认中文分词器
- `jiwer>=2.5.0`：文本预处理和错误率计算
- `pandas>=1.3.0`：数据处理和导出
- `python-Levenshtein>=0.12.2`：高效编辑距离计算

**可选依赖：**
- `thulac>=0.2.0`：THULAC高精度分词器
- `hanlp>=2.1.0`：HanLP深度学习分词器

## 🎮 使用方法

### 1. GUI界面方式（推荐）

```bash
python3 dev/src/main_with_tokenizers.py
```

#### 操作步骤：
1. **选择分词器**：在顶部下拉框中选择所需的分词器
2. **查看状态**：确认分词器状态显示为绿色✓，点击"分词器信息"查看详细信息
3. **导入文件**：
   - 左侧：点击"选择ASR文件"批量导入ASR转写结果
   - 右侧：点击"选择标注文件"批量导入标准标注文件
4. **建立对应关系**：通过拖拽调整文件顺序
5. **配置选项**：根据需要勾选"语气词过滤"
6. **计算统计**：点击"开始统计"按钮
7. **查看结果**：结果表格显示详细统计信息，包括使用的分词器类型
8. **导出数据**：点击"导出结果"保存为文件

#### 界面功能说明：
- **分词器选择区域**：选择和管理分词器
- **文件选择区域**：导入和管理文件列表
- **控制区域**：统计按钮和选项配置
- **结果展示区域**：详细的统计结果表格

### 2. 批量处理模式

对于批量文件处理，直接运行GUI界面：
```bash
python3 dev/src/main_with_tokenizers.py
```
然后按照界面操作步骤进行批量导入和处理。

## 🎯 分词器选择指南

### Jieba分词器
- **性能**：⚡ 高速
- **精度**：⭐⭐⭐ 中等
- **适用场景**：日常批量处理、快速验证
- **优势**：速度快、占用资源少、兼容性好

### THULAC分词器
- **性能**：⚡⚡ 中等速度
- **精度**：⭐⭐⭐⭐ 高精度
- **适用场景**：专业分析、高质量要求
- **优势**：清华大学开发、学术标准、词性标注准确

### HanLP分词器
- **性能**：⚡ 较慢（首次使用需下载模型）
- **精度**：⭐⭐⭐⭐⭐ 最高精度
- **适用场景**：科研环境、最高精度要求
- **优势**：深度学习模型、多任务支持、持续更新

## 📐 字准确率计算方法

使用字符错误率（CER）的补集：

```
字准确率 = 1 - CER = 1 - (S + D + I) / N
```

其中：
- **S**：替换错误数
- **D**：删除错误数  
- **I**：插入错误数
- **N**：标准文本中的字符总数

### 🔧 改进的计算流程

1. **分词预处理**：使用选定的分词器进行文本分词
2. **文本标准化**：处理全/半角字符、统一数字表达
3. **语气词过滤（可选）**：过滤"嗯"、"啊"、"呢"等语气词
4. **字符位置定位**：精确定位每个字符在原文中的位置
5. **编辑距离计算**：使用Levenshtein距离算法
6. **错误分析**：识别替换、删除、插入错误并提供可视化

## 📁 项目结构

```
cer-matchingtools/
├── dev/
│   ├── src/                           # 🧠 核心源代码
│   │   ├── text_tokenizers/           # 分词器模块
│   │   │   ├── __init__.py            # 模块导出接口
│   │   │   └── tokenizers/            # 分词器实现
│   │   │       ├── base.py            # 抽象基类
│   │   │       ├── factory.py         # 工厂类
│   │   │       ├── jieba_tokenizer.py # Jieba实现
│   │   │       ├── thulac_tokenizer.py# THULAC实现
│   │   │       └── hanlp_tokenizer.py # HanLP实现
│   │   ├── main_with_tokenizers.py    # 🎨 GUI界面主程序
│   │   ├── asr_metrics_refactored.py  # 📊 计算引擎
│   │   └── requirements.txt           # 📦 依赖管理
│   └── output/                        # 开发过程输出文件
├── docs/                              # 📚 技术文档
├── tests/                             # 🧪 测试文件和脚本
├── release/                           # 📦 发布包
├── ref/                               # 📋 参考资料
│   ├── demo/                          # 示例文件
│   └── logo/                          # 项目logo
└── README.md                          # 📋 项目说明
```

## 🔧 故障排除

### 常见问题

**Q: 分词器显示不可用怎么办？**
A: 检查对应依赖是否安装：
```bash
pip install thulac    # 安装THULAC
pip install hanlp     # 安装HanLP
```

**Q: HanLP首次使用很慢？**
A: HanLP需要下载深度学习模型，首次使用需要耐心等待。建议在网络良好的环境下使用。

**Q: 如何快速验证功能？**
A: 使用ref/demo目录中的示例文件测试：
```bash
# 使用GUI界面导入ref/demo目录中的示例文件进行测试
python3 dev/src/main_with_tokenizers.py
```

**Q: 如何选择合适的分词器？**
A: 参考分词器选择指南，根据速度和精度需求选择：
- 追求速度：选择Jieba
- 平衡性能：选择THULAC  
- 追求精度：选择HanLP

## 🆕 版本特性

### 当前版本亮点
- 🎯 **多分词器架构**：支持三种主流中文分词器
- 🚀 **智能切换**：自动检测和优雅降级
- 🎨 **优化界面**：更友好的用户体验
- 📊 **详细统计**：增强的结果展示和分析
- 🔧 **拖拽排序**：直观的文件对应关系管理

### 向后兼容
- ✅ 保持原有API接口不变
- ✅ 默认使用jieba分词器
- ✅ 支持原有文件格式和编码

## 📞 技术支持

如有问题，请查看：
- `ref/demo/` 目录 - 包含示例文件用于测试
- `docs/` 目录 - 详细的技术文档
- `dev/src/requirements.txt` - 完整的依赖列表

## 📄 许可证

本项目基于开源许可证发布，详见 `LICENSE` 文件。

---

🎉 **立即体验多分词器切换功能，提升ASR字准确率分析的精度和效率！** 