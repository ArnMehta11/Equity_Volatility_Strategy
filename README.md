# Equity_Volatility_Strategy

Systematic event-driven options straddle research across three catalysts — earnings announcements, FOMC decisions, and geopolitical shocks — using S&P 500 constituents and sector ETFs from 2016-2025. Identifies exploitable IV mispricing patterns through walk-forward long/short backtesting.

---

## Overview

This project investigates whether implied volatility around scheduled and unscheduled market events is systematically mispriced, and whether that mispricing can be exploited through a disciplined ATM straddle strategy. The research spans three distinct event types, each with its own data pipeline, analytical framework, and walk-forward backtest.

The theoretical foundation draws partially from Gao, Xing & Zhang (2018), "Anticipating Uncertainty: Straddles Around Earnings Announcements," published in the Journal of Financial and Quantitative Analysis. The paper documents a pre-announcement drift in implied volatility for individual stocks in the days before earnings, and provides a rigorous set of option selection filters that we adopt throughout this project.

---

## Academic Foundation

**Gao, Xing & Zhang (2018) — JFQA**

The paper's central finding is that implied volatility rises systematically in the 3 days before an earnings announcement and collapses sharply after results are released — a pattern known as IV crush. The authors argue that this run-up is not fully rational: the market underprices earnings uncertainty in the pre-announcement window, creating a long straddle edge that earns statistically significant positive returns even after controlling for standard risk factors.

The paper provides five option selection filters that we implement across all three pipelines:

| Filter | Rule |
|--------|------|
| F1 | Option price >= $0.125 |
| F2 | Stock price >= $5.00 |
| F5 | Days to expiry: 10-60 |
| F6 | Abs(delta): 0.375-0.625 |
| F7 | Moneyness: 0.9-1.1 |

ATM strike selection uses the globally nearest strike to spot within the moneyness window, then the nearest available expiry. Exit prices use the same contract pinned from entry — strike and expiry are fixed at entry and do not change on exit.

The return metric throughout is `pnl_pct = (exit_straddle_mid - entry_straddle_mid) / entry_straddle_mid`, representing return on the straddle premium paid, assuming equal dollar sizing per trade.

---

## Data

All options data is collected from the **Polygon.io** historical API. Underlying spot prices are fetched from **yfinance** and reverse-adjusted for stock splits using a custom `SplitAdjuster` class to match Polygon's historical strike price basis. VWAP is used as the primary price source for all option legs where available, falling back to the daily close. Across all three datasets, 100% VWAP coverage was achieved on both entry legs.

### Event Universes

| Event Type | Universe | Period | Events | Rows |
|---|---|---|---|---|
| Earnings | S&P 500 constituents (point-in-time) | 2016-2025 | 1,522 | 63,021 |
| FOMC | 15 sector ETFs | 2020-2025 | 49 meetings | 4,900 |
| Geopolitical | 15 sector ETFs | 2018-2025 | 182 events | 13,066 |

S&P 500 constituent membership is determined point-in-time using a daily snapshot CSV covering 1996-2026, eliminating survivorship bias. Only companies that were actually in the index during a given year are included in that year's analysis.

### Sector ETF Universe (FOMC and Geopolitical)

| Ticker | Description |
|--------|-------------|
| SPY | S&P 500 benchmark |
| QQQ | Nasdaq 100 |
| XLK | Technology |
| XLF | Financials |
| XLE | Energy |
| XLI | Industrials |
| XLV | Health Care |
| XLB | Materials |
| XLP | Consumer Staples |
| GLD | Gold |
| TLT | Long-duration Treasuries |
| IWM | Russell 2000 |
| EEM | Emerging Markets |
| XOP | Oil & Gas E&P |
| ITA | Aerospace & Defense |

---

## Entry/Exit Framework

### Earnings and FOMC

Entry and exit are expressed as offsets relative to the event date (T=0):

- **Entry offsets:** T-3, T-2, T-1, T+0
- **Exit offsets:** T+0, T+1, T+2, T+3
- **Valid combos:** 15 (16 minus the T0/T0 combination which always yields zero)

This produces a 4x4 grid of 16 entry/exit combinations per event, of which 15 are non-trivial. All offsets are in trading days, skipping weekends and holidays.

### Geopolitical

Geopolitical events are unknowable in advance, so entry cannot occur before the event:

- **Entry offsets:** T+1, T+2, T+3 (post-event only)
- **Exit offsets:** T+2 through T+7 (strictly after entry)
- **Valid combos:** 15 (exit must be strictly greater than entry)

---

## Research Workstreams

### 1. Earnings Straddle (Long)

The earnings pipeline collects ATM straddle prices for all S&P 500 constituents across 1,522 earnings events from 2016-2025. The structural hypothesis from Gao, Xing & Zhang is tested at scale: does the pre-announcement IV run-up create a systematic long straddle edge across the full index, and does it vary by sector?

Key findings:
- The T+0 exit combos (enter pre-announcement, exit on earnings day) show the most consistent positive returns, capturing the IV run-up without holding through IV crush
- Win rates on long straddles are below 50% on most combos, confirming the positive skew nature of the strategy — occasional large wins drive the average
- Technology sector shows the strongest and most consistent pre-announcement edge
- Returns deteriorate sharply after T+0 exit as IV crush dominates any continued directional movement

### 2. FOMC Straddle (Long and Short)

The FOMC pipeline tests whether rate decision uncertainty is systematically mispriced across 15 sector ETFs over 49 Fed meetings from 2020-2025. Unlike earnings, the FOMC framework tests both long and short straddles, since the Fed's extensive forward guidance may mean IV is overpriced heading into meetings rather than underpriced.

Key findings:
- SPY shows the classic short-duration pattern: positive returns only at T+0 exit, steep losses thereafter as IV crush dominates
- QQQ exhibits a longer positive window, remaining profitable through T+1 and T+2 exits — tech sector rate sensitivity creates sustained post-announcement movement
- XLK is the strongest performer with a nearly uniformly green matrix, including large positive returns on E+0/X+2 and E+0/X+3 entries — suggesting FOMC decision day itself is the optimal entry for technology
- TLT, despite being the most directly rate-sensitive instrument, shows catastrophic losses at T+2 and T+3 exits (approaching -32%) with near-zero win rates — suggesting treasury options already fully price in rate uncertainty before the meeting
- XLE shows the hardest exit rule in the dataset: profitable only at T+0, with win rates collapsing to 19-26% at T+2 and T+3
- Defensive sectors (XLV, XLP) show no meaningful FOMC edge and low coverage, confirming the options market does not build IV into these sectors around Fed meetings

The walk-forward strategy (2020-2022 train, 2023-2025 test) identifies long and short signals per ticker/combo and applies them out-of-sample.

### 3. Geopolitical Event Straddle

The geopolitical pipeline takes a fundamentally different approach. Since events are unscheduled and unknowable in advance, entry is strictly post-event (T+1 to T+3). The hypothesis is that elevated uncertainty after a major geopolitical shock persists for several days, creating a window to profit from continued volatility.

183 events across 14 categories are covered from 2018-2025:

| Category | Events |
|----------|--------|
| Military/War | 55 |
| Trade War | 34 |
| Political | 26 |
| Financial | 20 |
| Pandemic | 16 |
| Elections | 9 |
| Tech | 8 |
| Energy | 7 |
| Sanctions | 6 |
| Supply Chain | 4 |
| Natural Disaster | 3 |
| Cyber | 3 |
| Currency | 3 |
| Central Bank | 1 |

The strategy uses `(category, entry_offset, exit_offset)` triples as signal keys — the same combo may be long for Military/War events and short for Pandemic events. Walk-forward validation uses 2018-2021 as training and 2022-2025 as test.

---

## Methodology Notes

### Walk-Forward Validation

All three strategies use strict walk-forward validation to avoid look-ahead bias. Signals are identified exclusively on the training period and applied without modification to the test period. No re-optimization occurs between training and test.

For earnings the split is approximately 60/40 (2016-2021 train, 2022-2025 test), chosen to cover the zero-rate era and COVID shock in training while testing across the full rate cycle including hiking, plateau, and cutting regimes.

For FOMC the split is 2020-2022 train, 2023-2025 test — 3 years of training covering zero rates and the 2022 hiking shock, tested across the plateau and cutting cycle.

For geopolitical the split is 2018-2021 train, 2022-2025 test — covering the trade war and COVID periods in training, tested across Ukraine/Russia, Middle East conflicts, and the 2022-2025 macro regime.

### Signal Identification

Long signals require avg_ret > 1%, median_ret > 0%, and n > 10 in the training period. Short signals require avg_ret < -1%, median_ret < 0%, and n > 10. The median filter ensures the edge is consistent rather than driven by a small number of outlier events.

### Performance Metrics

The primary performance metrics are profit factor (gross profit / gross loss), avg win / avg loss ratio, win rate, and total PnL relative to capital deployed. Sharpe and Sortino ratios are computed on a portfolio basis using the fixed portfolio size as the capital denominator. Standard annualisation via sqrt(years) is used rather than trades-per-year to avoid inflating risk-adjusted metrics for high-frequency event-driven strategies.

---

## Repository Structure

```
equity_volatility/
├── mag7_data/                          # Mag 7 pilot data
├── options_data_sp500_2016_2020/       # Earnings options batch 1
│   ├── sp500_options_pit.csv
│   ├── sp500_earnings_history.csv
│   ├── sp500_constituents_by_year.json
│   └── split_history_cache.json
├── options_data_sp500_2020_2025/       # Earnings options batch 2
│   ├── sp500_options_pit.csv
│   ├── sp500_earnings_history.csv
│   ├── sp500_constituents_by_year.json
│   └── split_history_cache.json
├── fomc_etf_data/                      # FOMC ETF options
│   └── fomc_etf_options.csv
├── geopolitical_etf_data/              # Geopolitical ETF options
│   └── geopolitical_etf_options.csv
├── earnings_analysis.ipynb             # Earnings straddle analysis
├── fomc_analysis.ipynb                 # FOMC straddle analysis
├── geopolitical_analysis.ipynb         # Geopolitical straddle analysis
├── run_3-8.py                          # Earnings pipeline
└── README.md
```

---

## Key Limitations

**Look-ahead bias in signal selection.** All signals are identified on the training period only. However, the choice of thresholds (1%, n > 10) and the train/test split dates were determined with knowledge of the full dataset structure, which introduces a mild form of researcher degrees of freedom.

**Transaction costs.** All analysis assumes execution at the VWAP mid price. In practice, ATM options carry a bid-ask spread of $0.05-$0.20 per contract. A realistic friction estimate of $0.10 per leg per trade would reduce returns meaningfully on short-duration combos with small average returns.

**Capacity.** The strategy as designed cannot be implemented at institutional scale. Running straddles on 500+ stocks around every earnings date requires significant capital and creates concentration risk during earnings season.

**Sample size for geopolitical.** With only 182 events spread across 14 categories and 15 ETFs, many category/ETF/combo cells have very few observations. Signals in thin cells should be treated as directional hypotheses rather than statistically robust findings.

**Post-2010 decay.** Gao, Xing & Zhang note that the pre-announcement IV run-up weakened significantly after 2010 as the effect became widely known. Our 2016-2025 sample period tests whether any residual edge persists in a more crowded environment.

---

## Dependencies

```
pandas
numpy
plotly
yfinance
polygon-api-client
requests
beautifulsoup4
```

---

## Reference

Gao, M., Xing, Y., & Zhang, Y. (2018). Anticipating Uncertainty: Straddles Around Earnings Announcements. *Journal of Financial and Quantitative Analysis*, 53(2), 2155-2177.
