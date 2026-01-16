from typing import Any, Literal, TypedDict

from typing_extensions import NotRequired


DarkGray = Literal["#333333"]
iTaKOrange = Literal["#FF5A50"]
Gray = Literal["#666666"]
White = Literal["#FFFFFF"]
Black = Literal["#000000"]


DARK_GRAY: Literal["#333333"] = "#333333"
iTaK_ORANGE: Literal["#FF5A50"] = "#FF5A50"
GRAY: Literal["#666666"] = "#666666"
WHITE: Literal["#FFFFFF"] = "#FFFFFF"
BLACK: Literal["#000000"] = "#000000"


class FlowColors(TypedDict):
    bg: White
    start: iTaKOrange
    method: DarkGray
    router: DarkGray
    router_border: iTaKOrange
    edge: Gray
    router_edge: iTaKOrange
    text: White


class FontStyles(TypedDict, total=False):
    color: DarkGray | iTaKOrange | Gray | White | Black
    multi: Literal["html"]


class StartNodeStyle(TypedDict):
    color: iTaKOrange
    shape: Literal["box"]
    font: FontStyles
    label: NotRequired[str]
    margin: dict[str, int]


class MethodNodeStyle(TypedDict):
    color: DarkGray
    shape: Literal["box"]
    font: FontStyles
    label: NotRequired[str]
    margin: dict[str, int]


class RouterNodeStyle(TypedDict):
    color: dict[str, Any]
    shape: Literal["box"]
    font: FontStyles
    label: NotRequired[str]
    borderWidth: int
    borderWidthSelected: int
    shapeProperties: dict[str, list[int] | bool]
    margin: dict[str, int]


class CrewNodeStyle(TypedDict):
    color: dict[str, iTaKOrange | White]
    shape: Literal["box"]
    font: FontStyles
    label: NotRequired[str]
    borderWidth: int
    borderWidthSelected: int
    shapeProperties: dict[str, bool]
    margin: dict[str, int]


class NodeStyles(TypedDict):
    start: StartNodeStyle
    method: MethodNodeStyle
    router: RouterNodeStyle
    crew: CrewNodeStyle


COLORS: FlowColors = {
    "bg": WHITE,
    "start": iTaK_ORANGE,
    "method": DARK_GRAY,
    "router": DARK_GRAY,
    "router_border": iTaK_ORANGE,
    "edge": GRAY,
    "router_edge": iTaK_ORANGE,
    "text": WHITE,
}

NODE_STYLES: NodeStyles = {
    "start": {
        "color": iTaK_ORANGE,
        "shape": "box",
        "font": {"color": WHITE},
        "margin": {"top": 10, "bottom": 8, "left": 10, "right": 10},
    },
    "method": {
        "color": DARK_GRAY,
        "shape": "box",
        "font": {"color": WHITE},
        "margin": {"top": 10, "bottom": 8, "left": 10, "right": 10},
    },
    "router": {
        "color": {
            "background": DARK_GRAY,
            "border": iTaK_ORANGE,
            "highlight": {
                "border": iTaK_ORANGE,
                "background": DARK_GRAY,
            },
        },
        "shape": "box",
        "font": {"color": WHITE},
        "borderWidth": 3,
        "borderWidthSelected": 4,
        "shapeProperties": {"borderDashes": [5, 5]},
        "margin": {"top": 10, "bottom": 8, "left": 10, "right": 10},
    },
    "crew": {
        "color": {
            "background": WHITE,
            "border": iTaK_ORANGE,
        },
        "shape": "box",
        "font": {"color": BLACK},
        "borderWidth": 3,
        "borderWidthSelected": 4,
        "shapeProperties": {"borderDashes": False},
        "margin": {"top": 10, "bottom": 8, "left": 10, "right": 10},
    },
}
