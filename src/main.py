import pandas as pd
import glob
import os
import json
import re

import csv
from pandas.core.apply import reconstruct_func

from src.templates import TEMPLATES_BY_AGE, generate_personalized_push

transactions_columns = [
    "client_code",
    "name",
    "product",
    "status",
    "city",
    "date",
    "category",
    "amount",
    "currency",
]
transfers_columns = [
    "client_code",
    "name",
    "product",
    "status",
    "city",
    "date",
    "type",
    "direction",
    "amount",
    "currency",
]
avg_columns = [
    "client_code",
    "name",
    "status",
    "age",
    "city",
    "avg_monthly_balance_KZT",
]


directory = "case 1"

transactions_dfs = []
transfers_dfs = []

client_names = []
client_codes = []
clients = {}


def _natural_key(path):
    # сортировка 'file10' после 'file2' корректно
    name = os.path.basename(path)
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", name)]


csv_files = sorted(glob.glob(os.path.join(directory, "*.csv")), key=_natural_key)

for file in csv_files:
    file_name = os.path.basename(file)

    try:
        if file_name.endswith("transactions_3m.csv"):
            df = pd.read_csv(file, names=transactions_columns, skiprows=1, header=None)
            second_row = df.iloc[0]
            client_code = int(second_row["client_code"])
            name = second_row["name"]
            product = second_row["product"]
            status = second_row["status"]
            city = second_row["city"]
            if client_code not in clients:
                clients[client_code] = {
                    "name": name,
                    "product": product,
                    "status": status,
                    "city": city,
                    "age": 0,
                    "avg_monthly_balance_KZT": 0,
                    "transaction_data": {
                        "expenses": {
                            "USD": {"amount": 0.0, "transactions": 0},
                            "EUR": {"amount": 0.0, "transactions": 0},
                            "KZT": {"amount": 0.0, "transactions": 0},
                        },
                        "expenses_per_cat": {},
                    },
                    "transfer_data": {
                        "amount_in": {},
                        "amount_out": {},
                        "amount_in_per_type": {},
                        "amount_out_per_type": {},
                    },
                }
            if clients[client_code].get("product", "") == "":
                clients[client_code]["product"] = product
            for index, row in df.iterrows():
                category = row["category"]
                currency = row["currency"]
                amount = float(row["amount"])
                if (
                    category
                    not in clients[client_code]["transaction_data"]["expenses_per_cat"]
                ):
                    clients[client_code]["transaction_data"]["expenses_per_cat"][
                        category
                    ] = {
                        "USD": {"amount": 0.0, "transactions": 0},
                        "EUR": {"amount": 0.0, "transactions": 0},
                        "KZT": {"amount": 0.0, "transactions": 0},
                    }
                match currency:
                    case "EUR":
                        clients[client_code]["transaction_data"]["expenses_per_cat"][
                            category
                        ]["EUR"]["amount"] += amount
                        clients[client_code]["transaction_data"]["expenses_per_cat"][
                            category
                        ]["EUR"]["transactions"] += 1
                        clients[client_code]["transaction_data"]["expenses"]["EUR"][
                            "amount"
                        ] = (
                            clients[client_code]["transaction_data"]["expenses"][
                                "EUR"
                            ].get("amount", 0.0)
                            + amount
                        )
                        clients[client_code]["transaction_data"]["expenses"]["EUR"][
                            "transactions"
                        ] += 1
                    case "USD":
                        clients[client_code]["transaction_data"]["expenses_per_cat"][
                            category
                        ]["USD"]["amount"] += amount
                        clients[client_code]["transaction_data"]["expenses_per_cat"][
                            category
                        ]["USD"]["transactions"] += 1
                        clients[client_code]["transaction_data"]["expenses"]["USD"][
                            "amount"
                        ] = (
                            clients[client_code]["transaction_data"]["expenses"][
                                "USD"
                            ].get("amount", 0.0)
                            + amount
                        )
                        clients[client_code]["transaction_data"]["expenses"]["USD"][
                            "transactions"
                        ] += 1
                    case "KZT":
                        clients[client_code]["transaction_data"]["expenses_per_cat"][
                            category
                        ]["KZT"]["amount"] += amount
                        clients[client_code]["transaction_data"]["expenses_per_cat"][
                            category
                        ]["KZT"]["transactions"] += 1
                        clients[client_code]["transaction_data"]["expenses"]["KZT"][
                            "amount"
                        ] = (
                            clients[client_code]["transaction_data"]["expenses"][
                                "KZT"
                            ].get("amount", 0.0)
                            + amount
                        )
                        clients[client_code]["transaction_data"]["expenses"]["KZT"][
                            "transactions"
                        ] += 1

            print(f"Файл {file_name} успешно прочитан как транзакции.")

        elif file_name.endswith("transfers_3m.csv"):
            df = pd.read_csv(file, names=transfers_columns, skiprows=1, header=None)
            second_row = df.iloc[0]
            client_code = int(second_row["client_code"])
            name = second_row["name"]
            product = second_row["product"]
            status = second_row["status"]
            city = second_row["city"]
            if client_code not in clients:
                clients[client_code] = {
                    "name": name,
                    "product": product,
                    "status": status,
                    "city": city,
                    "age": 0,
                    "avg_monthly_balance_KZT": 0,
                    "transaction_data": {
                        "expenses": {
                            "USD": {"amount": 0.0, "transactions": 0},
                            "EUR": {"amount": 0.0, "transactions": 0},
                            "KZT": {"amount": 0.0, "transactions": 0},
                        },
                        "expenses_per_cat": {},
                    },
                    "transfer_data": {
                        "amount_in": {},
                        "amount_out": {},
                        "amount_in_per_type": {},
                        "amount_out_per_type": {},
                    },
                }
            if clients[client_code].get("product", "") == "":
                clients[client_code]["product"] = product
            for index, row in df.iterrows():
                transfer_type = row["type"]
                direction = row["direction"].lower().strip()
                currency = row["currency"].upper().strip()
                amount = float(row["amount"])
                transfer_data = clients[client_code]["transfer_data"]

                if currency not in transfer_data["amount_in"]:
                    transfer_data["amount_in"][currency] = {
                        "amount": 0.0,
                        "transactions": 0,
                    }
                    transfer_data["amount_out"][currency] = {
                        "amount": 0.0,
                        "transactions": 0,
                    }

                if direction == "in":

                    transfer_data["amount_in"][currency]["amount"] += amount
                    transfer_data["amount_in"][currency]["transactions"] += 1

                    if transfer_type not in transfer_data["amount_in_per_type"]:
                        transfer_data["amount_in_per_type"][transfer_type] = {
                            "USD": {"amount": 0.0, "transactions": 0},
                            "EUR": {"amount": 0.0, "transactions": 0},
                            "KZT": {"amount": 0.0, "transactions": 0},
                        }

                    transfer_data["amount_in_per_type"][transfer_type][currency][
                        "amount"
                    ] += amount
                    transfer_data["amount_in_per_type"][transfer_type][currency][
                        "transactions"
                    ] += 1

                elif direction == "out":

                    transfer_data["amount_out"][currency]["amount"] += amount
                    transfer_data["amount_out"][currency]["transactions"] += 1

                    if transfer_type not in transfer_data["amount_out_per_type"]:
                        transfer_data["amount_out_per_type"][transfer_type] = {
                            "USD": {"amount": 0.0, "transactions": 0},
                            "EUR": {"amount": 0.0, "transactions": 0},
                            "KZT": {"amount": 0.0, "transactions": 0},
                        }

                    transfer_data["amount_out_per_type"][transfer_type][currency][
                        "amount"
                    ] += amount
                    transfer_data["amount_out_per_type"][transfer_type][currency][
                        "transactions"
                    ] += 1
            print(f"Файл {file_name} успешно прочитан как трансфер.")
        elif file_name.endswith("clients.csv"):
            df = pd.read_csv(file, names=avg_columns, skiprows=1, header=None)
            for index, row in df.iterrows():
                client_code = int(row["client_code"])
                age = int(row["age"])
                avg_monthly_balance_KZT = int(row["avg_monthly_balance_KZT"])
                if client_code not in clients:
                    name = row["name"]
                    status = row["status"]
                    city = row["city"]
                    clients[client_code] = {
                        "name": name,
                        "product": "",
                        "status": status,
                        "city": city,
                        "age": age,
                        "avg_monthly_balance_KZT": avg_monthly_balance_KZT,
                        "transaction_data": {
                            "expenses": {
                                "USD": {"amount": 0.0, "transactions": 0},
                                "EUR": {"amount": 0.0, "transactions": 0},
                                "KZT": {"amount": 0.0, "transactions": 0},
                            },
                            "expenses_per_cat": {},
                        },
                        "transfer_data": {
                            "amount_in": {},
                            "amount_out": {},
                            "amount_in_per_type": {},
                            "amount_out_per_type": {},
                        },
                    }
                else:
                    clients[client_code]["age"] = age
                    clients[client_code][
                        "avg_monthly_balance_KZT"
                    ] = avg_monthly_balance_KZT
            print(f"Файл {file_name} успешно прочитан как клиенты.")
        else:
            print(
                f"Файл {file_name} не соответствует известным шаблонам и будет пропущен."
            )

    except Exception as e:
        print(f"Ошибка при чтении файла {file_name}: {e}")


output_file_path = "clients_data.json"

try:
    with open(output_file_path, "w", encoding="utf-8") as json_file:
        json.dump(clients, json_file, ensure_ascii=False, indent=4)

    print(f"Data successfully saved to {output_file_path}")

except Exception as e:
    print(f"Error writing to JSON file: {e}")

import math

TRAVEL_CATEGORIES = ["Путешествия", "Отели", "Такси"]
PREMIUM_CATEGORIES = [
    "Кафе и рестораны",
    "Ювелирные украшения",
    "Косметика и Парфюмерия",
]
KARTAKARTA_FAVORITES = ["Едим дома", "Смотрим дома", "Играем дома"]

# ====== БАЗОВЫЕ КОМИССИИ (для расчёта экономии) ======
BASE_FEE_ATM_RATE = 0.01  # 1% снятия
BASE_FEE_P2P_RATE = 0.005  # 0.5% переводы RK

# ====== TRAVEL CARD ======
TRAVEL_CB = 0.04
TRAVEL_ATM_FREE_CAP = 1_500_000.0
TRAVEL_NONCASH_MIN = 500_000.0
TRAVEL_DEPOSIT_MIN = 3_000_000.0
TRAVEL_SERVICE_FEE = 5_000.0

# ====== IRON / PREMIUM ======
PREMIUM_CB_TIERS = [(6_000_000.0, 0.04), (1_000_000.0, 0.03), (0.0, 0.02)]
PREMIUM_CB_CAP = 100_000.0
PREMIUM_ATM_FREE_CAP = 3_000_000.0

# ====== #KARTAKARTA (кредитка) ======
KARTAKARTA_CB = 0.10
KARTAKARTA_INSTALLMENT_BONUS = 2_000.0  # условный бонус, если favorites заметные

# ====== ДЕПОЗИТЫ / ИНВЕСТИЦИИ / ЗОЛОТО ======
RATE_DEPOSIT_MULTI = 0.145
RATE_DEPOSIT_FREEZE = 0.165
RATE_DEPOSIT_GAIN = 0.155
RATE_INVEST = 0.06
GOLD_THRESHOLD = 5_000_000.0
GOLD_RATE = 0.02


# ====== УТИЛИТЫ ======
def monthlyize(total_3m: float) -> float:
    return float(total_3m or 0.0) / 3.0


def safe_get_amt(d: dict, *keys) -> float:
    cur = d or {}
    for k in keys:
        cur = cur.get(k, {})
    if isinstance(cur, dict):
        return float(cur.get("amount", 0.0) or 0.0)
    try:
        return float(cur or 0.0)
    except Exception:
        return 0.0


# ====== ЛОГИКА БЕНЕФИТОВ (в МЕСЯЦ) ======
def calc_benefits_per_month(client: dict) -> dict:
    td = client.get("transaction_data", {}) or {}
    tr = client.get("transfer_data", {}) or {}
    exp = td.get("expenses") or {}
    exp_cat = td.get("expenses_per_cat") or {}
    avg_bal = float(client.get("avg_monthly_balance_KZT", 0) or 0.0)

    benefits = {}

    # Общие величины
    all_expenses_1m = monthlyize(safe_get_amt(exp, "KZT"))
    atm_out_1m = monthlyize(
        safe_get_amt(tr.get("amount_out_per_type", {}), "atm_withdrawal", "KZT")
    )
    p2p_out_1m = monthlyize(
        safe_get_amt(tr.get("amount_out_per_type", {}), "p2p_out", "KZT")
    )
    card_out_1m = monthlyize(
        safe_get_amt(tr.get("amount_out_per_type", {}), "card_out", "KZT")
    )

    # Travel card
    travel_spend_3m = sum(
        safe_get_amt(exp_cat.get(cat, {}), "KZT") for cat in TRAVEL_CATEGORIES
    )
    travel_cb_1m = TRAVEL_CB * monthlyize(travel_spend_3m)
    travel_save_atm = min(atm_out_1m, TRAVEL_ATM_FREE_CAP) * BASE_FEE_ATM_RATE
    travel_save_p2p = p2p_out_1m * BASE_FEE_P2P_RATE
    fee_waived = (card_out_1m >= TRAVEL_NONCASH_MIN) or (avg_bal >= TRAVEL_DEPOSIT_MIN)
    travel_fee = 0.0 if fee_waived else TRAVEL_SERVICE_FEE
    benefits["travel_card"] = round(
        travel_cb_1m + travel_save_atm + travel_save_p2p - travel_fee, 2
    )

    all_expenses_3m = safe_get_amt(exp, "KZT")
    all_expenses_1m = monthlyize(all_expenses_3m)
    travel_spend_3m = sum(
        safe_get_amt(exp_cat.get(cat, {}), "KZT") for cat in TRAVEL_CATEGORIES
    )
    premium_cats_3m = sum(
        safe_get_amt(exp_cat.get(cat, {}), "KZT") for cat in PREMIUM_CATEGORIES
    )

    travel_share = (travel_spend_3m / all_expenses_3m) if all_expenses_3m > 0 else 0.0
    premium_share = (premium_cats_3m / all_expenses_3m) if all_expenses_3m > 0 else 0.0

    # ATM/P2P usage (already monthlyized in your code as atm_out_1m / p2p_out_1m)
    heavy_cashflow = (atm_out_1m + p2p_out_1m) >= 300_000.0

    # ---------------- PREMIUM with gates ----------------
    # 1) eligibility
    prem_eligible = (
        (avg_bal >= 1_000_000.0) or heavy_cashflow or (premium_share >= 0.30)
    )

    if prem_eligible:
        # tier rate by avg balance
        for threshold, rate in PREMIUM_CB_TIERS:
            if avg_bal >= threshold:
                cb_rate = rate
                break
        # cashback on all spend, capped
        premium_cb = min(all_expenses_1m * cb_rate, PREMIUM_CB_CAP)

        # commission savings — only on the *part above* the free caps
        # (otherwise we were gifting savings even без реальной экономики)
        atm_over_cap = max(0.0, atm_out_1m - PREMIUM_ATM_FREE_CAP)
        prem_save_atm = atm_over_cap * BASE_FEE_ATM_RATE  # savings only above cap
        prem_save_p2p = p2p_out_1m * BASE_FEE_P2P_RATE  # keep as-is (RK transfers free)

        prem_benefit_raw = premium_cb + prem_save_atm + prem_save_p2p

        # 2) downweight if weak fit: tiny premium usage & tiny cashflow
        weak_fit = (premium_share < 0.15) and (atm_out_1m + p2p_out_1m < 150_000.0)
        fit_multiplier = 0.7 if weak_fit else 1.0

        benefits["premium_card"] = round(prem_benefit_raw * fit_multiplier, 2)
    else:
        benefits["premium_card"] = 0.0

    # #kartakarta (credit card)
    favorites_3m = sum(
        safe_get_amt(exp_cat.get(cat, {}), "KZT") for cat in KARTAKARTA_FAVORITES
    )
    kartakarta_cb_1m = KARTAKARTA_CB * monthlyize(favorites_3m)
    installment_bonus = (
        KARTAKARTA_INSTALLMENT_BONUS if monthlyize(favorites_3m) >= 100_000 else 0.0
    )
    benefits["kartakarta_credit_card"] = round(kartakarta_cb_1m + installment_bonus, 2)

    # FX
    fx_benefit = safe_get_amt(exp, "USD") * 0.02 + safe_get_amt(exp, "EUR") * 0.02
    benefits["fx"] = round(fx_benefit, 2)

    # Cash loan
    loan_3m = safe_get_amt(tr.get("amount_out_per_type", {}), "loan_payment_out", "KZT")
    benefits["cash_loan"] = round(monthlyize(loan_3m) * 0.10, 2)

    # Deposits
    benefits["multivalue_deposit"] = round(avg_bal * RATE_DEPOSIT_MULTI, 2)
    benefits["freeze_deposit"] = round(avg_bal * RATE_DEPOSIT_FREEZE, 2)
    benefits["gain_deposit"] = round(avg_bal * RATE_DEPOSIT_GAIN, 2)

    # Investments
    benefits["investments"] = round(avg_bal * RATE_INVEST, 2)

    # Gold
    benefits["gold"] = (
        round(avg_bal * GOLD_RATE, 2) if avg_bal > GOLD_THRESHOLD else 0.0
    )

    return benefits


def expand_to_periods(benefits_1m: dict):
    """Вернёт (per_month, for_3m) словари."""
    benefits_3m = {k: round(v * 3.0, 2) for k, v in benefits_1m.items()}
    return benefits_1m, benefits_3m


def find_best(benefits: dict):
    best_prod = max(benefits, key=benefits.get)
    return best_prod, benefits[best_prod]


# ====== MAIN ======


best_rows = [
    [
        "client_code",
        "name",
        "best_product_month",
        "benefit_month_kzt",
        "best_product_3m",
        "benefit_3m_kzt",
    ]
]
all_rows = [["client_code", "name", "product", "benefit_month_kzt", "benefit_3m_kzt"]]

for cid, data in clients.items():
    name = data.get("name", str(cid))

    b1m = calc_benefits_per_month(data)
    b1m, b3m = expand_to_periods(b1m)

    best_m, val_m = find_best(b1m)
    best_3m, val_3m = find_best(b3m)

    best_rows.append([cid, name, best_m, round(val_m, 2), best_3m, round(val_3m, 2)])

    for prod in sorted(b1m.keys()):
        all_rows.append([cid, name, prod, round(b1m[prod], 2), round(b3m[prod], 2)])

with open("best_recommendations.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows(best_rows)
with open("all_benefits.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows(all_rows)

print("✅ Saved: best_recommendations.csv, all_benefits.csv")


def process_all_clients(all_clients_data):
    recommendations_list = []
    for client_code, data in all_clients_data.items():
        # 1) считаем бенефиты за месяц
        benefits_1m = calc_benefits_per_month(data)
        # 2) находим лучший продукт по бенефиту
        best_product, max_benefit = find_best(benefits_1m)

        client_payload = {
            "client_code": client_code,
            "name": data.get("name"),
            "age": data.get("age"),
            "transaction_data": data.get("transaction_data"),
            "avg_monthly_balance_KZT": data.get("avg_monthly_balance_KZT"),
        }

        push_text = generate_personalized_push(
            client_payload=client_payload,
            product_key=best_product,
            benefit_val=max_benefit,
        )

        recommendations_list.append([client_code, best_product, push_text])

    csv_file_path = "notifs.csv"
    with open(csv_file_path, "w", newline="", encoding="utf-8") as new_file:
        writer = csv.writer(new_file)
        writer.writerow(["client_code", "product", "push_notification"])
        writer.writerows(recommendations_list)

    print(f"Данные успешно записаны в файл {csv_file_path}")


print(process_all_clients(clients))
