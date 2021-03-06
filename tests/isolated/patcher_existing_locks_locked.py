__test__ = False


def take(lock, sync1, sync2):
    sync2.acquire()
    sync1.release()
    with lock:
        sync2.release()


if __name__ == '__main__':
    import sys
    import threading
    lock = threading.RLock()
    lock.acquire()
    import eventlet
    eventlet.monkey_patch()

    lock.release()
    try:
        lock.release()
    except RuntimeError as e:
        assert e.args == ('cannot release un-acquired lock',)
    lock.acquire()

    sync1 = threading.Lock()
    sync2 = threading.Lock()
    sync1.acquire()
    eventlet.spawn(take, lock, sync1, sync2)
    # Ensure sync2 has been taken
    with sync1:
        pass

    # an RLock should be reentrant
    lock.acquire()
    lock.release()
    lock.release()
    # To acquire sync2, 'take' must have acquired lock, which has been locked
    # until now
    sync2.acquire()

    print('pass')
