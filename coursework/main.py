import consolemenu

import dataframe


def main():
    menu = consolemenu.SelectionMenu(['Кількість терористичних актів по рокам',
                                      'Кількість терористичних актів по країнам/регіонам',
                                      'Співвідношення вдалих/невдалих актів та актів, які були/не були спробою самогубства',
                                      'Статистика типів жертв та використаної зброї'])
    menu.show()
    if menu.is_selected_item_exit():
        return

    steps = [dataframe.plot_attacks_by_year_bar, dataframe.plot_country_region_barh,
             dataframe.plot_success_suicide_pie, dataframe.plot_target_props_barh]
    steps[menu.selected_option]()
    main()


if __name__ == '__main__':
    main()
