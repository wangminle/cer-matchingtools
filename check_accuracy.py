import os
import sys
import argparse
from src.utils import ASRMetrics

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

def calculate_accuracy(ref_file_path, asr_file_path, show_details=False):
    """
    读取文件并计算字准确率
    
    Args:
        ref_file_path (str): 参考文本文件路径
        asr_file_path (str): ASR结果文件路径
        show_details (bool): 是否显示详细的错误信息
        
    Returns:
        dict: 包含各种评估指标的字典
    """
    try:
        # 使用多种编码尝试读取文件
        ref_text = read_file_with_multiple_encodings(ref_file_path)
        asr_text = read_file_with_multiple_encodings(asr_file_path)

        # 使用 ASRMetrics 计算指标
        metrics = ASRMetrics.calculate_detailed_metrics(ref_text, asr_text)
        
        # 如果需要显示详细信息
        if show_details:
            # 获取错误高亮的文本
            ref_highlight, asr_highlight = ASRMetrics.highlight_errors(ref_text, asr_text)
            metrics['ref_highlight'] = ref_highlight
            metrics['asr_highlight'] = asr_highlight
            
            # 获取词性标注信息（使用jieba.posseg）
            ref_positions = ASRMetrics.get_character_positions(ref_text)
            asr_positions = ASRMetrics.get_character_positions(asr_text)
            metrics['ref_positions'] = ref_positions
            metrics['asr_positions'] = asr_positions
        
        return metrics
    except FileNotFoundError as e:
        print(f"错误：文件未找到 - {e}")
        return None
    except Exception as e:
        print(f"计算过程中发生错误: {e}")
        return None

def main():
    """
    字准统计工具的主入口
    使用 src.utils.ASRMetrics 进行计算
    """
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="字准统计工具 - 计算ASR识别准确率")
    parser.add_argument("--ref", required=True, help="参考文本文件路径")
    parser.add_argument("--asr", required=True, help="ASR识别结果文件路径")
    parser.add_argument("--details", action="store_true", help="显示详细的错误分析")
    parser.add_argument("--no-jieba", action="store_true", help="不使用jieba分词进行预处理")
    args = parser.parse_args()

    # 获取文件路径
    ref_file = args.ref
    asr_file = args.asr
    show_details = args.details

    # 打印文件路径
    print(f"参考文件路径: {ref_file}")
    print(f"ASR文件路径: {asr_file}")
    
    # 如果用户选择不使用jieba
    if args.no_jieba:
        print("注意: 禁用jieba分词预处理")
        # 这里可以添加代码来禁用jieba，但由于我们的实现不允许直接在这里修改ASRMetrics的行为
        # 所以这里只是一个提示，实际上jieba处理仍然会被使用
        print("(此选项在当前版本中不生效，jieba分词仍将被使用)")

    # 调用calculate_accuracy函数
    result = calculate_accuracy(ref_file, asr_file, show_details)

    # 如果计算成功，输出总结信息
    if result:
        print("\n===== 评估结果 =====")
        print(f"字准确率: {result['accuracy']:.4f} ({result['accuracy']*100:.2f}%)")
        print(f"错误率: {result['cer']:.4f} ({result['cer']*100:.2f}%)")
        print(f"替换错误数: {result['substitutions']}")
        print(f"删除错误数: {result['deletions']}")
        print(f"插入错误数: {result['insertions']}")
        print(f"参考文本长度: {result['ref_length']}")
        print(f"ASR文本长度: {result['hyp_length']}")
        
        if show_details and 'ref_highlight' in result:
            print("\n===== 错误分析 =====")
            print(f"标准文本(错误高亮): {result['ref_highlight']}")
            print(f"ASR文本(错误高亮): {result['asr_highlight']}")
            
            if 'ref_positions' in result:
                print("\n===== 字符位置信息示例(前10个) =====")
                for i, (char, pos) in enumerate(result['ref_positions'][:10]):
                    print(f"标准文本: 字符'{char}'位于位置{pos}")
        print("==================")

if __name__ == "__main__":
    main() 