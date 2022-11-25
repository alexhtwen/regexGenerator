import random as r
presenters = ['Spring', 'Oliver', 'MR Wu', '夢梅', '小偵', '振泰', 'Alex']


print(f"\n報告人： {', '.join(presenters)}\n")
print('抽籤順序(每人報告時間15分鐘)：')
shfffle_count = 5
for _ in range(shfffle_count):
    r.shuffle(presenters)

with open('./order_presentations.txt', 'w') as f_order:
    for order, presenter in enumerate(presenters, start=1):
        order_presenter = f'{order}:  {presenter}\n'
        print(order_presenter, end='')
        f_order.write(order_presenter)
