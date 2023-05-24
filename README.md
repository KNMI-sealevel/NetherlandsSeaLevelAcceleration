# Code and data for Keizer et al. (2023): "The acceleration of sea-level rise along the coast of the Netherlands started in the 1960s"
Use local tide gauges and atmospheric reanalyses to study the evolution of the rate of sea level rise over time.

This is the code supporting Keizer et al. 2023, [submitted to Ocean Science](https://egusphere.copernicus.org/preprints/2022/egusphere-2022-935/).

The analysis is organised in three steps:
1. Two Notebooks (*prepare_atmospheric_data.ipynb*, *obtain_pressure_gradient.ipynb*) explain how to download the input data, preprocess the data and export intermediate csv files to **/data_atmosphere**
2. *gam_model.ipynb* performs the statistical modeling and exports the results as csv files to **/outputs**
3. The final figures and tables are made in *make_figures.ipynb* and *make_tables.ipynb*, respectively. Figures are exported to **/figures** and tables are written out as latex format that is copy/pasted directly into the manuscript.

The analysis of sea surface temperature and sea level for the appendix of the manuscript is in the notebook *wind-driven-sea-level_sst_analysis.ipynb*.

### Reproducibility
There are 2 conda `environment.yml` files (because the two spectral packages `mtpec` and `spectrum` don't seem to want to be installed at the same time):
1. `environment_NLSL.yml`: used for almost all code
2. `environment_NLSL_mtspec.yml`: used for `figures_MV.ipynb`

### Data provenance
- tide gauge data (PSMSL)
- reanalysis for wind (20CR, ERA5)
- SST data (COBESST)

### License
BSD 3-Clause License, see `LICENSE` file