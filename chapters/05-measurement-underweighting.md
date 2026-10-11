[← Chapter 4. Processing Measurements](04-processing-measurements.md) · [Contents](README.md) · [Chapter 6. Bias Modeling (part 1 of 2) →](06-bias-modeling-part1.md)

# <span id="page-64-0"></span>Chapter 5. Measurement Underweighting

*Contributed by Renato Zanetti*

## 5.1. Introduction

<span id="page-64-1"></span>Given an $`m`$-dimensional random measurement $`{𝘆}`$ which is somehow related to an unknown, $`n`$-dimensional random vector $`{𝘅}`$ the family of affine estimators of $`{𝘅}`$ from $`{𝘆}`$ is

```math
\hat{{𝒙}} = {𝒂} + {𝐊}\,{𝘆} \qquad\qquad(5.1)
```

where $`{𝒂} \in \Re^{n}`$ and $`{𝐊} \in \Re^{n \times m}`$. The optimal, in a Minimum Mean Square Error sense, affine estimator has

```math
{𝐊} = {𝐏}_{{𝒙𝒚}}\,{𝐏}_{{𝒚𝒚}}^{-1} \qquad\qquad(5.2)
```

```math
{𝒂} = \mathrm{E}[{𝘅}] - {𝐊}\;\mathrm{E}[{𝘆}] \qquad\qquad(5.3)
```

where

```math
{𝐏}_{{𝒙𝒚}} = \mathrm{E}\Big[\Big({𝘅} - \mathrm{E}[{𝘅}]\Big)\Big({𝘆} - \mathrm{E}[{𝘆}]\Big)^{\top}\Big] \qquad\qquad(5.4)
```

```math
{𝐏}_{{𝒚𝒚}} = \mathrm{E}\Big[\Big({𝘆} - \mathrm{E}[{𝘆}]\Big)\Big({𝘆} - \mathrm{E}[{𝘆}]\Big)^{\top}\Big] \qquad\qquad(5.5)
```

In the presence of nonlinear measurements of the state,

```math
{𝘆} = {𝒉}({𝘅}) + {𝒗} \qquad\qquad(5.6)
```

(where $`{𝒗}`$ is zero-mean measurement noise) the extended Kalman filter (EKF) [[27](16-bibliography.md#page-171-5)] approximates all moments of $`{𝘆}`$ by linearization of the measurement function centered on the mean of $`{𝘅}`$. This methodology has proven very effective and produces very satisfactory results in most cases. Approaches other than the EKF exist, for example the Unscented Kalman Filter [[40](16-bibliography.md#page-171-8)] approximates the same quantities via stochastic linearization using a deterministic set of Sigma Points. High order truncations of the Taylor series are also possible. Underweighting [[46](16-bibliography.md#page-171-9),[50](16-bibliography.md#page-172-1)] is an ad-hoc technique to compensating for nonlinearities in the measurement models that are neglected by the EKF and successfully flew on the Space Shuttle, on Orion Exploration Flight Test 1, and the Artemis I mission.

The commonly implemented method for the underweighting of measurements for human space navigation was introduced by Lear [[48](16-bibliography.md#page-171-10)] for the Space Shuttle navigation system. In 1966 Denham and Pines showed the possible inadequacy of the linearization approximation when the effect of measurement nonlinearity is comparable to the measurement error [[19](16-bibliography.md#page-170-12)]. To compensate for the nonlinearity Denham and Pines proposed to increase the measurement noise covariance by a constant amount. In the early seventies, in anticipation of Shuttle flights, Lear and others developed relationships which accounted for the second-order effects in the measurements [[50](16-bibliography.md#page-172-1)].

It was noted that in situations involving large state errors and very precise measurements, application of the standard extended Kalman filter mechanization leads to conditions in which the state estimation error covariance decreases more rapidly than the actual state errors. Consequently the extended Kalman filter begins to ignore new measurements even when the measurement residual is relatively large. Underweighting was introduced to slow down the convergence of the state estimation error covariance thereby addressing the situation in which the error covariance becomes overly optimistic with respect to the actual state errors. The original work on the application of second-order correction terms led to the determination of the underweighting method by trial-and-error [[48](16-bibliography.md#page-171-10)].

More recently, studies on the effects of nonlinearity in sensor fusion problems with application to relative navigation have produced a so-called "bump-up" factor. [[23](16-bibliography.md#page-171-11), [54](16-bibliography.md#page-172-4), [67](16-bibliography.md#page-172-5), [69](16-bibliography.md#page-172-6)]. While Ferguson [[23](16-bibliography.md#page-171-11)] seems to initiate the use of the bump-up factor, the problem of mitigating filter divergence was more fully studied by Plinval [[69](16-bibliography.md#page-172-6)] and subsequently by Mandic [[54](16-bibliography.md#page-172-4)]. Mandic generalized Plinval's bump-up factor to allow flexibility and notes that the value selected influences the steady-state convergence of the filter. In essence, it was found that a larger factor keeps the filter from converging to the level that a lower factor would permit. This finding prompted Mandic to propose a two-step algorithm in which the bump-up factor is applied for a certain number of measurements only, upon which the factor was completely turned off. Finally, Perea, et al. [[67](16-bibliography.md#page-172-5)] summarize the findings of the previous works and introduce several ways of computing the applied factor. In all cases, the bump-up factor amounts in application to the underweighting factor introduced in Lear [[48](16-bibliography.md#page-171-10)]. Save for the two-step procedure of Mandic, the bump-up factor is allowed to persistently affect the Kalman gain which directly influences the obtainable steady-state covariance. Effectively, the ability to remove the underweighting factor autonomously and under some convergence condition was not introduced.

The work of Lear [[12](16-bibliography.md#page-170-13),[49](16-bibliography.md#page-171-12)] is not well known as it is mostly only documented in internal NASA memos [[48](16-bibliography.md#page-171-10),[50](16-bibliography.md#page-172-1)]. Kriegsman and Tau [[46](16-bibliography.md#page-171-9)] mention underweighting in their 1975 Shuttle navigation paper without a detailed explanation of the technique.

## 5.2. Nonlinear Effects and the Need for Underweighting

<span id="page-65-0"></span>We review briefly the three state estimate update approaches assuming a linear time-varying measurement model leading to the classical Kalman filter, a nonlinear measurement model with first-order linearization approximations leading the widely used extended Kalman filter, and a nonlinear model with second-order approximations leading to the second-order extended Kalman filter.

### 5.2.1. Linear Measurement Model and the Classical Kalman Filter Update

Let's briefly recap the linear Kalman filter. The measurement model is

```math
{𝒚}_i = {𝐇}_i {𝒙}_i + {𝒗}_i\,, \qquad\qquad(5.7)
```

where $`{𝒚}_i \in {ℝ}^m`$ are the $`m`$ measurements at each time $`t_i`$, $`{𝒙}_i \in {ℝ}^n`$ is the $`n`$-dimensional state vector, $`{𝐇}_i \in {ℝ}^{m \times n}`$ is the known measurement mapping matrix, $`{𝒗}_i \in {ℝ}^m`$ is modeled as a zero-mean white-noise sequence with $`\mathrm{E}[{𝒗}_i] = 0,\ \forall\ k`$ and $`\mathrm{E}\Big[{𝒗}_i {𝒗}_j^{\top}\Big] = {𝐑}_i \delta_{kj}`$ where $`{𝐑}_i \gt 0\ \forall\ k`$ and $`\delta_{kj} = 1`$ when $`k = j`$ and $`\delta_{kj} = 0`$ when $`k \neq j`$. The Kalman filter state update algorithm provides an optimal blending of the *a priori* estimate $`\hat{{𝒙}}_i^-`$ and the measurement $`{𝒚}_i`$ at time $`t_i`$ to obtain the *a posteriori* state estimate $`\hat{{𝒙}}_i^+`$ via

<span id="page-65-1"></span>

```math
\hat{{𝒙}}_i^+ = \hat{{𝒙}}_i^- + {𝐊}_i \Bigl[{𝒚}_i - {𝐇}_i \hat{{𝒙}}_i^-\Bigr]\,, \qquad\qquad(5.8)
```

where the superscript $`^-`$ denotes *a priori* and $`^+`$ denotes *a posteriori*.

Defining the *a priori* estimation error as $`{𝒆}_i^- = {𝒙}_i - \hat{{𝒙}}_i^-`$ and the *a posteriori* estimation error as $`{𝒆}_i^+ = {𝒙}_i - \hat{{𝒙}}_i^+`$ and assuming these errors to be zero mean, the associated symmetric, positive definite *a priori* and *a posteriori* estimation error covariances are $`{𝐏}_i^- = \mathrm{E}\Big[{𝒆}_i^-\Bigl({𝒆}_i^-\Bigr)^{\top}\Big]`$ and $`{𝐏}_i^+ = \mathrm{E}\Big[{𝒆}_i^+\Bigl({𝒆}_i^+\Bigr)^{\top}\Big]`$, respectively. Using Eq. [\(5.8\)](#page-65-1) and the definitions of the state estimation errors and error covariances, we obtain the *a posteriori* state estimation error covariance via the well-known Joseph formula

<span id="page-66-1"></span>

```math
{𝐏}_i^+ = [{𝐈} - {𝐊}_i {𝐇}_i]\,{𝐏}_i^-\,[{𝐈} - {𝐊}_i {𝐇}_i]^{\top} + {𝐊}_i {𝐑}_i {𝐊}_i^{\top}\,, \qquad\qquad(5.9)
```

which is valid for any $`{𝐊}_i`$. If the gain $`{𝐊}_i`$ is chosen so as to minimize the trace of the *a posteriori* estimation error, we call that gain the Kalman gain which is given by

<span id="page-66-0"></span>

```math
{𝐊}_i = {𝐏}_i {𝐇}_i^{\top}\Bigl[{𝐇}_i {𝐏}_i^- {𝐇}_i^{\top} + {𝐑}_i\Bigr]^{-1}. \qquad\qquad(5.10)
```

The trace of the state estimation error covariance is generally not a norm but is equivalent to the nuclear norm (the matrix Shatten 1-norm) for symmetric semi-positive matrices. If the gain given in Eq. [\(5.10\)](#page-66-0) is applied to the state estimation error covariance of Eq. [\(5.9\)](#page-66-1), then the update equation can be rewritten after some manipulation as

<span id="page-66-3"></span>

```math
{𝐏}_i^+ = [{𝐈} - {𝐊}_i {𝐇}_i]\,{𝐏}_i^-\,, \qquad\qquad(5.11)
```

or equivalently,

<span id="page-66-4"></span>

```math
{𝐏}_i^+ = {𝐏}_i^- - {𝐊}_i[{𝐇}_i {𝐏}_i^- {𝐇}_i^{\top} + {𝐑}_i]{𝐊}_i^{\top}. \qquad\qquad(5.12)
```

Under the assumptions of the Kalman filter development (linear, time-varying measurement model with a zero-mean white-noise sequence corrupting the measurements, unbiased *a priori* estimation errors, known dynamics and measurement models, etc.), the state estimate and state estimation error covariance updates are optimal and we expect no filter divergence issues. The estimation error covariance will remain positive definite for all $`t_i`$ and the estimation error covariance will be consistent with the true errors. In practice, the measurements are usually nonlinear functions of the state, leading to a variety of engineering solutions that must be carefully designed to ensure acceptable state estimation performance. Underweighting is one such method to improve the performance of the extended Kalman filter in practical settings.

### 5.2.2. The Nonlinear Measurement Model and the Extended Kalman Filter Update

In the nonlinear setting, consider the measurement model given by

```math
{𝒚}_i = {𝒉}({𝒙}_i, t_i) + {𝒗}_i\,, \qquad\qquad(5.13)
```

where $`{𝒉}({𝒙}_i) \in {ℝ}^m`$ is a vector-valued differentiable nonlinear function of the state vector $`{𝒙}_i \in {ℝ}^n`$. The idea behind the extended Kalman filter (EKF) is to utilize Taylor series approximations to obtain linearized models in such a fashion that the EKF state update algorithm has the same general form as the Kalman filter.

<span id="page-66-5"></span>

```math
{𝒚}_i \simeq {𝒉}(\hat{{𝒙}}_i^-, t_i) + {𝐇}_i\,{𝒆}_i^- + {𝒗}_i\,, \qquad\qquad(5.14)
```

where

<span id="page-66-2"></span>

```math
{𝐇}_i \triangleq \biggl[\left.\frac{\partial {𝒉}({𝒙}_i, t_i)}{\partial {𝒙}_i}\right|_{{𝒙}_i = \hat{{𝒙}}_i^-}\biggr]. \qquad\qquad(5.15)
```

Since the estimation error is (approximately) zero mean and the measurement noise is zero mean, it follows that

```math
\mathrm{E}[{𝒚}_i] \simeq {𝒉}(\hat{{𝒙}}_i^-, t_i), \qquad\qquad(5.16)
```

where all expectations are conditioned on past measurements and we find that the state estimate update is given by [[27](16-bibliography.md#page-171-5)]

<span id="page-67-0"></span>

```math
\hat{{𝒙}}_i^+ = \hat{{𝒙}}_i^- + {𝐊}_i[{𝒚}_i - {𝒉}(\hat{{𝒙}}_i^-)]\,. \qquad\qquad(5.17)
```

Similarly, the measurement residual is given by

```math
{𝒓}_i = {𝒚}_i - {𝒉}(\hat{{𝒙}}_i^-) \simeq {𝐇}_i {𝒆}_i^- + {𝒗}_i\,, \qquad\qquad(5.18)
```

Computing the measurement residual covariance $`\mathrm{E}[{𝒓}_i {𝒓}_i^{\top}]`$ yields

<span id="page-67-3"></span>

```math
{𝐖}_i = {𝐇}_i {𝐏}_i^- {𝐇}_i^{\top} + {𝐑}_i\,. \qquad\qquad(5.19)
```

The state estimation error covariance and Kalman gain are the same as in Eqs. [\(5.9\)](#page-66-1) and [\(5.10\)](#page-66-0), respectively, with $`{𝐇}_i`$ given as in Eq. [\(5.15\)](#page-66-2). The state estimation error covariances in the forms shown in Eqs. [\(5.11\)](#page-66-3) and [\(5.12\)](#page-66-4) also hold in the nonlinear setting with $`{𝐇}_i`$ as in Eq. [\(5.15\)](#page-66-2).

From Eqs. [\(5.12\)](#page-66-4) and [\(5.17\)](#page-67-0), it is seen that reducing the Kalman gain leads to a smaller update in both the state estimation error covariance and the state estimate, respectively. Reducing the gain and hence the update is the essence of underweighting and the need for this adjustment is illuminated in the following discussion.

Adopting the viewpoint that the state estimation error covariance matrix represents the level of uncertainty in the state estimate, we expect that when we process a measurement (adding new information) the uncertainty would decrease (or at least, not increase). This is, in fact, the case and can be seen in Eq. [\(5.12\)](#page-66-4). Under the assumption that the symmetric matrices $`{𝐏}_i^- \gt 0`$ and $`{𝐑}_i \gt 0`$, it follows that

```math
{𝐊}_i[{𝐇}_i {𝐏}_i^- {𝐇}_i^{\top} + {𝐑}_i]{𝐊}_i^{\top} \geq 0\,, \qquad\qquad(5.20)
```

and we can find a number $`\alpha_i \geq 0`$ at each time $`t_i`$ such that

```math
{𝐏}_i^- - {𝐏}_i^+ \geq \alpha_i {𝑰}\,, \qquad\qquad(5.21)
```

which shows that the $`{𝐏}_i^- - {𝐏}_i^+`$ is non-negative definite. The same argument can be made from the viewpoint of comparing the trace (or the matrix norm) of the *a posteriori* and *a priori* state estimation error covariances. As each new measurement is processed by the EKF, we expect the uncertainty in the estimation error to decrease. The question is, does the *a posteriori* uncertainty as computed by the EKF represent the actual uncertainty, or in other words, is the state estimation error covariance matrix always consistent with the actual state errors? In the nonlinear setting when there is a large *a priori* uncertainty in the state estimate and a very accurate measurement, it can happen that the state estimation error covariance reduction at the measurement update is too large. Underweighting is a method to address this situation by limiting the magnitude of the state estimation error covariance update with the goal of retaining consistency of the filter covariance and the actual state estimation error through situations of high nonlinearity of the measurements.

Pre- and post-multiplying the *a posteriori* state estimation error covariance in Eq. [\(5.12\)](#page-66-4) by $`{𝐇}_i`$ and $`{𝐇}_i^{\top}`$, respectively, yields (after some manipulation)

<span id="page-67-1"></span>

```math
{𝐇}_i {𝐏}_i^+ {𝐇}_i^{\top} = {𝐇}_i {𝐏}_i^- {𝐇}_i^{\top}({𝐇}_i {𝐏}_i^- {𝐇}_i^{\top} + {𝐑}_i)^{-1}{𝐑}_i\,. \qquad\qquad(5.22)
```

In Eq. [\(5.22\)](#page-67-1), we see that if $`{𝐇}_i {𝐏}_i^- {𝐇}_i^{\top} \gg {𝐑}_i`$ then it follows that

<span id="page-67-2"></span>

```math
{𝐇}_i {𝐏}_i^+ {𝐇}_i^{\top} \simeq {𝐑}_i\,. \qquad\qquad(5.23)
```

The result in Eq. [\(5.23\)](#page-67-2) is of fundamental importance and is the motivation behind underweighting. What this equation express is the fact that when the *a priori* estimated state uncertainty $`{𝐇}_i {𝐏}_i^- {𝐇}_i^{\top}`$ is much larger than the measurement error covariance $`{𝐑}_i`$, the Kalman filter largely neglects the prior information and relies heavily on the measurement. Therefore the *a posteriori* estimated state uncertainty $`{𝐇}_i {𝐏}_i^+ {𝐇}_i^{\top}`$ is approximately equal to $`{𝐑}_i`$.

### <span id="page-68-2"></span>5.2.3. The Nonlinear Measurement Model and the 2nd-Order Kalman Filter Update

Whereas Eq. [\(5.14\)](#page-66-5) truncates the Taylor series expansion of the nonlinear measurement function to first order, carrying it to second order we obtain

```math
{𝒚}_i \simeq {𝒉}(\hat{{𝒙}}_i^-, t_i) + {𝐇}_i\,{𝒆}_i^- + \sum_{k=1}^{m}\biggl(\frac{\partial^2 {𝒉}({𝒙}_i, t_i)}{\partial {𝒙}_i \partial x_i(k)}\biggr|_{{𝒙}_i = \hat{{𝒙}}_i^-} e_i(k)\,{𝒆}_i\biggr) + {𝒗}_i \qquad\qquad(5.24)
```

```math
= {𝒉}(\hat{{𝒙}}_i^-, t_i) + {𝐇}_i\,{𝒆}_i^- + {𝒃}_i + {𝒗}_i\,, \qquad\qquad(5.25)
```

where $`e_i(k)`$ and $`x_i(k)`$ are the $`k`$-th elements of vectors $`{𝒆}_i`$ and $`{𝒙}_i`$, respectively. The expected value of the measurement now includes contributions from the second order terms, denoted as $`\hat{{𝒃}}_i`$

```math
\mathrm{E}[{𝒚}_i] \simeq {𝒉}(\hat{{𝒙}}_i^-, t_i) + \hat{{𝒃}}_i \qquad\qquad(5.26)
```

Define

```math
{𝐇}_{i,k}^{\top} \triangleq \biggl[\frac{\partial^2 h_i({𝒙}_i)}{\partial {𝒙}_i \partial {𝒙}_i^{\top}}\biggr|_{{𝒙}_i = \hat{{𝒙}}_i^-}\biggr],
```

where $`h_i({𝒙}_i)`$ is the $`k`$-th component of $`{𝒉}({𝒙}_i)`$. Then the $`k`$-th component of $`{𝒃}_i`$ is given by

```math
b_{i,k} = \frac{1}{2}\,({𝒆}_i^-)^{\top}{𝐇}_{i,k}^{\top}{𝒆}_i^- = \frac{1}{2}\;\mathop{\mathrm{tr}}({𝐇}_{i,k}^{\top}{𝒆}_i^-({𝒆}_i^-)^{\top})\,. \qquad\qquad(5.27)
```

where $`\mathop{\mathrm{tr}}`$ denotes the trace. To keep the filter unbiased, the $`k`$-th component of $`\hat{{𝒃}}_i`$ is given by

```math
\hat{b}_{i,k} = 1/2\,\mathop{\mathrm{tr}}({𝐇}_{i,k}^{\top}{𝐏}_i^-)\,.
```

The measurement residual is

<span id="page-68-0"></span>

```math
{𝒓}_i = {𝒚}_i - \mathrm{E}[{𝒚}_i] \qquad\qquad(5.28)
```

Expanding Eq. [\(5.28\)](#page-68-0), the $`k`$-th component of the residual is obtained to be

```math
r_{i,k} = {𝒉}_{i,k}^{\top}\,{𝒆}_i^- + 1/2\,\mathop{\mathrm{tr}}({𝐇}_i^{\top}(t_i){𝒆}_i^-({𝒆}_i^-)^{\top}) - 1/2\,\mathop{\mathrm{tr}}({𝐇}_i^{\top}(t_i){𝐏}_i^-) + v_{i,k}\,, \qquad\qquad(5.29)
```

where $`{𝒉}_{i,k}^{\top}`$ is the $`ik`$-th row of the measurement Jacobian and $`v_{i,k}`$ is the $`k`$-th component of the measurement noise $`{𝒗}_i`$. Computing the measurement residual covariance $`\mathrm{E}[{𝒓}_i {𝒓}_i^{\top}]`$ yields

<span id="page-68-1"></span>

```math
{𝐖}_i = {𝐇}_i {𝐏}_i^- {𝐇}_i^{\top} + {𝐁}_i + {𝐑}_i\,, \qquad\qquad(5.30)
```

where matrix $`{𝐁}_i`$ is the contribution of the second order effects and its $`(kj)`$-th component is given by

```math
\begin{aligned} B_{i,kj} \triangleq{} & 1/4\,\mathrm{E}\big[\mathop{\mathrm{tr}}({𝐇}_i^{\top}(t_i){𝒆}_i^-({𝒆}_i^-)^{\top})\;\mathop{\mathrm{tr}}({𝐇}_i^{\top}(t_i){𝒆}_i^-({𝒆}_i^-)^{\top})\big] \\ & - 1/4\;\mathop{\mathrm{tr}}({𝐇}_i^{\top}(t_i){𝐏}_i^-)\;\mathop{\mathrm{tr}}({𝐇}_i^{\top}(t_i){𝐏}_i^-)\,. \end{aligned}
```

where it was assumed that the third order central moments are all zeros. Assuming the prior estimation error is distributed as a zero-mean gaussian distribution with covariance $`{𝐏}_i^-`$, the $`ij^{th}`$ component of $`{𝐁}_i`$ is given by

```math
B_{i,kj} = \frac{1}{2}\mathop{\mathrm{tr}}({𝐇}_{i,k}^{\top}\,{𝐏}_i^-\,{𝐇}_{i,j}^{\top}\,{𝐏}_i^-)\,. \qquad\qquad(5.31)
```

Comparing the measurement residual covariance for the EKF in Eq. [\(5.19\)](#page-67-3) with the measurement residual covariance for the second-order filter in Eq. [\(5.30\)](#page-68-1), we see that when the nonlinearities lead to significant second-order terms which should not be neglected, then the EKF tends to provide residual covariance estimates that are not consistent with the actual errors. Typically, we address this by tuning the EKF using $`{𝐑}_i`$ as a parameter to be tweaked. If the contribution of the *a priori* estimation error $`{𝐇}_i {𝐏}_i^- {𝐇}_i^{\top}`$ to the residuals covariance is much larger than the contribution of the measurement error $`{𝐑}_i`$, the EKF algorithm will produce $`{𝐇}_i {𝐏}_i^+ {𝐇}_i^{\top} \simeq {𝐑}_i`$. If $`{𝐁}_i`$ is of comparable magnitude to $`{𝐑}_i`$ then the actual covariance of the posterior measurement estimate should be $`{𝐇}_i {𝐏}_i^+ {𝐇}_i^{\top} \simeq {𝐑}_i + {𝐁}_i`$. Therefore, a large underestimation of the *a posteriori* covariance can occur in the presence of nonlinearities when the estimated measurement error covariance is much larger than the measurement error covariance.

The covariance update is given by the modified Gaussian second order filter update [[38](16-bibliography.md#page-171-0)]

```math
{𝐏}_i^+ = {𝐏}_i^- - {𝐇}_i {𝐏}_i^- {𝐖}_i^{-1}\Bigl({𝐇}_i {𝐏}_i^-\Bigr)^{\top}, \qquad\qquad(5.32)
```

where the residual covariance $`{𝐖}_i`$ is given by Eq. [\(5.30\)](#page-68-1).

## 5.3. Underweighting Measurements

<span id="page-69-0"></span>In the prior section we saw that when "large" values of $`{𝐇}_i {𝐏}_i^- {𝐇}_i^{\top}`$ exist (or similarly, large values of $`{𝐏}_i^-`$), and possibly "small" values of $`{𝐑}_i`$, the EKF is at risk underestimating the posterior estimation error covariance matrix. We must repeat that this can only happen in the presence of "large" nonlinearities. The larger $`{𝐏}_i^-`$ is, the larger the domain of possible values of the true state $`{𝒙}`$, hence the more likely the higher order terms of the expansion of the nonlinear measurement functions will become relevant. If a measurement function is largely non-linear, but the prior estimate is very precise, the EKF algorithm and linearization are likely sufficiently accurate since:

- (1) The posterior measurement will rely heavily on the prior and rely less on the measurement
- (2) Since the error is small, while the Hessian matrix might be relatively large, the actual contributions of the second order effects is likely to remain small

Underweighting is the process of modifying the residual covariance to reduce the update and compensate for the second-order effects described above. In this section, we describe three common methods for performing underweighting with the EKF algorithm.

### 5.3.1. Additive Compensation Method

The most straightforward underweighting scheme is to add an underweighting factor $`{𝐔}_i`$ as

```math
{𝑾}_i = {𝐇}_i {𝐏}_i^- {𝐇}_i^{\top} + {𝐑}_i + {𝐔}_i\,. \qquad\qquad(5.33)
```

With the Kalman gain given by

```math
{𝐊}_i = {𝐏}_i^- {𝐇}_i^{\top} {𝑾}_i^{-1}\,, \qquad\qquad(5.34)
```

we see that the symmetric, positive-definite underweighting factor $`{𝐔}_i`$ decreases the Kalman gain, thereby reducing the state estimate and state estimation error covariance updates. One choice is to select $`{𝐔}_i = {𝐁}_i`$, which is the contribution to the covariance assuming the prior distribution of the estimation error is Gaussian. The advantage of this choice is its theoretical foundation based on analyzing the second-order terms of the Taylor series expansions. The disadvantages include higher computational costs to calculate the second-order partials and the reliance on the assumption that the estimation errors possess Gaussian distributions. In practical applications, the matrix $`{𝐔}_i`$ needs to be tuned appropriately for acceptable overall performance of the EKF. The process of tuning a positive definite matrix is less obvious than tuning a single scalar parameter.

### 5.3.2. Scaling the Measurement Error Covariance

Another possible underweighting approach is to scale the measurement noise by choosing

```math
{𝐔}_i = \gamma {𝐑}_i\,, \qquad\qquad(5.35)
```

where $`\gamma \gt 0`$ is a scalar parameter selected in the design process. This approach has been successfully used [[39](16-bibliography.md#page-171-13)]; however, it is not recommended from both a conceptual and a practical reason. Recalling that the underweighting is necessary because of neglecting the second-order terms of the Taylor series expansion of the measurement function, it seems more natural to express the underweighting as a function of the *a priori* estimation error covariance. Choosing a constant coefficient to scale $`{𝐑}_i`$ seems less practical and will probably lead to a more complicated tuning procedure. As long as the measurement noise is white the contributions of the second order effects are not a function of the measurement error covariance, therefore making them a fraction or a multiple of the measurement noise (an unrelated quantity) is likely not the best choice.

### 5.3.3. Lear's Method

Lear's choice was to make $`{𝐔}_i`$ a percentage of the *a priori* estimation error covariance via [[48](16-bibliography.md#page-171-10)]

```math
{𝐔}_i = \beta {𝐇}_i {𝐏}_i^- {𝐇}_i^{\top}\,. \qquad\qquad(5.36)
```

Let $`\bar{{𝐏}}_i^- \in {ℝ}^{3 \times 3}`$ be the partition of the state estimation error covariance associated with the position error states. The Space Shuttle employs underweighting when $`\sqrt{\mathop{\mathrm{tr}}\bar{{𝐏}}_i^-} \gt \alpha`$. The positive scalars $`\alpha`$ and $`\beta`$ are design parameters. For the Space Shuttle, $`\alpha`$ is selected to be 1000 meters and $`\beta`$ is selected to be $`0.2`$ [[48](16-bibliography.md#page-171-10)]. When $`\sqrt{\mathop{\mathrm{tr}}\bar{{𝐏}}_i^-} \gt 1000`$ m, then $`\beta = 0.2`$, otherwise $`\beta = 0`$.

Orion employs a slightly different approach, underweighting is applied when $`{𝐇}_i {𝐏}_i^- {𝐇}_i^{\top} \gt \alpha`$, where $`\alpha`$ is a tunable flight software parameter.

This choice of underweighting scheme is sound since it assumes that the higher order effects are a fraction (or a multiple) of the first order effects, which are a related quantity. There may exist some unusual nonlinear measurement cases where the measurement Jacobian evaluates to zero, or a small value, while at the same time the Hessian does not vanish; these cases are not appropriately handled by underweighting.

## 5.4. Pre-Flight Tuning Aids

<span id="page-70-0"></span>In this section, a technique to aid the tuning of the underweighting coefficient during pre-flight analysis is presented. When the nonlinearities lead to second-order terms that cannot be neglected, we find that the measurement residual covariance is more accurately given by (see Eq. [\(5.30\)](#page-68-1))

<span id="page-70-1"></span>

```math
{𝐖}_i = {𝐇}_i {𝐏}_i^- {𝐇}_i^{\top} + {𝐑}_i + {𝐁}_i\,. \qquad\qquad(5.37)
```

Following Lear's approach to underweighting, we have that

<span id="page-70-2"></span>

```math
{𝐖}_{U,i} = (1 + \beta){𝐇}_i {𝐏}_i^- {𝐇}_i^{\top} + {𝐑}_i\,. \qquad\qquad(5.38)
```

Comparing Eqs. [\(5.37\)](#page-70-1) and [\(5.38\)](#page-70-2), the desired effect is to have

```math
\mathop{\mathrm{tr}}{𝐖}_{U,i} \geq \mathop{\mathrm{tr}}{𝐖}_i\,. \qquad\qquad(5.39)
```

This leads us to choose the underweighting coefficient $`\beta_i`$ such that

```math
\beta \geq \mathop{\mathrm{tr}}{𝐁}_i / \mathop{\mathrm{tr}}{𝐇}_i {𝐏}_i^- {𝐇}_i^{\top} \qquad \forall i. \qquad\qquad(5.40)
```

The designer can run simulations before the flight and calculate the time history of $`\mathop{\mathrm{tr}}{𝐁}_i / \mathop{\mathrm{tr}}{𝐇}_i {𝐏}_i^- {𝐇}_i^{\top}`$ and choose an appropriate value of $`\beta`$. It is unlikely that higher order terms than $`{𝐁}_i`$ will need to be considered in designing the value of $`\beta`$.

---

[← Chapter 4. Processing Measurements](04-processing-measurements.md) · [Contents](README.md) · [Chapter 6. Bias Modeling (part 1 of 2) →](06-bias-modeling-part1.md)
