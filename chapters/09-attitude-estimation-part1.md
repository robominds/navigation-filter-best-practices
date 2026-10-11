[← Chapter 8. Factorization Methods (part 3 of 3)](08-factorization-methods-part3.md) · [Contents](README.md) · [Chapter 9. Attitude Estimation (part 2 of 2) →](09-attitude-estimation-part2.md)

# Chapter 9. Attitude Estimation

*Contributed by F. Landis Markley*

<span id="page-108-0"></span>The particular complications of attitude estimation arise from a fundamental difference between rotational kinematics and translational kinematics. The translational state of motion can be completely specified in a nonsingular way by the cartesian components of the position vector $`{𝐫}(t)`$ and the velocity vector $`{𝐯}(t)`$. The integral of any reasonable function $`{𝐯}(t)`$ between two times gives the translational displacement of $`{𝐫}(t)`$ between these two times. Other parameterizations of the translational state may be singular; the classical Keplerian orbit elements are singular for zero inclination or zero eccentricity, for example. It is the case, however, that globally nonsingular six-parameter representations exist.

Rotations in three-dimensional space have three degrees of freedom, just like translations in three dimensions, and the angular velocity vector $`{𝝎}(t)`$ is the rotational analog of the velocity vector. However, two different time histories $`{𝝎}(t)`$ that have the same integral over a time interval can result in different rotational displacements over the interval. This is because the order in which rotations are performed is significant, unlike the order in which translations are performed. Thus integration of $`{𝝎}(t)`$ does not result in a three-vector rotational analog of the position vector. In fact, it can be proven that no global three-component parameterization of rotations without singular points exists [[80](16-bibliography.md#page-173-12)]. Rotational analysis is forced to deal with either higher-dimensional representations of rotations or with three-dimensional representations possessing singularities or discontinuities. The following seven sections will briefly present a nine-parameter representation, two four-parameter representations, and five three-parameter representations. Fuller discussions can be found in Refs. [[59](16-bibliography.md#page-172-10),[78](16-bibliography.md#page-173-13)]. The discussion of attitude representations is followed by two sections on extended Kalman filters for attitude estimation.

## 9.1. Attitude Matrix Representation

<span id="page-108-1"></span>Attitude representations are the methods of representing the orientation of an orthonormal triad of basis vectors in one reference frame with respect to an orthonormal triad in some other reference frame. The attitude matrix, in particular, represents the orientation of a vehicle's body frame with respect to a frame that is often, but not always, an inertial frame. The attitude determination of earth-pointing spacecraft, for example, typically employs a reference frame in which one basis vector is pointed from the spacecraft toward the center of the earth and another points opposite to the orbital angular velocity. The body frame of a rigid vehicle is simply defined as a frame fixed in the vehicle. No vehicle is completely rigid, though, so it is quite common to define the body frame operationally as the orientation of some *navigation base*, a sufficiently rigid subsystem of the spacecraft including the most critical attitude sensors and payload instruments.

For actual applications, representations are $`3\times 3`$ matrices that transform the representations of vectors in one frame, i.e. their components along the basis vectors in that frame, to their representations in a different frame. Thus attitude representations describe a fixed physical vector in a rotated frame rather than a rotated vector. This is the *passive* interpretation of a transformation, also known as the *alias* sense (from the Latin word for "otherwise," in the sense of "otherwise known as") [[78](16-bibliography.md#page-173-13)]. The alternative *active* interpretation (also known as the *alibi* sense from the Latin word for "elsewhere") considers the representation in a fixed reference frame of a rotated physical vector. It is crucial to keep this distinction in mind, because an active rotation in one direction corresponds to a passive rotation in the opposite direction. Overlooking this point has led to errors in flight software.[<sup>1</sup>](#page-109-0)

<span id="page-109-0"></span><sup>1</sup> One example is an incorrect sign for the velocity aberration correction for star tracker measurements on the Wilkinson Microwave Anisotropy Probe (WMAP) spacecraft, which fortunately was easily corrected.

Now consider transforming the representation of a vector $`\vec{{𝒙}}`$ in a frame $`{ℱ}`$ to its representation in a frame $`{𝒢}`$ and then from frame $`{𝒢}`$ to frame $`{ℋ}`$ or directly from frame $`{ℱ}`$ to frame $`{ℋ}`$, so

```math
{𝐱}_{{ℋ}} = {𝐀}_{{ℋ}{𝒢}}{𝐱}_{{𝒢}} = {𝐀}_{{ℋ}{𝒢}}\left({𝐀}_{{𝒢}{ℱ}}{𝐱}_{{ℱ}}\right) = {𝐀}_{{ℋ}{ℱ}}{𝐱}_{{ℱ}} \qquad\qquad(9.1)
```

These transformations must be equivalent for any vector $`{𝐱}_{{ℱ}}`$, so successive transformations are accomplished by simple matrix multiplication:

<span id="page-109-1"></span>

```math
{𝐀}_{{ℋ}{ℱ}} = {𝐀}_{{ℋ}{𝒢}}{𝐀}_{{𝒢}{ℱ}} \qquad\qquad(9.2)
```

This may appear to be an obvious result, but only one other attitude representation has such a simple composition rule. Matrix multiplication is associative, meaning that $`{𝐀}_{{ℋ}{𝒢}}({𝐀}_{{𝒢}{ℱ}}{𝐀}_{{ℱ}{ℰ}}) = ({𝐀}_{{ℋ}{𝒢}}{𝐀}_{{𝒢}{ℱ}}){𝐀}_{{ℱ}{ℰ}}`$. Matrix multiplication is not commutative, however, which means that $`{𝐀}_{{ℋ}{𝒢}}{𝐀}_{{𝒢}{ℱ}} \neq {𝐀}_{{𝒢}{ℱ}}{𝐀}_{{ℋ}{𝒢}}`$ in general. The non-commutativity of matrix multiplication is at the heart of the problem of finding a suitable attitude representation.

Transforming from frame $`{ℱ}`$ to frame $`{𝒢}`$ and back to frame $`{ℱ}`$ is effected by the matrix $`{𝐀}_{FF} = {𝐀}_{{ℱ}{𝒢}}{𝐀}_{{𝒢}{ℱ}}`$, which must be the identity matrix. Rotations must also preserve inner products and norms of vectors, so

```math
{𝐱}_{{ℱ}} \cdot {𝐲}_{{ℱ}} = {𝐱}_{{𝒢}} \cdot {𝐲}_{{𝒢}} = \left({𝐀}_{{𝒢}{ℱ}}{𝐱}_{{ℱ}}\right)^T {𝐀}_{{𝒢}{ℱ}}{𝐲}_{{ℱ}} = {𝐱}_{{ℱ}}^T {𝐀}_{{𝒢}{ℱ}}^T {𝐀}_{{𝒢}{ℱ}}{𝐲}_{{ℱ}} \qquad\qquad(9.3)
```

These two observations mean that

```math
{𝐀}_{{𝒢}{ℱ}}^T = {𝐀}_{{𝒢}{ℱ}}^{-1} = {𝐀}_{{ℱ}{𝒢}} \qquad\qquad(9.4)
```

A matrix with its transpose is equal to its inverse is called an *orthogonal* matrix, and its determinant must equal $`\pm 1`$. The attitude matrix must be a *proper* orthogonal matrix, i.e. have determinant $`+1`$, in order to transform a right-handed coordinate frame to a right-handed coordinate frame.

The nine-component attitude matrix is in some ways the ideal representation of a vehicle's attitude. It has a 1:1 correspondence with physical attitudes, it varies smoothly as the physical attitude varies smoothly, its elements all have magnitudes less than or equal to one, and it follows a simple rule for combining successive rotations. It is not an efficient representation, though; only three of its nine parameters are independent because the orthogonality constraint is equivalent to six independent scalar constraints. This provides the opportunity to specify an attitude or an attitude matrix using only three parameters, but not, as was pointed out above, in a globally continuous and nonsingular fashion.

## 9.2. Euler Axis/Angle Representation

<span id="page-110-0"></span>The *Euler axis/angle* representation of a rotation matrix is based on *Euler's Theorem*, which states that the general displacement of a rigid body with one point fixed is a rotation about a fixed axis [[29](16-bibliography.md#page-171-15)]. Specify the axis by a unit vector $`\vec{{𝒆}}`$ and the rotation angle by $`\vartheta`$, and denote the matrix that maps the representations of vectors from frame $`{ℱ}`$ to frame $`{𝒢}`$ by $`{𝐀}_{{𝒢}{ℱ}}({𝐞},\vartheta)`$. The rotation axis is fixed, so $`{𝐞}`$ can be its representation in either frame $`{ℱ}`$ or frame $`{𝒢}`$, which are identical. Consider the mapping of a vector $`\vec{{𝒙}}`$ whose representation in frame $`{ℱ}`$ is

```math
{𝐱}_{{ℱ}} = ({𝐞}\,{𝐞}^T){𝐱}_{{ℱ}} + ({𝐈}_3 - {𝐞}\,{𝐞}^T){𝐱}_{{ℱ}} \qquad\qquad(9.5)
```

where $`{𝐈}_n`$ denotes the $`n\times n`$ identity matrix. The first term on the right side is parallel and the second is perpendicular to to the rotation axis. The rotation does not affect the parallel component and rotates the perpendicular component through an angle $`\vartheta`$ around the rotation axis out of the plane defined by that axis and $`{𝐱}_{{ℱ}}`$, so

<span id="page-110-1"></span>

```math
{𝐱}_{{𝒢}} = {𝐀}_{{𝒢}{ℱ}}({𝐞},\vartheta){𝐱}_{{ℱ}} = ({𝐞}\,{𝐞}^T){𝐱}_{{ℱ}} + \cos\vartheta\,({𝐈}_3 - {𝐞}\,{𝐞}^T){𝐱}_{{ℱ}} - \sin\vartheta\,({𝐞}\times{𝐱}_{{ℱ}}) \qquad\qquad(9.6)
```

This formula preserves the norm of $`{𝐱}_{{ℱ}}`$ because $`{𝐞}\times{𝐱}_{{ℱ}}`$ and $`({𝐈}_3 - {𝐞}\,{𝐞}^T){𝐱}_{{ℱ}}`$ are orthogonal and have equal magnitude. Since $`{𝐱}_{{ℱ}}`$ is an arbitrary vector, Eq. [\(9.6\)](#page-110-1) means that

<span id="page-110-2"></span>

```math
{𝐀}({𝐞},\vartheta) = (\cos\vartheta)\,{𝐈}_3 - \sin\vartheta\,[{𝐞}\times] + (1-\cos\vartheta)\,{𝐞}\,{𝐞}^T \qquad\qquad(9.7)
```

where $`[{𝐞}\times]`$ is the cross-product matrix:

```math
[{𝐞}\times] \equiv \begin{bmatrix} 0 & -e_3 & e_2 \\ e_3 & 0 & -e_1 \\ -e_2 & e_1 & 0 \end{bmatrix} \qquad\qquad(9.8)
```

The cross-product matrix is defined so that $`[{𝐱}\times]\,{𝐲} = {𝐱}\times{𝐲}`$. Equation [\(9.7\)](#page-110-2) is the *Euler axis/angle* parameterization of an attitude matrix, with explicit frame indices omitted. It requires four parameters, but only three are independent because of the unit vector constraint $`\|{𝐞}\| = 1`$.

The $`\sin\vartheta`$ terms in Eqs. [\(9.6\)](#page-110-1) and [\(9.7\)](#page-110-2) are negative because the rotation in Euler's theorem is an active rotation of the frame $`{𝒢}`$ relative to the frame $`{ℱ}`$, while the rotation matrix $`{𝐀}({𝐞},\vartheta)`$ specifies the passive mapping of the representation of $`\vec{{𝒙}}`$ from frame $`{ℱ}`$ to frame $`{𝒢}`$.

The Euler axis/angle representation can be used to find the time dependence of the rotation matrix. The fundamental definition of a derivative gives

<span id="page-110-3"></span>

```math
\begin{aligned} \dot{{𝐀}}_{{𝒢}{ℱ}}(t) &\equiv \lim_{\Delta t\to 0} \frac{{𝐀}_{{𝒢}{ℱ}}(t+\Delta t) - {𝐀}_{{𝒢}{ℱ}}(t)}{\Delta t} \\ &= \left(\lim_{\Delta t\to 0} \frac{{𝐀}_{{𝒢}{ℱ}}(t+\Delta t){𝐀}_{{ℱ}{𝒢}}(t) - {𝐈}_3}{\Delta t}\right){𝐀}_{{𝒢}{ℱ}}(t) \end{aligned} \qquad\qquad(9.9)
```

because $`{𝐀}_{{ℱ}{𝒢}}(t){𝐀}_{{𝒢}{ℱ}}(t)`$ is equal to the identity matrix. For small $`\Delta t`$, the matrix product $`{𝐀}_{{𝒢}{ℱ}}(t+\Delta t){𝐀}_{{ℱ}{𝒢}}(t)`$ differs from the identity matrix by a small rotation, so it can be represented by a small angle approximation of Eq. [\(9.7\)](#page-110-2):

```math
{𝐀}_{{𝒢}{ℱ}}(t+\Delta t){𝐀}_{{ℱ}{𝒢}}(t) \approx {𝐈}_3 - \vartheta\,[{𝐞}\times] \qquad\qquad(9.10)
```

Inserting this into Eq. [\(9.9\)](#page-110-3), taking the limit of as $`\Delta t`$ goes to zero, and omitting time arguments gives

<span id="page-110-4"></span>

```math
\dot{{𝐀}}_{{𝒢}{ℱ}} = -[{𝝎}_{{𝒢}}^{{𝒢}{ℱ}}\times]{𝐀}_{{𝒢}{ℱ}} \qquad\qquad(9.11)
```

where

<span id="page-110-5"></span>

```math
{𝝎}_{{𝒢}}^{{𝒢}{ℱ}} \equiv \lim_{\Delta t\to 0} \frac{\vartheta\,{𝐞}}{\Delta t} \qquad\qquad(9.12)
```

is the vector representation in frame $`{𝒢}`$ of the angular velocity of frame $`{𝒢}`$ with respect to frame $`{ℱ}`$. The angular velocity is known to be represented in frame $`{𝒢}`$ because the product $`{𝐀}_{{𝒢}{ℱ}}(t+\Delta t){𝐀}_{{ℱ}{𝒢}}(t)`$ is a rotation from frame $`{𝒢}`$ at one time to frame $`{𝒢}`$ at a different time, and these two frames coincide in the limit that $`\Delta t`$ goes to zero. The angular velocity is usually written simply as $`{𝝎}`$, with the frames understood. Its units are rad/sec, assuming that time is measured in seconds, because radian measure was assumed in taking the small angle limit of $`\sin\vartheta`$.

Equation [\(9.11\)](#page-110-4) is the fundamental equation of attitude kinematics. It does not distinguish between the situations where frame $`{ℱ}`$ or frame $`{𝒢}`$ or both frames are rotating in an absolute sense; it only cares about the relative rotation between the two frames. This equation can also be written as

```math
\dot{{𝐀}}_{{𝒢}{ℱ}} = -{𝐀}_{{𝒢}{ℱ}}{𝐀}_{{ℱ}{𝒢}}[{𝝎}_{{𝒢}}^{{𝒢}{ℱ}}\times]{𝐀}_{{ℱ}{𝒢}}^T = -{𝐀}_{{𝒢}{ℱ}}[{𝐀}_{{ℱ}{𝒢}}{𝝎}_{{𝒢}}^{{𝒢}{ℱ}}\times] = -{𝐀}_{{𝒢}{ℱ}}[{𝝎}_{{ℱ}}^{{𝒢}{ℱ}}\times] \qquad\qquad(9.13)
```

which expresses the kinematics in terms of the representation in frame $`{ℱ}`$ of $`{𝝎}^{{𝒢}{ℱ}}`$. The second equality uses an identity that holds for any proper orthogonal matrix. These kinematic equations, if integrated exactly, preserve the orthogonality of the attitude matrix.

The Euler axis/angle representation is fundamental for analysis, as demonstrated above, but it has been entirely superseded for practical applications by a superior four-parameter representation described in the next section.

## 9.3. Quaternion Representation

<span id="page-111-0"></span>Applying trigonometric half-angle identities to Eq. [\(9.7\)](#page-110-2) gives

<span id="page-111-2"></span>

```math
{𝐀}({𝐪}) = \Bigl(q_4^2 - \|{𝐪}_{1:3}\|^2\Bigr){𝐈}_3 - 2q_4[{𝐪}_{1:3}\times] + 2\,{𝐪}_{1:3}{𝐪}_{1:3}^T \qquad\qquad(9.14)
```

where the three-component vector $`{𝐪}_{1:3}`$ and the scalar $`q_4`$ are defined by

```math
{𝐪}_{1:3} = {𝐞}\sin(\vartheta/2) \qquad\qquad(9.15a)
```

```math
q_4 = \cos(\vartheta/2) \qquad\qquad(9.15b)
```

This representation has the advantage over the Euler axis/angle representation of requiring no trigonometric function evaluations, and its four components are more economical than the nine-component attitude matrix.

The four parameters of this representation were first considered by Euler but their full significance was revealed by Rodrigues, so they are often referred to as the *Euler symmetric parameters* or *Euler-Rodrigues* parameters. This representation is called the quaternion representation and denoted $`{𝐀}({𝐪})`$ because the four parameters can be regarded as the components of a quaternion

```math
{𝐪} = \begin{bmatrix} {𝐪}_{1:3} \\ q_4 \end{bmatrix} \qquad\qquad(9.16)
```

with vector part $`{𝐪}_{1:3}`$ and scalar $`q_4`$. A quaternion is basically four-component vector with some additional operations defined for it.[<sup>2</sup>](#page-111-1) The attitude quaternion

<span id="page-111-3"></span>

```math
{𝐪}({𝐞},\vartheta) = \begin{bmatrix} {𝐞}\sin(\vartheta/2) \\ \cos(\vartheta/2) \end{bmatrix} \qquad\qquad(9.17)
```

is a unit quaternion, obeying the norm constraint $`\|{𝐪}\| = 1`$, but not all quaternions are unit quaternions. It is clear from Eq. [\(9.14\)](#page-111-2) that $`{𝐪}`$ and $`-{𝐪}`$ give the same attitude matrix. This 2:1 mapping of quaternions to rotations is a minor annoyance that cannot be removed without introducing discontinuities in the representation.

<span id="page-111-1"></span><sup>2</sup> This is *conceptually* different from the quaternion introduced by Hamilton in 1844, before the introduction of vector notation, as a hypercomplex extension $`q = q_0 + iq_1 + jq_2 + kq_3`$ of a complex number $`z = x + iy`$. The scalar part of a quaternion is often labeled $`q_0`$ and put at the top of the column vector. Care must be taken to thoroughly understand the conventions embodied in any quaternion equation that one chooses to reference.

The most important added quaternion operations are two different products of two quaternions $`{𝐪}`$ and $`\bar{{𝐪}}`$. They can be implemented in matrix form similar to the matrix form of the vector cross product:[<sup>3</sup>](#page-112-0)

<span id="page-112-0"></span><sup>3</sup> The notation $`{𝐪}\otimes\bar{{𝐪}}`$ was introduced in Ref. [[53](16-bibliography.md#page-172-11)], and $`{𝐪}\odot\bar{{𝐪}}`$ is a modification of notation introduced in Ref. [[68](16-bibliography.md#page-172-12)]. Hamilton's product $`q\bar{q}`$ corresponds to $`{𝐪}\odot\bar{{𝐪}}`$, but $`{𝐪}\otimes\bar{{𝐪}}`$ has proven to be more useful in attitude analysis. The order of the quaternion products in Eqs. [\(9.27\)](#page-113-0) and [\(9.28\)](#page-113-1) would be reversed with the classical definition of quaternion multiplication.

```math
{𝐪}\otimes\bar{{𝐪}} = [{𝚿}({𝐪})\ \ {𝐪}]\,\bar{{𝐪}} \qquad\qquad(9.18a)
```

<span id="page-112-4"></span>

```math
{𝐪}\odot\bar{{𝐪}} = [{𝚵}({𝐪})\ \ {𝐪}]\,\bar{{𝐪}} \qquad\qquad(9.18b)
```

where $`{𝚿}({𝐪})`$ and $`{𝚵}({𝐪})`$ are the $`4\times 3`$ matrices

<span id="page-112-1"></span>

```math
{𝚿}({𝐪}) \equiv \begin{bmatrix} q_4\,{𝐈}_3 - [{𝐪}_{1:3}\times] \\ -{𝐪}_{1:3}^T \end{bmatrix} \qquad\qquad(9.19a)
```

<span id="page-112-2"></span>

```math
{𝚵}({𝐪}) \equiv \begin{bmatrix} q_4\,{𝐈}_3 + [{𝐪}_{1:3}\times] \\ -{𝐪}_{1:3}^T \end{bmatrix} \qquad\qquad(9.19b)
```

Unlike the vector cross product, though, the norm of either product of two quaternions is equal to the product of their norms.

Both quaternion products are associative but not commutative in general, in parallel with matrix products. The two product definitions differ only in the signs of the cross product matrices in Eqs. [\(9.19a\)](#page-112-1) and [\(9.19b\)](#page-112-2), from which it follows that

<span id="page-112-3"></span>

```math
{𝐪}\otimes\bar{{𝐪}} = \bar{{𝐪}}\odot{𝐪} \qquad\qquad(9.20)
```

The identity quaternion

```math
{𝐈}_q \equiv \begin{bmatrix} 0 & 0 & 0 & 1 \end{bmatrix}^T \qquad\qquad(9.21)
```

acts in quaternion multiplication like the identity matrix in matrix multiplication. The conjugate $`{𝐪}^*`$ of a quaternion is obtained by changing the sign of its vector part:

```math
{𝐪}^* = \begin{bmatrix} {𝐪}_{1:3} \\ q_4 \end{bmatrix}^* \equiv \begin{bmatrix} -{𝐪}_{1:3} \\ q_4 \end{bmatrix} \qquad\qquad(9.22)
```

Either product of a quaternion with its conjugate is equal to the square of its norm times the identity quaternion.

The inverse of any quaternion having nonzero norm is defined by

```math
{𝐪}^{-1} \equiv {𝐪}^*/\|{𝐪}\|^2 \qquad\qquad(9.23)
```

A unit quaternion, such as the attitude quaternion, always has an inverse, which is identical with its conjugate. The conjugate of the product of two quaternions is equal to the product of their conjugates in the opposite order: $`(\bar{{𝐪}}\otimes{𝐪})^* = {𝐪}^*\otimes\bar{{𝐪}}^*`$. The same relationship holds for the other product definition and with conjugates replaced by inverses.

Equation [\(9.14\)](#page-111-2) can be compactly written as

```math
{𝐀}({𝐪}) = {𝚵}^T({𝐪}){𝚿}({𝐪}) \qquad\qquad(9.24)
```

Now consider, for a unit quaternion $`{𝐪}`$, the product

```math
\begin{aligned} {𝐪}\otimes\begin{bmatrix}{𝐱}\\0\end{bmatrix}\otimes{𝐪}^* &= {𝐪}^*\odot\left({𝐪}\otimes\begin{bmatrix}{𝐱}\\0\end{bmatrix}\right) = \begin{bmatrix}{𝚵}({𝐪}^*) & {𝐪}^*\end{bmatrix}\begin{bmatrix}{𝚿}({𝐪}) & {𝐪}\end{bmatrix}\begin{bmatrix}{𝐱}\\0\end{bmatrix} \\ &= \begin{bmatrix}{𝚵}^T({𝐪})\\ {𝐪}^T\end{bmatrix}{𝚿}({𝐪})\,{𝐱} = \begin{bmatrix}{𝐀}({𝐪})\,{𝐱}\\0\end{bmatrix} \end{aligned} \qquad\qquad(9.25)
```

Applying a transformation by a second quaternion $`\bar{{𝐪}}`$ gives

```math
\begin{aligned} \bar{{𝐪}}\otimes\left({𝐪}\otimes\begin{bmatrix}{𝐱}\\0\end{bmatrix}\otimes{𝐪}^*\right)\otimes\bar{{𝐪}}^* &= \bar{{𝐪}}\otimes\begin{bmatrix}{𝐀}({𝐪})\,{𝐱}\\0\end{bmatrix}\otimes\bar{{𝐪}}^* = \begin{bmatrix}{𝐀}(\bar{{𝐪}}){𝐀}({𝐪})\,{𝐱}\\0\end{bmatrix} \\ &= (\bar{{𝐪}}\otimes{𝐪})\otimes\begin{bmatrix}{𝐱}\\0\end{bmatrix}\otimes(\bar{{𝐪}}\otimes{𝐪})^* = \begin{bmatrix}{𝐀}(\bar{{𝐪}}\otimes{𝐪})\,{𝐱}\\0\end{bmatrix} \end{aligned} \qquad\qquad(9.26)
```

Because this must hold for any $`{𝐱}`$, it shows that

<span id="page-113-0"></span>

```math
{𝐀}(\bar{{𝐪}}\otimes{𝐪}) = {𝐀}(\bar{{𝐪}}){𝐀}({𝐪}) \qquad\qquad(9.27)
```

This and Eq. [\(9.2\)](#page-109-1) mean that the quaternion corresponding to successive rotations is just the product

<span id="page-113-1"></span>

```math
{𝐪}_{{ℋ}{ℱ}} = {𝐪}_{{ℋ}{𝒢}}\otimes{𝐪}_{{𝒢}{ℱ}} \qquad\qquad(9.28)
```

A simple bilinear composition rule of this type holds only for the attitude matrix and quaternion representations, a major reason for the popularity of quaternions.

Representing the rotation between times $`t`$ and $`t+\Delta t`$ by an Euler axis and angle, Eqs. [\(9.28\)](#page-113-1), [\(9.17\)](#page-111-3), [\(9.20\)](#page-112-3), and [\(9.18b\)](#page-112-4) give

```math
\begin{aligned} {𝐪}(t+\Delta t) &= \begin{bmatrix}{𝐞}\sin(\vartheta/2)\\ \cos(\vartheta/2)\end{bmatrix}\otimes{𝐪}(t) = \cos(\vartheta/2){𝐪}(t) + \sin(\vartheta/2)\begin{bmatrix}{𝐞}\\0\end{bmatrix}\otimes{𝐪}(t) \\ &= \cos(\vartheta/2){𝐪}(t) + \sin(\vartheta/2){𝚵}\left({𝐪}(t)\right){𝐞} \end{aligned} \qquad\qquad(9.29)
```

This quaternion propagation equation has proven to be very useful. It preserves the unity norm of the attitude quaternion. If the angular velocity is well approximated as constant over the time interval, then $`\vartheta = \|{𝝎}\|\Delta t`$ and $`{𝐞} = {𝝎}/\|{𝝎}\|`$. Alternatively, and particularly for onboard applications, $`\vartheta{𝐞}`$ can be computed by differencing the outputs of rate-integrating gyroscopes.

Using small angle approximations for the sine and cosine leads to the kinematic equation for the quaternion:

<span id="page-113-2"></span>

```math
\dot{{𝐪}} \equiv \lim_{\Delta t\to 0}\frac{{𝐪}(t+\Delta t) - {𝐪}(t)}{\Delta t} = \frac{1}{2}\begin{bmatrix}{𝝎}\\0\end{bmatrix}\otimes{𝐪} = \frac{1}{2}{𝚵}({𝐪})\,{𝝎} \qquad\qquad(9.30)
```

where $`{𝝎}`$ is defined by Eq. [\(9.12\)](#page-110-5) and several time arguments have been omitted. Exact integration of this equation preserves the unit norm of the quaternion. The inverse of Eq. [\(9.30\)](#page-113-2) is often useful:

```math
{𝝎} = 2{𝚵}^T({𝐪})\dot{{𝐪}} \qquad\qquad(9.31)
```

The quaternion representation of a given attitude matrix $`{𝐀}`$ can be found by normalizing any one of the four vectors [[56](16-bibliography.md#page-172-13)]

```math
\begin{aligned} \begin{bmatrix} 1 + 2A_{11} - \mathop{\mathrm{tr}}{𝐀} \\ A_{12} + A_{21} \\ A_{13} + A_{31} \\ A_{23} - A_{32} \end{bmatrix} &= 4q_1{𝐪}\,, &\qquad \begin{bmatrix} A_{21} + A_{12} \\ 1 + 2A_{22} - \mathop{\mathrm{tr}}{𝐀} \\ A_{23} + A_{32} \\ A_{31} - A_{13} \end{bmatrix} &= 4q_2{𝐪} \\ \begin{bmatrix} A_{31} + A_{13} \\ A_{32} + A_{23} \\ 1 + 2A_{33} - \mathop{\mathrm{tr}}{𝐀} \\ A_{12} - A_{21} \end{bmatrix} &= 4q_3{𝐪}\,, &\qquad \begin{bmatrix} A_{23} - A_{32} \\ A_{31} - A_{13} \\ A_{12} - A_{21} \\ 1 + \mathop{\mathrm{tr}}{𝐀} \end{bmatrix} &= 4q_4{𝐪} \end{aligned} \qquad\qquad(9.32)
```

Numerical errors are minimized by choosing the vector with the greatest norm, which can be found by the following procedure. Find the largest of $`\mathop{\mathrm{tr}}{𝐀}`$ and the three diagonal elements of $`{𝐀}`$. If $`\mathop{\mathrm{tr}}{𝐀}`$ is the largest, then $`|q_4|`$ is the largest of the $`|q_i|`$, otherwise the largest value of $`|q_i|`$ is the one with the same index as the largest diagonal element of $`{𝐀}`$. The overall sign of the normalized vector is not determined, reflecting the twofold ambiguity of the quaternion representation.

Extracting many of the other parameterizations from an attitude matrix is most easily accomplished by first extracting a quaternion and then converting to the desired representation. The kinematic equations of these other representations can also be readily derived through the intermediary of the quaternion representation.

A three-parameter representation can be obtained by using only three components of the quaternion, say the $`i, j, k`$ components, with the fourth component given by

<span id="page-114-2"></span>

```math
q_\ell = \pm\sqrt{1 - q_i^2 - q_j^2 - q_k^2} \qquad\qquad(9.33)
```

The sign is not arbitrary, but is determined by the four-component quaternion being represented by three of its components. Once so determined, the sign will not change if the quaternion varies smoothly unless $`q_\ell`$ passes through zero. To avoid a sign error if $`|q_\ell|`$ becomes small, the representation is switched to make $`q_\ell`$ one of three components in the three-parameter representation, replacing one of the other components, which is then given by the square root with the correct sign. The unit norm constraint on the attitude quaternion means that at least one of its components must have magnitude $`1/2`$ or greater. To minimize switching, it should be done when $`|q_\ell|`$ is significantly less than $`1/2`$, and the component replaced by $`q_\ell`$ in the three-component representation should have magnitude no smaller than $`1/2`$. To first order in the errors, the error in the fourth component of the quaternion is

<span id="page-114-3"></span>

```math
\Delta q_\ell = -\,q_\ell^{-1}(q_i\Delta q_i + q_j\Delta q_j + q_k\Delta q_k) \qquad\qquad(9.34)
```

This approaches the indeterminate quantity $`0/0`$ as $`|q_\ell|\to 0`$, providing another reason for switching.

## 9.4. Rodrigues Parameter Representation

<span id="page-114-0"></span>The three *Rodrigues parameters* appeared in 1840 [[72](16-bibliography.md#page-172-14)], but were first arranged in a vector by Gibbs, who invented modern vector notation. For this reason, the vector of Rodrigues parameters is often called the *Gibbs vector* and denoted by $`{𝐠}`$. The Rodrigues parameters are related to the Euler axis/angle and the quaternion by

<span id="page-114-1"></span>

```math
{𝐠} = {𝐞}\tan(\vartheta/2) = \frac{{𝐪}_{1:3}}{q_4} \qquad\qquad(9.35)
```

The quaternion as a function of the Gibbs vector is

```math
{𝐪} = \frac{\pm 1}{\sqrt{1 + \|{𝐠}\|^2}}\begin{bmatrix}{𝐠}\\1\end{bmatrix} \qquad\qquad(9.36)
```

It is clear from Eq. [\(9.35\)](#page-114-1) that $`{𝐪}`$ and $`-{𝐪}`$ map to the same Gibbs vector, so the Rodrigues parameters provide a 1:1 mapping of rotations. The price paid for this is that the Gibbs vector is infinite for a $`180^\circ`$ rotation. Thus this parameterization is not recommended as a global attitude representation, but it provides an excellent representation of small rotations.

The Rodrigues parameter representation of the attitude matrix is

```math
{𝐀}({𝐠}) = {𝐈}_3 + 2\,\frac{[{𝐠}\times]^2 - [{𝐠}\times]}{1 + \|{𝐠}\|^2} \qquad\qquad(9.37)
```

This resembles the quaternion representation in requiring no transcendental function evaluations, but it is a rational function rather than a simple polynomial.

The composition rule for the Rodrigues parameters corresponding to the quaternion product $`\bar{{𝐪}}\otimes{𝐪}`$ is

```math
\bar{{𝐠}} \boxtimes {𝐠} \equiv \frac{\bar{{𝐠}} + {𝐠} - \bar{{𝐠}}\times{𝐠}}{1 - \bar{{𝐠}}\cdot{𝐠}} \qquad\qquad(9.38)
```

This composition law is associative but not commutative in general, in parallel with matrix and quaternion products. Because it is not a bilinear function of the constituent Gibbs vectors, it cannot be represented as a matrix product like quaternion composition.

The kinematic equation for the Rodrigues parameters is

```math
\dot{{𝐠}} = (1/2)\Bigl({𝐈}_3 + [{𝐠}\times] + {𝐠}{𝐠}^T\Bigr){𝝎} \qquad\qquad(9.39)
```

with the inverse

```math
{𝝎} = 2\left(1 + \|{𝐠}\|^2\right)^{-1}\left(\dot{{𝐠}} - {𝐠}\times\dot{{𝐠}}\right) \qquad\qquad(9.40)
```

---

[← Chapter 8. Factorization Methods (part 3 of 3)](08-factorization-methods-part3.md) · [Contents](README.md) · [Chapter 9. Attitude Estimation (part 2 of 2) →](09-attitude-estimation-part2.md)
