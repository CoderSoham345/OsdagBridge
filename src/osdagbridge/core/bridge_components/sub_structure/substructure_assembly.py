from osdagbridge.core.bridge_components.sub_structure.pier_cap.builder import (
    build_pier_cap_geometry,
)
from osdagbridge.core.bridge_components.sub_structure.pier.builder import (
    build_pier_geometry,
)
from osdagbridge.core.bridge_components.foundation.pile_cap.builder import (
    build_pile_cap_geometry,
)
from osdagbridge.core.bridge_components.foundation.pile.builder import (
    build_piles_geometry,
)


def build_full_substructure(
    *,
    x_center=0.0,
    y_center=0.0,
    z_deck_level=0.0,
    bearing_offset_z=0.0,
    pier_cap_top_width=3000.0,
    pier_cap_bottom_width=1200.0,
    pier_cap_depth=600.0,
    pier_cap_length=2200.0,
    deck_width=None,
    pier_diameter=800.0,
    pier_height=3000.0,
    pile_cap_length=2200.0,
    pile_cap_width=1200.0,
    pile_cap_depth=600.0,
    n_piles_per_cap=4,
    pile_diameter=400.0,
    pile_length=5000.0,
    pile_spacing=600.0,
    rebar_main_diameter=16.0,
    rebar_spacing_longitudinal=150.0,
    rebar_transverse_diameter=8.0,
    rebar_spacing_transverse=200.0,
    rebar_cover=40.0,
):
    """Assemble pier cap, pier, pile cap, and 2x2 piles with rebar in X/Y/Z mm."""
    cap_top_z = z_deck_level - bearing_offset_z
    pier_top_z = cap_top_z - pier_cap_depth
    pile_cap_top_z = pier_top_z - pier_height
    piles_top_z = pile_cap_top_z - pile_cap_depth

    rebar_cfg = dict(
        rebar_main_diameter=rebar_main_diameter,
        rebar_spacing_longitudinal=rebar_spacing_longitudinal,
        rebar_transverse_diameter=rebar_transverse_diameter,
        rebar_spacing_transverse=rebar_spacing_transverse,
        rebar_cover=rebar_cover,
    )

    pier_cap = build_pier_cap_geometry(
        pier_cap_top_width=pier_cap_top_width,
        pier_cap_bottom_width=pier_cap_bottom_width,
        pier_cap_depth=pier_cap_depth,
        pier_cap_length=pier_cap_length,
        deck_width=deck_width,
        z_top=cap_top_z,
        x_center=x_center,
        **rebar_cfg,
    )
    pier = build_pier_geometry(
        pier_diameter=pier_diameter,
        pier_height=pier_height,
        z_top=pier_top_z,
        x_center=x_center,
        y_center=y_center,
        **rebar_cfg,
    )
    pile_cap = build_pile_cap_geometry(
        pile_cap_length=pile_cap_length,
        pile_cap_width=pile_cap_width,
        pile_cap_depth=pile_cap_depth,
        z_top=pile_cap_top_z,
        x_center=x_center,
        y_center=y_center,
        **rebar_cfg,
    )
    piles = build_piles_geometry(
        n_piles_per_cap=n_piles_per_cap,
        pile_diameter=pile_diameter,
        pile_length=pile_length,
        pile_spacing=pile_spacing,
        z_top=piles_top_z,
        x_center=x_center,
        y_center=y_center,
        **rebar_cfg,
    )

    return {
        "pier_cap": pier_cap,
        "pier": pier,
        "pile_cap": pile_cap,
        "piles": piles,
        "concrete": (
            pier_cap["concrete"]
            + pier["concrete"]
            + pile_cap["concrete"]
            + piles["concrete"]
        ),
        "rebar": (
            pier_cap["rebar"]
            + pier["rebar"]
            + pile_cap["rebar"]
            + piles["rebar"]
        ),
    }
