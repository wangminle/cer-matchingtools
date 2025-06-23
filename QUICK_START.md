# ASR字准确率对比工具 - 快速开始指南

## 🚀 快速体验

### 1. 运行架构演示（推荐）
```bash
# 无需安装任何依赖，直接体验完整架构
cd cer-matchingtools
python3 src/test_architecture_demo.py
```

### 2. 安装完整版本
```bash
# 安装基础依赖
pip install -r requirements.txt

# 可选：安装其他分词器
pip install thulac hanlp

# 运行完整版应用
python3 src/main_with_tokenizers.py
```

## 📁 项目结构
```
cer-matchingtools/
├── src/
│   ├── tokenizers/                    # 🧠 分词器核心模块
│   ├── main_with_tokenizers.py        # 🎨 新版GUI界面
│   ├── asr_metrics_refactored.py      # 📊 重构后的计算模块
│   └── test_architecture_demo.py      # 🔬 架构演示程序
├── docs/                              # 📚 文档目录
├── requirements.txt                   # 📦 依赖管理
└── QUICK_START.md                     # 🚀 快速开始
```

## 🎯 核心功能

### 三种分词器支持
- **Jieba**: 默认选择，高速分词
- **THULAC**: 高精度分词，清华大学开发
- **HanLP**: 深度学习分词，最高精度

### 智能特性
- ✅ 自动检测分词器可用性
- ✅ 不可用时自动降级到jieba
- ✅ GUI实时显示分词器状态
- ✅ 详细的错误信息提示

## 💡 使用建议

### 分词器选择指南
- **日常使用**: 选择jieba（速度快）
- **高精度需求**: 选择THULAC（精度高）
- **科研环境**: 选择HanLP（最高精度）

### 依赖安装顺序
1. 先安装基础依赖（jieba, jiwer等）
2. 再根据需要安装其他分词器
3. 应用会自动适配可用的分词器

## 🔧 故障排除

### 常见问题
1. **分词器显示不可用**：检查对应依赖是否安装
2. **HanLP首次使用慢**：需要下载深度学习模型
3. **SSL证书错误**：使用演示程序体验架构设计

### 演示程序优势
- 无依赖要求
- 完整功能展示
- 快速验证设计
- 适合开发测试

## 📞 技术支持

如有问题，请查看：
- `docs/project_development_summary.md` - 详细开发总结
- `docs/test_cases.md` - 测试用例说明
- `src/test_architecture_demo.py` - 架构演示代码

---
🎉 **开始探索ASR字准确率对比工具的分词器切换功能吧！** 