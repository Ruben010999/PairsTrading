
from __future__ import annotations
import numpy as np, pandas as pd
from dataclasses import dataclass
from statsmodels.tsa.stattools import adfuller

# ---------- Stats ----------
def ols_beta(y: pd.Series, x: pd.Series):
    df = pd.concat([y,x], axis=1, join="inner").dropna()
    Y = df.iloc[:,0].values
    X = df.iloc[:,1].values
    X_ = np.column_stack([np.ones_like(X), X])
    a,b = np.linalg.lstsq(X_, Y, rcond=None)[0]
    return float(a), float(b)

def spread(y: pd.Series, x: pd.Series, beta: float, alpha: float=0.0):
    return (y - (alpha + beta*x)).dropna()

def adf_test(series: pd.Series):
    s = series.dropna().astype(float)
    stat, pval, *_ = adfuller(s, autolag="AIC")
    return float(stat), float(pval)

def engle_granger(y: pd.Series, x: pd.Series):
    a,b = ols_beta(y,x)
    res = spread(y,x,b,a)
    stat,p = adf_test(res)
    return a,b,stat,p,res

def half_life(series: pd.Series):
    s = series.dropna().astype(float)
    if len(s) < 30: return None
    s_lag = s.shift(1).dropna()
    ds = s.diff().dropna()
    idx = s_lag.index.intersection(ds.index)
    s_lag, ds = s_lag.loc[idx], ds.loc[idx]
    X = np.column_stack([np.ones(len(s_lag)), s_lag.values])
    phi = np.linalg.lstsq(X, ds.values, rcond=None)[0][1]
    import math
    try:
        kappa = -np.log1p(phi)
        if kappa <= 0: return None
        return float(np.log(2.0)/kappa)
    except Exception:
        return None

# ---------- Signals & Risk ----------
def rolling_zscore(spread: pd.Series, window: int):
    mu = spread.rolling(window).mean()
    sd = spread.rolling(window).std(ddof=1)
    return (spread - mu) / sd

def ewma_vol(series: pd.Series, span: int):
    r = series.diff()
    ew = r.ewm(span=span, adjust=False).std(bias=False)
    return ew * np.sqrt(252.0)

def target_size(spread_vol: pd.Series, target_ann_vol: float, max_weight: float):
    w = target_ann_vol / spread_vol.replace(0.0, np.nan)
    return w.clip(upper=max_weight).fillna(0.0)

def apply_costs(turnover: pd.Series, commission_bps: float, slippage_bps: float):
    bps = (commission_bps + slippage_bps)/10000.0
    return -bps * turnover.abs()

# ---------- Backtester ----------
@dataclass
class PairParams:
    z_open: float
    z_close: float
    z_stop: float
    max_hold_days: int
    roll_window_z: int
    ewma_span_vol: int
    target_ann_vol: float
    max_pair_weight: float
    commission_bps: float
    slippage_bps: float

def backtest_pair(y: pd.Series, x: pd.Series, alpha: float, beta: float, p: PairParams):
    df = pd.concat({"y":y, "x":x}, axis=1).dropna()
    S  = df["y"] - (alpha + beta*df["x"])
    Z  = rolling_zscore(S, p.roll_window_z)

    pos = pd.Series(0.0, index=S.index)
    entry_date = None
    for t in range(1, len(S)):
        date = S.index[t]
        z_t  = Z.iloc[t]
        prev = pos.iloc[t-1]
        exit_sig = (abs(z_t) <= p.z_close) or (abs(z_t) >= p.z_stop)
        time_stop = False
        if entry_date is not None:
            if (date - entry_date).days >= p.max_hold_days:
                time_stop = True
        if prev != 0 and (exit_sig or time_stop):
            pos.iloc[t] = 0.0
            entry_date = None
            continue
        if prev == 0:
            if z_t >= p.z_open:
                pos.iloc[t] = -1.0
                entry_date = date
            elif z_t <= -p.z_open:
                pos.iloc[t] = +1.0
                entry_date = date
            else:
                pos.iloc[t] = 0.0
        else:
            pos.iloc[t] = prev

    vol = ewma_vol(S, p.ewma_span_vol)
    size = target_size(vol, p.target_ann_vol, p.max_pair_weight)
    dS = S.diff().fillna(0.0)

    gross = (pos.shift(1).fillna(0.0) * size.shift(1).fillna(0.0)) * dS
    turnover = pos.diff().abs().fillna(0.0) * size.shift(1).fillna(0.0)
    costs = apply_costs(turnover, p.commission_bps, p.slippage_bps)
    pnl = gross + costs
    equity = (1.0 + pnl).cumprod()

    return pd.DataFrame({"spread":S, "z":Z, "pos":pos, "size":size,
                         "pnl":pnl, "equity":equity, "turnover":turnover, "costs":costs})

def perf_stats(pnl: pd.Series):
    r = pnl.dropna()
    ann_ret = r.mean()*252.0
    ann_vol = r.std(ddof=1)*np.sqrt(252.0)
    sharpe  = ann_ret/ann_vol if ann_vol>0 else np.nan
    eq = (1.0+r).cumprod()
    peak = eq.cummax()
    dd = (eq/peak - 1.0).min()
    return {"ann_return":float(ann_ret),"ann_vol":float(ann_vol),"sharpe":float(sharpe),"max_drawdown":float(dd)}
