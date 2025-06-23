# 三种分词工具切换功能 - 测试计划

## 测试概述

本测试计划涵盖三种分词工具（Jieba、THULAC、HanLP）切换功能的完整测试，包括单元测试、集成测试和端到端测试。

## 1. 单元测试用例

### 1.1 分词器抽象层测试 (`tests/test_tokenizers_base.py`)

#### BaseTokenizer 抽象类测试
```python
class TestBaseTokenizer(unittest.TestCase):
    def test_abstract_methods_not_implemented(self):
        """测试抽象方法不能直接实例化"""
        with self.assertRaises(TypeError):
            BaseTokenizer()
    
    def test_validate_text_valid_input(self):
        """测试有效文本输入验证"""
        # 通过具体实现类测试
        pass
    
    def test_validate_text_invalid_input(self):
        """测试无效文本输入验证"""
        # 测试非字符串输入、空字符串等
        pass
    
    def test_get_info_method(self):
        """测试获取分词器信息方法"""
        pass
```

#### 异常处理测试
```python
class TestTokenizerExceptions(unittest.TestCase):
    def test_tokenizer_error_hierarchy(self):
        """测试异常继承关系"""
        self.assertTrue(issubclass(TokenizerInitError, TokenizerError))
        self.assertTrue(issubclass(TokenizerProcessError, TokenizerError))
    
    def test_exception_messages(self):
        """测试异常消息格式"""
        error = TokenizerInitError("测试错误")
        self.assertEqual(str(error), "测试错误")
```

### 1.2 具体分词器测试

#### JiebaTokenizer 测试 (`tests/test_jieba_tokenizer.py`)
```python
class TestJiebaTokenizer(unittest.TestCase):
    def setUp(self):
        self.tokenizer = JiebaTokenizer()
        self.tokenizer.initialize()
        self.test_text = "我来到北京清华大学"
        self.empty_text = ""
        self.english_text = "Hello world"
        self.mixed_text = "今天weather很好"
    
    def test_initialization(self):
        """测试Jieba分词器初始化"""
        self.assertTrue(self.tokenizer.is_initialized)
        self.assertEqual(self.tokenizer.name, "JiebaTokenizer")
    
    def test_cut_basic_functionality(self):
        """测试基础分词功能"""
        result = self.tokenizer.cut(self.test_text)
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)
        self.assertIn("北京", result)
        self.assertIn("清华大学", result)
    
    def test_cut_empty_text(self):
        """测试空文本分词"""
        result = self.tokenizer.cut(self.empty_text)
        self.assertEqual(result, [])
    
    def test_cut_english_text(self):
        """测试英文文本分词"""
        result = self.tokenizer.cut(self.english_text)
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)
    
    def test_cut_mixed_text(self):
        """测试中英混合文本分词"""
        result = self.tokenizer.cut(self.mixed_text)
        self.assertIsInstance(result, list)
        self.assertIn("今天", result)
        self.assertIn("weather", result)
    
    def test_posseg_functionality(self):
        """测试词性标注功能"""
        result = self.tokenizer.posseg(self.test_text)
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)
        
        # 检查返回格式：(词语, 词性)
        for word, pos in result:
            self.assertIsInstance(word, str)
            self.assertIsInstance(pos, str)
        
        # 检查特定词性
        pos_dict = dict(result)
        self.assertIn("北京", pos_dict)
        self.assertEqual(pos_dict["北京"], "ns")  # 地名
    
    def test_tokenize_functionality(self):
        """测试tokenize功能（返回位置信息）"""
        result = self.tokenizer.tokenize(self.test_text)
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)
        
        # 检查返回格式：(词语, 起始位置, 结束位置)
        for word, start, end in result:
            self.assertIsInstance(word, str)
            self.assertIsInstance(start, int)
            self.assertIsInstance(end, int)
            self.assertTrue(start >= 0)
            self.assertTrue(end > start)
            self.assertEqual(self.test_text[start:end], word)
    
    def test_tokenize_position_accuracy(self):
        """测试tokenize位置准确性"""
        result = self.tokenizer.tokenize(self.test_text)
        reconstructed = ""
        for word, start, end in sorted(result, key=lambda x: x[1]):
            reconstructed += word
        
        # 重构的文本应该与原文本一致（去除空格）
        self.assertEqual(reconstructed.replace(" ", ""), self.test_text.replace(" ", ""))
    
    def test_error_handling(self):
        """测试错误处理"""
        # 测试非字符串输入
        with self.assertRaises(TokenizerProcessError):
            self.tokenizer.cut(123)
        
        with self.assertRaises(TokenizerProcessError):
            self.tokenizer.posseg(None)
    
    def test_performance_benchmark(self):
        """测试性能基准"""
        import time
        long_text = self.test_text * 1000
        
        start_time = time.time()
        result = self.tokenizer.cut(long_text)
        end_time = time.time()
        
        processing_time = end_time - start_time
        self.assertTrue(processing_time < 5.0)  # 应该在5秒内完成
        self.assertTrue(len(result) > 0)
```

#### ThulacTokenizer 测试 (`tests/test_thulac_tokenizer.py`)
```python
class TestThulacTokenizer(unittest.TestCase):
    def setUp(self):
        try:
            self.tokenizer = ThulacTokenizer()
            self.tokenizer.initialize()
            self.thulac_available = True
        except TokenizerInitError:
            self.thulac_available = False
            self.skipTest("THULAC未安装，跳过测试")
    
    def test_thulac_specific_features(self):
        """测试THULAC特有功能"""
        if not self.thulac_available:
            self.skipTest("THULAC不可用")
        
        text = "我来到北京清华大学"
        result = self.tokenizer.posseg(text)
        
        # THULAC的词性标注体系测试
        pos_tags = [pos for _, pos in result]
        self.assertTrue(any(tag in ['n', 'ns', 'v'] for tag in pos_tags))
    
    def test_tokenize_position_calculation(self):
        """测试THULAC的手动位置计算"""
        if not self.thulac_available:
            self.skipTest("THULAC不可用")
        
        text = "北京大学"
        result = self.tokenizer.tokenize(text)
        
        # 验证位置计算正确性
        for word, start, end in result:
            self.assertEqual(text[start:end], word)
        
        # 验证位置连续性
        sorted_result = sorted(result, key=lambda x: x[1])
        for i in range(len(sorted_result) - 1):
            current_end = sorted_result[i][2]
            next_start = sorted_result[i + 1][1]
            self.assertTrue(current_end <= next_start)
```

#### HanlpTokenizer 测试 (`tests/test_hanlp_tokenizer.py`)
```python
class TestHanlpTokenizer(unittest.TestCase):
    def setUp(self):
        try:
            self.tokenizer = HanlpTokenizer()
            self.tokenizer.initialize()
            self.hanlp_available = True
        except TokenizerInitError:
            self.hanlp_available = False
            self.skipTest("HanLP未安装或模型下载失败，跳过测试")
    
    def test_model_loading(self):
        """测试HanLP模型加载"""
        if not self.hanlp_available:
            self.skipTest("HanLP不可用")
        
        self.assertIsNotNone(self.tokenizer.tok_engine)
        self.assertIsNotNone(self.tokenizer.pos_engine)
    
    def test_hanlp_accuracy(self):
        """测试HanLP分词准确性"""
        if not self.hanlp_available:
            self.skipTest("HanLP不可用")
        
        text = "中国科学院计算技术研究所"
        result = self.tokenizer.cut(text)
        
        # HanLP应该能正确识别机构名
        self.assertIn("中国科学院", result)
        self.assertIn("计算技术研究所", result)
```

### 1.3 分词器工厂测试 (`tests/test_tokenizer_factory.py`)

```python
class TestTokenizerFactory(unittest.TestCase):
    def setUp(self):
        self.factory = TokenizerFactory()
    
    def test_get_available_tokenizers(self):
        """测试获取可用分词器列表"""
        available = self.factory.get_available_tokenizers()
        self.assertIsInstance(available, list)
        self.assertIn('jieba', available)  # jieba应该始终可用
    
    def test_create_jieba_tokenizer(self):
        """测试创建Jieba分词器"""
        tokenizer = self.factory.create_tokenizer('jieba')
        self.assertIsInstance(tokenizer, JiebaTokenizer)
        self.assertTrue(tokenizer.is_initialized)
    
    def test_singleton_pattern(self):
        """测试单例模式"""
        tokenizer1 = self.factory.create_tokenizer('jieba')
        tokenizer2 = self.factory.create_tokenizer('jieba')
        self.assertIs(tokenizer1, tokenizer2)
    
    def test_invalid_tokenizer_name(self):
        """测试无效分词器名称"""
        with self.assertRaises(ValueError):
            self.factory.create_tokenizer('invalid_tokenizer')
    
    def test_case_insensitive(self):
        """测试大小写不敏感"""
        tokenizer1 = self.factory.create_tokenizer('jieba')
        tokenizer2 = self.factory.create_tokenizer('JIEBA')
        self.assertIs(tokenizer1, tokenizer2)
    
    def test_get_tokenizer_info(self):
        """测试获取分词器信息"""
        info = self.factory.get_tokenizer_info('jieba')
        self.assertIsInstance(info, dict)
        self.assertIn('name', info)
        self.assertIn('initialized', info)
        self.assertIn('version', info)
```

### 1.4 ASRMetrics改造测试 (`tests/test_asr_metrics.py`)

```python
class TestASRMetricsWithTokenizers(unittest.TestCase):
    def setUp(self):
        self.ref_text = "今天天气真不错，阳光明媚。"
        self.hyp_text = "今天天气真不错阳光明美"
    
    def test_asr_metrics_with_jieba(self):
        """测试使用Jieba的ASRMetrics"""
        metrics = ASRMetrics(tokenizer_name='jieba')
        self.assertEqual(metrics.tokenizer_name, 'jieba')
        
        accuracy = metrics.calculate_accuracy(self.ref_text, self.hyp_text)
        self.assertIsInstance(accuracy, float)
        self.assertTrue(0 <= accuracy <= 1)
    
    def test_asr_metrics_fallback(self):
        """测试分词器回退机制"""
        # 使用不存在的分词器，应该回退到jieba
        metrics = ASRMetrics(tokenizer_name='nonexistent')
        self.assertEqual(metrics.tokenizer_name, 'jieba')
    
    def test_preprocess_chinese_text(self):
        """测试中文预处理"""
        metrics = ASRMetrics(tokenizer_name='jieba')
        result = metrics.preprocess_chinese_text(self.ref_text)
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)
    
    def test_filter_filler_words(self):
        """测试语气词过滤"""
        metrics = ASRMetrics(tokenizer_name='jieba')
        text_with_fillers = "嗯，今天天气真不错啊。"
        filtered = metrics.filter_filler_words(text_with_fillers)
        
        # 语气词应该被过滤
        self.assertNotIn("嗯", filtered)
        self.assertNotIn("啊", filtered)
        self.assertIn("今天", filtered)
    
    def test_get_character_positions(self):
        """测试字符位置获取"""
        metrics = ASRMetrics(tokenizer_name='jieba')
        positions = metrics.get_character_positions(self.ref_text)
        
        self.assertIsInstance(positions, list)
        self.assertTrue(len(positions) > 0)
        
        # 检查位置格式
        for char, pos in positions:
            self.assertIsInstance(char, str)
            self.assertIsInstance(pos, int)
            self.assertTrue(pos >= 0)
    
    def test_calculate_detailed_metrics(self):
        """测试详细指标计算"""
        metrics = ASRMetrics(tokenizer_name='jieba')
        result = metrics.calculate_detailed_metrics(self.ref_text, self.hyp_text)
        
        required_keys = ['cer', 'accuracy', 'substitutions', 'deletions', 
                        'insertions', 'ref_length', 'hyp_length']
        for key in required_keys:
            self.assertIn(key, result)
            self.assertIsInstance(result[key], (int, float))
```

## 2. 集成测试用例

### 2.1 分词器集成测试 (`tests/test_integration_tokenizers.py`)

```python
class TestTokenizerIntegration(unittest.TestCase):
    def setUp(self):
        self.test_texts = [
            "我来到北京清华大学",
            "中国科学院计算技术研究所",
            "今天天气真不错，阳光明媚。",
            "嗯，这个结果还可以吧。"
        ]
        self.available_tokenizers = get_available_tokenizers()
    
    def test_all_tokenizers_consistency(self):
        """测试所有可用分词器的一致性"""
        for tokenizer_name in self.available_tokenizers:
            with self.subTest(tokenizer=tokenizer_name):
                tokenizer = get_tokenizer(tokenizer_name)
                
                for text in self.test_texts:
                    # 测试基础分词
                    words = tokenizer.cut(text)
                    self.assertIsInstance(words, list)
                    
                    # 测试词性标注
                    pos_result = tokenizer.posseg(text)
                    self.assertIsInstance(pos_result, list)
                    self.assertEqual(len(pos_result), len([item for item in pos_result if len(item) == 2]))
                    
                    # 测试tokenize
                    tokens = tokenizer.tokenize(text)
                    self.assertIsInstance(tokens, list)
                    self.assertEqual(len(tokens), len([item for item in tokens if len(item) == 3]))
    
    def test_cross_tokenizer_cer_calculation(self):
        """测试不同分词器的CER计算结果"""
        ref_text = "今天天气真不错，阳光明媚。"
        hyp_text = "今天天气真不错阳光明美"
        
        results = {}
        for tokenizer_name in self.available_tokenizers:
            metrics = ASRMetrics(tokenizer_name=tokenizer_name)
            accuracy = metrics.calculate_accuracy(ref_text, hyp_text)
            results[tokenizer_name] = accuracy
        
        # 所有分词器的结果应该在合理范围内
        for tokenizer_name, accuracy in results.items():
            with self.subTest(tokenizer=tokenizer_name):
                self.assertTrue(0 <= accuracy <= 1)
                self.assertTrue(accuracy > 0.5)  # 这个例子的准确率应该不会太低
    
    def test_filler_word_filtering_consistency(self):
        """测试语气词过滤的一致性"""
        text_with_fillers = "嗯，今天天气真不错啊，呢。"
        
        for tokenizer_name in self.available_tokenizers:
            with self.subTest(tokenizer=tokenizer_name):
                metrics = ASRMetrics(tokenizer_name=tokenizer_name)
                filtered = metrics.filter_filler_words(text_with_fillers)
                
                # 常见语气词应该被过滤
                self.assertNotIn("嗯", filtered)
                self.assertNotIn("啊", filtered)
                self.assertNotIn("呢", filtered)
                # 实际内容应该保留
                self.assertIn("今天", filtered)
                self.assertIn("天气", filtered)
```

### 2.2 GUI集成测试 (`tests/test_gui_integration.py`)

```python
class TestGUIIntegration(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = ASRComparisonTool(self.root)
        self.root.withdraw()  # 隐藏窗口进行测试
    
    def tearDown(self):
        self.root.destroy()
    
    def test_tokenizer_selection_ui(self):
        """测试分词器选择UI"""
        # 检查分词器下拉框是否正确初始化
        self.assertIsNotNone(self.app.tokenizer_combo)
        self.assertTrue(len(self.app.available_tokenizers) > 0)
        self.assertIn('jieba', self.app.available_tokenizers)
    
    def test_tokenizer_info_update(self):
        """测试分词器信息更新"""
        # 模拟用户选择分词器
        self.app.tokenizer_var.set('jieba')
        self.app.update_tokenizer_info()
        
        # 检查信息标签是否更新
        info_text = self.app.tokenizer_info_label.cget('text')
        self.assertIn('版本', info_text)
    
    def test_calculation_with_different_tokenizers(self):
        """测试使用不同分词器进行计算"""
        # 创建测试文件
        import tempfile
        import os
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # 创建测试文件
            ref_file = os.path.join(temp_dir, 'ref.txt')
            asr_file = os.path.join(temp_dir, 'asr.txt')
            
            with open(ref_file, 'w', encoding='utf-8') as f:
                f.write("今天天气真不错，阳光明媚。")
            
            with open(asr_file, 'w', encoding='utf-8') as f:
                f.write("今天天气真不错阳光明美")
            
            # 模拟文件选择
            self.app.asr_files = [asr_file]
            self.app.ref_files = [ref_file]
            
            # 更新Canvas（模拟）
            self.app.update_canvas_items(self.app.asr_canvas, self.app.asr_files)
            self.app.update_canvas_items(self.app.ref_canvas, self.app.ref_files)
            
            # 测试不同分词器
            for tokenizer_name in self.app.available_tokenizers:
                with self.subTest(tokenizer=tokenizer_name):
                    self.app.tokenizer_var.set(tokenizer_name)
                    
                    # 模拟点击开始统计
                    try:
                        self.app.calculate_accuracy()
                        # 检查是否有结果
                        self.assertTrue(len(self.app.results) > 0)
                    except Exception as e:
                        self.fail(f"分词器 {tokenizer_name} 计算失败: {e}")
```

### 2.3 命令行集成测试 (`tests/test_cli_integration.py`)

```python
class TestCLIIntegration(unittest.TestCase):
    def setUp(self):
        import tempfile
        self.temp_dir = tempfile.mkdtemp()
        
        # 创建测试文件
        self.ref_file = os.path.join(self.temp_dir, 'ref.txt')
        self.asr_file = os.path.join(self.temp_dir, 'asr.txt')
        
        with open(self.ref_file, 'w', encoding='utf-8') as f:
            f.write("今天天气真不错，阳光明媚。")
        
        with open(self.asr_file, 'w', encoding='utf-8') as f:
            f.write("今天天气真不错阳光明美")
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_cli_with_different_tokenizers(self):
        """测试命令行使用不同分词器"""
        available_tokenizers = get_available_tokenizers()
        
        for tokenizer_name in available_tokenizers:
            with self.subTest(tokenizer=tokenizer_name):
                # 模拟命令行调用
                result = calculate_accuracy(
                    self.ref_file, 
                    self.asr_file, 
                    show_details=False,
                    filter_fillers=False,
                    tokenizer_name=tokenizer_name
                )
                
                self.assertIsNotNone(result)
                self.assertIn('accuracy', result)
                self.assertTrue(0 <= result['accuracy'] <= 1)
    
    def test_cli_error_handling(self):
        """测试命令行错误处理"""
        # 测试无效分词器
        result = calculate_accuracy(
            self.ref_file,
            self.asr_file,
            tokenizer_name='invalid_tokenizer'
        )
        
        # 应该回退到jieba并成功计算
        self.assertIsNotNone(result)
```

## 3. 端到端测试用例

### 3.1 完整工作流测试 (`tests/test_e2e_workflow.py`)

```python
class TestEndToEndWorkflow(unittest.TestCase):
    def test_complete_gui_workflow(self):
        """测试完整的GUI工作流"""
        # 1. 启动应用
        # 2. 选择文件
        # 3. 选择分词器
        # 4. 计算准确率
        # 5. 导出结果
        pass
    
    def test_performance_with_large_files(self):
        """测试大文件性能"""
        # 创建大文件并测试性能
        pass
    
    def test_batch_processing(self):
        """测试批量处理"""
        # 测试多文件批量处理
        pass
```

## 4. 性能测试用例

### 4.1 分词器性能对比 (`tests/test_performance.py`)

```python
class TestTokenizerPerformance(unittest.TestCase):
    def test_tokenizer_speed_comparison(self):
        """对比不同分词器的速度"""
        import time
        
        test_text = "今天天气真不错，阳光明媚。" * 1000
        results = {}
        
        for tokenizer_name in get_available_tokenizers():
            tokenizer = get_tokenizer(tokenizer_name)
            
            start_time = time.time()
            for _ in range(10):
                tokenizer.cut(test_text)
            end_time = time.time()
            
            results[tokenizer_name] = end_time - start_time
        
        # 输出性能对比结果
        for tokenizer_name, duration in results.items():
            print(f"{tokenizer_name}: {duration:.4f}s")
    
    def test_memory_usage(self):
        """测试内存使用情况"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # 创建多个分词器实例
        tokenizers = []
        for _ in range(10):
            for tokenizer_name in get_available_tokenizers():
                tokenizers.append(get_tokenizer(tokenizer_name))
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # 单例模式应该限制内存增长
        self.assertTrue(memory_increase < 100 * 1024 * 1024)  # 小于100MB
```

## 5. 测试执行策略

### 5.1 测试分组
- **快速测试**: 基础单元测试（<30秒）
- **标准测试**: 包含集成测试（<5分钟）
- **完整测试**: 包含性能和端到端测试（<30分钟）

### 5.2 持续集成配置
```yaml
# .github/workflows/test.yml
name: Test Suite
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10]
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        pip install -r src/requirements.txt
        pip install -r tests/requirements-test.txt
    - name: Run unit tests
      run: python -m pytest tests/test_*_unit.py -v
    - name: Run integration tests
      run: python -m pytest tests/test_*_integration.py -v
```

这个完整的测试计划确保了三种分词工具切换功能的可靠性、性能和用户体验。 