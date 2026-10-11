[← Chapter 10. Usability Considerations](10-usability-considerations.md) · [Contents](README.md) · [Chapter 12. Advanced Estimation Algorithms →](12-advanced-estimation-algorithms.md)

# Chapter 11. Smoothing

<span id="page-136-0"></span>*Contributed by Christopher N. D'Souza and J. Russell Carpenter*

Since this work is primarily concerned with onboard navigation filters, one might question the need for a chapter on best practices for smoothing. While the addition of a smoother to an onboard navigation system has usually proved unnecessary, smoothing has nonetheless proved to be a useful ancillary capability for trajectory reconstruction by ground-based analysts. Smoothed trajectories form the basis for our best proxies for truth, in the form of "best estimated trajectories," (BET) and McReynold's "filter-smoother consistency test," propagated by Jim Wright [[90](16-bibliography.md#page-173-17)], has proven to be a useful aid to tuning a filter using flight data. Also, sequential smoothing techniques can provide optimal estimates of the process noise sequence, as Appendix X of Bierman's text [[5](16-bibliography.md#page-170-1)] shows. These estimates may prove useful as part of the filter tuning process.

It is also worth mentioning the topic of "smoothability." As described in for example Gelb [[27](16-bibliography.md#page-171-5)], only states that are controllable from the process noise will be affected by smoothing. So for example, estimates of random constant measurement biases cannot be improved by smoothing.

In point of fact there are three types of smoothing: fixed-interval smoothing, fixed-lag smoothing, and fixed-point smoothing. The context described above is concerned with fixed-interval smoothing. Maximum likelihood estimation (MLE) of states over a fixed interval has been subject of investigation ever since the advent of the Kalman filter [[44](16-bibliography.md#page-171-1)] in 1961. In 1962, Bryson and Frazier first approached the problem from a continuous time perspective [[8](16-bibliography.md#page-170-20)] and obtained the smoother equations as necessary conditions of an optimal control problem[†](#page-136-1). In 1965, Rauch, Tung and Striebel [[70](16-bibliography.md#page-172-19)] (RTS) continued the development of the MLE filters but from a discrete time perspective. Their smoother, soon called the RTS smoother, was widely used because of its ease of implementation. However, as Bierman [[5](16-bibliography.md#page-170-1)] and others [[61](16-bibliography.md#page-172-20)] pointed out, there can sometimes arise numerical difficulties in implementing the RTS smoother. A short time later Fraser and Potter [[24](16-bibliography.md#page-171-23), [25](16-bibliography.md#page-171-24)] approached the problem a bit differently, looking at smoothing as a optimal combination of two optimal linear filters and obtained different, yet equivalent, equations. Bierman's Square-Root Information Filter [[5](16-bibliography.md#page-170-1)] (SRIF) also has an accompanying smoother form, suitable for applications utilizing the SRIF. Since the Fraser-Potter form avoids the numerical issues of the RTS form, and since it can be easily adapted from existing onboard Kalman-type forward filtering algorithms, it is generally to be preferred.

<span id="page-136-1"></span><sup>†</sup> The Bryson-Frazier smoother is a continuous time instantiation of the smoother. It won't be considered here for we are interested in discrete smoothers. [[8](16-bibliography.md#page-170-20)]

The boundary conditions for the Fraser-Potter (FP) smoother require the backward covariance at the final time to be infinite, and the backward filter's final state to be zero. Fraser and Potter avoided the infinity by maintaining the backward filter covariance in information form, so that both the information matrix and the information vector are zero. As Brown points out [[7](16-bibliography.md#page-170-3)], the backward filter may be retained in covariance form, and the infinite boundary condition covariance replaced by either a covariance that is many multiples of the forward filter's initial covariance, or by the covariance and state from a short batch least-squares solution using the final few measurements. Many practical smoother implementations used by NASA have followed an approach of this sort.

Thus, a practical covariance form of the FP smoother results from running whatever implementation of Algorithm [1.3](01-the-extended-kalman-filter.md#page-30-0) has proved suitable for the application at hand, but in reverse time, and combining the backward filter results with the forward filter results at each measurement time. Given the forward filter state and covariance, $`\hat{{𝑿}}^{+}_{F_i}`$ and $`{𝐏}^{+}_{F_i}`$, which include the measurement at $`t_i`$, and the backward filter state and covariance, $`\hat{{𝑿}}^{-}_{B_i}`$ and $`{𝐏}^{-}_{B_i}`$, which *do not* include the measurement at $`t_i`$, the optimally smoothed state and covariance at $`t_i`$ are given by

<span id="page-137-0"></span>
```math
\hat{{𝑿}}^{S}_{i} = {𝐏}^{S}_{i} \Bigl[ ({𝐏}^{+}_{F_i})^{-1} \hat{{𝑿}}^{+}_{F_i} + ({𝐏}^{-}_{B_i})^{-1} \hat{{𝑿}}^{-}_{B_i} \Bigr] \qquad\qquad(11.1)
```

<span id="page-137-1"></span>
```math
{𝐏}^{S}_{i} = \Bigl[ ({𝐏}^{+}_{F_i})^{-1} + ({𝐏}^{-}_{B_i})^{-1} \Bigr]^{-1} \qquad\qquad(11.2)
```

If covariance form is to be retained, the tedious number of inverses apparent in Eqs. [\(11.1\)](#page-137-0) and [\(11.2\)](#page-137-1) may be avoided as follows. Suppose we define the smoothed state as a linear fusion of the forward and backward filter states:

```math
\hat{{𝑿}}^{S}_{i} = {𝐖}_{F_i} \hat{{𝑿}}^{+}_{F_i} + {𝐖}_{B_i} \hat{{𝑿}}^{-}_{B_i} \qquad\qquad(11.3)
```

For $`\hat{{𝑿}}^{S}_{i}`$ to be unbiased, we must choose either $`{𝐖}_{F_i} = {𝐈} - {𝐖}_{B_i}`$ or $`{𝐖}_{B_i} = {𝐈} - {𝐖}_{F_i}`$. Choosing the latter, the smoothed state becomes

<span id="page-137-4"></span>
```math
\hat{{𝑿}}^{S}_{i} = {𝐖}_{F_i} \hat{{𝑿}}^{+}_{F_i} + ({𝐈} - {𝐖}_{F_i})\, \hat{{𝑿}}^{-}_{B_i} \qquad\qquad(11.4)
```

Given the enforced lack of correlation between the forward and backward filters, the fused (smoothed) covariance is given by

```math
{𝐏}^{S}_{i} = {𝐖}_{F_i} {𝐏}^{+}_{F_i} {𝐖}^{{𝖳}}_{F_i} + {𝐖}_{B_i} {𝐏}^{-}_{B_i} {𝐏}^{-}_{B_i} {𝐖}^{{𝖳}}_{B_i} \qquad\qquad(11.5)
```

<span id="page-137-2"></span>
```math
= {𝐖}_{F_i} {𝐏}^{+}_{F_i} {𝐖}^{{𝖳}}_{F_i} + ({𝐈} - {𝐖}_{F_i})\, {𝐏}^{-}_{B_i}\, ({𝐈} - {𝐖}_{F_i})^{{𝖳}} \qquad\qquad(11.6)
```

Choosing $`{𝐖}_{F_i}`$ to minimize the trace of $`{𝐏}^{S}_{i}`$ results in

<span id="page-137-3"></span>
```math
{𝐖}_{F_i} = {𝐏}^{-}_{B_i} ({𝐏}^{+}_{F_i} + {𝐏}^{-}_{B_i})^{-1} \qquad\qquad(11.7)
```

To see that Eq. [\(11.6\)](#page-137-2), with Eq. [\(11.7\)](#page-137-3), is equal to Eq. [\(11.2\)](#page-137-1), expand Eq. [\(11.6\)](#page-137-2), substituting Eq. [\(11.7\)](#page-137-3), and recall Woodbury's identity:

<span id="page-137-5"></span>
```math
\Bigl[ ({𝐏}^{+}_{F_i})^{-1} + ({𝐏}^{-}_{B_i})^{-1} \Bigr]^{-1} = {𝐏}^{-}_{B_i} - {𝐏}^{-}_{B_i} ({𝐏}^{+}_{F_i} + {𝐏}^{-}_{B_i})^{-1} {𝐏}^{-}_{B_i} \qquad\qquad(11.8)
```

<span id="page-137-6"></span>
```math
= {𝐏}^{+}_{F_i} - {𝐏}^{+}_{F_i} ({𝐏}^{+}_{F_i} + {𝐏}^{-}_{B_i})^{-1} {𝐏}^{+}_{F_i} \qquad\qquad(11.9)
```

To see that Eq. [\(11.4\)](#page-137-4), with Eq. [\(11.7\)](#page-137-3), is equal to Eq. [\(11.1\)](#page-137-0), use Eq. [\(11.8\)](#page-137-5) to show that $`{𝐏}^{S}_{i} ({𝐏}^{-}_{B_i})^{-1} = {𝐖}_{B_i}`$ and use Eq. [\(11.9\)](#page-137-6) to show that $`{𝐏}^{S}_{i} ({𝐏}^{+}_{F_i})^{-1} = {𝐖}_{F_i}`$.

In a typical application, the forward filter has been running continuously onboard the vehicle, and ground-based analysts will periodically wish to generate a BET over a particular span of recently downlinked data. If the telemetry system has recorded and downlinked the full state and covariance at each measurement time, along with the measurements, the ground system need only run a "copy" of the forward filter backwards through the measurements and fuse the data according to Eqs. [\(11.1\)](#page-137-0) and [\(11.2\)](#page-137-1). Care must be taken that regeneration of the state transition matrices and process noise covariances is consistent with the forward filter's modeling, and with the negative flow of time.

For various reasons, it may be necessary or desirable to run the forward filter on the ground as well, e.g. with higher-fidelity modeling than the onboard implementation permits. If so, it is efficient to store the state transition matrices and process noise covariances computed in the forward pass for use in the backward filter. In this case, Brown shows that the backward covariance may be propagated using

```math
{𝐏}^{-}_{B_i} = {𝚽}^{-1}_{i+1,i} \Bigl[ {𝐏}^{+}_{B_{i+1}} + {𝐒}_{i+1} \Bigr] {𝚽}^{-{𝖳}}_{i+1,i} \qquad\qquad(11.10)
```

---

[← Chapter 10. Usability Considerations](10-usability-considerations.md) · [Contents](README.md) · [Chapter 12. Advanced Estimation Algorithms →](12-advanced-estimation-algorithms.md)
