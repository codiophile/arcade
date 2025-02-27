from dataclasses import dataclass
from typing import Optional, Dict, Union

import arcade
from arcade import Texture, Color
from arcade.gui.nine_patch import NinePatchTexture
from arcade.gui.property import bind, DictProperty
from arcade.gui.style import UIStyleBase, UIStyledWidget
from arcade.gui.widgets import UIInteractiveWidget, Surface
from arcade.gui.widgets.text import UITextWidget
from arcade.text import FontNameOrNames


class UITextureButton(UIInteractiveWidget, UIStyledWidget, UITextWidget):
    """
    A button with an image for the face of the button.

    :param float x: x coordinate of bottom left
    :param float y: y coordinate of bottom left
    :param float width: width of widget. Defaults to texture width if not specified.
    :param float height: height of widget. Defaults to texture height if not specified.
    :param Texture texture: texture to display for the widget.
    :param Texture texture_hovered: different texture to display if mouse is hovering over button.
    :param Texture texture_pressed: different texture to display if mouse button is pressed while hovering over button.
    :param str text: text to add to the button.
    :param style: style information for the button.
    :param float scale: scale the button, based on the base texture size.
    :param size_hint: Tuple of floats (0.0-1.0), how much space of the parent should be requested
    :param size_hint_min: min width and height in pixel
    :param size_hint_max: max width and height in pixel
    """

    _textures: Dict[str, Union[Texture, NinePatchTexture]] = DictProperty()  # type: ignore

    @dataclass
    class UIStyle(UIStyleBase):
        font_size: int = 12
        font_name: FontNameOrNames = ("calibri", "arial")
        font_color: Color = arcade.color.WHITE
        border_width: int = 2

    DEFAULT_STYLE = {
        "normal": UIStyle(),
        "hover": UIStyle(
            font_size=12,
            font_name=("calibri", "arial"),
            font_color=arcade.color.WHITE,
            border_width=2,
        ),
        "press": UIStyle(
            font_size=12,
            font_name=("calibri", "arial"),
            font_color=arcade.color.BLACK,
            border_width=2,
        ),
        "disabled": UIStyle(
            font_size=12,
            font_name=("calibri", "arial"),
            font_color=arcade.color.WHITE,
            border_width=2,
        )
    }

    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        width: Optional[float] = None,
        height: Optional[float] = None,
        texture: Union[None, Texture, NinePatchTexture] = None,
        texture_hovered: Union[None, Texture, NinePatchTexture] = None,
        texture_pressed: Union[None, Texture, NinePatchTexture] = None,
        texture_disabled: Union[None, Texture, NinePatchTexture] = None,
        text: str = "",
        scale: Optional[float] = None,
        style: Optional[Dict[str, UIStyleBase]] = None,
        size_hint=None,
        size_hint_min=None,
        size_hint_max=None,
        **kwargs,
    ):

        if width is None and texture is not None:
            width = texture.size[0]

        if height is None and texture is not None:
            height = texture.size[1]

        if scale is not None and texture is not None:
            width = texture.size[0] * scale
            height = texture.size[1] * scale

        super().__init__(
            x=x,
            y=y,
            width=width,
            height=height,
            style=style or self.DEFAULT_STYLE,
            size_hint=size_hint,
            size_hint_min=size_hint_min,
            size_hint_max=size_hint_max,
            text=text,
            **kwargs,
        )

        self._textures = {}

        if texture:
            self._textures["normal"] = texture
            self._textures["hover"] = texture
            self._textures["press"] = texture
            self._textures["disabled"] = texture
        if texture_hovered:
            self._textures["hover"] = texture_hovered
        if texture_pressed:
            self._textures["press"] = texture_pressed
        if texture_disabled:
            self._textures["disabled"] = texture_disabled

        bind(self, "_textures", self.trigger_render)

    def get_current_state(self) -> str:
        if self.disabled:
            return "disabled"
        elif self.pressed:
            return "press"
        elif self.hovered:
            return "hover"
        else:
            return "normal"

    @property
    def texture(self):
        return self._textures["normal"]

    @texture.setter
    def texture(self, value: Texture):
        self._textures["normal"] = value
        self.trigger_render()

    @property
    def texture_hovered(self):
        return self._textures["hover"]

    @texture_hovered.setter
    def texture_hovered(self, value: Texture):
        self._textures["hover"] = value
        self.trigger_render()

    @property
    def texture_pressed(self):
        return self._textures["press"]

    @texture_pressed.setter
    def texture_pressed(self, value: Texture):
        self._textures["press"] = value
        self.trigger_render()

    def do_render(self, surface: Surface):
        self.prepare_render(surface)

        style = self.get_current_style()

        # update label
        self.apply_style(style)

        current_state = self.get_current_state()
        current_texture = self._textures.get(current_state)
        if current_texture:
            surface.draw_texture(0, 0, self.width, self.height, current_texture)

    def apply_style(self, style: UIStyleBase):
        """
        Callback which is called right before rendering to apply changes for rendering.
        """
        font_name = style.get("font_name")
        font_size = style.get("font_size")
        font_color = style.get("font_color")

        self._label.layout.begin_update()
        self._label.layout.font_name = font_name
        self._label.layout.font_size = font_size
        self._label.layout.color = font_color


class UIFlatButton(UIInteractiveWidget, UIStyledWidget, UITextWidget):
    """
    A text button, with support for background color and a border.

    :param float x: x coordinate of bottom left
    :param float y: y coordinate of bottom left
    :param float width: width of widget. Defaults to texture width if not specified.
    :param float height: height of widget. Defaults to texture height if not specified.
    :param str text: text to add to the button.
    :param style: Used to style the button

    """

    @dataclass
    class UIStyle(UIStyleBase):
        font_size: int = 12
        font_name: FontNameOrNames = ("calibri", "arial")
        font_color: Color = arcade.color.WHITE
        bg: Color = (21, 19, 21)
        border: Optional[Color] = None
        border_width: int = 0

    DEFAULT_STYLE = {
        "normal": UIStyle(),
        "hover": UIStyle(
            font_size=12,
            font_name=("calibri", "arial"),
            font_color=arcade.color.WHITE,
            bg=(21, 19, 21),
            border=(77, 81, 87),
            border_width=2,
        ),
        "press": UIStyle(
            font_size=12,
            font_name=("calibri", "arial"),
            font_color=arcade.color.BLACK,
            bg=arcade.color.WHITE,
            border=arcade.color.WHITE,
            border_width=2,
        ),
        "disabled": UIStyle(
            font_size=12,
            font_name=("calibri", "arial"),
            font_color=arcade.color.WHITE,
            bg=arcade.color.GRAY,
            border=None,
            border_width=2,
        )
    }

    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        width: float = 100,
        height: float = 50,
        text="",
        size_hint=None,
        size_hint_min=None,
        size_hint_max=None,
        style=None,
        **kwargs,
    ):
        super().__init__(
            x=x,
            y=y,
            width=width,
            height=height,
            size_hint=size_hint,
            size_hint_min=size_hint_min,
            size_hint_max=size_hint_max,
            style=style or self.DEFAULT_STYLE,
            text=text,
            **kwargs
        )

        self.add(self._label)

    def get_current_state(self) -> str:
        if self.disabled:
            return "disabled"
        elif self.pressed:
            return "press"
        elif self.hovered:
            return "hover"
        else:
            return "normal"

    def do_render(self, surface: Surface):
        self.prepare_render(surface)
        style = self.get_current_style()

        # update label
        self.apply_style(style)

        # Render button
        border_width = style.get("border_width")
        border_color = style.get("border")
        bg_color = style.get("bg")
        if bg_color:
            surface.clear(bg_color)

        # render button border (which is not the widgets border)
        if border_color and border_width:
            arcade.draw_xywh_rectangle_outline(
                border_width,
                border_width,
                self.content_width - 2 * border_width,
                self.content_height - 2 * border_width,
                color=border_color,
                border_width=border_width,
            )

    def apply_style(self, style: UIStyleBase):
        """
        Callback which is called right before rendering to apply changes for rendering.
        """
        font_name = style.get("font_name")
        font_size = style.get("font_size")
        font_color = style.get("font_color")

        self._label.layout.begin_update()
        self._label.layout.font_name = font_name
        self._label.layout.font_size = font_size
        self._label.layout.color = font_color
