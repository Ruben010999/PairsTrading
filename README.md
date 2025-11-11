# Market‑Neutral Pairs Trading (Equities/ETFs, US)

**Goal**: Build a professional, interview‑ready pairs trading project that demonstrates:
- Understanding of **cointegration** (not just correlation)
- Clean **IS/OOS** protocol with walk‑forward updates
- Realistic **transaction costs**, **volatility targeting**, and simple **risk overlays**
- Clear, didactic Markdown explaining theory, assumptions, and code

## Key Ideas
- Cointegration between two price series $X_t$ and $Y_t$ means a linear combination \(S_t = Y_t - \beta X_t\) is **stationary**.
- The spread \(S_t\) is modeled as a mean‑reverting process (e.g., OU). Trading signal is based on standardized spread: \(Z_t = (S_t - \mu)/\sigma\).
- We target market‑neutrality (long/short) and control volatility at the portfolio level.

## Notebooks
1. **01_universe_and_data** — universe definition, data ingestion, cleaning, calendar alignment.
2. **02_pair_selection_cointegration** — Engle‑Granger ADF on residuals, FDR correction, half‑life.
3. **03_signal_and_risk_engine** — spread & z‑score signals, position sizing, risk overlays.
4. **04_backtest_IS_OOS** — strict IS/OOS split, walk‑forward re‑estimation, sensitivity tests.
5. **05_report_pairs_trading** — academic‑style report (formulas + figures + limitations).

## Reproducibility
- Use the provided `env.yml`.
- All parameters centralized in `config.py`.
- Code in `src/`; notebooks import from `src/`.

## Data Sources
- Default: Yahoo Finance via `yfinance` (daily bars). You may replace with your SQL source.

## Run Order
1. Fill `config.py`
2. Run notebook 01 → 02 → 03 → 04, then export results into 05.

## Limitations & Next Steps
- This is an educational, **non‑live** research project.
- Extend to a **portfolio of 20–50 pairs**; add sector/beta neutrality; explore borrow fees. 