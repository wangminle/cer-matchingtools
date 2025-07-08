"""
重构后的ASRMetrics类
支持多种分词器的字准确率计算引擎
"""

import jiwer
import difflib
import re
from typing import List, Tuple, Dict, Any, Optional

# 导入分词器模块
from text_tokenizers import get_tokenizer, get_available_tokenizers, TokenizerError


class ASRMetrics:
    """
    ASR字准确率计算类
    支持多种分词器：jieba、THULAC、HanLP
    """
    
    def __init__(self, tokenizer_name: str = "jieba"):
        """
        初始化ASRMetrics实例
        
        Args:
            tokenizer_name (str): 分词器名称，默认为"jieba"
        """
        self.tokenizer_name = tokenizer_name
        self.tokenizer = None
        self._initialize_tokenizer()
    
    def _initialize_tokenizer(self):
        """
        初始化分词器实例
        如果指定的分词器不可用，自动回退到jieba
        """
        try:
            self.tokenizer = get_tokenizer(self.tokenizer_name)
        except Exception as e:
            print(f"警告: {self.tokenizer_name}分词器初始化失败: {str(e)}")
            print("自动回退到jieba分词器")
            
            # 尝试回退到jieba
            try:
                self.tokenizer_name = "jieba"
                self.tokenizer = get_tokenizer("jieba")
            except Exception as fallback_e:
                raise RuntimeError(f"无法初始化任何分词器。Jieba回退也失败: {str(fallback_e)}")
    
    def preprocess_chinese_text(self, text: str) -> str:
        """
        使用当前分词器进行中文文本分词预处理
        
        Args:
            text (str): 输入中文文本
            
        Returns:
            str: 分词后重新组合的文本
        """
        try:
            if not text or not text.strip():
                return ""
            
            # 优化：对于很短的文本，跳过分词处理
            if len(text.strip()) <= 2:
                return text.strip()
            
            # 使用当前分词器进行分词
            words = self.tokenizer.cut(text)
            # 重新组合文本，保持原始字符
            return "".join(words)
        except Exception as e:
            print(f"警告: 分词预处理失败: {str(e)}")
            # 返回原始文本
            return text
    
    def filter_filler_words(self, text: str) -> str:
        """
        过滤中文语气词，如"嗯"、"啊"、"呢"等
        
        Args:
            text (str): 输入中文文本
            
        Returns:
            str: 过滤掉语气词后的文本
        """
        try:
            if not text.strip():
                return ""
            
            # 定义常见的语气词列表
            filler_words = ["嗯", "啊", "呢", "吧", "哦", "呀", "啦", "喔", 
                           "诶", "唉", "噢", "喂", "呐", "呵", "咯", "咦", "嘿"]
            
            # 使用当前分词器进行词性标注
            words_pos = self.tokenizer.posseg(text)
            
            # 过滤语气词
            filtered_words = []
            for word, flag in words_pos:
                # 检查是否为语气词
                if word in filler_words:
                    continue
                # 检查词性是否为语气词（y）
                if flag == 'y':
                    continue
                filtered_words.append(word)
            
            # 重新组合文本
            return "".join(filtered_words)
            
        except Exception as e:
            print(f"警告: 语气词过滤失败: {str(e)}")
            # 如果词性标注失败，仅使用词表过滤
            filler_words = ["嗯", "啊", "呢", "吧", "哦", "呀", "啦", "喔", 
                           "诶", "唉", "噢", "喂", "呐", "呵", "咯", "咦", "嘿"]
            result = text
            for filler in filler_words:
                result = result.replace(filler, "")
            return result
    
    def normalize_chinese_text(self, text: str) -> str:
        """
        针对中文特性的标准化处理
        
        Args:
            text (str): 输入中文文本
            
        Returns:
            str: 标准化后的文本
        """
        # 移除标点符号
        text = re.sub(r'[^\w\s]', '', text)
        
        # 统一全角/半角字符
        full_width = "".join(chr(0xff00 + ord(c) - 0x20) if ord(c) <= 0x7f else c for c in text)
        
        # 统一数字格式
        normalized_text = re.sub(r'[0-9０-９]+', '0', full_width)
        
        # 统一空格处理
        normalized_text = re.sub(r'\s+', '', normalized_text)
        
        return normalized_text
    
    def get_character_positions(self, text: str) -> List[Tuple[str, int]]:
        """
        利用当前分词器的tokenize功能进行精确字符定位
        
        Args:
            text (str): 输入文本
            
        Returns:
            list: 包含(字符, 位置)元组的列表
        """
        try:
            if not text.strip():
                return []
            
            positions = []
            tokens = self.tokenizer.tokenize(text)
            
            for word, start, end in tokens:
                for i, char in enumerate(word):
                    positions.append((char, start + i))
            
            return positions
            
        except Exception as e:
            print(f"警告: 字符位置获取失败: {str(e)}")
            # 回退到简单的字符位置
            return [(char, i) for i, char in enumerate(text)]
    
    def preprocess_text(self, text: str, filter_fillers: bool = False) -> str:
        """
        预处理文本：移除标点符号、转换为小写、移除多余空格等
        
        Args:
            text (str): 输入文本
            filter_fillers (bool): 是否过滤语气词
            
        Returns:
            str: 预处理后的文本
        """
        # 优化：如果文本为空，直接返回
        if not text or not text.strip():
            return ""
        
        # 创建基本预处理转换
        transformation = jiwer.Compose([
            jiwer.RemoveMultipleSpaces(),
            jiwer.Strip(),
            jiwer.RemovePunctuation(),
            jiwer.ToLowerCase(),
        ])
        
        # 应用预处理
        processed_text = transformation(text)
        
        # 优化：如果处理后为空，直接返回
        if not processed_text:
            return ""
        
        # 如果需要过滤语气词
        if filter_fillers:
            processed_text = self.filter_filler_words(processed_text)
            if not processed_text:
                return ""
        
        # 对于中文，先进行分词预处理
        processed_text = self.preprocess_chinese_text(processed_text)
        
        # 应用中文标准化处理
        processed_text = self.normalize_chinese_text(processed_text)
        
        return processed_text
    
    def calculate_cer(self, reference: str, hypothesis: str, filter_fillers: bool = False) -> float:
        """
        计算字符错误率 (Character Error Rate)
        
        Args:
            reference (str): 参考文本（标准文本）
            hypothesis (str): 假设文本（ASR生成文本）
            filter_fillers (bool): 是否过滤语气词
            
        Returns:
            float: 字符错误率
        """
        # 预处理文本
        ref_processed = self.preprocess_text(reference, filter_fillers)
        hyp_processed = self.preprocess_text(hypothesis, filter_fillers)
        
        # 获取字符位置信息
        ref_positions = self.get_character_positions(ref_processed)
        hyp_positions = self.get_character_positions(hyp_processed)
        
        # 提取字符列表
        ref_chars = [pos[0] for pos in ref_positions] if ref_positions else list(ref_processed)
        hyp_chars = [pos[0] for pos in hyp_positions] if hyp_positions else list(hyp_processed)
        
        # 确保两个字符串都不为空
        if len(ref_chars) == 0:
            ref_chars = [""]
        if len(hyp_chars) == 0:
            hyp_chars = [""]
        
        # 计算编辑距离
        try:
            import Levenshtein
            distance = Levenshtein.distance(ref_processed, hyp_processed)
        except ImportError:
            # 如果没有Levenshtein库，使用基本的编辑距离算法
            distance = self._calculate_edit_distance(ref_processed, hyp_processed)
        
        # 计算CER
        if len(ref_processed) > 0:
            cer = distance / len(ref_processed)
        else:
            cer = 1.0 if len(hyp_processed) > 0 else 0.0
        
        return cer
    
    def _calculate_edit_distance(self, s1: str, s2: str) -> int:
        """
        计算两个字符串的编辑距离（Levenshtein距离）
        
        Args:
            s1 (str): 第一个字符串
            s2 (str): 第二个字符串
            
        Returns:
            int: 编辑距离
        """
        if len(s1) == 0:
            return len(s2)
        if len(s2) == 0:
            return len(s1)
        
        # 创建距离矩阵
        matrix = [[0] * (len(s2) + 1) for _ in range(len(s1) + 1)]
        
        # 初始化第一行和第一列
        for i in range(len(s1) + 1):
            matrix[i][0] = i
        for j in range(len(s2) + 1):
            matrix[0][j] = j
        
        # 计算距离
        for i in range(1, len(s1) + 1):
            for j in range(1, len(s2) + 1):
                if s1[i-1] == s2[j-1]:
                    cost = 0
                else:
                    cost = 1
                
                matrix[i][j] = min(
                    matrix[i-1][j] + 1,      # 删除
                    matrix[i][j-1] + 1,      # 插入
                    matrix[i-1][j-1] + cost  # 替换
                )
        
        return matrix[len(s1)][len(s2)]
    
    def calculate_wer(self, reference: str, hypothesis: str, filter_fillers: bool = False) -> float:
        """
        计算词错误率 (Word Error Rate)
        
        Args:
            reference (str): 参考文本（标准文本）
            hypothesis (str): 假设文本（ASR生成文本）
            filter_fillers (bool): 是否过滤语气词
            
        Returns:
            float: 词错误率
        """
        # 预处理文本
        ref_processed = self.preprocess_text(reference, filter_fillers)
        hyp_processed = self.preprocess_text(hypothesis, filter_fillers)
        
        # 对于中文文本，每个字符视为一个"词"
        ref_words = [char for char in ref_processed]
        hyp_words = [char for char in hyp_processed]
        
        # 确保列表不为空
        if not ref_words:
            ref_words = [""]
        if not hyp_words:
            hyp_words = [""]
        
        # 使用自定义的方式计算WER
        s, d, i = self._calculate_edit_ops(ref_words, hyp_words)
        if len(ref_words) > 0:
            wer = (s + d + i) / len(ref_words)
        else:
            wer = 1.0 if len(hyp_words) > 0 else 0.0
        
        return wer
    
    def _calculate_edit_ops(self, reference: List[str], hypothesis: List[str]) -> Tuple[int, int, int]:
        """
        计算编辑操作（替换、删除、插入）的数量
        
        Args:
            reference (List[str]): 参考字符列表
            hypothesis (List[str]): 假设字符列表
            
        Returns:
            Tuple[int, int, int]: (替换数, 删除数, 插入数)
        """
        try:
            import Levenshtein
            
            # 将列表转为字符串，然后计算编辑距离
            ref_str = "".join(reference)
            hyp_str = "".join(hypothesis)
            
            # 计算编辑操作
            ops = Levenshtein.editops(ref_str, hyp_str)
            
            # 统计各类操作数量
            s = len([op for op in ops if op[0] == 'replace'])  # 替换
            d = len([op for op in ops if op[0] == 'delete'])   # 删除
            i = len([op for op in ops if op[0] == 'insert'])   # 插入
            
            return s, d, i
            
        except ImportError:
            # 如果没有Levenshtein库，使用简单的估算
            total_distance = self._calculate_edit_distance("".join(reference), "".join(hypothesis))
            # 简单估算：假设操作平均分布
            s = total_distance // 3
            d = total_distance // 3
            i = total_distance - s - d
            return s, d, i
    
    def calculate_accuracy(self, reference: str, hypothesis: str, filter_fillers: bool = False) -> float:
        """
        计算准确率 (1 - CER)
        
        Args:
            reference (str): 参考文本（标准文本）
            hypothesis (str): 假设文本（ASR生成文本）
            filter_fillers (bool): 是否过滤语气词
            
        Returns:
            float: 准确率
        """
        cer = self.calculate_cer(reference, hypothesis, filter_fillers)
        return 1.0 - cer
    
    def calculate_detailed_metrics(self, reference: str, hypothesis: str, filter_fillers: bool = False) -> Dict[str, Any]:
        """
        计算详细的错误指标，包括插入、删除、替换错误
        
        Args:
            reference (str): 参考文本（标准文本）
            hypothesis (str): 假设文本（ASR生成文本）
            filter_fillers (bool): 是否过滤语气词
            
        Returns:
            dict: 包含各种错误指标的字典
        """
        # 预处理文本
        ref_processed = self.preprocess_text(reference, filter_fillers)
        hyp_processed = self.preprocess_text(hypothesis, filter_fillers)
        
        # 获取字符位置信息
        ref_positions = self.get_character_positions(ref_processed)
        hyp_positions = self.get_character_positions(hyp_processed)
        
        # 提取字符列表
        ref_chars = [pos[0] for pos in ref_positions] if ref_positions else list(ref_processed)
        hyp_chars = [pos[0] for pos in hyp_positions] if hyp_positions else list(hyp_processed)
        
        # 确保列表不为空
        if not ref_chars:
            ref_chars = [""]
        if not hyp_chars:
            hyp_chars = [""]
        
        # 使用自定义方式计算详细指标
        s, d, i = self._calculate_edit_ops(ref_chars, hyp_chars)
        
        # 计算总错误数和字符错误率
        total_errors = s + d + i
        ref_length = len(ref_chars)
        hyp_length = len(hyp_chars)
        
        if ref_length > 0:
            cer = total_errors / ref_length
        else:
            cer = 1.0 if hyp_length > 0 else 0.0
        
        # 返回详细指标
        return {
            'cer': cer,
            'wer': cer,  # 对于中文，CER和WER相同
            'mer': cer,  # 匹配错误率
            'wil': cer,  # 词信息丢失率
            'wip': 1.0 - cer,  # 词信息保留率
            'hits': ref_length - (s + d),  # 命中数
            'substitutions': s,  # 替换错误数
            'deletions': d,      # 删除错误数
            'insertions': i,     # 插入错误数
            'ref_length': ref_length,  # 参考文本长度
            'hyp_length': hyp_length,  # 假设文本长度
            'accuracy': 1.0 - cer,  # 准确率
            'tokenizer': self.tokenizer_name  # 使用的分词器
        }
    
    def show_differences(self, reference: str, hypothesis: str, filter_fillers: bool = False) -> str:
        """
        显示两个文本之间的差异
        
        Args:
            reference (str): 参考文本（标准文本）
            hypothesis (str): 假设文本（ASR生成文本）
            filter_fillers (bool): 是否过滤语气词
            
        Returns:
            str: 格式化的差异信息
        """
        # 预处理文本
        ref_processed = self.preprocess_text(reference, filter_fillers)
        hyp_processed = self.preprocess_text(hypothesis, filter_fillers)
        
        # 使用difflib计算差异
        d = difflib.Differ()
        diff = list(d.compare(list(ref_processed), list(hyp_processed)))
        
        return ''.join(diff)
    
    def highlight_errors(self, reference: str, hypothesis: str, filter_fillers: bool = False) -> Tuple[str, str]:
        """
        高亮显示错误部分
        
        Args:
            reference (str): 参考文本（标准文本）
            hypothesis (str): 假设文本（ASR生成文本）
            filter_fillers (bool): 是否过滤语气词
            
        Returns:
            tuple: (参考文本高亮版, 假设文本高亮版)
        """
        # 预处理文本
        ref_processed = self.preprocess_text(reference, filter_fillers)
        hyp_processed = self.preprocess_text(hypothesis, filter_fillers)
        
        # 使用difflib的SequenceMatcher找出匹配和不匹配的部分
        matcher = difflib.SequenceMatcher(None, ref_processed, hyp_processed)
        
        # 构建高亮标记的字符串
        ref_highlighted = []
        hyp_highlighted = []
        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                ref_highlighted.append(ref_processed[i1:i2])
                hyp_highlighted.append(hyp_processed[j1:j2])
            elif tag == 'replace':
                ref_highlighted.append(f"[{ref_processed[i1:i2]}]")
                hyp_highlighted.append(f"[{hyp_processed[j1:j2]}]")
            elif tag == 'delete':
                ref_highlighted.append(f"[{ref_processed[i1:i2]}]")
            elif tag == 'insert':
                hyp_highlighted.append(f"[{hyp_processed[j1:j2]}]")
        
        return ''.join(ref_highlighted), ''.join(hyp_highlighted)
    
    def get_tokenizer_info(self) -> Dict[str, Any]:
        """
        获取当前使用的分词器信息
        
        Returns:
            Dict[str, Any]: 分词器信息
        """
        if self.tokenizer:
            return self.tokenizer.get_info()
        else:
            return {'name': self.tokenizer_name, 'available': False}