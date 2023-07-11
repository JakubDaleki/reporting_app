from pydantic import BaseModel


class Commission(BaseModel):
    promotions: dict[float, float]
    total: float
    order_avg: float


class Report(BaseModel):
    customers: int | None = None
    total_discount_amount: float | None = None
    items: int | None = None
    order_total_avg: float | None = None
    discount_rate_avg: float | None = None
    commissions: Commission | None = None

