import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from IPython.display import display
from datetime import datetime

"""**Загрузка данных:**"""

#для загрузки через колаб, выбрать файл "crime"

# from google.colab import files
# uploaded = files.upload()

crime = pd.read_csv(open('crime.csv','rb'))

#для загрузки через anaconda

crime = pd.read_csv('crime.csv')

crime = crime.rename(columns = {'Unnamed: 0': 'date/time'})
crime['date/time'] = pd.to_datetime(crime['date/time'])
crime = crime.set_index('date/time')
crime = crime.rename(columns = {'driver_race': 'race', 'driver_gender': 'gender'})

display(crime.head(3))

# задание 1 балл (сум 2)
# какие виды нарушений (violation) зафиксированны
# ответ список

"""**Cписок зафиксированных нарушений (violation) и их количество:**


"""

violations = crime['violation'].unique()

display(violations)
len(violations)

"""**Количества нарушений по полу и по расе в виде series:**"""

violations_gender = crime.groupby(['gender']).violation.count()
violations_race = crime.groupby(['race']).violation.count()

display(violations_gender)
display(violations_race)

# задание 1 балл (сум 6)
# построить сводную таблицу по количеству правонарушений (строки - пол, колонки - расса)
# ответ таблица DataFrame: строки - пол, колонки - расса, значения - количество правонарушений

"""**Сводная таблица количества нарушений, строки - пол, столбцы - раса:**"""

gender_race = crime.pivot_table('violation', index = 'gender', columns = 'race', aggfunc = 'count')

display(gender_race)

"""**Сводная таблица количества нарушений по расе в процентах для каждого пола:**"""

gender_race_prob = gender_race.apply(lambda x: x*100/sum(x), axis = 0)

display(gender_race_prob)

"""**Столбцовый график по предыдущей таблице:**"""

sns.set()
(gender_race_prob.T/100).plot(kind = 'bar', stacked = True,
                              title = "share of violations in dependence of driver's gender for different races");
plt.ylabel("share of violations");
plt.xlabel("race of a driver");
plt.xticks(rotation = 0);
plt.legend(bbox_to_anchor = (1.02,1.017));
plt.show()

"""**Количество преступлений в каждый час для всего периода:**"""

day = crime.copy().loc[:,['violation']].reset_index()
day['date/time'] = day['date/time'].apply(lambda x: datetime.strftime(x, "%Y-%m-%d %H:00"))
day = day.groupby(['date/time']).violation.count()

display(day)

"""**График среднего количества нарушений в каждый час для рабочих и выходных дней:**"""

df = pd.DataFrame(day)
df.index = pd.to_datetime(df.index)

df['time'] = df.index.time
df['year'] = df.index.year
df['day'] = df.index.date
df['day'] = df['day'].apply(lambda x: datetime.weekday(x) < 5)
df.day = df.day.replace({True: 'Workday', False: 'Weekend'})
df = df.reset_index(drop = True)

df = df.groupby(['year','day','time']).violation.mean().reset_index()

display(df.head(5))

pd.set_option("plotting.matplotlib.register_converters", True)
hourly_ticks = df['time'].values[::4]

fig, ax = plt.subplots(figsize = [10,6])

sns.lineplot(x = df['time'].astype(str), y = df['violation'], hue = df['day']);
plt.suptitle("mean amount of violations in dependence of day time for weekends and workdays");
plt.ylabel("mean amount of violations");
plt.xlabel("time of a day");
plt.xticks(hourly_ticks.astype(str));
plt.show()