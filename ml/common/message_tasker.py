"""
# ml.common.message_tasker.py

@author: Jason Zhu
@email: jason_zhuyx@hotmail.com
@created: 2019-01-30

"""
import logging

from ml.config import get_uint
from ml.utils.logger import get_logger

DEBUG_LEVEL = get_uint('debug.level', logging.INFO)
LOGGER = get_logger(__name__, level=DEBUG_LEVEL)

LEVEL_LIMIT = get_uint('tasks.max_nested_level', 3)


class MessageTasker():
    """
    MessageTasker processes a task list.
    """
    def __init__(self, tasks, message={}, max_level=LEVEL_LIMIT):
        """
        Constructor of ml.common.MessageTasker

        @param tasks: a list of tasks with recursive multi-layer sub-tasks that
                      describes a tasks workflow.
        @param message: pre-processed message (dict).
        @param max_level: the maximum nested sub-tasks level.
        @notes:
          * example of tasks list:

            ```
            [{
                "_name": "task_1",
                "_func": __function_task_1__,
                "tasks": []
            }, {
                "_name": "task_2",
                "_func": __function_task_2__,
                "tasks": [{
                    "_name": "task_2.1",
                    "_func": __function_task_2_1__,
                }, {
                    "_name": "task_2.2",
                    "_func": __function_task_2_2__,
                }]
            }]
            ```
          * nested sub-tasks level is up to self.max_level
          * each task function should implement the same interface:

            ```
            def __func__(message, **kwargs):
                '''
                Implement a MessageTasker task function.
                :param message: processed message (dict).
                :param kwargs: data returned from previous process.
                :return: processed data passing to next task.
                :note:
                  - should always return not-None dictionary.
                  - passing kwargs if no processed data.
                '''
            ```
        """
        self.tasks = tasks or {}
        self.message = message or {}
        self._max_level = LEVEL_LIMIT if max_level < 0 or max_level > LEVEL_LIMIT else max_level
        self._run_level = -1
        self._done = False
        pass

    def _run_task(self, task, **kwargs):
        """
        Start specific task to process message.
        """
        _data = kwargs
        _func = task.get('_func')
        _name = task.get('_name', '__unnamed__')
        _desc = task.get('_desc', '')

        if _func:
            log_prefix = '{}- [{}]'.format('-' * self._run_level, self._run_level)
            log = 'starting task: {} - {}'.format(_name, _desc)
            LOGGER.debug('%s %s', log_prefix, log)
            LOGGER.debug(
                '%s running task [%s]: %s - message: \n%s',
                log_prefix, _func.__name__, _data, self.message)  # noqa
            _new_data = _func(self.message, **_data)
            _data.update(_new_data or {})
            LOGGER.debug('%s updated data: %s', log_prefix, _data)
            log = 'done task [{}]: {}'.format(_name, self.message)
            LOGGER.debug('%s %s', log_prefix, log)

        _next_tasks = task.get('tasks', [])

        if _next_tasks:
            if self._run_level >= self._max_level:
                err = 'cannot start sub-tasks beyond maximum nested level'
                msg = '{}: {}'.format(err, self._max_level)
                LOGGER.warning(
                    '%s* [%s] %s', '*'*self._run_level, self._run_level, msg)
                return _data

            log = 'starting sub-tasks for task: {}'.format(_name)
            LOGGER.debug('%s- [%s] %s', '-' * self._run_level, self._run_level, log)
            # passing _data to sub-tasks
            _new_data = self._run_tasks(_next_tasks, **_data)
            # updating _data from sub-tasks
            _data.update(_new_data or {})

        # passing updated _data to next task
        return _data

    def _run_tasks(self, tasks, **kwargs):
        """
        Start a sub tasks list workflow to process message.
        """
        data = kwargs
        self._run_level += 1

        # LOGGER.debug(
        #     '[%s] processing message: %s\n- with kwargs: %s',
        #     self._run_level, self.message, kwargs)  # noqa
        for task in tasks:
            _new_data = self._run_task(task, **data)
            # updating data for next task
            data.update(_new_data or {})

        self._run_level -= 1
        return data

    def start(self, message={}, **kwargs):
        """
        Start whole task workflow to process message.
        @param message: the original message to start with.
        @param kwargs: optional initial data to read from.
        """
        if message and isinstance(message, dict):
            self.message = message  # overwrite and start with new message
            self._done = False
        if isinstance(self.message, dict) and not self._done:
            self._run_tasks(self.tasks, **kwargs)

        self._done = True  # prevent from processing the message again
        # returning processed message
        return self.message
