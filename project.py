"""
File: project.py
Author: Cytrogen
"""
import os
import sys
import random
from functools import partial

import pygame

from button import Button
from input_box import InputBox
from game import info_bar, start_game, quit_game, adopt_dog, create_dog, attack, defend
from menu import (
    Menu, draw_title, draw_main_menu, draw_adopt_dog_menu,
    draw_name_dog_menu, draw_battle_menu, draw_display_dog_menu
)
from configs import COLORS, surface, manipulate_json_file


def data_init() -> None:
    """
    Initialize pygame.
    初始化pygame。
    :return:
    """
    if not os.path.exists('data'):
        os.mkdir('data')

    # Create JSON files for the user's and enemy's dogs.
    # 创建用户和敌人的狗的JSON文件。
    json_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/dog.json')
    with open(json_file_path, 'w', encoding='UTF-8') as file:
        file.write('{}')

    json_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/enemy.json')
    with open(json_file_path, 'w', encoding='UTF-8') as file:
        file.write('{}')


def create_menu(draw_menu_func, input_box=None, infobar=None):
    """
    Create a menu.
    创建菜单。
    :param draw_menu_func:
    :param input_box:
    :param infobar:
    :return:
    """
    return Menu(
        draw_menu=draw_menu_func,
        input_box=input_box,
        info_bar=infobar
    )


def create_button(x, y, width, height, text, action, next_menu=None):
    """
    Create a button.
    创建按钮。
    :param x:
    :param y:
    :param width:
    :param height:
    :param text:
    :param action:
    :param next_menu:
    :return:
    """
    return Button(
        x=x, y=y,
        width=width, height=height,
        text=text,
        text_color=COLORS['white'],
        button_color=COLORS['black'],
        action=action,
        next_menu=next_menu
    )


def create_menus():
    """
    Create menus.
    创建菜单。
    :return:
    """
    battle_menu = create_menu(draw_battle_menu, infobar=info_bar)
    battle_menu.add_button(
        create_button(
            x=20, y=315,
            width=100, height=50,
            text='ATTACK',
            action=lambda: attack(True)
        )
    )
    battle_menu.add_button(
        create_button(
            x=130, y=315,
            width=100, height=50,
            text='DEFEND',
            action=lambda: defend(True)
        )
    )

    display_dog_menu = create_menu(draw_display_dog_menu)
    display_dog_menu.add_button(
        create_button(
            x=420, y=315,
            width=150, height=50,
            text='GO BATTLE!',
            action=start_game,
            next_menu=battle_menu
        )
    )

    name_dog_menu = create_menu(draw_name_dog_menu, input_box=InputBox())
    name_dog_menu.add_button(
        create_button(
            x=350, y=260,
            width=100, height=40,
            text='NAME!',
            action=lambda: create_dog(name_dog_menu.input_box.text),
            next_menu=display_dog_menu
        )
    )

    adopt_dog_menu = create_menu(draw_adopt_dog_menu)
    button_positions = [(55, 310), (240, 310), (425, 310)]
    for i, position in enumerate(button_positions, start=1):
        adopt_dog_menu.add_button(
            create_button(
                x=position[0], y=position[1],
                width=100, height=40,
                text='ADOPT',
                action=partial(adopt_dog, i),
                next_menu=name_dog_menu
            )
        )

    main_menu = create_menu(draw_main_menu)
    main_menu.add_button(
        create_button(
            x=75, y=180,
            width=200, height=50,
            text='ADOPT YOUR DOG',
            action=start_game,
            next_menu=adopt_dog_menu
        )
    )
    main_menu.add_button(
        create_button(
            x=75, y=255,
            width=200, height=50,
            text='GET OUT',
            action=quit_game
        )
    )

    return main_menu


def handle_input_box_event(menu, event) -> None:
    """
    Handle the input box's event.
    处理输入框的事件。
    :param menu:
    :param event:
    :return:
    """
    if menu.input_box is not None:
        menu.input_box.handle_event(event)


def handle_battle_event(menu, event) -> None:
    user_data = manipulate_json_file('read', None)
    enemy_data = manipulate_json_file('read', None, False)

    # If it is the user's turn, allow the user to click the buttons.
    # 如果是用户的回合，那么允许用户点击按钮。
    if user_data['turn']:
        # Since this is a loop, we need to make sure that the last message in
        # the message list is not the message we want to add.
        # 鉴于这是一个循环，所以需要确保消息列表的最后一条消息不是我们想要添加的消息。
        if len(info_bar.messages) == 0 or \
                info_bar.messages[-1] != f"{user_data['name']}'s turn!":
            info_bar.add_message(f"{user_data['name']}'s turn!")

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in menu.buttons:
                if button.rect.collidepoint(event.pos):
                    button.click(screen=surface)
                    break

    # If it is the enemy's turn, allow the enemy to randomly choose to attack or defend
    # within 3 seconds.
    # 如果是敌人的回合，那么敌人会随机选择攻击或防御。
    else:
        if len(info_bar.messages) == 0 \
                or info_bar.messages[-1] != f"{enemy_data['name']}'s turn!":
            info_bar.add_message(f"{enemy_data['name']}'s turn!")

        action_to_execute = random.choice([attack, defend])
        action_to_execute(False)


def handle_menu_buttons_event(menu, event) -> None:
    """
    Handle the buttons' event.
    处理按钮的事件。
    :param menu:
    :param event:
    :return:
    """
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        for button in menu.buttons:
            if button.rect.collidepoint(event.pos):
                button.click(screen=surface)

                # If the button has a next menu, change the current menu。
                # 如果按钮有下一个菜单，则更改当前菜单。
                if button.next_menu is not None:
                    menu.draw_menu = button.next_menu.draw_menu
                    menu.buttons = button.next_menu.buttons
                    menu.input_box = button.next_menu.input_box
                    menu.info_bar = button.next_menu.info_bar


def check_game_over() -> None:
    """
    Check if the game is over.
    检查游戏是否结束。
    :return:
    """
    try:
        if manipulate_json_file('read', None)['current_health'] <= 0:
            surface.fill(COLORS['white'])
            draw_title(surface, 'YOU LOSE!', 100, 'center', 'center')
            pygame.display.flip()
            pygame.time.delay(5000)
            quit_game()

        if manipulate_json_file('read', None, False)['current_health'] <= 0:
            surface.fill(COLORS['white'])
            draw_title(surface, 'YOU WIN!', 100, 'center', 'center')
            pygame.display.flip()
            pygame.time.delay(5000)
            quit_game()
    except KeyError:
        pass


def main():
    """
    The main function.
    主函数。
    :return:
    """
    data_init()
    main_menu = create_menus()
    current_menu = main_menu

    while True:
        # Loop through the event list.
        # 遍历事件列表。
        for event in pygame.event.get():
            # If the user clicks the "X" button, quit the game.
            # 如果用户点击了“X”按钮，那么退出游戏。
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if current_menu.input_box is not None:
                handle_input_box_event(current_menu, event)

            if current_menu.info_bar is not None:
                handle_battle_event(current_menu, event)
            else:
                handle_menu_buttons_event(current_menu, event)

        # Draw the current menu.
        # 绘制当前菜单。
        current_menu.draw(surface)
        check_game_over()


if __name__ == '__main__':
    main()
