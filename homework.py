from typing import ClassVar
from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Печать результатов тренировки."""
        return (f'Тип тренировки: {self.training_type}; Длительность: '
                f'{self.duration:.3f} ч.; Дистанция: {self.distance:.3f} км;'
                f' Ср. скорость: {self.speed:.3f} км/ч; Потрачено ккал:'
                f' {self.calories:.3f}.')


@dataclass
class Training:
    """Базовый класс тренировки."""

    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000
    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Определите в'
                                  'соответствующем классе тренировки')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type = type(self).__name__
        duration = self.duration
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        info = InfoMessage(training_type, duration, distance, speed, calories)
        return info


@dataclass
class Running(Training):
    """Тренировка: бег."""

    COEFF_CALORIE_1: ClassVar[int] = 18
    COEFF_CALORIE_2: ClassVar[int] = 20
    HOUR: ClassVar[int] = 60

    def get_spent_calories(self):
        speed = self.get_mean_speed()
        calories = ((self.COEFF_CALORIE_1 * speed - self.COEFF_CALORIE_2)
                    * self.weight / self.M_IN_KM * self.duration * self.HOUR)
        return calories


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    HOUR: ClassVar[int] = 60
    DEGREE: ClassVar[int] = 2
    COEFF_WALKING_1: ClassVar[float] = 0.035
    COEFF_WALKING_2: ClassVar[float] = 0.029
    height: float

    def get_spent_calories(self):
        speed = self.get_distance()
        calories = ((self.COEFF_WALKING_1 * self.weight + (speed
                     ** self.DEGREE // self.height) * self.COEFF_WALKING_2
                     * self.weight) * self.duration * self.HOUR)
        return calories


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: ClassVar[float] = 1.38
    KOEFF_SPENT_CALORIES_1: ClassVar[float] = 1.1
    KOEFF_SPENT_CALORIES_2: ClassVar[int] = 2
    length_pool: float
    count_pool: int

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self):
        speed = (self.length_pool
                 * self.count_pool / self.M_IN_KM / self.duration)

        return speed

    def get_spent_calories(self):
        calories = ((self.get_mean_speed() + self.KOEFF_SPENT_CALORIES_1)
                    * self.KOEFF_SPENT_CALORIES_2 * self.weight)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_type_trening = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in dict_type_trening:
        training_type = dict_type_trening[workout_type](*data)
        return training_type
    raise KeyError(f'Неккоретный тип тренировки: {workout_type}')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
