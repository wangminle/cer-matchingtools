# 三种分词工具切换功能测试用例

## 1. 单元测试用例

### 1.1 分词器抽象层测试 (test_tokenizers.py)

#### 测试类: TestBaseTokenizer
```python
class TestBaseTokenizer(unittest.TestCase):
    """测试分词器抽象基类"""
    
    def test_validate_text_valid_input(self):
        """测试有效文本输入验证"""
        # 测试数据
        valid_texts = [
            "我来到北京清华大学",
            "Hello World 你好世界",
            "123 ABC 中文",
            "   带空格的文本   "
        ]
        # 预期结果: 返回清理后的文本
        
    def test_validate_text_invalid_input(self):
        """测试无效文本输入验证"""
        # 测试数据
        invalid_inputs = [None, 123, [], {}, ""]
        # 预期结果: 抛出TokenizerProcessError或返回空字符串
        
    def test_get_info(self):
        """测试获取分词器信息"""
        # 预期结果: 返回包含name, initialized, version的字典
```

#### 测试类: TestJiebaTokenizer
```python
class TestJiebaTokenizer(unittest.TestCase):
    """测试Jieba分词器实现"""
    
    def setUp(self):
        self.tokenizer = JiebaTokenizer()
        self.test_text = "我来到北京清华大学"
        
    def test_initialize_success(self):
        """测试Jieba分词器初始化成功"""
        result = self.tokenizer.initialize()
        self.assertTrue(result)
        self.assertTrue(self.tokenizer.is_initialized)
        
    def test_cut_basic(self):
        """测试基础分词功能"""
        # 测试数据
        test_cases = [
            ("我来到北京清华大学", ["我", "来到", "北京", "清华大学"]),
            ("他来到了网易杭研大厦", ["他", "来到", "了", "网易", "杭研", "大厦"]),
            ("", [])
        ]
        # 验证分词结果的类型和长度
        
    def test_posseg_functionality(self):
        """测试词性标注功能"""
        result = self.tokenizer.posseg(self.test_text)
        # 验证返回类型为list[tuple[str, str]]
        # 验证每个元组包含词语和词性
        
    def test_tokenize_positions(self):
        """测试精确分词位置信息"""
        result = self.tokenizer.tokenize(self.test_text)
        # 验证返回类型为list[tuple[str, int, int]]
        # 验证位置信息的正确性
        # 验证位置连续性
        
    def test_error_handling(self):
        """测试错误处理"""
        # 测试无效输入的处理
        with self.assertRaises(TokenizerProcessError):
            self.tokenizer.cut(None)
```

#### 测试类: TestThulacTokenizer
```python
class TestThulacTokenizer(unittest.TestCase):
    """测试THULAC分词器实现"""
    
    def setUp(self):
        try:
            self.tokenizer = ThulacTokenizer()
            self.available = True
        except TokenizerInitError:
            self.available = False
            
    def test_availability_check(self):
        """测试THULAC可用性检查"""
        # 如果THULAC未安装，验证异常处理
        
    @unittest.skipUnless(THULAC_AVAILABLE, "THULAC not available")
    def test_cut_functionality(self):
        """测试THULAC分词功能"""
        if not self.available:
            self.skipTest("THULAC not available")
            
        result = self.tokenizer.cut("我来到北京清华大学")
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)
        
    @unittest.skipUnless(THULAC_AVAILABLE, "THULAC not available")
    def test_posseg_pos_tags(self):
        """测试THULAC词性标注"""
        # 验证词性标注结果格式
        # 验证词性标签的有效性
        
    @unittest.skipUnless(THULAC_AVAILABLE, "THULAC not available")
    def test_tokenize_position_calculation(self):
        """测试THULAC位置计算的准确性"""
        text = "我来到北京清华大学"
        result = self.tokenizer.tokenize(text)
        
        # 验证位置计算的准确性
        reconstructed = ""
        for word, start, end in result:
            reconstructed += word
        self.assertEqual(reconstructed, text.replace(" ", ""))
```

#### 测试类: TestHanlpTokenizer
```python
class TestHanlpTokenizer(unittest.TestCase):
    """测试HanLP分词器实现"""
    
    def setUp(self):
        try:
            self.tokenizer = HanlpTokenizer()
            self.available = True
        except TokenizerInitError:
            self.available = False
            
    @unittest.skipUnless(HANLP_AVAILABLE, "HanLP not available")
    def test_model_loading(self):
        """测试HanLP模型加载"""
        # 验证模型加载是否成功
        # 验证初始化状态
        
    @unittest.skipUnless(HANLP_AVAILABLE, "HanLP not available")
    def test_cut_with_bert_model(self):
        """测试HanLP BERT模型分词"""
        if not self.available:
            self.skipTest("HanLP not available")
            
        result = self.tokenizer.cut("我来到北京清华大学")
        self.assertIsInstance(result, list)
        
    @unittest.skipUnless(HANLP_AVAILABLE, "HanLP not available")
    def test_tokenize_offset_support(self):
        """测试HanLP偏移量支持"""
        # 验证是否支持输出偏移量
        # 验证偏移量的准确性
```

### 1.2 分词器工厂测试 (test_factory.py)

#### 测试类: TestTokenizerFactory
```python
class TestTokenizerFactory(unittest.TestCase):
    """测试分词器工厂"""
    
    def test_get_available_tokenizers(self):
        """测试获取可用分词器列表"""
        available = get_available_tokenizers()
        self.assertIsInstance(available, list)
        self.assertIn('jieba', available)  # jieba应该总是可用
        
    def test_create_jieba_tokenizer(self):
        """测试创建Jieba分词器"""
        tokenizer = get_tokenizer('jieba')
        self.assertIsInstance(tokenizer, JiebaTokenizer)
        self.assertTrue(tokenizer.is_initialized)
        
    def test_create_invalid_tokenizer(self):
        """测试创建无效分词器"""
        with self.assertRaises(ValueError):
            get_tokenizer('invalid_tokenizer')
            
    def test_singleton_pattern(self):
        """测试单例模式"""
        tokenizer1 = get_tokenizer('jieba')
        tokenizer2 = get_tokenizer('jieba')
        self.assertIs(tokenizer1, tokenizer2)
        
    def test_tokenizer_info(self):
        """测试分词器信息获取"""
        from src.tokenizers.factory import TokenizerFactory
        info = TokenizerFactory.get_tokenizer_info('jieba')
        self.assertIn('name', info)
        self.assertIn('initialized', info)
```

### 1.3 ASRMetrics重构测试 (test_asr_metrics.py)

#### 测试类: TestASRMetricsRefactored
```python
class TestASRMetricsRefactored(unittest.TestCase):
    """测试重构后的ASRMetrics类"""
    
    def setUp(self):
        self.asr_metrics = ASRMetrics(tokenizer_name='jieba')
        self.ref_text = "今天天气真不错，阳光明媚。"
        self.hyp_text = "今天天气真不错阳光明美"
        
    def test_initialization_with_valid_tokenizer(self):
        """测试使用有效分词器初始化"""
        metrics = ASRMetrics(tokenizer_name='jieba')
        self.assertEqual(metrics.tokenizer_name, 'jieba')
        self.assertIsNotNone(metrics.tokenizer)
        
    def test_initialization_with_invalid_tokenizer(self):
        """测试使用无效分词器初始化"""
        # 应该回退到jieba
        metrics = ASRMetrics(tokenizer_name='invalid')
        self.assertEqual(metrics.tokenizer_name, 'jieba')
        
    def test_preprocess_chinese_text(self):
        """测试中文文本预处理"""
        result = self.asr_metrics.preprocess_chinese_text(self.ref_text)
        self.assertIsInstance(result, str)
        # 验证分词预处理的效果
        
    def test_filter_filler_words(self):
        """测试语气词过滤"""
        text_with_fillers = "嗯，今天天气真不错啊。"
        result = self.asr_metrics.filter_filler_words(text_with_fillers)
        self.assertNotIn("嗯", result)
        self.assertNotIn("啊", result)
        
    def test_get_character_positions(self):
        """测试字符位置获取"""
        result = self.asr_metrics.get_character_positions(self.ref_text)
        self.assertIsInstance(result, list)
        # 验证位置信息的格式和准确性
        
    def test_calculate_cer_consistency(self):
        """测试不同分词器CER计算一致性"""
        # 测试使用不同分词器计算相同文本的CER
        available_tokenizers = get_available_tokenizers()
        results = {}
        
        for tokenizer_name in available_tokenizers:
            metrics = ASRMetrics(tokenizer_name=tokenizer_name)
            cer = metrics.calculate_cer(self.ref_text, self.hyp_text)
            results[tokenizer_name] = cer
            
        # 验证结果在合理范围内
        for cer in results.values():
            self.assertGreaterEqual(cer, 0.0)
            self.assertLessEqual(cer, 1.0)
            
    def test_method_backward_compatibility(self):
        """测试方法向后兼容性"""
        # 验证所有原有方法仍然可用
        methods_to_test = [
            'calculate_accuracy',
            'calculate_detailed_metrics',
            'highlight_errors'
        ]
        
        for method_name in methods_to_test:
            self.assertTrue(hasattr(self.asr_metrics, method_name))
            method = getattr(self.asr_metrics, method_name)
            self.assertTrue(callable(method))
```

## 2. 集成测试用例

### 2.1 GUI集成测试 (test_gui_integration.py)

#### 测试类: TestGUITokenizerIntegration
```python
class TestGUITokenizerIntegration(unittest.TestCase):
    """测试GUI与分词器的集成"""
    
    def setUp(self):
        self.root = tk.Tk()
        self.app = ASRComparisonTool(self.root)
        
    def tearDown(self):
        self.root.destroy()
        
    def test_tokenizer_combo_initialization(self):
        """测试分词器下拉框初始化"""
        # 验证下拉框包含可用分词器
        values = self.app.tokenizer_combo['values']
        self.assertIn('jieba', values)
        
    def test_tokenizer_selection_change(self):
        """测试分词器选择变化"""
        # 模拟用户选择不同分词器
        available_tokenizers = self.app.available_tokenizers
        
        for tokenizer_name in available_tokenizers:
            self.app.tokenizer_var.set(tokenizer_name)
            self.app.on_tokenizer_changed()
            # 验证状态更新
            
    def test_tokenizer_status_display(self):
        """测试分词器状态显示"""
        # 测试可用分词器的状态显示
        self.app.tokenizer_var.set('jieba')
        self.app.update_tokenizer_info()
        # 验证状态标签显示正确信息
        
    def test_calculate_with_different_tokenizers(self):
        """测试使用不同分词器进行计算"""
        # 准备测试文件
        self.prepare_test_files()
        
        available_tokenizers = self.app.available_tokenizers
        for tokenizer_name in available_tokenizers:
            with self.subTest(tokenizer=tokenizer_name):
                self.app.tokenizer_var.set(tokenizer_name)
                # 模拟计算过程
                # 验证结果正确性
                
    def prepare_test_files(self):
        """准备测试文件"""
        # 创建临时测试文件
        import tempfile
        import os
        
        self.temp_dir = tempfile.mkdtemp()
        
        # 创建ASR文件
        asr_content = "今天天气真不错阳光明美"
        with open(os.path.join(self.temp_dir, "test_asr.txt"), 'w', encoding='utf-8') as f:
            f.write(asr_content)
            
        # 创建标注文件
        ref_content = "今天天气真不错，阳光明媚。"
        with open(os.path.join(self.temp_dir, "test_ref.txt"), 'w', encoding='utf-8') as f:
            f.write(ref_content)
```

### 2.2 命令行集成测试 (test_cli_integration.py)

#### 测试类: TestCLITokenizerIntegration
```python
class TestCLITokenizerIntegration(unittest.TestCase):
    """测试命令行工具与分词器的集成"""
    
    def setUp(self):
        self.prepare_test_files()
        
    def test_tokenizer_parameter(self):
        """测试--tokenizer参数"""
        available_tokenizers = get_available_tokenizers()
        
        for tokenizer_name in available_tokenizers:
            with self.subTest(tokenizer=tokenizer_name):
                # 模拟命令行调用
                result = self.run_cli_command([
                    '--ref', self.ref_file,
                    '--asr', self.asr_file,
                    '--tokenizer', tokenizer_name
                ])
                # 验证命令执行成功
                # 验证输出包含预期信息
                
    def test_invalid_tokenizer_parameter(self):
        """测试无效分词器参数"""
        result = self.run_cli_command([
            '--ref', self.ref_file,
            '--asr', self.asr_file,
            '--tokenizer', 'invalid_tokenizer'
        ])
        # 验证命令返回错误
        self.assertNotEqual(result.returncode, 0)
        
    def test_tokenizer_with_details(self):
        """测试分词器与详细分析结合"""
        available_tokenizers = get_available_tokenizers()
        
        for tokenizer_name in available_tokenizers:
            with self.subTest(tokenizer=tokenizer_name):
                result = self.run_cli_command([
                    '--ref', self.ref_file,
                    '--asr', self.asr_file,
                    '--tokenizer', tokenizer_name,
                    '--details'
                ])
                # 验证详细输出包含分词器信息
                
    def run_cli_command(self, args):
        """运行命令行命令"""
        import subprocess
        import sys
        
        cmd = [sys.executable, 'check_accuracy.py'] + args
        return subprocess.run(cmd, capture_output=True, text=True)
        
    def prepare_test_files(self):
        """准备测试文件"""
        import tempfile
        import os
        
        self.temp_dir = tempfile.mkdtemp()
        self.ref_file = os.path.join(self.temp_dir, "ref.txt")
        self.asr_file = os.path.join(self.temp_dir, "asr.txt")
        
        with open(self.ref_file, 'w', encoding='utf-8') as f:
            f.write("今天天气真不错，阳光明媚。")
            
        with open(self.asr_file, 'w', encoding='utf-8') as f:
            f.write("今天天气真不错阳光明美")
```

### 2.3 端到端测试 (test_e2e.py)

#### 测试类: TestEndToEndWorkflow
```python
class TestEndToEndWorkflow(unittest.TestCase):
    """端到端工作流程测试"""
    
    def test_complete_workflow_with_different_tokenizers(self):
        """测试使用不同分词器的完整工作流程"""
        test_cases = [
            {
                'ref': "北京大学是中国最著名的高等学府之一。",
                'asr': "北京大学是中国最著名的高登学府之一。",
                'expected_errors': ['著->登']
            },
            {
                'ref': "今天天气真不错，阳光明媚。",
                'asr': "今天天气真不错阳光明美",
                'expected_errors': ['，->删除', '媚->美']
            }
        ]
        
        available_tokenizers = get_available_tokenizers()
        
        for tokenizer_name in available_tokenizers:
            for i, test_case in enumerate(test_cases):
                with self.subTest(tokenizer=tokenizer_name, case=i):
                    # 创建ASRMetrics实例
                    metrics = ASRMetrics(tokenizer_name=tokenizer_name)
                    
                    # 计算详细指标
                    result = metrics.calculate_detailed_metrics(
                        test_case['ref'], 
                        test_case['asr']
                    )
                    
                    # 验证基本指标
                    self.assertIn('accuracy', result)
                    self.assertIn('cer', result)
                    self.assertGreaterEqual(result['accuracy'], 0.0)
                    self.assertLessEqual(result['accuracy'], 1.0)
                    
    def test_performance_comparison(self):
        """测试不同分词器的性能对比"""
        import time
        
        large_text = "我来到北京清华大学学习自然语言处理技术。" * 100
        available_tokenizers = get_available_tokenizers()
        performance_results = {}
        
        for tokenizer_name in available_tokenizers:
            start_time = time.time()
            
            metrics = ASRMetrics(tokenizer_name=tokenizer_name)
            for _ in range(10):  # 重复10次测试
                metrics.preprocess_chinese_text(large_text)
                
            end_time = time.time()
            performance_results[tokenizer_name] = end_time - start_time
            
        # 验证所有分词器都能在合理时间内完成
        for tokenizer_name, duration in performance_results.items():
            self.assertLess(duration, 10.0, f"{tokenizer_name} took too long: {duration}s")
            
    def test_accuracy_consistency(self):
        """测试不同分词器准确率计算的一致性"""
        test_pairs = [
            ("完全相同的文本", "完全相同的文本"),  # 期望CER=0
            ("完全不同", "totally different"),      # 期望CER=1
            ("部分相同的文本", "部分相同文本")      # 期望0<CER<1
        ]
        
        available_tokenizers = get_available_tokenizers()
        
        for ref, hyp in test_pairs:
            results = {}
            for tokenizer_name in available_tokenizers:
                metrics = ASRMetrics(tokenizer_name=tokenizer_name)
                cer = metrics.calculate_cer(ref, hyp)
                results[tokenizer_name] = cer
                
            # 验证结果的合理性
            if ref == hyp:
                for cer in results.values():
                    self.assertAlmostEqual(cer, 0.0, places=2)
            elif not any(c1 == c2 for c1, c2 in zip(ref, hyp)):
                for cer in results.values():
                    self.assertGreater(cer, 0.8)  # 应该很高但不一定是1.0
```

## 3. 性能和稳定性测试

### 3.1 性能测试用例
```python
class TestPerformance(unittest.TestCase):
    """性能测试"""
    
    def test_large_file_processing(self):
        """测试大文件处理性能"""
        # 创建大文件内容
        large_content = "这是一段很长的测试文本。" * 1000
        
        for tokenizer_name in get_available_tokenizers():
            with self.subTest(tokenizer=tokenizer_name):
                start_time = time.time()
                metrics = ASRMetrics(tokenizer_name=tokenizer_name)
                result = metrics.calculate_cer(large_content, large_content)
                duration = time.time() - start_time
                
                self.assertLess(duration, 30.0)  # 应该在30秒内完成
                self.assertAlmostEqual(result, 0.0, places=2)
                
    def test_memory_usage(self):
        """测试内存使用"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # 创建多个分词器实例
        tokenizers = []
        for _ in range(10):
            for tokenizer_name in get_available_tokenizers():
                tokenizers.append(ASRMetrics(tokenizer_name=tokenizer_name))
                
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # 内存增长应该在合理范围内（比如不超过500MB）
        self.assertLess(memory_increase, 500 * 1024 * 1024)
```

### 3.2 稳定性测试用例
```python
class TestStability(unittest.TestCase):
    """稳定性测试"""
    
    def test_error_recovery(self):
        """测试错误恢复能力"""
        # 测试各种异常输入
        invalid_inputs = [None, "", "   ", 123, [], {}]
        
        for tokenizer_name in get_available_tokenizers():
            metrics = ASRMetrics(tokenizer_name=tokenizer_name)
            
            for invalid_input in invalid_inputs:
                with self.subTest(tokenizer=tokenizer_name, input=invalid_input):
                    # 应该优雅处理错误，不崩溃
                    try:
                        result = metrics.calculate_cer("valid text", invalid_input)
                        # 应该返回合理的默认值
                    except Exception as e:
                        # 应该是预期的异常类型
                        self.assertIsInstance(e, (TokenizerError, ValueError, TypeError))
                        
    def test_concurrent_usage(self):
        """测试并发使用"""
        import threading
        import time
        
        results = []
        errors = []
        
        def worker(tokenizer_name):
            try:
                metrics = ASRMetrics(tokenizer_name=tokenizer_name)
                for i in range(100):
                    result = metrics.calculate_cer(
                        f"测试文本{i}", 
                        f"测试文本{i}"
                    )
                    results.append(result)
            except Exception as e:
                errors.append(e)
                
        threads = []
        for tokenizer_name in get_available_tokenizers():
            thread = threading.Thread(target=worker, args=(tokenizer_name,))
            threads.append(thread)
            thread.start()
            
        for thread in threads:
            thread.join()
            
        # 验证没有错误发生
        self.assertEqual(len(errors), 0)
        # 验证所有结果都是0（相同文本）
        for result in results:
            self.assertAlmostEqual(result, 0.0, places=2)
```

## 4. 运行测试的命令

```bash
# 运行所有单元测试
python -m pytest tests/test_tokenizers.py -v

# 运行集成测试
python -m pytest tests/test_gui_integration.py -v
python -m pytest tests/test_cli_integration.py -v

# 运行端到端测试
python -m pytest tests/test_e2e.py -v

# 运行性能测试
python -m pytest tests/test_performance.py -v --timeout=60

# 运行所有测试并生成覆盖率报告
python -m pytest tests/ --cov=src --cov-report=html

# 运行特定分词器的测试（如果该分词器可用）
python -m pytest tests/ -k "jieba" -v
python -m pytest tests/ -k "thulac" -v
python -m pytest tests/ -k "hanlp" -v
```

这些测试用例覆盖了：
1. **功能正确性** - 确保所有分词器实现正确的接口
2. **错误处理** - 验证异常情况的处理
3. **性能要求** - 确保性能在可接受范围内
4. **稳定性** - 验证系统在各种条件下的稳定性
5. **兼容性** - 确保向后兼容和跨分词器一致性
6. **集成性** - 验证GUI和CLI的完整工作流程 