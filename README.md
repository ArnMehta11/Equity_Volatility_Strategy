# Equity_Volatility_Strategy

Systematic event-driven options straddle research across three catalysts:

1. Earnings Announcements
2. FOMC Decisions
3. Geopolitical Shocks

Using S&P 500 constituents and sector ETFs from 2016-2025. Identifies exploitable IV mispricing patterns through walk-forward long/short backtesting.

---

## Overview

This project investigates whether implied volatility around scheduled and unscheduled market events is systematically mispriced, and whether that mispricing can be exploited through a disciplined ATM straddle strategy. The research spans three distinct event types, each with its own data pipeline, analytical framework, and walk-forward backtest.

The theoretical foundation draws partially from Gao, Xing & Zhang (2018), "Anticipating Uncertainty: Straddles Around Earnings Announcements," published in the Journal of Financial and Quantitative Analysis. The paper documents a pre-announcement drift in implied volatility for individual stocks in the days before earnings, and provides a rigorous set of option selection filters that we adopt throughout this project.

---

## Academic Foundation

**Gao, Xing & Zhang (2018) - JFQA**

The paper's central finding is that implied volatility rises systematically in the 3 days before an earnings announcement and collapses sharply after results are released, a pattern known as IV crush. The authors argue that this run-up is not fully rational: the market underprices earnings uncertainty in the pre-announcement window, creating a long straddle edge that earns statistically significant positive returns even after controlling for standard risk factors.

The paper provides five option selection filters that we implement across all three pipelines:

| Filter | Rule |
|--------|------|
| F1 | Option price >= $0.125 |
| F2 | Stock price >= $5.00 |
| F5 | Days to expiry: 10-60 |
| F6 | Abs(delta): 0.375-0.625 |
| F7 | Moneyness: 0.9-1.1 |

ATM strike selection uses the globally nearest strike to spot within the moneyness window, then the nearest available expiry. Exit prices use the same contract pinned from entry - strike and expiry are fixed at entry and do not change on exit.

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

### Sector ETF Universe (for FOMC and Geopolitical)

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

## Reference

Gao, M., Xing, Y., & Zhang, Y. (2018). Anticipating Uncertainty: Straddles Around Earnings Announcements. *Journal of Financial and Quantitative Analysis*, 53(2), 2155-2177.
