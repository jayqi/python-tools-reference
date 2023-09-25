from enum import StrEnum
from pathlib import Path
import tomllib

from jinja2 import Environment, FileSystemLoader, select_autoescape
from pydantic import BaseModel

env = Environment(loader=FileSystemLoader("templates"), autoescape=select_autoescape())

template = env.get_template("index.html.jinja")


class FunctionalityInfo(BaseModel):
    name: str
    description: str


class IconEnum(StrEnum):
    DEFAULT = "default"
    PYTHON = "python"
    CONDA = "conda"


class ToolFunctionalityInfo(BaseModel):
    explanation: str
    reference: str
    icon: IconEnum = IconEnum.DEFAULT


if __name__ == "__main__":
    with Path("data.toml").open("rb") as fp:
        data = tomllib.load(fp)

    FunctionalitiesEnum = StrEnum(
        "FunctionalitiesEnum", {k.upper(): k for k in data["functionalities"].keys()}
    )

    functionalities = {
        FunctionalitiesEnum(key): FunctionalityInfo.model_validate(value)
        for key, value in data["functionalities"].items()
    }

    class ToolInfo(BaseModel):
        name: str
        description: str
        functionalities: dict[FunctionalitiesEnum, list[ToolFunctionalityInfo]]

    tools = [ToolInfo.model_validate(item) for item in data["tools"]]
    print(functionalities)
    print(tools)
    with Path("site/index.html").open("w") as fp:
        fp.write(template.render(functionalities=functionalities, tools=tools))
