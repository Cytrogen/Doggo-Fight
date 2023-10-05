import pytest


def test_manipulate_json_file():
    from project import data_init
    from configs import manipulate_json_file

    data_init()
    assert manipulate_json_file('read', None, True) == {}
    manipulate_json_file('add', {'current_health': 100})
    assert manipulate_json_file('read', None, True) == {'current_health': 100}
    manipulate_json_file('modify', {'current_health': 50})
    assert manipulate_json_file('read', None, True) == {'current_health': 50}


def test_generate_base_points():
    from dog import generate_base_points

    base_points = generate_base_points()
    assert len(base_points) == 4
    assert sum(base_points) <= 510


def test_dog():
    from dog import Dog

    dog_test = Dog('test')
    assert dog_test.name == 'test'


def test_info_bar():
    from infobar import InfoBar

    info_bar = InfoBar(None, 0, (0, 0), 0)
    assert info_bar.messages == []
    info_bar.add_message('test')
    assert info_bar.messages == ['test']


def test_menu():
    from menu import Menu

    menu = Menu(None)

    assert menu.buttons == []
    menu.add_button(None)
    assert menu.buttons == [None]
