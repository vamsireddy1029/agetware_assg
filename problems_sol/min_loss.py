def minimize_loss(prices):
    min_loss = float('inf')
    buy_year = sell_year = -1
    for i in range(len(prices)):
        for j in range(i+1, len(prices)):
            if prices[j] < prices[i]:
                loss = prices[i] - prices[j]
                if loss < min_loss:
                    min_loss = loss
                    buy_year = i + 1
                    sell_year = j + 1
    if buy_year == -1:
        return "No valid loss possible"
    return f"Buy in year: {buy_year}, sell in year: {sell_year}, min_loss: {min_loss}"
n = int(input("Enter no.of.years: "))
prices = list(map(int, input().split()))
print(minimize_loss(prices))
