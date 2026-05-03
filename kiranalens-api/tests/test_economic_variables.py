from app.utils.economic_variables import (
    calculate_competition_factor,
    calculate_demand_index,
    calculate_efficiency_factor,
    calculate_inventory_capacity,
    calculate_manual_adjustment,
    calculate_turnover_rate,
)


def test_inventory_capacity_uses_band_and_visual_strength():
    result = calculate_inventory_capacity(
        {
            "inventory_value_band": "high",
            "shelf_density_index": 80,
            "sku_diversity_score": 70,
        }
    )

    assert result[0] >= 300_000
    assert result[1] > result[0]


def test_turnover_high_activity_partially_empty_is_fast():
    assert calculate_turnover_rate(
        {
            "refill_signal": "partially_empty",
            "counter_activity_proxy": 80,
            "store_organization_score": 65,
        }
    ) == (5, 7)


def test_demand_index_stays_in_bounds():
    result = calculate_demand_index(
        {
            "footfall_proxy_index": 100,
            "catchment_density_score": 100,
            "road_type_score": 100,
            "neighbourhood_quality_score": 100,
        }
    )

    assert result == (1.4, 1.5)


def test_competition_factor_drops_with_many_competitors():
    result = calculate_competition_factor(
        {"competition_density_score": 90, "competitor_count": 10}
    )

    assert 0.6 <= result[0] < 0.7
    assert result[1] <= 1.1


def test_efficiency_factor_uses_conversion_quality():
    low = calculate_efficiency_factor(
        {
            "store_organization_score": 20,
            "counter_activity_proxy": 20,
            "exterior_quality_score": 20,
        }
    )
    high = calculate_efficiency_factor(
        {
            "store_organization_score": 90,
            "counter_activity_proxy": 90,
            "exterior_quality_score": 90,
        }
    )

    assert low[1] < high[0]


def test_manual_adjustment_is_optional_and_bounded():
    neutral = calculate_manual_adjustment()
    strong = calculate_manual_adjustment(rent=35_000, years_in_operation=8, shop_size=450)

    assert neutral == (0.98, 1.02)
    assert strong[0] >= neutral[0]
    assert strong[1] <= 1.1
