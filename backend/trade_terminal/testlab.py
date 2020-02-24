resp = {
  "BTC_USD": [
    {
      "order_id": "14",
      "created": "1435517311",
      "type": "buy",
      "pair": "BTC_USD",
      "price": "100",
      "quantity": "1",
      "amount": "100"
    }
  ],
  "ETH_RUB": [
    {
      "order_id": "10",
      "created": "1435517311",
      "type": "buy",
      "pair": "BTC_USD",
      "price": "100",
      "quantity": "1",
      "amount": "100"
    }
  ],
}

result = resp['ETH_RUB']
print(result)

for item in result:
    if item['order_id'] == '10':
        print('find!')
