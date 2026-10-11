[← Chapter 9. Attitude Estimation (part 2 of 2)](09-attitude-estimation-part2.md) · [Contents](README.md) · [Chapter 11. Smoothing →](11-smoothing.md)

# <span id="page-124-0"></span>Chapter 10. Usability Considerations

*Contributed by Cheryl J. Gramling*

This chapter is written to address best practices for mechanisms like selective processing of measurements, reinitializations and restarts, backup ephemeris, and the availability of a ground system corollary to a flight filter implementation. These become key considerations when using filtering techniques for navigation solutions operationally, and are especially pertinent to autonomous operations.

## 10.1. Editing

<span id="page-124-1"></span>Let $`{𝗿} = {𝘆} - {𝒉}({𝘅})`$, where $`{𝘆}`$ is the observed measurement, $`{𝒉}({𝘅})`$ is the value of the measurement computed from the state $`{𝘅}`$, $`{𝘆} = {𝒉}({𝘅}) + {𝘃}`$, and $`{𝘃}`$ is the measurement noise, $`\mathrm{E}[{𝘃}] = {𝟎}`$, $`\mathrm{E}[{𝘃}{𝘃}^{{𝖳}}] = {𝐑}`$. The quantity $`{𝗿}`$ is known as the *innovation* or sometimes the *pre-fit residual*. The covariance of $`{𝗿}`$ is given by

```math
{𝐖} = {𝐇}{𝐏}{𝐇}^{{𝖳}} + {𝐑} \qquad\qquad(10.1)
```

where $`{𝐏} = \mathrm{E}[{𝗲}{𝗲}^{{𝖳}}]`$, $`{𝐇} = \partial {𝒉}({𝘅})/\partial {𝘅}`$, and $`{𝗲}`$ is the error in the estimate of $`{𝘅}`$. The squared *Mahalanobis distance* associated with $`{𝗿}`$,

```math
m_{{𝗿}}^2 = {𝗿}^{{𝖳}} {𝐖}^{-1} {𝗿} \qquad\qquad(10.2)
```

has a $`\chi^2`$ distribution with degrees of freedom equal to the number of measurements contained in the vector $`{𝘆}`$. The statistic $`m_{{𝗿}}^2`$, also known as the squared residual or innovations ratio, may be compared to a $`\chi^2`$ statistic with a given probability in order to edit outlying measurements. For a purely linear estimation scheme, such editing is unnecessary, but for an *ad hoc* linearization such as the EKF, editing is essential to prevent large innovations that would violate Taylor series truncations used to develop the EKF approximation, even in the unlikely scenario in which sensors produced measurements with noise characteristics that perfectly followed their assumed (Gaussian) probability distributions.

Experience has shown that it is beneficial to provide for a command-able capability to selectively apply a three-way editing flag to each measurement type. This flag may be enumerated with the labels "accept," "inhibit," and "force," or similar. The "accept" label denotes use of the measurement, if it is accepted by the aforementioned edit test (in the parlance used by Shuttle and Orion, this flag is labeled "auto"). The "inhibit" flag indicates that the measurement should be rejected regardless of the status of the edit test. The "force" flag correspondingly indicates that the measurement should be ingested regardless of the edit test result.

Additional measurement edit or selection parameters may be considered to identify invalid measurements for filter processing and state update, as applicable to the orbit regime or application. The following categories capture a representative set of these criteria:

- Satisfying time constraints. For example, elapsed time from the last successful measurement update is greater than or equal to a threshold value, such as the expected measurement sampling interval.
- Satisfying transmitter or sensor performance and operability criteria. For example, transmitter or sensor are not available, or enabled, and/or have no valid state vector or ephemeris, or exhibits an errant telemetry value that violates a specified tolerance.
- Acceptance for processing measurements that occur during a maneuver time span. NOTE: This criteria type strongly depends on the procedure for process noise adjustments to accommodate maneuvers. If a maneuver is known to occur, then the filter operator may elect to introduce additional process noise to allow state update from the measurements during or soon after the maneuver span and reflect a more representative covariance during that period. Depending on the filter tuning, measurement processing for a state update across or after a small maneuver may not need an increase in process noise.
- Satisfying measurement-type specific selection criteria. For example, include only valid measurements: according to the GNSS receiver selection criteria for GPS space vehicles; that meet radial distance constraints to achieve minimum signal-to-noise ratio (SNR); when the receiving antenna boresight angle falls within the specified minimum and maximum constraints.
- Satisfying visibility criteria.

Visibility tests may take on different forms, but can generally be categorized as criteria that interrupt or corrupt the line of sight for the sensed observation. Editing accommodation may be needed to handle scenarios where the line of sight between a source (e.g. transmitter, celestial body for imaging) and the measuring sensor (e.g. receiver, camera) is

- interrupted by an occultation, e.g. the Moon blocks the view to Earth;
- corrupted by an element known to introduce multipath reflections, like a spacecraft appendage; or
- degraded by expected interference in sensor performance, such as an angular keep-out zone to ensure the Sun-Earth-Probe angle meets the minimum threshold for signal-to-noise for a viable measurement.

One common example for visibility editing criteria occurs when the line of sight of the received signal from the transmission source travels through a path of ionospheric or atmospheric disturbance above a specified tolerance. To avoid these corrupted observations adversely influencing the filter solution accuracy, it may be suitable to preclude these observations from a state update. Relevant editing schemes include Height of Ray Path (HORP) and Transmit-to-Receive elevation angle.

### 10.1.1. Height of Ray Path Editing

The HORP test is useful for measurements obtained from a signal between two orbiting assets. The edit test is predicated on defining the distance of the transmission path, or ray path, between the two orbiting assets with respect to the central body radius, followed by a comparison of that distance to the sum of the central body radius plus defined altitudes for the atmospheric interference zone. Figure [10.1](#page-126-0) portrays a case where the signal ray path incurs no violation, while in Figure [10.2](#page-126-1) the signal ray path passes through the defined atmospheric region to be considered for edit. The HORP test can be used to identify and edit for occultations by using an altitude of zero km above the occulting body.

<span id="page-126-0"></span>![](../_page_126_Diagram_2.jpeg)

*Figure 10.1. Signal Ray Path Above the Defined Atmosphere Region*

<span id="page-126-1"></span>![](../_page_126_Diagram_4.jpeg)

*Figure 10.2. Signal Ray Path Transits Through the Defined Atmosphere Region*

The HORP editing test starts by computing the distance between the two orbiters at the specific time instance:

```math
d = \|\vec{{𝒅}}\| = \biggl\| \vec{{𝑹}}_s - \frac{\vec{{𝒙}}(\vec{{𝒙}} \cdot \vec{{𝑹}}_s)}{x^2} \biggr\| \qquad\qquad(10.3)
```

where $`x = \|\vec{{𝒙}}\|`$,

```math
\vec{{𝒙}} = \vec{{𝑹}} - \vec{{𝑹}}_s \qquad\qquad(10.4)
```

and

$`\vec{{𝑹}}_s`$ = transmitter satellite position vector at the measurement time

$`\vec{{𝑹}}`$ = receiver position vector at the measurement time

<span id="page-127-1"></span>Accept the measurement if $`d \geq R_e + h`$, [Figure [10.1\]](#page-126-0), where $`R_e`$ equals the mean equatorial radius of the Earth (or relevant central body) and $`h`$ is the height of the atmosphere (a configurable parameter, based on the atmosphere applicable to the central body).

If $`d \lt R_e + h`$ [Figure [10.2\]](#page-126-1), compute

```math
\delta = x' - \sqrt{(R_e + h)^2 - d^2} \qquad\qquad(10.5)
```

where

```math
x' = \left\| \frac{\vec{{𝒙}} \cdot \vec{{𝑹}}_s}{x} \right\| \qquad\qquad(10.6)
```

If $`x' \leq \delta`$, accept the measurement.

If $`x' \gt \delta`$, accept the measurement if $`\alpha \lt \alpha_{\max}`$, where $`\alpha_{\max}`$ is the maximum central angle, a configurable parameter, nominally equal to 70 degrees for Earth as a central body, given by

```math
\alpha = \cos^{-1} \left( \frac{\vec{{𝑹}}_s \cdot \vec{{𝑹}}}{R_s R} \right) \qquad\qquad(10.7)
```

and $`R_s = \|\vec{{𝑹}}_s\|`$, $`R = \|\vec{{𝑹}}\|`$.

### 10.1.2. Elevation Angle Editing

An elevation angle editing test can be used to identify measurements that may be impacted by a known multipath source, a long path through the atmosphere between a ground antenna and the spacecraft, a lower SNR from a spill-over signal that may originate beyond an antenna pattern threshold, or other impacting sources that can be defined through an angular constraint. Figure [10.3](#page-127-0) depicts an example used herein, which represents editing for when the line of sight between a ground station and spacecraft falls below a local horizon minimum elevation. Case A represents accepted measurements and Case B represents measurements for editing.

<span id="page-127-0"></span>![](../_page_127_Figure_12.jpeg)

*Figure 10.3. Elevation Angle Test, Represented for Ground Station to Spacecraft Atmosphere Transit*

Compute the instantaneous line-of-sight vector from the receiving satellite to the $`i`$th transmitting ground station (GS) as follows:

```math
\vec{{𝝆}}^{\,i} = \vec{{𝑹}}(t_k) - \vec{{𝑹}}^{i}_{\text{GS}}(t_k) \qquad\qquad(10.8)
```

where

$`\vec{{𝑹}}(t_k)`$ = position vector of the receiving satellite at time $`t_k`$

$`\vec{{𝑹}}^{i}_{\text{GS}}(t_k)`$ = position vector of the $`i`$th transmitting GS at time $`t_k`$

The editing test is based on whether the elevation angle, $`E`$, of the line-of-sight vector with respect to the local horizon is greater than a minimum elevation angle, $`E_{\min}`$. The measurement is accepted (Fig [10.3,](#page-127-0) Case A) if the following is true:

```math
\sin E \gt \sin E_{\min} \qquad\qquad(10.9)
```

where $`E_{\min}`$ is a commandable minimum elevation angle within the $`\pm 90`$ degrees range, and $`E_{\min}`$ and $`E`$ are positive above the local horizon and negative below the horizon. In addition, $`\sin E`$ is computed as:

```math
\sin E = \frac{\vec{{𝝆}}^{\,i} \cdot \vec{{𝑹}}^{i}_{\text{GS}}(t_k)}{\|\vec{{𝝆}}^{\,i}\| \, \|\vec{{𝑹}}^{i}_{\text{GS}}(t_k)\|} \qquad\qquad(10.10)
```

Otherwise, the measurement is edited and not used to update the state.

### 10.1.3. General Angle Editing

One can apply angular editing tests to other mission constraints, such as an angle between the signal source-to-sun vector and the signal source-to-spacecraft to avoid solar scintillation impacts on the signal that may corrupt the navigation observable. A common application is when the signal source is a ground station on Earth; then the resultant angle is referred to as the Sun-Earth-Probe angle. In this example shown in Figure [10.4,](#page-128-0) this angle is denoted as $`\alpha`$. Note that the signal source may be a relay spacecraft or a GNSS space vehicle. The threshold angle, $`\alpha_{\min}`$, is a configurable parameter and may vary depending on the spacecraft's distance to the sun and the power-level of the signal between the spacecraft and source.

```math
\alpha(t_k) = \cos^{-1} \left( \frac{\vec{{𝑹}}_S(t_k) \cdot \vec{{𝑹}}_{\text{GS-SC}}(t_k)}{R_S(t_k) \, R_{\text{GS-SC}}(t_k)} \right) \qquad\qquad(10.11)
```

where

$`\vec{{𝑹}}_S(t_k)`$ = Ground Station to Sun vector at the measurement time, $`t_k`$

$`\vec{{𝑹}}_{\text{GS-SC}}(t_k)`$ = Ground Station to Spacecraft vector at the measurement time, $`t_k`$

Accept the measurement if $`\alpha \gt \alpha_{\min}`$. Otherwise, the measurement is edited and not used to update the state.

<span id="page-128-0"></span>![](../_page_128_Diagram_14.jpeg)

*Figure 10.4. General Angle Editing Test Applied to Sun-Earth-Probe Angle*

## 10.2. Reinitialization and Restarts

<span id="page-129-0"></span>Since no EKF can be guaranteed to remain converged, it is prudent to provide for features that can ease the process of recovering nominal filter operation . While to a large extent the particulars of each application will guide a designer to select among a variety of filter recovery features, a few general design principles are broadly relevant.

Experience has shown that the fairly drastic step of completely re-initializing the filter may not always be necessary or prudent. In particular, under conditions in which it is reasonably clear that the filter has begun to edit measurements because its covariance matrix has become overly optimistic, but there remains reason to believe that the state estimate has not yet become corrupted, it may be beneficial to reinitialize the covariance while retaining the current state estimate. It may also be desirable to retain flexibility to retain only the position/velocity state components, while reinitializing the various bias components.

If the filter has halted for some reason other than divergence (e.g. a flight computer reset), or if the start of the divergence can be reliably determined, it may be useful to "restart" the filter from a previously saved state and covariance, especially if there would otherwise be a long time required for re-convergence. To enable such a restart capability, the full state and covariance must have been periodically saved, and then they must be propagated to the restart time.

## 10.3. Backup Ephemeris

<span id="page-129-1"></span>A backup ephemeris can be a useful tool with navigation filters, serving as:

- a comparison to the filtered estimate, providing an input to fault detection based on commandable tolerances to detect degraded filter performance;
- a reinitialization state, if needed by an onboard filter based on mission-defined tolerance violation, or a previously identified fault response, or when a ground uplink is known to not be available in a timely manner;
- an alternative navigation estimate that can be reliably propagated without any measurement updates to maintain spacecraft orbit knowledge for health and safety and communication link pointing, e.g. in case of a safe-mode trigger or other case whereby the onboard filter is disabled.

Backup ephemeris can be instantiated by several representations, and the selected representation should be based on the mission operations concept, data systems employed, risk level, and requirements. In addition, the selected mean element variable set must align with the proper mean theory [[84](16-bibliography.md#page-173-16), Section 9.7.3]. Backup ephemerides based on Brouwer-Lyddane mean orbital elements and rates offer a mean representation of the orbit over a defined time period. The mean element representation given in Table [1](#page-130-0) has been used successfully on near-circular LEO and GEO missions (not at the critical inclination of 63.483 degrees), and used onboard to support navigation fault detection, isolation, and recovery [[31](16-bibliography.md#page-171-22)]. To obtain a backup ephemeris from a filtered estimate, the process usually involves converting the predicted osculating elements to Brouwer-Lyddane mean elements. The Brouwer-Lyddane mean elements will deteriorate over time, especially if the propagation or conversion does not account for the non-gravitational perturbations, such as atmospheric drag for a LEO orbit or solar radiation pressure for a GEO orbit. When used as a backup ephemeris, the accuracy expected from Brouwer-Lyddane mean elements, along with the expected coverage period and update rate for the orbital element set, must be taken into consideration according to the use case.

Chebyshev polynomials provide another option to represent a backup ephemeris, and may offer a consistent representation format for the spacecraft as well as celestial bodies. The Spacecraft Planet Instrument C-matrix Events [\(SPICE\)](https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/req/spk.html) toolkit offered by NASA's Navigation and Ancillary Information Facility [\(NAIF\)](https://naif.jpl.nasa.gov/naif/index.html) provides commonly accepted utilities for Chebyshev polynomials from an ephemeris (Types 2, 3, 14, and 20), as well as Hermite interpolators to evaluate the polynomial at a selected epoch (Types 12 and 13). While it is possible to compute mean elements or Chebyshev polynomials onboard, the computational overhead may induce a mission to periodically upload these types of backups from the ground.

<span id="page-130-0"></span>*Table 1. Brouwer-Lyddane Mean Elements*

| Element | Unit | Description |
|---------|------|-------------|
| $`T`$ | days | Epoch of the elements |
| $`a`$ | m | Semi-major axis |
| $`e`$ | n/a | Eccentricity |
| $`i`$ | deg | Inclination |
| $`\omega`$ | deg | Argument of periapsis |
| $`\Omega`$ | deg | Right Ascension of Ascending Node (RAAN) |
| $`M`$ | deg | Mean anomaly |
| $`\dot{a}`$ | m/s | Semi-major axis rate |
| $`\dot{\omega}`$ | deg/s | Argument of periapsis rate |
| $`\dot{\Omega}`$ | deg/s | RAAN rate |
| $`\dot{M}`$ | deg/s | Mean anomaly rate<sup>a</sup> |

<span id="page-130-1"></span><sup>a</sup> In Reference [[31](16-bibliography.md#page-171-22)], the mean anomaly rate, $`\dot{M}`$, for a LEO polar orbiting case combined mean anomaly and argument of periapsis as

```math
\dot{M} = \frac{[M(t_2) + \omega(t_2)] - [M(t_1) + \omega(t_1)]}{t_2 - t_1}
```

whereas, for the GEO low inclination case, $`\dot{M}`$ also includes RAAN to give

```math
\dot{M} = \frac{[M(t_2) + \omega(t_2) + \Omega(t_2)] - [M(t_1) + \omega(t_1) + \Omega(t_1)]}{t_2 - t_1}
```

The expected accuracy of the Brouwer-Lyddane elements for the respective orbit representations are on the order of tens of kilometers, which serves the purposes for the mission.

In some applications, such as use of measurements from a Global Navigation Satellite System receiver, the receiver's independent "point solution" may serve as a useful comparison source. The periodically saved filter state that contains the full state and covariance, discussed as a means to restart the filter, also provides capability to maintain a backup ephemeris. For flight phases of limited duration, the backup ephemeris may be propagated inertially without any measurement updates. For extended operations, it will usually be necessary to re-seed the backup with a current filter state at periodic intervals.

Averaged equinoctial elements offer a more accurate backup that aligns with autonomous operations and onboard processing capabilities, and more readily accommodate all trajectory types because they avoid the singularities found in classical elements. In particular, an equinoctial system of elements can be defined to represent any inclination or eccentricity, including $`e = 0`$ and $`e \gt 1`$. Selecting equinoctial elements and rates that vary slowly can be especially useful in a mission with variable or low-thrust. Lastly, equinoctial elements can be transformed to Cartesian or Keplerian elements. Elements averaged over a period of time that sufficiently represents the trajectory based on the filter estimates can serve as a state for comparison or to reinitialize a navigation filter to start state estimation.

The following set of equinoctial elements [[6](16-bibliography.md#page-170-18), [15](16-bibliography.md#page-170-19)], have been successfully implemented and operationally used in onboard filters. Table [2](#page-131-0) provides a definition of the equinoctial elements $`(a, h, k, p, q, \lambda)`$, based on the classical Keplerian elements $`(a, e, i, \Omega, \omega, M)`$. As Table [2](#page-131-0) describes, the equinoctial elements can be interpreted in terms of an equinoctial coordinate frame, whose principal direction, $`\hat{x}_{ep}`$, is the "origin of longitudes" as shown in Figure [10.5.](#page-132-0)

<span id="page-131-0"></span>*Table 2. Equinoctial Element System*

| Element | Definition | Conversion from Keplerian Elements |
|---------|------------|------------------------------------|
| $`a`$ | Semi-major axis | $`a`$ |
| $`h`$ | Projection of the eccentricity vector $`\vec{{𝒆}}`$ on the $`\hat{y}_{ep}`$ axis | $`e\sin(\omega + \Omega)`$ |
| $`k`$ | Projection of the eccentricity vector $`\vec{{𝒆}}`$ on the $`\hat{x}_{ep}`$ axis | $`e\,\cos(\omega + \Omega)`$ |
| $`p`$ | Projection of the nodal vector $`\vec{{𝑵}}`$ on the $`\hat{y}_{ep}`$ axis | $`\left(\tan\left(\frac{i}{2}\right)\right)^j \sin\Omega`$ |
| $`q`$ | Projection of the nodal vector $`\vec{{𝑵}}`$ on the $`\hat{x}_{ep}`$ axis | $`\left(\tan\left(\frac{i}{2}\right)\right)^j \cos\Omega`$ |
| $`\lambda`$ | Mean longitude | $`M + \omega + \Omega`$ |

$`\vec{{𝒆}}`$ = eccentricity vector pointing in the direction of the $`\hat{x}_p`$ axis (perifocus) with a magnitude equal to the orbital eccentricity

$`\vec{{𝑵}}`$ = nodal vector pointing in the direction of the ascending node with a magnitude equal to $`\left(\tan\left(\frac{i}{2}\right)\right)^j`$ where $`i`$ denotes the orbital inclination and $`j`$ is defined as: $`j = 1`$ for direct orbits $`(0 \leq i \leq 90^\circ)`$; $`j = -1`$ for retrograde orbits $`(90 \lt i \leq 180^\circ)`$

These equinoctial elements can be averaged over more than one orbital period to define an averaged set of elements and associated rates.

```math
\overline{(E_i)^0_{\text{ref}}} = \frac{1}{N+1} \sum_{n=0}^{N} E_i(t_0 + n\,\delta t), i = 1, 5 \qquad\qquad(10.12)
```

```math
\overline{(E_6)^0_{\text{ref}}} = \lambda(t_{\text{ref}}) \qquad\qquad(10.13)
```

<span id="page-132-1"></span><span id="page-132-0"></span>![](../_page_132_Diagram_2.jpeg)

*Figure 10.5. The Equinoctial Coordinate Frame*

where

- $`\overline{(E_i)^0_{\text{ref}}}`$ = reference averaged equinoctial element vector $`(\bar{a}, \bar{h}, \bar{k}, \bar{p}, \bar{q}, \bar{\lambda})`$ associated with the current reference time, $`t_{\text{ref}}`$
- $`t_{\text{ref}}`$ = reference time for a new set of reference averaged equinoctial elements, equal to the center of the averaging interval
- $`t_0`$ = time of the first point in the current summation interval
- $`E_i(t)`$ = component of osculating equinoctial element vector at time $`t`$ obtained from the osculating position and velocity vectors
- $`N`$ = number of osculating equinoctial element sets included in the summation
- $`\delta t`$ = time interval between successive osculating equinoctial elements included in the summation, commandable parameter (recommended to be on the order of one (1) second

The value of $`N`$ should be chosen so the average is performed over one spacecraft orbital period to within a commandable tolerance.

```math
N = 2 \left( \mathop{\mathrm{int}} \left[ \frac{P + \delta t}{2\delta t} \right] \right) \qquad\qquad(10.14)
```

where

```math
P = 2\pi \sqrt{\frac{\Bigl(\overline{a^{-1}_{\text{ref}}}\Bigr)^3}{\mu_{\text{CB}}}} \qquad\qquad(10.15)
```

and

- $`\mu_{\text{CB}}`$ = gravitation constant of the central body
- $`\overline{a^{-1}_{\text{ref}}}`$ = reference averaged semi-major axis associated with the prior set of reference averaged equinoctial elements

Equinoctial element rates for semi-major axis and mean longitude are computed as follows using the average for each element over the current and previous orbital periods:

```math
\overline{\dot{a}^0_{\text{ref}}} = \frac{1}{t_{\text{ref}} - t^{-1}_{\text{ref}}} \Bigl[ \overline{a^0_{\text{ref}}} - \overline{a^{-1}_{\text{ref}}} \Bigr] \qquad\qquad(10.16)
```

```math
\overline{\dot{\lambda}^0_{\text{ref}}} = \frac{1}{t_{\text{ref}} - t^{-1}_{\text{ref}}} \Bigl[ \overline{\lambda^0_{\text{ref}}} - \overline{\lambda^{-1}_{\text{ref}}} + 2\pi \Bigr] \qquad\qquad(10.17)
```

Averaged equinoctial elements assume that there is not a large change in the eccentricity vector or node over successive orbital periods; hence they should not be used over large discrete maneuvers unless special care is taken. Therefore, generally, rates for the other elements are assumed to be zero. If a maneuver does occur, the computation should be restarted.

To obtain the averaged equinoctial state vector at the current time, $`t_c`$, perform the computation as follows:

```math
\overline{\overline{E}(t_c)} = \overline{\overline{E}^{-2}_{\text{ref}}} + \overline{\dot{\overline{E}}^{-2}_{\text{ref}}}\,\Delta t \qquad\qquad(10.18)
```

where

- $`\overline{\overline{E}(t_c)}`$ = vector of averaged equinoctial elements (listed in Table [2\)](#page-131-0) evaluated at time $`t_c`$
- $`\overline{\overline{E}^{-2}_{\text{ref}}}`$ = vector of reference averaged equinoctial elements at reference time $`t^{-2}_{\text{ref}}`$
- $`\overline{\dot{\overline{E}}^{-2}_{\text{ref}}}`$ = vector of reference averaged equinoctial element rates at reference time $`t^{-2}_{\text{ref}}`$
- $`t^{-2}_{\text{ref}}`$ = reference time of the reference equinoctial elements and rates computed over the orbital period prior to the last
- $`\Delta t`$ = the time difference between the current time and the time of the reference equinoctial elements and rates two orbits prior, $`t_c - t^{-2}_{\text{ref}}`$

## 10.4. Ground System Considerations

<span id="page-133-0"></span>The operations concept, requirements on the onboard filter performance and products derived from the filter estimate, whether derived onboard or on the ground, filter commissioning, anomaly resolution, and performance monitoring are critical factors to consider in designing a ground system commensurate with the mission needs. The command and telemetry parameters necessary to understand filter performance and the derived products need to be designed into the mission as early in the design life cycle as possible. Filter operation, expected performance, known signatures or constraints on operation, and any maintenance at the requisite cadence should be documented and maintained throughout the mission lifetime. Default and current filter tuning parameters and variables that effect operating modes should be archived for ready access in case of a cold restart or for troubleshooting. While it may seem intuitive that all parameters affecting filter performance should be available for re-tuning from the ground via mechanisms such as commands, table uploads, etc., experience has shown that decisions about ground system design and telemetry and commanding constraints often limit the accessibility of key tuning parameters. Adequate bandwidth in telemetry for full insight into filter performance, including access to full covariance data, the restart record discussed above, and the backup ephemeris must be available, if only for limited periods during commissioning and/or troubleshooting activities. As a best practice, a comprehensive snapshot of the filter performance including the restart record (full state and covariance), and performance metrics on editing, measurement update, and tolerance parameters should be made available in telemetry at a regularly defined cadence commensurate with the mission concept and orbit regime .

The complementary side is that the ground system must be able to reproduce the onboard filter's performance when provided with corresponding input data via downlinked telemetry. Empirical evidence recommends that the ground system include the ability to use a high-fidelity and tunable representation of the filter to address current performance, analyses, and troubleshooting for anomaly resolution. This includes access to default, current, and prior upload parameters for modeling and tuning.

Often, the filter estimate developed onboard is used by the ground system to create subsequent products for the mission. This includes the use of the as-telemetered filter state for predictive planning products or analysis for covariance realism. In some cases, it may be necessary to develop a best estimated trajectory (BET), the generation of which may require alternate tuning or additional processing (e.g. through the use of smoothing algorithms) on the ground to achieve the most accurate orbit knowledge. The BET can be used to comparatively analyze filter performance, or may be a source for predictive products for mission objective planning or projected filter performance under alternative scenarios.

Careful consideration should be given to comprehensive operations concepts and usage for onboard filters. These include editing methods, availability of restart records, the need for and type of backup ephemeris, appropriate access for tuning and modeling changes, adequate information content available in telemetry, and the appropriate instantiation of a ground system for filter commissioning and performance monitoring throughout the mission lifetime.

---

[← Chapter 9. Attitude Estimation (part 2 of 2)](09-attitude-estimation-part2.md) · [Contents](README.md) · [Chapter 11. Smoothing →](11-smoothing.md)
