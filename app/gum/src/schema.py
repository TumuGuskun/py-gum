from dataclasses import dataclass, field, fields, asdict
from functools import partial
from typing import Optional


TUPLE_FIELDS = ["margin", "padding"]
FLAG_FIELDS = ["bold", "faint", "italic", "underline", "strikethrough", "no_limit"]


@dataclass(kw_only=True)
class BaseTextOptions:
    border_background: Optional[str] = None  # Border Background Color
    border_foreground: Optional[str] = None  # Border Foreground Color
    border: Optional[str] = None  # Border Style
    background: str = ""  # Background Color
    foreground: str = ""  # Foreground Color
    align: str = "left"  # Text Alignment
    bold: bool = False  # Bold text
    faint: bool = False  # Faint text
    italic: bool = False  # Italicize text
    underline: bool = False  # Underline text
    strikethrough: bool = False  # Strikethrough text
    height: Optional[int] = None  # Text height
    width: Optional[int] = None  # Text width
    margin: list[int] = [0, 0]  # Text margin
    padding: list[int] = [0, 0]  # Text padding


@dataclass(kw_only=True)
class ItemOptions(BaseTextOptions):
    def to_kv_args_and_flags(self) -> tuple[dict, list]:
        all_fields = asdict(self)
        for field in fields(self):
            if all_fields[field.name] == field.default:
                all_fields.pop(field.name)

        kv_args = {}
        flags = []
        for key, value in all_fields.items():
            if key in TUPLE_FIELDS:
                kv_args[f"--item.{key}"] = f'"{" ".join(value)}"'
            elif key in FLAG_FIELDS:
                flags.append(f"--item.{key}")
            else:
                kv_args[f"--item.{key}"] = value

        return kv_args, flags


@dataclass(kw_only=True)
class CursorOptions(BaseTextOptions):
    prefix: str = "[•] "  # Prefix to show on the cursor item (hidden if limit is 1)
    foreground: str = "212"  # Foreground color
    cursor: str = "> "  # Prefix to show on item that corresponds to the cursor position

    def to_kv_args_and_flags(self) -> tuple[dict, list]:
        all_fields = asdict(self)
        for field in fields(self):
            if all_fields[field.name] == field.default:
                all_fields.pop(field.name)

        kv_args = {}
        flags = []
        for key, value in all_fields.items():
            if key == "prefix":
                kv_args["--cursor-prefix"] = value
            elif key == "cursor":
                kv_args["--cursor"] = value
            elif key in TUPLE_FIELDS:
                kv_args[f"--cursor.{key}"] = f'"{" ".join(value)}"'
            elif key in FLAG_FIELDS:
                flags.append(f"--cursor.{key}")
            else:
                kv_args[f"--cursor.{key}"] = value

        return kv_args, flags


@dataclass(kw_only=True)
class SelectedOptions(BaseTextOptions):
    selected_prefix: str = (
        "[x] "  # Prefix to show on selected items (hidden if limit is 1)
    )
    unselected_prefix: str = "[ ] "
    selected: list[str] = field(default_factory=list)

    def to_kv_args_and_flags(self) -> tuple[dict, list]:
        all_fields = asdict(self)
        for field in fields(self):
            if all_fields[field.name] == field.default:
                all_fields.pop(field.name)

        kv_args = {}
        flags = []
        for key, value in all_fields.items():
            if key == "selected_prefix":
                kv_args["--selected-prefix"] = value
            elif key == "unselected_prefix":
                kv_args["--unselected-prefix"] = value
            elif key == "selected":
                kv_args["--selected"] = ",".join(value)
            elif key in TUPLE_FIELDS:
                kv_args[f"--selected.{key}"] = f'"{" ".join(value)}"'
            elif key in FLAG_FIELDS:
                flags.append(f"--selected.{key}")
            else:
                kv_args[f"--selected.{key}"] = value

        return kv_args, flags

@dataclass
class UnselectedOptions(BaseException):
    
    


@dataclass(kw_only=True)
class PromptOptions(BaseTextOptions):
    margin: list[int] = [1, 0, 0, 0]

    def to_kv_args_and_flags(self) -> tuple[dict, list]:
        all_fields = asdict(self)
        for field in fields(self):
            if all_fields[field.name] == field.default:
                all_fields.pop(field.name)

        kv_args = {}
        flags = []
        for key, value in all_fields.items():
            if key in TUPLE_FIELDS:
                kv_args[f"--prompt.{key}"] = f'"{" ".join(value)}"'
            elif key in FLAG_FIELDS:
                flags.append(f"--prompt.{key}")
            else:
                kv_args[f"--prompt.{key}"] = value

        return kv_args, flags


# Top level Commands


@dataclass(kw_only=True)
class ChooseOptions:
    cursor: CursorOptions = field(default_factory=partial(CursorOptions, prefix="○ "))
    item: ItemOptions = field(default_factory=ItemOptions)
    selected: SelectedOptions = field(
        default_factory=partial(SelectedOptions, selected_prefix="◉ ")
    )
    height: int = 10  # Height of the list
    limit: int = 1  # Maximum number of options to pick
    no_limit: bool = False  # Pick an unlimited number of options (ignores limit)

    def to_kv_args_and_flags(self) -> tuple[dict, list]:
        all_fields = asdict(self)
        for field in fields(self):
            if all_fields[field.name] == field.default:
                all_fields.pop(field.name)

        kv_args = {}
        flags = []
        for key, value in all_fields.items():
            if key in TUPLE_FIELDS:
                kv_args[f"--prompt.{key}"] = f'"{" ".join(value)}"'
            elif key in FLAG_FIELDS:
                flags.append(f"--prompt.{key}")
            else:
                kv_args[f"--prompt.{key}"] = value

        return kv_args, flags


@dataclass(kw_only=True)
class ConfirmOptions:
    affirmative: str = "Yes"
    default: str = "Yes"
    negative: str = "No"
    prompt: PromptOptions = field(default_factory=PromptOptions)
    selected: SelectedOptions = field(
        default_factory=partial(SelectedOptions, margin=[1, 1], padding=[0, 3])
    )
