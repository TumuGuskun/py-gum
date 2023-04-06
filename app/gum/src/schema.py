from dataclasses import dataclass
from enum import Enum


class BorderType(Enum):
    NONE = "none"
    HIDDEN = "hidden"
    NORMAL = "normal"
    ROUNDED = "rounded"
    THICK = "thick"
    DOUBLE = "double"


class AlignType(Enum):
    CENTER = "center"
    LEFT = "left"
    TOP = "top"
    BOTTOM = "bottom"
    RIGHT = "right"


class SpinnerType(Enum):
    LINE = "line"
    DOT = "dot"
    MINIDOT = "minidot"
    JUMP = "jump"
    PULSE = "pulse"
    POINTS = "points"
    GLOBE = "globe"
    MOON = "moon"
    MONKEY = "monkey"
    METER = "meter"
    HAMBURGER = "hamburger"


@dataclass
class BaseConfig:
    border_background: int | None = None  # Border Background Color
    border_foreground: int | None = None  # Border Foreground Color
    border: BorderType | None = None  # Border Style
    background: int | None = None  # Background Color
    foreground: int | None = None  # Foreground Color
    align: AlignType | None = None  # Text Alignment
    bold: bool = False  # Bold text
    faint: bool = False  # Faint text
    italic: bool = False  # Italicize text
    underline: bool = False  # Underline text
    strikethrough: bool = False  # Strikethrough text
    height: int | None = None  # Text height
    width: int | None = None  # Text width
    margin: list[int] | None = None  # Text margin
    padding: list[int] | None = None  # Text padding

    def to_kv_args_and_flags(self, prefix: str = "") -> tuple[dict, list]:
        kv_args, flags = {}, []

        # key value args
        if self.border_background:
            kv_args[f"--{prefix}border-background"] = self.border_background
        if self.border_foreground:
            kv_args[f"--{prefix}border-foreground"] = self.border_foreground
        if self.border:
            kv_args[f"--{prefix}border"] = self.border.value
        if self.background:
            kv_args[f"--{prefix}background"] = self.background
        if self.foreground:
            kv_args[f"--{prefix}foreground"] = self.foreground
        if self.align:
            kv_args[f"--{prefix}align"] = self.align.value
        if self.height:
            kv_args[f"--{prefix}height"] = self.height
        if self.width:
            kv_args[f"--{prefix}width"] = self.width
        if self.margin:
            kv_args[f"--{prefix}margin"] = " ".join(
                [str(dimension) for dimension in self.margin]
            )
        if self.padding:
            kv_args[f"--{prefix}padding"] = " ".join(
                [str(dimension) for dimension in self.padding]
            )

        # sentinel flags
        if self.bold:
            flags.append(f"--{prefix}bold")
        if self.faint:
            flags.append(f"--{prefix}faint")
        if self.italic:
            flags.append(f"--{prefix}italic")
        if self.underline:
            flags.append(f"--{prefix}underline")
        if self.strikethrough:
            flags.append(f"--{prefix}strikethrough")

        return kv_args, flags


# Top level Commands


@dataclass
class ChooseConfig:
    # key value args
    cursor_prefix: str | None = None
    height: int | None = None  # Height of the list
    limit: int | None = None  # Maximum number of options to pick
    selected_prefix: str | None = None
    unselected_prefix: str | None = None
    # flags
    no_limit: bool = False  # Pick an unlimited number of options (ignores limit)
    # sub configs
    item_config: BaseConfig | None = None
    cursor_config: BaseConfig | None = None
    selected_config: BaseConfig | None = None

    def to_kv_args_and_flags(self) -> tuple[dict, list]:
        kv_args, flags = {}, []
        # key value args
        if self.cursor_prefix:
            kv_args["--cursor-prefix"] = self.cursor_prefix
        if self.height:
            kv_args["--height"] = self.height
        if self.limit:
            kv_args["--limit"] = self.limit
        if self.selected_prefix:
            kv_args["--selected-prefix"] = self.selected_prefix
        if self.unselected_prefix:
            kv_args["--unselected-prefix"] = self.unselected_prefix

        # flags
        if self.no_limit:
            flags.append("--no-limit")

        # sub configs
        if self.item_config:
            item_kv_args, item_flags = self.item_config.to_kv_args_and_flags(
                prefix="item"
            )
            kv_args.update(item_kv_args)
            flags.extend(item_flags)
        if self.cursor_config:
            cursor_kv_args, cursor_flags = self.cursor_config.to_kv_args_and_flags(
                prefix="cursor"
            )
            kv_args.update(cursor_kv_args)
            flags.extend(cursor_flags)
        if self.selected_config:
            (
                selected_kv_args,
                selected_flags,
            ) = self.selected_config.to_kv_args_and_flags(prefix="selected")
            kv_args.update(selected_kv_args)
            flags.extend(selected_flags)

        return kv_args, flags


@dataclass
class SpinConfig:
    # key value args
    align: AlignType | None = None  # Alignment of spinner with regard to the title
    spinner: SpinnerType | None = None
    title: str | None = None
    # flags
    show_output: bool = False
    # sub configs
    spinner_config: BaseConfig | None = None
    title_config: BaseConfig | None = None

    def to_kv_args_and_flags(self) -> tuple[dict, list]:
        kv_args, flags = {}, []

        # key value args
        if self.align:
            kv_args["--align"] = self.align.value
        if self.spinner:
            kv_args["--spinner"] = self.spinner.value
        if self.title:
            kv_args["--title"] = self.title

        # flags
        if self.show_output:
            flags.append("--show-output")

        # sub configs
        if self.spinner_config:
            spinner_kv_args, spinner_flags = self.spinner_config.to_kv_args_and_flags(
                prefix="spinner"
            )
            kv_args.update(spinner_kv_args)
            flags.extend(spinner_flags)
        if self.title_config:
            title_kv_args, title_flags = self.title_config.to_kv_args_and_flags(
                prefix="title"
            )
            kv_args.update(title_kv_args)
            flags.extend(title_flags)

        return kv_args, flags
