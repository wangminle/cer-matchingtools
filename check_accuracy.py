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

def calculate_accuracy(ref_file_path, asr_file_path):
    """
    读取文件并计算字准确率
    """
    try:
        # 使用多种编码尝试读取文件
        ref_text = read_file_with_multiple_encodings(ref_file_path)
        asr_text = read_file_with_multiple_encodings(asr_file_path)

        # 使用 ASRMetrics 计算指标
        metrics = ASRMetrics.calculate_detailed_metrics(ref_text, asr_text)
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
    args = parser.parse_args()

    # 获取文件路径
    ref_file = args.ref
    asr_file = args.asr

    # 打印文件路径
    print(f"参考文件路径: {ref_file}")
    print(f"ASR文件路径: {asr_file}")

    # 调用新的 calculate_accuracy 函数
    result = calculate_accuracy(ref_file, asr_file)

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
        print("==================")

if __name__ == "__main__":
    main() 