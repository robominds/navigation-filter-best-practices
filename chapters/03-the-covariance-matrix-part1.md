[← Chapter 2. Batch-Sequential Filters](02-batch-sequential-filters.md) · [Contents](README.md) · [Chapter 3. The Covariance Matrix (part 2 of 3) →](03-the-covariance-matrix-part2.md)

# <span id="page-38-0"></span>Chapter 3. The Covariance Matrix

*Contributed by J. Russell Carpenter*

As Chapter [1](01-the-extended-kalman-filter.md#page-24-0) pointed out, the EKF estimate $`\hat{{𝑿}}(t)`$ is at best an approximation for $`\mathrm{E}[{𝗫}(t)|{𝕐}]`$, and hence the EKF symbol $`{𝐏}(t)`$ is at best an approximation for $`\mathrm{E}[{𝗲}(t){𝗲}^{{𝖳}}(t)|{𝕐}]`$. In the present Chapter we discuss best practices for maintaining such approximations, and henceforth we will simply refer to $`{𝐏}(t)`$ as the covariance matrix.

## 3.1. Metrics for Orbit State Covariances

<span id="page-38-1"></span>To discuss what makes one covariance approximation better or worse than another, we must be able to compare matrices to one another, and hence we must adopt metrics. For matrices that serve as coefficients, there exist various matrix norms that serve as distance-like metrics for the strength of the coefficient. For covariance matrices, we are usually more interested in measures of the range of possible realizations that could be drawn from the probability distribution characterized by the covariance. The square root of the trace of the covariance is often a reasonable choice, since it is the root sum squared (RSS) formal estimation error. A drawback to the trace for orbital applications is that coordinates and their derivatives typically differ by several orders of magnitude, so that for example the RSS position error will dominate the RSS velocity error if the trace is taken over a $`6 \times 6`$ Cartesian position and velocity state error covariance, unless some scaling is introduced. Although arbitrary scalings are possible, we discuss several metrics herein that have been found to be especially suitable to space applications.

Orbit determination is distinguishable from other types of positioning and navigation not only by the use of dynamics suitable to orbiting bodies, but also by a fundamental need to produce states that predict accurately. This need arises because spacecraft operations require accurate predictions for acquisition by communications assets, for planning future activities such as maneuvers and observations, for predicting conjunctions with other space objects, etc. For closed, i.e. elliptical, orbits about most planetary bodies, the two-body potential dominates all other forces by several orders of magnitude. Thus, in most cases, the ability of an orbit estimate to predict accurately is dominated by semi-major axis (SMA) error, $`\delta a`$. This is because SMA error translates into period error through Kepler's third law, and an error in orbit period translates into a secularly increasing error in position along the orbit track. As Reference [[10](16-bibliography.md#page-170-8)] shows, the along-track drift per orbit revolution, $`\delta s`$, for an elliptical orbit with eccentricity $`e`$ is bounded by

```math
\delta s = -3\pi\sqrt{\frac{1+e}{1-e}}\,\delta a \quad \text{from periapse to periapse} \qquad\qquad(3.1)
```

```math
\delta s = -3\pi\sqrt{\frac{1-e}{1+e}}\,\delta a \quad \text{from apoapse to apoapse} \qquad\qquad(3.2)
```

This phenomenon is especially significant for rendezvous and formation flying applications, where relative positions must be precisely controlled.

For a central body whose gravitational constant is $`\mu`$, the SMA of a closed Keplerian orbit, $`a`$, may be found from the *vis viva* equation,

<span id="page-39-0"></span>

```math
-\frac{\mu}{2a} = -\frac{\mu}{r} + \frac{v^2}{2} \qquad\qquad(3.3)
```

from which one can see that achieving SMA accuracy requires good knowledge of both radius, $`r`$, and speed, $`v`$. What is less obvious from [\(3.3\)](#page-39-0) is that radius and speed errors must also be both well-balanced and well-correlated to maximize SMA accuracy [[10](16-bibliography.md#page-170-8),[13](16-bibliography.md#page-170-9),[35](16-bibliography.md#page-171-3)], as Figure [3.1](#page-39-1) illustrates. In this figure, radius standard deviation, or formal error, $`\sigma_r`$, has been normalized by the squared ratio of radius to SMA, and speed formal error, $`\sigma_v`$, has been normalized by $`nv_c/v`$, where the orbital rate is $`n = \sqrt{\mu/a^3}`$, and the circular speed is $`v_c = \sqrt{\mu/a}`$, to make the relationships illustrated be independent of any particular point in any particular closed orbit. Figure [3.1](#page-39-1)'s contours of constant SMA error, $`\sigma_a`$, show that $`\sigma_a`$ is dominated by radius error below a diagonal region, and dominated by speed error above the diagonal. When radius and speed errors are balanced, along the diagonal, SMA accuracy can be substantially improved by increasing (negative) correlation. Experience has shown that $`\sigma_a`$ is one of the more useful figures of merit for evaluating orbit determination performance, particularly for relative navigation applications.

![](../_page_39_Figure_6.jpeg)

<span id="page-39-1"></span>*Figure 3.1. Formal error in semi-major axis depends on formal errors in radius, speed, their correlation, and their balance. All scales are in units of position.*

In fact, it is easy to show that any function of two (scalar) random variables possesses a similar correlation and balance structure, at least to first order. For example, navigation requirements for atmospheric entry are often stated in terms of flight-path angle error, $`\delta\gamma`$. Since $`\sin\gamma = \vec{{𝒓}}/\|\vec{{𝒓}}\| \cdot \vec{{𝒗}}/\|\vec{{𝒗}}\|`$, then from geometrical considerations we should expect that $`\delta\gamma`$ depends on the component of position error which is in the local horizontal plane, in the direction of the velocity vector, and on the component of velocity error that is normal to both velocity and angular momentum, i.e. binormal to the velocity vector. These are of course the in-plane components of position and velocity that are normal to radius and speed. Thus by using the pair $`\delta a`$ and $`\delta\gamma`$ as metrics, we can fully characterize the correlation and balance of the in-plane covariance components. The following subsections derive these relationships.

### 3.1.1. Variance of an Arbitrary Function of Two Random Variables

Suppose there exists a random variable $`{𝗓}`$ which is a possibly nonlinear function[<sup>1</sup>](#page-40-0) of two other random variables, $`{𝗑}`$ and $`{𝗒}`$, such that

```math
{𝗓} = f({𝗑}, {𝗒}) \qquad\qquad(3.4)
```

and let the joint covariance of $`{𝗑}`$ and $`{𝗒}`$ be given by

```math
{𝐏} = \begin{bmatrix} \sigma_{{𝗑}}^2 & \rho_{{𝗑𝗒}}\sigma_{{𝗑}}\sigma_{{𝗒}} \\ \rho_{{𝗑𝗒}}\sigma_{{𝗑}}\sigma_{{𝗒}} & \sigma_{{𝗒}}^2 \end{bmatrix} \qquad\qquad(3.5)
```

The variance of $`{𝗓}`$ is given by

```math
\sigma_{{𝗓}}^2 = \mathrm{E}\big[({𝗓} - \mathrm{E}[{𝗓}])^2\big] \qquad\qquad(3.6)
```

where

```math
\mathrm{E}[{𝗓}] = \int_{-\infty}^{\infty} \zeta\, \mathrm{p}_{{𝗓}}(\zeta)\, \mathrm{d}\zeta = \int_{-\infty}^{\infty}\int_{-\infty}^{\infty} f(\xi, \eta)\, \mathrm{p}_{{𝗓}}(f(\xi, \eta))\, \mathrm{d}\xi\, \mathrm{d}\eta \qquad\qquad(3.7)
```

Let $`\hat{x} = \mathrm{E}[{𝗑}]`$ and $`\hat{y} = \mathrm{E}[{𝗒}]`$. Then $`\mathrm{E}[{𝗑} - \hat{x}] = 0`$ and $`\mathrm{E}[{𝗒} - \hat{y}] = 0`$. Expanding $`f({𝗑}, {𝗒})`$ around $`f(\hat{x}, \hat{y})`$ in a Taylor series to first order, we find that

```math
f({𝗑}, {𝗒}) \approx f(\hat{x}, \hat{y}) + f_x \cdot ({𝗑} - \hat{x}) + f_y \cdot ({𝗒} - \hat{y}) \qquad\qquad(3.8)
```

where $`f_x`$ and $`f_y`$ are the partials of $`f`$ with respect to $`x`$ and $`y`$, respectively; so, to first order,

```math
\hat{z} = \mathrm{E}[{𝗓}] = \mathrm{E}[f({𝗑}, {𝗒})] \approx f(\hat{x}, \hat{y}) \qquad\qquad(3.9)
```

Now let us similarly expand $`({𝗓} - \mathrm{E}[{𝗓}])^2`$ to first order:

```math
({𝗓} - \mathrm{E}[{𝗓}])^2 = (f({𝗑}, {𝗒}) - f(\hat{x}, \hat{y}))^2 \qquad\qquad(3.10)
```

```math
\approx f_x^2 \cdot ({𝗑} - \hat{x})^2 + 2 f_x f_y \cdot ({𝗑} - \hat{x})({𝗒} - \hat{y}) + f_y^2 \cdot ({𝗒} - \hat{y})^2 \qquad\qquad(3.11)
```

Taking expectations on both sides yields

```math
\mathrm{E}\big[({𝗓} - \mathrm{E}[{𝗓}])^2\big] = f_x^2\, \mathrm{E}\big[({𝗑} - \hat{x})^2\big] + 2 f_x f_y\, \mathrm{E}[({𝗑} - \hat{x})({𝗒} - \hat{y})] + f_y^2\, \mathrm{E}\big[({𝗒} - \hat{y})^2\big] \qquad\qquad(3.12)
```

```math
\sigma_{{𝗓}}^2 = f_x^2 \sigma_{{𝗑}}^2 + 2 f_x f_y \rho_{{𝗑𝗒}} \sigma_{{𝗑}} \sigma_{{𝗒}} + f_y^2 \sigma_{{𝗒}}^2 \qquad\qquad(3.13)
```

```math
= {𝐅}{𝐏}{𝐅}^{{𝖳}} \qquad\qquad(3.14)
```

where $`{𝐅} = [f_x, f_y]`$. Since $`-1 \lt \rho_{{𝗑𝗒}} \lt 1`$, it is clear that a high negative correlation between $`{𝗑}`$ and $`{𝗒}`$ will minimize $`\sigma_{{𝗓}}`$ for given values of $`\sigma_{{𝗑}}`$ and $`\sigma_{{𝗒}}`$, but if either $`f_x\sigma_{{𝗑}} \gt  \gt f_y\sigma_{{𝗒}}`$ or $`f_x\sigma_{{𝗑}} \lt  \lt f_y\sigma_{{𝗒}}`$, the impact of the negative correlation will be insignificant. Thus, the only way to simultaneously achieve $`\sigma_{{𝗓}} \lt  \lt f_x\sigma_{{𝗑}}`$ and $`\sigma_{{𝗓}} \lt  \lt f_y\sigma_{{𝗒}}`$ is when $`\rho_{{𝗑𝗒}} \approx -1`$ and $`f_x\sigma_{{𝗑}} \approx f_y\sigma_{{𝗒}}`$, which are the correlation and balance conditions mentioned above, and which occur along the diagonal of Figure [3.1.](#page-39-1)

<span id="page-40-0"></span><sup>1</sup> If the function is nonlinear, the variance formula here is an approximate, first-order result.

Note also that by defining new variables scaled by their respective partial derivatives, $`\tilde{x} = x f_x`$ and $`\tilde{y} = y f_y`$, and correspondingly $`\tilde{\sigma}_{{𝗑}} = f_x\sigma_{{𝗑}}`$ and $`\tilde{\sigma}_{{𝗒}} = f_y\sigma_{{𝗒}}`$, then a normalization of the fashion described above is also possible:

```math
\sigma_{{𝗓}} = \sqrt{\tilde{\sigma}_{{𝗑}}^2 + 2\rho_{{𝗑𝗒}}\tilde{\sigma}_{{𝗑}}\tilde{\sigma}_{{𝗒}} + \tilde{\sigma}_{{𝗒}}^2} \qquad\qquad(3.15)
```

### 3.1.2. Semi-Major Axis Variance

To derive a relationship for semi-major axis variance, let us take variations on [\(3.3\)](#page-39-0), which results in

```math
\frac{\delta a}{a^2} = \frac{2\delta r}{r^2} + \frac{2v\delta v}{\mu} \qquad\qquad(3.16)
```

If we replace the variations with deviations of random variables from their expectations, and the non-deviated terms with their expected values, we find that

```math
({𝖺} - \hat{a}) = 2\hat{a}^2 \left( \frac{({𝗋} - \hat{r})}{\hat{r}^2} + \frac{\hat{v}({𝗏} - \hat{v})}{\mu} \right) \qquad\qquad(3.17)
```

which by squaring and taking expectation yields the following linearized approximation for the SMA variance:

<span id="page-41-0"></span>

```math
\sigma_{{𝖺}}^2 = 4\hat{a}^4 \biggl\{ \frac{1}{\hat{r}^4}\sigma_{{𝗋}}^2 + 2\frac{\hat{v}}{\mu\hat{r}^2}\rho_{{𝗋𝗏}}\sigma_{{𝗋}}\sigma_{{𝗏}} + \frac{\hat{v}^2}{\mu^2}\sigma_{{𝗏}}^2 \biggr\} \qquad\qquad(3.18)
```

For the normalization used in Figure [3.1,](#page-39-1) rewrite [\(3.18\)](#page-41-0) as

```math
\sigma_{{𝖺}} = 2\sqrt{\biggl(\frac{\sigma_{{𝗋}}}{\hat{r}^2/\hat{a}^2}\biggr)^2 + 2\rho_{{𝗋𝗏}}\biggl(\frac{\sigma_{{𝗋}}}{\hat{r}^2/\hat{a}^2}\biggr)\biggl(\frac{\sigma_{{𝗏}}}{\mu/(\hat{a}^2\hat{v})}\biggr) + \biggl(\frac{\sigma_{{𝗏}}}{\mu/(\hat{a}^2\hat{v})}\biggr)^2} \qquad\qquad(3.19)
```

and note that $`\mu/(\hat{a}^2\hat{v}) = \hat{n}\hat{v}_c/\hat{v}`$. As mentioned above, normalizing radius and speed standard deviation in this manner permits comparison of data across all points in all closed orbits.

If the orbit is exactly circular, then further simplification of [\(3.18\)](#page-41-0) is possible. In this case, $`a = r`$ and $`v/\mu = T_p/2\pi`$, where $`T_p`$ is the orbit period. Then [\(3.18\)](#page-41-0) may be rewritten as

```math
\sigma_{{𝖺}} = 2\sqrt{\sigma_{{𝗋}}^2 + 2\left(\frac{T_p}{2\pi}\right)\rho_{{𝗋𝗏}}\sigma_{{𝗋}}\sigma_{{𝗏}} + \left(\frac{T_p}{2\pi}\right)^2\sigma_{{𝗏}}^2} \qquad\qquad(3.20)
```

For orbit determination applications, the state representation most often chosen is a Cartesian inertial state vector, $`{𝐱} = [\vec{{𝒓}}^{{𝖳}}, \vec{{𝒗}}^{{𝖳}}]^{{𝖳}}`$. Rewriting [\(3.3\)](#page-39-0) as

```math
a({𝐱}) = \left( \frac{2}{\|\vec{{𝒓}}\|} - \frac{\|\vec{{𝒗}}\|^2}{\mu} \right)^{-1} \qquad\qquad(3.21)
```

and taking partials yields

```math
\left.\frac{\partial a}{\partial {𝐱}}\right|_{\hat{{𝐱}}} = {𝐅}_a(\hat{{𝐱}}) = 2\hat{a}^2 \begin{bmatrix} \dfrac{\hat{\vec{{𝒓}}}^{{𝖳}}}{\hat{r}^3} & \dfrac{\hat{\vec{{𝒗}}}^{{𝖳}}}{\mu} \end{bmatrix} \qquad\qquad(3.22)
```

so that

```math
\sigma_{{𝖺}}^2 = {𝐅}_a(\hat{{𝒙}}){𝐏}_{{𝘅}}{𝐅}_a^{{𝖳}}(\hat{{𝒙}}) \qquad\qquad(3.23)
```

where $`{𝐏}_{{𝘅}}`$ is the state error covariance.

### 3.1.3. Flight-Path Angle Variance

The flight-path angle, $`\gamma`$, is the angle between the velocity vector and the local horizontal plane; it is therefore the complement of the angle between the position and velocity vectors, so that

```math
\gamma = \arcsin({𝒖}_{\vec{{𝒓}}} \cdot {𝒖}_{\vec{{𝒗}}}) \qquad\qquad(3.24)
```

where $`{𝒖}_{\vec{{𝒓}}} = \vec{{𝒓}}/r`$ and $`{𝒖}_{\vec{{𝒗}}} = \vec{{𝒗}}/v`$. Taking partials with respect to $`{𝒙}`$, we find that

```math
F_{\gamma}(\hat{{𝒙}}) = \left.\frac{\partial \gamma}{\partial {𝒙}}\right|_{\hat{{𝒙}}} = \frac{1}{\sqrt{1 - \sin^2\hat{\gamma}}} \begin{bmatrix} \dfrac{{𝒖}_{\hat{{𝒗}}}^{{𝖳}} - \sin\hat{\gamma}\,{𝒖}_{\hat{{𝒓}}}^{{𝖳}}}{\hat{r}} & \dfrac{{𝒖}_{\hat{{𝒓}}}^{{𝖳}} - \sin\hat{\gamma}\,{𝒖}_{\hat{{𝒗}}}^{{𝖳}}}{\hat{v}} \end{bmatrix}, \; -\frac{\pi}{2} \lt \hat{\gamma} \lt \frac{\pi}{2} \qquad\qquad(3.25)
```

so that

<span id="page-42-0"></span>

```math
\sigma_{\gamma}^2 = {𝐅}_{\gamma}(\hat{{𝒙}}){𝐏}_{{𝘅}}{𝐅}_{\gamma}^{{𝖳}}(\hat{{𝒙}}) \qquad\qquad(3.26)
```

which is a form suitable for use in an OD filter estimating a Cartesian inertial state.

For analysis, a simpler form of [\(3.26\)](#page-42-0) is as follows. Let us define two vectors that are normal to both the position vector and a vector normal to the orbit plane, $`\vec{{𝒏}}`$: the unit in-track vector,

```math
{𝒖}_{\Delta\vec{{𝒗}}} = {𝒖}_{\vec{{𝒏}}} \times {𝒖}_{\vec{{𝒓}}} = \frac{{𝒖}_{\vec{{𝒗}}} - {𝒖}_{\vec{{𝒓}}}\sin\gamma}{\sqrt{1 - \sin^2\gamma}} \qquad\qquad(3.27)
```

which defines a unit vector in the orbit plane that is along the orbit track at apoapsis and periapsis, and the unit bi-normal vector,

```math
{𝒖}_{\vec{{𝒃}}} = {𝒖}_{\vec{{𝒗}}} \times {𝒖}_{\vec{{𝒏}}} = \frac{{𝒖}_{\vec{{𝒓}}} - {𝒖}_{\vec{{𝒗}}}\sin\gamma}{\sqrt{1 - \sin^2\gamma}} \qquad\qquad(3.28)
```

which defines a unit vector in the orbit plane that is along the position vector at apoapsis and periapsis. Let us next define a composite transformation matrix as follows. Let

```math
{𝐌}_{rtn} = \begin{bmatrix} {𝒖}_{\vec{{𝒓}}_{{ℐ}}} & {𝒖}_{\Delta\vec{{𝒗}}_{{ℐ}}} & {𝒖}_{\vec{{𝒏}}_{{ℐ}}} \end{bmatrix} \qquad\qquad(3.29)
```

where the subscript $`{ℐ}`$ indicates that the specified vector is expressed in an inertial basis. The unitary matrix $`{𝐌}_{rtn}^{{𝖳}}`$ thus transforms coordinates of vectors in physical space, which are given in the frame $`{ℐ}`$, to a coordinates defined in the basis given by the the radial, transverse, and normal unit vectors. Similarly, define $`{𝐌}_{vnb}`$ as

```math
{𝐌}_{vnb} = \begin{bmatrix} {𝒖}_{\vec{{𝒗}}_{{ℐ}}} & {𝒖}_{\vec{{𝒏}}_{{ℐ}}} & {𝒖}_{\vec{{𝒃}}_{{ℐ}}} \end{bmatrix} \qquad\qquad(3.30)
```

Now define the block diagonal transformation matrix $`{𝐌}`$ as

```math
{𝐌} = \begin{bmatrix} {𝐌}_{rtn} & {𝟎}_{3x3} \\ {𝟎}_{3x3} & {𝐌}_{vnb} \end{bmatrix} \qquad\qquad(3.31)
```

Using the matrix $`{𝐌}`$, we can transform the state error covariance, given in inertial coordinates, such that its position error covariance is expressed in the "RTN" frame, and its velocity error covariance is in the "VNB" frame. Using the preceding results in [\(3.26\)](#page-42-0) results in considerable simplification:

<span id="page-42-1"></span>

```math
\sigma_{\gamma}^2 = \begin{bmatrix} {𝒖}_{\hat{{𝒕}}}^{{𝖳}}/\hat{r} & {𝒖}_{\hat{{𝒃}}}^{{𝖳}}/\hat{v} \end{bmatrix} \begin{bmatrix} {𝐌}_{rtn}^{{𝖳}} & {𝟎}_{3x3} \\ {𝟎}_{3x3} & {𝐌}_{vnb}^{{𝖳}} \end{bmatrix} {𝐏}_{{𝘅}} \begin{bmatrix} {𝐌}_{rtn} & {𝟎}_{3x3} \\ {𝟎}_{3x3} & {𝐌}_{vnb} \end{bmatrix} \begin{bmatrix} {𝒖}_{\hat{{𝒕}}}/\hat{r} \\ {𝒖}_{\hat{{𝒃}}}/\hat{v} \end{bmatrix} \qquad\qquad(3.32)
```

```math
= \left(\frac{\sigma_{{𝗿}_{{𝒕}}}}{\hat{r}}\right)^2 + 2\rho_{{𝗿}_{{𝒕}}{𝘃}_{{𝒃}}}\left(\frac{\sigma_{{𝗿}_{{𝒕}}}}{\hat{r}}\right)\left(\frac{\sigma_{{𝘃}_{{𝒃}}}}{\hat{v}}\right) + \left(\frac{\sigma_{{𝘃}_{{𝒃}}}}{\hat{v}}\right)^2 \qquad\qquad(3.33)
```

which demonstrates the aforementioned assertion that flight-path angle error depends on the intrack component of position error, and the bi-normal component of velocity error. Note that [\(3.33\)](#page-42-1) possesses the desirable feature that the relevant covariance information (in-track position variance and bi-normal velocity variance) is normalized by radius and speed, allowing differing orbital <span id="page-43-1"></span>conditions to be readily compared with one another. In most applications, $`\sigma_{{𝗿}_{{𝒕}}} \lt  \lt \hat{r}`$ and $`\sigma_{{𝘃}_{{𝒃}}} \lt  \lt \hat{v}`$ so that these ratios can be taken as small angles and expressed in angular measures commensurate with the units chosen for flight-path angle itself. Figure [3.2](#page-43-0) employs this convention.

![](../_page_43_Figure_3.jpeg)

<span id="page-43-0"></span>*Figure 3.2. Formal error in flight-path angle depends on formal errors of in-track component of position, bi-normal component of velocity, their correlation, and their balance.*

### 3.1.4. Summary of Orbit Determination Covariance Metrics

A recommended best practice for comparison of OD covariances is to use the semi-major axis standard deviation as a metric for most applications, with a secondary emphasis on flight-path angle standard deviation. For entry applications, a best practice is to use flight-path angle standard deviation at entry interface as the primary metric. In using these metrics, one should keep in mind that when computed in the manner shown here, they are nonlinear functions of the state variables, and hence do not preserve properties of the underlying state error distributions. A summary of these metrics is as follows.

> <span id="page-44-3"></span>For orbits that are very close to circular:
>
> ```math
> \sigma_{{𝖺}} = 2\sqrt{\sigma_{{𝗋}}^2 + 2\left(\frac{T_p}{2\pi}\right)\rho_{{𝗋𝗏}}\sigma_{{𝗋}}\sigma_{{𝗏}} + \left(\frac{T_p}{2\pi}\right)^2\sigma_{{𝗏}}^2} \qquad\qquad(3.34)
> ```
>
> For elliptical orbits:
>
> ```math
> \sigma_{{𝖺}} = 2\hat{a}^2\sqrt{\frac{1}{\hat{r}^4}\sigma_{{𝗋}}^2 + 2\frac{\hat{v}}{\mu\hat{r}^2}\rho_{{𝗋𝗏}}\sigma_{{𝗋}}\sigma_{{𝗏}} + \frac{\hat{v}^2}{\mu^2}\sigma_{{𝗏}}^2} \qquad\qquad(3.35)
> ```
>
> For normalization of radius and speed standard deviations across points in closed orbits:
>
> ```math
> \sigma_{{𝖺}} = 2\sqrt{\biggl(\frac{\sigma_{{𝗋}}}{\hat{r}^2/\hat{a}^2}\biggr)^2 + 2\rho_{{𝗋𝗏}}\biggl(\frac{\sigma_{{𝗋}}}{\hat{r}^2/\hat{a}^2}\biggr)\left(\frac{\sigma_{{𝗏}}}{\hat{n}\hat{v}_c/\hat{v}}\right) + \left(\frac{\sigma_{{𝗏}}}{\hat{n}\hat{v}_c/\hat{v}}\right)^2} \qquad\qquad(3.36)
> ```
>
> For entry applications, and as a secondary metric:
>
> ```math
> \sigma_{\gamma} = \sqrt{\left(\frac{\sigma_{{𝗿}_{{𝒕}}}}{\hat{r}}\right)^2 + 2\rho_{{𝗿}_{{𝒕}}{𝘃}_{{𝒃}}}\left(\frac{\sigma_{{𝗿}_{{𝒕}}}}{\hat{r}}\right)\left(\frac{\sigma_{{𝘃}_{{𝒃}}}}{\hat{v}}\right) + \left(\frac{\sigma_{{𝘃}_{{𝒃}}}}{\hat{v}}\right)^2} \qquad\qquad(3.37)
> ```
>
> For use in an OD filter that is estimating a Cartesian inertial state vector:
>
> ```math
> \sigma_{{𝖺}} = \sqrt{{𝐅}_a(\hat{{𝐱}}){𝐏}_{{𝐱}}{𝐅}_a^{{𝖳}}(\hat{{𝐱}})}, \quad {𝐅}_a(\hat{{𝐱}}) = 2\hat{a}^2 \begin{bmatrix} \dfrac{\hat{\vec{{𝒓}}}^{{𝖳}}}{\hat{r}^3} & \dfrac{\hat{\vec{{𝒗}}}^{{𝖳}}}{\mu} \end{bmatrix} \qquad\qquad(3.38)
> ```
>
> ```math
> \sigma_{\gamma} = \sqrt{{𝐅}_{\gamma}(\hat{{𝐱}}){𝐏}_{{𝐱}}{𝐅}_{\gamma}^{{𝖳}}(\hat{{𝐱}})}, \quad {𝐅}_{\gamma}(\hat{{𝐱}}) = \begin{bmatrix} \dfrac{{𝒖}_{\hat{{𝒕}}}^{{𝖳}}}{\hat{r}} & \dfrac{{𝒖}_{\hat{{𝒃}}}^{{𝖳}}}{\hat{v}} \end{bmatrix} \qquad\qquad(3.39)
> ```

---

[← Chapter 2. Batch-Sequential Filters](02-batch-sequential-filters.md) · [Contents](README.md) · [Chapter 3. The Covariance Matrix (part 2 of 3) →](03-the-covariance-matrix-part2.md)
