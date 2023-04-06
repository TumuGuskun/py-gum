from dataclasses import dataclass
import sys
from typing import Any, Callable, TypeVar

from .shell_command import CommandResult, ShellCommand
from .schema import BaseConfig, ChooseConfig, SpinConfig

T = TypeVar("T")


@dataclass
class GumSelection:
    index: int
    selection: Any


def normalize_choices(choice: Any) -> str:
    return str(choice).strip()


def clear_last_line():
    sys.stdout.write("\033[F\033[K")
    sys.stdout.flush()


def gum_confirm(
    message: str = "", timeout: int = 0, default: bool | None = None
) -> bool:
    gum_command = ShellCommand(shell_command=["gum", "confirm"])
    if message:
        gum_command.add_command_args(message)
    if timeout:
        gum_command.add_key_value_arg(key="--timeout", value=f"{timeout}s")
    if default is not None:
        gum_command.add_key_value_arg(key="--default", value=str(default).lower())

    gum_result = gum_command.run(check=False)
    return gum_result.passed


def gum_choose_multiple(
    choices: list[T],
    message: str = "",
    display_function: Callable[[T], str] = normalize_choices,
    choose_config: ChooseConfig | None = None,
) -> list[GumSelection]:
    if message:
        print(message)

    display_choices = [display_function(choice) for choice in choices]

    gum_command = ShellCommand(shell_command=["gum", "choose"])
    gum_command.add_command_args(*display_choices)
    if choose_config:
        kv_args, flags = choose_config.to_kv_args_and_flags()
        gum_command.add_key_value_args(kv_args=kv_args)
        gum_command.add_flags(flags=flags)

    gum_result = gum_command.run()

    if message:
        clear_last_line()

    selections = gum_result.text.split("\n")

    gum_selections = []
    for selection in selections:
        index = display_choices.index(selection)
        choice = choices[index]
        gum_selections.append(GumSelection(index=index, selection=choice))

    return gum_selections


def gum_choose(
    choices: list[T],
    message: str = "",
    display_function: Callable[[T], str] = normalize_choices,
    choose_config: ChooseConfig | None = None,
) -> GumSelection:
    if choose_config is None:
        choose_config = ChooseConfig(limit=1)
    else:
        choose_config.limit = 1

    return gum_choose_multiple(
        choices=choices,
        message=message,
        display_function=display_function,
        choose_config=choose_config,
    )[0]


def gum_input(message: str = "", default: str = "") -> str:
    gum_command = ShellCommand(shell_command=["gum", "input"])
    if message:
        gum_command.add_key_value_arg(key="--prompt", value=f"{message}: ")
    if default:
        gum_command.add_key_value_arg(key="--placeholder", value=default)
    gum_result = gum_command.run()
    return gum_result.text or str(default)


def gum_filter(
    choices: list[T],
    placeholder: str = "",
    display_function: Callable[[T], str] = normalize_choices,
) -> GumSelection:
    gum_command = ShellCommand(shell_command=["gum", "filter"])
    gum_command.add_key_value_arg(key="--limit", value=str(1))
    if placeholder:
        gum_command.add_key_value_arg(key="--placeholder", value=placeholder)

    display_choices = [display_function(choice) for choice in choices]
    joined_choices = "\n".join(display_choices)
    echo_command = ShellCommand(shell_command=["echo", f"{joined_choices}"])
    gum_command.add_input(input_command=echo_command)
    gum_result = gum_command.run()
    choice_index = display_choices.index(gum_result.text)
    return GumSelection(index=choice_index, selection=choices[choice_index])


def gum_style(message: str, style_config: BaseConfig) -> str:
    gum_command = ShellCommand(shell_command=["gum", "style"])
    gum_command.add_command_args(message)

    gum_result = gum_command.run(check=False)
    return gum_result.text


def gum_spin(command_to_spin: ShellCommand, spin_config: SpinConfig) -> CommandResult:
    gum_command = ShellCommand(shell_command=["gum", "spin"])
    kv_args, flags = spin_config.to_kv_args_and_flags()
    gum_command.add_key_value_args(kv_args=kv_args)
    gum_command.add_flags(flags=flags)

    gum_command.add_command_args("--", *command_to_spin.command)

    gum_result = gum_command.run()
    return gum_result
