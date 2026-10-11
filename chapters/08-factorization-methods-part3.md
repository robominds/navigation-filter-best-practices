[← Chapter 8. Factorization Methods (part 2 of 3)](08-factorization-methods-part2.md) · [Contents](README.md) · [Chapter 9. Attitude Estimation (part 1 of 2) →](09-attitude-estimation-part1.md)

*Chapter 8. Factorization Methods, continued*

#### The Agee-Turner Rank One Update Algorithm

Appendix [B.3](14-appendix-b-the-mathematics-behind-the-udu-factorization-part2.md#page-150-0) contains the development of the Agee-Turner Rank-One update which is the key to reducing the numerical operations on the UDU Time Update. Given $`{𝐔}`$ and $`{𝐃}`$, along with $`c`$, and the vector $`{𝐱}`$, we are interested in obtaining $`\tilde{{𝐔}}`$ and $`\tilde{{𝐃}}`$ along the lines of

```math
\tilde{{𝐔}}\tilde{{𝐃}}\tilde{{𝐔}}^{{𝖳}} = {𝐔}{𝐃}{𝐔}^{{𝖳}} + c\,{𝐱}{𝐱}^{{𝖳}} \qquad\qquad(8.44)
```

where $`c \gt 0`$ is a specified scalar term.

The algorithm to compute $`\tilde{U}_{ij}`$ and $`\tilde{D}_{ii}`$ is:

> $`{𝒞}^n = c`$  
> **for** $`j = n, \cdots, 2`$ **do**  
> &emsp;$`\tilde{D}_{jj} = D_{jj} + {𝒞}^j x_j^2,`$ &emsp; $`[n-1, 2(n-1), 0]`$  
> &emsp;$`\tilde{U}_{jj} = 1`$  
> &emsp;$`\beta_j = {𝒞}^j / \tilde{D}_{jj}`$ &emsp; $`[0, 0, (n-1)]`$  
> &emsp;$`v_j = \beta_j x_j`$ &emsp; $`[0, (n-1), 0]`$  
> &emsp;**for** $`i = 1, \cdots, j-1`$ **do**  
> &emsp;&emsp;$`x_i := x_i - U_{ij}x_j`$ &emsp; $`[\frac{1}{2}(n^2-n), \frac{1}{2}(n^2-n), 0]`$  
> &emsp;&emsp;$`\tilde{U}_{ij} = U_{ij} + x_i v_j`$ &emsp; $`[\frac{1}{2}(n^2-n), \frac{1}{2}(n^2-n), 0]`$  
> &emsp;**end for**  
> &emsp;$`{𝒞}^{j-1} = \beta_j D_{jj}`$ &emsp; $`[0, (n-1), 0]`$  
> **end for**  
> $`\tilde{D}_{11} = D_{11} + {𝒞}^1 x_1^2`$ &emsp; $`[1, 2, 0]`$

This algorithm has $`n^2`$ adds, $`(n^2 + 3n + 2)`$ multiplies and $`n - 1`$ divides.

### 8.3.3. Arithmetic Operations for Time Update

For the time update of the covariance matrix, we have the following arithmetic operations:

```math
\text{Adds}: \quad 1.5n_{{𝐱}}^3 + n_{{𝐱}}^2 m_{{𝐱}} + n_{{𝐱}}^2 n_{{𝐩}} - 0.5n_{{𝐱}}^2 + n_{{𝐩}} + n_{{𝐱}}(n_{{𝐩}}+1)n_{{𝐩}} + \sum_{k=1}^{n_{{𝐩}}} k^2
```

```math
\text{Multiplies}: \quad 0.5n_{{𝐱}}^2(3n_{{𝐱}}+1) + n_{{𝐱}}m_{{𝐱}}(n_{{𝐱}}+1) + (5.5 + 5n_{{𝐱}} + n_{{𝐱}}^2)n_{{𝐩}} + \frac{1}{2}(2n_{{𝐱}}+5)n_{{𝐩}}^2 + \sum_{k=1}^{n_{{𝐩}}} k^2
```

```math
\text{Divides}: \quad (n_{{𝐱}} + m_{{𝐱}})(n_{{𝐱}} - 1) + n_{{𝐩}}
```

For $`n_{{𝐱}} = 9`$, $`m_{{𝐱}} = 9`$, $`n_{{𝐩}} = 26`$, we will utilize 16,407 adds, 19,338 multiplies, and 170 divides. In contrast, if we did the MGS on all 35 states ($`n_{{𝐱}} = 35`$, $`m_{{𝐱}} = 35`$ and $`n_{{𝐩}} = 0`$), we would use 85,750 adds, 88,200 multiplies, and 34 divides. Finally, if the covariance were updated (without any consideration given to the structure of $`{𝚽}_k`$ from $`{𝚽}_k{𝐏}_k^-{𝚽}_k^{{𝖳}} + {𝐐}_k`$) in the conventional manner, with $`n_{{𝐱}} = 35`$, $`m_{{𝐱}} = 35`$, it would cost 84,525 adds, 85,750 multiplies and no divides[<sup>†</sup>](#page-103-1). Thus, a very strong case is made for using the UDU factorization and harnessing the benefit of updating the sensor parameters using the Agee-Turner Rank-One update. Thus, the UDU time update taking advantage of the fact that most of the states are sensor parameters results in nearly **five times fewer** adds and multiplies and 170 more divides that if we operated on the full covariance matrix.

<span id="page-103-1"></span><sup>†</sup> For matrices, $`{𝐀}`$ and $`{𝐁}`$ of dimension $`n \times m`$ and $`m \times p`$, respectively, the product

```math
{𝐂} = {𝐀}{𝐁} \qquad\qquad(8.45)
```

results in $`n(m-1)p`$ adds, $`nmp`$ multiplies and no divides.

## 8.4. The Measurement Update

<span id="page-103-0"></span>The UDU factorization requires that we process the measurements one-at-a-time [[5](16-bibliography.md#page-170-1)]. This should not be construed as a weakness of the formulation. If the measurements are correlated, they can be 'decorrelated' as in Appendix [B.4](14-appendix-b-the-mathematics-behind-the-udu-factorization-part2.md#page-153-0)

We remind ourselves that the covariance update equation is

```math
{𝐏}^+ = {𝐏}^- - {𝐊}{𝐇}{𝐏}^- \qquad\qquad(8.46)
```

where $`{𝐊}`$ is the Kalman Gain matrix, $`{𝐇}`$ is the measurement partial, $`{𝐏}^-`$ is the *a priori* covariance, and $`{𝐏}^+`$ is the *a posteriori* covariance matrix. Using the covariance factors $`{𝐔}`$ and $`{𝐃}`$, we rewrite the above equation as

<span id="page-104-0"></span>
```math
{𝐔}^+{𝐃}^+{𝐔}^{+{𝖳}} = {𝐔}^-{𝐃}^-{𝐔}^{-{𝖳}} - {𝐊}{𝐇}{𝐔}^-{𝐃}^-{𝐔}^{-{𝖳}} \qquad\qquad(8.47)
```

We note that $`{𝐔}`$ and $`{𝐔}^-`$ and $`{𝐃}`$ and $`{𝐃}^-`$ are $`n \times n`$ matrices, and because we are using the paradigm of processing the measurements one at a time, $`{𝐇}`$ is an $`1 \times n`$ vector and $`{𝐊}`$ is an $`n \times 1`$ vector. Recalling that $`{𝐊}`$ is defined as

```math
{𝐊} = {𝐏}^-{𝐇}^{{𝖳}}\left({𝐇}{𝐏}^-{𝐇}^{{𝖳}} + {𝐑}\right)^{-1} = \frac{{𝐔}^-{𝐃}^-{𝐔}^{-{𝖳}}{𝐇}^{{𝖳}}}{{𝐇}{𝐔}^-{𝐃}^-{𝐔}^{-{𝖳}}{𝐇}^{{𝖳}} + {𝐑}} = \frac{{𝐔}^-{𝐃}^-{𝐔}^{-{𝖳}}{𝐇}^{{𝖳}}}{\alpha} \qquad\qquad(8.48)
```

where the scalar $`\alpha`$ is defined to be

```math
\alpha \triangleq {𝐇}{𝐔}^-{𝐃}^-{𝐔}^{-{𝖳}}{𝐇}^{{𝖳}} + {𝐑} \qquad\qquad(8.49)
```

We find that Eq. [\(8.47\)](#page-104-0) becomes

<span id="page-104-1"></span>
```math
{𝐔}^+{𝐃}^+{𝐔}^{+{𝖳}} = {𝐔}^-\left[{𝐃}^- - \frac{{𝐃}^-{𝐔}^{-{𝖳}}{𝐇}^{{𝖳}}}{\alpha}{𝐇}{𝐔}^-{𝐃}^-\right]{𝐔}^{-{𝖳}} \qquad\qquad(8.50)
```

If we define the $`n \times 1`$ vector $`{𝐯}`$ as

```math
{𝐯} \triangleq {𝐃}^-{𝐔}^{-{𝖳}}{𝐇}^{{𝖳}} \qquad\qquad(8.51)
```

Eq. [\(8.50\)](#page-104-1) becomes

<span id="page-104-2"></span>
```math
{𝐔}^+{𝐃}^+{𝐔}^{+{𝖳}} = {𝐔}^-\left[{𝐃}^- - \frac{1}{\alpha}{𝐯}{𝐯}^{{𝖳}}\right]{𝐔}^{-{𝖳}} \qquad\qquad(8.52)
```

We now analyze the bracketed term in Eq. [\(8.52\)](#page-104-2) and find that we can define

<span id="page-104-3"></span>
```math
\tilde{{𝐔}}\tilde{{𝐃}}\tilde{{𝐔}}^{{𝖳}} \triangleq {𝐃}^- - \frac{1}{\alpha}{𝐯}{𝐯}^{{𝖳}} \qquad\qquad(8.53)
```

Therefore,

```math
{𝐔}^+ = {𝐔}^-\tilde{{𝐔}} \qquad \text{and} \qquad {𝐃}^+ = \tilde{{𝐃}} \qquad\qquad(8.54)
```

So, how do we proceed? This has all the marks of a rank-one update, for after all $`{𝐯}`$ is of rank one. We *can* proceed by using the Agee-Turner rank-one update. Except for one thing – that pesky minus sign in Eq. [\(8.53\)](#page-104-3). That minus sign portends all sorts of numerical issues because there is a possibility that we can lose numerical precision if the Agee-Turner update is used blindly. It turns out that we can have 'our cake and eat it too'; Neil Carlson developed a rank-one update to precisely remedy our issue. The mathematical development of this algorithm is detailed in Appendix [B.5.](14-appendix-b-the-mathematics-behind-the-udu-factorization-part3.md#page-153-1)

The algorithm is as follows: Given $`{𝐔}^-`$, $`{𝐃}^-`$, $`{𝐑}`$, and $`{𝐇}`$

> $`{𝐟} = {𝐔}^{-{𝖳}}{𝐇}^{{𝖳}}`$ &emsp; where &emsp; $`{𝐟} = \left[\, f_1 \;\; f_2 \;\; \cdots \;\; f_n \,\right]^{{𝖳}}`$ &emsp; $`[\frac{1}{2}(n_{{𝐱}}^2 - n_{{𝐱}}), \frac{1}{2}(n_{{𝐱}}^2 - n_{{𝐱}}), 0]`$  
> $`{𝐯} = {𝐃}^{-{𝖳}}{𝐟}`$ &emsp; where &emsp; $`{𝐯} = \left[\, \bar{d}_1 f_1 \;\; \bar{d}_2 f_2 \;\; \cdots \;\; \bar{d}_n f_n \,\right]^{{𝖳}}`$ &emsp; $`[0, n_{{𝐱}}, 0]`$  
> $`\overline{{𝐊}}_1 = \left[\, v_1 \;\; 0 \;\; \cdots \;\; \bar{0} \,\right]^{{𝖳}}`$  
> $`\alpha_1 = {𝐑} + v_1 f_1`$ &emsp; $`[1, 1, 0]`$  
> $`d_1 = \left(\frac{{𝐑}}{\alpha_1}\right)\bar{d}_1`$ &emsp; $`[0, 1, 1]`$  
> **for** $`j = 2, \cdots, n`$ **do**  
> &emsp;$`\alpha_j = \alpha_{j-1} + v_j f_j`$ &emsp; $`[n_{{𝐱}} - 1, n_{{𝐱}} - 1, 0]`$  
> &emsp;$`d_j = \left(\frac{\alpha_{j-1}}{\alpha_j}\right)\bar{d}_j`$ &emsp; $`[0, n_{{𝐱}} - 1, n_{{𝐱}} - 1]`$  
> &emsp;$`\lambda_j = -\left(f_j/\alpha_{j-1}\right)`$ &emsp; $`[0, 0, n_{{𝐱}} - 1]`$  
> &emsp;$`{𝐔}_j^+ = {𝐔}_j^- + \lambda_j\overline{{𝐊}}_{j-1}`$ &emsp; $`[\frac{1}{2}(n_{{𝐱}}^2 - n_{{𝐱}}), \frac{1}{2}(n_{{𝐱}}^2 - n_{{𝐱}}), 0]`$  
> &emsp;$`\overline{{𝐊}}_j = \overline{{𝐊}}_{j-1} + v_j{𝐔}_j^-`$ &emsp; $`[\frac{1}{2}(n_{{𝐱}}^2 - n_{{𝐱}}), \frac{1}{2}(n_{{𝐱}}^2 - n_{{𝐱}}), 0]`$  
> **end for**  
> $`{𝐊} = \overline{{𝐊}}_n/\alpha`$ &emsp; $`[0, 0, n_{{𝐱}}]`$

Thus, taking advantage of the triangularity of the $`{𝐔}^-`$ matrix (and the fact that $`{𝐔}^{-{𝖳}}{𝐇}^{{𝖳}}`$ and $`\lambda_j\overline{{𝐊}}_{j-1}`$ and $`v_j{𝐔}_j^-`$ use $`n_{{𝐱}}(n_{{𝐱}}-1)/2`$multiplies and adds), for each measurement processed, the covariance update results in $`1.5n_{{𝐱}}^2 - 0.5n_{{𝐱}}`$ adds, $`1.5n_{{𝐱}}^2 + 1.5n_{{𝐱}}`$ multiplies and $`3n_{{𝐱}} - 1`$ divides.

For the normal, Joseph Kalman filter update, for a scalar measurement, we find that if we use efficient methods of calculating and storing quantities [[5](16-bibliography.md#page-170-1)], we use $`4.5n_{{𝐱}}^2 + 3.5n_{{𝐱}}`$ adds, $`4n_{{𝐱}}^2 + 4.5n_{{𝐱}}`$ multiplies and 1 divide.

For the "Conventional" Kalman filter update ($`{𝐏} = {𝐏}^- - {𝐊}{𝐇}{𝐏}^-`$ in Eq.(61)), for a scalar measurement, we find that [[5](16-bibliography.md#page-170-1)] we use $`1.5n_{{𝐱}}^2 + 1.5n_{{𝐱}}`$ adds, $`1.5n_{{𝐱}}^2 + 0.5n_{{𝐱}}`$ multiplies and 1 divide.

Thus, for $`n_{{𝐱}} = 35`$, the covariance update due to measurement processing with the UDU factorization uses 1820 adds, 1890 divides and 104 divides compared with 5635 adds, 5058 multiplies and 1 divide for the efficient Joseph update. The "Conventional" Kalman update uses 1890 adds, 1855 multiplies, and 1 divide.

Hence there is almost a factor of 2.5 improvement in the adds and multiplies using the triangular (UDU) update compared with the Joseph update. This rivals the efficiency of the "conventional" Kalman Filter update.

### 8.4.1. Consider Covariance and its Implementation in the UDU Filter

'Consider' Analysis was first introduced by S. F. Schmidt of NASA Ames in the mid 1960s as a means to account for errors in both the dynamic and measurement models due to uncertain parameters [[75](16-bibliography.md#page-173-5)]. The Consider Kalman Filter, also called the Schmidt-Kalman Filter, resulted from this body of work. The consider approach is especially useful when parameters have low observability.

We partition the state-vector, $`{𝐱}`$ into the $`n_{{𝐬}}`$"estimated states", $`{𝐬}`$, and the $`n_{{𝐩}}`$ "consider" parameters, $`{𝐩}`$, as

```math
{𝐱} \triangleq \begin{bmatrix} {𝐬} \\ {𝐩} \end{bmatrix} \qquad\qquad(8.55)
```

so that

```math
{𝐏} = \begin{bmatrix} {𝐏}_{{𝐬𝐬}} & {𝐏}_{{𝐬𝐩}} \\ {𝐏}_{{𝐩𝐬}} & {𝐏}_{{𝐩𝐩}} \end{bmatrix}, \qquad {𝐇} = \begin{bmatrix} {𝐇}_{{𝐬}} & {𝐇}_{{𝐩}} \end{bmatrix} \qquad\qquad(8.56)
```

```math
{𝐊}_{opt} = \begin{bmatrix} {𝐊}_{{𝐬},opt} \\ {𝐊}_{{𝐩},opt} \end{bmatrix} = \begin{bmatrix} {𝐏}_{{𝐬𝐬}}^-{𝐇}_{{𝐬}}^{{𝖳}} + {𝐏}_{{𝐬𝐩}}^-{𝐇}_{{𝐩}}^{{𝖳}} \\ {𝐏}_{{𝐩𝐬}}^-{𝐇}_{{𝐬}}^{{𝖳}} + {𝐏}_{{𝐩𝐩}}^-{𝐇}_{{𝐩}}^{{𝖳}} \end{bmatrix}{𝐖}^{-1} \qquad\qquad(8.57)
```

where $`{𝐊}_{opt}`$ is the optimal Kalman gain computed for the full state, $`{𝐱}`$, and $`{𝐖}`$ is

```math
{𝐖} = {𝐇}_{{𝐬}}{𝐏}_{{𝐬𝐬}}^-{𝐇}_{{𝐬}}^{{𝖳}} + {𝐇}_{{𝐬}}{𝐏}_{{𝐬𝐩}}^-{𝐇}_{{𝐩}}^{{𝖳}} + {𝐇}_{{𝐩}}{𝐏}_{{𝐩𝐬}}^-{𝐇}_{{𝐬}}^{{𝖳}} + {}+{𝐇}_{{𝐩}}{𝐏}_{{𝐩𝐩}}^-{𝐇}_{{𝐩}}^{{𝖳}} \qquad\qquad(8.58)
```

Therefore, if we now choose the $`{𝐊}_{{𝐬}}`$ and $`{𝐊}_{{𝐩}}`$ carefully such that the $`{𝐊}_{{𝐬}} = {𝐊}_{{𝐬},opt}`$, the *a posteriori* covariance matrix is

```math
{𝐏}^+ = \begin{bmatrix} {𝐏}_{{𝐬𝐬}}^- - {𝐊}_{{𝐬}}{𝐖}{𝐊}_{{𝐬}}^{{𝖳}} & {𝐏}_{{𝐬𝐩}}^- - {𝐊}_{{𝐬}}{𝐇}\begin{bmatrix} {𝐏}_{{𝐬𝐩}}^- \\ {𝐏}_{{𝐩𝐩}}^- \end{bmatrix} \\ {𝐏}_{{𝐩𝐬}}^- - \begin{bmatrix} {𝐏}_{{𝐬𝐩}}^- \\ {𝐏}_{{𝐩𝐩}}^- \end{bmatrix}^{{𝖳}}{𝐇}^{{𝖳}}{𝐊}_{{𝐬}}^{{𝖳}} & {𝐏}_{{𝐩𝐩}}^- - {𝐊}_{{𝐩}}{𝐖}{𝐊}_{{𝐩}}^{{𝖳}} \end{bmatrix} \qquad\qquad(8.59)
```

This equation is valid for any value of $`{𝐊}_{{𝐩}}`$. Notice that there is no $`{𝐊}_{{𝐩}}`$ in the correlation terms of the covariance matrix. **Therefore, what is *remarkable* about this equation is that once the optimal $`{𝐊}_{{𝐬}}`$ is chosen, the correlation between $`{𝐬}`$ and $`{𝐩}`$ is independent of the choice of $`{𝐊}_{{𝐩}}`$.**

In its essence, the consider parameters are not updated; therefore, the Kalman gain associated with the consider parameters, $`{𝐩}`$, is zero, *i.e.* $`{𝐊}_{{𝐩}} = {𝟎}`$. However, several comments are in order:

- (1) When using the Schmidt-Kalman filter, the *a priori* and *a posteriori* covariance of the parameters ($`{𝐏}_{{𝐩𝐩}}`$) are the same.
- (2) The *a posteriori* covariance matrix of the states and the correlation between the states and the parameters are the same regardless of whether one uses the Schmidt-Kalman filter or the optimal Kalman update

Therefore, the *consider* covariance, $`{𝐏}_{con}^+`$ is

```math
{𝐏}_{con}^+ = \begin{bmatrix} {𝐏}_{{𝐬𝐬}}^- - {𝐊}_{{𝐬}}{𝐖}{𝐊}_{{𝐬}}^{{𝖳}} & {𝐏}_{{𝐬𝐩}}^- - {𝐊}_{{𝐬}}{𝐇}\begin{bmatrix} {𝐏}_{{𝐬𝐩}}^- \\ {𝐏}_{{ℬℬ}}^- \end{bmatrix} \\ {𝐏}_{{𝐩𝐬}}^- - \begin{bmatrix} {𝐏}_{{𝐬𝐩}}^- \\ {𝐏}_{{𝐩𝐩}}^- \end{bmatrix}^{{𝖳}}{𝐇}^{{𝖳}}{𝐊}_{{𝐬}}^{{𝖳}} & {𝐏}_{{𝐩𝐩}}^- \end{bmatrix} \qquad\qquad(8.60)
```

Of course, the "full" optimal covariance matrix update is

```math
{𝐏}_{opt}^+ = \begin{bmatrix} {𝐏}_{{𝐬𝐬}}^- - {𝐊}_{{𝐬},opt}{𝐖}{𝐊}_{{𝐬},opt}' & {𝐏}_{{𝐬𝐩}}^- - {𝐊}_{{𝐬},opt}{𝐇}\begin{bmatrix} {𝐏}_{{𝐬𝐩}}^- \\ {𝐏}_{{𝐩𝐩}}^- \end{bmatrix} \\ {𝐏}_{{𝐩𝐬}}^- - \begin{bmatrix} {𝐏}_{{𝐬𝐩}}^- \\ {𝐏}_{{𝐩𝐩}}^- \end{bmatrix}^{{𝖳}}{𝐇}^{{𝖳}}{𝐊}_{{𝐬},opt}' & {𝐏}_{{𝐩𝐩}}^- - {𝐊}_{{𝐩},opt}{𝐖}{𝐊}_{{𝐩},opt}' \end{bmatrix} \qquad\qquad(8.61)
```

The UDU formulation, while numerically stable and tight, is quite inflexible to making any changes in the framework. At first blush, it would seem that the consider analysis would not fit into the framework. However, all is not in vain. With some clever rearrangements, we can allow for a rank-one update to include consider states in the measurement update. The measurement update, expressed in terms of the consider covariance [[92](16-bibliography.md#page-173-11)], is

<span id="page-106-0"></span>
```math
{𝐏}_{opt}^+ = {𝐏}_{con}^+ - ({𝐒}{𝐊}_{opt})\,{𝐖}\,({𝐒}{𝐊}_{opt})' \qquad\qquad(8.62)
```

where $`{𝐒}`$ is an $`n_{{𝐱}} \times n_{{𝐱}}`$ matrix (defining $`n_{{𝐱}} \triangleq n_{{𝐬}} + n_{{𝐩}}`$, where $`n_{{𝐱}}`$ is the total number of states, $`n_{{𝐩}}`$ is the number of consider states, and $`n_{{𝐬}}`$ is the number of "non-consider" states) defined as

```math
{𝐒} \triangleq \begin{bmatrix} {𝟎}_{n_{{𝐬}} \times n_{{𝐬}}} & {𝟎}_{n_{{𝐬}} \times n_{{𝐩}}} \\ {𝟎}_{n_{{𝐩}} \times n_{{𝐬}}} & {𝐈}_{n_{{𝐩}} \times n_{{𝐩}}} \end{bmatrix} \qquad\qquad(8.63)
```

Since we are processing scalar measurements, we note that $`{𝐖} = \frac{1}{\alpha}`$ is a scalar and $`{𝐊}_{opt}`$ is an $`n_{{𝐱}} \times 1`$ vector. Therefore $`{𝐒}{𝐊}_{opt}`$ is an $`n_{{𝐱}} \times 1`$ vector. Therefore, solving for the consider covariance,

```math
{𝐏}_{con}^+ = {𝐏}_{opt}^+ + W\,({𝐒}{𝐊}_{opt})\,({𝐒}{𝐊}_{opt})^{{𝖳}} \qquad\qquad(8.64)
```

Eq. [\(8.62\)](#page-106-0) has the same form as the original rank-one update *i.e.* $`{𝐏}^+ = {𝐏}^- + c\,{𝐚}{𝐚}^{{𝖳}}`$, with $`{𝐚} = {𝐒}{𝐊}_{opt}`$ and $`c = \frac{1}{\alpha}`$. With this in mind, we can use the (un-modified) rank-one update which is a backward-recursive update [[1](16-bibliography.md#page-170-16)]. If, for example, all the consider parameters are in the lower part of the state-space, we can effectively reduce the computations by ending the update when the covariance of the state of the last consider parameter is updated.

Therefore, the procedure is as follows: first perform a complete Carlson rank-one measurement update with the optimal Kalman Gain ($`{𝐊}_{opt}`$) on the full covariance matrix. Second, perform another rank-one update with $`{𝐚} = {𝐒}{𝐊}_{opt}`$ and $`c = \frac{1}{\alpha}`$, according to the Agee-Turner rank-one update (as in Table 1).

Therefore, since there is an additional rank-one update associated with the consider states and if no rearrangements of the consider states are performed, then there will be an additional $`n_{{𝐱}}^2`$ adds, $`n_{{𝐱}}^2 + 3n_{{𝐱}} + 2`$ multiplies, and $`n_{{𝐱}} - 1`$ divides per measurement.

The use of the "consider state" option, if it is exercised, is likely to be used in "consider"ing the attitude states, particularly during entry. The rationale for this is that in certain degenerate cases, like when GPS satellites are reacquired after entry blackout, the attitude estimate could be adversely affected. So, to protect against this, the "consider" option may be exercised with respect to the attitude states.

## 8.5. Conclusions

<span id="page-107-0"></span>Matrix factorization methods, particularly the UDU factorization, are very useful – indeed essential – for onboard navigation algorithms. They are numerically stable and computationally efficient, competitive with the classic Kalman filter implementation. In addition, they allow the navigation designer to investigate the positive definiteness of the covariance matrix for "free," since by inspecting the entries of $`{𝐃}`$, if any elements of $`{𝐃}`$ are negative, then the covariance matrix will not be positive semi-definite.

---

[← Chapter 8. Factorization Methods (part 2 of 3)](08-factorization-methods-part2.md) · [Contents](README.md) · [Chapter 9. Attitude Estimation (part 1 of 2) →](09-attitude-estimation-part1.md)
