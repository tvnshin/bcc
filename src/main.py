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