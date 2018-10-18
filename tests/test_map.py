from app import config
from app.map import Map
from app.utils import resource


def test_map_as_emoji():
    words = resource.words(config.WORD_LIST_NAME)
    map_ = Map.random(words=words)
    assert {
        config.EMOJI_BLUE_HEART,
        config.EMOJI_RED_HEART,
        config.EMOJI_GREEN_HEART,
        config.EMOJI_BLACK_HEART
    } == {
        cell.emoji
        for row in map_.cells
        for cell in row
    }


def test_map_as_keyboard():
    words = resource.words(config.WORD_LIST_NAME)
    map_ = Map.random(words=words)
    kb = map_.as_keyboard()
    assert all(
        button['color'] == config.BUTTON_COLOR_DEFAULT
        for buttons in kb['buttons']
        for button in buttons
    )

    cell = map_.cells[0][0]
    cell.flip()

    kb = map_.as_keyboard()
    assert any(
        button['color'] == cell.button_color
        for buttons in kb['buttons']
        for button in buttons
    )
