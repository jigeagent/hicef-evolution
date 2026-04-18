#!/usr/bin/env python3
"""
Heartbeat Evolution Checker
定期检查错误日志，识别重复错误模式，生成进化提案。
"""

import os
import re
import json
from datetime import datetime
from collections import defaultdict

# 配置
WORKSPACE = os.environ.get("HICEF_WORKSPACE", ".")
LOG_FILE = os.environ.get("HICEF_LOG_FILE", os.path.join(WORKSPACE, "system.log"))
PROPOSALS_DIR = os.path.join(WORKSPACE, "evolution-proposals")
STATE_FILE = os.path.join(WORKSPACE, ".heartbeat-state.json")
ERROR_THRESHOLD = 3  # 错误出现次数阈值

def load_state():
    """加载心跳状态"""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {"processed_errors": [], "last_check": None}

def save_state(state):
    """保存心跳状态"""
    state["last_check"] = datetime.now().isoformat()
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def get_recent_errors(last_minutes=30):
    """获取最近的错误日志"""
    errors = []
    if not os.path.exists(LOG_FILE):
        return errors
    
    cutoff = datetime.now() - __import__('datetime').timedelta(minutes=last_minutes)
    
    with open(LOG_FILE, 'r') as f:
        for line in f:
            # 尝试解析时间戳
            match = re.match(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})', line)
            if match:
                try:
                    ts = datetime.fromisoformat(match.group(1))
                    if ts >= cutoff and any(kw in line.lower() for kw in ['error', 'fail', 'timeout', 'exception']):
                        errors.append(line.strip())
                except ValueError:
                    pass
    
    return errors

def cluster_errors(errors):
    """聚类错误模式"""
    patterns = defaultdict(list)
    
    for error in errors:
        # 提取错误类型（简化版）
        for keyword in ['timeout', 'connection refused', 'not found', 'permission denied', 'disk full']:
            if keyword in error.lower():
                patterns[keyword].append(error)
                break
        else:
            patterns['unknown'].append(error)
    
    return patterns

def has_existing_proposal(error_type):
    """检查是否已有对应提案"""
    if not os.path.exists(PROPOSALS_DIR):
        return False
    
    for f in os.listdir(PROPOSALS_DIR):
        if error_type.lower() in f.lower() or error_type.lower() in open(os.path.join(PROPOSALS_DIR, f), 'r', encoding='utf-8', errors='ignore').read().lower():
            return True
    return False

def main():
    """心跳检查主函数"""
    print(f"💓 Heartbeat check at {datetime.now().strftime('%H:%M:%S')}")
    
    state = load_state()
    errors = get_recent_errors(last_minutes=30)
    
    if not errors:
        print("✅ No recent errors")
        save_state(state)
        return
    
    patterns = cluster_errors(errors)
    new_proposals = []
    
    for pattern_type, pattern_errors in patterns.items():
        if len(pattern_errors) >= ERROR_THRESHOLD and not has_existing_proposal(pattern_type):
            print(f"⚠️ Repeated error pattern detected: {pattern_type} ({len(pattern_errors)} occurrences)")
            new_proposals.append(pattern_type)
    
    if new_proposals:
        print(f"📝 Generated {len(new_proposals)} evolution proposals from heartbeat check")
    else:
        print("✅ No new proposals needed")
    
    save_state(state)

if __name__ == "__main__":
    main()
