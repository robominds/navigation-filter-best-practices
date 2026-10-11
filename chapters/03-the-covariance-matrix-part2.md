[← Chapter 3. The Covariance Matrix (part 1 of 3)](03-the-covariance-matrix-part1.md) · [Contents](README.md) · [Chapter 3. The Covariance Matrix (part 3 of 3) →](03-the-covariance-matrix-part3.md)

*Chapter 3. The Covariance Matrix, continued*

## 3.2. Covariance Propagation

<span id="page-44-0"></span>This section discusses best practices for implementing the covariance propagation recursion

<span id="page-44-1"></span>

```math
{𝐏}_i^- = {𝚽}(t_i, t_{i-1}){𝐏}_{i-1}^+{𝚽}^{{𝖳}}(t_i, t_{i-1}) + {𝐒}_i, \quad {𝐏}_0^+ = {𝐏}_o \qquad\qquad(3.40)
```

As Chapter [1](01-the-extended-kalman-filter.md#page-24-0) mentions, to achieve this goal we need suitable approximations for the state transition matrix, $`{𝚽}(t_i, t_{i-1})`$, and the process noise covariance, $`{𝐒}_i`$. However, the suitability of a given set of approximations is strongly dependent on specifics of the application. For example, if a set of measurements from which the state is fully observable are available at an interval that is a small fraction of the orbit period, without significant drop-outs, and prediction of the covariance far into the future of the time of availability of the measurements is not required, then simple models such as those to which Chapter [1](01-the-extended-kalman-filter.md#page-24-0) alluded have been successfully employed. Selection of appropriate covariance propagation approximations also depends strongly on the choice of state representation, which is the subject of Chapter [7.](07-state-representations.md#page-84-0) Therefore, this section will discuss the merits of some of the more common and generally applicable approaches, in the context of orbit determination.

### 3.2.1. Matrix Riccati Equation

Many textbooks on Kalman filtering derive [\(3.40\)](#page-44-1) as the solution of a matrix Riccati equation; using the notation of Chapter [1,](01-the-extended-kalman-filter.md#page-24-0) this takes the following form:

<span id="page-44-2"></span>

```math
\dot{{𝐏}}(t) = {𝐀}(t){𝐏}(t) + {𝐏}(t){𝐀}^{{𝖳}}(t) + {𝐐}(t) \qquad\qquad(3.41)
```

Use of [\(3.41\)](#page-44-2) would seem to avoid the need to perform the integrations required to compute the state transition matrix (STM) and process noise covariance (PNC). In orbit determination practice however, [\(3.40\)](#page-44-1) has been found to be more numerically stable and also, despite the need to compute or approximate the state transition and process noise integrals, more efficient than [\(3.41\)](#page-44-2).

### <span id="page-45-4"></span>3.2.2. State Transition Matrix

A common approach in ground-based OD, especially in the batch least squares context, is to simultaneously integrate the STM along with the state vector,

<span id="page-45-0"></span>

```math
\dot{{𝑿}}(t) = {𝒇}({𝑿}(t), t), \quad {𝑿}(t_o) = {𝑿}_o \qquad\qquad(3.42)
```

```math
\dot{{𝚽}}(t, t_o) = {𝐀}(t){𝚽}(t, t_o), \quad {𝚽}(t_o, t_o) = {𝐈} \qquad\qquad(3.43)
```

When coupled with a good numerical integration algorithm, this method has excellent fidelity, which is rarely necessary in onboard OD applications. Lear [[50](16-bibliography.md#page-172-1)] studied a number of practical methods for computing the STM in the onboard OD context. As his report is not widely available, we will summarize some key findings here.

Lear's approach was to compare various orders of truncated Taylor series and Runge-Kutta approximations to the solution of [\(3.43\)](#page-45-0). He used these STM approximations to propagate an initially diagonal covariance for one revolution in a two-body circular orbit around a point mass with the $`GM`$ of Earth. By comparing these results to those he obtained using an analytic STM, Lear could compute the maximum step size that would result in a given relative accuracy for radius and speed formal standard deviations. Table [1](#page-45-1) lists a few of Lear's results. Notably, Method H has the desirable feature that simply saving the value of the state Jacobian from the previous propagation step allows for more than an order of magnitude increase in allowable time step, with essentially the same computational burden as Method B. If it is not too burdensome to compute $`{𝐀}`$ at the midpoint of the propagation step, then Method G offers nearly equivalent performance without the need to retain the previous value of $`{𝐀}`$. For higher-rate propagations, Method B offers far more accuracy than Method A with only a small additional computational burden. While Method A appears to be a poor choice for many applications, it does play a central role in some useful approximations to the process noise covariance, as the sequel shows.

| | Description | Method | Max. Step [sec] |
|---|---|---|--:|
| A. | 1<sup>st</sup>-order Taylor | $`{𝐈} + {𝐀}_i\Delta t`$ | 0.125 |
| B. | 2<sup>nd</sup>-order Taylor, ignoring $`\dot{{𝐀}}`$ | $`{𝐈} + {𝐀}_i\Delta t + {𝐀}_i^2\Delta t^2/2`$ | 1.0 |
| C. | 2<sup>nd</sup>-order Taylor | $`{𝐈} + {𝐀}_i\Delta t + (\dot{{𝐀}}_i + {𝐀}_i^2)\Delta t^2/2`$ | 16 |
| F. | 1<sup>st</sup>-order Runge-Kutta | $`{𝐈} + {𝐀}_{i+.5}\Delta t`$ | 0.14 |
| G. | 2<sup>nd</sup>-order Runge-Kutta, with one evaluation of $`{𝐀}`$ | $`{𝐈} + {𝐀}_{i+.5}\Delta t + {𝐀}_{i+.5}^2\Delta t^2/2`$ | 14 |
| H. | 2<sup>nd</sup>-order Runge-Kutta, with two evaluations of $`{𝐀}`$ | $`{𝐈} + ({𝐀}_i + {𝐀}_{i+1})\Delta t/2 + {𝐀}_{i+1}{𝐀}_i\Delta t^2/2`$ | 16 |

<span id="page-45-1"></span>*Table 1. A few of Lear's STM Comparison Results, for 1% relative error.*

### 3.2.3. Process Noise Covariance

As stated in Chapter [1,](01-the-extended-kalman-filter.md#page-24-0) nearly all practical methods for computing the process noise covariance assume that $`\mathrm{E}[{𝘄}(t){𝘄}^{{𝖳}}(\tau)] = {𝐐}(t)\delta(t - \tau)`$, so that [\(1.29\)](01-the-extended-kalman-filter.md#page-28-5) simplifies to a single integral for the process noise covariance[<sup>2</sup>](#page-45-2), given by [\(1.42\)](01-the-extended-kalman-filter.md#page-29-2), and repeated here:

<span id="page-45-3"></span>

```math
{𝐒}_i = \int_{t_{i-1}}^{t_i} {𝚽}(t_i, \tau){𝐁}(\tau){𝐐}(\tau){𝐁}^{{𝖳}}(\tau){𝚽}^{{𝖳}}(t_i, \tau)\, \mathrm{d}\tau \qquad\qquad(3.44)
```

<span id="page-45-2"></span><sup>2</sup> A notable exception is the work of Wright [[89](16-bibliography.md#page-173-2)], which describes a correlated process noise model that is intended to account for gravity modeling errors in a "physically realistic" manner. Although this method has had occasional onboard application, it is more widely known for its inclusion in commercial-off-the-shelf software for ground-based OD.

Tapley, Schutz, and Born [[81](16-bibliography.md#page-173-3)] describe two approximations to the portion of [\(3.44\)](#page-45-3) which corresponds to position and velocity state noise, which have proven useful in both ground- and onboard-OD applications. Reference [81](16-bibliography.md#page-173-3) refers to these methods as "State Noise Compensation" (SNC) and "Dynamic Model Compensation" (DMC). Before describing SNC and DMC however, we will consider some inappropriate models.

Chapter [1](01-the-extended-kalman-filter.md#page-24-0) pointed out that

```math
\begin{aligned} &\mathrm{E}\biggl[\int_{t_{i-1}}^{t_i}\int_{t_{i-1}}^{t_i} {𝚽}(t_i, \tau){𝐁}(\tau){𝘄}(\tau){𝘄}^{{𝖳}}(\sigma){𝐁}^{{𝖳}}(\sigma){𝚽}^{{𝖳}}(t_i, \sigma)\, \mathrm{d}\tau\, \mathrm{d}\sigma\biggr] \\ &\qquad \neq \mathrm{E}\biggl[\int_{t_{i-1}}^{t_i} {𝚽}(t_i, \tau){𝐁}(\tau){𝘄}(\tau)\, \mathrm{d}\tau \int_{t_{i-1}}^{t_i} {𝘄}^{{𝖳}}(\tau){𝐁}^{{𝖳}}(\tau){𝚽}^{{𝖳}}(t_i, \tau)\, \mathrm{d}\tau\biggr] \end{aligned} \qquad\qquad(3.45)
```

Let us explore the implications of assuming equality of the expression above. Suppose we assume that the process noise increments are approximately constant over some particular interval $`\Delta t = t_i - t_{i-1}`$, and that $`\mathrm{E}[{𝘄}(t_i){𝘄}^{{𝖳}}(t_j)] = {𝐖}(t_i)\delta_{ij}`$, where $`\delta_{ij}`$ denotes the Kronecker delta function. Then,

<span id="page-46-0"></span>

```math
\begin{aligned} &\mathrm{E}\biggl[\int_{t_{i-1}}^{t_i} {𝚽}(t_i, \tau){𝐁}(\tau){𝘄}(\tau)\, \mathrm{d}\tau \int_{t_{i-1}}^{t_i} {𝘄}^{{𝖳}}(\tau){𝐁}^{{𝖳}}(\tau){𝚽}^{{𝖳}}(t_i, \tau)\, \mathrm{d}\tau\biggr] \\ &\quad = \int_{t_{i-1}}^{t_i} {𝚽}(t_i, \tau){𝐁}(\tau)\, \mathrm{d}\tau\; \mathrm{E}[{𝘄}(t_i){𝘄}(t_i)^{{𝖳}}] \int_{t_{i-1}}^{t_i} {𝐁}^{{𝖳}}(\tau){𝚽}^{{𝖳}}(t_i, \tau)\, \mathrm{d}\tau \\ &\quad = {𝚪}_i{𝐖}_i{𝚪}_i^{{𝖳}} \end{aligned} \qquad\qquad(3.46)
```

There is a subtlety with [\(3.46\)](#page-46-0) that can lead to issues: if the time interval associated with the assumption that $`\mathrm{E}[{𝘄}(t_i){𝘄}^{{𝖳}}(t_j)] = {𝐖}(t_i)\delta_{ij}`$ is not the same as the time interval associated with the integral $`{𝚪}_i = \int_{t_{i-1}}^{t_i}{𝚽}(t_i, \tau){𝐁}(\tau)\, \mathrm{d}\tau`$, then the process noise will not be consistently applied. For example, if the EKF is tuned at a particular time step using a particular noise covariance $`{𝐖}`$, and then for some reason the time step is changed, then one must retune the value of $`{𝐖}`$.

A similar issue occurs when the process noise covariance is chosen without regard for the dynamics, e.g. by setting it equal to a diagonal matrix of user-specified parameters. Whatever careful tuning has been done to choose such parameters will be invalidated by a change in the time step.

#### 3.2.3.1. State Noise Compensation

For SNC, as applied to OD, we assume velocity error is an uncorrelated random walk with fixed intensity in orbit-fixed coordinates, such as the RTN or VNB coordinates described above. Thus, assuming RTN coordinates without loss of generality, the process noise spectral density matrix becomes

```math
{𝐐}(t) = {𝐐}_{rtn} = \begin{bmatrix} q_r & 0 & 0 \\ 0 & q_t & 0 \\ 0 & 0 & q_n \end{bmatrix} \qquad\qquad(3.47)
```

We assume the transformation from orbit-fixed coordinates to the coordinates used for navigation, which are typically inertial coordinates, is approximately constant over the interval $`\Delta t = t_i - t_{i-1}`$, and ignore the correlation-inducing dependence of this transformation on the estimated position and velocity. This results in

```math
{𝐁}(t) = {𝐁}_{rtn} = \begin{bmatrix} {𝟎}_{3\times 3} \\ {𝐌}_{rtn} \end{bmatrix} \qquad\qquad(3.48)
```

<span id="page-47-0"></span>We also assume that $`\Delta t`$ is small enough that a 1<sup>st</sup>-order Taylor series truncation (Lear's Model A) is adequate for modeling the STM $`{𝚽}(t_i, \tau)`$ in the integrand of [\(3.44\)](#page-45-3), and that $`{𝐌}_{rtn}`$ is constant. With these assumptions, [\(3.44\)](#page-45-3) becomes

```math
{𝐒}_i = \begin{bmatrix} \tilde{{𝐐}}\dfrac{\Delta t^3}{3} & \tilde{{𝐐}}\dfrac{\Delta t^2}{2} \\[2ex] \tilde{{𝐐}}\dfrac{\Delta t^2}{2} & \tilde{{𝐐}}\Delta t \end{bmatrix} \qquad\qquad(3.49)
```

where $`\tilde{{𝐐}} = {𝐌}_{rtn}{𝐐}_{rtn}{𝐌}_{rtn}^{{𝖳}}`$. Note that with the SNC model, velocity covariance grows linearly with time, as expected for a random walk model, and hence we should expect the units of $`\sqrt{q_i}`$, $`i = r, t, n`$ to be meters per second$`^{3/2}`$. Reference [[79](16-bibliography.md#page-173-4)] provides alternative approximations to [\(3.44\)](#page-45-3) for an orbital element state representation, and for relative spacecraft states at both small and large interspacecraft separations.

#### 3.2.3.2. State Noise Compensation for Maneuvers

During powered flight, it is often necessary to include additional process noise to accommodate maneuver magnitude and direction errors. One approach is to simply define an additional SNC process noise covariance, with intensities that are sized to the maneuvering errors. While this works fine for modeling maneuver magnitude errors, direction errors may be more accurately modeled by recognizing that a misaligned maneuver vector may be represented by $`({𝐈}_3 - \delta{𝜽}^{\times})\Delta\vec{{𝒗}}_{nom}`$, where $`\delta{𝜽}^{\times}`$ represents a skew-symmetric matrix of small angle misalignments, and $`\Delta\vec{{𝒗}}_{nom}`$ is the nominal maneuver vector. Thus, $`\Delta\vec{{𝒗}}_{nom}^{\times}\delta{𝜽}`$ is the error in the velocity increment due to maneuver direction errors, or if sensed accelerations are being fed-forward into the dynamics, due to IMU misalignments. To model these direction errors as a process noise term, let

```math
{𝐁}(t) = \begin{bmatrix} {𝟎}_{3\times 3} \\ \Delta\vec{{𝒗}}_{nom}^{\times} \end{bmatrix} \qquad\qquad(3.50)
```

and let $`q_\theta`$ be the intensity of the maneuver direction noise. Then the SNC-style process noise for accommodating maneuver direction errors becomes

```math
{𝐒}_i = q_\theta \begin{bmatrix} -(\Delta\vec{{𝒗}}_{nom}^{\times})^2\dfrac{\Delta t^3}{3} & -(\Delta\vec{{𝒗}}_{nom}^{\times})^2\dfrac{\Delta t^2}{2} \\[2ex] -(\Delta\vec{{𝒗}}_{nom}^{\times})^2\dfrac{\Delta t^2}{2} & -(\Delta\vec{{𝒗}}_{nom}^{\times})^2\Delta t \end{bmatrix} \qquad\qquad(3.51)
```

since $`\Delta\vec{{𝒗}}_{nom}^{\times}\Delta\vec{{𝒗}}_{nom}^{\times{𝖳}} = -(\Delta\vec{{𝒗}}_{nom}^{\times})^2`$. A version of this method was used by the Space Shuttle during powered flight with IMU-sensed accelerations.

#### 3.2.3.3. Dynamic Model Compensation

The DMC approach assumes the presence of exponentially-correlated acceleration biases, which are included as additional solve-fors in the filter state. As Chapter [6](06-bias-modeling-part1.md#page-72-0) and Appendix [A](13-appendix-a-models-and-realizations-of-random-variables.md#page-146-0) discuss, a model for such biases is given by

```math
b(t + \Delta t) = \mathrm{e}^{-\frac{\Delta t}{\tau}}\, b(t) + \varpi(t) \qquad\qquad(3.52)
```

where $`b(t_o) \sim N(0, p_{bo})`$, and $`\varpi(t) \sim N\!\left(0, \frac{q\tau}{2}\left(1 - \mathrm{e}^{-\frac{2\Delta t}{\tau}}\right)\right)`$. As Chapter [6](06-bias-modeling-part1.md#page-72-0) discusses, $`\tau`$ is a time constant controlling the "smoothness" of the random process, and $`q`$ is a power spectral density that describes the intensity of the random input. While Chapter [6](06-bias-modeling-part1.md#page-72-0) discusses a variety of other bias models that might be used, the exponentially-correlated model has proved to be a *best practice* for applications in which there are measurements continually available to persistently excite it. Refer to Chapter [6](06-bias-modeling-part1.md#page-72-0) for a fuller discussion of the relative merits of various bias modeling approaches.

As above, without loss of generality we can assume the acceleration biases are aligned with the RTN frame, and again assume that $`\Delta t`$ is small enough that a 1<sup>st</sup>-order Taylor series truncation is adequate for modeling the portion of the STM corresponding to position and velocity errors. With these assumptions, the terms appearing the integrand of [\(3.44\)](#page-45-3) become

```math
{𝐁}(t) = {𝐁}_{rtn} = \begin{bmatrix} {𝟎}_{3\times 3} \\ {𝟎}_{3\times 3} \\ {𝐌}_{rtn} \end{bmatrix} \qquad\qquad(3.53)
```

and

```math
{𝚽}(t + \Delta t, t) = \begin{bmatrix} {𝐈}_3 & \Delta t{𝐈}_3 & \left\{\tau\Delta t - \tau^2(1 - \mathrm{e}^{-\Delta t/\tau})\right\}{𝐈}_3 \\ {𝟎}_{3\times 3} & {𝐈}_3 & \tau(1 - \mathrm{e}^{-\Delta t/\tau}){𝐈}_3 \\ {𝟎}_{3\times 3} & {𝟎}_{3\times 3} & \mathrm{e}^{-\Delta t/\tau}\,{𝐈}_3 \end{bmatrix} \qquad\qquad(3.54)
```

and the process noise covariance becomes[<sup>3</sup>](#page-48-0)

<span id="page-48-1"></span>

```math
{𝐒}_i = \begin{bmatrix} \gamma_{pp}\tilde{{𝐐}} & \gamma_{pv}\tilde{{𝐐}} & \gamma_{pa}\tilde{{𝐐}} \\ \gamma_{pv}\tilde{{𝐐}} & \gamma_{vv}\tilde{{𝐐}} & \gamma_{va}\tilde{{𝐐}} \\ \gamma_{pa}\tilde{{𝐐}} & \gamma_{va}\tilde{{𝐐}} & \gamma_{aa}\tilde{{𝐐}} \end{bmatrix} \qquad\qquad(3.55)
```

with

```math
\gamma_{pp} = \tfrac{\tau^5}{2}\left\{\left(1 - \mathrm{e}^{-2\Delta t/\tau}\right) + \tfrac{2\Delta t}{\tau}\left(1 - 2\,\mathrm{e}^{-\Delta t/\tau}\right) - 2\left(\tfrac{\Delta t}{\tau}\right)^2 + \tfrac{2}{3}\left(\tfrac{\Delta t}{\tau}\right)^3\right\} \qquad\qquad(3.56)
```

```math
\gamma_{pv} = \tfrac{\tau^4}{2}\left\{\left(\mathrm{e}^{-2\Delta t/\tau} - 1\right) - 2\left(\mathrm{e}^{-\Delta t/\tau} - 1\right) + \tfrac{2\Delta t}{\tau}\left(\mathrm{e}^{-\Delta t/\tau} - 1\right) + \left(\tfrac{\Delta t}{\tau}\right)^2\right\} \qquad\qquad(3.57)
```

```math
\gamma_{pa} = \tfrac{\tau^3}{2}\left\{\left(1 - \mathrm{e}^{-2\Delta t/\tau}\right) - \tfrac{2\Delta t}{\tau}\,\mathrm{e}^{-\Delta t/\tau}\right\} \qquad\qquad(3.58)
```

```math
\gamma_{vv} = \tfrac{\tau^3}{2}\left\{\left(1 - \mathrm{e}^{-2\Delta t/\tau}\right) - 4\left(1 - \mathrm{e}^{-\Delta t/\tau}\right) + 2\Delta t/\tau\right\} \qquad\qquad(3.59)
```

```math
\gamma_{va} = \tfrac{\tau^2}{2}\left(1 - \mathrm{e}^{-\Delta t/\tau}\right)^2 \qquad\qquad(3.60)
```

```math
\gamma_{aa} = \tfrac{\tau}{2}\left(1 - \mathrm{e}^{-2\Delta t/\tau}\right) \qquad\qquad(3.61)
```

This analytic result for the DMC model first appeared in [[18](16-bibliography.md#page-170-10)].

<span id="page-48-0"></span><sup>3</sup> In [\(3.55\)](#page-48-1), the matrix $`\tilde{{𝐐}}`$ has the same form as it does for the SNC method, but with $`\sqrt{q_i}`$, $`i = r, t, n`$ now representing acceleration intensities, with units of meters per second$`^{5/2}`$. Also note that [\(3.55\)](#page-48-1) assumes the same time constant is applicable to all three acceleration channels. While this is usually sufficient, it is straightforward to extend [\(3.55\)](#page-48-1) to accommodate separate time constants for each channel.

#### 3.2.3.4. Explicit Dynamic Biases

While the DMC approach allows for quite general estimation of otherwise unmodeled forces on the spacecraft, it is often the case that the domain of application provides context that can narrow the filter designer's focus. For example, it may be the case that the only under-modeled force of appreciable significance on the spacecraft is drag, or perhaps solar radiation pressure, within the context of the application. Alternatively, the application may require much higher resolution models than DMC, which might necessitate estimation of smaller forces with larger uncertainties such as Earth radiation pressure, spacecraft thermal emission, etc., or panel-based modeling of drag and/or solar radiation pressure, etc. In such cases, it is often useful to tailor the DMC approach so that it estimates model-specific biases, such a drag or SRP corrections, rather than modeling three general RTN biases. Similarly, during powered flight, maneuver magnitude and direction errors might be more successfully modeled explicitly.

As an example of an explicit bias, consider estimating a multiplicative correction to the density; a similar approach may be used for drag or solar radiation pressure coefficients. Let $`t`$ denote geocentric coordinate time. Let $`{ℛ}`$ denote a planetary-body-fixed, body-centric system of coordinates, aligned with the central body's rotation axis. Let $`{ℐ}`$ denote a body-centric, celestially-referenced system of coordinates, aligned with $`{ℛ}`$ at an epoch $`t_o`$. Let $`\vec{{𝒓}}`$ represent the position of the center of gravity of a satellite, expressed in $`{ℐ}`$. Let $`\vec{{𝒗}}`$ represent the satellite's velocity within $`{ℐ}`$. Let $`\vec{{𝒗}}_r`$ represent the satellite's velocity within frame $`{ℛ}`$. Assume that $`\vec{{𝒓}}`$ evolves with respect to $`t`$ and $`{ℐ}`$ in the vicinity of $`t_o`$ according to

```math
\frac{{}^{{ℐ}}\mathrm{d}^2}{\mathrm{d}t^2}\vec{{𝒓}} = -\frac{\mu}{r^3}\vec{{𝒓}} - \frac{1}{2}C_D\frac{A}{m}\rho\left(1 + \frac{\delta\rho}{\rho}\right)v_r\vec{{𝒗}}_r \qquad\qquad(3.62)
```

where $`r = \|\vec{{𝒓}}\|`$, $`v_r = \|\vec{{𝒗}}_r\|`$, $`\delta\rho`$ is an atmospheric density disturbance, $`\rho`$ is the undisturbed atmospheric density, $`A`$ is the area of the satellite in a plane normal to $`\vec{{𝒗}}_r`$, $`m`$ is the satellite mass, and $`C_D`$ is the satellite's coefficient of drag. Assume that $`\delta\rho/\rho`$ is a random process that formally evolves as a first-order Gauss-Markov process, similar to a DMC bias:

```math
\frac{\mathrm{d}}{\mathrm{d}t}\left(\frac{\delta\rho}{\rho}\right) = -\frac{1}{\tau}\left(\frac{\delta\rho}{\rho}\right) + w_\rho \qquad\qquad(3.63)
```

where $`q_\rho`$ is the intensity of $`w_\rho`$. Let the state vector be $`{𝐱} = [\vec{{𝒓}}', \vec{{𝒗}}', (\delta\rho/\rho)]'`$. With these assumptions, the state dynamics and noise input partials are

```math
{𝐀}(t) = \begin{bmatrix} {𝟎}_{3\times 3} & {𝐈}_3 & {𝟎}_{3\times 1} \\ {𝐆}(t) + {𝐃}_r(t) & {𝐃}_v(t) & \vec{{𝒅}}(t) \\ {𝟎}_{1\times 3} & {𝟎}_{1\times 3} & -1/\tau \end{bmatrix}, \; {𝐁}(t) = \begin{bmatrix} {𝟎}_{3\times 1} \\ {𝟎}_{3\times 1} \\ 1 \end{bmatrix} \qquad\qquad(3.64)
```

where $`{𝐆}(t)`$ is the gravity gradient matrix, $`\vec{{𝒅}}(t) = -\frac{1}{2}C_D\frac{A}{m}\rho v_r\vec{{𝒗}}_r`$ is the nominal drag acceleration, and $`{𝐃}_r`$ and $`{𝐃}_v`$ are partials of the drag acceleration with respect to position and velocity, respectively[<sup>4</sup>](#page-49-0).

<span id="page-49-0"></span><sup>4</sup> The sensitivity $`{𝐃}_r`$ contains terms that are roughly proportional to the drag acceleration magnitude divided by the atmospheric scale height, and to the product of drag acceleration magnitude and the ratio of planetary rotation rate to speed relative to the atmosphere. For nearly all spacecraft, these terms will be many orders magnitude smaller than the gravity gradient, which is proportional to the gravity acceleration divided by the radius. So $`{𝐃}_r`$ can usually be neglected. For reference, $`{𝐃}_v = -\frac{1}{2}C_D\frac{A}{m}\rho v_r(\vec{{𝒖}}_{v_r}\vec{{𝒖}}_{v_r}' + {𝐈}_3)`$, and $`{𝐃}_r = d/R_s(\vec{{𝒖}}_r\vec{{𝒖}}_{v_r}') - {𝐃}_v\vec{{𝝎}}^{\times}`$, where $`\vec{{𝝎}}^{\times}`$ is the skew-symmetric "cross-product" matrix formed from the central body's rotation rate vector, and the notation $`\vec{{𝒖}}_{(\cdot)}`$ indicates the unit vector of its subscript.

Using the DMC results from above, with the assumption that the nominal drag acceleration is approximately constant over the integration time, $`\Delta t`$, the term $`{𝚽}(t + \Delta t, t){𝐁}(t)`$ appearing in the integrand of [\(3.44\)](#page-45-3) becomes

```math
{𝚽}(t + \Delta, t){𝐁}(t) = \begin{bmatrix} \left\{\tau\Delta t - \tau^2(1 - \mathrm{e}^{-\Delta t/\tau})\right\}\vec{{𝒅}} \\ \tau(1 - \mathrm{e}^{-\Delta t/\tau})\vec{{𝒅}} \\ \mathrm{e}^{-\Delta t/\tau} \end{bmatrix} \qquad\qquad(3.65)
```

and the process noise for a proportional density bias becomes

```math
{𝐒}_i = q_\rho \begin{bmatrix} \gamma_{pp}\vec{{𝒅}}\vec{{𝒅}}' & \gamma_{pv}\vec{{𝒅}}\vec{{𝒅}}' & \gamma_{pa}\vec{{𝒅}} \\ \gamma_{pv}\vec{{𝒅}}\vec{{𝒅}}' & \gamma_{vv}\vec{{𝒅}}\vec{{𝒅}}' & \gamma_{va}\vec{{𝒅}} \\ \gamma_{pa}\vec{{𝒅}}' & \gamma_{va}\vec{{𝒅}}' & \gamma_{aa} \end{bmatrix} \qquad\qquad(3.66)
```

#### 3.2.3.5. Episodic Dynamic Biases

It has sometimes been found to be the case, particularly for crewed missions, that episodic spacecraft activities can produce un-modeled accelerations. In the early days of manned spaceflight, events such as vents, momentum unloads, thruster-based attitude control firings, etc. that may perturb a spacecraft's trajectory were not well modeled, and came to be described as FLAK, which was supposed to be an acronym for (un)-Fortunate Lack of Acceleration Knowledge.

If the mean time between such activities can be characterized, along with the expected intensity of the acceleration, a compound Poisson-Gaussian process noise model may be effective. Conveniently, it turns out that the covariance of a linear system driven by a train of Gaussiandistributed impulses whose arrival times follow a Poisson distribution is the same as the covariance of the same system driven by a white noise input process, except for the scaling of the process noise covariance by the Poisson process rate parameter [[32](16-bibliography.md#page-171-4)].

To understand this result, consider a linear model of the error in a spacecraft trajectory as follows

```math
\dot{{𝘅}}(t) = {𝐀}(t){𝘅}(t) + {𝐁}(t){𝘂}(t) \qquad\qquad(3.67)
```

where $`{𝘅}`$ represents the deviation of the actual position/velocity state from its estimated or nominal value, and $`{𝘂}`$ represents the FLAK acceleration bias. Then, if we make use of inertial coordinates,

```math
{𝐀}(t) = \begin{bmatrix} {𝟎} & {𝐈} \\ {𝐆}(t) & {𝟎} \end{bmatrix}, \; {𝐁}(t) = \begin{bmatrix} {𝟎} \\ {𝐌}(t) \end{bmatrix} \qquad\qquad(3.68)
```

where $`{𝐆}`$ represents the gravity gradient matrix, and $`{𝐌}`$ is the direction cosine matrix rotating the supposed body-fixed FLAK into the inertial frame. There is no general solution to this differential equation, but over short time intervals, we can assume that

```math
{𝘅}(t_k) = {𝚽}(t_k, t_{k-1}){𝘅}_{k-1} + \int_{t_{k-1}}^{t_k} {𝚽}(t_k, \tau){𝐁}(\tau){𝘂}(\tau)\, \mathrm{d}\tau \qquad\qquad(3.69)
```

where

```math
{𝚽}(t_k, t_{k-1}) = {𝐈} + {𝐀}(t_k)(t_k - t_{k-1}) \qquad\qquad(3.70)
```

We assume the input is a sequence of velocity impulses of (random) length $`n_k`$,

```math
{𝘂}(t) = \sum_{i=1}^{n_k} {𝘂}_i\delta(t - t_i) \qquad\qquad(3.71)
```

with $`t_{k-1} \lt t_i \lt t_k`$. The delta functions annihilate the integral and our model becomes (with $`\Delta t_i = t_k - t_i`$):

```math
{𝘅}(t_k) = {𝚽}(t_k, t_{k-1}){𝘅}_{k-1} + \sum_{i=1}^{n_k} \begin{bmatrix} \vec{{𝜿}}_i\Delta t_i \\ \vec{{𝜿}}_i \end{bmatrix} \|{𝘂}_i\| \qquad\qquad(3.72)
```

where $`\vec{{𝜿}}_i`$ is the unit inertial direction vector for the FLAK event. Note that the input response is in some sense fundamentally an increment to the entire state vector at each $`t_k`$; we can however compute an equivalent zero-order hold acceleration by dividing the velocity increment by the time step $`t_k - t_{k-1}`$.

Since we assume each impulse is zero-mean and Gaussian, the input response has zero mean. To find a tractable form for the covariance, assume that the direction of the FLAK event is constant over each interval $`t_k - t_{k-1}`$. This assumption assures that the impulses are identically distributed over each sampling interval. Then, the process noise covariance is given by Reference [32](16-bibliography.md#page-171-4):

```math
{𝐒}(t_k) = q\lambda\int_{t_{k-1}}^{t_k} \begin{bmatrix} \vec{{𝜿}}_k(t_k - \tau) \\ \vec{{𝜿}}_k \end{bmatrix} \begin{bmatrix} \vec{{𝜿}}_k'(t_k - \tau), \vec{{𝜿}}_k' \end{bmatrix} \mathrm{d}\tau \qquad\qquad(3.73)
```

where $`q`$ is the variance of the discrete Gaussian velocity impulses and $`\lambda`$ is the rate parameter of the Poisson process. Carrying out the integration results in

```math
{𝐒}(t_k) = q\lambda \begin{bmatrix} \vec{{𝜿}}_k\vec{{𝜿}}_k'\Delta t^3/3 & \vec{{𝜿}}_k\vec{{𝜿}}_k'\Delta t^2/2 \\ \vec{{𝜿}}_k\vec{{𝜿}}_k'\Delta t^2/2 & \vec{{𝜿}}_k\vec{{𝜿}}_k'\Delta t \end{bmatrix} \qquad\qquad(3.74)
```

where the product $`q\lambda`$ must have "SNC" kinds of units, such as meters$`^2`$ per second$`^3`$.

#### 3.2.3.6. Computational Considerations

The primary computational issues that can affect covariance propagation may be broadly characterized as underflow and overflow. Underflow can occur especially because many of the process noise parameters described above may often have values that approach computational truncation limits, which can lead to non-positive-definite process noise covariances. Overflow can similarly occur when truncation limits are approached by very large covariance values such as can occur with long propagation times. Because the orbital dynamics are at best marginally stable, even propagating without process noise can result in differences of many orders of magnitude between largest and smallest eigenvalues. This problem will be exacerbated if process noise is present, since all of the process noise models described above introduce unbounded position covariance error growth[<sup>5</sup>](#page-51-0).

<span id="page-51-0"></span><sup>5</sup> Reference [11](16-bibliography.md#page-170-11) proposes an approximate "solution" to this problem via a Floquet analysis of a modified set of covariance propagation dynamics that include artificially-introduced damping.

Simple tricks like enforcing symmetry, or adding a small positive diagonal matrix, will not always ensure positive eigenvalues in such cases. A better solution is to maintain the covariance in factorized form, for example as Chapter [8](08-factorization-methods-part1.md#page-94-0) describes. In lieu of a fully factorized filtering approach, process noise factors may be computed from their factorizations. Chapter [6](06-bias-modeling-part1.md#page-72-0) shows a few examples of Cholesky factorizations that may be employed in this fashion.

---

[← Chapter 3. The Covariance Matrix (part 1 of 3)](03-the-covariance-matrix-part1.md) · [Contents](README.md) · [Chapter 3. The Covariance Matrix (part 3 of 3) →](03-the-covariance-matrix-part3.md)
