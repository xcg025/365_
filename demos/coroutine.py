from collections import deque
import time
import asyncio
import threading

# def printer():
#     counter = 0
#     while True:
#         print('printer is running')
#         # time.sleep(100)
#         string = (yield )
#         print('[{}] {}'.format(counter, string))
#         counter += 1
#
# if __name__ == '__main__':
#     p = printer()
#     next(p)
#     # next(p)
#     # next(p)
#     p.send('Hi')
#     p.send('My name is andrew')
#     p.send('Bye!')

# class Runner(object):
#     def __init__(self, tasks):
#         self.tasks = deque(tasks)
#     def next(self):
#         return self.tasks.pop()
#     def run(self):
#         while len(self.tasks):
#             print(len(self.tasks))
#             task = self.next()
#             try:
#                 next(task)
#             except StopIteration:
#                 pass
#             else:
#                 # print('what is now')
#                 self.tasks.appendleft(task)
#
# def task(name, times):
#     for i in range(times):
#         yield
#         print(name, i)
#
# Runner([task('zhangsan',5), task('lisi', 4), task('wangwu',6)]).run()

# @asyncio.coroutine
# def hello():
#     print('hello world')
#     r = yield from asyncio.sleep(10)
#     print('hello again')
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(hello())
# loop.close()

# @asyncio.coroutine
# def hello():
#     print('Hello world! {}'.format(threading.currentThread()))
#     yield from asyncio.sleep(10)
#     print('Hello world! {}'.format(threading.currentThread()))
#
# loop = asyncio.get_event_loop()
# tasks = [hello(), hello()]
# loop.run_until_complete(asyncio.wait(tasks))
# loop.close()

# import time
#
# now = lambda : time.time()
# async def do_some_work(x):
#     print('Waiting: ', x)
#
# start = now()
# coroutine = do_some_work(2)
# loop = asyncio.get_event_loop()
# loop.run_until_complete(coroutine)
# print('TIME: ', now() - start)

# now = lambda: time.time()
#
#
# async def do_some_work(x):
#     print('Waiting: ', x)
#     return 'Done after {}s'.format(x)
#
#
# def callback(future):
#     print('Callback: ', future.result())
#
#
# start = now()
#
# coroutine = do_some_work(2)
# loop = asyncio.get_event_loop()
# task = asyncio.ensure_future(coroutine)
# task.add_done_callback(callback)
# loop.run_until_complete(task)
#
# print('TIME: ', now() - start)

now = lambda: time.time()


async def do_some_work(x):
    print('Waiting: ', x)

    await asyncio.sleep(x)
    return 'Done after {}s'.format(x)


start = now()

coroutine1 = do_some_work(1)
coroutine2 = do_some_work(2)
coroutine3 = do_some_work(4)

tasks = [
    asyncio.ensure_future(coroutine1),
    asyncio.ensure_future(coroutine2),
    asyncio.ensure_future(coroutine3)
]

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))

for task in tasks:
    print('Task ret: ', task.result())

print('TIME: ', now() - start)


