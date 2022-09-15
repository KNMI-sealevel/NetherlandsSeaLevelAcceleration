# NetherlandsSeaLevelAcceleration
Use local tide gauges and atmospheric reanalyses to study the evolution of the rate of sea level rise over time.

This is the code supporting Keizer et al. 2022, submitted to Ocean Science (add link to preprint).

The analysis is organised in three steps:
1. Two Notebooks (*prepare_atmospheric_data.ipynb*, *obtain_pressure_gradient.ipynb*) explain how to download the input data, preprocess the data and export intermediate csv files to **/data_atmosphere**
2. *gam_model.ipynb* performs the statistical modeling and exports the results as csv files to **/outputs**
3. The final figures and tables are made in *make_figures&tables.ipynb*. Figures are exported to **/figures** and tables are writen out as latex format that is copy/pasted directly into the manuscript.

The analysis of sea surface temperature and sea level for the appendix of the manuscript is in the notebook *wind-driven-sea-level_sst_analysis.ipynb*