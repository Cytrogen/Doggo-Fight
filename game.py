"""
file: game.py
author: Cytrogen
"""
import sys
import random
import pygame

from dog import Dog
from infobar import InfoBar
from configs import COLORS, surface, manipulate_json_file


info_bar = InfoBar(
    screen=surface,
    line_height=16,
    xy=(243, 300),
    width=343
)


def start_game(screen) -> None:
    """
    Start the game.
    开始游戏。
    :param screen:
    :return:
    """
    screen.fill(COLORS['white'])


def quit_game() -> None:
    """
    Quit the game.
    退出游戏。
    :return:
    """
    pygame.quit()
    sys.exit()


def adopt_dog(num) -> None:
    """
    Adopt a dog, and add its appearance data to the JSON file.
    领养一只狗，将其样貌数据加入到JSON文件中。
    :param num:
    :return:
    """
    manipulate_json_file('add', {'dog': num})


def create_dog(name) -> None:
    """
    Create a dog, and add its data to the JSON file.
    创建一只狗，并将其数据加入到JSON文件中。
    :param name:
    :return:
    """
    # Create data for the user and the enemy's dog.
    # 为用户和敌人的狗创建数据。
    user_dog = Dog(name).get_stats
    manipulate_json_file('add', user_dog)
    enemy_dog = Dog('ENEMY').get_stats
    enemy_dog['dog'] = random.randint(4, 6)
    manipulate_json_file('add', enemy_dog, False)

    # If the user's dog's speed is greater than the enemy's dog's speed, then the user's dog
    # attacks first.
    # 如果用户的狗的速度大于敌人的狗的速度，则用户的狗先攻击。
    if user_dog['speed'] > enemy_dog['speed']:
        manipulate_json_file('modify', {'turn': True})
    elif user_dog['speed'] < enemy_dog['speed']:
        manipulate_json_file('modify', {'turn': True}, False)
    # If the user's dog's speed is equal to the enemy's dog's speed, then randomly decide who
    # attacks first.
    # 如果用户的狗的速度等于敌人的狗的速度，则随机决定谁先攻击。
    else:
        manipulate_json_file('modify', {'turn': random.choice([True, False])})
        manipulate_json_file('modify', {'turn': not manipulate_json_file('read', None)['turn']},
                             False)


def attack(is_user: bool) -> None:
    """
    Attack the target based on whether it is the user's turn.
    根据是否是用户的回合来决定谁会攻击。
    :param is_user:
    :return:
    """
    user_data = manipulate_json_file('read', None)
    enemy_data = manipulate_json_file('read', None, False)

    # If it is the user's turn, attack the enemy.
    # 如果是用户的回合，则攻击敌人。
    if is_user:
        # Calculate the damage based on the formula used by Pokémon.
        # 根据宝可梦的公式来计算伤害。
        damage = int(round(
            (2 * user_data['level'] + 10) / 250 *
            (user_data['attack'] / enemy_data['defense']) * (user_data['charge_level'] * 5) + 2
        ))

        # Subtract the damage from the enemy's health.
        # 从敌人的生命值中减去伤害。
        enemy_data['current_health_exact'] -= damage

        # Set the user's turn to False, and the enemy's turn to True.
        # 将用户的回合设为False，将敌人的回合设为True。
        manipulate_json_file(
            'modify',
            {
                'turn': False,
                # If the user defended last time, then the user's defense is back to normal
                # after this action.
                # 如果上次行动时防御了，则这次行动后防御值恢复正常。
                'defense': int(user_data['defense'] / 2)
                if user_data['defense'] == user_data['defended_defense']
                else user_data['defense'],
                # If the user's charge level is less than 10 after the attack, then the user's
                # charge level is increased by 1, otherwise the user's charge level is 10.
                # 攻击后如果充能等级小于10，则充能等级加1，否则充能等级为10。
                'charge_level': user_data['charge_level'] + 1 if user_data['charge_level'] < 10
                else 10
            })
        manipulate_json_file(
            'modify',
            {
                'current_health_exact': enemy_data['current_health_exact'],
                'damage': damage,
                # If the enemy's defense is equal to the enemy's defended defense, then the enemy's
                # defense is back to normal.
                # 如果敌人的防御值等于敌人防御后的防御值，则敌人的防御值恢复正常。
                'defense': int(enemy_data['defense'] / 2)
                if enemy_data['defense'] == enemy_data['defended_defense']
                else enemy_data['defense'],
                'turn': True
            },
            False
        )

        info_bar.add_message(f'{user_data["name"]} choose to attack.')
        info_bar.add_message(f'{enemy_data["name"]} took {damage} damage.')

    else:
        damage = int(round(
            (2 * enemy_data['level'] + 10) / 250 *
            (enemy_data['attack'] / user_data['defense']) * (enemy_data['charge_level'] * 5) + 2
        ))
        user_data['current_health_exact'] -= damage

        # Set the enemy's turn to False, and the user's turn to True.
        # 将敌人的回合设为False，将用户的回合设为True。
        manipulate_json_file(
            'modify',
            {
                'turn': False,
                # If the enemy defended last time, then the enemy's defense is back to normal
                # after this action.
                # 如果敌人上次行动时防御了，则这次行动后防御值恢复正常。
                'defense': int(enemy_data['defense'] / 2)
                if enemy_data['defense'] == enemy_data['defended_defense']
                else enemy_data['defense'],
                # If the enemy's charge level is less than 10 after the attack, then the enemy's
                # charge level is increased by 1, otherwise the enemy's charge level is 10.
                # 攻击后如果充能等级小于10，则充能等级加1，否则充能等级为10。
                'charge_level': enemy_data['charge_level'] + 1 if enemy_data['charge_level'] < 10
                else 10
            },
            False)
        manipulate_json_file(
            'modify',
            {
                'current_health_exact': user_data['current_health_exact'],
                'damage': damage,
                # If the user's defense is equal to the user's defended defense, then the user's
                # defense is back to normal.
                # 如果用户的防御值等于用户防御后的防御值，则用户的防御值恢复正常。
                'defense': int(user_data['defense'] / 2)
                if user_data['defense'] == user_data['defended_defense']
                else user_data['defense'],
                'turn': True,
            }
        )
        info_bar.add_message(f'{enemy_data["name"]} choose to attack.')
        info_bar.add_message(f'{user_data["name"]} took {damage} damage.')


def defend(is_user: bool) -> None:
    """
    Defend the target based on whether it is the user's turn.
    根据是否是用户的回合来决定谁会防御。
    :param is_user:
    :return:
    """
    user_data = manipulate_json_file('read', None)
    enemy_data = manipulate_json_file('read', None, False)

    # If it is the user's turn, then the user's defense is doubled.
    # 如果是用户的回合，则将防御值加倍。
    if is_user:
        manipulate_json_file(
            'modify',
            {
                'defense': user_data['defended_defense'],
                'turn': False,
                'charge_level': user_data['charge_level'] - 1
                if user_data['charge_level'] > 0
                else 0
            }
        )
        manipulate_json_file('modify', {'turn': True}, False)

        info_bar.add_message(f'{user_data["name"]} choose to defend.')

    else:
        manipulate_json_file(
            'modify',
            {
                'defense': enemy_data['defended_defense'],
                'turn': False,
                'charge_level': enemy_data['charge_level'] - 1
                if enemy_data['charge_level'] > 0
                else 0
            },
            False
        )
        manipulate_json_file('modify', {'turn': True})

        info_bar.add_message(f'{enemy_data["name"]} choose to defend.')
