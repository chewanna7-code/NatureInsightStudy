"""
================================================================================
ITALIAN FLAG EVIDENCE SCORING FOR NBS INTERVENTIONS - WANSBECK CATCHMENT
================================================================================

Methodology:
- Evidence scored across 10 trade-off categories (Storage, Habitat, Carbon, 
  Cost, Cost Effectiveness, Time to Effectiveness, Durability, Stakeholder 
  Risk, Policy Alignment, Disservices Risk)
- Literature density (Google Scholar papers) informs uncertainty
- NatureInsight metrics (storage, carbon, habitat, cost, recommendations) 
  inform performance
- Scores are PROPORTIONS: Green + White + Red = 100%

Color Meanings:
- GREEN: Evidence FOR success (benefits, proven mechanisms, strong performance)
- WHITE: Uncertainty/fuzziness (evidence gaps, conflicting data, unknowns)
- RED: Evidence AGAINST/Concerns (high costs, risks, barriers, disservices)

Author: Generated for Anna Chew's MEng Dissertation
Date: May 2026
================================================================================
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ============================================================================
# SECTION 1: REFERENCE DATA
# ============================================================================

# Literature Evidence Base (Google Scholar paper counts)
# Higher count = more research = lower uncertainty from lack of information
LITERATURE_COUNTS = {
    'Tree Planting': 8390,           # MASSIVE - very low lit uncertainty
    'Peat Management': 7190,         # Very large
    'Soil Management': 7160,         # Very large
    'Buffer Strips': 1600,           # Moderate
    'RAFs': 1410,                    # Moderate
    'LWD': 1150,                     # Moderate-low
    'Floodplain Reconnection': 1120, # Moderate-low
    'Wet Woodland': 415,             # Small - high lit uncertainty
    'Grip Blocking': 172,            # Very small - very high lit uncertainty
    'Gully Stuffing': 89             # TINY - extreme lit uncertainty
}

# NatureInsight Performance Data (T70 threshold)
# From dissertation tables: opportunities, storage, cost, carbon, habitat, rankings
NATUREINSIGHT_DATA = {
    'RAFs': {
        'opportunities': 1193,       # NI: Highly recommended (most sites)
        'storage': 596500,           # NI: Strong storage capacity
        'cost': 7754500,             # NI: High total cost but distributed
        'carbon_net': 85.50,         # NI: Minimal carbon benefit
        'habitat_net': 1200.71,      # NI: Moderate habitat benefit
        'storage_per_£_rank': 6,     # NI: Mid-range storage cost-effectiveness
        'carbon_per_£_rank': 3,      # NI: Poor carbon value
        'habitat_per_£_rank': 4      # NI: Mid-range habitat value
    },
    'Floodplain Reconnection': {
        'opportunities': 279,        # NI: Fewer sites (site-limited)
        'storage': 279000,           # NI: Excellent storage
        'cost': 4603500,             # NI: Very high cost
        'carbon_net': 64.95,         # NI: Minimal carbon
        'habitat_net': 2334.24,      # NI: BEST habitat benefit
        'storage_per_£_rank': 5,     # NI: Mid-range storage value
        'carbon_per_£_rank': 4,      # NI: Poor carbon value
        'habitat_per_£_rank': 5      # NI: Mid-range habitat value
    },
    'LWD': {
        'opportunities': 564,        # NI: Moderate recommendations
        'storage': 56400,            # NI: Low storage
        'cost': 3243000,             # NI: Moderate-high cost
        'carbon_net': 0.00,          # NI: ZERO net carbon (!)
        'habitat_net': 0.00,         # NI: ZERO net habitat (contradicts lit!)
        'storage_per_£_rank': 2,     # NI: Good storage cost-effectiveness
        'carbon_per_£_rank': 1,      # NI: Worst carbon value (zero benefit)
        'habitat_per_£_rank': 1      # NI: Worst habitat value (contradicts lit biodiversity claims)
    },
    'Tree Planting': {
        'opportunities': 240,        # NI: Fewer opportunities
        'storage': 7816.88,          # NI: Very low storage (time lag issue)
        'cost': 858437.50,           # NI: Low-moderate cost
        'carbon_net': 5413.86,       # NI: EXCELLENT carbon sequestration
        'habitat_net': 3135.77,      # NI: Strong habitat creation
        'storage_per_£_rank': 1,     # NI: BEST storage cost-effectiveness
        'carbon_per_£_rank': 7,      # NI: Good carbon value
        'habitat_per_£_rank': 7      # NI: Good habitat value
    },
    'Wet Woodland': {
        'opportunities': 183,        # NI: Limited opportunities (site-specific)
        'storage': 92365.63,         # NI: Good storage
        'cost': 564375,              # NI: Moderate cost
        'carbon_net': 3845.54,       # NI: Strong carbon
        'habitat_net': 4069.42,      # NI: Strong habitat
        'storage_per_£_rank': 7,     # NI: Good storage value
        'carbon_per_£_rank': 8,      # NI: Good carbon value
        'habitat_per_£_rank': 9      # NI: BEST habitat cost-effectiveness
    },
    'Buffer Strips': {
        'opportunities': 974,        # NI: Highly recommended
        'storage': 14937.50,         # NI: Very low storage (not primary flood tool)
        'cost': 834350,              # NI: Low cost
        'carbon_net': 2202.11,       # NI: Moderate carbon
        'habitat_net': 4507.76,      # NI: Good habitat
        'storage_per_£_rank': 3,     # NI: Good storage value (but low absolute)
        'carbon_per_£_rank': 6,      # NI: Moderate carbon value
        'habitat_per_£_rank': 8      # NI: Good habitat value
    },
    'Soil Management': {
        'opportunities': 1101,       # NI: Second-most recommended
        'storage': 109715.63,        # NI: Good storage
        'cost': 660375,              # NI: Low cost
        'carbon_net': 6724.21,       # NI: BEST carbon sequestration
        'habitat_net': 0.00,         # NI: ZERO habitat benefit
        'storage_per_£_rank': 8,     # NI: Good storage value
        'carbon_per_£_rank': 9,      # NI: BEST carbon cost-effectiveness
        'habitat_per_£_rank': 2      # NI: No habitat (rank 2 = second worst)
    },
    'Gully Stuffing': {
        'opportunities': 163,        # NI: Limited opportunities
        'storage': 1630,             # NI: Very low storage
        'cost': 40750,               # NI: Very low cost
        'carbon_net': 0.00,          # NI: No carbon
        'habitat_net': 0.00,         # NI: No habitat
        'storage_per_£_rank': 4,     # NI: Mid-range storage value
        'carbon_per_£_rank': 2,      # NI: Poor carbon value (zero)
        'habitat_per_£_rank': 3      # NI: Poor habitat value (zero)
    },
    'Grip Blocking': {
        'opportunities': 94,         # NI: Least recommended (limited applicability)
        'storage': 37600,            # NI: Low storage
        'cost': 58750,               # NI: Very low cost
        'carbon_net': 14.59,         # NI: Minimal carbon
        'habitat_net': 145.12,       # NI: Minimal habitat
        'storage_per_£_rank': 9,     # NI: BEST storage per £ (low cost helps)
        'carbon_per_£_rank': 5,      # NI: Moderate carbon value
        'habitat_per_£_rank': 6      # NI: Moderate habitat value
    }
}

# ============================================================================
# SECTION 2: ITALIAN FLAG SCORES
# ============================================================================
# Each intervention scored based on:
# - Literature evidence (mechanisms, case studies, field validation)
# - NatureInsight performance (storage, carbon, habitat, cost, recommendations)
# - Wansbeck context (geomorphology, flood type, land availability)
# Across 10 trade-off categories synthesized into overall proportions

ITALIAN_FLAGS = {
    
    # ------------------------------------------------------------------------
    'RAFs': {
        'green': 65,
        'white': 20,
        'red': 15,
        'notes': {
            'green': [
                'NI: Highly recommended (1193 opportunities - most of all interventions)',
                'NI: Strong storage capacity (596,500 m³)',
                'NI: Immediate effect upon installation (no time lag)',
                'Lit: Proven surface water management mechanism (1410 papers)',
                'Lit: Sediment trapping and water quality co-benefits documented',
                'Wansbeck: Suitable for upland moorland areas with rapid runoff'
            ],
            'white': [
                'NI: Mid-range cost-effectiveness (rank 6 storage/£, rank 3-4 co-benefits)',
                'Lit: Network effects difficult to quantify for distributed measures',
                'Lit: Limited field validation at catchment scale',
                'Lit: Extreme event performance (1-in-100 year) unclear',
                'Lit: Moderate evidence base (1410 papers) - not tiny, but some gaps'
            ],
            'red': [
                'NI: High total cost (£7.75M) though distributed across many sites',
                'Lit: Land-take constraints limit widespread deployment',
                'Lit: Minimal impact once storage capacity reached'
            ]
        }
    },
    
    # ------------------------------------------------------------------------
    'Floodplain Reconnection': {
        'green': 65,
        'white': 15,
        'red': 20,  # Higher red: very high cost £16.5k/site, complex consents, site-limited
        'notes': {
            'green': [
                'NI: Excellent storage (279,000 m³ - second highest)',
                'NI: BEST habitat benefit (2334 net units)',
                'Lit: "Top performer" for fluvial flood risk in literature review',
                'Lit: Natural process restoration with multiple co-benefits',
                'Lit: 1120 papers = moderate-low evidence base',
                'Wansbeck: Suitable floodplain areas in lower catchment near Morpeth'
            ],
            'white': [
                'NI: Mid-range cost-effectiveness despite strong absolute performance',
                'Lit: Standard of protection highly site-specific',
                'Lit: Groundwater interaction effects poorly understood',
                'Lit: Field validation gaps across different spatial scales'
            ],
            'red': [
                'NI: Very high cost (£4.6M for 279 sites = £16.5k/site)',
                'Lit: Complex hydraulic modeling requirements',
                'Lit: Extensive legal consent process',
                'Lit: Long planning and implementation timelines',
                'Wansbeck: Limited to lower catchment - not applicable upland'
            ]
        }
    },
    
    # ------------------------------------------------------------------------
    'LWD': {
        'green': 45,
        'white': 25,
        'red': 30,
        'notes': {
            'green': [
                'NI: 564 opportunities across catchment',
                'NI: Rank 2 storage cost-effectiveness (good value)',
                'NI: Low cost (£3.24M / 564 sites = £5.7k/site)',
                'Lit: Proven hydraulic roughness increase mechanism (1150 papers)',
                'Lit: Quick installation, headwater-appropriate',
                'Wansbeck: Suitable for upland streams'
            ],
            'white': [
                'NI: ZERO net carbon and habitat (contradicts lit biodiversity claims!)',
                'Lit: Decomposition rates unknown - lifespan highly uncertain',
                'Lit: Long-term engineering performance data lacking',
                'Lit: Detachment thresholds poorly defined',
                'Lit: Extreme event behavior unknown',
                'NI vs Lit: Major disagreement on habitat benefit creates high uncertainty'
            ],
            'red': [
                'Lit: Short life expectancy (needs replacement)',
                'Lit: Detachment risk → downstream blockage hazard',
                'Lit: Can INCREASE local flood risk to non-target areas upstream',
                'NI: Zero co-benefits limits multi-objective value',
                'Lit: Safety concerns for infrastructure downstream'
            ]
        }
    },
    
    # ------------------------------------------------------------------------
    'Tree Planting': {
        'green': 50,
        'white': 40,  # High white due to time lag uncertainty and scaling challenges
        'red': 10,    # Lower red: cheap, no major safety issues, just time/land-use concerns
        'notes': {
            'green': [
                'NI: EXCELLENT carbon sequestration (5414 net - second best)',
                'NI: Strong habitat creation (3136 net units)',
                'NI: BEST storage cost-effectiveness (rank 1)',
                'Lit: MASSIVE evidence base (8390 papers - most of all interventions)',
                'Lit: Proven mechanisms (porosity, interception, evapotranspiration)',
                'Lit: Maximum scores for air quality, climate, habitat in review'
            ],
            'white': [
                'NI: Very low storage (7817 m³ - reflects time lag issue)',
                'Lit: 10-20+ year time lag before hydrological benefits',
                'Lit: Catchment-scale up-scaling "challenges quantifying"',
                'Lit: Time lag highly variable by species, climate, soil',
                'Lit: Optimal density and species mix unclear for Wansbeck',
                'Wansbeck: Time horizon of project affects viability'
            ],
            'red': [
                'Lit: Loss of productive farmland (land-use conflict)',
                'Lit: Landowner resistance in agricultural areas',
                'Lit: Establishment phase vulnerable to failure',
                'NI: Low immediate flood benefit due to establishment time'
            ]
        }
    },
    
    # ------------------------------------------------------------------------
    'Wet Woodland': {
        'green': 65,
        'white': 25,  # Higher white due to small lit base (415 papers) and site-specificity
        'red': 10,    # Lower red: moderate cost, main issue is limited applicability not safety/cost
        'notes': {
            'green': [
                'NI: Good storage (92,366 m³)',
                'NI: Strong carbon (3846 net) and habitat (4069 net)',
                'NI: BEST habitat cost-effectiveness (rank 9)',
                'Lit: QUANTIFIED - 5x greater roughness than grassland',
                'Lit: Self-sustaining once established',
                'Wansbeck: Suitable for waterlogged areas in lower catchment'
            ],
            'white': [
                'NI: Limited opportunities (183 sites - site-specific)',
                'Lit: Only 415 papers - small evidence base creates uncertainty',
                'Lit: Natural regeneration vs planting timing unclear',
                'Lit: Optimal management regime undefined',
                'Lit: Extreme event roughness maintenance uncertain'
            ],
            'red': [
                'NI: Site-limited (only waterlogged/floodplain areas)',
                'Lit: High setup costs for active planting',
                'Lit: Not suitable upland or free-draining soils',
                'Wansbeck: Limited applicable area (not widespread)'
            ]
        }
    },
    
    # ------------------------------------------------------------------------
    'Buffer Strips': {
        'green': 45,
        'white': 30,
        'red': 25,
        'notes': {
            'green': [
                'NI: Highly recommended (974 opportunities)',
                'NI: Low cost (£834k), good habitat value (rank 8)',
                'Lit: PROVEN 30%+ sediment and fertilizer reduction (1600 papers)',
                'Lit: High funding availability (agri-environment schemes)',
                'Lit: Low maintenance requirements',
                'Lit: Farmer acceptance relatively high'
            ],
            'white': [
                'NI: Very low storage (14,938 m³ - not primary flood tool)',
                'Lit: "No consensus" on optimal widths',
                'Lit: "Limited evidence" of catchment-scale runoff reduction',
                'Lit: Flood benefit magnitude uncertain',
                'Lit: Bypassed by tramlines and microtopography - effectiveness variable'
            ],
            'red': [
                'Lit: LOW fluvial flood impact (score 40 in tool)',
                'Lit: Primary benefit is water quality NOT flood reduction',
                'NI: Low absolute storage despite good cost-effectiveness rank',
                'Lit: Functionality compromised by field features',
                'Wansbeck: Questionable for primary flood objective'
            ]
        }
    },
    
    # ------------------------------------------------------------------------
    'Soil Management': {
        'green': 35,
        'white': 30,
        'red': 35,
        'notes': {
            'green': [
                'NI: Second-most recommended (1101 opportunities)',
                'NI: BEST carbon sequestration (6724 net)',
                'NI: BEST carbon cost-effectiveness (rank 9)',
                'NI: Low cost (£660k), good storage (109,716 m³)',
                'Lit: MASSIVE evidence base (7160 papers)',
                'Lit: High funding availability, farmer-accessible'
            ],
            'white': [
                'NI: Zero habitat benefit (contradicts some ecosystem service lit)',
                'Lit: "Statistically insignificant" short-term catchment impacts',
                'Lit: Persistence of benefits unclear',
                'Lit: Soil type dependency poorly defined',
                'Lit: Extreme event effectiveness questionable'
            ],
            'red': [
                'Lit: LOWEST fluvial flood impact (score 20 in tool)',
                'Lit: Annual implementation required (not persistent)',
                'Lit: Farmer compliance variable',
                'Lit: Benefits easily reversed by compaction',
                'Lit: No air quality benefits',
                'Wansbeck: Questionable as primary flood intervention'
            ]
        }
    },
    
    # ------------------------------------------------------------------------
    'Gully Stuffing': {
        'green': 50,
        'white': 35,  # High white: tiny lit base (89 papers), extreme event gaps
        'red': 15,    # Moderate red: cheap but short-lived, limited co-benefits
        'notes': {
            'green': [
                'NI: Very low cost (£40.7k - cheapest intervention)',
                'Lit: "Immediate effect upon installation" (no time lag)',
                'Lit: Effective at slowing headwater flows',
                'Lit: Simple construction using local materials',
                'Wansbeck: Appropriate for upland moorland gullies'
            ],
            'white': [
                'NI: Very low storage (1630 m³), zero carbon/habitat',
                'Lit: TINY evidence base (only 89 papers - extreme uncertainty)',
                'Lit: "General lack of info" on extreme rainfall performance',
                'Lit: Detachment potential and thresholds unknown',
                'Lit: Optimal design specifications unclear',
                'Lit: Whole-life cost-effectiveness vs other measures unknown'
            ],
            'red': [
                'Lit: Short life expectancy (5-10 years typically)',
                'Lit: Requires ongoing replacement/maintenance',
                'NI: Limited opportunities (163 sites)',
                'Lit: Low co-benefits (air quality, health access)',
                'Lit: Structure integrity in 1-in-100 year events unknown'
            ]
        }
    },
    
    # ------------------------------------------------------------------------
    'Grip Blocking': {
        'green': 35,  # Lower green: conflicting evidence, minimal Wansbeck peatland
        'white': 50,  # VERY high white: conflicting evidence + tiny lit (172 papers)
        'red': 15,    # Moderate red: cheap but limited applicability in Wansbeck
        'notes': {
            'green': [
                'NI: Very low cost (£58.7k), BEST storage per £ (rank 9)',
                'Lit: Restores natural headwater drainage',
                'Lit: Creates Sphagnum habitat (peatland restoration)',
                'Lit: High climate regulation potential (carbon storage)',
                'Wansbeck: Some degraded peatland in upland areas'
            ],
            'white': [
                'NI: Least recommended (94 opportunities - very limited)',
                'Lit: VERY SMALL evidence base (172 papers - high uncertainty)',
                'Lit: "Limited studies" on runoff rates for gully blocking',
                'Lit: "CONFLICTING evidence" on streamflow impacts (some increase, some decrease)',
                'Lit: Mechanism poorly understood',
                'Lit: Highly site-dependent on peat condition',
                'Wansbeck: Minimal peatland limits applicability'
            ],
            'red': [
                'NI: Low absolute storage (37,600 m³)',
                'NI: Minimal carbon (14.6) and habitat (145) benefits',
                'Lit: Only applicable to degraded peatland (not widespread in Wansbeck)',
                'Lit: Requires ongoing maintenance and monitoring',
                'Lit: Access for machinery difficult in upland areas'
            ]
        }
    }
}

# ============================================================================
# SECTION 3: VISUALIZATION SETUP
# ============================================================================

# Define order for display (left to right, top to bottom)
INTERVENTION_ORDER = [
    'RAFs',
    'Floodplain Reconnection',
    'LWD',
    'Tree Planting',
    'Wet Woodland',
    'Buffer Strips',
    'Soil Management',
    'Gully Stuffing',
    'Grip Blocking'
]

# Full names for display
INTERVENTION_NAMES = {
    'RAFs': 'Runoff Attenuation\nFeatures',
    'Floodplain Reconnection': 'Floodplain\nReconnection',
    'LWD': 'Large Woody\nDebris',
    'Tree Planting': 'Tree Planting',
    'Wet Woodland': 'Wet Woodland',
    'Buffer Strips': 'Buffer Strips',
    'Soil Management': 'Soil Management',
    'Gully Stuffing': 'Gully Stuffing',
    'Grip Blocking': 'Grip Blocking'
}

# Colors (Italian flag theme)
COLOR_GREEN = '#2d7a4f'  # Evidence FOR success
COLOR_WHITE = '#ffffff'  # Uncertainty / unknowns
COLOR_RED = '#c73e3a'    # Evidence AGAINST / concerns

# ============================================================================
# SECTION 4: GENERATE VISUALIZATION
# ============================================================================

def create_italian_flags():
    """Generate all 9 Italian flags on one page with legend"""
    
    # Create figure with 3x3 grid - wider aspect ratio for slimmer flags
    fig, axes = plt.subplots(3, 3, figsize=(18, 10))
    fig.suptitle('Italian Flag Evidence Scoring - NbS Interventions in Wansbeck Catchment', 
                 fontsize=17, fontweight='bold', y=0.99, fontfamily='serif')
    
    # Flatten axes for easier iteration
    axes_flat = axes.flatten()
    
    # Create each flag
    for idx, intervention in enumerate(INTERVENTION_ORDER):
        ax = axes_flat[idx]
        scores = ITALIAN_FLAGS[intervention]
        
        # Get proportions
        green_pct = scores['green']
        white_pct = scores['white']
        red_pct = scores['red']
        
        # Verify they sum to 100
        total = green_pct + white_pct + red_pct
        assert total == 100, f"{intervention} scores don't sum to 100: {total}"
        
        # Draw flag as horizontal bar - SLIMMER for elegant dissertation look
        # Green from left
        ax.barh(0, green_pct, left=0, color=COLOR_GREEN, 
                edgecolor='black', linewidth=1.5, height=0.4)
        
        # White in middle
        ax.barh(0, white_pct, left=green_pct, color=COLOR_WHITE,
                edgecolor='black', linewidth=1.5, height=0.4)
        
        # Red from right
        ax.barh(0, red_pct, left=green_pct + white_pct, color=COLOR_RED,
                edgecolor='black', linewidth=1.5, height=0.4)
        
        # Add title above flag - slightly larger and more elegant
        ax.set_title(INTERVENTION_NAMES[intervention], 
                    fontsize=12, fontweight='bold', pad=12, fontfamily='serif')
        
        # Add literature count below flag - elegant grey
        lit_count = LITERATURE_COUNTS[intervention]
        ax.text(50, -0.6, f'Literature: {lit_count:,} papers',
               ha='center', va='top', fontsize=9.5, style='italic',
               color='#555555', fontfamily='serif')
        
        # Format axes - adjusted for slimmer flags
        ax.set_xlim(0, 100)
        ax.set_ylim(-0.85, 0.65)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
    
    # Add legend at bottom - elegant and professional
    legend_elements = [
        mpatches.Patch(facecolor=COLOR_GREEN, edgecolor='black', linewidth=1.5,
                      label='Evidence FOR Success'),
        mpatches.Patch(facecolor=COLOR_WHITE, edgecolor='black', linewidth=1.5,
                      label='Uncertainty / Unknowns'),
        mpatches.Patch(facecolor=COLOR_RED, edgecolor='black', linewidth=1.5,
                      label='Evidence AGAINST / Concerns')
    ]
    
    fig.legend(handles=legend_elements, loc='lower center', 
              ncol=3, fontsize=12, frameon=True, 
              bbox_to_anchor=(0.5, -0.01),
              prop={'family': 'serif'},
              edgecolor='black', fancybox=False)
    
    plt.tight_layout(rect=[0, 0.025, 1, 0.97])
    
    return fig

# ============================================================================
# SECTION 5: ASSUMPTIONS & LIMITATIONS
# ============================================================================

ASSUMPTIONS = """
ASSUMPTIONS:
1. NatureInsight T70 threshold used as primary tool reference (balanced suitability)
2. Literature density indicates evidence maturity but is NOT the main driver of uncertainty
3. White area primarily from: conflicting evidence, field validation gaps, scale uncertainties, extreme event gaps
4. Scores are relative comparisons between interventions (not absolute assessments)
5. Multi-day rainfall fluvial flooding is primary mechanism in Wansbeck
6. Upland moorland → lowland Morpeth geomorphology affects intervention suitability
7. Time horizon matters for interventions with establishment lag (trees, woodland)
8. Field validation observations from dissertation weighted heavily
9. Cost data from NatureInsight used as implementation barrier indicator
10. NatureInsight rankings interpreted as performance indicators (rank 1-4=strong, 5-8=moderate, 9-12=weak)
11. Conflicting evidence between literature and NatureInsight increases uncertainty (white)
12. Red scores based on actual barriers (cost, safety, complexity) not just absence of positives
"""

LIMITATIONS = """
LIMITATIONS:
1. Publication bias likely exists (successes published more than failures)
2. Literature may be urban-SuDS heavy; rural NFM evidence sparser
3. NatureInsight is a MODEL - outputs are recommendations, not validated predictions
4. Field visits covered sample of sites only, not comprehensive validation
5. Scale effects (plot → catchment) poorly understood for most interventions
6. Extreme event performance (1-in-100 to 1-in-1000 year) universally uncertain
7. Climate change impacts on future performance unclear
8. Synchronization effects for distributed measures (RAFs, LWD) unknown
9. Manning's n calibration affects roughness-based measures (LWD, Wet Woodland, Buffers)
10. Scores synthesize across 10 categories - some nuance lost in aggregation
"""

# ============================================================================
# SECTION 6: RUN VISUALIZATION
# ============================================================================

if __name__ == "__main__":
    # Print assumptions and limitations
    print(ASSUMPTIONS)
    print(LIMITATIONS)
    
    # Generate and save figure
    fig = create_italian_flags()
    output_path = '/mnt/user-data/outputs/italian_flags_all_interventions.png'
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Visualization saved to: {output_path}")
    
    # Also save as PDF for high quality
    pdf_path = '/mnt/user-data/outputs/italian_flags_all_interventions.pdf'
    fig.savefig(pdf_path, bbox_inches='tight')
    print(f"✓ PDF version saved to: {pdf_path}")
    
    print("\n✓ Complete! All 9 Italian flags generated on one page.")
