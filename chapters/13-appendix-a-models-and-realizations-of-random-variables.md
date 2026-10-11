[← Chapter 12. Advanced Estimation Algorithms](12-advanced-estimation-algorithms.md) · [Contents](README.md) · [Appendix B. The Mathematics Behind the UDU Factorization (part 1 of 3) →](14-appendix-b-the-mathematics-behind-the-udu-factorization-part1.md)

# <span id="page-146-0"></span>Appendix A. Models and Realizations of Random Variables

*Contributed by J. Russell Carpenter*

A continuous random variable is a function that maps the outcomes of random events to the real line. Realizations of random variables are thus real numbers. A vector of $`n`$ random variables maps outcomes of random events to $`{ℝ}^n`$. For our purposes, random variables will always be associated with a probability density function that indicates the likelihood that a realization occurs within a particular interval of the real line, or within a particular subspace of $`{ℝ}^n`$ for the vector case. It is common to assume that this density is the normal or Gaussian density. For the vector case, the normal probability density function is

```math
\mathrm{p}_{{𝘅}}({𝒙}) = \frac{1}{\sqrt{\vert 2\pi{𝐏} \vert}}\, \mathrm{e}^{-\frac{1}{2}({𝒙}-{𝝁})^{{𝖳}}{𝐏}^{-1}({𝒙}-{𝝁})} \qquad\qquad(A.1)
```

where $`{𝝁}`$ is a vector of mean values for each component of $`{𝘅}`$, and $`{𝐏}`$ is a matrix that contains the variances of each component of $`{𝘅}`$ along its diagonal, and the covariances between each component as its off-diagonal components. The covariances indicate the degree of correlation between the random variables composing $`{𝘅}`$. The matrix $`{𝐏}`$ is thus called the variance-covariance matrix, which we will hereafter abbreviate to just "covariance matrix," or "covariance." Since the normal density is completely characterized by its mean and covariance, we will use the following notation as a shorthand to describe drawing a realization from a normally-distributed random vector:

```math
{𝒙} \sim N({𝝁}, {𝐏}) \qquad\qquad(A.2)
```

Thus, the model for realizations of a measurement noise vector is

```math
{𝒗} \sim N({𝟎}, {𝐑}) \qquad\qquad(A.3)
```

For the scalar case, or for the vector case when the covariance is diagonal, we may directly generate realizations of a normally-distributed random vector from normal random number generators available in most software libraries. If $`{𝐏}`$ has non-zero off-diagonal elements, we must model the specified correlations when we generate realizations. If $`{𝐏}`$ is strictly positive definite, we can factor it as follows:

```math
{𝐏} = {}^{C}\!\sqrt{{𝐏}}\, {}^{C}\!\sqrt{{𝐏}}^{{𝖳}} \qquad\qquad(A.4)
```

where $`{}^{C}\!\sqrt{{𝐏}}`$ is a triangular matrix known as a Cholesky factor; this can be viewed as a "matrix square root." The Cholesky factorization is available in many linear algebra libraries. We can then use $`{}^{C}\!\sqrt{{𝐏}}`$ to generate correlated realizations of $`{𝘅}`$ as follows. Let $`{𝒛}`$ be a realization of a normally-distributed random vector of the same dimension as $`{𝘅}`$, with zero mean and unit variance, that is

```math
{𝒛} \sim N({𝟎}, {𝐈}) \qquad\qquad(A.5)
```

Then, with

```math
{𝒙} = {}^{C}\!\sqrt{{𝐏}}\, {𝒛} \qquad\qquad(A.6)
```

we can generate properly correlated realizations of $`{𝘅}`$. We can also use a Cholesky factorization of the measurement noise covariance $`{𝐑}`$, if $`{𝐑}`$ is non-diagonal, to transform correlated measurements into uncorrelated auxiliary measurements for cases in which the estimator cannot handle correlated measurement data.

If $`{𝐏}`$ is only non-negative definite, i.e. $`{𝐏} \geq 0`$ rather than $`{𝐏} \gt 0`$ as above, the Cholesky factorization does not exist. In this case, since $`{𝐏}`$'s eigenvalues are real and distinct, it has a diagonal factorization:

```math
{𝐏} = {𝐕}{𝐃}{𝐕}^{{𝖳}} \qquad\qquad(A.7)
```

where $`{𝐕}`$ is a matrix of eigenvectors and $`{𝐃}`$ is a diagonal matrix of eigenvalues. Then, with $`{𝒛}`$ as above,

```math
{𝒙} = {𝐕}\sqrt{{𝐃}}\, {𝒛} \qquad\qquad(A.8)
```

where $`\sqrt{{𝐃}}`$ implies taking the square roots of each diagonal element.

---

[← Chapter 12. Advanced Estimation Algorithms](12-advanced-estimation-algorithms.md) · [Contents](README.md) · [Appendix B. The Mathematics Behind the UDU Factorization (part 1 of 3) →](14-appendix-b-the-mathematics-behind-the-udu-factorization-part1.md)
