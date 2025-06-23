#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试运行脚本
提供便捷的测试运行命令和测试环境检查
"""

import sys
import subprocess
import importlib
from pathlib import Path

def check_dependencies():
    """检查测试依赖"""
    print("检查测试依赖...")
    
    # 必需依赖
    required_deps = ['jieba', 'jiwer', 'pandas', 'pytest']
    missing_required = []
    
    for dep in required_deps:
        try:
            importlib.import_module(dep)
            print(f"✓ {dep} - 已安装")
        except ImportError:
            print(f"✗ {dep} - 未安装")
            missing_required.append(dep)
    
    # 可选依赖
    optional_deps = ['thulac', 'hanlp']
    available_optional = []
    
    for dep in optional_deps:
        try:
            importlib.import_module(dep)
            print(f"✓ {dep} - 已安装（可选）")
            available_optional.append(dep)
        except ImportError:
            print(f"⚠ {dep} - 未安装（可选）")
    
    if missing_required:
        print(f"\n错误：缺少必需依赖: {', '.join(missing_required)}")
        print("请运行: pip install " + " ".join(missing_required))
        return False
    
    print(f"\n可用分词器: jieba" + (f", {', '.join(available_optional)}" if available_optional else ""))
    return True

def run_tests(test_type="all", verbose=True):
    """运行测试"""
    if not check_dependencies():
        return False
    
    cmd = ["python", "-m", "pytest"]
    
    if verbose:
        cmd.append("-v")
    
    # 根据测试类型选择测试
    if test_type == "unit":
        cmd.extend(["-m", "unit"])
    elif test_type == "integration":
        cmd.extend(["-m", "integration"])
    elif test_type == "performance":
        cmd.extend(["-m", "performance", "--timeout=60"])
    elif test_type == "stability":
        cmd.extend(["-m", "stability"])
    elif test_type == "jieba":
        cmd.extend(["-m", "jieba"])
    elif test_type == "thulac":
        cmd.extend(["-m", "thulac"])
    elif test_type == "hanlp":
        cmd.extend(["-m", "hanlp"])
    elif test_type == "all":
        cmd.append("tests/")
    else:
        print(f"未知测试类型: {test_type}")
        return False
    
    print(f"\n运行命令: {' '.join(cmd)}")
    print("=" * 50)
    
    try:
        result = subprocess.run(cmd, check=True)
        print("\n测试完成！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n测试失败，退出代码: {e.returncode}")
        return False

def run_coverage():
    """运行覆盖率测试"""
    print("运行覆盖率测试...")
    
    cmd = [
        "python", "-m", "pytest", 
        "tests/", 
        "--cov=src", 
        "--cov-report=html",
        "--cov-report=term"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("\n覆盖率报告已生成到 htmlcov/ 目录")
        return True
    except subprocess.CalledProcessError:
        print("覆盖率测试失败")
        return False

def show_help():
    """显示帮助信息"""
    help_text = """
测试运行脚本使用方法:

python run_tests.py [测试类型]

测试类型:
  all          - 运行所有测试（默认）
  unit         - 只运行单元测试
  integration  - 只运行集成测试
  performance  - 只运行性能测试
  stability    - 只运行稳定性测试
  jieba        - 只运行Jieba相关测试
  thulac       - 只运行THULAC相关测试
  hanlp        - 只运行HanLP相关测试
  coverage     - 运行覆盖率测试
  check        - 只检查依赖环境
  help         - 显示此帮助信息

示例:
  python run_tests.py unit
  python run_tests.py coverage
  python run_tests.py check
"""
    print(help_text)

def main():
    """主函数"""
    if len(sys.argv) < 2:
        test_type = "all"
    else:
        test_type = sys.argv[1].lower()
    
    if test_type in ["help", "-h", "--help"]:
        show_help()
        return
    
    if test_type == "check":
        check_dependencies()
        return
    
    if test_type == "coverage":
        run_coverage()
        return
    
    # 确保在正确的目录中运行
    script_dir = Path(__file__).parent
    if script_dir.name != "tests":
        print("请在tests目录中运行此脚本")
        return
    
    success = run_tests(test_type)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()