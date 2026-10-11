[← Front Matter](00-front-matter.md) · [Contents](README.md) · [Chapter 2. Batch-Sequential Filters →](02-batch-sequential-filters.md)

# <span id="page-24-0"></span>Chapter 1. The Extended Kalman Filter

*Contributed by J. Russell Carpenter*

As described in the preface, use of the Extended Kalman Filter (EKF) for navigation has a long history of flight-proven success. The EKF thus forms the foundational best practice advocated by this work, and it forms the basis for many of the best practices later chapters describe. The purpose of the present chapter is not to derive the EKF and its relations, but rather to present them in a basic form, as a jumping off point for the rest of the material we shall present. As we shall show, while the EKF is a powerful and robust algorithm, it is based on a few *ad hoc* assumptions, which can lead to misuses and misunderstandings. Many of the best practices we shall describe are tricks of the trade that address such issues.

## 1.1. The Additive Extended Kalman Filter

<span id="page-24-1"></span>The *additive* EKF is distinguished from the *multiplicative* EKF (MEKF) by the form of its measurement update. The additive EKF is the usual and original form of the EKF, and when we refer to the EKF without a modifier, one may assume we mean the additive form.

### 1.1.1. The Dynamics Model

Suppose we have a list of $`n`$ real quantities that we need to know in order to perform navigation, and we have a differential equation that tells us how these quantities evolve through time, such as

<span id="page-24-2"></span>

```math
\dot{{𝑿}}(t) = {𝒇}({𝑿}(t), t) \qquad\qquad(1.1)
```

where $`{𝑿} \in {ℝ}^n`$, which we call the *state vector*, contains the quantities of interest; we shall call $`{𝒇}({𝑿}, t)`$ the *dynamics function*. If we knew these quantities perfectly at any time, [\(1.1\)](#page-24-2) would allow us to know them at any other time. For a variety of reasons, this is not the case however; both the initial conditions and the dynamics function are corrupted by uncertainty.

Suppose instead that the quantities of interest are realizations of a random process, $`{𝗫}(t)`$, whose distribution at some initial time $`t_o`$ is known to us, and whose evolution (forward) in time follows the stochastic differential equation given by

<span id="page-24-3"></span>

```math
\mathrm{d}{𝗫}(t) = {𝒇}({𝗫}(t), t)\,\mathrm{d}t + {𝐁}(t)\,\mathrm{d}{𝘄}(t) \qquad\qquad(1.2)
```

where the presence of the *process noise* $`\mathrm{d}{𝘄}(t)`$ reflects uncertainty in the dynamics. To interpret [\(1.2\)](#page-24-3), imagine $`\mathrm{d}{𝘄}(t)`$ as the limit of a discrete sequence of random increments, as the time between increments goes to zero. The result will be a continuous but non-differentiable process; hence the notation $`\dot{{𝗫}}(t)`$ has ambiguous meaning. Henceforth, we shall define our notation such that when we write

<span id="page-24-4"></span>

```math
\dot{{𝗫}}(t) = {𝒇}({𝗫}(t), t) + {𝐁}(t){𝘄}(t) \qquad\qquad(1.3)
```

what we mean is really [\(1.2\)](#page-24-3).

Finally, suppose that at some earliest time, $`t_o`$, the initial distribution of $`{𝗫}(t_o)`$ is Gaussian, with mean and covariance given by

```math
\mathrm{E}[{𝗫}(t_o)] = \bar{{𝑿}}_o \quad \text{and} \quad \mathrm{E}\big[({𝗫}(t_o) - \bar{{𝑿}}_o)({𝗫}(t_o) - \bar{{𝑿}}_o)^{{𝖳}}\big] = {𝐏}_o \qquad\qquad(1.4)
```

and suppose that infinitesimal increments of $`{𝘄}(t)`$ are Gaussian, with

<span id="page-25-4"></span>

```math
\mathrm{E}[{𝘄}(t)] = {𝟎} \quad \text{and} \quad \mathrm{E}[{𝘄}(t){𝘄}^{{𝖳}}(\tau)] = {𝐐}(t)\delta(t - \tau) \qquad\qquad(1.5)
```

where $`{𝐐}(t)`$ is the power spectral density function of $`{𝘄}(t)`$, and $`\delta(t - \tau)`$ is the Dirac delta, a generalized function. We shall also assume that

<span id="page-25-0"></span>

```math
\mathrm{E}\big[{𝘄}(t)({𝗫}(t_o) - \bar{{𝑿}}_o)^{{𝖳}}\big] = {𝟎},\ \forall\, t \qquad\qquad(1.6)
```

We shall take [\(1.3\)](#page-24-4) – [\(1.6\)](#page-25-0) to define the *dynamics model* for the additive EKF. Note that even though we have assumed $`{𝗫}(t_o)`$ and $`{𝘄}(t)`$ are Gaussian, we cannot assume that $`{𝗫}(t)`$ remains Gaussian for $`t \gt t_o`$, because $`{𝒇}`$ may be a nonlinear function.

### 1.1.2. The Measurement Model

In an ideal world, we might have devices for measuring all of the state vector components directly; then state determination would be simply a matter of collecting enough such observations to reduce the state uncertainty to sufficient levels. Unfortunately, this is almost never the case. Instead, like Socrates' prisoners, we can usually only perceive noisy projections of the state elements, at discrete times, $`t_i`$, in the form of *measurements*:

<span id="page-25-1"></span>

```math
{𝗬}(t_i) = {𝒉}({𝗫}(t_i), t_i) + {𝘃}(t_i) \qquad\qquad(1.7)
```

where $`{𝒉}`$ is a surjection from $`{ℝ}^n`$ to $`{ℝ}^m`$. We shall assume that $`{𝘃}(t_i)`$, which we call the *measurement noise*, is a Gaussian sequence, with mean and covariance given by

<span id="page-25-6"></span>

```math
\mathrm{E}[{𝘃}(t_i)] = {𝟎} \quad \text{and} \quad \mathrm{E}[{𝘃}(t_i){𝘃}(t_j)^{{𝖳}}] = {𝐑}(t_i)\delta_{ij} \qquad\qquad(1.8)
```

where $`\delta_{ij}`$ is the Kronecker delta function. We shall also assume that

<span id="page-25-2"></span>

```math
\mathrm{E}\big[{𝘃}(t_i)({𝗫}(t_o) - \bar{{𝑿}}_o)^{{𝖳}}\big] = {𝟎} \quad \text{and} \quad \mathrm{E}[{𝘄}(t){𝘃}(t_i)^{{𝖳}}] = {𝟎},\ \forall\, i, t \qquad\qquad(1.9)
```

We shall take [\(1.7\)](#page-25-1) – [\(1.9\)](#page-25-2) to define the *measurement model* for the additive EKF. Note that we cannot assume that $`{𝗬}(t_i)`$ is Gaussian, because $`{𝒉}`$ may be a nonlinear function. For compactness of notation, we shall often suppress the time argument and write [\(1.7\)](#page-25-1) as

<span id="page-25-5"></span>

```math
{𝗬}_i = {𝒉}_i({𝗫}_i) + {𝘃}_i \qquad\qquad(1.10)
```

### Bayes' Law, the Markov Property, and Observability

Bayes' Law tells us how to update the conditional probability density function (PDF) of $`{𝗫}(t_i)`$, given a realization $`{𝒀}(t_i)`$ of the random process $`{𝗬}(t_i)`$:

<span id="page-25-3"></span>

```math
\mathrm{p}_{{𝗫}_i|{𝗬}_i}({𝑿}_i|{𝒀}_i) = \mathrm{p}_{{𝗬}_i|{𝗫}_i}({𝒀}_i|{𝑿}_i)\,\frac{\mathrm{p}_{{𝗫}_i}({𝑿}_i)}{\mathrm{p}_{{𝗬}_i}({𝒀}_i)} \qquad\qquad(1.11)
```

If all the PDFs in [\(1.11\)](#page-25-3) were known, it would be relatively simple to use [\(1.11\)](#page-25-3) to estimate the state vector from a single measurement; our best estimate of the state would simply be the mean of $`\mathrm{p}_{{𝗫}_i|{𝗬}_i}({𝑿}_i|{𝒀}_i)`$. But to apply [\(1.11\)](#page-25-3) to the navigation problem, where we have a time sequence of measurements, $`{𝕐}_i = \{{𝒀}_i, {𝒀}_{i-1}, \ldots, {𝒀}_1\}`$, we need to consider how the state dynamics evolve.

Unlike [\(1.1\)](#page-24-2), our dynamics model, given by [\(1.3\)](#page-24-4), only runs forward in time. Hence, the state at any future time depends only on its history. Also, because the non-homogeneous inputs to [\(1.3\)](#page-24-4) are uncorrelated by the Dirac delta in [\(1.5\)](#page-25-4), the value of the state at any particular time in the future depends only on its present value, and its accumulated diffusion due to the process noise over the interval between now and the future time of interest. Random processes such as this are said to possess the *Markov Property*. Using this property, we can write [\(1.11\)](#page-25-3) in terms of the measurement history as follows:

<span id="page-26-0"></span>

```math
\mathrm{p}_{{𝗫}_i|{𝕐}_i}({𝑿}_i|{𝕐}_i) = \mathrm{p}_{{𝗬}_i|{𝗫}_i}({𝒀}_i|{𝑿}_i)\,\frac{\mathrm{p}_{{𝗫}_i|{𝕐}_{i-1}}({𝑿}_i|{𝕐}_{i-1})}{\mathrm{p}_{{𝗬}_i|{𝕐}_{i-1}}({𝒀}_i|{𝕐}_{i-1})} \qquad\qquad(1.12)
```

Even if we could compute all of the PDFs in [\(1.12\)](#page-26-0), we are not guaranteed that the sequence of measurements provide sufficient information to reduce the initial uncertainty of all the modes of [\(1.1\)](#page-24-2). If the system given by [\(1.1\)](#page-24-2) and [\(1.10\)](#page-25-5) is such that use of [\(1.12\)](#page-26-0) results in uncertainty in all the modes going asymptotically to zero in finite time, from any initial condition, then we say the system is *globally asymptotically observable*. If at least all of the unstable modes are observable, then we say the system is *detectable*. Unfortunately, for nonlinear systems, there is no known way to compute global observability. At best, under certain restrictions on [\(1.1\)](#page-24-2) and [\(1.10\)](#page-25-5), we can in principle establish local observability, in the neighborhood of a particular initial condition. However, this is a laborious calculation, often numerically unstable to evaluate. Also, note that observability is a property of the structure of [\(1.1\)](#page-24-2) and [\(1.10\)](#page-25-5), and hence is dependent on how one chooses to represent the navigation problem. Hence, a system that is observable with one representation may be unobservable with a different representation.

Kalman's original filter, which we now usually call the *linear Kalman filter* (LKF), is the result when the dynamics and measurement models are linear, Markov, Gaussian, and observable. An appreciation of the linear Kalman filter is essential to understanding the strengths and weaknesses of the EKF, although it is almost never the case that such assumptions are valid for real-world navigation problems.

### 1.1.3. The Linear Kalman Filter

Suppose the dynamics and measurements are given by the following discrete-time linear models:

<span id="page-26-2"></span>

```math
{𝘅}_i = {𝚽}_{i,i-1}{𝘅}_{i-1} + {𝚪}_i{𝘂}_i \qquad\qquad(1.13)
```

<span id="page-26-3"></span>

```math
{𝘆}_i = {𝐇}_i{𝘅}_i + {𝘃}_i \qquad\qquad(1.14)
```

with

```math
\mathrm{E}[{𝘅}_o] = \bar{{𝒙}}_o \quad \text{and} \quad \mathrm{E}[({𝘅}_o - \bar{{𝒙}}_o)({𝘅}_o - \bar{{𝒙}}_o)]^{{𝖳}}] = {𝐏}_o \qquad\qquad(1.15)
```

```math
\mathrm{E}[{𝘂}_i] = {𝟎} \quad \text{and} \quad \mathrm{E}\big[{𝚪}_i{𝘂}_i{𝘂}_j^{{𝖳}}{𝚪}_i^{{𝖳}}\big] = {𝐒}_i\delta_{ij} \qquad\qquad(1.16)
```

and the moments of $`{𝘃}_i`$ as given by [\(1.8\)](#page-25-6). This system will be globally observable if the *observability Gramian* is strictly positive definite,

<span id="page-26-1"></span>

```math
{𝐖}_k = \sum_{i=1}^{k} {𝚽}_{i,1}^{{𝖳}}{𝐇}_i^{{𝖳}}{𝐇}_i{𝚽}_{i,1} \gt 0 \qquad\qquad(1.17)
```

i.e. it has full rank.

With such assumptions, Kalman showed [[44](16-bibliography.md#page-171-1)] that Algorithm [1.1](#page-27-0) provides an optimal (both minimum variance and maximum likelihood) estimate of the moments of the PDFs appearing in [\(1.11\)](#page-25-3). Note that in Algorithm [1.1,](#page-27-0) the covariance recursion given by [\(1.19\)](#page-27-1) and [\(1.22\)](#page-27-2) does not depend on the measurement history, and hence one may compute the gain sequence, $`{𝐊}_i`$, off-line and store it as a time-indexed table or *schedule*, along with $`{𝚽}_{i,i-1}`$ and $`{𝐇}_i`$. Also note that because the system is globally observable, there is no chance that it will fail to converge from any initial condition, except perhaps due to build up of numerical truncation and/or roundoff error.

If we further suppose the dynamics and measurements are given by linear time-invariant (LTI) models,

```math
{𝘅}_i = {𝚽}{𝘅}_{i-1} + {𝚪}{𝘂}_i \qquad\qquad(1.23)
```

```math
{𝘆}_i = {𝐇}{𝘅}_i + {𝘃}_i \qquad\qquad(1.24)
```

then we may test its global observability using a somewhat simpler calculation than [\(1.17\)](#page-26-1), as follows:

```math
{𝐖} = \begin{bmatrix} {𝐇} \\ {𝐇}{𝚽} \\ {𝐇}{𝚽}^2 \\ \vdots \\ {𝐇}{𝚽}^{n-1} \end{bmatrix} \gt 0 \qquad\qquad(1.25)
```

If the system is detectable, then it turns out that the covariance recursion given by [\(1.19\)](#page-27-1) and [\(1.22\)](#page-27-2) reaches a steady-state, which we denote $`{𝐏}_\infty`$. The corresponding gain is $`{𝐊}_\infty = {𝐏}_\infty{𝐇}^{{𝖳}}{𝐑}^{-1}`$. There exist numerous software packages that will compute such quantities, e.g. the *Matlab Control Systems Toolbox*, which may unfortunately lead to their misuse in inappropriate contexts. Perhaps worse, experts from other domains, who are familiar with techniques such as pole placement for control of LTI systems, may recognize that the steady-state linear Kalman filter is "just a pole placement algorithm," and may infer that the EKF is not much more than a clever pole placement algorithm as well. As we shall show below, this is far from being the case; the EKF operates directly on the nonlinear system of interest, for which such LTI concepts have dubious applicability.

> <span id="page-27-0"></span>**Algorithm 1.1** The Linear Kalman Filter
>
> <span id="page-27-3"></span>
>
> ```math
> \hat{{𝒙}}_i^- = {𝚽}_{i,i-1}\hat{{𝒙}}_{i-1}^+, \quad \hat{{𝒙}}_0^+ = \bar{{𝒙}}_o \qquad\qquad(1.18)
> ```
>
> <span id="page-27-1"></span>
>
> ```math
> {𝐏}_i^- = {𝚽}_{i,i-1}{𝐏}_{i-1}^+{𝚽}_{i,i-1}^{{𝖳}} + {𝐒}_i, \quad {𝐏}_0^+ = {𝐏}_o \qquad\qquad(1.19)
> ```
>
> ```math
> {𝐊}_i = {𝐏}_i^-{𝐇}_i^{{𝖳}}\Bigl({𝐇}_i{𝐏}_i^-{𝐇}_i^{{𝖳}} + {𝐑}_i\Bigr)^{-1} \qquad\qquad(1.20)
> ```
>
> ```math
> \hat{{𝒙}}_i^+ = \hat{{𝒙}}_i^- + {𝐊}_i\Bigl({𝒚}_i - {𝐇}_i\hat{{𝒙}}_i^-\Bigr) \qquad\qquad(1.21)
> ```
>
> <span id="page-27-2"></span>
>
> ```math
> {𝐏}_i^+ = {𝐏}_i^- - {𝐊}_i{𝐇}_i{𝐏}_i^- \qquad\qquad(1.22)
> ```

### 1.1.4. The Linearized Kalman Filter

An immediately apparent generalization of the linear Kalman Filter is to use it to solve for small corrections to a nonlinearly propagated *fixed* reference trajectory. While such an approach may have certain applications over limited time horizons, and/or for ground-based applications where an operator can periodically intervene, experience with onboard navigation systems has shown that such corrections can fail to remain small enough to justify the required approximations.

### 1.1.5. The Extended Kalman Filter

There are a number of ways to proceed from Algorithm [1.1](#page-27-0) to "derive" the EKF, but all contain a variety of *ad hoc* assumptions that are not guaranteed to hold in all circumstances. Most weaknesses and criticisms of the EKF arise from such assumptions. Rather than reproduce one or more of such derivations, we will simply point out that if one replaces [\(1.18\)](#page-27-3) with an integral of [\(1.1\)](#page-24-2) over the time between measurements, and computes the coefficient matrices appearing in [\(1.13\)](#page-26-2) and [\(1.14\)](#page-26-3) as Jacobians evaluated at the current solution of [\(1.1\)](#page-24-2), then the result is Algorithm [1.2,](#page-28-0) which bears more than a passing resemblance to the Kalman filter.

Several observations are in order regarding Algorithm [1.2.](#page-28-0)

> <span id="page-28-0"></span>**Algorithm 1.2** A Naive Extension of the Kalman Filter
>
> <span id="page-28-1"></span>
>
> ```math
> \hat{{𝑿}}_i^- = \hat{{𝑿}}_{i-1}^+ + \int_{t_{i-1}}^{t_i} {𝒇}({𝑿}(\tau), \tau)\,\mathrm{d}\tau, \quad \hat{{𝑿}}_0^+ = \bar{{𝑿}}_o \qquad\qquad(1.26)
> ```
>
> ```math
> {𝐀}(t) = \left.\frac{\partial {𝒇}}{\partial {𝑿}}\right|_{\hat{{𝑿}}(t)}, \quad {𝐇}_i = \left.\frac{\partial {𝒉}_i}{\partial {𝑿}}\right|_{\hat{{𝑿}}_i^-} \qquad\qquad(1.27)
> ```
>
> <span id="page-28-6"></span>
>
> ```math
> {𝚽}(t_i, t_{i-1}) = {𝐈} + \int_{t_{i-1}}^{t_i} {𝐀}(\tau){𝚽}(t_i, \tau)\,\mathrm{d}\tau \qquad\qquad(1.28)
> ```
>
> <span id="page-28-5"></span>
>
> ```math
> {𝐒}_i = \int_{t_{i-1}}^{t_i}\int_{t_{i-1}}^{t_i} {𝚽}(t_i, \tau){𝐁}(\tau)\,\mathrm{E}[{𝘄}(\tau){𝘄}^{{𝖳}}(\sigma)]\,{𝐁}^{{𝖳}}(\sigma){𝚽}^{{𝖳}}(t_i, \sigma)\,\mathrm{d}\tau\,\mathrm{d}\sigma \qquad\qquad(1.29)
> ```
>
> <span id="page-28-7"></span>
>
> ```math
> {𝐏}_i^- = {𝚽}(t_i, t_{i-1}){𝐏}_{i-1}^+{𝚽}^{{𝖳}}(t_i, t_{i-1}) + {𝐒}_i, \quad {𝐏}_0^+ = {𝐏}_o \qquad\qquad(1.30)
> ```
>
> <span id="page-28-4"></span>
>
> ```math
> {𝐊}_i = {𝐏}_i^-{𝐇}_i^{{𝖳}}\Bigl({𝐇}_i{𝐏}_i^-{𝐇}_i^{{𝖳}} + {𝐑}_i\Bigr)^{-1} \qquad\qquad(1.31)
> ```
>
> <span id="page-28-2"></span>
>
> ```math
> \hat{{𝑿}}_i^+ = \hat{{𝑿}}_i^- + {𝐊}_i\Big({𝒀}_i - {𝒉}_i(\hat{{𝑿}}_i^-)\Big) \qquad\qquad(1.32)
> ```
>
> <span id="page-28-3"></span>
>
> ```math
> {𝐏}_i^+ = {𝐏}_i^- - {𝐊}_i{𝐇}_i{𝐏}_i^- \qquad\qquad(1.33)
> ```

- One might infer from [\(1.26\)](#page-28-1) that $`\hat{{𝑿}}_i^- = \mathrm{E}[{𝗫}|{𝕐}_{i-1}]`$. This would be a somewhat problematic inference however, since in general

```math
\int_{t_{i-1}}^{t_i} {𝒇}(\mathrm{E}[{𝑿}(\tau)], \tau)\,\mathrm{d}\tau \neq \mathrm{E}\biggl[\int_{t_{i-1}}^{t_i} {𝒇}({𝑿}(\tau), \tau)\,\mathrm{d}\tau\biggr] \qquad\qquad(1.34)
```

  This implies that an initially Gaussian distribution for the state cannot in general remain Gaussian. At best, all we can hope is that $`\hat{{𝑿}}_i^- \approx \mathrm{E}[{𝗫}|{𝕐}_{i-1}]`$.

- Let us define the *estimation error* as $`{𝗲}(t) = {𝗫}(t) - \hat{{𝑿}}(t)`$. Then since $`\hat{{𝑿}}(t) \neq \mathrm{E}[{𝗫}(t)|{𝕐}_{i-1}]`$,

```math
{𝐏}(t) \neq \mathrm{E}[{𝗲}(t){𝗲}^{{𝖳}}(t)|{𝕐}_{i-1}] \qquad\qquad(1.35)
```

  At best, all we can hope is that $`{𝐏}(t) \approx \mathrm{E}[{𝗲}(t){𝗲}^{{𝖳}}(t)|{𝕐}_{i-1}]`$.

- Let us define the *innovation* as $`{𝗿}_i = {𝗬}_i - {𝐡}(\hat{{𝑿}}_i^-)`$. Then since $`{𝐡}(\hat{{𝑿}}_i^-) \neq \mathrm{E}[{𝗬}]`$,

```math
{𝐇}_i{𝐏}_i^-{𝐇}_i^{{𝖳}} + {𝐑}_i \neq \mathrm{E}[{𝗿}_i{𝗿}_i^{{𝖳}}] \qquad\qquad(1.36)
```

  At best, all we can hope is that the above will hold approximately.

- Taken together, the approximations listed above imply that [\(1.32\)](#page-28-2) and [\(1.33\)](#page-28-3) can at best satisfy [\(1.12\)](#page-26-0) only approximately, not only because the mean and covariance are approximations, but also because the PDFs fail to remain Gaussian, and hence fail to be characterized completely by only their first two moments.

- Even if all of the above are reasonable approximations, there is a problem with [\(1.33\)](#page-28-3). The *posterior covariance* should be approximated by

```math
{𝐏}_i^+ \approx \mathrm{E}\big[{𝗲}_i^+({𝗲}_i^+)^{{𝖳}}|{𝕐}_i\big] \qquad\qquad(1.37)
```

  Let us assume that

```math
{𝗬}_i - {𝒉}_i(\hat{{𝑿}}_i^-) \approx {𝐇}_i{𝗲}_i^- + {𝘃}_i \qquad\qquad(1.38)
```

  Then [\(1.32\)](#page-28-2) implies that

```math
{𝗲}_i^+ = {𝗲}_i^- - {𝐊}_i{𝐇}_i{𝗲}_i^- - {𝐊}_i{𝘃}_i \qquad\qquad(1.39)
```

  and by our prior assumption that $`\mathrm{E}\big[{𝗲}_i^-{𝘃}_i^{{𝖳}}\big] = {𝟎}`$,

```math
{𝐏}_i^+ \approx \mathrm{E}\big[{𝗲}_i^+({𝗲}_i^+)^{{𝖳}}|{𝕐}_i\big] \qquad\qquad(1.40)
```

  <span id="page-29-1"></span>

```math
= ({𝐈} - {𝐊}_i{𝐇}_i)\,{𝐏}_i^-\,({𝐈} - {𝐊}_i{𝐇}_i)^{{𝖳}} + {𝐊}_i{𝐑}_i{𝐊}_i^{{𝖳}} \qquad\qquad(1.41)
```

  Equation [\(1.41\)](#page-29-1) is *Joseph's Formula*, and it holds for any gain $`{𝐊}_i`$. Only for the optimal gain and true covariance does [\(1.41\)](#page-29-1) reduce to [\(1.33\)](#page-28-3). Since [\(1.31\)](#page-28-4) was computed with only an approximate covariance, and due to the various other approximations listed above as well, $`{𝐊}_i`$ cannot be the optimal gain, so at best, [\(1.33\)](#page-28-3) will only hold approximately. At worst, such approximations may lead to $`{𝐏}_i^+`$ becoming non-positive definite, which is a significant issue. Because of its symmetric and additive form, [\(1.41\)](#page-29-1) is much less likely (but not impossible!) to produce a non-positive definite $`{𝐏}_i^+`$.

- By our assumption that $`\mathrm{E}[{𝘄}(t){𝘄}^{{𝖳}}(\tau)] = {𝐐}(t)\delta(t-\tau)`$, one of the integrals in [\(1.29\)](#page-28-5) should be annihilated by the Dirac delta, resulting in

  <span id="page-29-2"></span>

```math
{𝐒}_i = \int_{t_{i-1}}^{t_i} {𝚽}(t_i, \tau){𝐁}(\tau){𝐐}(\tau){𝐁}^{{𝖳}}(\tau){𝚽}^{{𝖳}}(t_i, \tau)\,\mathrm{d}\tau \qquad\qquad(1.42)
```

  In any case, unlike for a discrete time dynamics model,

```math
\begin{aligned} &\mathrm{E}\biggl[\int_{t_{i-1}}^{t_i}\int_{t_{i-1}}^{t_i} {𝚽}(t_i, \tau){𝐁}(\tau){𝘄}(\tau){𝘄}^{{𝖳}}(\sigma){𝐁}^{{𝖳}}(\sigma){𝚽}^{{𝖳}}(t_i, \sigma)\,\mathrm{d}\tau\,\mathrm{d}\sigma\biggr] \\ &\qquad \neq \mathrm{E}\biggl[\int_{t_{i-1}}^{t_i} {𝚽}(t_i, \tau){𝐁}(\tau){𝘄}(\tau)\,\mathrm{d}\tau \int_{t_{i-1}}^{t_i} {𝘄}^{{𝖳}}(\tau){𝐁}^{{𝖳}}(\tau){𝚽}^{{𝖳}}(t_i, \tau)\,\mathrm{d}\tau\biggr] \end{aligned} \qquad\qquad(1.43)
```

- In general, one would need to simultaneously integrate [\(1.26\)](#page-28-1) and [\(1.28\)](#page-28-6) due to their interdependence via the Jacobian $`{𝐀}`$. If the time between measurements is small enough, then if one were to employ a suitable approximation for [\(1.28\)](#page-28-6), perhaps as simple as

```math
{𝚽}(t_i, t_{i-1}) \approx {𝐈} + {𝐀}(t_i)\,(t_i - t_{i-1}) \qquad\qquad(1.44)
```

  then one may reasonably expect that a carefully chosen approximation would be no worse than the many other approximations inherent in the EKF. One may also consider the same or simpler approximations when considering approximations to [\(1.42\)](#page-29-2).

- Because there is no way to prove global observability for a nonlinear system, the EKF may fail to converge from some initial conditions, even if the system is locally observable in particular neighborhoods.

In light of the above observations, we conclude this section by presenting a slightly improved version of the EKF as Algorithm [1.3.](#page-30-0) In subsequent chapters, we shall describe additional improvements to the EKF.

## 1.2. The Multiplicative Extended Kalman Filter

<span id="page-29-0"></span>An interesting variation on the EKF is possible in the context of estimating attitude parameters. An attitude correction may be viewed as a small-angle rotation from a frame associated with the previous estimate to a frame associated with a current estimate. In this context, one may use the previous attitude estimate as a linearization reference for a linearized Kalman Filter's Jacobian matrices, and estimate the small-angle correction as the filter state. After each state update, one performs a rectification of the attitude reference by applying the small-angle correction. Since for many attitude representations, a frame rotation is multiplicative operation, this procedure has become known as the multiplicative EKF. Chapter [9](09-attitude-estimation-part1.md#page-108-0) covers this subject.

> <span id="page-30-0"></span>**Algorithm 1.3** A Slightly Improved Extension of the Kalman Filter
>
> <span id="page-30-1"></span>
>
> ```math
> \hat{{𝑿}}_i^- = \hat{{𝑿}}_{i-1}^+ + \int_{t_{i-1}}^{t_i} {𝒇}({𝑿}(\tau), \tau)\,\mathrm{d}\tau, \quad \hat{{𝑿}}_0^+ = \bar{{𝑿}}_o \qquad\qquad(1.45)
> ```
>
> ```math
> {𝐀}(t) = \left.\frac{\partial {𝒇}}{\partial {𝑿}}\right|_{\hat{{𝑿}}(t)}, \quad {𝐇}_i = \left.\frac{\partial {𝒉}_i}{\partial {𝑿}}\right|_{\hat{{𝑿}}_i^-} \qquad\qquad(1.46)
> ```
>
> ```math
> {𝚽}(t_i, t_{i-1}) = \text{a suitable approximation to (1.28)} \qquad\qquad(1.47)
> ```
>
> ```math
> {𝐒}_i = \text{a suitable approximation to (1.42)} \qquad\qquad(1.48)
> ```
>
> <span id="page-30-2"></span>
>
> ```math
> {𝐏}_i^- = {𝚽}(t_i, t_{i-1}){𝐏}_{i-1}^+{𝚽}^{{𝖳}}(t_i, t_{i-1}) + {𝐒}_i, \quad {𝐏}_0^+ = {𝐏}_o \qquad\qquad(1.49)
> ```
>
> ```math
> {𝐊}_i = {𝐏}_i^-{𝐇}_i^{{𝖳}}\Bigl({𝐇}_i{𝐏}_i^-{𝐇}_i^{{𝖳}} + {𝐑}_i\Bigr)^{-1} \qquad\qquad(1.50)
> ```
>
> ```math
> \hat{{𝑿}}_i^+ = \hat{{𝑿}}_i^- + {𝐊}_i\Big({𝒀}_i - {𝒉}_i(\hat{{𝑿}}_i^-)\Big) \qquad\qquad(1.51)
> ```
>
> ```math
> {𝐏}_i^+ = ({𝐈} - {𝐊}_i{𝐇}_i)\,{𝐏}_i^-\,({𝐈} - {𝐊}_i{𝐇}_i)^{{𝖳}} + {𝐊}_i{𝐑}_i{𝐊}_i^{{𝖳}} \qquad\qquad(1.52)
> ```

---

[← Front Matter](00-front-matter.md) · [Contents](README.md) · [Chapter 2. Batch-Sequential Filters →](02-batch-sequential-filters.md)
