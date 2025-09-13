from typing import Dict, Any, Tuple, List
import datetime

# Age-grouped templates (from your text), keyed by product -> age_range
TEMPLATES_BY_AGE = {
    "travel_card": {
        "0-16": "{name}, ездите с семьёй? тревел-карта вернёт часть расходов на поездки и такси и даст привилегии Visa Signature. С этим вы бы сэкономили {benefit}. Поделитесь с родителем.",
        "17-25": "{name}, много поездок или такси? с тревел-картой 4% кешбэк на поездки и билеты плюс привилегии для путешествий. С этим вы бы сэкономили {benefit}. Оформить карту.",
        "26-38": "{name}, вы часто бронируете отели и билеты? тревел-карта даёт 4% кешбэк на путешествия и такси. С этим вы бы сэкономили {benefit}. Посмотреть выгоду.",
        "39-50": "{name}, часто в командировках или поездках? тревел-карта вернёт 4% по авиабилетам, отелям и такси. С этим вы бы сэкономили {benefit}. Оформить карту.",
        "51-99": "{name}, планируете поездку? тревел-карта вернёт 4% на поездки и такси и упростит расчёты за границей. С этим вы бы сэкономили {benefit}. Посмотреть условия."
    },
    "premium_card": {
        "0-16": "{name}, премиальная карта — семейное преимущество: повышенный кешбэк и бесплатные снятия. С этим вы бы сэкономили {benefit}. Поделитесь с родителем.",
        "17-25": "{name}, хотите больше кешбэка в кафе и на покупки? премиальная карта даёт базовые 2% и повышенный кешбэк в ресторанах. С этим вы бы сэкономили {benefit}. Оформить сейчас.",
        "26-38": "{name}, у вас стабильный остаток {avg_balance} — премиальная карта даст до {tier}% кешбэка и бесплатные снятия. С этим вы бы сэкономили {benefit}. Оформить сейчас.",
        "39-50": "{name}, держите крупные остатки и часто снимаете? премиальная карта даёт до 4% при депозите и бесплатные снятия до 3 000 000 ₸/мес. С этим вы бы сэкономили {benefit}. Подключить карту.",
        "51-99": "{name}, хотите выгоды от крупного депозита и бесплатных снятий? премиальная карта даст повышенный кешбэк. С этим вы бы сэкономили {benefit}. Узнать условия."
    },
    "credit_card": {
        "0-16": "{name}, кредитные карты доступны совершеннолетним. Но с ними можно экономить. С этим вы бы сэкономили {benefit}. Поделитесь с родителем.",
        "17-25": "{name}, ваши топ-категории — {cat1}, {cat2}, {cat3}. кредитная карта даёт до 10% кешбэка и рассрочку. С этим вы бы сэкономили {benefit}. Оформить карту.",
        "26-38": "{name}, часто платите в {cat1} и онлайн-сервисах? кредитная карта даёт до 10% кешбэка и льготный лимит. С этим вы бы сэкономили {benefit}. Оформить карту.",
        "39-50": "{name}, планируете крупные покупки или рассрочку? кредитная карта предложит до 10% кешбэка. С этим вы бы сэкономили {benefit}. Узнать условия.",
        "51-99": "{name}, нужна удобная рассрочка и кешбэк на привычные покупки? кредитная карта даст льготный период. С этим вы бы сэкономили {benefit}. Узнать условия."
    },
    "fx": {
        "0-16": "{name}, часто платите за границей? мультивалютный продукт помогает экономить на обмене. С этим вы бы сэкономили {benefit}. Поделитесь с родителем.",
        "17-25": "{name}, платите в {fx_curr}? выгодный обмен 24/7 и авто-покупка по целевому курсу. С этим вы бы сэкономили {benefit}. Настроить обмен.",
        "26-38": "{name}, часто тратите в {fx_curr}? настройте выгодный обмен и авто-покупку. С этим вы бы сэкономили {benefit}. Настроить обмен.",
        "39-50": "{name}, регулярные траты в {fx_curr}? мультивалютный продукт даст выгодный курс. С этим вы бы сэкономили {benefit}. Настроить обмен.",
        "51-99": "{name}, платите или копите в {fx_curr}? мультивалютный вклад и обмен упростят операции. С этим вы бы сэкономили {benefit}. Узнать условия."
    },
    "cash_loan": {
        "0-16": "{name}, кредиты доступны совершеннолетним. Но с ними можно экономить. С этим вы бы сэкономили {benefit}. Поделитесь с родителем.",
        "17-25": "{name}, нужен запас на крупные покупки или учёбу? кредит наличными онлайн без залога и гибкие сроки. С этим вы бы сэкономили {benefit}. Узнать лимит.",
        "26-38": "{name}, нужен финансовый запас на важные траты? кредит наличными без справок и с гибким графиком. С этим вы бы сэкономили {benefit}. Узнать лимит.",
        "39-50": "{name}, планируете ремонт или крупную покупку? кредит наличными с досрочным погашением. С этим вы бы сэкономили {benefit}. Узнать лимит.",
        "51-99": "{name}, нужен доступный кредит без залога? условия выгодные. С этим вы бы сэкономили {benefit}. Узнать лимит."
    },
    "deposit_multi": {
        "0-16": "{name}, начните копить с семьёй: мультивалютный вклад (KZT/USD/EUR/RUB). С этим вы бы сэкономили {benefit}. Поделитесь с родителем.",
        "17-25": "{name}, хотите хранить валюты и зарабатывать? мультивалютный вклад 14,50% и свободный доступ. С этим вы бы сэкономили {benefit}. Открыть вклад.",
        "26-38": "{name}, у вас остаются свободные средства: мультивалютный вклад 14,50% без ограничений. С этим вы бы сэкономили {benefit}. Открыть вклад.",
        "39-50": "{name}, храните и ребалансируйте валюты с выгодой: мультивалютный вклад 14,50%. С этим вы бы сэкономили {benefit}. Открыть вклад.",
        "51-99": "{name}, хотите диверсифицировать с доступом к средствам? мультивалютный вклад 14,50%. С этим вы бы сэкономили {benefit}. Узнать условия."
    },
    "deposit_saving": {
        "0-16": "{name}, вклад для семьи: максимальная ставка при «заморозке» средств. С этим вы бы сэкономили {benefit}. Поделитесь с родителем.",
        "17-25": "{name}, ищете высокую ставку? сберегательный вклад 16,50% (KDIF). С этим вы бы сэкономили {benefit}. Узнать условия.",
        "26-38": "{name}, готовы «заморозить» средства ради высокой ставки? сберегательный вклад 16,50%. С этим вы бы сэкономили {benefit}. Узнать условия.",
        "39-50": "{name}, хотите максимальную ставку и защиту KDIF? сберегательный вклад 16,50%. С этим вы бы сэкономили {benefit}. Узнать условия.",
        "51-99": "{name}, предпочтительна высокая доходность и защита вкладов? сберегательный вклад 16,50%. С этим вы бы сэкономили {benefit}. Узнать условия."
    },
    "deposit_nakop": {
        "0-16": "{name}, начните копить с семьёй: накопительный вклад с повышенной ставкой. С этим вы бы сэкономили {benefit}. Поделитесь с родителем.",
        "17-25": "{name}, откладываете на цель? накопительный вклад 15,50% с пополнением. С этим вы бы сэкономили {benefit}. Открыть вклад.",
        "26-38": "{name}, планируете крупную покупку? накопительный вклад 15,50% поможет накопить. С этим вы бы сэкономили {benefit}. Открыть вклад.",
        "39-50": "{name}, хотите планомерно копить с хорошей ставкой? накопительный вклад 15,50%. С этим вы бы сэкономили {benefit}. Открыть вклад.",
        "51-99": "{name}, хотите сохранить и приумножить с регулярными пополнениями? накопительный вклад 15,50%. С этим вы бы сэкономили {benefit}. Узнать условия."
    },
    "investments": {
        "0-16": "{name}, инвестиции доступны через родителя. Но с ними можно экономить. С этим вы бы сэкономили {benefit}. Поделитесь с родителем.",
        "17-25": "{name}, хотите начать инвестировать с малой суммы? счёт от 6 ₸ и 0% комиссий. С этим вы бы сэкономили {benefit}. Открыть счёт.",
        "26-38": "{name}, готовы инвестировать без комиссий на старт? счёт с порогом от 6 ₸. С этим вы бы сэкономили {benefit}. Открыть счёт.",
        "39-50": "{name}, интересует долгосрочный рост с низкими издержками? инвестиционный счёт без комиссий. С этим вы бы сэкономили {benefit}. Открыть счёт.",
        "51-99": "{name}, хотите диверсифицировать и начать с небольшой суммы? инвестиции без стартовых комиссий. С этим вы бы сэкономили {benefit}. Узнать условия."
    },
    "gold_bars": {
        "0-16": "{name}, золотые слитки доступны через родителя. Но с ними можно экономить. С этим вы бы сэкономили {benefit}. Поделитесь с родителем.",
        "17-25": "{name}, думаете о диверсификации? слитки 999,9 пробы и хранение в банке. С этим вы бы сэкономили {benefit}. Узнать условия.",
        "26-38": "{name}, рассматриваете долгосрочную защиту капитала? покупка золотых слитков и хранение в сейфе. С этим вы бы сэкономили {benefit}. Узнать условия.",
        "39-50": "{name}, хотите диверсифицировать портфель? золотые слитки 999,9 пробы. С этим вы бы сэкономили {benefit}. Узнать условия.",
        "51-99": "{name}, думаете о защите накоплений? золотые слитки и хранение в сейфе. С этим вы бы сэкономили {benefit}. Узнать условия."
    }
}
"""
personalization.py

Contains:
 - format_money_kzt
 - helpers to safely extract sums from client payload
 - get_product_benefit(client_data, months=3)
 - find_best_product_for_client(client_data, months=3)
 - generate_personalized_push(client_payload, product_key=None, benefit_val=None)

This module is standalone and can be imported from your pipeline.
"""

# Product keys used consistently across the system
PRODUCT_LABELS = {
    "travel_card": "Карта для путешествий",
    "premium_card": "Премиальная карта",
    "credit_card": "Кредитная карта",
    "fx": "Обмен валют",
    "cash_loan": "Кредит наличными",
    "deposit_multi": "Депозит Мультивалютный",
    "deposit_saving": "Депозит Сберегательный",
    "deposit_nakop": "Депозит Накопительный",
    "investments": "Инвестиции",
    "gold_bars": "Золотые слитки",
}

# Categories used for heuristics
TRAVEL_CATEGORIES = ["Путешествия", "Отели", "Такси"]
PREMIUM_CATEGORIES = ["Кафе и рестораны", "Ювелирные украшения", "Косметика и Парфюмерия"]
CREDIT_FAV_CATEGORIES = ["Едим дома", "Смотрим дома", "Играем дома", "Кино"]
ONLINE_CATEGORIES = ["Играем дома", "Смотрим дома", "Едим дома", "Кино"]

# Deposit / investment annual rates (as decimals)
RATES = {
    "deposit_multi": 0.1450,
    "deposit_saving": 0.1650,
    "deposit_nakop": 0.1550,
    "investments": 0.06,  # conservative proxy for expected return for ranking
}


def format_money_kzt(value: float) -> str:
    """Format number like '2 490,50 ₸' with two decimals and space thousands."""
    try:
        v = float(value or 0.0)
    except Exception:
        v = 0.0
    s = f"{v:,.2f}"  # e.g. "2,490.50"
    # convert to space thousands and comma decimal
    s = s.replace(",", "X").replace(".", ",").replace("X", " ")
    return f"{s} ₸"


def _safe_get_kzt_amount(client: Dict[str, Any], category: str) -> float:
    """Return KZT amount for a given category (safely)."""
    try:
        return float(client.get("transaction_data", {}).get("expenses_per_cat", {}).get(category, {}).get("KZT", 0.0) or 0.0)
    except Exception:
        return 0.0


def _sum_kzt_in_categories(client: Dict[str, Any], categories: List[str]) -> float:
    s = 0.0
    for c in categories:
        s += _safe_get_kzt_amount(client, c)
    return s


def _total_kzt_expenses(client: Dict[str, Any]) -> float:
    try:
        return float(client.get("transaction_data", {}).get("expenses", {}).get("KZT", {}).get("amount", 0.0) or 0.0)
    except Exception:
        return 0.0


def _sum_fx_expenses(client: Dict[str, Any]) -> float:
    """Sum expenses in USD and EUR converted to KZT is not possible here; we treat USD/EUR amounts as proxy and rank accordingly.
    For our heuristic we simply sum reported USD and EUR expense amounts (assuming they are in local currency units if present).
    """
    try:
        usd = float(client.get("transaction_data", {}).get("expenses", {}).get("USD", {}).get("amount", 0.0) or 0.0)
        eur = float(client.get("transaction_data", {}).get("expenses", {}).get("EUR", {}).get("amount", 0.0) or 0.0)
        return usd + eur
    except Exception:
        return 0.0


def _safe_transfer_amount(client: Dict[str, Any], direction_type: str, transfer_type: str) -> float:
    """Helper to safely read transfer_data[direction_type + '_per_type'][transfer_type]['KZT']['amount']"""
    try:
        return float(client.get("transfer_data", {}).get(direction_type + "_per_type", {}).get(transfer_type, {}).get("KZT", {}).get("amount", 0.0) or 0.0)
    except Exception:
        return 0.0


def get_product_benefit(client_data: Dict[str, Any], months: int = 3) -> Dict[str, float]:
    """Calculate an estimated benefit (in KZT) for each product for ranking purposes.

    Notes:
    - All benefits are estimated consistently for a time window of `months` months so they are comparable.
    - Cashback products use percent * observed spend for the period.
    - Deposits/investments use avg_monthly_balance projected for `months` months using annual rates.
    - FX uses a small heuristic based on non-KZT spending.
    - Values are heuristics for ranking only (not guaranteed customer-facing economics).
    """
    benefits: Dict[str, float] = {k: 0.0 for k in PRODUCT_LABELS.keys()}
    period_frac = months / 12.0

    # Travel card: 4% on travel-related categories
    travel_spend = _sum_kzt_in_categories(client_data, TRAVEL_CATEGORIES)
    benefits["travel_card"] = 0.04 * travel_spend

    # Premium card: 4% on premium categories; base cashback 2% normally, 3% if avg_balance 1-6M, 4% if >6M
    premium_spend = _sum_kzt_in_categories(client_data, PREMIUM_CATEGORIES)
    total_expenses = _total_kzt_expenses(client_data)
    base_spend = max(total_expenses - premium_spend, 0.0)
    avg_balance = float(client_data.get("avg_monthly_balance_KZT") or 0.0)
    if avg_balance >= 6_000_000:
        base_rate = 0.04
    elif avg_balance >= 1_000_000:
        base_rate = 0.03
    else:
        base_rate = 0.02
    premium_rate = 0.04
    premium_benefit = premium_rate * premium_spend + base_rate * base_spend
    # cashback cap 100 000 ₸/month -> scale for `months`
    cap_per_month = 100_000.0
    cap_total = cap_per_month * months
    benefits["premium_card"] = min(premium_benefit, cap_total)

    # Credit card: up to 10% in top-3 favorite categories + 10% on online services
    # pick top-3 categories actually used by user
    # We'll pick top 3 by KZT amount from expenses_per_cat
    ex_cat = client_data.get("transaction_data", {}).get("expenses_per_cat", {}) or {}
    cat_sums = {cat: float((ex_cat.get(cat, {}).get("KZT") or 0.0)) for cat in ex_cat.keys()}
    top3 = sorted(cat_sums.items(), key=lambda x: x[1], reverse=True)[:3]
    top3_sum = sum([v for _, v in top3])
    online_sum = _sum_kzt_in_categories(client_data, ONLINE_CATEGORIES)
    # avoid double count: union of categories (top3 may include online categories)
    # calculate union_sum by summing unique category amounts
    union_cats = set([c for c, _ in top3] + ONLINE_CATEGORIES)
    union_sum = _sum_kzt_in_categories(client_data, list(union_cats))
    benefits["credit_card"] = 0.10 * union_sum

    # FX / Обмен валют: benefit estimated as 2% of non-KZT spending (heuristic)
    fx_spend = _sum_fx_expenses(client_data)
    benefits["fx"] = 0.02 * fx_spend

    # Cash loan: if client has loan payments, benefit is estimated as the monthly flexibility/savings
    # We take loan_payment_out (3-month sum) and assume offering a competitive product would save small percent
    loan_payments = _safe_transfer_amount(client_data, "amount_out", "loan_payment_out")
    # heuristic: 2% of loan payments over the period
    benefits["cash_loan"] = 0.02 * loan_payments

    # Deposits & investments: estimate interest earned on avg_balance for `months` months
    for key in ("deposit_multi", "deposit_saving", "deposit_nakop", "investments"):
        rate = RATES.get(key, 0.0)
        # interest for months on avg monthly balance
        benefits[key] = (float(client_data.get("avg_monthly_balance_KZT") or 0.0)) * rate * period_frac

    # Gold bars: estimated benefit is small for short horizon — we use a tiny proxy to rank
    benefits["gold_bars"] = max(0.0, (float(client_data.get("avg_monthly_balance_KZT") or 0.0)) * 0.005 * period_frac)

    # Ensure non-negative and round
    for k in benefits.keys():
        try:
            benefits[k] = round(max(0.0, float(benefits[k])), 2)
        except Exception:
            benefits[k] = 0.0

    return benefits


def find_best_product_for_client(client_data: Dict[str, Any], months: int = 3) -> Tuple[str, float, List[Tuple[str, float]]]:
    """Return: (best_product_key, best_value, sorted_list_of_products_descending)

    sorted_list contains tuples (product_key, benefit_val) sorted by benefit descending.
    If all benefits are zero, fallback logic will recommend either a deposit or investments depending on avg balance.
    """
    benefits = get_product_benefit(client_data, months=months)
    # produce sorted list
    sorted_items = sorted(benefits.items(), key=lambda x: x[1], reverse=True)

    # fallback if top 4 all zeros: recommend deposit_nakop if avg balance small, else investments
    if sorted_items[0][1] == 0.0:
        avg_balance = float(client_data.get("avg_monthly_balance_KZT") or 0.0)
        if avg_balance <= 100_000:
            fallback = "deposit_nakop"
        elif avg_balance <= 1_000_000:
            fallback = "deposit_multi"
        else:
            fallback = "investments"
        return fallback, benefits.get(fallback, 0.0), sorted_items

    best_key, best_val = sorted_items[0]
    return best_key, best_val, sorted_items


def _get_age_group(age: int) -> str:
    if age is None:
        return "26-38"
    a = int(age)
    if 0 <= a <= 16:
        return "0-16"
    if 17 <= a <= 25:
        return "17-25"
    if 26 <= a <= 38:
        return "26-38"
    if 39 <= a <= 50:
        return "39-50"
    return "51-99"


def _extract_top_categories(client: Dict[str, Any], n: int = 3) -> List[str]:
    ex_cat = client.get("transaction_data", {}).get("expenses_per_cat", {}) or {}
    cat_sums = {cat: float((ex_cat.get(cat, {}).get("KZT") or 0.0)) for cat in ex_cat.keys()}
    sorted_cats = sorted(cat_sums.items(), key=lambda x: x[1], reverse=True)
    top = [name for name, _ in sorted_cats[:n]]
    while len(top) < n:
        top.append("")
    return top


def generate_personalized_push(client_payload: Dict[str, Any], product_key: str = None, benefit_val: float = None) -> Tuple[str, str, float]:
    """Generate a personalized push notification and return a tuple: (product_label, push_text, benefit_val)

    If product_key is None, the function will compute the best product using find_best_product_for_client.
    """
    # If no product provided, find best
    if product_key is None:
        product_key, benefit_val, _ = find_best_product_for_client(client_payload, months=3)

    # If benefit not provided, compute it
    if benefit_val is None:
        benefit_val = get_product_benefit(client_payload, months=3).get(product_key, 0.0)

    templates = TEMPLATES_BY_AGE
    age_group = _get_age_group(client_payload.get("age"))
    templates_for_product = templates.get(product_key) or {}
    template = templates_for_product.get(age_group) or templates_for_product.get("26-38") or "{name}, у нас есть персональное предложение. Узнать подробнее."

    name = str(client_payload.get("name") or "").strip().split()[0] if client_payload.get("name") else ""
    cat1, cat2, cat3 = _extract_top_categories(client_payload, n=3)
    avg_balance = client_payload.get("avg_monthly_balance_KZT") or 0.0

    ctx = {
        "name": name,
        "cat1": cat1,
        "cat2": cat2,
        "cat3": cat3,
        "fx_curr": "USD",
        "benefit": format_money_kzt(benefit_val),
        "avg_balance": format_money_kzt(avg_balance),
        "month": datetime.datetime.now().strftime("%d.%m.%Y")
    }

    try:
        text = template.format_map(ctx)
    except Exception:
        text = f"{name}, у нас есть персональное предложение. Узнать подробнее."

    # Enforce a few TOV rules:
    # - one CTA in template (we rely on templates); - trim to 220 chars; - max 1 exclamation
    if len(text) > 220:
        # try to cut gracefully
        cut = text[:217]
        last_space = cut.rfind(" ")
        if last_space > 0:
            cut = cut[:last_space]
        text = cut + "..."
    # limit exclamation marks
    if text.count("!") > 1:
        parts = []
        ex = 0
        for ch in text:
            if ch == "!":
                ex += 1
                parts.append("!" if ex == 1 else ".")
            else:
                parts.append(ch)
        text = "".join(parts)

    # final product label
    product_label = PRODUCT_LABELS.get(product_key, product_key)

    return product_label, text, round(float(benefit_val or 0.0), 2)


# If used as a script, small demo
if __name__ == "__main__":
    demo_client = {
        "name": "Айгерим",
        "age": 29,
        "avg_monthly_balance_KZT": 92_643,
        "transaction_data": {
            "expenses": {"KZT": {"amount": 2_626_914.27}},
            "expenses_per_cat": {
                "Такси": {"KZT": 232_520.11},
                "Путешествия": {"KZT": 275_433.72},
                "Кафе и рестораны": {"KZT": 518_757.59},
            }
        },
        "transfer_data": {}
    }

    pk, txt, val = generate_personalized_push(demo_client)
    print(pk)
    print(txt)
    print("Estimated benefit:", format_money_kzt(val))
