This folder contains the hydrograph generation, comparison and analysis workflows developed for the dissertation project.

The notebooks and scripts within this section were used to assess how Nature-based Solutions (NbS) interventions influenced modelled flood hydrograph behaviour across the River Wansbeck catchment under varying return period conditions. Although, they are designed with the intention of being applicable to any catchment with clear signposting for where necessary adjustments are.

Hydrograph analysis formed a critical component of the dissertation, supporting evaluation of the hydrological performance and practical flood attenuation potential of NatureInsight® intervention scenarios.

A key aim of the analysis was to investigate whether the interventions proposed by NatureInsight® produced meaningful changes in:

Peak flow magnitude
Time-to-peak
Hydrograph shape
Flood response behaviour

and across sub-catchments which can be accessed [here](Subcatchment_Analysis_Clean.ipynb)..

The analysis also contributed to wider critical discussion surrounding the realism, assumptions and uncertainty associated with conceptual catchment-scale decision-support tools.

The workflows within this folder were used to:

Generate baseline (“No Intervention”) hydrographs
Compare intervention versus baseline hydrographs
Assess changes across multiple return periods
Evaluate intervention grouping performance
Compare hydrograph shape and timing behaviour
Analyse subcatchment hydrograph responses
Quantify peak flow reduction and attenuation effects
Understand the influence of altering intervention storage parameters
Analyse the impact of individual storage buckets
Isolate select interventions to understand NbS types strengths on flood management
Understand peak synchronisation

Scenarios were assessed under varying:

Suitability thresholds
Ranking selections
Ordered By optimisation settings
Return period conditions (e.g. RP10–RP500)

Hydrograph analysis focused on:

Peak flow (m³/s)
Time-to-peak
Percentage peak flow reduction
Percentage delay in time-to-peak
Hydrograph shape comparison
Relative intervention performance between scenarios

The hydrograph workflows were developed to assess:

The potential flood attenuation performance of NatureInsight® outputs
Whether intervention benefits remained consistent across return periods
The sensitivity of modelled hydrological responses to scenario configuration
Spatial variability in intervention effectiveness across the catchment
Potential limitations associated with conceptual hydrological representation


These analyses supported wider discussion regarding model assumptions, simplification, routing uncertainty, peak synchronisation and the reliability of decision support tools. It also highlighted the value of antecedent events and  underlying soil.


Hydrograph outputs were generated using NatureInsight® and associated SCALGO-based modelling workflows. The dissertation critically acknowledges that these hydrographs represent conceptual strategic-scale outputs rather than fully physically-based hydrodynamic simulations.

Observed gauge data and statistical flood estimation approaches were therefore used where appropriate to provide additional context and comparison for interpreted model behaviour.

### Example Output: Subcatchment Summary

The notebook summarises NatureInsight outputs by subcatchment, allowing intervention opportunities to be compared across the catchment.

![Subcatchment Summary](../images/subcatchment_code_example.png)

### Example Output: Subcatchment Hydrographs

Observed and modelled hydrographs can be compared between subcatchments to explore differences in hydrological response.

![Subcatchment Hydrograph](../images/subcatchment_hydrograph_image.png)

### Example Output: Intervention Distribution

Pie charts are produced to visualise the relative contribution of intervention types within each subcatchment.

![Subcatchment Pie Charts](../images/pie_charts_subcatchment.png)

