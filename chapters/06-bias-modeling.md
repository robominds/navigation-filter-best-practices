[← Chapter 5. Measurement Underweighting](05-measurement-underweighting.md) · [Contents](README.md) · [Chapter 7. State Representations →](07-state-representations.md)

# Chapter 6. Bias Modeling

*Contributed by J. Russell Carpenter*

<span id="page-72-0"></span>A general model for a measurement error is as follows:

$$
\mathsf{e} = \mathsf{b} + \mathsf{v} \tag{6.1}
$$

where $\mathsf{b}$ models the systematic errors, and $\mathsf{v}$ models the measurement noise. We assume that the measurement noise is a discrete sequence of uncorrelated random numbers. Variables such as $\mathsf{v}$ are known as random variables, and Appendix [A](13-appendix-a-models-and-realizations-of-random-variables.md#page-146-0) describes how to model them. This Chapter describes models for the systematic errors.

The discussion of systematic errors treats such errors as scalar quantities to simplify the exposition; generalization to the vector case is straightforward. Note that if the measurement is nonscalar, but the errors in the component measurements are independent of one another, then we can model each measurement independently, so modeling the biases as a vector is not required. If the measurement errors are not independent, then many estimators require that we apply a transformation to the data prior to processing so that the data input to the estimator have independent measurement errors; Appendix [A](13-appendix-a-models-and-realizations-of-random-variables.md#page-146-0) describes some ways to accomplish this transformation.

## 6.1. Zero-Input Bias State Models

<span id="page-72-1"></span>The simplest non-zero measurement error consists only of measurement noise. The next simplest class of measurement errors consists of biases which are either themselves constant, or are the integrals of constants. We can view such biases as the output of a system which has zero inputs, and which may have internal states. In the sequel, we will consider cases where there are random inputs to the system.

In cases where the bias is the output of a system with internal states, the estimator may treat the internal states as solve-for or consider parameters. In such cases, the estimator requires a measurement partials matrix. Otherwise, the "measurement partial" is just $H = \partial b/\partial b = 1$.

### 6.1.1. Random Constant

The simplest type of systematic error is a constant bias on the measurement. There are two types of such biases: deterministic constants, which are truly constant for all time, and random constants, which are constant or very nearly so over a particular time of interest. For example, each time a sensor is power-cycled, a bias associated with it may change in value, but so long as the sensor remains powered on, the bias will not change.

In some cases, we may have reason to believe that a particular systematic error source truly is a deterministic bias, but due to limited observability, we do not have knowledge of its true value. In such cases, we may view our estimate of the bias as a random constant, and its variance as a measure of the imprecision of our knowledge.

Thus, we may view all constants that could be solve-for or consider parameters in orbit determination as random constants. A model for a random constant is

$$
\dot{\mathsf{b}}(t) = 0,\ b(t_o) \sim N(0, p_{\mathsf{b}o}). \tag{6.2}
$$

Thus the unconditional mean of $\mathsf{b}(t)$ is zero for all time, and its unconditional covariance is constant for all time as well. If $\mathsf{b}(t)$ is a filter solve-for variable that is observable, then its covariance conditioned on the measurement sequence will reach zero in the limit as $t \to \infty$. This is an undesirable characteristic for application in a sequential navigation filter.

To simulate a realization of the random constant, we need only generate a random number according to $N(0, p_{\mathsf{b}o})$, as the previous subsection described.

### 6.1.2. Random Ramp

The random ramp model assumes that the rate of change of the bias is itself a random constant; thus the random ramp model is

$$
\ddot{\mathsf{b}}(t) = 0,\ \dot{b}(t_o) \sim N(0, p_{\dot{\mathsf{b}}o}). \tag{6.3}
$$

Thus, the initial condition $\dot{\mathsf{b}}(t_o)$ is a random constant. For a pure random ramp, the initial condition on $\mathsf{b}(t_o)$ and its covariance are taken to be zero, but an obvious and common generalization is to allow $\mathsf{b}(t_o)$ to also be a random constant.

It is convenient to write this model as a first-order vector system as follows:

$$
\begin{bmatrix} \dot{\mathsf{b}}(t) \\ \ddot{\mathsf{b}}(t) \end{bmatrix} = \begin{bmatrix} \dot{\mathsf{b}}(t) \\ \dot{\mathsf{d}}(t) \end{bmatrix} = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix} \begin{bmatrix} \mathsf{b}(t) \\ \mathsf{d}(t) \end{bmatrix} \tag{6.4}
$$

$$
\dot{\boldsymbol{\mathsf{x}}}(t) = \mathbf{A}\boldsymbol{\mathsf{x}}(t) \tag{6.5}
$$

where $\mathsf{d}(t) = \dot{\mathsf{b}}(t)$. The resulting output equation for the total measurement error is

$$
\mathsf{e} = \begin{bmatrix} 1 & 0 \end{bmatrix} \boldsymbol{\mathsf{x}} + \mathsf{v} \tag{6.6}
$$

$$
= \mathbf{H}\boldsymbol{\mathsf{x}} + \mathsf{v} \tag{6.7}
$$

Note that the ensemble of realizations of $\boldsymbol{\mathsf{x}}(t)$ has zero-mean for all time. The unconditional covariance evolves in time according to

$$
\mathbf{P}_{\boldsymbol{\mathsf{x}}}(t) = \boldsymbol{\Phi}(t - t_o)\mathbf{P}_{\boldsymbol{\mathsf{x}}o}\boldsymbol{\Phi}^{\mathsf{T}}(t - t_o) \tag{6.8}
$$

where

$$
\boldsymbol{\Phi}(t) = \begin{bmatrix} 1 & t \\ 0 & 1 \end{bmatrix} \text{ and } \mathbf{P}_{\boldsymbol{\mathsf{x}}o} = \begin{bmatrix} p_{\mathsf{b}o} & 0 \\ 0 & p_{\dot{\mathsf{b}}o} \end{bmatrix} \tag{6.9}
$$

which we can also write in recursive form as

$$
\mathbf{P}_{\boldsymbol{\mathsf{x}}}(t + \Delta t) = \boldsymbol{\Phi}(\Delta t)\mathbf{P}_{\boldsymbol{\mathsf{x}}}(t)\boldsymbol{\Phi}^{\mathsf{T}}(\Delta t) \tag{6.10}
$$

Thus, we can generate realizations of the random ramp with either $\boldsymbol{x}(t) \sim N(\mathbf{0}, \mathbf{P}_{\boldsymbol{\mathsf{x}}}(t))$ or recursively from

$$
\boldsymbol{x}(t + \Delta t) = \boldsymbol{\Phi}(\Delta t)\boldsymbol{x}(t) \tag{6.11}
$$

Note that the norm of the unconditional covariance becomes infinite as $t^2$ becomes infinite. This could lead to an overflow of the representation of the covariance in a computer program if the propagation time between measurements is large, if the bias is unobservable, or if the bias is a consider parameter, and could also lead to the representation of the covariance losing either its symmetry and/or its positive definiteness due to roundoff and/or truncation. If the bias and drift are filter solve-for variables, then the norm of their covariance conditioned on the measurement sequence will reach zero in the limit as $t \to \infty$. These are all undesirable characteristics for application in a sequential navigation filter.

### <span id="page-74-2"></span>6.1.3. Higher-Order Derivatives of Random Constants

In principle, a random constant may be associated with any derivative of the bias in a straightforward extension of the models above. In practice, it is rare to need more than two or three derivatives. Conventional terminology does not appear in the literature for derivatives of higher order than the random ramp. The slope of the bias is most commonly described as the "bias drift," so that a "drift random ramp" would be one way to describe a bias whose second derivative is a random constant. The measurement partials matrix needs to be accordingly padded with trailing zeros for the derivatives of the bias in such cases.

## 6.2. Single-Input Bias State Models

<span id="page-74-0"></span>The simplest non-constant systematic errors are systems with a single input that is a random process. We can think of a random process as the result of some kind of limit in which the intervals between an uncorrelated sequence of random variables get infinitesimally small. In this limit, each random increment instantaneously perturbs the sequence, so that the resulting process is continuous but non-differentiable. We call this kind of a random input "process noise."

Although such random processes are non-differentiable, there are various techniques for generalizing the concept of integration so that something like integrals of the process noise exist, and hence so do the differentials that appear under the integral signs. It turns out that so long as any coefficients of the process noise are non-random, these differentials behave for all practical purposes as if they were differentiable.

### 6.2.1. Random Walk

The random walk is the simplest random process of the type described above. In terms of the "formal derivatives" mentioned above, the random walk model for a measurement bias is

$$
\dot{\mathsf{b}}(t) = \mathsf{w}(t),\ w(t) \sim N(0, q\delta(t - s)) \tag{6.12}
$$

The input noise process on the right hand side is known as "white noise," and the Dirac delta function that appears in the expression for its variance indicates that the white noise process consists of something like an infinitely-tightly spaced set of impulses. The term $q$ that appears along with the delta function is the intensity of each impulse[<sup>1</sup>](#page-74-1). The initial condition $\mathsf{b}(t_o)$ is an unbiased random constant. Since $\mathsf{b}(t_o)$ and $\mathsf{w}(t)$ are zero-mean, then $\mathsf{b}(t)$ is also zero-mean for all time. The unconditional variance of $\mathsf{b}$ evolves in time according to

$$
p_{\mathsf{b}}(t) = p_{\mathsf{b}o} + q(t - t_o) \tag{6.13}
$$

which we can also write in recursive form as

$$
p_{\mathsf{b}}(t + \Delta t) = p_{\mathsf{b}}(t) + q\Delta t \tag{6.14}
$$

Thus, to generate a realization of the random walk at time $t$, we need only generate a random number according to $N(0, p_{\mathsf{b}}(t))$. Equivalently, we could also generate realizations of $\varpi(t) \sim N(0, q\Delta t)$, and recursively add these discrete noise increments to the bias as follows:

$$
b(t + \Delta t) = b(t) + \varpi(t) \tag{6.15}
$$

Note that the unconditional variance becomes infinite as $t$ becomes infinite. This could lead to an overflow of the representation of $p_{\mathsf{b}}$ if $q$ is large in the following circumstances: in a long gap between measurements, if the bias is unobservable, or if the bias is a consider parameter. These are all somewhat undesirable characteristics for application in a sequential navigation filter. However, because the process is persistently stimulated by the input, its variance conditioned on a measurement history will remain positive for all time. Hence the random walk finds frequent application in sequential navigation filters, particularly when continuous measurements from which the bias is observable are generally available, such as often occurs for GPS data.

<span id="page-74-1"></span><sup>1</sup> Another way to imagine the input sequence, in terms of a frequency domain interpretation, is that it is a noise process whose power spectral density, $q$, is non-zero at all frequencies, which implies infinite bandwidth.

### 6.2.2. Random Run

The random run model assumes that the rate of change of the bias is itself a random walk; thus the random run model is

$$
\ddot{\mathsf{b}}(t) = \mathsf{w}(t),\ w(t) \sim N(0, q\delta(t - s)) \tag{6.16}
$$

The initial condition $\dot{\mathsf{b}}(t_o)$ is a random constant. For a pure random run, the initial condition on $\mathsf{b}(t_o)$ and its covariance are taken to be zero, but an obvious and common generalization is to allow $\mathsf{b}(t_o)$ to also be a random constant.

It is convenient to write this model as a first-order vector system as follows:

$$
\begin{bmatrix} \dot{\mathsf{b}}(t) \\ \ddot{\mathsf{b}}(t) \end{bmatrix} = \begin{bmatrix} \dot{\mathsf{b}}(t) \\ \dot{\mathsf{d}}(t) \end{bmatrix} = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix} \begin{bmatrix} \mathsf{b}(t) \\ \mathsf{d}(t) \end{bmatrix} + \begin{bmatrix} 0 \\ 1 \end{bmatrix} \mathsf{w}(t) \tag{6.17}
$$

$$
\dot{\boldsymbol{\mathsf{x}}}(t) = \mathbf{A}\boldsymbol{\mathsf{x}}(t) + \mathbf{B}\mathsf{w}(t) \tag{6.18}
$$

The measurement partial is the same as for the random ramp. The initial condition $\boldsymbol{\mathsf{x}}(t_o)$ is an unbiased random constant. Since $\boldsymbol{\mathsf{x}}(t_o)$ and $\mathsf{w}(t)$ are zero-mean, then $\boldsymbol{\mathsf{x}}(t)$ is also zero-mean for all time. The covariance evolves in time according to

$$
\mathbf{P}_{\boldsymbol{\mathsf{x}}}(t) = \boldsymbol{\Phi}(t - t_o)\mathbf{P}_{\boldsymbol{\mathsf{x}}o}\boldsymbol{\Phi}^{\mathsf{T}}(t - t_o) + \mathbf{S}(t - t_o) \tag{6.19}
$$

where

$$
\boldsymbol{\Phi}(t - t_o) = \begin{bmatrix} 1 & t \\ 0 & 1 \end{bmatrix} \text{ and } \mathbf{P}_{\boldsymbol{\mathsf{x}}o} = \begin{bmatrix} p_{\mathsf{b}o} & 0 \\ 0 & p_{\dot{\mathsf{b}}o} \end{bmatrix} \tag{6.20}
$$

and

$$
\mathbf{S}(t) = q \begin{bmatrix} t^3/3 & t^2/2 \\ t^2/2 & t \end{bmatrix} \tag{6.21}
$$

which we can also write in recursive form as

$$
\mathbf{P}_{\boldsymbol{\mathsf{x}}}(t + \Delta t) = \boldsymbol{\Phi}(\Delta t)\mathbf{P}_{\boldsymbol{\mathsf{x}}}(t)\boldsymbol{\Phi}^{\mathsf{T}}(\Delta t) + \mathbf{S}(\Delta t) \tag{6.22}
$$

Thus, we can generate realizations of the random run with either $\boldsymbol{x}(t) \sim N(\mathbf{0}, \mathbf{P}_{\boldsymbol{\mathsf{x}}(t)})$ or recursively from

$$
\boldsymbol{x}(t + \Delta t) = \boldsymbol{\Phi}(\Delta t)\boldsymbol{x}(t) + \boldsymbol{\varpi}(t) \tag{6.23}
$$

where $\boldsymbol{\varpi}(t) \sim N(\mathbf{0}, \mathbf{S}(\Delta t))$ is a noise sample *vector* arising from formal integration of the scalar noise input process over the sample time. A Cholesky decomposition of $\mathbf{S}(t)$ useful for sampling is

$$
{}^{C}\!\sqrt{\mathbf{S}(t)} = \begin{bmatrix} \sqrt{3t^3}/3 & 0 \\ \sqrt{3t}/2 & \sqrt{t}/2 \end{bmatrix} \tag{6.24}
$$

Note that the norm of the unconditional covariance becomes infinite as $t^3$ becomes infinite, and the process is persistently stimulated by the input, so its covariance conditioned on a measurement history will remain positive definite for all time. Hence, the random run shares similar considerations with the random walk for application in sequential navigation filters.

### 6.2.3. Higher-Order Derivatives of Random Walks

In principle, a random walk may be associated with any derivative of the bias in a straightforward extension of the models above. In practice, it is rare to need more than two or three derivatives. Conventional terminology does not appear in the literature for derivatives of higher order than the random run. A "drift random run" would be one way to describe a bias whose second derivative is a random walk. Below, we will refer to such a model as a "random zoom."

### <span id="page-76-1"></span>6.2.4. First-Order Gauss-Markov

The first-order Gauss-Markov (FOGM) process is one of the simplest random processes that introduces time correlation between samples. In terms of a frequency domain interpretation, we can view it as white noise passed through a low-pass filter. Since such noise, often called "colored noise," has finite bandwidth, it is physically realizable, unlike white noise. In the notation of formal derivatives, the FOGM model is

$$
\dot{\mathsf{b}}(t) = -\frac{1}{\tau}\mathsf{b}(t) + \mathsf{w}(t), \tag{6.25}
$$

where, as with the random walk, $b(t_o) \sim N(0, p_{bo})$, and $w(t) \sim N(0, q\delta(t-s))$. The time constant, $\tau$ gives the correlation time, or the time over which the intensity of the time correlation will fade to $1/\mathrm{e}$ of its prior value[<sup>2</sup>](#page-76-0). Note that as $\tau \to \infty$, the FOGM approximates a random walk.

<span id="page-76-0"></span><sup>2</sup> One sometimes sees $\tau$ described as the "half-life," but since $1/\mathrm{e} < 1/2$, this is not an accurate label.

Since $\mathsf{b}(t_o)$ and $\mathsf{w}(t)$ are zero-mean, then $\mathsf{b}(t)$ is also zero-mean for all time. The covariance evolves in time according to

$$
p_{\mathsf{b}}(t) = \mathrm{e}^{-\frac{2}{\tau}(t - t_o)}\, p_{\mathsf{b}o} + s(t - t_o) \tag{6.26}
$$

where

$$
s(t - t_o) = \frac{q\tau}{2}\left(1 - \mathrm{e}^{-\frac{2}{\tau}(t - t_o)}\right) \tag{6.27}
$$

which we can also write in recursive form as

$$
p_{\mathsf{b}}(t + \Delta t) = \mathrm{e}^{-\frac{2\Delta t}{\tau}}\, p_{\mathsf{b}}(t) + s(\Delta t) \tag{6.28}
$$

Thus, to generate discrete samples of a particular realization of the FOGM, we can either generate samples from $b(t) \sim N(0, p_{\mathsf{b}}(t))$, or generate a realization of the initial bias value, and then at each sample time generate realizations of $\varpi(t) \sim N(0, s(\Delta t))$, and recursively add these discrete noise sample increments to the bias sample history as follows:

$$
b(t + \Delta t) = \mathrm{e}^{-\frac{\Delta t}{\tau}}\, b(t) + \varpi(t) \tag{6.29}
$$

Note that $p_{\mathsf{b}}$ approaches a finite steady-state value equal to $q\tau/2$ as $t$ becomes infinite. One can choose the parameters of the FOGM so that this steady-state value avoids any overflow of the representation of $p_{\mathsf{b}}$ in a computer program, and such that the FOGM's covariance evolution prior to reaching steady-state closely mimics that of a random walk. For these reasons, the FOGM is recommended as a *best practice* for bias modeling in sequential navigation filters.

### 6.2.5. Integrated First-Order Gauss-Markov Model

As with the random walk and random constant models, any number of derivatives of the bias may be associated with a FOGM process. However, integration of the FOGM destroys its stability. For example, the singly integrated first-order Gauss-Markov model is given by

$$
\begin{bmatrix} \dot{\mathsf{b}}(t) \\ \dot{\mathsf{d}}(t) \end{bmatrix} = \begin{bmatrix} 0 & 1 \\ 0 & -1/\tau \end{bmatrix} \begin{bmatrix} \mathsf{b}(t) \\ \mathsf{d}(t) \end{bmatrix} + \begin{bmatrix} 0 \\ \mathsf{w}(t) \end{bmatrix}, \tag{6.30}
$$

which leads to the following state transition matrix,

$$
\boldsymbol{\Phi}(t) = \begin{bmatrix} 1 & \tau\left(1 - \mathrm{e}^{-t/\tau}\right) \\ 0 & \mathrm{e}^{-t/\tau} \end{bmatrix}, \tag{6.31}
$$

and process noise covariance[<sup>3</sup>](#page-77-0),

<span id="page-77-1"></span>
$$
\mathbf{S}(t) = \frac{q\tau}{2} \begin{bmatrix} \tau^2\left\{\left(1 - \mathrm{e}^{-2t/\tau}\right) - 4\left(1 - \mathrm{e}^{-t/\tau}\right) + 2t/\tau\right\} & \tau\left(1 - \mathrm{e}^{-t/\tau}\right)^2 \\ \tau\left(1 - \mathrm{e}^{-t/\tau}\right)^2 & \left(1 - \mathrm{e}^{-2t/\tau}\right) \end{bmatrix}. \tag{6.32}
$$

<span id="page-77-0"></span><sup>3</sup> Note that [\(6.32\)](#page-77-1) corrects an error in Reference [14](16-bibliography.md#page-170-14).

Clearly, this is an unstable model, as the bias variance increases linearly with elapsed time. As an alternative, the following second-order model is available.

### 6.2.6. Second-Order Gauss-Markov

The model for a second-order Gauss-Markov (SOGM) random process is

$$
\ddot{\mathsf{b}}(t) = -2\zeta\omega_n\dot{\mathsf{b}}(t) - \omega_n^2\mathsf{b}(t) + \mathsf{w}(t),\ w(t) \sim N(0, q\delta(t - s)) \tag{6.33}
$$

The initial conditions $\mathsf{b}(t_o)$ and $\dot{\mathsf{b}}(t_o)$ are random constants. It is convenient to write this model as a first-order vector system as follows:

$$
\begin{bmatrix} \dot{\mathsf{b}}(t) \\ \ddot{\mathsf{b}}(t) \end{bmatrix} = \begin{bmatrix} \dot{\mathsf{b}}(t) \\ \dot{\mathsf{d}}(t) \end{bmatrix} = \begin{bmatrix} 0 & 1 \\ -\omega_n^2 & -2\zeta\omega_n \end{bmatrix} \begin{bmatrix} \mathsf{b}(t) \\ \mathsf{d}(t) \end{bmatrix} + \begin{bmatrix} 0 \\ 1 \end{bmatrix} \mathsf{w}(t) \tag{6.34}
$$

$$
\dot{\boldsymbol{\mathsf{x}}}(t) = \mathbf{A}\boldsymbol{\mathsf{x}}(t) + \mathbf{B}\mathsf{w}(t) \tag{6.35}
$$

The measurement partial is the same as for the random ramp. The initial condition $\boldsymbol{\mathsf{x}}(t_o)$ is an unbiased random constant vector. Since $\boldsymbol{\mathsf{x}}(t_o)$ and $\mathsf{w}(t)$ are zero-mean, then $\boldsymbol{\mathsf{x}}(t)$ is also zero-mean for all time.

The covariance evolves in time according to

$$
\mathbf{P}_{\boldsymbol{\mathsf{x}}}(t) = \boldsymbol{\Phi}(t - t_o)\mathbf{P}_{\boldsymbol{\mathsf{x}}o}\boldsymbol{\Phi}^{\mathsf{T}}(t - t_o) + \mathbf{S}(t - t_o) \tag{6.36}
$$

which we can also write in recursive form as

$$
\mathbf{P}_{\boldsymbol{\mathsf{x}}}(t + \Delta t) = \boldsymbol{\Phi}(\Delta t)\mathbf{P}_{\boldsymbol{\mathsf{x}}}(t)\boldsymbol{\Phi}^{\mathsf{T}}(\Delta t) + \mathbf{S}(\Delta t) \tag{6.37}
$$

Thus, we can generate realizations of the SOGM with either $\boldsymbol{x}(t) \sim N(\mathbf{0}, \mathbf{P}_{\boldsymbol{\mathsf{x}}}(t))$ or recursively from

$$
\boldsymbol{x}(t + \Delta t) = \boldsymbol{\Phi}(\Delta t)\boldsymbol{x}(t) + \boldsymbol{\varpi}(t) \tag{6.38}
$$

where $\boldsymbol{\varpi}(t) \sim N(0, \mathbf{S}(\Delta t))$.

For the underdamped case ($\zeta < 1$), the state transition matrix and discrete process noise covariance are given by Reference [86](16-bibliography.md#page-173-6):

$$
\boldsymbol{\Phi}(t) = \frac{\mathrm{e}^{-\zeta\omega_n t}}{\omega_d} \begin{bmatrix} (\omega_d \cos\omega_d t + \zeta\omega_n \sin\omega_d t) & \sin\omega_d t \\ -\omega_n^2 \sin\omega_d t & (\omega_d \cos\omega_d t - \zeta\omega_n \sin\omega_d t) \end{bmatrix} \tag{6.39}
$$

and

$$
\mathbf{S}_{(1,1)}(t) = \frac{q}{4\zeta\omega_n^3} \left[ 1 - \frac{\mathrm{e}^{-2\zeta\omega_n t}}{w_d^2} (\omega_d^2 + 2\zeta\omega_n\omega_d \cos\omega_d t \sin\omega_d t + 2\zeta^2\omega_n^2 \sin^2\omega_d t) \right] \tag{6.40}
$$

$$
\mathbf{S}_{(2,2)}(t) = \frac{q}{4\zeta\omega_n} \left[ 1 - \frac{\mathrm{e}^{-2\zeta\omega_n t}}{w_d^2} (\omega_d^2 - 2\zeta\omega_n\omega_d \cos\omega_d t \sin\omega_d t + 2\zeta^2\omega_n^2 \sin^2\omega_d t) \right] \tag{6.41}
$$

$$
\mathbf{S}_{(1,2)}(t) = \frac{q}{2\omega_d^2}\, \mathrm{e}^{-2\zeta\omega_n t} \sin^2\omega_d t, \tag{6.42}
$$

$$
\mathbf{S}_{(2,1)}(t) = \mathbf{S}_{(1,2)}(t) \tag{6.43}
$$

where $\omega_d = \omega_n\sqrt{1 - \zeta^2}$. In the over-damped case ($\zeta > 1$), replace $\sin$ and $\cos$ with $\sinh$ and $\cosh$, respectively. In the critically-damped case,

$$
\boldsymbol{\Phi}(t) = \begin{bmatrix} \mathrm{e}^{-\omega_n t}(1 + \omega_n t) & t\,\mathrm{e}^{-\omega_n t} \\ -\omega_n^2 t\,\mathrm{e}^{-\omega_n t} & \mathrm{e}^{-\omega_n t}(1 - \omega_n t) \end{bmatrix} \tag{6.44}
$$

and

$$
\mathbf{S}_{(1,1)}(t) = \frac{q}{4\omega_n^3} \left[ 1 - \mathrm{e}^{-2\omega_n t}(1 + 2\omega_n t + 2\omega_n^2 t^2) \right] \tag{6.45}
$$

$$
\mathbf{S}_{(2,2)}(t) = \frac{q}{4\omega_n} \left[ 1 - \mathrm{e}^{-2\omega_n t}(1 - 2\omega_n t + 2\omega_n^2 t^2) \right] \tag{6.46}
$$

$$
\mathbf{S}_{(2,1)}(t) = \mathbf{S}_{(1,2)}(t) = \frac{qt^2}{2}\, \mathrm{e}^{-2\omega_n t} \tag{6.47}
$$

Note that for any damping ratio, $\|\mathbf{P}_{\boldsymbol{\mathsf{x}}}\|$ remains finite, since as $t \to \infty$,

$$
\mathbf{P}_{\boldsymbol{\mathsf{x}}}(t \to \infty) = \frac{q}{4\zeta\omega_n} \begin{bmatrix} 1/\omega_n^2 & 0 \\ 0 & 1 \end{bmatrix}. \tag{6.48}
$$

Thus, the ratio of the steady-state standard deviations of the bias and drift will be

$$
\frac{\sigma_{\mathsf{d}}}{\sigma_{\mathsf{b}}} = \omega_n, \tag{6.49}
$$

and these are related to the power spectral density by

$$
q = 4\zeta\frac{\sigma_{\mathsf{d}}^3}{\sigma_{\mathsf{b}}}. \tag{6.50}
$$

Hence, we can choose the parameters of the SOGM so that we avoid any overflow, loss of symmetry and/or positive definiteness of $\mathbf{P}_{\boldsymbol{\mathsf{x}}}$ due to roundoff and/or truncation. For these reasons, the SOGM is recommended as a *best practice* for bias drift modeling in sequential navigation filters.

### 6.2.7. Vasicek Model

A criticism of the FOGM process is that as $t \to \infty$, $\mathrm{E}[b(t)] \to 0$. In the filtering context, this implies that a data outage that is long relative to the time constant, $\tau$, can result in the filter's bias estimate decaying toward zero, which may be undesirable. To address this concern, Seago et al. [[77](16-bibliography.md#page-173-7)] proposed that biases the filter should retain across such outages might be modeled instead with a model proposed by Vasicek [[85](16-bibliography.md#page-173-8)] for modeling interest rates:

<span id="page-78-0"></span>
$$
\dot{\mathsf{b}}(t) = -\frac{1}{\tau}(\mathsf{b}(t) - b_\infty) + \mathsf{w}(t), \tag{6.51}
$$

where, as previously, $b(t_o) \sim N(0, \mathbf{P}_{bo})$, and $w(t) \sim N(0, q\delta(t - s))$. A formal solution to [\(6.51\)](#page-78-0) gives

$$
\mathsf{b}(t) = \mathsf{b}(t_o)\, \mathrm{e}^{-\frac{t - t_o}{\tau}} + b_\infty\left(1 - \mathrm{e}^{-\frac{t - t_o}{\tau}}\right) + \int_{t_o}^{t} \mathrm{e}^{-\frac{s}{\tau}}\, \mathsf{w}(s)\, \mathrm{d}s \tag{6.52}
$$

Since $\mathsf{b}(t_o)$ and $\mathsf{w}(t)$ are zero-mean, then

$$
\mathrm{E}[\mathsf{b}(t)] = b_\infty\left(1 - \mathrm{e}^{-\frac{t - t_o}{\tau}}\right) \tag{6.53}
$$

and $\mathrm{E}[\mathsf{b}(t)] = b_\infty$ as $t \to \infty$. Since $\mathrm{E}[\mathsf{b}(t)]^2$ is subtracted from $\mathrm{E}\left[\mathsf{b}(t)^2\right]$ to get the covariance, the covariance evolves in time identically to the FOGM,

$$
p_{\mathsf{b}}(t) = \mathrm{e}^{-\frac{2}{\tau}(t - t_o)}\, p_{\mathsf{b}o} + s(t - t_o) \tag{6.54}
$$

where as before

$$
s(t - t_o) = \frac{q\tau}{2}\left(1 - \mathrm{e}^{-\frac{2}{\tau}(t - t_o)}\right) \tag{6.55}
$$

Thus, to generate a realization of the Vasicek Model at particular time $t$, we could generate a realization of the initial bias value, and then at each sample time generate realizations of $\varpi(t) \sim N(0, s(\Delta t))$, and recursively add these discrete noise sample increments to the bias sample history as follows:

$$
b(t + \Delta t) = b(t)\, \mathrm{e}^{-\frac{\Delta t}{\tau}} + b_\infty\left(1 - \mathrm{e}^{-\frac{\Delta t}{\tau}}\right) + \varpi(t) \tag{6.56}
$$

or we could generate a random realization of $N(0, p_{\mathsf{b}}(t))$ and add this to $b_\infty\left(1 - \mathrm{e}^{-\frac{t - t_o}{\tau}}\right)$.

To configure or "tune" the Vasicek model, one chooses the time constant $\tau$ and the noise PSD $q$ in a manner analogous to the FOGM process; it is less clear how one might choose $b_\infty$. Seago et al. [[77](16-bibliography.md#page-173-7)] proposed that $b_\infty$ be estimated as a random constant filter state. Casting the Vasicek model into such a two-state form results in the following model:

$$
\begin{bmatrix} \dot{\mathsf{b}}(t) \\ \dot{\mathsf{b}}_\infty \end{bmatrix} = \begin{bmatrix} -1/\tau & 1/\tau \\ 0 & 0 \end{bmatrix} \begin{bmatrix} \mathsf{b}(t) \\ \mathsf{b}_\infty \end{bmatrix} + \begin{bmatrix} \mathsf{w}(t) \\ 0 \end{bmatrix}, \tag{6.57}
$$

which leads to the following state transition matrix and process noise covariance:

$$
\boldsymbol{\Phi}(t) = \begin{bmatrix} \mathrm{e}^{-t/\tau} & 1 - \mathrm{e}^{-t/\tau} \\ 0 & 1 \end{bmatrix}, \quad \mathbf{S}(t) = \begin{bmatrix} \frac{q\tau}{2}\left(1 - \mathrm{e}^{-\frac{2t}{\tau}}\right) & 0 \\ 0 & 0 \end{bmatrix}. \tag{6.58}
$$

While the Vasicek Model shares with the FOGM the desirable feature that $p_{\mathsf{b}} \to q\tau/2$ as $t \to \infty$, in the two-state form just described, it also has the undesirable feature that the variance of $\mathsf{b}_\infty$ goes to zero as $t \to \infty$. Modeling $\mathsf{b}_\infty$ with process noise, e.g. as a random walk with PSD of $q_\infty$, introduces an unstable integral of the process noise as occurs for the integrated FOGM:

$$
\mathbf{S}(t) = \begin{bmatrix} q_\infty\left(t - \frac{3\tau}{2} + 2\tau\,\mathrm{e}^{-\frac{t}{\tau}} - \frac{\tau}{2}\,\mathrm{e}^{-\frac{2t}{\tau}}\right) + \frac{q\tau}{2}\left(1 - \mathrm{e}^{-\frac{2t}{\tau}}\right) & q_\infty t - q_\infty\tau\left(1 - \mathrm{e}^{-\frac{t}{\tau}}\right) \\ q_\infty t - q_\infty\tau\left(1 - \mathrm{e}^{-\frac{t}{\tau}}\right) & q_\infty t \end{bmatrix}, \tag{6.59}
$$

although choosing $q_\infty$ appropriately small may mitigate this concern. In any case, retaining a steady-state bias across long data gaps may not always be warranted, depending on the context. And if long measurement gaps are not present, the need to retain such a bias, with the accompanying complexity of maintaining an additional state, may not be necessary. We will consider further such multi-input bias models in the sequel.

## 6.3. Multi-Input Bias State Models

<span id="page-79-0"></span>We may combine any of the above models to create multi-input bias models; for example the bias could be a second-order Gauss-Markov, and the bias rate could be a first-order Gauss-Markov. In practice, the most useful combinations have been found to be the following.

### 6.3.1. Bias and Drift Random Walks (Random Walk + Random Run)

A common model for biases in clocks, gyros, and accelerometers is that the bias is driven by both its own white noise input, and also by the integral of the white noise of its drift. Such models derive from observations that the error magnitudes of these devices depend on the time scale over which the device is observed. They are often characterized by Allan deviation specifications, which may be heuristically associated with the white noise power spectral densities. The model is as follows:

$$
\begin{bmatrix} \dot{\mathsf{b}}(t) \\ \dot{\mathsf{d}}(t) \end{bmatrix} = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix} \begin{bmatrix} \mathsf{b}(t) \\ \mathsf{d}(t) \end{bmatrix} + \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix} \begin{bmatrix} \mathsf{w}_{\mathsf{b}}(t) \\ \mathsf{w}_{\mathsf{d}}(t) \end{bmatrix} \tag{6.60}
$$

$$
\dot{\boldsymbol{\mathsf{x}}}(t) = \mathbf{A}\boldsymbol{\mathsf{x}}(t) + \mathbf{B}\boldsymbol{\mathsf{w}}(t) \tag{6.61}
$$

The measurement partial is the same as for the random ramp. The initial condition $\boldsymbol{\mathsf{x}}(t_o)$ is an unbiased random constant. Since $\boldsymbol{\mathsf{x}}(t_o)$ and $\boldsymbol{\mathsf{w}}(t)$ are zero-mean, then $\boldsymbol{\mathsf{x}}(t)$ is also zero-mean for all time. The covariance evolves in time according to

$$
\mathbf{P}_{\boldsymbol{\mathsf{x}}}(t) = \boldsymbol{\Phi}(t - t_o)\mathbf{P}_{\boldsymbol{\mathsf{x}}o}\boldsymbol{\Phi}^{\mathsf{T}}(t - t_o) + \mathbf{S}(t - t_o) \tag{6.62}
$$

where

$$
\boldsymbol{\Phi}(t) = \begin{bmatrix} 1 & t \\ 0 & 1 \end{bmatrix} \text{ and } \mathbf{P}_{\boldsymbol{\mathsf{x}}o} = \begin{bmatrix} p_{\mathsf{b}o} & 0 \\ 0 & p_{\dot{\mathsf{b}}o} \end{bmatrix} \tag{6.63}
$$

and

$$
\mathbf{S}(t) = \begin{bmatrix} q_{\mathsf{b}}t + q_{\mathsf{d}}t^3/3 & q_{\mathsf{d}}t^2/2 \\ q_{\mathsf{d}}t^2/2 & q_{\mathsf{d}}t \end{bmatrix} \tag{6.64}
$$

which we can also write in recursive form as

$$
\mathbf{P}_x(t + \Delta t) = \boldsymbol{\Phi}(\Delta t)\mathbf{P}_x(t)\boldsymbol{\Phi}^{\mathsf{T}}(\Delta t) + \mathbf{S}(\Delta t) \tag{6.65}
$$

Thus, we can generate realizations of the random run with either $\boldsymbol{x}(t) \sim N(\mathbf{0}, \mathbf{P}_{\boldsymbol{\mathsf{x}}}(t))$ or recursively from

$$
\boldsymbol{x}(t + \Delta t) = \boldsymbol{\Phi}(\Delta t)\boldsymbol{x}(t) + \boldsymbol{\varpi}(t) \tag{6.66}
$$

where $\boldsymbol{\varpi}(t) \sim N(0, \mathbf{S}(\Delta t))$. Note that a Cholesky decomposition of $\mathbf{S}(t)$ is

$$
{}^{C}\!\sqrt{\mathbf{S}(t)} = \begin{bmatrix} \sqrt{q_{\mathsf{b}}t + q_{\mathsf{d}}t^3/12} & \sqrt{q_{\mathsf{d}}t^3}/2 \\ 0 & \sqrt{q_{\mathsf{d}}t} \end{bmatrix} \tag{6.67}
$$

As with its constituent models, the norm of the unconditional covariance becomes infinite as $t^3$ becomes infinite, while the process is persistently stimulated by the input, so its covariance conditioned on a measurement history will remain positive definite for all time. Hence, this model shares similar considerations with its constituents for application in sequential navigation filters.

### 6.3.2. Bias, Drift, and Drift Rate Random Walks (Random Walk + Random Run + Random Zoom)

Another model for biases in very-high precision clocks, gyros, and accelerometers is that the bias is driven by two integrals of white noise in addition to its own white noise input. Such models are often characterized by Hadamard deviation specifications, which may be heuristically associated with the white noise power spectral densities. The model is as follows:

$$
\begin{bmatrix} \dot{\mathsf{b}}(t) \\ \dot{\mathsf{d}}(t) \\ \ddot{\mathsf{d}}(t) \end{bmatrix} = \begin{bmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ 0 & 0 & 0 \end{bmatrix} \begin{bmatrix} \mathsf{b}(t) \\ \mathsf{d}(t) \\ \dot{\mathsf{d}}(t) \end{bmatrix} + \begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} \mathsf{w}_b(t) \\ \mathsf{w}_d(t) \\ \mathsf{w}_{\dot{\mathsf{d}}}(t) \end{bmatrix} \tag{6.68}
$$

$$
\dot{\boldsymbol{\mathsf{x}}}(t) = \mathbf{A}\boldsymbol{\mathsf{x}}(t) + \mathbf{B}\boldsymbol{\mathsf{w}}(t) \tag{6.69}
$$

The resulting output equation is

$$
\mathsf{e} = \begin{bmatrix} 1 & 0 & 0 \end{bmatrix} \boldsymbol{\mathsf{x}} + \mathsf{v} \tag{6.70}
$$

$$
= \mathbf{H}\boldsymbol{\mathsf{x}} + \mathsf{v} \tag{6.71}
$$

The initial condition $\boldsymbol{\mathsf{x}}(t_o)$ is an unbiased random constant. Since $\boldsymbol{\mathsf{x}}(t_o)$ and $\boldsymbol{\mathsf{w}}(t)$ are zero-mean, then $\boldsymbol{\mathsf{x}}(t)$ is also zero-mean for all time. The covariance evolves in time according to

$$
\mathbf{P}_{\boldsymbol{\mathsf{x}}}(t) = \boldsymbol{\Phi}(t - t_o)\mathbf{P}_{\boldsymbol{\mathsf{x}}o}\boldsymbol{\Phi}^{\mathsf{T}}(t - t_o) + \mathbf{S}(t - t_o) \tag{6.72}
$$

where

$$
\boldsymbol{\Phi}(t) = \begin{bmatrix} 1 & t & t^2/2 \\ 0 & 1 & t \\ 0 & 0 & 1 \end{bmatrix} \text{ and } \mathbf{P}_{\boldsymbol{\mathsf{x}}o} = \begin{bmatrix} p_{\mathsf{b}o} & 0 & 0 \\ 0 & p_{\mathsf{d}o} & 0 \\ 0 & 0 & p_{\dot{\mathsf{d}}o} \end{bmatrix} \tag{6.73}
$$

and

$$
\mathbf{S}(t) = \begin{bmatrix} q_{\mathsf{b}}t + q_{\mathsf{d}}t^3/3 + q_{\dot{\mathsf{d}}}t^5/5 & q_{\mathsf{d}}t^2/2 + q_{\dot{\mathsf{d}}}t^4/8 & q_{\dot{\mathsf{d}}}t^3/6 \\ q_{\mathsf{d}}t^2/2 + q_{\dot{\mathsf{d}}}t^4/8 & q_{\mathsf{d}}t + q_{\dot{\mathsf{d}}}t^3/3 & q_{\dot{\mathsf{d}}}t^2/2 \\ q_{\dot{\mathsf{d}}}t^3/6 & q_{\dot{\mathsf{d}}}t^2/2 & q_{\dot{\mathsf{d}}}t \end{bmatrix} \tag{6.74}
$$

which we can also write in recursive form as

$$
\mathbf{P}_{\boldsymbol{\mathsf{x}}}(t + \Delta t) = \boldsymbol{\Phi}(\Delta t)\mathbf{P}_{\boldsymbol{\mathsf{x}}}(t)\boldsymbol{\Phi}^{\mathsf{T}}(\Delta t) + \mathbf{S}(\Delta t) \tag{6.75}
$$

Thus, we can generate realizations of the random run with either $\boldsymbol{x}(t) \sim N(\mathbf{0}, \mathbf{P}_{\boldsymbol{\mathsf{x}}}(t))$ or recursively from

$$
\boldsymbol{x}(t + \Delta t) = \boldsymbol{\Phi}(\Delta t)\boldsymbol{x}(t) + \boldsymbol{\varpi}(t) \tag{6.76}
$$

where $\boldsymbol{\varpi}(t) \sim N(0, \mathbf{S}(\Delta t))$. Note that a Cholesky decomposition of $\mathbf{S}(t)$ is

$$
{}^{C}\!\sqrt{\mathbf{S}(t)} = \begin{bmatrix} \sqrt{q_{\mathsf{b}}t + q_{\mathsf{d}}t^3/12 + q_{\dot{\mathsf{d}}}t^5/720} & t/2\sqrt{q_{\mathsf{d}}t + q_{\dot{\mathsf{d}}}t^3/12} & t^2/6\sqrt{q_{\dot{\mathsf{d}}}t} \\ 0 & \sqrt{q_{\mathsf{d}}t + q_{\dot{\mathsf{d}}}t^3/12} & t/2\sqrt{q_{\dot{\mathsf{d}}}t} \\ 0 & 0 & \sqrt{q_{\dot{\mathsf{d}}}t} \end{bmatrix} \tag{6.77}
$$

Similar to its constituent models, the norm of the unconditional covariance becomes infinite as $t^5$ becomes infinite, while the process is persistently stimulated by the input, so its covariance conditioned on a measurement history will remain positive definite for all time. Hence, this model shares similar considerations with its constituents for application in sequential navigation filters.

### 6.3.3. Bias and Drift Coupled First- and Second-Order Gauss-Markov

The following model provides a stable alternative, developed in Reference [14](16-bibliography.md#page-170-14), to the "Random Walk + Random Run" model. Note that the following description corrects a sign error in the process noise cross-covariance results of the cited work. The transient response of the stable alternative can be tuned to approximate the Random Walk + Random Run model, and its stable steady-state response can be used to avoid computational issues with long propagation times, observability, consider states, etc. Although this model has received limited application as of the time of this writing, due to its stability, it shows promising potential to evolve into a *best practice* for sequential navigation filtering applications.

The coupled first- and second-order Gauss-Markov model is as follows.

$$
\begin{bmatrix} \dot{\mathsf{b}}(t) \\ \dot{\mathsf{d}}(t) \end{bmatrix} = \begin{bmatrix} -1/\tau & 1 \\ -\omega_n^2 & -2\zeta\omega_n \end{bmatrix} \begin{bmatrix} \mathsf{b}(t) \\ \mathsf{d}(t) \end{bmatrix} + \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix} \begin{bmatrix} \mathsf{w}_b(t) \\ \mathsf{w}_d(t) \end{bmatrix} \tag{6.78}
$$

$$
\dot{\boldsymbol{\mathsf{x}}}(t) = \mathbf{A}\boldsymbol{\mathsf{x}}(t) + \mathbf{B}\boldsymbol{\mathsf{w}}(t) \tag{6.79}
$$

The measurement partial is the same as for the random ramp. The initial condition $\boldsymbol{\mathsf{x}}(t_o)$ is an unbiased random constant. Since $\boldsymbol{\mathsf{x}}(t_o)$ and $\boldsymbol{\mathsf{w}}(t)$ are zero-mean, then $\boldsymbol{\mathsf{x}}(t)$ is also zero-mean for all time. The covariance evolves in time according to

$$
\mathbf{P}_{\boldsymbol{\mathsf{x}}}(t) = \boldsymbol{\Phi}(t - t_o)\mathbf{P}_{\boldsymbol{\mathsf{x}}o}\boldsymbol{\Phi}^{\mathsf{T}}(t - t_o) + \mathbf{S}(t - t_o) \tag{6.80}
$$

where

$$
\boldsymbol{\Phi}(t) = \frac{\mathrm{e}^{\eta t}}{\nu} \begin{bmatrix} \nu\cos\nu t + (\eta + 2\zeta\omega_n)\sin\nu t & \sin\nu t \\ -\omega_n^2 \sin\nu t & \nu\cos\nu t + (\eta + \beta)\sin\nu t \end{bmatrix} \tag{6.81}
$$

<span id="page-82-0"></span>with

$$
\beta = 1/\tau, \tag{6.82}
$$

$$
\eta = -\frac{1}{2}\left(\beta + 2\zeta\omega_n\right), \tag{6.83}
$$

$$
\nu = \sqrt{\omega_d^2 + \beta\zeta\omega_n - \frac{1}{4}\beta^2}, \tag{6.84}
$$

$$
\omega_d = \omega_n\sqrt{1 - \zeta^2} \tag{6.85}
$$

and we assume that $\nu^2 > 0$. Let

$$
\kappa = -\frac{\beta}{2} + \zeta\omega_n
$$

Then, the process noise covariance is given by the following:

$$
\begin{aligned}
\mathbf{S}_{(1,1)}(t) = q_{\mathsf{b}} \Bigg[ & \frac{\mathrm{e}^{2\eta t} - 1}{4\eta}\left(1 + \frac{\kappa^2}{\nu^2}\right) + \frac{\mathrm{e}^{2\eta t}\sin 2\nu t}{4(\eta^2 + \nu^2)}\left(\frac{\nu^2 - \kappa^2 + \eta\kappa}{\nu}\right) \\
& + \frac{\mathrm{e}^{2\eta t}\cos 2\nu t - 1}{4(\eta^2 + \nu^2)}\left(\frac{\eta\nu^2 - \eta\kappa^2 + 2\nu^2\kappa}{\nu^2}\right) \Bigg] \\
& + \frac{q_{\mathsf{d}}}{\nu^2}\left(\frac{\mathrm{e}^{2\eta t} - 1}{4\eta} - \frac{\mathrm{e}^{2\eta t}(\nu\sin 2\nu t + \eta\cos 2\nu t) - \eta}{4(\eta^2 + \nu^2)}\right)
\end{aligned} \tag{6.86}
$$

$$
\begin{aligned}
\mathbf{S}_{(2,2)}(t) = q_{\mathsf{d}} \Bigg[ & \frac{\mathrm{e}^{2\eta t} - 1}{4\eta}\left(1 + \frac{\kappa^2}{\nu^2}\right) + \frac{\mathrm{e}^{2\eta t}\sin 2\nu t}{4(\eta^2 + \nu^2)}\left(\frac{\nu^2 - \kappa^2 + \eta\kappa}{\nu}\right) \\
& + \frac{\mathrm{e}^{2\eta t}\cos 2\nu t - 1}{4(\eta^2 + \nu^2)}\left(\frac{\eta\nu^2 - \eta\kappa^2 + 2\nu^2\kappa}{\nu^2}\right) \Bigg] \\
& + \frac{q_{\mathsf{b}}\omega_n^4}{\nu^2}\left(\frac{\mathrm{e}^{2\eta t} - 1}{4\eta} - \frac{\mathrm{e}^{2\eta t}(\nu\sin 2\nu t + \eta\cos 2\nu t) - \eta}{4(\eta^2 + \nu^2)}\right)
\end{aligned} \tag{6.87}
$$

$$
\begin{aligned}
\mathbf{S}_{(1,2)}(t) = {} & \frac{q_{\mathsf{b}}\omega_n^2}{\nu^2}\left[\frac{\kappa}{4\eta}\left(1 - \mathrm{e}^{2\eta t}\right) + \frac{\mathrm{e}^{2\eta t}\left[(\nu\kappa - \eta\nu)\sin 2\nu t + (\eta\kappa + \nu^2)\cos 2\nu t\right] - (\eta\kappa + \nu^2)}{4(\eta^2 + \nu^2)}\right] \\
& + \frac{q_{\mathsf{d}}}{\nu^2}\left[\frac{\kappa}{4\eta}\left(1 - \mathrm{e}^{2\eta t}\right) + \frac{\mathrm{e}^{2\eta t}\left[(\eta\nu + \nu\kappa)\sin 2\nu t + (\eta\kappa - \nu^2)\cos 2\nu t\right] - (\eta\kappa - \nu^2)}{4(\eta^2 + \nu^2)}\right]
\end{aligned} \tag{6.88}
$$

$$
\mathbf{S}_{(2,1)}(t) = \mathbf{S}_{(1,2)}(t) \tag{6.89}
$$

Examining the solution given above, we see that the parameter $\eta$ governs the rate of decay of all of the exponential terms. Therefore, we define the "rise time" as that interval within which the transient response of the covariance will reach a close approximation to the above steady-state value; thus, we define the rise time as follows:

$$
t_r = -\frac{3}{\eta} \tag{6.90}
$$

Next, we note that all of the trigonometric terms are modulated by $2\nu$; thus we may view this value as a characteristic damped frequency of the coupled system. The period of the oscillation, $\Pi$, is then

$$
\Pi = \pi/\nu \tag{6.91}
$$

<span id="page-83-0"></span>In the limit as $t \to \infty$, all the exponential terms in the analytical solution die out, so that the steady-state value of the covariance simplifies to:

$$
\mathbf{P}(\infty) = -\frac{1}{4\eta(\eta^2 + \nu^2)} \begin{bmatrix} q_{\mathsf{d}} + (2\eta^2 + \nu^2 + \kappa^2 - \eta\kappa)q_{\mathsf{b}} & q_{\mathsf{b}}\omega_n^2(\eta - \kappa) - q_{\mathsf{d}}(\eta + \kappa) \\ q_{\mathsf{b}}\omega_n^2(\eta - \kappa) - q_{\mathsf{d}}(\eta + \kappa) & (2\eta^2 + \nu^2 + \kappa^2 + \eta\kappa)q_{\mathsf{d}} + q_{\mathsf{b}}\omega_n^4 \end{bmatrix} \tag{6.92}
$$

which may be expressed in terms of the original parameters as

$$
\begin{aligned}
\mathbf{P}(\infty) = {} & \frac{1}{4\omega_n(\omega_n + 2\beta\zeta)(\zeta\omega_n + \beta/2)} \\
& \cdot \begin{bmatrix} q_{\mathsf{d}} + (\omega_n^2 + 2\beta\zeta\omega_n + 4\zeta^2\omega_n^2)q_{\mathsf{b}} & q_{\mathsf{d}}\beta - 2\zeta\omega_n^3 q_{\mathsf{b}} \\ q_{\mathsf{d}}\beta - 2\zeta\omega_n^3 q_{\mathsf{b}} & (\omega_n^2 + 2\beta\zeta\omega_n + \beta^2)q_{\mathsf{d}} + \omega_n^4 q_b \end{bmatrix}
\end{aligned} \tag{6.93}
$$

---

[← Chapter 5. Measurement Underweighting](05-measurement-underweighting.md) · [Contents](README.md) · [Chapter 7. State Representations →](07-state-representations.md)
