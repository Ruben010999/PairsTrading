# Market-Neutral Pairs Trading (Cointegration-Based)

---

<p align="center">
  <img src="images/IS%20Equity%20curve.png" alt="IS Equity curve" width="700">
</p>

<p align="center">
  <img src="images/Pairs-Trading%20Suitability%20Heatmap.png" alt="Pairs-Trading Suitability Heatmap" width="700">
</p>

<p align="center">
  <img src="images/Per-Pair%20Sharpe%20Compariso%20(IS%20vs%20OOS).png" alt="Per-Pair Sharpe Compariso (IS vs OOS)" width="700">
</p>


This repository presents a complete quantitative research project implementing a cointegration-based pairs trading strategy on U.S. equities and ETFs. The project is developed in Python with NumPy, Pandas, Matplotlib, and Statsmodels — without machine learning or external trading frameworks. The goal is educational and analytical: to demonstrate the logic, mathematics, and empirical fragility of a classic statistical-arbitrage strategy.

---

## 1. Overview

The project follows a standard research workflow used in quantitative finance:
1. data preparation and cleaning; 2. cointegration and pair selection; 3. signal generation and risk control; 4. backtesting and performance analysis; 5. reporting and interpretation of results.

The strategy seeks mean reversion in a spread between two assets that exhibit a long-run equilibrium.

---

## 2. Theoretical Foundation

Pairs trading assumes a long-run equilibrium (cointegration) between two price series $X_t$ and $Y_t$.  
We define the spread:

$$
S_t = Y_t - \alpha - \beta X_t
$$

and test whether $S_t$ is stationary.

---

**Engle–Granger two-step procedure**

1. Estimate $(\alpha,\beta)$ via OLS:

$$
Y_t = \alpha + \beta X_t + \varepsilon_t
$$

2. Test residuals $\varepsilon_t$ for stationarity using the Augmented Dickey–Fuller (ADF) test.  
   If $p_{\text{value}} < 0.05$, the pair is treated as cointegrated.

---

**Trading logic (z-score signals)**

With rolling mean $\mu_t$ and standard deviation $\sigma_t$, define:

$$
Z_t = \frac{S_t - \mu_t}{\sigma_t}
$$

Rules:

- **Enter** when $\lvert Z_t \rvert \ge z_{\text{open}}$ (direction by sign of $Z_t$)  
- **Exit** when $\lvert Z_t \rvert \le z_{\text{close}}$  
- **Emergency stop** when $\lvert Z_t \rvert \ge z_{\text{stop}}$  
- **Optional time stop** after $D_{\max}$ days

---

**Risk control**  
Position sizing targets a constant annualized volatility of the spread using an EWMA estimator and a cap on per-pair weight.

---

## 3. Implementation Details

- **Data source:** Yahoo Finance (daily).  
- **Pair selection:** Engle–Granger (ADF on residuals); ranking by p-value and, where computed, mean-reversion half-life.  
- **Signals:** rolling z-scores of spread; threshold-based entries/exits.  
- **Risk:** EWMA volatility targeting; per-pair weight cap; time stop; emergency stop.  
- **Backtest:** vectorized daily simulation; explicit transaction costs (commissions + slippage).  
- **Validation:** strict IS/OOS split; summary metrics (annualized return/volatility, Sharpe, max drawdown); parameter sensitivity across $(z_{\text{open}}, z_{\text{close}}, \text{window})$.

---

## 4. Key Results (indicative)

| Metric | In-Sample | Out-of-Sample |
|:--|:--:|:--:|
| Annualized Return | 3–5% | 0–1% |
| Annualized Volatility | 8–10% | 9–11% |
| Sharpe | 0.4–0.6 | $\approx 0.0$ |
| Max Drawdown | −8% | −10% |

Interpretation: mild IS profitability deteriorates to near-zero or negative OOS performance. After transaction costs, no robust alpha remains.

---

## 5. Representative Visualizations

- Portfolio equity curves, IS vs OOS (cumulative PnL).  
- Portfolio drawdowns, IS vs OOS.  
- Per-pair IS vs OOS Sharpe scatter with pair labels.  
- Sensitivity maps: Sharpe across $(z_{\text{open}}, z_{\text{close}}, \text{window})$.

Images should be exported from notebooks and referenced in the README, for example:

---

## 6. Why Out-of-Sample Performance Fails

1. **Instability of cointegration.** Economic regimes, sector rotation, corporate events, and macro shocks break the historical equilibrium; $S_t$ ceases to be stationary in OOS windows.  
2. **Non-stationarity and regime shifts.** The 2020–2025 period involves structural breaks; estimated $(\alpha,\beta)$ and $Z_t$ thresholds are not stable.  
3. **Parameter sensitivity.** Sensitivity surfaces in $(z_{\text{open}}, z_{\text{close}}, \text{window})$ show no persistent maxima; small changes cause large PnL differences, indicating weak signal-to-noise.  
4. **Transaction costs.** Thin mean-reversion edges are fully consumed by realistic spreads, commissions, and slippage.  
5. **Daily granularity.** Intraday threshold crossings and microstructure dynamics are missed; daily bars mask short-lived opportunities.  
6. **Crowding and efficiency.** Pairs trading is well known; slower implementations face residual noise rather than persistent mispricing.  
7. **Composition drift and survivorship.** ETF constituents and firm fundamentals evolve; fixed-coefficient relationships decay.

---

## 7. Educational Value

- End-to-end research workflow with transparent, reproducible code.  
- Correct use of stationarity and cointegration diagnostics (ADF, Engle–Granger).  
- Proper IS/OOS evaluation with realistic costs.  
- Honest analysis of failure modes: non-stationarity, cost pressure, parameter fragility.  
- A demonstration that methodological rigor is more important than backtest overfitting.

---

## 8. Future Work

- Rolling or state-dependent re-estimation of $(\alpha,\beta)$; walk-forward model updates.  
- Regime detection and adaptive thresholds $z_{\text{open}}$, $z_{\text{close}}$.  
- Higher-frequency data; explicit microstructure cost modeling.  
- Portfolio construction across many pairs with sector/beta neutrality.  
- Alternative spread formation (e.g., Johansen, state-space/Kalman), and disciplined comparison to ML-based residual models.

---

## 9. Requirements

- python
- numpy
- pandas
- matplotlib
- statsmodels
- yfinance
  
---

## 10. License

MIT License. Intended for academic and research purposes.

---

## 11. Citation

Kostanyan, Ruben (2025). *Market-Neutral Pairs Trading (Cointegration-Based): An Empirical Backtest and Sensitivity Study.* GitHub Repository: https://github.com/Ruben010999/PairsTrading
