import datetime
from typing import Dict, Any

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


# helper: mapping month number to Russian month short/full name
RUS_MONTHS = {
    1: "января", 2: "февраля", 3: "марта", 4: "апреля",
    5: "мая", 6: "июня", 7: "июля", 8: "августа",
    9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
}

def format_money_kzt(value: float) -> str:
    """Format number like '2 490,50 ₸' with two decimals and space thousands."""
    try:
        v = float(value)
    except Exception:
        v = 0.0
    s = f"{v:,.2f}"             # e.g. "2,490.50"
    s = s.replace(",", "X").replace(".", ",").replace("X", " ")
    return f"{s} ₸"

def get_age_group(age: int) -> str:
    """Return age group label matching your five buckets."""
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

class SafeDict(dict):
    def __missing__(self, key):
        return ""

def extract_top_categories(payload: Dict[str, Any], n: int = 3):
    """Return top-n category names and sums from transaction_data.expenses_per_cat (descending by KZT)."""
    ex_cat = payload.get("transaction_data", {}).get("expenses_per_cat", {}) or {}
    # build dict of category -> kzt amount
    cat_sums = {}
    for cat, curmap in ex_cat.items():
        # prefer KZT if present, otherwise try to sum available currencies (not ideal but fallback)
        k = curmap.get("KZT")
        if k is None:
            # sum any numeric amounts
            try:
                k = sum([float(v) for v in curmap.values() if isinstance(v, (int, float))])
            except Exception:
                k = 0.0
        cat_sums[cat] = float(k or 0.0)
    # sort
    sorted_cats = sorted(cat_sums.items(), key=lambda x: x[1], reverse=True)
    top_names = [name for name, _ in sorted_cats[:n]]
    # pad if fewer than n
    while len(top_names) < n:
        top_names.append("")
    return top_names

def detect_fx_currency(payload: Dict[str, Any]) -> str:
    """Try to detect most-used FX currency from payload (USD/EUR), fallback to 'USD'."""
    # look in transfers for fx events or in expenses per cat for non-zero USD/EUR
    tr = payload.get("transfer_data", {})
    # check amount_in_per_type and amount_out_per_type for fx_buy/fx_sell
    for m in ("amount_in_per_type", "amount_out_per_type"):
        part = tr.get(m, {}) or {}
        for tname, cmap in part.items():
            if tname in ("fx_buy", "fx_sell"):
                # find currency with non-zero amount
                for cur, val in cmap.items():
                    if isinstance(val, dict):
                        amt = val.get("amount", 0) or 0
                        if cur.upper() in ("USD", "EUR") and amt and float(amt) > 0:
                            return cur.upper()
    # fallback: check expenses_per_cat values for any USD/EUR non-zero
    ex_cat = payload.get("transaction_data", {}).get("expenses_per_cat", {}) or {}
    for cat, cmap in ex_cat.items():
        for cur, amt in cmap.items():
            if cur.upper() in ("USD", "EUR") and amt and float(amt) > 0:
                return cur.upper()
    return "USD"

def safe_truncate(msg: str, limit: int = 220) -> str:
    if len(msg) <= limit:
        return msg
    # try to cut at last space before limit
    cut = msg[:limit-3]
    last_space = cut.rfind(" ")
    if last_space > 0:
        cut = cut[:last_space]
    return cut.rstrip() + "..."

def enforce_exclaim_limit(msg: str, max_exclaims: int = 1) -> str:
    if msg.count("!") <= max_exclaims:
        return msg
    # keep first max_exclaims '!' then replace further ones by '.'
    result = []
    ex_count = 0
    for ch in msg:
        if ch == "!":
            ex_count += 1
            if ex_count > max_exclaims:
                result.append(".")
            else:
                result.append(ch)
        else:
            result.append(ch)
    return "".join(result)

def first_name(full_name: str) -> str:
    if not full_name:
        return ""
    return str(full_name).strip().split()[0]

def generate_personalized_push(client_payload: Dict[str, Any], product_key: str, benefit_val: float = None) -> str:
    """
    Main function.
    client_payload: the JSON/dict for one client (structure like your provided example).
    product_key: one of keys in TEMPLATES_BY_AGE (e.g. 'travel_card', 'premium_card', ...)
    benefit_val: numeric benefit in KZT (optional) — if provided, will be inserted into template as {benefit}.
    Returns: formatted push string (Russian), respects TOV and formatting rules.
    """
    # safe defaults
    age = client_payload.get("age")
    name_full = client_payload.get("name", "")
    name = first_name(name_full) or ""
    age_group = get_age_group(age if age is not None else 26)
    templates_for_product = TEMPLATES_BY_AGE.get(product_key)
    if not templates_for_product:
        # fallback to a neutral template
        templates_for_product = {age_group: "{name}, у нас есть персональное предложение. Узнать подробнее."}

    template = templates_for_product.get(age_group) or templates_for_product.get("26-38")

    # build context for placeholders
    top_cats = extract_top_categories(client_payload, n=3)
    cat1, cat2, cat3 = top_cats[0], top_cats[1], top_cats[2]

    fx_curr = detect_fx_currency(client_payload)
    # taxi sum (KZT) if present
    taxi_sum_raw = client_payload.get("transaction_data", {}).get("expenses_per_cat", {}).get("Такси", {}).get("KZT", 0.0) or 0.0
    taxi_count = client_payload.get("transaction_data", {}).get("expenses_per_cat", {}).get("Такси", {}).get("transactions",
                 client_payload.get("transaction_data", {}).get("expenses_per_cat", {}).get("Такси", {}).get("count", 0))
    try:
        taxi_count = int(taxi_count or 0)
    except Exception:
        taxi_count = 0

    avg_balance = client_payload.get("avg_monthly_balance_KZT", 0.0) or 0.0
    # month: try to infer from current date
    now = datetime.datetime.now()
    month_str = RUS_MONTHS.get(now.month, "")

    # prepare context dict (use SafeDict to avoid KeyError when formatting)
    ctx = SafeDict({
        "name": name,
        "cat1": cat1,
        "cat2": cat2,
        "cat3": cat3,
        "fx_curr": fx_curr,
        "benefit": format_money_kzt(benefit_val) if benefit_val is not None else "",
        "avg_balance": format_money_kzt(avg_balance),
        "month": month_str,
        "taxi_sum": format_money_kzt(taxi_sum_raw),
        "taxi_count": taxi_count,
    })

    # fill template
    try:
        msg = template.format_map(ctx)
    except Exception:
        # safest fallback
        msg = f"{name}, у нас есть персональное предложение. Узнать подробнее."

    # enforce red policy / TOV:
    #  - max 1 exclamation
    msg = enforce_exclaim_limit(msg, max_exclaims=1)
    #  - no ALL CAPS sequences: convert any long all-caps words to title-case (basic guard)
    words = msg.split()
    cleaned_words = []
    for w in words:
        if len(w) > 1 and w.isupper():
            cleaned_words.append(w.capitalize())
        else:
            cleaned_words.append(w)
    msg = " ".join(cleaned_words)

    #  - trim to 220 chars (safe_truncate preserves words)
    msg = safe_truncate(msg, limit=220)

    # final ensure one CTA (we assume CTA present in template) and that message starts with observation (template already constructed that way)
    return msg

# Example usage:
if __name__ == "__main__":
    # sample usage with your example payload (replace with real dict)
    sample_client = {
        "name": "Айгерим",
        "age": 29,
        "avg_monthly_balance_KZT": 92643,
        "transaction_data": {
            "expenses_per_cat": {
                "Такси": {"KZT": 232520.11},
                "Путешествия": {"KZT": 275433.72},
                "Кафе и рестораны": {"KZT": 518757.59},
            }
        },
        "transfer_data": {}  # ...
    }
    push = generate_personalized_push(sample_client, "travel_card", benefit_val=1500)
    print(push)
