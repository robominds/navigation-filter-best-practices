[← Front Matter](00-front-matter.md) · [Contents](README.md) · [Chapter 2. Batch-Sequential Filters →](02-batch-sequential-filters.md)

# <span id="page-24-0"></span>Chapter 1. The Extended Kalman Filter

*Contributed by J. Russell Carpenter*

As described in the preface, use of the Extended Kalman Filter (EKF) for navigation has a long history of flight-proven success. The EKF thus forms the foundational best practice advocated by this work, and it forms the basis for many of the best practices later chapters describe. The purpose of the present chapter is not to derive the EKF and its relations, but rather to present them in a basic form, as a jumping off point for the rest of the material we shall present. As we shall show, while the EKF is a powerful and robust algorithm, it is based on a few *ad hoc* assumptions, which can lead to misuses and misunderstandings. Many of the best practices we shall describe are tricks of the trade that address such issues.

## 1.1. The Additive Extended Kalman Filter

<span id="page-24-1"></span>The *additive* EKF is distinguished from the *multiplicative* EKF (MEKF) by the form of its measurement update. The additive EKF is the usual and original form of the EKF, and when we refer to the EKF without a modifier, one may assume we mean the additive form.

### 1.1.1. The Dynamics Model

Suppose we have a list of $n$ real quantities that we need to know in order to perform navigation, and we have a differential equation that tells us how these quantities evolve through time, such as

<span id="page-24-2"></span>

$$
\dot{\boldsymbol{X}}(t) = \boldsymbol{f}(\boldsymbol{X}(t), t) \tag{1.1}
$$

where $\boldsymbol{X} \in \mathbb{R}^n$, which we call the *state vector*, contains the quantities of interest; we shall call $\boldsymbol{f}(\boldsymbol{X}, t)$ the *dynamics function*. If we knew these quantities perfectly at any time, [\(1.1\)](#page-24-2) would allow us to know them at any other time. For a variety of reasons, this is not the case however; both the initial conditions and the dynamics function are corrupted by uncertainty.

Suppose instead that the quantities of interest are realizations of a random process, $\boldsymbol{\mathsf{X}}(t)$, whose distribution at some initial time $t_o$ is known to us, and whose evolution (forward) in time follows the stochastic differential equation given by

<span id="page-24-3"></span>

$$
\mathrm{d}\boldsymbol{\mathsf{X}}(t) = \boldsymbol{f}(\boldsymbol{\mathsf{X}}(t), t)\,\mathrm{d}t + \mathbf{B}(t)\,\mathrm{d}\boldsymbol{\mathsf{w}}(t) \tag{1.2}
$$

where the presence of the *process noise* $\mathrm{d}\boldsymbol{\mathsf{w}}(t)$ reflects uncertainty in the dynamics. To interpret [\(1.2\)](#page-24-3), imagine $\mathrm{d}\boldsymbol{\mathsf{w}}(t)$ as the limit of a discrete sequence of random increments, as the time between increments goes to zero. The result will be a continuous but non-differentiable process; hence the notation $\dot{\boldsymbol{\mathsf{X}}}(t)$ has ambiguous meaning. Henceforth, we shall define our notation such that when we write

<span id="page-24-4"></span>

$$
\dot{\boldsymbol{\mathsf{X}}}(t) = \boldsymbol{f}(\boldsymbol{\mathsf{X}}(t), t) + \mathbf{B}(t)\boldsymbol{\mathsf{w}}(t) \tag{1.3}
$$

what we mean is really [\(1.2\)](#page-24-3).

Finally, suppose that at some earliest time, $t_o$, the initial distribution of $\boldsymbol{\mathsf{X}}(t_o)$ is Gaussian, with mean and covariance given by

$$
\mathrm{E}[\boldsymbol{\mathsf{X}}(t_o)] = \bar{\boldsymbol{X}}_o \quad \text{and} \quad \mathrm{E}\big[(\boldsymbol{\mathsf{X}}(t_o) - \bar{\boldsymbol{X}}_o)(\boldsymbol{\mathsf{X}}(t_o) - \bar{\boldsymbol{X}}_o)^{\mathsf{T}}\big] = \mathbf{P}_o \tag{1.4}
$$

and suppose that infinitesimal increments of $\boldsymbol{\mathsf{w}}(t)$ are Gaussian, with

<span id="page-25-4"></span>

$$
\mathrm{E}[\boldsymbol{\mathsf{w}}(t)] = \mathbf{0} \quad \text{and} \quad \mathrm{E}[\boldsymbol{\mathsf{w}}(t)\boldsymbol{\mathsf{w}}^{\mathsf{T}}(\tau)] = \mathbf{Q}(t)\delta(t - \tau) \tag{1.5}
$$

where $\mathbf{Q}(t)$ is the power spectral density function of $\boldsymbol{\mathsf{w}}(t)$, and $\delta(t - \tau)$ is the Dirac delta, a generalized function. We shall also assume that

<span id="page-25-0"></span>

$$
\mathrm{E}\big[\boldsymbol{\mathsf{w}}(t)(\boldsymbol{\mathsf{X}}(t_o) - \bar{\boldsymbol{X}}_o)^{\mathsf{T}}\big] = \mathbf{0},\ \forall\, t \tag{1.6}
$$

We shall take [\(1.3\)](#page-24-4) – [\(1.6\)](#page-25-0) to define the *dynamics model* for the additive EKF. Note that even though we have assumed $\boldsymbol{\mathsf{X}}(t_o)$ and $\boldsymbol{\mathsf{w}}(t)$ are Gaussian, we cannot assume that $\boldsymbol{\mathsf{X}}(t)$ remains Gaussian for $t > t_o$, because $\boldsymbol{f}$ may be a nonlinear function.

### 1.1.2. The Measurement Model

In an ideal world, we might have devices for measuring all of the state vector components directly; then state determination would be simply a matter of collecting enough such observations to reduce the state uncertainty to sufficient levels. Unfortunately, this is almost never the case. Instead, like Socrates' prisoners, we can usually only perceive noisy projections of the state elements, at discrete times, $t_i$, in the form of *measurements*:

<span id="page-25-1"></span>

$$
\boldsymbol{\mathsf{Y}}(t_i) = \boldsymbol{h}(\boldsymbol{\mathsf{X}}(t_i), t_i) + \boldsymbol{\mathsf{v}}(t_i) \tag{1.7}
$$

where $\boldsymbol{h}$ is a surjection from $\mathbb{R}^n$ to $\mathbb{R}^m$. We shall assume that $\boldsymbol{\mathsf{v}}(t_i)$, which we call the *measurement noise*, is a Gaussian sequence, with mean and covariance given by

<span id="page-25-6"></span>

$$
\mathrm{E}[\boldsymbol{\mathsf{v}}(t_i)] = \mathbf{0} \quad \text{and} \quad \mathrm{E}[\boldsymbol{\mathsf{v}}(t_i)\boldsymbol{\mathsf{v}}(t_j)^{\mathsf{T}}] = \mathbf{R}(t_i)\delta_{ij} \tag{1.8}
$$

where $\delta_{ij}$ is the Kronecker delta function. We shall also assume that

<span id="page-25-2"></span>

$$
\mathrm{E}\big[\boldsymbol{\mathsf{v}}(t_i)(\boldsymbol{\mathsf{X}}(t_o) - \bar{\boldsymbol{X}}_o)^{\mathsf{T}}\big] = \mathbf{0} \quad \text{and} \quad \mathrm{E}[\boldsymbol{\mathsf{w}}(t)\boldsymbol{\mathsf{v}}(t_i)^{\mathsf{T}}] = \mathbf{0},\ \forall\, i, t \tag{1.9}
$$

We shall take [\(1.7\)](#page-25-1) – [\(1.9\)](#page-25-2) to define the *measurement model* for the additive EKF. Note that we cannot assume that $\boldsymbol{\mathsf{Y}}(t_i)$ is Gaussian, because $\boldsymbol{h}$ may be a nonlinear function. For compactness of notation, we shall often suppress the time argument and write [\(1.7\)](#page-25-1) as

<span id="page-25-5"></span>

$$
\boldsymbol{\mathsf{Y}}_i = \boldsymbol{h}_i(\boldsymbol{\mathsf{X}}_i) + \boldsymbol{\mathsf{v}}_i \tag{1.10}
$$

### Bayes' Law, the Markov Property, and Observability

Bayes' Law tells us how to update the conditional probability density function (PDF) of $\boldsymbol{\mathsf{X}}(t_i)$, given a realization $\boldsymbol{Y}(t_i)$ of the random process $\boldsymbol{\mathsf{Y}}(t_i)$:

<span id="page-25-3"></span>

$$
\mathrm{p}_{\boldsymbol{\mathsf{X}}_i|\boldsymbol{\mathsf{Y}}_i}(\boldsymbol{X}_i|\boldsymbol{Y}_i) = \mathrm{p}_{\boldsymbol{\mathsf{Y}}_i|\boldsymbol{\mathsf{X}}_i}(\boldsymbol{Y}_i|\boldsymbol{X}_i)\,\frac{\mathrm{p}_{\boldsymbol{\mathsf{X}}_i}(\boldsymbol{X}_i)}{\mathrm{p}_{\boldsymbol{\mathsf{Y}}_i}(\boldsymbol{Y}_i)} \tag{1.11}
$$

If all the PDFs in [\(1.11\)](#page-25-3) were known, it would be relatively simple to use [\(1.11\)](#page-25-3) to estimate the state vector from a single measurement; our best estimate of the state would simply be the mean of $\mathrm{p}_{\boldsymbol{\mathsf{X}}_i|\boldsymbol{\mathsf{Y}}_i}(\boldsymbol{X}_i|\boldsymbol{Y}_i)$. But to apply [\(1.11\)](#page-25-3) to the navigation problem, where we have a time sequence of measurements, $\mathbb{Y}_i = \{\boldsymbol{Y}_i, \boldsymbol{Y}_{i-1}, \ldots, \boldsymbol{Y}_1\}$, we need to consider how the state dynamics evolve.

Unlike [\(1.1\)](#page-24-2), our dynamics model, given by [\(1.3\)](#page-24-4), only runs forward in time. Hence, the state at any future time depends only on its history. Also, because the non-homogeneous inputs to [\(1.3\)](#page-24-4) are uncorrelated by the Dirac delta in [\(1.5\)](#page-25-4), the value of the state at any particular time in the future depends only on its present value, and its accumulated diffusion due to the process noise over the interval between now and the future time of interest. Random processes such as this are said to possess the *Markov Property*. Using this property, we can write [\(1.11\)](#page-25-3) in terms of the measurement history as follows:

<span id="page-26-0"></span>

$$
\mathrm{p}_{\boldsymbol{\mathsf{X}}_i|\mathbb{Y}_i}(\boldsymbol{X}_i|\mathbb{Y}_i) = \mathrm{p}_{\boldsymbol{\mathsf{Y}}_i|\boldsymbol{\mathsf{X}}_i}(\boldsymbol{Y}_i|\boldsymbol{X}_i)\,\frac{\mathrm{p}_{\boldsymbol{\mathsf{X}}_i|\mathbb{Y}_{i-1}}(\boldsymbol{X}_i|\mathbb{Y}_{i-1})}{\mathrm{p}_{\boldsymbol{\mathsf{Y}}_i|\mathbb{Y}_{i-1}}(\boldsymbol{Y}_i|\mathbb{Y}_{i-1})} \tag{1.12}
$$

Even if we could compute all of the PDFs in [\(1.12\)](#page-26-0), we are not guaranteed that the sequence of measurements provide sufficient information to reduce the initial uncertainty of all the modes of [\(1.1\)](#page-24-2). If the system given by [\(1.1\)](#page-24-2) and [\(1.10\)](#page-25-5) is such that use of [\(1.12\)](#page-26-0) results in uncertainty in all the modes going asymptotically to zero in finite time, from any initial condition, then we say the system is *globally asymptotically observable*. If at least all of the unstable modes are observable, then we say the system is *detectable*. Unfortunately, for nonlinear systems, there is no known way to compute global observability. At best, under certain restrictions on [\(1.1\)](#page-24-2) and [\(1.10\)](#page-25-5), we can in principle establish local observability, in the neighborhood of a particular initial condition. However, this is a laborious calculation, often numerically unstable to evaluate. Also, note that observability is a property of the structure of [\(1.1\)](#page-24-2) and [\(1.10\)](#page-25-5), and hence is dependent on how one chooses to represent the navigation problem. Hence, a system that is observable with one representation may be unobservable with a different representation.

Kalman's original filter, which we now usually call the *linear Kalman filter* (LKF), is the result when the dynamics and measurement models are linear, Markov, Gaussian, and observable. An appreciation of the linear Kalman filter is essential to understanding the strengths and weaknesses of the EKF, although it is almost never the case that such assumptions are valid for real-world navigation problems.

### 1.1.3. The Linear Kalman Filter

Suppose the dynamics and measurements are given by the following discrete-time linear models:

<span id="page-26-2"></span>

$$
\boldsymbol{\mathsf{x}}_i = \boldsymbol{\Phi}_{i,i-1}\boldsymbol{\mathsf{x}}_{i-1} + \boldsymbol{\Gamma}_i\boldsymbol{\mathsf{u}}_i \tag{1.13}
$$

<span id="page-26-3"></span>

$$
\boldsymbol{\mathsf{y}}_i = \mathbf{H}_i\boldsymbol{\mathsf{x}}_i + \boldsymbol{\mathsf{v}}_i \tag{1.14}
$$

with

$$
\mathrm{E}[\boldsymbol{\mathsf{x}}_o] = \bar{\boldsymbol{x}}_o \quad \text{and} \quad \mathrm{E}[(\boldsymbol{\mathsf{x}}_o - \bar{\boldsymbol{x}}_o)(\boldsymbol{\mathsf{x}}_o - \bar{\boldsymbol{x}}_o)]^{\mathsf{T}}] = \mathbf{P}_o \tag{1.15}
$$

$$
\mathrm{E}[\boldsymbol{\mathsf{u}}_i] = \mathbf{0} \quad \text{and} \quad \mathrm{E}\big[\boldsymbol{\Gamma}_i\boldsymbol{\mathsf{u}}_i\boldsymbol{\mathsf{u}}_j^{\mathsf{T}}\boldsymbol{\Gamma}_i^{\mathsf{T}}\big] = \mathbf{S}_i\delta_{ij} \tag{1.16}
$$

and the moments of $\boldsymbol{\mathsf{v}}_i$ as given by [\(1.8\)](#page-25-6). This system will be globally observable if the *observability Gramian* is strictly positive definite,

<span id="page-26-1"></span>

$$
\mathbf{W}_k = \sum_{i=1}^{k} \boldsymbol{\Phi}_{i,1}^{\mathsf{T}}\mathbf{H}_i^{\mathsf{T}}\mathbf{H}_i\boldsymbol{\Phi}_{i,1} > 0 \tag{1.17}
$$

i.e. it has full rank.

With such assumptions, Kalman showed [[44](16-bibliography.md#page-171-1)] that Algorithm [1.1](#page-27-0) provides an optimal (both minimum variance and maximum likelihood) estimate of the moments of the PDFs appearing in [\(1.11\)](#page-25-3). Note that in Algorithm [1.1,](#page-27-0) the covariance recursion given by [\(1.19\)](#page-27-1) and [\(1.22\)](#page-27-2) does not depend on the measurement history, and hence one may compute the gain sequence, $\mathbf{K}_i$, off-line and store it as a time-indexed table or *schedule*, along with $\boldsymbol{\Phi}_{i,i-1}$ and $\mathbf{H}_i$. Also note that because the system is globally observable, there is no chance that it will fail to converge from any initial condition, except perhaps due to build up of numerical truncation and/or roundoff error.

If we further suppose the dynamics and measurements are given by linear time-invariant (LTI) models,

$$
\boldsymbol{\mathsf{x}}_i = \boldsymbol{\Phi}\boldsymbol{\mathsf{x}}_{i-1} + \boldsymbol{\Gamma}\boldsymbol{\mathsf{u}}_i \tag{1.23}
$$

$$
\boldsymbol{\mathsf{y}}_i = \mathbf{H}\boldsymbol{\mathsf{x}}_i + \boldsymbol{\mathsf{v}}_i \tag{1.24}
$$

then we may test its global observability using a somewhat simpler calculation than [\(1.17\)](#page-26-1), as follows:

$$
\mathbf{W} = \begin{bmatrix} \mathbf{H} \\ \mathbf{H}\boldsymbol{\Phi} \\ \mathbf{H}\boldsymbol{\Phi}^2 \\ \vdots \\ \mathbf{H}\boldsymbol{\Phi}^{n-1} \end{bmatrix} > 0 \tag{1.25}
$$

If the system is detectable, then it turns out that the covariance recursion given by [\(1.19\)](#page-27-1) and [\(1.22\)](#page-27-2) reaches a steady-state, which we denote $\mathbf{P}_\infty$. The corresponding gain is $\mathbf{K}_\infty = \mathbf{P}_\infty\mathbf{H}^{\mathsf{T}}\mathbf{R}^{-1}$. There exist numerous software packages that will compute such quantities, e.g. the *Matlab Control Systems Toolbox*, which may unfortunately lead to their misuse in inappropriate contexts. Perhaps worse, experts from other domains, who are familiar with techniques such as pole placement for control of LTI systems, may recognize that the steady-state linear Kalman filter is "just a pole placement algorithm," and may infer that the EKF is not much more than a clever pole placement algorithm as well. As we shall show below, this is far from being the case; the EKF operates directly on the nonlinear system of interest, for which such LTI concepts have dubious applicability.

> <span id="page-27-0"></span>**Algorithm 1.1** The Linear Kalman Filter
>
> <span id="page-27-3"></span>
>
> $$ \hat{\boldsymbol{x}}_i^- = \boldsymbol{\Phi}_{i,i-1}\hat{\boldsymbol{x}}_{i-1}^+, \quad \hat{\boldsymbol{x}}_0^+ = \bar{\boldsymbol{x}}_o \tag{1.18} $$
>
> <span id="page-27-1"></span>
>
> $$ \mathbf{P}_i^- = \boldsymbol{\Phi}_{i,i-1}\mathbf{P}_{i-1}^+\boldsymbol{\Phi}_{i,i-1}^{\mathsf{T}} + \mathbf{S}_i, \quad \mathbf{P}_0^+ = \mathbf{P}_o \tag{1.19} $$
>
> $$ \mathbf{K}_i = \mathbf{P}_i^-\mathbf{H}_i^{\mathsf{T}}\left(\mathbf{H}_i\mathbf{P}_i^-\mathbf{H}_i^{\mathsf{T}} + \mathbf{R}_i\right)^{-1} \tag{1.20} $$
>
> $$ \hat{\boldsymbol{x}}_i^+ = \hat{\boldsymbol{x}}_i^- + \mathbf{K}_i\left(\boldsymbol{y}_i - \mathbf{H}_i\hat{\boldsymbol{x}}_i^-\right) \tag{1.21} $$
>
> <span id="page-27-2"></span>
>
> $$ \mathbf{P}_i^+ = \mathbf{P}_i^- - \mathbf{K}_i\mathbf{H}_i\mathbf{P}_i^- \tag{1.22} $$

### 1.1.4. The Linearized Kalman Filter

An immediately apparent generalization of the linear Kalman Filter is to use it to solve for small corrections to a nonlinearly propagated *fixed* reference trajectory. While such an approach may have certain applications over limited time horizons, and/or for ground-based applications where an operator can periodically intervene, experience with onboard navigation systems has shown that such corrections can fail to remain small enough to justify the required approximations.

### 1.1.5. The Extended Kalman Filter

There are a number of ways to proceed from Algorithm [1.1](#page-27-0) to "derive" the EKF, but all contain a variety of *ad hoc* assumptions that are not guaranteed to hold in all circumstances. Most weaknesses and criticisms of the EKF arise from such assumptions. Rather than reproduce one or more of such derivations, we will simply point out that if one replaces [\(1.18\)](#page-27-3) with an integral of [\(1.1\)](#page-24-2) over the time between measurements, and computes the coefficient matrices appearing in [\(1.13\)](#page-26-2) and [\(1.14\)](#page-26-3) as Jacobians evaluated at the current solution of [\(1.1\)](#page-24-2), then the result is Algorithm [1.2,](#page-28-0) which bears more than a passing resemblance to the Kalman filter.

Several observations are in order regarding Algorithm [1.2.](#page-28-0)

> <span id="page-28-0"></span>**Algorithm 1.2** A Naive Extension of the Kalman Filter
>
> <span id="page-28-1"></span>
>
> $$ \hat{\boldsymbol{X}}_i^- = \hat{\boldsymbol{X}}_{i-1}^+ + \int_{t_{i-1}}^{t_i} \boldsymbol{f}(\boldsymbol{X}(\tau), \tau)\,\mathrm{d}\tau, \quad \hat{\boldsymbol{X}}_0^+ = \bar{\boldsymbol{X}}_o \tag{1.26} $$
>
> $$ \mathbf{A}(t) = \left.\frac{\partial \boldsymbol{f}}{\partial \boldsymbol{X}}\right|_{\hat{\boldsymbol{X}}(t)}, \quad \mathbf{H}_i = \left.\frac{\partial \boldsymbol{h}_i}{\partial \boldsymbol{X}}\right|_{\hat{\boldsymbol{X}}_i^-} \tag{1.27} $$
>
> <span id="page-28-6"></span>
>
> $$ \boldsymbol{\Phi}(t_i, t_{i-1}) = \mathbf{I} + \int_{t_{i-1}}^{t_i} \mathbf{A}(\tau)\boldsymbol{\Phi}(t_i, \tau)\,\mathrm{d}\tau \tag{1.28} $$
>
> <span id="page-28-5"></span>
>
> $$ \mathbf{S}_i = \int_{t_{i-1}}^{t_i}\int_{t_{i-1}}^{t_i} \boldsymbol{\Phi}(t_i, \tau)\mathbf{B}(\tau)\,\mathrm{E}[\boldsymbol{\mathsf{w}}(\tau)\boldsymbol{\mathsf{w}}^{\mathsf{T}}(\sigma)]\,\mathbf{B}^{\mathsf{T}}(\sigma)\boldsymbol{\Phi}^{\mathsf{T}}(t_i, \sigma)\,\mathrm{d}\tau\,\mathrm{d}\sigma \tag{1.29} $$
>
> <span id="page-28-7"></span>
>
> $$ \mathbf{P}_i^- = \boldsymbol{\Phi}(t_i, t_{i-1})\mathbf{P}_{i-1}^+\boldsymbol{\Phi}^{\mathsf{T}}(t_i, t_{i-1}) + \mathbf{S}_i, \quad \mathbf{P}_0^+ = \mathbf{P}_o \tag{1.30} $$
>
> <span id="page-28-4"></span>
>
> $$ \mathbf{K}_i = \mathbf{P}_i^-\mathbf{H}_i^{\mathsf{T}}\left(\mathbf{H}_i\mathbf{P}_i^-\mathbf{H}_i^{\mathsf{T}} + \mathbf{R}_i\right)^{-1} \tag{1.31} $$
>
> <span id="page-28-2"></span>
>
> $$ \hat{\boldsymbol{X}}_i^+ = \hat{\boldsymbol{X}}_i^- + \mathbf{K}_i\Big(\boldsymbol{Y}_i - \boldsymbol{h}_i(\hat{\boldsymbol{X}}_i^-)\Big) \tag{1.32} $$
>
> <span id="page-28-3"></span>
>
> $$ \mathbf{P}_i^+ = \mathbf{P}_i^- - \mathbf{K}_i\mathbf{H}_i\mathbf{P}_i^- \tag{1.33} $$

- One might infer from [\(1.26\)](#page-28-1) that $\hat{\boldsymbol{X}}_i^- = \mathrm{E}[\boldsymbol{\mathsf{X}}|\mathbb{Y}_{i-1}]$. This would be a somewhat problematic inference however, since in general

  $$
  \int_{t_{i-1}}^{t_i} \boldsymbol{f}(\mathrm{E}[\boldsymbol{X}(\tau)], \tau)\,\mathrm{d}\tau \neq \mathrm{E}\left[\int_{t_{i-1}}^{t_i} \boldsymbol{f}(\boldsymbol{X}(\tau), \tau)\,\mathrm{d}\tau\right] \tag{1.34}
  $$

  This implies that an initially Gaussian distribution for the state cannot in general remain Gaussian. At best, all we can hope is that $\hat{\boldsymbol{X}}_i^- \approx \mathrm{E}[\boldsymbol{\mathsf{X}}|\mathbb{Y}_{i-1}]$.

- Let us define the *estimation error* as $\boldsymbol{\mathsf{e}}(t) = \boldsymbol{\mathsf{X}}(t) - \hat{\boldsymbol{X}}(t)$. Then since $\hat{\boldsymbol{X}}(t) \neq \mathrm{E}[\boldsymbol{\mathsf{X}}(t)|\mathbb{Y}_{i-1}]$,

  $$
  \mathbf{P}(t) \neq \mathrm{E}[\boldsymbol{\mathsf{e}}(t)\boldsymbol{\mathsf{e}}^{\mathsf{T}}(t)|\mathbb{Y}_{i-1}] \tag{1.35}
  $$

  At best, all we can hope is that $\mathbf{P}(t) \approx \mathrm{E}[\boldsymbol{\mathsf{e}}(t)\boldsymbol{\mathsf{e}}^{\mathsf{T}}(t)|\mathbb{Y}_{i-1}]$.

- Let us define the *innovation* as $\boldsymbol{\mathsf{r}}_i = \boldsymbol{\mathsf{Y}}_i - \mathbf{h}(\hat{\boldsymbol{X}}_i^-)$. Then since $\mathbf{h}(\hat{\boldsymbol{X}}_i^-) \neq \mathrm{E}[\boldsymbol{\mathsf{Y}}]$,

  $$
  \mathbf{H}_i\mathbf{P}_i^-\mathbf{H}_i^{\mathsf{T}} + \mathbf{R}_i \neq \mathrm{E}[\boldsymbol{\mathsf{r}}_i\boldsymbol{\mathsf{r}}_i^{\mathsf{T}}] \tag{1.36}
  $$

  At best, all we can hope is that the above will hold approximately.

- Taken together, the approximations listed above imply that [\(1.32\)](#page-28-2) and [\(1.33\)](#page-28-3) can at best satisfy [\(1.12\)](#page-26-0) only approximately, not only because the mean and covariance are approximations, but also because the PDFs fail to remain Gaussian, and hence fail to be characterized completely by only their first two moments.

- Even if all of the above are reasonable approximations, there is a problem with [\(1.33\)](#page-28-3). The *posterior covariance* should be approximated by

  $$
  \mathbf{P}_i^+ \approx \mathrm{E}\big[\boldsymbol{\mathsf{e}}_i^+(\boldsymbol{\mathsf{e}}_i^+)^{\mathsf{T}}|\mathbb{Y}_i\big] \tag{1.37}
  $$

  Let us assume that

  $$
  \boldsymbol{\mathsf{Y}}_i - \boldsymbol{h}_i(\hat{\boldsymbol{X}}_i^-) \approx \mathbf{H}_i\boldsymbol{\mathsf{e}}_i^- + \boldsymbol{\mathsf{v}}_i \tag{1.38}
  $$

  Then [\(1.32\)](#page-28-2) implies that

  $$
  \boldsymbol{\mathsf{e}}_i^+ = \boldsymbol{\mathsf{e}}_i^- - \mathbf{K}_i\mathbf{H}_i\boldsymbol{\mathsf{e}}_i^- - \mathbf{K}_i\boldsymbol{\mathsf{v}}_i \tag{1.39}
  $$

  and by our prior assumption that $\mathrm{E}\big[\boldsymbol{\mathsf{e}}_i^-\boldsymbol{\mathsf{v}}_i^{\mathsf{T}}\big] = \mathbf{0}$,

  $$
  \mathbf{P}_i^+ \approx \mathrm{E}\big[\boldsymbol{\mathsf{e}}_i^+(\boldsymbol{\mathsf{e}}_i^+)^{\mathsf{T}}|\mathbb{Y}_i\big] \tag{1.40}
  $$

  <span id="page-29-1"></span>

  $$
  = (\mathbf{I} - \mathbf{K}_i\mathbf{H}_i)\,\mathbf{P}_i^-\,(\mathbf{I} - \mathbf{K}_i\mathbf{H}_i)^{\mathsf{T}} + \mathbf{K}_i\mathbf{R}_i\mathbf{K}_i^{\mathsf{T}} \tag{1.41}
  $$

  Equation [\(1.41\)](#page-29-1) is *Joseph's Formula*, and it holds for any gain $\mathbf{K}_i$. Only for the optimal gain and true covariance does [\(1.41\)](#page-29-1) reduce to [\(1.33\)](#page-28-3). Since [\(1.31\)](#page-28-4) was computed with only an approximate covariance, and due to the various other approximations listed above as well, $\mathbf{K}_i$ cannot be the optimal gain, so at best, [\(1.33\)](#page-28-3) will only hold approximately. At worst, such approximations may lead to $\mathbf{P}_i^+$ becoming non-positive definite, which is a significant issue. Because of its symmetric and additive form, [\(1.41\)](#page-29-1) is much less likely (but not impossible!) to produce a non-positive definite $\mathbf{P}_i^+$.

- By our assumption that $\mathrm{E}[\boldsymbol{\mathsf{w}}(t)\boldsymbol{\mathsf{w}}^{\mathsf{T}}(\tau)] = \mathbf{Q}(t)\delta(t-\tau)$, one of the integrals in [\(1.29\)](#page-28-5) should be annihilated by the Dirac delta, resulting in

  <span id="page-29-2"></span>

  $$
  \mathbf{S}_i = \int_{t_{i-1}}^{t_i} \boldsymbol{\Phi}(t_i, \tau)\mathbf{B}(\tau)\mathbf{Q}(\tau)\mathbf{B}^{\mathsf{T}}(\tau)\boldsymbol{\Phi}^{\mathsf{T}}(t_i, \tau)\,\mathrm{d}\tau \tag{1.42}
  $$

  In any case, unlike for a discrete time dynamics model,

  $$
  \begin{aligned}
  &\mathrm{E}\left[\int_{t_{i-1}}^{t_i}\int_{t_{i-1}}^{t_i} \boldsymbol{\Phi}(t_i, \tau)\mathbf{B}(\tau)\boldsymbol{\mathsf{w}}(\tau)\boldsymbol{\mathsf{w}}^{\mathsf{T}}(\sigma)\mathbf{B}^{\mathsf{T}}(\sigma)\boldsymbol{\Phi}^{\mathsf{T}}(t_i, \sigma)\,\mathrm{d}\tau\,\mathrm{d}\sigma\right] \\
  &\qquad \neq \mathrm{E}\left[\int_{t_{i-1}}^{t_i} \boldsymbol{\Phi}(t_i, \tau)\mathbf{B}(\tau)\boldsymbol{\mathsf{w}}(\tau)\,\mathrm{d}\tau \int_{t_{i-1}}^{t_i} \boldsymbol{\mathsf{w}}^{\mathsf{T}}(\tau)\mathbf{B}^{\mathsf{T}}(\tau)\boldsymbol{\Phi}^{\mathsf{T}}(t_i, \tau)\,\mathrm{d}\tau\right]
  \end{aligned} \tag{1.43}
  $$

- In general, one would need to simultaneously integrate [\(1.26\)](#page-28-1) and [\(1.28\)](#page-28-6) due to their interdependence via the Jacobian $\mathbf{A}$. If the time between measurements is small enough, then if one were to employ a suitable approximation for [\(1.28\)](#page-28-6), perhaps as simple as

  $$
  \boldsymbol{\Phi}(t_i, t_{i-1}) \approx \mathbf{I} + \mathbf{A}(t_i)\,(t_i - t_{i-1}) \tag{1.44}
  $$

  then one may reasonably expect that a carefully chosen approximation would be no worse than the many other approximations inherent in the EKF. One may also consider the same or simpler approximations when considering approximations to [\(1.42\)](#page-29-2).

- Because there is no way to prove global observability for a nonlinear system, the EKF may fail to converge from some initial conditions, even if the system is locally observable in particular neighborhoods.

In light of the above observations, we conclude this section by presenting a slightly improved version of the EKF as Algorithm [1.3.](#page-30-0) In subsequent chapters, we shall describe additional improvements to the EKF.

## 1.2. The Multiplicative Extended Kalman Filter

<span id="page-29-0"></span>An interesting variation on the EKF is possible in the context of estimating attitude parameters. An attitude correction may be viewed as a small-angle rotation from a frame associated with the previous estimate to a frame associated with a current estimate. In this context, one may use the previous attitude estimate as a linearization reference for a linearized Kalman Filter's Jacobian matrices, and estimate the small-angle correction as the filter state. After each state update, one performs a rectification of the attitude reference by applying the small-angle correction. Since for many attitude representations, a frame rotation is multiplicative operation, this procedure has become known as the multiplicative EKF. Chapter [9](09-attitude-estimation.md#page-108-0) covers this subject.

> <span id="page-30-0"></span>**Algorithm 1.3** A Slightly Improved Extension of the Kalman Filter
>
> <span id="page-30-1"></span>
>
> $$ \hat{\boldsymbol{X}}_i^- = \hat{\boldsymbol{X}}_{i-1}^+ + \int_{t_{i-1}}^{t_i} \boldsymbol{f}(\boldsymbol{X}(\tau), \tau)\,\mathrm{d}\tau, \quad \hat{\boldsymbol{X}}_0^+ = \bar{\boldsymbol{X}}_o \tag{1.45} $$
>
> $$ \mathbf{A}(t) = \left.\frac{\partial \boldsymbol{f}}{\partial \boldsymbol{X}}\right|_{\hat{\boldsymbol{X}}(t)}, \quad \mathbf{H}_i = \left.\frac{\partial \boldsymbol{h}_i}{\partial \boldsymbol{X}}\right|_{\hat{\boldsymbol{X}}_i^-} \tag{1.46} $$
>
> $$ \boldsymbol{\Phi}(t_i, t_{i-1}) = \text{a suitable approximation to (1.28)} \tag{1.47} $$
>
> $$ \mathbf{S}_i = \text{a suitable approximation to (1.42)} \tag{1.48} $$
>
> <span id="page-30-2"></span>
>
> $$ \mathbf{P}_i^- = \boldsymbol{\Phi}(t_i, t_{i-1})\mathbf{P}_{i-1}^+\boldsymbol{\Phi}^{\mathsf{T}}(t_i, t_{i-1}) + \mathbf{S}_i, \quad \mathbf{P}_0^+ = \mathbf{P}_o \tag{1.49} $$
>
> $$ \mathbf{K}_i = \mathbf{P}_i^-\mathbf{H}_i^{\mathsf{T}}\left(\mathbf{H}_i\mathbf{P}_i^-\mathbf{H}_i^{\mathsf{T}} + \mathbf{R}_i\right)^{-1} \tag{1.50} $$
>
> $$ \hat{\boldsymbol{X}}_i^+ = \hat{\boldsymbol{X}}_i^- + \mathbf{K}_i\Big(\boldsymbol{Y}_i - \boldsymbol{h}_i(\hat{\boldsymbol{X}}_i^-)\Big) \tag{1.51} $$
>
> $$ \mathbf{P}_i^+ = (\mathbf{I} - \mathbf{K}_i\mathbf{H}_i)\,\mathbf{P}_i^-\,(\mathbf{I} - \mathbf{K}_i\mathbf{H}_i)^{\mathsf{T}} + \mathbf{K}_i\mathbf{R}_i\mathbf{K}_i^{\mathsf{T}} \tag{1.52} $$

---

[← Front Matter](00-front-matter.md) · [Contents](README.md) · [Chapter 2. Batch-Sequential Filters →](02-batch-sequential-filters.md)
