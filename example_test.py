#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
示例测试文件，展示如何使用ASRMetrics类计算字准确率
"""

from utils import ASRMetrics

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

def test_english_text():
    """测试英文文本的字准确率计算"""
    # 示例英文文本
    reference = "The quick brown fox jumps over the lazy dog."
    hypothesis = "The quik brown fox jump over the lasy dog"  # 几个拼写错误，缺少句号
    
    # 计算字准确率
    accuracy = ASRMetrics.calculate_accuracy(reference, hypothesis)
    print(f"英文字准确率: {accuracy:.4f}")
    
    # 计算词错误率
    wer = ASRMetrics.calculate_wer(reference, hypothesis)
    print(f"英文词错误率: {wer:.4f}")

def test_from_files():
    """从文件读取文本并计算字准确率"""
    try:
        # 尝试从文件读取
        with open('example_ref.txt', 'r', encoding='utf-8') as f:
            reference = f.read()
        
        with open('example_hyp.txt', 'r', encoding='utf-8') as f:
            hypothesis = f.read()
        
        # 计算字准确率
        accuracy = ASRMetrics.calculate_accuracy(reference, hypothesis)
        print(f"文件字准确率: {accuracy:.4f}")
        
    except FileNotFoundError:
        print("示例文件不存在，请先创建example_ref.txt和example_hyp.txt文件")
        
        # 创建示例文件
        with open('example_ref.txt', 'w', encoding='utf-8') as f:
            f.write("这是一个示例标准文本，用于测试字准确率计算功能。")
        
        with open('example_hyp.txt', 'w', encoding='utf-8') as f:
            f.write("这是一个示范标准文本用于测试字准确率计算功能")
        
        print("已创建示例文件，请重新运行测试")

if __name__ == "__main__":
    print("===== 中文文本测试 =====")
    test_chinese_text()
    
    print("\n===== 英文文本测试 =====")
    test_english_text()
    
    print("\n===== 文件测试 =====")
    test_from_files() 