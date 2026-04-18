#!/usr/bin/env python3
"""
REM Dream Evolution Scanner
扫描当日记忆文件，提取进化机会，生成进化提案。
"""

import os
import re
import json
from datetime import datetime, timedelta
from pathlib import Path

# 配置
WORKSPACE = os.environ.get("HICEF_WORKSPACE", ".")
MEMORY_DIR = os.path.join(WORKSPACE, "memory")
PROPOSALS_DIR = os.path.join(WORKSPACE, "evolution-proposals")
MAX_PROPOSALS_PER_DAY = 3

def load_memory(date_str=None):
    """加载当日记忆文件"""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    path = os.path.join(MEMORY_DIR, f"{date_str}.md")
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    return None

def extract_repeated_errors(content):
    """提取重复出现的错误"""
    error_patterns = []
    # 匹配错误/失败关键词
    keywords = ['失败', 'error', '超时', 'timeout', '崩溃', 'crash']
    for keyword in keywords:
        matches = re.findall(f'.*{keyword}.*', content, re.IGNORECASE)
        if len(matches) >= 2:  # 至少出现 2 次才算重复
            error_patterns.append({
                'type': f'重复错误: {keyword}',
                'count': len(matches),
                'examples': matches[:2]
            })
    return error_patterns

def extract_success_patterns(content):
    """提取成功的模式"""
    patterns = []
    # 匹配成功/完成/优化关键词
    keywords = ['成功', '完成', '优化', '提升', '改善', 'success']
    for keyword in keywords:
        matches = re.findall(f'.*{keyword}.*', content, re.IGNORECASE)
        if matches:
            patterns.append({
                'type': f'成功模式: {keyword}',
                'examples': matches[:1]
            })
    return patterns

def extract_pain_points(content):
    """提取流程痛点"""
    pains = []
    keywords = ['手动', '重复', '繁琐', '耗时', 'pain', 'manual']
    for keyword in keywords:
        matches = re.findall(f'.*{keyword}.*', content, re.IGNORECASE)
        if matches:
            pains.append({
                'type': f'流程痛点: {keyword}',
                'examples': matches[:1]
            })
    return pains

def get_next_proposal_id():
    """获取下一个提案序号"""
    today = datetime.now().strftime("%Y-%m-%d")
    existing = []
    if os.path.exists(PROPOSALS_DIR):
        for f in os.listdir(PROPOSALS_DIR):
            if f.startswith(f'evo-{today}'):
                match = re.search(r'evo-\d{4}-\d{2}-\d{2}-(\d+)', f)
                if match:
                    existing.append(int(match.group(1)))
    next_num = max(existing, default=0) + 1
    return f'evo-{today}-{next_num:03d}'

def create_proposal(title, category, description, priority="P1"):
    """创建进化提案"""
    proposal_id = get_next_proposal_id()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    proposal = f"""---
id: {proposal_id}
created_at: {now}
category: {category}
priority: {priority}
status: pending
trigger: sleep_rem
author: Agent
---

# 进化提案 {proposal_id}：{title}

## 进化目标
- **类别**：{category}
- **问题描述**：{description}
- **进化方向**：...

## 当前基线
- **当前表现**：...
- **数据支撑**：...

## 预期改进
- **改进后表现**：...
- **可量化指标**：...

## 执行计划
1. ...

## 风险评估
- **风险等级**：低 / 中 / 高
- **回滚方案**：...

## 良知判断
- ✅ 是否为用户创造真实价值？
- ✅ 是否符合核心原则？
- ⚠️ 是否有副作用？

---
## 人类审批

- **审批结果**：pending
- **审批时间**：...
- **备注**：...

---
## 执行记录

- **执行时间**：...
- **执行结果**：...
- **实际改进**：...
"""
    
    filepath = os.path.join(PROPOSALS_DIR, f"{proposal_id}.md")
    os.makedirs(PROPOSALS_DIR, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(proposal)
    
    return proposal_id, filepath

def main():
    """REM 梦境进化扫描主函数"""
    print(f"🐯 REM Dream Evolution Scanner starting at {datetime.now().strftime('%H:%M:%S')}")
    
    today = datetime.now().strftime("%Y-%m-%d")
    content = load_memory(today)
    
    if not content:
        print(f"⚠️ No memory file found for {today}")
        return
    
    proposals = []
    
    # 1. 扫描重复错误
    errors = extract_repeated_errors(content)
    for error in errors:
        pid, path = create_proposal(
            title=error['type'],
            category="skill",
            description=f"发现重复错误 {error['count']} 次",
            priority="P1"
        )
        proposals.append(pid)
    
    # 2. 扫描成功模式
    successes = extract_success_patterns(content)
    for success in successes:
        pid, path = create_proposal(
            title=f"固化 {success['type']}",
            category="process",
            description=f"发现成功模式可固化",
            priority="P2"
        )
        proposals.append(pid)
    
    # 3. 扫描流程痛点
    pains = extract_pain_points(content)
    for pain in pains:
        pid, path = create_proposal(
            title=f"优化 {pain['type']}",
            category="process",
            description=f"发现流程痛点需要优化",
            priority="P1"
        )
        proposals.append(pid)
    
    # 限制每日提案数
    proposals = proposals[:MAX_PROPOSALS_PER_DAY]
    
    print(f"📝 Generated {len(proposals)} evolution proposals:")
    for p in proposals:
        print(f"  - {p}")
    
    print("✅ REM scan complete")

if __name__ == "__main__":
    main()
