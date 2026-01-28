import pickle
import pandas as pd
import numpy as np

def load_pnl_results(path):
    with open(path, "rb") as f:
        pnl_results = pickle.load(f)
    return pnl_results

def flatten_pnl_results(pnl_results):
    rows = []
    for strategy, trade_pcts in pnl_results.items():
        for i, pct in enumerate(trade_pcts):
            rows.append({
                "strategy": strategy,
                "trade_idx": i,
                "trade_pct": pct
            })
    return pd.DataFrame(rows)
def compute_win_loss_stats(trade_pct, eps=1e-12):
    trade_pct = np.asarray(trade_pct, dtype=float)
    wins = np.sum(trade_pct > eps)
    losses = np.sum(trade_pct < -eps)
    breakevens = np.sum(np.abs(trade_pct) <= eps)
    n_trades = len(trade_pct)
    denom = wins + losses
    win_rate = wins / denom if denom > 0 else np.nan
    win_loss_ratio = wins / losses if losses > 0 else np.inf
    return {
        "n_trades": n_trades,
        "wins": wins,
        "losses": losses,
        "breakevens": breakevens,
        "win_rate": win_rate,
        "win_loss_ratio": win_loss_ratio
    }

def compute_pnl_stats(trade_pct, win_loss_stats, eps=1e-12):
    trade_pct = np.asarray(trade_pct, dtype=float)

    total_pnl_pct = np.sum(trade_pct)
    avg_trade_pct = np.mean(trade_pct) if len(trade_pct) > 0 else np.nan

    wins_mask = trade_pct > eps
    losses_mask = trade_pct < -eps

    avg_win_pct = np.mean(trade_pct[wins_mask]) if np.any(wins_mask) else np.nan
    avg_loss_pct = np.mean(trade_pct[losses_mask]) if np.any(losses_mask) else np.nan

    payoff_ratio = (
        avg_win_pct / abs(avg_loss_pct)
        if avg_win_pct is not np.nan and avg_loss_pct is not np.nan and avg_loss_pct != 0
        else np.nan
    )

    win_rate = win_loss_stats["win_rate"]
    expectancy_pct = (
        win_rate * avg_win_pct + (1 - win_rate) * avg_loss_pct
        if not np.isnan(win_rate)
        else np.nan
    )

    return {
        "total_pnl_pct": total_pnl_pct,
        "avg_trade_pct": avg_trade_pct,
        "avg_win_pct": avg_win_pct,
        "avg_loss_pct": avg_loss_pct,
        "payoff_ratio": payoff_ratio,
        "expectancy_pct": expectancy_pct
    }

def compute_strategy_summary(trade_pct, strategy_name):
    wl_stats = compute_win_loss_stats(trade_pct)
    pnl_stats = compute_pnl_stats(trade_pct, wl_stats)

    summary = {
        "strategy": strategy_name,
        **wl_stats,
        **pnl_stats
    }
    return summary


def summarize_all_strategies(pnl_results):
    summaries = []
    for strategy_name, trade_pcts in pnl_results.items():
        summary = compute_strategy_summary(trade_pcts, strategy_name)
        summaries.append(summary)
    df = pd.DataFrame(summaries)
    df = df.sort_values("total_pnl_pct", ascending=False).reset_index(drop=True)
    return df


def print_leaderboard(df, top_n=10):
    cols = [
        "strategy",
        "n_trades",
        "win_rate",
        "avg_win_pct",
        "avg_loss_pct",
        "payoff_ratio",
        "expectancy_pct",
        "total_pnl_pct",
    ]
    print(df[cols].head(top_n))

if __name__ == "__main__":
    pnl_results = load_pnl_results("pnl_results.pkl")
    df_summary = summarize_all_strategies(pnl_results)
    print_leaderboard(df_summary)
    df_summary.to_csv("strategy_summary.csv", index=False)
