sequenceDiagram
    participant User as 用户
    participant GUI as GUI界面(main.py)
    participant Factory as 分词器工厂
    participant Tokenizer as 分词器实例
    participant ASRMetrics as ASRMetrics
    participant Utils as 工具函数

    Note over User,Utils: 1. 应用启动阶段
    User->>GUI: 启动应用
    GUI->>Factory: get_available_tokenizers()
    Factory->>Factory: 检查各分词器依赖
    Factory-->>GUI: 返回可用分词器列表
    GUI->>GUI: 初始化分词器下拉框
    GUI-->>User: 显示界面(默认jieba)

    Note over User,Utils: 2. 用户选择文件阶段  
    User->>GUI: 选择ASR文件和标注文件
    GUI->>GUI: 更新文件列表显示
    User->>GUI: 拖拽调整文件顺序
    GUI->>GUI: 更新文件配对关系

    Note over User,Utils: 3. 分词器选择阶段
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

    Note over User,Utils: 4. 开始统计阶段
    User->>GUI: 点击"开始统计"按钮
    GUI->>GUI: 验证文件配对
    GUI->>Factory: create_tokenizer("thulac")
    Factory->>Tokenizer: 获取或创建分词器实例
    Tokenizer-->>Factory: 返回分词器实例
    Factory-->>GUI: 返回分词器实例
    GUI->>ASRMetrics: new ASRMetrics(tokenizer_name="thulac")
    ASRMetrics->>Factory: get_tokenizer("thulac")
    Factory-->>ASRMetrics: 返回分词器实例
    ASRMetrics-->>GUI: 返回ASRMetrics实例

    Note over User,Utils: 5. 文件处理循环
    loop 每对文件
        GUI->>Utils: read_file_with_multiple_encodings(asr_file)
        Utils-->>GUI: 返回ASR文本
        GUI->>Utils: read_file_with_multiple_encodings(ref_file)
        Utils-->>GUI: 返回参考文本
        
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
        ASRMetrics-->>GUI: 返回详细指标
        
        GUI->>GUI: 更新结果表格
    end

    Note over User,Utils: 6. 结果展示和导出
    GUI-->>User: 显示完整结果
    opt 用户选择导出
        User->>GUI: 点击"导出结果"
        GUI->>GUI: 生成导出数据
        GUI->>Utils: 写入文件(CSV/TXT)
        Utils-->>GUI: 导出完成
        GUI-->>User: 显示成功提示
    end