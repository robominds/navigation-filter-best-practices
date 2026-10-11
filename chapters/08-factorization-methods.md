[← Chapter 7. State Representations](07-state-representations.md) · [Contents](README.md) · [Chapter 9. Attitude Estimation →](09-attitude-estimation.md)

# <span id="page-94-0"></span>Chapter 8. Factorization Methods

*Contributed by Christopher D'Souza*

Of the various covariance factorization methods[<sup>∗</sup>](#page-94-2), the UDU covariance factorization technique is among the most commonly used covariance matrix factorization methodologies used in practice. For example, it is implemented in the Goddard Enhanced Onboard Navigation System (GEONS), which has flown on several robotic missions, and is the heart of the Orion Absolute Navigation System. This chapter is intended to present the UDU triangular factorization method and the rationale for its use.

<span id="page-94-2"></span><sup>∗</sup> Other options include the Square Root Covariance Factorization and the Square Root Information Filter (SRIF).

Above all, we demonstrate that the UDU factorization results in a significant reduction in the arithmetic operations (specifically adds and multiplies) compared with the usual ($\mathbf{P}_{k+1}^- = \boldsymbol{\Phi}(t_k, t_{k+1})\mathbf{P}_k\boldsymbol{\Phi}^{\mathsf{T}}(t_k, t_{k+1}) + \mathbf{Q}_k$) time update and the Joseph measurement update.

In the next section, we present some notational and preliminary operations for the matrix factors $\mathbf{U}$ and $\mathbf{D}$. In the section that follows, we will derive the time update equations for the aforementioned covariance matrix factors. Next, we will derive the measurement update equations for the covariance matrix factors. Finally, we will present some concluding comments.

## 8.1. Why Use the UDU Factorization?

<span id="page-94-1"></span>The usual Kalman filter equations work well for rather simple problems. But once the state-space becomes large, the condition number of the covariance matrix becomes large and nonlinear effects begin to affect the numerical characteristics, problems such as filter divergence and nonpositive definiteness of the covariance matrix occur. These issues began to be observed almost as soon as Kalman filters began to be used in real problems. Matrix factorization techniques were introduced to solve (at least) some of these issues. The earliest was the Potter Square Root Factorization, which was used in the on-board Apollo navigation filters.

In fact Bierman and Thornton, in a 1976 JPL Report, rather cheekily compare those who insist on using the conventional Kalman filtering and batch least-squares algorithms (*contra* the matrix factorization algorithms) to unrepentant smokers by describing "*an attitude often encountered among estimation practitioners [is] that they will switch to the more accurate and stable algorithms if and when numerical problems occur. An analogy comes to mind of a smoker who promises to stop when cancer or heart ailment symptoms are detected. To expand on the analogy, one may note the following:*

- *Most smokers do not get cancer or heart disease. (Most applications of the Kalman algorithms work.)*
- *Even when catastrophic illness does not occur, there is diminished health. (Even when algorithms work, performance may be degraded.)*
- *Smokers can take precautions to lessen the danger, such as smoking low tar or filtered cigarettes. (Engineers can scale their variables to reduce the dynamic range or use double-precision arithmetic.)*
- *Lung cancer may not be diagnosed until it is too advanced for treatment. (Numerical problems may not be detected in time to be remedied.)* " [[83](16-bibliography.md#page-173-9)]

In addition, a little advertised, but incredibly useful feature of the UDU factorization is the ability to interrogate for the positive definiteness of the covariance matrix for 'free', because the condition required for positive definiteness of $\mathbf{P}$ is that the entries of $\mathbf{D}$ are positive[<sup>††</sup>](#page-95-1).

<span id="page-95-1"></span><sup>††</sup> The positive definiteness of the covariance matrix, $\mathbf{P}$, can be determined by interrogating the entries of $\mathbf{D}$. It must be noted that the elements of $\mathbf{D}$ are *not* the eigenvalues of $\mathbf{P}$. To see this we begin with the definition of positive definiteness of a matrix

$$
\mathbf{x}^{\mathsf{T}}\mathbf{P}\,\mathbf{x} > 0
$$

for any $\mathbf{x}$, so that if we can factor the (symmetric) covariance matrix in terms of its eigenvectors ($\mathbf{E}$) and eigenvalues ($\boldsymbol{\Lambda}$) we find that

$$
\mathbf{x}^{\mathsf{T}}\mathbf{P}\,\mathbf{x} = \mathbf{x}^{\mathsf{T}}\mathbf{E}\,\boldsymbol{\Lambda}\,\mathbf{E}^{\mathsf{T}}\mathbf{x} = \mathbf{y}^{\mathsf{T}}\boldsymbol{\Lambda}\,\mathbf{y} > 0
$$

where $\mathbf{y} = \mathbf{E}^{\mathsf{T}}\mathbf{x}$. As well, we can also factor the covariance matrix in terms of its UDU factors as

$$
\mathbf{x}^{\mathsf{T}}\mathbf{P}\,\mathbf{x} = \mathbf{x}^{\mathsf{T}}\mathbf{U}\,\mathbf{D}\,\mathbf{U}^{\mathsf{T}}\mathbf{x} = \mathbf{z}^{\mathsf{T}}\mathbf{D}\,\mathbf{z} > 0
$$

where $\mathbf{z} = \mathbf{U}^{\mathsf{T}}\mathbf{x}$. Since, in general $\mathbf{U} \neq \mathbf{E}$, this means that $\mathbf{D} \neq \boldsymbol{\Lambda}$ and the eigenvalues of $\mathbf{P}$ are not the entries of $\mathbf{D}$. However, since $\mathbf{D}$ is a diagonal matrix, for positive definiteness of the covariance matrix we must have $d_{ii} > 0$.

This sets the stage for the need for the matrix factorization techniques and the UDU technique in particular.

## 8.2. Preliminaries

<span id="page-95-0"></span>Let us factor a covariance matrix, $\mathbf{P}$, into the following form

$$
\mathbf{P} = \mathbf{U}\mathbf{D}\mathbf{U}^{\mathsf{T}} \tag{8.1}
$$

where $\mathbf{U}$ is a upper triangular matrix with 1's on the diagonals and 0's on the lower portion of the matrix, $\mathbf{D}$ is a diagonal matrix. We can write $\mathbf{U}$ and $\mathbf{D}$ compactly as

<span id="page-95-2"></span>
$$
\mathbf{U} = \{u_{ij}\}, \qquad i < j \tag{8.2}
$$

$$
\mathbf{D} = \{d_{ii}\} \tag{8.3}
$$

as well

$$
u_{ii} = 1 \tag{8.4}
$$

It should be noted that Eq. [\(8.2\)](#page-95-2) gives the upper triangular portion of the covariance; the lower triangular matrix can be obtained by reflection or by evaluation of Eq. [\(8.2\)](#page-95-2), with $u_{lm} = 0$ for $l > m$.

With this in hand, the off-diagonal elements of $\mathbf{P}$ are

$$
p_{ij} = \sum_{k=j}^{n} u_{ik} d_{kk} u_{jk}, \qquad i < j \tag{8.5}
$$

and for the diagonals we find,

$$
p_{ii} = \sum_{k=j}^{n} u_{ik}^2 d_{kk} \tag{8.6}
$$

So, given an $n \times n$ symmetric, positive semi-definite matrix $\mathbf{P}$, the unit upper triangular factor $\mathbf{U}$ and the diagonal factor $\mathbf{D}$ (such that $\mathbf{P} = \mathbf{U}\mathbf{D}\mathbf{U}^{\mathsf{T}}$) is obtained using the following equations. We begin with the $(n, n)$ element and work upwards (along the columns).

The algorithm is as follows:

> **for** $j = n : -1 : 2$ **do**  
> &emsp;$d_{j,j} = p_{j,j}$  
> &emsp;*one_over_d* = 0.0  
> &emsp;**if** $d_{j,j} > \epsilon$ **then**  
> &emsp;&emsp;*one_over_d* = $1.0/d_{jj}$  
> &emsp;**else**  
> &emsp;&emsp;$d_{j,j} = 0.0$  
> &emsp;**end if**  
> &emsp;$u_{j,j} = 1.0$  
> &emsp;**for** $k = 1 : j-1$ **do**  
> &emsp;&emsp;$\beta = p_{k,j}$  
> &emsp;&emsp;$u_{k,j} = \beta \cdot \mathit{one\_over\_d}$  
> &emsp;&emsp;**for** $i = 1 : k$ **do**  
> &emsp;&emsp;&emsp;$p_{i,k} = p_{i,k} - u_{i,j} \cdot \beta$  
> &emsp;&emsp;**end for**  
> &emsp;**end for**  
> **end for**

A word of caution: Maybeck [[60](16-bibliography.md#page-172-3)] on page 392, rather uncharacteristically, calls the matrix $\mathbf{U}$ a unitary matrix, ostensibly because there are 1's on the diagonals. Strictly speaking a if $\mathbf{U}$ were a unitary matrix, $\mathbf{U}\mathbf{U}^{\mathsf{T}} = \mathbf{U}^{\mathsf{T}}\mathbf{U} = \mathbf{I}$, which is clearly not the case for the $\mathbf{U}$ in the UDU factorization.

In practice, particularly when storage limitations are driving the design, the $n \times n$ matrix $\mathbf{D}$, which is a diagonal matrix comprising of non-zero entries (for a positive definite matrix $\mathbf{P}$), can be stored as a $n-$vector. Likewise, the matrix $n \times n$ matrix $\mathbf{U}$ which is upper triangular with 1's on the diagonal, can be stored as a $n(n-1)/2$ vector. The storage savings can be particularly significant as $n$ increases. Of course the algorithms need to be designed to ensure that the entries of $\mathbf{U}$ above the diagonal are the only ones used in the computations.

## 8.3. The Time Update of the Covariance

<span id="page-96-0"></span>As is necessary in Kalman Filtering, we wish to propagate the UDU factorization of the covariance matrix. We loosely follow Maybeck [[60](16-bibliography.md#page-172-3)] in this development. First, we will pose the more general problem and then we will specialize it for navigation problems with a large number of sensor biases.

We begin by expressing the equations for the general time update problem. Next, we specialize the general problem to the case where a subset of states, which we will call 'parameters', whose dynamics are uncorrelated with any other state other than themselves. Finally, we present the arithmetic operation (numbers of adds, multiplies, and divides) of the time update of the covariance matrix.

### 8.3.1. The General Time Update Problem

Given a state, $\mathbf{x}$, that evolves according to

$$
\mathbf{x}(t_k) = \boldsymbol{\Phi}(t_k, t_{k-1})\mathbf{x}(t_{k-1}) + \mathbf{G}_k\mathbf{w}_k
$$

where $\mathbf{w}_k$ is the process noise at time $t_k$, where $\mathbf{x}$ is an $n \times 1$ vector, and $\mathbf{w}$ is an $m \times 1$ vector. With this in hand, the general problem is as follows [[82](16-bibliography.md#page-173-10)]: we wish to propagate the covariance matrix defined by

<span id="page-97-0"></span>
$$
\overline{\mathbf{P}}(t_k) = \boldsymbol{\Phi}(t_k, t_{k-1})\mathbf{P}(t_{k-1})\boldsymbol{\Phi}^{\mathsf{T}}(t_k, t_{k-1}) + \mathbf{G}_k\mathbf{Q}_k\mathbf{G}_k^{\mathsf{T}} \tag{8.7}
$$

where $\overline{\mathbf{P}}$ is the propagated covariance (the overbar indicates a propagated quantity) and $\mathbf{P}$ is the updated covariance at the prior time step, $\mathbf{Q}_k$ is the diagonal process noise covariance matrix and $\mathbf{G}_k$ is the $n \times m$ mapping matrix of the noise to the state. To save memory, since $\mathbf{Q}_k$ and $\mathbf{D}_k$ are diagonal matrices, in the implementation, we pass $\mathbf{Q}_k$ and $\mathbf{D}_k$ as vectors.

We want to find the propagated factors $\mathbf{U}_k^-$ and $\mathbf{D}_k^-$, such that $\mathbf{P}_k^- \triangleq \mathbf{U}_k^-\mathbf{D}_k^-\mathbf{U}_k^{-\mathsf{T}}$. For compactness, we now drop the time subscripts. Given the UDU factorization of covariance matrices, we can write Eq. [\(8.7\)](#page-97-0) as

<span id="page-97-1"></span>
$$
\mathbf{U}_k^-\mathbf{D}_k^-\mathbf{U}_k^{-\mathsf{T}} = \boldsymbol{\Phi}_k\mathbf{U}_{k-1}\mathbf{D}_{k-1}\mathbf{U}_{k-1}^{\mathsf{T}}\boldsymbol{\Phi}_k^{\mathsf{T}} + \mathbf{G}_k\mathbf{Q}_k\mathbf{G}_k^{\mathsf{T}} \tag{8.8}
$$

$$
= \begin{bmatrix} \boldsymbol{\Phi}_k\mathbf{U}_{k-1} & \mathbf{G}_k \end{bmatrix} \begin{bmatrix} \mathbf{D}_{k-1} & \mathbf{0} \\ \mathbf{0} & \mathbf{Q}_k \end{bmatrix} \begin{bmatrix} \boldsymbol{\Phi}_k\mathbf{U}_{k-1} & \mathbf{G}_k \end{bmatrix}^{\mathsf{T}} \tag{8.9}
$$

Since $\mathbf{x}$ is an $n \times 1$ vector, and $\mathbf{w}$ is an $m \times 1$ vector, $\boldsymbol{\Phi}_k$ is an $n \times n$ matrix, $\mathbf{G}_k$ is an $n \times m$ matrix, and $\mathbf{Q}_k$ is an $m \times m$ matrix.

We recall that both $\mathbf{U}_k^-$ and $\mathbf{U}_{k-1}$ are $n \times n$ upper triangular matrices, with 1's on the diagonal and $\mathbf{D}^-$ and $\mathbf{D}$ are purely diagonal matrices. So, we have some work to do on Eq, [\(8.9\)](#page-97-1) because $\begin{bmatrix} \boldsymbol{\Phi}_k\mathbf{U}_{k-1} & \mathbf{G}_k \end{bmatrix}$ is an $n \times (n+m)$ matrix and $\begin{bmatrix} \mathbf{D}_{k-1} & \mathbf{0} \\ \mathbf{0} & \mathbf{Q}_k \end{bmatrix}$ is an $(n+m) \times (n+m)$ diagonal matrix.

Defining the first matrix ($\begin{bmatrix} \boldsymbol{\Phi}_k\mathbf{U}_{k-1} & \mathbf{G}_k \end{bmatrix}$ which is an $n \times (n+m)$ matrix) on the right hand side of Eq.[\(8.9\)](#page-97-1) as

$$
\mathbf{Y} \triangleq \begin{bmatrix} \boldsymbol{\Phi}_k\mathbf{U}_{k-1} & \mathbf{G}_k \end{bmatrix} \tag{8.10}
$$

we seek a matrix $\mathbf{T}_k$ that transforms $\mathbf{Y}_k$ such that

$$
\mathbf{Y}_k\mathbf{T}_k^{-\mathsf{T}} = \begin{bmatrix} \mathbf{U}_k^- & \mathbf{0}_{n \times m} \end{bmatrix} \tag{8.11}
$$

where $\mathbf{U}_k^-$ is an $n \times n$ upper triangular matrix with 1's on the diagonal. $\mathbf{T}_k$ is an $(n+m) \times (n+m)$ orthogonal matrix with $(n+m) \times 1$ basis vectors $\mathbf{b}_i$, $i = 1, \cdots, n+m$ as

$$
\mathbf{T}_k = \begin{bmatrix} \mathbf{b}_1 & \mathbf{b}_2 & \mathbf{b}_3 & \cdots & \mathbf{b}_n & \mathbf{b}_{n+1} & \cdots & \mathbf{b}_{n+m} \end{bmatrix} \tag{8.12}
$$

In order to find the desired matrix $\mathbf{T}_k$ we perform a modified weighted Gram-Schmidt orthogonalization[<sup>‡</sup>](#page-97-2). We define the diagonal matrix $\widetilde{\mathbf{D}}_k$ as

$$
\widetilde{\mathbf{D}}_k \triangleq \begin{bmatrix} \mathbf{D}_{k-1} & \mathbf{0} \\ \mathbf{0} & \mathbf{Q}_k \end{bmatrix} \tag{8.13}
$$

which will be important as we define the weighted inner product in the Gram-Schmidt Orthogonalization. Eq. [\(8.9\)](#page-97-1) which was

$$
\mathbf{U}_k^-\mathbf{D}_k^-\mathbf{U}_k^{-\mathsf{T}} = \mathbf{Y}_k\widetilde{\mathbf{D}}_k\mathbf{Y}_k^{\mathsf{T}} \tag{8.14}
$$

can now be rewritten as

$$
\mathbf{U}_k^-\mathbf{D}_k^-\mathbf{U}_k^{-\mathsf{T}} = \mathbf{Y}_k\mathbf{T}_k^{-\mathsf{T}}\left[\mathbf{T}_k^{\mathsf{T}}\widetilde{\mathbf{D}}_k\mathbf{T}_k\right]\mathbf{T}_k^{-1}\mathbf{Y}_k^{\mathsf{T}} \tag{8.15}
$$

<span id="page-97-2"></span><sup>‡</sup> Whereas we can use a `qr` factorization, we specifically perform a modified weighted Gram-Schmidt factorization specialized to the UDU factorization on the non-parameter states.

We note that the matrix $\left[\mathbf{T}_k^{\mathsf{T}}\widetilde{\mathbf{D}}_k\mathbf{T}_k\right]$ is a diagonal matrix.

"*All*" that remains is to find $\mathbf{T}_k$. This is where we harness the power of the modified Gram-Schmidt orthogonalization process which provides us with what we were after: $\mathbf{U}_k^-$ and $\mathbf{D}_k^-$.

#### 8.3.1.1. The Modified Gram-Schmidt Algorithm

Given the $n \times (n+m)$ matrix $\mathbf{Y}_k = \begin{bmatrix} \boldsymbol{\Phi}_k\mathbf{U}_{k-1} & \mathbf{G}_k \end{bmatrix}$, $\boldsymbol{\Phi}_k\mathbf{U}_{k-1}$ can be constructed taking advantage of the structure of $\mathbf{U}_{k-1}$ which is an upper triangular matrix with 1's on the diagonal, with $\frac{1}{2}(n^3 - n^2)$ adds and $\frac{1}{2}(n^3 - n^2)$ multiplies. We recall that $\mathbf{Y}_k$ is an $n \times (n+m)$ matrix and $\mathbf{b}_i$ are the $(n+m) \times 1$ basis vectors. In the following algorithm, the number of adds, multiplies and divides as a consequence of each operation is expressed in terms of '[adds, multiplies, divides]'. We only go to $j = 2$ because $\mathbf{U}_{11}^- = 1$. The MGS algorithm can be expressed as:

> **for** $l = n, \cdots, 2$ **do**  
> &emsp;$\mathbf{b}_l = \mathbf{Y}_l$  
> **end for**
>
> **for** $j = n, \cdots, 2$ **do**  
> &emsp;$\mathbf{f}_j = \widetilde{\mathbf{D}}\mathbf{b}_j$ &emsp; $[0, n(n+m), 0]$  
> &emsp;$\mathbf{D}_{jj}^- = \mathbf{b}_j^{\mathsf{T}}\mathbf{f}_j$ &emsp; $[n(n+m), n(n+m), 0]$  
> &emsp;$\mathbf{f}_j = \mathbf{f}_j / \mathbf{D}_{jj}^-$ &emsp; $[0, 0, (n+m)(n-1)]$  
> &emsp;**for** $i = 1, \cdots, j-1$ **do**  
> &emsp;&emsp;$\mathbf{U}_{ij}^- = \mathbf{b}_i^{\mathsf{T}}\mathbf{f}_j$ &emsp; $\left[(n+m)\frac{(n^2-n)}{2}, (n+m)\frac{(n^2-n)}{2}, 0\right]$  
> &emsp;&emsp;$\mathbf{b}_i = \mathbf{b}_i - \mathbf{U}_{ij}^-\mathbf{b}_j$ &emsp; $\left[(n+m)\frac{(n^2-n)}{2}, (n+m)\frac{(n^2-n)}{2}, 0\right]$  
> &emsp;**end for**  
> &emsp;$\mathbf{U}_{11}^- = 1$  
> &emsp;$\mathbf{f}_1 = \widetilde{\mathbf{D}}\mathbf{b}_1$  
> &emsp;$\mathbf{D}_{11}^- = \mathbf{b}_1^{\mathsf{T}}\mathbf{f}_1$  
> **end for**

Thus, the algorithm not only provides the orthogonal basis vectors, $\mathbf{b}_j$, $j = 1, \cdots, n_{\mathbf{x}}$, but it also provides the triangular matrix factors $\mathbf{U}^-$ and $\mathbf{D}^-$.

Since we are also interested in the arithmetic operations, we find that there are $n_{\mathbf{x}}^3 + n_{\mathbf{x}}^2 m_{\mathbf{x}}$ adds, $n_{\mathbf{x}}(n_{\mathbf{x}}+1)(n_{\mathbf{x}}+m_{\mathbf{x}})$ multiplies and $(n_{\mathbf{x}}+m_{\mathbf{x}})(n_{\mathbf{x}}-1)$divides. For the case when $m_{\mathbf{x}} = 0$, i.e. no process noise, we have $n_{\mathbf{x}}^3$ adds and $n_{\mathbf{x}}^3 + n_{\mathbf{x}}^2$ multiplies and $n_{\mathbf{x}}^2 - n_{\mathbf{x}}$ divides.

Finally, the entire covariance update algorithm, including the computation of $\mathbf{Y}_k$ uses $1.5n_{\mathbf{x}}^3 + 0.5n_{\mathbf{x}}^2(2m_{\mathbf{x}} - 1)$ adds, $0.5n_{\mathbf{x}}^2(3n_{\mathbf{x}} + 1) + n_{\mathbf{x}}m_{\mathbf{x}}(n_{\mathbf{x}} + 1)$ mulitplies and $(n_{\mathbf{x}}+m_{\mathbf{x}})(n_{\mathbf{x}}-1)$ divides.

The Modified Gram-Schmidt orthogonalization process makes no assumptions regarding the structure of $\boldsymbol{\Phi}$. For a large number of states (say, $n_{\mathbf{x}} = 35$ with process noise inputs, $m_{\mathbf{x}} = 35$), most of which might be biases (or Gauss Markov processes), much of this is wasted considering the sparseness of $\boldsymbol{\Phi}$. In Appendix B.1, we show that we use $[n_{\mathbf{x}}^3 + n_{\mathbf{x}}^2 m_{\mathbf{x}}]$ adds and $[n_{\mathbf{x}}(n_{\mathbf{x}}+1)(n_{\mathbf{x}}+m_{\mathbf{x}})]$ multiplies to obtain $\mathbf{U}_k^-$ and $\mathbf{D}_k^-$. For $n_{\mathbf{x}} = 35$ and $m_{\mathbf{x}} = 35$, we require 85,750 adds and 88,200 multiplies – quite a large number of computations. We can stop here and all will be well – if we are willing to pay the heavy computational price.

But we can do better! We can vastly improve (reduce) on the number of computations by partitioning the original state vector into 'states' and 'parameters', where the parameters will be modeled as first-order Gauss-Markov processes. Unlike the parameters, the states can vary in any manner. This motivates the next section.

### 8.3.2. An Improvement for the Case of Parameters

As stated earlier, for a large number of states (say, $n_{\mathbf{x}} = 35$), the UDU time update for the full covariance matrix (à la Gram-Schmidt orthogonalization) is computationally expensive, requiring $2n_{\mathbf{x}}^3 + 2n_{\mathbf{x}}^2$ multiplies and additions. This is not competitive with the "standard" ($\mathbf{P}_{k+1}^- = \boldsymbol{\Phi}(t_k, t_{k+1})\mathbf{P}_k^+\boldsymbol{\Phi}^{\mathsf{T}}(t_k, t_{k+1}) + \mathbf{G}_k\mathbf{Q}_k\mathbf{G}_k^{\mathsf{T}}$) formulation (which uses $2n_{\mathbf{x}}^3$ multiplies). However, one might guess that an improvement can be made. This is particularly significant because, normally, most of the states are biases or ECRVs (Exponentially Correlated Random Variables) or first-order Gauss-Markov processes. In order to generalize the development, we assume ECRVs for the 'parameter' (or bias) states.

For most space-borne navigation applications, we can usually partition the states into position, velocity, attitude (if applicable) and clock states, all of which we group together and denote as $\mathbf{x}$, and parameter states which usually comprise the sensor biases, scale factors, *etc.*, which we denote as $\mathbf{p}$. This means that the full state space is

$$
\mathcal{X} = \begin{bmatrix} \mathbf{x} \\ \mathbf{p} \end{bmatrix} \tag{8.16}
$$

The 'states' partition must comprise all those quantities whose time evolution cannot be described as purely self-auto correlated processes. With this in hand, we partition $\mathbf{U}$ and $\mathbf{D}$ as

$$
\mathbf{U} = \begin{bmatrix} \mathbf{U}_{\mathbf{xx}} & \mathbf{U}_{\mathbf{xp}} \\ \mathbf{0} & \mathbf{U}_{\mathbf{pp}} \end{bmatrix} \qquad \mathbf{D} = \begin{bmatrix} \mathbf{D}_{\mathbf{xx}} & \mathbf{0} \\ \mathbf{0} & \mathbf{D}_{\mathbf{pp}} \end{bmatrix} \tag{8.17}
$$

Also, partition $\boldsymbol{\Phi}_k$ according to

$$
\boldsymbol{\Phi}(t_{k+1}, t_k) = \boldsymbol{\Phi}_k = \begin{bmatrix} \boldsymbol{\Phi}_{\mathbf{xx}_k} & \boldsymbol{\Phi}_{\mathbf{xp}_k} \\ \mathbf{0} & \mathbf{M} \end{bmatrix} = \begin{bmatrix} \mathbf{I} & \mathbf{0} \\ \mathbf{0} & \mathbf{M} \end{bmatrix} \begin{bmatrix} \boldsymbol{\Phi}_{\mathbf{xx}_k} & \boldsymbol{\Phi}_{\mathbf{xp}_k} \\ \mathbf{0} & \mathbf{I} \end{bmatrix} = \boldsymbol{\Phi}_{2_k}\boldsymbol{\Phi}_{1_k} \tag{8.18}
$$

where $\mathbf{M}$ is a diagonal matrix, representing an ECRV whose propagation for $p_k$ is

$$
p_k^- = e^{-\Delta t/\tau} p_{k-1}^+ \tag{8.19}
$$

so that

$$
\mathbf{M}(i, i) = m_i = e^{-\Delta t/\tau_i} \tag{8.20}
$$

where $\tau_i$ is the time constant of the $i^{\text{th}}$ ECRV state.

Likewise $\mathbf{Q}_k$ is partitioned according to

$$
\begin{aligned}
\mathbf{Q}_k &= \begin{bmatrix} \mathbf{G}_{\mathbf{xx}_k}\mathbf{Q}_{\mathbf{xx}_k}\mathbf{G}_{\mathbf{xx}_k}^{\mathsf{T}} & \mathbf{0} \\ \mathbf{0} & \mathbf{Q}_{\mathbf{pp}_k} \end{bmatrix} = \begin{bmatrix} \mathbf{G}_{\mathbf{xx}_k}\mathbf{Q}_{\mathbf{xx}_k}\mathbf{G}_{\mathbf{xx}_k}^{\mathsf{T}} & \mathbf{0} \\ \mathbf{0} & \mathbf{0} \end{bmatrix} + \begin{bmatrix} \mathbf{0} & \mathbf{0} \\ \mathbf{0} & \mathbf{Q}_{\mathbf{pp}_k} \end{bmatrix} \\
&= \mathbf{Q}_{1_k} + \mathbf{Q}_{2_k}
\end{aligned} \tag{8.21}
$$

where we assume that the parameters are ECRVs and hence $\mathbf{Q}_{\mathbf{pp}}$ is a diagonal matrix.

Recall that the original propagation equation was

$$
\mathbf{U}_{k+1}^-\mathbf{D}_{k+1}^-\mathbf{U}_{k+1}^{-\mathsf{T}} = \boldsymbol{\Phi}_k\mathbf{U}_k^+\mathbf{D}_k^+\mathbf{U}_k^{+\mathsf{T}}\boldsymbol{\Phi}_k^{\mathsf{T}} + \mathbf{G}_k\mathbf{Q}_k\mathbf{G}_k^{\mathsf{T}} \tag{8.22}
$$

Harnessing the development in Appendix [B.1,](14-appendix-b-the-mathematics-behind-the-udu-factorization.md#page-148-1) $\mathbf{U}_{k+1}^-\mathbf{D}_{k+1}^-\mathbf{U}_{k+1}^{-\mathsf{T}}$ becomes

$$
\mathbf{U}_{k+1}^-\mathbf{D}_{k+1}^-\mathbf{U}_{k+1}^{-\mathsf{T}} = \boldsymbol{\Phi}_{2_k}\left[\boldsymbol{\Phi}_{1_k}\mathbf{U}_k^+\mathbf{D}_k^+\mathbf{U}_k^{+\mathsf{T}}\boldsymbol{\Phi}_{1_k}^{\mathsf{T}} + \mathbf{Q}_{1_k}\right]\boldsymbol{\Phi}_{2_k}^{\mathsf{T}} + \mathbf{Q}_{2_k} \tag{8.23}
$$

This suggests the following two-step process:

1) Find $\widetilde{\mathbf{U}}$ and $\widetilde{\mathbf{D}}$ from

<span id="page-100-0"></span>
$$
\widetilde{\mathbf{U}}_k\widetilde{\mathbf{D}}_k\widetilde{\mathbf{U}}_k^{\mathsf{T}} = \boldsymbol{\Phi}_{1_k}\mathbf{U}_k^+\mathbf{D}_k^+\mathbf{U}_k^{+\mathsf{T}}\boldsymbol{\Phi}_{1_k}^{\mathsf{T}} + \mathbf{Q}_{1_k} \tag{8.24}
$$

2) Find $\mathbf{U}_{k+1}^-$ and $\mathbf{D}_{k+1}^-$ from

<span id="page-100-5"></span>
$$
\mathbf{U}_{k+1}^-\mathbf{D}_{k+1}^-\mathbf{U}_{k+1}^{-\mathsf{T}} = \boldsymbol{\Phi}_{2_k}\widetilde{\mathbf{U}}_k\widetilde{\mathbf{D}}_k\widetilde{\mathbf{U}}_k^{\mathsf{T}}\boldsymbol{\Phi}_{2_k}^{\mathsf{T}} + \mathbf{Q}_{2_k} \tag{8.25}
$$

The following sub-sections will describe each of these steps.

#### 8.3.2.1. The First Sub-Problem ($\boldsymbol{\Phi}_{1_k}\mathbf{U}_k^+\mathbf{D}_k^+\mathbf{U}_k^{+\mathsf{T}}\boldsymbol{\Phi}_{1_k}^{\mathsf{T}} + \mathbf{Q}_{1_k}$)

Lets look at 1). The left hand side of Eq. [\(8.24\)](#page-100-0) is

<span id="page-100-1"></span>
$$
\widetilde{\mathbf{U}}_k\widetilde{\mathbf{D}}_k\widetilde{\mathbf{U}}_k^{\mathsf{T}} = \begin{bmatrix} \widetilde{\mathbf{U}}_{\mathbf{xx}_k}\widetilde{\mathbf{D}}_{\mathbf{xx}_k}\widetilde{\mathbf{U}}_{\mathbf{xx}_k}^{\mathsf{T}} + \widetilde{\mathbf{U}}_{\mathbf{xp}_k}\widetilde{\mathbf{D}}_{\mathbf{pp}_k}\widetilde{\mathbf{U}}_{\mathbf{xp}_k}^{\mathsf{T}} & \widetilde{\mathbf{U}}_{\mathbf{xp}_k}\widetilde{\mathbf{D}}_{\mathbf{pp}_k}\widetilde{\mathbf{U}}_{\mathbf{pp}_k}^{\mathsf{T}} \\ \widetilde{\mathbf{U}}_{\mathbf{pp}_k}\widetilde{\mathbf{D}}_{\mathbf{pp}_k}\widetilde{\mathbf{U}}_{\mathbf{xp}_k}^{\mathsf{T}} & \widetilde{\mathbf{U}}_{\mathbf{pp}_k}\widetilde{\mathbf{D}}_{\mathbf{pp}_k}\widetilde{\mathbf{U}}_{\mathbf{pp}_k}^{\mathsf{T}} \end{bmatrix} \tag{8.26}
$$

The right hand side of Eq. [\(8.24\)](#page-100-0) is

<span id="page-100-2"></span>
$$
\widetilde{\mathbf{U}}_k\widetilde{\mathbf{D}}_k\widetilde{\mathbf{U}}_k^{\mathsf{T}} = \left[\begin{array}{c|c}
\boldsymbol{\Phi}_{\mathbf{xx}_k}\Big(\mathbf{U}_{\mathbf{xx}_k}^+\mathbf{D}_{\mathbf{xx}}^+\mathbf{U}_{\mathbf{xx}_k}^{+\mathsf{T}} + \mathbf{U}_{\mathbf{xp}_k}^+\mathbf{D}_{\mathbf{pp}_k}^+\mathbf{U}_{\mathbf{xp}_k}^{+\mathsf{T}}\Big)\boldsymbol{\Phi}_{\mathbf{xx}_k}^{\mathsf{T}} & \boldsymbol{\Phi}_{\mathbf{xx}_k}\mathbf{U}_{\mathbf{xp}_k}^+\mathbf{D}_{\mathbf{pp}_k}^+\mathbf{U}_{\mathbf{pp}_k}^{+\mathsf{T}} \\
+\boldsymbol{\Phi}_{\mathbf{xx}_k}\mathbf{U}_{\mathbf{xp}_k}^+\mathbf{D}_{\mathbf{pp}_k}^+\mathbf{U}_{\mathbf{pp}_k}^{+\mathsf{T}}\boldsymbol{\Phi}_{\mathbf{xp}_k}^{\mathsf{T}} & +\boldsymbol{\Phi}_{\mathbf{xp}_k}\mathbf{U}_{\mathbf{pp}_k}^+\mathbf{D}_{\mathbf{pp}_k}^+\mathbf{U}_{\mathbf{pp}_k}^{+\mathsf{T}} \\
+\boldsymbol{\Phi}_{\mathbf{xp}_k}\mathbf{U}_{\mathbf{pp}_k}^+\mathbf{D}_{\mathbf{pp}_k}^+\mathbf{U}_{\mathbf{xp}_k}^{+\mathsf{T}}\boldsymbol{\Phi}_{\mathbf{xx}_k}^{\mathsf{T}} & \\
+\boldsymbol{\Phi}_{\mathbf{xp}_k}\mathbf{U}_{\mathbf{pp}_k}^+\mathbf{D}_{\mathbf{pp}_k}^+\mathbf{U}_{\mathbf{pp}_k}^{+\mathsf{T}}\boldsymbol{\Phi}_{\mathbf{xp}_k}^{\mathsf{T}} + \mathbf{Q}_{\mathbf{xx}_k} & \\
\hline
\mathbf{U}_{\mathbf{pp}_k}^+\mathbf{D}_{\mathbf{pp}_k}^+\mathbf{U}_{\mathbf{xp}_k}^{+\mathsf{T}}\boldsymbol{\Phi}_{\mathbf{xx}_k}^{\mathsf{T}} + \mathbf{U}_{\mathbf{pp}_k}^+\mathbf{D}_{\mathbf{pp}_k}^+\mathbf{U}_{\mathbf{pp}_k}^{+\mathsf{T}}\boldsymbol{\Phi}_{\mathbf{xp}_k}^{\mathsf{T}} & \mathbf{U}_{\mathbf{pp}_k}^+\mathbf{D}_{\mathbf{pp}_k}^+\mathbf{U}_{\mathbf{pp}_k}^{+\mathsf{T}}
\end{array}\right] \tag{8.27}
$$

Equating each component of the matrix in Eqs [\(8.26\)](#page-100-1) and [\(8.27\)](#page-100-2), we find that the $(2, 2)$ component yields

<span id="page-100-3"></span>
$$
\widetilde{\mathbf{U}}_{\mathbf{pp}_k} = \mathbf{U}_{\mathbf{pp}_k}^+ \tag{8.28}
$$

$$
\widetilde{\mathbf{D}}_{\mathbf{pp}_k} = \mathbf{D}_{\mathbf{pp}_k}^+ \tag{8.29}
$$

Equating the $(1, 2)$ (or $(2, 1)$) component yields

<span id="page-100-4"></span>
$$
\widetilde{\mathbf{U}}_{\mathbf{xp}_k} = \boldsymbol{\Phi}_{\mathbf{xx}_k}\mathbf{U}_{\mathbf{xp}_k}^+ + \boldsymbol{\Phi}_{\mathbf{xp}_k}\mathbf{U}_{\mathbf{pp}_k}^+ \tag{8.30}
$$

Finally, equating the $(1, 1)$ components of Eqs. [\(8.26\)](#page-100-1) and [\(8.27\)](#page-100-2), and using Eqs. [\(8.28\)](#page-100-3), [\(8.29\)](#page-100-3) and [\(8.30\)](#page-100-4), we find that

$$
\widetilde{\mathbf{U}}_{\mathbf{xx}_k}\widetilde{\mathbf{D}}_{\mathbf{xx}_k}\widetilde{\mathbf{U}}_{\mathbf{xx}_k}^{\mathsf{T}} = \boldsymbol{\Phi}_{\mathbf{xx}_k}\mathbf{U}_{\mathbf{xx}_k}^+\mathbf{D}_{\mathbf{xx}_k}^+\mathbf{U}_{\mathbf{xx}_k}^{+\mathsf{T}}\boldsymbol{\Phi}_{\mathbf{xx}_k}^{\mathsf{T}} + \mathbf{Q}_{\mathbf{xx}_k} \tag{8.31}
$$

Since we have partitioned the states such that $\mathbf{x}$ comprises the position, velocity, attitude and clock states (or others, as appropriate), we use the ***modified* Gram-Schmidt algorithm** to update $\widetilde{\mathbf{U}}_{\mathbf{xx}_k}$ and $\widetilde{\mathbf{D}}_{\mathbf{xx}_k}$. And then we compute $\widetilde{\mathbf{U}}_{\mathbf{pp}_k}$, $\widetilde{\mathbf{D}}_{\mathbf{pp}_k}$ and $\widetilde{\mathbf{U}}_{\mathbf{xp}_k}$ according to Eqs. [\(8.28\)](#page-100-3) - [\(8.30\)](#page-100-4).

Thus, given $n_{\mathbf{x}}$ states with $m_{\mathbf{x}}$ process noise parameters associated with those states, the number of computations associated with the the first sub-problem is: $[1.5n_{\mathbf{x}}^3 + 0.5n_{\mathbf{x}}^2(2m_{\mathbf{x}} - 1)]$ adds, $[0.5n_{\mathbf{x}}^2(3n_{\mathbf{x}} + 1) + n_{\mathbf{x}}m_{\mathbf{x}}(n_{\mathbf{x}} + 1)]$ multiplies, and $[(n_{\mathbf{x}} + m_{\mathbf{x}})(n_{\mathbf{x}} - 1)]$ divides.

#### 8.3.2.2. The Second Sub-Problem ($\boldsymbol{\Phi}_{2_k}\widetilde{\mathbf{U}}_k\widetilde{\mathbf{D}}_k\widetilde{\mathbf{U}}_k^{\mathsf{T}}\boldsymbol{\Phi}_{2_k}^{\mathsf{T}} + \mathbf{Q}_{2_k}$)

Now we look at 2). We now partition $\widetilde{\mathbf{U}}_k$ and $\widetilde{\mathbf{D}}_k$ as

$$
\widetilde{\mathbf{U}}_k = \begin{bmatrix} \widetilde{\mathbf{U}}_{\mathbf{aa}_k} & \widetilde{\mathbf{U}}_{\mathbf{a}b_k} & \widetilde{\mathbf{U}}_{\mathbf{ac}_k} \\ \mathbf{0} & 1 & \widetilde{\mathbf{U}}_{b\mathbf{c}_k} \\ \mathbf{0} & \mathbf{0} & \widetilde{\mathbf{U}}_{\mathbf{cc}_k} \end{bmatrix} \begin{matrix} \}\, n_a \\ \}\, 1 \\ \}\, n_c \end{matrix} \qquad \text{and} \qquad \widetilde{\mathbf{D}}_k = \begin{bmatrix} \widetilde{\mathbf{D}}_{\mathbf{aa}_k} & \mathbf{0} & \mathbf{0} \\ \mathbf{0} & \widetilde{d}_{b_k} & \mathbf{0} \\ \mathbf{0} & \mathbf{0} & \widetilde{\mathbf{D}}_{\mathbf{cc}_k} \end{bmatrix} \begin{matrix} \}\, n_a \\ \}\, 1 \\ \}\, n_c \end{matrix} \tag{8.32}
$$

in order to isolate a parameter. Correspondingly,

$$
\boldsymbol{\Phi}_{2_k} = \begin{bmatrix} \mathbf{I} & \mathbf{0} & \mathbf{0} \\ \mathbf{0} & 1 & \mathbf{0} \\ \mathbf{0} & \mathbf{0} & \mathbf{M}_{c_k} \end{bmatrix} \begin{bmatrix} \mathbf{I} & \mathbf{0} & \mathbf{0} \\ \mathbf{0} & m_{b_k} & \mathbf{0} \\ \mathbf{0} & \mathbf{0} & \mathbf{I} \end{bmatrix} = \boldsymbol{\Phi}_{c_k}\boldsymbol{\Phi}_{b_k} \tag{8.33}
$$

and since the process noise of an ECRV is constant $\mathbf{Q}_{2_k} = \mathbf{Q}_2$ so that $\mathbf{Q}_2$ is

$$
\mathbf{Q}_2 = \begin{bmatrix} \mathbf{0} & \mathbf{0} & \mathbf{0} \\ \mathbf{0} & q_b & \mathbf{0} \\ \mathbf{0} & \mathbf{0} & \mathbf{0} \end{bmatrix} + \begin{bmatrix} \mathbf{0} & \mathbf{0} & \mathbf{0} \\ \mathbf{0} & 0 & \mathbf{0} \\ \mathbf{0} & \mathbf{0} & \mathbf{Q}_c \end{bmatrix} = \mathbf{Q}_b + \mathbf{Q}_c \tag{8.34}
$$

As in the previous section, we note that $\boldsymbol{\Phi}_{c_k}^{-1}\mathbf{Q}_b\boldsymbol{\Phi}_{c_k}^{-\mathsf{T}} = \mathbf{Q}_b$. So, now Eq. [\(8.25\)](#page-100-5) becomes

<span id="page-101-0"></span>
$$
\mathbf{U}_{k+1}^-\mathbf{D}_{k+1}^-\mathbf{U}_{k+1}^{-\mathsf{T}} = \boldsymbol{\Phi}_{c_k}\left[\boldsymbol{\Phi}_{b_k}\widetilde{\mathbf{U}}_k\widetilde{\mathbf{D}}_k\widetilde{\mathbf{U}}_k^{\mathsf{T}}\boldsymbol{\Phi}_{b_k}^{\mathsf{T}} + \mathbf{Q}_b\right]\boldsymbol{\Phi}_{c_k}^{\mathsf{T}} + \mathbf{Q}_c \tag{8.35}
$$

The term in the square bracket in Eq. [\(8.35\)](#page-101-0) is

$$
\breve{\mathbf{U}}_k\breve{\mathbf{D}}_k\breve{\mathbf{U}}_k^{\mathsf{T}} = \boldsymbol{\Phi}_{b_k}\widetilde{\mathbf{U}}_k\widetilde{\mathbf{D}}_k\widetilde{\mathbf{U}}_k^{\mathsf{T}}\boldsymbol{\Phi}_{b_k}^{\mathsf{T}} + \mathbf{Q}_b \tag{8.36}
$$

In Appendix B, the equation above is expanded until we find that

$$
\breve{\mathbf{U}}_{\mathbf{ac}_k} = \widetilde{\mathbf{U}}_{\mathbf{ac}_k}, \qquad \breve{\mathbf{D}}_{\mathbf{cc}_k} = \widetilde{\mathbf{D}}_{\mathbf{cc}_k}, \qquad \breve{\mathbf{U}}_{\mathbf{cc}_k}^{\mathsf{T}} = \widetilde{\mathbf{U}}_{\mathbf{cc}_k}^{\mathsf{T}} \tag{8.37}
$$

Additionally,

<span id="page-101-4"></span>
$$
\breve{\mathbf{U}}_{b\mathbf{c}_k} = m_{b_k}\widetilde{\mathbf{U}}_{b\mathbf{c}_k} \tag{8.38}
$$

and

<span id="page-101-2"></span>
$$
\breve{d}_{b_k} = m_{b_k}^2\widetilde{d}_{b_k} + q_b \tag{8.39}
$$

and

<span id="page-101-3"></span>
$$
\breve{\mathbf{U}}_{\mathbf{a}b_k} = m_{b_k}\frac{\widetilde{d}_{b_k}}{\breve{d}_{b_k}}\widetilde{\mathbf{U}}_{\mathbf{a}b_k} \tag{8.40}
$$

Finally, we find that

<span id="page-101-1"></span>
$$
\breve{\mathbf{U}}_{\mathbf{aa}_k}\breve{\mathbf{D}}_{\mathbf{aa}_k}\breve{\mathbf{U}}_{\mathbf{aa}_k}^{\mathsf{T}} = \widetilde{\mathbf{U}}_{\mathbf{aa}_k}\widetilde{\mathbf{D}}_{\mathbf{aa}_k}\widetilde{\mathbf{U}}_{\mathbf{aa}_k}^{\mathsf{T}} + \left(\frac{\widetilde{d}_{b_k}q_b}{\breve{d}_{b_k}}\right)\widetilde{\mathbf{U}}_{\mathbf{a}b_k}\widetilde{\mathbf{U}}_{\mathbf{a}b_k}^{\mathsf{T}} \tag{8.41}
$$

We note that $\widetilde{\mathbf{U}}_{\mathbf{a}b_k}$ is a column vector (and is thereby of rank 1) so Eq. [\(8.41\)](#page-101-1) constitutes a 'rank one' update. Since $\breve{d}_{b_k}$, $\widetilde{d}_{b_k}$ and $q_b$ are all positive (assuming $m_{b_k}$ is a positive quantity), we can use the Agee-Turner Rank One update [[1](16-bibliography.md#page-170-16)]. It should be pointed out that as the algorithm proceeds down the 'list' of parameters, the size of the states $\mathbf{a}$ increases by one (and consequently the size of the parameters $\mathbf{c}$ decreases by one. Hence $\breve{\mathbf{U}}_{\mathbf{aa}_k}$ and $\breve{\mathbf{D}}_{\mathbf{aa}_k}$ begins with a dimension of $n_{\mathbf{x}}$ and concludes with dimension $n_{\mathbf{x}} + n_{\mathbf{p}} - 1$.

Therefore, this is done recursively for all the (sensor) parameters $\mathbf{p}$ which are of size $n_{\mathbf{p}}$.

#### The Algorithm for $\boldsymbol{\Phi}_{2_k}\widetilde{\mathbf{U}}_k\widetilde{\mathbf{D}}_k\widetilde{\mathbf{U}}_k^{\mathsf{T}}\boldsymbol{\Phi}_{2_k}^{\mathsf{T}} + \mathbf{Q}_{2_k}$

The algorithm can be expressed as follows (with the arithmetic operations (adds, multiplies, divides) in square brackets per $k$ ):

> **for** $k = 1, \cdots, n_{\mathbf{p}}$ **do**  
> &emsp;$\breve{\mathbf{D}}(n_{\mathbf{x}}+k, n_{\mathbf{x}}+k) = \mathbf{M}(k,k)^2\widetilde{\mathbf{D}}(n_{\mathbf{x}}+k, n_{\mathbf{x}}+k) + \mathbf{Q}_{\mathbf{pp}}(k,k)$ &emsp; (Eq. [\(8.39\)](#page-101-2)) $[1, 2, 0]$  
> &emsp;$\alpha = \mathbf{M}(k,k)\frac{\widetilde{\mathbf{D}}(n_{\mathbf{x}}+k, n_{\mathbf{x}}+k)}{\breve{\mathbf{D}}(n_{\mathbf{x}}+k, n_{\mathbf{x}}+k)}$ &emsp; $[0, 1, 1]$  
> &emsp;**for** $i = 1, \cdots, (n_{\mathbf{x}}+k-1)$ **do**  
> &emsp;&emsp;$\breve{\mathbf{U}}(i, n_{\mathbf{x}}+k) = \alpha\widetilde{\mathbf{U}}(i, n_{\mathbf{x}}+k)$ &emsp; (Eq. [\(8.40\)](#page-101-3)) $[0, n_{\mathbf{x}}+k-1, 0]$  
> &emsp;**end for**  
> &emsp;**for** $j = n_{\mathbf{x}}+k+1, \cdots, (n_{\mathbf{x}}+n_{\mathbf{p}})$ **do**  
> &emsp;&emsp;$\breve{\mathbf{U}}(n_{\mathbf{x}}+k, j) = \mathbf{M}(k,k)\widetilde{\mathbf{U}}(n_{\mathbf{x}}+k, j)$ &emsp; (Eq. [\(8.38\)](#page-101-4)) $[0, n_{\mathbf{p}}-k, 0]$  
> &emsp;**end for**  
> &emsp;Solve for $\breve{\mathbf{U}}_{\mathbf{xx}}^{(k)}, \breve{\mathbf{D}}_{\mathbf{xx}}^{(k)}$ using<sup>1</sup> the Rank-One update $[n_{\mathbf{x}}+k)^2, (n_{\mathbf{x}}+k)^2 + 3(n_{\mathbf{x}}+k) + 2, 0]$  
> **end for**

<span id="page-102-0"></span><sup>1</sup> We are using the nomenclature $\mathbf{U}^{(k)}$ and $\mathbf{D}^{(k)}$ to denote the upper left $n_{\mathbf{x}} + k - 1$ rows and columns of the $\mathbf{U}$ and $\mathbf{D}$ matrices

Thus, the arithmetic operations are as follows:

Adds:

$$
\sum_{k=1}^{n_{\mathbf{p}}}\left((n_{\mathbf{x}}+k)^2 + 1\right) = n_{\mathbf{x}}^2 n_{\mathbf{p}} + n_{\mathbf{p}} + n_{\mathbf{x}}(n_{\mathbf{p}}+1)n_{\mathbf{p}} + \sum_{k=1}^{n_{\mathbf{p}}} k^2 \tag{8.42}
$$

Multiplies:

$$
\begin{aligned}
\sum_{k=1}^{n_{\mathbf{p}}}\left(3 + (n_{\mathbf{x}}+k-1) + n_{\mathbf{p}} - k + (n_{\mathbf{x}}+k)^2 + 3(n_{\mathbf{x}}+k) + 2\right) &= (5.5 + 5n_{\mathbf{x}} + n_{\mathbf{x}}^2)n_{\mathbf{p}} \\
&\quad + \frac{1}{2}(2n_{\mathbf{x}} + 5)n_{\mathbf{p}}^2 + \sum_{k=1}^{n_{\mathbf{p}}} k^2
\end{aligned} \tag{8.43}
$$

and $n_{\mathbf{p}}$ divides.

#### The Agee-Turner Rank One Update Algorithm

Appendix [B.3](14-appendix-b-the-mathematics-behind-the-udu-factorization.md#page-150-0) contains the development of the Agee-Turner Rank-One update which is the key to reducing the numerical operations on the UDU Time Update. Given $\mathbf{U}$ and $\mathbf{D}$, along with $c$, and the vector $\mathbf{x}$, we are interested in obtaining $\widetilde{\mathbf{U}}$ and $\widetilde{\mathbf{D}}$ along the lines of

$$
\widetilde{\mathbf{U}}\widetilde{\mathbf{D}}\widetilde{\mathbf{U}}^{\mathsf{T}} = \mathbf{U}\mathbf{D}\mathbf{U}^{\mathsf{T}} + c\,\mathbf{x}\mathbf{x}^{\mathsf{T}} \tag{8.44}
$$

where $c > 0$ is a specified scalar term.

The algorithm to compute $\widetilde{U}_{ij}$ and $\widetilde{D}_{ii}$ is:

> $\mathcal{C}^n = c$  
> **for** $j = n, \cdots, 2$ **do**  
> &emsp;$\widetilde{D}_{jj} = D_{jj} + \mathcal{C}^j x_j^2,$ &emsp; $[n-1, 2(n-1), 0]$  
> &emsp;$\widetilde{U}_{jj} = 1$  
> &emsp;$\beta_j = \mathcal{C}^j / \widetilde{D}_{jj}$ &emsp; $[0, 0, (n-1)]$  
> &emsp;$v_j = \beta_j x_j$ &emsp; $[0, (n-1), 0]$  
> &emsp;**for** $i = 1, \cdots, j-1$ **do**  
> &emsp;&emsp;$x_i := x_i - U_{ij}x_j$ &emsp; $[\frac{1}{2}(n^2-n), \frac{1}{2}(n^2-n), 0]$  
> &emsp;&emsp;$\widetilde{U}_{ij} = U_{ij} + x_i v_j$ &emsp; $[\frac{1}{2}(n^2-n), \frac{1}{2}(n^2-n), 0]$  
> &emsp;**end for**  
> &emsp;$\mathcal{C}^{j-1} = \beta_j D_{jj}$ &emsp; $[0, (n-1), 0]$  
> **end for**  
> $\widetilde{D}_{11} = D_{11} + \mathcal{C}^1 x_1^2$ &emsp; $[1, 2, 0]$

This algorithm has $n^2$ adds, $(n^2 + 3n + 2)$ multiplies and $n - 1$ divides.

### 8.3.3. Arithmetic Operations for Time Update

For the time update of the covariance matrix, we have the following arithmetic operations:

$$
\text{Adds}: \quad 1.5n_{\mathbf{x}}^3 + n_{\mathbf{x}}^2 m_{\mathbf{x}} + n_{\mathbf{x}}^2 n_{\mathbf{p}} - 0.5n_{\mathbf{x}}^2 + n_{\mathbf{p}} + n_{\mathbf{x}}(n_{\mathbf{p}}+1)n_{\mathbf{p}} + \sum_{k=1}^{n_{\mathbf{p}}} k^2
$$

$$
\text{Multiplies}: \quad 0.5n_{\mathbf{x}}^2(3n_{\mathbf{x}}+1) + n_{\mathbf{x}}m_{\mathbf{x}}(n_{\mathbf{x}}+1) + (5.5 + 5n_{\mathbf{x}} + n_{\mathbf{x}}^2)n_{\mathbf{p}} + \frac{1}{2}(2n_{\mathbf{x}}+5)n_{\mathbf{p}}^2 + \sum_{k=1}^{n_{\mathbf{p}}} k^2
$$

$$
\text{Divides}: \quad (n_{\mathbf{x}} + m_{\mathbf{x}})(n_{\mathbf{x}} - 1) + n_{\mathbf{p}}
$$

For $n_{\mathbf{x}} = 9$, $m_{\mathbf{x}} = 9$, $n_{\mathbf{p}} = 26$, we will utilize 16,407 adds, 19,338 multiplies, and 170 divides. In contrast, if we did the MGS on all 35 states ($n_{\mathbf{x}} = 35$, $m_{\mathbf{x}} = 35$ and $n_{\mathbf{p}} = 0$), we would use 85,750 adds, 88,200 multiplies, and 34 divides. Finally, if the covariance were updated (without any consideration given to the structure of $\boldsymbol{\Phi}_k$ from $\boldsymbol{\Phi}_k\mathbf{P}_k^-\boldsymbol{\Phi}_k^{\mathsf{T}} + \mathbf{Q}_k$) in the conventional manner, with $n_{\mathbf{x}} = 35$, $m_{\mathbf{x}} = 35$, it would cost 84,525 adds, 85,750 multiplies and no divides[<sup>†</sup>](#page-103-1). Thus, a very strong case is made for using the UDU factorization and harnessing the benefit of updating the sensor parameters using the Agee-Turner Rank-One update. Thus, the UDU time update taking advantage of the fact that most of the states are sensor parameters results in nearly **five times fewer** adds and multiplies and 170 more divides that if we operated on the full covariance matrix.

<span id="page-103-1"></span><sup>†</sup> For matrices, $\mathbf{A}$ and $\mathbf{B}$ of dimension $n \times m$ and $m \times p$, respectively, the product

$$
\mathbf{C} = \mathbf{A}\mathbf{B} \tag{8.45}
$$

results in $n(m-1)p$ adds, $nmp$ multiplies and no divides.

## 8.4. The Measurement Update

<span id="page-103-0"></span>The UDU factorization requires that we process the measurements one-at-a-time [[5](16-bibliography.md#page-170-1)]. This should not be construed as a weakness of the formulation. If the measurements are correlated, they can be 'decorrelated' as in Appendix [B.4](14-appendix-b-the-mathematics-behind-the-udu-factorization.md#page-153-0)

We remind ourselves that the covariance update equation is

$$
\mathbf{P}^+ = \mathbf{P}^- - \mathbf{K}\mathbf{H}\mathbf{P}^- \tag{8.46}
$$

where $\mathbf{K}$ is the Kalman Gain matrix, $\mathbf{H}$ is the measurement partial, $\mathbf{P}^-$ is the *a priori* covariance, and $\mathbf{P}^+$ is the *a posteriori* covariance matrix. Using the covariance factors $\mathbf{U}$ and $\mathbf{D}$, we rewrite the above equation as

<span id="page-104-0"></span>
$$
\mathbf{U}^+\mathbf{D}^+\mathbf{U}^{+\mathsf{T}} = \mathbf{U}^-\mathbf{D}^-\mathbf{U}^{-\mathsf{T}} - \mathbf{K}\mathbf{H}\mathbf{U}^-\mathbf{D}^-\mathbf{U}^{-\mathsf{T}} \tag{8.47}
$$

We note that $\mathbf{U}$ and $\mathbf{U}^-$ and $\mathbf{D}$ and $\mathbf{D}^-$ are $n \times n$ matrices, and because we are using the paradigm of processing the measurements one at a time, $\mathbf{H}$ is an $1 \times n$ vector and $\mathbf{K}$ is an $n \times 1$ vector. Recalling that $\mathbf{K}$ is defined as

$$
\mathbf{K} = \mathbf{P}^-\mathbf{H}^{\mathsf{T}}\left(\mathbf{H}\mathbf{P}^-\mathbf{H}^{\mathsf{T}} + \mathbf{R}\right)^{-1} = \frac{\mathbf{U}^-\mathbf{D}^-\mathbf{U}^{-\mathsf{T}}\mathbf{H}^{\mathsf{T}}}{\mathbf{H}\mathbf{U}^-\mathbf{D}^-\mathbf{U}^{-\mathsf{T}}\mathbf{H}^{\mathsf{T}} + \mathbf{R}} = \frac{\mathbf{U}^-\mathbf{D}^-\mathbf{U}^{-\mathsf{T}}\mathbf{H}^{\mathsf{T}}}{\alpha} \tag{8.48}
$$

where the scalar $\alpha$ is defined to be

$$
\alpha \triangleq \mathbf{H}\mathbf{U}^-\mathbf{D}^-\mathbf{U}^{-\mathsf{T}}\mathbf{H}^{\mathsf{T}} + \mathbf{R} \tag{8.49}
$$

We find that Eq. [\(8.47\)](#page-104-0) becomes

<span id="page-104-1"></span>
$$
\mathbf{U}^+\mathbf{D}^+\mathbf{U}^{+\mathsf{T}} = \mathbf{U}^-\left[\mathbf{D}^- - \frac{\mathbf{D}^-\mathbf{U}^{-\mathsf{T}}\mathbf{H}^{\mathsf{T}}}{\alpha}\mathbf{H}\mathbf{U}^-\mathbf{D}^-\right]\mathbf{U}^{-\mathsf{T}} \tag{8.50}
$$

If we define the $n \times 1$ vector $\mathbf{v}$ as

$$
\mathbf{v} \triangleq \mathbf{D}^-\mathbf{U}^{-\mathsf{T}}\mathbf{H}^{\mathsf{T}} \tag{8.51}
$$

Eq. [\(8.50\)](#page-104-1) becomes

<span id="page-104-2"></span>
$$
\mathbf{U}^+\mathbf{D}^+\mathbf{U}^{+\mathsf{T}} = \mathbf{U}^-\left[\mathbf{D}^- - \frac{1}{\alpha}\mathbf{v}\mathbf{v}^{\mathsf{T}}\right]\mathbf{U}^{-\mathsf{T}} \tag{8.52}
$$

We now analyze the bracketed term in Eq. [\(8.52\)](#page-104-2) and find that we can define

<span id="page-104-3"></span>
$$
\widetilde{\mathbf{U}}\widetilde{\mathbf{D}}\widetilde{\mathbf{U}}^{\mathsf{T}} \triangleq \mathbf{D}^- - \frac{1}{\alpha}\mathbf{v}\mathbf{v}^{\mathsf{T}} \tag{8.53}
$$

Therefore,

$$
\mathbf{U}^+ = \mathbf{U}^-\widetilde{\mathbf{U}} \qquad \text{and} \qquad \mathbf{D}^+ = \widetilde{\mathbf{D}} \tag{8.54}
$$

So, how do we proceed? This has all the marks of a rank-one update, for after all $\mathbf{v}$ is of rank one. We *can* proceed by using the Agee-Turner rank-one update. Except for one thing – that pesky minus sign in Eq. [\(8.53\)](#page-104-3). That minus sign portends all sorts of numerical issues because there is a possibility that we can lose numerical precision if the Agee-Turner update is used blindly. It turns out that we can have 'our cake and eat it too'; Neil Carlson developed a rank-one update to precisely remedy our issue. The mathematical development of this algorithm is detailed in Appendix [B.5.](14-appendix-b-the-mathematics-behind-the-udu-factorization.md#page-153-1)

The algorithm is as follows: Given $\mathbf{U}^-$, $\mathbf{D}^-$, $\mathbf{R}$, and $\mathbf{H}$

> $\mathbf{f} = \mathbf{U}^{-\mathsf{T}}\mathbf{H}^{\mathsf{T}}$ &emsp; where &emsp; $\mathbf{f} = \begin{bmatrix} f_1 & f_2 & \cdots & f_n \end{bmatrix}^{\mathsf{T}}$ &emsp; $[\frac{1}{2}(n_{\mathbf{x}}^2 - n_{\mathbf{x}}), \frac{1}{2}(n_{\mathbf{x}}^2 - n_{\mathbf{x}}), 0]$  
> $\mathbf{v} = \mathbf{D}^{-\mathsf{T}}\mathbf{f}$ &emsp; where &emsp; $\mathbf{v} = \begin{bmatrix} \bar{d}_1 f_1 & \bar{d}_2 f_2 & \cdots & \bar{d}_n f_n \end{bmatrix}^{\mathsf{T}}$ &emsp; $[0, n_{\mathbf{x}}, 0]$  
> $\overline{\mathbf{K}}_1 = \begin{bmatrix} v_1 & 0 & \cdots & \bar{0} \end{bmatrix}^{\mathsf{T}}$  
> $\alpha_1 = \mathbf{R} + v_1 f_1$ &emsp; $[1, 1, 0]$  
> $d_1 = \left(\frac{\mathbf{R}}{\alpha_1}\right)\bar{d}_1$ &emsp; $[0, 1, 1]$  
> **for** $j = 2, \cdots, n$ **do**  
> &emsp;$\alpha_j = \alpha_{j-1} + v_j f_j$ &emsp; $[n_{\mathbf{x}} - 1, n_{\mathbf{x}} - 1, 0]$  
> &emsp;$d_j = \left(\frac{\alpha_{j-1}}{\alpha_j}\right)\bar{d}_j$ &emsp; $[0, n_{\mathbf{x}} - 1, n_{\mathbf{x}} - 1]$  
> &emsp;$\lambda_j = -\left(f_j/\alpha_{j-1}\right)$ &emsp; $[0, 0, n_{\mathbf{x}} - 1]$  
> &emsp;$\mathbf{U}_j^+ = \mathbf{U}_j^- + \lambda_j\overline{\mathbf{K}}_{j-1}$ &emsp; $[\frac{1}{2}(n_{\mathbf{x}}^2 - n_{\mathbf{x}}), \frac{1}{2}(n_{\mathbf{x}}^2 - n_{\mathbf{x}}), 0]$  
> &emsp;$\overline{\mathbf{K}}_j = \overline{\mathbf{K}}_{j-1} + v_j\mathbf{U}_j^-$ &emsp; $[\frac{1}{2}(n_{\mathbf{x}}^2 - n_{\mathbf{x}}), \frac{1}{2}(n_{\mathbf{x}}^2 - n_{\mathbf{x}}), 0]$  
> **end for**  
> $\mathbf{K} = \overline{\mathbf{K}}_n/\alpha$ &emsp; $[0, 0, n_{\mathbf{x}}]$

Thus, taking advantage of the triangularity of the $\mathbf{U}^-$ matrix (and the fact that $\mathbf{U}^{-\mathsf{T}}\mathbf{H}^{\mathsf{T}}$ and $\lambda_j\overline{\mathbf{K}}_{j-1}$ and $v_j\mathbf{U}_j^-$ use $n_{\mathbf{x}}(n_{\mathbf{x}}-1)/2$multiplies and adds), for each measurement processed, the covariance update results in $1.5n_{\mathbf{x}}^2 - 0.5n_{\mathbf{x}}$ adds, $1.5n_{\mathbf{x}}^2 + 1.5n_{\mathbf{x}}$ multiplies and $3n_{\mathbf{x}} - 1$ divides.

For the normal, Joseph Kalman filter update, for a scalar measurement, we find that if we use efficient methods of calculating and storing quantities [[5](16-bibliography.md#page-170-1)], we use $4.5n_{\mathbf{x}}^2 + 3.5n_{\mathbf{x}}$ adds, $4n_{\mathbf{x}}^2 + 4.5n_{\mathbf{x}}$ multiplies and 1 divide.

For the "Conventional" Kalman filter update ($\mathbf{P} = \mathbf{P}^- - \mathbf{K}\mathbf{H}\mathbf{P}^-$ in Eq.(61)), for a scalar measurement, we find that [[5](16-bibliography.md#page-170-1)] we use $1.5n_{\mathbf{x}}^2 + 1.5n_{\mathbf{x}}$ adds, $1.5n_{\mathbf{x}}^2 + 0.5n_{\mathbf{x}}$ multiplies and 1 divide.

Thus, for $n_{\mathbf{x}} = 35$, the covariance update due to measurement processing with the UDU factorization uses 1820 adds, 1890 divides and 104 divides compared with 5635 adds, 5058 multiplies and 1 divide for the efficient Joseph update. The "Conventional" Kalman update uses 1890 adds, 1855 multiplies, and 1 divide.

Hence there is almost a factor of 2.5 improvement in the adds and multiplies using the triangular (UDU) update compared with the Joseph update. This rivals the efficiency of the "conventional" Kalman Filter update.

### 8.4.1. Consider Covariance and its Implementation in the UDU Filter

'Consider' Analysis was first introduced by S. F. Schmidt of NASA Ames in the mid 1960s as a means to account for errors in both the dynamic and measurement models due to uncertain parameters [[75](16-bibliography.md#page-173-5)]. The Consider Kalman Filter, also called the Schmidt-Kalman Filter, resulted from this body of work. The consider approach is especially useful when parameters have low observability.

We partition the state-vector, $\mathbf{x}$ into the $n_{\mathbf{s}}$"estimated states", $\mathbf{s}$, and the $n_{\mathbf{p}}$ "consider" parameters, $\mathbf{p}$, as

$$
\mathbf{x} \triangleq \begin{bmatrix} \mathbf{s} \\ \mathbf{p} \end{bmatrix} \tag{8.55}
$$

so that

$$
\mathbf{P} = \begin{bmatrix} \mathbf{P}_{\mathbf{ss}} & \mathbf{P}_{\mathbf{sp}} \\ \mathbf{P}_{\mathbf{ps}} & \mathbf{P}_{\mathbf{pp}} \end{bmatrix}, \qquad \mathbf{H} = \begin{bmatrix} \mathbf{H}_{\mathbf{s}} & \mathbf{H}_{\mathbf{p}} \end{bmatrix} \tag{8.56}
$$

$$
\mathbf{K}_{opt} = \begin{bmatrix} \mathbf{K}_{\mathbf{s},opt} \\ \mathbf{K}_{\mathbf{p},opt} \end{bmatrix} = \begin{bmatrix} \mathbf{P}_{\mathbf{ss}}^-\mathbf{H}_{\mathbf{s}}^{\mathsf{T}} + \mathbf{P}_{\mathbf{sp}}^-\mathbf{H}_{\mathbf{p}}^{\mathsf{T}} \\ \mathbf{P}_{\mathbf{ps}}^-\mathbf{H}_{\mathbf{s}}^{\mathsf{T}} + \mathbf{P}_{\mathbf{pp}}^-\mathbf{H}_{\mathbf{p}}^{\mathsf{T}} \end{bmatrix}\mathbf{W}^{-1} \tag{8.57}
$$

where $\mathbf{K}_{opt}$ is the optimal Kalman gain computed for the full state, $\mathbf{x}$, and $\mathbf{W}$ is

$$
\mathbf{W} = \mathbf{H}_{\mathbf{s}}\mathbf{P}_{\mathbf{ss}}^-\mathbf{H}_{\mathbf{s}}^{\mathsf{T}} + \mathbf{H}_{\mathbf{s}}\mathbf{P}_{\mathbf{sp}}^-\mathbf{H}_{\mathbf{p}}^{\mathsf{T}} + \mathbf{H}_{\mathbf{p}}\mathbf{P}_{\mathbf{ps}}^-\mathbf{H}_{\mathbf{s}}^{\mathsf{T}} + {+\mathbf{H}_{\mathbf{p}}\mathbf{P}_{\mathbf{pp}}^-\mathbf{H}_{\mathbf{p}}^{\mathsf{T}}} \tag{8.58}
$$

Therefore, if we now choose the $\mathbf{K}_{\mathbf{s}}$ and $\mathbf{K}_{\mathbf{p}}$ carefully such that the $\mathbf{K}_{\mathbf{s}} = \mathbf{K}_{\mathbf{s},opt}$, the *a posteriori* covariance matrix is

$$
\mathbf{P}^+ = \begin{bmatrix} \mathbf{P}_{\mathbf{ss}}^- - \mathbf{K}_{\mathbf{s}}\mathbf{W}\mathbf{K}_{\mathbf{s}}^{\mathsf{T}} & \mathbf{P}_{\mathbf{sp}}^- - \mathbf{K}_{\mathbf{s}}\mathbf{H}\begin{bmatrix} \mathbf{P}_{\mathbf{sp}}^- \\ \mathbf{P}_{\mathbf{pp}}^- \end{bmatrix} \\ \mathbf{P}_{\mathbf{ps}}^- - \begin{bmatrix} \mathbf{P}_{\mathbf{sp}}^- \\ \mathbf{P}_{\mathbf{pp}}^- \end{bmatrix}^{\mathsf{T}}\mathbf{H}^{\mathsf{T}}\mathbf{K}_{\mathbf{s}}^{\mathsf{T}} & \mathbf{P}_{\mathbf{pp}}^- - \mathbf{K}_{\mathbf{p}}\mathbf{W}\mathbf{K}_{\mathbf{p}}^{\mathsf{T}} \end{bmatrix} \tag{8.59}
$$

This equation is valid for any value of $\mathbf{K}_{\mathbf{p}}$. Notice that there is no $\mathbf{K}_{\mathbf{p}}$ in the correlation terms of the covariance matrix. **Therefore, what is *remarkable* about this equation is that once the optimal $\mathbf{K}_{\mathbf{s}}$ is chosen, the correlation between $\mathbf{s}$ and $\mathbf{p}$ is independent of the choice of $\mathbf{K}_{\mathbf{p}}$.**

In its essence, the consider parameters are not updated; therefore, the Kalman gain associated with the consider parameters, $\mathbf{p}$, is zero, *i.e.* $\mathbf{K}_{\mathbf{p}} = \mathbf{0}$. However, several comments are in order:

- (1) When using the Schmidt-Kalman filter, the *a priori* and *a posteriori* covariance of the parameters ($\mathbf{P}_{\mathbf{pp}}$) are the same.
- (2) The *a posteriori* covariance matrix of the states and the correlation between the states and the parameters are the same regardless of whether one uses the Schmidt-Kalman filter or the optimal Kalman update

Therefore, the *consider* covariance, $\mathbf{P}_{con}^+$ is

$$
\mathbf{P}_{con}^+ = \begin{bmatrix} \mathbf{P}_{\mathbf{ss}}^- - \mathbf{K}_{\mathbf{s}}\mathbf{W}\mathbf{K}_{\mathbf{s}}^{\mathsf{T}} & \mathbf{P}_{\mathbf{sp}}^- - \mathbf{K}_{\mathbf{s}}\mathbf{H}\begin{bmatrix} \mathbf{P}_{\mathbf{sp}}^- \\ \mathbf{P}_{\mathcal{BB}}^- \end{bmatrix} \\ \mathbf{P}_{\mathbf{ps}}^- - \begin{bmatrix} \mathbf{P}_{\mathbf{sp}}^- \\ \mathbf{P}_{\mathbf{pp}}^- \end{bmatrix}^{\mathsf{T}}\mathbf{H}^{\mathsf{T}}\mathbf{K}_{\mathbf{s}}^{\mathsf{T}} & \mathbf{P}_{\mathbf{pp}}^- \end{bmatrix} \tag{8.60}
$$

Of course, the "full" optimal covariance matrix update is

$$
\mathbf{P}_{opt}^+ = \begin{bmatrix} \mathbf{P}_{\mathbf{ss}}^- - \mathbf{K}_{\mathbf{s},opt}\mathbf{W}\mathbf{K}_{\mathbf{s},opt}' & \mathbf{P}_{\mathbf{sp}}^- - \mathbf{K}_{\mathbf{s},opt}\mathbf{H}\begin{bmatrix} \mathbf{P}_{\mathbf{sp}}^- \\ \mathbf{P}_{\mathbf{pp}}^- \end{bmatrix} \\ \mathbf{P}_{\mathbf{ps}}^- - \begin{bmatrix} \mathbf{P}_{\mathbf{sp}}^- \\ \mathbf{P}_{\mathbf{pp}}^- \end{bmatrix}^{\mathsf{T}}\mathbf{H}^{\mathsf{T}}\mathbf{K}_{\mathbf{s},opt}' & \mathbf{P}_{\mathbf{pp}}^- - \mathbf{K}_{\mathbf{p},opt}\mathbf{W}\mathbf{K}_{\mathbf{p},opt}' \end{bmatrix} \tag{8.61}
$$

The UDU formulation, while numerically stable and tight, is quite inflexible to making any changes in the framework. At first blush, it would seem that the consider analysis would not fit into the framework. However, all is not in vain. With some clever rearrangements, we can allow for a rank-one update to include consider states in the measurement update. The measurement update, expressed in terms of the consider covariance [[92](16-bibliography.md#page-173-11)], is

<span id="page-106-0"></span>
$$
\mathbf{P}_{opt}^+ = \mathbf{P}_{con}^+ - (\mathbf{S}\mathbf{K}_{opt})\,\mathbf{W}\,(\mathbf{S}\mathbf{K}_{opt})' \tag{8.62}
$$

where $\mathbf{S}$ is an $n_{\mathbf{x}} \times n_{\mathbf{x}}$ matrix (defining $n_{\mathbf{x}} \triangleq n_{\mathbf{s}} + n_{\mathbf{p}}$, where $n_{\mathbf{x}}$ is the total number of states, $n_{\mathbf{p}}$ is the number of consider states, and $n_{\mathbf{s}}$ is the number of "non-consider" states) defined as

$$
\mathbf{S} \triangleq \begin{bmatrix} \mathbf{0}_{n_{\mathbf{s}} \times n_{\mathbf{s}}} & \mathbf{0}_{n_{\mathbf{s}} \times n_{\mathbf{p}}} \\ \mathbf{0}_{n_{\mathbf{p}} \times n_{\mathbf{s}}} & \mathbf{I}_{n_{\mathbf{p}} \times n_{\mathbf{p}}} \end{bmatrix} \tag{8.63}
$$

Since we are processing scalar measurements, we note that $\mathbf{W} = \frac{1}{\alpha}$ is a scalar and $\mathbf{K}_{opt}$ is an $n_{\mathbf{x}} \times 1$ vector. Therefore $\mathbf{S}\mathbf{K}_{opt}$ is an $n_{\mathbf{x}} \times 1$ vector. Therefore, solving for the consider covariance,

$$
\mathbf{P}_{con}^+ = \mathbf{P}_{opt}^+ + W\,(\mathbf{S}\mathbf{K}_{opt})\,(\mathbf{S}\mathbf{K}_{opt})^{\mathsf{T}} \tag{8.64}
$$

Eq. [\(8.62\)](#page-106-0) has the same form as the original rank-one update *i.e.* $\mathbf{P}^+ = \mathbf{P}^- + c\,\mathbf{a}\mathbf{a}^{\mathsf{T}}$, with $\mathbf{a} = \mathbf{S}\mathbf{K}_{opt}$ and $c = \frac{1}{\alpha}$. With this in mind, we can use the (un-modified) rank-one update which is a backward-recursive update [[1](16-bibliography.md#page-170-16)]. If, for example, all the consider parameters are in the lower part of the state-space, we can effectively reduce the computations by ending the update when the covariance of the state of the last consider parameter is updated.

Therefore, the procedure is as follows: first perform a complete Carlson rank-one measurement update with the optimal Kalman Gain ($\mathbf{K}_{opt}$) on the full covariance matrix. Second, perform another rank-one update with $\mathbf{a} = \mathbf{S}\mathbf{K}_{opt}$ and $c = \frac{1}{\alpha}$, according to the Agee-Turner rank-one update (as in Table 1).

Therefore, since there is an additional rank-one update associated with the consider states and if no rearrangements of the consider states are performed, then there will be an additional $n_{\mathbf{x}}^2$ adds, $n_{\mathbf{x}}^2 + 3n_{\mathbf{x}} + 2$ multiplies, and $n_{\mathbf{x}} - 1$ divides per measurement.

The use of the "consider state" option, if it is exercised, is likely to be used in "consider"ing the attitude states, particularly during entry. The rationale for this is that in certain degenerate cases, like when GPS satellites are reacquired after entry blackout, the attitude estimate could be adversely affected. So, to protect against this, the "consider" option may be exercised with respect to the attitude states.

## 8.5. Conclusions

<span id="page-107-0"></span>Matrix factorization methods, particularly the UDU factorization, are very useful – indeed essential – for onboard navigation algorithms. They are numerically stable and computationally efficient, competitive with the classic Kalman filter implementation. In addition, they allow the navigation designer to investigate the positive definiteness of the covariance matrix for "free," since by inspecting the entries of $\mathbf{D}$, if any elements of $\mathbf{D}$ are negative, then the covariance matrix will not be positive semi-definite.

---

[← Chapter 7. State Representations](07-state-representations.md) · [Contents](README.md) · [Chapter 9. Attitude Estimation →](09-attitude-estimation.md)
