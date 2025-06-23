"""
Jieba分词器实现
基于jieba库的分词器，完全兼容现有功能
"""

from typing import List, Tuple
import jieba
import jieba.posseg
from .base import BaseTokenizer, TokenizerInitError, TokenizerProcessError


class JiebaTokenizer(BaseTokenizer):
    """
    Jieba分词器实现
    基于jieba库，提供中文分词、词性标注和精确位置分词功能
    """
    
    def __init__(self):
        super().__init__()
        self.name = "jieba"
    
    def initialize(self) -> bool:
        """
        初始化Jieba分词器
        
        Returns:
            bool: 初始化是否成功
            
        Raises:
            TokenizerInitError: 初始化失败时抛出
        """
        try:
            # Jieba无需特殊初始化，但可以预加载词典
            # 这里进行一次简单的分词操作来确保jieba正常工作
            test_result = list(jieba.cut("测试"))
            if not test_result:
                raise TokenizerInitError("Jieba分词器测试失败")
            
            # 获取jieba版本信息
            self.version = getattr(jieba, '__version__', 'unknown')
            
            self.is_initialized = True
            return True
            
        except Exception as e:
            raise TokenizerInitError(f"Jieba分词器初始化失败: {str(e)}")
    
    def cut(self, text: str) -> List[str]:
        """
        基础分词功能
        
        Args:
            text (str): 待分词的文本
            
        Returns:
            List[str]: 分词结果列表
            
        Raises:
            TokenizerProcessError: 分词处理失败时抛出
        """
        try:
            cleaned_text = self.validate_text(text)
            if not cleaned_text:
                return []
            
            # 使用jieba进行分词
            result = list(jieba.cut(cleaned_text))
            return result
            
        except Exception as e:
            raise TokenizerProcessError(f"Jieba分词失败: {str(e)}")
    
    def posseg(self, text: str) -> List[Tuple[str, str]]:
        """
        词性标注功能
        
        Args:
            text (str): 待标注的文本
            
        Returns:
            List[Tuple[str, str]]: (词语, 词性)的元组列表
            
        Raises:
            TokenizerProcessError: 词性标注失败时抛出
        """
        try:
            cleaned_text = self.validate_text(text)
            if not cleaned_text:
                return []
            
            # 使用jieba进行词性标注
            result = []
            for word, flag in jieba.posseg.cut(cleaned_text):
                result.append((word, flag))
            
            return result
            
        except Exception as e:
            raise TokenizerProcessError(f"Jieba词性标注失败: {str(e)}")
    
    def tokenize(self, text: str) -> List[Tuple[str, int, int]]:
        """
        精确分词，返回词语及其在原文中的位置
        
        Args:
            text (str): 待分词的文本
            
        Returns:
            List[Tuple[str, int, int]]: (词语, 开始位置, 结束位置)的元组列表
            
        Raises:
            TokenizerProcessError: 分词处理失败时抛出
        """
        try:
            cleaned_text = self.validate_text(text)
            if not cleaned_text:
                return []
            
            # 使用jieba的tokenize功能获取精确位置
            result = []
            for tk in jieba.tokenize(cleaned_text):
                word, start, end = tk
                result.append((word, start, end))
            
            return result
            
        except Exception as e:
            raise TokenizerProcessError(f"Jieba精确分词失败: {str(e)}")
    
    def get_info(self) -> dict:
        """
        获取Jieba分词器信息
        
        Returns:
            dict: 包含分词器详细信息的字典
        """
        info = super().get_info()
        info.update({
            'description': '基于jieba库的中文分词器',
            'features': ['分词', '词性标注', '精确位置分词'],
            'dependencies': ['jieba'],
            'performance': '高速',
            'accuracy': '中等'
        })
        return info 