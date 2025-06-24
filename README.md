# ASR Character Accuracy Comparison Tool

A Python-based tool for batch comparing character accuracy rates between ASR (Automatic Speech Recognition) transcription results and standard text, with multi-tokenizer support.

## ✨ Core Features

### 🎯 Multi-Tokenizer Support
- **Jieba Tokenizer**: Default choice, high-speed segmentation, suitable for daily use
- **THULAC Tokenizer**: Developed by Tsinghua University, high-precision segmentation, suitable for professional analysis
- **HanLP Tokenizer**: Deep learning model, highest precision, suitable for research environments

### 🚀 Smart Features
- ✅ **Automatic Tokenizer Detection**: Detects installed tokenizers at startup
- ✅ **Smart Fallback Mechanism**: Automatically fallback to jieba when tokenizers are unavailable
- ✅ **Real-time Status Display**: GUI shows tokenizer status and version information
- ✅ **Dependency-free Demo**: Complete architecture demonstration without additional dependencies

### 📊 Advanced Functions
- Batch import ASR transcription result documents and standard annotation documents
- Drag-and-drop to establish one-to-one correspondence between ASR results and annotation files
- Automatically calculate Character Accuracy Rate
- Count document character information
- Support exporting statistical results in TXT or CSV format
- Support multiple text encodings (UTF-8, GBK, GB2312, GB18030, ANSI)
- **Filler word filtering**: Optional filtering of filler words like "嗯", "啊"
- **Optimized user interface**: Larger result display area, more user-friendly experience

## 📦 Installation & Dependencies

### Quick Experience (Recommended)
```bash
# Experience complete architecture without any dependencies
cd cer-matchingtools
python3 tests/test_architecture_demo.py
```

### Full Installation
```bash
# Install core dependencies
pip install -r requirements.txt

# Optional: Install other tokenizers
pip install thulac    # Install THULAC tokenizer
pip install hanlp     # Install HanLP tokenizer (large, first use requires model download)
```

#### Dependency Description
**Core Dependencies (Required):**
- `jieba>=0.42.1`: Default Chinese tokenizer
- `jiwer>=2.5.0`: Text preprocessing and error rate calculation
- `pandas>=1.3.0`: Data processing and export
- `python-Levenshtein>=0.12.2`: Efficient edit distance calculation

**Optional Dependencies:**
- `thulac>=0.2.0`: THULAC high-precision tokenizer
- `hanlp>=2.1.0`: HanLP deep learning tokenizer

## 🎮 Usage

### 1. GUI Mode (Recommended)

```bash
python3 src/main_with_tokenizers.py
```

#### Operation Steps:
1. **Select Tokenizer**: Choose the desired tokenizer in the top dropdown
2. **Check Status**: Confirm tokenizer status shows green ✓
3. **Import Files**:
   - Left: Click "Select ASR Files" to batch import ASR transcription results
   - Right: Click "Select Annotation Files" to batch import standard annotation files
4. **Establish Correspondence**: Adjust file order by drag-and-drop
5. **Configure Options**: Check "Filter Filler Words" as needed
6. **Calculate Statistics**: Click "Start Calculation" button
7. **View Results**: Result table shows detailed statistics
8. **Export Data**: Click "Export Results" to save as file

#### Interface Function Description:
- **Tokenizer Selection Area**: Select and manage tokenizers
- **File Selection Area**: Import and manage file lists
- **Control Area**: Statistics button and option configuration
- **Result Display Area**: Detailed statistical result table

### 2. Architecture Demo Mode

```bash
python3 tests/test_architecture_demo.py
```

This demo program:
- 📚 **No external dependencies required**
- 🔬 **Shows complete architecture design**
- ⚡ **Quick function verification**
- 🧪 **Suitable for development testing**

### 3. Command-Line Tool Mode

Compare two specified files:

```bash
# Basic usage
python3 src/check_accuracy.py --ref reference_file.txt --asr asr_result.txt

# Show detailed error analysis
python3 src/check_accuracy.py --ref reference_file.txt --asr asr_result.txt --details

# Filter filler words
python3 src/check_accuracy.py --ref reference_file.txt --asr asr_result.txt --filter-fillers
```

## 🎯 Tokenizer Selection Guide

### Jieba Tokenizer
- **Performance**: ⚡ High Speed
- **Accuracy**: ⭐⭐⭐ Medium
- **Use Cases**: Daily batch processing, quick verification
- **Advantages**: Fast speed, low resource usage, good compatibility

### THULAC Tokenizer
- **Performance**: ⚡⚡ Medium Speed
- **Accuracy**: ⭐⭐⭐⭐ High Precision
- **Use Cases**: Professional analysis, high quality requirements
- **Advantages**: Developed by Tsinghua University, academic standards, accurate POS tagging

### HanLP Tokenizer
- **Performance**: ⚡ Slower (first use requires model download)
- **Accuracy**: ⭐⭐⭐⭐⭐ Highest Precision
- **Use Cases**: Research environments, highest precision requirements
- **Advantages**: Deep learning models, multi-task support, continuous updates

## 📐 Character Accuracy Calculation Method

Uses the complement of Character Error Rate (CER):

```
Character Accuracy = 1 - CER = 1 - (S + D + I) / N
```

Where:
- **S**: Number of substitution errors
- **D**: Number of deletion errors
- **I**: Number of insertion errors
- **N**: Total number of characters in the standard text

### 🔧 Improved Calculation Process

1. **Tokenization Preprocessing**: Use selected tokenizer for text segmentation
2. **Text Normalization**: Process full/half-width characters, unify numerical expressions
3. **Filler Word Filtering (Optional)**: Filter filler words like "嗯", "啊", "呢"
4. **Character Position Localization**: Precisely locate each character's position in original text
5. **Edit Distance Calculation**: Use Levenshtein distance algorithm
6. **Error Analysis**: Identify substitution, deletion, insertion errors with visualization

## 📁 Project Structure

```
cer-matchingtools/
├── src/
│   ├── text_tokenizers/           # 🧠 Core tokenizer module
│   │   ├── __init__.py            # Module export interface
│   │   └── tokenizers/            # Tokenizer implementations
│   │       ├── base.py            # Abstract base class
│   │       ├── factory.py         # Factory class
│   │       ├── jieba_tokenizer.py # Jieba implementation
│   │       ├── thulac_tokenizer.py# THULAC implementation
│   │       └── hanlp_tokenizer.py # HanLP implementation
│   ├── main_with_tokenizers.py    # 🎨 New GUI interface
│   ├── asr_metrics_refactored.py  # 📊 Refactored calculation engine
│   └── v0.1.0/                    # 📦 Original version backup
├── tests/
│   └── test_architecture_demo.py  # 🔬 Architecture demo program
├── docs/                          # 📚 Detailed documentation
├── demo/                          # 🧪 Example files
├── requirements.txt               # 📦 Dependency management
└── QUICK_START.md                 # 🚀 Quick start guide
```

## 🔧 Troubleshooting

### Common Issues

**Q: How to handle unavailable tokenizers?**
A: Check if corresponding dependencies are installed:
```bash
pip install thulac    # Install THULAC
pip install hanlp     # Install HanLP
```

**Q: Why is HanLP slow on first use?**
A: HanLP needs to download deep learning models, first use requires patience. Recommend using in good network environment.

**Q: How to verify architecture design?**
A: Run the architecture demo program:
```bash
python3 tests/test_architecture_demo.py
```

**Q: How to choose the right tokenizer?**
A: Refer to tokenizer selection guide, choose based on speed and accuracy needs:
- For speed: Choose Jieba
- For balance: Choose THULAC
- For precision: Choose HanLP

## 🆕 Version Features

### Current Version Highlights
- 🎯 **Multi-tokenizer Architecture**: Support for three mainstream Chinese tokenizers
- 🚀 **Smart Switching**: Automatic detection and graceful fallback
- 🎨 **Optimized Interface**: More user-friendly experience
- 🔬 **Architecture Demo**: Complete feature demonstration without dependencies
- 📊 **Detailed Statistics**: Enhanced result display and analysis

### Backward Compatibility
- ✅ Maintain original API interfaces unchanged
- ✅ Default to jieba tokenizer
- ✅ Support original file formats and encodings

## 📞 Technical Support

For issues, please check:
- `QUICK_START.md` - Quick start guide
- `docs/project_development_summary.md` - Detailed development summary
- `docs/test_cases.md` - Test case documentation
- `tests/test_architecture_demo.py` - Architecture demo code

## 📄 License

This project is released under an open source license, see `LICENSE` file for details.

---

🎉 **Experience multi-tokenizer switching now to improve ASR character accuracy analysis precision and efficiency!** 