from catnames import config, wordlist
from catnames.map import Map
from catnames.cells import BlueCell, RedCell, NeutralCell


def test_map_as_emoji():
    words = wordlist.load(config.DEFAULT_WORDLIST_NAME)
    map_ = Map.random(words)
    assert {
        config.EMOJI_BLUE_HEART,
        config.EMOJI_RED_HEART,
        config.EMOJI_GREEN_HEART,
        config.EMOJI_BLACK_HEART,
    } == {cell.emoji for row in map_.cells for cell in row}


def test_map_as_keyboard():
    b0 = BlueCell("b0")
    b1 = BlueCell("b1")
    n0 = NeutralCell("n0")
    r0 = RedCell("r0")
    cells = [[b0, b1], [n0, r0]]
    map_ = Map(cells)

    assert map_.as_keyboard().buttons == [["b0", "b1"], ["n0", "r0"]]

    b1.flip()
    assert map_.as_keyboard().buttons == [["b0", config.EMOJI_BLUE_HEART], ["n0", "r0"]]

    n0.flip()
    assert map_.as_keyboard().buttons == [
        ["b0", config.EMOJI_BLUE_HEART],
        [config.EMOJI_GREEN_HEART, "r0"],
    ]


def test_all_flipped():
    b0 = BlueCell("b0")
    b1 = BlueCell("b1")
    n0 = NeutralCell("r0")
    r0 = RedCell("r1")
    cells = [[b0, b1], [n0, r0]]
    map_ = Map(cells)
    assert not map_.all_flipped(BlueCell)
    assert not map_.all_flipped(RedCell)
    assert not map_.all_flipped(NeutralCell)

    b0.flip()
    assert b0.flipped
    assert not map_.all_flipped(BlueCell)
    assert not map_.all_flipped(RedCell)
    assert not map_.all_flipped(NeutralCell)

    n0.flip()
    assert n0.flipped
    assert not map_.all_flipped(BlueCell)
    assert not map_.all_flipped(RedCell)
    assert map_.all_flipped(NeutralCell)

    b1.flip()
    assert b1.flipped
    assert map_.all_flipped(BlueCell)
    assert not map_.all_flipped(RedCell)
    assert map_.all_flipped(NeutralCell)

    r0.flip()
    assert r0.flipped
    assert map_.all_flipped(BlueCell)
    assert map_.all_flipped(RedCell)
    assert map_.all_flipped(NeutralCell)
