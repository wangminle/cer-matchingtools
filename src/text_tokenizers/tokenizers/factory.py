"""
分词器工厂
提供分词器的创建、管理和获取功能
"""

from typing import Dict, List, Optional, Any
from .base import BaseTokenizer, TokenizerInitError
from .jieba_tokenizer import JiebaTokenizer
from .thulac_tokenizer import ThulacTokenizer
from .hanlp_tokenizer import HanlpTokenizer


class TokenizerFactory:
    """
    分词器工厂类
    使用单例模式管理分词器实例，避免重复初始化
    """
    
    _instance = None
    _tokenizers: Dict[str, BaseTokenizer] = {}
    _available_tokenizers: Dict[str, type] = {
        'jieba': JiebaTokenizer,
        'thulac': ThulacTokenizer,
        'hanlp': HanlpTokenizer
    }
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TokenizerFactory, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def get_available_tokenizers(cls) -> List[str]:
        """
        获取可用的分词器列表
        检查每个分词器的依赖是否满足
        
        Returns:
            List[str]: 可用的分词器名称列表
        """
        available = []
        
        for name, tokenizer_class in cls._available_tokenizers.items():
            try:
                # 尝试创建分词器实例
                tokenizer = tokenizer_class()
                tokenizer.initialize()
                available.append(name)
            except TokenizerInitError:
                # 如果初始化失败，该分词器不可用
                continue
            except Exception:
                # 其他异常也视为不可用
                continue
        
        # 确保jieba总是在列表中（如果可用的话）
        if 'jieba' not in available:
            # 再次尝试jieba
            try:
                jieba_tokenizer = JiebaTokenizer()
                jieba_tokenizer.initialize()
                available.insert(0, 'jieba')
            except:
                pass
        
        return available
    
    @classmethod
    def get_tokenizer(cls, name: str) -> BaseTokenizer:
        """
        获取分词器实例（单例模式）
        
        Args:
            name (str): 分词器名称
            
        Returns:
            BaseTokenizer: 分词器实例
            
        Raises:
            ValueError: 如果分词器名称不支持
            TokenizerInitError: 如果分词器初始化失败
        """
        if name not in cls._available_tokenizers:
            raise ValueError(f"不支持的分词器: {name}，可用的分词器: {list(cls._available_tokenizers.keys())}")
        
        # 如果已经创建过该分词器实例，直接返回
        if name in cls._tokenizers:
            return cls._tokenizers[name]
        
        # 创建新的分词器实例
        tokenizer_class = cls._available_tokenizers[name]
        tokenizer = tokenizer_class()
        
        # 初始化分词器
        try:
            success = tokenizer.initialize()
            if not success:
                raise TokenizerInitError(f"{name}分词器初始化失败")
        except Exception as e:
            raise TokenizerInitError(f"{name}分词器初始化失败: {str(e)}")
        
        # 缓存分词器实例
        cls._tokenizers[name] = tokenizer
        
        return tokenizer
    
    @classmethod
    def get_tokenizer_info(cls, name: str) -> Dict[str, Any]:
        """
        获取分词器信息
        
        Args:
            name (str): 分词器名称
            
        Returns:
            Dict[str, Any]: 分词器信息字典
        """
        if name not in cls._available_tokenizers:
            return {
                'name': name,
                'available': False,
                'error': f'不支持的分词器: {name}'
            }
        
        try:
            tokenizer = cls.get_tokenizer(name)
            info = tokenizer.get_info()
            info['available'] = True
            return info
        except Exception as e:
            return {
                'name': name,
                'available': False,
                'error': str(e)
            }
    
    @classmethod
    def check_tokenizer_availability(cls, name: str) -> bool:
        """
        检查指定分词器是否可用
        
        Args:
            name (str): 分词器名称
            
        Returns:
            bool: 是否可用
        """
        if name not in cls._available_tokenizers:
            return False
        
        try:
            tokenizer_class = cls._available_tokenizers[name]
            tokenizer = tokenizer_class()
            return tokenizer.initialize()
        except:
            return False
    
    @classmethod
    def create_tokenizer(cls, name: str) -> BaseTokenizer:
        """
        创建新的分词器实例（不使用缓存）
        
        Args:
            name (str): 分词器名称
            
        Returns:
            BaseTokenizer: 新的分词器实例
            
        Raises:
            ValueError: 如果分词器名称不支持
            TokenizerInitError: 如果分词器初始化失败
        """
        if name not in cls._available_tokenizers:
            raise ValueError(f"不支持的分词器: {name}")
        
        tokenizer_class = cls._available_tokenizers[name]
        tokenizer = tokenizer_class()
        
        # 初始化分词器
        try:
            success = tokenizer.initialize()
            if not success:
                raise TokenizerInitError(f"{name}分词器初始化失败")
        except Exception as e:
            raise TokenizerInitError(f"{name}分词器初始化失败: {str(e)}")
        
        return tokenizer
    
    @classmethod
    def clear_cache(cls):
        """
        清除缓存的分词器实例
        """
        cls._tokenizers.clear()
    
    @classmethod
    def get_all_tokenizer_info(cls) -> Dict[str, Dict[str, Any]]:
        """
        获取所有分词器的信息
        
        Returns:
            Dict[str, Dict[str, Any]]: 所有分词器的信息字典
        """
        info = {}
        for name in cls._available_tokenizers.keys():
            info[name] = cls.get_tokenizer_info(name)
        return info


# 便捷函数
def get_tokenizer(name: str) -> BaseTokenizer:
    """
    获取分词器实例的便捷函数
    
    Args:
        name (str): 分词器名称
        
    Returns:
        BaseTokenizer: 分词器实例
    """
    factory = TokenizerFactory()
    return factory.get_tokenizer(name)


def get_available_tokenizers() -> List[str]:
    """
    获取可用分词器列表的便捷函数
    
    Returns:
        List[str]: 可用的分词器名称列表
    """
    factory = TokenizerFactory()
    return factory.get_available_tokenizers()


def get_tokenizer_info(name: str) -> Dict[str, Any]:
    """
    获取分词器信息的便捷函数
    
    Args:
        name (str): 分词器名称
        
    Returns:
        Dict[str, Any]: 分词器信息字典
    """
    factory = TokenizerFactory()
    return factory.get_tokenizer_info(name)