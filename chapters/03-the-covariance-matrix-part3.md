[← Chapter 3. The Covariance Matrix (part 2 of 3)](03-the-covariance-matrix-part2.md) · [Contents](README.md) · [Chapter 4. Processing Measurements →](04-processing-measurements.md)

*Chapter 3. The Covariance Matrix, continued*

### 3.2.4. Tuning the Covariance Propagation

Since even the best practices this Chapter has discussed are at best approximations, it is inevitable that EKF designers must perform some artful tuning of the free parameters to achieve acceptable results. Furthermore, computational limitations of flight computers often lead to the need for compromises in modeling fidelity. What one generally hopes to accomplish via tuning of the covariance propagation is that any approximations or compromises the EKF has had to endure to be implementable have not impaired its covariance's accuracy too much. In particular, one would like to compute an idealized "truth" covariance matrix, based on the best-available models and data, and adjust the EKF's "formal" covariance via the tuning process to yield some semblance of a match.

In some cases, it is possible to compute the true covariance. In particular, if we are studying a linear system, and the random components have zero-mean Gaussian distributions, then the mean errors will be zero, and we can use linear covariance analysis [[27](16-bibliography.md#page-171-5), [58](16-bibliography.md#page-172-2), [60](16-bibliography.md#page-172-3)] to compute the covariances. It is often possible to approximate the performance for a nonlinear system with this technique by linearization. This is often a first step in early conceptual design studies.

One may divide tuning of the covariance propagation into those activities a designer performs (1) during the detailed development of a system, prior to the collection of any flight data, and (2) during the commissioning of a new system or an existing system in a new application, when flight data are available. For pre-flight detailed design studies, one generally simulates the system, so one has access to truth data. One can also run the mission simulation many times, generating an ensemble of parallel results, performing a Monte Carlo analysis. During and after the actual mission, we never have access to truth data. At best, we can reconstruct the trajectory after the fact using more sophisticated processing and additional data that were not available in real-time. For near real-time analysis, we can compare current state estimates to predictions from previous epochs. These predictions can come from either mission products generated in real-time at a past epoch, or past reconstructions of the trajectory. In all cases, the best we have are differences between estimates, not errors from the truth. There are several empirical approximations to the true covariance that one might use in these situations.

#### 3.2.4.1. Empirical Approximations of the True Covariance

Let $`{𝗲}_j(t_i)`$ represent the random error vector at time $`t_i`$ for case $`j`$ from a Monte Carlo simulation, and $`\{{𝗲}(t_i)\}`$ be the set of all cases at time $`t_i`$. Assume the total number of cases is $`K`$, and the total number of time samples is $`N`$.

**Time Series Expectation:** We can take statistics of the error realizations across time for each case, $`{𝒆}_j(t_i)`$, to get the time series expectations for each case:

```math
\hat{\mathrm{E}}_t({𝗲}_j) = \frac{1}{N}\sum_{i=1}^{N} {𝒆}_j(t_i) \qquad\qquad(3.75)
```

```math
\hat{\mathrm{E}}_t({𝗲}_j{𝗲}_j^{{𝖳}}) = \frac{1}{N-1}\sum_{i=1}^{N} {𝒆}_j(t_i){𝒆}_j^{{𝖳}}(t_i) \qquad\qquad(3.76)
```

If the data are stationary[<sup>6</sup>](#page-52-0), the time series statistics are usually an adequate approximation, if we have considered a long enough time span. In some systems, described as *ergodic*, a long time series is in some sense equivalent to a large number of shorter Monte Carlo cases.

<span id="page-52-0"></span><sup>6</sup> Stationary data are those for which the statistics do not change when the time origin shifts.

**Ensemble Expectation:** We can take statistics of the error realizations over all the cases at each time sample to get the ensemble expectations:

```math
\hat{\mathrm{E}}_e\{{𝗲}(t_i)\} = \frac{1}{K}\sum_{j=1}^{K} {𝒆}_j(t_i) \qquad\qquad(3.77)
```

```math
\hat{\mathrm{E}}_e\{{𝗲}(t_i){𝗲}^{{𝖳}}(t_i)\} = \frac{1}{K-1}\sum_{j=1}^{K} {𝒆}_j(t_i){𝒆}_j^{{𝖳}}(t_i) \qquad\qquad(3.78)
```

The ensemble statistics will generally give the best indication of performance if the data are non-stationary, so long as we use an adequate number of Monte Carlo cases.

Since there is nothing analogous to an ensemble of Monte Carlo cases for flight data, we cannot use ensemble statistics as defined above. Let $`{𝗱}`$ represent the random difference vector between the quantity of interest and its comparison value. We can apply time series statistics, but as the mission evolves, the span of the time series continually extends, so we have to decide which subsets of the entire mission span to use, e.g. the time series extending back over the entire history of the mission, extending back only over some shorter interval, etc., and also how frequently to recompute the time series statistics, e.g. continuously, once per day, etc. There are some other approximations to the expectation that we might use here.

**Sliding Window Time Series Expectation:** We can take statistics of the difference realizations, $`{𝒅}(t_i)`$, across a sliding window extending $`\Delta t`$ into the past from each observation, for each case, to get the $`\Delta t`$-sliding window time series expectations:

```math
\hat{\mathrm{E}}_{t,\Delta t}({𝗱}) = \frac{1}{\Delta n}\sum_{i=0}^{\Delta n - 1} {𝒅}(t_{N-i}) \qquad\qquad(3.79)
```

```math
\hat{\mathrm{E}}_{t,\Delta t}({𝗱}{𝗱}^{{𝖳}}) = \frac{1}{\Delta n - 1}\sum_{i=0}^{\Delta n - 1} {𝒅}(t_{N-i}){𝒅}(t_{N-i})^{{𝖳}} \qquad\qquad(3.80)
```

where $`\Delta n`$ is the number of time samples in the window $`\Delta t`$.

**Period-Folding Expectation:** If the data are periodic, we can break up the data into $`K`$ spans of one period in duration each, and shift the time origin of each span so that the data are "folded" into the same, one-period-long interval. We can then take ensemble statistics over times at the same phase angle, $`t_{\phi i}`$, within each period.

```math
\hat{\mathrm{E}}_f\{{𝗱}(t_{\phi i})\} = \frac{1}{K}\sum_{j=1}^{K} {𝒅}_j(t_{\phi i}) \qquad\qquad(3.81)
```

```math
\hat{\mathrm{E}}_f\{{𝗱}(t_{\phi i}){𝗱}(t_{\phi i})^{{𝖳}}\} = \frac{1}{K-1}\sum_{j=1}^{K} {𝒅}_j(t_{\phi i}){𝒅}_j^{{𝖳}}(t_{\phi i}) \qquad\qquad(3.82)
```

It is often useful to fold the data into bins of equal mean anomaly. This is especially useful for orbits with notable eccentricity, since it ensures that a roughly equal number of time points will be present in each bin.

**Sliding Window Period-Folding Expectation:** Period-folding can obviously be applied over a sliding window as well, with each window extending $`n`$ periods into the past.

```math
\hat{\mathrm{E}}_{f,n}\{{𝗱}(t_{\phi i})\} = \frac{1}{n}\sum_{j=0}^{n-1} {𝒅}_{K-j}(t_{\phi i}) \qquad\qquad(3.83)
```

```math
\hat{\mathrm{E}}_{f,n}\{{𝗱}(t_{\phi i}){𝗱}(t_{\phi i})^{{𝖳}}\} = \frac{1}{n-1}\sum_{j=0}^{n-1} {𝒅}_{K-j}(t_{\phi i}){𝒅}_{K-j}^{{𝖳}}(t_{\phi i}) \qquad\qquad(3.84)
```

This is especially useful for identifying secular trends in periodic data sets.

#### 3.2.4.2. Tuning for Along-track Error Growth

As described above, the position error component along the orbit track will dominate covariance propagation error, and so the most important step in tuning the covariance propagation is to ensure that this component grows no faster or slower than it should based on the truncations and approximations that the EKF design has employed. One may use any of the analytical or empirical methods described above to estimate the "true" covariance. For example, for preflight analysis, one may generate a time series or ensemble of time series of differences between states propagated using the formal models the filter employs, and a best available "truth" model of the system. One can then compare the appropriate empirical covariance computed from this data set to the filter's formal covariance, and adjust the process noise intensities until a reasonable match occurs. For flight data analysis, one may similarly difference across overlaps between predictive and definitive states, and compare these empirical covariances of these differences to the sum of the predictive and definitive formal covariances from the filter.

If one uses the SNC method, the primary "knob" for tuning the alongtrack covariance growth rate is the corresponding alongtrack component of the process noise intensity $`q_T`$ or $`q_V`$, depending on whether RTN or VNB components are used, respectively. Essentially, an impulse along the velocity vector, or change in speed, causes a change in SMA, corresponding to a change in period, and hence a secular growth in position error along the orbit, as discussed at the beginning of this Chapter. This mechanism is especially transparent for near-circular orbits, and some simple analysis yields a good starting point. One may find a fuller exposition of the following result in Reference [28](16-bibliography.md#page-171-6).

<span id="page-54-1"></span>For near-circular orbits, the position components of the integrand in [\(3.44\)](03-the-covariance-matrix-part2.md#page-45-3) become, in RTN coordinates,

```math
{𝚽}_{rv}(\Delta t) \begin{bmatrix} q_R & 0 & 0 \\ 0 & q_T & 0 \\ 0 & 0 & q_N \end{bmatrix} {𝚽}_{rv}^{{𝖳}}(\Delta t) \qquad\qquad(3.85)
```

where $`{𝚽}_{rv}(\Delta t)`$ is given, per Hill, Clohessy, and Wiltshire, by

```math
{𝚽}_{rv}(\Delta t) = \begin{bmatrix} \sin(n\Delta t)/n & 2(1 - \cos(n\Delta t))/n & 0 \\ 2(\cos(n\Delta t) - 1)/n & 4\sin(n\Delta t)/n - 3\Delta t & 0 \\ 0 & 0 & \sin(n\Delta t)/n \end{bmatrix} \qquad\qquad(3.86)
```

Retaining only secular terms and carrying out the integral, the along-track component of the process noise covariance becomes

```math
S_T(\Delta t) \approx 3\Delta t^3 q_T \qquad\qquad(3.87)
```

an approximation which holds for $`\Delta t \gt T_p`$. Thus, one may use an empirical covariance of the along-track error after one orbit period, such as $`\hat{\sigma}_{\delta s}^2 = \hat{\mathrm{E}}_f\{\delta s^2\}`$, to derive a starting point from which to tune $`q_T`$, as

```math
q_T = \frac{\hat{\sigma}_{\delta s}^2}{3T_p^3} \qquad\qquad(3.88)
```

## 3.3. Covariance Measurement Update

<span id="page-54-0"></span>This section discusses methods for implementing the covariance measurement update. Some of the most important of these best practices are related to factorization methods and underweighting, which are topics of enough significance to warrant their own chapters.

### 3.3.1. "Stable Form" of non-Joseph Covariance Update

As Chapter [1](01-the-extended-kalman-filter.md#page-24-0) pointed out, only for the optimal gain and true covariance does the Joseph form of the covariance measurement update, [\(1.41\)](01-the-extended-kalman-filter.md#page-29-1),

```math
{𝐏}_i^+ = \left({𝐈} - {𝐊}_i{𝐇}_i\right) {𝐏}_i^- \left({𝐈} - {𝐊}_i{𝐇}_i\right)^{{𝖳}} + {𝐊}_i{𝐑}_i{𝐊}_i^{{𝖳}} \qquad\qquad(3.89)
```

reduce to [\(1.33\)](01-the-extended-kalman-filter.md#page-28-3),

```math
{𝐏}_i^+ = {𝐏}_i^- - {𝐊}_i {𝐇}_i {𝐏}_i^- \qquad\qquad(3.90)
```

While this assertion is strictly true, the cancellations that produce the above results will still occur so long as the EKF algorithm is internally consistent with truncating and approximating its various terms. The resulting "covariance" will not accurately represent $`\mathrm{E}\big[{𝗲}_i^+ ({𝗲}_i^+)^{{𝖳}} \vert {𝕐}_i\big]`$, but the fact that these truncations and approximations have produced a suboptimal gain will, in themselves, provide no computational issues. In effect, the resulting suboptimal gain remains "optimal" with respect to the internally consistent set of approximations and truncations internal to the filter.

However, even if the gain is optimal, the stability of the non-Joseph form depends on the order of multiplication, as Schmidt points out [[75](16-bibliography.md#page-173-5)]. He describes a "stable form" of the non-Joseph update, given by Algorithm [3.1,](#page-55-0) which was successfully used by the Space Shuttle. Algorithm [3.1](#page-55-0) processes each $`j`$th scalar element of the measurement vector one at a time, using only the $`j`$th row of the measurement partials matrix, $`{𝐡}_j`$, and the $`(j, j)`$ diagonal element of the measurement noise covariance, $`r_j`$, assuming $`{𝐑}_i`$ is a diagonal matrix. In comparison with $`{𝐏}_i^+ = ({𝐈} - {𝐊}_i{𝐇}_i){𝐏}_i^-`$, use of Algorithm [3.1](#page-55-0) also reduces the computational burden from $`O(n^3)`$ to $`O(n^2/2)`$, where $`n`$ is the state dimension.

Although Algorithm [3.1](#page-55-0) does not show the state update, it may also be sequentially updated as part of the iteration. However, the order in which the scalar measurements update the state can affect the outcome, if the measurement partials are computed one row at a time, corresponding with each scalar update. This may produce undesirable or even unstable outcomes. Chapter [4](04-processing-measurements.md#page-58-0) will discuss such issues further.

> <span id="page-55-0"></span>**Algorithm 3.1** "Stable form" of the non-Joseph Covariance Measurement Update
>
> $`{𝐏}_1 = {𝐏}_i^-`$
>
> **for** each scalar measurement $`j = 1`$ through $`k`$ **do**
>
> &emsp;$`{𝐡}_j = j`$th row of $`{𝐇}_i`$
>
> &emsp;$`r_j = (j, j)`$ element of $`{𝐑}_i`$
>
> &emsp;$`{𝐛}_j = {𝐏}_j {𝐡}_j^{{𝖳}}`$
>
> &emsp;$`{𝐤}_j = {𝐛}_j / ({𝐡}_j {𝐛}_j + r_j)`$
>
> &emsp;$`{𝐏}_j \leftarrow {𝐏}_j - {𝐤}_j {𝐛}_j^{{𝖳}}`$
>
> **end for**
>
> $`{𝐏}_i^+ = {𝐏}_k`$
>
> Only the non-redundant (upper or lower triangular) portions of the covariance should be updated, and then the other redundant elements set equal to the ones that have been computed.

Despite the extensive and successful flight heritage of Algorithm [3.1,](#page-55-0) it cannot guarantee numerical stability and positive definiteness of the covariance. Chapter [8](08-factorization-methods-part1.md#page-94-0) describes a recommended best practice for the covariance update, the $`UD`$-factorization, which makes checking for positive definiteness transparently easy.

### 3.3.2. Use of Consider States

It may often be the case that unobservable states are present in the system being estimated. Most commonly, such states will be parameters whose values are unknown or uncertain. Inclusion of such parameters as solve-for states in the EKF is a not a recommended practice. However, if the EKF completely ignores the uncertainty that such parameters introduce, its covariance can become overly optimistic, a condition sometimes known as "filter smugness." One approach to addressing this problem was introduced by Schmidt [[75](16-bibliography.md#page-173-5)], originally in the context of reducing the computational burden that the EKF imposed on flight computers of the 1960's. Schmidt's idea is essentially for the EKF to maintain a covariance containing all of the states whose uncertainties are significant enough to affect filter performance, but only to update a subset of those states. The states which are not updated in this framework are typically known as "consider" parameters, and such a filter has been called a "consider filter" or a "Schmidt-Kalman" filter. Although most commonly the state space is simply partitioned by selecting states as either solve-for or consider states, Reference [58](16-bibliography.md#page-172-2) points out that partitioning using linear combinations of the full state space is also possible.

Following Reference [58](16-bibliography.md#page-172-2), suppose the filter produces estimates for a subset of $`n_s`$ solve-for states, out of the full state of size $`n`$. The filter does not estimate the remaining $`n_c = n - n_s`$ consider states. Denote the true solve-for vector by $`{𝘀}(t)`$, and the true consider vector by $`{𝗰}(t)`$. Assume that these are linear combinations of the true states, according to the following:

<span id="page-55-1"></span>
```math
{𝘀}(t) = {𝐒}(t){𝘅}(t) \quad \text{and} \quad {𝗰}(t) = {𝐂}(t){𝘅}(t) \qquad\qquad(3.91)
```

where the $`n_s \times n`$ matrix $`{𝐒}(t)`$ and the $`n_c \times n`$ matrix $`{𝐂}(t)`$ are such that the matrix

```math
{𝐌} = \begin{bmatrix} {𝐒} \\ {𝐂} \end{bmatrix} \qquad\qquad(3.92)
```

is non-singular. The inverse of $`{𝐌}`$ is partitioned into an $`n \times n_s`$ matrix $`\tilde{{𝐒}}`$ and an $`n \times n_c`$ matrix $`\tilde{{𝐂}}`$:

```math
{𝐌}^{-1} = \begin{bmatrix} \tilde{{𝐒}}, & \tilde{{𝐂}} \end{bmatrix}. \qquad\qquad(3.93)
```

The properties of the matrix inverse then lead immediately to the identities

```math
{𝐒}\tilde{{𝐒}} = {𝐈}_{n_s}, \quad {𝐂}\tilde{{𝐂}} = {𝐈}_{n_c}, \quad {𝐒}\tilde{{𝐂}} = {𝟎}_{n_s \times n_c}, \quad {𝐂}\tilde{{𝐒}} = {𝟎}_{n_c \times n_s}, \qquad\qquad(3.94)
```

and

<span id="page-56-1"></span>
```math
\tilde{{𝐒}}{𝐒} + \tilde{{𝐂}}{𝐂} = {𝐈}_n. \qquad\qquad(3.95)
```

In the usual case that the elements of the solve-for and consider vectors are merely selected and possibly permuted components of the state vector, the matrix $`{𝐌}`$ is an orthogonal permutation matrix. In this case, and in any case for which $`{𝐌}`$ is orthogonal, the matrices $`\tilde{{𝐒}}`$ and $`\tilde{{𝐂}}`$ are just the transposes of $`{𝐒}`$ and $`{𝐂}`$, respectively, which makes inversion of $`{𝐌}`$ unnecessary and simplifies many of the following equations.

It follows from Eqs. [3.91](#page-55-1) and [3.95](#page-56-1) that

```math
{𝘅}(t) = \tilde{{𝐒}}(t){𝘀}(t) + \tilde{{𝐂}}(t){𝗰}(t). \qquad\qquad(3.96)
```

Relations similar to Eq. [3.91](#page-55-1) give the estimated solve-for vector $`\hat{{𝘀}}(t)`$ and the assumed consider vector $`\hat{{𝗰}}(t)`$ in terms of the estimated state $`\hat{{𝘅}}(t)`$. Thus, errors in the solve-for and consider states are given by

```math
{𝗲}_s(t) = {𝘀}(t) - \hat{{𝘀}}(t) = {𝐒}(t){𝗲}(t) \qquad\qquad(3.97)
```

```math
{𝗲}_c(t) = {𝗰}(t) - \hat{{𝗰}}(t) = {𝐂}(t){𝗲}(t) \qquad\qquad(3.98)
```

and the true error may be written in terms of the solve-for and consider errors by

```math
{𝗲}(t) = \tilde{{𝐒}}(t){𝗲}_s(t) + \tilde{{𝐂}}(t){𝗲}_c(t). \qquad\qquad(3.99)
```

In terms of this notation, the EKF update has the form

```math
\hat{{𝘀}}_i^+ = \hat{{𝘀}}_i^- + {𝐊}_i{𝗿}_i^- \qquad\qquad(3.100)
```

where

```math
{𝗿}_i^- = {𝘆}_i - {𝒉}(\hat{{𝘅}}_i^-) = {𝐇}_i{𝗲}_i^- + {𝘃}_i, \qquad\qquad(3.101)
```

and the subscript $`i`$ is a shorthand for the time argument $`t_i`$. The usual EKF will not contain the full covariance, but only its solve-for part

```math
{𝐏}_{ss}(t) = \mathrm{E}\Bigl[{𝗲}_s(t){𝗲}_s^{{𝖳}}(t)\Bigr] \qquad\qquad(3.102)
```

By contrast, the Schmidt-Kalman filter will use the full covariance, $`{𝐏}(t)`$. In the usual case, the Kalman gain is given by

```math
{𝐊}_i = {𝐏}_{ssi}^-{𝐇}_{si}^{{𝖳}}\Bigl[{𝐇}_{si}{𝐏}_{ssi}^-{𝐇}_{si}^{{𝖳}} + {𝐑}_i\Bigr]^{-1} \qquad\qquad(3.103)
```

where

```math
{𝐇}_{si} = {𝐇}_i\tilde{{𝐒}}_i \qquad\qquad(3.104)
```

In the Schmidt-Kalman case,

```math
{𝐊}_i = {𝐒}_i{𝐏}_i^-{𝐇}_i^{{𝖳}}\Bigl[{𝐇}_i{𝐏}_i^-{𝐇}_{si}^{{𝖳}} + {𝐑}_i\Bigr]^{-1} \qquad\qquad(3.105)
```

Thus, the Schmidt-Kalman gain matrix is computed from the full covariance, but only applies measurement innovations to the solve-for states.

## 3.4. Sigma-Point Methods

<span id="page-56-0"></span>Before concluding this Chapter, it is worth noting that a promising method for propagating and updating the covariance that is coming into greater use and acceptance within the navigation community is the use of sigma-point methods, also known as "unscented" transforms. A subsequent chapter covering Advanced Topics will cover these topics in a section on sigma-point filtering.

---

[← Chapter 3. The Covariance Matrix (part 2 of 3)](03-the-covariance-matrix-part2.md) · [Contents](README.md) · [Chapter 4. Processing Measurements →](04-processing-measurements.md)
