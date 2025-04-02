import os
import sys
import importlib.util
import argparse

def main():
    """
    字准和句准统计工具的主入口
    调用wer-matchingtools中的check_accuracy.py脚本进行计算
    """
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="字准和句准统计工具 - 计算ASR识别准确率")
    parser.add_argument("--ref", help="参考文本文件路径")
    parser.add_argument("--asr", help="ASR识别结果文件路径")
    parser.add_argument("--dir", help="指定样本目录（默认为samples）", default="samples")
    args = parser.parse_args()
    
    # 获取当前脚本的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 设置wer-matchingtools路径
    wer_tool_dir = os.path.join(current_dir, "wer-matchingtools")
    
    # 动态导入module
    tool_path = os.path.join(wer_tool_dir, "check_accuracy.py")
    
    # 使用importlib动态导入模块，避免命名冲突
    spec = importlib.util.spec_from_file_location("wer_tool", tool_path)
    wer_tool = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(wer_tool)
    
    # 获取calculate_accuracy函数
    calculate_accuracy = wer_tool.calculate_accuracy
    
    # 设置文件路径
    sample_dir = os.path.join(current_dir, args.dir)
    if args.ref and args.asr:
        # 使用命令行指定的文件
        ref_file = args.ref
        asr_file = args.asr
    else:
        # 使用默认文件
        ref_file = os.path.join(sample_dir, "听打定稿-211003上师客厅开示.txt")
        asr_file = os.path.join(sample_dir, "原始录音-211003上师客厅开示.txt")
    
    # 检查文件是否存在
    if not os.path.exists(ref_file):
        print(f"错误：参考文件不存在 - {ref_file}")
        return
    
    if not os.path.exists(asr_file):
        print(f"错误：ASR文件不存在 - {asr_file}")
        return
    
    # 打印文件路径
    print(f"参考文件路径: {ref_file}")
    print(f"ASR文件路径: {asr_file}")
    
    # 计算并输出准确率
    result = calculate_accuracy(ref_file, asr_file)
    
    # 如果计算成功，输出总结信息
    if result:
        print("\n===== 评估结果 =====")
        print(f"字准确率: {result['accuracy']:.4f} ({result['accuracy']*100:.2f}%)")
        print(f"错误率: {1-result['accuracy']:.4f} ({(1-result['accuracy'])*100:.2f}%)")
        print("==================")

if __name__ == "__main__":
    main() 