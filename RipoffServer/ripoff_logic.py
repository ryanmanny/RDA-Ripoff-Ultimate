from models import PaymentType

PULLMAN_SALES_TAX = 7.8  # PERCENT


def calculate_actual_cost(base_price, payment_type, discount_plan=None, rda_plan=None):
    """
    Base cost is the advertised price
    Actual cost is what it actually ends up costs you
    """
    if payment_type == PaymentType.RDA:
        discount = discount_plan.rda_discount
        proportion_of_base_cost_used = (base_price / rda_plan.dollars) * rda_plan.base_cost
        actual_cost = base_price * (100 - discount) + proportion_of_base_cost_used

    elif payment_type == PaymentType.CGR:
        discount = discount_plan.cgr_discount
        actual_cost = base_price * (100 - discount)

    elif payment_type == PaymentType.CRD:
        actual_cost = base_price * (100 + PULLMAN_SALES_TAX)

    else:
        raise ValueError("Invalid Payment Type!")

    return actual_cost


def find_best_payment_method(base_price, discount_plan, rda_plan=None):  # If no RDA plan provided it doesn't try the RDA
    """
    This function gives Dining Services a fairer shake than they deserve
    It will always return Cougar Cash
    """
    lowest_cost = float("inf")
    best_payment_method = None

    if rda_plan:
        rda_cost = calculate_actual_cost(
            base_price=base_price,
            payment_type=PaymentType.RDA,
            discount_plan=discount_plan,
            rda_plan=rda_plan,
        )
    else:
        rda_cost = float("inf")

    if rda_cost < lowest_cost:
        lowest_cost = rda_cost
        best_payment_method = PaymentType.RDA

    cgr_cost = calculate_actual_cost(
        base_price=base_price,
        payment_type=PaymentType.CGR,
        discount_plan=discount_plan,
    )

    if cgr_cost < lowest_cost:
        lowest_cost = cgr_cost
        best_payment_method = PaymentType.CGR

    crd_cost = calculate_actual_cost(
        base_price=base_price,
        payment_type=PaymentType.CRD,
    )

    if crd_cost < lowest_cost:
        lowest_cost = crd_cost
        best_payment_method = PaymentType.CRD

    if best_payment_method in (PaymentType.RDA, PaymentType.CRD):
        raise ArithmeticError("Best payment method should never be {}!".format(best_payment_method.name))

    return PaymentType.CGR


def calculate_simple_ripoff(base_price, payment_type, discount_plan, rda_plan):
    return base_price


# TODO: Add more robust Ripoff models that calculate different types of Ripoffs (e.g. Walmart comparison?)
