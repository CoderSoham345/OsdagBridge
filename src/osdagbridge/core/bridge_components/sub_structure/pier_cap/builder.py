from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakePrism
from OCC.Core.BRepBuilderAPI import (
    BRepBuilderAPI_MakePolygon,
    BRepBuilderAPI_MakeFace,
    BRepBuilderAPI_Transform,
)
from OCC.Core.gp import gp_Pnt, gp_Ax2, gp_Dir, gp_Vec, gp_Trsf


def _translate(shape, x=0.0, y=0.0, z=0.0):
    trsf = gp_Trsf()
    trsf.SetTranslation(gp_Vec(x, y, z))
    return BRepBuilderAPI_Transform(shape, trsf, True).Shape()


def build_pier_cap_geometry(
    *,
    pier_cap_top_width=3000.0,
    pier_cap_bottom_width=1200.0,
    pier_cap_depth=600.0,
    pier_cap_length=2200.0,
    deck_width=None,
    z_top=0.0,
    x_center=0.0,
    rebar_main_diameter=16.0,
    rebar_spacing_longitudinal=150.0,
    rebar_transverse_diameter=8.0,
    rebar_spacing_transverse=200.0,
    rebar_cover=40.0,
):
    """Build parametric trapezoidal/hammerhead pier cap concrete and internal rebar in mm."""
    cap_len = float(deck_width) if deck_width is not None else float(pier_cap_length)
    half_top = pier_cap_top_width / 2.0
    half_bot = pier_cap_bottom_width / 2.0
    z_bot = z_top - pier_cap_depth

    # Trapezoidal cross-section in YZ plane extruded longitudinally along +X
    poly = BRepBuilderAPI_MakePolygon()
    poly.Add(gp_Pnt(0.0, -half_bot, z_bot))
    poly.Add(gp_Pnt(0.0, half_bot, z_bot))
    poly.Add(gp_Pnt(0.0, half_top, z_top))
    poly.Add(gp_Pnt(0.0, -half_top, z_top))
    poly.Close()

    face = BRepBuilderAPI_MakeFace(poly.Wire()).Face()
    prism = BRepPrimAPI_MakePrism(face, gp_Vec(cap_len, 0.0, 0.0)).Shape()
    concrete_solid = _translate(prism, x=x_center - cap_len / 2.0)

    rebar_solids = []
    x_start = x_center - cap_len / 2.0 + rebar_cover
    x_end = x_center + cap_len / 2.0 - rebar_cover
    bar_len = max(x_end - x_start, 50.0)

    y_min = -half_bot + rebar_cover + rebar_main_diameter / 2.0
    y_max = half_bot - rebar_cover - rebar_main_diameter / 2.0
    n_y = max(2, int((y_max - y_min) / rebar_spacing_longitudinal) + 1)

    z_bot_bar = z_bot + rebar_cover + rebar_main_diameter / 2.0
    z_top_bar = z_top - rebar_cover - rebar_main_diameter / 2.0

    for j in range(n_y):
        yy = y_min if n_y == 1 else y_min + j * (y_max - y_min) / (n_y - 1)
        for zz in (z_bot_bar, z_top_bar):
            ax_x = gp_Ax2(gp_Pnt(x_start, yy, zz), gp_Dir(1.0, 0.0, 0.0))
            rebar_solids.append(
                BRepPrimAPI_MakeCylinder(ax_x, rebar_main_diameter / 2.0, bar_len).Shape()
            )

    n_x = max(2, int(bar_len / rebar_spacing_transverse) + 1)
    stirrup_y = max(pier_cap_bottom_width - 2.0 * rebar_cover, 50.0)
    stirrup_z = max(pier_cap_depth - 2.0 * rebar_cover, 50.0)

    for i in range(n_x):
        xx = x_start + i * bar_len / max(n_x - 1, 1)
        stirrup = BRepPrimAPI_MakeBox(
            gp_Pnt(xx - rebar_transverse_diameter / 2.0, -stirrup_y / 2.0, z_bot + rebar_cover),
            rebar_transverse_diameter,
            stirrup_y,
            stirrup_z,
        ).Shape()
        rebar_solids.append(stirrup)

    return {"concrete": [concrete_solid], "rebar": rebar_solids}
