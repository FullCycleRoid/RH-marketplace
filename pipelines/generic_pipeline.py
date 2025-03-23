from __future__ import annotations

from abc import abstractmethod
from typing import (
    Callable,
    Generator,
    Generic,
    Iterable,
    List,
    Optional,
    Protocol,
    TypeVar,
    Union,
)

from src.core.logger import logger

Context = TypeVar("Context")


def error_handler(error: Exception, context: Context, next_step: NextStep):
    logger.error(f"Error: {error}", exc_info=True)
    context.failed_records += 1


class PipelineError(Exception):
    pass


NextStep = Callable[[Context], Iterable[Union[Exception, Context]]]
ErrorHandler = Callable[[Exception, Context, NextStep], None]


class PipelineStep(Protocol[Context]):
    @abstractmethod
    def __call__(self, context: Context, next_step: NextStep) -> Generator[Context]: ...


def _default_error_handler(
    error: Exception, context: Context, next_step: NextStep
) -> None:
    raise error


class PipelineCursor(Generic[Context]):
    def __init__(self, steps: List[PipelineStep], error_handler: ErrorHandler):
        self.queue = steps
        self.error_handler: ErrorHandler = error_handler

    def __call__(self, context: Context) -> None:
        if not self.queue:
            return

        current_step = self.queue[0]
        next_step = PipelineCursor(self.queue[1:], self.error_handler)

        try:
            print(
                f"========= Start step: {self.step_name(str(current_step))} ========="
            )
            current_step(context, next_step)

        except Exception as error:
            self.error_handler(error, context, next_step)

    @staticmethod
    def step_name(name: str) -> str:
        step_name = str(name).split(".")[-1]
        return str(step_name).split(" ")[0]


class Pipeline(Generic[Context]):
    def __init__(self, *steps: PipelineStep):
        self.queue = [step for step in steps]

    def append(self, step: PipelineStep) -> None:
        self.queue.append(step)

    def __call__(
        self, context: Context, error_handler: Optional[ErrorHandler] = None
    ) -> None:
        execute = PipelineCursor(self.queue, error_handler or _default_error_handler)
        execute(context)

    def __len__(self) -> int:
        return len(self.queue)
