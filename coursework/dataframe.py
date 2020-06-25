import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

import storage

matplotlib.use('Qt5Agg')
df = pd.DataFrame(storage.mongo_collection().find({'year': {'$gte': 2000}}))


def plot_attacks_by_year_bar():
    years = df['year'].unique()
    attacks = [df[df['year'] == y].size for y in years]
    plt.bar([str(y) for y in years], attacks, zorder=2)
    plt.xticks(rotation=45)
    plt.ylabel('Кількість терористих актів')
    plt.grid('grey', zorder=0, axis='y')
    plt.get_current_fig_manager().window.showMaximized()
    plt.show()


def plot_country_region_barh():
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.tight_layout()

    countries = np.array(df['country'].unique())
    country_attacks = np.array([df[df['country'] == c].size for c in countries])
    indexes = np.argsort(-country_attacks)
    ax1.title.set_text('ТОП-20 країн по кількості терористичних актів')
    ax1.barh(countries[indexes][:20][::-1], country_attacks[indexes][:20][::-1], zorder=2)
    ax1.grid('grey', zorder=0, axis='x')
    ax1.set(xlabel="Кількість терористичних актів")

    regions = np.array(df['region'].unique())
    region_attacks = np.array([df[df['region'] == r].size for r in regions])
    indexes = np.argsort(region_attacks)
    ax2.title.set_text('Розподіл терористичних актів по регіонам')
    ax2.barh([r.replace('&', '&\n') for r in regions[indexes]], region_attacks[indexes], zorder=2)
    ax2.grid('grey', zorder=0, axis='x')
    ax2.set(xlabel="Кількість терористичних актів")

    plt.get_current_fig_manager().window.showMaximized()
    plt.show()


def plot_success_suicide_pie():
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.tight_layout()

    success_count = df[df['success'] == True].size
    unsuccess_count = df[df['success'] == False].size
    ax1.pie([success_count, unsuccess_count], labels=['Успішні', 'Неуспішні'], autopct='%1.1f%%', labeldistance=1.03)
    ax1.title.set_text('Співвідношення успішних/неуспішних\nтерористичних актів')

    suicide_count = df[df['suicide'] == True].size
    nosuicide_count = df[df['suicide'] == False].size
    ax2.pie([suicide_count, nosuicide_count], labels=['Суїцид', 'Не-суїцид'], autopct='%1.1f%%', labeldistance=1.03)
    ax2.title.set_text('Співвідношення терористих актів,\n які були/не були виконані терористом-смертником')

    plt.get_current_fig_manager().window.showMaximized()
    plt.show()


def plot_target_props_barh():
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.tight_layout()

    target_types = np.array(df['targtype'].unique())
    target_count = np.array([df[df['targtype'] == t].size for t in target_types])
    target_types = target_types[target_count > 10_000]
    target_count = target_count[target_count > 10_000]
    indexes = np.argsort(target_count)
    ax1.barh([t.split('&')[0].split('/')[0].replace(' ', '\n') for t in target_types[indexes]],
             target_count[indexes], zorder=2)
    ax1.grid('grey', zorder=0, axis='x')
    ax1.title.set_text("Типи об'єктів нападу")

    weapon_types = np.array(df['weaptype'].unique())
    weapon_counts = np.array([df[df['weaptype'] == w].size for w in weapon_types])
    weapon_types = weapon_types[weapon_counts > 1_500]
    weapon_counts = weapon_counts[weapon_counts > 1_500]
    indexes = np.argsort(weapon_counts)
    ax2.barh(weapon_types[indexes], weapon_counts[indexes], zorder=2)
    ax2.title.set_text('Тип озброєння, використаної для терористичного акту')
    ax2.grid('grey', zorder=0, axis='x')

    plt.get_current_fig_manager().window.showMaximized()
    plt.show()
