[← Chapter 6. Bias Modeling (part 1 of 2)](06-bias-modeling-part1.md) · [Contents](README.md) · [Chapter 7. State Representations →](07-state-representations.md)

*Chapter 6. Bias Modeling, continued*

## 6.3. Multi-Input Bias State Models

<span id="page-79-0"></span>We may combine any of the above models to create multi-input bias models; for example the bias could be a second-order Gauss-Markov, and the bias rate could be a first-order Gauss-Markov. In practice, the most useful combinations have been found to be the following.

### 6.3.1. Bias and Drift Random Walks (Random Walk + Random Run)

A common model for biases in clocks, gyros, and accelerometers is that the bias is driven by both its own white noise input, and also by the integral of the white noise of its drift. Such models derive from observations that the error magnitudes of these devices depend on the time scale over which the device is observed. They are often characterized by Allan deviation specifications, which may be heuristically associated with the white noise power spectral densities. The model is as follows:

```math
\begin{bmatrix} \dot{{𝖻}}(t) \\ \dot{{𝖽}}(t) \end{bmatrix} = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix} \begin{bmatrix} {𝖻}(t) \\ {𝖽}(t) \end{bmatrix} + \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix} \begin{bmatrix} {𝗐}_{{𝖻}}(t) \\ {𝗐}_{{𝖽}}(t) \end{bmatrix} \qquad\qquad(6.60)
```

```math
\dot{{𝘅}}(t) = {𝐀}{𝘅}(t) + {𝐁}{𝘄}(t) \qquad\qquad(6.61)
```

The measurement partial is the same as for the random ramp. The initial condition $`{𝘅}(t_o)`$ is an unbiased random constant. Since $`{𝘅}(t_o)`$ and $`{𝘄}(t)`$ are zero-mean, then $`{𝘅}(t)`$ is also zero-mean for all time. The covariance evolves in time according to

```math
{𝐏}_{{𝘅}}(t) = {𝚽}(t - t_o){𝐏}_{{𝘅}o}{𝚽}^{{𝖳}}(t - t_o) + {𝐒}(t - t_o) \qquad\qquad(6.62)
```

where

```math
{𝚽}(t) = \begin{bmatrix} 1 & t \\ 0 & 1 \end{bmatrix} \text{ and } {𝐏}_{{𝘅}o} = \begin{bmatrix} p_{{𝖻}o} & 0 \\ 0 & p_{\dot{{𝖻}}o} \end{bmatrix} \qquad\qquad(6.63)
```

and

```math
{𝐒}(t) = \begin{bmatrix} q_{{𝖻}}t + q_{{𝖽}}t^3/3 & q_{{𝖽}}t^2/2 \\ q_{{𝖽}}t^2/2 & q_{{𝖽}}t \end{bmatrix} \qquad\qquad(6.64)
```

which we can also write in recursive form as

```math
{𝐏}_x(t + \Delta t) = {𝚽}(\Delta t){𝐏}_x(t){𝚽}^{{𝖳}}(\Delta t) + {𝐒}(\Delta t) \qquad\qquad(6.65)
```

Thus, we can generate realizations of the random run with either $`{𝒙}(t) \sim N({𝟎}, {𝐏}_{{𝘅}}(t))`$ or recursively from

```math
{𝒙}(t + \Delta t) = {𝚽}(\Delta t){𝒙}(t) + {𝝕}(t) \qquad\qquad(6.66)
```

where $`{𝝕}(t) \sim N(0, {𝐒}(\Delta t))`$. Note that a Cholesky decomposition of $`{𝐒}(t)`$ is

```math
{}^{C}\!\sqrt{{𝐒}(t)} = \begin{bmatrix} \sqrt{q_{{𝖻}}t + q_{{𝖽}}t^3/12} & \sqrt{q_{{𝖽}}t^3}/2 \\ 0 & \sqrt{q_{{𝖽}}t} \end{bmatrix} \qquad\qquad(6.67)
```

As with its constituent models, the norm of the unconditional covariance becomes infinite as $`t^3`$ becomes infinite, while the process is persistently stimulated by the input, so its covariance conditioned on a measurement history will remain positive definite for all time. Hence, this model shares similar considerations with its constituents for application in sequential navigation filters.

### 6.3.2. Bias, Drift, and Drift Rate Random Walks (Random Walk + Random Run + Random Zoom)

Another model for biases in very-high precision clocks, gyros, and accelerometers is that the bias is driven by two integrals of white noise in addition to its own white noise input. Such models are often characterized by Hadamard deviation specifications, which may be heuristically associated with the white noise power spectral densities. The model is as follows:

```math
\begin{bmatrix} \dot{{𝖻}}(t) \\ \dot{{𝖽}}(t) \\ \ddot{{𝖽}}(t) \end{bmatrix} = \begin{bmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ 0 & 0 & 0 \end{bmatrix} \begin{bmatrix} {𝖻}(t) \\ {𝖽}(t) \\ \dot{{𝖽}}(t) \end{bmatrix} + \begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} {𝗐}_b(t) \\ {𝗐}_d(t) \\ {𝗐}_{\dot{{𝖽}}}(t) \end{bmatrix} \qquad\qquad(6.68)
```

```math
\dot{{𝘅}}(t) = {𝐀}{𝘅}(t) + {𝐁}{𝘄}(t) \qquad\qquad(6.69)
```

The resulting output equation is

```math
{𝖾} = \begin{bmatrix} 1 & 0 & 0 \end{bmatrix} {𝘅} + {𝗏} \qquad\qquad(6.70)
```

```math
= {𝐇}{𝘅} + {𝗏} \qquad\qquad(6.71)
```

The initial condition $`{𝘅}(t_o)`$ is an unbiased random constant. Since $`{𝘅}(t_o)`$ and $`{𝘄}(t)`$ are zero-mean, then $`{𝘅}(t)`$ is also zero-mean for all time. The covariance evolves in time according to

```math
{𝐏}_{{𝘅}}(t) = {𝚽}(t - t_o){𝐏}_{{𝘅}o}{𝚽}^{{𝖳}}(t - t_o) + {𝐒}(t - t_o) \qquad\qquad(6.72)
```

where

```math
{𝚽}(t) = \begin{bmatrix} 1 & t & t^2/2 \\ 0 & 1 & t \\ 0 & 0 & 1 \end{bmatrix} \text{ and } {𝐏}_{{𝘅}o} = \begin{bmatrix} p_{{𝖻}o} & 0 & 0 \\ 0 & p_{{𝖽}o} & 0 \\ 0 & 0 & p_{\dot{{𝖽}}o} \end{bmatrix} \qquad\qquad(6.73)
```

and

```math
{𝐒}(t) = \begin{bmatrix} q_{{𝖻}}t + q_{{𝖽}}t^3/3 + q_{\dot{{𝖽}}}t^5/5 & q_{{𝖽}}t^2/2 + q_{\dot{{𝖽}}}t^4/8 & q_{\dot{{𝖽}}}t^3/6 \\ q_{{𝖽}}t^2/2 + q_{\dot{{𝖽}}}t^4/8 & q_{{𝖽}}t + q_{\dot{{𝖽}}}t^3/3 & q_{\dot{{𝖽}}}t^2/2 \\ q_{\dot{{𝖽}}}t^3/6 & q_{\dot{{𝖽}}}t^2/2 & q_{\dot{{𝖽}}}t \end{bmatrix} \qquad\qquad(6.74)
```

which we can also write in recursive form as

```math
{𝐏}_{{𝘅}}(t + \Delta t) = {𝚽}(\Delta t){𝐏}_{{𝘅}}(t){𝚽}^{{𝖳}}(\Delta t) + {𝐒}(\Delta t) \qquad\qquad(6.75)
```

Thus, we can generate realizations of the random run with either $`{𝒙}(t) \sim N({𝟎}, {𝐏}_{{𝘅}}(t))`$ or recursively from

```math
{𝒙}(t + \Delta t) = {𝚽}(\Delta t){𝒙}(t) + {𝝕}(t) \qquad\qquad(6.76)
```

where $`{𝝕}(t) \sim N(0, {𝐒}(\Delta t))`$. Note that a Cholesky decomposition of $`{𝐒}(t)`$ is

```math
{}^{C}\!\sqrt{{𝐒}(t)} = \begin{bmatrix} \sqrt{q_{{𝖻}}t + q_{{𝖽}}t^3/12 + q_{\dot{{𝖽}}}t^5/720} & t/2\sqrt{q_{{𝖽}}t + q_{\dot{{𝖽}}}t^3/12} & t^2/6\sqrt{q_{\dot{{𝖽}}}t} \\ 0 & \sqrt{q_{{𝖽}}t + q_{\dot{{𝖽}}}t^3/12} & t/2\sqrt{q_{\dot{{𝖽}}}t} \\ 0 & 0 & \sqrt{q_{\dot{{𝖽}}}t} \end{bmatrix} \qquad\qquad(6.77)
```

Similar to its constituent models, the norm of the unconditional covariance becomes infinite as $`t^5`$ becomes infinite, while the process is persistently stimulated by the input, so its covariance conditioned on a measurement history will remain positive definite for all time. Hence, this model shares similar considerations with its constituents for application in sequential navigation filters.

### 6.3.3. Bias and Drift Coupled First- and Second-Order Gauss-Markov

The following model provides a stable alternative, developed in Reference [14](16-bibliography.md#page-170-14), to the "Random Walk + Random Run" model. Note that the following description corrects a sign error in the process noise cross-covariance results of the cited work. The transient response of the stable alternative can be tuned to approximate the Random Walk + Random Run model, and its stable steady-state response can be used to avoid computational issues with long propagation times, observability, consider states, etc. Although this model has received limited application as of the time of this writing, due to its stability, it shows promising potential to evolve into a *best practice* for sequential navigation filtering applications.

The coupled first- and second-order Gauss-Markov model is as follows.

```math
\begin{bmatrix} \dot{{𝖻}}(t) \\ \dot{{𝖽}}(t) \end{bmatrix} = \begin{bmatrix} -1/\tau & 1 \\ -\omega_n^2 & -2\zeta\omega_n \end{bmatrix} \begin{bmatrix} {𝖻}(t) \\ {𝖽}(t) \end{bmatrix} + \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix} \begin{bmatrix} {𝗐}_b(t) \\ {𝗐}_d(t) \end{bmatrix} \qquad\qquad(6.78)
```

```math
\dot{{𝘅}}(t) = {𝐀}{𝘅}(t) + {𝐁}{𝘄}(t) \qquad\qquad(6.79)
```

The measurement partial is the same as for the random ramp. The initial condition $`{𝘅}(t_o)`$ is an unbiased random constant. Since $`{𝘅}(t_o)`$ and $`{𝘄}(t)`$ are zero-mean, then $`{𝘅}(t)`$ is also zero-mean for all time. The covariance evolves in time according to

```math
{𝐏}_{{𝘅}}(t) = {𝚽}(t - t_o){𝐏}_{{𝘅}o}{𝚽}^{{𝖳}}(t - t_o) + {𝐒}(t - t_o) \qquad\qquad(6.80)
```

where

```math
{𝚽}(t) = \frac{\mathrm{e}^{\eta t}}{\nu} \begin{bmatrix} \nu\cos\nu t + (\eta + 2\zeta\omega_n)\sin\nu t & \sin\nu t \\ -\omega_n^2 \sin\nu t & \nu\cos\nu t + (\eta + \beta)\sin\nu t \end{bmatrix} \qquad\qquad(6.81)
```

<span id="page-82-0"></span>with

```math
\beta = 1/\tau, \qquad\qquad(6.82)
```

```math
\eta = -\frac{1}{2}\left(\beta + 2\zeta\omega_n\right), \qquad\qquad(6.83)
```

```math
\nu = \sqrt{\omega_d^2 + \beta\zeta\omega_n - \frac{1}{4}\beta^2}, \qquad\qquad(6.84)
```

```math
\omega_d = \omega_n\sqrt{1 - \zeta^2} \qquad\qquad(6.85)
```

and we assume that $`\nu^2 \gt 0`$. Let

```math
\kappa = -\frac{\beta}{2} + \zeta\omega_n
```

Then, the process noise covariance is given by the following:

```math
\begin{aligned} {𝐒}_{(1,1)}(t) = q_{{𝖻}} \Bigg[ & \frac{\mathrm{e}^{2\eta t} - 1}{4\eta}\left(1 + \frac{\kappa^2}{\nu^2}\right) + \frac{\mathrm{e}^{2\eta t}\sin 2\nu t}{4(\eta^2 + \nu^2)}\left(\frac{\nu^2 - \kappa^2 + \eta\kappa}{\nu}\right) \\ & + \frac{\mathrm{e}^{2\eta t}\cos 2\nu t - 1}{4(\eta^2 + \nu^2)}\left(\frac{\eta\nu^2 - \eta\kappa^2 + 2\nu^2\kappa}{\nu^2}\right) \Bigg] \\ & + \frac{q_{{𝖽}}}{\nu^2}\left(\frac{\mathrm{e}^{2\eta t} - 1}{4\eta} - \frac{\mathrm{e}^{2\eta t}(\nu\sin 2\nu t + \eta\cos 2\nu t) - \eta}{4(\eta^2 + \nu^2)}\right) \end{aligned} \qquad\qquad(6.86)
```

```math
\begin{aligned} {𝐒}_{(2,2)}(t) = q_{{𝖽}} \Bigg[ & \frac{\mathrm{e}^{2\eta t} - 1}{4\eta}\left(1 + \frac{\kappa^2}{\nu^2}\right) + \frac{\mathrm{e}^{2\eta t}\sin 2\nu t}{4(\eta^2 + \nu^2)}\left(\frac{\nu^2 - \kappa^2 + \eta\kappa}{\nu}\right) \\ & + \frac{\mathrm{e}^{2\eta t}\cos 2\nu t - 1}{4(\eta^2 + \nu^2)}\left(\frac{\eta\nu^2 - \eta\kappa^2 + 2\nu^2\kappa}{\nu^2}\right) \Bigg] \\ & + \frac{q_{{𝖻}}\omega_n^4}{\nu^2}\left(\frac{\mathrm{e}^{2\eta t} - 1}{4\eta} - \frac{\mathrm{e}^{2\eta t}(\nu\sin 2\nu t + \eta\cos 2\nu t) - \eta}{4(\eta^2 + \nu^2)}\right) \end{aligned} \qquad\qquad(6.87)
```

```math
\begin{aligned} {𝐒}_{(1,2)}(t) = {} & \frac{q_{{𝖻}}\omega_n^2}{\nu^2}\left[\frac{\kappa}{4\eta}\left(1 - \mathrm{e}^{2\eta t}\right) + \frac{\mathrm{e}^{2\eta t}\left[(\nu\kappa - \eta\nu)\sin 2\nu t + (\eta\kappa + \nu^2)\cos 2\nu t\right] - (\eta\kappa + \nu^2)}{4(\eta^2 + \nu^2)}\right] \\ & + \frac{q_{{𝖽}}}{\nu^2}\left[\frac{\kappa}{4\eta}\left(1 - \mathrm{e}^{2\eta t}\right) + \frac{\mathrm{e}^{2\eta t}\left[(\eta\nu + \nu\kappa)\sin 2\nu t + (\eta\kappa - \nu^2)\cos 2\nu t\right] - (\eta\kappa - \nu^2)}{4(\eta^2 + \nu^2)}\right] \end{aligned} \qquad\qquad(6.88)
```

```math
{𝐒}_{(2,1)}(t) = {𝐒}_{(1,2)}(t) \qquad\qquad(6.89)
```

Examining the solution given above, we see that the parameter $`\eta`$ governs the rate of decay of all of the exponential terms. Therefore, we define the "rise time" as that interval within which the transient response of the covariance will reach a close approximation to the above steady-state value; thus, we define the rise time as follows:

```math
t_r = -\frac{3}{\eta} \qquad\qquad(6.90)
```

Next, we note that all of the trigonometric terms are modulated by $`2\nu`$; thus we may view this value as a characteristic damped frequency of the coupled system. The period of the oscillation, $`\Pi`$, is then

```math
\Pi = \pi/\nu \qquad\qquad(6.91)
```

<span id="page-83-0"></span>In the limit as $`t \to \infty`$, all the exponential terms in the analytical solution die out, so that the steady-state value of the covariance simplifies to:

```math
{𝐏}(\infty) = -\frac{1}{4\eta(\eta^2 + \nu^2)} \begin{bmatrix} q_{{𝖽}} + (2\eta^2 + \nu^2 + \kappa^2 - \eta\kappa)q_{{𝖻}} & q_{{𝖻}}\omega_n^2(\eta - \kappa) - q_{{𝖽}}(\eta + \kappa) \\ q_{{𝖻}}\omega_n^2(\eta - \kappa) - q_{{𝖽}}(\eta + \kappa) & (2\eta^2 + \nu^2 + \kappa^2 + \eta\kappa)q_{{𝖽}} + q_{{𝖻}}\omega_n^4 \end{bmatrix} \qquad\qquad(6.92)
```

which may be expressed in terms of the original parameters as

```math
\begin{aligned} {𝐏}(\infty) = {} & \frac{1}{4\omega_n(\omega_n + 2\beta\zeta)(\zeta\omega_n + \beta/2)} \\ & \cdot \begin{bmatrix} q_{{𝖽}} + (\omega_n^2 + 2\beta\zeta\omega_n + 4\zeta^2\omega_n^2)q_{{𝖻}} & q_{{𝖽}}\beta - 2\zeta\omega_n^3 q_{{𝖻}} \\ q_{{𝖽}}\beta - 2\zeta\omega_n^3 q_{{𝖻}} & (\omega_n^2 + 2\beta\zeta\omega_n + \beta^2)q_{{𝖽}} + \omega_n^4 q_b \end{bmatrix} \end{aligned} \qquad\qquad(6.93)
```

---

[← Chapter 6. Bias Modeling (part 1 of 2)](06-bias-modeling-part1.md) · [Contents](README.md) · [Chapter 7. State Representations →](07-state-representations.md)
