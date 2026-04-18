#!/usr/bin/env python3
"""
Evolution Proposal Generator
从结构化数据生成进化提案 Markdown 文件。
"""

import os
import json
from datetime import datetime

def generate_proposal(data, output_dir="evolution-proposals"):
    """
    生成进化提案文件
    
    Args:
        data: dict containing proposal fields
            - category: skill/memory/process/code/personality
            - priority: P0/P1/P2
            - title: str
            - description: str
            - baseline: dict with 'current' and 'data'
            - expected: dict with 'after' and 'metrics'
            - plan: list of steps
            - risk: dict with 'level', 'rollback', 'notes'
            - author: str
            - trigger: heartbeat/sleep/manual/emergence
        output_dir: str, directory to save the proposal
    """
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    
    # 获取提案序号
    existing = []
    if os.path.exists(output_dir):
        for f in os.listdir(output_dir):
            if f.startswith(f'evo-{date_str}'):
                import re
                match = re.search(r'evo-\d{4}-\d{2}-\d{2}-(\d+)', f)
                if match:
                    existing.append(int(match.group(1)))
    num = max(existing, default=0) + 1
    proposal_id = f'evo-{date_str}-{num:03d}'
    
    # 渲染 Markdown
    steps = "\n".join([f"{i+1}. {step}" for i, step in enumerate(data.get('plan', []))])
    metrics = "\n".join([f"  - {m}" for m in data.get('expected', {}).get('metrics', [])])
    
    proposal = f"""---
id: {proposal_id}
created_at: {now.strftime("%Y-%m-%d %H:%M")}
category: {data.get('category', 'process')}
priority: {data.get('priority', 'P1')}
status: pending
trigger: {data.get('trigger', 'manual')}
author: {data.get('author', 'Agent')}
---

# 进化提案 {proposal_id}：{data.get('title', '未命名')}

## 进化目标
- **类别**：{data.get('category', 'process')}
- **问题描述**：{data.get('description', '')}
- **进化方向**：{data.get('expected', {}).get('after', '')}

## 当前基线
- **当前表现**：{data.get('baseline', {}).get('current', '')}
- **数据支撑**：{data.get('baseline', {}).get('data', '')}

## 预期改进
- **改进后表现**：{data.get('expected', {}).get('after', '')}
- **可量化指标**：
{metrics}

## 执行计划
{steps}

## 风险评估
- **风险等级**：{data.get('risk', {}).get('level', '中')}
- **回滚方案**：{data.get('risk', {}).get('rollback', '...')}
- **注意事项**：{data.get('risk', {}).get('notes', '...')}

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
    
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f"{proposal_id}.md")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(proposal)
    
    return proposal_id, filepath

# CLI usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python proposal_generator.py <json_file>")
        print("Example JSON:")
        print(json.dumps({
            "category": "skill",
            "priority": "P1",
            "title": "修复搜索超时",
            "description": "搜索 API 频繁超时",
            "baseline": {"current": "超时率 30%", "data": "最近 24 小时 15 次超时"},
            "expected": {"after": "超时率 < 5%", "metrics": ["超时率从 30% 降到 5%", "成功率从 70% 提升到 95%"]},
            "plan": ["增加重试机制", "添加备用 API", "优化超时配置"],
            "risk": {"level": "低", "rollback": "恢复原配置", "notes": "备用 API 可能有限流"},
            "author": "虎哥",
            "trigger": "heartbeat"
        }, indent=2, ensure_ascii=False))
        sys.exit(1)
    
    json_file = sys.argv[1]
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    pid, path = generate_proposal(data)
    print(f"✅ Proposal created: {pid} → {path}")
