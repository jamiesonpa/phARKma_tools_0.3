tickers = []
with open("tickerpossibles.txt") as readfile:
    words = readfile.read().split(" ")
    for word in words:
        if word.isupper():
            if word.find("ETF") == -1:
                if len(word) > 2:
                    if word.find("&") == -1:
                        if len(word) < 6:
                            tickers.append(word)

for ticker in tickers:
    print(ticker)
