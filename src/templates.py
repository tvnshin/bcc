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
        "0-16": "{name}, премиальная карта - повышенный кешбэк и бесплатные снятия. С этим вы бы сэкономили {benefit}. Поделитесь с родителем.",
        "17-25": "{name}, хотите больше кешбэка в кафе и на покупки? премиальная карта даёт базовые 2% и повышенный кешбэк в ресторанах. С этим вы бы сэкономили {benefit}. Оформить сейчас.",
        "26-38": "{name}, у вас стабильный остаток {avg_balance} — премиальная карта даст до {tier}% кешбэка и бесплатные снятия. С этим вы бы сэкономили {benefit}. Оформить сейчас.",
        "39-50": "{name}, держите крупные остатки и часто снимаете? премиальная карта даёт до 4% при депозите и бесплатные снятия до 3 000 000 ₸/мес. С этим вы бы сэкономили {benefit}. Подключить карту.",
        "51-99": "{name}, хотите выгоды от крупного депозита и бесплатных снятий? премиальная карта даст повышенный кешбэк. С этим вы бы сэкономили {benefit}. Узнать условия."
    },
    "credit_card": {
        "0-16": "{name}, кредитные карты доступны совершеннолетним. Но с ними можно экономить. С этим вы бы сэкономили {benefit}. Поделитесь с родителем.",
        "17-25": "{name}, ваши топ-категории — {cat1}, {cat2}, {cat3}. Кредитная карта даёт до 10% кешбэка и рассрочку. С этим вы бы сэкономили {benefit}. Оформить карту.",
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
        "17-25": "{name}, нужен запас на крупные покупки или учёбу? кредит наличными онлайн без залога и гибкие сроки. С этим вы бы сэкономили {benefit}.",
        "26-38": "{name}, нужен финансовый запас на важные траты? кредит наличными без справок и с гибким графиком. С этим вы бы сэкономили {benefit}.",
        "39-50": "{name}, планируете ремонт или крупную покупку? кредит наличными с досрочным погашением. С этим вы бы сэкономили {benefit}.",
        "51-99": "{name}, нужен доступный кредит без залога? условия выгодные. С этим вы бы сэкономили {benefit}."
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
import math

def _age_to_bracket(age: int) -> str:
    try:
        age = int(age)
    except Exception:
        return "26-38"
    if age <= 16:
        return "0-16"
    if 17 <= age <= 25:
        return "17-25"
    if 26 <= age <= 38:
        return "26-38"
    if 39 <= age <= 50:
        return "39-50"
    return "51-99"

def _fmt_money(val, currency_symbol="₸"):
    """
    Форматирует число с разделителем тысяч и добавляет символ валюты.
    Если val None -> пустая строка.
    """
    # None -> empty
    if val is None:
        return ""
    try:
        fv = float(val)
    except Exception:
        return str(val)
    # >= 1 -> integer with space thousands
    if abs(fv) >= 1:
        rounded = int(round(fv))
        s = f"{rounded:,}"            # "1,234,567"
        s = s.replace(",", " ")       # "1 234 567"
        return f"{s} {currency_symbol}"
    # < 1 -> two decimals, comma decimal separator
    s = f"{fv:.2f}"                  # "0.50"
    s = s.replace(".", ",")          # "0,50"
    return f"{s} {currency_symbol}"

def generate_personalized_push(client_payload: dict, product_key: str, benefit_val):
    """
    Формирует персонализированное push-сообщение по шаблону.
    Возвращает список [client_code, product_title, push_text] — готовый ряд для CSV.
    """

    def _safe_get_tx(client_payload):
        return client_payload.get("transaction_data", {}) or {}

    # --- safe basic fields ---
    name = client_payload.get("name") or "Клиент"
    age = client_payload.get("age", None)
    client_code = client_payload.get("client_code", "")
    bracket = _age_to_bracket(age)

    # --- map internal product_key -> exact product title required in CSV ---
    PRODUCT_TITLE = {
        "travel_card": "Карта для путешествий",
        "premium_card": "Премиальная карта",
        "credit_card": "Кредитная карта",
        "fx": "Обмен валют",
        "cash_loan": "Кредит наличными",
        "multivalue_deposit": "Депозит мультивалютный",
        "deposit_multi": "Депозит мультивалютный",
        "freeze_deposit": "Депозит Сберегательный",
        "deposit_saving": "Депозит Сберегательный",
        "gain_deposit": "Депозит Накопительный",
        "deposit_nakop": "Депозит Накопительный",
        "investments": "Инвестиции",
        "gold_bars": "Золотые слитки",
    }
    product_title = PRODUCT_TITLE.get(product_key, product_key)

    # --- avg balance / tier ---
    avg_balance = client_payload.get("avg_monthly_balance_KZT")
    avg_balance_str = _fmt_money(avg_balance, "₸") if avg_balance is not None else ""

    try:
        ab = float(avg_balance) if avg_balance is not None else 0.0
    except Exception:
        ab = 0.0
    if ab >= 3_000_000:
        tier_percent = 4
    elif ab >= 1_000_000:
        tier_percent = 3
    elif ab >= 300_000:
        tier_percent = 2
    else:
        tier_percent = 1
    tier_str = f"{tier_percent}"

    # --- top categories (KZT) ---
    cat1 = cat2 = cat3 = "онлайн-услуги"
    try:
        expenses_per_cat = _safe_get_tx(client_payload).get("expenses_per_cat", {}) or {}
        cat_sums = []
        for cat, bycur in expenses_per_cat.items():
            try:
                k = float(bycur.get("KZT", {}).get("amount", 0.0) or 0.0)
            except Exception:
                k = 0.0
            cat_sums.append((cat, k))
        cat_sums.sort(key=lambda x: x[1], reverse=True)
        if len(cat_sums) > 0:
            cat1 = cat_sums[0][0]
        if len(cat_sums) > 1:
            cat2 = cat_sums[1][0]
        if len(cat_sums) > 2:
            cat3 = cat_sums[2][0]
    except Exception:
        pass

    # --- FX currency choice ---
    fx_curr = "USD/EUR"
    try:
        expenses = _safe_get_tx(client_payload).get("expenses", {}) or {}
        usd_amt = float(expenses.get("USD", {}).get("amount", 0.0) or 0.0)
        eur_amt = float(expenses.get("EUR", {}).get("amount", 0.0) or 0.0)
        if usd_amt == 0 and eur_amt == 0:
            fx_curr = "USD/EUR"
        elif usd_amt >= eur_amt:
            fx_curr = "USD"
        else:
            fx_curr = "EUR"
    except Exception:
        fx_curr = "USD/EUR"

    # --- format benefit properly ---
    # if product_key looks like FX, display benefit in fx_curr (if numeric)
    try:
        benefit_num = float(benefit_val) if benefit_val is not None else 0.0
    except Exception:
        benefit_num = None

    if product_key == "fx":
        # benefit may already be in USD/EUR — show with currency code
        benefit_str = _fmt_money(benefit_num, fx_curr) if benefit_num is not None else ""
    else:
        benefit_str = _fmt_money(benefit_num, "₸") if benefit_num is not None else ""

    # --- pick template ---
    product_templates = TEMPLATES_BY_AGE.get(product_key, {})
    template = product_templates.get(bracket) if product_templates else None
    if template is None and product_templates:
        template = next(iter(product_templates.values()))
    if template is None:
        template = "{name}, мы подобрали для вас продукт {product} — потенциальная выгода {benefit}."

    # --- replacements for formatting ---
    replacements = {
        "name": name,
        "benefit": benefit_str,
        "avg_balance": avg_balance_str,
        "tier": tier_str,
        "cat1": cat1,
        "cat2": cat2,
        "cat3": cat3,
        "fx_curr": fx_curr,
        "product": product_title
    }

    # --- render template safely ---
    try:
        push_text = template.format(**replacements)
    except Exception:
        # fallback safe replace
        push_text = template
        for k, v in replacements.items():
            push_text = push_text.replace("{" + k + "}", str(v))

    # --- enforce TOV / length limits: no caps, max one exclamation, length <= 220 ---
    # remove excessive CAPS (simple heuristic): if string is mostly lowercase already, keep as is;
    # otherwise lower only words not at sentence start. To avoid aggressive transformations, we'll
    # lower the whole string but capitalize first letter.
    if any(ch.isupper() for ch in push_text):
        push_text = push_text.lower()
        if len(push_text):
            push_text = push_text[0].upper() + push_text[1:]

    # ensure max one exclamation: replace multiple '!' with single
    if push_text.count("!") > 1:
        push_text = push_text.replace("!", "")
        # add at most one at the end if it feels like a CTA (not mandatory)
        # skip adding an exclamation to avoid sounding pushy.

    # Trim to 220 chars preserving UTF-8 characters; prefer to keep whole words
    max_len = 220
    if len(push_text) > max_len:
        truncated = push_text[:max_len].rsplit(" ", 1)[0]
        if len(truncated) < 30:
            # if truncation too aggressive, just hard cut
            truncated = push_text[:max_len]
        push_text = truncated + "…"

    # final safety: no all-caps and no leading/trailing spaces
    push_text = push_text.strip()

    # return CSV-ready row: [client_code, product_title, push_text]
    return [client_code, product_title, push_text]
