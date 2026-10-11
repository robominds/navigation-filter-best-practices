[← Chapter 5. Measurement Underweighting](05-measurement-underweighting.md) · [Contents](README.md) · [Chapter 6. Bias Modeling (part 2 of 2) →](06-bias-modeling-part2.md)

# Chapter 6. Bias Modeling

*Contributed by J. Russell Carpenter*

<span id="page-72-0"></span>A general model for a measurement error is as follows:

```math
{𝖾} = {𝖻} + {𝗏} \qquad\qquad(6.1)
```

where $`{𝖻}`$ models the systematic errors, and $`{𝗏}`$ models the measurement noise. We assume that the measurement noise is a discrete sequence of uncorrelated random numbers. Variables such as $`{𝗏}`$ are known as random variables, and Appendix [A](13-appendix-a-models-and-realizations-of-random-variables.md#page-146-0) describes how to model them. This Chapter describes models for the systematic errors.

The discussion of systematic errors treats such errors as scalar quantities to simplify the exposition; generalization to the vector case is straightforward. Note that if the measurement is nonscalar, but the errors in the component measurements are independent of one another, then we can model each measurement independently, so modeling the biases as a vector is not required. If the measurement errors are not independent, then many estimators require that we apply a transformation to the data prior to processing so that the data input to the estimator have independent measurement errors; Appendix [A](13-appendix-a-models-and-realizations-of-random-variables.md#page-146-0) describes some ways to accomplish this transformation.

## 6.1. Zero-Input Bias State Models

<span id="page-72-1"></span>The simplest non-zero measurement error consists only of measurement noise. The next simplest class of measurement errors consists of biases which are either themselves constant, or are the integrals of constants. We can view such biases as the output of a system which has zero inputs, and which may have internal states. In the sequel, we will consider cases where there are random inputs to the system.

In cases where the bias is the output of a system with internal states, the estimator may treat the internal states as solve-for or consider parameters. In such cases, the estimator requires a measurement partials matrix. Otherwise, the "measurement partial" is just $`H = \partial b/\partial b = 1`$.

### 6.1.1. Random Constant

The simplest type of systematic error is a constant bias on the measurement. There are two types of such biases: deterministic constants, which are truly constant for all time, and random constants, which are constant or very nearly so over a particular time of interest. For example, each time a sensor is power-cycled, a bias associated with it may change in value, but so long as the sensor remains powered on, the bias will not change.

In some cases, we may have reason to believe that a particular systematic error source truly is a deterministic bias, but due to limited observability, we do not have knowledge of its true value. In such cases, we may view our estimate of the bias as a random constant, and its variance as a measure of the imprecision of our knowledge.

Thus, we may view all constants that could be solve-for or consider parameters in orbit determination as random constants. A model for a random constant is

```math
\dot{{𝖻}}(t) = 0,\ b(t_o) \sim N(0, p_{{𝖻}o}). \qquad\qquad(6.2)
```

Thus the unconditional mean of $`{𝖻}(t)`$ is zero for all time, and its unconditional covariance is constant for all time as well. If $`{𝖻}(t)`$ is a filter solve-for variable that is observable, then its covariance conditioned on the measurement sequence will reach zero in the limit as $`t \to \infty`$. This is an undesirable characteristic for application in a sequential navigation filter.

To simulate a realization of the random constant, we need only generate a random number according to $`N(0, p_{{𝖻}o})`$, as the previous subsection described.

### 6.1.2. Random Ramp

The random ramp model assumes that the rate of change of the bias is itself a random constant; thus the random ramp model is

```math
\ddot{{𝖻}}(t) = 0,\ \dot{b}(t_o) \sim N(0, p_{\dot{{𝖻}}o}). \qquad\qquad(6.3)
```

Thus, the initial condition $`\dot{{𝖻}}(t_o)`$ is a random constant. For a pure random ramp, the initial condition on $`{𝖻}(t_o)`$ and its covariance are taken to be zero, but an obvious and common generalization is to allow $`{𝖻}(t_o)`$ to also be a random constant.

It is convenient to write this model as a first-order vector system as follows:

```math
\begin{bmatrix} \dot{{𝖻}}(t) \\ \ddot{{𝖻}}(t) \end{bmatrix} = \begin{bmatrix} \dot{{𝖻}}(t) \\ \dot{{𝖽}}(t) \end{bmatrix} = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix} \begin{bmatrix} {𝖻}(t) \\ {𝖽}(t) \end{bmatrix} \qquad\qquad(6.4)
```

```math
\dot{{𝘅}}(t) = {𝐀}{𝘅}(t) \qquad\qquad(6.5)
```

where $`{𝖽}(t) = \dot{{𝖻}}(t)`$. The resulting output equation for the total measurement error is

```math
{𝖾} = \begin{bmatrix} 1 & 0 \end{bmatrix} {𝘅} + {𝗏} \qquad\qquad(6.6)
```

```math
= {𝐇}{𝘅} + {𝗏} \qquad\qquad(6.7)
```

Note that the ensemble of realizations of $`{𝘅}(t)`$ has zero-mean for all time. The unconditional covariance evolves in time according to

```math
{𝐏}_{{𝘅}}(t) = {𝚽}(t - t_o){𝐏}_{{𝘅}o}{𝚽}^{{𝖳}}(t - t_o) \qquad\qquad(6.8)
```

where

```math
{𝚽}(t) = \begin{bmatrix} 1 & t \\ 0 & 1 \end{bmatrix} \text{ and } {𝐏}_{{𝘅}o} = \begin{bmatrix} p_{{𝖻}o} & 0 \\ 0 & p_{\dot{{𝖻}}o} \end{bmatrix} \qquad\qquad(6.9)
```

which we can also write in recursive form as

```math
{𝐏}_{{𝘅}}(t + \Delta t) = {𝚽}(\Delta t){𝐏}_{{𝘅}}(t){𝚽}^{{𝖳}}(\Delta t) \qquad\qquad(6.10)
```

Thus, we can generate realizations of the random ramp with either $`{𝒙}(t) \sim N({𝟎}, {𝐏}_{{𝘅}}(t))`$ or recursively from

```math
{𝒙}(t + \Delta t) = {𝚽}(\Delta t){𝒙}(t) \qquad\qquad(6.11)
```

Note that the norm of the unconditional covariance becomes infinite as $`t^2`$ becomes infinite. This could lead to an overflow of the representation of the covariance in a computer program if the propagation time between measurements is large, if the bias is unobservable, or if the bias is a consider parameter, and could also lead to the representation of the covariance losing either its symmetry and/or its positive definiteness due to roundoff and/or truncation. If the bias and drift are filter solve-for variables, then the norm of their covariance conditioned on the measurement sequence will reach zero in the limit as $`t \to \infty`$. These are all undesirable characteristics for application in a sequential navigation filter.

### <span id="page-74-2"></span>6.1.3. Higher-Order Derivatives of Random Constants

In principle, a random constant may be associated with any derivative of the bias in a straightforward extension of the models above. In practice, it is rare to need more than two or three derivatives. Conventional terminology does not appear in the literature for derivatives of higher order than the random ramp. The slope of the bias is most commonly described as the "bias drift," so that a "drift random ramp" would be one way to describe a bias whose second derivative is a random constant. The measurement partials matrix needs to be accordingly padded with trailing zeros for the derivatives of the bias in such cases.

## 6.2. Single-Input Bias State Models

<span id="page-74-0"></span>The simplest non-constant systematic errors are systems with a single input that is a random process. We can think of a random process as the result of some kind of limit in which the intervals between an uncorrelated sequence of random variables get infinitesimally small. In this limit, each random increment instantaneously perturbs the sequence, so that the resulting process is continuous but non-differentiable. We call this kind of a random input "process noise."

Although such random processes are non-differentiable, there are various techniques for generalizing the concept of integration so that something like integrals of the process noise exist, and hence so do the differentials that appear under the integral signs. It turns out that so long as any coefficients of the process noise are non-random, these differentials behave for all practical purposes as if they were differentiable.

### 6.2.1. Random Walk

The random walk is the simplest random process of the type described above. In terms of the "formal derivatives" mentioned above, the random walk model for a measurement bias is

```math
\dot{{𝖻}}(t) = {𝗐}(t),\ w(t) \sim N(0, q\delta(t - s)) \qquad\qquad(6.12)
```

The input noise process on the right hand side is known as "white noise," and the Dirac delta function that appears in the expression for its variance indicates that the white noise process consists of something like an infinitely-tightly spaced set of impulses. The term $`q`$ that appears along with the delta function is the intensity of each impulse[<sup>1</sup>](#page-74-1). The initial condition $`{𝖻}(t_o)`$ is an unbiased random constant. Since $`{𝖻}(t_o)`$ and $`{𝗐}(t)`$ are zero-mean, then $`{𝖻}(t)`$ is also zero-mean for all time. The unconditional variance of $`{𝖻}`$ evolves in time according to

```math
p_{{𝖻}}(t) = p_{{𝖻}o} + q(t - t_o) \qquad\qquad(6.13)
```

which we can also write in recursive form as

```math
p_{{𝖻}}(t + \Delta t) = p_{{𝖻}}(t) + q\Delta t \qquad\qquad(6.14)
```

Thus, to generate a realization of the random walk at time $`t`$, we need only generate a random number according to $`N(0, p_{{𝖻}}(t))`$. Equivalently, we could also generate realizations of $`\varpi(t) \sim N(0, q\Delta t)`$, and recursively add these discrete noise increments to the bias as follows:

```math
b(t + \Delta t) = b(t) + \varpi(t) \qquad\qquad(6.15)
```

Note that the unconditional variance becomes infinite as $`t`$ becomes infinite. This could lead to an overflow of the representation of $`p_{{𝖻}}`$ if $`q`$ is large in the following circumstances: in a long gap between measurements, if the bias is unobservable, or if the bias is a consider parameter. These are all somewhat undesirable characteristics for application in a sequential navigation filter. However, because the process is persistently stimulated by the input, its variance conditioned on a measurement history will remain positive for all time. Hence the random walk finds frequent application in sequential navigation filters, particularly when continuous measurements from which the bias is observable are generally available, such as often occurs for GPS data.

<span id="page-74-1"></span><sup>1</sup> Another way to imagine the input sequence, in terms of a frequency domain interpretation, is that it is a noise process whose power spectral density, $`q`$, is non-zero at all frequencies, which implies infinite bandwidth.

### 6.2.2. Random Run

The random run model assumes that the rate of change of the bias is itself a random walk; thus the random run model is

```math
\ddot{{𝖻}}(t) = {𝗐}(t),\ w(t) \sim N(0, q\delta(t - s)) \qquad\qquad(6.16)
```

The initial condition $`\dot{{𝖻}}(t_o)`$ is a random constant. For a pure random run, the initial condition on $`{𝖻}(t_o)`$ and its covariance are taken to be zero, but an obvious and common generalization is to allow $`{𝖻}(t_o)`$ to also be a random constant.

It is convenient to write this model as a first-order vector system as follows:

```math
\begin{bmatrix} \dot{{𝖻}}(t) \\ \ddot{{𝖻}}(t) \end{bmatrix} = \begin{bmatrix} \dot{{𝖻}}(t) \\ \dot{{𝖽}}(t) \end{bmatrix} = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix} \begin{bmatrix} {𝖻}(t) \\ {𝖽}(t) \end{bmatrix} + \begin{bmatrix} 0 \\ 1 \end{bmatrix} {𝗐}(t) \qquad\qquad(6.17)
```

```math
\dot{{𝘅}}(t) = {𝐀}{𝘅}(t) + {𝐁}{𝗐}(t) \qquad\qquad(6.18)
```

The measurement partial is the same as for the random ramp. The initial condition $`{𝘅}(t_o)`$ is an unbiased random constant. Since $`{𝘅}(t_o)`$ and $`{𝗐}(t)`$ are zero-mean, then $`{𝘅}(t)`$ is also zero-mean for all time. The covariance evolves in time according to

```math
{𝐏}_{{𝘅}}(t) = {𝚽}(t - t_o){𝐏}_{{𝘅}o}{𝚽}^{{𝖳}}(t - t_o) + {𝐒}(t - t_o) \qquad\qquad(6.19)
```

where

```math
{𝚽}(t - t_o) = \begin{bmatrix} 1 & t \\ 0 & 1 \end{bmatrix} \text{ and } {𝐏}_{{𝘅}o} = \begin{bmatrix} p_{{𝖻}o} & 0 \\ 0 & p_{\dot{{𝖻}}o} \end{bmatrix} \qquad\qquad(6.20)
```

and

```math
{𝐒}(t) = q \begin{bmatrix} t^3/3 & t^2/2 \\ t^2/2 & t \end{bmatrix} \qquad\qquad(6.21)
```

which we can also write in recursive form as

```math
{𝐏}_{{𝘅}}(t + \Delta t) = {𝚽}(\Delta t){𝐏}_{{𝘅}}(t){𝚽}^{{𝖳}}(\Delta t) + {𝐒}(\Delta t) \qquad\qquad(6.22)
```

Thus, we can generate realizations of the random run with either $`{𝒙}(t) \sim N({𝟎}, {𝐏}_{{𝘅}(t)})`$ or recursively from

```math
{𝒙}(t + \Delta t) = {𝚽}(\Delta t){𝒙}(t) + {𝝕}(t) \qquad\qquad(6.23)
```

where $`{𝝕}(t) \sim N({𝟎}, {𝐒}(\Delta t))`$ is a noise sample *vector* arising from formal integration of the scalar noise input process over the sample time. A Cholesky decomposition of $`{𝐒}(t)`$ useful for sampling is

```math
{}^{C}\!\sqrt{{𝐒}(t)} = \begin{bmatrix} \sqrt{3t^3}/3 & 0 \\ \sqrt{3t}/2 & \sqrt{t}/2 \end{bmatrix} \qquad\qquad(6.24)
```

Note that the norm of the unconditional covariance becomes infinite as $`t^3`$ becomes infinite, and the process is persistently stimulated by the input, so its covariance conditioned on a measurement history will remain positive definite for all time. Hence, the random run shares similar considerations with the random walk for application in sequential navigation filters.

### 6.2.3. Higher-Order Derivatives of Random Walks

In principle, a random walk may be associated with any derivative of the bias in a straightforward extension of the models above. In practice, it is rare to need more than two or three derivatives. Conventional terminology does not appear in the literature for derivatives of higher order than the random run. A "drift random run" would be one way to describe a bias whose second derivative is a random walk. Below, we will refer to such a model as a "random zoom."

### <span id="page-76-1"></span>6.2.4. First-Order Gauss-Markov

The first-order Gauss-Markov (FOGM) process is one of the simplest random processes that introduces time correlation between samples. In terms of a frequency domain interpretation, we can view it as white noise passed through a low-pass filter. Since such noise, often called "colored noise," has finite bandwidth, it is physically realizable, unlike white noise. In the notation of formal derivatives, the FOGM model is

```math
\dot{{𝖻}}(t) = -\frac{1}{\tau}{𝖻}(t) + {𝗐}(t), \qquad\qquad(6.25)
```

where, as with the random walk, $`b(t_o) \sim N(0, p_{bo})`$, and $`w(t) \sim N(0, q\delta(t-s))`$. The time constant, $`\tau`$ gives the correlation time, or the time over which the intensity of the time correlation will fade to $`1/\mathrm{e}`$ of its prior value[<sup>2</sup>](#page-76-0). Note that as $`\tau \to \infty`$, the FOGM approximates a random walk.

<span id="page-76-0"></span><sup>2</sup> One sometimes sees $`\tau`$ described as the "half-life," but since $`1/\mathrm{e} \lt 1/2`$, this is not an accurate label.

Since $`{𝖻}(t_o)`$ and $`{𝗐}(t)`$ are zero-mean, then $`{𝖻}(t)`$ is also zero-mean for all time. The covariance evolves in time according to

```math
p_{{𝖻}}(t) = \mathrm{e}^{-\frac{2}{\tau}(t - t_o)}\, p_{{𝖻}o} + s(t - t_o) \qquad\qquad(6.26)
```

where

```math
s(t - t_o) = \frac{q\tau}{2}\biggl(1 - \mathrm{e}^{-\frac{2}{\tau}(t - t_o)}\biggr) \qquad\qquad(6.27)
```

which we can also write in recursive form as

```math
p_{{𝖻}}(t + \Delta t) = \mathrm{e}^{-\frac{2\Delta t}{\tau}}\, p_{{𝖻}}(t) + s(\Delta t) \qquad\qquad(6.28)
```

Thus, to generate discrete samples of a particular realization of the FOGM, we can either generate samples from $`b(t) \sim N(0, p_{{𝖻}}(t))`$, or generate a realization of the initial bias value, and then at each sample time generate realizations of $`\varpi(t) \sim N(0, s(\Delta t))`$, and recursively add these discrete noise sample increments to the bias sample history as follows:

```math
b(t + \Delta t) = \mathrm{e}^{-\frac{\Delta t}{\tau}}\, b(t) + \varpi(t) \qquad\qquad(6.29)
```

Note that $`p_{{𝖻}}`$ approaches a finite steady-state value equal to $`q\tau/2`$ as $`t`$ becomes infinite. One can choose the parameters of the FOGM so that this steady-state value avoids any overflow of the representation of $`p_{{𝖻}}`$ in a computer program, and such that the FOGM's covariance evolution prior to reaching steady-state closely mimics that of a random walk. For these reasons, the FOGM is recommended as a *best practice* for bias modeling in sequential navigation filters.

### 6.2.5. Integrated First-Order Gauss-Markov Model

As with the random walk and random constant models, any number of derivatives of the bias may be associated with a FOGM process. However, integration of the FOGM destroys its stability. For example, the singly integrated first-order Gauss-Markov model is given by

```math
\begin{bmatrix} \dot{{𝖻}}(t) \\ \dot{{𝖽}}(t) \end{bmatrix} = \begin{bmatrix} 0 & 1 \\ 0 & -1/\tau \end{bmatrix} \begin{bmatrix} {𝖻}(t) \\ {𝖽}(t) \end{bmatrix} + \begin{bmatrix} 0 \\ {𝗐}(t) \end{bmatrix}, \qquad\qquad(6.30)
```

which leads to the following state transition matrix,

```math
{𝚽}(t) = \begin{bmatrix} 1 & \tau\left(1 - \mathrm{e}^{-t/\tau}\right) \\ 0 & \mathrm{e}^{-t/\tau} \end{bmatrix}, \qquad\qquad(6.31)
```

and process noise covariance[<sup>3</sup>](#page-77-0),

<span id="page-77-1"></span>
```math
{𝐒}(t) = \frac{q\tau}{2} \begin{bmatrix} \tau^2\left\{\left(1 - \mathrm{e}^{-2t/\tau}\right) - 4\left(1 - \mathrm{e}^{-t/\tau}\right) + 2t/\tau\right\} & \tau\left(1 - \mathrm{e}^{-t/\tau}\right)^2 \\ \tau\left(1 - \mathrm{e}^{-t/\tau}\right)^2 & \left(1 - \mathrm{e}^{-2t/\tau}\right) \end{bmatrix}. \qquad\qquad(6.32)
```

<span id="page-77-0"></span><sup>3</sup> Note that [\(6.32\)](#page-77-1) corrects an error in Reference [14](16-bibliography.md#page-170-14).

Clearly, this is an unstable model, as the bias variance increases linearly with elapsed time. As an alternative, the following second-order model is available.

### 6.2.6. Second-Order Gauss-Markov

The model for a second-order Gauss-Markov (SOGM) random process is

```math
\ddot{{𝖻}}(t) = -2\zeta\omega_n\dot{{𝖻}}(t) - \omega_n^2{𝖻}(t) + {𝗐}(t),\ w(t) \sim N(0, q\delta(t - s)) \qquad\qquad(6.33)
```

The initial conditions $`{𝖻}(t_o)`$ and $`\dot{{𝖻}}(t_o)`$ are random constants. It is convenient to write this model as a first-order vector system as follows:

```math
\begin{bmatrix} \dot{{𝖻}}(t) \\ \ddot{{𝖻}}(t) \end{bmatrix} = \begin{bmatrix} \dot{{𝖻}}(t) \\ \dot{{𝖽}}(t) \end{bmatrix} = \begin{bmatrix} 0 & 1 \\ -\omega_n^2 & -2\zeta\omega_n \end{bmatrix} \begin{bmatrix} {𝖻}(t) \\ {𝖽}(t) \end{bmatrix} + \begin{bmatrix} 0 \\ 1 \end{bmatrix} {𝗐}(t) \qquad\qquad(6.34)
```

```math
\dot{{𝘅}}(t) = {𝐀}{𝘅}(t) + {𝐁}{𝗐}(t) \qquad\qquad(6.35)
```

The measurement partial is the same as for the random ramp. The initial condition $`{𝘅}(t_o)`$ is an unbiased random constant vector. Since $`{𝘅}(t_o)`$ and $`{𝗐}(t)`$ are zero-mean, then $`{𝘅}(t)`$ is also zero-mean for all time.

The covariance evolves in time according to

```math
{𝐏}_{{𝘅}}(t) = {𝚽}(t - t_o){𝐏}_{{𝘅}o}{𝚽}^{{𝖳}}(t - t_o) + {𝐒}(t - t_o) \qquad\qquad(6.36)
```

which we can also write in recursive form as

```math
{𝐏}_{{𝘅}}(t + \Delta t) = {𝚽}(\Delta t){𝐏}_{{𝘅}}(t){𝚽}^{{𝖳}}(\Delta t) + {𝐒}(\Delta t) \qquad\qquad(6.37)
```

Thus, we can generate realizations of the SOGM with either $`{𝒙}(t) \sim N({𝟎}, {𝐏}_{{𝘅}}(t))`$ or recursively from

```math
{𝒙}(t + \Delta t) = {𝚽}(\Delta t){𝒙}(t) + {𝝕}(t) \qquad\qquad(6.38)
```

where $`{𝝕}(t) \sim N(0, {𝐒}(\Delta t))`$.

For the underdamped case ($`\zeta \lt 1`$), the state transition matrix and discrete process noise covariance are given by Reference [86](16-bibliography.md#page-173-6):

```math
{𝚽}(t) = \frac{\mathrm{e}^{-\zeta\omega_n t}}{\omega_d} \begin{bmatrix} (\omega_d \cos\omega_d t + \zeta\omega_n \sin\omega_d t) & \sin\omega_d t \\ -\omega_n^2 \sin\omega_d t & (\omega_d \cos\omega_d t - \zeta\omega_n \sin\omega_d t) \end{bmatrix} \qquad\qquad(6.39)
```

and

```math
{𝐒}_{(1,1)}(t) = \frac{q}{4\zeta\omega_n^3} \biggl[ 1 - \frac{\mathrm{e}^{-2\zeta\omega_n t}}{w_d^2} (\omega_d^2 + 2\zeta\omega_n\omega_d \cos\omega_d t \sin\omega_d t + 2\zeta^2\omega_n^2 \sin^2\omega_d t) \biggr] \qquad\qquad(6.40)
```

```math
{𝐒}_{(2,2)}(t) = \frac{q}{4\zeta\omega_n} \biggl[ 1 - \frac{\mathrm{e}^{-2\zeta\omega_n t}}{w_d^2} (\omega_d^2 - 2\zeta\omega_n\omega_d \cos\omega_d t \sin\omega_d t + 2\zeta^2\omega_n^2 \sin^2\omega_d t) \biggr] \qquad\qquad(6.41)
```

```math
{𝐒}_{(1,2)}(t) = \frac{q}{2\omega_d^2}\, \mathrm{e}^{-2\zeta\omega_n t} \sin^2\omega_d t, \qquad\qquad(6.42)
```

```math
{𝐒}_{(2,1)}(t) = {𝐒}_{(1,2)}(t) \qquad\qquad(6.43)
```

where $`\omega_d = \omega_n\sqrt{1 - \zeta^2}`$. In the over-damped case ($`\zeta \gt 1`$), replace $`\sin`$ and $`\cos`$ with $`\sinh`$ and $`\cosh`$, respectively. In the critically-damped case,

```math
{𝚽}(t) = \begin{bmatrix} \mathrm{e}^{-\omega_n t}(1 + \omega_n t) & t\,\mathrm{e}^{-\omega_n t} \\ -\omega_n^2 t\,\mathrm{e}^{-\omega_n t} & \mathrm{e}^{-\omega_n t}(1 - \omega_n t) \end{bmatrix} \qquad\qquad(6.44)
```

and

```math
{𝐒}_{(1,1)}(t) = \frac{q}{4\omega_n^3} \Bigl[ 1 - \mathrm{e}^{-2\omega_n t}(1 + 2\omega_n t + 2\omega_n^2 t^2) \Bigr] \qquad\qquad(6.45)
```

```math
{𝐒}_{(2,2)}(t) = \frac{q}{4\omega_n} \Bigl[ 1 - \mathrm{e}^{-2\omega_n t}(1 - 2\omega_n t + 2\omega_n^2 t^2) \Bigr] \qquad\qquad(6.46)
```

```math
{𝐒}_{(2,1)}(t) = {𝐒}_{(1,2)}(t) = \frac{qt^2}{2}\, \mathrm{e}^{-2\omega_n t} \qquad\qquad(6.47)
```

Note that for any damping ratio, $`\|{𝐏}_{{𝘅}}\|`$ remains finite, since as $`t \to \infty`$,

```math
{𝐏}_{{𝘅}}(t \to \infty) = \frac{q}{4\zeta\omega_n} \begin{bmatrix} 1/\omega_n^2 & 0 \\ 0 & 1 \end{bmatrix}. \qquad\qquad(6.48)
```

Thus, the ratio of the steady-state standard deviations of the bias and drift will be

```math
\frac{\sigma_{{𝖽}}}{\sigma_{{𝖻}}} = \omega_n, \qquad\qquad(6.49)
```

and these are related to the power spectral density by

```math
q = 4\zeta\frac{\sigma_{{𝖽}}^3}{\sigma_{{𝖻}}}. \qquad\qquad(6.50)
```

Hence, we can choose the parameters of the SOGM so that we avoid any overflow, loss of symmetry and/or positive definiteness of $`{𝐏}_{{𝘅}}`$ due to roundoff and/or truncation. For these reasons, the SOGM is recommended as a *best practice* for bias drift modeling in sequential navigation filters.

### 6.2.7. Vasicek Model

A criticism of the FOGM process is that as $`t \to \infty`$, $`\mathrm{E}[b(t)] \to 0`$. In the filtering context, this implies that a data outage that is long relative to the time constant, $`\tau`$, can result in the filter's bias estimate decaying toward zero, which may be undesirable. To address this concern, Seago et al. [[77](16-bibliography.md#page-173-7)] proposed that biases the filter should retain across such outages might be modeled instead with a model proposed by Vasicek [[85](16-bibliography.md#page-173-8)] for modeling interest rates:

<span id="page-78-0"></span>
```math
\dot{{𝖻}}(t) = -\frac{1}{\tau}({𝖻}(t) - b_\infty) + {𝗐}(t), \qquad\qquad(6.51)
```

where, as previously, $`b(t_o) \sim N(0, {𝐏}_{bo})`$, and $`w(t) \sim N(0, q\delta(t - s))`$. A formal solution to [\(6.51\)](#page-78-0) gives

```math
{𝖻}(t) = {𝖻}(t_o)\, \mathrm{e}^{-\frac{t - t_o}{\tau}} + b_\infty\biggl(1 - \mathrm{e}^{-\frac{t - t_o}{\tau}}\biggr) + \int_{t_o}^{t} \mathrm{e}^{-\frac{s}{\tau}}\, {𝗐}(s)\, \mathrm{d}s \qquad\qquad(6.52)
```

Since $`{𝖻}(t_o)`$ and $`{𝗐}(t)`$ are zero-mean, then

```math
\mathrm{E}[{𝖻}(t)] = b_\infty\biggl(1 - \mathrm{e}^{-\frac{t - t_o}{\tau}}\biggr) \qquad\qquad(6.53)
```

and $`\mathrm{E}[{𝖻}(t)] = b_\infty`$ as $`t \to \infty`$. Since $`\mathrm{E}[{𝖻}(t)]^2`$ is subtracted from $`\mathrm{E}\left[{𝖻}(t)^2\right]`$ to get the covariance, the covariance evolves in time identically to the FOGM,

```math
p_{{𝖻}}(t) = \mathrm{e}^{-\frac{2}{\tau}(t - t_o)}\, p_{{𝖻}o} + s(t - t_o) \qquad\qquad(6.54)
```

where as before

```math
s(t - t_o) = \frac{q\tau}{2}\biggl(1 - \mathrm{e}^{-\frac{2}{\tau}(t - t_o)}\biggr) \qquad\qquad(6.55)
```

Thus, to generate a realization of the Vasicek Model at particular time $`t`$, we could generate a realization of the initial bias value, and then at each sample time generate realizations of $`\varpi(t) \sim N(0, s(\Delta t))`$, and recursively add these discrete noise sample increments to the bias sample history as follows:

```math
b(t + \Delta t) = b(t)\, \mathrm{e}^{-\frac{\Delta t}{\tau}} + b_\infty\left(1 - \mathrm{e}^{-\frac{\Delta t}{\tau}}\right) + \varpi(t) \qquad\qquad(6.56)
```

or we could generate a random realization of $`N(0, p_{{𝖻}}(t))`$ and add this to $`b_\infty\biggl(1 - \mathrm{e}^{-\frac{t - t_o}{\tau}}\biggr)`$.

To configure or "tune" the Vasicek model, one chooses the time constant $`\tau`$ and the noise PSD $`q`$ in a manner analogous to the FOGM process; it is less clear how one might choose $`b_\infty`$. Seago et al. [[77](16-bibliography.md#page-173-7)] proposed that $`b_\infty`$ be estimated as a random constant filter state. Casting the Vasicek model into such a two-state form results in the following model:

```math
\begin{bmatrix} \dot{{𝖻}}(t) \\ \dot{{𝖻}}_\infty \end{bmatrix} = \begin{bmatrix} -1/\tau & 1/\tau \\ 0 & 0 \end{bmatrix} \begin{bmatrix} {𝖻}(t) \\ {𝖻}_\infty \end{bmatrix} + \begin{bmatrix} {𝗐}(t) \\ 0 \end{bmatrix}, \qquad\qquad(6.57)
```

which leads to the following state transition matrix and process noise covariance:

```math
{𝚽}(t) = \begin{bmatrix} \mathrm{e}^{-t/\tau} & 1 - \mathrm{e}^{-t/\tau} \\ 0 & 1 \end{bmatrix}, \quad {𝐒}(t) = \begin{bmatrix} \frac{q\tau}{2}\left(1 - \mathrm{e}^{-\frac{2t}{\tau}}\right) & 0 \\ 0 & 0 \end{bmatrix}. \qquad\qquad(6.58)
```

While the Vasicek Model shares with the FOGM the desirable feature that $`p_{{𝖻}} \to q\tau/2`$ as $`t \to \infty`$, in the two-state form just described, it also has the undesirable feature that the variance of $`{𝖻}_\infty`$ goes to zero as $`t \to \infty`$. Modeling $`{𝖻}_\infty`$ with process noise, e.g. as a random walk with PSD of $`q_\infty`$, introduces an unstable integral of the process noise as occurs for the integrated FOGM:

```math
{𝐒}(t) = \begin{bmatrix} q_\infty\left(t - \frac{3\tau}{2} + 2\tau\,\mathrm{e}^{-\frac{t}{\tau}} - \frac{\tau}{2}\,\mathrm{e}^{-\frac{2t}{\tau}}\right) + \frac{q\tau}{2}\left(1 - \mathrm{e}^{-\frac{2t}{\tau}}\right) & q_\infty t - q_\infty\tau\left(1 - \mathrm{e}^{-\frac{t}{\tau}}\right) \\ q_\infty t - q_\infty\tau\left(1 - \mathrm{e}^{-\frac{t}{\tau}}\right) & q_\infty t \end{bmatrix}, \qquad\qquad(6.59)
```

although choosing $`q_\infty`$ appropriately small may mitigate this concern. In any case, retaining a steady-state bias across long data gaps may not always be warranted, depending on the context. And if long measurement gaps are not present, the need to retain such a bias, with the accompanying complexity of maintaining an additional state, may not be necessary. We will consider further such multi-input bias models in the sequel.

---

[← Chapter 5. Measurement Underweighting](05-measurement-underweighting.md) · [Contents](README.md) · [Chapter 6. Bias Modeling (part 2 of 2) →](06-bias-modeling-part2.md)
