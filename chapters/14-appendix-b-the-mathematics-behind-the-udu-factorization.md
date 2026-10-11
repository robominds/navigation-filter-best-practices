[← Appendix A. Models and Realizations of Random Variables](13-appendix-a-models-and-realizations-of-random-variables.md) · [Contents](README.md) · [Appendix C. An Analysis of Dual Inertial-Absolute and Inertial-Relative Navigation Filters →](15-appendix-c-an-analysis-of-dual-inertial-absolute-and-inertial-relative.md)

# <span id="page-148-0"></span>Appendix B. The Mathematics Behind the UDU Factorization

*Contributed by Chris D'Souza*

## B.1. The Partitioning into Two Subproblems

<span id="page-148-1"></span>We can find that the update equation is

$$
\mathbf{U}_{k+1}^{-}\mathbf{D}_{k+1}^{-}\mathbf{U}_{k+1}^{-\mathsf{T}} = \boldsymbol{\Phi}_k\mathbf{U}_k^{+}\mathbf{D}_k^{+}\mathbf{U}_k^{+\mathsf{T}}\boldsymbol{\Phi}_k^{\mathsf{T}} + \mathbf{Q}_k \tag{B.1}
$$

$$
\begin{aligned}
&= \boldsymbol{\Phi}_{2_k}\boldsymbol{\Phi}_{1_k}\mathbf{U}_k^{+}\mathbf{D}_k^{+}\mathbf{U}_k^{+\mathsf{T}}\boldsymbol{\Phi}_{1_k}^{\mathsf{T}}\boldsymbol{\Phi}_{2_k}^{\mathsf{T}} + \mathbf{Q}_{1_k} + \mathbf{Q}_{2_k} \\
&= \boldsymbol{\Phi}_{2_k}\left[\boldsymbol{\Phi}_{1_k}\mathbf{U}_k^{+}\mathbf{D}_k^{+}\mathbf{U}_k^{+\mathsf{T}}\boldsymbol{\Phi}_{1_k}^{\mathsf{T}}\right]\boldsymbol{\Phi}_{2_k}^{\mathsf{T}} + \mathbf{Q}_{1_k} + \mathbf{Q}_{2_k}
\end{aligned} \tag{B.2}
$$

Recalling that $\mathbf{Q}_{1_k} = \boldsymbol{\Phi}_{2_k}\boldsymbol{\Phi}_{2_k}^{-1}\mathbf{Q}_{1_k}\boldsymbol{\Phi}_{2_k}^{-\mathsf{T}}\boldsymbol{\Phi}_{2_k}^{\mathsf{T}}$ and

$$
\boldsymbol{\Phi}_{2_k}^{-1} = \begin{bmatrix} \mathbf{I} & \mathbf{0} \\ \mathbf{0} & \mathbf{M}_k^{-1} \end{bmatrix} \tag{B.3}
$$

where $\mathbf{M}_k^{-1} = \operatorname{diag}(1/m_{k_i}),\ i = 1, 2, 3, \cdots, n_{\mathbf{p}}$. We note that

$$
\boldsymbol{\Phi}_{2_k}^{-1}\mathbf{Q}_{1_k}\boldsymbol{\Phi}_{2_k}^{-\mathsf{T}} = \begin{bmatrix} \mathbf{I} & \mathbf{0} \\ \mathbf{0} & \mathbf{M}_k^{-1} \end{bmatrix} \begin{bmatrix} \mathbf{Q}_{\mathbf{xx}_k} & \mathbf{0} \\ \mathbf{0} & \mathbf{0} \end{bmatrix} \begin{bmatrix} \mathbf{I} & \mathbf{0} \\ \mathbf{0} & \mathbf{M}_k^{-1} \end{bmatrix} = \begin{bmatrix} \mathbf{Q}_{\mathbf{xx}_k} & \mathbf{0} \\ \mathbf{0} & \mathbf{0} \end{bmatrix} = \mathbf{Q}_{1_k} \tag{B.4}
$$

## B.2. The Mathematics Behind the Second Subproblem

<span id="page-148-2"></span>Recall that we partitioned $\widetilde{\mathbf{U}}$ and $\widetilde{\mathbf{D}}$ as

$$
\widetilde{\mathbf{U}}_k = \begin{bmatrix} \widetilde{\mathbf{U}}_{\mathbf{aa}_k} & \widetilde{\mathbf{U}}_{\mathbf{a}b_k} & \widetilde{\mathbf{U}}_{\mathbf{ac}_k} \\ \mathbf{0} & 1 & \widetilde{\mathbf{U}}_{b\mathbf{c}_k} \\ \mathbf{0} & \mathbf{0} & \widetilde{\mathbf{U}}_{\mathbf{cc}_k} \end{bmatrix} \begin{array}{l} \}\, n_a \\ \}\, 1 \\ \}\, n_c \end{array} \qquad \text{and} \qquad \widetilde{\mathbf{D}}_k = \begin{bmatrix} \widetilde{\mathbf{D}}_{\mathbf{aa}_k} & \mathbf{0} & \mathbf{0} \\ \mathbf{0} & \widetilde{d}_{b_k} & \mathbf{0} \\ \mathbf{0} & \mathbf{0} & \widetilde{\mathbf{D}}_{\mathbf{cc}_k} \end{bmatrix} \begin{array}{l} \}\, n_a \\ \}\, 1 \\ \}\, n_c \end{array} \tag{B.5}
$$

in order to isolate a parameter. In fact, the state we choose to isolate is one of the Gauss-Markov states (likely associated with a sensor). Let

$$
\boldsymbol{\Phi}_{2_k} = \begin{bmatrix} \mathbf{I} & \mathbf{0} & \mathbf{0} \\ \mathbf{0} & 1 & \mathbf{0} \\ \mathbf{0} & \mathbf{0} & \mathbf{M}_{c_k} \end{bmatrix} \begin{bmatrix} \mathbf{I} & \mathbf{0} & \mathbf{0} \\ \mathbf{0} & m_{b_k} & \mathbf{0} \\ \mathbf{0} & \mathbf{0} & \mathbf{I} \end{bmatrix} = \boldsymbol{\Phi}_{c_k}\boldsymbol{\Phi}_{b_k} \tag{B.6}
$$

and

$$
\mathbf{Q}_{2_k} = \begin{bmatrix} \mathbf{0} & \mathbf{0} & \mathbf{0} \\ \mathbf{0} & q_{b_k} & \mathbf{0} \\ \mathbf{0} & \mathbf{0} & \mathbf{0} \end{bmatrix} + \begin{bmatrix} \mathbf{0} & \mathbf{0} & \mathbf{0} \\ \mathbf{0} & 0 & \mathbf{0} \\ \mathbf{0} & \mathbf{0} & \mathbf{Q}_{c_k} \end{bmatrix} = \mathbf{Q}_{b_k} + \mathbf{Q}_{c_k} \tag{B.7}
$$

As in the previous exercise, we note that $\boldsymbol{\Phi}_{c_k}^{-1}\mathbf{Q}_{b_k}\boldsymbol{\Phi}_{c_k}^{-\mathsf{T}} = \mathbf{Q}_{b_k}$. So, now Eq. [\(8.25\)](08-factorization-methods.md#page-100-5) becomes

<span id="page-149-0"></span>
$$
\mathbf{U}_{k+1}^{-}\mathbf{D}_{k+1}^{-}\mathbf{U}_{k+1}^{-\mathsf{T}} = \boldsymbol{\Phi}_{c_k}\left[\boldsymbol{\Phi}_{b_k}\widetilde{\mathbf{U}}_k\widetilde{\mathbf{D}}_k\widetilde{\mathbf{U}}_k^{\mathsf{T}}\boldsymbol{\Phi}_{b_k}^{\mathsf{T}} + \mathbf{Q}_{b_k}\right]\boldsymbol{\Phi}_{c_k}^{\mathsf{T}} + \mathbf{Q}_{c_k} \tag{B.8}
$$

The term in the square bracket in Eq. [\(B.8\)](#page-149-0) is

<span id="page-149-1"></span>
$$
\breve{\mathbf{U}}_k\breve{\mathbf{D}}_k\breve{\mathbf{U}}_k^{\mathsf{T}} = \boldsymbol{\Phi}_{b_k}\widetilde{\mathbf{U}}_k\widetilde{\mathbf{D}}_k\widetilde{\mathbf{U}}_k^{\mathsf{T}}\boldsymbol{\Phi}_{b_k}^{\mathsf{T}} + \mathbf{Q}_{b_k} \tag{B.9}
$$

The left side of Eq. [\(B.9\)](#page-149-1) (recalling that $\breve{\mathbf{U}}_{bb_k} = 1$) is

<span id="page-149-2"></span>
$$
\breve{\mathbf{U}}_k\breve{\mathbf{D}}_k\breve{\mathbf{U}}_k^{\mathsf{T}} = \left[\begin{array}{c|c|c}
\breve{\mathbf{U}}_{\mathbf{aa}_k}\breve{\mathbf{D}}_{\mathbf{aa}_k}\breve{\mathbf{U}}_{\mathbf{aa}_k}^{\mathsf{T}} & \breve{\mathbf{U}}_{\mathbf{ac}_k}\breve{\mathbf{D}}_{\mathbf{cc}_k}\breve{\mathbf{U}}_{\mathbf{ac}_k}^{\mathsf{T}} & \breve{\mathbf{U}}_{\mathbf{ac}_k}\breve{\mathbf{D}}_{\mathbf{cc}_k}\breve{\mathbf{U}}_{\mathbf{cc}_k}^{\mathsf{T}} \\
+\breve{\mathbf{U}}_{\mathbf{a}b_k}\breve{d}_{b_k}\breve{\mathbf{U}}_{\mathbf{a}b_k}^{\mathsf{T}} & +\breve{\mathbf{U}}_{\mathbf{a}b_k}\breve{d}_{b_k} & \\
\breve{\mathbf{U}}_{\mathbf{ac}_k}\breve{\mathbf{D}}_{\mathbf{cc}_k}\breve{\mathbf{U}}_{\mathbf{ac}_k}^{\mathsf{T}} & & \\
\hdashline
\breve{d}_{b_k}\breve{\mathbf{U}}_{\mathbf{a}b_k}^{\mathsf{T}} & \breve{d}_{b_k} + \breve{\mathbf{U}}_{b\mathbf{c}_k}\breve{\mathbf{D}}_{\mathbf{cc}_k}\breve{\mathbf{U}}_{b\mathbf{c}_k}^{\mathsf{T}} & \breve{\mathbf{U}}_{b\mathbf{c}_k}\breve{\mathbf{D}}_{\mathbf{cc}_k}\breve{\mathbf{U}}_{\mathbf{cc}_k}^{\mathsf{T}} \\
\breve{\mathbf{U}}_{b\mathbf{c}_k}\breve{\mathbf{D}}_{\mathbf{cc}_k}\breve{\mathbf{U}}_{\mathbf{ac}_k}^{\mathsf{T}} & & \\
\hdashline
\breve{\mathbf{U}}_{\mathbf{cc}_k}\breve{\mathbf{D}}_{\mathbf{cc}_k}\breve{\mathbf{U}}_{\mathbf{ac}_k}^{\mathsf{T}} & \breve{\mathbf{U}}_{\mathbf{cc}_k}\breve{\mathbf{D}}_{\mathbf{cc}_k}\breve{\mathbf{U}}_{b\mathbf{c}_k}^{\mathsf{T}} & \breve{\mathbf{U}}_{\mathbf{cc}_k}\breve{\mathbf{D}}_{\mathbf{cc}_k}\breve{\mathbf{U}}_{\mathbf{cc}_k}^{\mathsf{T}}
\end{array}\right] \tag{B.10}
$$

The right side of Eq. [\(B.9\)](#page-149-1), once again recalling that $\widetilde{\mathbf{U}}_{bb_k} = 1$, is

<span id="page-149-3"></span>
$$
\begin{aligned}
&\boldsymbol{\Phi}_{b_k}\widetilde{\mathbf{U}}_k\widetilde{\mathbf{D}}_k\widetilde{\mathbf{U}}_k^{\mathsf{T}}\boldsymbol{\Phi}_{b_k}^{\mathsf{T}} + \mathbf{Q}_{b_k} = \\
&\quad \left[\begin{array}{c|c|c}
\widetilde{\mathbf{U}}_{\mathbf{aa}_k}\widetilde{\mathbf{D}}_{\mathbf{aa}_k}\widetilde{\mathbf{U}}_{\mathbf{aa}_k}^{\mathsf{T}} & m_{b_k}\widetilde{\mathbf{U}}_{\mathbf{ac}_k}\widetilde{\mathbf{D}}_{\mathbf{cc}_k}\widetilde{\mathbf{U}}_{\mathbf{ac}_k}^{\mathsf{T}} & \widetilde{\mathbf{U}}_{\mathbf{ac}_k}\widetilde{\mathbf{D}}_{\mathbf{cc}_k}\widetilde{\mathbf{U}}_{\mathbf{cc}_k}^{\mathsf{T}} \\
+\widetilde{\mathbf{U}}_{\mathbf{a}b_k}\widetilde{d}_{b_k}\widetilde{\mathbf{U}}_{\mathbf{a}b_k}^{\mathsf{T}} & +m_{b_k}\widetilde{\mathbf{U}}_{\mathbf{a}b_k}\widetilde{d}_{b_k} & \\
\widetilde{\mathbf{U}}_{\mathbf{ac}_k}\widetilde{\mathbf{D}}_{\mathbf{cc}_k}\widetilde{\mathbf{U}}_{\mathbf{ac}_k}^{\mathsf{T}} & & \\
\hdashline
m_{b_k}\widetilde{d}_{b_k}\widetilde{\mathbf{U}}_{\mathbf{a}b_k}^{\mathsf{T}} & m_{b_k}^2\widetilde{\mathbf{U}}_{b\mathbf{c}_k}\widetilde{\mathbf{D}}_{\mathbf{cc}_k}\widetilde{\mathbf{U}}_{b\mathbf{c}_k}^{\mathsf{T}} & m_{b_k}\widetilde{\mathbf{U}}_{b\mathbf{c}_k}\widetilde{\mathbf{D}}_{\mathbf{cc}_k}\widetilde{\mathbf{U}}_{\mathbf{cc}_k}^{\mathsf{T}} \\
+m_{b_k}\widetilde{\mathbf{U}}_{b\mathbf{c}_k}\widetilde{\mathbf{D}}_{\mathbf{cc}_k}\widetilde{\mathbf{U}}_{\mathbf{ac}_k}^{\mathsf{T}} & +m_{b_k}^2\widetilde{d}_{b_k} + q_{b_k} & \\
\hdashline
\widetilde{\mathbf{U}}_{\mathbf{cc}_k}\widetilde{\mathbf{D}}_{\mathbf{cc}_k}\widetilde{\mathbf{U}}_{\mathbf{ac}_k}^{\mathsf{T}} & m_{b_k}\widetilde{\mathbf{U}}_{\mathbf{cc}_k}\widetilde{\mathbf{D}}_{\mathbf{cc}_k}\widetilde{\mathbf{U}}_{b\mathbf{c}_k}^{\mathsf{T}} & \widetilde{\mathbf{U}}_{\mathbf{cc}_k}\widetilde{\mathbf{D}}_{\mathbf{cc}_k}\widetilde{\mathbf{U}}_{\mathbf{cc}_k}^{\mathsf{T}}
\end{array}\right]
\end{aligned} \tag{B.11}
$$

Equating the components in Eqs. [\(B.10\)](#page-149-2) and [\(B.11\)](#page-149-3), from the (1,3) and (3,3) element, we find

$$
\breve{\mathbf{U}}_{\mathbf{ac}_k} = \widetilde{\mathbf{U}}_{\mathbf{ac}_k}, \qquad \breve{\mathbf{D}}_{\mathbf{cc}_k} = \widetilde{\mathbf{D}}_{\mathbf{cc}_k}, \qquad \breve{\mathbf{U}}_{\mathbf{cc}_k}^{\mathsf{T}} = \widetilde{\mathbf{U}}_{\mathbf{cc}_k}^{\mathsf{T}} \tag{B.12}
$$

From the (2,3) element we get,

<span id="page-149-4"></span>
$$
\breve{\mathbf{U}}_{b\mathbf{c}_k} = m_{b_k}\widetilde{\mathbf{U}}_{b\mathbf{c}_k} \tag{B.13}
$$

From the (2,2) element and using the results of Eq. [\(B.13\)](#page-149-4), we find that

$$
\breve{d}_{b_k} = m_{b_k}^2\widetilde{d}_{b_k} + q_{b_k} \tag{B.14}
$$

The (2,1) element yields

$$
\breve{\mathbf{U}}_{\mathbf{a}b_k} = m_{b_k}\frac{\widetilde{d}_{b_k}}{\breve{d}_{b_k}}\widetilde{\mathbf{U}}_{\mathbf{a}b_k} \tag{B.15}
$$

What finally remains is the (1,1) element and it is on this we focus. Using the relations in the previous equations, we find that

<span id="page-150-1"></span>
$$
\breve{\mathbf{U}}_{\mathbf{aa}_k}\breve{\mathbf{D}}_{\mathbf{aa}_k}\breve{\mathbf{U}}_{\mathbf{aa}_k}^{\mathsf{T}} = \widetilde{\mathbf{U}}_{\mathbf{aa}_k}\widetilde{\mathbf{D}}_{\mathbf{aa}_k}\widetilde{\mathbf{U}}_{\mathbf{aa}_k}^{\mathsf{T}} + \left[\widetilde{d}_{b_k} - m_{b_k}^2\frac{\widetilde{d}_{b_k}}{\breve{d}_{b_k}}\right]\widetilde{\mathbf{U}}_{\mathbf{a}b_k}\widetilde{\mathbf{U}}_{\mathbf{a}b_k}^{\mathsf{T}} \tag{B.16}
$$

The term in the bracket can be simplified as

$$
\left[\widetilde{d}_{b_k} - m_{b_k}^2\frac{\widetilde{d}_{b_k}}{\breve{d}_{b_k}}\right] = \frac{m_{b_k}^2\widetilde{d}_{b_k}^2 + q_{b_k}\widetilde{d}_{b_k} - m_{b_k}^2\widetilde{d}_{b_k}^2}{m_{b_k}^2\widetilde{d}_{b_k} + q_{b_k}} = \frac{\widetilde{d}_{b_k}q_{b_k}}{m_{b_k}^2\widetilde{d}_{b_k} + q_{b_k}} = \frac{\widetilde{d}_{b_k}q_{b_k}}{\breve{d}_{b_k}} \tag{B.17}
$$

so Eq. [\(B.16\)](#page-150-1) becomes

<span id="page-150-2"></span>
$$
\breve{\mathbf{U}}_{\mathbf{aa}_k}\breve{\mathbf{D}}_{\mathbf{aa}_k}\breve{\mathbf{U}}_{\mathbf{aa}_k}^{\mathsf{T}} = \widetilde{\mathbf{U}}_{\mathbf{aa}_k}\widetilde{\mathbf{D}}_{\mathbf{aa}_k}\widetilde{\mathbf{U}}_{\mathbf{aa}_k}^{\mathsf{T}} + \left(\frac{\widetilde{d}_{b_k}q_{b_k}}{\breve{d}_{b_k}}\right)\widetilde{\mathbf{U}}_{\mathbf{a}b_k}\widetilde{\mathbf{U}}_{\mathbf{a}b_k}^{\mathsf{T}} \tag{B.18}
$$

We note that $\widetilde{\mathbf{U}}_{\mathbf{a}b_k}$ is a column vector so Eq. [\(B.18\)](#page-150-2), and hence is of rank 1, constitutes a 'rank one' update. Since $\breve{d}_{b_k}$, $\widetilde{d}_{b_k}$ and $q_{b_k}$ are all positive (assuming $m_{b_k}$ is a positive quantity), we can use the Agee-Turner Rank One update [[1](16-bibliography.md#page-170-16)]. It should be pointed out that as the algorithm proceeds down the 'list' of parameters, the size of the states $\mathbf{a}$ increases by one (and consequently the size of the parameters $\mathbf{c}$ decreases by one. Hence $\breve{\mathbf{U}}_{\mathbf{aa}_k}$ and $\breve{\mathbf{D}}_{\mathbf{aa}_k}$ begin with a dimension of $n_{\mathbf{x}}$ and conclude with dimension $n_{\mathbf{x}} + n_{\mathbf{p}} - 1$.

Therefore, this is done recursively for all the (sensor) parameters $\mathbf{p}$ which are of size $n_{\mathbf{p}}$.

## B.3. The Agee-Turner Rank-One Update

<span id="page-150-0"></span>In trying to get an efficient algorithm for performing the time update of the covariance matrix, we were faced with Eq. [\(8.41\)](08-factorization-methods.md#page-101-1), which is of the form

$$
\widetilde{\mathbf{U}}\widetilde{\mathbf{D}}\widetilde{\mathbf{U}}^{\mathsf{T}} = \mathbf{U}\mathbf{D}\mathbf{U}^{\mathsf{T}} + c\,\mathbf{x}\mathbf{x}^{\mathsf{T}} \tag{B.19}
$$

This is called a 'rank one' update because we are updating the matrix factors $\mathbf{U}$ and $\mathbf{D}$ based upon products of $\mathbf{x}$ which is of rank 1.

In order to reduce the number of mathematical operations (adds/subtracts, multiplies and divides), for the case of parameter or ECRV/First-order Gauss Markov processes, for sensor parameters, we consider the rank-one update first introduced by Agee and Turner (of the White Sands Missile Range (WSMR)) in 1972.

Consider a covariance matrix update of the form,

$$
\widetilde{\mathbf{P}} = \mathbf{P} + c\,\mathbf{x}\mathbf{x}^{\mathsf{T}} \tag{B.20}
$$

or

$$
\widetilde{\mathbf{U}}\widetilde{\mathbf{D}}\widetilde{\mathbf{U}}^{\mathsf{T}} = \mathbf{U}\mathbf{D}\mathbf{U}^{\mathsf{T}} + c\,\mathbf{x}\mathbf{x}^{\mathsf{T}} \tag{B.21}
$$

so, $\widetilde{p}_{ij}$ can be expressed (and defined) as

<span id="page-150-3"></span>
$$
\widetilde{p}_{ij} \triangleq \sum_{k=j}^{n}\widetilde{u}_{ik}\widetilde{d}_{kk}\widetilde{u}_{jk} = \sum_{k=j}^{n}u_{ik}d_{kk}u_{jk} + cx_ix_j \tag{B.22}
$$

and

$$
\widetilde{p}_{ii} = \sum_{k=i}^{n}\widetilde{u}_{ik}^2\widetilde{d}_{kk} = \sum_{k=i}^{n}u_{ik}^2d_{kk} + cx_i^2 \tag{B.23}
$$

We recall that $\widetilde{u}_{ii} = u_{ii} = 1$ and thus, for an $n \times n$ matrix, for $j = n$ (i.e. the last column),

$$
\widetilde{d}_{nn} = d_{nn} + c\,x_n^2 \tag{B.24}
$$

$$
\widetilde{p}_{in} = \widetilde{u}_{in}\widetilde{d}_{nn}\widetilde{u}_{nn} = d_{nn}u_{in}u_{nn} + cx_ix_n \tag{B.25}
$$

so that

<span id="page-151-0"></span>
$$
\widetilde{u}_{in} = \frac{1}{\widetilde{d}_{nn}}\left(d_{nn}u_{in} + cx_ix_n\right) \tag{B.26}
$$

The second-to-the-last ($n-1$-th) column of $\mathbf{U}$ can now be can be operated on, by means of the following decomposition of Eq. [\(B.22\)](#page-150-3), as

<span id="page-151-1"></span>
$$
\sum_{k=j}^{n-1}\widetilde{u}_{ik}\widetilde{d}_{kk}\widetilde{u}_{jk} + \widetilde{u}_{in}\widetilde{d}_{nn}\widetilde{u}_{jn} = \sum_{k=j}^{n-1}u_{ik}d_{kk}u_{jk} + u_{in}d_{nn}u_{jn} + cx_ix_j \tag{B.27}
$$

which leads to

$$
\sum_{k=j}^{n-1}\widetilde{u}_{ik}\widetilde{d}_{kk}\widetilde{u}_{jk} = \sum_{k=j}^{n-1}u_{ik}d_{kk}u_{jk} + \Upsilon_n \tag{B.28}
$$

If we work on the terms outside the two summations, using Eq. [\(B.26\)](#page-151-0) for $\widetilde{u}_{in}$ and $\widetilde{u}_{jn}$, $\Upsilon_n$ becomes

$$
\begin{aligned}
\Upsilon_n &= -\widetilde{u}_{in}\widetilde{d}_{nn}\widetilde{u}_{jn} + u_{in}d_{nn}u_{jn} + cx_ix_j \\
&= -\frac{1}{\widetilde{d}_{nn}}\left[d_{nn}u_{in} + cx_ix_n\right]\left[d_{nn}u_{jn} + cx_jx_n\right] \\
&\quad + \frac{d_{nn} + c\,x_n^2}{\widetilde{d}_{nn}}\left(u_{in}d_{nn}u_{jn} + cx_ix_j\right) \\
&= \frac{1}{\widetilde{d}_{nn}}\big[-c\,d_{nn}u_{jn}x_nx_i - c\,d_{nn}u_{in}x_nx_j + c\,d_{nn}x_ix_j + c\,d_{nn}x_n^2u_{in}u_{jn}\big) \\
&= \frac{c\,d_{nn}}{\widetilde{d}_{nn}}\left(x_i - u_{in}x_n\right)\left(x_j - u_{jn}x_n\right)
\end{aligned} \tag{B.29}
$$

Therefore, Eq. [\(B.27\)](#page-151-1) can be written as

<span id="page-151-2"></span>
$$
\sum_{k=j}^{n-1}\widetilde{u}_{ik}\widetilde{d}_{kk}\widetilde{u}_{jk} = \sum_{k=j}^{n-1}u_{ik}d_{kk}u_{jk} + \frac{c\,d_{nn}}{\widetilde{d}_{nn}}\left(x_i - u_{in}x_n\right)\left(x_j - u_{jn}x_n\right) \tag{B.30}
$$

Now, if we operate a bit more on the quantity $\widetilde{u}_{in}$, we find from Eq. [\(B.26\)](#page-151-0), that we get

$$
\widetilde{u}_{in} = \frac{d_{nn}}{\widetilde{d}_{nn}}u_{in} + \frac{c}{\widetilde{d}_{nn}}x_ix_n \tag{B.31}
$$

$$
= \frac{\widetilde{d}_{nn} - c\,x_n^2}{\widetilde{d}_{nn}}u_{in} + \frac{c}{\widetilde{d}_{nn}}x_ix_n \tag{B.32}
$$

$$
= u_{in} + \left(x_i - u_{in}x_n\right)\frac{c\,x_n}{\widetilde{d}_{nn}} \tag{B.33}
$$

and if we define $\alpha_i$ and $v_n$ as

$$
\alpha_i \triangleq \left(x_i - u_{in}x_n\right) \tag{B.34}
$$

$$
v_n \triangleq \frac{c\,x_n}{\widetilde{d}_{nn}} \tag{B.35}
$$

$\widetilde{u}_{in}$ can be rewritten as

$$
\widetilde{u}_{in} = u_{in} + \alpha_i\,v_n \tag{B.36}
$$

If we want to generalize this, we can write Eq. [\(B.30\)](#page-151-2) as

<span id="page-152-0"></span>
$$
\sum_{k=j}^{n-1}\widetilde{u}_{ik}\widetilde{d}_{kk}\widetilde{u}_{jk} = \sum_{k=j}^{n-1}u_{ik}d_{kk}u_{jk} + \mathcal{C}^n\mathcal{X}_i^n\mathcal{X}_j^n \tag{B.37}
$$

where

$$
\mathcal{C}^n \triangleq \frac{c\,d_{nn}}{\widetilde{d}_{nn}} \tag{B.38}
$$

$$
\mathcal{X}_i^n \triangleq x_i - u_{in}x_n \tag{B.39}
$$

with

$$
\begin{aligned}
\widetilde{u}_{in} &= u_{in} + \alpha_i^n\,v_n \\
\alpha_i^n &= x_i - u_{in}x_n \\
v_n &= \frac{c\,x_n}{\widetilde{d}_{nn}} \\
\widetilde{d}_{nn} &= d_{nn} + c\,x_n^2
\end{aligned}
$$

Thus, for the third-to-the-last column ($j = n-2$), we expand Eq. [\(B.37\)](#page-152-0) as

$$
\begin{aligned}
\sum_{k=j}^{n-2}\widetilde{u}_{ik}\widetilde{d}_{kk}\widetilde{u}_{jk} + \widetilde{u}_{i,n-1}\widetilde{d}_{n-1,n-1}\widetilde{u}_{j,n-1} &= \sum_{k=j}^{n-2}u_{ik}d_{kk}u_{jk} \\
&\quad + u_{i,n-1}d_{n-1,n-1}u_{j,n-1} \\
&\quad + \mathcal{C}^n\mathcal{X}_i^n\mathcal{X}_j^n
\end{aligned} \tag{B.40}
$$

which produces

$$
\begin{aligned}
\sum_{k=j}^{n-2}\widetilde{u}_{ik}\widetilde{d}_{kk}\widetilde{u}_{jk} &= \sum_{k=j}^{n-2}u_{ik}d_{kk}u_{jk} \\
&\quad + \frac{\mathcal{C}^n d_{n-1,n-1}}{\widetilde{d}_{n-1,n-1}}\left[\mathcal{X}_i^n - u_{i,n-1}\mathcal{X}_n^n\right]\left[\mathcal{X}_j^n - u_{j,n-1}\mathcal{X}_n^n\right]
\end{aligned} \tag{B.41}
$$

so that using the same machinery as above, we get

$$
\sum_{k=j}^{n-2}\widetilde{u}_{ik}\widetilde{d}_{kk}\widetilde{u}_{jk} = \sum_{k=j}^{n-2}u_{ik}d_{kk}u_{jk} + \mathcal{C}^{n-1}\mathcal{X}_i^{n-1}\mathcal{X}_j^{n-1} \tag{B.42}
$$

$$
\mathcal{C}^{n-1} = \frac{\mathcal{C}^n\,d_{n-1,n-1}}{\widetilde{d}_{n-1,n-1}} \tag{B.43}
$$

$$
\mathcal{X}_i^{n-1} = \alpha_i^{n-1} = \mathcal{X}_i^n - u_{i,n-1}\,\mathcal{X}_n^n \tag{B.44}
$$

$$
v_{n-1} = \frac{\mathcal{C}^n\,\mathcal{X}_i^n}{\widetilde{d}_{n-1,n-1}} \tag{B.45}
$$

$$
\widetilde{u}_{i,n-1} = u_{i,n-1} + \mathcal{X}_i^{n-1}\,v_{n-1} \tag{B.46}
$$

$$
\widetilde{d}_{n-1,n-1} = d_{n-1,n-1} + \mathcal{C}^n\,x_{n-1}^2 \tag{B.47}
$$

We also are reminded that $\widetilde{u}_{i,i} = 1$.

## B.4. Decorrelating Measurements

<span id="page-153-0"></span>We normalize the (original) measurement equation

$$
\mathbf{z}_{orig} = \mathbf{H}_{orig}\mathbf{x} + \boldsymbol{\nu}_{orig} \tag{B.48}
$$

where the measurement noise has statistics

$$
E[\boldsymbol{\nu}_{orig}] = \mathbf{0} \tag{B.49}
$$

$$
E[\boldsymbol{\nu}_{orig}\boldsymbol{\nu}_{orig}^{\mathsf{T}}] = \mathbf{R}_{orig} \tag{B.50}
$$

where $\mathbf{R}_{orig}$ is the measurement noise.

We now change variables so that

$$
\mathbf{z} \triangleq \mathbf{R}_{orig}^{-1/2}\mathbf{z}_{orig} \tag{B.51}
$$

$$
\mathbf{H} \triangleq \mathbf{R}_{orig}^{-1/2}\mathbf{H}_{orig} \tag{B.52}
$$

$$
\boldsymbol{\nu} \triangleq \mathbf{R}_{orig}^{-1/2}\boldsymbol{\nu}_{orig} \tag{B.53}
$$

where $\mathbf{R}_{orig}^{-1/2}$ is the inverse of the Cholesky factor of $\mathbf{R}_{orig}$ ($= \mathbf{R}_{orig}^{1/2}\mathbf{R}_{orig}^{T/2}$). With this, the new normalized measurement equation is

$$
\mathbf{z} = \mathbf{H}\mathbf{x} + \boldsymbol{\nu} \tag{B.54}
$$

where $E[\boldsymbol{\nu}] = \mathbf{0}$ and $E[\boldsymbol{\nu}\boldsymbol{\nu}^{\mathsf{T}}] = \mathbf{I}$. This is sometimes referred to as **pre-whitening** or *decorrelation*, because if the original measurements were correlated, the normalized measurements are now uncorrelated (via the Cholesky decomposition of $\mathbf{R}_{orig}$).

Alternatively, we can decorrelate the measurements by using a UDU factorization on the measurement noise covariance matrix as

$$
\mathbf{R}_{orig} = \mathbf{U}_R\mathbf{D}_R\mathbf{U}_R^{\mathsf{T}} \tag{B.55}
$$

so that the measurement equation, the measurement partial and the measurement noise are

$$
\mathbf{z} \triangleq \mathbf{U}_R^{-1}\mathbf{z}_{orig} \tag{B.56}
$$

$$
\mathbf{H} \triangleq \mathbf{U}_R^{-1}\mathbf{H}_{orig} \tag{B.57}
$$

$$
\boldsymbol{\nu} \triangleq \mathbf{U}_R^{-1}\boldsymbol{\nu}_{orig} \tag{B.58}
$$

where the new/modified measurement equation is now uncorrelated with $E[\boldsymbol{\nu}] = \mathbf{0}$ and $E[\boldsymbol{\nu}\boldsymbol{\nu}^{\mathsf{T}}] = \mathbf{D}_R$.

## B.5. The Carlson Rank-One Update

<span id="page-153-1"></span>The Carlson rank-one update [[9](16-bibliography.md#page-170-21)], introduced in 1973, addresses the problem of updating the covariance due to a loss of precision involved in the differencing of two positive quantities which are nearly equal. In particular, the diagonal elements $d_{ii}$ have the potential of going negative in certain cases if the Agee-Turner rank-one update is blindly used. Thankfully, we resort to the *Carlson rank-one update* to compute the measurement update without losing numerical precision.

We recall that $\alpha$ and $\mathbf{v}$ were defined earlier. We also define the $n \times 1$ vector $\mathbf{f}$ as

$$
\mathbf{f} \triangleq \mathbf{U}^{-\mathsf{T}}\mathbf{H}^{\mathsf{T}} \tag{B.59}
$$

Therefore, since $\mathbf{f}$ is an $n \times 1$ vector and $\mathbf{D}$ is a diagonal matrix, we can express $\alpha$ as

$$
\alpha = \alpha_n = R + \sum_{i=1}^{n}f_i^2d_{ii} \tag{B.60}
$$

so that

$$
\alpha_j = R + \sum_{i=1}^{j}f_i^2d_{ii} = \alpha_{j-1} + f_j^2d_{jj} \tag{B.61}
$$

Since $\mathbf{v}$ can be written as

$$
\mathbf{v} = \mathbf{D}\mathbf{f} \tag{B.62}
$$

we can also write

$$
v_j = d_{jj}f_j \tag{B.63}
$$

and we can write $\alpha_j$ as

<span id="page-154-3"></span>
$$
\alpha_j = \alpha_{j-1} + \frac{v_j^2}{d_{jj}} \tag{B.64}
$$

$$
\widetilde{\mathbf{U}}_k\widetilde{\mathbf{D}}_k\widetilde{\mathbf{U}}_k^{\mathsf{T}} \triangleq \mathbf{a}r\mathbf{D} - \frac{1}{\alpha}\mathbf{v}\mathbf{v}^{\mathsf{T}} \tag{B.65}
$$

which can be rewritten as:

$$
\widetilde{\mathbf{U}}_k\widetilde{\mathbf{D}}_k\widetilde{\mathbf{U}}_k^{\mathsf{T}} \triangleq \mathbf{a}r\mathbf{U}\mathbf{a}r\mathbf{D}\mathbf{a}r\mathbf{U}^{\mathsf{T}} - \frac{1}{\alpha}\mathbf{v}\mathbf{v}^{\mathsf{T}} \tag{B.66}
$$

where $\mathbf{a}r\mathbf{U} = \mathbf{I}$. Following the reasoning in the description for the Rank-One update earlier in this Appendix,

<span id="page-154-0"></span>
$$
\widetilde{p}_{ij} \triangleq \sum_{k=j}^{n}\widetilde{u}_{ik}\widetilde{d}_{kk}\widetilde{u}_{jk} = -\frac{1}{\alpha}v_iv_j \tag{B.67}
$$

and

<span id="page-154-1"></span>
$$
\widetilde{p}_{ii} = \sum_{k=i}^{n}\widetilde{u}_{ik}^2\widetilde{d}_{kk} = d_{ii} - \frac{1}{\alpha}v_i^2 \tag{B.68}
$$

For $j = n$, Eq. [\(B.67\)](#page-154-0) becomes

$$
\widetilde{u}_{in}\widetilde{d}_{nn}\widetilde{u}_{nn} = -\frac{1}{\alpha}v_iv_n \tag{B.69}
$$

and from Eq. [\(B.68\)](#page-154-1),

$$
\widetilde{u}_{nn}^2\widetilde{d}_{nn} = d_{nn} - \frac{1}{\alpha}v_n^2 \tag{B.70}
$$

Recalling that $\widetilde{u}_{nn} = 1$, we get

$$
\widetilde{d}_{nn} = d_{nn} - \frac{1}{\alpha}v_n^2 \tag{B.71}
$$

and

<span id="page-154-2"></span>
$$
\widetilde{u}_{in} = -\frac{1}{\alpha\widetilde{d}_{nn}}v_iv_n \tag{B.72}
$$

So, Eq. [\(B.67\)](#page-154-0) can be written as

<span id="page-155-5"></span>
$$
\sum_{k=j}^{n-1}\widetilde{u}_{ik}\widetilde{d}_{kk}\widetilde{u}_{jk} + \widetilde{u}_{in}\widetilde{d}_{nn}\widetilde{u}_{jn} = -\frac{1}{\alpha}v_iv_j \tag{B.73}
$$

Substituting for $\widetilde{u}_{in}$ and $\widetilde{u}_{in}$ from Eq. [\(B.72\)](#page-154-2), we find

<span id="page-155-0"></span>
$$
\sum_{k=j}^{n-1}\widetilde{u}_{ik}\widetilde{d}_{kk}\widetilde{u}_{jk} = -\frac{1}{\alpha}\left[1 + \frac{1}{\alpha\widetilde{d}_{nn}}v_n^2\right]v_iv_j \tag{B.74}
$$

But since

$$
\left[1 + \frac{1}{\alpha\widetilde{d}_{nn}}v_n^2\right] = \frac{d_{nn}}{\widetilde{d}_{nn}} \tag{B.75}
$$

Eq. [\(B.74\)](#page-155-0) becomes

<span id="page-155-1"></span>
$$
\sum_{k=j}^{n-1}\widetilde{u}_{ik}\widetilde{d}_{kk}\widetilde{u}_{jk} = -\frac{1}{\alpha}\frac{d_{nn}}{\widetilde{d}_{nn}}v_iv_j \tag{B.76}
$$

So, we can expand Eq. [\(B.76\)](#page-155-1) as

<span id="page-155-4"></span>
$$
\sum_{k=j}^{n-2}\widetilde{u}_{ik}\widetilde{d}_{kk}\widetilde{u}_{jk} + \widetilde{u}_{i,n-1}\widetilde{d}_{n-1,n-1}\widetilde{u}_{j,n-1} = -\frac{1}{\alpha}\frac{d_{nn}}{\widetilde{d}_{nn}}v_iv_j \tag{B.77}
$$

We need to obtain $\widetilde{u}_{i,n-1}$ and $\widetilde{d}_{n-1,n-1}$. First we work on $\widetilde{u}_{i,n-1}\widetilde{d}_{n-1,n-1}$ from Eq. [\(B.67\)](#page-154-0) with $i = n-1$ as follows:

$$
\widetilde{u}_{n-1,n-1}^2\widetilde{d}_{n-1,n-1} + \widetilde{u}_{n-1,n}^2\widetilde{d}_{n,n} = d_{n-1} - \frac{1}{\alpha}v_{n-1}^2 \tag{B.78}
$$

Recalling that $\widetilde{u}_{n-1,n-1} = 1$ and $\widetilde{u}_{n-1,n}$ was obtained (with $i = n-1$) in Eq. [\(B.72\)](#page-154-2), we get

$$
\widetilde{d}_{n-1,n-1} = d_{n-1,n-1} - \frac{1}{\alpha}\left[1 + \frac{1}{\alpha\widetilde{d}_{n,n}}v_n^2\right]v_{n-1}^2 \tag{B.79}
$$

Knowing that

<span id="page-155-3"></span>
$$
\left[1 + \frac{1}{\alpha\widetilde{d}_{n,n}}v_n^2\right] = \frac{d_{n,n}}{\widetilde{d}_{n,n}} \tag{B.80}
$$

$\widetilde{d}_{n-1,n-1}$ becomes

<span id="page-155-2"></span>
$$
\widetilde{d}_{n-1,n-1} = d_{n-1,n-1} - \frac{1}{\alpha}\left(\frac{d_{n,n}}{\widetilde{d}_{n,n}}\right)v_{n-1}^2 \tag{B.81}
$$

Now we work on $\widetilde{u}_{i,n-1}$. We recall that from Eq. [\(B.68\)](#page-154-1), with $j = n-1$, we find that

$$
\widetilde{u}_{i,n-1}\widetilde{d}_{n-1,n-1}\widetilde{u}_{n-1,n-1} + \widetilde{u}_{i,n}\widetilde{d}_{n,n}\widetilde{u}_{n-1,n} = -\frac{1}{\alpha}v_iv_{n-1} \tag{B.82}
$$

We substitute for $\widetilde{d}_{n-1,n-1}$ from Eq. [\(B.81\)](#page-155-2), for $\widetilde{u}_{i,n}$ and $\widetilde{u}_{n-1,n}$ from Eq. [\(B.72\)](#page-154-2) and noting that $\widetilde{u}_{n-1,n-1} = 1$, we get

$$
\widetilde{u}_{i,n-1} = -\frac{1}{\alpha\widetilde{d}_{n-1,n-1}}\left[1 + \frac{1}{\alpha\widetilde{d}_{n,n}}v_n^2\right]v_iv_{n-1} \tag{B.83}
$$

Using Eq. [\(B.80\)](#page-155-3), $\widetilde{u}_{i,n-1}$ becomes

$$
\widetilde{u}_{i,n-1} = -\frac{1}{\alpha\widetilde{d}_{n-1,n-1}}\left(\frac{d_{n,n}}{\widetilde{d}_{n,n}}\right)v_iv_{n-1} \tag{B.84}
$$

With this in mind, we are now prepared to work on Eq. [\(B.77\)](#page-155-4), and we find that

$$
\begin{aligned}
\sum_{k=j}^{n-2}\widetilde{u}_{ik}\widetilde{d}_{kk}\widetilde{u}_{jk} &= -\left(\frac{d_{n,n}}{\alpha\widetilde{d}_{n,n}}\right)\left[\frac{d_{n,n}}{\alpha\widetilde{d}_{n,n}}v_{n-1}^2 - 1\right]v_iv_j \\
&= -\left(\frac{d_{n,n}}{\alpha\widetilde{d}_{n,n}}\right)\left(\frac{d_{n-1,n-1}}{\widetilde{d}_{n-1,n-1}}\right)v_iv_j
\end{aligned} \tag{B.85}
$$

This has the same form as Eq. [\(B.73\)](#page-155-5), so this suggests a recursion as follows:

With $\mathcal{C}_n = -1/\alpha$ for $j = n, \cdots, 1$:

<span id="page-156-0"></span>
$$
\widetilde{d}_{jj} = d_{jj} + \mathcal{C}^jv_j^2 \tag{B.86}
$$

$$
\widetilde{u}_{ij} = \mathcal{C}^jv_iv_j/\widetilde{d}_{jj}, \quad k = 1, \cdots, j-1 \tag{B.87}
$$

$$
C^{j-1} = C^jd_{jj}/\widetilde{d}_{jj} \tag{B.88}
$$

From Eq. [\(B.86\)](#page-156-0), we get

$$
\widetilde{d}_{jj} = d_{jj} + \mathcal{C}^jv_j^2
$$

and from Eq. [\(B.88\)](#page-156-0), we find that

$$
\mathcal{C}^{j-1} = \mathcal{C}^j\frac{d_{jj}}{\widetilde{d}_{jj}} = \frac{\mathcal{C}^jd_{jj}}{d_{jj} + C^jv_j^2} = \frac{d_{jj}}{\frac{d_{jj}}{\mathcal{C}^j} + v_j^2} \tag{B.89}
$$

This can be written as

$$
\frac{1}{\mathcal{C}^{j-1}} = \frac{1}{\mathcal{C}^j} + \frac{v_j^2}{d_{jj}} \tag{B.90}
$$

or

<span id="page-156-1"></span>
$$
-\frac{1}{\mathcal{C}^j} = -\frac{1}{\mathcal{C}^{j-1}} + \frac{v_j^2}{d_{jj}} \tag{B.91}
$$

Comparing Eqs. [\(B.64\)](#page-154-3) and Eq. [\(B.91\)](#page-156-1) we find that

<span id="page-156-3"></span>
$$
\alpha_j = -\frac{1}{\mathcal{C}^j} \tag{B.92}
$$

Using this equation, we find that

<span id="page-156-2"></span>
$$
\widetilde{d}_{jj} = d_{jj}\left(\frac{\alpha_{j-1}}{\alpha_j}\right) \tag{B.93}
$$

From Eq. [\(B.87\)](#page-156-0) and using Eqs. [\(B.93\)](#page-156-2) and [\(B.92\)](#page-156-3), we can express $\widetilde{u}_{ij}$ as

$$
\widetilde{u}_{ij} = -\frac{v_iv_j}{d_{jj}\alpha_{j-1}} \tag{B.94}
$$

Recalling that $v_j = d_{jj}f_j$,

$$
\widetilde{u}_{ij} = -\frac{v_if_j}{\alpha_{j-1}} \tag{B.95}
$$

If we define $\lambda_j$ as

$$
\lambda_j \triangleq -\frac{f_j}{\alpha_{j-1}} \tag{B.96}
$$

$\widetilde{u}_{ij}$ becomes

$$
\widetilde{u}_{ij} = \lambda_jv_i \tag{B.97}
$$

$\widetilde{U}_{ij}$ has the structure

$$
\widetilde{\mathbf{U}}_k = \begin{bmatrix}
1 & \lambda_2v_1 & \lambda_3v_1 & \lambda_4v_1 & \cdots & \lambda_nv_1 \\
0 & 1 & \lambda_3v_2 & \lambda_4v_2 & \cdots & \lambda_nv_2 \\
0 & 0 & 1 & \lambda_4v_3 & \cdots & \lambda_nv_3 \\
0 & 0 & 0 & 1 & \cdots & \lambda_nv_4 \\
\vdots & \vdots & \vdots & \vdots & \vdots & \vdots \\
0 & 0 & 0 & 0 & \cdots & 1
\end{bmatrix} \tag{B.98}
$$

We can rewrite $\widetilde{\mathbf{U}}$ as

$$
\widetilde{\mathbf{U}}_k = \mathbf{I}_n + \begin{bmatrix} \mathbf{0}_{n\times 1} & \lambda_2\mathbf{v}^{(1)} & \lambda_3\mathbf{v}^{(2)} & \lambda_4\mathbf{v}^{(3)} & \cdots & \lambda_n\mathbf{v}^{(n-1)} \end{bmatrix} \tag{B.99}
$$

where $\mathbf{v}^{(j)}$ is an $n \times 1$ vector defined as

$$
\mathbf{v}^{(j)} \triangleq \begin{bmatrix} v_1 & v_2 & v_3 & \cdots & v_j & 0 & \cdots & 0 \end{bmatrix}^{\mathsf{T}} \tag{B.100}
$$

We recall that

$$
\mathbf{U}\mathbf{D}\mathbf{U}^{\mathsf{T}} = \mathbf{U}^{-}\left[\mathbf{D}^{-} - \frac{1}{\alpha}\mathbf{v}\mathbf{v}^{\mathsf{T}}\right]\mathbf{a}r\mathbf{U}^{\mathsf{T}}
$$

and

$$
\widetilde{\mathbf{U}}_k\widetilde{\mathbf{D}}_k\widetilde{\mathbf{U}}_k^{\mathsf{T}} \triangleq \mathbf{D}^{-} - \frac{1}{\alpha}\mathbf{v}\mathbf{v}^{\mathsf{T}}
$$

and

$$
\mathbf{U} = \mathbf{U}^{-}\widetilde{\mathbf{U}}_k \qquad \text{and} \qquad \mathbf{D} = \widetilde{\mathbf{D}}
$$

With this in mind, $\mathbf{U}$ is

$$
\mathbf{U} = \mathbf{U}^{-} + \mathbf{U}^{-}\begin{bmatrix} \mathbf{0}_{n\times 1} & \lambda_2\mathbf{v}^{(1)} & \lambda_3\mathbf{v}^{(3)} & \lambda_4\mathbf{v}^{(3)} & \cdots & \lambda_n\mathbf{v}^{(n-1)} \end{bmatrix} \tag{B.101}
$$

If we denote $\mathbf{U}^{(j)}$ and $\mathbf{U}^{-j}$ as the $j$th columns of $\mathbf{U}$ and $\mathbf{U}^{-}$, respectively, we find that

$$
\mathbf{U}^{(j)} = \mathbf{U}^{-j} + \lambda_j\overline{\mathbf{K}}_{j-1} \tag{B.102}
$$

where

$$
\overline{\mathbf{K}}_j = \mathbf{U}^{-}\mathbf{v}^{(j)} = \overline{\mathbf{K}}_{j-1} + v_j\mathbf{U}^{-j} \quad \text{with} \quad \overline{\mathbf{K}}_0 = \mathbf{0}_{n\times 1} \tag{B.103}
$$

Finally,

$$
\mathbf{K} = \frac{1}{\alpha_n}\overline{\mathbf{K}}_n \tag{B.104}
$$

---

[← Appendix A. Models and Realizations of Random Variables](13-appendix-a-models-and-realizations-of-random-variables.md) · [Contents](README.md) · [Appendix C. An Analysis of Dual Inertial-Absolute and Inertial-Relative Navigation Filters →](15-appendix-c-an-analysis-of-dual-inertial-absolute-and-inertial-relative.md)
