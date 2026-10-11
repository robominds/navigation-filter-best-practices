[← Chapter 2. Batch-Sequential Filters](02-batch-sequential-filters.md) · [Contents](README.md) · [Chapter 4. Processing Measurements →](04-processing-measurements.md)

# <span id="page-38-0"></span>Chapter 3. The Covariance Matrix

*Contributed by J. Russell Carpenter*

As Chapter [1](01-the-extended-kalman-filter.md#page-24-0) pointed out, the EKF estimate $\hat{\boldsymbol{X}}(t)$ is at best an approximation for $\mathrm{E}[\boldsymbol{\mathsf{X}}(t)|\mathbb{Y}]$, and hence the EKF symbol $\mathbf{P}(t)$ is at best an approximation for $\mathrm{E}[\boldsymbol{\mathsf{e}}(t)\boldsymbol{\mathsf{e}}^{\mathsf{T}}(t)|\mathbb{Y}]$. In the present Chapter we discuss best practices for maintaining such approximations, and henceforth we will simply refer to $\mathbf{P}(t)$ as the covariance matrix.

## 3.1. Metrics for Orbit State Covariances

<span id="page-38-1"></span>To discuss what makes one covariance approximation better or worse than another, we must be able to compare matrices to one another, and hence we must adopt metrics. For matrices that serve as coefficients, there exist various matrix norms that serve as distance-like metrics for the strength of the coefficient. For covariance matrices, we are usually more interested in measures of the range of possible realizations that could be drawn from the probability distribution characterized by the covariance. The square root of the trace of the covariance is often a reasonable choice, since it is the root sum squared (RSS) formal estimation error. A drawback to the trace for orbital applications is that coordinates and their derivatives typically differ by several orders of magnitude, so that for example the RSS position error will dominate the RSS velocity error if the trace is taken over a $6 \times 6$ Cartesian position and velocity state error covariance, unless some scaling is introduced. Although arbitrary scalings are possible, we discuss several metrics herein that have been found to be especially suitable to space applications.

Orbit determination is distinguishable from other types of positioning and navigation not only by the use of dynamics suitable to orbiting bodies, but also by a fundamental need to produce states that predict accurately. This need arises because spacecraft operations require accurate predictions for acquisition by communications assets, for planning future activities such as maneuvers and observations, for predicting conjunctions with other space objects, etc. For closed, i.e. elliptical, orbits about most planetary bodies, the two-body potential dominates all other forces by several orders of magnitude. Thus, in most cases, the ability of an orbit estimate to predict accurately is dominated by semi-major axis (SMA) error, $\delta a$. This is because SMA error translates into period error through Kepler's third law, and an error in orbit period translates into a secularly increasing error in position along the orbit track. As Reference [[10](16-bibliography.md#page-170-8)] shows, the along-track drift per orbit revolution, $\delta s$, for an elliptical orbit with eccentricity $e$ is bounded by

$$
\delta s = -3\pi\sqrt{\frac{1+e}{1-e}}\,\delta a \quad \text{from periapse to periapse} \tag{3.1}
$$

$$
\delta s = -3\pi\sqrt{\frac{1-e}{1+e}}\,\delta a \quad \text{from apoapse to apoapse} \tag{3.2}
$$

This phenomenon is especially significant for rendezvous and formation flying applications, where relative positions must be precisely controlled.

For a central body whose gravitational constant is $\mu$, the SMA of a closed Keplerian orbit, $a$, may be found from the *vis viva* equation,

<span id="page-39-0"></span>

$$
-\frac{\mu}{2a} = -\frac{\mu}{r} + \frac{v^2}{2} \tag{3.3}
$$

from which one can see that achieving SMA accuracy requires good knowledge of both radius, $r$, and speed, $v$. What is less obvious from [\(3.3\)](#page-39-0) is that radius and speed errors must also be both well-balanced and well-correlated to maximize SMA accuracy [[10](16-bibliography.md#page-170-8),[13](16-bibliography.md#page-170-9),[35](16-bibliography.md#page-171-3)], as Figure [3.1](#page-39-1) illustrates. In this figure, radius standard deviation, or formal error, $\sigma_r$, has been normalized by the squared ratio of radius to SMA, and speed formal error, $\sigma_v$, has been normalized by $nv_c/v$, where the orbital rate is $n = \sqrt{\mu/a^3}$, and the circular speed is $v_c = \sqrt{\mu/a}$, to make the relationships illustrated be independent of any particular point in any particular closed orbit. Figure [3.1](#page-39-1)'s contours of constant SMA error, $\sigma_a$, show that $\sigma_a$ is dominated by radius error below a diagonal region, and dominated by speed error above the diagonal. When radius and speed errors are balanced, along the diagonal, SMA accuracy can be substantially improved by increasing (negative) correlation. Experience has shown that $\sigma_a$ is one of the more useful figures of merit for evaluating orbit determination performance, particularly for relative navigation applications.

![](../_page_39_Figure_6.jpeg)

<span id="page-39-1"></span>*Figure 3.1. Formal error in semi-major axis depends on formal errors in radius, speed, their correlation, and their balance. All scales are in units of position.*

In fact, it is easy to show that any function of two (scalar) random variables possesses a similar correlation and balance structure, at least to first order. For example, navigation requirements for atmospheric entry are often stated in terms of flight-path angle error, $\delta\gamma$. Since $\sin\gamma = \vec{\boldsymbol{r}}/\|\vec{\boldsymbol{r}}\| \cdot \vec{\boldsymbol{v}}/\|\vec{\boldsymbol{v}}\|$, then from geometrical considerations we should expect that $\delta\gamma$ depends on the component of position error which is in the local horizontal plane, in the direction of the velocity vector, and on the component of velocity error that is normal to both velocity and angular momentum, i.e. binormal to the velocity vector. These are of course the in-plane components of position and velocity that are normal to radius and speed. Thus by using the pair $\delta a$ and $\delta\gamma$ as metrics, we can fully characterize the correlation and balance of the in-plane covariance components. The following subsections derive these relationships.

### 3.1.1. Variance of an Arbitrary Function of Two Random Variables

Suppose there exists a random variable $\mathsf{z}$ which is a possibly nonlinear function[<sup>1</sup>](#page-40-0) of two other random variables, $\mathsf{x}$ and $\mathsf{y}$, such that

$$
\mathsf{z} = f(\mathsf{x}, \mathsf{y}) \tag{3.4}
$$

and let the joint covariance of $\mathsf{x}$ and $\mathsf{y}$ be given by

$$
\mathbf{P} = \begin{bmatrix} \sigma_{\mathsf{x}}^2 & \rho_{\mathsf{xy}}\sigma_{\mathsf{x}}\sigma_{\mathsf{y}} \\ \rho_{\mathsf{xy}}\sigma_{\mathsf{x}}\sigma_{\mathsf{y}} & \sigma_{\mathsf{y}}^2 \end{bmatrix} \tag{3.5}
$$

The variance of $\mathsf{z}$ is given by

$$
\sigma_{\mathsf{z}}^2 = \mathrm{E}\big[(\mathsf{z} - \mathrm{E}[\mathsf{z}])^2\big] \tag{3.6}
$$

where

$$
\mathrm{E}[\mathsf{z}] = \int_{-\infty}^{\infty} \zeta\, \mathrm{p}_{\mathsf{z}}(\zeta)\, \mathrm{d}\zeta = \int_{-\infty}^{\infty}\int_{-\infty}^{\infty} f(\xi, \eta)\, \mathrm{p}_{\mathsf{z}}(f(\xi, \eta))\, \mathrm{d}\xi\, \mathrm{d}\eta \tag{3.7}
$$

Let $\hat{x} = \mathrm{E}[\mathsf{x}]$ and $\hat{y} = \mathrm{E}[\mathsf{y}]$. Then $\mathrm{E}[\mathsf{x} - \hat{x}] = 0$ and $\mathrm{E}[\mathsf{y} - \hat{y}] = 0$. Expanding $f(\mathsf{x}, \mathsf{y})$ around $f(\hat{x}, \hat{y})$ in a Taylor series to first order, we find that

$$
f(\mathsf{x}, \mathsf{y}) \approx f(\hat{x}, \hat{y}) + f_x \cdot (\mathsf{x} - \hat{x}) + f_y \cdot (\mathsf{y} - \hat{y}) \tag{3.8}
$$

where $f_x$ and $f_y$ are the partials of $f$ with respect to $x$ and $y$, respectively; so, to first order,

$$
\hat{z} = \mathrm{E}[\mathsf{z}] = \mathrm{E}[f(\mathsf{x}, \mathsf{y})] \approx f(\hat{x}, \hat{y}) \tag{3.9}
$$

Now let us similarly expand $(\mathsf{z} - \mathrm{E}[\mathsf{z}])^2$ to first order:

$$
(\mathsf{z} - \mathrm{E}[\mathsf{z}])^2 = (f(\mathsf{x}, \mathsf{y}) - f(\hat{x}, \hat{y}))^2 \tag{3.10}
$$

$$
\approx f_x^2 \cdot (\mathsf{x} - \hat{x})^2 + 2 f_x f_y \cdot (\mathsf{x} - \hat{x})(\mathsf{y} - \hat{y}) + f_y^2 \cdot (\mathsf{y} - \hat{y})^2 \tag{3.11}
$$

Taking expectations on both sides yields

$$
\mathrm{E}\big[(\mathsf{z} - \mathrm{E}[\mathsf{z}])^2\big] = f_x^2\, \mathrm{E}\big[(\mathsf{x} - \hat{x})^2\big] + 2 f_x f_y\, \mathrm{E}[(\mathsf{x} - \hat{x})(\mathsf{y} - \hat{y})] + f_y^2\, \mathrm{E}\big[(\mathsf{y} - \hat{y})^2\big] \tag{3.12}
$$

$$
\sigma_{\mathsf{z}}^2 = f_x^2 \sigma_{\mathsf{x}}^2 + 2 f_x f_y \rho_{\mathsf{xy}} \sigma_{\mathsf{x}} \sigma_{\mathsf{y}} + f_y^2 \sigma_{\mathsf{y}}^2 \tag{3.13}
$$

$$
= \mathbf{F}\mathbf{P}\mathbf{F}^{\mathsf{T}} \tag{3.14}
$$

where $\mathbf{F} = [f_x, f_y]$. Since $-1 < \rho_{\mathsf{xy}} < 1$, it is clear that a high negative correlation between $\mathsf{x}$ and $\mathsf{y}$ will minimize $\sigma_{\mathsf{z}}$ for given values of $\sigma_{\mathsf{x}}$ and $\sigma_{\mathsf{y}}$, but if either $f_x\sigma_{\mathsf{x}} >> f_y\sigma_{\mathsf{y}}$ or $f_x\sigma_{\mathsf{x}} << f_y\sigma_{\mathsf{y}}$, the impact of the negative correlation will be insignificant. Thus, the only way to simultaneously achieve $\sigma_{\mathsf{z}} << f_x\sigma_{\mathsf{x}}$ and $\sigma_{\mathsf{z}} << f_y\sigma_{\mathsf{y}}$ is when $\rho_{\mathsf{xy}} \approx -1$ and $f_x\sigma_{\mathsf{x}} \approx f_y\sigma_{\mathsf{y}}$, which are the correlation and balance conditions mentioned above, and which occur along the diagonal of Figure [3.1.](#page-39-1)

<span id="page-40-0"></span><sup>1</sup> If the function is nonlinear, the variance formula here is an approximate, first-order result.

Note also that by defining new variables scaled by their respective partial derivatives, $\tilde{x} = x f_x$ and $\tilde{y} = y f_y$, and correspondingly $\tilde{\sigma}_{\mathsf{x}} = f_x\sigma_{\mathsf{x}}$ and $\tilde{\sigma}_{\mathsf{y}} = f_y\sigma_{\mathsf{y}}$, then a normalization of the fashion described above is also possible:

$$
\sigma_{\mathsf{z}} = \sqrt{\tilde{\sigma}_{\mathsf{x}}^2 + 2\rho_{\mathsf{xy}}\tilde{\sigma}_{\mathsf{x}}\tilde{\sigma}_{\mathsf{y}} + \tilde{\sigma}_{\mathsf{y}}^2} \tag{3.15}
$$

### 3.1.2. Semi-Major Axis Variance

To derive a relationship for semi-major axis variance, let us take variations on [\(3.3\)](#page-39-0), which results in

$$
\frac{\delta a}{a^2} = \frac{2\delta r}{r^2} + \frac{2v\delta v}{\mu} \tag{3.16}
$$

If we replace the variations with deviations of random variables from their expectations, and the non-deviated terms with their expected values, we find that

$$
(\mathsf{a} - \hat{a}) = 2\hat{a}^2 \left( \frac{(\mathsf{r} - \hat{r})}{\hat{r}^2} + \frac{\hat{v}(\mathsf{v} - \hat{v})}{\mu} \right) \tag{3.17}
$$

which by squaring and taking expectation yields the following linearized approximation for the SMA variance:

<span id="page-41-0"></span>

$$
\sigma_{\mathsf{a}}^2 = 4\hat{a}^4 \left\{ \frac{1}{\hat{r}^4}\sigma_{\mathsf{r}}^2 + 2\frac{\hat{v}}{\mu\hat{r}^2}\rho_{\mathsf{rv}}\sigma_{\mathsf{r}}\sigma_{\mathsf{v}} + \frac{\hat{v}^2}{\mu^2}\sigma_{\mathsf{v}}^2 \right\} \tag{3.18}
$$

For the normalization used in Figure [3.1,](#page-39-1) rewrite [\(3.18\)](#page-41-0) as

$$
\sigma_{\mathsf{a}} = 2\sqrt{\left(\frac{\sigma_{\mathsf{r}}}{\hat{r}^2/\hat{a}^2}\right)^2 + 2\rho_{\mathsf{rv}}\left(\frac{\sigma_{\mathsf{r}}}{\hat{r}^2/\hat{a}^2}\right)\left(\frac{\sigma_{\mathsf{v}}}{\mu/(\hat{a}^2\hat{v})}\right) + \left(\frac{\sigma_{\mathsf{v}}}{\mu/(\hat{a}^2\hat{v})}\right)^2} \tag{3.19}
$$

and note that $\mu/(\hat{a}^2\hat{v}) = \hat{n}\hat{v}_c/\hat{v}$. As mentioned above, normalizing radius and speed standard deviation in this manner permits comparison of data across all points in all closed orbits.

If the orbit is exactly circular, then further simplification of [\(3.18\)](#page-41-0) is possible. In this case, $a = r$ and $v/\mu = T_p/2\pi$, where $T_p$ is the orbit period. Then [\(3.18\)](#page-41-0) may be rewritten as

$$
\sigma_{\mathsf{a}} = 2\sqrt{\sigma_{\mathsf{r}}^2 + 2\left(\frac{T_p}{2\pi}\right)\rho_{\mathsf{rv}}\sigma_{\mathsf{r}}\sigma_{\mathsf{v}} + \left(\frac{T_p}{2\pi}\right)^2\sigma_{\mathsf{v}}^2} \tag{3.20}
$$

For orbit determination applications, the state representation most often chosen is a Cartesian inertial state vector, $\mathbf{x} = [\vec{\boldsymbol{r}}^{\mathsf{T}}, \vec{\boldsymbol{v}}^{\mathsf{T}}]^{\mathsf{T}}$. Rewriting [\(3.3\)](#page-39-0) as

$$
a(\mathbf{x}) = \left( \frac{2}{\|\vec{\boldsymbol{r}}\|} - \frac{\|\vec{\boldsymbol{v}}\|^2}{\mu} \right)^{-1} \tag{3.21}
$$

and taking partials yields

$$
\left.\frac{\partial a}{\partial \mathbf{x}}\right|_{\hat{\mathbf{x}}} = \mathbf{F}_a(\hat{\mathbf{x}}) = 2\hat{a}^2 \begin{bmatrix} \dfrac{\hat{\vec{\boldsymbol{r}}}^{\mathsf{T}}}{\hat{r}^3} & \dfrac{\hat{\vec{\boldsymbol{v}}}^{\mathsf{T}}}{\mu} \end{bmatrix} \tag{3.22}
$$

so that

$$
\sigma_{\mathsf{a}}^2 = \mathbf{F}_a(\hat{\boldsymbol{x}})\mathbf{P}_{\boldsymbol{\mathsf{x}}}\mathbf{F}_a^{\mathsf{T}}(\hat{\boldsymbol{x}}) \tag{3.23}
$$

where $\mathbf{P}_{\boldsymbol{\mathsf{x}}}$ is the state error covariance.

### 3.1.3. Flight-Path Angle Variance

The flight-path angle, $\gamma$, is the angle between the velocity vector and the local horizontal plane; it is therefore the complement of the angle between the position and velocity vectors, so that

$$
\gamma = \arcsin(\boldsymbol{u}_{\vec{\boldsymbol{r}}} \cdot \boldsymbol{u}_{\vec{\boldsymbol{v}}}) \tag{3.24}
$$

where $\boldsymbol{u}_{\vec{\boldsymbol{r}}} = \vec{\boldsymbol{r}}/r$ and $\boldsymbol{u}_{\vec{\boldsymbol{v}}} = \vec{\boldsymbol{v}}/v$. Taking partials with respect to $\boldsymbol{x}$, we find that

$$
F_{\gamma}(\hat{\boldsymbol{x}}) = \left.\frac{\partial \gamma}{\partial \boldsymbol{x}}\right|_{\hat{\boldsymbol{x}}} = \frac{1}{\sqrt{1 - \sin^2\hat{\gamma}}} \begin{bmatrix} \dfrac{\boldsymbol{u}_{\hat{\boldsymbol{v}}}^{\mathsf{T}} - \sin\hat{\gamma}\,\boldsymbol{u}_{\hat{\boldsymbol{r}}}^{\mathsf{T}}}{\hat{r}} & \dfrac{\boldsymbol{u}_{\hat{\boldsymbol{r}}}^{\mathsf{T}} - \sin\hat{\gamma}\,\boldsymbol{u}_{\hat{\boldsymbol{v}}}^{\mathsf{T}}}{\hat{v}} \end{bmatrix}, \; -\frac{\pi}{2} < \hat{\gamma} < \frac{\pi}{2} \tag{3.25}
$$

so that

<span id="page-42-0"></span>

$$
\sigma_{\gamma}^2 = \mathbf{F}_{\gamma}(\hat{\boldsymbol{x}})\mathbf{P}_{\boldsymbol{\mathsf{x}}}\mathbf{F}_{\gamma}^{\mathsf{T}}(\hat{\boldsymbol{x}}) \tag{3.26}
$$

which is a form suitable for use in an OD filter estimating a Cartesian inertial state.

For analysis, a simpler form of [\(3.26\)](#page-42-0) is as follows. Let us define two vectors that are normal to both the position vector and a vector normal to the orbit plane, $\vec{\boldsymbol{n}}$: the unit in-track vector,

$$
\boldsymbol{u}_{\Delta\vec{\boldsymbol{v}}} = \boldsymbol{u}_{\vec{\boldsymbol{n}}} \times \boldsymbol{u}_{\vec{\boldsymbol{r}}} = \frac{\boldsymbol{u}_{\vec{\boldsymbol{v}}} - \boldsymbol{u}_{\vec{\boldsymbol{r}}}\sin\gamma}{\sqrt{1 - \sin^2\gamma}} \tag{3.27}
$$

which defines a unit vector in the orbit plane that is along the orbit track at apoapsis and periapsis, and the unit bi-normal vector,

$$
\boldsymbol{u}_{\vec{\boldsymbol{b}}} = \boldsymbol{u}_{\vec{\boldsymbol{v}}} \times \boldsymbol{u}_{\vec{\boldsymbol{n}}} = \frac{\boldsymbol{u}_{\vec{\boldsymbol{r}}} - \boldsymbol{u}_{\vec{\boldsymbol{v}}}\sin\gamma}{\sqrt{1 - \sin^2\gamma}} \tag{3.28}
$$

which defines a unit vector in the orbit plane that is along the position vector at apoapsis and periapsis. Let us next define a composite transformation matrix as follows. Let

$$
\mathbf{M}_{rtn} = \begin{bmatrix} \boldsymbol{u}_{\vec{\boldsymbol{r}}_{\mathcal{I}}} & \boldsymbol{u}_{\Delta\vec{\boldsymbol{v}}_{\mathcal{I}}} & \boldsymbol{u}_{\vec{\boldsymbol{n}}_{\mathcal{I}}} \end{bmatrix} \tag{3.29}
$$

where the subscript $\mathcal{I}$ indicates that the specified vector is expressed in an inertial basis. The unitary matrix $\mathbf{M}_{rtn}^{\mathsf{T}}$ thus transforms coordinates of vectors in physical space, which are given in the frame $\mathcal{I}$, to a coordinates defined in the basis given by the the radial, transverse, and normal unit vectors. Similarly, define $\mathbf{M}_{vnb}$ as

$$
\mathbf{M}_{vnb} = \begin{bmatrix} \boldsymbol{u}_{\vec{\boldsymbol{v}}_{\mathcal{I}}} & \boldsymbol{u}_{\vec{\boldsymbol{n}}_{\mathcal{I}}} & \boldsymbol{u}_{\vec{\boldsymbol{b}}_{\mathcal{I}}} \end{bmatrix} \tag{3.30}
$$

Now define the block diagonal transformation matrix $\mathbf{M}$ as

$$
\mathbf{M} = \begin{bmatrix} \mathbf{M}_{rtn} & \mathbf{0}_{3x3} \\ \mathbf{0}_{3x3} & \mathbf{M}_{vnb} \end{bmatrix} \tag{3.31}
$$

Using the matrix $\mathbf{M}$, we can transform the state error covariance, given in inertial coordinates, such that its position error covariance is expressed in the "RTN" frame, and its velocity error covariance is in the "VNB" frame. Using the preceding results in [\(3.26\)](#page-42-0) results in considerable simplification:

<span id="page-42-1"></span>

$$
\sigma_{\gamma}^2 = \begin{bmatrix} \boldsymbol{u}_{\hat{\boldsymbol{t}}}^{\mathsf{T}}/\hat{r} & \boldsymbol{u}_{\hat{\boldsymbol{b}}}^{\mathsf{T}}/\hat{v} \end{bmatrix} \begin{bmatrix} \mathbf{M}_{rtn}^{\mathsf{T}} & \mathbf{0}_{3x3} \\ \mathbf{0}_{3x3} & \mathbf{M}_{vnb}^{\mathsf{T}} \end{bmatrix} \mathbf{P}_{\boldsymbol{\mathsf{x}}} \begin{bmatrix} \mathbf{M}_{rtn} & \mathbf{0}_{3x3} \\ \mathbf{0}_{3x3} & \mathbf{M}_{vnb} \end{bmatrix} \begin{bmatrix} \boldsymbol{u}_{\hat{\boldsymbol{t}}}/\hat{r} \\ \boldsymbol{u}_{\hat{\boldsymbol{b}}}/\hat{v} \end{bmatrix} \tag{3.32}
$$

$$
= \left(\frac{\sigma_{\boldsymbol{\mathsf{r}}_{\boldsymbol{t}}}}{\hat{r}}\right)^2 + 2\rho_{\boldsymbol{\mathsf{r}}_{\boldsymbol{t}}\boldsymbol{\mathsf{v}}_{\boldsymbol{b}}}\left(\frac{\sigma_{\boldsymbol{\mathsf{r}}_{\boldsymbol{t}}}}{\hat{r}}\right)\left(\frac{\sigma_{\boldsymbol{\mathsf{v}}_{\boldsymbol{b}}}}{\hat{v}}\right) + \left(\frac{\sigma_{\boldsymbol{\mathsf{v}}_{\boldsymbol{b}}}}{\hat{v}}\right)^2 \tag{3.33}
$$

which demonstrates the aforementioned assertion that flight-path angle error depends on the intrack component of position error, and the bi-normal component of velocity error. Note that [\(3.33\)](#page-42-1) possesses the desirable feature that the relevant covariance information (in-track position variance and bi-normal velocity variance) is normalized by radius and speed, allowing differing orbital <span id="page-43-1"></span>conditions to be readily compared with one another. In most applications, $\sigma_{\boldsymbol{\mathsf{r}}_{\boldsymbol{t}}} << \hat{r}$ and $\sigma_{\boldsymbol{\mathsf{v}}_{\boldsymbol{b}}} << \hat{v}$ so that these ratios can be taken as small angles and expressed in angular measures commensurate with the units chosen for flight-path angle itself. Figure [3.2](#page-43-0) employs this convention.

![](../_page_43_Figure_3.jpeg)

<span id="page-43-0"></span>*Figure 3.2. Formal error in flight-path angle depends on formal errors of in-track component of position, bi-normal component of velocity, their correlation, and their balance.*

### 3.1.4. Summary of Orbit Determination Covariance Metrics

A recommended best practice for comparison of OD covariances is to use the semi-major axis standard deviation as a metric for most applications, with a secondary emphasis on flight-path angle standard deviation. For entry applications, a best practice is to use flight-path angle standard deviation at entry interface as the primary metric. In using these metrics, one should keep in mind that when computed in the manner shown here, they are nonlinear functions of the state variables, and hence do not preserve properties of the underlying state error distributions. A summary of these metrics is as follows.

> <span id="page-44-3"></span>For orbits that are very close to circular:
>
> $$
> \sigma_{\mathsf{a}} = 2\sqrt{\sigma_{\mathsf{r}}^2 + 2\left(\frac{T_p}{2\pi}\right)\rho_{\mathsf{rv}}\sigma_{\mathsf{r}}\sigma_{\mathsf{v}} + \left(\frac{T_p}{2\pi}\right)^2\sigma_{\mathsf{v}}^2} \tag{3.34}
> $$
>
> For elliptical orbits:
>
> $$
> \sigma_{\mathsf{a}} = 2\hat{a}^2\sqrt{\frac{1}{\hat{r}^4}\sigma_{\mathsf{r}}^2 + 2\frac{\hat{v}}{\mu\hat{r}^2}\rho_{\mathsf{rv}}\sigma_{\mathsf{r}}\sigma_{\mathsf{v}} + \frac{\hat{v}^2}{\mu^2}\sigma_{\mathsf{v}}^2} \tag{3.35}
> $$
>
> For normalization of radius and speed standard deviations across points in closed orbits:
>
> $$
> \sigma_{\mathsf{a}} = 2\sqrt{\left(\frac{\sigma_{\mathsf{r}}}{\hat{r}^2/\hat{a}^2}\right)^2 + 2\rho_{\mathsf{rv}}\left(\frac{\sigma_{\mathsf{r}}}{\hat{r}^2/\hat{a}^2}\right)\left(\frac{\sigma_{\mathsf{v}}}{\hat{n}\hat{v}_c/\hat{v}}\right) + \left(\frac{\sigma_{\mathsf{v}}}{\hat{n}\hat{v}_c/\hat{v}}\right)^2} \tag{3.36}
> $$
>
> For entry applications, and as a secondary metric:
>
> $$
> \sigma_{\gamma} = \sqrt{\left(\frac{\sigma_{\boldsymbol{\mathsf{r}}_{\boldsymbol{t}}}}{\hat{r}}\right)^2 + 2\rho_{\boldsymbol{\mathsf{r}}_{\boldsymbol{t}}\boldsymbol{\mathsf{v}}_{\boldsymbol{b}}}\left(\frac{\sigma_{\boldsymbol{\mathsf{r}}_{\boldsymbol{t}}}}{\hat{r}}\right)\left(\frac{\sigma_{\boldsymbol{\mathsf{v}}_{\boldsymbol{b}}}}{\hat{v}}\right) + \left(\frac{\sigma_{\boldsymbol{\mathsf{v}}_{\boldsymbol{b}}}}{\hat{v}}\right)^2} \tag{3.37}
> $$
>
> For use in an OD filter that is estimating a Cartesian inertial state vector:
>
> $$
> \sigma_{\mathsf{a}} = \sqrt{\mathbf{F}_a(\hat{\mathbf{x}})\mathbf{P}_{\mathbf{x}}\mathbf{F}_a^{\mathsf{T}}(\hat{\mathbf{x}})}, \quad \mathbf{F}_a(\hat{\mathbf{x}}) = 2\hat{a}^2 \begin{bmatrix} \dfrac{\hat{\vec{\boldsymbol{r}}}^{\mathsf{T}}}{\hat{r}^3} & \dfrac{\hat{\vec{\boldsymbol{v}}}^{\mathsf{T}}}{\mu} \end{bmatrix} \tag{3.38}
> $$
>
> $$
> \sigma_{\gamma} = \sqrt{\mathbf{F}_{\gamma}(\hat{\mathbf{x}})\mathbf{P}_{\mathbf{x}}\mathbf{F}_{\gamma}^{\mathsf{T}}(\hat{\mathbf{x}})}, \quad \mathbf{F}_{\gamma}(\hat{\mathbf{x}}) = \begin{bmatrix} \dfrac{\boldsymbol{u}_{\hat{\boldsymbol{t}}}^{\mathsf{T}}}{\hat{r}} & \dfrac{\boldsymbol{u}_{\hat{\boldsymbol{b}}}^{\mathsf{T}}}{\hat{v}} \end{bmatrix} \tag{3.39}
> $$

## 3.2. Covariance Propagation

<span id="page-44-0"></span>This section discusses best practices for implementing the covariance propagation recursion

<span id="page-44-1"></span>

$$
\mathbf{P}_i^- = \boldsymbol{\Phi}(t_i, t_{i-1})\mathbf{P}_{i-1}^+\boldsymbol{\Phi}^{\mathsf{T}}(t_i, t_{i-1}) + \mathbf{S}_i, \quad \mathbf{P}_0^+ = \mathbf{P}_o \tag{3.40}
$$

As Chapter [1](01-the-extended-kalman-filter.md#page-24-0) mentions, to achieve this goal we need suitable approximations for the state transition matrix, $\boldsymbol{\Phi}(t_i, t_{i-1})$, and the process noise covariance, $\mathbf{S}_i$. However, the suitability of a given set of approximations is strongly dependent on specifics of the application. For example, if a set of measurements from which the state is fully observable are available at an interval that is a small fraction of the orbit period, without significant drop-outs, and prediction of the covariance far into the future of the time of availability of the measurements is not required, then simple models such as those to which Chapter [1](01-the-extended-kalman-filter.md#page-24-0) alluded have been successfully employed. Selection of appropriate covariance propagation approximations also depends strongly on the choice of state representation, which is the subject of Chapter [7.](07-state-representations.md#page-84-0) Therefore, this section will discuss the merits of some of the more common and generally applicable approaches, in the context of orbit determination.

### 3.2.1. Matrix Riccati Equation

Many textbooks on Kalman filtering derive [\(3.40\)](#page-44-1) as the solution of a matrix Riccati equation; using the notation of Chapter [1,](01-the-extended-kalman-filter.md#page-24-0) this takes the following form:

<span id="page-44-2"></span>

$$
\dot{\mathbf{P}}(t) = \mathbf{A}(t)\mathbf{P}(t) + \mathbf{P}(t)\mathbf{A}^{\mathsf{T}}(t) + \mathbf{Q}(t) \tag{3.41}
$$

Use of [\(3.41\)](#page-44-2) would seem to avoid the need to perform the integrations required to compute the state transition matrix (STM) and process noise covariance (PNC). In orbit determination practice however, [\(3.40\)](#page-44-1) has been found to be more numerically stable and also, despite the need to compute or approximate the state transition and process noise integrals, more efficient than [\(3.41\)](#page-44-2).

### <span id="page-45-4"></span>3.2.2. State Transition Matrix

A common approach in ground-based OD, especially in the batch least squares context, is to simultaneously integrate the STM along with the state vector,

<span id="page-45-0"></span>

$$
\dot{\boldsymbol{X}}(t) = \boldsymbol{f}(\boldsymbol{X}(t), t), \quad \boldsymbol{X}(t_o) = \boldsymbol{X}_o \tag{3.42}
$$

$$
\dot{\boldsymbol{\Phi}}(t, t_o) = \mathbf{A}(t)\boldsymbol{\Phi}(t, t_o), \quad \boldsymbol{\Phi}(t_o, t_o) = \mathbf{I} \tag{3.43}
$$

When coupled with a good numerical integration algorithm, this method has excellent fidelity, which is rarely necessary in onboard OD applications. Lear [[50](16-bibliography.md#page-172-1)] studied a number of practical methods for computing the STM in the onboard OD context. As his report is not widely available, we will summarize some key findings here.

Lear's approach was to compare various orders of truncated Taylor series and Runge-Kutta approximations to the solution of [\(3.43\)](#page-45-0). He used these STM approximations to propagate an initially diagonal covariance for one revolution in a two-body circular orbit around a point mass with the $GM$ of Earth. By comparing these results to those he obtained using an analytic STM, Lear could compute the maximum step size that would result in a given relative accuracy for radius and speed formal standard deviations. Table [1](#page-45-1) lists a few of Lear's results. Notably, Method H has the desirable feature that simply saving the value of the state Jacobian from the previous propagation step allows for more than an order of magnitude increase in allowable time step, with essentially the same computational burden as Method B. If it is not too burdensome to compute $\mathbf{A}$ at the midpoint of the propagation step, then Method G offers nearly equivalent performance without the need to retain the previous value of $\mathbf{A}$. For higher-rate propagations, Method B offers far more accuracy than Method A with only a small additional computational burden. While Method A appears to be a poor choice for many applications, it does play a central role in some useful approximations to the process noise covariance, as the sequel shows.

| | Description | Method | Max. Step [sec] |
|---|---|---|--:|
| A. | 1<sup>st</sup>-order Taylor | $\mathbf{I} + \mathbf{A}_i\Delta t$ | 0.125 |
| B. | 2<sup>nd</sup>-order Taylor, ignoring $\dot{\mathbf{A}}$ | $\mathbf{I} + \mathbf{A}_i\Delta t + \mathbf{A}_i^2\Delta t^2/2$ | 1.0 |
| C. | 2<sup>nd</sup>-order Taylor | $\mathbf{I} + \mathbf{A}_i\Delta t + (\dot{\mathbf{A}}_i + \mathbf{A}_i^2)\Delta t^2/2$ | 16 |
| F. | 1<sup>st</sup>-order Runge-Kutta | $\mathbf{I} + \mathbf{A}_{i+.5}\Delta t$ | 0.14 |
| G. | 2<sup>nd</sup>-order Runge-Kutta, with one evaluation of $\mathbf{A}$ | $\mathbf{I} + \mathbf{A}_{i+.5}\Delta t + \mathbf{A}_{i+.5}^2\Delta t^2/2$ | 14 |
| H. | 2<sup>nd</sup>-order Runge-Kutta, with two evaluations of $\mathbf{A}$ | $\mathbf{I} + (\mathbf{A}_i + \mathbf{A}_{i+1})\Delta t/2 + \mathbf{A}_{i+1}\mathbf{A}_i\Delta t^2/2$ | 16 |

<span id="page-45-1"></span>*Table 1. A few of Lear's STM Comparison Results, for 1% relative error.*

### 3.2.3. Process Noise Covariance

As stated in Chapter [1,](01-the-extended-kalman-filter.md#page-24-0) nearly all practical methods for computing the process noise covariance assume that $\mathrm{E}[\boldsymbol{\mathsf{w}}(t)\boldsymbol{\mathsf{w}}^{\mathsf{T}}(\tau)] = \mathbf{Q}(t)\delta(t - \tau)$, so that [\(1.29\)](01-the-extended-kalman-filter.md#page-28-5) simplifies to a single integral for the process noise covariance[<sup>2</sup>](#page-45-2), given by [\(1.42\)](01-the-extended-kalman-filter.md#page-29-2), and repeated here:

<span id="page-45-3"></span>

$$
\mathbf{S}_i = \int_{t_{i-1}}^{t_i} \boldsymbol{\Phi}(t_i, \tau)\mathbf{B}(\tau)\mathbf{Q}(\tau)\mathbf{B}^{\mathsf{T}}(\tau)\boldsymbol{\Phi}^{\mathsf{T}}(t_i, \tau)\, \mathrm{d}\tau \tag{3.44}
$$

<span id="page-45-2"></span><sup>2</sup> A notable exception is the work of Wright [[89](16-bibliography.md#page-173-2)], which describes a correlated process noise model that is intended to account for gravity modeling errors in a "physically realistic" manner. Although this method has had occasional onboard application, it is more widely known for its inclusion in commercial-off-the-shelf software for ground-based OD.

Tapley, Schutz, and Born [[81](16-bibliography.md#page-173-3)] describe two approximations to the portion of [\(3.44\)](#page-45-3) which corresponds to position and velocity state noise, which have proven useful in both ground- and onboard-OD applications. Reference [81](16-bibliography.md#page-173-3) refers to these methods as "State Noise Compensation" (SNC) and "Dynamic Model Compensation" (DMC). Before describing SNC and DMC however, we will consider some inappropriate models.

Chapter [1](01-the-extended-kalman-filter.md#page-24-0) pointed out that

$$
\begin{aligned}
&\mathrm{E}\left[\int_{t_{i-1}}^{t_i}\int_{t_{i-1}}^{t_i} \boldsymbol{\Phi}(t_i, \tau)\mathbf{B}(\tau)\boldsymbol{\mathsf{w}}(\tau)\boldsymbol{\mathsf{w}}^{\mathsf{T}}(\sigma)\mathbf{B}^{\mathsf{T}}(\sigma)\boldsymbol{\Phi}^{\mathsf{T}}(t_i, \sigma)\, \mathrm{d}\tau\, \mathrm{d}\sigma\right] \\
&\qquad \neq \mathrm{E}\left[\int_{t_{i-1}}^{t_i} \boldsymbol{\Phi}(t_i, \tau)\mathbf{B}(\tau)\boldsymbol{\mathsf{w}}(\tau)\, \mathrm{d}\tau \int_{t_{i-1}}^{t_i} \boldsymbol{\mathsf{w}}^{\mathsf{T}}(\tau)\mathbf{B}^{\mathsf{T}}(\tau)\boldsymbol{\Phi}^{\mathsf{T}}(t_i, \tau)\, \mathrm{d}\tau\right]
\end{aligned} \tag{3.45}
$$

Let us explore the implications of assuming equality of the expression above. Suppose we assume that the process noise increments are approximately constant over some particular interval $\Delta t = t_i - t_{i-1}$, and that $\mathrm{E}[\boldsymbol{\mathsf{w}}(t_i)\boldsymbol{\mathsf{w}}^{\mathsf{T}}(t_j)] = \mathbf{W}(t_i)\delta_{ij}$, where $\delta_{ij}$ denotes the Kronecker delta function. Then,

<span id="page-46-0"></span>

$$
\begin{aligned}
&\mathrm{E}\left[\int_{t_{i-1}}^{t_i} \boldsymbol{\Phi}(t_i, \tau)\mathbf{B}(\tau)\boldsymbol{\mathsf{w}}(\tau)\, \mathrm{d}\tau \int_{t_{i-1}}^{t_i} \boldsymbol{\mathsf{w}}^{\mathsf{T}}(\tau)\mathbf{B}^{\mathsf{T}}(\tau)\boldsymbol{\Phi}^{\mathsf{T}}(t_i, \tau)\, \mathrm{d}\tau\right] \\
&\quad = \int_{t_{i-1}}^{t_i} \boldsymbol{\Phi}(t_i, \tau)\mathbf{B}(\tau)\, \mathrm{d}\tau\; \mathrm{E}[\boldsymbol{\mathsf{w}}(t_i)\boldsymbol{\mathsf{w}}(t_i)^{\mathsf{T}}] \int_{t_{i-1}}^{t_i} \mathbf{B}^{\mathsf{T}}(\tau)\boldsymbol{\Phi}^{\mathsf{T}}(t_i, \tau)\, \mathrm{d}\tau \\
&\quad = \boldsymbol{\Gamma}_i\mathbf{W}_i\boldsymbol{\Gamma}_i^{\mathsf{T}}
\end{aligned} \tag{3.46}
$$

There is a subtlety with [\(3.46\)](#page-46-0) that can lead to issues: if the time interval associated with the assumption that $\mathrm{E}[\boldsymbol{\mathsf{w}}(t_i)\boldsymbol{\mathsf{w}}^{\mathsf{T}}(t_j)] = \mathbf{W}(t_i)\delta_{ij}$ is not the same as the time interval associated with the integral $\boldsymbol{\Gamma}_i = \int_{t_{i-1}}^{t_i}\boldsymbol{\Phi}(t_i, \tau)\mathbf{B}(\tau)\, \mathrm{d}\tau$, then the process noise will not be consistently applied. For example, if the EKF is tuned at a particular time step using a particular noise covariance $\mathbf{W}$, and then for some reason the time step is changed, then one must retune the value of $\mathbf{W}$.

A similar issue occurs when the process noise covariance is chosen without regard for the dynamics, e.g. by setting it equal to a diagonal matrix of user-specified parameters. Whatever careful tuning has been done to choose such parameters will be invalidated by a change in the time step.

#### 3.2.3.1. State Noise Compensation

For SNC, as applied to OD, we assume velocity error is an uncorrelated random walk with fixed intensity in orbit-fixed coordinates, such as the RTN or VNB coordinates described above. Thus, assuming RTN coordinates without loss of generality, the process noise spectral density matrix becomes

$$
\mathbf{Q}(t) = \mathbf{Q}_{rtn} = \begin{bmatrix} q_r & 0 & 0 \\ 0 & q_t & 0 \\ 0 & 0 & q_n \end{bmatrix} \tag{3.47}
$$

We assume the transformation from orbit-fixed coordinates to the coordinates used for navigation, which are typically inertial coordinates, is approximately constant over the interval $\Delta t = t_i - t_{i-1}$, and ignore the correlation-inducing dependence of this transformation on the estimated position and velocity. This results in

$$
\mathbf{B}(t) = \mathbf{B}_{rtn} = \begin{bmatrix} \mathbf{0}_{3\times 3} \\ \mathbf{M}_{rtn} \end{bmatrix} \tag{3.48}
$$

<span id="page-47-0"></span>We also assume that $\Delta t$ is small enough that a 1<sup>st</sup>-order Taylor series truncation (Lear's Model A) is adequate for modeling the STM $\boldsymbol{\Phi}(t_i, \tau)$ in the integrand of [\(3.44\)](#page-45-3), and that $\mathbf{M}_{rtn}$ is constant. With these assumptions, [\(3.44\)](#page-45-3) becomes

$$
\mathbf{S}_i = \begin{bmatrix} \tilde{\mathbf{Q}}\dfrac{\Delta t^3}{3} & \tilde{\mathbf{Q}}\dfrac{\Delta t^2}{2} \\[2ex] \tilde{\mathbf{Q}}\dfrac{\Delta t^2}{2} & \tilde{\mathbf{Q}}\Delta t \end{bmatrix} \tag{3.49}
$$

where $\tilde{\mathbf{Q}} = \mathbf{M}_{rtn}\mathbf{Q}_{rtn}\mathbf{M}_{rtn}^{\mathsf{T}}$. Note that with the SNC model, velocity covariance grows linearly with time, as expected for a random walk model, and hence we should expect the units of $\sqrt{q_i}$, $i = r, t, n$ to be meters per second$^{3/2}$. Reference [[79](16-bibliography.md#page-173-4)] provides alternative approximations to [\(3.44\)](#page-45-3) for an orbital element state representation, and for relative spacecraft states at both small and large interspacecraft separations.

#### 3.2.3.2. State Noise Compensation for Maneuvers

During powered flight, it is often necessary to include additional process noise to accommodate maneuver magnitude and direction errors. One approach is to simply define an additional SNC process noise covariance, with intensities that are sized to the maneuvering errors. While this works fine for modeling maneuver magnitude errors, direction errors may be more accurately modeled by recognizing that a misaligned maneuver vector may be represented by $(\mathbf{I}_3 - \delta\boldsymbol{\theta}^{\times})\Delta\vec{\boldsymbol{v}}_{nom}$, where $\delta\boldsymbol{\theta}^{\times}$ represents a skew-symmetric matrix of small angle misalignments, and $\Delta\vec{\boldsymbol{v}}_{nom}$ is the nominal maneuver vector. Thus, $\Delta\vec{\boldsymbol{v}}_{nom}^{\times}\delta\boldsymbol{\theta}$ is the error in the velocity increment due to maneuver direction errors, or if sensed accelerations are being fed-forward into the dynamics, due to IMU misalignments. To model these direction errors as a process noise term, let

$$
\mathbf{B}(t) = \begin{bmatrix} \mathbf{0}_{3\times 3} \\ \Delta\vec{\boldsymbol{v}}_{nom}^{\times} \end{bmatrix} \tag{3.50}
$$

and let $q_\theta$ be the intensity of the maneuver direction noise. Then the SNC-style process noise for accommodating maneuver direction errors becomes

$$
\mathbf{S}_i = q_\theta \begin{bmatrix} -(\Delta\vec{\boldsymbol{v}}_{nom}^{\times})^2\dfrac{\Delta t^3}{3} & -(\Delta\vec{\boldsymbol{v}}_{nom}^{\times})^2\dfrac{\Delta t^2}{2} \\[2ex] -(\Delta\vec{\boldsymbol{v}}_{nom}^{\times})^2\dfrac{\Delta t^2}{2} & -(\Delta\vec{\boldsymbol{v}}_{nom}^{\times})^2\Delta t \end{bmatrix} \tag{3.51}
$$

since $\Delta\vec{\boldsymbol{v}}_{nom}^{\times}\Delta\vec{\boldsymbol{v}}_{nom}^{\times\mathsf{T}} = -(\Delta\vec{\boldsymbol{v}}_{nom}^{\times})^2$. A version of this method was used by the Space Shuttle during powered flight with IMU-sensed accelerations.

#### 3.2.3.3. Dynamic Model Compensation

The DMC approach assumes the presence of exponentially-correlated acceleration biases, which are included as additional solve-fors in the filter state. As Chapter [6](06-bias-modeling.md#page-72-0) and Appendix [A](13-appendix-a-models-and-realizations-of-random-variables.md#page-146-0) discuss, a model for such biases is given by

$$
b(t + \Delta t) = \mathrm{e}^{-\frac{\Delta t}{\tau}}\, b(t) + \varpi(t) \tag{3.52}
$$

where $b(t_o) \sim N(0, p_{bo})$, and $\varpi(t) \sim N\!\left(0, \frac{q\tau}{2}\left(1 - \mathrm{e}^{-\frac{2\Delta t}{\tau}}\right)\right)$. As Chapter [6](06-bias-modeling.md#page-72-0) discusses, $\tau$ is a time constant controlling the "smoothness" of the random process, and $q$ is a power spectral density that describes the intensity of the random input. While Chapter [6](06-bias-modeling.md#page-72-0) discusses a variety of other bias models that might be used, the exponentially-correlated model has proved to be a *best practice* for applications in which there are measurements continually available to persistently excite it. Refer to Chapter [6](06-bias-modeling.md#page-72-0) for a fuller discussion of the relative merits of various bias modeling approaches.

As above, without loss of generality we can assume the acceleration biases are aligned with the RTN frame, and again assume that $\Delta t$ is small enough that a 1<sup>st</sup>-order Taylor series truncation is adequate for modeling the portion of the STM corresponding to position and velocity errors. With these assumptions, the terms appearing the integrand of [\(3.44\)](#page-45-3) become

$$
\mathbf{B}(t) = \mathbf{B}_{rtn} = \begin{bmatrix} \mathbf{0}_{3\times 3} \\ \mathbf{0}_{3\times 3} \\ \mathbf{M}_{rtn} \end{bmatrix} \tag{3.53}
$$

and

$$
\boldsymbol{\Phi}(t + \Delta t, t) = \begin{bmatrix} \mathbf{I}_3 & \Delta t\mathbf{I}_3 & \left\{\tau\Delta t - \tau^2(1 - \mathrm{e}^{-\Delta t/\tau})\right\}\mathbf{I}_3 \\ \mathbf{0}_{3\times 3} & \mathbf{I}_3 & \tau(1 - \mathrm{e}^{-\Delta t/\tau})\mathbf{I}_3 \\ \mathbf{0}_{3\times 3} & \mathbf{0}_{3\times 3} & \mathrm{e}^{-\Delta t/\tau}\,\mathbf{I}_3 \end{bmatrix} \tag{3.54}
$$

and the process noise covariance becomes[<sup>3</sup>](#page-48-0)

<span id="page-48-1"></span>

$$
\mathbf{S}_i = \begin{bmatrix} \gamma_{pp}\tilde{\mathbf{Q}} & \gamma_{pv}\tilde{\mathbf{Q}} & \gamma_{pa}\tilde{\mathbf{Q}} \\ \gamma_{pv}\tilde{\mathbf{Q}} & \gamma_{vv}\tilde{\mathbf{Q}} & \gamma_{va}\tilde{\mathbf{Q}} \\ \gamma_{pa}\tilde{\mathbf{Q}} & \gamma_{va}\tilde{\mathbf{Q}} & \gamma_{aa}\tilde{\mathbf{Q}} \end{bmatrix} \tag{3.55}
$$

with

$$
\gamma_{pp} = \tfrac{\tau^5}{2}\left\{\left(1 - \mathrm{e}^{-2\Delta t/\tau}\right) + \tfrac{2\Delta t}{\tau}\left(1 - 2\,\mathrm{e}^{-\Delta t/\tau}\right) - 2\left(\tfrac{\Delta t}{\tau}\right)^2 + \tfrac{2}{3}\left(\tfrac{\Delta t}{\tau}\right)^3\right\} \tag{3.56}
$$

$$
\gamma_{pv} = \tfrac{\tau^4}{2}\left\{\left(\mathrm{e}^{-2\Delta t/\tau} - 1\right) - 2\left(\mathrm{e}^{-\Delta t/\tau} - 1\right) + \tfrac{2\Delta t}{\tau}\left(\mathrm{e}^{-\Delta t/\tau} - 1\right) + \left(\tfrac{\Delta t}{\tau}\right)^2\right\} \tag{3.57}
$$

$$
\gamma_{pa} = \tfrac{\tau^3}{2}\left\{\left(1 - \mathrm{e}^{-2\Delta t/\tau}\right) - \tfrac{2\Delta t}{\tau}\,\mathrm{e}^{-\Delta t/\tau}\right\} \tag{3.58}
$$

$$
\gamma_{vv} = \tfrac{\tau^3}{2}\left\{\left(1 - \mathrm{e}^{-2\Delta t/\tau}\right) - 4\left(1 - \mathrm{e}^{-\Delta t/\tau}\right) + 2\Delta t/\tau\right\} \tag{3.59}
$$

$$
\gamma_{va} = \tfrac{\tau^2}{2}\left(1 - \mathrm{e}^{-\Delta t/\tau}\right)^2 \tag{3.60}
$$

$$
\gamma_{aa} = \tfrac{\tau}{2}\left(1 - \mathrm{e}^{-2\Delta t/\tau}\right) \tag{3.61}
$$

This analytic result for the DMC model first appeared in [[18](16-bibliography.md#page-170-10)].

<span id="page-48-0"></span><sup>3</sup> In [\(3.55\)](#page-48-1), the matrix $\tilde{\mathbf{Q}}$ has the same form as it does for the SNC method, but with $\sqrt{q_i}$, $i = r, t, n$ now representing acceleration intensities, with units of meters per second$^{5/2}$. Also note that [\(3.55\)](#page-48-1) assumes the same time constant is applicable to all three acceleration channels. While this is usually sufficient, it is straightforward to extend [\(3.55\)](#page-48-1) to accommodate separate time constants for each channel.

#### 3.2.3.4. Explicit Dynamic Biases

While the DMC approach allows for quite general estimation of otherwise unmodeled forces on the spacecraft, it is often the case that the domain of application provides context that can narrow the filter designer's focus. For example, it may be the case that the only under-modeled force of appreciable significance on the spacecraft is drag, or perhaps solar radiation pressure, within the context of the application. Alternatively, the application may require much higher resolution models than DMC, which might necessitate estimation of smaller forces with larger uncertainties such as Earth radiation pressure, spacecraft thermal emission, etc., or panel-based modeling of drag and/or solar radiation pressure, etc. In such cases, it is often useful to tailor the DMC approach so that it estimates model-specific biases, such a drag or SRP corrections, rather than modeling three general RTN biases. Similarly, during powered flight, maneuver magnitude and direction errors might be more successfully modeled explicitly.

As an example of an explicit bias, consider estimating a multiplicative correction to the density; a similar approach may be used for drag or solar radiation pressure coefficients. Let $t$ denote geocentric coordinate time. Let $\mathcal{R}$ denote a planetary-body-fixed, body-centric system of coordinates, aligned with the central body's rotation axis. Let $\mathcal{I}$ denote a body-centric, celestially-referenced system of coordinates, aligned with $\mathcal{R}$ at an epoch $t_o$. Let $\vec{\boldsymbol{r}}$ represent the position of the center of gravity of a satellite, expressed in $\mathcal{I}$. Let $\vec{\boldsymbol{v}}$ represent the satellite's velocity within $\mathcal{I}$. Let $\vec{\boldsymbol{v}}_r$ represent the satellite's velocity within frame $\mathcal{R}$. Assume that $\vec{\boldsymbol{r}}$ evolves with respect to $t$ and $\mathcal{I}$ in the vicinity of $t_o$ according to

$$
\frac{{}^{\mathcal{I}}\mathrm{d}^2}{\mathrm{d}t^2}\vec{\boldsymbol{r}} = -\frac{\mu}{r^3}\vec{\boldsymbol{r}} - \frac{1}{2}C_D\frac{A}{m}\rho\left(1 + \frac{\delta\rho}{\rho}\right)v_r\vec{\boldsymbol{v}}_r \tag{3.62}
$$

where $r = \|\vec{\boldsymbol{r}}\|$, $v_r = \|\vec{\boldsymbol{v}}_r\|$, $\delta\rho$ is an atmospheric density disturbance, $\rho$ is the undisturbed atmospheric density, $A$ is the area of the satellite in a plane normal to $\vec{\boldsymbol{v}}_r$, $m$ is the satellite mass, and $C_D$ is the satellite's coefficient of drag. Assume that $\delta\rho/\rho$ is a random process that formally evolves as a first-order Gauss-Markov process, similar to a DMC bias:

$$
\frac{\mathrm{d}}{\mathrm{d}t}\left(\frac{\delta\rho}{\rho}\right) = -\frac{1}{\tau}\left(\frac{\delta\rho}{\rho}\right) + w_\rho \tag{3.63}
$$

where $q_\rho$ is the intensity of $w_\rho$. Let the state vector be $\mathbf{x} = [\vec{\boldsymbol{r}}', \vec{\boldsymbol{v}}', (\delta\rho/\rho)]'$. With these assumptions, the state dynamics and noise input partials are

$$
\mathbf{A}(t) = \begin{bmatrix} \mathbf{0}_{3\times 3} & \mathbf{I}_3 & \mathbf{0}_{3\times 1} \\ \mathbf{G}(t) + \mathbf{D}_r(t) & \mathbf{D}_v(t) & \vec{\boldsymbol{d}}(t) \\ \mathbf{0}_{1\times 3} & \mathbf{0}_{1\times 3} & -1/\tau \end{bmatrix}, \; \mathbf{B}(t) = \begin{bmatrix} \mathbf{0}_{3\times 1} \\ \mathbf{0}_{3\times 1} \\ 1 \end{bmatrix} \tag{3.64}
$$

where $\mathbf{G}(t)$ is the gravity gradient matrix, $\vec{\boldsymbol{d}}(t) = -\frac{1}{2}C_D\frac{A}{m}\rho v_r\vec{\boldsymbol{v}}_r$ is the nominal drag acceleration, and $\mathbf{D}_r$ and $\mathbf{D}_v$ are partials of the drag acceleration with respect to position and velocity, respectively[<sup>4</sup>](#page-49-0).

<span id="page-49-0"></span><sup>4</sup> The sensitivity $\mathbf{D}_r$ contains terms that are roughly proportional to the drag acceleration magnitude divided by the atmospheric scale height, and to the product of drag acceleration magnitude and the ratio of planetary rotation rate to speed relative to the atmosphere. For nearly all spacecraft, these terms will be many orders magnitude smaller than the gravity gradient, which is proportional to the gravity acceleration divided by the radius. So $\mathbf{D}_r$ can usually be neglected. For reference, $\mathbf{D}_v = -\frac{1}{2}C_D\frac{A}{m}\rho v_r(\vec{\boldsymbol{u}}_{v_r}\vec{\boldsymbol{u}}_{v_r}' + \mathbf{I}_3)$, and $\mathbf{D}_r = d/R_s(\vec{\boldsymbol{u}}_r\vec{\boldsymbol{u}}_{v_r}') - \mathbf{D}_v\vec{\boldsymbol{\omega}}^{\times}$, where $\vec{\boldsymbol{\omega}}^{\times}$ is the skew-symmetric "cross-product" matrix formed from the central body's rotation rate vector, and the notation $\vec{\boldsymbol{u}}_{(\cdot)}$ indicates the unit vector of its subscript.

Using the DMC results from above, with the assumption that the nominal drag acceleration is approximately constant over the integration time, $\Delta t$, the term $\boldsymbol{\Phi}(t + \Delta t, t)\mathbf{B}(t)$ appearing in the integrand of [\(3.44\)](#page-45-3) becomes

$$
\boldsymbol{\Phi}(t + \Delta, t)\mathbf{B}(t) = \begin{bmatrix} \left\{\tau\Delta t - \tau^2(1 - \mathrm{e}^{-\Delta t/\tau})\right\}\vec{\boldsymbol{d}} \\ \tau(1 - \mathrm{e}^{-\Delta t/\tau})\vec{\boldsymbol{d}} \\ \mathrm{e}^{-\Delta t/\tau} \end{bmatrix} \tag{3.65}
$$

and the process noise for a proportional density bias becomes

$$
\mathbf{S}_i = q_\rho \begin{bmatrix} \gamma_{pp}\vec{\boldsymbol{d}}\vec{\boldsymbol{d}}' & \gamma_{pv}\vec{\boldsymbol{d}}\vec{\boldsymbol{d}}' & \gamma_{pa}\vec{\boldsymbol{d}} \\ \gamma_{pv}\vec{\boldsymbol{d}}\vec{\boldsymbol{d}}' & \gamma_{vv}\vec{\boldsymbol{d}}\vec{\boldsymbol{d}}' & \gamma_{va}\vec{\boldsymbol{d}} \\ \gamma_{pa}\vec{\boldsymbol{d}}' & \gamma_{va}\vec{\boldsymbol{d}}' & \gamma_{aa} \end{bmatrix} \tag{3.66}
$$

#### 3.2.3.5. Episodic Dynamic Biases

It has sometimes been found to be the case, particularly for crewed missions, that episodic spacecraft activities can produce un-modeled accelerations. In the early days of manned spaceflight, events such as vents, momentum unloads, thruster-based attitude control firings, etc. that may perturb a spacecraft's trajectory were not well modeled, and came to be described as FLAK, which was supposed to be an acronym for (un)-Fortunate Lack of Acceleration Knowledge.

If the mean time between such activities can be characterized, along with the expected intensity of the acceleration, a compound Poisson-Gaussian process noise model may be effective. Conveniently, it turns out that the covariance of a linear system driven by a train of Gaussiandistributed impulses whose arrival times follow a Poisson distribution is the same as the covariance of the same system driven by a white noise input process, except for the scaling of the process noise covariance by the Poisson process rate parameter [[32](16-bibliography.md#page-171-4)].

To understand this result, consider a linear model of the error in a spacecraft trajectory as follows

$$
\dot{\boldsymbol{\mathsf{x}}}(t) = \mathbf{A}(t)\boldsymbol{\mathsf{x}}(t) + \mathbf{B}(t)\boldsymbol{\mathsf{u}}(t) \tag{3.67}
$$

where $\boldsymbol{\mathsf{x}}$ represents the deviation of the actual position/velocity state from its estimated or nominal value, and $\boldsymbol{\mathsf{u}}$ represents the FLAK acceleration bias. Then, if we make use of inertial coordinates,

$$
\mathbf{A}(t) = \begin{bmatrix} \mathbf{0} & \mathbf{I} \\ \mathbf{G}(t) & \mathbf{0} \end{bmatrix}, \; \mathbf{B}(t) = \begin{bmatrix} \mathbf{0} \\ \mathbf{M}(t) \end{bmatrix} \tag{3.68}
$$

where $\mathbf{G}$ represents the gravity gradient matrix, and $\mathbf{M}$ is the direction cosine matrix rotating the supposed body-fixed FLAK into the inertial frame. There is no general solution to this differential equation, but over short time intervals, we can assume that

$$
\boldsymbol{\mathsf{x}}(t_k) = \boldsymbol{\Phi}(t_k, t_{k-1})\boldsymbol{\mathsf{x}}_{k-1} + \int_{t_{k-1}}^{t_k} \boldsymbol{\Phi}(t_k, \tau)\mathbf{B}(\tau)\boldsymbol{\mathsf{u}}(\tau)\, \mathrm{d}\tau \tag{3.69}
$$

where

$$
\boldsymbol{\Phi}(t_k, t_{k-1}) = \mathbf{I} + \mathbf{A}(t_k)(t_k - t_{k-1}) \tag{3.70}
$$

We assume the input is a sequence of velocity impulses of (random) length $n_k$,

$$
\boldsymbol{\mathsf{u}}(t) = \sum_{i=1}^{n_k} \boldsymbol{\mathsf{u}}_i\delta(t - t_i) \tag{3.71}
$$

with $t_{k-1} < t_i < t_k$. The delta functions annihilate the integral and our model becomes (with $\Delta t_i = t_k - t_i$):

$$
\boldsymbol{\mathsf{x}}(t_k) = \boldsymbol{\Phi}(t_k, t_{k-1})\boldsymbol{\mathsf{x}}_{k-1} + \sum_{i=1}^{n_k} \begin{bmatrix} \vec{\boldsymbol{\kappa}}_i\Delta t_i \\ \vec{\boldsymbol{\kappa}}_i \end{bmatrix} \|\boldsymbol{\mathsf{u}}_i\| \tag{3.72}
$$

where $\vec{\boldsymbol{\kappa}}_i$ is the unit inertial direction vector for the FLAK event. Note that the input response is in some sense fundamentally an increment to the entire state vector at each $t_k$; we can however compute an equivalent zero-order hold acceleration by dividing the velocity increment by the time step $t_k - t_{k-1}$.

Since we assume each impulse is zero-mean and Gaussian, the input response has zero mean. To find a tractable form for the covariance, assume that the direction of the FLAK event is constant over each interval $t_k - t_{k-1}$. This assumption assures that the impulses are identically distributed over each sampling interval. Then, the process noise covariance is given by Reference [32](16-bibliography.md#page-171-4):

$$
\mathbf{S}(t_k) = q\lambda\int_{t_{k-1}}^{t_k} \begin{bmatrix} \vec{\boldsymbol{\kappa}}_k(t_k - \tau) \\ \vec{\boldsymbol{\kappa}}_k \end{bmatrix} \begin{bmatrix} \vec{\boldsymbol{\kappa}}_k'(t_k - \tau), \vec{\boldsymbol{\kappa}}_k' \end{bmatrix} \mathrm{d}\tau \tag{3.73}
$$

where $q$ is the variance of the discrete Gaussian velocity impulses and $\lambda$ is the rate parameter of the Poisson process. Carrying out the integration results in

$$
\mathbf{S}(t_k) = q\lambda \begin{bmatrix} \vec{\boldsymbol{\kappa}}_k\vec{\boldsymbol{\kappa}}_k'\Delta t^3/3 & \vec{\boldsymbol{\kappa}}_k\vec{\boldsymbol{\kappa}}_k'\Delta t^2/2 \\ \vec{\boldsymbol{\kappa}}_k\vec{\boldsymbol{\kappa}}_k'\Delta t^2/2 & \vec{\boldsymbol{\kappa}}_k\vec{\boldsymbol{\kappa}}_k'\Delta t \end{bmatrix} \tag{3.74}
$$

where the product $q\lambda$ must have "SNC" kinds of units, such as meters$^2$ per second$^3$.

#### 3.2.3.6. Computational Considerations

The primary computational issues that can affect covariance propagation may be broadly characterized as underflow and overflow. Underflow can occur especially because many of the process noise parameters described above may often have values that approach computational truncation limits, which can lead to non-positive-definite process noise covariances. Overflow can similarly occur when truncation limits are approached by very large covariance values such as can occur with long propagation times. Because the orbital dynamics are at best marginally stable, even propagating without process noise can result in differences of many orders of magnitude between largest and smallest eigenvalues. This problem will be exacerbated if process noise is present, since all of the process noise models described above introduce unbounded position covariance error growth[<sup>5</sup>](#page-51-0).

<span id="page-51-0"></span><sup>5</sup> Reference [11](16-bibliography.md#page-170-11) proposes an approximate "solution" to this problem via a Floquet analysis of a modified set of covariance propagation dynamics that include artificially-introduced damping.

Simple tricks like enforcing symmetry, or adding a small positive diagonal matrix, will not always ensure positive eigenvalues in such cases. A better solution is to maintain the covariance in factorized form, for example as Chapter [8](08-factorization-methods.md#page-94-0) describes. In lieu of a fully factorized filtering approach, process noise factors may be computed from their factorizations. Chapter [6](06-bias-modeling.md#page-72-0) shows a few examples of Cholesky factorizations that may be employed in this fashion.

### 3.2.4. Tuning the Covariance Propagation

Since even the best practices this Chapter has discussed are at best approximations, it is inevitable that EKF designers must perform some artful tuning of the free parameters to achieve acceptable results. Furthermore, computational limitations of flight computers often lead to the need for compromises in modeling fidelity. What one generally hopes to accomplish via tuning of the covariance propagation is that any approximations or compromises the EKF has had to endure to be implementable have not impaired its covariance's accuracy too much. In particular, one would like to compute an idealized "truth" covariance matrix, based on the best-available models and data, and adjust the EKF's "formal" covariance via the tuning process to yield some semblance of a match.

In some cases, it is possible to compute the true covariance. In particular, if we are studying a linear system, and the random components have zero-mean Gaussian distributions, then the mean errors will be zero, and we can use linear covariance analysis [[27](16-bibliography.md#page-171-5), [58](16-bibliography.md#page-172-2), [60](16-bibliography.md#page-172-3)] to compute the covariances. It is often possible to approximate the performance for a nonlinear system with this technique by linearization. This is often a first step in early conceptual design studies.

One may divide tuning of the covariance propagation into those activities a designer performs (1) during the detailed development of a system, prior to the collection of any flight data, and (2) during the commissioning of a new system or an existing system in a new application, when flight data are available. For pre-flight detailed design studies, one generally simulates the system, so one has access to truth data. One can also run the mission simulation many times, generating an ensemble of parallel results, performing a Monte Carlo analysis. During and after the actual mission, we never have access to truth data. At best, we can reconstruct the trajectory after the fact using more sophisticated processing and additional data that were not available in real-time. For near real-time analysis, we can compare current state estimates to predictions from previous epochs. These predictions can come from either mission products generated in real-time at a past epoch, or past reconstructions of the trajectory. In all cases, the best we have are differences between estimates, not errors from the truth. There are several empirical approximations to the true covariance that one might use in these situations.

#### 3.2.4.1. Empirical Approximations of the True Covariance

Let $\boldsymbol{\mathsf{e}}_j(t_i)$ represent the random error vector at time $t_i$ for case $j$ from a Monte Carlo simulation, and $\{\boldsymbol{\mathsf{e}}(t_i)\}$ be the set of all cases at time $t_i$. Assume the total number of cases is $K$, and the total number of time samples is $N$.

**Time Series Expectation:** We can take statistics of the error realizations across time for each case, $\boldsymbol{e}_j(t_i)$, to get the time series expectations for each case:

$$
\hat{\mathrm{E}}_t(\boldsymbol{\mathsf{e}}_j) = \frac{1}{N}\sum_{i=1}^{N} \boldsymbol{e}_j(t_i) \tag{3.75}
$$

$$
\hat{\mathrm{E}}_t(\boldsymbol{\mathsf{e}}_j\boldsymbol{\mathsf{e}}_j^{\mathsf{T}}) = \frac{1}{N-1}\sum_{i=1}^{N} \boldsymbol{e}_j(t_i)\boldsymbol{e}_j^{\mathsf{T}}(t_i) \tag{3.76}
$$

If the data are stationary[<sup>6</sup>](#page-52-0), the time series statistics are usually an adequate approximation, if we have considered a long enough time span. In some systems, described as *ergodic*, a long time series is in some sense equivalent to a large number of shorter Monte Carlo cases.

<span id="page-52-0"></span><sup>6</sup> Stationary data are those for which the statistics do not change when the time origin shifts.

**Ensemble Expectation:** We can take statistics of the error realizations over all the cases at each time sample to get the ensemble expectations:

$$
\hat{\mathrm{E}}_e\{\boldsymbol{\mathsf{e}}(t_i)\} = \frac{1}{K}\sum_{j=1}^{K} \boldsymbol{e}_j(t_i) \tag{3.77}
$$

$$
\hat{\mathrm{E}}_e\{\boldsymbol{\mathsf{e}}(t_i)\boldsymbol{\mathsf{e}}^{\mathsf{T}}(t_i)\} = \frac{1}{K-1}\sum_{j=1}^{K} \boldsymbol{e}_j(t_i)\boldsymbol{e}_j^{\mathsf{T}}(t_i) \tag{3.78}
$$

The ensemble statistics will generally give the best indication of performance if the data are non-stationary, so long as we use an adequate number of Monte Carlo cases.

Since there is nothing analogous to an ensemble of Monte Carlo cases for flight data, we cannot use ensemble statistics as defined above. Let $\boldsymbol{\mathsf{d}}$ represent the random difference vector between the quantity of interest and its comparison value. We can apply time series statistics, but as the mission evolves, the span of the time series continually extends, so we have to decide which subsets of the entire mission span to use, e.g. the time series extending back over the entire history of the mission, extending back only over some shorter interval, etc., and also how frequently to recompute the time series statistics, e.g. continuously, once per day, etc. There are some other approximations to the expectation that we might use here.

**Sliding Window Time Series Expectation:** We can take statistics of the difference realizations, $\boldsymbol{d}(t_i)$, across a sliding window extending $\Delta t$ into the past from each observation, for each case, to get the $\Delta t$-sliding window time series expectations:

$$
\hat{\mathrm{E}}_{t,\Delta t}(\boldsymbol{\mathsf{d}}) = \frac{1}{\Delta n}\sum_{i=0}^{\Delta n - 1} \boldsymbol{d}(t_{N-i}) \tag{3.79}
$$

$$
\hat{\mathrm{E}}_{t,\Delta t}(\boldsymbol{\mathsf{d}}\boldsymbol{\mathsf{d}}^{\mathsf{T}}) = \frac{1}{\Delta n - 1}\sum_{i=0}^{\Delta n - 1} \boldsymbol{d}(t_{N-i})\boldsymbol{d}(t_{N-i})^{\mathsf{T}} \tag{3.80}
$$

where $\Delta n$ is the number of time samples in the window $\Delta t$.

**Period-Folding Expectation:** If the data are periodic, we can break up the data into $K$ spans of one period in duration each, and shift the time origin of each span so that the data are "folded" into the same, one-period-long interval. We can then take ensemble statistics over times at the same phase angle, $t_{\phi i}$, within each period.

$$
\hat{\mathrm{E}}_f\{\boldsymbol{\mathsf{d}}(t_{\phi i})\} = \frac{1}{K}\sum_{j=1}^{K} \boldsymbol{d}_j(t_{\phi i}) \tag{3.81}
$$

$$
\hat{\mathrm{E}}_f\{\boldsymbol{\mathsf{d}}(t_{\phi i})\boldsymbol{\mathsf{d}}(t_{\phi i})^{\mathsf{T}}\} = \frac{1}{K-1}\sum_{j=1}^{K} \boldsymbol{d}_j(t_{\phi i})\boldsymbol{d}_j^{\mathsf{T}}(t_{\phi i}) \tag{3.82}
$$

It is often useful to fold the data into bins of equal mean anomaly. This is especially useful for orbits with notable eccentricity, since it ensures that a roughly equal number of time points will be present in each bin.

**Sliding Window Period-Folding Expectation:** Period-folding can obviously be applied over a sliding window as well, with each window extending $n$ periods into the past.

$$
\hat{\mathrm{E}}_{f,n}\{\boldsymbol{\mathsf{d}}(t_{\phi i})\} = \frac{1}{n}\sum_{j=0}^{n-1} \boldsymbol{d}_{K-j}(t_{\phi i}) \tag{3.83}
$$

$$
\hat{\mathrm{E}}_{f,n}\{\boldsymbol{\mathsf{d}}(t_{\phi i})\boldsymbol{\mathsf{d}}(t_{\phi i})^{\mathsf{T}}\} = \frac{1}{n-1}\sum_{j=0}^{n-1} \boldsymbol{d}_{K-j}(t_{\phi i})\boldsymbol{d}_{K-j}^{\mathsf{T}}(t_{\phi i}) \tag{3.84}
$$

This is especially useful for identifying secular trends in periodic data sets.

#### 3.2.4.2. Tuning for Along-track Error Growth

As described above, the position error component along the orbit track will dominate covariance propagation error, and so the most important step in tuning the covariance propagation is to ensure that this component grows no faster or slower than it should based on the truncations and approximations that the EKF design has employed. One may use any of the analytical or empirical methods described above to estimate the "true" covariance. For example, for preflight analysis, one may generate a time series or ensemble of time series of differences between states propagated using the formal models the filter employs, and a best available "truth" model of the system. One can then compare the appropriate empirical covariance computed from this data set to the filter's formal covariance, and adjust the process noise intensities until a reasonable match occurs. For flight data analysis, one may similarly difference across overlaps between predictive and definitive states, and compare these empirical covariances of these differences to the sum of the predictive and definitive formal covariances from the filter.

If one uses the SNC method, the primary "knob" for tuning the alongtrack covariance growth rate is the corresponding alongtrack component of the process noise intensity $q_T$ or $q_V$, depending on whether RTN or VNB components are used, respectively. Essentially, an impulse along the velocity vector, or change in speed, causes a change in SMA, corresponding to a change in period, and hence a secular growth in position error along the orbit, as discussed at the beginning of this Chapter. This mechanism is especially transparent for near-circular orbits, and some simple analysis yields a good starting point. One may find a fuller exposition of the following result in Reference [28](16-bibliography.md#page-171-6).

<span id="page-54-1"></span>For near-circular orbits, the position components of the integrand in [\(3.44\)](#page-45-3) become, in RTN coordinates,

$$
\boldsymbol{\Phi}_{rv}(\Delta t) \begin{bmatrix} q_R & 0 & 0 \\ 0 & q_T & 0 \\ 0 & 0 & q_N \end{bmatrix} \boldsymbol{\Phi}_{rv}^{\mathsf{T}}(\Delta t) \tag{3.85}
$$

where $\boldsymbol{\Phi}_{rv}(\Delta t)$ is given, per Hill, Clohessy, and Wiltshire, by

$$
\boldsymbol{\Phi}_{rv}(\Delta t) = \begin{bmatrix} \sin(n\Delta t)/n & 2(1 - \cos(n\Delta t))/n & 0 \\ 2(\cos(n\Delta t) - 1)/n & 4\sin(n\Delta t)/n - 3\Delta t & 0 \\ 0 & 0 & \sin(n\Delta t)/n \end{bmatrix} \tag{3.86}
$$

Retaining only secular terms and carrying out the integral, the along-track component of the process noise covariance becomes

$$
S_T(\Delta t) \approx 3\Delta t^3 q_T \tag{3.87}
$$

an approximation which holds for $\Delta t > T_p$. Thus, one may use an empirical covariance of the along-track error after one orbit period, such as $\hat{\sigma}_{\delta s}^2 = \hat{\mathrm{E}}_f\{\delta s^2\}$, to derive a starting point from which to tune $q_T$, as

$$
q_T = \frac{\hat{\sigma}_{\delta s}^2}{3T_p^3} \tag{3.88}
$$

## 3.3. Covariance Measurement Update

<span id="page-54-0"></span>This section discusses methods for implementing the covariance measurement update. Some of the most important of these best practices are related to factorization methods and underweighting, which are topics of enough significance to warrant their own chapters.

### 3.3.1. "Stable Form" of non-Joseph Covariance Update

As Chapter [1](01-the-extended-kalman-filter.md#page-24-0) pointed out, only for the optimal gain and true covariance does the Joseph form of the covariance measurement update, [\(1.41\)](01-the-extended-kalman-filter.md#page-29-1),

$$
\mathbf{P}_i^+ = \left(\mathbf{I} - \mathbf{K}_i\mathbf{H}_i\right) \mathbf{P}_i^- \left(\mathbf{I} - \mathbf{K}_i\mathbf{H}_i\right)^{\mathsf{T}} + \mathbf{K}_i\mathbf{R}_i\mathbf{K}_i^{\mathsf{T}} \tag{3.89}
$$

reduce to [\(1.33\)](01-the-extended-kalman-filter.md#page-28-3),

$$
\mathbf{P}_i^+ = \mathbf{P}_i^- - \mathbf{K}_i \mathbf{H}_i \mathbf{P}_i^- \tag{3.90}
$$

While this assertion is strictly true, the cancellations that produce the above results will still occur so long as the EKF algorithm is internally consistent with truncating and approximating its various terms. The resulting "covariance" will not accurately represent $\mathrm{E}\big[\boldsymbol{\mathsf{e}}_i^+ (\boldsymbol{\mathsf{e}}_i^+)^{\mathsf{T}} \vert \mathbb{Y}_i\big]$, but the fact that these truncations and approximations have produced a suboptimal gain will, in themselves, provide no computational issues. In effect, the resulting suboptimal gain remains "optimal" with respect to the internally consistent set of approximations and truncations internal to the filter.

However, even if the gain is optimal, the stability of the non-Joseph form depends on the order of multiplication, as Schmidt points out [[75](16-bibliography.md#page-173-5)]. He describes a "stable form" of the non-Joseph update, given by Algorithm [3.1,](#page-55-0) which was successfully used by the Space Shuttle. Algorithm [3.1](#page-55-0) processes each $j$th scalar element of the measurement vector one at a time, using only the $j$th row of the measurement partials matrix, $\mathbf{h}_j$, and the $(j, j)$ diagonal element of the measurement noise covariance, $r_j$, assuming $\mathbf{R}_i$ is a diagonal matrix. In comparison with $\mathbf{P}_i^+ = (\mathbf{I} - \mathbf{K}_i\mathbf{H}_i)\mathbf{P}_i^-$, use of Algorithm [3.1](#page-55-0) also reduces the computational burden from $O(n^3)$ to $O(n^2/2)$, where $n$ is the state dimension.

Although Algorithm [3.1](#page-55-0) does not show the state update, it may also be sequentially updated as part of the iteration. However, the order in which the scalar measurements update the state can affect the outcome, if the measurement partials are computed one row at a time, corresponding with each scalar update. This may produce undesirable or even unstable outcomes. Chapter [4](04-processing-measurements.md#page-58-0) will discuss such issues further.

> <span id="page-55-0"></span>**Algorithm 3.1** "Stable form" of the non-Joseph Covariance Measurement Update
>
> $\mathbf{P}_1 = \mathbf{P}_i^-$
>
> **for** each scalar measurement $j = 1$ through $k$ **do**
>
> &emsp;$\mathbf{h}_j = j$th row of $\mathbf{H}_i$
>
> &emsp;$r_j = (j, j)$ element of $\mathbf{R}_i$
>
> &emsp;$\mathbf{b}_j = \mathbf{P}_j \mathbf{h}_j^{\mathsf{T}}$
>
> &emsp;$\mathbf{k}_j = \mathbf{b}_j / (\mathbf{h}_j \mathbf{b}_j + r_j)$
>
> &emsp;$\mathbf{P}_j \leftarrow \mathbf{P}_j - \mathbf{k}_j \mathbf{b}_j^{\mathsf{T}}$
>
> **end for**
>
> $\mathbf{P}_i^+ = \mathbf{P}_k$
>
> Only the non-redundant (upper or lower triangular) portions of the covariance should be updated, and then the other redundant elements set equal to the ones that have been computed.

Despite the extensive and successful flight heritage of Algorithm [3.1,](#page-55-0) it cannot guarantee numerical stability and positive definiteness of the covariance. Chapter [8](08-factorization-methods.md#page-94-0) describes a recommended best practice for the covariance update, the $UD$-factorization, which makes checking for positive definiteness transparently easy.

### 3.3.2. Use of Consider States

It may often be the case that unobservable states are present in the system being estimated. Most commonly, such states will be parameters whose values are unknown or uncertain. Inclusion of such parameters as solve-for states in the EKF is a not a recommended practice. However, if the EKF completely ignores the uncertainty that such parameters introduce, its covariance can become overly optimistic, a condition sometimes known as "filter smugness." One approach to addressing this problem was introduced by Schmidt [[75](16-bibliography.md#page-173-5)], originally in the context of reducing the computational burden that the EKF imposed on flight computers of the 1960's. Schmidt's idea is essentially for the EKF to maintain a covariance containing all of the states whose uncertainties are significant enough to affect filter performance, but only to update a subset of those states. The states which are not updated in this framework are typically known as "consider" parameters, and such a filter has been called a "consider filter" or a "Schmidt-Kalman" filter. Although most commonly the state space is simply partitioned by selecting states as either solve-for or consider states, Reference [58](16-bibliography.md#page-172-2) points out that partitioning using linear combinations of the full state space is also possible.

Following Reference [58](16-bibliography.md#page-172-2), suppose the filter produces estimates for a subset of $n_s$ solve-for states, out of the full state of size $n$. The filter does not estimate the remaining $n_c = n - n_s$ consider states. Denote the true solve-for vector by $\boldsymbol{\mathsf{s}}(t)$, and the true consider vector by $\boldsymbol{\mathsf{c}}(t)$. Assume that these are linear combinations of the true states, according to the following:

<span id="page-55-1"></span>
$$
\boldsymbol{\mathsf{s}}(t) = \mathbf{S}(t)\boldsymbol{\mathsf{x}}(t) \quad \text{and} \quad \boldsymbol{\mathsf{c}}(t) = \mathbf{C}(t)\boldsymbol{\mathsf{x}}(t) \tag{3.91}
$$

where the $n_s \times n$ matrix $\mathbf{S}(t)$ and the $n_c \times n$ matrix $\mathbf{C}(t)$ are such that the matrix

$$
\mathbf{M} = \begin{bmatrix} \mathbf{S} \\ \mathbf{C} \end{bmatrix} \tag{3.92}
$$

is non-singular. The inverse of $\mathbf{M}$ is partitioned into an $n \times n_s$ matrix $\tilde{\mathbf{S}}$ and an $n \times n_c$ matrix $\tilde{\mathbf{C}}$:

$$
\mathbf{M}^{-1} = \begin{bmatrix} \tilde{\mathbf{S}}, & \tilde{\mathbf{C}} \end{bmatrix}. \tag{3.93}
$$

The properties of the matrix inverse then lead immediately to the identities

$$
\mathbf{S}\tilde{\mathbf{S}} = \mathbf{I}_{n_s}, \quad \mathbf{C}\tilde{\mathbf{C}} = \mathbf{I}_{n_c}, \quad \mathbf{S}\tilde{\mathbf{C}} = \mathbf{0}_{n_s \times n_c}, \quad \mathbf{C}\tilde{\mathbf{S}} = \mathbf{0}_{n_c \times n_s}, \tag{3.94}
$$

and

<span id="page-56-1"></span>
$$
\tilde{\mathbf{S}}\mathbf{S} + \tilde{\mathbf{C}}\mathbf{C} = \mathbf{I}_n. \tag{3.95}
$$

In the usual case that the elements of the solve-for and consider vectors are merely selected and possibly permuted components of the state vector, the matrix $\mathbf{M}$ is an orthogonal permutation matrix. In this case, and in any case for which $\mathbf{M}$ is orthogonal, the matrices $\tilde{\mathbf{S}}$ and $\tilde{\mathbf{C}}$ are just the transposes of $\mathbf{S}$ and $\mathbf{C}$, respectively, which makes inversion of $\mathbf{M}$ unnecessary and simplifies many of the following equations.

It follows from Eqs. [3.91](#page-55-1) and [3.95](#page-56-1) that

$$
\boldsymbol{\mathsf{x}}(t) = \tilde{\mathbf{S}}(t)\boldsymbol{\mathsf{s}}(t) + \tilde{\mathbf{C}}(t)\boldsymbol{\mathsf{c}}(t). \tag{3.96}
$$

Relations similar to Eq. [3.91](#page-55-1) give the estimated solve-for vector $\hat{\boldsymbol{\mathsf{s}}}(t)$ and the assumed consider vector $\hat{\boldsymbol{\mathsf{c}}}(t)$ in terms of the estimated state $\hat{\boldsymbol{\mathsf{x}}}(t)$. Thus, errors in the solve-for and consider states are given by

$$
\boldsymbol{\mathsf{e}}_s(t) = \boldsymbol{\mathsf{s}}(t) - \hat{\boldsymbol{\mathsf{s}}}(t) = \mathbf{S}(t)\boldsymbol{\mathsf{e}}(t) \tag{3.97}
$$

$$
\boldsymbol{\mathsf{e}}_c(t) = \boldsymbol{\mathsf{c}}(t) - \hat{\boldsymbol{\mathsf{c}}}(t) = \mathbf{C}(t)\boldsymbol{\mathsf{e}}(t) \tag{3.98}
$$

and the true error may be written in terms of the solve-for and consider errors by

$$
\boldsymbol{\mathsf{e}}(t) = \tilde{\mathbf{S}}(t)\boldsymbol{\mathsf{e}}_s(t) + \tilde{\mathbf{C}}(t)\boldsymbol{\mathsf{e}}_c(t). \tag{3.99}
$$

In terms of this notation, the EKF update has the form

$$
\hat{\boldsymbol{\mathsf{s}}}_i^+ = \hat{\boldsymbol{\mathsf{s}}}_i^- + \mathbf{K}_i\boldsymbol{\mathsf{r}}_i^- \tag{3.100}
$$

where

$$
\boldsymbol{\mathsf{r}}_i^- = \boldsymbol{\mathsf{y}}_i - \boldsymbol{h}(\hat{\boldsymbol{\mathsf{x}}}_i^-) = \mathbf{H}_i\boldsymbol{\mathsf{e}}_i^- + \boldsymbol{\mathsf{v}}_i, \tag{3.101}
$$

and the subscript $i$ is a shorthand for the time argument $t_i$. The usual EKF will not contain the full covariance, but only its solve-for part

$$
\mathbf{P}_{ss}(t) = \mathrm{E}\left[\boldsymbol{\mathsf{e}}_s(t)\boldsymbol{\mathsf{e}}_s^{\mathsf{T}}(t)\right] \tag{3.102}
$$

By contrast, the Schmidt-Kalman filter will use the full covariance, $\mathbf{P}(t)$. In the usual case, the Kalman gain is given by

$$
\mathbf{K}_i = \mathbf{P}_{ssi}^-\mathbf{H}_{si}^{\mathsf{T}}\left[\mathbf{H}_{si}\mathbf{P}_{ssi}^-\mathbf{H}_{si}^{\mathsf{T}} + \mathbf{R}_i\right]^{-1} \tag{3.103}
$$

where

$$
\mathbf{H}_{si} = \mathbf{H}_i\tilde{\mathbf{S}}_i \tag{3.104}
$$

In the Schmidt-Kalman case,

$$
\mathbf{K}_i = \mathbf{S}_i\mathbf{P}_i^-\mathbf{H}_i^{\mathsf{T}}\left[\mathbf{H}_i\mathbf{P}_i^-\mathbf{H}_{si}^{\mathsf{T}} + \mathbf{R}_i\right]^{-1} \tag{3.105}
$$

Thus, the Schmidt-Kalman gain matrix is computed from the full covariance, but only applies measurement innovations to the solve-for states.

## 3.4. Sigma-Point Methods

<span id="page-56-0"></span>Before concluding this Chapter, it is worth noting that a promising method for propagating and updating the covariance that is coming into greater use and acceptance within the navigation community is the use of sigma-point methods, also known as "unscented" transforms. A subsequent chapter covering Advanced Topics will cover these topics in a section on sigma-point filtering.

---

[← Chapter 2. Batch-Sequential Filters](02-batch-sequential-filters.md) · [Contents](README.md) · [Chapter 4. Processing Measurements →](04-processing-measurements.md)
