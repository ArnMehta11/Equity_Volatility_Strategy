# %%
# Import neccessary libraries
import warnings
warnings.filterwarnings("ignore")
import math, os, json
import numpy as np
import pandas as pd
import yfinance as yf
from polygon import RESTClient
from datetime import timedelta
from concurrent.futures import ThreadPoolExecutor

# %%
unemployment_dates = ["Friday, January 10, 2025",
"Friday, February 7, 2025",
"Friday, March 7, 2025",
"Friday, April 4, 2025",
"Friday, May 2, 2025",
"Friday, June 6, 2025",
"Thursday, July 3, 2025",
"Friday, August 1, 2025",
"Friday, September 5, 2025",
"Thursday, November 20, 2025",
"Tuesday, December 16, 2025",
"Friday, January 05, 2024",
"Friday, February 02, 2024",
"Friday, March 08, 2024",
"Friday, April 5, 2024",
"Friday, May 3, 2024",
"Friday, June 7, 2024",
"Friday, July 05, 2024",
"Friday, August 2, 2024",
"Friday, September 6, 2024",
"Friday, October 04, 2024",
"Friday, November 1, 2024",
"Friday, December 06, 2024",
"Friday, January 06, 2023",
"Friday, February 03, 2023",
"Friday, March 10, 2023",
"Friday, April 07, 2023",
"Friday, May 05, 2023",
"Friday, June 02, 2023",
"Friday, July 07, 2023",
"Friday, August 04, 2023",
"Friday, September 01, 2023",
"Friday, October 06, 2023",
"Friday, November 03, 2023",
"Friday, December 08, 2023",
"Friday, January 07, 2022",
"Friday, February 04, 2022",
"Friday, March 4, 2022",
"Friday, April 1, 2022",
"Friday, May 06, 2022",
"Friday, June 3, 2022",
"Friday, July 8, 2022",
"Friday, August 05, 2022",
"Friday, September 02, 2022",
"Friday, October 07, 2022",
"Friday, November 04, 2022",
"Friday, December 02, 2022",
"Friday, January 8, 2021",
"Friday, February 5, 2021",
"Friday, March 5, 2021",
"Friday, April 2, 2021",
"Friday, May 07, 2021",
"Friday, June 04, 2021",
"Friday, July 2, 2021",
"Friday, August 6, 2021",
"Friday, September 3, 2021",
"Friday, October 8, 2021",
"Friday, November 05, 2021",
"Friday, December 3, 2021",
"Friday, January 10, 2020",
"Friday, February 07, 2020",
"Friday, March 06, 2020",
"Friday, April 03, 2020",
"Friday, May 08, 2020",
"Friday, June 05, 2020",
"Thursday, July 02, 2020",
"Friday, August 07, 2020",
"Friday, September 04, 2020",
"Friday, October 02, 2020",
"Friday, November 6, 2020",
"Friday, December 4, 2020",
"Friday, January 04, 2019",
"Friday, February 01, 2019",
"Friday, March 08, 2019",
"Friday, April 05, 2019",
"Friday, May 03, 2019",
"Friday, June 07, 2019",
"Friday, July 05, 2019",
"Friday, August 02, 2019",
"Friday, September 06, 2019",
"Friday, October 04, 2019",
"Friday, November 01, 2019",
"Friday, December 06, 2019",
"Friday, January 05, 2018",
"Friday, February 02, 2018",
"Friday, March 09, 2018",
"Friday, April 06, 2018",
"Friday, May 04, 2018",
"Friday, June 01, 2018",
"Friday, July 06, 2018",
"Friday, August 03, 2018",
"Friday, September 07, 2018",
"Friday, October 05, 2018",
"Friday, November 02, 2018",
"Friday, December 07, 2018",
"Friday, January 06, 2017",
"Friday, February 03, 2017",
"Friday, March 10, 2017",
"Friday, April 07, 2017",
"Friday, May 05, 2017",
"Friday, June 02, 2017",
"Friday, July 07, 2017",
"Friday, August 04, 2017",
"Friday, September 01, 2017",
"Friday, October 06, 2017",
"Friday, November 03, 2017",
"Friday, December 08, 2017",
"Friday, January 08, 2016",
"Friday, February 05, 2016",
"Friday, March 04, 2016",
"Friday, April 01, 2016",
"Friday, May 06, 2016",
"Friday, June 03, 2016",
"Friday, July 08, 2016",
"Friday, August 05, 2016",
"Friday, September 02, 2016",
"Friday, October 07, 2016",
"Friday, November 04, 2016",
"Friday, December 02, 2016",]

# convert dates to datetime format
unemployment_dates = pd.to_datetime(unemployment_dates)
unemployment_dates

# %%
CPI_dates = ["2016-01-20",
"2016-02-19",
"2016-03-16",
"2016-04-14",
"2016-05-17",
"2016-06-16",
"2016-07-15",
"2016-08-16",
"2016-09-16",
"2016-10-18",
"2016-11-17",
"2016-12-15",
"2017-01-18",
"2017-02-13",
"2017-02-15",
"2017-03-15",
"2017-04-14",
"2017-05-12",
"2017-06-14",
"2017-07-14",
"2017-08-11",
"2017-09-14",
"2017-10-13",
"2017-11-15",
"2017-12-13",
"2018-01-12",
"2018-02-14",
"2018-03-13",
"2018-04-11",
"2018-05-10",
"2018-06-12",
"2018-07-12",
"2018-08-10",
"2018-09-13",
"2018-10-11",
"2018-11-14",
"2018-12-12",
"2019-01-11",
"2019-02-11",
"2019-02-13",
"2019-03-12",
"2019-04-10",
"2019-05-10",
"2019-06-12",
"2019-07-11",
"2019-08-13",
"2019-09-12",
"2019-10-10",
"2019-11-13",
"2019-12-11",
"2020-01-14",
"2020-02-11",
"2020-02-13",
"2020-03-11",
"2020-04-10",
"2020-05-12",
"2020-06-10",
"2020-07-14",
"2020-08-12",
"2020-09-11",
"2020-10-13",
"2020-11-12",
"2020-12-10",
"2021-01-13",
"2021-02-08",
"2021-02-10",
"2021-03-10",
"2021-04-13",
"2021-05-12",
"2021-06-10",
"2021-07-13",
"2021-08-11",
"2021-09-14",
"2021-10-13",
"2021-11-10",
"2021-12-10",
"2022-01-12",
"2022-02-08",
"2022-02-10",
"2022-03-10",
"2022-04-12",
"2022-05-11",
"2022-06-10",
"2022-07-13",
"2022-08-10",
"2022-09-13",
"2022-10-13",
"2022-11-10",
"2022-12-13",
"2023-01-12",
"2023-02-10",
"2023-02-14",
"2023-03-14",
"2023-04-12",
"2023-05-10",
"2023-06-13",
"2023-07-12",
"2023-08-10",
"2023-09-13",
"2023-10-12",
"2023-11-14",
"2023-12-12",
"2024-01-11",
"2024-02-09",
"2024-02-13",
"2024-03-12",
"2024-04-10",
"2024-05-15",
"2024-06-12",
"2024-07-11",
"2024-08-14",
"2024-09-11",
"2024-10-10",
"2024-11-13",
"2024-12-11",
"2025-01-15",
"2025-02-12",
"2025-03-12",
"2025-04-10",
"2025-05-13",
"2025-06-11",
"2025-07-15",
"2025-08-12",
"2025-09-11",
"2025-10-24",
"2025-12-18",
]

# convert dates to datetime format
CPI_dates = pd.to_datetime(CPI_dates)
CPI_dates

# %%
# Configurations
from dotenv import load_dotenv
load_dotenv()

API_KEY    = os.getenv("polygon_key")
OUTPUT_DIR  = "fomc_etf_data"
OUTPUT_FILE = f"{OUTPUT_DIR}/cpi_unemployment_etf_options.csv"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ETF universe
TICKERS = [
    "SPY",   # S&P 500 benchmark
    "QQQ",   # Nasdaq 100
    "XLK",   # Technology
    "XLF",   # Financials
    "XLE",   # Energy
    "XLI",   # Industrials
    "XLV",   # Health Care
    "XLB",   # Materials
    "XLP",   # Consumer Staples
    "GLD",   # Gold
    "TLT",   # Long-duration Treasuries
    "IWM",   # Russell 2000
    "EEM",   # Emerging Markets
    "XOP",   # Oil & Gas E&P
    "ITA",   # Aerospace & Defense
]

# Build combined event list with event_type tags
# Unemployment dates need parsing from long-form strings; CPI dates are already ISO
EVENT_DATES = []
for d in unemployment_dates:
    EVENT_DATES.append((pd.to_datetime(d).strftime("%Y-%m-%d"), "Unemployment"))
for d in CPI_dates:
    EVENT_DATES.append((pd.to_datetime(d).strftime("%Y-%m-%d"), "CPI"))

# Sort chronologically and deduplicate
EVENT_DATES = sorted(set(EVENT_DATES), key=lambda x: x[0])
print(f"Total event dates: {len(EVENT_DATES)} "
      f"(CPI: {sum(1 for _,t in EVENT_DATES if t=='CPI')}, "
      f"Unemployment: {sum(1 for _,t in EVENT_DATES if t=='Unemployment')})")

# Entry/exit grid
ENTRY_OFFSETS = [-3, -2, -1, 0]
EXIT_OFFSETS  = [0, 1, 2, 3]
VALID_COMBOS  = [(e, x) for e in ENTRY_OFFSETS
                          for x in EXIT_OFFSETS if x >= e]

# Paper filters
MIN_OPTION_PRICE = 0.125
MIN_STOCK_PRICE  = 5.0
MIN_DTE          = 10
MAX_DTE          = 60
MIN_DELTA        = 0.375
MAX_DELTA        = 0.625
MIN_MONEYNESS    = 0.9
MAX_MONEYNESS    = 1.1
R                = 0.05
MIN_DTE_FOR_IV   = 3

# %%
# SPLIT ADJUSTER  (ETFs rarely split but TLT, GLD etc. occasionally do)
SPLIT_CACHE_FILE = f"{OUTPUT_DIR}/split_cache.json"

class SplitAdjuster:
    def __init__(self, cache_file=None):
        self._mem   = {}
        self._disk  = {}
        self._cfile = cache_file
        if cache_file and os.path.exists(cache_file):
            try:
                with open(cache_file) as f:
                    self._disk = json.load(f)
            except Exception: pass

    def _fetch(self, ticker):
        try:
            splits = yf.Ticker(ticker).splits
            if splits.empty: return []
            out = []
            for dt, r in splits.items():
                out.append((pd.to_datetime(dt).tz_localize(None)
                              .normalize().strftime("%Y-%m-%d"), float(r)))
            return sorted(out)
        except Exception:
            return []

    def get_splits(self, ticker):
        if ticker in self._mem:  return self._mem[ticker]
        if ticker in self._disk:
            self._mem[ticker] = self._disk[ticker]; return self._disk[ticker]
        s = self._fetch(ticker)
        self._mem[ticker] = s
        if self._cfile:
            self._disk[ticker] = s
            try:
                with open(self._cfile, "w") as f: json.dump(self._disk, f)
            except Exception: pass
        return s

    def unadjust(self, ticker, date_str, adj_close):
        if adj_close is None or np.isnan(adj_close): return adj_close
        trade_dt = pd.to_datetime(date_str)
        factor   = 1.0
        for sd, r in self.get_splits(ticker):
            if pd.to_datetime(sd) > trade_dt: factor *= r
        return round(adj_close * factor, 2)

    def get_closes(self, ticker, dates):
        closes = {}
        if not dates: return closes
        dts      = [pd.to_datetime(d) for d in dates]
        min_date = (min(dts) - timedelta(days=7)).strftime("%Y-%m-%d")
        max_date = (max(dts) + timedelta(days=1)).strftime("%Y-%m-%d")
        try:
            df = yf.download(ticker, start=min_date, end=max_date,
                             progress=False, auto_adjust=True)
            if df.empty: return closes
            for date_str in dates:
                dt  = pd.to_datetime(date_str)
                sub = df[df.index <= dt]
                if not sub.empty:
                    val = sub["Close"].iloc[-1]
                    adj = round(float(val.iloc[0] if hasattr(val,"iloc") else val), 2)
                    closes[date_str] = self.unadjust(ticker, date_str, adj)
                else:
                    closes[date_str] = None
        except Exception as e:
            print(f"  [yfinance] {ticker}: {e}")
        return closes


adjuster = SplitAdjuster(cache_file=SPLIT_CACHE_FILE)

# %%
# Polygon Helpers
def _ohlc(client, oticker, date_str):
    try:
        d    = pd.to_datetime(date_str).strftime("%Y-%m-%d")
        aggs = list(client.get_aggs(oticker, 1, "day", d, d))
        if aggs:
            a = aggs[0]
            return (
                float(a.vwap)  if (hasattr(a,"vwap")  and a.vwap)  else None,
                float(a.close) if (hasattr(a,"close") and a.close) else None,
                float(a.high)  if (hasattr(a,"high")  and a.high)  else None,
                float(a.low)   if (hasattr(a,"low")   and a.low)   else None,
            )
    except Exception: pass
    return None, None, None, None


def _fetch_legs(client, call_ticker, put_ticker, date_str):
    with ThreadPoolExecutor(max_workers=2) as ex:
        fc = ex.submit(_ohlc, client, call_ticker, date_str)
        fp = ex.submit(_ohlc, client, put_ticker,  date_str)
        cv, cc, ch, cl = fc.result()
        pv, pc, ph, pl = fp.result()
    return cv, cc, ch, cl, pv, pc, ph, pl


def _mid(vwap, close):
    if vwap  is not None and vwap  > 0: return vwap,  "vwap"
    if close is not None and close > 0: return close, "close"
    return None, None

# %%
# Black Scholes
def _ncdf(x): return 0.5*(1.0 + math.erf(x/math.sqrt(2.0)))

def _bs(S, K, T, r, sig, opt):
    if T<=0 or sig<=0 or S<=0 or K<=0: return float("nan")
    d1 = (math.log(S/K)+(r+0.5*sig**2)*T)/(sig*math.sqrt(T)); d2=d1-sig*math.sqrt(T)
    return S*_ncdf(d1)-K*math.exp(-r*T)*_ncdf(d2) if opt=="call" \
           else K*math.exp(-r*T)*_ncdf(-d2)-S*_ncdf(-d1)

def _iv(price, S, K, T, r, opt, lo=1e-6, hi=5.0, tol=1e-6, n=120):
    if price is None or np.isnan(price) or price<=0 or T<=0: return float("nan")
    fl=_bs(S,K,T,r,lo,opt)-price; fh=_bs(S,K,T,r,hi,opt)-price
    if np.isnan(fl) or np.isnan(fh) or fl*fh>0: return float("nan")
    for _ in range(n):
        m=0.5*(lo+hi); fm=_bs(S,K,T,r,m,opt)-price
        if abs(fm)<tol: return m
        if fl*fm<=0: hi,fh=m,fm
        else:        lo,fl=m,fm
    return 0.5*(lo+hi)

def _delta(S, K, T, r, sig, opt):
    if T<=0 or sig<=0 or S<=0 or K<=0: return float("nan")
    d1 = (math.log(S/K)+(r+0.5*sig**2)*T)/(sig*math.sqrt(T))
    return _ncdf(d1) if opt=="call" else _ncdf(d1)-1.0

def _trading_day(date_str, offset):
    cur = pd.to_datetime(date_str)
    direction = 1 if offset >= 0 else -1
    rem = abs(offset)
    while rem > 0:
        cur += timedelta(days=direction)
        if cur.weekday() < 5: rem -= 1
    return cur.strftime("%Y-%m-%d")

# %%
# Entry Snapshot
def _entry(client, ticker, entry_date, spot):
    if spot is None or spot < MIN_STOCK_PRICE: return None

    trade_dt = pd.to_datetime(entry_date)
    exp_min  = (trade_dt + timedelta(days=MIN_DTE)).strftime("%Y-%m-%d")
    exp_max  = (trade_dt + timedelta(days=MAX_DTE)).strftime("%Y-%m-%d")

    try:
        contracts = list(client.list_options_contracts(
            underlying_ticker=ticker,
            expiration_date_gte=exp_min, expiration_date_lte=exp_max,
            expired=True, limit=1000,
        ))
    except Exception as e:
        print(f"  [entry] {ticker} {entry_date}: {e}"); return None
    if not contracts: return None

    df = pd.DataFrame([{"oticker":c.ticker, "strike":float(c.strike_price),
                         "expiry":str(c.expiration_date),
                         "type":str(c.contract_type)} for c in contracts])
    df["moneyness"] = df["strike"] / spot
    df = df[df["moneyness"].between(MIN_MONEYNESS, MAX_MONEYNESS)]
    if df.empty: return None

    best_strike = min(df["strike"].unique(), key=lambda s: abs(s-spot))
    sdf = df[df["strike"]==best_strike]

    for expiry in sorted(sdf["expiry"].unique()):
        edf = sdf[sdf["expiry"]==expiry]
        dte = (pd.to_datetime(expiry)-trade_dt).days
        T   = max(dte/365.25, 1e-6)
        cr  = edf[edf["type"]=="call"]; pr = edf[edf["type"]=="put"]
        if cr.empty or pr.empty: continue

        cv,cc,ch,cl,pv,pc,ph,pl = _fetch_legs(
            client, cr.iloc[0]["oticker"], pr.iloc[0]["oticker"], entry_date)
        cm, cs = _mid(cv, cc); pm, ps = _mid(pv, pc)
        if cm is None or pm is None: continue
        if cm < MIN_OPTION_PRICE or pm < MIN_OPTION_PRICE: continue

        civ = _iv(cm, spot, best_strike, T, R, "call")
        piv = _iv(pm, spot, best_strike, T, R, "put")
        cd  = _delta(spot, best_strike, T, R, civ if not np.isnan(civ) else 0.3, "call")
        pd_ = _delta(spot, best_strike, T, R, piv if not np.isnan(piv) else 0.3, "put")

        if np.isnan(cd) or np.isnan(pd_): continue
        if not (MIN_DELTA <= abs(cd) <= MAX_DELTA): continue
        if not (MIN_DELTA <= abs(pd_) <= MAX_DELTA): continue

        return {
            "stock_close": spot, "strike": best_strike, "expiry": expiry,
            "dte": dte, "call_ticker": cr.iloc[0]["oticker"],
            "call_mid": cm, "call_vwap": cv, "call_close": cc,
            "call_high": ch, "call_low": cl, "call_iv": civ, "call_delta": cd,
            "put_ticker": pr.iloc[0]["oticker"],
            "put_mid": pm, "put_vwap": pv, "put_close": pc,
            "put_high": ph, "put_low": pl, "put_iv": piv, "put_delta": pd_,
            "straddle_mid": cm+pm, "price_source": f"{cs}+{ps}",
            "atm_iv": float(np.nanmean([civ, piv])), "moneyness": best_strike/spot,
        }
    return None

# %%
# Exit Snapshot
def _exit(client, ticker, exit_date, pin_strike, pin_expiry, spot_exit):
    trade_dt = pd.to_datetime(exit_date)
    exp_dt   = pd.to_datetime(pin_expiry)
    dte      = (exp_dt - trade_dt).days
    if trade_dt > exp_dt: return None

    try:
        contracts = list(client.list_options_contracts(
            underlying_ticker=ticker,
            expiration_date_gte=pin_expiry, expiration_date_lte=pin_expiry,
            expired=True, limit=1000,
        ))
    except Exception as e:
        print(f"  [exit] {ticker} {exit_date}: {e}"); return None
    if not contracts: return None

    df = pd.DataFrame([{"oticker":c.ticker, "strike":float(c.strike_price),
                         "expiry":str(c.expiration_date),
                         "type":str(c.contract_type)} for c in contracts])
    df = df[df["strike"]==pin_strike]
    if df.empty: return None

    cr = df[df["type"]=="call"]; pr = df[df["type"]=="put"]
    if cr.empty or pr.empty: return None

    cv,cc,ch,cl,pv,pc,ph,pl = _fetch_legs(
        client, cr.iloc[0]["oticker"], pr.iloc[0]["oticker"], exit_date)
    cm, cs = _mid(cv, cc); pm, ps = _mid(pv, pc)
    if cm is None or pm is None: return None

    T    = max(dte/365.25, 1e-6)
    iv_r = dte >= MIN_DTE_FOR_IV
    civ  = _iv(cm, spot_exit, pin_strike, T, R, "call") if spot_exit else float("nan")
    piv  = _iv(pm, spot_exit, pin_strike, T, R, "put")  if spot_exit else float("nan")

    return {
        "stock_close": spot_exit, "dte": dte, "iv_reliable": iv_r,
        "call_mid": cm, "call_vwap": cv, "call_close": cc,
        "call_high": ch, "call_low": cl, "call_iv": civ,
        "put_mid": pm, "put_vwap": pv, "put_close": pc,
        "put_high": ph, "put_low": pl, "put_iv": piv,
        "straddle_mid": cm+pm, "price_source": f"{cs}+{ps}",
        "atm_iv": float(np.nanmean([civ, piv])),
    }

# %%
# Process one ticker per one event date
def process(ticker, event_date, event_type, job_num, total_jobs, done):
    client = RESTClient(API_KEY)
    rows   = []

    # Bulk fetch all closes needed
    all_dates = set(_trading_day(event_date, o)
                    for o in ENTRY_OFFSETS + EXIT_OFFSETS)
    closes = adjuster.get_closes(ticker, list(all_dates))

    # Entry snapshots
    entry_snaps = {}
    for e_off in ENTRY_OFFSETS:
        needed = [(e_off, x) for x in EXIT_OFFSETS
                  if x >= e_off and (ticker, event_date, event_type, e_off, x) not in done]
        if not needed: continue
        e_date = _trading_day(event_date, e_off)
        snap   = _entry(client, ticker, e_date, closes.get(e_date))
        if snap: entry_snaps[e_off] = (e_date, snap)

    if not entry_snaps: return rows

    exit_cache = {}

    for e_off, (e_date, esnap) in entry_snaps.items():
        for x_off in EXIT_OFFSETS:
            if x_off < e_off: continue
            if (ticker, event_date, event_type, e_off, x_off) in done: continue

            x_date = _trading_day(event_date, x_off)
            s_exit = closes.get(x_date)

            # Same day → reuse entry as exit
            if x_date == e_date:
                xsnap = {
                    "stock_close": esnap["stock_close"], "dte": esnap["dte"],
                    "iv_reliable": esnap["dte"] >= MIN_DTE_FOR_IV,
                    "call_mid": esnap["call_mid"], "call_vwap": esnap["call_vwap"],
                    "call_close": esnap["call_close"], "call_high": esnap["call_high"],
                    "call_low": esnap["call_low"], "call_iv": esnap["call_iv"],
                    "put_mid": esnap["put_mid"], "put_vwap": esnap["put_vwap"],
                    "put_close": esnap["put_close"], "put_high": esnap["put_high"],
                    "put_low": esnap["put_low"], "put_iv": esnap["put_iv"],
                    "straddle_mid": esnap["straddle_mid"],
                    "price_source": esnap["price_source"], "atm_iv": esnap["atm_iv"],
                }
            else:
                ck = (x_date, esnap["strike"], esnap["expiry"])
                if ck not in exit_cache:
                    exit_cache[ck] = _exit(client, ticker, x_date,
                                           esnap["strike"], esnap["expiry"], s_exit)
                xsnap = exit_cache[ck]

            if xsnap is None: continue

            pnl     = xsnap["straddle_mid"] - esnap["straddle_mid"]
            pnl_pct = pnl / esnap["straddle_mid"] if esnap["straddle_mid"] > 0 else None
            smove   = ((xsnap["stock_close"] - esnap["stock_close"]) /
                        esnap["stock_close"]
                       if xsnap["stock_close"] and esnap["stock_close"] else None)
            iv_chg  = (xsnap["atm_iv"] - esnap["atm_iv"]
                       if (xsnap["iv_reliable"] and
                           not np.isnan(xsnap["atm_iv"]) and
                           not np.isnan(esnap["atm_iv"])) else None)

            rows.append({
                "ticker":             ticker,
                "event_date":         event_date,
                "event_type":         event_type,
                "year":               int(event_date[:4]),
                "entry_offset":       e_off,
                "exit_offset":        x_off,
                "entry_date":         e_date,
                "exit_date":          x_date,
                "strike":             esnap["strike"],
                "expiry":             esnap["expiry"],
                "dte_at_entry":       esnap["dte"],
                "dte_at_exit":        xsnap["dte"],
                "exit_iv_reliable":   xsnap["iv_reliable"],
                "moneyness_at_entry": esnap["moneyness"],
                "call_ticker":        esnap["call_ticker"],
                "put_ticker":         esnap["put_ticker"],
                "stock_entry":        esnap["stock_close"],
                "stock_exit":         xsnap["stock_close"],
                "stock_move":         smove,
                "entry_call_mid":     esnap["call_mid"],
                "entry_call_iv":      esnap["call_iv"],
                "entry_call_delta":   esnap["call_delta"],
                "entry_put_mid":      esnap["put_mid"],
                "entry_put_iv":       esnap["put_iv"],
                "entry_put_delta":    esnap["put_delta"],
                "entry_straddle_mid": esnap["straddle_mid"],
                "entry_atm_iv":       esnap["atm_iv"],
                "entry_price_source": esnap["price_source"],
                "exit_call_mid":      xsnap["call_mid"],
                "exit_call_iv":       xsnap["call_iv"],
                "exit_put_mid":       xsnap["put_mid"],
                "exit_put_iv":        xsnap["put_iv"],
                "exit_straddle_mid":  xsnap["straddle_mid"],
                "exit_atm_iv":        xsnap["atm_iv"],
                "exit_price_source":  xsnap["price_source"],
                "pnl_per_straddle":   pnl,
                "pnl_pct":            pnl_pct,
                "iv_change":          iv_chg,
            })

    if rows:
        print(f"  [{job_num}/{total_jobs}] {ticker} {event_date} ({event_type}): {len(rows)} rows")
    return rows

# %%
print("CPI + Unemployment Straddle Pipeline  - 15 SECTOR ETFs - 2016-2025")
print(f"Tickers      : {TICKERS}")
print(f"Event dates  : {len(EVENT_DATES)} "
      f"(CPI: {sum(1 for _,t in EVENT_DATES if t=='CPI')}, "
      f"Unemployment: {sum(1 for _,t in EVENT_DATES if t=='Unemployment')})")
print(f"Valid combos : {len(VALID_COMBOS)} per job")
print(f"Total jobs   : {len(TICKERS) * len(EVENT_DATES)}")
print(f"Max rows     : {len(TICKERS) * len(EVENT_DATES) * len(VALID_COMBOS):,}")
print(f"Output       : {OUTPUT_FILE}")

# Build job list - ticker × (event_date, event_type), sorted chronologically
jobs = [(t, d, et) for (d, et) in EVENT_DATES for t in TICKERS]

# Resume
done = set()
if os.path.exists(OUTPUT_FILE):
    ex = pd.read_csv(OUTPUT_FILE)
    done = set(zip(ex["ticker"], ex["event_date"], ex["event_type"],
                   ex["entry_offset"], ex["exit_offset"]))
    print(f"\nResuming — {len(done):,} combo-rows already done "
          f"({ex['ticker'].nunique()} tickers, "
          f"{ex['event_date'].nunique()} event dates)")

total_jobs = len(jobs)
print(f"Jobs to run  : {total_jobs}\n")

for job_num, (ticker, event_date, event_type) in enumerate(jobs, 1):
    try:
        rows = process(ticker, event_date, event_type, job_num, total_jobs, done)
    except Exception as e:
        print(f"  {ticker} {event_date} ({event_type}): {e}")
        rows = []

    if rows:
        batch        = pd.DataFrame(rows)
        write_header = not os.path.exists(OUTPUT_FILE)
        batch.to_csv(OUTPUT_FILE, mode="a", header=write_header, index=False)
        for r in rows:
            done.add((r["ticker"], r["event_date"], r["event_type"],
                      r["entry_offset"], r["exit_offset"]))

    # Checkpoint every 100 jobs
    if job_num % 100 == 0 and os.path.exists(OUTPUT_FILE):
        saved = pd.read_csv(OUTPUT_FILE)
        print(f"\n── Checkpoint {job_num}/{total_jobs} "
              f"({job_num/total_jobs*100:.0f}%) ──")
        print(f"   Rows : {len(saved):,} | "
              f"Tickers: {saved['ticker'].nunique()} | "
              f"Events : {saved['event_date'].nunique()}\n")

# Summary
print("Pipeline complete!")

if os.path.exists(OUTPUT_FILE):
    out = pd.read_csv(OUTPUT_FILE)
    print(f"\n {OUTPUT_FILE}")
    print(f"  Rows       : {len(out):,}")
    print(f"  Tickers    : {out['ticker'].nunique()}")
    print(f"  Event dates: {out['event_date'].nunique()}")
    print(f"  Years      : {sorted(out['year'].unique())}")
    print(f"  Combos     : {out.groupby(['entry_offset','exit_offset']).ngroups}")

    # Dedup
    KEY = ["ticker","event_date","event_type","entry_offset","exit_offset"]
    before = len(out)
    out = (out.sort_values("entry_straddle_mid", ascending=False)
              .drop_duplicates(subset=KEY, keep="first")
              .reset_index(drop=True))
    if before != len(out):
        out.to_csv(OUTPUT_FILE, index=False)
        print(f"  Dedup: {before:,} → {len(out):,} "
              f"(removed {before-len(out):,})")

    # Performance by event_type
    print(f"\n  Avg return by event type:")
    print(out.groupby("event_type").agg(
        n       =("pnl_pct","count"),
        avg_ret =("pnl_pct","mean"),
        win_rate=("pnl_pct", lambda x: (x>0).mean()),
    ).round(4).to_string())

    # Performance by ticker
    print(f"\n  Avg return by ticker:")
    print(out.groupby("ticker").agg(
        n       =("pnl_pct","count"),
        avg_ret =("pnl_pct","mean"),
        win_rate=("pnl_pct", lambda x: (x>0).mean()),
    ).round(4).sort_values("avg_ret", ascending=False).to_string())

    # Performance by event_type × ticker
    print(f"\n  Avg return by event type × ticker:")
    print(out.groupby(["event_type","ticker"]).agg(
        n       =("pnl_pct","count"),
        avg_ret =("pnl_pct","mean"),
        win_rate=("pnl_pct", lambda x: (x>0).mean()),
    ).round(4).sort_values("avg_ret", ascending=False).to_string())


