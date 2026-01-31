from datetime import datetime as dt

from django.conf import settings


class MoonsCalc:
    """docstring for MoonsCalc"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MoonsCalc, cls).__new__(cls)
            print("Создан экземпляр MoonsCalc")
        return cls._instance

    def __init__(self):
        self.full_moons = []
        self.new_moons = []
        self.create_moons_db()
        print("Проинициализирован экземпляр MoonsCalc")

    def create_moons_db(self):
        """    3 фев 1931  0:26"""

        MONTH_TRANSLATE = {
            'янв': '01',
            'фев': '02',
            'мар': '03',
            'апр': '04',
            'мая': '05',
            'июн': '06',
            'июл': '07',
            'авг': '08',
            'сен': '09',
            'окт': '10',
            'ноя': '11',
            'дек': '12'
            }

        with open(settings.BASE_DIR / 'main/foolmoons30-99.txt') as fmf:
            for line in fmf:
                # self.full_moons.append(dt.strptime("09/23/2030 8:28","%m/%d/%Y %H:%M")
                date_components_list = line.strip().split()
                date_components_list[1] = MONTH_TRANSLATE[date_components_list[1]]
                valid_date = ' '.join(date_components_list)
                self.full_moons.append(dt.strptime(valid_date, "%d %m %Y %H:%M"))
                try:
                    delta = (self.full_moons[-1] - self.full_moons[-2]) / 2
                    self.new_moons.append(self.full_moons[-1] - delta)
                except IndexError:
                    pass

        print(f'В базу внесено {len(self.full_moons)} полнолуний \
            с {self.full_moons[0].year} по {self.full_moons[-1].year}')

    def fool_moons_calc(self, birth_date):
        for fool_moon in self.full_moons:
            if birth_date < fool_moon:
                start_moon = self.full_moons.index(fool_moon)
                previous_moon = self.full_moons[start_moon - 1]
                fractional_part = (birth_date - previous_moon) / (fool_moon - previous_moon)
                precise_start_moon = start_moon - 1 + fractional_part
                break
        now_date = dt.now()
        for fool_moon in self.full_moons:
            if now_date < fool_moon:
                end_moon = self.full_moons.index(fool_moon)
                previous_moon = self.full_moons[end_moon - 1]
                fractional_part = (now_date - previous_moon) / (fool_moon - previous_moon)
                precise_end_moon = end_moon - 1 + fractional_part
                break
        return end_moon - start_moon, round(precise_end_moon - precise_start_moon, 2)

    def new_moons_calc(self, birth_date):
        for new_moon in self.new_moons:
            if birth_date < new_moon:
                start_moon = self.new_moons.index(new_moon)
                previous_moon = self.new_moons[start_moon - 1]
                fractional_part = (birth_date - previous_moon) / (new_moon - previous_moon)
                precise_start_moon = start_moon - 1 + fractional_part
                break
        now_date = dt.now()
        for new_moon in self.new_moons:
            if now_date < new_moon:
                end_moon = self.new_moons.index(new_moon)
                previous_moon = self.new_moons[end_moon - 1]
                fractional_part = (now_date - previous_moon) / (new_moon - previous_moon)
                fase = MoonsCalc.fase_calc(fractional_part)
                precise_end_moon = end_moon - 1 + fractional_part
                break
        return end_moon - start_moon, round(precise_end_moon - precise_start_moon, 2), fase

    def moons_calc(self, birth_date):
        ''' надо сделать DRY на fool_moons_calc и new_moons_calc'''
        pass

    @staticmethod
    def fase_calc(fraction):
        """
        Docstring for fase_calc
        :param fraction: float{0...1} фаза луны, где 0 - новолуние 0.5 - полнолуние
        return:
        0 - новолуние
        1 - молодая луна
        2 - первая четверть
        3 - растущая луна
        4 - полнолуние
        5 - убывающая луна
        6 - последняя четверть
        7 - старая луна
        """
        if fraction > 0.05 and fraction <= 0.21:
            return 1
        if fraction > 0.21 and fraction <= 0.29:
            return 2
        if fraction > 0.29 and fraction <= 0.45:
            return 3
        if fraction > 0.45 and fraction <= 0.55:
            return 4
        if fraction > 0.55 and fraction <= 0.71:
            return 5
        if fraction > 0.71 and fraction <= 0.79:
            return 6
        if fraction > 0.79 and fraction <= 0.95:
            return 7
        return 0

    def round_moon_date(self, birth_date, moons):
        for new_moon in self.new_moons:
            if birth_date < new_moon:
                start_moon = self.new_moons.index(new_moon)
                previous_moon = self.new_moons[start_moon - 1]
                fractional_part = (birth_date - previous_moon) / (new_moon - previous_moon)
                precise_birth_moon = start_moon - 1 + fractional_part
                break
        precise_end_moon = precise_birth_moon + moons
        return self.moons_to_date(precise_end_moon)

    def moons_to_date(self, moon_idx):
        integer_part = int(moon_idx)
        fractional_part = moon_idx - integer_part
        try:
            start_dt, end_dt = self.new_moons[integer_part:integer_part+2]
        except ValueError:
            return "только в следующем веке"
        return start_dt + (end_dt - start_dt) * fractional_part


def rounding(age):
    if age // 10 != age / 10:
        return int((age // 10 + 1) * 10)
    elif age // 50 != age / 50:
        return int((age // 50 + 1) * 50)
    elif age // 100 != age / 100:
        return int((age // 100 + 1) * 100)
    elif age // 500 != age / 500:
        return int((age // 500 + 1) * 500)
    else:
        return int((age // 1000 + 1) * 1000)


def fase_presentation(fase):
    if fase == 0:
        return '🌑', 'в новолуние'
    if fase == 1:
        return '🌒', 'в молодую луну (растущий серп)'
    if fase == 2:
        return '🌓', 'в первую четверть лунного цикла'
    if fase == 3:
        return '🌔', 'в растущую луну'
    if fase == 4:
        return '🌕', 'в полнолуние'
    if fase == 5:
        return '🌖', 'в убывающую луну'
    if fase == 6:
        return '🌗', 'в последнюю четверть лунного цикла'
    if fase == 7:
        return '🌘', 'в старую луну (убывающий серп)'


MC = MoonsCalc()


if __name__ == "__main__":
    MC = MoonsCalc()
    print('Введите дату рождения')
    birth_day = int(input('дата (1...31) : '))
    print('Введите месяц рождения')
    birth_month = int(input('месяц (1...12) : '))
    print('Введите год рождения')
    birth_year = int(input('год (19.. / 20..) : '))
    if birth_year < 100:
        birth_year += 1900
        if birth_year < 1930:
            birth_year += 100
    birth_date = dt(birth_year, birth_month, birth_day)
    print('Ваша дата рождения ', birth_date)
    pf_moons = MC.fool_moons_calc(birth_date)[0]
    pn_moons, moon_age, birth_moon = MC.new_moons_calc(birth_date)
    print(f'Вы пережили {pf_moons} полнолуний')
    print(f'Вы пережили {pn_moons} новолуний')
    print(f'Ваш точный лунный возраст: {moon_age} лун')
    next_moonniversary = rounding(moon_age)
    print(f'Ваш лунный юбилей в {next_moonniversary} лун состоится:\
          {MC.round_moon_date(birth_date, next_moonniversary)}')
    if next_moonniversary % 1000:
        next_moonniversary = rounding(next_moonniversary)
        print(f'Ваш лунный юбилей в {next_moonniversary} лун состоится:\
              {MC.round_moon_date(birth_date, next_moonniversary)}')
    if next_moonniversary % 1000:
        next_moonniversary = rounding(next_moonniversary)
        print(f'Ваш лунный юбилей в {next_moonniversary} лун состоится:\
              {MC.round_moon_date(birth_date, next_moonniversary)}')
