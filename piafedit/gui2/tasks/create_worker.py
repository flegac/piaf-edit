import random
import time
from logging import Logger

from piafedit.gui2.tasks.worker import Task, Worker


def create_worker():
    def task(i: int) -> Task:
        if i % 4 == 1:
            def work(logger: Logger):
                logger.debug('test logger')
                time.sleep(random.randint(500, 1000) / 1000)
                raise ValueError(i)

            return work

        def work(logger: Logger):
            logger.info('test logger -----------')

            time.sleep(random.randint(500, 1000) / 1000)
            res = f'work-{i}'
            return res

        return work

    return Worker(*[task(i) for i in range(10)])
