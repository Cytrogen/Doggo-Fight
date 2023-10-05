"""
file: menu.py
author: Cytrogen
"""
import pygame

from configs import COLORS, manipulate_json_file
from ascii_art import draw_dog, draw_title, draw_health_bar, draw_charge_bar, draw_damage


class Menu:
    """
    A class to represent a menu.
    一个代表菜单的类。

    ...

    Attributes
    ----------
    draw_menu : function
        The function to draw the menu.
        绘制菜单的函数。
    buttons : list
        The buttons in the menu.
        菜单中的按钮。
    input_box : InputBox
        The input box in the menu.
        菜单中的输入框。

    Methods
    -------
    draw(screen)
        Draw the specified menu.
        绘制指定的菜单。
    add_button(button)
        Add a button to the menu.
        将按钮添加到菜单中。
    """
    def __init__(self, draw_menu, input_box=None, info_bar=None):
        self.draw_menu = draw_menu
        self.buttons = []
        self.input_box = input_box
        self.info_bar = info_bar

    def draw(self, screen) -> None:
        """
        Draw the specified menu.
        绘制指定的菜单。
        :param screen:
        :return:
        """
        screen.fill(COLORS['white'])
        self.draw_menu(screen)

        if len(self.buttons) != 0:
            for button in self.buttons:
                button.draw(screen)

        if self.input_box is not None:
            self.input_box.draw(screen)

        if self.info_bar is not None:
            self.info_bar.draw()

        pygame.display.flip()

    def add_button(self, button) -> None:
        """
        Add a button to the menu.
        将按钮添加到菜单中。
        :param button:
        :return:
        """
        self.buttons.append(button)


def draw_main_menu(screen) -> None:
    """
    Draws the main menu.
    绘制主菜单。
    :param screen:
    :return:
    """
    draw_title(screen, 'DOGGO FIGHT', 48, 'title', 'center')
    draw_dog(screen, 350, 200, 0, 20)


def draw_adopt_dog_menu(screen) -> None:
    """
    Draws the dog adoption menu.
    绘制领养狗的菜单。
    :param screen:
    :return:
    """
    draw_title(screen, 'ADOPT YOUR DOG', 36, (300, 50), 'center')
    draw_title(screen, 'WHICH DOG?', 20, (300, 100), 'center')
    draw_dog(screen, 40, 125, 1, 20)
    draw_dog(screen, 230, 125, 2, 20)
    draw_dog(screen, 375, 125, 3, 20)


def draw_name_dog_menu(screen) -> None:
    """
    Draws the dog naming menu.
    绘制取名菜单。
    :param screen:
    :return:
    """
    draw_title(screen, r"WHAT IS YOUR DOG'S NAME?", 36, 'title', 'center')
    user_data = manipulate_json_file('read', None)
    draw_dog(screen, 50, 150, user_data['dog'], 20)


def draw_display_dog_menu(screen) -> None:
    """
    Draws the dog display menu.
    绘制展示狗的菜单。
    :param screen:
    :return:
    """
    draw_title(screen, "THIS IS YOUR DOG!", 36, (300, 50), 'center')
    user_data = manipulate_json_file('read', None)
    draw_dog(screen, 50, 125, user_data['dog'], 20)

    draw_title(screen, f"NAME: {user_data['name']}", 24, (400, 125), 'center')
    draw_title(screen, f"ATTACK: {user_data['attack']}", 24, (400, 175), 'center')
    draw_title(screen, f"DEFENSE: {user_data['defense']}", 24, (400, 225), 'center')
    draw_title(screen, f"SPEED: {user_data['speed']}", 24, (400, 275), 'center')


def draw_battle_menu(screen) -> None:
    """
    Draws the battle menu.
    绘制对战菜单。
    :param screen:
    :return:
    """
    user_data = manipulate_json_file('read', None)
    enemy_data = manipulate_json_file('read', None, False)

    draw_title(screen, r'VS', 60, (300, 45), 'center')

    # Draw the user's dog's information.
    # 绘制用户的狗的信息。
    draw_title(screen, user_data['name'], 24, (38, 10), 'left')
    draw_health_bar(screen, user_data['current_health'], user_data['max_health'], (35, 35), True)
    draw_charge_bar(screen, user_data['charge_level'], (35, 70), True)
    # If the user's dog's health is less than 0, then do not draw the user's dog.
    # 如果用户的狗的生命值小于0，则不绘制用户的狗。
    if user_data['current_health_exact'] > 0:
        draw_dog(screen, 40, 105, user_data['dog'], 20)

    # Draw the enemy's dog's information.
    # 绘制敌人的狗的信息。
    draw_title(screen, enemy_data['name'], 24, (562, 10), 'right')
    draw_health_bar(screen, enemy_data['current_health'], enemy_data['max_health'],
                    (360, 35), False)
    draw_charge_bar(screen, enemy_data['charge_level'], (446, 70), False)
    # If the enemy's dog's health is less than 0, then do not draw the enemy's dog.
    # 如果敌人的狗的生命值小于0，则不绘制敌人的狗。
    if enemy_data['current_health_exact'] > 0:
        draw_dog(screen, 420, 105, enemy_data['dog'], 20)

    # Draw the user's dog's health bar slowly decreasing when the user's dog is damaged.
    # 逐一绘制用户的狗受伤时慢慢减少的生命值。
    if user_data['current_health'] != user_data['current_health_exact'] \
            and user_data['current_health'] > 0:
        draw_damage(screen, user_data['damage'], (200, 125))
        manipulate_json_file('modify', {'current_health': user_data['current_health'] - 1})

    # Draw the enemy's dog's health bar slowly decreasing when the enemy's dog is damaged.
    # 逐一绘制敌人的狗受伤时慢慢减少的生命值。
    if enemy_data['current_health'] != enemy_data['current_health_exact'] \
            and enemy_data['current_health'] > 0:
        draw_damage(screen, enemy_data['damage'], (360, 125))
        manipulate_json_file('modify', {'current_health': enemy_data['current_health'] - 1}, False)
