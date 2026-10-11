[← Chapter 6. Bias Modeling (part 2 of 2)](06-bias-modeling-part2.md) · [Contents](README.md) · [Chapter 8. Factorization Methods (part 1 of 3) →](08-factorization-methods-part1.md)

# Chapter 7. State Representations

<span id="page-84-4"></span><span id="page-84-0"></span>*Contributed by J. Russell Carpenter and Christopher N. D'Souza*

This Chapter discusses state representation, primarily for translations; attitude representations are discussed in Chapter [9.](09-attitude-estimation-part1.md#page-108-0)

## 7.1. Selection of Solve-For State Variables for Estimation

<span id="page-84-1"></span>As has been discussed in Chapter [3,](03-the-covariance-matrix-part1.md#page-38-0) it not good practice to include unobservable states in the EKF solve-for vector, particularly if this introduces unstable dynamical modes. Nonetheless, during the early stages of designing a navigation filter, it may not be clear to the designer which states to include. There are essentially two approaches to addressing this question, which we may describe as the additive and subtractive methods. With the additive approach, one begins with the smallest possible set of states, adding additional models as one deems them necessary. The problem with this approach is essentially that it is not possible to foresee how additional states will affect the system until they are added; one cannot analyze the sensitivity of the filter's performance to states which are not present in the analysis. The preferred, subtractive, approach is instead to start with a design of as high a fidelity as practical, including even modes which one may suspect are unobservable and possibly destabilizing. A designer may then readily perform sensitivity and covariance analysis [[27](16-bibliography.md#page-171-5), [60](16-bibliography.md#page-172-3)] to winnow the solve-for state to as parsimonious a set of observable states as needed to achieve design requirements.

## 7.2. Units and Precision

<span id="page-84-2"></span>In the early days of ground-based orbit determination, canonical units were preferred due to the limited word lengths that were available for computation. Factorized filtering methods largely eliminated the need for canonical units even before "modern" double-precision word lengths became available in onboard processors. A renewed interest in single-precision computations has emerged however as the desire to utilize processors based on Field Programmable Gate Arrays has become widespread. Thus, the possibility of overflow, truncation, and roundoff errors must still be considered. Wherever possible, filter computations, especially those involving the covariance matrix (even when it is factorized!), should be done in double precision, and time should be maintained in either two double-precision variables, or in quadruple precision if available. For low-Earth orbit navigation in an Earth-centered frame, position/velocity units based on meters and seconds are often adequate; for applications that may reach into cislunar space and beyond, units based on kilometers and seconds are preferred.

## 7.3. Coordinate and Time Systems

<span id="page-84-3"></span>For most orbital navigation applications, use of an "inertial" coordinate frame, such as the International Celestial Reference Frame, the "J2000" (FK5) frame, etc., will be desirable, since onboard computations utilizing navigation filter state estimates will typically most naturally occur in an inertial setting. It is usually convenient to choose a frame whose origin is at the center of the primary gravitational body. Some missions, such as cislunar and interplanetary missions, will occur within the Hill spheres of more than one celestial body, and some mechanism for changing the coordinate system origin without requiring reset of the filter should be considered.

In some cases, consideration may be given to central-body-fixed frames, such as the International Terrestrial Reference Frame, World Geodetic System of 1984, etc., particularly for applications that rely primarily on Global Navigation Satellite Systems (GNSS), and/or ground-based tracking systems. Although integrating the equations of motion in such systems necessitates additional calculations of Coriolis and centripetal acceleration, such calculations are relatively trivial in comparison to the computations required to accurately maintain a transformation between central-body-fixed and inertial frames. Computations of higher-order gravity acceleration are simplified, and maintenance of polar motion coefficients is also eliminated. Several of NASA's early Global Positioning System relative navigation experiments used such a formulation successfully [[66](16-bibliography.md#page-172-7), [74](16-bibliography.md#page-172-8)]. If other onboard applications require inertial states, but are indifferent as to which inertial frame is provided, it may be prudent to consider defining a fixed, true-of-date inertial frame which is identical to the body-fixed frame at the initial power-up of the navigation system, and which is henceforth related to the body-fixed frame by a simple single-axis polar rotation. Such an approach will permit navigation in the body-fixed frame without the difficulties of maintaining a relationship onboard the spacecraft to one of the conventional inertial frames.

With regard to time systems, navigation filter designs should strongly avoid dependence upon discontinuous time scales, such as Coordinated Universal Time ("UTC"). While ground-based applications will generally prefer UTC, it is far easier for the mission's ground system to manage leap seconds than it is to robustly test and maintain discontinuous time scales in an autonomous onboard navigation setting. The filter designer should strive to ensure that a misapplication of leap second logic can never affect filter performance. If requirements for maintenance of UTC onboard cannot be avoided, all such calculations should occur independently from the uniform continuous time scale that the filter uses internally. Time-tagged commands that affect filter performance should also utilize the same internal, continuous time scale.

## 7.4. Orbit Parameterizations

<span id="page-85-0"></span>For orbital navigation applications, orbital elements are geometrically appealing as a state representation, and there exist various "semi-analytic" theories for improving their usefulness as ephemeris representations for real-world orbits, such as the GPS broadcast ephemeris model, two-line elements, etc. Furthermore, long-term evolution of the orbital error covariance more naturally occurs in element representations, which may be especially relevant to conjunction analysis. However, NASA's experience has been that Cartesian parameters generally offer computational efficiencies for high-fidelity measurement and dynamics models, including for the Jacobian matrices required in estimation algorithms. Cartesian coordinates are also free of singularities.

## 7.5. Relative State Representations

<span id="page-85-1"></span>Although the subject of this Section implies the need for relative state knowledge, it is not necessarily the case that this implies estimation of the relative states directly. For example, if each spacecraft's only sensor is a GNSS receiver, and there is no method for exchanging the GNSS data between spacecraft, then each satellite's measurement errors will be largely uncorrelated, assuming that errors in the GNSS constellation data are minimal. Furthermore, there may be no common sources of dynamical error, such as might arise from common yet imperfect models of atmospheric density for low Earth orbiters. In such cases, mission requirements may be met simply be performing isolated state estimation onboard each satellite, and simply differencing the estimated state vectors. In such cases, the covariance of the relative state error between any two spacecraft is given by

```math
\begin{aligned} P_{\text{rel}} &= \mathrm{E}[(e_2 - e_1)(e_2 - e_1)^{{𝖳}}] \\ &= P_1 + P_2 \end{aligned} \qquad\qquad(7.1)
```

where $`e_i`$ denotes the estimation error for spacecraft $`i`$, since (by assumption) $`\mathrm{E}[e_1 e_2^{{𝖳}}] = 0`$. For many other applications, either the measurements or the dynamics or both will induce a correlation structure, making it necessary to simultaneously estimate some combination of Earth-centered (a.k.a. "absolute" or "inertial") states and spacecraft-to-spacecraft relative states. The choice of state representation and associated dynamical model for each application can have significant impacts on efficiency and accuracy, and requires careful consideration.

Aside from the choice of orbit parameterization, there are at least three choices for estimating a relative orbit. The most obvious choice is to solve directly for the differences between the parameters chosen for the orbit representation; that is, to solve for relative position and relative velocity, or relative orbital elements. In some contexts, such as nearly circular orbits, efficient dynamics, such as the linear time-invariant Hill-Clohessy-Wilshire model [[17](16-bibliography.md#page-170-15), [34](16-bibliography.md#page-171-14)], become available with a choice to solve directly for relative Cartesian states. In many other contexts, higher fidelity may be required, and furthermore, models for drag, solar radiation pressure, the ephemerides of other gravitational bodies, etc. may require knowledge of the Earth-centered (Cartesian) state of one or more of the spacecraft. In such cases, the estimator may solve for a combination of pure absolute/inertial states, or some combination of absolute and relative states. The architecture originally developed for NASA's *Apollo* missions was the former "dual-inertial" formulation [[63](16-bibliography.md#page-172-9)]. While the absolute/relative formulation may appear to be mathematically equivalent, computational considerations may choose one or the other to be favored in various application contexts. A general observation is that the dual-inertial formulation may be favorable for computations involving the state and state error covariance, and for "absolute" measurements such as undifferenced GPS pseudorange, while the absolute/relative formulation may be favorable for computations involving satellite-to-satellite relative measurements. Reference [[63](16-bibliography.md#page-172-9)] provides a comprehensive mathematical description of the dual-inertial formulation in the context of relative range, Doppler, and bearing measurements that one may easily adapt to any other measurement types.

### 7.5.1. Dual Inertial State Representation

Here, we consider only two spacecraft, but the results are easily generalized. Let $`x_i = [r_i^{{𝖳}}, v_i^{{𝖳}}]^{{𝖳}},\ i = 1, 2`$ denote the true state of spacecraft $`i`$, with $`r_i, v_i`$ the position and velocity vectors expressed in non-rotating coordinates centered on the primary central gravitational body. Based on mission requirements, any appropriate fidelity of dynamics may be directly utilized, e.g.

```math
\dot{x}_i = \begin{bmatrix} v_i \\ -\tfrac{\mu}{\|r_i\|^3} r_i + \sum_j f_j \end{bmatrix} \qquad\qquad(7.2)
```

where the specific forces $`f_j`$ may include thrust, higher-order gravity, drag, solar radiation pressure, gravity from non-central bodies such as the moon and the sun, etc.

Let $`e_i = \hat{x}_i - x_i`$, where $`\hat{x}_i`$ is an estimate for the state of spacecraft $`i`$. Then, the error in the state estimate $`\hat{x} = [\hat{x}_1^{{𝖳}}, \hat{x}_2^{{𝖳}}]^{{𝖳}}`$ is $`e = [e_1^{{𝖳}}, e_2^{{𝖳}}]^{{𝖳}}`$, and the error covariance is

```math
P = \mathrm{E}[e e^{{𝖳}}] = \begin{bmatrix} P_1 & P_{12} \\ P_{12}^{{𝖳}} & P_2 \end{bmatrix} \qquad\qquad(7.3)
```

<span id="page-87-0"></span>Any linear unbiased estimate of $`x`$ will have the following measurement update equation:

```math
\hat{x}^+ = \hat{x}^- + K(y - h(\hat{x}^-)) \qquad\qquad(7.4)
```

where $`\hat{x}^-`$ is the value of $`\hat{x}`$ immediately prior to incorporating the observation, $`y`$, and $`h(\hat{x}^-)`$ is an unbiased prediction of the measurement's value. The optimal gain is

```math
K = P H^{{𝖳}} (H P H^{{𝖳}} + R)^{-1} \qquad\qquad(7.5)
```

where $`R`$ is the measurement noise covariance and $`H = \partial h(x)/\partial x|_{\hat{x}^-}`$. Partition the update as follows:

```math
\begin{bmatrix} \hat{x}_1^+ \\ \hat{x}_2^+ \end{bmatrix} = \begin{bmatrix} \hat{x}_1^- \\ \hat{x}_2^- \end{bmatrix} + \begin{bmatrix} K_1 \\ K_2 \end{bmatrix} (y - h(\hat{x}^-)) \qquad\qquad(7.6)
```

```math
= \begin{bmatrix} \hat{x}_1^- \\ \hat{x}_2^- \end{bmatrix} + \begin{bmatrix} P_1 H_1^{{𝖳}} + P_{12} H_2^{{𝖳}} \\ P_{12}^{{𝖳}} H_1^{{𝖳}} + P_2 H_2^{{𝖳}} \end{bmatrix} (H P H^{{𝖳}} + R)^{-1} (y - h(\hat{x}^-)) \qquad\qquad(7.7)
```

from which it is clear that the optimal update for the relative state $`\hat{x}_{\text{rel}} = \hat{x}_2 - \hat{x}_1`$ is

```math
\hat{x}_{\text{rel}}^+ = \hat{x}_{\text{rel}}^- + (P_2 H_2^{{𝖳}} - P_1 H_1^{{𝖳}} - P_{12} H_2^{{𝖳}} + P_{12}^{{𝖳}} H_1^{{𝖳}})(H P H^{{𝖳}} + R)^{-1} (y - h(\hat{x}^-)) \qquad\qquad(7.8)
```

with corresponding relative error covariance

```math
P_{\text{rel}} = P_1 + P_2 - P_{12} - P_{12}^{{𝖳}} \qquad\qquad(7.9)
```

Noting that it must be true that $`h(x_{\text{rel}}) = h(x)`$ and hence that $`\partial h(x_{\text{rel}})/\partial x_{\text{rel}} = \partial h(x_2)/\partial x_2 = -\partial h(x_1)/\partial x_1`$, let $`H_{\text{rel}} = H_2 = -H_1`$. Then it is clear that

```math
P_{\text{rel}} H_{\text{rel}}^{{𝖳}} = P_2 H_2^{{𝖳}} - P_1 H_1^{{𝖳}} - P_{12} H_2^{{𝖳}} + P_{12}^{{𝖳}} H_1^{{𝖳}} \qquad\qquad(7.10)
```

and that

```math
H_{\text{rel}} P_{\text{rel}} H_{\text{rel}}^{{𝖳}} = H P H^{{𝖳}} \qquad\qquad(7.11)
```

and hence

```math
\hat{x}_{\text{rel}}^+ = \hat{x}_{\text{rel}}^- + P_{\text{rel}} H_{\text{rel}}^{{𝖳}} (H_{\text{rel}} P_{\text{rel}} H_{\text{rel}}^{{𝖳}} + R)^{-1} (y - h(\hat{x}_{\text{rel}}^-)) \qquad\qquad(7.12)
```

Therefore, the dual inertial state update is mathematically (although perhaps not computationally) equivalent to a direct update of the relative state.

Appendix [C](15-appendix-c-an-analysis-of-dual-inertial-absolute-and-inertial-relative.md#page-160-0) reproduces a memorandum that further details the benefits of the dual inertial formulation.

### 7.5.2. Linearized Relative State Representation

While it is sometimes useful to employ a linear model of the relative dynamics, especially for close proximity operations in near-circular orbits, there is significant benefit to casting the equations of motion in spherical coordinates. The following derivation of the Hill-Clohessy-Wiltshire equations in spherical coordinates is derived from notes from a lecture given by Robert H. Bishop. Let the position of a spacecraft be given by a set of right-handed spherical coordinates

```math
r = \rho \begin{bmatrix} \cos\phi \sin\theta \\ \sin\phi \\ \cos\phi \cos\theta \end{bmatrix} \qquad\qquad(7.13)
```

where $`\rho`$ is the distance from the central body to the spacecraft, $`\theta`$ is measured along some specified great circle of the central body, and $`\phi`$ is measured along a great circle of the central body that is normal to the former great circle, and contains the position vector, as Figure [7.1](#page-88-0) depicts. Define a state vector as follows: $`x = [\rho, \dot{\rho}, \theta, \dot{\theta}, \phi, \dot{\phi}]`$. If the only force on the spacecraft is point-mass gravity from the central body, then the equations of motion are given by

<span id="page-88-0"></span>

![](../_page_88_Picture_2.jpeg)

*Figure 7.1. Spherical coordinates.*

<span id="page-88-1"></span>
```math
\dot{x} = f(x) = \begin{bmatrix} \dot{\rho} \\ -\mu/\rho^2 + \rho\dot{\phi}^2 + \rho\dot{\theta}^2 \cos^2\phi \\ \dot{\theta} \\ -2\dot{\rho}\dot{\theta}/\rho + 2\dot{\phi}\dot{\theta}\tan\phi \\ \dot{\phi} \\ -2\dot{\rho}\dot{\phi}/\rho - \dot{\theta}^2 \cos\phi \sin\phi \end{bmatrix} \qquad\qquad(7.14)
```

Now consider a circular reference orbit, with radius $`\rho_*`$, which is in the plane of the great circle containing the $`\theta`$ coordinate. Let $`\omega_* = \sqrt{\mu/\rho_*^3}`$. Then, the state of an object following the circular reference orbit at any time $`t \gt t_o`$ will be $`x_*(t) = [\rho_*, 0, \omega_*(t - t_o) - \theta_o, \omega_*, 0, 0]`$. Without loss of generality, take $`\theta_o = t_o = 0`$. Letting $`\delta x = x - x_*`$, linearization of [\(7.14\)](#page-88-1) in the neighborhood of $`x_*`$ yields

```math
\delta\dot{x}(t) = \left.\frac{\partial f(x)}{\partial x}\right|_{x_*(t)} \delta x(t) = \begin{bmatrix} 0 & 1 & 0 & 0 & 0 & 0 \\ 3\omega_*^2 & 0 & 0 & 2\omega_*\rho_* & 0 & 0 \\ 0 & 0 & 0 & 1 & 0 & 0 \\ 0 & -2\omega_*/\rho_* & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 1 \\ 0 & 0 & 0 & 0 & -\omega_*^2 & 0 \end{bmatrix} \delta x(t) \qquad\qquad(7.15)
```

In this context, it is useful to redefine the state vector $`\tilde{x} = [\rho, \dot{\rho}, \rho_*\theta, \rho_*\dot{\theta}, \rho_*\phi, \rho_*\dot{\phi}]`$ so that angles are replaced by arc lengths. Then, the linearized equations of motion become

```math
\delta\dot{\tilde{x}}(t) = \begin{bmatrix} 0 & 1 & 0 & 0 & 0 & 0 \\ 3\omega_*^2 & 0 & 0 & 2\omega_* & 0 & 0 \\ 0 & 0 & 0 & 1 & 0 & 0 \\ 0 & -2\omega_* & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 1 \\ 0 & 0 & 0 & 0 & -\omega_*^2 & 0 \end{bmatrix} \delta\tilde{x}(t) \qquad\qquad(7.16)
```

If linearized relative dynamics are to be used for relative navigation in near-circular orbits, then interpreting the motion along the orbit track, and normal to the orbit track, as arc lengths, per the derivation above, is desirable since it will preserve the linearity of the approximation over a much wider range than if the along-track and cross-track coordinates are taken as rectilinear tangents to the reference orbit position.

## 7.6. Modeling Inertial Components

<span id="page-89-0"></span>Many onboard navigation systems employ inertial components consisting of gyros and/or accelerometers. In some applications, an external algorithm will process the increments of rotational and/or translational motion that these devices inherently measure, and produce an acceleration vector that the filter can directly incorporate into its computation of the equations of motion. However, it will often be the case that biases affecting these devices should be estimated by the filter. This section describes some recommended models for such biases, as well as the computations that need to be performed to accumulate the inertial measurement unit's (IMU) angle and velocity increments.

### 7.6.1. The Gyro Model

The gyro is modeled in terms of the bias, scale factor and nonorthogonality. The IMU *case frame* is defined such that the $`x`$-axis of the gyro is the reference direction with the $`x - y`$ plane being the reference plane; the $`y`$- and $`z`$-axes are not mounted perfectly orthogonal to it (this is why we don't have a full misalignment/nonorthogonality matrix as we will in the accelerometer model). The errors in determining these misalignments are the so-called *non-orthogonality errors*, expressed as a matrix $`{𝚪}`$, as

```math
{𝚪} \triangleq \begin{bmatrix} 0 & 0 & 0 \\ \gamma_{yx} & 0 & 0 \\ \gamma_{zx} & \gamma_{zy} & 0 \end{bmatrix}
```

The gyro scale factor represents the error in conversion from raw sensor outputs (gyro digitizer pulses) to useful units. In general we model the scale-factor error as a first-order Markov (or a Gauss-Markov) process in terms of a diagonal matrix given as

```math
{𝐒}^g = \begin{bmatrix} s_x^g & 0 & 0 \\ 0 & s_y^g & 0 \\ 0 & 0 & s_z^g \end{bmatrix}
```

Similarly, the gyro bias errors are modeled as as first-order vector Gauss-Markov processes as

```math
{𝖻}^g = \begin{bmatrix} b_x^g \\ b_y^g \\ b_z^g \end{bmatrix}
```

Finally, the gyro noise is represented by $`\epsilon_g`$. Hence

```math
\omega_m^{{𝒞}} = ({𝐈}_3 + {𝚪} + {𝐒}^g)\Bigl(\omega^{{𝒞}} + {𝖻}_g + \epsilon_g\Bigr) \qquad\qquad(7.17)
```

where $`{𝐈}_3`$ is a $`3 \times 3`$ identity matrix, the superscript $`{𝒞}`$ indicates that this is an inertial measurement at the "box-level" expressed in *case-frame* co-ordinates, and $`\omega^{{𝒞}}`$ is the 'true' angular velocity in the case frame. If we let $`{𝚫}^g \triangleq {𝚪} + {𝐒}^g`$ and $`({𝐈} + {𝚫}^g)^{-1} \approx {𝐈} - {𝚫}^g`$ [‡](#page-89-1), we can express the actual angular velocity in terms of the measured angular velocity as

```math
\omega^{{𝒞}} = ({𝐈}_3 - {𝚫}^g)\,\omega_m^{{𝒞}} - {𝖻}_g - \epsilon_g \qquad\qquad(7.18)
```

<span id="page-89-1"></span><sup>‡</sup> In order to evaluate $`({𝐈} + {𝚫})^{-1}`$ we recall the Woodbury matrix identity

```math
({𝐀} + {𝐔}{𝐂}{𝐕})^{-1} = {𝐀}^{-1} - {𝐀}^{-1}{𝐔}\left({𝐂}^{-1} + {𝐕}{𝐀}^{-1}{𝐔}\right)^{-1}{𝐕}{𝐀}^{-1}
```

Using this, we obtain the following relation (with $`{𝐀} = {𝐈}`$, $`{𝐔} = {𝚫}`$, $`{𝐂} = {𝐈}`$ and $`{𝐕} = {𝐈}`$),

```math
({𝐈} + {𝚫})^{-1} = {𝐈} - {𝚫}({𝐈} + {𝚫})^{-1}
```

which, worked recursively, yields the following approximation

```math
({𝐈} + {𝚫})^{-1} = {𝐈} - {𝚫} + {𝚫}^2 - {𝚫}^3 + {𝚫}^4 - {𝚫}^5 + \cdots
```

Therefore, to first-order (neglecting second-order and higher terms in the above equation), we get

```math
({𝐈} + {𝚫})^{-1} \approx {𝐈} - {𝚫}
```

### 7.6.2. The Accumulated $`\Delta{𝜽}`$

In order to find the accumulated angle (not as a function of the measurement, but purely as a function of the true angular velocity), we define $`\Delta{𝜽}`$ as

```math
\Bigl(\Delta{𝜽}_{{𝒞}_{k-1}}^{{𝒞}_k}\Bigr)_m \triangleq \int_{t_{k-1}}^{t_k} \biggl\{ \omega_m^{{𝒞}}(\tau) + \frac{1}{2}{𝝓}_{{𝒞}_{ref}}^{{𝒞}} \times \omega_m^{{𝒞}}(\tau) \biggr\} d\tau \qquad\qquad(7.19)
```

```math
= \int_{t_{k-1}}^{t_k} \biggl\{ \omega_m^{{𝒞}}(\tau) + \frac{1}{2}\biggl[ \int_{t_{k-1}}^{\tau} \dot{{𝝓}}_{{𝒞}_{ref}}^{{𝒞}}(\chi)\, d\chi \biggr] \times \omega_m^{{𝒞}}(\tau) \biggr\} d\tau \qquad\qquad(7.20)
```

```math
= \int_{t_{k-1}}^{t_k} \biggl\{ \omega_m^{{𝒞}}(\tau) + \frac{1}{2}\biggl[ \int_{t_{k-1}}^{\tau} \biggl( \omega_m^{{𝒞}}(\chi) + \frac{1}{2}{𝝓}_{{𝒞}_{ref}}^{{𝒞}} \times \omega_m^{{𝒞}}(\chi) \biggr) d\chi \biggr] \times \omega_m^{{𝒞}}(\tau) \biggr\} d\tau
```

Ignoring second-order terms, we get

```math
\Bigl(\Delta{𝜽}_{{𝒞}_{k-1}}^{{𝒞}_k}\Bigr)_m = \int_{t_{k-1}}^{t_k} \biggl[ \omega_m^{{𝒞}}(\tau) + \frac{1}{2}\int_{t_{k-1}}^{\tau} \omega_m^{{𝒞}}(\chi)\, d\chi \times \omega_m^{{𝒞}}(\tau) \biggr] d\tau \qquad\qquad(7.21)
```

With this expression, we find that, by analogy, we can express $`\Bigl(\Delta{𝜽}_{{𝒞}_{k-1}}^{{𝒞}_k}\Bigr)`$ as

```math
\Bigl(\Delta{𝜽}_{{𝒞}_{k-1}}^{{𝒞}_k}\Bigr) = \int_{t_{k-1}}^{t_k} \biggl[ \omega^{{𝒞}}(\tau) + \frac{1}{2}\int_{t_{k-1}}^{\tau} \omega^{{𝒞}}(\chi)\, d\chi \times \omega^{{𝒞}}(\tau) \biggr] d\tau \qquad\qquad(7.22)
```

### 7.6.3. The Accelerometer Model

The accelerometer package will likely be misaligned relative to the IMU reference frame. This is due to the fact that the three accelerometers (contained in the accelerometer package) are not mounted orthogonal to each other and these errors are expressed in terms of six different small angles as:

```math
{𝚵}^a = \begin{bmatrix} 0 & \xi_{xy}^a & \xi_{xz}^a \\ \xi_{yx}^a & 0 & \xi_{yz}^a \\ \xi_{zx}^a & \xi_{zy}^a & 0 \end{bmatrix}
```

As with the gyros, the accelerometer scale factor represents the error in conversion from raw sensor outputs (accelerometer digitizer pulses) to useful units. In general we model the scale-factor error as a first-order (Gauss-) Markov process in terms of a diagonal matrix given as

```math
{𝐒}^a = \begin{bmatrix} s_x^a & 0 & 0 \\ 0 & s_y^a & 0 \\ 0 & 0 & s_z^a \end{bmatrix}
```

Similarly, the bias errors are modeled as first-order Gauss-Markov processes as

```math
{𝖻}^a = \begin{bmatrix} b_x^a \\ b_y^a \\ b_z^a \end{bmatrix}
```

So, the accelerometer measurements, $`{𝐚}_m^{{𝒞}}`$ are modeled as:

```math
{𝐚}_m^{{𝒞}} = ({𝐈}_3 + {𝚵}^a)({𝐈}_3 + {𝐒}^a)\Bigl({𝐚}^{{𝒞}} + {𝖻}^a + {𝝊}_a\Bigr) \qquad\qquad(7.23)
```

where $`{𝐈}_3`$ is a $`3 \times 3`$ identity matrix, the superscript $`{𝒞}`$ indicates that this is an inertial measurement at the 'box-level' expressed in *case-frame* co-ordinates, and $`{𝐀}^{{𝒞}}`$ is the 'true' non-gravitational acceleration in the case frame. The quantity $`{𝝊}_a`$ is the velocity random walk, a zero-mean white sequence on acceleration that integrates into a velocity random walk, which is the 'noise' on the accelerometer output. If we assume that the errors are small, then to first-order

```math
({𝐈}_3 + {𝚵}^a)({𝐈} + {𝐒}^a) \approx {𝐈} + {𝚵}^a + {𝐒}^a
```

So, the linear accelerometer measurements (in the case frame) are:

<span id="page-91-1"></span>
```math
{𝐚}_m^{{𝒞}} = ({𝐈}_3 + {𝚵}^a + {𝐒}^a)\Bigl({𝐚}^{{𝒞}} + {𝖻}^a + {𝝊}_a\Bigr) \qquad\qquad(7.24)
```

### 7.6.4. Accumulated $`\Delta{𝐯}`$

We note that the measured $`\Delta{𝐯}`$ in the case frame, $`\Delta{𝐯}_m^{{𝒞}}`$, is mapped to the end of its corresponding time interval by the sculling algorithm within the IMU firmware, so that we can write

```math
\Bigl(\Delta{𝐯}_m^{{𝒞}}\Bigr)_k = \int_{t_{k-1}}^{t_k} {𝐓}_{{𝒞}(t)}^{{𝒞}_k} {𝐚}_m^{{𝒞}(t)}\, dt \qquad\qquad(7.25)
```

where $`\Bigl(\Delta{𝐯}_m^{{𝒞}}\Bigr)_k`$ covers the time interval from $`t_{k-1}`$ to $`t_k`$ ($`t_k \gt t_{k-1}`$) and $`{𝒞}(t)`$ is the instantaneous case frame[§](#page-91-0). We recall that a transformation matrix can be written in terms of the Euler axis/angle as

```math
T({𝝓}) = \cos(\phi){𝐈} - \frac{\sin\phi}{\phi}[{𝝓}\times] + \frac{1 - \cos\phi}{\phi^2}{𝝓}{𝝓}^{{𝖳}} \qquad\qquad(7.28)
```

```math
= {𝐈} - \frac{\sin\phi}{\phi}[{𝝓}\times] + \frac{1 - \cos\phi}{\phi^2}[{𝝓}\times][{𝝓}\times] \qquad\qquad(7.29)
```

which, for $`{𝝓} \sim {𝟎}`$, can be approximated as

```math
T({𝝓}) = {𝐈} - [{𝝓}\times] \qquad\qquad(7.30)
```

With this in mind, $`{𝐓}_{{𝒞}(t)}^{{𝒞}_k} = {𝐈}_3 - \Bigl[{𝜽}_{{𝒞}(t)}^{{𝒞}_k}\times\Bigr]`$, and $`\Bigl(\Delta{𝐯}_m^{C}\Bigr)_k`$, using Eq. [\(7.24\)](#page-91-1), becomes

```math
\Bigl(\Delta{𝐯}_m^{{𝒞}}\Bigr)_k = \int_{t_{k-1}}^{t_k} \Bigl[{𝐈}_3 - \Bigl[{𝜽}_{{𝒞}(t)}^{{𝒞}_k}\times\Bigr]\Bigr] \Bigl[({𝐈}_3 + {𝚫}^a)\,{𝐚}^{{𝒞}} + {𝖻}^a + {𝝊}_a\Bigr] dt \qquad\qquad(7.31)
```

We can expand this equation, neglecting terms of second-order, as follows

<span id="page-91-2"></span>
```math
\begin{aligned} \Bigl(\Delta{𝐯}_m^{{𝒞}}\Bigr)_k &= \int_{t_{k-1}}^{t_k} \Bigl[{𝐈}_3 - \Bigl[{𝜽}_{{𝒞}(t)}^{{𝒞}_k}\times\Bigr]\Bigr] {𝐚}^{{𝒞}}\, dt + \int_{t_{k-1}}^{t_k} \Bigl({𝖻}^a + {𝝊}_a\Bigr) dt \\ &\quad + \int_{t_{k-1}}^{t_k} {𝚫}^a {𝐚}^{{𝒞}}\, dt \end{aligned} \qquad\qquad(7.32)
```

<span id="page-91-0"></span><sup>§</sup> Or equivalently,

```math
\Bigl(\Delta{𝐯}_m^B\Bigr)_k = \int_{t_{k-1}}^{t_k} {𝐓}_{B(t)}^{B_k} {𝐚}_m^{B(t)}\, dt \qquad\qquad(7.26)
```

But since $`{𝐓}_{B(t)}^{B_k} \approx {𝐈}_3 - \Bigl[{𝝓}_{B(t)}^{B_k}\times\Bigr]`$, we find

```math
\Bigl(\Delta{𝐯}_m^B\Bigr)_k = \int_{t_{k-1}}^{t_k} \Bigl[{𝐈}_3 - \Bigl[{𝝓}_{B(t)}^{B_k}\times\Bigr]\Bigr] {𝐚}_m^{B(t)}\, dt \qquad\qquad(7.27)
```

<span id="page-92-0"></span>The first term in the above equation (Eq. [\(7.32\)](#page-91-2)) becomes

```math
\int_{t_{k-1}}^{t_k} \Bigl[{𝐈}_3 - \Bigl[{𝜽}_{{𝒞}(t)}^{{𝒞}_k}\times\Bigr]\Bigr] {𝐚}^{{𝒞}}\, dt = \left(\Delta{𝐯}^{{𝒞}}\right)_k \qquad\qquad(7.33)
```

and the third term becomes

```math
\int_{t_{k-1}}^{t_k} {𝚫}^a {𝐚}^{{𝒞}}\, dt = {𝚫}^a \int_{t_{k-1}}^{t_k} {𝐚}^{{𝒞}}\, dt \approx {𝚫}^a \left(\Delta{𝐯}^{{𝒞}}\right)_k \qquad\qquad(7.34)
```

Finally, the accelerometer noise, which is a zero-mean process with spectral density $`{𝐒}_a`$ becomes

```math
\int_{t_k}^{t_{k+1}} {𝝊}_a\, dt = {𝐮}_a \qquad\qquad(7.35)
```

where $`{𝐮}_a`$ is a random vector with covariance $`{𝐒}_a(t_k - t_{k-1})`$. So, Eq. [\(7.32\)](#page-91-2) becomes

```math
\Bigl(\Delta{𝐯}_m^{{𝒞}}\Bigr)_k = [{𝐈}_3 + {𝚫}^a]\left(\Delta{𝐯}^{{𝒞}}\right)_k + {𝖻}^a \Delta t + {𝝊}_a \Delta t \qquad\qquad(7.36)
```

Since we have established that $`[{𝐈}_3 + {𝚫}^a]^{-1} \approx [{𝐈}_3 - {𝚫}^a]`$, and neglecting terms of second-order,

```math
\left(\Delta{𝐯}^{{𝒞}}\right)_k = [{𝐈}_3 - {𝚫}^a]\Bigl(\Delta{𝐯}_m^{{𝒞}}\Bigr)_k - {𝖻}^a \Delta t - {𝝊}_a \Delta t \qquad\qquad(7.37)
```

The average acceleration in the case frame is

```math
{𝐚}_{ave}^{{𝒞}} = \frac{\left(\Delta{𝐯}^{{𝒞}}\right)_k}{\Delta t} \qquad\qquad(7.38)
```

and the average measured acceleration in the case frame is

```math
\Bigl({𝐚}_m^{{𝒞}}\Bigr)_{ave} = \frac{\Bigl(\Delta{𝐯}_m^{{𝒞}}\Bigr)_k}{\Delta t} \qquad\qquad(7.39)
```

so we find that

```math
{𝐚}_{ave}^{{𝒞}} = [{𝐈}_3 - {𝚫}^a]\Bigl({𝐚}_m^{{𝒞}}\Bigr)_{ave} - {𝖻}^a - {𝝊}_a \qquad\qquad(7.40)
```

Recalling that the IMU measures accelerations except for gravity, total acceleration is

```math
{𝐚}^I = {𝐠}^I({𝐫}) + \Bigl({𝐓}_{B_{ref}}^I\Bigr)_k {𝐓}_B^{B_{ref}} {𝐓}_{{𝒞}}^B {𝐚}_{ave}^{{𝒞}} \qquad\qquad(7.41)
```

### 7.6.5. The Gravity Call

One of the more expensive computations involving the propagation of the trajectory with IMU data is the gravity calculation. This is particularly acute when the gravity field used is of high order. The gravity gradient matrix requires even more computation. Hence it goes without saying that if a way is found to minimize the gravity calls, that would make the navigation software more tractable. Taking advantage of the fact that propagation of the trajectory using IMU data occurs at a high rate (usually at 40 Hz or higher), we expand the gravity vector in terms of a Taylor series about $`{𝐫}^*`$ as

```math
{𝐠}({𝐫}) = {𝐠}({𝐫}^*) + \left.\frac{\partial{𝐠}}{\partial{𝐫}}\right|_{{𝐫}={𝐫}^*} [{𝐫} - {𝐫}^*] + \frac{1}{2}[{𝐫} - {𝐫}^*]^{{𝖳}} \left.\frac{\partial^2{𝐠}}{\partial{𝐫}^2}\right|_{{𝐫}={𝐫}^*} [{𝐫} - {𝐫}^*] + \ldots \qquad\qquad(7.42)
```

Knowing that the gravity gradient matrix, $`{𝐆}`$, is

```math
{𝐆}({𝐫}^*) = \left.\frac{\partial{𝐠}}{\partial{𝐫}}\right|_{{𝐫}={𝐫}^*} \qquad\qquad(7.43)
```

and truncating after the first-order in $`{𝐫}`$, we find that

```math
{𝐠}({𝐫}) \approx {𝐠}({𝐫}^*) + {𝐆}({𝐫}^*)[{𝐫} - {𝐫}^*] \qquad\qquad(7.44)
```

```math
\approx {𝐆}({𝐫}^*){𝐫} + [{𝐠}({𝐫}^*) - {𝐆}({𝐫}^*){𝐫}^*] \qquad\qquad(7.45)
```

where now the gravity vector and the gravity gradient matrix need only to be evaluated at the beginning of the major cycle.

---

[← Chapter 6. Bias Modeling (part 2 of 2)](06-bias-modeling-part2.md) · [Contents](README.md) · [Chapter 8. Factorization Methods (part 1 of 3) →](08-factorization-methods-part1.md)
