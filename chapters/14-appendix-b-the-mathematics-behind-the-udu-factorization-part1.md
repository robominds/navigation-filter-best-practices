[← Appendix A. Models and Realizations of Random Variables](13-appendix-a-models-and-realizations-of-random-variables.md) · [Contents](README.md) · [Appendix B. The Mathematics Behind the UDU Factorization (part 2 of 3) →](14-appendix-b-the-mathematics-behind-the-udu-factorization-part2.md)

# <span id="page-148-0"></span>Appendix B. The Mathematics Behind the UDU Factorization

*Contributed by Chris D'Souza*

## B.1. The Partitioning into Two Subproblems

<span id="page-148-1"></span>We can find that the update equation is

```math
{𝐔}_{k+1}^{-}{𝐃}_{k+1}^{-}{𝐔}_{k+1}^{-{𝖳}} = {𝚽}_k{𝐔}_k^{+}{𝐃}_k^{+}{𝐔}_k^{+{𝖳}}{𝚽}_k^{{𝖳}} + {𝐐}_k \qquad\qquad(B.1)
```

```math
\begin{aligned} &= {𝚽}_{2_k}{𝚽}_{1_k}{𝐔}_k^{+}{𝐃}_k^{+}{𝐔}_k^{+{𝖳}}{𝚽}_{1_k}^{{𝖳}}{𝚽}_{2_k}^{{𝖳}} + {𝐐}_{1_k} + {𝐐}_{2_k} \\ &= {𝚽}_{2_k}\Bigl[{𝚽}_{1_k}{𝐔}_k^{+}{𝐃}_k^{+}{𝐔}_k^{+{𝖳}}{𝚽}_{1_k}^{{𝖳}}\Bigr]{𝚽}_{2_k}^{{𝖳}} + {𝐐}_{1_k} + {𝐐}_{2_k} \end{aligned} \qquad\qquad(B.2)
```

Recalling that $`{𝐐}_{1_k} = {𝚽}_{2_k}{𝚽}_{2_k}^{-1}{𝐐}_{1_k}{𝚽}_{2_k}^{-{𝖳}}{𝚽}_{2_k}^{{𝖳}}`$ and

```math
{𝚽}_{2_k}^{-1} = \begin{bmatrix} {𝐈} & {𝟎} \\ {𝟎} & {𝐌}_k^{-1} \end{bmatrix} \qquad\qquad(B.3)
```

where $`{𝐌}_k^{-1} = \mathop{\mathrm{diag}}(1/m_{k_i}),\ i = 1, 2, 3, \cdots, n_{{𝐩}}`$. We note that

```math
{𝚽}_{2_k}^{-1}{𝐐}_{1_k}{𝚽}_{2_k}^{-{𝖳}} = \begin{bmatrix} {𝐈} & {𝟎} \\ {𝟎} & {𝐌}_k^{-1} \end{bmatrix} \begin{bmatrix} {𝐐}_{{𝐱𝐱}_k} & {𝟎} \\ {𝟎} & {𝟎} \end{bmatrix} \begin{bmatrix} {𝐈} & {𝟎} \\ {𝟎} & {𝐌}_k^{-1} \end{bmatrix} = \begin{bmatrix} {𝐐}_{{𝐱𝐱}_k} & {𝟎} \\ {𝟎} & {𝟎} \end{bmatrix} = {𝐐}_{1_k} \qquad\qquad(B.4)
```

## B.2. The Mathematics Behind the Second Subproblem

<span id="page-148-2"></span>Recall that we partitioned $`\tilde{{𝐔}}`$ and $`\tilde{{𝐃}}`$ as

```math
\tilde{{𝐔}}_k = \begin{bmatrix} \tilde{{𝐔}}_{{𝐚𝐚}_k} & \tilde{{𝐔}}_{{𝐚}b_k} & \tilde{{𝐔}}_{{𝐚𝐜}_k} \\ {𝟎} & 1 & \tilde{{𝐔}}_{b{𝐜}_k} \\ {𝟎} & {𝟎} & \tilde{{𝐔}}_{{𝐜𝐜}_k} \end{bmatrix} \begin{array}{l} \}\, n_a \\ \}\, 1 \\ \}\, n_c \end{array} \qquad \text{and} \qquad \tilde{{𝐃}}_k = \begin{bmatrix} \tilde{{𝐃}}_{{𝐚𝐚}_k} & {𝟎} & {𝟎} \\ {𝟎} & \tilde{d}_{b_k} & {𝟎} \\ {𝟎} & {𝟎} & \tilde{{𝐃}}_{{𝐜𝐜}_k} \end{bmatrix} \begin{array}{l} \}\, n_a \\ \}\, 1 \\ \}\, n_c \end{array} \qquad\qquad(B.5)
```

in order to isolate a parameter. In fact, the state we choose to isolate is one of the Gauss-Markov states (likely associated with a sensor). Let

```math
{𝚽}_{2_k} = \begin{bmatrix} {𝐈} & {𝟎} & {𝟎} \\ {𝟎} & 1 & {𝟎} \\ {𝟎} & {𝟎} & {𝐌}_{c_k} \end{bmatrix} \begin{bmatrix} {𝐈} & {𝟎} & {𝟎} \\ {𝟎} & m_{b_k} & {𝟎} \\ {𝟎} & {𝟎} & {𝐈} \end{bmatrix} = {𝚽}_{c_k}{𝚽}_{b_k} \qquad\qquad(B.6)
```

and

```math
{𝐐}_{2_k} = \begin{bmatrix} {𝟎} & {𝟎} & {𝟎} \\ {𝟎} & q_{b_k} & {𝟎} \\ {𝟎} & {𝟎} & {𝟎} \end{bmatrix} + \begin{bmatrix} {𝟎} & {𝟎} & {𝟎} \\ {𝟎} & 0 & {𝟎} \\ {𝟎} & {𝟎} & {𝐐}_{c_k} \end{bmatrix} = {𝐐}_{b_k} + {𝐐}_{c_k} \qquad\qquad(B.7)
```

As in the previous exercise, we note that $`{𝚽}_{c_k}^{-1}{𝐐}_{b_k}{𝚽}_{c_k}^{-{𝖳}} = {𝐐}_{b_k}`$. So, now Eq. [\(8.25\)](08-factorization-methods-part2.md#page-100-5) becomes

<span id="page-149-0"></span>
```math
{𝐔}_{k+1}^{-}{𝐃}_{k+1}^{-}{𝐔}_{k+1}^{-{𝖳}} = {𝚽}_{c_k}\Bigl[{𝚽}_{b_k}\tilde{{𝐔}}_k\tilde{{𝐃}}_k\tilde{{𝐔}}_k^{{𝖳}}{𝚽}_{b_k}^{{𝖳}} + {𝐐}_{b_k}\Bigr]{𝚽}_{c_k}^{{𝖳}} + {𝐐}_{c_k} \qquad\qquad(B.8)
```

The term in the square bracket in Eq. [\(B.8\)](#page-149-0) is

<span id="page-149-1"></span>
```math
\breve{{𝐔}}_k\breve{{𝐃}}_k\breve{{𝐔}}_k^{{𝖳}} = {𝚽}_{b_k}\tilde{{𝐔}}_k\tilde{{𝐃}}_k\tilde{{𝐔}}_k^{{𝖳}}{𝚽}_{b_k}^{{𝖳}} + {𝐐}_{b_k} \qquad\qquad(B.9)
```

The left side of Eq. [\(B.9\)](#page-149-1) (recalling that $`\breve{{𝐔}}_{bb_k} = 1`$) is

<span id="page-149-2"></span>
```math
\breve{{𝐔}}_k\breve{{𝐃}}_k\breve{{𝐔}}_k^{{𝖳}} = \biggl[\begin{array}{c|c|c} \breve{{𝐔}}_{{𝐚𝐚}_k}\breve{{𝐃}}_{{𝐚𝐚}_k}\breve{{𝐔}}_{{𝐚𝐚}_k}^{{𝖳}} & \breve{{𝐔}}_{{𝐚𝐜}_k}\breve{{𝐃}}_{{𝐜𝐜}_k}\breve{{𝐔}}_{{𝐚𝐜}_k}^{{𝖳}} & \breve{{𝐔}}_{{𝐚𝐜}_k}\breve{{𝐃}}_{{𝐜𝐜}_k}\breve{{𝐔}}_{{𝐜𝐜}_k}^{{𝖳}} \\ +\breve{{𝐔}}_{{𝐚}b_k}\breve{d}_{b_k}\breve{{𝐔}}_{{𝐚}b_k}^{{𝖳}} & +\breve{{𝐔}}_{{𝐚}b_k}\breve{d}_{b_k} & \\ \breve{{𝐔}}_{{𝐚𝐜}_k}\breve{{𝐃}}_{{𝐜𝐜}_k}\breve{{𝐔}}_{{𝐚𝐜}_k}^{{𝖳}} & & \\ \hline \breve{d}_{b_k}\breve{{𝐔}}_{{𝐚}b_k}^{{𝖳}} & \breve{d}_{b_k} + \breve{{𝐔}}_{b{𝐜}_k}\breve{{𝐃}}_{{𝐜𝐜}_k}\breve{{𝐔}}_{b{𝐜}_k}^{{𝖳}} & \breve{{𝐔}}_{b{𝐜}_k}\breve{{𝐃}}_{{𝐜𝐜}_k}\breve{{𝐔}}_{{𝐜𝐜}_k}^{{𝖳}} \\ \breve{{𝐔}}_{b{𝐜}_k}\breve{{𝐃}}_{{𝐜𝐜}_k}\breve{{𝐔}}_{{𝐚𝐜}_k}^{{𝖳}} & & \\ \hline \breve{{𝐔}}_{{𝐜𝐜}_k}\breve{{𝐃}}_{{𝐜𝐜}_k}\breve{{𝐔}}_{{𝐚𝐜}_k}^{{𝖳}} & \breve{{𝐔}}_{{𝐜𝐜}_k}\breve{{𝐃}}_{{𝐜𝐜}_k}\breve{{𝐔}}_{b{𝐜}_k}^{{𝖳}} & \breve{{𝐔}}_{{𝐜𝐜}_k}\breve{{𝐃}}_{{𝐜𝐜}_k}\breve{{𝐔}}_{{𝐜𝐜}_k}^{{𝖳}} \end{array}\biggr] \qquad\qquad(B.10)
```

The right side of Eq. [\(B.9\)](#page-149-1), once again recalling that $`\tilde{{𝐔}}_{bb_k} = 1`$, is

<span id="page-149-3"></span>
```math
\begin{aligned} &{𝚽}_{b_k}\tilde{{𝐔}}_k\tilde{{𝐃}}_k\tilde{{𝐔}}_k^{{𝖳}}{𝚽}_{b_k}^{{𝖳}} + {𝐐}_{b_k} = \\ &\quad \biggl[\begin{array}{c|c|c} \tilde{{𝐔}}_{{𝐚𝐚}_k}\tilde{{𝐃}}_{{𝐚𝐚}_k}\tilde{{𝐔}}_{{𝐚𝐚}_k}^{{𝖳}} & m_{b_k}\tilde{{𝐔}}_{{𝐚𝐜}_k}\tilde{{𝐃}}_{{𝐜𝐜}_k}\tilde{{𝐔}}_{{𝐚𝐜}_k}^{{𝖳}} & \tilde{{𝐔}}_{{𝐚𝐜}_k}\tilde{{𝐃}}_{{𝐜𝐜}_k}\tilde{{𝐔}}_{{𝐜𝐜}_k}^{{𝖳}} \\ +\tilde{{𝐔}}_{{𝐚}b_k}\tilde{d}_{b_k}\tilde{{𝐔}}_{{𝐚}b_k}^{{𝖳}} & +m_{b_k}\tilde{{𝐔}}_{{𝐚}b_k}\tilde{d}_{b_k} & \\ \tilde{{𝐔}}_{{𝐚𝐜}_k}\tilde{{𝐃}}_{{𝐜𝐜}_k}\tilde{{𝐔}}_{{𝐚𝐜}_k}^{{𝖳}} & & \\ \hline m_{b_k}\tilde{d}_{b_k}\tilde{{𝐔}}_{{𝐚}b_k}^{{𝖳}} & m_{b_k}^2\tilde{{𝐔}}_{b{𝐜}_k}\tilde{{𝐃}}_{{𝐜𝐜}_k}\tilde{{𝐔}}_{b{𝐜}_k}^{{𝖳}} & m_{b_k}\tilde{{𝐔}}_{b{𝐜}_k}\tilde{{𝐃}}_{{𝐜𝐜}_k}\tilde{{𝐔}}_{{𝐜𝐜}_k}^{{𝖳}} \\ +m_{b_k}\tilde{{𝐔}}_{b{𝐜}_k}\tilde{{𝐃}}_{{𝐜𝐜}_k}\tilde{{𝐔}}_{{𝐚𝐜}_k}^{{𝖳}} & +m_{b_k}^2\tilde{d}_{b_k} + q_{b_k} & \\ \hline \tilde{{𝐔}}_{{𝐜𝐜}_k}\tilde{{𝐃}}_{{𝐜𝐜}_k}\tilde{{𝐔}}_{{𝐚𝐜}_k}^{{𝖳}} & m_{b_k}\tilde{{𝐔}}_{{𝐜𝐜}_k}\tilde{{𝐃}}_{{𝐜𝐜}_k}\tilde{{𝐔}}_{b{𝐜}_k}^{{𝖳}} & \tilde{{𝐔}}_{{𝐜𝐜}_k}\tilde{{𝐃}}_{{𝐜𝐜}_k}\tilde{{𝐔}}_{{𝐜𝐜}_k}^{{𝖳}} \end{array}\biggr] \end{aligned} \qquad\qquad(B.11)
```

Equating the components in Eqs. [\(B.10\)](#page-149-2) and [\(B.11\)](#page-149-3), from the (1,3) and (3,3) element, we find

```math
\breve{{𝐔}}_{{𝐚𝐜}_k} = \tilde{{𝐔}}_{{𝐚𝐜}_k}, \qquad \breve{{𝐃}}_{{𝐜𝐜}_k} = \tilde{{𝐃}}_{{𝐜𝐜}_k}, \qquad \breve{{𝐔}}_{{𝐜𝐜}_k}^{{𝖳}} = \tilde{{𝐔}}_{{𝐜𝐜}_k}^{{𝖳}} \qquad\qquad(B.12)
```

From the (2,3) element we get,

<span id="page-149-4"></span>
```math
\breve{{𝐔}}_{b{𝐜}_k} = m_{b_k}\tilde{{𝐔}}_{b{𝐜}_k} \qquad\qquad(B.13)
```

From the (2,2) element and using the results of Eq. [\(B.13\)](#page-149-4), we find that

```math
\breve{d}_{b_k} = m_{b_k}^2\tilde{d}_{b_k} + q_{b_k} \qquad\qquad(B.14)
```

The (2,1) element yields

```math
\breve{{𝐔}}_{{𝐚}b_k} = m_{b_k}\frac{\tilde{d}_{b_k}}{\breve{d}_{b_k}}\tilde{{𝐔}}_{{𝐚}b_k} \qquad\qquad(B.15)
```

What finally remains is the (1,1) element and it is on this we focus. Using the relations in the previous equations, we find that

<span id="page-150-1"></span>
```math
\breve{{𝐔}}_{{𝐚𝐚}_k}\breve{{𝐃}}_{{𝐚𝐚}_k}\breve{{𝐔}}_{{𝐚𝐚}_k}^{{𝖳}} = \tilde{{𝐔}}_{{𝐚𝐚}_k}\tilde{{𝐃}}_{{𝐚𝐚}_k}\tilde{{𝐔}}_{{𝐚𝐚}_k}^{{𝖳}} + \biggl[\tilde{d}_{b_k} - m_{b_k}^2\frac{\tilde{d}_{b_k}}{\breve{d}_{b_k}}\biggr]\tilde{{𝐔}}_{{𝐚}b_k}\tilde{{𝐔}}_{{𝐚}b_k}^{{𝖳}} \qquad\qquad(B.16)
```

The term in the bracket can be simplified as

```math
\biggl[\tilde{d}_{b_k} - m_{b_k}^2\frac{\tilde{d}_{b_k}}{\breve{d}_{b_k}}\biggr] = \frac{m_{b_k}^2\tilde{d}_{b_k}^2 + q_{b_k}\tilde{d}_{b_k} - m_{b_k}^2\tilde{d}_{b_k}^2}{m_{b_k}^2\tilde{d}_{b_k} + q_{b_k}} = \frac{\tilde{d}_{b_k}q_{b_k}}{m_{b_k}^2\tilde{d}_{b_k} + q_{b_k}} = \frac{\tilde{d}_{b_k}q_{b_k}}{\breve{d}_{b_k}} \qquad\qquad(B.17)
```

so Eq. [\(B.16\)](#page-150-1) becomes

<span id="page-150-2"></span>
```math
\breve{{𝐔}}_{{𝐚𝐚}_k}\breve{{𝐃}}_{{𝐚𝐚}_k}\breve{{𝐔}}_{{𝐚𝐚}_k}^{{𝖳}} = \tilde{{𝐔}}_{{𝐚𝐚}_k}\tilde{{𝐃}}_{{𝐚𝐚}_k}\tilde{{𝐔}}_{{𝐚𝐚}_k}^{{𝖳}} + \left(\frac{\tilde{d}_{b_k}q_{b_k}}{\breve{d}_{b_k}}\right)\tilde{{𝐔}}_{{𝐚}b_k}\tilde{{𝐔}}_{{𝐚}b_k}^{{𝖳}} \qquad\qquad(B.18)
```

We note that $`\tilde{{𝐔}}_{{𝐚}b_k}`$ is a column vector so Eq. [\(B.18\)](#page-150-2), and hence is of rank 1, constitutes a 'rank one' update. Since $`\breve{d}_{b_k}`$, $`\tilde{d}_{b_k}`$ and $`q_{b_k}`$ are all positive (assuming $`m_{b_k}`$ is a positive quantity), we can use the Agee-Turner Rank One update [[1](16-bibliography.md#page-170-16)]. It should be pointed out that as the algorithm proceeds down the 'list' of parameters, the size of the states $`{𝐚}`$ increases by one (and consequently the size of the parameters $`{𝐜}`$ decreases by one. Hence $`\breve{{𝐔}}_{{𝐚𝐚}_k}`$ and $`\breve{{𝐃}}_{{𝐚𝐚}_k}`$ begin with a dimension of $`n_{{𝐱}}`$ and conclude with dimension $`n_{{𝐱}} + n_{{𝐩}} - 1`$.

Therefore, this is done recursively for all the (sensor) parameters $`{𝐩}`$ which are of size $`n_{{𝐩}}`$.

---

[← Appendix A. Models and Realizations of Random Variables](13-appendix-a-models-and-realizations-of-random-variables.md) · [Contents](README.md) · [Appendix B. The Mathematics Behind the UDU Factorization (part 2 of 3) →](14-appendix-b-the-mathematics-behind-the-udu-factorization-part2.md)
