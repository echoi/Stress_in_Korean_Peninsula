# Suggested Workflow

To generate a two-layer (i.e., lithosphere and asthenosphere) mesh with a fault plane,

1. check if the two-layer geometry file, `Korea_lithasth.sat` exists. 
    - If not, run `Korea_geometry_lithasth.jou` with Cubit or Trelis.
    - `Korea_geometry_lithasth.jou` requires boundary geometry files. To generate them, refer to https://osf.io/6szrn/wiki/Tohoku_Meshing/.
2. check if the fault plane geometry file (e.g., `rupture_zone_s1946NANKAI01BABA.sat`) exists. 
    - If not, run a corresponding Cubit/Trelis meshing file, e.g., `rupture_zone_s1946NANKAI01BABA.jou`.
    - Getting XY coordinates for the fault plane's epicenter is critical. To get them, see the [relevant documentatioin](https://osf.io/6szrn/wiki/Defining%20boundary%20surfaces%20and%20fault%20plane/) and run the [provided Jupyter notebook](https://osf.io/6szrn/files/github/ComplexModel%2Fboundaries%2Fdefine_domain.ipynb).
3. Run a meshing file, e.g., `Korea_Tohoku_mesh_16.3_lithasth.jou` or `Korea_Nankai_mesh_16.3_lithasth.jou`.