# Doggo-Fight

English | [简体中文](doc/README_CN.md)

## Description

> You are a Doggo trainer, and you have to fight against other Doggo trainers. 
> 
> You have to choose your only one Doggo from the three starter Doggos.
> 
> Battle with other Doggo trainers! And become the best Doggo trainer in the world!

Doggo-Fight is my final project of the course CS50P. It is a game that you can choose your Doggo and fight with other Doggo trainers.

<details>
<summary>CS50P Final Project Specification</summary>

- Your project must be implemented in Python.
- Your project must have a `main` function and three or more additional functions. At least three of those additional functions must be accompanied by tests that can be executed with `pytest`.
  - Your `main` function must be in a file called `project.py`, which should be in the “root” (i.e., top-level folder) of your project.
  - Your 3 required custom functions other than `main` must also be in `project.py` and defined at the same indentation level as `main` (i.e., not nested under any classes or functions).
  - Your test functions must be in a file called `test_project.py`, which should also be in the “root” of your project. Be sure they have the same name as your custom functions, prepended with `test_` (`test_custom_function`, for example, where `custom_function` is a function you’ve implemented in `project.py`).
  - You are welcome to implement additional classes and functions as you see fit beyond the minimum requirement.
- Implementing your project should entail more time and effort than is required by each of the course’s problem sets.
- Any `pip`-installable libraries that your project requires must be listed, one per line, in a file called `requirements.txt` in the root of your project.
</details>

Video Demo: [Click me](https://youtu.be/NxKk9IK_pZM)

### How to play

1. Choose your dog
2. Name your dog
3. The dog with higher speed will act first
4. Choose your action: attack or defend? Your choice!
5. Repeat the process until one of the dog is defeated

#### More

- Every time a dog attacks, its charge level will increase by 1
- Every time a dog defends, its charge level will decrease by 1
- The charge level of a dog will affect the damage it deals
- One dog can have at most 10 charge level
- When a dog defends, its defense value will double, until it attacks again

## Development

### Requirements

- Python 3.10+
  - This is because I used the `match` statement in the code. It is adjustable since this statement only occurs a few time and can be replaced by `if-elif-else` statement.
- Pygame 2.5.2
  - The version is not tested. This is the version I used to develop this game.

### TODO

- [ ] Add more Doggos
- [ ] Rewrite the battle system
- [ ] Rewrite the logic of displaying damage
