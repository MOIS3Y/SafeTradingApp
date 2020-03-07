# resp = {
#   "BTC_USD": [
#     {
#       "order_id": "14",
#       "created": "1435517311",
#       "type": "buy",
#       "pair": "BTC_USD",
#       "price": "100",
#       "quantity": "1",
#       "amount": "100"
#     }
#   ],
#   "ETH_RUB": [
#     {
#       "order_id": "10",
#       "created": "1435517311",
#       "type": "buy",
#       "pair": "BTC_USD",
#       "price": "100",
#       "quantity": "1",
#       "amount": "100"
#     }
#   ],
# }

# result = resp['ETH_RUB']
# print(result)

# for item in result:
#     if item['order_id'] == '10':
#         print('find!')


# class Test(object):
#     def _decorator(foo):
#         def magic(self):
#             print("start magic")
#             foo(self)
#             print("end magic")
#         return magic

#     @_decorator
#     def bar(self):
#         print("normal call")


# if __name__ == "__main__":
#     test = Test()
#     test.bar()


def decorator_function(func):
    def wrapper():
        print('Функция-обёртка!')
        print('Оборачиваемая функция: {}'.format(func))
        print('Выполняем обёрнутую функцию...')
        func()
        print('Выходим из обёртки')
    return wrapper


# @decorator_function
# def hello_world():
#     print('Hello world')

def hello_world():
    print('Hello world')


hello_world = decorator_function(hello_world)

hello_world()
