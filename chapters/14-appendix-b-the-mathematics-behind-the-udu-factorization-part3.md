[← Appendix B. The Mathematics Behind the UDU Factorization (part 2 of 3)](14-appendix-b-the-mathematics-behind-the-udu-factorization-part2.md) · [Contents](README.md) · [Appendix C. An Analysis of Dual Inertial-Absolute and Inertial-Relative Navigation Filters →](15-appendix-c-an-analysis-of-dual-inertial-absolute-and-inertial-relative.md)

*Appendix B. The Mathematics Behind the UDU Factorization, continued*

## B.5. The Carlson Rank-One Update

<span id="page-153-1"></span>The Carlson rank-one update [[9](16-bibliography.md#page-170-21)], introduced in 1973, addresses the problem of updating the covariance due to a loss of precision involved in the differencing of two positive quantities which are nearly equal. In particular, the diagonal elements $`d_{ii}`$ have the potential of going negative in certain cases if the Agee-Turner rank-one update is blindly used. Thankfully, we resort to the *Carlson rank-one update* to compute the measurement update without losing numerical precision.

We recall that $`\alpha`$ and $`{𝐯}`$ were defined earlier. We also define the $`n \times 1`$ vector $`{𝐟}`$ as

```math
{𝐟} \triangleq {𝐔}^{-{𝖳}}{𝐇}^{{𝖳}} \qquad\qquad(B.59)
```

Therefore, since $`{𝐟}`$ is an $`n \times 1`$ vector and $`{𝐃}`$ is a diagonal matrix, we can express $`\alpha`$ as

```math
\alpha = \alpha_n = R + \sum_{i=1}^{n}f_i^2d_{ii} \qquad\qquad(B.60)
```

so that

```math
\alpha_j = R + \sum_{i=1}^{j}f_i^2d_{ii} = \alpha_{j-1} + f_j^2d_{jj} \qquad\qquad(B.61)
```

Since $`{𝐯}`$ can be written as

```math
{𝐯} = {𝐃}{𝐟} \qquad\qquad(B.62)
```

we can also write

```math
v_j = d_{jj}f_j \qquad\qquad(B.63)
```

and we can write $`\alpha_j`$ as

<span id="page-154-3"></span>
```math
\alpha_j = \alpha_{j-1} + \frac{v_j^2}{d_{jj}} \qquad\qquad(B.64)
```

```math
\tilde{{𝐔}}_k\tilde{{𝐃}}_k\tilde{{𝐔}}_k^{{𝖳}} \triangleq {𝐚}r{𝐃} - \frac{1}{\alpha}{𝐯}{𝐯}^{{𝖳}} \qquad\qquad(B.65)
```

which can be rewritten as:

```math
\tilde{{𝐔}}_k\tilde{{𝐃}}_k\tilde{{𝐔}}_k^{{𝖳}} \triangleq {𝐚}r{𝐔}{𝐚}r{𝐃}{𝐚}r{𝐔}^{{𝖳}} - \frac{1}{\alpha}{𝐯}{𝐯}^{{𝖳}} \qquad\qquad(B.66)
```

where $`{𝐚}r{𝐔} = {𝐈}`$. Following the reasoning in the description for the Rank-One update earlier in this Appendix,

<span id="page-154-0"></span>
```math
\tilde{p}_{ij} \triangleq \sum_{k=j}^{n}\tilde{u}_{ik}\tilde{d}_{kk}\tilde{u}_{jk} = -\frac{1}{\alpha}v_iv_j \qquad\qquad(B.67)
```

and

<span id="page-154-1"></span>
```math
\tilde{p}_{ii} = \sum_{k=i}^{n}\tilde{u}_{ik}^2\tilde{d}_{kk} = d_{ii} - \frac{1}{\alpha}v_i^2 \qquad\qquad(B.68)
```

For $`j = n`$, Eq. [\(B.67\)](#page-154-0) becomes

```math
\tilde{u}_{in}\tilde{d}_{nn}\tilde{u}_{nn} = -\frac{1}{\alpha}v_iv_n \qquad\qquad(B.69)
```

and from Eq. [\(B.68\)](#page-154-1),

```math
\tilde{u}_{nn}^2\tilde{d}_{nn} = d_{nn} - \frac{1}{\alpha}v_n^2 \qquad\qquad(B.70)
```

Recalling that $`\tilde{u}_{nn} = 1`$, we get

```math
\tilde{d}_{nn} = d_{nn} - \frac{1}{\alpha}v_n^2 \qquad\qquad(B.71)
```

and

<span id="page-154-2"></span>
```math
\tilde{u}_{in} = -\frac{1}{\alpha\tilde{d}_{nn}}v_iv_n \qquad\qquad(B.72)
```

So, Eq. [\(B.67\)](#page-154-0) can be written as

<span id="page-155-5"></span>
```math
\sum_{k=j}^{n-1}\tilde{u}_{ik}\tilde{d}_{kk}\tilde{u}_{jk} + \tilde{u}_{in}\tilde{d}_{nn}\tilde{u}_{jn} = -\frac{1}{\alpha}v_iv_j \qquad\qquad(B.73)
```

Substituting for $`\tilde{u}_{in}`$ and $`\tilde{u}_{in}`$ from Eq. [\(B.72\)](#page-154-2), we find

<span id="page-155-0"></span>
```math
\sum_{k=j}^{n-1}\tilde{u}_{ik}\tilde{d}_{kk}\tilde{u}_{jk} = -\frac{1}{\alpha}\biggl[1 + \frac{1}{\alpha\tilde{d}_{nn}}v_n^2\biggr]v_iv_j \qquad\qquad(B.74)
```

But since

```math
\biggl[1 + \frac{1}{\alpha\tilde{d}_{nn}}v_n^2\biggr] = \frac{d_{nn}}{\tilde{d}_{nn}} \qquad\qquad(B.75)
```

Eq. [\(B.74\)](#page-155-0) becomes

<span id="page-155-1"></span>
```math
\sum_{k=j}^{n-1}\tilde{u}_{ik}\tilde{d}_{kk}\tilde{u}_{jk} = -\frac{1}{\alpha}\frac{d_{nn}}{\tilde{d}_{nn}}v_iv_j \qquad\qquad(B.76)
```

So, we can expand Eq. [\(B.76\)](#page-155-1) as

<span id="page-155-4"></span>
```math
\sum_{k=j}^{n-2}\tilde{u}_{ik}\tilde{d}_{kk}\tilde{u}_{jk} + \tilde{u}_{i,n-1}\tilde{d}_{n-1,n-1}\tilde{u}_{j,n-1} = -\frac{1}{\alpha}\frac{d_{nn}}{\tilde{d}_{nn}}v_iv_j \qquad\qquad(B.77)
```

We need to obtain $`\tilde{u}_{i,n-1}`$ and $`\tilde{d}_{n-1,n-1}`$. First we work on $`\tilde{u}_{i,n-1}\tilde{d}_{n-1,n-1}`$ from Eq. [\(B.67\)](#page-154-0) with $`i = n-1`$ as follows:

```math
\tilde{u}_{n-1,n-1}^2\tilde{d}_{n-1,n-1} + \tilde{u}_{n-1,n}^2\tilde{d}_{n,n} = d_{n-1} - \frac{1}{\alpha}v_{n-1}^2 \qquad\qquad(B.78)
```

Recalling that $`\tilde{u}_{n-1,n-1} = 1`$ and $`\tilde{u}_{n-1,n}`$ was obtained (with $`i = n-1`$) in Eq. [\(B.72\)](#page-154-2), we get

```math
\tilde{d}_{n-1,n-1} = d_{n-1,n-1} - \frac{1}{\alpha}\biggl[1 + \frac{1}{\alpha\tilde{d}_{n,n}}v_n^2\biggr]v_{n-1}^2 \qquad\qquad(B.79)
```

Knowing that

<span id="page-155-3"></span>
```math
\biggl[1 + \frac{1}{\alpha\tilde{d}_{n,n}}v_n^2\biggr] = \frac{d_{n,n}}{\tilde{d}_{n,n}} \qquad\qquad(B.80)
```

$`\tilde{d}_{n-1,n-1}`$ becomes

<span id="page-155-2"></span>
```math
\tilde{d}_{n-1,n-1} = d_{n-1,n-1} - \frac{1}{\alpha}\left(\frac{d_{n,n}}{\tilde{d}_{n,n}}\right)v_{n-1}^2 \qquad\qquad(B.81)
```

Now we work on $`\tilde{u}_{i,n-1}`$. We recall that from Eq. [\(B.68\)](#page-154-1), with $`j = n-1`$, we find that

```math
\tilde{u}_{i,n-1}\tilde{d}_{n-1,n-1}\tilde{u}_{n-1,n-1} + \tilde{u}_{i,n}\tilde{d}_{n,n}\tilde{u}_{n-1,n} = -\frac{1}{\alpha}v_iv_{n-1} \qquad\qquad(B.82)
```

We substitute for $`\tilde{d}_{n-1,n-1}`$ from Eq. [\(B.81\)](#page-155-2), for $`\tilde{u}_{i,n}`$ and $`\tilde{u}_{n-1,n}`$ from Eq. [\(B.72\)](#page-154-2) and noting that $`\tilde{u}_{n-1,n-1} = 1`$, we get

```math
\tilde{u}_{i,n-1} = -\frac{1}{\alpha\tilde{d}_{n-1,n-1}}\biggl[1 + \frac{1}{\alpha\tilde{d}_{n,n}}v_n^2\biggr]v_iv_{n-1} \qquad\qquad(B.83)
```

Using Eq. [\(B.80\)](#page-155-3), $`\tilde{u}_{i,n-1}`$ becomes

```math
\tilde{u}_{i,n-1} = -\frac{1}{\alpha\tilde{d}_{n-1,n-1}}\left(\frac{d_{n,n}}{\tilde{d}_{n,n}}\right)v_iv_{n-1} \qquad\qquad(B.84)
```

With this in mind, we are now prepared to work on Eq. [\(B.77\)](#page-155-4), and we find that

```math
\begin{aligned} \sum_{k=j}^{n-2}\tilde{u}_{ik}\tilde{d}_{kk}\tilde{u}_{jk} &= -\left(\frac{d_{n,n}}{\alpha\tilde{d}_{n,n}}\right)\biggl[\frac{d_{n,n}}{\alpha\tilde{d}_{n,n}}v_{n-1}^2 - 1\biggr]v_iv_j \\ &= -\left(\frac{d_{n,n}}{\alpha\tilde{d}_{n,n}}\right)\left(\frac{d_{n-1,n-1}}{\tilde{d}_{n-1,n-1}}\right)v_iv_j \end{aligned} \qquad\qquad(B.85)
```

This has the same form as Eq. [\(B.73\)](#page-155-5), so this suggests a recursion as follows:

With $`{𝒞}_n = -1/\alpha`$ for $`j = n, \cdots, 1`$:

<span id="page-156-0"></span>
```math
\tilde{d}_{jj} = d_{jj} + {𝒞}^jv_j^2 \qquad\qquad(B.86)
```

```math
\tilde{u}_{ij} = {𝒞}^jv_iv_j/\tilde{d}_{jj}, \quad k = 1, \cdots, j-1 \qquad\qquad(B.87)
```

```math
C^{j-1} = C^jd_{jj}/\tilde{d}_{jj} \qquad\qquad(B.88)
```

From Eq. [\(B.86\)](#page-156-0), we get

```math
\tilde{d}_{jj} = d_{jj} + {𝒞}^jv_j^2
```

and from Eq. [\(B.88\)](#page-156-0), we find that

```math
{𝒞}^{j-1} = {𝒞}^j\frac{d_{jj}}{\tilde{d}_{jj}} = \frac{{𝒞}^jd_{jj}}{d_{jj} + C^jv_j^2} = \frac{d_{jj}}{\frac{d_{jj}}{{𝒞}^j} + v_j^2} \qquad\qquad(B.89)
```

This can be written as

```math
\frac{1}{{𝒞}^{j-1}} = \frac{1}{{𝒞}^j} + \frac{v_j^2}{d_{jj}} \qquad\qquad(B.90)
```

or

<span id="page-156-1"></span>
```math
-\frac{1}{{𝒞}^j} = -\frac{1}{{𝒞}^{j-1}} + \frac{v_j^2}{d_{jj}} \qquad\qquad(B.91)
```

Comparing Eqs. [\(B.64\)](#page-154-3) and Eq. [\(B.91\)](#page-156-1) we find that

<span id="page-156-3"></span>
```math
\alpha_j = -\frac{1}{{𝒞}^j} \qquad\qquad(B.92)
```

Using this equation, we find that

<span id="page-156-2"></span>
```math
\tilde{d}_{jj} = d_{jj}\left(\frac{\alpha_{j-1}}{\alpha_j}\right) \qquad\qquad(B.93)
```

From Eq. [\(B.87\)](#page-156-0) and using Eqs. [\(B.93\)](#page-156-2) and [\(B.92\)](#page-156-3), we can express $`\tilde{u}_{ij}`$ as

```math
\tilde{u}_{ij} = -\frac{v_iv_j}{d_{jj}\alpha_{j-1}} \qquad\qquad(B.94)
```

Recalling that $`v_j = d_{jj}f_j`$,

```math
\tilde{u}_{ij} = -\frac{v_if_j}{\alpha_{j-1}} \qquad\qquad(B.95)
```

If we define $`\lambda_j`$ as

```math
\lambda_j \triangleq -\frac{f_j}{\alpha_{j-1}} \qquad\qquad(B.96)
```

$`\tilde{u}_{ij}`$ becomes

```math
\tilde{u}_{ij} = \lambda_jv_i \qquad\qquad(B.97)
```

$`\tilde{U}_{ij}`$ has the structure

```math
\tilde{{𝐔}}_k = \begin{bmatrix} 1 & \lambda_2v_1 & \lambda_3v_1 & \lambda_4v_1 & \cdots & \lambda_nv_1 \\ 0 & 1 & \lambda_3v_2 & \lambda_4v_2 & \cdots & \lambda_nv_2 \\ 0 & 0 & 1 & \lambda_4v_3 & \cdots & \lambda_nv_3 \\ 0 & 0 & 0 & 1 & \cdots & \lambda_nv_4 \\ \vdots & \vdots & \vdots & \vdots & \vdots & \vdots \\ 0 & 0 & 0 & 0 & \cdots & 1 \end{bmatrix} \qquad\qquad(B.98)
```

We can rewrite $`\tilde{{𝐔}}`$ as

```math
\tilde{{𝐔}}_k = {𝐈}_n + \begin{bmatrix} {𝟎}_{n\times 1} & \lambda_2{𝐯}^{(1)} & \lambda_3{𝐯}^{(2)} & \lambda_4{𝐯}^{(3)} & \cdots & \lambda_n{𝐯}^{(n-1)} \end{bmatrix} \qquad\qquad(B.99)
```

where $`{𝐯}^{(j)}`$ is an $`n \times 1`$ vector defined as

```math
{𝐯}^{(j)} \triangleq \begin{bmatrix} v_1 & v_2 & v_3 & \cdots & v_j & 0 & \cdots & 0 \end{bmatrix}^{{𝖳}} \qquad\qquad(B.100)
```

We recall that

```math
{𝐔}{𝐃}{𝐔}^{{𝖳}} = {𝐔}^{-}\left[{𝐃}^{-} - \frac{1}{\alpha}{𝐯}{𝐯}^{{𝖳}}\right]{𝐚}r{𝐔}^{{𝖳}}
```

and

```math
\tilde{{𝐔}}_k\tilde{{𝐃}}_k\tilde{{𝐔}}_k^{{𝖳}} \triangleq {𝐃}^{-} - \frac{1}{\alpha}{𝐯}{𝐯}^{{𝖳}}
```

and

```math
{𝐔} = {𝐔}^{-}\tilde{{𝐔}}_k \qquad \text{and} \qquad {𝐃} = \tilde{{𝐃}}
```

With this in mind, $`{𝐔}`$ is

```math
{𝐔} = {𝐔}^{-} + {𝐔}^{-}\begin{bmatrix} {𝟎}_{n\times 1} & \lambda_2{𝐯}^{(1)} & \lambda_3{𝐯}^{(3)} & \lambda_4{𝐯}^{(3)} & \cdots & \lambda_n{𝐯}^{(n-1)} \end{bmatrix} \qquad\qquad(B.101)
```

If we denote $`{𝐔}^{(j)}`$ and $`{𝐔}^{-j}`$ as the $`j`$th columns of $`{𝐔}`$ and $`{𝐔}^{-}`$, respectively, we find that

```math
{𝐔}^{(j)} = {𝐔}^{-j} + \lambda_j\overline{{𝐊}}_{j-1} \qquad\qquad(B.102)
```

where

```math
\overline{{𝐊}}_j = {𝐔}^{-}{𝐯}^{(j)} = \overline{{𝐊}}_{j-1} + v_j{𝐔}^{-j} \quad \text{with} \quad \overline{{𝐊}}_0 = {𝟎}_{n\times 1} \qquad\qquad(B.103)
```

Finally,

```math
{𝐊} = \frac{1}{\alpha_n}\overline{{𝐊}}_n \qquad\qquad(B.104)
```

---

[← Appendix B. The Mathematics Behind the UDU Factorization (part 2 of 3)](14-appendix-b-the-mathematics-behind-the-udu-factorization-part2.md) · [Contents](README.md) · [Appendix C. An Analysis of Dual Inertial-Absolute and Inertial-Relative Navigation Filters →](15-appendix-c-an-analysis-of-dual-inertial-absolute-and-inertial-relative.md)
