# Bridge Substructure & Foundation 3D CAD + IFC Integration (OsdagBridge)

## File Structure
- `src/osdagbridge/core/bridge_components/sub_structure/pier/builder.py`: Circular pier concrete column and longitudinal/transverse reinforcement (`build_pier_geometry`).
- `src/osdagbridge/core/bridge_components/sub_structure/pier_cap/builder.py`: Hammerhead/trapezoidal pier cap concrete and reinforcement (`build_pier_cap_geometry`).
- `src/osdagbridge/core/bridge_components/foundation/pile_cap/builder.py`: Rectangular prism pile cap concrete and top/bottom longitudinal + transverse rebar grid (`build_pile_cap_geometry`).
- `src/osdagbridge/core/bridge_components/foundation/pile/builder.py`: 2x2 grid circular piles with longitudinal bars and transverse ties (`build_piles_geometry`).
- `src/osdagbridge/core/bridge_components/sub_structure/substructure_assembly.py`: Combined assembly in X (span), Y (deck width), Z (vertical) coordinates (`build_full_substructure`).
- `src/osdagbridge/core/bridge_types/plate_girder/cad_generator.py`: Substructure CAD shape routing (`generate_substructure_shapes`).
- `src/osdagbridge/desktop/ui/cad_3d.py`: 3D viewer rendering with semi-transparent concrete (`opacity = 0.35`, `SetTransparency(0.65)`) and opaque steel rebar (`render_substructure_in_viewer`).
- `src/osdagbridge/core/ifc_export_bridge/bridge_ifc_generator.py`: IFC4 spatial binding for substructure concrete and `IfcReinforcingBar` (`add_substructure_elements_to_ifc`).

## Default Parametric Dimensions (mm)
- Pier: `pier_diameter = 800`, `pier_height = 3000`
- Pier Cap: `pier_cap_top_width = 3000`, `pier_cap_bottom_width = 1200`, `pier_cap_depth = 600`, `pier_cap_length = 2200` (or `deck_width`)
- Pile Cap: `pile_cap_length = 2200`, `pile_cap_width = 1200`, `pile_cap_depth = 600`
- Piles: `n_piles_per_cap = 4` (2x2 grid), `pile_diameter = 400`, `pile_length = 5000`, `pile_spacing = 600`
- Reinforcement: `rebar_main_diameter = 16`, `rebar_spacing_longitudinal = 150`, `rebar_transverse_diameter = 8`, `rebar_spacing_transverse = 200`, `rebar_cover = 40`
