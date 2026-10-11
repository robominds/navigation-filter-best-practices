[← Chapter 9. Attitude Estimation (part 1 of 2)](09-attitude-estimation-part1.md) · [Contents](README.md) · [Chapter 10. Usability Considerations →](10-usability-considerations.md)

*Chapter 9. Attitude Estimation, continued*

## 9.5. Modified Rodrigues Parameters

<span id="page-115-0"></span>The modified Rodrigues parameters (MRPs) were invented by T. F. Wiener in 1962 [[88](16-bibliography.md#page-173-14)], rediscovered by Marandi and Modi in 1987 [[55](16-bibliography.md#page-172-15)], and have been championed by Junkins and Schaub [[73](16-bibliography.md#page-172-16)]. The vector of MRPs is related to the Euler axis/angle and the quaternion by

<span id="page-115-2"></span>

```math
{𝐩} = {𝐞}\tan(\vartheta/4) = \frac{{𝐪}_{1:3}}{1 + q_4} \qquad\qquad(9.41)
```

The quaternion as a function of the MRPs is

```math
{𝐪} = \frac{1}{1 + \|{𝐩}\|^2}\begin{bmatrix} 2{𝐩} \\ 1 - \|{𝐩}\|^2 \end{bmatrix} \qquad\qquad(9.42)
```

and the attitude matrix is given by

```math
{𝐀}({𝐩}) = {𝐈}_3 + \frac{8\,[{𝐩}\times]^2 - 4\left(1 - \|{𝐩}\|^2\right)[{𝐩}\times]}{(1 + \|{𝐩}\|^2)^2} \qquad\qquad(9.43)
```

Every vector of MRPs has a *shadow*

<span id="page-115-1"></span>

```math
{𝐩}^S \equiv -\frac{{𝐩}}{\|{𝐩}\|^2} = \frac{-{𝐪}_{1:3}}{1 - q_4} \qquad\qquad(9.44)
```

An MRP vector and its shadow represent the same attitude because $`{𝐪}`$ and $`-{𝐪}`$ represent the same attitude, so the MRPs are a 2:1 mapping of the rotations just as the quaternions are. It is clear from Eq. [\(9.44\)](#page-115-1) that $`\|{𝐩}^S\|\|{𝐩}\| = 1`$, so every attitude can be represented by either an MRP vector with $`\|{𝐩}\| \le 1`$ or an equivalent MRP vector in the *shadow set* of MRPs with $`\|{𝐩}\| \ge 1`$.

The MRP vector corresponding to the quaternion product $`\bar{{𝐪}}\otimes{𝐪}`$ follows the composition rule

```math
\bar{{𝐩}} \boxdot {𝐩} \equiv \frac{\left(1 - \|{𝐩}\|^2\right)\bar{{𝐩}} + \left(1 - \|\bar{{𝐩}}\|^2\right){𝐩} - 2\,\bar{{𝐩}}\times{𝐩}}{1 + \|{𝐩}\|^2\|\bar{{𝐩}}\|^2 - 2\,\bar{{𝐩}}\cdot{𝐩}} \qquad\qquad(9.45)
```

This composition law is associative but not commutative in general, in parallel with matrix and quaternion products. It cannot be represented as a matrix product.

The kinematic equation for the MRPs is

<span id="page-116-1"></span>

```math
\dot{{𝐩}} = \frac{1 + \|{𝐩}\|^2}{4}\biggl({𝐈}_3 + 2\,\frac{[{𝐩}\times]^2 + [{𝐩}\times]}{1 + \|{𝐩}\|^2}\biggr){𝝎} \qquad\qquad(9.46)
```

The matrix in parentheses is orthogonal, so the inverse of Eq. [\(9.46\)](#page-116-1) is

```math
{𝝎} = \frac{4}{1 + \|{𝐩}\|^2}\biggl({𝐈}_3 + 2\,\frac{[{𝐩}\times]^2 - [{𝐩}\times]}{1 + \|{𝐩}\|^2}\biggr)\dot{{𝐩}} \qquad\qquad(9.47)
```

The norm of an MRP vector can grow without limit during dynamic propagation or attitude estimation; Eq. [\(9.41\)](#page-115-2) shows that the norm is infinite for $`\vartheta = 2\pi`$. This singularity can be avoided by switching from the MRP vector to its shadow. The norm can be restricted to be less than or equal to unity in theory, but in practice it is best to allow the norm to exceed unity by some amount before switching in order to avoid "chattering" between the MRP and its shadow. An error $`\Delta{𝐩}`$ in an MRP vector corresponds to an error

<span id="page-116-3"></span>

```math
\Delta{𝐩}^S = \frac{\partial{𝐩}^S}{\partial{𝐩}}\Delta{𝐩} = \frac{2{𝐩}{𝐩}^T - \|{𝐩}\|^2\,{𝐈}_3}{\|{𝐩}\|^4}\Delta{𝐩} = \Bigl[2{𝐩}^S({𝐩}^S)^T - \|{𝐩}^S\|^2\,{𝐈}_3\Bigr]\Delta{𝐩} \qquad\qquad(9.48)
```

in its shadow. This relation is useful for mapping covariance matrices into and out of the shadow set. The 2:1 four-component quaternion representation does not have these complications because the two quaternions representing the same attitude both have unit norm, so there is no need to switch between them.

## 9.6. Rotation Vector Representation

<span id="page-116-0"></span>It is convenient for analysis, but not for computations, to combine the Euler axis and angle into the three-component *rotation vector*

```math
{𝝑} \equiv \vartheta\,{𝐞} = 2(\cos^{-1} q_4)\frac{{𝐪}_{1:3}}{\|{𝐪}_{1:3}\|} \qquad\qquad(9.49)
```

This leads to the very elegant expression

```math
{𝐀}({𝝑}) = \exp(-[{𝝑}\times]) \qquad\qquad(9.50)
```

where $`\exp(\cdot)`$ is the matrix exponential. This equation can be verified by expansion of it and Eq. [\(9.7\)](09-attitude-estimation-part1.md#page-110-2) as Taylor series in $`\vartheta`$ and repeated applications of the identity $`[{𝐞}\times]^2 = {𝐞}{𝐞}^T - {𝐈}_3`$.

The kinematic equation for the rotation vector is

<span id="page-116-2"></span>

```math
\dot{{𝝑}} = {𝝎} + \frac{1}{2}\,{𝝑}\times{𝝎} + \frac{1}{\vartheta^2}\left(1 - \frac{\vartheta}{2}\cot\frac{\vartheta}{2}\right){𝝑}\times({𝝑}\times{𝝎}) \qquad\qquad(9.51)
```

The coefficient of $`{𝝑}\times({𝝑}\times{𝝎})`$ goes to $`1/12`$ as $`\vartheta`$ goes to zero, but it is singular for $`\vartheta`$ equal to any nonzero multiple of $`2\pi`$. The inverse of Eq. [\(9.51\)](#page-116-2) is

```math
{𝝎} = \dot{{𝝑}} - \frac{1 - \cos\vartheta}{\vartheta^2}\,{𝝑}\times\dot{{𝝑}} + \frac{\vartheta - \sin\vartheta}{\vartheta^3}\,{𝝑}\times({𝝑}\times\dot{{𝝑}}) \qquad\qquad(9.52)
```

<span id="page-117-3"></span>The rotation vector is useful for the analysis of small rotations, but not for large rotations, because of both the computational cost of evaluating the matrix exponential and the kinematic singularity for $`\|{𝝑}\| = 2\pi`$. This singularity can be avoided, as for the MRPs, by switching from the rotation vector to its shadow

```math
{𝝑}^S \equiv \left(1 - 2\pi\|{𝝑}\|^{-1}\right){𝝑} \qquad\qquad(9.53)
```

which represents the same attitude. This can restrict the norm of the rotation vector to $`\pi`$ or less in theory, but in practice it is best to allow the norm to exceed $`\pi`$ by some amount before switching in order to avoid "chattering" between the rotation vector and its shadow.

The properties of the rotation vector are very similar to those of the MRPs, and it has no obvious advantages over the MRPs. It has the disadvantage of requiring transcendental function evaluations to compute the attitude matrix, so it is rarely used in practical applications.

## 9.7. Euler Angles

<span id="page-117-0"></span>An Euler angle representation parameterizes a rotation by the product of three rotations about coordinate frame unit vectors:

<span id="page-117-1"></span>

```math
{𝐀}_{ijk}(\phi,\theta,\psi) = {𝐀}({𝐞}_k,\psi){𝐀}({𝐞}_j,\theta){𝐀}({𝐞}_i,\phi) \qquad\qquad(9.54)
```

where $`{𝐞}_j`$, $`{𝐞}_j`$, and $`{𝐞}_j`$ are selected from the set

```math
{𝐞}_1 = \begin{bmatrix} 1 & 0 & 0 \end{bmatrix}^T, \quad {𝐞}_2 = \begin{bmatrix} 0 & 1 & 0 \end{bmatrix}^T, \quad {𝐞}_3 = \begin{bmatrix} 0 & 0 & 1 \end{bmatrix}^T \qquad\qquad(9.55)
```

The possible choice of axes is constrained by the requirements $`i \neq j`$ and $`j \neq k`$, leaving six symmetric sets with $`ijk`$ equal to 121, 131, 232, 212, 313, and 323 and six asymmetric sets with $`ijk`$ equal to 123, 132, 231, 213, 312, and 321. Symmetric Euler angle sets are used in classical studies of rigid body motion [[29](16-bibliography.md#page-171-15), [36](16-bibliography.md#page-171-16), [43](16-bibliography.md#page-171-17), [59](16-bibliography.md#page-172-10), [87](16-bibliography.md#page-173-15)].

The asymmetric sets of angles are called the *Tait-Bryan* angles or *roll*, *pitch*, and *yaw* angles. The latter terminology originally described the motions of ships and then was carried over into aircraft and spacecraft. Roll is a rotation about the vehicle body axis that is closest to the vehicle's usual direction of motion, and hence would be perceived as a screwing motion. The roll axis is conventionally assigned index 1. Yaw is a rotation about the vehicle body axis that is usually closest to the direction of local gravity, and hence would be be perceived as a motion that points the vehicle left or right. The yaw axis is conventionally assigned index 3. Pitch is a rotation about the remaining vehicle body axis, and hence would be perceived as a motion that points the vehicle up or down. The pitch axis is conventionally assigned index 2. Note that Eq. [\(9.54\)](#page-117-1) assigns the variables $`\phi`$, $`\theta`$, and $`\psi`$ based on the order of rotations in the sequence, making no definite association between these variables and either the axis labels 1, 2, and 3 or the names roll, pitch and yaw. Many authors follow a different convention, denoting roll by $`\phi`$, pitch by $`\theta`$, and yaw by $`\psi`$. As always, the reader consulting any source should be careful to understand the conventions that it follows.

Using the product rule and Eq. [\(9.11\)](09-attitude-estimation-part1.md#page-110-4) to compute the time derivative of Eq. [\(9.54\)](#page-117-1) gives

```math
\begin{aligned} -[{𝝎}\times]{𝐀}_{ijk}(\phi,\theta,\psi) = \Big\{ &-[(\dot{\psi}{𝐞}_k)\times] - {𝐀}({𝐞}_k,\psi)[(\dot{\theta}{𝐞}_j)\times]{𝐀}^T({𝐞}_k,\psi) \\ &-{𝐀}({𝐞}_k,\psi){𝐀}({𝐞}_j,\theta)[(\dot{\phi}{𝐞}_i)\times]{𝐀}^T({𝐞}_j,\theta){𝐀}^T({𝐞}_k,\psi)\Big\}\,{𝐀}_{ijk}(\phi,\theta,\psi) \end{aligned} \qquad\qquad(9.56)
```

The identity $`{𝐀}[{𝐱}\times]{𝐀}^T = [({𝐀}{𝐱})\times]`$, which holds for any proper orthogonal $`{𝐀}`$, gives

<span id="page-117-2"></span>

```math
{𝝎} = \dot{\psi}\,{𝐞}_k + \dot{\theta}{𝐀}({𝐞}_k,\psi){𝐞}_j + \dot{\phi}{𝐀}({𝐞}_k,\psi){𝐀}({𝐞}_j,\theta){𝐞}_i = {𝐀}({𝐞}_k,\psi){𝐌}[\dot{\phi}\ \ \dot{\theta}\ \ \dot{\psi}]^T \qquad\qquad(9.57)
```

where

```math
{𝐌} = [{𝐀}({𝐞}_j,\theta){𝐞}_i \quad {𝐞}_j \quad {𝐞}_k\,] \qquad\qquad(9.58)
```

The second equality in Eq. [\(9.57\)](#page-117-2) makes use of $`{𝐀}({𝐞}_k,\psi){𝐞}_k = {𝐞}_k`$. The Euler angle rates as functions of the angular velocity are

```math
[\dot{\phi}\ \ \dot{\theta}\ \ \dot{\psi}]^T = {𝐌}^{-1}{𝐀}^T({𝐞}_k,\psi){𝝎} \qquad\qquad(9.59)
```

<span id="page-118-1"></span>This kinematic equation is singular if the determinant of $`{𝐌}`$ is zero. Equation [\(9.7\)](09-attitude-estimation-part1.md#page-110-2) and the Euler axis requirement that $`{𝐞}_i\cdot{𝐞}_j = {𝐞}_j\cdot{𝐞}_k = 0`$ gives

```math
\det{𝐌} = [{𝐀}({𝐞}_j,\theta){𝐞}_i]\cdot({𝐞}_j\times{𝐞}_k) = \cos\theta\,[\,{𝐞}_i\cdot({𝐞}_j\times{𝐞}_k)] - \sin\theta\,({𝐞}_i\cdot{𝐞}_k) \qquad\qquad(9.60)
```

The triple vector product $`{𝐞}_i\cdot({𝐞}_j\times{𝐞}_k)`$ is zero for the symmetric Euler angles, so the kinematic equations of these representations are singular if $`\sin\theta = 0`$. The dot product $`{𝐞}_i\cdot{𝐞}_k`$ is zero for the asymmetric Euler angles, so the kinematics of these representations are singular if $`\cos\theta = 0`$. This singularity is known as *gimbal lock* and is caused by collinearity of the *physical* rotation axis vectors of the first and third rotations in the sequence. Note that the column vector representations of these rotation axes are always parallel for the symmetric Euler angle sequences and always perpendicular for the asymmetric sequences, but this neither causes nor prevents gimbal lock.

Because Euler angles are discussed in many references on rotational motion and because they are not widely used in navigation filters, they will not be discussed further here. Kinematic equations and explicit forms of the attitude matrices for all twelve sets can be found in Refs. [[36](16-bibliography.md#page-171-16), [43](16-bibliography.md#page-171-17), [59](16-bibliography.md#page-172-10), [87](16-bibliography.md#page-173-15)].

## 9.8. Additive EKF (AEKF)

<span id="page-118-0"></span>Three-component representations are the most natural representations for filtering, because only three parameters are needed to represent rotations. As was pointed out at the beginning of this Chapter, though, all three-parameter representations of the rotation group have discontinuities or singularities. Any filter using a three-dimensional attitude representation must provide some guarantee of avoiding these singular points, either by restricting the vehicle's attitude or by switching between different parameter sets if the representation approaches a discontinuity or singularity.

The earliest Kalman filters for spacecraft attitude estimation used a roll, pitch, yaw sequence of Euler or Tait-Bryan angles discussed in Section [9.7](#page-117-0) [[21](16-bibliography.md#page-170-17),[22](16-bibliography.md#page-171-18)]. This is a very useful representation if the middle angle of the sequence, generally the pitch angle, stays well away from $`\pm 90^\circ`$, and has been used for Earth-pointing spacecraft with small pitch angles. One disadvantage of this representation is its trigonometric function evaluations, but this is less of an issue with the computing power now available, especially in onboard computers.

An EKF can estimate three components of a quaternion, with the fourth component being determined by the quaternion unit norm constraint, as discussed at the end of Section [9.3](09-attitude-estimation-part1.md#page-111-0) [[53](16-bibliography.md#page-172-11)]. If the fourth component becomes small, it must be added to the set of estimated quaternion components, with one of the other components switched out. This switch should be made when the magnitude of the fourth component is is not too close to either end of the range from 0 and $`1/2`$ to avoid "chattering" between component sets. The switch must be accompanied by the following covariance matrix transformation. Assuming the three components in the pre-switch representation have indices $`i, j, k`$ in ascending order, their $`3\times 3`$ covariance matrix is the symmetric matrix

```math
{𝐏}_{3\times 3} = \begin{bmatrix} P_{ii} & P_{ij} & P_{ik} \\ P_{ji} & P_{jj} & P_{jk} \\ P_{ki} & P_{kj} & P_{kk} \end{bmatrix} \qquad\qquad(9.61)
```

The $`4\times 4`$ covariance matrix of the full quaternion is formed by adding the $`\ell`$th row and column, keeping the indices in ascending order. The needed covariance components, using using Eqs. [\(9.33\)](09-attitude-estimation-part1.md#page-114-2) and [\(9.34\)](09-attitude-estimation-part1.md#page-114-3), are

```math
P_{m\ell} = P_{\ell m} = -q_\ell^{-1}(q_i P_{im} + q_j P_{jm} + q_k P_{km}) \quad \text{for} \quad m = i, j, k \qquad\qquad(9.62a)
```

```math
P_{\ell\ell} = q_\ell^{-2}(q_i^2 P_{ii} + q_j^2 P_{jj} + q_k^2 P_{kk} + 2q_i q_j P_{ji} + 2q_i q_k P_{ik} + 2q_j q_k P_{jk}) \qquad\qquad(9.62b)
```

<span id="page-119-3"></span>Then the row and column corresponding to the quaternion component switched out of the representation are deleted to form the new $`3\times 3`$ covariance matrix.

The modified Rodrigues parameters (MRPs) are non-singular for rotations of less than $`360^\circ`$, and the singularity can be avoided by switching to an MRP in the shadow set, as discussed in Section [9.5.](#page-115-0) The switch to the shadow set is made at some angle greater than $`180^\circ`$ to avoid "chattering" between the two parameter sets. The switch must be accompanied by a covariance matrix transformation using Eq. [\(9.48\)](#page-116-3)

```math
{𝐏}_{pp}^S = \Bigl[2{𝐩}^S({𝐩}^S)^T - \|{𝐩}^S\|^2\,{𝐈}_3\Bigr]{𝐏}_{pp}\Bigl[2{𝐩}^S({𝐩}^S)^T - \|{𝐩}^S\|^2\,{𝐈}_3\Bigr] \qquad\qquad(9.63)
```

where $`{𝐏}_{pp}`$ is the covariance before the switch, and $`{𝐏}_{pp}^S`$ is the covariance of $`{𝐩}^S`$ after the switch [[45](16-bibliography.md#page-171-19)]. This covariance mapping is simpler than the corresponding mapping for the three-component quaternion representation, and the MRP representation avoids a square root computation. The appearance of $`\vartheta/4`$ in Eq. [\(9.41\)](#page-115-2) as opposed to $`\vartheta/2`$ in Eq. [\(9.17\)](09-attitude-estimation-part1.md#page-111-3) means that switching will be less frequent when the MRP representation is used. For these reasons the MRP representation has become the preferred three-parameter attitude filter when the attitude is unrestricted.

The Gibbs vector or Rodrigues parameter representation has been used in an EKF [[37](16-bibliography.md#page-171-20)], but it is not well suited to filtering because of its inability to represent $`180^\circ`$ rotations, as discussed in Section [9.4.](09-attitude-estimation-part1.md#page-114-0) It provides an excellent representation of small attitude errors, however. The rotation vector, discussed in Section [9.6,](#page-116-0) is also not recommended for application in an EKF, as it has no clear advantage over the MRPs and has the disadvantage of requiring transcendental function evaluations.

The nine-component attitude matrix and the four-component quaternion represent the entire rotation group without singularities or discontinuities, but the linear measurement update in EKFs employing these representations violates the orthogonality constraint on the attitude matrix or the unit norm constraint on the quaternion. Various methods have been proposed to circumvent this difficulty, but these are not without problems [[59](16-bibliography.md#page-172-10)]. At the very least, they are inefficient due to the larger dimesionality of the covariance matrix.

## 9.9. Multiplicative EKF (MEKF)

<span id="page-119-0"></span>The multiplicative EKF (MEKF) uses the nine-component attitude matrix or the four-component quaternion as the "global" attitude representation and a three-component vector $`{𝜹𝝑}`$ for the "local" representation of attitude errors, so that the true attitude is represented as a product

<span id="page-119-1"></span>

```math
{𝐀}^{\text{true}} = {𝜹}{𝐀}({𝜹𝝑})\hat{{𝐀}} \qquad\qquad(9.64a)
```

```math
{𝐪}^{\text{true}} = {𝜹}{𝐪}({𝜹𝝑})\otimes\hat{{𝐪}} \qquad\qquad(9.64b)
```

The constraints on the representations are satisfied because $`{𝐀}^{\text{true}}`$, $`{𝜹}{𝐀}`$, and $`\hat{{𝐀}}`$ are all proper orthogonal matrices, and $`{𝐪}^{\text{true}}`$, $`{𝜹}{𝐪}`$, and $`\hat{{𝐪}}`$ all have unit norm. The MEKF avoids the attitude restrictions or switching required by additive attitude EKFs because the error vector $`{𝜹𝝑}`$ is assumed to be small enough to completely avoid singularities in the parameterizations $`{𝜹}{𝐀}({𝜹𝝑})`$ or $`{𝜹}{𝐪}({𝜹𝝑})`$. In some sense, though, Eq. [\(9.64\)](#page-119-1) incorporates a continuous switching of the attitude reference.

Only the quaternion version of the MEKF, which is much more widely employed, is presented here. Reference [[53](16-bibliography.md#page-172-11)] reviews its history. Any three-component attitude representation that is related to first order in $`{𝜹𝝑}`$ to the quaternion by

<span id="page-119-2"></span>

```math
{𝜹}{𝐪} \approx \begin{bmatrix} {𝜹𝝑}/2 \\ 1 \end{bmatrix} \qquad\qquad(9.65)
```

<span id="page-120-3"></span>can be used as the error vector. Common choices are the rotation vector, as suggested by the notation of Eq. [\(9.64\)](#page-119-1), two times the vector part of the quaternion, two times the vector of Rodrigues parameters, four times the vector of MRPs, or a vector of suitably indexed roll, pitch, and yaw angles [[59](16-bibliography.md#page-172-10)].

The order of the factors on the right side of Eq. [\(9.64\)](#page-119-1) means that the attitude errors are in the body reference frame. This leads to a major advantage of the MEKF, that the covariance of the attitude error angles in the body frame has a transparent physical interpretation. The covariance of estimators using other attitude representations has a less obvious interpretation unless the attitude matrix is close to the identity matrix. It is possible to reverse the order of the factors on the right side of Eq. [\(9.64\)](#page-119-1) so the attitude errors are in the reference frame [[26](16-bibliography.md#page-171-21)]. The covariance can be mapped into the body frame if desired.

The MEKF estimates $`{𝜹𝝑}`$ and any other state variables of interest. This discussion addresses only the attitude part, as the equations for the other components of the state vector obey the usual EKF equations. The MEKF proceeds by iteration of three steps: measurement update, state vector reset, and propagation to the next measurement time. The measurement update step updates the local error state vector. The reset moves the updated information from the local error state to the global attitude representation and resets the components of the local error state to zero. The propagation step propagates the global variables to the time of the next measurement. The local error state variables do not need to be propagated because they are identically zero over the propagation step. These three steps will be discussed in more detail.

### 9.9.1. Measurement Update

The observation model in given in terms of the true global state

```math
{𝐲} = {𝐡}({𝐪}^{\text{true}}) + {𝐯} \qquad\qquad(9.66)
```

but the measurement sensitivity matrix is the partial derivative with respect to the local error state, so the measurement sensitivity matrix is

<span id="page-120-0"></span>

```math
{𝐇} = \frac{\partial{𝐡}}{\partial{𝐪}}\,\frac{\partial{𝐪}^{\text{true}}}{\partial({𝜹𝝑})} \qquad\qquad(9.67)
```

Equations [\(9.64\)](#page-119-1), [\(9.65\)](#page-119-2), [\(9.18b\)](09-attitude-estimation-part1.md#page-112-4), and [\(9.20\)](09-attitude-estimation-part1.md#page-112-3) give, to first order in the error vector,

<span id="page-120-1"></span>

```math
{𝐪}^{\text{true}} \approx \begin{bmatrix} {𝜹𝝑}/2 \\ 1 \end{bmatrix}\otimes\hat{{𝐪}} = \hat{{𝐪}} + \frac{1}{2}\Xi(\hat{{𝐪}}){𝜹𝝑} \qquad\qquad(9.68)
```

Inserting the partial derivative of this with respect to $`{𝜹𝝑}`$ into Eq. [\(9.67\)](#page-120-0) then gives

```math
{𝐇} = \frac{1}{2}\frac{\partial{𝐡}}{\partial{𝐪}}\,\Xi(\hat{{𝐪}}) \qquad\qquad(9.69)
```

Simplifications are possible in some special cases.

The Kalman gain computation and covariance update have the standard Kalman filter forms. The error state update employs the first-order Taylor expansion

```math
E\{{𝐡}({𝐪}^{\text{true}})\} \approx {𝐡}(\hat{{𝐪}}) + {𝐇}{𝜹}\hat{{𝝑}} \qquad\qquad(9.70)
```

giving

<span id="page-120-2"></span>

```math
{𝜹}\hat{{𝝑}}^{+} = {𝜹}\hat{{𝝑}}^{-} + {𝐊}\left[{𝐲} - E\{{𝐡}({𝐪}^{\text{true}})\}\right] = ({𝐈} - {𝐊}{𝐇}){𝜹}\hat{{𝝑}}^{-} + {𝐊}\left[{𝐲} - {𝐡}(\hat{{𝐪}}^{-})\right] \qquad\qquad(9.71)
```

### 9.9.2. Reset

The discrete measurement update assigns a finite post-update value to $`{𝜹}\hat{{𝝑}}^{+}`$, but the global state still retains the value $`\hat{{𝐪}}^{-}`$. A reset procedure is used to move the update information to a post-update estimate global state vector $`\hat{{𝐪}}^{+}`$, while simultaneously resetting $`{𝜹}\hat{{𝝑}}`$ to $`{𝟎}_3`$, the three-component vector with all zero components. The reset does not change the overall estimate, so the reset must obey

```math
\hat{{𝐪}}^{+} = {𝜹}{𝐪}({𝟎}_3)\otimes\hat{{𝐪}}^{+} = {𝜹}{𝐪}({𝜹}\hat{{𝝑}}^{+})\otimes\hat{{𝐪}}^{-} \qquad\qquad(9.72)
```

Thus the reset moves information from one part of the estimate to another part.

Every EKF includes an additive reset of the global state vector, but this is usually implicit rather than explicit. The multiplicative quaternion reset is the special feature of the MEKF. This reset has to preserve the quaternion norm, so an exact unit-norm expression for the functional dependence of $`{𝜹}{𝐪}`$ on $`{𝜹𝝑}`$ must be used, not the linear approximation of Eq. [\(9.65\)](#page-119-2). Using the Rodrigues parameter vector has the practical advantage that the reset operation for this parameterization is

```math
\hat{{𝐪}}^{+} = {𝜹}{𝐪}({𝜹}\hat{{𝝑}}^{+})\otimes\hat{{𝐪}}^{-} = \frac{1}{\sqrt{1 + \|{𝜹}\hat{{𝝑}}^{+}/2\|^2}}\begin{bmatrix} {𝜹}\hat{{𝝑}}^{+}/2 \\ 1 \end{bmatrix}\otimes\hat{{𝐪}}^{-} \qquad\qquad(9.73)
```

Using an argument similar to Eq. [\(9.68\)](#page-120-1), this can be accomplished in two steps:

```math
{𝐪}' = \hat{{𝐪}}^{-} + \frac{1}{2}\Xi(\hat{{𝐪}}^{-}){𝜹}\hat{{𝝑}}^{+} \qquad\qquad(9.74)
```

followed by

```math
\hat{{𝐪}}^{+} = \frac{{𝐪}'}{\|{𝐪}'\|} \qquad\qquad(9.75)
```

The first step is just the usual linear Kalman update, and the second step is equivalent to a brute force normalization of the updated quaternion. Thus the MEKF using Rodrigues parameters for the error vector provides a theoretical justification for brute force renormalization, with the added advantage of completely avoiding the accumulation of quaternion norm errors after many updates. The Rodrigues parameters also have the conceptual advantage that they map the rotation group into three-dimensional Euclidean space, with the largest possible $`180^\circ`$ attitude errors mapped to points at infinity. Thus probability distributions with infinitely long tails, such as Gaussian distributions, make sense in Rodrigues parameter space.

If a measurement update immediately follows a reset or propagation, the $`{𝜹}\hat{{𝝑}}^{-}`$ term on the right side of Eq. [\(9.71\)](#page-120-2) can be omitted because $`{𝜹}\hat{{𝝑}}^{-}`$ is zero. The reset is often delayed for computational efficiency until all the updates for a set of simultaneous measurements have been performed, though, in which case $`{𝜹}\hat{{𝝑}}^{-}`$ may have a finite value and all the terms in Eq. [\(9.71\)](#page-120-2) must be included. It is imperative to perform a reset before beginning the time propagation, however, to avoid the necessity of propagating $`{𝜹}\hat{{𝝑}}`$ between measurements.

There is some controversy over the question of whether the reset affects the covariance. One argument holds that it doesn't because the covariance depends not on the actual measurements but on their assumed statistics. Measurement errors are assumed to have zero mean, so the mean reset is zero. But the reset is very different from the measurement update in that it changes the reference frame for the attitude covariance, which might be expected to modify the covariance even though it adds no new information. The change in the covariance of $`{𝜹𝝑}`$ resulting from the effect of the actual update, rather than its zero expectation, can be computed to be [[57](16-bibliography.md#page-172-17), [71](16-bibliography.md#page-172-18)]

```math
{𝐏}_{\vartheta\vartheta}^{\text{reset}} = \Bigl({𝐈}_3 - [{𝜹}\hat{{𝝑}}^{+}\times]/2\Bigr){𝐏}_{\vartheta\vartheta}^{+}\Bigl({𝐈}_3 - [{𝜹}\hat{{𝝑}}^{+}\times]/2\Bigr)^T \qquad\qquad(9.76)
```

<span id="page-122-3"></span>to first order in $`{𝜹}\hat{{𝝑}}^{+}`$. Comparison with Eq. [\(9.7\)](09-attitude-estimation-part1.md#page-110-2) shows that the covariance reset looks to this order like a rotation by $`{𝜹}\hat{{𝝑}}^{+}/2`$, but this equivalence does not hold in higher orders. Most applications omit this covariance reset, but Reynolds has found that it speeds convergence and adds robustness in the presence of large updates, and that omitting it can even lead to filter divergence in some cases [[71](16-bibliography.md#page-172-18)].

### 9.9.3. Propagation

An EKF must propagate the expectation and covariance of the state. The MEKF is unusual in propagating the expectation $`\hat{{𝐪}}`$ and the covariance of the error-state vector. The propagation of the attitude error is found by by differentiating Eq. [\(9.64\)](#page-119-1):

<span id="page-122-0"></span>

```math
\dot{{𝐪}}^{\text{true}} = {𝜹}\dot{{𝐪}}\otimes\hat{{𝐪}} + {𝜹}{𝐪}\otimes\dot{\hat{{𝐪}}} \qquad\qquad(9.77)
```

The true and estimated quaternions satisfy the kinematic equations

```math
\dot{{𝐪}}^{\text{true}} = \frac{1}{2}\begin{bmatrix} {𝝎}^{\text{true}} \\ 0 \end{bmatrix}\otimes{𝐪}^{\text{true}} \qquad\qquad(9.78a)
```

```math
\dot{\hat{{𝐪}}} = \frac{1}{2}\begin{bmatrix} \hat{{𝝎}} \\ 0 \end{bmatrix}\otimes\hat{{𝐪}} \qquad\qquad(9.78b)
```

where $`{𝝎}^{\text{true}}`$ and $`\hat{{𝝎}}`$ are the true and estimated angular rates, respectively. Substituting these equations and Eq. [\(9.64\)](#page-119-1) into Eq. [\(9.77\)](#page-122-0), multiplying on the right by $`\hat{{𝐪}}^{-1}`$, and rearranging terms gives [[53](16-bibliography.md#page-172-11)]

```math
{𝜹}\dot{{𝐪}} = \frac{1}{2}\left(\begin{bmatrix} {𝝎}^{\text{true}} \\ 0 \end{bmatrix}\otimes{𝜹}{𝐪} - {𝜹}{𝐪}\otimes\begin{bmatrix} \hat{{𝝎}} \\ 0 \end{bmatrix}\right) \qquad\qquad(9.79)
```

Substituting Eq. [\(9.65\)](#page-119-2) and $`{𝝎}^{\text{true}} = \hat{{𝝎}} + {𝜹𝝎}`$, where $`{𝜹𝝎}`$ is the angular velocity error, and multiplying by two leads to

<span id="page-122-1"></span>

```math
\begin{bmatrix} {𝜹}\dot{{𝝑}} \\ 0 \end{bmatrix} = \begin{bmatrix} \hat{{𝝎}} \\ 0 \end{bmatrix}\otimes\begin{bmatrix} {𝜹𝝑}/2 \\ 1 \end{bmatrix} - \begin{bmatrix} {𝜹𝝑}/2 \\ 1 \end{bmatrix}\otimes\begin{bmatrix} \hat{{𝝎}} \\ 0 \end{bmatrix} + \begin{bmatrix} {𝜹𝝎} \\ 0 \end{bmatrix}\otimes\begin{bmatrix} {𝜹𝝑}/2 \\ 1 \end{bmatrix} \qquad\qquad(9.80)
```

Ignoring products of the small terms $`{𝜹𝝎}`$ and $`{𝜹𝝑}`$, in the spirit of the (linearized) EKF, the first three components of Eq. [\(9.80\)](#page-122-1) are

<span id="page-122-2"></span>

```math
{𝜹}\dot{{𝝑}} = -\hat{{𝝎}}\times{𝜹𝝑} + {𝜹𝝎} \qquad\qquad(9.81)
```

and the fourth component is $`0 = 0`$. Equation [\(9.81\)](#page-122-2) is the equation needed to propagate the covariance of the attitude error-angle covariance.

The expectation of Eq. [\(9.81\)](#page-122-2) is

```math
{𝜹}\dot{\hat{{𝝑}}} = -\hat{{𝝎}}\times{𝜹}\hat{{𝝑}} \qquad\qquad(9.82)
```

because $`{𝜹𝝎}`$ has zero expectation. This says that if $`{𝜹}\hat{{𝝑}}`$ is zero at the beginning of a propagation it will remain zero through the propagation, which is equivalent to saying that $`{𝜹}\hat{{𝐪}}`$ will be equal to the identity quaternion throughout the propagation.

---

[← Chapter 9. Attitude Estimation (part 1 of 2)](09-attitude-estimation-part1.md) · [Contents](README.md) · [Chapter 10. Usability Considerations →](10-usability-considerations.md)
