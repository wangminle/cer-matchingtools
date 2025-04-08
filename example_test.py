#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
示例测试文件，展示如何使用ASRMetrics类计算字准确率
"""

# 修改导入语句，假设脚本从根目录运行
from src.utils import ASRMetrics
import os
import sys

def read_file_with_multiple_encodings(file_path):
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
            print(f"成功使用 {encoding} 编码读取文件 {file_path}")
            return content
        except UnicodeDecodeError as e:
            # 记录错误但继续尝试其他编码
            errors.append((encoding, str(e)))
            continue
    
    # 如果所有编码都失败，抛出异常
    error_msg = f"无法解码文件 {file_path}，尝试了以下编码：\n"
    for encoding, error in errors:
        error_msg += f"- {encoding}: {error}\n"
    raise Exception(error_msg)

def test_chinese_text():
    """测试中文文本的字准确率计算"""
    # 示例中文文本
    reference = "今天天气真不错，阳光明媚。"
    hypothesis = "今天天气真不错阳光明美"  # 缺少逗号，"媚"写成了"美"
    
    # 计算字准确率
    accuracy = ASRMetrics.calculate_accuracy(reference, hypothesis)
    print(f"中文字准确率: {accuracy:.4f}")
    
    # 计算字错误率
    cer = ASRMetrics.calculate_cer(reference, hypothesis)
    print(f"中文字错误率: {cer:.4f}")
    
    # 获取详细指标
    metrics = ASRMetrics.calculate_detailed_metrics(reference, hypothesis)
    print(f"详细指标: {metrics}")
    
    # 显示差异
    ref_highlight, hyp_highlight = ASRMetrics.highlight_errors(reference, hypothesis)
    print(f"标准文本(高亮错误): {ref_highlight}")
    print(f"ASR结果(高亮错误): {hyp_highlight}")
    
    print("\n===== 复杂中文文本测试 =====")
    # 更复杂的中文文本，包含各种常见ASR错误
    reference_complex = "北京大学是中国最著名的高等学府之一，创建于1898年，位于北京市海淀区，占地面积约3000亩。"
    hypothesis_complex = "北京大学是中国最著名的高登学府之一，创建与1898年，位于北京市海淀区，占地面积大约三千亩。"
    # 错误包括：
    # - "著" -> "登"（形近字）
    # - "于" -> "与"（近音字）
    # - "3000" -> "三千"（数字表达方式不同）
    # - "约" -> "大约"（多字）
    
    # 计算字准确率
    accuracy_complex = ASRMetrics.calculate_accuracy(reference_complex, hypothesis_complex)
    print(f"复杂中文字准确率: {accuracy_complex:.4f}")
    
    # 计算字错误率
    cer_complex = ASRMetrics.calculate_cer(reference_complex, hypothesis_complex)
    print(f"复杂中文字错误率: {cer_complex:.4f}")
    
    # 显示差异
    ref_highlight_complex, hyp_highlight_complex = ASRMetrics.highlight_errors(reference_complex, hypothesis_complex)
    print(f"标准文本(高亮错误): {ref_highlight_complex}")
    print(f"ASR结果(高亮错误): {hyp_highlight_complex}")

def test_english_text():
    """测试英文文本的字准确率计算"""
    # 示例英文文本
    reference = "The quick brown fox jumps over the lazy dog."
    hypothesis = "The quik brown fox jumped over the lazy dog."  # 拼写错误和时态错误
    
    # 计算字准确率
    accuracy = ASRMetrics.calculate_accuracy(reference, hypothesis)
    print(f"英文字准确率: {accuracy:.4f}")
    
    # 计算字错误率
    cer = ASRMetrics.calculate_cer(reference, hypothesis)
    print(f"英文字错误率: {cer:.4f}")
    
    # 计算词错误率（对英文更有意义）
    wer = ASRMetrics.calculate_wer(reference, hypothesis)
    print(f"英文词错误率: {wer:.4f}")

def test_filler_words_filtering():
    """测试过滤语气词的字准确率计算"""
    print("\n===== 语气词过滤测试 =====")
    
    # 示例含有语气词的文本
    reference = "嗯，今天啊，天气真不错呢，阳光明媚啊。"
    hypothesis = "今天啊天气真不错嗯阳光明美啊"  # 包含语气词，但位置不同，且有错误
    
    # 不过滤语气词的准确率计算
    accuracy_no_filter = ASRMetrics.calculate_accuracy(reference, hypothesis)
    print(f"不过滤语气词的字准确率: {accuracy_no_filter:.4f}")
    
    # 过滤语气词的准确率计算
    accuracy_with_filter = ASRMetrics.calculate_accuracy(reference, hypothesis, filter_fillers=True)
    print(f"过滤语气词后的字准确率: {accuracy_with_filter:.4f}")
    
    # 显示过滤前后的差异
    print("\n语气词过滤前：")
    ref_highlight, hyp_highlight = ASRMetrics.highlight_errors(reference, hypothesis)
    print(f"标准文本: {ref_highlight}")
    print(f"ASR结果: {hyp_highlight}")
    
    print("\n语气词过滤后：")
    ref_highlight_filtered, hyp_highlight_filtered = ASRMetrics.highlight_errors(reference, hypothesis, filter_fillers=True)
    print(f"标准文本: {ref_highlight_filtered}")
    print(f"ASR结果: {hyp_highlight_filtered}")
    
    # 更复杂的例子：多种语气词混合
    print("\n更复杂的语气词示例：")
    reference_complex = "嗯，那个，我想说啊，这个产品呢，质量还是不错的哦，您觉得呢？"
    hypothesis_complex = "那个我想说啊这个产品呢质量还是不错的您觉得哦"
    
    # 分别计算过滤前后的准确率
    accuracy_no_filter = ASRMetrics.calculate_accuracy(reference_complex, hypothesis_complex)
    accuracy_with_filter = ASRMetrics.calculate_accuracy(reference_complex, hypothesis_complex, filter_fillers=True)
    
    print(f"不过滤语气词的字准确率: {accuracy_no_filter:.4f}")
    print(f"过滤语气词后的字准确率: {accuracy_with_filter:.4f}")
    
    # 显示过滤前后的文本对比
    print("\n过滤前的文本对比：")
    ref_text = ASRMetrics.preprocess_text(reference_complex)
    hyp_text = ASRMetrics.preprocess_text(hypothesis_complex)
    print(f"预处理后的标准文本: {ref_text}")
    print(f"预处理后的ASR结果: {hyp_text}")
    
    print("\n过滤后的文本对比：")
    ref_text_filtered = ASRMetrics.preprocess_text(reference_complex, filter_fillers=True)
    hyp_text_filtered = ASRMetrics.preprocess_text(hypothesis_complex, filter_fillers=True)
    print(f"过滤语气词后的标准文本: {ref_text_filtered}")
    print(f"过滤语气词后的ASR结果: {hyp_text_filtered}")

def test_from_files():
    """测试从文件读取文本并计算字准确率"""
    # 测试文件路径
    ref_file = "example_ref.txt"
    hyp_file = "example_hyp.txt"
    
    # 确保文件存在
    if not os.path.exists(ref_file) or not os.path.exists(hyp_file):
        print(f"测试文件不存在: {ref_file} 或 {hyp_file}")
        return
    
    # 读取文件内容
    try:
        with open(ref_file, 'r', encoding='utf-8') as f:
            reference = f.read().strip()
        with open(hyp_file, 'r', encoding='utf-8') as f:
            hypothesis = f.read().strip()
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return
    
    # 计算字准确率
    accuracy = ASRMetrics.calculate_accuracy(reference, hypothesis)
    print(f"\n从文件读取的字准确率: {accuracy:.4f}")
    
    # 计算字错误率
    cer = ASRMetrics.calculate_cer(reference, hypothesis)
    print(f"从文件读取的字错误率: {cer:.4f}")
    
    # 获取详细指标
    metrics = ASRMetrics.calculate_detailed_metrics(reference, hypothesis)
    print(f"详细指标: {metrics}")

def main():
    """主函数，运行所有测试"""
    print("===== 开始字准确率计算测试 =====")
    
    # 测试中文文本
    print("\n----- 中文文本测试 -----")
    test_chinese_text()
    
    # 测试英文文本
    print("\n----- 英文文本测试 -----")
    test_english_text()
    
    # 测试语气词过滤功能
    print("\n----- 语气词过滤测试 -----")
    test_filler_words_filtering()
    
    # 测试从文件读取
    print("\n----- 从文件读取测试 -----")
    test_from_files()
    
    print("\n===== 测试完成 =====")

if __name__ == "__main__":
    main() 