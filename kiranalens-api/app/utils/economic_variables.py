"""
Economic variable mapping for the KiranaLens underwriting model.

The functions in this module convert visual and geographic signals into
interpretable ranges used by the supply and demand sales estimator.
"""
from typing import Dict, Optional, Tuple


ScoreRange = Tuple[float, float]
RupeeRange = Tuple[int, int]
DayRange = Tuple[int, int]


def _clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))


def _score(features: Dict, key: str, default: float = 50.0) -> float:
    try:
        return float(features.get(key, default))
    except (TypeError, ValueError):
        return default


def calculate_inventory_capacity(
    visual_features: Dict,
    store_size: Optional[float] = None
) -> RupeeRange:
    """
    Calculate inventory capacity range from visual supply-side features.

    Args:
        visual_features: Visual feature dictionary from the vision pipeline.
        store_size: Optional shop size in square feet.

    Returns:
        Tuple of minimum and maximum inventory value in rupees.
    """
    band = str(visual_features.get("inventory_value_band", "medium")).lower()
    band_ranges = {
        "low": (50_000, 100_000),
        "medium": (100_000, 300_000),
        "high": (300_000, 700_000),
        "very_high": (700_000, 1_500_000),
    }
    base_min, base_max = band_ranges.get(band, band_ranges["medium"])

    shelf = _score(visual_features, "shelf_density_index")
    diversity = _score(visual_features, "sku_diversity_score")
    signal_strength = ((shelf * 0.6) + (diversity * 0.4) - 50.0) / 100.0
    multiplier = _clamp(1.0 + signal_strength, 0.75, 1.25)

    if store_size is not None and store_size > 0:
        if store_size < 120:
            multiplier *= 0.85
        elif store_size > 500:
            multiplier *= 1.15

    return (int(round(base_min * multiplier)), int(round(base_max * multiplier)))


def calculate_turnover_rate(visual_features: Dict) -> DayRange:
    """
    Calculate inventory turnover days from velocity-related visual features.

    Args:
        visual_features: Visual feature dictionary from the vision pipeline.

    Returns:
        Tuple of minimum and maximum turnover days.
    """
    refill_signal = str(visual_features.get("refill_signal", "normal")).lower()
    activity = _score(visual_features, "counter_activity_proxy")
    organization = _score(visual_features, "store_organization_score")

    if refill_signal == "partially_empty" and activity >= 65:
        return (5, 7)
    if refill_signal == "overfilled" or activity < 35:
        if organization < 45 or activity < 25:
            return (20, 30)
        return (15, 25)
    if activity >= 75 and organization >= 60:
        return (7, 10)
    return (10, 15)


def calculate_demand_index(geo_features: Dict) -> ScoreRange:
    """
    Calculate demand potential index from location demand signals.

    Args:
        geo_features: Geographic feature dictionary from the geo pipeline.

    Returns:
        Tuple of minimum and maximum demand index in the range 0.5 to 1.5.
    """
    weighted_score = (
        _score(geo_features, "footfall_proxy_index") * 0.35
        + _score(geo_features, "catchment_density_score") * 0.30
        + _score(geo_features, "road_type_score") * 0.20
        + _score(geo_features, "neighbourhood_quality_score") * 0.15
    )
    center = 0.5 + (weighted_score / 100.0)
    return (_clamp(center - 0.10, 0.5, 1.5), _clamp(center + 0.10, 0.5, 1.5))


def calculate_competition_factor(geo_features: Dict) -> ScoreRange:
    """
    Calculate competition pressure factor.

    Args:
        geo_features: Geographic feature dictionary from the geo pipeline.

    Returns:
        Tuple of minimum and maximum competition factor in the range 0.6 to 1.1.
    """
    competition_score = _score(geo_features, "competition_density_score")
    competitor_count = int(_score(geo_features, "competitor_count", 0))

    pressure = (competition_score / 100.0) * 0.75 + min(competitor_count, 10) / 10.0 * 0.25
    center = 1.1 - (pressure * 0.5)
    return (_clamp(center - 0.05, 0.6, 1.1), _clamp(center + 0.05, 0.6, 1.1))


def calculate_efficiency_factor(visual_features: Dict) -> ScoreRange:
    """
    Calculate conversion efficiency from store execution quality.

    Args:
        visual_features: Visual feature dictionary from the vision pipeline.

    Returns:
        Tuple of minimum and maximum efficiency factor in the range 0.7 to 1.2.
    """
    weighted_score = (
        _score(visual_features, "store_organization_score") * 0.45
        + _score(visual_features, "counter_activity_proxy") * 0.35
        + _score(visual_features, "exterior_quality_score") * 0.20
    )
    center = 0.7 + (weighted_score / 100.0) * 0.5
    return (_clamp(center - 0.07, 0.7, 1.2), _clamp(center + 0.07, 0.7, 1.2))


def calculate_manual_adjustment(
    rent: Optional[float] = None,
    years_in_operation: Optional[int] = None,
    shop_size: Optional[float] = None
) -> ScoreRange:
    """
    Calculate optional manual adjustment factor.

    Args:
        rent: Optional monthly rent in rupees.
        years_in_operation: Optional operating history in years.
        shop_size: Optional shop size in square feet.

    Returns:
        Tuple of minimum and maximum adjustment factor in the range 0.9 to 1.1.
    """
    adjustment = 1.0

    if years_in_operation is not None:
        if years_in_operation >= 5:
            adjustment += 0.04
        elif years_in_operation < 1:
            adjustment -= 0.04

    if shop_size is not None:
        if shop_size >= 350:
            adjustment += 0.03
        elif shop_size < 100:
            adjustment -= 0.03

    if rent is not None:
        if rent >= 30_000:
            adjustment += 0.02
        elif 0 < rent < 5_000:
            adjustment -= 0.02

    center = _clamp(adjustment, 0.9, 1.1)
    return (_clamp(center - 0.02, 0.9, 1.1), _clamp(center + 0.02, 0.9, 1.1))
