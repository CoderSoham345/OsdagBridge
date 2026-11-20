import math
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCylinder
from OCC.Core.gp import gp_Pnt, gp_Ax2, gp_Dir


def build_piles_geometry(
    *,
    n_piles_per_cap=4,
    pile_diameter=400.0,
    pile_length=5000.0,
    pile_spacing=600.0,
    z_top=-3600.0,
    x_center=0.0,
    y_center=0.0,
    rebar_main_diameter=16.0,
    rebar_spacing_longitudinal=150.0,
    rebar_transverse_diameter=8.0,
    rebar_spacing_transverse=200.0,
    rebar_cover=40.0,
):
    """Build circular piles in a 2x2 grid with longitudinal bars and transverse ties in mm."""
    concrete_solids = []
    rebar_solids = []

    half_sp = pile_spacing / 2.0
    pile_positions = [
        (x_center + dx, y_center + dy)
        for dx in (-half_sp, half_sp)
        for dy in (-half_sp, half_sp)
    ][:n_piles_per_cap]

    z_bot = z_top - pile_length
    cage_r = max(
        (pile_diameter / 2.0) - rebar_cover - rebar_transverse_diameter - rebar_main_diameter / 2.0,
        10.0,
    )
    bar_len = max(pile_length - 2.0 * rebar_cover, 50.0)
    n_bars = max(4, int((2.0 * math.pi * cage_r) / rebar_spacing_longitudinal))
    n_ties = max(1, int(bar_len / rebar_spacing_transverse))

    for px, py in pile_positions:
        ax_z = gp_Ax2(gp_Pnt(px, py, z_bot), gp_Dir(0.0, 0.0, 1.0))
        concrete_solids.append(
            BRepPrimAPI_MakeCylinder(ax_z, pile_diameter / 2.0, pile_length).Shape()
        )

        for i in range(n_bars):
            ang = (2.0 * math.pi * i) / n_bars
            bx = px + cage_r * math.cos(ang)
            by = py + cage_r * math.sin(ang)
            bar_ax = gp_Ax2(gp_Pnt(bx, by, z_bot + rebar_cover), gp_Dir(0.0, 0.0, 1.0))
            rebar_solids.append(
                BRepPrimAPI_MakeCylinder(bar_ax, rebar_main_diameter / 2.0, bar_len).Shape()
            )

        for k in range(n_ties):
            tz = z_bot + rebar_cover + k * rebar_spacing_transverse
            tie_ax = gp_Ax2(gp_Pnt(px, py, tz), gp_Dir(0.0, 0.0, 1.0))
            rebar_solids.append(
                BRepPrimAPI_MakeCylinder(
                    tie_ax,
                    cage_r + rebar_transverse_diameter / 2.0,
                    rebar_transverse_diameter,
                ).Shape()
            )

    return {"concrete": concrete_solids, "rebar": rebar_solids}
