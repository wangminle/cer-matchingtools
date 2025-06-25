```mermaid
sequenceDiagram
    participant User as 用户
    participant GUI as GUI界面(main.py)
    participant Factory as 分词器工厂
    participant Tokenizer as 分词器实例
    participant ASRMetrics as ASRMetrics

    Note over User,ASRMetrics: 1. 应用启动阶段
    User->>GUI: 启动应用
    GUI->>Factory: get_available_tokenizers()
    Factory->>Factory: 检查各分词器依赖
    Factory-->>GUI: 返回可用分词器列表
    GUI->>GUI: 初始化分词器下拉框
    GUI-->>User: 显示界面(默认jieba)

    Note over User,ASRMetrics: 2. 用户选择文件阶段  
    User->>GUI: 选择ASR文件和标注文件
    GUI->>GUI: 更新文件列表显示
    User->>GUI: 拖拽调整文件顺序
    GUI->>GUI: 更新文件配对关系

    Note over User,ASRMetrics: 3. 分词器选择阶段
    User->>GUI: 选择分词器(如THULAC)
    GUI->>Factory: get_tokenizer_info("thulac")
    Factory->>Tokenizer: 尝试创建ThulacTokenizer
    Tokenizer->>Tokenizer: initialize()
    alt 初始化成功
        Tokenizer-->>Factory: 返回分词器实例
        Factory-->>GUI: 返回分词器信息
        GUI->>GUI: 更新状态显示(绿色✓)
    else 初始化失败
        Tokenizer-->>Factory: 抛出TokenizerInitError
        Factory-->>GUI: 返回错误信息
        GUI->>GUI: 显示错误状态(红色✗)
        GUI->>User: 提示用户安装依赖
    end

    Note over User,ASRMetrics: 4. 开始统计阶段
    User->>GUI: 点击"开始统计"按钮
    GUI->>GUI: 验证文件配对
    GUI->>GUI: 获取选择的分词器名称
    
    alt 分词器未缓存
        GUI->>ASRMetrics: new ASRMetrics(tokenizer_name)
        ASRMetrics->>Factory: get_tokenizer(tokenizer_name)
        Factory-->>ASRMetrics: 返回分词器实例
        ASRMetrics->>ASRMetrics: _initialize_tokenizer()
        GUI->>GUI: 缓存ASRMetrics实例
    else 分词器已缓存
        GUI->>GUI: 使用缓存的ASRMetrics实例
    end

    Note over User,ASRMetrics: 5. 文件处理循环
    loop 每对文件
        GUI->>GUI: read_file_with_multiple_encodings(asr_file)
        Note right of GUI: 内部方法：尝试多种编码读取
        GUI->>GUI: read_file_with_multiple_encodings(ref_file)
        
        GUI->>ASRMetrics: calculate_detailed_metrics(ref_text, asr_text, filter_fillers)
        ASRMetrics->>Tokenizer: preprocess_chinese_text(text)
        Tokenizer->>Tokenizer: cut(text)
        Tokenizer-->>ASRMetrics: 返回分词结果
        
        alt 启用语气词过滤
            ASRMetrics->>Tokenizer: posseg(text)
            Tokenizer-->>ASRMetrics: 返回词性标注
            ASRMetrics->>ASRMetrics: filter_filler_words(text)
        end
        
        ASRMetrics->>ASRMetrics: calculate_cer(ref_processed, asr_processed)
        ASRMetrics-->>GUI: 返回详细指标(包含tokenizer信息)
        
        GUI->>GUI: 更新结果表格(包含分词器列)
    end

    Note over User,ASRMetrics: 6. 结果展示和导出
    GUI-->>User: 显示完整结果
    opt 用户选择导出
        User->>GUI: 点击"导出结果"
        GUI->>GUI: 生成导出数据(包含分词器信息)
        GUI->>GUI: 写入文件(CSV/TXT)
        Note right of GUI: 导出内容包含：ASR文件、标注文件、<br/>字数统计、准确率、语气词过滤状态、分词器类型
        GUI-->>User: 显示成功提示
    end