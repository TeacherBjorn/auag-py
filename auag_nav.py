# auag_nav.py
import requests
import time

INVESTED_AMOUNT_NOK = 0

HOLDINGS = {
    "CDE": ("Coeur Mining", 0.08),
    "AG": ("First Majestic Silver", 0.08),
    "HL": ("Hecla Mining", 0.08),
    "PAAS": ("Pan American Silver", 0.08),

    "AYA.TO": ("Aya Gold & Silver", 0.04),
    "DSV.TO": ("Discovery Silver", 0.04),
    "EXK": ("Endeavour Silver", 0.04),
    "HOC.L": ("Hochschild Mining", 0.04),
    "FRES.L": ("Fresnillo", 0.04),
    "KGH.WA": ("KGHM", 0.04),
    "MUX": ("McEwen Mining", 0.04),
    "OR": ("OR Royalties", 0.04),
    "SVM": ("Silvercorp Metals", 0.04),
    "WPM": ("Wheaton Precious Metals", 0.04),
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}


def get_close_change_percent(ticker: str) -> float | None:
    url = (
        f"https://query1.finance.yahoo.com/v8/finance/chart/"
        f"{ticker}?range=2d&interval=1d"
    )

    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()

        data = r.json()
        result = data.get("chart", {}).get("result")

        if not result:
            return None

        closes = result[0]["indicators"]["quote"][0]["close"]

        if not closes or len(closes) < 2:
            return None

        yesterday, today = closes[-2], closes[-1]
        return ((today - yesterday) / yesterday) * 100

    except Exception:
        return None


def main():
    print("\nAUAG – estimert NAV (manuell kjøring)\n")

    weighted_sum = 0.0
    weight_sum = 0.0

    for ticker, (name, weight) in HOLDINGS.items():
        change = get_close_change_percent(ticker)

        if change is None:
            print(f"{name:<25} : ingen data")
        else:
            weighted_sum += change * weight
            weight_sum += weight
            sign = "+" if change >= 0 else ""
            print(
                f"{name:<25} : {sign}{change:.2f} %   "
                f"(vekt {int(weight*100)} %)"
            )

        time.sleep(0.5)  # viktig: unngå Yahoo rate-limit

    if weight_sum == 0:
        print("\nKunne ikke beregne NAV-endring.")
        return

    avg_change = weighted_sum / weight_sum
    value_change = INVESTED_AMOUNT_NOK * (avg_change / 100)

    print("\n------------------------------------")
    print(f"Vektet NAV-endring : {avg_change:.4f} %")
    print(f"Verdiendring NOK   : {value_change:,.2f} kr")
    print("------------------------------------\n")


if __name__ == "__main__":
    main()
