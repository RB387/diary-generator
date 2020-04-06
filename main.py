# coding=utf-8
import random
import datetime as dt
import pandas as pd
import numpy as np, numpy.random

MEAN_MINUTES = 210

class ExerciseType(object):
    def get_name(self):
        pass

    def get_property_range(self):
        pass


class JumpingOnPlaceExerciseType(ExerciseType):
    def get_name(self):
        return "Прыжки на месте"

    def get_property_range(self):
        return [40, 70]


class PushUpsExerciseType(ExerciseType):
    def get_name(self):
        return "Отжимания"

    def get_property_range(self):
        return [20, 40]


class SquattingExerciseType(ExerciseType):
    def get_name(self):
        return "Приседания"

    def get_property_range(self):
        return [30, 50]


class AbsExerciseType(ExerciseType):
    def get_name(self):
        return "Пресс"

    def get_property_range(self):
        return [30, 50]


class PullUpExerciseType(ExerciseType):
    def get_name(self):
        return "Подтягивания"

    def get_property_range(self):
        return [10, 20]


def generate_trainings(time):
    exercise_types = [
        JumpingOnPlaceExerciseType(),
        PushUpsExerciseType(),
        SquattingExerciseType(),
        PullUpExerciseType(),
        AbsExerciseType()
    ]
    count = random.randint(3, len(exercise_types))
    dirichlet = np.random.dirichlet(np.ones(count), size=1)[0] * time
    trainings = []
    for idx in range(count):
        idx_training = random.randint(0, len(exercise_types)-1)
        exercise = exercise_types[idx_training]
        count = int(dirichlet[idx]*2)
        if count > 5:
            trainings.append({'name': exercise.get_name(),
                              'count': count,
                              'time': int(dirichlet[idx]) })
            exercise_types.pop(idx_training)
    return trainings

def generate_dataframe(diary):
    trainings_str = ['' for _ in range(len(diary))]
    total_time = [0 for _ in range(len(diary))]
    for idx, day in enumerate(diary):
        for training in day['trainings']:
            trainings_str[idx] += f'{training["name"]} {training["count"]} раз\n'
            total_time[idx] += training['time']
    data_frame = [[x['day'].strftime("%d.%m.%Y") for x in diary],
                 ['' for _ in range(len(diary))],
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
    print('Total time: ', sum(total_time))
    print('Correct data if time less than 180 minutes')
    return pd.DataFrame(data_frame)

def generate(weight, date):
    dirichlet = np.random.dirichlet(np.ones(7), size=1)[0] * MEAN_MINUTES
    date_formatted = dt.datetime.strptime(date, "%Y-%m-%d")
    diary = []
    for day in range(7):
        exersice = generate_trainings(dirichlet[day])
        if len(exersice) > 0:
            diary_day = dict(day=date_formatted + dt.timedelta(days=day),
                             self_feeling=random.randint(3, 5),
                             sleep=random.randint(3, 5),
                             appetite=random.randint(3, 5),
                             trainings=exersice,
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
