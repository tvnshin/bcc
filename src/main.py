import pandas as pd
import glob
import os
import json

transactions_columns = ['client_code', 'name', 'product', 'status', 'city', 'date', 'category', 'amount', 'currency']
transfers_columns = ['client_code', 'name', 'product', 'status', 'city', 'date', 'type', 'direction', 'amount',
                     'currency']
avg_columns = ['client_code', 'name', 'status', 'age', 'city', 'avg_monthly_balance_KZT']


directory = 'files'

transactions_dfs = []
transfers_dfs = []

client_names = []
client_codes = []
clients = {}

csv_files = glob.glob(os.path.join(directory, "*.csv"))

for file in csv_files:
    file_name = os.path.basename(file)

    try:
        if file_name.endswith('transactions_3m.csv'):
            df = pd.read_csv(file, names=transactions_columns, skiprows=1, header=None)
            second_row = df.iloc[0]
            client_code = int(second_row['client_code'])
            name = second_row['name']
            product = second_row['product']
            status = second_row['status']
            city = second_row['city']
            if client_code not in clients:
                clients[client_code] = {
                    'name': name,
                    'product': product,
                    'status': status,
                    'city': city,
                    'age': 0,
                    'avg_monthly_balance_KZT': 0,
                    'transaction_data': {
                        'expenses': {
                            'USD': {
                                'amount': 0.0,
                                'transactions': 0
                            },
                            'EUR': {
                                'amount': 0.0,
                                'transactions': 0
                            },
                            'KZT': {
                                'amount': 0.0,
                                'transactions': 0
                            }
                        },
                        'expenses_per_cat': {},
                    },
                    'transfer_data': {
                        "amount_in": {},
                        "amount_out": {},
                        "amount_in_per_type": {},
                        "amount_out_per_type": {}
                    }
                }
            if clients[client_code].get('product', '') == '':
                clients[client_code]['product'] = product
            for index, row in df.iterrows():
                category = row['category']
                currency = row['currency']
                amount = float(row['amount'])
                if category not in clients[client_code]['transaction_data']['expenses_per_cat']:
                    clients[client_code]['transaction_data']['expenses_per_cat'][category] = {
                        'USD': {
                            'amount': 0.0,
                            'transactions': 0
                        },
                        'EUR': {
                            'amount': 0.0,
                            'transactions': 0
                        },
                        'KZT': {
                            'amount': 0.0,
                            'transactions': 0
                        }
                    }
                match currency:
                    case 'EUR':
                        clients[client_code]['transaction_data']['expenses_per_cat'][category]['EUR'][
                            'amount'] += amount
                        clients[client_code]['transaction_data']['expenses_per_cat'][category]['EUR'][
                            'transactions'] += 1
                        clients[client_code]['transaction_data']['expenses']['EUR']['amount'] = \
                        clients[client_code]['transaction_data']['expenses']['EUR'].get('amount', 0.0) + amount
                        clients[client_code]['transaction_data']['expenses']['EUR']['transactions'] += 1
                    case 'USD':
                        clients[client_code]['transaction_data']['expenses_per_cat'][category]['USD'][
                            'amount'] += amount
                        clients[client_code]['transaction_data']['expenses_per_cat'][category]['USD'][
                            'transactions'] += 1
                        clients[client_code]['transaction_data']['expenses']['USD']['amount'] = \
                        clients[client_code]['transaction_data']['expenses']['USD'].get('amount', 0.0) + amount
                        clients[client_code]['transaction_data']['expenses']['USD']['transactions'] += 1
                    case 'KZT':
                        clients[client_code]['transaction_data']['expenses_per_cat'][category]['KZT'][
                            'amount'] += amount
                        clients[client_code]['transaction_data']['expenses_per_cat'][category]['KZT'][
                            'transactions'] += 1
                        clients[client_code]['transaction_data']['expenses']['KZT']['amount'] = \
                        clients[client_code]['transaction_data']['expenses']['KZT'].get('amount', 0.0) + amount
                        clients[client_code]['transaction_data']['expenses']['KZT']['transactions'] += 1

            print(f"Файл {file_name} успешно прочитан как транзакции.")

        elif file_name.endswith('transfers_3m.csv'):
            df = pd.read_csv(file, names=transfers_columns, skiprows=1, header=None)
            second_row = df.iloc[0]
            client_code = int(second_row['client_code'])
            name = second_row['name']
            product = second_row['product']
            status = second_row['status']
            city = second_row['city']
            if client_code not in clients:
                clients[client_code] = {
                    'name': name,
                    'product': product,
                    'status': status,
                    'city': city,
                    'age': 0,
                    'avg_monthly_balance_KZT': 0,
                    'transaction_data': {
                        'expenses': {
                            'USD': {
                                'amount': 0.0,
                                'transactions': 0
                            },
                            'EUR': {
                                'amount': 0.0,
                                'transactions': 0
                            },
                            'KZT': {
                                'amount': 0.0,
                                'transactions': 0
                            }
                        },
                        'expenses_per_cat': {},
                    },
                    'transfer_data': {
                        "amount_in": {},
                        "amount_out": {},
                        "amount_in_per_type": {},
                        "amount_out_per_type": {}
                    }
                }
            if clients[client_code].get('product', '') == '':
                clients[client_code]['product'] = product
            for index, row in df.iterrows():
                transfer_type = row['type']
                direction = row['direction'].lower().strip()
                currency = row['currency'].upper().strip()
                amount = float(row['amount'])
                transfer_data = clients[client_code]['transfer_data']

                if currency not in transfer_data['amount_in']:
                    transfer_data['amount_in'][currency] = {"amount": 0.0, "transactions": 0}
                    transfer_data['amount_out'][currency] = {"amount": 0.0, "transactions": 0}

                if direction == 'in':

                    transfer_data['amount_in'][currency]['amount'] += amount
                    transfer_data['amount_in'][currency]['transactions'] += 1


                    if transfer_type not in transfer_data['amount_in_per_type']:
                        transfer_data['amount_in_per_type'][transfer_type] = {
                            "USD": {"amount": 0.0, "transactions": 0},
                            "EUR": {"amount": 0.0, "transactions": 0},
                            "KZT": {"amount": 0.0, "transactions": 0}
                        }


                    transfer_data['amount_in_per_type'][transfer_type][currency]['amount'] += amount
                    transfer_data['amount_in_per_type'][transfer_type][currency]['transactions'] += 1

                elif direction == 'out':

                    transfer_data['amount_out'][currency]['amount'] += amount
                    transfer_data['amount_out'][currency]['transactions'] += 1


                    if transfer_type not in transfer_data['amount_out_per_type']:
                        transfer_data['amount_out_per_type'][transfer_type] = {
                            "USD": {"amount": 0.0, "transactions": 0},
                            "EUR": {"amount": 0.0, "transactions": 0},
                            "KZT": {"amount": 0.0, "transactions": 0}
                        }


                    transfer_data['amount_out_per_type'][transfer_type][currency]['amount'] += amount
                    transfer_data['amount_out_per_type'][transfer_type][currency]['transactions'] += 1
            print(f"Файл {file_name} успешно прочитан как трансфер.")
        elif file_name.endswith('clients.csv'):
            df = pd.read_csv(file, names=avg_columns, skiprows=1, header=None)
            for index, row in df.iterrows():
                client_code = int(row['client_code'])
                age = int(row['age'])
                avg_monthly_balance_KZT = int(row['avg_monthly_balance_KZT'])
                if client_code not in clients:
                    name = row['name']
                    status = row['status']
                    city = row['city']
                    clients[client_code] = {
                        'name': name,
                        'product': '',
                        'status': status,
                        'city': city,
                        'age': age,
                        'avg_monthly_balance_KZT': avg_monthly_balance_KZT,
                        'transaction_data': {
                            'expenses': {
                                'USD': {
                                    'amount': 0.0,
                                    'transactions': 0
                                },
                                'EUR': {
                                    'amount': 0.0,
                                    'transactions': 0
                                },
                                'KZT': {
                                    'amount': 0.0,
                                    'transactions': 0
                                }
                            },
                            'expenses_per_cat': {},
                        },
                        'transfer_data': {
                            "amount_in": {},
                            "amount_out": {},
                            "amount_in_per_type": {},
                            "amount_out_per_type": {}
                        }
                    }
                else:
                    clients[client_code]['age'] = age
                    clients[client_code]['avg_monthly_balance_KZT'] = avg_monthly_balance_KZT
            print(f"Файл {file_name} успешно прочитан как клиенты.")
        else:
            print(f"Файл {file_name} не соответствует известным шаблонам и будет пропущен.")

    except Exception as e:
        print(f"Ошибка при чтении файла {file_name}: {e}")


output_file_path = 'clients_data.json'

try:
    with open(output_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(clients, json_file, ensure_ascii=False, indent=4)

    print(f"Data successfully saved to {output_file_path}")

except Exception as e:
    print(f"Error writing to JSON file: {e}")

import math

TRAVEL_CATEGORIES = ["Путешествия", "Отели", "Такси"]
PREMIUM_CATEGORIES = ["Кафе и рестораны", "Ювелирные украшения", "Косметика и Парфюмерия", "Ювелирные украшения", "Косметика и Парфюмерия"]
CREDIT_CARD_CATEGORIES = ["Едим дома", "Смотрим дома", "Играем дома"]
def get_product_benefit(client_data):
    """
    Вычисляет потенциальную выгоду от каждого продукта для данного клиента.

    Args:
        client_data (dict): Словарь с данными одного клиента.

    Returns:
        dict: Словарь с названием продукта и его рассчитанной выгодой.
    """
    benefits = {}

    # Вычисляем выгоду для 'Карта для путешествий'
    travel_spend = 0
    for cat in TRAVEL_CATEGORIES:
        if cat in client_data["transaction_data"]["expenses_per_cat"]:
            travel_spend += client_data["transaction_data"]["expenses_per_cat"][cat]["KZT"]["amount"]
    # Упрощенная метрика: 4% от трат на путешествия/такси
    benefits["travel_card"] = 0.04 * travel_spend

    premium_spend = 0
    for cat in PREMIUM_CATEGORIES:
        if cat in client_data["transaction_data"]["expenses_per_cat"]:
            premium_spend += client_data["transaction_data"]["expenses_per_cat"][cat]["KZT"]["amount"]

    # Расчет базовых трат (все траты минус траты в премиум-категориях)
    all_expenses = client_data["transaction_data"]["expenses"]["KZT"]["amount"]
    base_spend = all_expenses - premium_spend

    # Метрика: 2% базового кешбэка + 4% от трат в премиум-категориях
    benefits["premium_card"] = (0.02 * base_spend) + (0.04 * premium_spend)

    # Вычисляем выгоду для 'Кредитная карта'
    credit_card_spend = 0
    for cat in CREDIT_CARD_CATEGORIES:
        if cat in client_data["transaction_data"]["expenses_per_cat"]:
            credit_card_spend += client_data["transaction_data"]["expenses_per_cat"][cat]["KZT"]["amount"]
    # Упрощенная метрика: 10% от трат в "любимых" категориях. Мы берем только онлайн-сервисы.
    benefits["credit_card"] = 0.1 * credit_card_spend

    # Вычисляем выгоду для 'Обмен валют'
    # Сигнал: траты в USD/EUR.
    # В ваших данных все траты в KZT, поэтому выгода будет 0.
    benefits["fx"] = (
        client_data["transaction_data"]["expenses"]["USD"]["amount"] * 0.02
        + client_data["transaction_data"]["expenses"]["EUR"]["amount"] * 0.02
    )

    # Вычисляем выгоду для 'Кредит наличными'
    # Сигнал: низкий баланс и регулярные платежи по кредитам
    # Упрощенная метрика: высокий потенциал, если баланс низкий
    # и есть платежи по кредитам
    loan_payments = client_data["transfer_data"]["amount_out_per_type"]["loan_payment_out"]["KZT"]["amount"]
    benefits["cash_loan"] = loan_payments * 0.1 # Условный коэффициент выгоды

    # Для Депозитов и Инвестиций вычисляем выгоду на основе баланса.
    avg_balance = client_data["avg_monthly_balance_KZT"]

    # 'Депозит сберегательный (с «заморозкой»)'
    # Сигнал: стабильный крупный остаток.
    # Упрощенная метрика: выше выгода, чем у других депозитов.
    benefits["freeze_deposit"] = avg_balance * 0.05

    # 'Депозит накопительный'
    # Сигнал: регулярные небольшие остатки.
    benefits["gain_deposit"] = avg_balance * 0.03

    # 'Депозит мультивалютный'
    # Сигнал: свободный остаток + FX-активность.
    benefits["multivalue_deposit"] = avg_balance * 0.04
    # Условный коэффициент, так как нет данных по валютным тратам.

    # 'Инвестиции (брокерский счёт)'
    # Сигнал: свободные деньги (высокий баланс).
    benefits["investments"] = avg_balance * 0.06

    return benefits


def find_best_product_for_client(client_data):
    """
    Находит наиболее выгодный продукт для одного клиента.

    Args:
        client_data (dict): Словарь с данными одного клиента.

    Returns:
        tuple: (название самого выгодного продукта, его выгода).
    """
    benefits = get_product_benefit(client_data)
    best_product = max(benefits, key=benefits.get)
    max_benefit = benefits[best_product]
    return (best_product, max_benefit)


def process_all_clients(all_clients_data):
    """
    Обрабатывает словарь всех клиентов и выводит рекомендации.

    Args:
        all_clients_data (dict): Словарь с данными всех клиентов.

    Returns:
        dict: Словарь с рекомендациями для каждого клиента.
    """
    recommendations = {}
    for client_id, data in all_clients_data.items():
        best_product, max_benefit = find_best_product_for_client(data)
        recommendations[data["name"]] = {
            "Наиболее выгодный продукт": best_product,
            "Потенциальная выгода (условная, KZT)": f"{max_benefit:.2f}",
        }
    return recommendations

print(process_all_clients(clients))