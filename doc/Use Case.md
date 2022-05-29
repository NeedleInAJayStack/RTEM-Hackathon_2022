# Use Case

## Intro

### Background

Reducing energy use in buildings is expensive. Despite advances in fault-detection and diagnostic systems, acheiving building energy savings still requires manual effort to evaluate issues and make the necessary virtual or physical changes to rectify them. Because of this, there is a need for improved prioritization in order to satisfy the biggest opportunities first.

Historically, prioritization has typically taken two paths:

1. High level metrics: Industry standard metrics like energy use intensity are used to compare buildings to their peers and grade their efficiency. Unfortunately, these metrics do very little to suggest actions to take for energy reduction within a given building.
2. Low level analytics: Analytics identify discrete operational issues which are extremely useful for determining actions to take. However, these rarely output energy savings estimates, and when they do the values are unreliable because system interaction is often complex.

There is opportunity for a middle layer that improves high level prioritization and provides a clear path to implementation. This is where I am focused.

### Proposal

In this document I propose a set of key performance indicators (KPIs) and an analysis framework to identify and prioritize energy reduction from unoccupied setbacks. Nearly every building can acheive significant energy reductions by basic changes to their unoccupied operation, and these savings are extremely cost-effective. The largest energy savings opportunity in most non-industrial building involves modifying zone air temperatures, minimum discharge air flow setpoints, or lighting based on occupancy. The propsed framework identifies these opportunities.

## Approach

This framework requires whole-building energy use values at hourly frequencies or faster. This data was easily extracted for 80 of the buildings in the RTEM dataset. This whole-building energy usage is cleaned by removing meter rollover artifacts, aligning timestamps to a consistent frequency with missing values interpolated, dis-aggregating values if represented by a monitonically increasing value, and finally passing the values through an outlier filter. After this process, we are left with clear, consistent energy usage data for the whole building.

Next, the cleaned data is split into weekly periods and passed through a k-means clustering algorithm that identifies 2 nodes, a "high-usage" cluster and a "low-usage" cluster. This process provides a mapping between each energy usage reading and whether it belongs in the high or low usage, as well as values for the high and low-usage clusters. We interpret the high-usage period to be the occupied time in a building, and the low-usage period to be the unoccupied time.

From these results, we can compute two meaningful weekly KPIs:
1. Unoccupied Turndown Factor: The high-usage value divided by the low-usage value. Scaled from 0 to 1, lower values indicate more effective unoccupied setbacks. Lower is better from an energy savings standpoint.
2. Occupied Duration Factor: The amount of time the building was in a high-usage state, divided by the total time in the week. Scaled from 0 to 1, lower values indicate more prevalent unoccupied setbacks, in terms of time.  Lower is better from an energy savings standpoint.

This simple approach offers several significant benefits over alternatives. First, the data requirements are extremely low; only a single historical reading for total energy use is required. Energy use is commonly trended on many buildings, or can be readily accessed by installing a smart meter device or requesting interval data from most utility companies. Second, it is widely applicable. The analysis process is not impacted by the type of building, the pattern of occupancy throughout the week, or the type of equipment within the building. Since no assumptions are made on the time of occupancy, it would function as well on irregularly occupied buildings (like community centers or sports arenas) as on regularly occupied buildings (like commerical office buildings). Finally, it delivers actionable results. Even the oldest and most primitive control systems offer features for modifying operation according to occupancy.

**mention additional tagging needs, and that the total usage was determined manually**

## Usage

These KPIs alone do not indicate energy usage, so ideally these KPIs would be used alongside an Energy Use Intensity-based analysis. For example, if comparing buildings within a portfolio, the EUI could be used to determine the worst-performing facilities, and then the KPIs above could be used to determine whether these facilities would benefit from improving the unoccupied operation.

The different KPIs suggest different actions:
- A large Unoccupied Turndown Factor suggests that unoccupied operation should be investigated. When unoccupied, minimum discharge airflow setpoints should be going to 0, zone air temperature setpoint deadbands should widen significantly, and lights should be shut off if possible. Also, this KPI suggests that there may be areas that never enter an unoccupied state.
- A large Occupied Duration Factor suggests that occupancy detection systems should be investigated. Of course, unoccupied energy saving measures must conform to each building's unique occupancy patterns. However, if occupancy is based on a schedule, that schedule should be checked to ensure that it matches actual occupancy patterns. If occupancy is detected using a sensor, the sensors should be validated for correct operation.

While a KPI value on a particular building at a particular time is meaningful, KPIs are typically most useful when they are compared between entities or over time. A building with a large KPI value compared to its peers, or with a KPI value that increases over time may provide context on what a "large" KPI value is.

## Results

Show table of results across buildings.

### Unoccupied Turndown Factor

We can determine buildings with high values that would benefit from unoccupied energy use analysis:
- 275 (large user)
- 250

Others can be identified as performing well:
- 122 (large user)
- 157 (large user)
- 316

### Occupied Duration Factor

We can determine buildings with high values that would benefit from restricted occupancy hours:
- 127 (see Oct 2018)

Ranges are fairly restrained to near 50% due to approach. Few are less than 0.3 or more than 0.7

## Expanding to future buildings

## Additional Applications

- This analysis approach is not specific to total-building electric energy use. It could potentially be applied in very similar ways to:
  1. Other building-level utilities: Total building gas, chilled water, or steam use
  2. Submetering: Zone or tenant-level unoccuiped setback analysis and tracking
  3. Non-energy metrics: Zone air temperature setpoints, VAV discharge airflow, AHU chilled water valve position

## Conclusion

- Recap:
  - This paper presents a strategy for analyzing the effectiveness of unoccupied setbacks on total building energy usage and comparing buildings against one another.
  - It presents results from the existing dataset and is easily extended as new data becomes available
- Carbon reduction is as much about electrification as it is about reducing existing energy usage. Low-hanging fruit is plentiful.