def enumerate_fn_odd(lit):
    '''enumerate函数：获取每个元素的索引和值
     可以返回索引和值  even number 是偶数 odd number 是奇数'''
    for index, value in enumerate(lit):
        if index % 2 == 0:
            yield (value)
        else:
            pass



a = ["a","b",'c']


t =enumerate_fn_odd(a)
