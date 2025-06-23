# ASR字准统计工具 - 项目结构

## 📁 项目目录结构

```
cer-matchingtools/
├── 📂 src/                              # 核心源代码目录
│   ├── 📄 main_with_tokenizers.py       # GUI主程序（启动入口）
│   ├── 📄 asr_metrics_refactored.py     # ASR度量计算引擎
│   ├── 📂 text_tokenizers/              # 分词器模块
│   │   ├── 📄 __init__.py               # 分词器统一接口
│   │   └── ...                          # 各种分词器实现
│   ├── 📂 v0.1.0/                      # 历史版本代码
│   └── 📂 __pycache__/                  # Python缓存目录
│
├── 📂 tests/                            # 测试代码目录
│   ├── 📄 run_tests.py                  # 测试运行器
│   ├── 📄 pytest.ini                   # pytest配置
│   ├── 📄 test_cases.md                 # 测试用例文档
│   ├── 📄 test_plan.md                  # 测试计划文档
│   ├── 📄 requirements-test.txt         # 测试依赖
│   ├── 📄 test_hanlp_integration.py     # HanLP集成测试
│   ├── 📄 hanlp_tok_only.py            # HanLP分词专用测试
│   ├── 📄 hanlp_tokenizer_optimized.py # HanLP优化版测试
│   ├── 📄 performance_test.py           # 性能测试
│   ├── 📄 simple_test.py               # 简单功能测试
│   ├── 📄 test_system.py               # 系统集成测试
│   ├── 📄 test_architecture_demo.py    # 架构演示测试
│   └── 📄 test_tokenizers.py           # 分词器单元测试
│
├── 📂 docs/                             # 文档目录
│   ├── 📄 project_structure.md          # 项目结构说明（本文档）
│   ├── 📄 business_sequence_diagram.md  # 业务流程图
│   ├── 📄 hanlp_solution_analysis.md   # HanLP解决方案分析
│   ├── 📄 project_development_summary.md # 项目开发总结
│   ├── 📄 HANLP_INTEGRATION_SUCCESS.md # HanLP集成成功报告
│   ├── 📄 开发测试用例.md               # 中文测试用例
│   └── 📸 *.png                         # 项目相关图片
│
├── 📂 test/                            # 测试数据目录
│   └── ...                             # 测试用的数据文件
│
├── 📄 requirements.txt                  # 项目依赖
├── 📄 .gitignore                       # Git忽略文件配置
├── 📄 QUICK_START.md                   # 快速开始指南
└── 📄 README.md                        # 项目说明文档
```

## 🎯 核心模块说明

### 📂 src/ - 核心源代码

#### 主程序模块
- **`main_with_tokenizers.py`** - GUI主程序
  - 提供用户界面
  - 文件选择和管理
  - 分词器选择
  - CER计算结果展示

#### 计算引擎
- **`asr_metrics_refactored.py`** - ASR度量计算引擎
  - 支持多种分词器
  - CER (字错误率) 计算
  - WER (词错误率) 计算
  - 文本预处理和优化

#### 分词器模块
- **`text_tokenizers/`** - 分词器统一框架
  - `__init__.py` - 统一接口和工厂类
  - `JiebaTokenizer` - Jieba分词器
  - `ThulacTokenizer` - THULAC分词器  
  - `HanlpTokenizer` - HanLP分词器（新增）

### 📂 tests/ - 测试代码

#### 测试运行和配置
- **`run_tests.py`** - 统一测试运行器
- **`pytest.ini`** - pytest配置文件
- **`requirements-test.txt`** - 测试专用依赖

#### 测试文档
- **`test_cases.md`** - 详细测试用例
- **`test_plan.md`** - 测试计划和策略

#### 功能测试
- **`test_hanlp_integration.py`** - HanLP集成完整性测试
- **`simple_test.py`** - 基础功能快速测试  
- **`test_system.py`** - 系统级集成测试

#### 专项测试
- **`hanlp_tok_only.py`** - HanLP分词专用功能测试
- **`hanlp_tokenizer_optimized.py`** - HanLP优化版本测试
- **`performance_test.py`** - 性能基准测试
- **`test_tokenizers.py`** - 分词器单元测试
- **`test_architecture_demo.py`** - 架构演示和验证

### 📂 docs/ - 项目文档

#### 技术文档
- **`business_sequence_diagram.md`** - 业务流程和时序图
- **`hanlp_solution_analysis.md`** - HanLP技术方案分析
- **`HANLP_INTEGRATION_SUCCESS.md`** - HanLP集成成功报告

#### 项目管理
- **`project_development_summary.md`** - 开发历程总结
- **`project_structure.md`** - 项目结构说明（本文档）

## 🚀 使用方式

### 启动主程序
```bash
cd src
python main_with_tokenizers.py
```

### 运行测试
```bash
cd tests
python run_tests.py                    # 运行所有测试
python test_hanlp_integration.py       # 仅测试HanLP集成
python simple_test.py                  # 快速功能验证
```

### 性能测试
```bash
cd tests  
python performance_test.py             # 性能基准测试
```

## 🎯 分词器支持

| 分词器 | 精度 | 速度 | 模型大小 | 状态 |
|--------|------|------|----------|------|
| **jieba** | 中等 | 极快 | 5MB | ✅ 可用 |
| **thulac** | 高 | 快 | 50MB | ✅ 可用 |
| **hanlp** | 最高(98.36%) | 中等 | 45MB | ✅ 可用 |

## 📈 项目特性

### ✅ 已实现功能
1. **多分词器支持** - jieba、THULAC、HanLP三种分词器
2. **高精度计算** - CER字错误率计算
3. **性能优化** - 缓存机制、单例模式
4. **GUI界面** - 用户友好的图形界面
5. **本地化部署** - 模型本地缓存，无需网络

### 🔧 技术架构
- **模块化设计** - 清晰的分层架构
- **工厂模式** - 统一的分词器管理
- **缓存优化** - 避免重复初始化
- **异常处理** - 完善的错误处理机制

### 📊 性能表现
- **HanLP精度** - F1分数达98.36%（业界最高）
- **启动速度** - 优化后秒级启动
- **内存占用** - 合理的内存使用
- **用户体验** - 界面响应迅速，无卡顿

---

**项目状态**: ✅ 生产就绪  
**最后更新**: 2024年（HanLP集成完成后）  
**维护状态**: 🔥 活跃开发 