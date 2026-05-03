"""
Range-based sales estimation for KiranaLens.

This module models supply and demand separately, then applies the constraint
model where feasible daily sales are capped by the smaller of the two ranges.
"""
from typing import Dict, Optional, Tuple

from app.utils.economic_variables import (
    calculate_competition_factor,
    calculate_demand_index,
    calculate_efficiency_factor,
    calculate_inventory_capacity,
    calculate_manual_adjustment,
    calculate_turnover_rate,
)


IntRange = Tuple[int, int]
FloatRange = Tuple[float, float]


def _ordered_int_range(low: float, high: float) -> IntRange:
    low_int = max(0, int(round(low)))
    high_int = max(low_int, int(round(high)))
    return (low_int, high_int)


def calculate_supply_sales(
    inventory_capacity: IntRange,
    turnover_days: IntRange
) -> IntRange:
    """
    Calculate supply-driven daily sales range.

    Args:
        inventory_capacity: Inventory value range in rupees.
        turnover_days: Turnover days range.

    Returns:
        Tuple of minimum and maximum daily sales in rupees.
    """
    min_inventory, max_inventory = inventory_capacity
    min_days, max_days = turnover_days
    min_days = max(1, min_days)
    max_days = max(min_days, max_days)
    return _ordered_int_range(min_inventory / max_days, max_inventory / min_days)


def calculate_demand_sales(
    demand_index: FloatRange,
    efficiency: FloatRange,
    competition: FloatRange,
    base_sales: IntRange = (8_000, 15_000)
) -> IntRange:
    """
    Calculate demand-driven daily sales range.

    Args:
        demand_index: Demand index range.
        efficiency: Efficiency factor range.
        competition: Competition factor range.
        base_sales: Base daily sales range.

    Returns:
        Tuple of minimum and maximum daily sales in rupees.
    """
    min_sales = base_sales[0] * demand_index[0] * efficiency[0] * competition[0]
    max_sales = base_sales[1] * demand_index[1] * efficiency[1] * competition[1]
    return _ordered_int_range(min_sales, max_sales)


def calculate_final_sales(
    supply_sales: IntRange,
    demand_sales: IntRange
) -> IntRange:
    """
    Calculate final daily sales using the supply-demand constraint.

    Args:
        supply_sales: Supply-driven daily sales range.
        demand_sales: Demand-driven daily sales range.

    Returns:
        Tuple of final minimum and maximum daily sales in rupees.
    """
    return (min(supply_sales[0], demand_sales[0]), min(supply_sales[1], demand_sales[1]))


def calculate_monthly_revenue(daily_sales: IntRange) -> IntRange:
    """
    Calculate monthly revenue range.

    Args:
        daily_sales: Daily sales range.

    Returns:
        Tuple of monthly revenue range in rupees.
    """
    return (daily_sales[0] * 30, daily_sales[1] * 30)


def determine_margin_range(visual_features: Dict) -> FloatRange:
    """
    Determine profit margin range based on inferred product mix.

    Args:
        visual_features: Visual feature dictionary from the vision pipeline.

    Returns:
        Tuple of minimum and maximum margin.
    """
    diversity = float(visual_features.get("sku_diversity_score", 50) or 50)
    inventory_band = str(visual_features.get("inventory_value_band", "medium")).lower()

    if diversity >= 70 and inventory_band in {"high", "very_high"}:
        return (0.18, 0.25)
    if diversity <= 35 or inventory_band == "low":
        return (0.08, 0.12)
    return (0.12, 0.18)


def calculate_monthly_income(
    monthly_revenue: IntRange,
    margin: FloatRange
) -> IntRange:
    """
    Calculate monthly income range.

    Args:
        monthly_revenue: Monthly revenue range.
        margin: Profit margin range.

    Returns:
        Tuple of monthly income range in rupees.
    """
    return _ordered_int_range(monthly_revenue[0] * margin[0], monthly_revenue[1] * margin[1])


def run_complete_estimation(
    visual_features: Dict,
    geo_features: Dict,
    optional_inputs: Optional[Dict] = None
) -> Dict:
    """
    Run the complete economic sales estimation pipeline.

    Args:
        visual_features: Visual feature dictionary from the vision pipeline.
        geo_features: Geographic feature dictionary from the geo pipeline.
        optional_inputs: Optional manual inputs such as rent, age, and size.

    Returns:
        Dictionary containing final ranges and intermediate calculations.
    """
    optional_inputs = optional_inputs or {}
    inventory_capacity = calculate_inventory_capacity(
        visual_features,
        optional_inputs.get("shop_size"),
    )
    turnover_days = calculate_turnover_rate(visual_features)
    demand_index = calculate_demand_index(geo_features)
    competition_factor = calculate_competition_factor(geo_features)
    efficiency_factor = calculate_efficiency_factor(visual_features)
    manual_adjustment = calculate_manual_adjustment(
        optional_inputs.get("rent"),
        optional_inputs.get("years_in_operation"),
        optional_inputs.get("shop_size"),
    )

    adjusted_efficiency = (
        max(0.7, efficiency_factor[0] * manual_adjustment[0]),
        min(1.2, efficiency_factor[1] * manual_adjustment[1]),
    )
    supply_sales = calculate_supply_sales(inventory_capacity, turnover_days)
    demand_sales = calculate_demand_sales(demand_index, adjusted_efficiency, competition_factor)
    daily_sales = calculate_final_sales(supply_sales, demand_sales)
    monthly_revenue = calculate_monthly_revenue(daily_sales)
    margin_range = determine_margin_range(visual_features)
    monthly_income = calculate_monthly_income(monthly_revenue, margin_range)

    return {
        "inventory_capacity": inventory_capacity,
        "turnover_days": turnover_days,
        "demand_index": demand_index,
        "competition_factor": competition_factor,
        "efficiency_factor": adjusted_efficiency,
        "manual_adjustment": manual_adjustment,
        "supply_sales": supply_sales,
        "demand_sales": demand_sales,
        "daily_sales_range": daily_sales,
        "monthly_revenue_range": monthly_revenue,
        "margin_range": margin_range,
        "monthly_income_range": monthly_income,
    }
