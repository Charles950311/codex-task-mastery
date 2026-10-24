#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""彩票选号方法 · 参数化数学复算 + 可复现的“结构性”选号（科普 / 教学用）。

覆盖两彩种：
  - ssq 双色球：红球 33 选 6 + 蓝球 16 选 1，全部组合 17,721,088
  - dlt 超级大乐透：前区 35 选 5 + 后区 12 选 2，全部组合 21,425,712

免责声明：开奖是独立随机事件。本脚本仅用于数学 / 概率科普与教学，不构成投注建议，
也不能改变任何一注的期望中奖概率。

用法：
    python lottery_math.py list
    python lottery_math.py facts --game ssq
    python lottery_math.py facts --game dlt
    python lottery_math.py pick  --game ssq --n 3
"""
import argparse
import math
from itertools import combinations

# 参数化玩法定义：pools = [(区名, 号码区间, 选几个), ...]，第一区为主区（做结构约束用）
GAMES = {
    "ssq": {
        "name": "双色球",
        "pools": [("红球", range(1, 34), 6), ("蓝球", range(1, 17), 1)],
        "odd_count": 17,        # 1..33 中奇数 17 个、偶数 16 个
        "even_count": 16,
        "price": 2.0,           # 基本投注 2 元/注
        "return_rate": 0.51,    # 视频口径：返奖率 51%
        "periods": 3505,        # 视频所用历史期数
    },
    "dlt": {
        "name": "超级大乐透",
        "pools": [("前区", range(1, 36), 5), ("后区", range(1, 13), 2)],
        "odd_count": 18,        # 1..35 中奇数 18 个、偶数 17 个
        "even_count": 17,
        "price": 2.0,
        "return_rate": 0.51,
        "periods": 2950,        # 大乐透视频口径
    },
}


def zone_total(pool_range, k):
    return math.comb(len(pool_range), k)


def all_total(game):
    total = 1
    for _, rng, k in GAMES[game]["pools"]:
        total *= zone_total(rng, k)
    return total


def jackpot_prob(game):
    return 1.0 / all_total(game)


def jackpot_bits(game):
    return math.log2(all_total(game))


def expectation(game):
    g = GAMES[game]
    return g["price"] * g["return_rate"] - g["price"]


def cold_hot_mean(game):
    g = GAMES[game]
    _, rng, k = g["pools"][0]
    return g["periods"] * k / len(rng)


def sum_stats(game):
    """主区 k 个号之和的均值与标准差（无放回抽样）。"""
    g = GAMES[game]
    _, rng, k = g["pools"][0]
    n = len(rng)
    mean = k * (1 + n) / 2.0
    vpop = (n * n - 1) / 12.0                 # 1..n 的总体方差
    var = k * (n - k) / (n - 1) * vpop        # 无放回求和方差
    return mean, math.sqrt(var), (sum(range(1, k + 1)), sum(range(n - k + 1, n + 1)))


def odd_even_distribution(game):
    """主区精确奇偶比分布：返回 [(奇, 偶, 组合数, 概率)]。"""
    g = GAMES[game]
    _, rng, k = g["pools"][0]
    total = zone_total(rng, k)
    out = []
    for o in range(k + 1):
        cnt = math.comb(g["odd_count"], o) * math.comb(g["even_count"], k - o)
        out.append((o, k - o, cnt, cnt / total))
    return out


def chi2_crit(df, z=1.6449):
    """卡方临界值 chi2(df, 0.95) 的 Wilson-Hilferty 近似（可复现，无需 scipy）。"""
    return df * (1 - 2 / (9 * df) + z * math.sqrt(2 / (9 * df))) ** 3


def structural_pick(game, n=1):
    """确定性结构选号：主区限“均衡奇偶比”，按 |和值-均值| 升序、再字典序取前 n 组。"""
    g = GAMES[game]
    _, rng, k = g["pools"][0]
    pool = list(rng)
    target = k * (1 + len(pool)) / 2.0
    half = k / 2.0
    allowed_odd = {o for o in range(k + 1) if abs(o - half) <= 1}
    ranked = []
    for combo in combinations(pool, k):
        odd = sum(1 for x in combo if x % 2 == 1)
        if odd not in allowed_odd:
            continue
        ranked.append((abs(sum(combo) - target), combo))
    ranked.sort(key=lambda t: (t[0], t[1]))
    seen, result = set(), []
    for _, combo in ranked:
        if combo in seen:
            continue
        seen.add(combo)
        result.append(combo)
        if len(result) >= n:
            break
    rest = []
    for _, r2, k2 in g["pools"][1:]:
        rest.append(list(combinations(list(r2), k2)))
    return result, rest


def fmt(combo):
    return " ".join(f"{x:02d}" for x in combo)


def cmd_list(_args):
    for key, g in GAMES.items():
        zones = " + ".join(f"{nm}{len(rng)}选{k}" for nm, rng, k in g["pools"])
        print(f"{key:4} {g['name']}：{zones}，全部组合 {all_total(key):,}")


def cmd_facts(args):
    game = args.game
    g = GAMES[game]
    print(f"=== {g['name']}（{game}）核心数学 ===")
    parts = []
    for nm, rng, k in g["pools"]:
        c = zone_total(rng, k)
        parts.append(f"C({len(rng)},{k})={c:,}")
        print(f"{nm}: C({len(rng)},{k}) = {c:,}")
    total = all_total(game)
    print(f"全部组合 N = {' x '.join(parts)} = {total:,}  (~{total/10000:.0f} 万)")
    print(f"头奖概率 P1 = 1/N = {jackpot_prob(game):.6e}")
    print(f"信息量 H = log2(N) = {jackpot_bits(game):.4f} bit")
    print(f"每注期望 E = {g['price']:.0f}x{g['return_rate']:.0%} - {g['price']:.0f} = {expectation(game):+.2f} 元/注")
    print(f"冷热均值（{g['periods']} 期） = {cold_hot_mean(game):.2f} 次/号（理论均匀）")
    mean, sd, (lo, hi) = sum_stats(game)
    print(f"主区和值 均值/标准差 = {mean:.2f} / {sd:.2f}（最小 {lo}，最大 {hi}）")
    df = len(list(g["pools"][0][1])) - 1
    print(f"主区均匀性卡方临界 chi2({df}, 0.95) ~= {chi2_crit(df):.3f}")
    print("主区奇偶比（精确）：")
    for o, e, cnt, pr in odd_even_distribution(game):
        print(f"  {o}:{e}  {cnt:>9,}  {pr*100:6.2f}%")


def cmd_pick(args):
    game = args.game
    g = GAMES[game]
    print(f"=== {g['name']} 可复现的结构性选号（仅供教学；不改变中奖概率） ===")
    mains, rests = structural_pick(game, args.n)
    for i, main in enumerate(mains):
        line = f"第{i+1}注: {g['pools'][0][0]} {fmt(main)}"
        for j, pool in enumerate(rests):
            line += f"   {g['pools'][j+1][0]} {fmt(pool[i % len(pool)])}"
        odd = sum(1 for x in main if x % 2)
        line += f"   (和值={sum(main)}, 奇偶={odd}:{len(main)-odd})"
        print(line)
    print(f"任意一注中头奖概率均为 1/{all_total(game):,}；期望 {expectation(game):+.2f} 元/注。")
    print("结构（和值/奇偶）只改变组合落在哪个分布区间，不改变单注概率与期望。")


def main():
    ap = argparse.ArgumentParser(description="彩票选号数学复算与结构性选号（教学用）")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list", help="列出支持的彩种与组合数")
    pf = sub.add_parser("facts", help="打印核心数学量")
    pf.add_argument("--game", choices=list(GAMES), default="ssq")
    pp = sub.add_parser("pick", help="确定性生成结构性号码")
    pp.add_argument("--game", choices=list(GAMES), default="ssq")
    pp.add_argument("--n", type=int, default=3, help="注数（默认 3）")
    args = ap.parse_args()
    {"list": cmd_list, "facts": cmd_facts, "pick": cmd_pick}[args.cmd](args)


if __name__ == "__main__":
    main()