from datetime import date


# For now, the cover and premium are constant.
DEFAULT_COVER = 200000
DEFAULT_PREMIUM = 100


def calculate_age(dob):
    # Calculate age based on date of birth
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


def get_premium_multiplier(age_band):
    # Get premium multiplier based on age band
    # This is a placeholder, the actual implementation should be more complex
    if age_band == "under-18":
        return 1.0
    elif age_band == "18-40":
        return 1.5
    elif age_band == "41-60":
        return 2.0
    else:
        return 3.0


def calculate_premium(age, amount):
    # Calculate premium based on age and cover
    multiplier = get_premium_multiplier(age)
    return amount * multiplier


def calculate_quote(customer, policy_type, amount=DEFAULT_PREMIUM):
    # Calculate quote based on customer, policy type, and cover
    age = calculate_age(customer.dob)
    premium = calculate_premium(age, amount)
    return premium, DEFAULT_COVER
