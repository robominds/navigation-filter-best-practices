[← Appendix B. The Mathematics Behind the UDU Factorization (part 1 of 3)](14-appendix-b-the-mathematics-behind-the-udu-factorization-part1.md) · [Contents](README.md) · [Appendix B. The Mathematics Behind the UDU Factorization (part 3 of 3) →](14-appendix-b-the-mathematics-behind-the-udu-factorization-part3.md)

*Appendix B. The Mathematics Behind the UDU Factorization, continued*

## B.3. The Agee-Turner Rank-One Update

<span id="page-150-0"></span>In trying to get an efficient algorithm for performing the time update of the covariance matrix, we were faced with Eq. [\(8.41\)](08-factorization-methods-part2.md#page-101-1), which is of the form

```math
\tilde{{𝐔}}\tilde{{𝐃}}\tilde{{𝐔}}^{{𝖳}} = {𝐔}{𝐃}{𝐔}^{{𝖳}} + c\,{𝐱}{𝐱}^{{𝖳}} \qquad\qquad(B.19)
```

This is called a 'rank one' update because we are updating the matrix factors $`{𝐔}`$ and $`{𝐃}`$ based upon products of $`{𝐱}`$ which is of rank 1.

In order to reduce the number of mathematical operations (adds/subtracts, multiplies and divides), for the case of parameter or ECRV/First-order Gauss Markov processes, for sensor parameters, we consider the rank-one update first introduced by Agee and Turner (of the White Sands Missile Range (WSMR)) in 1972.

Consider a covariance matrix update of the form,

```math
\tilde{{𝐏}} = {𝐏} + c\,{𝐱}{𝐱}^{{𝖳}} \qquad\qquad(B.20)
```

or

```math
\tilde{{𝐔}}\tilde{{𝐃}}\tilde{{𝐔}}^{{𝖳}} = {𝐔}{𝐃}{𝐔}^{{𝖳}} + c\,{𝐱}{𝐱}^{{𝖳}} \qquad\qquad(B.21)
```

so, $`\tilde{p}_{ij}`$ can be expressed (and defined) as

<span id="page-150-3"></span>
```math
\tilde{p}_{ij} \triangleq \sum_{k=j}^{n}\tilde{u}_{ik}\tilde{d}_{kk}\tilde{u}_{jk} = \sum_{k=j}^{n}u_{ik}d_{kk}u_{jk} + cx_ix_j \qquad\qquad(B.22)
```

and

```math
\tilde{p}_{ii} = \sum_{k=i}^{n}\tilde{u}_{ik}^2\tilde{d}_{kk} = \sum_{k=i}^{n}u_{ik}^2d_{kk} + cx_i^2 \qquad\qquad(B.23)
```

We recall that $`\tilde{u}_{ii} = u_{ii} = 1`$ and thus, for an $`n \times n`$ matrix, for $`j = n`$ (i.e. the last column),

```math
\tilde{d}_{nn} = d_{nn} + c\,x_n^2 \qquad\qquad(B.24)
```

```math
\tilde{p}_{in} = \tilde{u}_{in}\tilde{d}_{nn}\tilde{u}_{nn} = d_{nn}u_{in}u_{nn} + cx_ix_n \qquad\qquad(B.25)
```

so that

<span id="page-151-0"></span>
```math
\tilde{u}_{in} = \frac{1}{\tilde{d}_{nn}}\left(d_{nn}u_{in} + cx_ix_n\right) \qquad\qquad(B.26)
```

The second-to-the-last ($`n-1`$-th) column of $`{𝐔}`$ can now be can be operated on, by means of the following decomposition of Eq. [\(B.22\)](#page-150-3), as

<span id="page-151-1"></span>
```math
\sum_{k=j}^{n-1}\tilde{u}_{ik}\tilde{d}_{kk}\tilde{u}_{jk} + \tilde{u}_{in}\tilde{d}_{nn}\tilde{u}_{jn} = \sum_{k=j}^{n-1}u_{ik}d_{kk}u_{jk} + u_{in}d_{nn}u_{jn} + cx_ix_j \qquad\qquad(B.27)
```

which leads to

```math
\sum_{k=j}^{n-1}\tilde{u}_{ik}\tilde{d}_{kk}\tilde{u}_{jk} = \sum_{k=j}^{n-1}u_{ik}d_{kk}u_{jk} + \Upsilon_n \qquad\qquad(B.28)
```

If we work on the terms outside the two summations, using Eq. [\(B.26\)](#page-151-0) for $`\tilde{u}_{in}`$ and $`\tilde{u}_{jn}`$, $`\Upsilon_n`$ becomes

```math
\begin{aligned} \Upsilon_n &= -\tilde{u}_{in}\tilde{d}_{nn}\tilde{u}_{jn} + u_{in}d_{nn}u_{jn} + cx_ix_j \\ &= -\frac{1}{\tilde{d}_{nn}}\left[d_{nn}u_{in} + cx_ix_n\right]\left[d_{nn}u_{jn} + cx_jx_n\right] \\ &\quad + \frac{d_{nn} + c\,x_n^2}{\tilde{d}_{nn}}\left(u_{in}d_{nn}u_{jn} + cx_ix_j\right) \\ &= \frac{1}{\tilde{d}_{nn}}\big[-c\,d_{nn}u_{jn}x_nx_i - c\,d_{nn}u_{in}x_nx_j + c\,d_{nn}x_ix_j + c\,d_{nn}x_n^2u_{in}u_{jn}\big) \\ &= \frac{c\,d_{nn}}{\tilde{d}_{nn}}\left(x_i - u_{in}x_n\right)\left(x_j - u_{jn}x_n\right) \end{aligned} \qquad\qquad(B.29)
```

Therefore, Eq. [\(B.27\)](#page-151-1) can be written as

<span id="page-151-2"></span>
```math
\sum_{k=j}^{n-1}\tilde{u}_{ik}\tilde{d}_{kk}\tilde{u}_{jk} = \sum_{k=j}^{n-1}u_{ik}d_{kk}u_{jk} + \frac{c\,d_{nn}}{\tilde{d}_{nn}}\left(x_i - u_{in}x_n\right)\left(x_j - u_{jn}x_n\right) \qquad\qquad(B.30)
```

Now, if we operate a bit more on the quantity $`\tilde{u}_{in}`$, we find from Eq. [\(B.26\)](#page-151-0), that we get

```math
\tilde{u}_{in} = \frac{d_{nn}}{\tilde{d}_{nn}}u_{in} + \frac{c}{\tilde{d}_{nn}}x_ix_n \qquad\qquad(B.31)
```

```math
= \frac{\tilde{d}_{nn} - c\,x_n^2}{\tilde{d}_{nn}}u_{in} + \frac{c}{\tilde{d}_{nn}}x_ix_n \qquad\qquad(B.32)
```

```math
= u_{in} + \left(x_i - u_{in}x_n\right)\frac{c\,x_n}{\tilde{d}_{nn}} \qquad\qquad(B.33)
```

and if we define $`\alpha_i`$ and $`v_n`$ as

```math
\alpha_i \triangleq \left(x_i - u_{in}x_n\right) \qquad\qquad(B.34)
```

```math
v_n \triangleq \frac{c\,x_n}{\tilde{d}_{nn}} \qquad\qquad(B.35)
```

$`\tilde{u}_{in}`$ can be rewritten as

```math
\tilde{u}_{in} = u_{in} + \alpha_i\,v_n \qquad\qquad(B.36)
```

If we want to generalize this, we can write Eq. [\(B.30\)](#page-151-2) as

<span id="page-152-0"></span>
```math
\sum_{k=j}^{n-1}\tilde{u}_{ik}\tilde{d}_{kk}\tilde{u}_{jk} = \sum_{k=j}^{n-1}u_{ik}d_{kk}u_{jk} + {𝒞}^n{𝒳}_i^n{𝒳}_j^n \qquad\qquad(B.37)
```

where

```math
{𝒞}^n \triangleq \frac{c\,d_{nn}}{\tilde{d}_{nn}} \qquad\qquad(B.38)
```

```math
{𝒳}_i^n \triangleq x_i - u_{in}x_n \qquad\qquad(B.39)
```

with

```math
\begin{aligned} \tilde{u}_{in} &= u_{in} + \alpha_i^n\,v_n \\ \alpha_i^n &= x_i - u_{in}x_n \\ v_n &= \frac{c\,x_n}{\tilde{d}_{nn}} \\ \tilde{d}_{nn} &= d_{nn} + c\,x_n^2 \end{aligned}
```

Thus, for the third-to-the-last column ($`j = n-2`$), we expand Eq. [\(B.37\)](#page-152-0) as

```math
\begin{aligned} \sum_{k=j}^{n-2}\tilde{u}_{ik}\tilde{d}_{kk}\tilde{u}_{jk} + \tilde{u}_{i,n-1}\tilde{d}_{n-1,n-1}\tilde{u}_{j,n-1} &= \sum_{k=j}^{n-2}u_{ik}d_{kk}u_{jk} \\ &\quad + u_{i,n-1}d_{n-1,n-1}u_{j,n-1} \\ &\quad + {𝒞}^n{𝒳}_i^n{𝒳}_j^n \end{aligned} \qquad\qquad(B.40)
```

which produces

```math
\begin{aligned} \sum_{k=j}^{n-2}\tilde{u}_{ik}\tilde{d}_{kk}\tilde{u}_{jk} &= \sum_{k=j}^{n-2}u_{ik}d_{kk}u_{jk} \\ &\quad + \frac{{𝒞}^n d_{n-1,n-1}}{\tilde{d}_{n-1,n-1}}\Bigl[{𝒳}_i^n - u_{i,n-1}{𝒳}_n^n\Bigr]\Bigl[{𝒳}_j^n - u_{j,n-1}{𝒳}_n^n\Bigr] \end{aligned} \qquad\qquad(B.41)
```

so that using the same machinery as above, we get

```math
\sum_{k=j}^{n-2}\tilde{u}_{ik}\tilde{d}_{kk}\tilde{u}_{jk} = \sum_{k=j}^{n-2}u_{ik}d_{kk}u_{jk} + {𝒞}^{n-1}{𝒳}_i^{n-1}{𝒳}_j^{n-1} \qquad\qquad(B.42)
```

```math
{𝒞}^{n-1} = \frac{{𝒞}^n\,d_{n-1,n-1}}{\tilde{d}_{n-1,n-1}} \qquad\qquad(B.43)
```

```math
{𝒳}_i^{n-1} = \alpha_i^{n-1} = {𝒳}_i^n - u_{i,n-1}\,{𝒳}_n^n \qquad\qquad(B.44)
```

```math
v_{n-1} = \frac{{𝒞}^n\,{𝒳}_i^n}{\tilde{d}_{n-1,n-1}} \qquad\qquad(B.45)
```

```math
\tilde{u}_{i,n-1} = u_{i,n-1} + {𝒳}_i^{n-1}\,v_{n-1} \qquad\qquad(B.46)
```

```math
\tilde{d}_{n-1,n-1} = d_{n-1,n-1} + {𝒞}^n\,x_{n-1}^2 \qquad\qquad(B.47)
```

We also are reminded that $`\tilde{u}_{i,i} = 1`$.

## B.4. Decorrelating Measurements

<span id="page-153-0"></span>We normalize the (original) measurement equation

```math
{𝐳}_{orig} = {𝐇}_{orig}{𝐱} + {𝝂}_{orig} \qquad\qquad(B.48)
```

where the measurement noise has statistics

```math
E[{𝝂}_{orig}] = {𝟎} \qquad\qquad(B.49)
```

```math
E[{𝝂}_{orig}{𝝂}_{orig}^{{𝖳}}] = {𝐑}_{orig} \qquad\qquad(B.50)
```

where $`{𝐑}_{orig}`$ is the measurement noise.

We now change variables so that

```math
{𝐳} \triangleq {𝐑}_{orig}^{-1/2}{𝐳}_{orig} \qquad\qquad(B.51)
```

```math
{𝐇} \triangleq {𝐑}_{orig}^{-1/2}{𝐇}_{orig} \qquad\qquad(B.52)
```

```math
{𝝂} \triangleq {𝐑}_{orig}^{-1/2}{𝝂}_{orig} \qquad\qquad(B.53)
```

where $`{𝐑}_{orig}^{-1/2}`$ is the inverse of the Cholesky factor of $`{𝐑}_{orig}`$ ($`= {𝐑}_{orig}^{1/2}{𝐑}_{orig}^{T/2}`$). With this, the new normalized measurement equation is

```math
{𝐳} = {𝐇}{𝐱} + {𝝂} \qquad\qquad(B.54)
```

where $`E[{𝝂}] = {𝟎}`$ and $`E[{𝝂}{𝝂}^{{𝖳}}] = {𝐈}`$. This is sometimes referred to as **pre-whitening** or *decorrelation*, because if the original measurements were correlated, the normalized measurements are now uncorrelated (via the Cholesky decomposition of $`{𝐑}_{orig}`$).

Alternatively, we can decorrelate the measurements by using a UDU factorization on the measurement noise covariance matrix as

```math
{𝐑}_{orig} = {𝐔}_R{𝐃}_R{𝐔}_R^{{𝖳}} \qquad\qquad(B.55)
```

so that the measurement equation, the measurement partial and the measurement noise are

```math
{𝐳} \triangleq {𝐔}_R^{-1}{𝐳}_{orig} \qquad\qquad(B.56)
```

```math
{𝐇} \triangleq {𝐔}_R^{-1}{𝐇}_{orig} \qquad\qquad(B.57)
```

```math
{𝝂} \triangleq {𝐔}_R^{-1}{𝝂}_{orig} \qquad\qquad(B.58)
```

where the new/modified measurement equation is now uncorrelated with $`E[{𝝂}] = {𝟎}`$ and $`E[{𝝂}{𝝂}^{{𝖳}}] = {𝐃}_R`$.

---

[← Appendix B. The Mathematics Behind the UDU Factorization (part 1 of 3)](14-appendix-b-the-mathematics-behind-the-udu-factorization-part1.md) · [Contents](README.md) · [Appendix B. The Mathematics Behind the UDU Factorization (part 3 of 3) →](14-appendix-b-the-mathematics-behind-the-udu-factorization-part3.md)
