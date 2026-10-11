[← Chapter 11. Smoothing](11-smoothing.md) · [Contents](README.md) · [Appendix A. Models and Realizations of Random Variables →](13-appendix-a-models-and-realizations-of-random-variables.md)

# Chapter 12. Advanced Estimation Algorithms

<span id="page-140-0"></span>This chapter will describe advanced estimation algorithms that have yet to achieve the status of best practices, but which appear to the contributors to have good potential for someday reaching such status.

## <span id="page-140-1"></span>The Sigma-Point Estimator

*Contributed by J. Russell Carpenter*

Derivative-free state estimation techniques have received increasing attention in recent years. A particular class of such estimators make use of the columns of the factors of the estimators' error covariance matrices, which are scaled to form vectors that have become generally known as "sigma points." The so-called "Unscented Kalman Filter" [[41](16-bibliography.md#page-171-25), [42](16-bibliography.md#page-171-26), [52](16-bibliography.md#page-172-21)] is a particular example of a sigma-point filter. A more general form is the divided-difference sigma-point filter, which is a sequential estimator that replaces first-order truncations of Taylor series approximations with second-order numerical differencing equations to approximate nonlinear dynamics and measurement models [[64](16-bibliography.md#page-172-22), [65](16-bibliography.md#page-172-23)]. If the process and measurement noise enter the system additively, Lee and Alfriend showed that several simplifications are possible, including a substantial reduction in the number of sigma-points [[51](16-bibliography.md#page-172-24)]. They refer to this construction as the Additive Divided Difference Sigma-Point Filter (ADDSPF).

This section highlights some broad aspects of sigma-point filtering, then briefly reviews how the ADDSPF works. It concludes with some brief comments comparing the ADDSPF to other sequential filters.

### The Sigma-Point Filter

In its most general form, the sigma-point filter performs sequential estimation of the $n$-dimensional state, $\mathbf{x}$, whose nonlinear dynamics over the time interval $[t_k, t_{k+1}]$ are given by

$$
\mathbf{x}_{k+1} = \mathbf{f}(\mathbf{x}_k, \mathbf{w}_k) \tag{12.1}
$$

The process noise input, $\mathbf{w}$, consists of independent increments whose first two moments are $\mathrm{E}[\mathbf{w}_k] = \mathbf{0}$ and $\mathrm{E}[\mathbf{w}_k \mathbf{w}_\ell] = \mathbf{Q}_k \delta_{k\ell}$, where $\delta_{k\ell}$ is the Kronecker delta. Although the second moment may be a function of the time index, this estimator assumes that all of the samples of $\mathbf{w}$ arise from the same type of distribution, and this work further assumes that this distribution is Gaussian, so that higher-order moments may be neglected.

The filter sequentially processes an ordered set of measurements, $\mathbb{Y}_k = [\mathbf{y}_0, \mathbf{y}_1, \ldots, \mathbf{y}_k]$ of the form

$$
\mathbf{y}_k = \mathbf{h}(\mathbf{x}_k, \mathbf{v}_k) \tag{12.2}
$$

where the measurement noise input, $\mathbf{v}$, consists of independent and identically distributed (again, in this work, Gaussian) increments whose first two moments are $\mathrm{E}[\mathbf{v}_k] = \mathbf{0}$ and $\mathrm{E}[\mathbf{v}_k \mathbf{v}_\ell] = \mathbf{R}_k \delta_{k\ell}$.

By contrast, the ADDSPF utilizes models where the noise sources enter additively:

$$
\mathbf{x}_{k+1} = \mathbf{f}(\mathbf{x}_k) + \mathbf{g}(\mathbf{x}_k)\mathbf{w}_k \tag{12.3}
$$

and

$$
\mathbf{y}_k = \mathbf{h}(\mathbf{x}_k) + \mathbf{v}_k. \tag{12.4}
$$

All sigma-point filters utilize a linear measurement update equation of the form

<span id="page-141-0"></span>
$$
\hat{\mathbf{x}}_k^+ = \hat{\mathbf{x}}_k^- + \mathbf{K}_k \left( \mathbf{y}_k - \hat{\mathbf{y}}_k^- \right) \tag{12.5}
$$

where the accented variables in Eq. [\(12.5\)](#page-141-0) denote conditional expectations, as in the Kalman filter:

$$
\hat{\mathbf{x}}_k^+ = \mathrm{E}[\mathbf{x}_k \vert \mathbb{Y}_k] \tag{12.6}
$$

$$
\hat{\mathbf{x}}_k^- = \mathrm{E}[\mathbf{x}_k \vert \mathbb{Y}_{k-1}] \tag{12.7}
$$

$$
\hat{\mathbf{y}}_k^- = \mathrm{E}[\mathbf{y}_k \vert \mathbb{Y}_{k-1}] \tag{12.8}
$$

The gain matrix, $\mathbf{K}$, is based on conditional covariances, as in the Kalman filter:

<span id="page-141-1"></span>
$$
\mathbf{K}_k = \mathbf{P}_{xy_k}^- \left( \mathbf{P}_{yy_k}^- \right)^{-1} \tag{12.9}
$$

$$
\mathbf{P}_k^- = \mathbf{P}_{xx_k}^- = \mathrm{E}\Big[ \left( \mathbf{x}_k - \hat{\mathbf{x}}_k^- \right) \left( \mathbf{x}_k - \hat{\mathbf{x}}_k^- \right)^{\mathsf{T}} \vert \mathbb{Y}_{k-1} \Big] \tag{12.10}
$$

$$
\mathbf{P}_{xy_k}^- = \mathrm{E}\Big[ \left( \mathbf{x}_k - \hat{\mathbf{x}}_k^- \right) \left( \mathbf{y}_k - \hat{\mathbf{y}}_k^- \right)^{\mathsf{T}} \vert \mathbb{Y}_{k-1} \Big] \tag{12.11}
$$

$$
\mathbf{P}_{yy_k}^- = \mathrm{E}\Big[ \left( \mathbf{y}_k - \hat{\mathbf{y}}_k^- \right) \left( \mathbf{y}_k - \hat{\mathbf{y}}_k^- \right)^{\mathsf{T}} \vert \mathbb{Y}_{k-1} \Big] \tag{12.12}
$$

$$
\, \tag{12.13}
$$

and the covariance associated with state estimate $\hat{\mathbf{x}}_k^+$ is

$$
\mathbf{P}_k^+ = \mathbf{P}_{xx_k}^+ = \mathrm{E}\Big[ \left( \mathbf{x}_k - \hat{\mathbf{x}}_k^+ \right) \left( \mathbf{x}_k - \hat{\mathbf{x}}_k^+ \right)^{\mathsf{T}} \vert \mathbb{Y}_k \Big] \tag{12.14}
$$

Hereafter, equations will suppress the time index if it is the same for all variables in the equation.

Estimators such as the Kalman filter estimate these conditional expectations by approximating the nonlinear functions $\mathbf{f}$ and $\mathbf{h}$ with first-order Taylor series truncations, e.g.:

$$
\mathbf{f}(\mathbf{x}) \approx \mathbf{f}(\hat{\mathbf{x}}^-) + \mathbf{f}'(\mathbf{x})(\mathbf{x} - \hat{\mathbf{x}}^-) \tag{12.15}
$$

where $\mathbf{f}'$ is an exact gradient. By contrast, the divided difference filter uses a second-order truncation along with numerical differencing formulas for the derivatives:

$$
\mathbf{f}(\mathbf{x}) \approx \mathbf{f}(\hat{\mathbf{x}}^-) + \tilde{\mathrm{D}}_{\Delta \mathbf{x}}^{(1)} \mathbf{f}(\hat{\mathbf{x}}^-) + \tilde{\mathrm{D}}_{\Delta \mathbf{x}}^{(2)} \mathbf{f}(\hat{\mathbf{x}}^-) \tag{12.16}
$$

where the divided difference operators, $\tilde{\mathrm{D}}_{\Delta \mathbf{x}}^{(i)} \mathbf{f}(\hat{\mathbf{x}}^-)$, approximate the coefficients of the multidimensional Taylor series expansion using Stirling interpolations. These interpolators difference perturbations of $\mathbf{f}(\hat{\mathbf{x}}^-)$ across a (dimensionless) interval, $h$, over a spanning basis set. Whether they are first-order, such as the unscented filter, or second order, sigma-point filters choose the interval so as to better approximate the moments required for the gain calculation, and choose as the spanning basis a set of sigma points, which are derived from $\hat{\mathbf{x}}^-$ and the columns of the Cholesky factors of $\mathbf{P}^-$ as follows.

### The ADDSPF

Let $\hat{\mathcal{X}}$ denote the array whose columns are a particular ordering of the sigma points derived from $\hat{\mathbf{x}}$ and its corresponding covariance, $\mathbf{P}$. Then

$$
\hat{\mathcal{X}} = \Big[ \hat{\mathbf{x}},\ \hat{\mathbf{x}} + h\, {}^{c}\!\sqrt{\mathbf{P}}_{(:,1)},\ \hat{\mathbf{x}} + h\, {}^{c}\!\sqrt{\mathbf{P}}_{(:,2)}, \ldots, \hat{\mathbf{x}} - h\, {}^{c}\!\sqrt{\mathbf{P}}_{(:,1)}, \hat{\mathbf{x}} - h\, {}^{c}\!\sqrt{\mathbf{P}}_{(:,2)}, \ldots \Big] \tag{12.17}
$$

where the subscript $(:, i)$ denotes column $i$ of the corresponding array, and $\mathbf{P} = {}^{c}\!\sqrt{\mathbf{P}}\, {}^{c}\!\sqrt{\mathbf{P}}^{\mathsf{T}}$ denotes a Cholesky factorization. In the sequel, the shorthand notation $\hat{\mathbf{x}} \pm h\, {}^{c}\!\sqrt{\mathbf{P}}$ will denote the array on the right-hand side of the equation above. Then, for the ADDSPF, Ref. [51](16-bibliography.md#page-172-24) shows that as each new measurement becomes available, an array of sigma points generated from the prior update should be propagated to the new measurement time:

$$
\hat{\mathcal{X}}_k^- = \mathbf{f}(\hat{\mathcal{X}}_{k-1}^+) \tag{12.18}
$$

These propagated sigma points are then merged to form the state estimate just prior to incorporating the new measurement as follows:

$$
\hat{\mathbf{x}}^- = \mu_h(\hat{\mathcal{X}}^-) = \frac{h^2 - n}{h^2} \hat{\mathcal{X}}_{(:,1)}^- + \frac{1}{2h^2} \sum_{i=2}^{2n+1} \hat{\mathcal{X}}_{(:,i)}^- \tag{12.19}
$$

To form an associated covariance, the following divided-differences are next computed:

$$
\tilde{\mathrm{D}}_{\Delta \mathbf{x}}^{(1)} \mathbf{f}(\hat{\mathbf{x}}^-)_{(:,i)} = \frac{1}{2h} \left[ \hat{\mathcal{X}}_{(:,i+1)}^- - \hat{\mathcal{X}}_{(:,i+1+n)}^- \right] \tag{12.20}
$$

$$
\tilde{\mathrm{D}}_{\Delta \mathbf{x}}^{(2)} \mathbf{f}(\hat{\mathbf{x}}^-)_{(:,i)} = \frac{\sqrt{h^2-1}}{2h^2} \left[ \hat{\mathcal{X}}_{(:,i+1)}^- + \hat{\mathcal{X}}_{(:,i+1+n)}^- - 2\hat{\mathcal{X}}_{(:,1)}^- \right] \tag{12.21}
$$

Ref. [51](16-bibliography.md#page-172-24) shows that the covariance may then be computed from

<span id="page-142-0"></span>
$$
\mathbf{P}^- = \left[ \tilde{\mathrm{D}}_{\Delta \mathbf{x}}^{(1)} \mathbf{f}(\hat{\mathbf{x}}^-),\, \tilde{\mathrm{D}}_{\Delta \mathbf{x}}^{(2)} \mathbf{f}(\hat{\mathbf{x}}^-),\ {}^{c}\!\sqrt{\mathbf{Q}_d} \right] \left[ \tilde{\mathrm{D}}_{\Delta \mathbf{x}}^{(1)} \mathbf{f}(\hat{\mathbf{x}}^-),\, \tilde{\mathrm{D}}_{\Delta \mathbf{x}}^{(2)} \mathbf{f}(\hat{\mathbf{x}}^-),\ {}^{c}\!\sqrt{\mathbf{Q}_d} \right]^{\mathsf{T}} \tag{12.22}
$$

One advantage of sigma-point filters is that the full covariance need not be maintained, but rather only its Cholesky factor. Although the factors in square brackets in Eq. [\(12.22\)](#page-142-0) are not Cholesky factors, since each is a full $n \times 3n$ matrix, one may extract an $n \times n$ triangular factor from it using the so-called "thin" version [[30](16-bibliography.md#page-171-27)] of the QR decomposition[<sup>1</sup>](#page-142-1), or alternatively using a Householder factorization [[5](16-bibliography.md#page-170-1)]. Thus,

$$
\mathbf{M} \begin{bmatrix} {}^{c}\!\sqrt{\mathbf{P}^-}^{\mathsf{T}} \\ \mathbf{O}_{2n \times n} \end{bmatrix} = \left[ \tilde{\mathrm{D}}_{\Delta \mathbf{x}}^{(1)} \mathbf{f}(\hat{\mathbf{x}}^-),\, \tilde{\mathrm{D}}_{\Delta \mathbf{x}}^{(2)} \mathbf{f}(\hat{\mathbf{x}}^-),\ {}^{c}\!\sqrt{\mathbf{Q}_d} \right]^{\mathsf{T}} \tag{12.23}
$$

where $\mathbf{M}$ is a full $3n \times 3n$ orthonormal matrix, and $\mathbf{O}_{2n \times n}$ is a $2n \times n$ matrix of zeros.

<span id="page-142-1"></span><sup>1</sup> For *Matlab* users, this may be accomplished in several ways, e.g. by passing the transpose of this matrix to the `qr` function, then keeping the first $n$ non-zero rows from the second output, and transposing this result.

For the measurement update, a new array of sigma points must be generated from $\hat{\mathbf{x}}^-$ and $\mathbf{P}^-$; this array is denoted $\hat{\mathcal{X}}^*$. These sigma points are used to generate a set of sigma points representing the measurement:

$$
\hat{\mathcal{Y}}^- = \mathbf{h}(\hat{\mathcal{X}}^*) \tag{12.24}
$$

In similar fashion to the time update, the sigma points of the measurement are then merged to form the estimated measurement:

$$
\hat{\mathbf{y}}^- = \mu_h(\hat{\mathcal{Y}}^-) \tag{12.25}
$$

the corresponding divided-differences are computed as:

$$
\tilde{\mathrm{D}}_{\Delta \mathbf{x}}^{(1)} \mathbf{h}(\hat{\mathbf{x}}^-)_{(:,i)} = \frac{1}{2h} \left[ \hat{\mathcal{Y}}_{(:,i+1)}^- - \hat{\mathcal{Y}}_{(:,i+1+n)}^- \right] \tag{12.26}
$$

$$
\tilde{\mathrm{D}}_{\Delta \mathbf{x}}^{(2)} \mathbf{h}(\hat{\mathbf{x}}^-)_{(:,i)} = \frac{\sqrt{h^2 - 1}}{2h^2} \left[ \hat{\mathcal{Y}}_{(:,i+1)}^- + \hat{\mathcal{Y}}_{(:,i+1+n)}^- - 2\hat{\mathcal{Y}}_{(:,1)}^- \right] \tag{12.27}
$$

and the covariances required for the gain calculation may then be computed from

$$
\mathbf{P}_{yy}^- = \left[ \tilde{\mathrm{D}}_{\Delta \mathbf{x}}^{(1)} \mathbf{h}(\hat{\mathbf{x}}^-),\, \tilde{\mathrm{D}}_{\Delta \mathbf{x}}^{(2)} \mathbf{h}(\hat{\mathbf{x}}^-),\ {}^{c}\!\sqrt{\mathbf{R}} \right] \left[ \tilde{\mathrm{D}}_{\Delta \mathbf{x}}^{(1)} \mathbf{h}(\hat{\mathbf{x}}^-),\, \tilde{\mathrm{D}}_{\Delta \mathbf{x}}^{(2)} \mathbf{h}(\hat{\mathbf{x}}^-),\ {}^{c}\!\sqrt{\mathbf{R}} \right]^{\mathsf{T}} \tag{12.28}
$$

$$
\mathbf{P}_{xy}^- = {}^{c}\!\sqrt{\mathbf{P}^-} \left[ \tilde{\mathrm{D}}_{\Delta \mathbf{x}}^{(1)} \mathbf{h}(\hat{\mathbf{x}}^-) \right]^{\mathsf{T}} \tag{12.29}
$$

Note that the second-order divided difference for the measurement function, $\tilde{\mathrm{D}}_{\Delta \mathbf{x}}^{(2)} \mathbf{h}(\hat{\mathbf{x}}^-)$, does *not* appear in the cross-covariance update. As with the time update, through the use of the thin QR factorization, only triangular factors need be maintained for $\mathbf{P}_{yy}^-$[<sup>2</sup>](#page-143-0):

$$
\mathbf{M}_{yy} \begin{bmatrix} {}^{c}\!\sqrt{\mathbf{P}_{yy}^-}^{\mathsf{T}} \\ \mathbf{O}_{2n \times n} \end{bmatrix} = \left[ \tilde{\mathrm{D}}_{\Delta \mathbf{x}}^{(1)} \mathbf{h}(\hat{\mathbf{x}}^-),\, \tilde{\mathrm{D}}_{\Delta \mathbf{x}}^{(2)} \mathbf{h}(\hat{\mathbf{x}}^-),\ {}^{c}\!\sqrt{\mathbf{R}} \right]^{\mathsf{T}} \tag{12.30}
$$

<span id="page-143-0"></span><sup>2</sup> Although it might seem that the full matrix $\mathbf{P}_{yy}^-$ is required for the gain computation of Eq. [\(12.9\)](#page-141-1), Ref. [64](16-bibliography.md#page-172-22) points out that, rather than inverting the product of the factors to compute the gain, the gain may be solved from forward and back substitution directly using the Cholesky factor.

Now, all of the terms required for the state update (Eqs. [12.5](#page-141-0) and [12.9\)](#page-141-1), are available. Ref. [51](16-bibliography.md#page-172-24) shows that the corresponding Cholesky factor of the covariance is extracted from

$$
\mathbf{M}^+ \begin{bmatrix} {}^{c}\!\sqrt{\mathbf{P}^+}^{\mathsf{T}} \\ \mathbf{O}_{2n \times n} \end{bmatrix} = \Big[ {}^{c}\!\sqrt{\mathbf{P}^-} - \mathbf{K} \tilde{\mathrm{D}}_{\Delta \mathbf{x}}^{(1)} \mathbf{h}(\hat{\mathbf{x}}^-),\ \mathbf{K} \left[ \tilde{\mathrm{D}}_{\Delta \mathbf{x}}^{(2)} \mathbf{h}(\hat{\mathbf{x}}^-),\ {}^{c}\!\sqrt{\mathbf{R}} \right] \Big] \tag{12.31}
$$

### The ADDSPF vs. Other Sequential Filters

To conclude this section, some observations concerning the ADDSPF in comparison to other filters are offered. These observations concern the number of sigma points, the order of approximation, and the existence and method of choice of free parameters in the algorithms.

Although in many problems of practical interest the noise enters the system additively, if this is not the case, then either the original divided difference filter or the unscented filter may provide superior results to the ADDSPF, at the cost of requiring more sigma points. In both of the former algorithms, the nonlinear functions must be perturbed not only over a basis spanning the state space, but also over the discrete process noise and measurement noise spaces. Thus, rather than $2n + 1$ sigma points, the more general algorithms require $2n_a + 1$, where $n_a = n + n_w + n_v$, and $n_w$ and $n_v$ are the dimensions of the discrete process noise and measurement noise inputs.

The Kalman filter is an exact algorithm for linear stochastic systems driven by Gaussian noise, and nothing is to be gained from the use the sigma-point filters for such purely linear systems. First-order sigma-point filters such as the UKF retain the Kalman filter's first-order truncation, but avoid the need for the designer to supply explicit gradients. The divided difference filter is comparable to a derivative-free version of the modified second-order Gaussian filter [[38](16-bibliography.md#page-171-0)] in that, for symmetric distributions, it retains some terms as high as order four.

Unlike the Kalman filter, for which all of the parameters in principle can be associated with properties of the underlying stochastic system, all of the sigma point filters involve at least one free parameter. In the unscented filter, the weights for combining the sigma points involve three parameters whose physical interpretation is perhaps less clear than with the single parameter in the divided difference algorithms, where the free parameter $h$ is clearly associated with the size of the perturbation in the numerical differencing formulae. Ref. [64](16-bibliography.md#page-172-22) shows that $h$ should be bounded below by $h > 1$, and that for symmetric distributions, $\sqrt{h}$ should be equal to the kurtosis, which for a Gaussian distribution is three[<sup>3</sup>](#page-144-0).

<span id="page-144-0"></span><sup>3</sup> Some authors subtract three from the definition of kurtosis, so that Gaussian distributions have zero kurtosis.

---

[← Chapter 11. Smoothing](11-smoothing.md) · [Contents](README.md) · [Appendix A. Models and Realizations of Random Variables →](13-appendix-a-models-and-realizations-of-random-variables.md)
