from monsters import MonsterHunter, MonsterBerserk


class Hero:
    # Базовый класс, который не подлежит изменению
    # У каждого наследника будут атрибуты:
    # - Имя
    # - Здоровье
    # - Сила
    # - Жив ли объект
    # Каждый наследник будет уметь:
    # - Атаковать
    # - Получать урон
    # - Выбирать действие для выполнения
    # - Описывать своё состояние

    max_hp = 150
    start_power = 10

    def __init__(self, name):
        self.name = name
        self.__hp = self.max_hp
        self.__power = self.start_power
        self.__is_alive = True

    def get_hp(self):
        return self.__hp

    def set_hp(self, new_value):
        self.__hp = max(new_value, 0)

    def get_power(self):
        return self.__power

    def set_power(self, new_power):
        self.__power = new_power

    def is_alive(self):
        return self.__is_alive

    # Все наследники должны будут переопределять каждый метод базового класса (кроме геттеров/сеттеров)
    # Переопределенные методы должны вызывать методы базового класса (при помощи super).
    # Методы attack и __str__ базового класса можно не вызывать (т.к. в них нет кода).
    # Они нужны исключительно для наглядности.
    # Метод make_a_move базового класса могут вызывать только герои, не монстры.
    def attack(self, target):
        # Каждый наследник будет наносить урон согласно правилам своего класса
        raise NotImplementedError("Вы забыли переопределить метод Attack!")

    def take_damage(self, damage):
        # Каждый наследник будет получать урон согласно правилам своего класса
        # При этом у всех наследников есть общая логика, которая определяет жив ли объект.
        print("\t", self.name, "Получил удар с силой равной = ", round(damage), ". Осталось здоровья - ",
              round(self.get_hp()))
        # Дополнительные принты помогут вам внимательнее следить за боем и изменять стратегию,
        # чтобы улучшить выживаемость героев
        if self.get_hp() <= 0:
            self.__is_alive = False

    def make_a_move(self, friends, enemies):
        # С каждым днём герои становятся всё сильнее.
        self.set_power(self.get_power() + 0.1)

    def __str__(self):
        # Каждый наследник должен выводить информацию о своём состоянии, чтобы вы могли отслеживать ход сражения
        raise NotImplementedError("Вы забыли переопределить метод __str__!")


class Healer(Hero):
    # Целитель:
    # Атрибуты:
    # - магическая сила
    # Методы:
    # - атака
    # - получение урона
    # - исцеление
    # - выбор действия

    def __init__(self, name):
        # - магическая сила - равна значению НАЧАЛЬНОГО показателя силы умноженному на 3 (self.__power * 3)
        super().__init__(name)
        self.__magic = self.start_power * 3

    def get_magic(self):
        # геттер показателя магической силы __magic
        return self.__magic

    def attack(self, target):
        # - атака - может атаковать врага, но атакует только в половину силы self.__power
        target.take_damage(self.get_power() / 2)

    def take_damage(self, power):
        # - получение урона - т.к. защита целителя слаба - он получает на 20% больше урона (1.2 * damage)
        damage = 1.2 * power
        self.set_hp(self.get_hp() - damage)
        super().take_damage(damage)

    def healing(self, target):
        # - исцеление - увеличивает здоровье цели на величину равную своей магической силе
        target_hp = target.get_hp() + self.get_magic()
        target.set_hp(target_hp)
        print('Исцеляю {target} на {magic} HP\nЗдоровье {target}: {hp}'.format(
            target=target.name,
            magic=self.get_magic(),
            hp=target_hp
        ))

    def make_a_move(self, friends, enemies):
        super().make_a_move(friends, enemies)
        # - выбор действия - получает на вход всех союзников и всех врагов
        # и на основе своей стратегии выполняет ОДНО из действий (атака,
        # исцеление) на выбранную им цель
        print(self.name, end=' ')
        sorted_friends_hp = sorted(friends, key=Hero.get_hp)
        target_of_heal = sorted_friends_hp[0]

        if target_of_heal.get_hp() < 100:
            self.healing(target_of_heal)
        else:
            if not enemies:
                return

            range_enemies = [enemy for enemy in enemies if isinstance(enemy, MonsterHunter)]
            if range_enemies:
                print("Атакую ближнего охотника -", range_enemies[0].name)
                self.attack(range_enemies[0])
            else:
                print("Атакую ближнего -", enemies[0].name)
                self.attack(enemies[0])
        print('\n')

    def __str__(self):
        status = 'Жив!' if self.is_alive() else 'Мертв!'

        return '{name} | HP: {hp} | Сила: {power} | Магия: {magic} - {is_alive}'.format(
            name=self.name,
            hp=self.get_hp(),
            power=self.get_power(),
            magic=self.__magic,
            is_alive=status
        )


class Tank(Hero):
    # Танк:
    # Атрибуты:
    # - показатель защиты
    # - поднят ли щит
    # Методы:
    # - атака
    # - получение урона
    # - поднять щит
    # - опустить щит
    # - выбор действия

    def __init__(self, name):
        # - показатель защиты - изначально равен 1, может увеличиваться и уменьшаться
        # - поднят ли щит - танк может поднимать щит, этот атрибут должен показывать поднят ли щит в данный момент
        super().__init__(name)
        self.__defense = 1
        self.is_shield_up = False

    def get_defense(self):
        # геттер показателя защиты __defense
        return self.__defense

    def set_defense(self, protection):
        # сеттер показателя защиты __defense
        self.__defense = protection

    def attack(self, target):
        # - атака - атакует, но т.к. доспехи очень тяжелые - наносит половину урона (self.__power)
        target.take_damage(self.get_power() / 2)

    def take_damage(self, power):
        # - получение урона - весь входящий урон делится на показатель защиты (power/self.defense)
        # и только потом отнимается от здоровья
        damage = power / self.get_defense()
        self.set_hp(self.get_hp() - damage)
        super().take_damage(damage)

    def shield_up(self):
        # - поднять щит - если щит не поднят - поднимает щит.
        # Это увеличивает показатель брони в 2 раза, но уменьшает показатель силы в 2 раза.
        self.is_shield_up = True
        self.set_defense(self.get_defense() * 2)
        self.set_power(self.get_power() / 2)
        print('Поднимаю щит!\nПоказатель брони: {defense}\nПоказатель силы: {power}'.format(
            defense=self.get_defense(),
            power=self.get_power()
        ))

    def shield_down(self):
        # - опустить щит - если щит поднят - опускает щит.
        # Это уменьшает показатель брони в 2 раза, но увеличивает показатель силы в 2 раза.
        self.is_shield_up = False
        self.set_defense(self.get_defense() / 2)
        self.set_power(self.get_power() * 2)
        print('Опускаю щит!\nПоказатель брони: {defense}\nПоказатель силы: {power}'.format(
            defense=self.get_defense(),
            power=self.get_power()
        ))

    def make_a_move(self, friends, enemies):
        super().make_a_move(friends, enemies)
        # - выбор действия - получает на вход всех союзников и всех врагов
        # и на основе своей стратегии выполняет ОДНО из действий (атака,
        # поднять щит/опустить щит) на выбранную им цель
        print(self.name, end=' ')
        if self.get_hp() < 100 and not self.is_shield_up:
            self.shield_up()
        elif self.get_hp() > 140 and self.is_shield_up:
            self.shield_down()
        else:
            if not enemies:
                return

            range_enemies = [enemy for enemy in enemies if isinstance(enemy, MonsterHunter)]
            if range_enemies:
                print("Атакую ближнего охотника -", range_enemies[0].name)
                self.attack(range_enemies[0])
            else:
                print("Атакую ближнего -", enemies[0].name)
                self.attack(enemies[0])
        print('\n')

    def __str__(self):
        status = 'Жив!' if self.is_alive() else 'Мертв!'
        shield_status = 'Поднят.' if self.is_shield_up else 'Опущен.'

        return '{name} | HP: {hp} | Сила: {power} | Защита: {protection} | Щит: {shield} - {is_alive}'.format(
            name=self.name,
            hp=self.get_hp(),
            power=self.get_power(),
            protection=self.__defense,
            shield=shield_status,
            is_alive=status
        )


class Attacker(Hero):
    # Убийца:
    # Атрибуты:
    # - коэффициент усиления урона (входящего и исходящего)
    # Методы:
    # - атака
    # - получение урона
    # - усиление
    # - ослабление
    # - выбор действия

    def __init__(self, name):
        # - коэффициент усиления урона (входящего и исходящего)
        super().__init__(name)
        self.__power_multiply = 1

    def get_power_multiply(self):
        # геттер коэффициента усиления урона __power_multiply
        return self.__power_multiply

    def set_power_multiply(self, new_multiply):
        # сеттер коэффициента усиления урона __power_multiply
        self.__power_multiply = new_multiply

    def attack(self, target):
        # - атака - наносит урон равный показателю силы (self.__power)
        # умноженному на коэффициент усиления урона (self.__power_multiply)
        # после нанесения урона - вызывается метод ослабления power_down.
        target.take_damage(self.get_power() * self.get_power_multiply())
        self.power_down()

    def take_damage(self, power):
        # - получение урона - получает урон равный входящему урону
        # умноженному на половину коэффициента усиления урона - damage * (
        # self.power_multiply / 2)
        damage = power * (self.get_power_multiply() / 2)
        self.set_hp(self.get_hp() - damage)
        super().take_damage(damage)

    def power_up(self):
        # - усиление - увеличивает коэффициента усиления урона в 2 раза
        self.set_power_multiply(self.get_power_multiply() * 2)
        print('Усиление!\nКоэффициент усиления урона:', self.get_power_multiply())

    def power_down(self):
        # - ослабление (power_down) - уменьшает коэффициент усиления урона в 2 раза
        self.set_power_multiply(self.get_power_multiply() / 2)
        print('Ослабление!\nКоэффициент усиления урона:', self.get_power_multiply())

    def make_a_move(self, friends, enemies):
        super().make_a_move(friends, enemies)
        # - выбор действия - получает на вход всех союзников и всех врагов
        # и на основе своей стратегии выполняет ОДНО из действий (атака,
        # усиление, ослабление) на выбранную им цель
        print(self.name, end=' ')
        if self.get_power_multiply() < 8:
            self.power_up()
        else:
            if not enemies:
                return

            melee_enemies = [enemy for enemy in enemies if isinstance(enemy, MonsterBerserk)]
            if melee_enemies:
                print("Атакую ближнего берсерка -", melee_enemies[0].name)
                self.attack(melee_enemies[0])
            else:
                print("Атакую ближнего охотника -", enemies[0].name)
                self.attack(enemies[0])
        print('\n')

    def __str__(self):
        status = 'Жив!' if self.is_alive() else 'Мертв!'

        return '{name} | HP: {hp} | Сила: {power} | Коэффициент урона: {multiply} - {is_alive}'.format(
            name=self.name,
            hp=self.get_hp(),
            power=self.get_power(),
            multiply=self.__power_multiply,
            is_alive=status
        )
