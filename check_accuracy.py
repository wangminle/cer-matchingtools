import Levenshtein
import os

def calculate_accuracy(ref_file, asr_file):
    # 确保文件存在
    if not os.path.exists(ref_file):
        print(f"参考文件不存在: {ref_file}")
        return
    if not os.path.exists(asr_file):
        print(f"ASR文件不存在: {asr_file}")
        return
    
    # 读取文件内容
    try:
        with open(ref_file, 'r', encoding='utf-8') as f:
            ref_text = f.read()
        
        with open(asr_file, 'r', encoding='utf-8') as f:
            asr_text = f.read()
    except Exception as e:
        print(f"读取文件时出错: {str(e)}")
        return
    
    # 移除空白字符，只保留实际字符
    asr_text_clean = ''.join(char for char in asr_text if char.strip())
    ref_text_clean = ''.join(char for char in ref_text if char.strip())
    
    # 计算字数
    asr_len = len(asr_text_clean)
    ref_len = len(ref_text_clean)
    
    # 计算编辑距离
    distance = Levenshtein.distance(ref_text_clean, asr_text_clean)
    
    # 计算字准确率
    accuracy = 1 - distance / ref_len if ref_len > 0 else 0
    
    # 输出结果
    print(f'ASR字数: {asr_len}')
    print(f'标注字数: {ref_len}')
    print(f'编辑距离: {distance}')
    print(f'字准确率: {accuracy:.4f}')
    
    return {
        'asr_len': asr_len,
        'ref_len': ref_len,
        'distance': distance,
        'accuracy': accuracy
    }

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    ref_file = os.path.join(script_dir, "samples", "听打定稿-211003上师客厅开示.txt")
    asr_file = os.path.join(script_dir, "samples", "原始录音-211003上师客厅开示.txt")
    
    # 打印文件路径
    print(f"参考文件路径: {ref_file}")
    print(f"ASR文件路径: {asr_file}")
    
    calculate_accuracy(ref_file, asr_file) 