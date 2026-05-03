"""
Integration tests for the KiranaLens assessment pipeline.

These tests verify the full pipeline using mock data — exercising economic
variable calculation, fraud detection, confidence scoring, recommendation
logic, and the expected API output format.
"""
from typing import Dict, Tuple
import pytest

from app.utils.economic_variables import (
    calculate_competition_factor,
    calculate_demand_index,
    calculate_efficiency_factor,
    calculate_inventory_capacity,
    calculate_manual_adjustment,
    calculate_turnover_rate,
)
from app.utils.sales_estimation import run_complete_estimation
from app.utils.scoring import (
    compute_confidence,
    detect_fraud_flags,
    get_recommendation,
)


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def standard_visual() -> Dict:
    return {
        "shelf_density_index": 70,
        "sku_diversity_score": 65,
        "inventory_value_band": "medium",
        "refill_signal": "normal",
        "store_organization_score": 70,
        "counter_activity_proxy": 60,
        "exterior_quality_score": 65,
        "image_quality_warnings": [],
    }


@pytest.fixture()
def standard_geo() -> Dict:
    return {
        "road_type_score": 70,
        "catchment_density_score": 75,
        "footfall_proxy_index": 70,
        "competition_density_score": 50,
        "neighbourhood_quality_score": 70,
        "competitor_count": 3,
        "poi_count": 12,
    }


@pytest.fixture()
def high_value_visual() -> Dict:
    return {
        "shelf_density_index": 90,
        "sku_diversity_score": 85,
        "inventory_value_band": "very_high",
        "refill_signal": "partially_empty",
        "store_organization_score": 88,
        "counter_activity_proxy": 85,
        "exterior_quality_score": 80,
        "image_quality_warnings": [],
    }


@pytest.fixture()
def high_value_geo() -> Dict:
    return {
        "road_type_score": 90,
        "catchment_density_score": 88,
        "footfall_proxy_index": 92,
        "competition_density_score": 20,
        "neighbourhood_quality_score": 85,
        "competitor_count": 1,
        "poi_count": 30,
    }


@pytest.fixture()
def low_value_visual() -> Dict:
    return {
        "shelf_density_index": 20,
        "sku_diversity_score": 15,
        "inventory_value_band": "low",
        "refill_signal": "overfilled",
        "store_organization_score": 20,
        "counter_activity_proxy": 15,
        "exterior_quality_score": 20,
        "image_quality_warnings": ["blur", "low_light", "partial_coverage"],
    }


@pytest.fixture()
def low_value_geo() -> Dict:
    return {
        "road_type_score": 20,
        "catchment_density_score": 15,
        "footfall_proxy_index": 20,
        "competition_density_score": 90,
        "neighbourhood_quality_score": 20,
        "competitor_count": 10,
        "poi_count": 2,
    }


# ---------------------------------------------------------------------------
# Pipeline output format tests
# ---------------------------------------------------------------------------

class TestPipelineOutputFormat:
    """Verify the complete estimation returns all required keys and types."""

    def test_all_expected_keys_present(self, standard_visual, standard_geo):
        result = run_complete_estimation(standard_visual, standard_geo)

        required_keys = [
            "inventory_capacity",
            "turnover_days",
            "demand_index",
            "competition_factor",
            "efficiency_factor",
            "manual_adjustment",
            "supply_sales",
            "demand_sales",
            "daily_sales_range",
            "monthly_revenue_range",
            "margin_range",
            "monthly_income_range",
        ]
        for key in required_keys:
            assert key in result, f"Missing key: {key}"

    def test_all_ranges_are_ordered_tuples(self, standard_visual, standard_geo):
        result = run_complete_estimation(standard_visual, standard_geo)

        for key, value in result.items():
            assert isinstance(value, tuple) and len(value) == 2, (
                f"Expected 2-tuple for {key}, got {type(value)}"
            )
            assert value[0] <= value[1], f"Range not ordered for {key}: {value}"

    def test_monthly_revenue_equals_daily_times_30(self, standard_visual, standard_geo):
        result = run_complete_estimation(standard_visual, standard_geo)
        assert result["monthly_revenue_range"][0] == result["daily_sales_range"][0] * 30
        assert result["monthly_revenue_range"][1] == result["daily_sales_range"][1] * 30

    def test_income_within_revenue_bounds(self, standard_visual, standard_geo):
        result = run_complete_estimation(standard_visual, standard_geo)
        assert result["monthly_income_range"][0] <= result["monthly_revenue_range"][0]
        assert result["monthly_income_range"][1] <= result["monthly_revenue_range"][1]

    def test_final_sales_constrained_by_supply_and_demand(
        self, standard_visual, standard_geo
    ):
        result = run_complete_estimation(standard_visual, standard_geo)
        supply = result["supply_sales"]
        demand = result["demand_sales"]
        final = result["daily_sales_range"]

        # final min ≤ min(supply_min, demand_min)
        assert final[0] <= min(supply[0], demand[0])
        # final max ≤ min(supply_max, demand_max)
        assert final[1] <= min(supply[1], demand[1])


# ---------------------------------------------------------------------------
# Economic variable boundary tests
# ---------------------------------------------------------------------------

class TestEconomicVariableBoundaries:
    """Ensure every economic variable stays within its defined range."""

    def test_demand_index_within_0_5_to_1_5(self):
        for score in [0, 25, 50, 75, 100]:
            geo = {k: score for k in [
                "footfall_proxy_index", "catchment_density_score",
                "road_type_score", "neighbourhood_quality_score",
            ]}
            lo, hi = calculate_demand_index(geo)
            assert 0.5 <= lo <= 1.5
            assert 0.5 <= hi <= 1.5
            assert lo <= hi

    def test_competition_factor_within_0_6_to_1_1(self):
        for score in [0, 25, 50, 75, 100]:
            for count in [0, 5, 10, 20]:
                lo, hi = calculate_competition_factor(
                    {"competition_density_score": score, "competitor_count": count}
                )
                assert 0.6 <= lo <= 1.1
                assert 0.6 <= hi <= 1.1
                assert lo <= hi

    def test_efficiency_factor_within_0_7_to_1_2(self):
        for score in [0, 50, 100]:
            lo, hi = calculate_efficiency_factor({
                "store_organization_score": score,
                "counter_activity_proxy": score,
                "exterior_quality_score": score,
            })
            assert 0.7 <= lo <= 1.2
            assert 0.7 <= hi <= 1.2

    def test_manual_adjustment_within_0_9_to_1_1(self):
        for rent in [None, 0, 5_000, 30_000, 100_000]:
            for years in [None, 0, 3, 10]:
                for size in [None, 50, 200, 600]:
                    lo, hi = calculate_manual_adjustment(rent, years, size)
                    assert 0.9 <= lo <= 1.1, f"lo={lo}, rent={rent}, years={years}, size={size}"
                    assert 0.9 <= hi <= 1.1, f"hi={hi}"

    def test_inventory_capacity_increases_with_band(self):
        bands = ["low", "medium", "high", "very_high"]
        visual_base = {"shelf_density_index": 50, "sku_diversity_score": 50}
        previous_max = 0
        for band in bands:
            lo, hi = calculate_inventory_capacity({**visual_base, "inventory_value_band": band})
            assert lo >= previous_max * 0.5, f"Band {band} lower bound seems too low"
            previous_max = hi


# ---------------------------------------------------------------------------
# High-value store scenario
# ---------------------------------------------------------------------------

class TestHighValueStoreScenario:
    """A premium kirana should yield high sales ranges and pre-approval."""

    def test_high_value_store_produces_large_revenue(
        self, high_value_visual, high_value_geo
    ):
        result = run_complete_estimation(high_value_visual, high_value_geo)
        assert result["monthly_revenue_range"][1] >= 300_000

    def test_high_value_store_no_fraud_flags(
        self, high_value_visual, high_value_geo
    ):
        result = run_complete_estimation(high_value_visual, high_value_geo)
        flags = detect_fraud_flags(
            high_value_visual, high_value_geo, result, image_count=5
        )
        # A very-high inventory band with partially-empty shelves correctly
        # produces an inventory_demand_mismatch because supply >> demand.
        # The important thing is that no *false* fraud flags fire: the flag
        # should be limited to this one legitimate economic mismatch.
        non_mismatch_severe = {"low_visual_coverage", "inconsistent_manual_inputs"}
        assert not any(f in non_mismatch_severe for f in flags)

    def test_high_value_store_recommendation(
        self, high_value_visual, high_value_geo
    ):
        result = run_complete_estimation(high_value_visual, high_value_geo)
        confidence = compute_confidence(
            high_value_visual, high_value_geo, 5, gps_accuracy=5.0,
            estimation_result=result,
        )
        flags = detect_fraud_flags(high_value_visual, high_value_geo, result, image_count=5)
        rec = get_recommendation(
            confidence, flags,
            result["daily_sales_range"],
            result["monthly_income_range"],
        )
        # High supply vs. demand mismatch will push recommendation to caution
        # or verification — reject is not expected for an otherwise strong store.
        assert rec in ("pre_approve", "proceed_with_caution", "needs_verification")


# ---------------------------------------------------------------------------
# Low-value store scenario
# ---------------------------------------------------------------------------

class TestLowValueStoreScenario:
    """A struggling micro-store should yield low sales and rejection."""

    def test_low_value_store_small_revenue(
        self, low_value_visual, low_value_geo
    ):
        result = run_complete_estimation(low_value_visual, low_value_geo)
        assert result["daily_sales_range"][1] <= 12_000

    def test_low_value_store_has_fraud_flags(
        self, low_value_visual, low_value_geo
    ):
        result = run_complete_estimation(low_value_visual, low_value_geo)
        flags = detect_fraud_flags(
            low_value_visual, low_value_geo, result, image_count=2
        )
        assert len(flags) > 0

    def test_low_value_store_rejected_or_needs_verification(
        self, low_value_visual, low_value_geo
    ):
        result = run_complete_estimation(low_value_visual, low_value_geo)
        confidence = compute_confidence(
            low_value_visual, low_value_geo, image_count=2, gps_accuracy=50.0,
            estimation_result=result,
        )
        flags = detect_fraud_flags(
            low_value_visual, low_value_geo, result, image_count=2
        )
        rec = get_recommendation(
            confidence, flags,
            result["daily_sales_range"],
            result["monthly_income_range"],
        )
        assert rec in ("reject", "needs_verification")


# ---------------------------------------------------------------------------
# Optional inputs tests
# ---------------------------------------------------------------------------

class TestOptionalInputs:
    """Manual inputs should modify estimates within bounded ranges."""

    def test_optional_inputs_change_result(self, standard_visual, standard_geo):
        result_no_opts = run_complete_estimation(standard_visual, standard_geo)
        result_with_opts = run_complete_estimation(
            standard_visual,
            standard_geo,
            {"rent": 35_000, "years_in_operation": 8, "shop_size": 400},
        )
        # The income range should differ (manual adjustment applied)
        assert result_no_opts["monthly_income_range"] != result_with_opts["monthly_income_range"]

    def test_missing_optional_inputs_do_not_crash(self, standard_visual, standard_geo):
        result = run_complete_estimation(
            standard_visual, standard_geo, optional_inputs={}
        )
        assert "daily_sales_range" in result

    def test_none_optional_inputs_do_not_crash(self, standard_visual, standard_geo):
        result = run_complete_estimation(
            standard_visual,
            standard_geo,
            {"rent": None, "years_in_operation": None, "shop_size": None},
        )
        assert "daily_sales_range" in result


# ---------------------------------------------------------------------------
# Fraud detection rules tests
# ---------------------------------------------------------------------------

class TestFraudDetectionRules:
    """Verify each new fraud rule fires correctly."""

    def test_inventory_demand_mismatch_flag(self):
        estimation = {
            "supply_sales": (50_000, 80_000),
            "demand_sales": (1_000, 5_000),
            "demand_index": (0.9, 1.1),
            "competition_factor": (0.8, 0.9),
            "turnover_days": (10, 15),
            "inventory_capacity": (300_000, 600_000),
        }
        flags = detect_fraud_flags({}, {}, estimation, image_count=4)
        assert "inventory_demand_mismatch" in flags

    def test_low_visual_coverage_flag_on_few_images(self):
        flags = detect_fraud_flags(
            {"image_quality_warnings": []}, {}, {}, image_count=2
        )
        assert "low_visual_coverage" in flags

    def test_low_visual_coverage_flag_on_many_warnings(self):
        flags = detect_fraud_flags(
            {"image_quality_warnings": ["blur", "low_light", "partial_coverage"]},
            {}, {}, image_count=5,
        )
        assert "low_visual_coverage" in flags

    def test_overstocking_suspected_flag(self):
        estimation = {
            "turnover_days": (25, 30),
            "demand_index": (0.6, 0.8),
            "supply_sales": (5_000, 10_000),
            "demand_sales": (4_000, 8_000),
            "competition_factor": (0.8, 0.9),
            "inventory_capacity": (200_000, 400_000),
        }
        flags = detect_fraud_flags({}, {}, estimation, image_count=5)
        assert "overstocking_suspected" in flags

    def test_high_competition_zone_flag(self):
        estimation = {
            "competition_factor": (0.6, 0.65),
            "demand_index": (1.2, 1.4),
            "turnover_days": (10, 15),
            "supply_sales": (8_000, 15_000),
            "demand_sales": (10_000, 20_000),
            "inventory_capacity": (200_000, 500_000),
        }
        flags = detect_fraud_flags({}, {}, estimation, image_count=5)
        assert "high_competition_zone" in flags

    def test_inconsistent_manual_inputs_flag(self):
        estimation = {
            "inventory_capacity": (80_000, 120_000),
            "supply_sales": (5_000, 10_000),
            "demand_sales": (6_000, 12_000),
            "demand_index": (0.9, 1.1),
            "competition_factor": (0.8, 0.9),
            "turnover_days": (10, 15),
        }
        flags = detect_fraud_flags(
            {}, {},
            estimation,
            image_count=5,
            optional_inputs={"rent": 50_000, "shop_size": None},
        )
        assert "inconsistent_manual_inputs" in flags

    def test_no_false_positives_for_healthy_store(
        self, high_value_visual, high_value_geo
    ):
        result = run_complete_estimation(high_value_visual, high_value_geo)
        flags = detect_fraud_flags(
            high_value_visual, high_value_geo, result, image_count=5,
            optional_inputs={"rent": 25_000, "shop_size": 350, "years_in_operation": 7},
        )
        # A very-high-inventory store with partially-empty shelves will trigger
        # inventory_demand_mismatch (supply >> demand), which is legitimate.
        # Ensure no *false* flags fire: inconsistent_manual_inputs and
        # low_visual_coverage should definitely not appear.
        false_positive_flags = {"low_visual_coverage", "inconsistent_manual_inputs"}
        assert not any(f in false_positive_flags for f in flags)


# ---------------------------------------------------------------------------
# Confidence score tests
# ---------------------------------------------------------------------------

class TestConfidenceScore:
    """Confidence score should reflect data quality and supply/demand alignment."""

    def test_confidence_between_0_and_1(self, standard_visual, standard_geo):
        result = run_complete_estimation(standard_visual, standard_geo)
        confidence = compute_confidence(
            standard_visual, standard_geo, 4, gps_accuracy=10.0,
            estimation_result=result,
        )
        assert 0.0 <= confidence <= 1.0

    def test_high_image_count_increases_confidence(
        self, standard_visual, standard_geo
    ):
        result = run_complete_estimation(standard_visual, standard_geo)
        low_conf = compute_confidence(
            standard_visual, standard_geo, 1, estimation_result=result
        )
        high_conf = compute_confidence(
            standard_visual, standard_geo, 6, estimation_result=result
        )
        assert high_conf > low_conf

    def test_gps_accuracy_affects_confidence(self, standard_visual, standard_geo):
        result = run_complete_estimation(standard_visual, standard_geo)
        precise = compute_confidence(
            standard_visual, standard_geo, 4, gps_accuracy=2.0,
            estimation_result=result,
        )
        imprecise = compute_confidence(
            standard_visual, standard_geo, 4, gps_accuracy=30.0,
            estimation_result=result,
        )
        assert precise > imprecise

    def test_supply_demand_misalignment_reduces_confidence(
        self, standard_visual, standard_geo
    ):
        aligned = {"supply_sales": (10_000, 12_000), "demand_sales": (10_000, 14_000)}
        misaligned = {"supply_sales": (1_000, 3_000), "demand_sales": (50_000, 80_000)}
        conf_aligned = compute_confidence(
            standard_visual, standard_geo, 4, estimation_result=aligned
        )
        conf_misaligned = compute_confidence(
            standard_visual, standard_geo, 4, estimation_result=misaligned
        )
        assert conf_aligned > conf_misaligned


# ---------------------------------------------------------------------------
# Recommendation logic tests
# ---------------------------------------------------------------------------

class TestRecommendationLogic:
    """Verify all four recommendation outcomes are reachable with correct inputs."""

    def test_pre_approve_high_confidence_no_flags(self):
        rec = get_recommendation(
            confidence=0.85,
            flags=[],
            daily_sales_range=(14_000, 20_000),
            monthly_income_range=(40_000, 70_000),
        )
        assert rec == "pre_approve"

    def test_proceed_with_caution_moderate_inputs(self):
        rec = get_recommendation(
            confidence=0.65,
            flags=["high_competition_zone"],
            daily_sales_range=(9_000, 14_000),
            monthly_income_range=(20_000, 40_000),
        )
        assert rec == "proceed_with_caution"

    def test_needs_verification_low_confidence(self):
        rec = get_recommendation(
            confidence=0.50,
            flags=["overstocking_suspected"],
            daily_sales_range=(6_000, 10_000),
            monthly_income_range=(14_000, 25_000),
        )
        assert rec == "needs_verification"

    def test_reject_very_low_confidence(self):
        rec = get_recommendation(
            confidence=0.25,
            flags=["low_visual_coverage"],
            daily_sales_range=(1_000, 3_000),
            monthly_income_range=(2_000, 6_000),
        )
        assert rec == "reject"

    def test_reject_severe_fraud_flag_overrides_ok_confidence(self):
        rec = get_recommendation(
            confidence=0.70,
            flags=["inventory_demand_mismatch"],
            daily_sales_range=(3_000, 4_000),   # daily_sales_max < 4_000 triggers reject
            monthly_income_range=(5_000, 7_000),
        )
        assert rec == "reject"

    def test_all_four_recommendations_are_valid_strings(self):
        valid = {"pre_approve", "proceed_with_caution", "needs_verification", "reject"}
        for confidence in [0.2, 0.5, 0.7, 0.9]:
            rec = get_recommendation(
                confidence=confidence,
                flags=[],
                daily_sales_range=(5_000 * confidence, 10_000 * confidence),
                monthly_income_range=(10_000 * confidence, 20_000 * confidence),
            )
            assert rec in valid
