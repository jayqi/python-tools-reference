from enum import StrEnum
from pathlib import Path
import tomllib
import textwrap
from typing import Annotated

from jinja2 import Environment, FileSystemLoader, select_autoescape
import minify_html
from pydantic import BaseModel, AfterValidator
from pydantic.networks import HttpUrl

env = Environment(loader=FileSystemLoader("templates"), autoescape=select_autoescape())

template = env.get_template("index.html.jinja")


def unwrap(text: str):
    return textwrap.dedent(text.strip()).replace("\n", " ")


LongStr = Annotated[str, AfterValidator(unwrap)]


class Meta(BaseModel):
    site_url: str


class FunctionalityInfo(BaseModel):
    name: str
    description: LongStr


class IconEnum(StrEnum):
    DEFAULT = "default"
    PYTHON = "python"
    CONDA = "conda"


class ToolFunctionalityInfo(BaseModel):
    explanation: LongStr
    reference: HttpUrl
    icon: IconEnum = IconEnum.DEFAULT


if __name__ == "__main__":
    with Path("data.toml").open("rb") as fp:
        data = tomllib.load(fp)

    meta = Meta.model_validate(data["meta"])

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
        website: HttpUrl
        functionalities: dict[FunctionalitiesEnum, list[ToolFunctionalityInfo]]

    tools = [ToolInfo.model_validate(item) for item in data["tools"]]
    print(functionalities)
    print(tools)
    with Path("site/index.html").open("w") as fp:
        rendered = template.render(meta=meta, functionalities=functionalities, tools=tools)
        minified = minify_html.minify(
            rendered, minify_js=True, remove_processing_instructions=True
        )
        fp.write(minified)
