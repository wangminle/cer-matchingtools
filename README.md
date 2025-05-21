# ASR Character Accuracy Comparison Tool

This is a Python tool for batch comparing the character accuracy rate between ASR (Automatic Speech Recognition) transcription results and standard text.

## Features

- Batch import ASR transcription result documents and standard annotation documents
- Establish one-to-one correspondence between ASR results and annotation files via drag-and-drop
- Automatically calculate Character Accuracy Rate
- Count document character information
- Support exporting statistical results in TXT or CSV format
- Support multiple text encodings (UTF-8, GBK, GB2312, GB18030, ANSI)
- Provide a default window size of 800x600, supports window maximization
- **New: Chinese text preprocessing based on jieba word segmentation**
- **New: Precise Chinese character position localization and error analysis**
- **New: Chinese text normalization (full/half-width conversion, number unification, etc.)**
- **New: Filler word filtering function, option to include filler words like "嗯", "啊" in CER calculation**
- **New: Optimized user interface layout, larger result display area**

## Install Dependencies

Install dependencies using pip:

```bash
pip install -r requirements.txt
```

Main dependencies:
- jiwer>=2.5.0: Used to calculate character/word error rate
- pandas>=1.3.5: Used for data processing and export
- tk>=0.1.0: Provides GUI interface support
- **jieba>=0.42.1: Chinese word segmentation library**
- **python-Levenshtein>=0.12.2: Calculate edit distance**

## Usage

This tool offers three different ways to use it:

### 1. GUI Mode (Recommended)

```bash
python src/main.py
```

Steps:
1. Click the "Select ASR Files" button on the left side of the interface to batch import ASR transcription result files.
2. Click the "Select Annotation Files" button on the right side of the interface to batch import standard annotation files.
3. If necessary, adjust the file order by drag-and-drop to establish correspondence.
4. Check the "Filter Filler Words" option as needed (hover over "?" for detailed explanation).
5. Click the "Start Calculation" button to calculate character accuracy.
6. View the results table, including file name, character count, accuracy, and filter status information.
7. Click the "Export Results" button to save the results as a TXT or CSV file.

### 2. Example Test Mode

Run the built-in example to see the character accuracy calculation function:

```bash
python example_test.py
```

This will demonstrate:
- Character accuracy calculation example for Chinese text
- Character accuracy calculation example for English text
- Example of reading text from files and calculating character accuracy
- **New: Character accuracy calculation example for complex Chinese text**

### 3. Command-Line Tool Mode

Directly compare two specified files:

```bash
python check_accuracy.py --ref <reference_file_path> --asr <asr_result_file_path> [options]
```

Available options:
- `--details`: Display detailed error analysis, including error highlighting and character position information.
- `--filter-fillers`: Filter filler words (e.g., "嗯", "啊", "呢"), not including them in CER calculation.

Example:
```bash
# Basic usage
python check_accuracy.py --ref ref_text1.txt --asr asr_result1.txt

# Display detailed error analysis
python check_accuracy.py --ref ref_text1.txt --asr asr_result1.txt --details

# Filter filler words for CER calculation
python check_accuracy.py --ref ref_text1.txt --asr asr_result1.txt --filter-fillers
```

The command-line tool will display detailed evaluation results, including character accuracy, error rate, substitution/deletion/insertion error counts, etc.

## Character Accuracy Calculation Method

The tool uses the complement of Character Error Rate (CER), calculated as:

```
Character Accuracy = 1 - CER = 1 - (S + D + I) / N
```

Where:
- S: Number of substitution errors
- D: Number of deletion errors
- I: Number of insertion errors
- N: Total number of characters in the standard text

**Improved Chinese Character Accuracy Calculation Process:**

1.  **Word Segmentation Preprocessing**: Use jieba for Chinese word segmentation to improve understanding of Chinese semantics.
2.  **Text Normalization**: Process full/half-width characters, unify numerical expressions, remove punctuation, etc.
3.  **Filler Word Filtering (Optional)**: Filter filler words like "嗯", "啊", "呢" to make CER more accurately reflect actual semantic content.
4.  **Character Position Localization**: Use `jieba.tokenize` to get the precise position of each character in the original text.
5.  **Edit Distance Calculation**: Use the Levenshtein distance algorithm to calculate character-level edit distance.
6.  **Error Analysis and Highlighting**: Identify substitution, deletion, and insertion errors, and provide visual error highlighting.

## UI Layout Optimization

The latest version has optimized the UI layout:

1.  **Compact File Selection Area**: Reduced the height of the file list display area, making the upper part more compact.
2.  **Enlarged Result Display Area**: The result display table below has increased from 8 rows to 12 rows to show more results.
3.  **Improved Control Area**: The "Start Calculation" button and "Filter Filler Words" checkbox are placed on the same line for a more reasonable layout.
4.  **Filler Word Filtering Function Hint**: Added a hover hint for users to understand the function's purpose.
5.  **Intelligent Layout Allocation**: The upper area has a fixed size, and the lower result area can automatically expand with window adjustment.

## Project Structure

- `src/main.py`: Main program, including GUI interface and main functions.
- `src/utils.py`: Utility class, including functions related to character accuracy calculation.
- `example_test.py`: Example test script.
- `check_accuracy.py`: Command-line comparison tool.
- `requirements.txt`: Project dependency list.
- `docs/UI-definition.md`: User interface definition document.

## Notes

- Supported file formats: Plain text files (.txt)
- File encoding: Supports UTF-8, GBK, GB2312, GB18030, and system default encoding (ANSI).
- Character accuracy calculation is character-level, especially suitable for languages like Chinese without clear word boundaries.
- **Jieba word segmentation may take a few seconds to build a dictionary cache 처음 로드될 때.**
- **For domain-specific text, consider adding a custom dictionary via `jieba.load_userdict()`**
- **The filler word filtering function recognizes 20 common Chinese filler words by default and also identifies "filler words (y)" based on jieba's part-of-speech tagging.** 