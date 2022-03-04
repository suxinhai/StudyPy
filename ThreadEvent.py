import threading


def do(event):
    print('start')
    event.wait()
    print('execute')


if __name__ == '__main__':
    event_obj = threading.Event()
    for i in range(2):
        t = threading.Thread(target=do, args=(event_obj,))
        t.start()

    event_obj.clear()
    inp = input('输入内容:')
    if inp == '1':
        event_obj.set()
