# coding=utf-8
import random
import datetime as dt
import pandas as pd


class ExerciseType(object):
    def get_name(self):
        pass

    def get_property_range(self):
        pass

    def get_property_suffix(self):
        pass


class JumpingOnPlaceExerciseType(ExerciseType):
    def get_name(self):
        return "Прыжки на месте"

    def get_property_range(self):
        return [5, 50]

    def get_property_suffix(self):
        return "раз"


class PushUpsExerciseType(ExerciseType):
    def get_name(self):
        return "Отжимания"

    def get_property_range(self):
        return [5, 25]

    def get_property_suffix(self):
        return "раз"


class SquattingExerciseType(ExerciseType):
    def get_name(self):
        return "Приседания"

    def get_property_range(self):
        return [5, 50]

    def get_property_suffix(self):
        return "раз"


class PullUpExerciseType(ExerciseType):
    def get_name(self):
        return "Подтягивания"

    def get_property_range(self):
        return [1, 20]

    def get_property_suffix(self):
        return "раз"


# Все возможные типы упражнений
EXERCISE_TYPES = [
    JumpingOnPlaceExerciseType(),
    PushUpsExerciseType(),
    SquattingExerciseType(),
    PullUpExerciseType()
]


def generate_trainings():
    exercise_types = [
        JumpingOnPlaceExerciseType(),
        PushUpsExerciseType(),
        SquattingExerciseType(),
        PullUpExerciseType()
    ]
    count = random.randint(1, len(exercise_types))
    trainings = []
    for _ in range(count):
        idx = random.randint(0, len(exercise_types)-1)
        exercise = exercise_types[idx]
        count = random.randint(exercise.get_property_range()[0], exercise.get_property_range()[1])
        trainings.append({'name': exercise.get_name(),
                          'count': count,
                          'time': count * random.randint(1, 2)})
        exercise_types.pop(idx)
    return trainings

def generate_dataframe(diary):
    trainings_str = ['' for _ in range(len(diary))]
    total_time = [0 for _ in range(len(diary))]
    for idx, day in enumerate(diary):
        for training in day['trainings']:
            trainings_str[idx] += f'{training["name"]} {training["count"]} раз\n'
            total_time[idx] += training['time']
    dataframe = [['' for _ in range(len(diary))],
                 [x['day'].strftime("%d.%m.%Y") for x in diary],
                 [x['self_feeling'] for x in diary],
                 [x['sleep'] for x in diary],
                 [x['appetite'] for x in diary],
                 ['' for _ in range(len(diary))],
                 trainings_str,
                 total_time,
                 [x['pulse']['before'] for x in diary],
                 [x['pulse']['in-time'] for x in diary],
                 [x['pulse']['after'] for x in diary],
                 [x['weight'] for x in diary],
                 [x['weight'] for x in diary]]
    return pd.DataFrame(dataframe)

def generate(weight, date):
    date_formatted = dt.datetime.strptime(date, "%Y-%m-%d")
    diary = []
    for day in range(7):
        diary_day = dict(day=date_formatted + dt.timedelta(days=day),
                         self_feeling=random.randint(3, 5),
                         sleep=random.randint(3, 5),
                         appetite=random.randint(3, 5),
                         trainings=generate_trainings(),
                         pulse={'before': random.randint(60, 80),
                                'in-time': random.randint(110, 150),
                                'after': random.randint(140, 160)},
                         weight=weight)
        diary.append(diary_day)
    return diary


if __name__ == "__main__":
    weight = input('Enter your weight: ')
    date = input('Enter start date YYYY-MM-DD: ')
    generate_dataframe(generate(weight, date)).to_excel("output.xlsx")
