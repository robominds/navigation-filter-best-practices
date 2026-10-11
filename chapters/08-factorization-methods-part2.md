[← Chapter 8. Factorization Methods (part 1 of 3)](08-factorization-methods-part1.md) · [Contents](README.md) · [Chapter 8. Factorization Methods (part 3 of 3) →](08-factorization-methods-part3.md)

*Chapter 8. Factorization Methods, continued*

### 8.3.2. An Improvement for the Case of Parameters

As stated earlier, for a large number of states (say, $`n_{{𝐱}} = 35`$), the UDU time update for the full covariance matrix (à la Gram-Schmidt orthogonalization) is computationally expensive, requiring $`2n_{{𝐱}}^3 + 2n_{{𝐱}}^2`$ multiplies and additions. This is not competitive with the "standard" ($`{𝐏}_{k+1}^- = {𝚽}(t_k, t_{k+1}){𝐏}_k^+{𝚽}^{{𝖳}}(t_k, t_{k+1}) + {𝐆}_k{𝐐}_k{𝐆}_k^{{𝖳}}`$) formulation (which uses $`2n_{{𝐱}}^3`$ multiplies). However, one might guess that an improvement can be made. This is particularly significant because, normally, most of the states are biases or ECRVs (Exponentially Correlated Random Variables) or first-order Gauss-Markov processes. In order to generalize the development, we assume ECRVs for the 'parameter' (or bias) states.

For most space-borne navigation applications, we can usually partition the states into position, velocity, attitude (if applicable) and clock states, all of which we group together and denote as $`{𝐱}`$, and parameter states which usually comprise the sensor biases, scale factors, *etc.*, which we denote as $`{𝐩}`$. This means that the full state space is

```math
{𝒳} = \begin{bmatrix} {𝐱} \\ {𝐩} \end{bmatrix} \qquad\qquad(8.16)
```

The 'states' partition must comprise all those quantities whose time evolution cannot be described as purely self-auto correlated processes. With this in hand, we partition $`{𝐔}`$ and $`{𝐃}`$ as

```math
{𝐔} = \begin{bmatrix} {𝐔}_{{𝐱𝐱}} & {𝐔}_{{𝐱𝐩}} \\ {𝟎} & {𝐔}_{{𝐩𝐩}} \end{bmatrix} \qquad {𝐃} = \begin{bmatrix} {𝐃}_{{𝐱𝐱}} & {𝟎} \\ {𝟎} & {𝐃}_{{𝐩𝐩}} \end{bmatrix} \qquad\qquad(8.17)
```

Also, partition $`{𝚽}_k`$ according to

```math
{𝚽}(t_{k+1}, t_k) = {𝚽}_k = \begin{bmatrix} {𝚽}_{{𝐱𝐱}_k} & {𝚽}_{{𝐱𝐩}_k} \\ {𝟎} & {𝐌} \end{bmatrix} = \begin{bmatrix} {𝐈} & {𝟎} \\ {𝟎} & {𝐌} \end{bmatrix} \begin{bmatrix} {𝚽}_{{𝐱𝐱}_k} & {𝚽}_{{𝐱𝐩}_k} \\ {𝟎} & {𝐈} \end{bmatrix} = {𝚽}_{2_k}{𝚽}_{1_k} \qquad\qquad(8.18)
```

where $`{𝐌}`$ is a diagonal matrix, representing an ECRV whose propagation for $`p_k`$ is

```math
p_k^- = e^{-\Delta t/\tau} p_{k-1}^+ \qquad\qquad(8.19)
```

so that

```math
{𝐌}(i, i) = m_i = e^{-\Delta t/\tau_i} \qquad\qquad(8.20)
```

where $`\tau_i`$ is the time constant of the $`i^{\text{th}}`$ ECRV state.

Likewise $`{𝐐}_k`$ is partitioned according to

```math
\begin{aligned} {𝐐}_k &= \begin{bmatrix} {𝐆}_{{𝐱𝐱}_k}{𝐐}_{{𝐱𝐱}_k}{𝐆}_{{𝐱𝐱}_k}^{{𝖳}} & {𝟎} \\ {𝟎} & {𝐐}_{{𝐩𝐩}_k} \end{bmatrix} = \begin{bmatrix} {𝐆}_{{𝐱𝐱}_k}{𝐐}_{{𝐱𝐱}_k}{𝐆}_{{𝐱𝐱}_k}^{{𝖳}} & {𝟎} \\ {𝟎} & {𝟎} \end{bmatrix} + \begin{bmatrix} {𝟎} & {𝟎} \\ {𝟎} & {𝐐}_{{𝐩𝐩}_k} \end{bmatrix} \\ &= {𝐐}_{1_k} + {𝐐}_{2_k} \end{aligned} \qquad\qquad(8.21)
```

where we assume that the parameters are ECRVs and hence $`{𝐐}_{{𝐩𝐩}}`$ is a diagonal matrix.

Recall that the original propagation equation was

```math
{𝐔}_{k+1}^-{𝐃}_{k+1}^-{𝐔}_{k+1}^{-{𝖳}} = {𝚽}_k{𝐔}_k^+{𝐃}_k^+{𝐔}_k^{+{𝖳}}{𝚽}_k^{{𝖳}} + {𝐆}_k{𝐐}_k{𝐆}_k^{{𝖳}} \qquad\qquad(8.22)
```

Harnessing the development in Appendix [B.1,](14-appendix-b-the-mathematics-behind-the-udu-factorization-part1.md#page-148-1) $`{𝐔}_{k+1}^-{𝐃}_{k+1}^-{𝐔}_{k+1}^{-{𝖳}}`$ becomes

```math
{𝐔}_{k+1}^-{𝐃}_{k+1}^-{𝐔}_{k+1}^{-{𝖳}} = {𝚽}_{2_k}\Bigl[{𝚽}_{1_k}{𝐔}_k^+{𝐃}_k^+{𝐔}_k^{+{𝖳}}{𝚽}_{1_k}^{{𝖳}} + {𝐐}_{1_k}\Bigr]{𝚽}_{2_k}^{{𝖳}} + {𝐐}_{2_k} \qquad\qquad(8.23)
```

This suggests the following two-step process:

1) Find $`\tilde{{𝐔}}`$ and $`\tilde{{𝐃}}`$ from

<span id="page-100-0"></span>
```math
\tilde{{𝐔}}_k\tilde{{𝐃}}_k\tilde{{𝐔}}_k^{{𝖳}} = {𝚽}_{1_k}{𝐔}_k^+{𝐃}_k^+{𝐔}_k^{+{𝖳}}{𝚽}_{1_k}^{{𝖳}} + {𝐐}_{1_k} \qquad\qquad(8.24)
```

2) Find $`{𝐔}_{k+1}^-`$ and $`{𝐃}_{k+1}^-`$ from

<span id="page-100-5"></span>
```math
{𝐔}_{k+1}^-{𝐃}_{k+1}^-{𝐔}_{k+1}^{-{𝖳}} = {𝚽}_{2_k}\tilde{{𝐔}}_k\tilde{{𝐃}}_k\tilde{{𝐔}}_k^{{𝖳}}{𝚽}_{2_k}^{{𝖳}} + {𝐐}_{2_k} \qquad\qquad(8.25)
```

The following sub-sections will describe each of these steps.

#### 8.3.2.1. The First Sub-Problem ($`{𝚽}_{1_k}{𝐔}_k^+{𝐃}_k^+{𝐔}_k^{+{𝖳}}{𝚽}_{1_k}^{{𝖳}} + {𝐐}_{1_k}`$)

Lets look at 1). The left hand side of Eq. [\(8.24\)](#page-100-0) is

<span id="page-100-1"></span>
```math
\tilde{{𝐔}}_k\tilde{{𝐃}}_k\tilde{{𝐔}}_k^{{𝖳}} = \begin{bmatrix} \tilde{{𝐔}}_{{𝐱𝐱}_k}\tilde{{𝐃}}_{{𝐱𝐱}_k}\tilde{{𝐔}}_{{𝐱𝐱}_k}^{{𝖳}} + \tilde{{𝐔}}_{{𝐱𝐩}_k}\tilde{{𝐃}}_{{𝐩𝐩}_k}\tilde{{𝐔}}_{{𝐱𝐩}_k}^{{𝖳}} & \tilde{{𝐔}}_{{𝐱𝐩}_k}\tilde{{𝐃}}_{{𝐩𝐩}_k}\tilde{{𝐔}}_{{𝐩𝐩}_k}^{{𝖳}} \\ \tilde{{𝐔}}_{{𝐩𝐩}_k}\tilde{{𝐃}}_{{𝐩𝐩}_k}\tilde{{𝐔}}_{{𝐱𝐩}_k}^{{𝖳}} & \tilde{{𝐔}}_{{𝐩𝐩}_k}\tilde{{𝐃}}_{{𝐩𝐩}_k}\tilde{{𝐔}}_{{𝐩𝐩}_k}^{{𝖳}} \end{bmatrix} \qquad\qquad(8.26)
```

The right hand side of Eq. [\(8.24\)](#page-100-0) is

<span id="page-100-2"></span>
```math
\tilde{{𝐔}}_k\tilde{{𝐃}}_k\tilde{{𝐔}}_k^{{𝖳}} = \biggl[\begin{array}{c|c} {𝚽}_{{𝐱𝐱}_k}\Big({𝐔}_{{𝐱𝐱}_k}^+{𝐃}_{{𝐱𝐱}}^+{𝐔}_{{𝐱𝐱}_k}^{+{𝖳}} + {𝐔}_{{𝐱𝐩}_k}^+{𝐃}_{{𝐩𝐩}_k}^+{𝐔}_{{𝐱𝐩}_k}^{+{𝖳}}\Big){𝚽}_{{𝐱𝐱}_k}^{{𝖳}} & {𝚽}_{{𝐱𝐱}_k}{𝐔}_{{𝐱𝐩}_k}^+{𝐃}_{{𝐩𝐩}_k}^+{𝐔}_{{𝐩𝐩}_k}^{+{𝖳}} \\ +{𝚽}_{{𝐱𝐱}_k}{𝐔}_{{𝐱𝐩}_k}^+{𝐃}_{{𝐩𝐩}_k}^+{𝐔}_{{𝐩𝐩}_k}^{+{𝖳}}{𝚽}_{{𝐱𝐩}_k}^{{𝖳}} & +{𝚽}_{{𝐱𝐩}_k}{𝐔}_{{𝐩𝐩}_k}^+{𝐃}_{{𝐩𝐩}_k}^+{𝐔}_{{𝐩𝐩}_k}^{+{𝖳}} \\ +{𝚽}_{{𝐱𝐩}_k}{𝐔}_{{𝐩𝐩}_k}^+{𝐃}_{{𝐩𝐩}_k}^+{𝐔}_{{𝐱𝐩}_k}^{+{𝖳}}{𝚽}_{{𝐱𝐱}_k}^{{𝖳}} & \\ +{𝚽}_{{𝐱𝐩}_k}{𝐔}_{{𝐩𝐩}_k}^+{𝐃}_{{𝐩𝐩}_k}^+{𝐔}_{{𝐩𝐩}_k}^{+{𝖳}}{𝚽}_{{𝐱𝐩}_k}^{{𝖳}} + {𝐐}_{{𝐱𝐱}_k} & \\ \hline {𝐔}_{{𝐩𝐩}_k}^+{𝐃}_{{𝐩𝐩}_k}^+{𝐔}_{{𝐱𝐩}_k}^{+{𝖳}}{𝚽}_{{𝐱𝐱}_k}^{{𝖳}} + {𝐔}_{{𝐩𝐩}_k}^+{𝐃}_{{𝐩𝐩}_k}^+{𝐔}_{{𝐩𝐩}_k}^{+{𝖳}}{𝚽}_{{𝐱𝐩}_k}^{{𝖳}} & {𝐔}_{{𝐩𝐩}_k}^+{𝐃}_{{𝐩𝐩}_k}^+{𝐔}_{{𝐩𝐩}_k}^{+{𝖳}} \end{array}\biggr] \qquad\qquad(8.27)
```

Equating each component of the matrix in Eqs [\(8.26\)](#page-100-1) and [\(8.27\)](#page-100-2), we find that the $`(2, 2)`$ component yields

<span id="page-100-3"></span>
```math
\tilde{{𝐔}}_{{𝐩𝐩}_k} = {𝐔}_{{𝐩𝐩}_k}^+ \qquad\qquad(8.28)
```

```math
\tilde{{𝐃}}_{{𝐩𝐩}_k} = {𝐃}_{{𝐩𝐩}_k}^+ \qquad\qquad(8.29)
```

Equating the $`(1, 2)`$ (or $`(2, 1)`$) component yields

<span id="page-100-4"></span>
```math
\tilde{{𝐔}}_{{𝐱𝐩}_k} = {𝚽}_{{𝐱𝐱}_k}{𝐔}_{{𝐱𝐩}_k}^+ + {𝚽}_{{𝐱𝐩}_k}{𝐔}_{{𝐩𝐩}_k}^+ \qquad\qquad(8.30)
```

Finally, equating the $`(1, 1)`$ components of Eqs. [\(8.26\)](#page-100-1) and [\(8.27\)](#page-100-2), and using Eqs. [\(8.28\)](#page-100-3), [\(8.29\)](#page-100-3) and [\(8.30\)](#page-100-4), we find that

```math
\tilde{{𝐔}}_{{𝐱𝐱}_k}\tilde{{𝐃}}_{{𝐱𝐱}_k}\tilde{{𝐔}}_{{𝐱𝐱}_k}^{{𝖳}} = {𝚽}_{{𝐱𝐱}_k}{𝐔}_{{𝐱𝐱}_k}^+{𝐃}_{{𝐱𝐱}_k}^+{𝐔}_{{𝐱𝐱}_k}^{+{𝖳}}{𝚽}_{{𝐱𝐱}_k}^{{𝖳}} + {𝐐}_{{𝐱𝐱}_k} \qquad\qquad(8.31)
```

Since we have partitioned the states such that $`{𝐱}`$ comprises the position, velocity, attitude and clock states (or others, as appropriate), we use the ***modified* Gram-Schmidt algorithm** to update $`\tilde{{𝐔}}_{{𝐱𝐱}_k}`$ and $`\tilde{{𝐃}}_{{𝐱𝐱}_k}`$. And then we compute $`\tilde{{𝐔}}_{{𝐩𝐩}_k}`$, $`\tilde{{𝐃}}_{{𝐩𝐩}_k}`$ and $`\tilde{{𝐔}}_{{𝐱𝐩}_k}`$ according to Eqs. [\(8.28\)](#page-100-3) - [\(8.30\)](#page-100-4).

Thus, given $`n_{{𝐱}}`$ states with $`m_{{𝐱}}`$ process noise parameters associated with those states, the number of computations associated with the the first sub-problem is: $`[1.5n_{{𝐱}}^3 + 0.5n_{{𝐱}}^2(2m_{{𝐱}} - 1)]`$ adds, $`[0.5n_{{𝐱}}^2(3n_{{𝐱}} + 1) + n_{{𝐱}}m_{{𝐱}}(n_{{𝐱}} + 1)]`$ multiplies, and $`[(n_{{𝐱}} + m_{{𝐱}})(n_{{𝐱}} - 1)]`$ divides.

#### 8.3.2.2. The Second Sub-Problem ($`{𝚽}_{2_k}\tilde{{𝐔}}_k\tilde{{𝐃}}_k\tilde{{𝐔}}_k^{{𝖳}}{𝚽}_{2_k}^{{𝖳}} + {𝐐}_{2_k}`$)

Now we look at 2). We now partition $`\tilde{{𝐔}}_k`$ and $`\tilde{{𝐃}}_k`$ as

```math
\tilde{{𝐔}}_k = \begin{bmatrix} \tilde{{𝐔}}_{{𝐚𝐚}_k} & \tilde{{𝐔}}_{{𝐚}b_k} & \tilde{{𝐔}}_{{𝐚𝐜}_k} \\ {𝟎} & 1 & \tilde{{𝐔}}_{b{𝐜}_k} \\ {𝟎} & {𝟎} & \tilde{{𝐔}}_{{𝐜𝐜}_k} \end{bmatrix} \begin{matrix} \}\, n_a \\ \}\, 1 \\ \}\, n_c \end{matrix} \qquad \text{and} \qquad \tilde{{𝐃}}_k = \begin{bmatrix} \tilde{{𝐃}}_{{𝐚𝐚}_k} & {𝟎} & {𝟎} \\ {𝟎} & \tilde{d}_{b_k} & {𝟎} \\ {𝟎} & {𝟎} & \tilde{{𝐃}}_{{𝐜𝐜}_k} \end{bmatrix} \begin{matrix} \}\, n_a \\ \}\, 1 \\ \}\, n_c \end{matrix} \qquad\qquad(8.32)
```

in order to isolate a parameter. Correspondingly,

```math
{𝚽}_{2_k} = \begin{bmatrix} {𝐈} & {𝟎} & {𝟎} \\ {𝟎} & 1 & {𝟎} \\ {𝟎} & {𝟎} & {𝐌}_{c_k} \end{bmatrix} \begin{bmatrix} {𝐈} & {𝟎} & {𝟎} \\ {𝟎} & m_{b_k} & {𝟎} \\ {𝟎} & {𝟎} & {𝐈} \end{bmatrix} = {𝚽}_{c_k}{𝚽}_{b_k} \qquad\qquad(8.33)
```

and since the process noise of an ECRV is constant $`{𝐐}_{2_k} = {𝐐}_2`$ so that $`{𝐐}_2`$ is

```math
{𝐐}_2 = \begin{bmatrix} {𝟎} & {𝟎} & {𝟎} \\ {𝟎} & q_b & {𝟎} \\ {𝟎} & {𝟎} & {𝟎} \end{bmatrix} + \begin{bmatrix} {𝟎} & {𝟎} & {𝟎} \\ {𝟎} & 0 & {𝟎} \\ {𝟎} & {𝟎} & {𝐐}_c \end{bmatrix} = {𝐐}_b + {𝐐}_c \qquad\qquad(8.34)
```

As in the previous section, we note that $`{𝚽}_{c_k}^{-1}{𝐐}_b{𝚽}_{c_k}^{-{𝖳}} = {𝐐}_b`$. So, now Eq. [\(8.25\)](#page-100-5) becomes

<span id="page-101-0"></span>
```math
{𝐔}_{k+1}^-{𝐃}_{k+1}^-{𝐔}_{k+1}^{-{𝖳}} = {𝚽}_{c_k}\Bigl[{𝚽}_{b_k}\tilde{{𝐔}}_k\tilde{{𝐃}}_k\tilde{{𝐔}}_k^{{𝖳}}{𝚽}_{b_k}^{{𝖳}} + {𝐐}_b\Bigr]{𝚽}_{c_k}^{{𝖳}} + {𝐐}_c \qquad\qquad(8.35)
```

The term in the square bracket in Eq. [\(8.35\)](#page-101-0) is

```math
\breve{{𝐔}}_k\breve{{𝐃}}_k\breve{{𝐔}}_k^{{𝖳}} = {𝚽}_{b_k}\tilde{{𝐔}}_k\tilde{{𝐃}}_k\tilde{{𝐔}}_k^{{𝖳}}{𝚽}_{b_k}^{{𝖳}} + {𝐐}_b \qquad\qquad(8.36)
```

In Appendix B, the equation above is expanded until we find that

```math
\breve{{𝐔}}_{{𝐚𝐜}_k} = \tilde{{𝐔}}_{{𝐚𝐜}_k}, \qquad \breve{{𝐃}}_{{𝐜𝐜}_k} = \tilde{{𝐃}}_{{𝐜𝐜}_k}, \qquad \breve{{𝐔}}_{{𝐜𝐜}_k}^{{𝖳}} = \tilde{{𝐔}}_{{𝐜𝐜}_k}^{{𝖳}} \qquad\qquad(8.37)
```

Additionally,

<span id="page-101-4"></span>
```math
\breve{{𝐔}}_{b{𝐜}_k} = m_{b_k}\tilde{{𝐔}}_{b{𝐜}_k} \qquad\qquad(8.38)
```

and

<span id="page-101-2"></span>
```math
\breve{d}_{b_k} = m_{b_k}^2\tilde{d}_{b_k} + q_b \qquad\qquad(8.39)
```

and

<span id="page-101-3"></span>
```math
\breve{{𝐔}}_{{𝐚}b_k} = m_{b_k}\frac{\tilde{d}_{b_k}}{\breve{d}_{b_k}}\tilde{{𝐔}}_{{𝐚}b_k} \qquad\qquad(8.40)
```

Finally, we find that

<span id="page-101-1"></span>
```math
\breve{{𝐔}}_{{𝐚𝐚}_k}\breve{{𝐃}}_{{𝐚𝐚}_k}\breve{{𝐔}}_{{𝐚𝐚}_k}^{{𝖳}} = \tilde{{𝐔}}_{{𝐚𝐚}_k}\tilde{{𝐃}}_{{𝐚𝐚}_k}\tilde{{𝐔}}_{{𝐚𝐚}_k}^{{𝖳}} + \left(\frac{\tilde{d}_{b_k}q_b}{\breve{d}_{b_k}}\right)\tilde{{𝐔}}_{{𝐚}b_k}\tilde{{𝐔}}_{{𝐚}b_k}^{{𝖳}} \qquad\qquad(8.41)
```

We note that $`\tilde{{𝐔}}_{{𝐚}b_k}`$ is a column vector (and is thereby of rank 1) so Eq. [\(8.41\)](#page-101-1) constitutes a 'rank one' update. Since $`\breve{d}_{b_k}`$, $`\tilde{d}_{b_k}`$ and $`q_b`$ are all positive (assuming $`m_{b_k}`$ is a positive quantity), we can use the Agee-Turner Rank One update [[1](16-bibliography.md#page-170-16)]. It should be pointed out that as the algorithm proceeds down the 'list' of parameters, the size of the states $`{𝐚}`$ increases by one (and consequently the size of the parameters $`{𝐜}`$ decreases by one. Hence $`\breve{{𝐔}}_{{𝐚𝐚}_k}`$ and $`\breve{{𝐃}}_{{𝐚𝐚}_k}`$ begins with a dimension of $`n_{{𝐱}}`$ and concludes with dimension $`n_{{𝐱}} + n_{{𝐩}} - 1`$.

Therefore, this is done recursively for all the (sensor) parameters $`{𝐩}`$ which are of size $`n_{{𝐩}}`$.

#### The Algorithm for $`{𝚽}_{2_k}\tilde{{𝐔}}_k\tilde{{𝐃}}_k\tilde{{𝐔}}_k^{{𝖳}}{𝚽}_{2_k}^{{𝖳}} + {𝐐}_{2_k}`$

The algorithm can be expressed as follows (with the arithmetic operations (adds, multiplies, divides) in square brackets per $`k`$ ):

> **for** $`k = 1, \cdots, n_{{𝐩}}`$ **do**  
> &emsp;$`\breve{{𝐃}}(n_{{𝐱}}+k, n_{{𝐱}}+k) = {𝐌}(k,k)^2\tilde{{𝐃}}(n_{{𝐱}}+k, n_{{𝐱}}+k) + {𝐐}_{{𝐩𝐩}}(k,k)`$ &emsp; (Eq. [\(8.39\)](#page-101-2)) $`[1, 2, 0]`$  
> &emsp;$`\alpha = {𝐌}(k,k)\frac{\tilde{{𝐃}}(n_{{𝐱}}+k, n_{{𝐱}}+k)}{\breve{{𝐃}}(n_{{𝐱}}+k, n_{{𝐱}}+k)}`$ &emsp; $`[0, 1, 1]`$  
> &emsp;**for** $`i = 1, \cdots, (n_{{𝐱}}+k-1)`$ **do**  
> &emsp;&emsp;$`\breve{{𝐔}}(i, n_{{𝐱}}+k) = \alpha\tilde{{𝐔}}(i, n_{{𝐱}}+k)`$ &emsp; (Eq. [\(8.40\)](#page-101-3)) $`[0, n_{{𝐱}}+k-1, 0]`$  
> &emsp;**end for**  
> &emsp;**for** $`j = n_{{𝐱}}+k+1, \cdots, (n_{{𝐱}}+n_{{𝐩}})`$ **do**  
> &emsp;&emsp;$`\breve{{𝐔}}(n_{{𝐱}}+k, j) = {𝐌}(k,k)\tilde{{𝐔}}(n_{{𝐱}}+k, j)`$ &emsp; (Eq. [\(8.38\)](#page-101-4)) $`[0, n_{{𝐩}}-k, 0]`$  
> &emsp;**end for**  
> &emsp;Solve for $`\breve{{𝐔}}_{{𝐱𝐱}}^{(k)}, \breve{{𝐃}}_{{𝐱𝐱}}^{(k)}`$ using<sup>1</sup> the Rank-One update $`[n_{{𝐱}}+k)^2, (n_{{𝐱}}+k)^2 + 3(n_{{𝐱}}+k) + 2, 0]`$  
> **end for**

<span id="page-102-0"></span><sup>1</sup> We are using the nomenclature $`{𝐔}^{(k)}`$ and $`{𝐃}^{(k)}`$ to denote the upper left $`n_{{𝐱}} + k - 1`$ rows and columns of the $`{𝐔}`$ and $`{𝐃}`$ matrices

Thus, the arithmetic operations are as follows:

Adds:

```math
\sum_{k=1}^{n_{{𝐩}}}\Bigl((n_{{𝐱}}+k)^2 + 1\Bigr) = n_{{𝐱}}^2 n_{{𝐩}} + n_{{𝐩}} + n_{{𝐱}}(n_{{𝐩}}+1)n_{{𝐩}} + \sum_{k=1}^{n_{{𝐩}}} k^2 \qquad\qquad(8.42)
```

Multiplies:

```math
\begin{aligned} \sum_{k=1}^{n_{{𝐩}}}\Bigl(3 + (n_{{𝐱}}+k-1) + n_{{𝐩}} - k + (n_{{𝐱}}+k)^2 + 3(n_{{𝐱}}+k) + 2\Bigr) &= (5.5 + 5n_{{𝐱}} + n_{{𝐱}}^2)n_{{𝐩}} \\ &\quad + \frac{1}{2}(2n_{{𝐱}} + 5)n_{{𝐩}}^2 + \sum_{k=1}^{n_{{𝐩}}} k^2 \end{aligned} \qquad\qquad(8.43)
```

and $`n_{{𝐩}}`$ divides.

---

[← Chapter 8. Factorization Methods (part 1 of 3)](08-factorization-methods-part1.md) · [Contents](README.md) · [Chapter 8. Factorization Methods (part 3 of 3) →](08-factorization-methods-part3.md)
