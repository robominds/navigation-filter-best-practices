[← Chapter 3. The Covariance Matrix (part 3 of 3)](03-the-covariance-matrix-part3.md) · [Contents](README.md) · [Chapter 5. Measurement Underweighting →](05-measurement-underweighting.md)

# <span id="page-58-2"></span><span id="page-58-0"></span>Chapter 4. Processing Measurements

*Contributed by Christopher N. D'Souza and J. Russell Carpenter*

This chapter will discuss how to handle real-world measurement processing issues. In particular, being able to handle measurements that aren't synchronous is of paramount importance to running filters in a real-time environment. As well, the performance of navigation filters which have nonlinear measurement models are susceptible to divergence depending on the order of processing of measurements which occur at the same epoch. Therefore, a technique which provides invariance to measurement processing is detailed. A technique for processing correlated measurements is presented, and brief comments on filter cascading and processing of inertial data are offered.

## 4.1. Measurement Latency

<span id="page-58-1"></span>In general, the measurement time tags are not going to be equal to the current filter epoch time, $`t_k`$. To state it another way, the measurements do not come in at the current filter time. Rather, they may be latent by up to $`p`$ seconds. Thus, a situation will arise where the filter has propagated its state and covariance to time $`t = t_k`$ from time $`t = t_{k-1}`$, and is subsequently given a measurement to be filtered (denoted by subscript $`m`$) that corresponds to the time $`t = t_m`$, where

```math
t_m \leq t_k \qquad\qquad(4.1)
```

If $`\Delta t = t_m - t_k`$ is not insignificant, the time difference between the measurement and the filter state and covariance will need to be accounted for during filtering in order to accurately process the measurement. This can be done in much the same way a batch filter operates (see pages 196-197 of Tapley [[81](16-bibliography.md#page-173-3)]). If the measurement at time $`t = t_m`$ is denoted as $`{𝗒}_m`$, the nominal filter state at that time is given by $`{𝗫}_m^* \equiv {𝗫}^*(t_m)`$ ($`*`$ denotes the nominal), and the measurement model is denoted as $`h_m\left({𝗫}_m, t_m\right)`$, then one can expand the measurement model to first order about the nominal filter state to get

```math
h_m\left({𝗫}_m, t_m\right) = h_m\Bigl({𝗫}_m^*, t_m\Bigr) + {𝐇}_m{𝘅}_m + \nu_m \qquad\qquad(4.2)
```

where $`{𝘅}_m = {𝗫}_m - {𝗫}_m^*`$ and $`{𝐇}_m`$ is defined as

```math
{𝐇}_m \triangleq \left( \frac{\partial h_m\left({𝗫}, t_m\right)}{\partial {𝗫}} \right)_{{𝗫}={𝗫}_m^*} \qquad\qquad(4.3)
```

The perturbed state at time $`t_m`$ can be written in terms of the state at time $`t_k`$ as follows

```math
{𝘅}_m = {𝚽}(t_m, t_k){𝘅}_k + {𝚪}_m{𝘄}_m \qquad\qquad(4.4)
```

so we can compute the measurement as

```math
h_m\left({𝗫}_m, t_m\right) = h_m\Bigl({𝗫}_m^*, t_m\Bigr) + {𝐇}_m{𝚽}(t_m, t_k){𝘅}_k + {𝐇}_m{𝚪}_m{𝘄}_m + \nu_m \qquad\qquad(4.5)
```

where the measurement noise has the characteristics $`\mathrm{E}[\nu_m] = 0`$ and $`\mathrm{E}\big[\nu_m^2\big] = R_m`$, the state process noise from $`t = t_m`$ to $`t = t_k`$ has the characteristics $`\mathrm{E}[{𝘄}_m] = {𝟬}`$ and $`\mathrm{E}[{𝘄}_m{𝘄}_m^{{𝖳}}] = {𝐐}_m`$, and the state deviation is given by

```math
{𝘅}_k = \delta{𝗫}_k = {𝗫}_k - {𝗫}_k^* \qquad\qquad(4.6)
```

(Note that the effect of the state process noise would be to increase the measurement noise variance. However, because the process noise term is very small over time periods of a few seconds, it can safely be neglected for the remainder of this analysis.)

Upon taking the conditional expectation of the measurement equation and rearranging, the scalar residual of the measurement is given by

```math
{𝗒}_m - \tilde{{𝐇}}_m\hat{{𝘅}}_k(-) = {𝖸}_m - h_m({𝗫}_m^*, t_m) - {𝐇}_m{𝚽}(t_m, t_k)\hat{{𝘅}}_k(-) \qquad\qquad(4.7)
```

where $`\hat{\cdot}`$ denotes an estimated value,

```math
\begin{aligned} {𝗒}_m &= {𝖸}_m - h_m({𝗫}_m^*, t_m) \\ \hat{{𝘅}}_k(-) &= \hat{{𝗫}}_k(-) - {𝗫}_k^* \end{aligned} \qquad\qquad(4.8)
```

The measurement partials that are used in the update, which map the measurement to the state at time $`t = t_k`$, are given by

<span id="page-59-1"></span>
```math
\tilde{{𝐇}}_m = {𝐇}_m{𝚽}(t_m, t_k) \qquad\qquad(4.9)
```

Eq. [4.9](#page-59-1) was derived by noting that

```math
\begin{aligned} {𝐇}_m\hat{{𝘅}}_m &= {𝐇}_m{𝚽}(t_m, t_k)\hat{{𝘅}}_k \\ &= \tilde{{𝐇}}_m\hat{{𝘅}}_k \end{aligned} \qquad\qquad(4.10)
```

From the above discussion, it is evident that the unknown quantities needed to update the state at time $`t = t_k`$ with a measurement from time $`t = t_m`$ are the nominal state at the measurement time, $`{𝗫}_m^*`$, and the state transition matrix relating the two times, $`{𝚽}(t_m, t_k)`$. Given those values, $`h_m\Bigl({𝗫}_m^*, t_m\Bigr)`$ and $`\tilde{{𝐇}}_m`$ can be calculated.

Thus the nominal state at the measurement time is calculated by back-propagating the filter state from time $`t_k`$ to time $`t_m`$. The same thing is done to calculate the required state transition matrix. The same propagation algorithms used in forward propagation ought to be utilized for the back-propagation, with the exception that the smaller time step allows for a $`1^{st}`$-order approximation of the matrix exponential used to update the state transition matrix.

## 4.2. Invariance to the Order of Measurement Processing

<span id="page-59-0"></span>It has long been known that the performance of an EKF is dependent on the order in which one processes measurements. This is of particular import in the case when there is powerful measurement coupled with a large *a priori* error. The state (and covariance) update will be large, very likely out of the linear range. Subsequent measurements which are processed may well be outside the residual edit thresholds, and hence will be rejected. In order to remedy this, we employ a hybrid Linear/Extended Kalman Filter measurement update. Recall that in an Extended Kalman Filter, the state is updated / relinearized / rectified after each measurement is processed, regardless of whether the measurements occur at the same time. Hence, the solution is highly dependent on the *order* in which the measurements are processed. This is not a desirable situation in which to be.

We obviate this difficulty simply by not updating the state until *all* the measurements at a given time are processed. We accumulate the state updates in state deviations $`{𝘅}`$, using Algorithm [4.1.](#page-60-1) This algorithm makes use of the fact that, in the absence of process noise, a batch/least squares algorithm is mathematically equivalent to a linear Kalman Filter [[33](16-bibliography.md#page-171-7)]. Algorithm [4.1](#page-60-1) is <span id="page-60-2"></span>a recommended *best practice*. Algorithm [4.1](#page-60-1) may readily be combined with the residual mapping approach described above when the measurements are asynchronous. Algorithm [4.1](#page-60-1) may also be readily combined with Algorithm [3.1,](03-the-covariance-matrix-part3.md#page-55-0) for cases in which the preferred factorized covariance methods are precluded.

> <span id="page-60-1"></span>**Algorithm 4.1** Measurement Update Invariant to Order of Processing
>
> **for** each (scalar) measurement $`j = 1`$ through $`k`$ **do**
>
> &emsp;$`{𝗒}_j = {𝖸}_j - h_j({𝗫}_m^*, t_m)`$
>
> &emsp;$`{𝐇}_j = \dfrac{\partial h_j}{\partial {𝗫}}({𝗫}_m^*, t_m)`$
>
> &emsp;$`{𝐊}_j = {𝐏}_j{𝐇}_j^{{𝖳}}\Bigl({𝐇}_j{𝐏}_j{𝐇}_j^{{𝖳}} + R_j\Bigr)^{-1}`$
>
> &emsp;$`\hat{{𝘅}}_j \leftarrow \hat{{𝘅}}_j + {𝐊}_j\left({𝗒}_j - {𝐇}_j\hat{{𝘅}}_j\right)`$
>
> &emsp;$`{𝐏}_j \leftarrow \left({𝐈} - {𝐊}_j{𝐇}_j\right){𝐏}_j\left({𝐈} - {𝐊}_j{𝐇}_j\right)^{{𝖳}} + {𝐊}_j R_j{𝐊}_j^{{𝖳}}`$
>
> **end for**
>
> $`{𝗫}_m \leftarrow {𝗫}_m^* + \hat{{𝘅}}_j`$

## 4.3. Processing Vector Measurements

<span id="page-60-0"></span>If the UDU factorization is used, the measurements are usually processed as scalars. If the vector measurements are correlated, one option is to assume they are uncorrelated and ignore the correlations between the measurements.

However, there is a better alternative. Given the measurement equation ($`{𝗬}_j = {𝐇}_j({𝗫}_j, t_j) + {𝝂}_j`$) with measurement error covariance matrix, $`{𝐑}_i`$, first decompose the matrix with a Cholesky factorization as

```math
{𝐑}_i = \mathrm{E}\big[{𝝂}_j{𝝂}_j^{{𝖳}}\big] = {𝐑}_i^{1/2}{𝐑}_i^{{𝖳}/2} \qquad\qquad(4.11)
```

and premultiply the measurement equation by $`{𝐑}_i^{-1/2}`$ to yield

```math
\tilde{{𝗬}}_j = \tilde{{𝐇}}_j({𝗫}_j, t_j) + \tilde{{𝝂}}_j \qquad\qquad(4.12)
```

with

```math
\tilde{{𝗬}}_j = {𝐑}_i^{-1/2}{𝗬}_j \qquad\qquad(4.13)
```

```math
\tilde{{𝐇}}_j({𝗫}_j, t_j) = {𝐑}_i^{-1/2}{𝐇}_j({𝗫}_j, t_j) \qquad\qquad(4.14)
```

```math
\tilde{{𝝂}}_j = {𝐑}_i^{-1/2}{𝝂}_j \qquad\qquad(4.15)
```

so that $`\mathrm{E}[\tilde{{𝝂}}_j\tilde{{𝝂}}_j] = {𝐈}`$. Thus, the new measurement equation has errors which are now decorrelated.

Alternatively, one can decompose the $`m \times m`$ measurement error covariance matrix with a UDU decomposition as $`{𝐑}_i = {𝐔}_{R_i}{𝐃}_{R_i}{𝐔}_{R_i}^{{𝖳}}`$ so that using a similar reasoning, we premultiply the measurement equation by $`{𝐔}_{R_i}^{-1}`$ so that in this case

```math
\tilde{{𝗬}}_j = {𝐔}_{R_i}^{-1}{𝗬}_j \qquad\qquad(4.16)
```

```math
\tilde{{𝐇}}_j({𝗫}_j, t_j) = {𝐔}_{R_i}^{-1}{𝐇}_j({𝗫}_j, t_j) \qquad\qquad(4.17)
```

```math
\tilde{{𝝂}}_j = {𝐔}_{R_i}^{-1}{𝝂}_j \qquad\qquad(4.18)
```

so that $`\mathrm{E}[\tilde{{𝝂}}_j\tilde{{𝝂}}_j] = {𝐃}_{R_i}`$ where $`{𝐃}_{R_i}`$ is a diagonal matrix and, as in the case of the Cholesky decomposition, the new measurement model has decorrelated measurement errors.

## <span id="page-61-3"></span><span id="page-61-0"></span>4.4. Filter Cascades

*Contributed by James McCabe*

It is often tempting to ingest the output of one navigation filter, an "upstream" filter, into another filter, a "downstream" filter. This is commonly proposed for systems equipped with sensors that furnish, in one sense or another, a post-processed data source, such as a Global Navigation Satellite System Position-Velocity-Time output, a derived measurement produced via an image processing algorithm such as seen in terrain relative navigation, or a pose solution from a lidar utilizing model matching. However, one of the few key, and often overlooked, assumptions critical to ensuring a Kalman filter's performance is that the measurement noise is white, i.e. uncorrelated in time. Many of these post-processed data sources employ online iterative procedures, many times themselves being Kalman filters, to produce the output. In this case, the measurement source has errors that are guaranteed to be time-correlated, and, if a practitioner is not careful, the system inherits a dangerous upstream filter/downstream filter relationship that can cause serious issues during runtime. If the downstream filter was provided or had *a priori* knowledge of the correlation this would not be an issue, but it is almost always impossible to directly quantify it. As such, the downstream Kalman filter is assuming a white noise signature, yet the input errors are time-correlated, and the resulting downstream estimates are flawed and, in practice, promote filter divergence (or, at minimum, a biased result). It is important to emphasize that, while this is often dismissed as a mere academic detail, cascades drastically increase overall navigation system risk.

This inadvertent relationship between assumed and real-world statistics is easy to accidentally happen into, especially considering that sensor vendors are manufacturing ever smarter and smarter sensors that employ "in the box" post-processing of their data to produce a convenient output for their customers. However, these outputs are often inconsistent with the Kalman filter's white noise assumption, even if the noise statistics provided on a specifications sheet are accurate. As such, a navigation practitioner is cautioned against presuming a post-processed output from any "navigation in a box" solution provided by a vendor can be naively ingested into a Kalman filter. Note that there are methods to aid in combating the negative effects of time-correlated measurement errors, often through the use of additional exponentially correlated random variable (ECRV) states in the filter to accommodate the bias-like effects of the time correlations, but the variances and time constants of these ECRVs become design variables that must be selected during tuning pre-flight, adding design complexity.

It is worth noting that there are cases where filter cascades have been utilized successfully despite their flaws, such as carrier-smoothing via pre-filtering of noisy high-rate data or direct ingestion of quaternion output from star tracker systems,[<sup>1</sup>](#page-61-2) but a navigator must be extremely careful in understanding the error signature in these signals to guarantee that the time history of the measurement errors are approximately white or appropriately treated within the filter formulation to account for time correlation. The success of these systems typically relies upon the upstream process producing a result that is, on the whole, fairly unbiased such that the signal appears to be corrupted by an approximately-white, zero-mean noise process.

<span id="page-61-2"></span><sup>1</sup> Note that some, but not all, quaternion outputs from such systems do not exhibit time-correlated errors, but this must be treated on a case-by-base basis.

## 4.5. Use of Data from Inertial Sensors

<span id="page-61-1"></span>Inertial measurement units (IMUs), consisting of gyros and accelerometers, sense rotational and translational accelerations. While in principle these high-rate data could be processed as observations in the navigation filter, it is often sufficient instead to use this data in *model replacement mode*, which Brown and Hwang [[7](16-bibliography.md#page-170-3)] compare to *complementary* filtering. In this approach, the sensed accelerations are fed forward as deterministic inputs to the navigation filter's dynamics model. Biases affecting the IMU data usually must be estimated by the filter. Thresholding the IMU accelerations is also usually necessary to avoid the introduction of unfiltered IMU noise into the filter state propagation. Chapter [7](07-state-representations.md#page-84-0) describes best practices for modeling the structures associated with IMU data.

---

[← Chapter 3. The Covariance Matrix (part 3 of 3)](03-the-covariance-matrix-part3.md) · [Contents](README.md) · [Chapter 5. Measurement Underweighting →](05-measurement-underweighting.md)
