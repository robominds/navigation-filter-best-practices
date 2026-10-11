[← Chapter 7. State Representations](07-state-representations.md) · [Contents](README.md) · [Chapter 8. Factorization Methods (part 2 of 3) →](08-factorization-methods-part2.md)

# <span id="page-94-0"></span>Chapter 8. Factorization Methods

*Contributed by Christopher D'Souza*

Of the various covariance factorization methods[<sup>∗</sup>](#page-94-2), the UDU covariance factorization technique is among the most commonly used covariance matrix factorization methodologies used in practice. For example, it is implemented in the Goddard Enhanced Onboard Navigation System (GEONS), which has flown on several robotic missions, and is the heart of the Orion Absolute Navigation System. This chapter is intended to present the UDU triangular factorization method and the rationale for its use.

<span id="page-94-2"></span><sup>∗</sup> Other options include the Square Root Covariance Factorization and the Square Root Information Filter (SRIF).

Above all, we demonstrate that the UDU factorization results in a significant reduction in the arithmetic operations (specifically adds and multiplies) compared with the usual ($`{𝐏}_{k+1}^- = {𝚽}(t_k, t_{k+1}){𝐏}_k{𝚽}^{{𝖳}}(t_k, t_{k+1}) + {𝐐}_k`$) time update and the Joseph measurement update.

In the next section, we present some notational and preliminary operations for the matrix factors $`{𝐔}`$ and $`{𝐃}`$. In the section that follows, we will derive the time update equations for the aforementioned covariance matrix factors. Next, we will derive the measurement update equations for the covariance matrix factors. Finally, we will present some concluding comments.

## 8.1. Why Use the UDU Factorization?

<span id="page-94-1"></span>The usual Kalman filter equations work well for rather simple problems. But once the state-space becomes large, the condition number of the covariance matrix becomes large and nonlinear effects begin to affect the numerical characteristics, problems such as filter divergence and nonpositive definiteness of the covariance matrix occur. These issues began to be observed almost as soon as Kalman filters began to be used in real problems. Matrix factorization techniques were introduced to solve (at least) some of these issues. The earliest was the Potter Square Root Factorization, which was used in the on-board Apollo navigation filters.

In fact Bierman and Thornton, in a 1976 JPL Report, rather cheekily compare those who insist on using the conventional Kalman filtering and batch least-squares algorithms (*contra* the matrix factorization algorithms) to unrepentant smokers by describing "*an attitude often encountered among estimation practitioners [is] that they will switch to the more accurate and stable algorithms if and when numerical problems occur. An analogy comes to mind of a smoker who promises to stop when cancer or heart ailment symptoms are detected. To expand on the analogy, one may note the following:*

- *Most smokers do not get cancer or heart disease. (Most applications of the Kalman algorithms work.)*
- *Even when catastrophic illness does not occur, there is diminished health. (Even when algorithms work, performance may be degraded.)*
- *Smokers can take precautions to lessen the danger, such as smoking low tar or filtered cigarettes. (Engineers can scale their variables to reduce the dynamic range or use double-precision arithmetic.)*
- *Lung cancer may not be diagnosed until it is too advanced for treatment. (Numerical problems may not be detected in time to be remedied.)* " [[83](16-bibliography.md#page-173-9)]

In addition, a little advertised, but incredibly useful feature of the UDU factorization is the ability to interrogate for the positive definiteness of the covariance matrix for 'free', because the condition required for positive definiteness of $`{𝐏}`$ is that the entries of $`{𝐃}`$ are positive[<sup>††</sup>](#page-95-1).

<span id="page-95-1"></span><sup>††</sup> The positive definiteness of the covariance matrix, $`{𝐏}`$, can be determined by interrogating the entries of $`{𝐃}`$. It must be noted that the elements of $`{𝐃}`$ are *not* the eigenvalues of $`{𝐏}`$. To see this we begin with the definition of positive definiteness of a matrix

```math
{𝐱}^{{𝖳}}{𝐏}\,{𝐱} \gt 0
```

for any $`{𝐱}`$, so that if we can factor the (symmetric) covariance matrix in terms of its eigenvectors ($`{𝐄}`$) and eigenvalues ($`{𝚲}`$) we find that

```math
{𝐱}^{{𝖳}}{𝐏}\,{𝐱} = {𝐱}^{{𝖳}}{𝐄}\,{𝚲}\,{𝐄}^{{𝖳}}{𝐱} = {𝐲}^{{𝖳}}{𝚲}\,{𝐲} \gt 0
```

where $`{𝐲} = {𝐄}^{{𝖳}}{𝐱}`$. As well, we can also factor the covariance matrix in terms of its UDU factors as

```math
{𝐱}^{{𝖳}}{𝐏}\,{𝐱} = {𝐱}^{{𝖳}}{𝐔}\,{𝐃}\,{𝐔}^{{𝖳}}{𝐱} = {𝐳}^{{𝖳}}{𝐃}\,{𝐳} \gt 0
```

where $`{𝐳} = {𝐔}^{{𝖳}}{𝐱}`$. Since, in general $`{𝐔} \neq {𝐄}`$, this means that $`{𝐃} \neq {𝚲}`$ and the eigenvalues of $`{𝐏}`$ are not the entries of $`{𝐃}`$. However, since $`{𝐃}`$ is a diagonal matrix, for positive definiteness of the covariance matrix we must have $`d_{ii} \gt 0`$.

This sets the stage for the need for the matrix factorization techniques and the UDU technique in particular.

## 8.2. Preliminaries

<span id="page-95-0"></span>Let us factor a covariance matrix, $`{𝐏}`$, into the following form

```math
{𝐏} = {𝐔}{𝐃}{𝐔}^{{𝖳}} \qquad\qquad(8.1)
```

where $`{𝐔}`$ is a upper triangular matrix with 1's on the diagonals and 0's on the lower portion of the matrix, $`{𝐃}`$ is a diagonal matrix. We can write $`{𝐔}`$ and $`{𝐃}`$ compactly as

<span id="page-95-2"></span>
```math
{𝐔} = \{u_{ij}\}, \qquad i \lt j \qquad\qquad(8.2)
```

```math
{𝐃} = \{d_{ii}\} \qquad\qquad(8.3)
```

as well

```math
u_{ii} = 1 \qquad\qquad(8.4)
```

It should be noted that Eq. [\(8.2\)](#page-95-2) gives the upper triangular portion of the covariance; the lower triangular matrix can be obtained by reflection or by evaluation of Eq. [\(8.2\)](#page-95-2), with $`u_{lm} = 0`$ for $`l \gt m`$.

With this in hand, the off-diagonal elements of $`{𝐏}`$ are

```math
p_{ij} = \sum_{k=j}^{n} u_{ik} d_{kk} u_{jk}, \qquad i \lt j \qquad\qquad(8.5)
```

and for the diagonals we find,

```math
p_{ii} = \sum_{k=j}^{n} u_{ik}^2 d_{kk} \qquad\qquad(8.6)
```

So, given an $`n \times n`$ symmetric, positive semi-definite matrix $`{𝐏}`$, the unit upper triangular factor $`{𝐔}`$ and the diagonal factor $`{𝐃}`$ (such that $`{𝐏} = {𝐔}{𝐃}{𝐔}^{{𝖳}}`$) is obtained using the following equations. We begin with the $`(n, n)`$ element and work upwards (along the columns).

The algorithm is as follows:

> **for** $`j = n : -1 : 2`$ **do**  
> &emsp;$`d_{j,j} = p_{j,j}`$  
> &emsp;*one_over_d* = 0.0  
> &emsp;**if** $`d_{j,j} \gt \epsilon`$ **then**  
> &emsp;&emsp;*one_over_d* = $`1.0/d_{jj}`$  
> &emsp;**else**  
> &emsp;&emsp;$`d_{j,j} = 0.0`$  
> &emsp;**end if**  
> &emsp;$`u_{j,j} = 1.0`$  
> &emsp;**for** $`k = 1 : j-1`$ **do**  
> &emsp;&emsp;$`\beta = p_{k,j}`$  
> &emsp;&emsp;$`u_{k,j} = \beta \cdot {𝑜𝑛𝑒\_𝑜𝑣𝑒𝑟\_𝑑}`$  
> &emsp;&emsp;**for** $`i = 1 : k`$ **do**  
> &emsp;&emsp;&emsp;$`p_{i,k} = p_{i,k} - u_{i,j} \cdot \beta`$  
> &emsp;&emsp;**end for**  
> &emsp;**end for**  
> **end for**

A word of caution: Maybeck [[60](16-bibliography.md#page-172-3)] on page 392, rather uncharacteristically, calls the matrix $`{𝐔}`$ a unitary matrix, ostensibly because there are 1's on the diagonals. Strictly speaking a if $`{𝐔}`$ were a unitary matrix, $`{𝐔}{𝐔}^{{𝖳}} = {𝐔}^{{𝖳}}{𝐔} = {𝐈}`$, which is clearly not the case for the $`{𝐔}`$ in the UDU factorization.

In practice, particularly when storage limitations are driving the design, the $`n \times n`$ matrix $`{𝐃}`$, which is a diagonal matrix comprising of non-zero entries (for a positive definite matrix $`{𝐏}`$), can be stored as a $`n-`$vector. Likewise, the matrix $`n \times n`$ matrix $`{𝐔}`$ which is upper triangular with 1's on the diagonal, can be stored as a $`n(n-1)/2`$ vector. The storage savings can be particularly significant as $`n`$ increases. Of course the algorithms need to be designed to ensure that the entries of $`{𝐔}`$ above the diagonal are the only ones used in the computations.

## 8.3. The Time Update of the Covariance

<span id="page-96-0"></span>As is necessary in Kalman Filtering, we wish to propagate the UDU factorization of the covariance matrix. We loosely follow Maybeck [[60](16-bibliography.md#page-172-3)] in this development. First, we will pose the more general problem and then we will specialize it for navigation problems with a large number of sensor biases.

We begin by expressing the equations for the general time update problem. Next, we specialize the general problem to the case where a subset of states, which we will call 'parameters', whose dynamics are uncorrelated with any other state other than themselves. Finally, we present the arithmetic operation (numbers of adds, multiplies, and divides) of the time update of the covariance matrix.

### 8.3.1. The General Time Update Problem

Given a state, $`{𝐱}`$, that evolves according to

```math
{𝐱}(t_k) = {𝚽}(t_k, t_{k-1}){𝐱}(t_{k-1}) + {𝐆}_k{𝐰}_k
```

where $`{𝐰}_k`$ is the process noise at time $`t_k`$, where $`{𝐱}`$ is an $`n \times 1`$ vector, and $`{𝐰}`$ is an $`m \times 1`$ vector. With this in hand, the general problem is as follows [[82](16-bibliography.md#page-173-10)]: we wish to propagate the covariance matrix defined by

<span id="page-97-0"></span>
```math
\overline{{𝐏}}(t_k) = {𝚽}(t_k, t_{k-1}){𝐏}(t_{k-1}){𝚽}^{{𝖳}}(t_k, t_{k-1}) + {𝐆}_k{𝐐}_k{𝐆}_k^{{𝖳}} \qquad\qquad(8.7)
```

where $`\overline{{𝐏}}`$ is the propagated covariance (the overbar indicates a propagated quantity) and $`{𝐏}`$ is the updated covariance at the prior time step, $`{𝐐}_k`$ is the diagonal process noise covariance matrix and $`{𝐆}_k`$ is the $`n \times m`$ mapping matrix of the noise to the state. To save memory, since $`{𝐐}_k`$ and $`{𝐃}_k`$ are diagonal matrices, in the implementation, we pass $`{𝐐}_k`$ and $`{𝐃}_k`$ as vectors.

We want to find the propagated factors $`{𝐔}_k^-`$ and $`{𝐃}_k^-`$, such that $`{𝐏}_k^- \triangleq {𝐔}_k^-{𝐃}_k^-{𝐔}_k^{-{𝖳}}`$. For compactness, we now drop the time subscripts. Given the UDU factorization of covariance matrices, we can write Eq. [\(8.7\)](#page-97-0) as

<span id="page-97-1"></span>
```math
{𝐔}_k^-{𝐃}_k^-{𝐔}_k^{-{𝖳}} = {𝚽}_k{𝐔}_{k-1}{𝐃}_{k-1}{𝐔}_{k-1}^{{𝖳}}{𝚽}_k^{{𝖳}} + {𝐆}_k{𝐐}_k{𝐆}_k^{{𝖳}} \qquad\qquad(8.8)
```

```math
= \begin{bmatrix} {𝚽}_k{𝐔}_{k-1} & {𝐆}_k \end{bmatrix} \begin{bmatrix} {𝐃}_{k-1} & {𝟎} \\ {𝟎} & {𝐐}_k \end{bmatrix} \begin{bmatrix} {𝚽}_k{𝐔}_{k-1} & {𝐆}_k \end{bmatrix}^{{𝖳}} \qquad\qquad(8.9)
```

Since $`{𝐱}`$ is an $`n \times 1`$ vector, and $`{𝐰}`$ is an $`m \times 1`$ vector, $`{𝚽}_k`$ is an $`n \times n`$ matrix, $`{𝐆}_k`$ is an $`n \times m`$ matrix, and $`{𝐐}_k`$ is an $`m \times m`$ matrix.

We recall that both $`{𝐔}_k^-`$ and $`{𝐔}_{k-1}`$ are $`n \times n`$ upper triangular matrices, with 1's on the diagonal and $`{𝐃}^-`$ and $`{𝐃}`$ are purely diagonal matrices. So, we have some work to do on Eq, [\(8.9\)](#page-97-1) because $`\left[\, {𝚽}_k{𝐔}_{k-1} \;\; {𝐆}_k \,\right]`$ is an $`n \times (n+m)`$ matrix and $`\left[\, \genfrac{}{}{0pt}{}{{𝐃}_{k-1}}{{𝟎}} \;\; \genfrac{}{}{0pt}{}{{𝟎}}{{𝐐}_k} \,\right]`$ is an $`(n+m) \times (n+m)`$ diagonal matrix.

Defining the first matrix ($`\left[\, {𝚽}_k{𝐔}_{k-1} \;\; {𝐆}_k \,\right]`$ which is an $`n \times (n+m)`$ matrix) on the right hand side of Eq.[\(8.9\)](#page-97-1) as

```math
{𝐘} \triangleq \begin{bmatrix} {𝚽}_k{𝐔}_{k-1} & {𝐆}_k \end{bmatrix} \qquad\qquad(8.10)
```

we seek a matrix $`{𝐓}_k`$ that transforms $`{𝐘}_k`$ such that

```math
{𝐘}_k{𝐓}_k^{-{𝖳}} = \begin{bmatrix} {𝐔}_k^- & {𝟎}_{n \times m} \end{bmatrix} \qquad\qquad(8.11)
```

where $`{𝐔}_k^-`$ is an $`n \times n`$ upper triangular matrix with 1's on the diagonal. $`{𝐓}_k`$ is an $`(n+m) \times (n+m)`$ orthogonal matrix with $`(n+m) \times 1`$ basis vectors $`{𝐛}_i`$, $`i = 1, \cdots, n+m`$ as

```math
{𝐓}_k = \begin{bmatrix} {𝐛}_1 & {𝐛}_2 & {𝐛}_3 & \cdots & {𝐛}_n & {𝐛}_{n+1} & \cdots & {𝐛}_{n+m} \end{bmatrix} \qquad\qquad(8.12)
```

In order to find the desired matrix $`{𝐓}_k`$ we perform a modified weighted Gram-Schmidt orthogonalization[<sup>‡</sup>](#page-97-2). We define the diagonal matrix $`\tilde{{𝐃}}_k`$ as

```math
\tilde{{𝐃}}_k \triangleq \begin{bmatrix} {𝐃}_{k-1} & {𝟎} \\ {𝟎} & {𝐐}_k \end{bmatrix} \qquad\qquad(8.13)
```

which will be important as we define the weighted inner product in the Gram-Schmidt Orthogonalization. Eq. [\(8.9\)](#page-97-1) which was

```math
{𝐔}_k^-{𝐃}_k^-{𝐔}_k^{-{𝖳}} = {𝐘}_k\tilde{{𝐃}}_k{𝐘}_k^{{𝖳}} \qquad\qquad(8.14)
```

can now be rewritten as

```math
{𝐔}_k^-{𝐃}_k^-{𝐔}_k^{-{𝖳}} = {𝐘}_k{𝐓}_k^{-{𝖳}}\Bigl[{𝐓}_k^{{𝖳}}\tilde{{𝐃}}_k{𝐓}_k\Bigr]{𝐓}_k^{-1}{𝐘}_k^{{𝖳}} \qquad\qquad(8.15)
```

<span id="page-97-2"></span><sup>‡</sup> Whereas we can use a `qr` factorization, we specifically perform a modified weighted Gram-Schmidt factorization specialized to the UDU factorization on the non-parameter states.

We note that the matrix $`\Bigl[{𝐓}_k^{{𝖳}}\tilde{{𝐃}}_k{𝐓}_k\Bigr]`$ is a diagonal matrix.

"*All*" that remains is to find $`{𝐓}_k`$. This is where we harness the power of the modified Gram-Schmidt orthogonalization process which provides us with what we were after: $`{𝐔}_k^-`$ and $`{𝐃}_k^-`$.

#### 8.3.1.1. The Modified Gram-Schmidt Algorithm

Given the $`n \times (n+m)`$ matrix $`{𝐘}_k = \left[\, {𝚽}_k{𝐔}_{k-1} \;\; {𝐆}_k \,\right]`$, $`{𝚽}_k{𝐔}_{k-1}`$ can be constructed taking advantage of the structure of $`{𝐔}_{k-1}`$ which is an upper triangular matrix with 1's on the diagonal, with $`\frac{1}{2}(n^3 - n^2)`$ adds and $`\frac{1}{2}(n^3 - n^2)`$ multiplies. We recall that $`{𝐘}_k`$ is an $`n \times (n+m)`$ matrix and $`{𝐛}_i`$ are the $`(n+m) \times 1`$ basis vectors. In the following algorithm, the number of adds, multiplies and divides as a consequence of each operation is expressed in terms of '[adds, multiplies, divides]'. We only go to $`j = 2`$ because $`{𝐔}_{11}^- = 1`$. The MGS algorithm can be expressed as:

> **for** $`l = n, \cdots, 2`$ **do**  
> &emsp;$`{𝐛}_l = {𝐘}_l`$  
> **end for**
>
> **for** $`j = n, \cdots, 2`$ **do**  
> &emsp;$`{𝐟}_j = \tilde{{𝐃}}{𝐛}_j`$ &emsp; $`[0, n(n+m), 0]`$  
> &emsp;$`{𝐃}_{jj}^- = {𝐛}_j^{{𝖳}}{𝐟}_j`$ &emsp; $`[n(n+m), n(n+m), 0]`$  
> &emsp;$`{𝐟}_j = {𝐟}_j / {𝐃}_{jj}^-`$ &emsp; $`[0, 0, (n+m)(n-1)]`$  
> &emsp;**for** $`i = 1, \cdots, j-1`$ **do**  
> &emsp;&emsp;$`{𝐔}_{ij}^- = {𝐛}_i^{{𝖳}}{𝐟}_j`$ &emsp; $`\left[(n+m)\frac{(n^2-n)}{2}, (n+m)\frac{(n^2-n)}{2}, 0\right]`$  
> &emsp;&emsp;$`{𝐛}_i = {𝐛}_i - {𝐔}_{ij}^-{𝐛}_j`$ &emsp; $`\left[(n+m)\frac{(n^2-n)}{2}, (n+m)\frac{(n^2-n)}{2}, 0\right]`$  
> &emsp;**end for**  
> &emsp;$`{𝐔}_{11}^- = 1`$  
> &emsp;$`{𝐟}_1 = \tilde{{𝐃}}{𝐛}_1`$  
> &emsp;$`{𝐃}_{11}^- = {𝐛}_1^{{𝖳}}{𝐟}_1`$  
> **end for**

Thus, the algorithm not only provides the orthogonal basis vectors, $`{𝐛}_j`$, $`j = 1, \cdots, n_{{𝐱}}`$, but it also provides the triangular matrix factors $`{𝐔}^-`$ and $`{𝐃}^-`$.

Since we are also interested in the arithmetic operations, we find that there are $`n_{{𝐱}}^3 + n_{{𝐱}}^2 m_{{𝐱}}`$ adds, $`n_{{𝐱}}(n_{{𝐱}}+1)(n_{{𝐱}}+m_{{𝐱}})`$ multiplies and $`(n_{{𝐱}}+m_{{𝐱}})(n_{{𝐱}}-1)`$divides. For the case when $`m_{{𝐱}} = 0`$, i.e. no process noise, we have $`n_{{𝐱}}^3`$ adds and $`n_{{𝐱}}^3 + n_{{𝐱}}^2`$ multiplies and $`n_{{𝐱}}^2 - n_{{𝐱}}`$ divides.

Finally, the entire covariance update algorithm, including the computation of $`{𝐘}_k`$ uses $`1.5n_{{𝐱}}^3 + 0.5n_{{𝐱}}^2(2m_{{𝐱}} - 1)`$ adds, $`0.5n_{{𝐱}}^2(3n_{{𝐱}} + 1) + n_{{𝐱}}m_{{𝐱}}(n_{{𝐱}} + 1)`$ mulitplies and $`(n_{{𝐱}}+m_{{𝐱}})(n_{{𝐱}}-1)`$ divides.

The Modified Gram-Schmidt orthogonalization process makes no assumptions regarding the structure of $`{𝚽}`$. For a large number of states (say, $`n_{{𝐱}} = 35`$ with process noise inputs, $`m_{{𝐱}} = 35`$), most of which might be biases (or Gauss Markov processes), much of this is wasted considering the sparseness of $`{𝚽}`$. In Appendix B.1, we show that we use $`[n_{{𝐱}}^3 + n_{{𝐱}}^2 m_{{𝐱}}]`$ adds and $`[n_{{𝐱}}(n_{{𝐱}}+1)(n_{{𝐱}}+m_{{𝐱}})]`$ multiplies to obtain $`{𝐔}_k^-`$ and $`{𝐃}_k^-`$. For $`n_{{𝐱}} = 35`$ and $`m_{{𝐱}} = 35`$, we require 85,750 adds and 88,200 multiplies – quite a large number of computations. We can stop here and all will be well – if we are willing to pay the heavy computational price.

But we can do better! We can vastly improve (reduce) on the number of computations by partitioning the original state vector into 'states' and 'parameters', where the parameters will be modeled as first-order Gauss-Markov processes. Unlike the parameters, the states can vary in any manner. This motivates the next section.

---

[← Chapter 7. State Representations](07-state-representations.md) · [Contents](README.md) · [Chapter 8. Factorization Methods (part 2 of 3) →](08-factorization-methods-part2.md)
