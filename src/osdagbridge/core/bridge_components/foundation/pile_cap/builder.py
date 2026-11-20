from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCC.Core.gp import gp_Pnt, gp_Ax2, gp_Dir


def build_pile_cap_geometry(
    *,
    pile_cap_length=2200.0,
    pile_cap_width=1200.0,
    pile_cap_depth=600.0,
    z_top=-3000.0,
    x_center=0.0,
    y_center=0.0,
    rebar_main_diameter=16.0,
    rebar_spacing_longitudinal=150.0,
    rebar_transverse_diameter=8.0,
    rebar_spacing_transverse=200.0,
    rebar_cover=40.0,
):
    """Build rectangular prism pile cap concrete and internal reinforcement grid in mm."""
    z_bot = z_top - pile_cap_depth
    x0 = x_center - pile_cap_length / 2.0
    y0 = y_center - pile_cap_width / 2.0

    concrete_solid = BRepPrimAPI_MakeBox(
        gp_Pnt(x0, y0, z_bot),
        pile_cap_length,
        pile_cap_width,
        pile_cap_depth,
    ).Shape()

    rebar_solids = []
    x_min = x0 + rebar_cover
    x_max = x0 + pile_cap_length - rebar_cover
    y_min = y0 + rebar_cover
    y_max = y0 + pile_cap_width - rebar_cover

    z_bot_bar = z_bot + rebar_cover + rebar_main_diameter / 2.0
    z_top_bar = z_top - rebar_cover - rebar_main_diameter / 2.0

    n_y = max(2, int((y_max - y_min) / rebar_spacing_longitudinal) + 1)
    long_len = max(x_max - x_min, 10.0)
    for j in range(n_y):
        yy = y_min if n_y == 1 else y_min + j * (y_max - y_min) / (n_y - 1)
        for zz in (z_bot_bar, z_top_bar):
            ax_x = gp_Ax2(gp_Pnt(x_min, yy, zz), gp_Dir(1.0, 0.0, 0.0))
            rebar_solids.append(
                BRepPrimAPI_MakeCylinder(ax_x, rebar_main_diameter / 2.0, long_len).Shape()
            )

    n_x = max(2, int((x_max - x_min) / rebar_spacing_transverse) + 1)
    trans_len = max(y_max - y_min, 10.0)
    for i in range(n_x):
        xx = x_min if n_x == 1 else x_min + i * (x_max - x_min) / (n_x - 1)
        for zz in (z_bot_bar + rebar_main_diameter, z_top_bar - rebar_main_diameter):
            ax_y = gp_Ax2(gp_Pnt(xx, y_min, zz), gp_Dir(0.0, 1.0, 0.0))
            rebar_solids.append(
                BRepPrimAPI_MakeCylinder(ax_y, rebar_transverse_diameter / 2.0, trans_len).Shape()
            )

    return {"concrete": [concrete_solid], "rebar": rebar_solids}
