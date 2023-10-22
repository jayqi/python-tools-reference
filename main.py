from enum import StrEnum
from pathlib import Path
import re
import tomllib
import textwrap
from typing import Annotated

from jinja2 import Environment, FileSystemLoader, select_autoescape
import markdown
import minify_html_onepass
from pydantic import BaseModel, AfterValidator
from pydantic.networks import HttpUrl

env = Environment(loader=FileSystemLoader("templates"), autoescape=True)

template = env.get_template("index.html.jinja")

nonparagraph_line_break = re.compile(r"(?<!\n)\n(?!\n)")


def unwrap(text: str):
    return nonparagraph_line_break.sub(" ", textwrap.dedent(text).strip())


LongStr = Annotated[str, AfterValidator(unwrap)]


class Meta(BaseModel):
    site_url: str


class Section(BaseModel):
    text: LongStr

    def render_text_as_markdown(self):
        return markdown.markdown(self.text)


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

    sections = {key: Section.model_validate(value) for key, value in data["sections"].items()}

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
        github: str | None = None
        website: HttpUrl
        functionalities: dict[FunctionalitiesEnum, list[ToolFunctionalityInfo]]

    tools = [ToolInfo.model_validate(item) for item in data["tools"]]
    print(functionalities)
    print(tools)
    with Path("site/index.html").open("w") as fp:
        rendered = template.render(
            meta=meta, sections=sections, functionalities=functionalities, tools=tools
        )
        minified = minify_html_onepass.minify(
            rendered,
            minify_css=True,
            minify_js=True,
        )
        fp.write(minified)
