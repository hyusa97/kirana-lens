from app.utils.sales_estimation import (
    calculate_demand_sales,
    calculate_final_sales,
    calculate_monthly_income,
    calculate_monthly_revenue,
    calculate_supply_sales,
    determine_margin_range,
    run_complete_estimation,
)


def test_supply_sales_divides_inventory_by_turnover_days():
    assert calculate_supply_sales((100_000, 300_000), (10, 20)) == (5_000, 30_000)


def test_demand_sales_combines_base_demand_efficiency_and_competition():
    result = calculate_demand_sales((1.0, 1.2), (0.9, 1.1), (0.8, 1.0))

    assert result == (5_760, 19_800)


def test_final_sales_applies_constraint_model():
    assert calculate_final_sales((20_000, 40_000), (10_000, 18_000)) == (10_000, 18_000)


def test_monthly_revenue_and_income_ranges():
    revenue = calculate_monthly_revenue((10_000, 20_000))
    income = calculate_monthly_income(revenue, (0.12, 0.18))

    assert revenue == (300_000, 600_000)
    assert income == (36_000, 108_000)


def test_margin_range_detects_fmcg_heavy_store():
    margin = determine_margin_range({"sku_diversity_score": 80, "inventory_value_band": "high"})

    assert margin == (0.18, 0.25)


def test_complete_estimation_returns_all_expected_ranges():
    result = run_complete_estimation(
        {
            "shelf_density_index": 70,
            "sku_diversity_score": 65,
            "inventory_value_band": "medium",
            "refill_signal": "normal",
            "store_organization_score": 70,
            "counter_activity_proxy": 60,
            "exterior_quality_score": 65,
        },
        {
            "road_type_score": 70,
            "catchment_density_score": 75,
            "footfall_proxy_index": 70,
            "competition_density_score": 50,
            "neighbourhood_quality_score": 70,
            "competitor_count": 3,
        },
    )

    assert result["daily_sales_range"][0] <= result["daily_sales_range"][1]
    assert result["monthly_revenue_range"][0] == result["daily_sales_range"][0] * 30
    assert "supply_sales" in result
    assert "demand_sales" in result
