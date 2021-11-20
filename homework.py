class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Печать результатов тренировки."""
        return (f'Тип тренировки: {self.training_type}; Длительность: '
                f'{self.duration:.3f} ч.; Дистанция: {self.distance:.3f} км;'
                f' Ср. скорость: {self.speed:.3f} км/ч; Потрачено ккал:'
                f' {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        LEN_STEP = 0.65
        M_IN_KM = 1000
        action_temp = self.action
        distance = action_temp * LEN_STEP / M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        distance = self.get_distance()
        speed = distance / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type = type(self).__name__
        duration = self.duration
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        info = InfoMessage(training_type, duration, distance, speed, calories)
        return info


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self):
        M_IN_KM = 1000
        speed = self.get_mean_speed()
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        calories = ((coeff_calorie_1 * speed - coeff_calorie_2)
                    * self.weight / M_IN_KM * self.duration * 60)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action,
                         duration,
                         weight)
        self.height = height

    def get_spent_calories(self):
        speed = self.get_distance()
        calories = ((0.035 * self.weight + (speed ** 2 // self.height)
                    * 0.029 * self.weight) * self.duration * 60)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action,
                         duration,
                         weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        LEN_STEP = 1.38
        M_IN_KM = 1000
        distance = self.action * LEN_STEP / M_IN_KM
        return distance

    def get_mean_speed(self):
        M_IN_KM = 1000
        speed = self.length_pool * self.count_pool / M_IN_KM / self.duration
        return speed

    def get_spent_calories(self):
        speed = self.get_mean_speed()
        calories = (speed + 1.1) * 2 * self.weight
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type == 'SWM':
        training_type = Swimming(data[0], data[1], data[2], data[3], data[4])
        return training_type
    elif workout_type == 'RUN':
        training_type = Running(data[0], data[1], data[2])
        return training_type
    elif workout_type == 'WLK':
        training_type = SportsWalking(data[0], data[1], data[2], data[3])
        return training_type


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
