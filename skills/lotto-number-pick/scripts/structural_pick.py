#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""大乐透(超级大乐透) 数学复算 + 可复现的"结构性"选号。

免责声明: 开奖是独立随机事件。本脚本仅用于数学/概率科普与教学, 不构成投注建议,
也不能改变任何一注的期望中奖概率。

用法:
    python structural_pick.py facts
    python structural_pick.py pick --n 3
"""
import argparse
import math
from itertools import combinations

FRONT_POOL = range(1, 36)   # 前区 1..35, 选 5
BACK_POOL = range(1, 13)    # 后区 1..12, 选 2
FRONT_K, BACK_K = 5, 2
TICKET_PRICE = 2.0          # 基本投注 2 元/注
RETURN_RATE = 0.51          # 视频口径: 返奖率 51%


def front_total():
    return math.comb(35, 5)          # 324632


def back_total():
    return math.comb(12, 2)          # 66


def grand_total():
    return front_total() * back_total()   # 21425712


def jackpot_prob():
    return 1.0 / grand_total()


def jackpot_bits():
    return math.log2(grand_total())


def expectation():
    return TICKET_PRICE * RETURN_RATE - TICKET_PRICE   # -0.98


def cold_hot_mean(periods=2950):
    return periods * FRONT_K / 35.0    # 421.43


def sum_mean():
    return FRONT_K * (1 + 35) / 2.0    # 90


def sum_range():
    return (sum(range(1, FRONT_K + 1)),
            sum(range(35 - FRONT_K + 1, 36)))


def odd_even_distribution():
    """精确奇偶比分布: 前区 18 奇 17 偶。返回 [(奇,偶,组合数,概率)]。"""
    odd_pool = 18
    even_pool = 17
    total = front_total()
    out = []
    for k in range(FRONT_K + 1):
        cnt = math.comb(odd_pool, k) * math.comb(even_pool, FRONT_K - k)
        out.append((k, FRONT_K - k, cnt, cnt / total))
    return out


def structural_front(target_sum=90, n=1):
    """确定性: 枚举 3:2 / 2:3 的前区组合, 按 |和值-target| 升序、字典序取前 n 个。"""
    picked = []
    for combo in combinations(FRONT_POOL, FRONT_K):
        odd = sum(1 for x in combo if x % 2 == 1)
        if (odd, FRONT_K - odd) not in ((3, 2), (2, 3)):
            continue
        picked.append((abs(sum(combo) - target_sum), combo))
        if len(picked) > 200000:  # 安全上限
            break
    picked.sort(key=lambda t: (t[0], t[1]))
    # 平手时(同一距离)按字典序, 天然确定; 取前 n 个互不相同的组合
    seen, result = set(), []
    for _, combo in picked:
        if combo in seen:
            continue
        seen.add(combo)
        result.append(combo)
        if len(result) >= n:
            break
    return result


def pick_back(n=1):
    """后区无结构可优化, 按字典序确定性取 n 组。"""
    return list(combinations(BACK_POOL, BACK_K))[:n]


def fmt(combo):
    return " ".join(f"{x:02d}" for x in combo)


def cmd_facts(_args):
    print("=== 大乐透核心数学 ===")
    print(f"C(35,5)            = {front_total():,}")
    print(f"C(12,2)            = {back_total():,}")
    print(f"N = 全部组合        = {grand_total():,}  (~{grand_total()/10000:.0f} 万)")
    print(f"P1 = 头奖概率       = {jackpot_prob():.4e}  (~1/{grand_total()/10000:.0f} 万)")
    print(f"H  = 信息量         = {jackpot_bits():.2f} bit")
    print(f"E  = 每注期望       = {expectation():+.2f} 元/注 (返奖率 {RETURN_RATE:.0%})")
    print(f"冷热均值(2950期)    = {cold_hot_mean():.2f} 次/号")
    lo, hi = sum_range()
    print(f"和值 均值/min/max   = {sum_mean():.0f} / {lo} / {hi}")
    print("奇偶比(精确):")
    for odd, even, cnt, p in odd_even_distribution():
        print(f"  {odd}:{even}  {cnt:>8,}  {p*100:6.2f}%")


def cmd_pick(args):
    print("=== 可复现的结构性选号(仅供教学; 不改变中奖概率) ===")
    for i, front in enumerate(structural_front(n=args.n), 1):
        back = pick_back(args.n)[i - 1]
        print(f"第{i}注: 前区 {fmt(front)}  后区 {fmt(back)}   "
              f"(和值={sum(front)}, 奇偶={sum(1 for x in front if x%2)}:{sum(1 for x in front if x%2==0)})")
    print(f"任意一注中头奖概率均为 1/{grand_total():,} = {jackpot_prob():.4e}; 期望 {expectation():+.2f} 元/注。")


def main():
    ap = argparse.ArgumentParser(description="大乐透数学复算与结构性选号(教学用)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("facts", help="打印全部核心数学量")
    p = sub.add_parser("pick", help="确定性生成结构性号码")
    p.add_argument("--n", type=int, default=3, help="注数(默认 3)")
    args = ap.parse_args()
    {"facts": cmd_facts, "pick": cmd_pick}[args.cmd](args)


if __name__ == "__main__":
    main()