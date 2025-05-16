import os
import sys
from multiprocessing import Process
from pathlib import Path
from typing import Any

from pygame.time import Clock
import pytest

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(BASE_DIR))

# Hide the pygame screen
os.environ['SDL_VIDEODRIVER'] = 'dummy'

TIMEOUT_ASSERT_MSG = (
    'Проект работает некорректно, проверка прервана.\n'
    'Вероятные причины ошибки:\n'
    '1. Исполняемый код (например, вызов функции `main()`) оказался в '
    'глобальной зоне видимости. Как исправить: вызов функции `main` поместите '
    'внутрь конструкции `if __name__ == "__main__":`.\n'
    '2. В цикле `while True` внутри функции `main` отсутствует вызов метода '
    '`tick` объекта `clock`. Не изменяйте прекод в этой части.'
)


def import_the_snake():
    """Импортирует модуль `the_snake` для проверки возможности его импорта."""
    import the_snake  # noqa


@pytest.fixture(scope='session')
def snake_import_test():
    """Проверяет, что модуль `the_snake` импортируется без зависаний."""
    check_import_process = Process(target=import_the_snake)
    check_import_process.start()
    pid = check_import_process.pid
    check_import_process.join(timeout=1)
    if check_import_process.is_alive():
        os.kill(pid, 9)
        raise AssertionError(TIMEOUT_ASSERT_MSG)


@pytest.fixture(scope='session')
def _the_snake(snake_import_test):
    """Импортирует модуль `the_snake` и проверяет наличие основных классов."""
    try:
        import the_snake
    except ImportError as error:
        raise AssertionError(
            'При импорте модуль `the_snake` произошла ошибка:\n'
            f'{type(error).__name__}: {error}'
        )
    for class_name in ('GameObject', 'Snake', 'Apple'):
        assert hasattr(the_snake, class_name), (
            'Убедитесь, что в модуле `the_snake` '
            f'определен класс `{class_name}`.'
        )
    return the_snake


def write_timeout_reasons(text, stream=None):
    """Выводит причины возможных ошибок при таймауте тестов."""
    if stream is None:
        stream = sys.stderr
    text = TIMEOUT_ASSERT_MSG
    stream.write(text)


def _create_game_object(class_name, module):
    """Создаёт экземпляр класса с именем `class_name` из модуля `module`.

    Проверяет, что конструктор класса корректно вызывается без обязательных
    параметров, кроме `self`.
    """
    try:
        return getattr(module, class_name)()
    except TypeError as error:
        raise AssertionError(
            f'При создании объекта класса `{class_name}` произошла ошибка:\n'
            f'`{type(error).__name__}: {error}`\n'
            f'Если в конструктор класса `{class_name}` помимо параметра '
            '`self` передаются какие-то ещё параметры - убедитесь, что для '
            'них установлены значения по умолчанию. Например:\n'
            '`def __init__(self, <параметр>=<значение_по_умолчанию>):`'
        )


class StopInfiniteLoop(Exception):
    """Исключение для прерывания бесконечного цикла в тестах."""

    pass


def loop_breaker_decorator(func):
    """Декоратор, который прерывает функцию после второго вызова.

    Используется для предотвращения бесконечных циклов в тестах.
    """
    call_counter = 0

    def wrapper(*args, **kwargs):
        nonlocal call_counter
        call_counter += 1
        if call_counter > 1:
            raise StopInfiniteLoop
        return func(*args, **kwargs)
    return wrapper


@pytest.fixture
def modified_clock(_the_snake):
    """Заменяет объект clock в модуле `the_snake` на модифицированную версию.

    В новой версии метод tick вызывает оригинальный tick, но бросает исключение
    после второго вызова для предотвращения бесконечного цикла.
    """
    class _Clock:
        def __init__(self, clock_obj: Clock) -> None:
            self.clock = clock_obj

        @loop_breaker_decorator
        def tick(self, *args, **kwargs):
            return self.clock.tick(*args, **kwargs)

        def __getattribute__(self, name: str) -> Any:
            if name in ['tick', 'clock']:
                return super().__getattribute__(name)
            return self.clock.__getattribute__(name)

    original_clock = _the_snake.clock
    modified_clock_obj = _Clock(original_clock)
    _the_snake.clock = modified_clock_obj
    yield
    _the_snake.clock = original_clock
