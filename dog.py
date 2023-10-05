"""
File: dog.py
Author: Cytrogen
"""
import random


class Dog:
    """
    A class to represent the basic information of a dog.

    ...

    Attributes
    ----------
    name : str
        The name of the dog.
        狗的名字。
    is_user : bool
        Whether the dog is the user's dog.
        狗是否是用户的狗。
    strength : list
        The strength of the dog, from left to right, are HP, attack, defense and speed.
        狗的个体值，从左到右分别是HP、攻击、防御和速度。
    level : int
        The level of the dog.
        狗的等级。
    characteristics : list
        The characteristics of the dog, from left to right, are HP, attack, defense and speed.
        狗的个性值，从左到右分别是HP、攻击、防御和速度。
    base_points : list
        The base points of the dog, from left to right, are HP, attack, defense and speed.
        狗的基础点数, 从左到右分别是HP、攻击、防御和速度。
    stats : list
        The stats of the dog, from left to right, are HP, attack, defense, speed and charge level.
        狗的能力值，从左到右分别是HP、攻击、防御、速度和充能等级。

    Methods
    -------
    generate_stats()
        Generate the stats of a dog.
        生成一只狗的能力值。

    calculate_stat(stat)
        Calculate the stat of a dog based on the index of the stat.
        基于能力值的下标计算能力值。

    calculate_health
        Calculate the health of a dog based on the formula used by most games after the
        third generation of the Pokémon series.
        基于宝可梦系列第三世代之后的大部分游戏所采用的公式来计算一只狗的HP能力值。
    """
    def __init__(self, name: str):
        self.name = name

        self.strength = [100, 50, 50, 100]
        self.level = 50
        self.characteristics = [random.randint(0, 30) for _ in range(4)]
        self.base_points = generate_base_points()

        self.stats = self.generate_stats()

    def generate_stats(self):
        """
        Generate the stats of a dog: the first one is HP, the next three are attack,
        defense and speed, and the last one is charge level.
        生成一只狗的能力值：第一个是HP，后面三个是攻击、防御和速度，最后是充能等级。
        :return:
        """
        stats = [self.calculate_health]
        for i in range(3):
            stats.append(self.calculate_stat(i))
        stats.append(0)
        return stats

    def calculate_stat(self, stat):
        """
        Calculate the stat of a dog based on the index of the stat.
        基于能力值的下标计算能力值。
        :param stat:
        :return:
        """
        return int(round((
            self.strength[stat] + self.characteristics[stat] + self.base_points[stat] / 4
        ) * self.level / 100 + 5))

    @property
    def calculate_health(self):
        """
        Calculate the health of a dog based on the formula used by most games after the third
        generation of the Pokémon series.
        基于宝可梦系列第三世代之后的大部分游戏所采用的公式来计算一只狗的HP能力值。
        :return:
        """
        return int(round((
                self.strength[0] * 2 + self.characteristics[0] + self.base_points[0] / 4
        ) * self.level / 100 + self.level + 10))

    @property
    def get_stats(self) -> dict:
        """
        Get the stats of a dog.
        获取一只狗的能力值。
        :return:
        """
        return {
            'name': self.name,
            'level': self.level,
            'current_health': self.stats[0],
            'current_health_exact': self.stats[0],
            'max_health': self.stats[0],
            'damaged': 0,
            'attack': self.stats[1],
            'defense': self.stats[2],
            'defended_defense': self.stats[2] * 2,
            'speed': self.stats[3],
            'charge_level': self.stats[4],
            'turn': False
        }


def generate_base_points():
    """
    Generate the base points of a dog.
    生成一只狗的基础点数。
    :return:
    """
    total = 0
    base_points = []

    for _ in range(4):
        max_allowed = 510 - total
        if max_allowed <= 0:
            break

        number = random.randint(0, min(255, max_allowed))
        base_points.append(number)
        total += number
    return base_points
