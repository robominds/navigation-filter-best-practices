[← Chapter 11. Smoothing](11-smoothing.md) · [Contents](README.md) · [Appendix A. Models and Realizations of Random Variables →](13-appendix-a-models-and-realizations-of-random-variables.md)

# Chapter 12. Advanced Estimation Algorithms

<span id="page-140-0"></span>This chapter will describe advanced estimation algorithms that have yet to achieve the status of best practices, but which appear to the contributors to have good potential for someday reaching such status.

## <span id="page-140-1"></span>The Sigma-Point Estimator

*Contributed by J. Russell Carpenter*

Derivative-free state estimation techniques have received increasing attention in recent years. A particular class of such estimators make use of the columns of the factors of the estimators' error covariance matrices, which are scaled to form vectors that have become generally known as "sigma points." The so-called "Unscented Kalman Filter" [[41](16-bibliography.md#page-171-25), [42](16-bibliography.md#page-171-26), [52](16-bibliography.md#page-172-21)] is a particular example of a sigma-point filter. A more general form is the divided-difference sigma-point filter, which is a sequential estimator that replaces first-order truncations of Taylor series approximations with second-order numerical differencing equations to approximate nonlinear dynamics and measurement models [[64](16-bibliography.md#page-172-22), [65](16-bibliography.md#page-172-23)]. If the process and measurement noise enter the system additively, Lee and Alfriend showed that several simplifications are possible, including a substantial reduction in the number of sigma-points [[51](16-bibliography.md#page-172-24)]. They refer to this construction as the Additive Divided Difference Sigma-Point Filter (ADDSPF).

This section highlights some broad aspects of sigma-point filtering, then briefly reviews how the ADDSPF works. It concludes with some brief comments comparing the ADDSPF to other sequential filters.

### The Sigma-Point Filter

In its most general form, the sigma-point filter performs sequential estimation of the $`n`$-dimensional state, $`{𝐱}`$, whose nonlinear dynamics over the time interval $`[t_k, t_{k+1}]`$ are given by

```math
{𝐱}_{k+1} = {𝐟}({𝐱}_k, {𝐰}_k) \qquad\qquad(12.1)
```

The process noise input, $`{𝐰}`$, consists of independent increments whose first two moments are $`\mathrm{E}[{𝐰}_k] = {𝟎}`$ and $`\mathrm{E}[{𝐰}_k {𝐰}_\ell] = {𝐐}_k \delta_{k\ell}`$, where $`\delta_{k\ell}`$ is the Kronecker delta. Although the second moment may be a function of the time index, this estimator assumes that all of the samples of $`{𝐰}`$ arise from the same type of distribution, and this work further assumes that this distribution is Gaussian, so that higher-order moments may be neglected.

The filter sequentially processes an ordered set of measurements, $`{𝕐}_k = [{𝐲}_0, {𝐲}_1, \ldots, {𝐲}_k]`$ of the form

```math
{𝐲}_k = {𝐡}({𝐱}_k, {𝐯}_k) \qquad\qquad(12.2)
```

where the measurement noise input, $`{𝐯}`$, consists of independent and identically distributed (again, in this work, Gaussian) increments whose first two moments are $`\mathrm{E}[{𝐯}_k] = {𝟎}`$ and $`\mathrm{E}[{𝐯}_k {𝐯}_\ell] = {𝐑}_k \delta_{k\ell}`$.

By contrast, the ADDSPF utilizes models where the noise sources enter additively:

```math
{𝐱}_{k+1} = {𝐟}({𝐱}_k) + {𝐠}({𝐱}_k){𝐰}_k \qquad\qquad(12.3)
```

and

```math
{𝐲}_k = {𝐡}({𝐱}_k) + {𝐯}_k. \qquad\qquad(12.4)
```

All sigma-point filters utilize a linear measurement update equation of the form

<span id="page-141-0"></span>
```math
\hat{{𝐱}}_k^+ = \hat{{𝐱}}_k^- + {𝐊}_k \Bigl( {𝐲}_k - \hat{{𝐲}}_k^- \Bigr) \qquad\qquad(12.5)
```

where the accented variables in Eq. [\(12.5\)](#page-141-0) denote conditional expectations, as in the Kalman filter:

```math
\hat{{𝐱}}_k^+ = \mathrm{E}[{𝐱}_k \vert {𝕐}_k] \qquad\qquad(12.6)
```

```math
\hat{{𝐱}}_k^- = \mathrm{E}[{𝐱}_k \vert {𝕐}_{k-1}] \qquad\qquad(12.7)
```

```math
\hat{{𝐲}}_k^- = \mathrm{E}[{𝐲}_k \vert {𝕐}_{k-1}] \qquad\qquad(12.8)
```

The gain matrix, $`{𝐊}`$, is based on conditional covariances, as in the Kalman filter:

<span id="page-141-1"></span>
```math
{𝐊}_k = {𝐏}_{xy_k}^- \Bigl( {𝐏}_{yy_k}^- \Bigr)^{-1} \qquad\qquad(12.9)
```

```math
{𝐏}_k^- = {𝐏}_{xx_k}^- = \mathrm{E}\Big[ \Bigl( {𝐱}_k - \hat{{𝐱}}_k^- \Bigr) \Bigl( {𝐱}_k - \hat{{𝐱}}_k^- \Bigr)^{{𝖳}} \vert {𝕐}_{k-1} \Big] \qquad\qquad(12.10)
```

```math
{𝐏}_{xy_k}^- = \mathrm{E}\Big[ \Bigl( {𝐱}_k - \hat{{𝐱}}_k^- \Bigr) \Bigl( {𝐲}_k - \hat{{𝐲}}_k^- \Bigr)^{{𝖳}} \vert {𝕐}_{k-1} \Big] \qquad\qquad(12.11)
```

```math
{𝐏}_{yy_k}^- = \mathrm{E}\Big[ \Bigl( {𝐲}_k - \hat{{𝐲}}_k^- \Bigr) \Bigl( {𝐲}_k - \hat{{𝐲}}_k^- \Bigr)^{{𝖳}} \vert {𝕐}_{k-1} \Big] \qquad\qquad(12.12)
```

```math
\, \qquad\qquad(12.13)
```

and the covariance associated with state estimate $`\hat{{𝐱}}_k^+`$ is

```math
{𝐏}_k^+ = {𝐏}_{xx_k}^+ = \mathrm{E}\Big[ \Bigl( {𝐱}_k - \hat{{𝐱}}_k^+ \Bigr) \Bigl( {𝐱}_k - \hat{{𝐱}}_k^+ \Bigr)^{{𝖳}} \vert {𝕐}_k \Big] \qquad\qquad(12.14)
```

Hereafter, equations will suppress the time index if it is the same for all variables in the equation.

Estimators such as the Kalman filter estimate these conditional expectations by approximating the nonlinear functions $`{𝐟}`$ and $`{𝐡}`$ with first-order Taylor series truncations, e.g.:

```math
{𝐟}({𝐱}) \approx {𝐟}(\hat{{𝐱}}^-) + {𝐟}'({𝐱})({𝐱} - \hat{{𝐱}}^-) \qquad\qquad(12.15)
```

where $`{𝐟}'`$ is an exact gradient. By contrast, the divided difference filter uses a second-order truncation along with numerical differencing formulas for the derivatives:

```math
{𝐟}({𝐱}) \approx {𝐟}(\hat{{𝐱}}^-) + \tilde{\mathrm{D}}_{\Delta {𝐱}}^{(1)} {𝐟}(\hat{{𝐱}}^-) + \tilde{\mathrm{D}}_{\Delta {𝐱}}^{(2)} {𝐟}(\hat{{𝐱}}^-) \qquad\qquad(12.16)
```

where the divided difference operators, $`\tilde{\mathrm{D}}_{\Delta {𝐱}}^{(i)} {𝐟}(\hat{{𝐱}}^-)`$, approximate the coefficients of the multidimensional Taylor series expansion using Stirling interpolations. These interpolators difference perturbations of $`{𝐟}(\hat{{𝐱}}^-)`$ across a (dimensionless) interval, $`h`$, over a spanning basis set. Whether they are first-order, such as the unscented filter, or second order, sigma-point filters choose the interval so as to better approximate the moments required for the gain calculation, and choose as the spanning basis a set of sigma points, which are derived from $`\hat{{𝐱}}^-`$ and the columns of the Cholesky factors of $`{𝐏}^-`$ as follows.

### The ADDSPF

Let $`\hat{{𝒳}}`$ denote the array whose columns are a particular ordering of the sigma points derived from $`\hat{{𝐱}}`$ and its corresponding covariance, $`{𝐏}`$. Then

```math
\hat{{𝒳}} = \Big[ \hat{{𝐱}},\ \hat{{𝐱}} + h\, {}^{c}\!\sqrt{{𝐏}}_{(:,1)},\ \hat{{𝐱}} + h\, {}^{c}\!\sqrt{{𝐏}}_{(:,2)}, \ldots, \hat{{𝐱}} - h\, {}^{c}\!\sqrt{{𝐏}}_{(:,1)}, \hat{{𝐱}} - h\, {}^{c}\!\sqrt{{𝐏}}_{(:,2)}, \ldots \Big] \qquad\qquad(12.17)
```

where the subscript $`(:, i)`$ denotes column $`i`$ of the corresponding array, and $`{𝐏} = {}^{c}\!\sqrt{{𝐏}}\, {}^{c}\!\sqrt{{𝐏}}^{{𝖳}}`$ denotes a Cholesky factorization. In the sequel, the shorthand notation $`\hat{{𝐱}} \pm h\, {}^{c}\!\sqrt{{𝐏}}`$ will denote the array on the right-hand side of the equation above. Then, for the ADDSPF, Ref. [51](16-bibliography.md#page-172-24) shows that as each new measurement becomes available, an array of sigma points generated from the prior update should be propagated to the new measurement time:

```math
\hat{{𝒳}}_k^- = {𝐟}(\hat{{𝒳}}_{k-1}^+) \qquad\qquad(12.18)
```

These propagated sigma points are then merged to form the state estimate just prior to incorporating the new measurement as follows:

```math
\hat{{𝐱}}^- = \mu_h(\hat{{𝒳}}^-) = \frac{h^2 - n}{h^2} \hat{{𝒳}}_{(:,1)}^- + \frac{1}{2h^2} \sum_{i=2}^{2n+1} \hat{{𝒳}}_{(:,i)}^- \qquad\qquad(12.19)
```

To form an associated covariance, the following divided-differences are next computed:

```math
\tilde{\mathrm{D}}_{\Delta {𝐱}}^{(1)} {𝐟}(\hat{{𝐱}}^-)_{(:,i)} = \frac{1}{2h} \Bigl[ \hat{{𝒳}}_{(:,i+1)}^- - \hat{{𝒳}}_{(:,i+1+n)}^- \Bigr] \qquad\qquad(12.20)
```

```math
\tilde{\mathrm{D}}_{\Delta {𝐱}}^{(2)} {𝐟}(\hat{{𝐱}}^-)_{(:,i)} = \frac{\sqrt{h^2-1}}{2h^2} \Bigl[ \hat{{𝒳}}_{(:,i+1)}^- + \hat{{𝒳}}_{(:,i+1+n)}^- - 2\hat{{𝒳}}_{(:,1)}^- \Bigr] \qquad\qquad(12.21)
```

Ref. [51](16-bibliography.md#page-172-24) shows that the covariance may then be computed from

<span id="page-142-0"></span>
```math
{𝐏}^- = \Bigl[ \tilde{\mathrm{D}}_{\Delta {𝐱}}^{(1)} {𝐟}(\hat{{𝐱}}^-),\, \tilde{\mathrm{D}}_{\Delta {𝐱}}^{(2)} {𝐟}(\hat{{𝐱}}^-),\ {}^{c}\!\sqrt{{𝐐}_d} \Bigr] \Bigl[ \tilde{\mathrm{D}}_{\Delta {𝐱}}^{(1)} {𝐟}(\hat{{𝐱}}^-),\, \tilde{\mathrm{D}}_{\Delta {𝐱}}^{(2)} {𝐟}(\hat{{𝐱}}^-),\ {}^{c}\!\sqrt{{𝐐}_d} \Bigr]^{{𝖳}} \qquad\qquad(12.22)
```

One advantage of sigma-point filters is that the full covariance need not be maintained, but rather only its Cholesky factor. Although the factors in square brackets in Eq. [\(12.22\)](#page-142-0) are not Cholesky factors, since each is a full $`n \times 3n`$ matrix, one may extract an $`n \times n`$ triangular factor from it using the so-called "thin" version [[30](16-bibliography.md#page-171-27)] of the QR decomposition[<sup>1</sup>](#page-142-1), or alternatively using a Householder factorization [[5](16-bibliography.md#page-170-1)]. Thus,

```math
{𝐌} \begin{bmatrix} {}^{c}\!\sqrt{{𝐏}^-}^{{𝖳}} \\ {𝐎}_{2n \times n} \end{bmatrix} = \Bigl[ \tilde{\mathrm{D}}_{\Delta {𝐱}}^{(1)} {𝐟}(\hat{{𝐱}}^-),\, \tilde{\mathrm{D}}_{\Delta {𝐱}}^{(2)} {𝐟}(\hat{{𝐱}}^-),\ {}^{c}\!\sqrt{{𝐐}_d} \Bigr]^{{𝖳}} \qquad\qquad(12.23)
```

where $`{𝐌}`$ is a full $`3n \times 3n`$ orthonormal matrix, and $`{𝐎}_{2n \times n}`$ is a $`2n \times n`$ matrix of zeros.

<span id="page-142-1"></span><sup>1</sup> For *Matlab* users, this may be accomplished in several ways, e.g. by passing the transpose of this matrix to the `qr` function, then keeping the first $`n`$ non-zero rows from the second output, and transposing this result.

For the measurement update, a new array of sigma points must be generated from $`\hat{{𝐱}}^-`$ and $`{𝐏}^-`$; this array is denoted $`\hat{{𝒳}}^*`$. These sigma points are used to generate a set of sigma points representing the measurement:

```math
\hat{{𝒴}}^- = {𝐡}(\hat{{𝒳}}^*) \qquad\qquad(12.24)
```

In similar fashion to the time update, the sigma points of the measurement are then merged to form the estimated measurement:

```math
\hat{{𝐲}}^- = \mu_h(\hat{{𝒴}}^-) \qquad\qquad(12.25)
```

the corresponding divided-differences are computed as:

```math
\tilde{\mathrm{D}}_{\Delta {𝐱}}^{(1)} {𝐡}(\hat{{𝐱}}^-)_{(:,i)} = \frac{1}{2h} \Bigl[ \hat{{𝒴}}_{(:,i+1)}^- - \hat{{𝒴}}_{(:,i+1+n)}^- \Bigr] \qquad\qquad(12.26)
```

```math
\tilde{\mathrm{D}}_{\Delta {𝐱}}^{(2)} {𝐡}(\hat{{𝐱}}^-)_{(:,i)} = \frac{\sqrt{h^2 - 1}}{2h^2} \Bigl[ \hat{{𝒴}}_{(:,i+1)}^- + \hat{{𝒴}}_{(:,i+1+n)}^- - 2\hat{{𝒴}}_{(:,1)}^- \Bigr] \qquad\qquad(12.27)
```

and the covariances required for the gain calculation may then be computed from

```math
{𝐏}_{yy}^- = \Bigl[ \tilde{\mathrm{D}}_{\Delta {𝐱}}^{(1)} {𝐡}(\hat{{𝐱}}^-),\, \tilde{\mathrm{D}}_{\Delta {𝐱}}^{(2)} {𝐡}(\hat{{𝐱}}^-),\ {}^{c}\!\sqrt{{𝐑}} \Bigr] \Bigl[ \tilde{\mathrm{D}}_{\Delta {𝐱}}^{(1)} {𝐡}(\hat{{𝐱}}^-),\, \tilde{\mathrm{D}}_{\Delta {𝐱}}^{(2)} {𝐡}(\hat{{𝐱}}^-),\ {}^{c}\!\sqrt{{𝐑}} \Bigr]^{{𝖳}} \qquad\qquad(12.28)
```

```math
{𝐏}_{xy}^- = {}^{c}\!\sqrt{{𝐏}^-} \Bigl[ \tilde{\mathrm{D}}_{\Delta {𝐱}}^{(1)} {𝐡}(\hat{{𝐱}}^-) \Bigr]^{{𝖳}} \qquad\qquad(12.29)
```

Note that the second-order divided difference for the measurement function, $`\tilde{\mathrm{D}}_{\Delta {𝐱}}^{(2)} {𝐡}(\hat{{𝐱}}^-)`$, does *not* appear in the cross-covariance update. As with the time update, through the use of the thin QR factorization, only triangular factors need be maintained for $`{𝐏}_{yy}^-`$[<sup>2</sup>](#page-143-0):

```math
{𝐌}_{yy} \begin{bmatrix} {}^{c}\!\sqrt{{𝐏}_{yy}^-}^{{𝖳}} \\ {𝐎}_{2n \times n} \end{bmatrix} = \Bigl[ \tilde{\mathrm{D}}_{\Delta {𝐱}}^{(1)} {𝐡}(\hat{{𝐱}}^-),\, \tilde{\mathrm{D}}_{\Delta {𝐱}}^{(2)} {𝐡}(\hat{{𝐱}}^-),\ {}^{c}\!\sqrt{{𝐑}} \Bigr]^{{𝖳}} \qquad\qquad(12.30)
```

<span id="page-143-0"></span><sup>2</sup> Although it might seem that the full matrix $`{𝐏}_{yy}^-`$ is required for the gain computation of Eq. [\(12.9\)](#page-141-1), Ref. [64](16-bibliography.md#page-172-22) points out that, rather than inverting the product of the factors to compute the gain, the gain may be solved from forward and back substitution directly using the Cholesky factor.

Now, all of the terms required for the state update (Eqs. [12.5](#page-141-0) and [12.9\)](#page-141-1), are available. Ref. [51](16-bibliography.md#page-172-24) shows that the corresponding Cholesky factor of the covariance is extracted from

```math
{𝐌}^+ \begin{bmatrix} {}^{c}\!\sqrt{{𝐏}^+}^{{𝖳}} \\ {𝐎}_{2n \times n} \end{bmatrix} = \Big[ {}^{c}\!\sqrt{{𝐏}^-} - {𝐊} \tilde{\mathrm{D}}_{\Delta {𝐱}}^{(1)} {𝐡}(\hat{{𝐱}}^-),\ {𝐊} \Bigl[ \tilde{\mathrm{D}}_{\Delta {𝐱}}^{(2)} {𝐡}(\hat{{𝐱}}^-),\ {}^{c}\!\sqrt{{𝐑}} \Bigr] \Big] \qquad\qquad(12.31)
```

### The ADDSPF vs. Other Sequential Filters

To conclude this section, some observations concerning the ADDSPF in comparison to other filters are offered. These observations concern the number of sigma points, the order of approximation, and the existence and method of choice of free parameters in the algorithms.

Although in many problems of practical interest the noise enters the system additively, if this is not the case, then either the original divided difference filter or the unscented filter may provide superior results to the ADDSPF, at the cost of requiring more sigma points. In both of the former algorithms, the nonlinear functions must be perturbed not only over a basis spanning the state space, but also over the discrete process noise and measurement noise spaces. Thus, rather than $`2n + 1`$ sigma points, the more general algorithms require $`2n_a + 1`$, where $`n_a = n + n_w + n_v`$, and $`n_w`$ and $`n_v`$ are the dimensions of the discrete process noise and measurement noise inputs.

The Kalman filter is an exact algorithm for linear stochastic systems driven by Gaussian noise, and nothing is to be gained from the use the sigma-point filters for such purely linear systems. First-order sigma-point filters such as the UKF retain the Kalman filter's first-order truncation, but avoid the need for the designer to supply explicit gradients. The divided difference filter is comparable to a derivative-free version of the modified second-order Gaussian filter [[38](16-bibliography.md#page-171-0)] in that, for symmetric distributions, it retains some terms as high as order four.

Unlike the Kalman filter, for which all of the parameters in principle can be associated with properties of the underlying stochastic system, all of the sigma point filters involve at least one free parameter. In the unscented filter, the weights for combining the sigma points involve three parameters whose physical interpretation is perhaps less clear than with the single parameter in the divided difference algorithms, where the free parameter $`h`$ is clearly associated with the size of the perturbation in the numerical differencing formulae. Ref. [64](16-bibliography.md#page-172-22) shows that $`h`$ should be bounded below by $`h \gt 1`$, and that for symmetric distributions, $`\sqrt{h}`$ should be equal to the kurtosis, which for a Gaussian distribution is three[<sup>3</sup>](#page-144-0).

<span id="page-144-0"></span><sup>3</sup> Some authors subtract three from the definition of kurtosis, so that Gaussian distributions have zero kurtosis.

---

[← Chapter 11. Smoothing](11-smoothing.md) · [Contents](README.md) · [Appendix A. Models and Realizations of Random Variables →](13-appendix-a-models-and-realizations-of-random-variables.md)
