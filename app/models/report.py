from pydantic import BaseModel


class Commission(BaseModel):
    promotions: dict[float, float]
    total: float
    order_avg: float


class Report(BaseModel):
    customers: int
    total_discount_amount: float
    items: int
    order_total_avg: float
    discount_rate_avg: float
    commissions: Commission

