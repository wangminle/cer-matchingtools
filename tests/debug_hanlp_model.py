#!/usr/bin/env python3
"""
详细检查HanLP模型加载状态
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def debug_hanlp_loading():
    """调试HanLP模型加载过程"""
    
    print("🔍 调试HanLP模型加载...")
    
    try:
        import hanlp
        print(f"✅ HanLP版本: {hanlp.__version__}")
        
        # 尝试加载不同的模型
        models_to_try = [
            'hanlp.pretrained.tok.SIGHAN2005_PKU_BERT_BASE_ZH',
            'hanlp.pretrained.tok.CTB6_CONVSEG',
            'PKU_NAME_MERGED_SYS_OPEN'
        ]
        
        loaded_model = None
        for model_path in models_to_try:
            try:
                print(f"\n🔄 尝试加载模型: {model_path}")
                if model_path.startswith('hanlp.'):
                    # 使用eval来访问嵌套属性
                    model_ref = eval(model_path)
                    loaded_model = hanlp.load(model_ref)
                else:
                    loaded_model = hanlp.load(model_path)
                
                print(f"✅ 成功加载: {type(loaded_model)}")
                
                # 测试模型
                test_result = loaded_model("测试文本")
                print(f"📝 测试结果: {test_result}")
                print(f"🆔 模型ID: {id(loaded_model)}")
                break
                
            except Exception as e:
                print(f"❌ 加载失败: {str(e)}")
                continue
        
        if loaded_model is None:
            print("❌ 所有模型加载都失败了！")
            return
            
        # 检查模型的内部结构
        print(f"\n🔬 模型详细信息:")
        print(f"模型类型: {type(loaded_model)}")
        print(f"模型属性: {dir(loaded_model)}")
        
        if hasattr(loaded_model, 'model'):
            print(f"内部模型: {type(loaded_model.model)}")
            print(f"内部模型ID: {id(loaded_model.model)}")
        
        if hasattr(loaded_model, 'config'):
            print(f"配置: {loaded_model.config}")
            
        # 测试多个相同的文本
        test_texts = [
            "我爱北京天安门",
            "中国科学技术大学", 
            "人工智能技术发展"
        ]
        
        print(f"\n📝 详细分词测试:")
        for text in test_texts:
            result = loaded_model(text)
            print(f"'{text}' -> {result}")
            
    except ImportError:
        print("❌ HanLP未安装")
    except Exception as e:
        print(f"❌ 调试失败: {str(e)}")
        import traceback
        traceback.print_exc()

def check_model_fallback():
    """检查是否存在模型回退机制"""
    
    print("\n🔍 检查模型回退机制...")
    
    try:
        from text_tokenizers.tokenizers.hanlp_tokenizer import HanlpTokenizer
        
        # 创建实例并检查初始化过程
        tokenizer = HanlpTokenizer()
        
        # 查看初始化前的状态
        print(f"初始化前 - tok_model: {tokenizer.tok_model}")
        print(f"初始化前 - pos_model: {tokenizer.pos_model}")
        
        # 执行初始化
        success = tokenizer.initialize()
        print(f"初始化结果: {success}")
        
        # 查看初始化后的状态
        print(f"初始化后 - tok_model: {type(tokenizer.tok_model)}")
        print(f"初始化后 - pos_model: {tokenizer.pos_model}")
        print(f"tok_model ID: {id(tokenizer.tok_model)}")
        
        # 检查模型是否有特殊的fallback行为
        if hasattr(tokenizer.tok_model, '__class__'):
            print(f"模型类: {tokenizer.tok_model.__class__}")
            print(f"模型模块: {tokenizer.tok_model.__module__}")
            
    except Exception as e:
        print(f"❌ 检查失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_hanlp_loading()
    check_model_fallback() 