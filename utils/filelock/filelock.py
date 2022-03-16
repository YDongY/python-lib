import os
import errno
import time


class FileLockException(Exception):
    pass


class FileLock:
    """
    基于上下文管理器的文件锁定机制
    """

    def __init__(self, file_name, timeout=10, delay=0.05):
        """
        实例化文件锁
        :param file_name: 被锁定的文件名
        :param timeout: 超时时间
        :param delay:  延时
        """
        if timeout is not None and delay is None:
            raise ValueError("If timeout is not None, then delay must not be None.")
        self.is_locked = False
        self.lockfile = os.path.join(os.getcwd(), "%s.lock" % file_name)
        self.file_name = file_name
        self.timeout = timeout
        self.delay = delay
        self.fd = None

    def acquire(self):
        """
        尝试获取锁，如果锁在使用中，则每隔 `delay` 秒检查一次，超过 `timeout` 的秒数，会抛出一个异常。
        """
        start_time = time.time()
        while not self.is_locked:
            try:
                self.fd = os.open(self.lockfile, os.O_CREAT | os.O_EXCL | os.O_RDWR)
                self.is_locked = True
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
                if self.timeout is None:
                    raise FileLockException("Could not acquire lock on {}".format(self.file_name))
                if (time.time() - start_time) >= self.timeout:
                    raise FileLockException("Timeout occurred.")
                time.sleep(self.delay)

    def release(self):
        """
        通过删除锁定文件来解除锁定
        """
        if self.is_locked:
            os.close(self.fd)
            os.unlink(self.lockfile)
            self.is_locked = False

    def __enter__(self):
        if not self.is_locked:
            self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.is_locked:
            self.release()

    def __del__(self):
        """
        确保 FileLock 实例不会留下 lockfile
        """
        self.release()
