[← Chapter 12. Advanced Estimation Algorithms](12-advanced-estimation-algorithms.md) · [Contents](README.md) · [Appendix B. The Mathematics Behind the UDU Factorization →](14-appendix-b-the-mathematics-behind-the-udu-factorization.md)

# <span id="page-146-0"></span>Appendix A. Models and Realizations of Random Variables

*Contributed by J. Russell Carpenter*

A continuous random variable is a function that maps the outcomes of random events to the real line. Realizations of random variables are thus real numbers. A vector of $n$ random variables maps outcomes of random events to $\mathbb{R}^n$. For our purposes, random variables will always be associated with a probability density function that indicates the likelihood that a realization occurs within a particular interval of the real line, or within a particular subspace of $\mathbb{R}^n$ for the vector case. It is common to assume that this density is the normal or Gaussian density. For the vector case, the normal probability density function is

$$
\mathrm{p}_{\boldsymbol{\mathsf{x}}}(\boldsymbol{x}) = \frac{1}{\sqrt{\vert 2\pi\mathbf{P} \vert}}\, \mathrm{e}^{-\frac{1}{2}(\boldsymbol{x}-\boldsymbol{\mu})^{\mathsf{T}}\mathbf{P}^{-1}(\boldsymbol{x}-\boldsymbol{\mu})} \tag{A.1}
$$

where $\boldsymbol{\mu}$ is a vector of mean values for each component of $\boldsymbol{\mathsf{x}}$, and $\mathbf{P}$ is a matrix that contains the variances of each component of $\boldsymbol{\mathsf{x}}$ along its diagonal, and the covariances between each component as its off-diagonal components. The covariances indicate the degree of correlation between the random variables composing $\boldsymbol{\mathsf{x}}$. The matrix $\mathbf{P}$ is thus called the variance-covariance matrix, which we will hereafter abbreviate to just "covariance matrix," or "covariance." Since the normal density is completely characterized by its mean and covariance, we will use the following notation as a shorthand to describe drawing a realization from a normally-distributed random vector:

$$
\boldsymbol{x} \sim N(\boldsymbol{\mu}, \mathbf{P}) \tag{A.2}
$$

Thus, the model for realizations of a measurement noise vector is

$$
\boldsymbol{v} \sim N(\mathbf{0}, \mathbf{R}) \tag{A.3}
$$

For the scalar case, or for the vector case when the covariance is diagonal, we may directly generate realizations of a normally-distributed random vector from normal random number generators available in most software libraries. If $\mathbf{P}$ has non-zero off-diagonal elements, we must model the specified correlations when we generate realizations. If $\mathbf{P}$ is strictly positive definite, we can factor it as follows:

$$
\mathbf{P} = {}^{C}\!\sqrt{\mathbf{P}}\, {}^{C}\!\sqrt{\mathbf{P}}^{\mathsf{T}} \tag{A.4}
$$

where ${}^{C}\!\sqrt{\mathbf{P}}$ is a triangular matrix known as a Cholesky factor; this can be viewed as a "matrix square root." The Cholesky factorization is available in many linear algebra libraries. We can then use ${}^{C}\!\sqrt{\mathbf{P}}$ to generate correlated realizations of $\boldsymbol{\mathsf{x}}$ as follows. Let $\boldsymbol{z}$ be a realization of a normally-distributed random vector of the same dimension as $\boldsymbol{\mathsf{x}}$, with zero mean and unit variance, that is

$$
\boldsymbol{z} \sim N(\mathbf{0}, \mathbf{I}) \tag{A.5}
$$

Then, with

$$
\boldsymbol{x} = {}^{C}\!\sqrt{\mathbf{P}}\, \boldsymbol{z} \tag{A.6}
$$

we can generate properly correlated realizations of $\boldsymbol{\mathsf{x}}$. We can also use a Cholesky factorization of the measurement noise covariance $\mathbf{R}$, if $\mathbf{R}$ is non-diagonal, to transform correlated measurements into uncorrelated auxiliary measurements for cases in which the estimator cannot handle correlated measurement data.

If $\mathbf{P}$ is only non-negative definite, i.e. $\mathbf{P} \geq 0$ rather than $\mathbf{P} > 0$ as above, the Cholesky factorization does not exist. In this case, since $\mathbf{P}$'s eigenvalues are real and distinct, it has a diagonal factorization:

$$
\mathbf{P} = \mathbf{V}\mathbf{D}\mathbf{V}^{\mathsf{T}} \tag{A.7}
$$

where $\mathbf{V}$ is a matrix of eigenvectors and $\mathbf{D}$ is a diagonal matrix of eigenvalues. Then, with $\boldsymbol{z}$ as above,

$$
\boldsymbol{x} = \mathbf{V}\sqrt{\mathbf{D}}\, \boldsymbol{z} \tag{A.8}
$$

where $\sqrt{\mathbf{D}}$ implies taking the square roots of each diagonal element.

---

[← Chapter 12. Advanced Estimation Algorithms](12-advanced-estimation-algorithms.md) · [Contents](README.md) · [Appendix B. The Mathematics Behind the UDU Factorization →](14-appendix-b-the-mathematics-behind-the-udu-factorization.md)
