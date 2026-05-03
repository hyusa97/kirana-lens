"""
Scoring utilities for KiranaLens assessment pipeline
Pure functions for CSQS calculation, tier assignment, and risk assessment
"""
from typing import Dict, List, Tuple

# Signal weights - all 12 signals summing to 1.0
SIGNAL_WEIGHTS = {
    # Visual signals (60% total weight)
    "shelf_density_index": 0.12,
    "sku_diversity_score": 0.10,
    "inventory_value_band": 0.15,
    "refill_signal": 0.08,
    "store_organization_score": 0.08,
    "counter_activity_proxy": 0.04,
    "exterior_quality_score": 0.03,
    
    # Geographic signals (40% total weight)
    "road_type_score": 0.08,
    "catchment_density_score": 0.12,
    "footfall_proxy_index": 0.10,
    "competition_density_score": 0.06,
    "neighbourhood_quality_score": 0.04,
}

# Tier thresholds for CSQS scores
TIER_THRESHOLDS = {
    'A': (85, 100),  # Excellent
    'B': (70, 84),   # Good
    'C': (55, 69),   # Average
    'D': (40, 54),   # Below Average
    'E': (0, 39),    # Poor
}

# Revenue ranges by CSQS score (in rupees)
REVENUE_RANGES = {
    # Daily sales ranges
    'daily_sales': {
        'A': (15000, 25000),
        'B': (10000, 18000),
        'C': (6000, 12000),
        'D': (3000, 8000),
        'E': (1000, 4000),
    },
    # Monthly revenue ranges
    'monthly_revenue': {
        'A': (450000, 750000),
        'B': (300000, 540000),
        'C': (180000, 360000),
        'D': (90000, 240000),
        'E': (30000, 120000),
    },
    # Monthly income ranges (after expenses)
    'monthly_income': {
        'A': (45000, 75000),
        'B': (30000, 54000),
        'C': (18000, 36000),
        'D': (9000, 24000),
        'E': (3000, 12000),
    }
}

# Fraud detection rules
FRAUD_RULES = {
    'low_inventory_high_sales': {
        'condition': lambda v, g: v.get('inventory_value_band', 0) < 30 and v.get('counter_activity_proxy', 0) > 80,
        'message': 'Low inventory but high sales activity detected',
        'severity': 'high'
    },
    'poor_exterior_prime_location': {
        'condition': lambda v, g: v.get('exterior_quality_score', 0) < 30 and g.get('footfall_proxy_index', 0) > 70,
        'message': 'Poor store exterior in prime location',
        'severity': 'medium'
    },
    'overstocked_low_activity': {
        'condition': lambda v, g: v.get('refill_signal', '') == 'overfilled' and v.get('counter_activity_proxy', 0) < 30,
        'message': 'Overstocked inventory with low customer activity',
        'severity': 'medium'
    },
    'high_competition_low_differentiation': {
        'condition': lambda v, g: g.get('competition_density_score', 0) > 80 and v.get('sku_diversity_score', 0) < 40,
        'message': 'High competition area with low product differentiation',
        'severity': 'low'
    },
    'inconsistent_organization': {
        'condition': lambda v, g: abs(v.get('store_organization_score', 0) - v.get('shelf_density_index', 0)) > 40,
        'message': 'Inconsistent store organization and shelf management',
        'severity': 'low'
    }
}


def inventory_band_to_score(band: str) -> int:
    """
    Convert inventory value band to numeric score.
    
    Args:
        band: Inventory value band ('low', 'medium', 'high', 'very_high')
        
    Returns:
        int: Numeric score (20, 40, 70, 90)
    """
    band_scores = {
        'low': 20,
        'medium': 40,
        'high': 70,
        'very_high': 90
    }
    return band_scores.get(band.lower(), 20)


def refill_signal_to_score(signal: str) -> int:
    """
    Convert refill signal to numeric score.
    
    Args:
        signal: Refill signal ('partially_empty', 'normal', 'overfilled')
        
    Returns:
        int: Numeric score (80, 60, 30)
    """
    signal_scores = {
        'partially_empty': 80,  # Good - indicates active sales
        'normal': 60,           # Average - balanced inventory
        'overfilled': 30        # Poor - potential stagnant inventory
    }
    return signal_scores.get(signal.lower(), 60)


def compute_csqs(visual: Dict, geo: Dict) -> float:
    """
    Compute Credit Score Quality Score (CSQS) from visual and geographic features.
    
    Args:
        visual: Dictionary of visual features
        geo: Dictionary of geographic features
        
    Returns:
        float: CSQS score (0.0 to 100.0)
    """
    total_score = 0.0
    
    # Process visual features
    for signal, weight in SIGNAL_WEIGHTS.items():
        if signal in ['inventory_value_band', 'refill_signal']:
            # Handle categorical features
            if signal == 'inventory_value_band':
                score = inventory_band_to_score(visual.get(signal, 'low'))
            elif signal == 'refill_signal':
                score = refill_signal_to_score(visual.get(signal, 'normal'))
        else:
            # Handle numeric features
            if signal in visual:
                score = visual[signal]
            elif signal in geo:
                score = geo[signal]
            else:
                score = 50  # Default neutral score
        
        total_score += score * weight
    
    # Ensure score is within bounds
    return max(0.0, min(100.0, total_score))


def csqs_to_tier(csqs: float) -> str:
    """
    Convert CSQS score to store tier.
    
    Args:
        csqs: CSQS score (0.0 to 100.0)
        
    Returns:
        str: Store tier ('A', 'B', 'C', 'D', 'E')
    """
    for tier, (min_score, max_score) in TIER_THRESHOLDS.items():
        if min_score <= csqs <= max_score:
            return tier
    return 'E'  # Default to lowest tier


def csqs_to_revenue_ranges(csqs: float) -> Dict[str, int]:
    """
    Convert CSQS score to revenue ranges.
    
    Args:
        csqs: CSQS score (0.0 to 100.0)
        
    Returns:
        dict: Revenue ranges with min/max values
    """
    tier = csqs_to_tier(csqs)
    
    daily_min, daily_max = REVENUE_RANGES['daily_sales'][tier]
    monthly_rev_min, monthly_rev_max = REVENUE_RANGES['monthly_revenue'][tier]
    monthly_inc_min, monthly_inc_max = REVENUE_RANGES['monthly_income'][tier]
    
    return {
        'daily_sales_min': daily_min,
        'daily_sales_max': daily_max,
        'monthly_revenue_min': monthly_rev_min,
        'monthly_revenue_max': monthly_rev_max,
        'monthly_income_min': monthly_inc_min,
        'monthly_income_max': monthly_inc_max,
    }


def compute_confidence(
    visual_features: Dict,
    geo_features: Dict,
    image_count: int,
    gps_accuracy: float = None
) -> float:
    """
    Compute confidence score for the assessment.
    
    Args:
        visual_features: Visual analysis results
        geo_features: Geographic analysis results
        image_count: Number of images analyzed
        gps_accuracy: GPS accuracy in metres (optional)
        
    Returns:
        float: Confidence score (0.0 to 1.0)
    """
    confidence_factors = []
    
    # Image quality factor (0.4 weight)
    image_quality_warnings = visual_features.get('image_quality_warnings', [])
    image_quality_score = max(0.0, 1.0 - (len(image_quality_warnings) * 0.1))
    image_count_score = min(1.0, image_count / 5.0)  # Optimal at 5+ images
    image_factor = (image_quality_score + image_count_score) / 2
    confidence_factors.append(('image', image_factor, 0.4))
    
    # GPS accuracy factor (0.2 weight)
    if gps_accuracy is not None:
        gps_factor = max(0.0, min(1.0, (20 - gps_accuracy) / 20))  # Better accuracy = higher confidence
    else:
        gps_factor = 0.5  # Neutral if no GPS accuracy data
    confidence_factors.append(('gps', gps_factor, 0.2))
    
    # Feature consistency factor (0.4 weight)
    # Check consistency between related features
    consistency_checks = []
    
    # Organization vs shelf density consistency
    org_score = visual_features.get('store_organization_score', 50)
    shelf_score = visual_features.get('shelf_density_index', 50)
    org_consistency = 1.0 - abs(org_score - shelf_score) / 100.0
    consistency_checks.append(org_consistency)
    
    # Location quality vs exterior quality consistency
    location_score = geo_features.get('neighbourhood_quality_score', 50)
    exterior_score = visual_features.get('exterior_quality_score', 50)
    location_consistency = 1.0 - abs(location_score - exterior_score) / 100.0
    consistency_checks.append(location_consistency)
    
    # Competition vs differentiation consistency
    competition_score = geo_features.get('competition_density_score', 50)
    diversity_score = visual_features.get('sku_diversity_score', 50)
    # High competition should correlate with high diversity
    competition_consistency = 1.0 - abs((100 - competition_score) - diversity_score) / 100.0
    consistency_checks.append(competition_consistency)
    
    consistency_factor = sum(consistency_checks) / len(consistency_checks)
    confidence_factors.append(('consistency', consistency_factor, 0.4))
    
    # Calculate weighted confidence
    total_confidence = sum(score * weight for _, score, weight in confidence_factors)
    
    return max(0.0, min(1.0, total_confidence))


def detect_fraud_flags(visual_features: Dict, geo_features: Dict) -> List[str]:
    """
    Detect potential fraud flags based on feature analysis.
    
    Args:
        visual_features: Visual analysis results
        geo_features: Geographic analysis results
        
    Returns:
        list: List of fraud flag messages
    """
    flags = []
    
    for rule_name, rule_config in FRAUD_RULES.items():
        try:
            if rule_config['condition'](visual_features, geo_features):
                flags.append(rule_config['message'])
        except (KeyError, TypeError, ValueError):
            # Skip rule if data is missing or invalid
            continue
    
    return flags


def get_recommendation(confidence: float, flags: List[str], csqs: float) -> str:
    """
    Get recommendation based on confidence, flags, and CSQS score.
    
    Args:
        confidence: Confidence score (0.0 to 1.0)
        flags: List of fraud flags
        csqs: CSQS score (0.0 to 100.0)
        
    Returns:
        str: Recommendation ('pre_approve', 'needs_verification', 'reject')
    """
    # Immediate rejection criteria
    if csqs < 25 or confidence < 0.3:
        return 'reject'
    
    # High-risk flags that require verification
    high_risk_keywords = ['high sales activity', 'poor store exterior', 'overstocked']
    has_high_risk_flags = any(
        any(keyword in flag.lower() for keyword in high_risk_keywords)
        for flag in flags
    )
    
    # Pre-approval criteria
    if (csqs >= 70 and 
        confidence >= 0.8 and 
        len(flags) == 0):
        return 'pre_approve'
    
    # Needs verification criteria
    if (csqs >= 40 and 
        confidence >= 0.5 and 
        (len(flags) <= 2 and not has_high_risk_flags)):
        return 'needs_verification'
    
    # Default to rejection for remaining cases
    return 'reject'


def validate_signal_weights() -> bool:
    """
    Validate that signal weights sum to 1.0.
    
    Returns:
        bool: True if weights are valid
    """
    total_weight = sum(SIGNAL_WEIGHTS.values())
    return abs(total_weight - 1.0) < 0.001  # Allow for floating point precision


def get_signal_importance_ranking() -> List[Tuple[str, float]]:
    """
    Get signals ranked by importance (weight).
    
    Returns:
        list: List of (signal_name, weight) tuples sorted by weight descending
    """
    return sorted(SIGNAL_WEIGHTS.items(), key=lambda x: x[1], reverse=True)


def get_tier_distribution_thresholds() -> Dict[str, Dict[str, float]]:
    """
    Get tier distribution with thresholds and midpoints.
    
    Returns:
        dict: Tier information with thresholds and midpoints
    """
    tier_info = {}
    for tier, (min_score, max_score) in TIER_THRESHOLDS.items():
        tier_info[tier] = {
            'min_score': min_score,
            'max_score': max_score,
            'midpoint': (min_score + max_score) / 2,
            'range': max_score - min_score + 1
        }
    return tier_info