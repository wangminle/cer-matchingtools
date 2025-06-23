#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分词器模块
支持多种中文分词器：jieba、THULAC、HanLP
"""

from typing import List, Tuple, Dict, Any
from abc import ABC, abstractmethod
import threading
import time


# 异常类定义
class TokenizerError(Exception):
    """分词器基础异常类"""
    pass


class TokenizerInitError(TokenizerError):
    """分词器初始化异常"""
    pass


class TokenizerProcessError(TokenizerError):
    """分词器处理异常"""
    pass


# 抽象基类
class BaseTokenizer(ABC):
    """分词器抽象基类"""
    
    def __init__(self):
        self.name = self.__class__.__name__.replace('Tokenizer', '').lower()
        self.is_initialized = False
        self.version = "1.0"
    
    @abstractmethod
    def initialize(self) -> bool:
        pass
    
    @abstractmethod
    def cut(self, text: str) -> List[str]:
        pass
    
    @abstractmethod
    def posseg(self, text: str) -> List[Tuple[str, str]]:
        pass
    
    @abstractmethod
    def tokenize(self, text: str) -> List[Tuple[str, int, int]]:
        pass
    
    def validate_text(self, text: str) -> str:
        if not isinstance(text, str):
            raise TokenizerProcessError("输入必须是字符串类型")
        return text.strip()
    
    def get_info(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'version': self.version,
            'initialized': self.is_initialized,
            'available': True,
            'class_name': self.__class__.__name__
        }


# Jieba分词器实现
class JiebaTokenizer(BaseTokenizer):
    """Jieba分词器"""
    
    def __init__(self):
        super().__init__()
        self.name = "jieba"
        self.jieba = None
        self.pseg = None
    
    def initialize(self) -> bool:
        try:
            import jieba
            import jieba.posseg as pseg
            self.jieba = jieba
            self.pseg = pseg
            self.is_initialized = True
            return True
        except ImportError:
            raise TokenizerInitError("jieba库未安装，请运行: pip install jieba")
    
    def cut(self, text: str) -> List[str]:
        cleaned_text = self.validate_text(text)
        if not cleaned_text:
            return []
        
        if not self.is_initialized:
            raise TokenizerProcessError("Jieba分词器未初始化")
        
        # 使用jieba分词，转换为列表
        return list(self.jieba.cut(cleaned_text))
    
    def posseg(self, text: str) -> List[Tuple[str, str]]:
        cleaned_text = self.validate_text(text)
        if not cleaned_text:
            return []
        
        if not self.is_initialized:
            raise TokenizerProcessError("Jieba分词器未初始化")
        
        # 使用jieba进行词性标注
        result = []
        for word, flag in self.pseg.cut(cleaned_text):
            result.append((word, flag))
        return result
    
    def tokenize(self, text: str) -> List[Tuple[str, int, int]]:
        cleaned_text = self.validate_text(text)
        if not cleaned_text:
            return []
        
        if not self.is_initialized:
            raise TokenizerProcessError("Jieba分词器未初始化")
        
        # 使用jieba.tokenize获得精确位置
        result = []
        for word, start, end in self.jieba.tokenize(cleaned_text):
            result.append((word, start, end))
        return result
    
    def get_info(self) -> dict:
        info = super().get_info()
        try:
            import jieba
            version = getattr(jieba, '__version__', 'unknown')
        except ImportError:
            version = 'not installed'
        
        info.update({
            'version': version,
            'description': 'Jieba中文分词器',
            'features': ['分词', '词性标注', '精确位置分词'],
            'dependencies': ['jieba'],
            'performance': '高速',
            'accuracy': '中等',
            'note': '适合大多数中文分词任务'
        })
        return info


# THULAC分词器实现
class ThulacTokenizer(BaseTokenizer):
    """THULAC分词器"""
    
    # 类级别的共享实例，避免重复加载模型
    _shared_thu = None
    _initialization_lock = False
    
    def __init__(self):
        super().__init__()
        self.name = "thulac"
        self.thulac = None
        self.thu = None
    
    def initialize(self) -> bool:
        try:
            import thulac
            self.thulac = thulac
            
            # 使用类级别的共享实例，避免重复初始化
            if ThulacTokenizer._shared_thu is None and not ThulacTokenizer._initialization_lock:
                ThulacTokenizer._initialization_lock = True
                print("  正在初始化THULAC分词器（仅执行一次）...")
                # 初始化THULAC实例（启用词性标注）
                ThulacTokenizer._shared_thu = thulac.thulac(seg_only=False)
                ThulacTokenizer._initialization_lock = False
            
            # 等待共享实例初始化完成
            while ThulacTokenizer._initialization_lock:
                import time
                time.sleep(0.1)
            
            self.thu = ThulacTokenizer._shared_thu
            self.is_initialized = True
            return True
        except ImportError:
            raise TokenizerInitError("THULAC库未安装，请运行: pip install thulac")
    
    def cut(self, text: str) -> List[str]:
        cleaned_text = self.validate_text(text)
        if not cleaned_text:
            return []
        
        if not self.is_initialized:
            raise TokenizerProcessError("THULAC分词器未初始化")
        
        # 使用THULAC分词，只返回词语
        result = self.thu.cut(cleaned_text, text=False)
        return [item[0] for item in result]
    
    def posseg(self, text: str) -> List[Tuple[str, str]]:
        cleaned_text = self.validate_text(text)
        if not cleaned_text:
            return []
        
        if not self.is_initialized:
            raise TokenizerProcessError("THULAC分词器未初始化")
        
        # 使用THULAC进行词性标注
        result = self.thu.cut(cleaned_text, text=False)
        return [(item[0], item[1]) for item in result]
    
    def tokenize(self, text: str) -> List[Tuple[str, int, int]]:
        cleaned_text = self.validate_text(text)
        if not cleaned_text:
            return []
        
        if not self.is_initialized:
            raise TokenizerProcessError("THULAC分词器未初始化")
        
        # THULAC没有直接的tokenize方法，我们需要手动计算位置
        words = self.cut(cleaned_text)
        result = []
        current_pos = 0
        
        for word in words:
            start_pos = cleaned_text.find(word, current_pos)
            if start_pos == -1:
                start_pos = current_pos
            end_pos = start_pos + len(word)
            result.append((word, start_pos, end_pos))
            current_pos = end_pos
        
        return result
    
    def get_info(self) -> dict:
        info = super().get_info()
        try:
            import thulac
            version = getattr(thulac, '__version__', '1.0')
        except ImportError:
            version = 'not installed'
        
        info.update({
            'version': version,
            'description': 'THULAC高精度中文分词器',
            'features': ['分词', '词性标注', '精确位置分词'],
            'dependencies': ['thulac'],
            'performance': '中等速度',
            'accuracy': '高精度',
            'note': '清华大学开发的中文词法分析工具包'
        })
        return info


# HanLP分词器实现（优化版 - 仅加载tok模型）
class HanlpTokenizer(BaseTokenizer):
    """HanLP分词器（仅分词功能）- 轻量化版本"""
    
    # 类级别的共享实例，实现单例模式
    _shared_tokenizer = None
    _initialization_lock = threading.Lock()
    _is_initialized = False
    
    def __init__(self):
        super().__init__()
        self.name = "hanlp"
        self.hanlp = None
        self.tokenizer = None
        self.model_name = None
    
    def initialize(self) -> bool:
        if HanlpTokenizer._is_initialized:
            return True
            
        try:
            with HanlpTokenizer._initialization_lock:
                if HanlpTokenizer._is_initialized:
                    return True
                
                import hanlp
                self.hanlp = hanlp
                
                print("  正在初始化HanLP分词器（仅加载分词模型）...")
                
                # 推荐的轻量化分词模型配置（按优先级排序）
                tokenizer_configs = [
                    {
                        'model': 'COARSE_ELECTRA_SMALL_ZH',
                        'desc': '粗粒度ELECTRA小模型',
                        'size': '45MB',
                        'performance': 'F1: 98.36%',
                        'suitable_for': '通用分词，性能优异'
                    },
                    {
                        'model': 'FINE_ELECTRA_SMALL_ZH', 
                        'desc': '细粒度ELECTRA小模型',
                        'size': '45MB',
                        'performance': 'F1: 98.11%',
                        'suitable_for': '精细分词，细粒度更好'
                    },
                    {
                        'model': 'CTB9_TOK_ELECTRA_SMALL',
                        'desc': 'CTB9训练的ELECTRA小模型',
                        'size': '45MB', 
                        'performance': 'F1: 97.26%',
                        'suitable_for': 'CTB标准分词'
                    }
                ]
                
                # 尝试加载首选的分词模型
                for config in tokenizer_configs:
                    try:
                        model_key = config['model']
                        print(f"    尝试加载 {config['desc']} ({config['size']}, {config['performance']})...")
                        
                        # 获取模型URL
                        model_url = getattr(hanlp.pretrained.tok, model_key)
                        
                        # 加载分词器
                        start_time = time.time()
                        self.tokenizer = hanlp.load(model_url)
                        load_time = time.time() - start_time
                        
                        self.model_name = config['desc']
                        print(f"    ✅ 成功加载 {config['desc']} (耗时: {load_time:.2f}秒)")
                        
                        # 设置类级别的初始化标志
                        HanlpTokenizer._is_initialized = True
                        HanlpTokenizer._shared_tokenizer = self.tokenizer
                        return True
                        
                    except Exception as e:
                        print(f"    ❌ 加载 {config['desc']} 失败: {str(e)}")
                        continue
                
                # 如果所有模型都加载失败
                print("    ❌ 所有HanLP分词模型加载失败")
                return False
                
        except ImportError:
            print("  ❌ HanLP未安装，请运行: pip install hanlp")
            return False
        except Exception as e:
            print(f"  ❌ HanLP分词器初始化失败: {str(e)}")
            return False
    
    def cut(self, text: str) -> List[str]:
        """分词功能"""
        if not HanlpTokenizer._is_initialized:
            if not self.initialize():
                raise TokenizerError("HanLP分词器初始化失败")
        
        try:
            if not text or not text.strip():
                return []
            
            # 使用共享的分词器实例
            tokenizer = HanlpTokenizer._shared_tokenizer or self.tokenizer
            
            # HanLP的分词器接受字符串或字符串列表
            if isinstance(text, str):
                result = tokenizer([text])  # 需要列表输入
                return result[0] if result else []
            else:
                result = tokenizer(text)
                return result[0] if result else []
                
        except Exception as e:
            print(f"警告: HanLP分词失败: {str(e)}")
            # 简单的字符级别回退
            return list(text)
    
    def posseg(self, text: str) -> List[Tuple[str, str]]:
        """
        词性标注功能
        注意：此版本专注于分词，提供基础词性标注
        """
        try:
            # 先进行分词
            words = self.cut(text)
            
            # 简单的词性推断
            result = []
            for word in words:
                if word.isdigit():
                    pos = 'm'  # 数词
                elif word in ['的', '了', '在', '是', '有', '和', '与', '或', '把', '被', '让', '给']:
                    pos = 'p'  # 介词/助词
                elif len(word) == 1 and not word.isalnum():
                    pos = 'w'  # 标点符号
                elif word in ['我', '你', '他', '她', '它', '我们', '你们', '他们', '这', '那']:
                    pos = 'r'  # 代词
                else:
                    pos = 'n'  # 默认为名词
                
                result.append((word, pos))
            
            return result
            
        except Exception as e:
            print(f"警告: HanLP词性标注失败: {str(e)}")
            # 回退到简单分词
            words = self.cut(text)
            return [(word, 'n') for word in words]
    
    def tokenize(self, text: str) -> List[Tuple[str, int, int]]:
        """精确分词，返回词和位置信息"""
        try:
            words = self.cut(text)
            result = []
            start = 0
            
            for word in words:
                end = start + len(word)
                result.append((word, start, end))
                start = end
            
            return result
            
        except Exception as e:
            print(f"警告: HanLP精确分词失败: {str(e)}")
            return [(char, i, i+1) for i, char in enumerate(text)]
    
    def get_info(self) -> dict:
        info = super().get_info()
        try:
            import hanlp
            version = getattr(hanlp, '__version__', 'unknown')
        except ImportError:
            version = 'not installed'
        
        info.update({
            'version': version,
            'model': self.model_name if self.model_name else 'unknown',
            'description': 'HanLP中文分词器（轻量化版）',
            'features': ['高精度分词'],
            'dependencies': ['hanlp', 'torch'],
            'performance': '高精度',
            'accuracy': '优秀 (F1: 97-98%)',
            'note': '仅加载分词模型，不包含其他NLP功能',
            'model_type': 'Transformer-based tokenizer',
            'optimization': '单任务模型，性能优化'
        })
        return info


# 分词器工厂类
class TokenizerFactory:
    """分词器工厂类"""
    
    _instance = None
    _tokenizers = {}
    _available_tokenizers_cache = None  # 缓存可用分词器列表
    _tokenizer_info_cache = {}  # 缓存分词器信息
    _available_tokenizers = {
        'jieba': JiebaTokenizer,
        'thulac': ThulacTokenizer,
        'hanlp': HanlpTokenizer  # 启用优化版HanLP分词器
    }
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TokenizerFactory, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def _check_tokenizer_availability(cls, name: str, tokenizer_class) -> bool:
        """检查单个分词器是否可用，不进行实际初始化"""
        try:
            if name == 'jieba':
                import jieba
                return True
            elif name == 'thulac':
                import thulac
                return True
            elif name == 'hanlp':
                import hanlp
                return True
            else:
                return False
        except ImportError:
            return False
        except Exception:
            return False
    
    @classmethod
    def get_available_tokenizers(cls) -> List[str]:
        """获取所有可用的分词器列表 - 使用缓存优化性能"""
        # 如果已经缓存，直接返回
        if cls._available_tokenizers_cache is not None:
            return cls._available_tokenizers_cache
        
        available = []
        for name, tokenizer_class in cls._available_tokenizers.items():
            # 只检查库是否可导入，不进行实际初始化
            if cls._check_tokenizer_availability(name, tokenizer_class):
                available.append(name)
        
        # 缓存结果
        cls._available_tokenizers_cache = available
        return available
    
    @classmethod
    def get_tokenizer(cls, name: str) -> BaseTokenizer:
        """获取指定名称的分词器实例 - 使用单例模式"""
        if name not in cls._available_tokenizers:
            raise ValueError(f"不支持的分词器: {name}")
        
        # 检查是否已经创建过实例
        if name in cls._tokenizers:
            return cls._tokenizers[name]
        
        # 创建新实例并初始化
        tokenizer_class = cls._available_tokenizers[name]
        tokenizer = tokenizer_class()
        tokenizer.initialize()
        cls._tokenizers[name] = tokenizer
        return tokenizer
    
    @classmethod
    def get_tokenizer_info(cls, name: str) -> Dict[str, Any]:
        """获取指定分词器的信息 - 使用缓存避免重复初始化"""
        if name not in cls._available_tokenizers:
            return {'name': name, 'available': False, 'error': f'不支持的分词器: {name}'}
        
        # 检查缓存
        if name in cls._tokenizer_info_cache:
            return cls._tokenizer_info_cache[name]
        
        try:
            # 首先检查基本可用性
            if not cls._check_tokenizer_availability(name, cls._available_tokenizers[name]):
                info = {
                    'name': name,
                    'available': False,
                    'error': f'{name}库未安装'
                }
                cls._tokenizer_info_cache[name] = info
                return info
            
            # 尝试获取实例（会使用缓存）
            tokenizer = cls.get_tokenizer(name)
            info = tokenizer.get_info()
            info['available'] = True
            
            # 缓存结果
            cls._tokenizer_info_cache[name] = info
            return info
            
        except Exception as e:
            info = {
                'name': name,
                'available': False,
                'error': str(e)
            }
            cls._tokenizer_info_cache[name] = info
            return info
    
    @classmethod
    def clear_cache(cls):
        """清理所有缓存"""
        cls._available_tokenizers_cache = None
        cls._tokenizer_info_cache = {}
        # 不清理_tokenizers，因为这些是已初始化的实例


# 全局函数接口（供外部调用）
def get_available_tokenizers() -> List[str]:
    """获取所有可用的分词器列表"""
    return TokenizerFactory.get_available_tokenizers()


def get_tokenizer(name: str) -> BaseTokenizer:
    """获取指定名称的分词器实例"""
    return TokenizerFactory.get_tokenizer(name)


def get_tokenizer_info(name: str) -> Dict[str, Any]:
    """获取指定分词器的信息"""
    return TokenizerFactory.get_tokenizer_info(name)


# 导出的公共接口
__all__ = [
    'TokenizerError',
    'TokenizerInitError', 
    'TokenizerProcessError',
    'BaseTokenizer',
    'JiebaTokenizer',
    'ThulacTokenizer',
    'HanlpTokenizer',
    'TokenizerFactory',
    'get_available_tokenizers',
    'get_tokenizer',
    'get_tokenizer_info'
] 