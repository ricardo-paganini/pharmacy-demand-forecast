import random

import numpy as np
import pandas as pd

random.seed(42)
np.random.seed(42)

# ---------- Lojas ----------
stores = pd.DataFrame({
    'store_id': ['S01', 'S02', 'S03', 'S04', 'S05'],
    'store_name': ['Curitiba Centro', 'Curitiba Batel', 'Londrina', 'Maringá', 'Ponta Grossa'],
    'city': ['Curitiba', 'Curitiba', 'Londrina', 'Maringá', 'Ponta Grossa'],
    'opening_date': ['2015-03-10', '2017-08-21', '2018-05-14', '2019-11-04', '2021-02-08'],
})
store_factor = {'S01': 1.4, 'S02': 1.1, 'S03': 1.0, 'S04': 0.9, 'S05': 0.7}

# ---------- Produtos ----------
# product_id, nome, categoria, preço, venda média por dia, tipo de sazonalidade
product_list = [
    ('P01', 'Antigripal Comprimidos', 'Gripe e resfriado', 18.90, 6, 'winter'),
    ('P02', 'Xarope para Tosse', 'Gripe e resfriado', 24.50, 5, 'winter'),
    ('P03', 'Descongestionante Nasal', 'Gripe e resfriado', 15.90, 4, 'winter'),
    ('P04', 'Pastilha para Garganta', 'Gripe e resfriado', 12.90, 5, 'winter'),
    ('P05', 'Vitamina C Efervescente', 'Vitaminas', 21.90, 4, 'winter_light'),
    ('P06', 'Multivitamínico', 'Vitaminas', 39.90, 3, 'none'),
    ('P07', 'Protetor Solar FPS 30', 'Proteção solar', 49.90, 3, 'summer'),
    ('P08', 'Protetor Solar FPS 50', 'Proteção solar', 59.90, 3, 'summer'),
    ('P09', 'Loção Pós-Sol', 'Proteção solar', 34.90, 2, 'summer'),
    ('P10', 'Repelente de Insetos', 'Proteção solar', 27.90, 3, 'summer_light'),
    ('P11', 'Soro de Reidratação', 'Digestivos', 9.90, 3, 'summer_light'),
    ('P12', 'Antiácido', 'Digestivos', 11.90, 5, 'none'),
    ('P13', 'Dipirona', 'Analgésicos', 8.90, 12, 'none'),
    ('P14', 'Paracetamol', 'Analgésicos', 10.90, 10, 'winter_light'),
    ('P15', 'Ibuprofeno', 'Analgésicos', 14.90, 8, 'none'),
    ('P16', 'Creme Dental', 'Higiene', 6.90, 15, 'none'),
    ('P17', 'Sabonete Líquido', 'Higiene', 13.90, 8, 'none'),
    ('P18', 'Shampoo', 'Higiene', 19.90, 7, 'none'),
    ('P19', 'Desodorante', 'Higiene', 16.90, 10, 'none'),
    ('P20', 'Fio Dental', 'Higiene', 9.90, 6, 'none'),
]
products = pd.DataFrame(
    [p[:4] for p in product_list],
    columns=['product_id', 'product_name', 'category', 'unit_price'],
)

# força da sazonalidade (amplitude) e dia do ano do pico
season_params = {
    'winter': (2.0, 196),        # pico em meados de julho
    'winter_light': (0.6, 196),
    'summer': (3.0, 15),         # pico em meados de janeiro
    'summer_light': (1.0, 25),
    'none': (0.0, 1),
}

# ---------- Feriados ----------
holiday_list = [
    ('2023-01-01', 'Confraternização Universal'), ('2023-02-20', 'Carnaval'),
    ('2023-02-21', 'Carnaval'), ('2023-04-07', 'Sexta-feira Santa'),
    ('2023-04-21', 'Tiradentes'), ('2023-05-01', 'Dia do Trabalho'),
    ('2023-06-08', 'Corpus Christi'), ('2023-09-07', 'Independência'),
    ('2023-10-12', 'Nossa Senhora Aparecida'), ('2023-11-02', 'Finados'),
    ('2023-11-15', 'Proclamação da República'), ('2023-12-25', 'Natal'),
    ('2024-01-01', 'Confraternização Universal'), ('2024-02-12', 'Carnaval'),
    ('2024-02-13', 'Carnaval'), ('2024-03-29', 'Sexta-feira Santa'),
    ('2024-04-21', 'Tiradentes'), ('2024-05-01', 'Dia do Trabalho'),
    ('2024-05-30', 'Corpus Christi'), ('2024-09-07', 'Independência'),
    ('2024-10-12', 'Nossa Senhora Aparecida'), ('2024-11-02', 'Finados'),
    ('2024-11-15', 'Proclamação da República'), ('2024-11-20', 'Consciência Negra'),
    ('2024-12-25', 'Natal'),
    ('2025-01-01', 'Confraternização Universal'), ('2025-03-03', 'Carnaval'),
    ('2025-03-04', 'Carnaval'), ('2025-04-18', 'Sexta-feira Santa'),
    ('2025-04-21', 'Tiradentes'), ('2025-05-01', 'Dia do Trabalho'),
    ('2025-06-19', 'Corpus Christi'), ('2025-09-07', 'Independência'),
    ('2025-10-12', 'Nossa Senhora Aparecida'), ('2025-11-02', 'Finados'),
    ('2025-11-15', 'Proclamação da República'), ('2025-11-20', 'Consciência Negra'),
    ('2025-12-25', 'Natal'),
    ('2026-01-01', 'Confraternização Universal'),
]
holidays = pd.DataFrame(holiday_list, columns=['date', 'holiday_name'])
holiday_dates = set(pd.to_datetime(holidays['date']))

# ---------- Promoções (campanhas de 7 dias na rede toda) ----------
dates = pd.date_range('2023-01-01', '2025-12-31', freq='D')
promo_days = {}
for p in product_list:
    days = set()
    for start in np.random.choice(len(dates) - 7, size=15, replace=False):
        days.update(dates[start:start + 7])
    promo_days[p[0]] = days

# ---------- Vendas diárias ----------
weekday_factor = {0: 1.0, 1: 1.0, 2: 1.0, 3: 1.0, 4: 1.05, 5: 0.85, 6: 0.6}
rows = []
for date in dates:
    years = (date - dates[0]).days / 365
    trend = 1 + 0.06 * years                      # crescimento de ~6% ao ano
    is_holiday = date in holiday_dates
    for store_id in stores['store_id']:
        factor = store_factor[store_id]
        if store_id == 'S03' and date >= pd.Timestamp('2025-04-01'):
            factor = factor * 0.8                 # concorrente abriu perto da loja de Londrina
        for product_id, name, _, price, base, season in product_list:
            amplitude, peak = season_params[season]
            season_factor = 1 + amplitude * (1 + np.cos(2 * np.pi * (date.dayofyear - peak) / 365)) / 2
            on_promotion = int(date in promo_days[product_id])
            demand = (base * factor * trend * weekday_factor[date.dayofweek] * season_factor
                      * (0.6 if is_holiday else 1) * (1.4 if on_promotion else 1))
            rows.append({
                'date': date.strftime('%Y-%m-%d'),
                'store_id': store_id,
                'product_name': name,
                'units_sold': np.random.poisson(demand),
                'unit_price': round(price * 0.85, 2) if on_promotion else price,
                'on_promotion': on_promotion,
            })
sales = pd.DataFrame(rows)

# ---------- Problemas de propósito ----------
# 1. Sistema da loja de Maringá fora do ar por 9 dias (dias faltando)
outage = (sales['store_id'] == 'S04') & (sales['date'].between('2024-08-12', '2024-08-20'))
sales = sales[~outage]

# 2. Linhas perdidas aleatoriamente (~1%)
sales = sales.drop(sales.sample(frac=0.01, random_state=42).index)

# 3. Devoluções lançadas como venda negativa (~0,3%)
returns_idx = sales.sample(frac=0.003, random_state=7).index
sales.loc[returns_idx, 'units_sold'] = -np.random.randint(1, 4, size=len(returns_idx))

# 4. Nomes de produto escritos de vários jeitos (~8%)
def messy_name(name):
    option = random.choice(['lower', 'upper', 'space', 'double'])
    if option == 'lower':
        return name.lower()
    if option == 'upper':
        return name.upper()
    if option == 'space':
        return name + ' '
    return name.replace(' ', '  ', 1)

messy_idx = sales.sample(frac=0.08, random_state=11).index
sales.loc[messy_idx, 'product_name'] = sales.loc[messy_idx, 'product_name'].apply(messy_name)

# 5. Linhas duplicadas (~0,2%)
duplicates = sales.sample(frac=0.002, random_state=21)
sales = pd.concat([sales, duplicates]).sort_values(['date', 'store_id'], kind='stable').reset_index(drop=True)

# ---------- Salvando ----------
stores.to_csv('stores.csv', index=False)
products.to_csv('products.csv', index=False)
holidays.to_csv('holidays.csv', index=False)
sales.to_csv('sales.csv', index=False)

print('stores.csv:', stores.shape)
print('products.csv:', products.shape)
print('holidays.csv:', holidays.shape)
print('sales.csv:', sales.shape)
