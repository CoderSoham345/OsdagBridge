import math
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCylinder
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.gp import gp_Pnt, gp_Ax2, gp_Dir, gp_Vec, gp_Trsf


def _translate(shape, x=0.0, y=0.0, z=0.0):
    trsf = gp_Trsf()
    trsf.SetTranslation(gp_Vec(x, y, z))
    return BRepBuilderAPI_Transform(shape, trsf, True).Shape()


def build_pier_geometry(
    *,
    pier_diameter=800.0,
    pier_height=3000.0,
    z_top=0.0,
    x_center=0.0,
    y_center=0.0,
    rebar_main_diameter=16.0,
    rebar_spacing_longitudinal=150.0,
    rebar_transverse_diameter=8.0,
    rebar_spacing_transverse=200.0,
    rebar_cover=40.0,
):
    z_bottom = z_top - pier_height
    ax_z = gp_Ax2(gp_Pnt(x_center, y_center, z_bottom), gp_Dir(0, 0, 1))
    concrete_solid = BRepPrimAPI_MakeCylinder(ax_z, pier_diameter / 2.0, pier_height).Shape()

    rebar_solids = []
    cage_radius = max(
        (pier_diameter / 2.0) - rebar_cover - (rebar_transverse_diameter + rebar_main_diameter / 2.0),
        10.0,
    )
    circumference = 2.0 * math.pi * cage_radius
    n_bars = max(4, int(circumference / rebar_spacing_longitudinal))
    bar_len = max(pier_height - 2.0 * rebar_cover, 50.0)

    for i in range(n_bars):
        ang = (2.0 * math.pi * i) / n_bars
        bx = x_center + cage_radius * math.cos(ang)
        by = y_center + cage_radius * math.sin(ang)
        bar_ax = gp_Ax2(gp_Pnt(bx, by, z_bottom + rebar_cover), gp_Dir(0, 0, 1))
        rebar_solids.append(
            BRepPrimAPI_MakeCylinder(bar_ax, rebar_main_diameter / 2.0, bar_len).Shape()
        )

    tie_radius = max((pier_diameter / 2.0) - rebar_cover - rebar_transverse_diameter / 2.0, 10.0)
    n_ties = max(1, int(bar_len / rebar_spacing_transverse))
    for k in range(n_ties):
        tz = z_bottom + rebar_cover + k * rebar_spacing_transverse
        outer = BRepPrimAPI_MakeCylinder(
            gp_Ax2(gp_Pnt(x_center, y_center, tz), gp_Dir(0, 0, 1)),
            tie_radius,
            rebar_transverse_diameter,
        ).Shape()
        rebar_solids.append(_translate(outer, 0.0, 0.0, 0.0))

    return {"concrete": [concrete_solid], "rebar": rebar_solids}
