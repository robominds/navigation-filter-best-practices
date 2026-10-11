[← Chapter 8. Factorization Methods](08-factorization-methods.md) · [Contents](README.md) · [Chapter 10. Usability Considerations →](10-usability-considerations.md)

# Chapter 9. Attitude Estimation

*Contributed by F. Landis Markley*

<span id="page-108-0"></span>The particular complications of attitude estimation arise from a fundamental difference between rotational kinematics and translational kinematics. The translational state of motion can be completely specified in a nonsingular way by the cartesian components of the position vector $\mathbf{r}(t)$ and the velocity vector $\mathbf{v}(t)$. The integral of any reasonable function $\mathbf{v}(t)$ between two times gives the translational displacement of $\mathbf{r}(t)$ between these two times. Other parameterizations of the translational state may be singular; the classical Keplerian orbit elements are singular for zero inclination or zero eccentricity, for example. It is the case, however, that globally nonsingular six-parameter representations exist.

Rotations in three-dimensional space have three degrees of freedom, just like translations in three dimensions, and the angular velocity vector $\boldsymbol{\omega}(t)$ is the rotational analog of the velocity vector. However, two different time histories $\boldsymbol{\omega}(t)$ that have the same integral over a time interval can result in different rotational displacements over the interval. This is because the order in which rotations are performed is significant, unlike the order in which translations are performed. Thus integration of $\boldsymbol{\omega}(t)$ does not result in a three-vector rotational analog of the position vector. In fact, it can be proven that no global three-component parameterization of rotations without singular points exists [[80](16-bibliography.md#page-173-12)]. Rotational analysis is forced to deal with either higher-dimensional representations of rotations or with three-dimensional representations possessing singularities or discontinuities. The following seven sections will briefly present a nine-parameter representation, two four-parameter representations, and five three-parameter representations. Fuller discussions can be found in Refs. [[59](16-bibliography.md#page-172-10),[78](16-bibliography.md#page-173-13)]. The discussion of attitude representations is followed by two sections on extended Kalman filters for attitude estimation.

## 9.1. Attitude Matrix Representation

<span id="page-108-1"></span>Attitude representations are the methods of representing the orientation of an orthonormal triad of basis vectors in one reference frame with respect to an orthonormal triad in some other reference frame. The attitude matrix, in particular, represents the orientation of a vehicle's body frame with respect to a frame that is often, but not always, an inertial frame. The attitude determination of earth-pointing spacecraft, for example, typically employs a reference frame in which one basis vector is pointed from the spacecraft toward the center of the earth and another points opposite to the orbital angular velocity. The body frame of a rigid vehicle is simply defined as a frame fixed in the vehicle. No vehicle is completely rigid, though, so it is quite common to define the body frame operationally as the orientation of some *navigation base*, a sufficiently rigid subsystem of the spacecraft including the most critical attitude sensors and payload instruments.

For actual applications, representations are $3\times 3$ matrices that transform the representations of vectors in one frame, i.e. their components along the basis vectors in that frame, to their representations in a different frame. Thus attitude representations describe a fixed physical vector in a rotated frame rather than a rotated vector. This is the *passive* interpretation of a transformation, also known as the *alias* sense (from the Latin word for "otherwise," in the sense of "otherwise known as") [[78](16-bibliography.md#page-173-13)]. The alternative *active* interpretation (also known as the *alibi* sense from the Latin word for "elsewhere") considers the representation in a fixed reference frame of a rotated physical vector. It is crucial to keep this distinction in mind, because an active rotation in one direction corresponds to a passive rotation in the opposite direction. Overlooking this point has led to errors in flight software.[<sup>1</sup>](#page-109-0)

<span id="page-109-0"></span><sup>1</sup> One example is an incorrect sign for the velocity aberration correction for star tracker measurements on the Wilkinson Microwave Anisotropy Probe (WMAP) spacecraft, which fortunately was easily corrected.

Now consider transforming the representation of a vector $\vec{\boldsymbol{x}}$ in a frame $\mathcal{F}$ to its representation in a frame $\mathcal{G}$ and then from frame $\mathcal{G}$ to frame $\mathcal{H}$ or directly from frame $\mathcal{F}$ to frame $\mathcal{H}$, so

$$
\mathbf{x}_{\mathcal{H}} = \mathbf{A}_{\mathcal{H}\mathcal{G}}\mathbf{x}_{\mathcal{G}} = \mathbf{A}_{\mathcal{H}\mathcal{G}}\left(\mathbf{A}_{\mathcal{G}\mathcal{F}}\mathbf{x}_{\mathcal{F}}\right) = \mathbf{A}_{\mathcal{H}\mathcal{F}}\mathbf{x}_{\mathcal{F}} \tag{9.1}
$$

These transformations must be equivalent for any vector $\mathbf{x}_{\mathcal{F}}$, so successive transformations are accomplished by simple matrix multiplication:

<span id="page-109-1"></span>

$$
\mathbf{A}_{\mathcal{H}\mathcal{F}} = \mathbf{A}_{\mathcal{H}\mathcal{G}}\mathbf{A}_{\mathcal{G}\mathcal{F}} \tag{9.2}
$$

This may appear to be an obvious result, but only one other attitude representation has such a simple composition rule. Matrix multiplication is associative, meaning that $\mathbf{A}_{\mathcal{H}\mathcal{G}}(\mathbf{A}_{\mathcal{G}\mathcal{F}}\mathbf{A}_{\mathcal{F}\mathcal{E}}) = (\mathbf{A}_{\mathcal{H}\mathcal{G}}\mathbf{A}_{\mathcal{G}\mathcal{F}})\mathbf{A}_{\mathcal{F}\mathcal{E}}$. Matrix multiplication is not commutative, however, which means that $\mathbf{A}_{\mathcal{H}\mathcal{G}}\mathbf{A}_{\mathcal{G}\mathcal{F}} \neq \mathbf{A}_{\mathcal{G}\mathcal{F}}\mathbf{A}_{\mathcal{H}\mathcal{G}}$ in general. The non-commutativity of matrix multiplication is at the heart of the problem of finding a suitable attitude representation.

Transforming from frame $\mathcal{F}$ to frame $\mathcal{G}$ and back to frame $\mathcal{F}$ is effected by the matrix $\mathbf{A}_{FF} = \mathbf{A}_{\mathcal{F}\mathcal{G}}\mathbf{A}_{\mathcal{G}\mathcal{F}}$, which must be the identity matrix. Rotations must also preserve inner products and norms of vectors, so

$$
\mathbf{x}_{\mathcal{F}} \cdot \mathbf{y}_{\mathcal{F}} = \mathbf{x}_{\mathcal{G}} \cdot \mathbf{y}_{\mathcal{G}} = \left(\mathbf{A}_{\mathcal{G}\mathcal{F}}\mathbf{x}_{\mathcal{F}}\right)^T \mathbf{A}_{\mathcal{G}\mathcal{F}}\mathbf{y}_{\mathcal{F}} = \mathbf{x}_{\mathcal{F}}^T \mathbf{A}_{\mathcal{G}\mathcal{F}}^T \mathbf{A}_{\mathcal{G}\mathcal{F}}\mathbf{y}_{\mathcal{F}} \tag{9.3}
$$

These two observations mean that

$$
\mathbf{A}_{\mathcal{G}\mathcal{F}}^T = \mathbf{A}_{\mathcal{G}\mathcal{F}}^{-1} = \mathbf{A}_{\mathcal{F}\mathcal{G}} \tag{9.4}
$$

A matrix with its transpose is equal to its inverse is called an *orthogonal* matrix, and its determinant must equal $\pm 1$. The attitude matrix must be a *proper* orthogonal matrix, i.e. have determinant $+1$, in order to transform a right-handed coordinate frame to a right-handed coordinate frame.

The nine-component attitude matrix is in some ways the ideal representation of a vehicle's attitude. It has a 1:1 correspondence with physical attitudes, it varies smoothly as the physical attitude varies smoothly, its elements all have magnitudes less than or equal to one, and it follows a simple rule for combining successive rotations. It is not an efficient representation, though; only three of its nine parameters are independent because the orthogonality constraint is equivalent to six independent scalar constraints. This provides the opportunity to specify an attitude or an attitude matrix using only three parameters, but not, as was pointed out above, in a globally continuous and nonsingular fashion.

## 9.2. Euler Axis/Angle Representation

<span id="page-110-0"></span>The *Euler axis/angle* representation of a rotation matrix is based on *Euler's Theorem*, which states that the general displacement of a rigid body with one point fixed is a rotation about a fixed axis [[29](16-bibliography.md#page-171-15)]. Specify the axis by a unit vector $\vec{\boldsymbol{e}}$ and the rotation angle by $\vartheta$, and denote the matrix that maps the representations of vectors from frame $\mathcal{F}$ to frame $\mathcal{G}$ by $\mathbf{A}_{\mathcal{G}\mathcal{F}}(\mathbf{e},\vartheta)$. The rotation axis is fixed, so $\mathbf{e}$ can be its representation in either frame $\mathcal{F}$ or frame $\mathcal{G}$, which are identical. Consider the mapping of a vector $\vec{\boldsymbol{x}}$ whose representation in frame $\mathcal{F}$ is

$$
\mathbf{x}_{\mathcal{F}} = (\mathbf{e}\,\mathbf{e}^T)\mathbf{x}_{\mathcal{F}} + (\mathbf{I}_3 - \mathbf{e}\,\mathbf{e}^T)\mathbf{x}_{\mathcal{F}} \tag{9.5}
$$

where $\mathbf{I}_n$ denotes the $n\times n$ identity matrix. The first term on the right side is parallel and the second is perpendicular to to the rotation axis. The rotation does not affect the parallel component and rotates the perpendicular component through an angle $\vartheta$ around the rotation axis out of the plane defined by that axis and $\mathbf{x}_{\mathcal{F}}$, so

<span id="page-110-1"></span>

$$
\mathbf{x}_{\mathcal{G}} = \mathbf{A}_{\mathcal{G}\mathcal{F}}(\mathbf{e},\vartheta)\mathbf{x}_{\mathcal{F}} = (\mathbf{e}\,\mathbf{e}^T)\mathbf{x}_{\mathcal{F}} + \cos\vartheta\,(\mathbf{I}_3 - \mathbf{e}\,\mathbf{e}^T)\mathbf{x}_{\mathcal{F}} - \sin\vartheta\,(\mathbf{e}\times\mathbf{x}_{\mathcal{F}}) \tag{9.6}
$$

This formula preserves the norm of $\mathbf{x}_{\mathcal{F}}$ because $\mathbf{e}\times\mathbf{x}_{\mathcal{F}}$ and $(\mathbf{I}_3 - \mathbf{e}\,\mathbf{e}^T)\mathbf{x}_{\mathcal{F}}$ are orthogonal and have equal magnitude. Since $\mathbf{x}_{\mathcal{F}}$ is an arbitrary vector, Eq. [\(9.6\)](#page-110-1) means that

<span id="page-110-2"></span>

$$
\mathbf{A}(\mathbf{e},\vartheta) = (\cos\vartheta)\,\mathbf{I}_3 - \sin\vartheta\,[\mathbf{e}\times] + (1-\cos\vartheta)\,\mathbf{e}\,\mathbf{e}^T \tag{9.7}
$$

where $[\mathbf{e}\times]$ is the cross-product matrix:

$$
[\mathbf{e}\times] \equiv \begin{bmatrix} 0 & -e_3 & e_2 \\ e_3 & 0 & -e_1 \\ -e_2 & e_1 & 0 \end{bmatrix} \tag{9.8}
$$

The cross-product matrix is defined so that $[\mathbf{x}\times]\,\mathbf{y} = \mathbf{x}\times\mathbf{y}$. Equation [\(9.7\)](#page-110-2) is the *Euler axis/angle* parameterization of an attitude matrix, with explicit frame indices omitted. It requires four parameters, but only three are independent because of the unit vector constraint $\|\mathbf{e}\| = 1$.

The $\sin\vartheta$ terms in Eqs. [\(9.6\)](#page-110-1) and [\(9.7\)](#page-110-2) are negative because the rotation in Euler's theorem is an active rotation of the frame $\mathcal{G}$ relative to the frame $\mathcal{F}$, while the rotation matrix $\mathbf{A}(\mathbf{e},\vartheta)$ specifies the passive mapping of the representation of $\vec{\boldsymbol{x}}$ from frame $\mathcal{F}$ to frame $\mathcal{G}$.

The Euler axis/angle representation can be used to find the time dependence of the rotation matrix. The fundamental definition of a derivative gives

<span id="page-110-3"></span>

$$
\begin{aligned}
\dot{\mathbf{A}}_{\mathcal{G}\mathcal{F}}(t) &\equiv \lim_{\Delta t\to 0} \frac{\mathbf{A}_{\mathcal{G}\mathcal{F}}(t+\Delta t) - \mathbf{A}_{\mathcal{G}\mathcal{F}}(t)}{\Delta t} \\
&= \left(\lim_{\Delta t\to 0} \frac{\mathbf{A}_{\mathcal{G}\mathcal{F}}(t+\Delta t)\mathbf{A}_{\mathcal{F}\mathcal{G}}(t) - \mathbf{I}_3}{\Delta t}\right)\mathbf{A}_{\mathcal{G}\mathcal{F}}(t)
\end{aligned} \tag{9.9}
$$

because $\mathbf{A}_{\mathcal{F}\mathcal{G}}(t)\mathbf{A}_{\mathcal{G}\mathcal{F}}(t)$ is equal to the identity matrix. For small $\Delta t$, the matrix product $\mathbf{A}_{\mathcal{G}\mathcal{F}}(t+\Delta t)\mathbf{A}_{\mathcal{F}\mathcal{G}}(t)$ differs from the identity matrix by a small rotation, so it can be represented by a small angle approximation of Eq. [\(9.7\)](#page-110-2):

$$
\mathbf{A}_{\mathcal{G}\mathcal{F}}(t+\Delta t)\mathbf{A}_{\mathcal{F}\mathcal{G}}(t) \approx \mathbf{I}_3 - \vartheta\,[\mathbf{e}\times] \tag{9.10}
$$

Inserting this into Eq. [\(9.9\)](#page-110-3), taking the limit of as $\Delta t$ goes to zero, and omitting time arguments gives

<span id="page-110-4"></span>

$$
\dot{\mathbf{A}}_{\mathcal{G}\mathcal{F}} = -[\boldsymbol{\omega}_{\mathcal{G}}^{\mathcal{G}\mathcal{F}}\times]\mathbf{A}_{\mathcal{G}\mathcal{F}} \tag{9.11}
$$

where

<span id="page-110-5"></span>

$$
\boldsymbol{\omega}_{\mathcal{G}}^{\mathcal{G}\mathcal{F}} \equiv \lim_{\Delta t\to 0} \frac{\vartheta\,\mathbf{e}}{\Delta t} \tag{9.12}
$$

is the vector representation in frame $\mathcal{G}$ of the angular velocity of frame $\mathcal{G}$ with respect to frame $\mathcal{F}$. The angular velocity is known to be represented in frame $\mathcal{G}$ because the product $\mathbf{A}_{\mathcal{G}\mathcal{F}}(t+\Delta t)\mathbf{A}_{\mathcal{F}\mathcal{G}}(t)$ is a rotation from frame $\mathcal{G}$ at one time to frame $\mathcal{G}$ at a different time, and these two frames coincide in the limit that $\Delta t$ goes to zero. The angular velocity is usually written simply as $\boldsymbol{\omega}$, with the frames understood. Its units are rad/sec, assuming that time is measured in seconds, because radian measure was assumed in taking the small angle limit of $\sin\vartheta$.

Equation [\(9.11\)](#page-110-4) is the fundamental equation of attitude kinematics. It does not distinguish between the situations where frame $\mathcal{F}$ or frame $\mathcal{G}$ or both frames are rotating in an absolute sense; it only cares about the relative rotation between the two frames. This equation can also be written as

$$
\dot{\mathbf{A}}_{\mathcal{G}\mathcal{F}} = -\mathbf{A}_{\mathcal{G}\mathcal{F}}\mathbf{A}_{\mathcal{F}\mathcal{G}}[\boldsymbol{\omega}_{\mathcal{G}}^{\mathcal{G}\mathcal{F}}\times]\mathbf{A}_{\mathcal{F}\mathcal{G}}^T = -\mathbf{A}_{\mathcal{G}\mathcal{F}}[\mathbf{A}_{\mathcal{F}\mathcal{G}}\boldsymbol{\omega}_{\mathcal{G}}^{\mathcal{G}\mathcal{F}}\times] = -\mathbf{A}_{\mathcal{G}\mathcal{F}}[\boldsymbol{\omega}_{\mathcal{F}}^{\mathcal{G}\mathcal{F}}\times] \tag{9.13}
$$

which expresses the kinematics in terms of the representation in frame $\mathcal{F}$ of $\boldsymbol{\omega}^{\mathcal{G}\mathcal{F}}$. The second equality uses an identity that holds for any proper orthogonal matrix. These kinematic equations, if integrated exactly, preserve the orthogonality of the attitude matrix.

The Euler axis/angle representation is fundamental for analysis, as demonstrated above, but it has been entirely superseded for practical applications by a superior four-parameter representation described in the next section.

## 9.3. Quaternion Representation

<span id="page-111-0"></span>Applying trigonometric half-angle identities to Eq. [\(9.7\)](#page-110-2) gives

<span id="page-111-2"></span>

$$
\mathbf{A}(\mathbf{q}) = \left(q_4^2 - \|\mathbf{q}_{1:3}\|^2\right)\mathbf{I}_3 - 2q_4[\mathbf{q}_{1:3}\times] + 2\,\mathbf{q}_{1:3}\mathbf{q}_{1:3}^T \tag{9.14}
$$

where the three-component vector $\mathbf{q}_{1:3}$ and the scalar $q_4$ are defined by

$$
\mathbf{q}_{1:3} = \mathbf{e}\sin(\vartheta/2) \tag{9.15a}
$$

$$
q_4 = \cos(\vartheta/2) \tag{9.15b}
$$

This representation has the advantage over the Euler axis/angle representation of requiring no trigonometric function evaluations, and its four components are more economical than the nine-component attitude matrix.

The four parameters of this representation were first considered by Euler but their full significance was revealed by Rodrigues, so they are often referred to as the *Euler symmetric parameters* or *Euler-Rodrigues* parameters. This representation is called the quaternion representation and denoted $\mathbf{A}(\mathbf{q})$ because the four parameters can be regarded as the components of a quaternion

$$
\mathbf{q} = \begin{bmatrix} \mathbf{q}_{1:3} \\ q_4 \end{bmatrix} \tag{9.16}
$$

with vector part $\mathbf{q}_{1:3}$ and scalar $q_4$. A quaternion is basically four-component vector with some additional operations defined for it.[<sup>2</sup>](#page-111-1) The attitude quaternion

<span id="page-111-3"></span>

$$
\mathbf{q}(\mathbf{e},\vartheta) = \begin{bmatrix} \mathbf{e}\sin(\vartheta/2) \\ \cos(\vartheta/2) \end{bmatrix} \tag{9.17}
$$

is a unit quaternion, obeying the norm constraint $\|\mathbf{q}\| = 1$, but not all quaternions are unit quaternions. It is clear from Eq. [\(9.14\)](#page-111-2) that $\mathbf{q}$ and $-\mathbf{q}$ give the same attitude matrix. This 2:1 mapping of quaternions to rotations is a minor annoyance that cannot be removed without introducing discontinuities in the representation.

<span id="page-111-1"></span><sup>2</sup> This is *conceptually* different from the quaternion introduced by Hamilton in 1844, before the introduction of vector notation, as a hypercomplex extension $q = q_0 + iq_1 + jq_2 + kq_3$ of a complex number $z = x + iy$. The scalar part of a quaternion is often labeled $q_0$ and put at the top of the column vector. Care must be taken to thoroughly understand the conventions embodied in any quaternion equation that one chooses to reference.

The most important added quaternion operations are two different products of two quaternions $\mathbf{q}$ and $\bar{\mathbf{q}}$. They can be implemented in matrix form similar to the matrix form of the vector cross product:[<sup>3</sup>](#page-112-0)

<span id="page-112-0"></span><sup>3</sup> The notation $\mathbf{q}\otimes\bar{\mathbf{q}}$ was introduced in Ref. [[53](16-bibliography.md#page-172-11)], and $\mathbf{q}\odot\bar{\mathbf{q}}$ is a modification of notation introduced in Ref. [[68](16-bibliography.md#page-172-12)]. Hamilton's product $q\bar{q}$ corresponds to $\mathbf{q}\odot\bar{\mathbf{q}}$, but $\mathbf{q}\otimes\bar{\mathbf{q}}$ has proven to be more useful in attitude analysis. The order of the quaternion products in Eqs. [\(9.27\)](#page-113-0) and [\(9.28\)](#page-113-1) would be reversed with the classical definition of quaternion multiplication.

$$
\mathbf{q}\otimes\bar{\mathbf{q}} = [\boldsymbol{\Psi}(\mathbf{q})\ \ \mathbf{q}]\,\bar{\mathbf{q}} \tag{9.18a}
$$

<span id="page-112-4"></span>

$$
\mathbf{q}\odot\bar{\mathbf{q}} = [\boldsymbol{\Xi}(\mathbf{q})\ \ \mathbf{q}]\,\bar{\mathbf{q}} \tag{9.18b}
$$

where $\boldsymbol{\Psi}(\mathbf{q})$ and $\boldsymbol{\Xi}(\mathbf{q})$ are the $4\times 3$ matrices

<span id="page-112-1"></span>

$$
\boldsymbol{\Psi}(\mathbf{q}) \equiv \begin{bmatrix} q_4\,\mathbf{I}_3 - [\mathbf{q}_{1:3}\times] \\ -\mathbf{q}_{1:3}^T \end{bmatrix} \tag{9.19a}
$$

<span id="page-112-2"></span>

$$
\boldsymbol{\Xi}(\mathbf{q}) \equiv \begin{bmatrix} q_4\,\mathbf{I}_3 + [\mathbf{q}_{1:3}\times] \\ -\mathbf{q}_{1:3}^T \end{bmatrix} \tag{9.19b}
$$

Unlike the vector cross product, though, the norm of either product of two quaternions is equal to the product of their norms.

Both quaternion products are associative but not commutative in general, in parallel with matrix products. The two product definitions differ only in the signs of the cross product matrices in Eqs. [\(9.19a\)](#page-112-1) and [\(9.19b\)](#page-112-2), from which it follows that

<span id="page-112-3"></span>

$$
\mathbf{q}\otimes\bar{\mathbf{q}} = \bar{\mathbf{q}}\odot\mathbf{q} \tag{9.20}
$$

The identity quaternion

$$
\mathbf{I}_q \equiv \begin{bmatrix} 0 & 0 & 0 & 1 \end{bmatrix}^T \tag{9.21}
$$

acts in quaternion multiplication like the identity matrix in matrix multiplication. The conjugate $\mathbf{q}^*$ of a quaternion is obtained by changing the sign of its vector part:

$$
\mathbf{q}^* = \begin{bmatrix} \mathbf{q}_{1:3} \\ q_4 \end{bmatrix}^* \equiv \begin{bmatrix} -\mathbf{q}_{1:3} \\ q_4 \end{bmatrix} \tag{9.22}
$$

Either product of a quaternion with its conjugate is equal to the square of its norm times the identity quaternion.

The inverse of any quaternion having nonzero norm is defined by

$$
\mathbf{q}^{-1} \equiv \mathbf{q}^*/\|\mathbf{q}\|^2 \tag{9.23}
$$

A unit quaternion, such as the attitude quaternion, always has an inverse, which is identical with its conjugate. The conjugate of the product of two quaternions is equal to the product of their conjugates in the opposite order: $(\bar{\mathbf{q}}\otimes\mathbf{q})^* = \mathbf{q}^*\otimes\bar{\mathbf{q}}^*$. The same relationship holds for the other product definition and with conjugates replaced by inverses.

Equation [\(9.14\)](#page-111-2) can be compactly written as

$$
\mathbf{A}(\mathbf{q}) = \boldsymbol{\Xi}^T(\mathbf{q})\boldsymbol{\Psi}(\mathbf{q}) \tag{9.24}
$$

Now consider, for a unit quaternion $\mathbf{q}$, the product

$$
\begin{aligned}
\mathbf{q}\otimes\begin{bmatrix}\mathbf{x}\\0\end{bmatrix}\otimes\mathbf{q}^* &= \mathbf{q}^*\odot\left(\mathbf{q}\otimes\begin{bmatrix}\mathbf{x}\\0\end{bmatrix}\right) = \begin{bmatrix}\boldsymbol{\Xi}(\mathbf{q}^*) & \mathbf{q}^*\end{bmatrix}\begin{bmatrix}\boldsymbol{\Psi}(\mathbf{q}) & \mathbf{q}\end{bmatrix}\begin{bmatrix}\mathbf{x}\\0\end{bmatrix} \\
&= \begin{bmatrix}\boldsymbol{\Xi}^T(\mathbf{q})\\ \mathbf{q}^T\end{bmatrix}\boldsymbol{\Psi}(\mathbf{q})\,\mathbf{x} = \begin{bmatrix}\mathbf{A}(\mathbf{q})\,\mathbf{x}\\0\end{bmatrix}
\end{aligned} \tag{9.25}
$$

Applying a transformation by a second quaternion $\bar{\mathbf{q}}$ gives

$$
\begin{aligned}
\bar{\mathbf{q}}\otimes\left(\mathbf{q}\otimes\begin{bmatrix}\mathbf{x}\\0\end{bmatrix}\otimes\mathbf{q}^*\right)\otimes\bar{\mathbf{q}}^* &= \bar{\mathbf{q}}\otimes\begin{bmatrix}\mathbf{A}(\mathbf{q})\,\mathbf{x}\\0\end{bmatrix}\otimes\bar{\mathbf{q}}^* = \begin{bmatrix}\mathbf{A}(\bar{\mathbf{q}})\mathbf{A}(\mathbf{q})\,\mathbf{x}\\0\end{bmatrix} \\
&= (\bar{\mathbf{q}}\otimes\mathbf{q})\otimes\begin{bmatrix}\mathbf{x}\\0\end{bmatrix}\otimes(\bar{\mathbf{q}}\otimes\mathbf{q})^* = \begin{bmatrix}\mathbf{A}(\bar{\mathbf{q}}\otimes\mathbf{q})\,\mathbf{x}\\0\end{bmatrix}
\end{aligned} \tag{9.26}
$$

Because this must hold for any $\mathbf{x}$, it shows that

<span id="page-113-0"></span>

$$
\mathbf{A}(\bar{\mathbf{q}}\otimes\mathbf{q}) = \mathbf{A}(\bar{\mathbf{q}})\mathbf{A}(\mathbf{q}) \tag{9.27}
$$

This and Eq. [\(9.2\)](#page-109-1) mean that the quaternion corresponding to successive rotations is just the product

<span id="page-113-1"></span>

$$
\mathbf{q}_{\mathcal{H}\mathcal{F}} = \mathbf{q}_{\mathcal{H}\mathcal{G}}\otimes\mathbf{q}_{\mathcal{G}\mathcal{F}} \tag{9.28}
$$

A simple bilinear composition rule of this type holds only for the attitude matrix and quaternion representations, a major reason for the popularity of quaternions.

Representing the rotation between times $t$ and $t+\Delta t$ by an Euler axis and angle, Eqs. [\(9.28\)](#page-113-1), [\(9.17\)](#page-111-3), [\(9.20\)](#page-112-3), and [\(9.18b\)](#page-112-4) give

$$
\begin{aligned}
\mathbf{q}(t+\Delta t) &= \begin{bmatrix}\mathbf{e}\sin(\vartheta/2)\\ \cos(\vartheta/2)\end{bmatrix}\otimes\mathbf{q}(t) = \cos(\vartheta/2)\mathbf{q}(t) + \sin(\vartheta/2)\begin{bmatrix}\mathbf{e}\\0\end{bmatrix}\otimes\mathbf{q}(t) \\
&= \cos(\vartheta/2)\mathbf{q}(t) + \sin(\vartheta/2)\boldsymbol{\Xi}\left(\mathbf{q}(t)\right)\mathbf{e}
\end{aligned} \tag{9.29}
$$

This quaternion propagation equation has proven to be very useful. It preserves the unity norm of the attitude quaternion. If the angular velocity is well approximated as constant over the time interval, then $\vartheta = \|\boldsymbol{\omega}\|\Delta t$ and $\mathbf{e} = \boldsymbol{\omega}/\|\boldsymbol{\omega}\|$. Alternatively, and particularly for onboard applications, $\vartheta\mathbf{e}$ can be computed by differencing the outputs of rate-integrating gyroscopes.

Using small angle approximations for the sine and cosine leads to the kinematic equation for the quaternion:

<span id="page-113-2"></span>

$$
\dot{\mathbf{q}} \equiv \lim_{\Delta t\to 0}\frac{\mathbf{q}(t+\Delta t) - \mathbf{q}(t)}{\Delta t} = \frac{1}{2}\begin{bmatrix}\boldsymbol{\omega}\\0\end{bmatrix}\otimes\mathbf{q} = \frac{1}{2}\boldsymbol{\Xi}(\mathbf{q})\,\boldsymbol{\omega} \tag{9.30}
$$

where $\boldsymbol{\omega}$ is defined by Eq. [\(9.12\)](#page-110-5) and several time arguments have been omitted. Exact integration of this equation preserves the unit norm of the quaternion. The inverse of Eq. [\(9.30\)](#page-113-2) is often useful:

$$
\boldsymbol{\omega} = 2\boldsymbol{\Xi}^T(\mathbf{q})\dot{\mathbf{q}} \tag{9.31}
$$

The quaternion representation of a given attitude matrix $\mathbf{A}$ can be found by normalizing any one of the four vectors [[56](16-bibliography.md#page-172-13)]

$$
\begin{aligned}
\begin{bmatrix} 1 + 2A_{11} - \operatorname{tr}\mathbf{A} \\ A_{12} + A_{21} \\ A_{13} + A_{31} \\ A_{23} - A_{32} \end{bmatrix} &= 4q_1\mathbf{q}\,, &\qquad \begin{bmatrix} A_{21} + A_{12} \\ 1 + 2A_{22} - \operatorname{tr}\mathbf{A} \\ A_{23} + A_{32} \\ A_{31} - A_{13} \end{bmatrix} &= 4q_2\mathbf{q} \\
\begin{bmatrix} A_{31} + A_{13} \\ A_{32} + A_{23} \\ 1 + 2A_{33} - \operatorname{tr}\mathbf{A} \\ A_{12} - A_{21} \end{bmatrix} &= 4q_3\mathbf{q}\,, &\qquad \begin{bmatrix} A_{23} - A_{32} \\ A_{31} - A_{13} \\ A_{12} - A_{21} \\ 1 + \operatorname{tr}\mathbf{A} \end{bmatrix} &= 4q_4\mathbf{q}
\end{aligned} \tag{9.32}
$$

Numerical errors are minimized by choosing the vector with the greatest norm, which can be found by the following procedure. Find the largest of $\operatorname{tr}\mathbf{A}$ and the three diagonal elements of $\mathbf{A}$. If $\operatorname{tr}\mathbf{A}$ is the largest, then $|q_4|$ is the largest of the $|q_i|$, otherwise the largest value of $|q_i|$ is the one with the same index as the largest diagonal element of $\mathbf{A}$. The overall sign of the normalized vector is not determined, reflecting the twofold ambiguity of the quaternion representation.

Extracting many of the other parameterizations from an attitude matrix is most easily accomplished by first extracting a quaternion and then converting to the desired representation. The kinematic equations of these other representations can also be readily derived through the intermediary of the quaternion representation.

A three-parameter representation can be obtained by using only three components of the quaternion, say the $i, j, k$ components, with the fourth component given by

<span id="page-114-2"></span>

$$
q_\ell = \pm\sqrt{1 - q_i^2 - q_j^2 - q_k^2} \tag{9.33}
$$

The sign is not arbitrary, but is determined by the four-component quaternion being represented by three of its components. Once so determined, the sign will not change if the quaternion varies smoothly unless $q_\ell$ passes through zero. To avoid a sign error if $|q_\ell|$ becomes small, the representation is switched to make $q_\ell$ one of three components in the three-parameter representation, replacing one of the other components, which is then given by the square root with the correct sign. The unit norm constraint on the attitude quaternion means that at least one of its components must have magnitude $1/2$ or greater. To minimize switching, it should be done when $|q_\ell|$ is significantly less than $1/2$, and the component replaced by $q_\ell$ in the three-component representation should have magnitude no smaller than $1/2$. To first order in the errors, the error in the fourth component of the quaternion is

<span id="page-114-3"></span>

$$
\Delta q_\ell = -\,q_\ell^{-1}(q_i\Delta q_i + q_j\Delta q_j + q_k\Delta q_k) \tag{9.34}
$$

This approaches the indeterminate quantity $0/0$ as $|q_\ell|\to 0$, providing another reason for switching.

## 9.4. Rodrigues Parameter Representation

<span id="page-114-0"></span>The three *Rodrigues parameters* appeared in 1840 [[72](16-bibliography.md#page-172-14)], but were first arranged in a vector by Gibbs, who invented modern vector notation. For this reason, the vector of Rodrigues parameters is often called the *Gibbs vector* and denoted by $\mathbf{g}$. The Rodrigues parameters are related to the Euler axis/angle and the quaternion by

<span id="page-114-1"></span>

$$
\mathbf{g} = \mathbf{e}\tan(\vartheta/2) = \frac{\mathbf{q}_{1:3}}{q_4} \tag{9.35}
$$

The quaternion as a function of the Gibbs vector is

$$
\mathbf{q} = \frac{\pm 1}{\sqrt{1 + \|\mathbf{g}\|^2}}\begin{bmatrix}\mathbf{g}\\1\end{bmatrix} \tag{9.36}
$$

It is clear from Eq. [\(9.35\)](#page-114-1) that $\mathbf{q}$ and $-\mathbf{q}$ map to the same Gibbs vector, so the Rodrigues parameters provide a 1:1 mapping of rotations. The price paid for this is that the Gibbs vector is infinite for a $180^\circ$ rotation. Thus this parameterization is not recommended as a global attitude representation, but it provides an excellent representation of small rotations.

The Rodrigues parameter representation of the attitude matrix is

$$
\mathbf{A}(\mathbf{g}) = \mathbf{I}_3 + 2\,\frac{[\mathbf{g}\times]^2 - [\mathbf{g}\times]}{1 + \|\mathbf{g}\|^2} \tag{9.37}
$$

This resembles the quaternion representation in requiring no transcendental function evaluations, but it is a rational function rather than a simple polynomial.

The composition rule for the Rodrigues parameters corresponding to the quaternion product $\bar{\mathbf{q}}\otimes\mathbf{q}$ is

$$
\bar{\mathbf{g}} \boxtimes \mathbf{g} \equiv \frac{\bar{\mathbf{g}} + \mathbf{g} - \bar{\mathbf{g}}\times\mathbf{g}}{1 - \bar{\mathbf{g}}\cdot\mathbf{g}} \tag{9.38}
$$

This composition law is associative but not commutative in general, in parallel with matrix and quaternion products. Because it is not a bilinear function of the constituent Gibbs vectors, it cannot be represented as a matrix product like quaternion composition.

The kinematic equation for the Rodrigues parameters is

$$
\dot{\mathbf{g}} = (1/2)\left(\mathbf{I}_3 + [\mathbf{g}\times] + \mathbf{g}\mathbf{g}^T\right)\boldsymbol{\omega} \tag{9.39}
$$

with the inverse

$$
\boldsymbol{\omega} = 2\left(1 + \|\mathbf{g}\|^2\right)^{-1}\left(\dot{\mathbf{g}} - \mathbf{g}\times\dot{\mathbf{g}}\right) \tag{9.40}
$$

## 9.5. Modified Rodrigues Parameters

<span id="page-115-0"></span>The modified Rodrigues parameters (MRPs) were invented by T. F. Wiener in 1962 [[88](16-bibliography.md#page-173-14)], rediscovered by Marandi and Modi in 1987 [[55](16-bibliography.md#page-172-15)], and have been championed by Junkins and Schaub [[73](16-bibliography.md#page-172-16)]. The vector of MRPs is related to the Euler axis/angle and the quaternion by

<span id="page-115-2"></span>

$$
\mathbf{p} = \mathbf{e}\tan(\vartheta/4) = \frac{\mathbf{q}_{1:3}}{1 + q_4} \tag{9.41}
$$

The quaternion as a function of the MRPs is

$$
\mathbf{q} = \frac{1}{1 + \|\mathbf{p}\|^2}\begin{bmatrix} 2\mathbf{p} \\ 1 - \|\mathbf{p}\|^2 \end{bmatrix} \tag{9.42}
$$

and the attitude matrix is given by

$$
\mathbf{A}(\mathbf{p}) = \mathbf{I}_3 + \frac{8\,[\mathbf{p}\times]^2 - 4\left(1 - \|\mathbf{p}\|^2\right)[\mathbf{p}\times]}{(1 + \|\mathbf{p}\|^2)^2} \tag{9.43}
$$

Every vector of MRPs has a *shadow*

<span id="page-115-1"></span>

$$
\mathbf{p}^S \equiv -\frac{\mathbf{p}}{\|\mathbf{p}\|^2} = \frac{-\mathbf{q}_{1:3}}{1 - q_4} \tag{9.44}
$$

An MRP vector and its shadow represent the same attitude because $\mathbf{q}$ and $-\mathbf{q}$ represent the same attitude, so the MRPs are a 2:1 mapping of the rotations just as the quaternions are. It is clear from Eq. [\(9.44\)](#page-115-1) that $\|\mathbf{p}^S\|\|\mathbf{p}\| = 1$, so every attitude can be represented by either an MRP vector with $\|\mathbf{p}\| \le 1$ or an equivalent MRP vector in the *shadow set* of MRPs with $\|\mathbf{p}\| \ge 1$.

The MRP vector corresponding to the quaternion product $\bar{\mathbf{q}}\otimes\mathbf{q}$ follows the composition rule

$$
\bar{\mathbf{p}} \boxdot \mathbf{p} \equiv \frac{\left(1 - \|\mathbf{p}\|^2\right)\bar{\mathbf{p}} + \left(1 - \|\bar{\mathbf{p}}\|^2\right)\mathbf{p} - 2\,\bar{\mathbf{p}}\times\mathbf{p}}{1 + \|\mathbf{p}\|^2\|\bar{\mathbf{p}}\|^2 - 2\,\bar{\mathbf{p}}\cdot\mathbf{p}} \tag{9.45}
$$

This composition law is associative but not commutative in general, in parallel with matrix and quaternion products. It cannot be represented as a matrix product.

The kinematic equation for the MRPs is

<span id="page-116-1"></span>

$$
\dot{\mathbf{p}} = \frac{1 + \|\mathbf{p}\|^2}{4}\left(\mathbf{I}_3 + 2\,\frac{[\mathbf{p}\times]^2 + [\mathbf{p}\times]}{1 + \|\mathbf{p}\|^2}\right)\boldsymbol{\omega} \tag{9.46}
$$

The matrix in parentheses is orthogonal, so the inverse of Eq. [\(9.46\)](#page-116-1) is

$$
\boldsymbol{\omega} = \frac{4}{1 + \|\mathbf{p}\|^2}\left(\mathbf{I}_3 + 2\,\frac{[\mathbf{p}\times]^2 - [\mathbf{p}\times]}{1 + \|\mathbf{p}\|^2}\right)\dot{\mathbf{p}} \tag{9.47}
$$

The norm of an MRP vector can grow without limit during dynamic propagation or attitude estimation; Eq. [\(9.41\)](#page-115-2) shows that the norm is infinite for $\vartheta = 2\pi$. This singularity can be avoided by switching from the MRP vector to its shadow. The norm can be restricted to be less than or equal to unity in theory, but in practice it is best to allow the norm to exceed unity by some amount before switching in order to avoid "chattering" between the MRP and its shadow. An error $\Delta\mathbf{p}$ in an MRP vector corresponds to an error

<span id="page-116-3"></span>

$$
\Delta\mathbf{p}^S = \frac{\partial\mathbf{p}^S}{\partial\mathbf{p}}\Delta\mathbf{p} = \frac{2\mathbf{p}\mathbf{p}^T - \|\mathbf{p}\|^2\,\mathbf{I}_3}{\|\mathbf{p}\|^4}\Delta\mathbf{p} = \left[2\mathbf{p}^S(\mathbf{p}^S)^T - \|\mathbf{p}^S\|^2\,\mathbf{I}_3\right]\Delta\mathbf{p} \tag{9.48}
$$

in its shadow. This relation is useful for mapping covariance matrices into and out of the shadow set. The 2:1 four-component quaternion representation does not have these complications because the two quaternions representing the same attitude both have unit norm, so there is no need to switch between them.

## 9.6. Rotation Vector Representation

<span id="page-116-0"></span>It is convenient for analysis, but not for computations, to combine the Euler axis and angle into the three-component *rotation vector*

$$
\boldsymbol{\vartheta} \equiv \vartheta\,\mathbf{e} = 2(\cos^{-1} q_4)\frac{\mathbf{q}_{1:3}}{\|\mathbf{q}_{1:3}\|} \tag{9.49}
$$

This leads to the very elegant expression

$$
\mathbf{A}(\boldsymbol{\vartheta}) = \exp(-[\boldsymbol{\vartheta}\times]) \tag{9.50}
$$

where $\exp(\cdot)$ is the matrix exponential. This equation can be verified by expansion of it and Eq. [\(9.7\)](#page-110-2) as Taylor series in $\vartheta$ and repeated applications of the identity $[\mathbf{e}\times]^2 = \mathbf{e}\mathbf{e}^T - \mathbf{I}_3$.

The kinematic equation for the rotation vector is

<span id="page-116-2"></span>

$$
\dot{\boldsymbol{\vartheta}} = \boldsymbol{\omega} + \frac{1}{2}\,\boldsymbol{\vartheta}\times\boldsymbol{\omega} + \frac{1}{\vartheta^2}\left(1 - \frac{\vartheta}{2}\cot\frac{\vartheta}{2}\right)\boldsymbol{\vartheta}\times(\boldsymbol{\vartheta}\times\boldsymbol{\omega}) \tag{9.51}
$$

The coefficient of $\boldsymbol{\vartheta}\times(\boldsymbol{\vartheta}\times\boldsymbol{\omega})$ goes to $1/12$ as $\vartheta$ goes to zero, but it is singular for $\vartheta$ equal to any nonzero multiple of $2\pi$. The inverse of Eq. [\(9.51\)](#page-116-2) is

$$
\boldsymbol{\omega} = \dot{\boldsymbol{\vartheta}} - \frac{1 - \cos\vartheta}{\vartheta^2}\,\boldsymbol{\vartheta}\times\dot{\boldsymbol{\vartheta}} + \frac{\vartheta - \sin\vartheta}{\vartheta^3}\,\boldsymbol{\vartheta}\times(\boldsymbol{\vartheta}\times\dot{\boldsymbol{\vartheta}}) \tag{9.52}
$$

<span id="page-117-3"></span>The rotation vector is useful for the analysis of small rotations, but not for large rotations, because of both the computational cost of evaluating the matrix exponential and the kinematic singularity for $\|\boldsymbol{\vartheta}\| = 2\pi$. This singularity can be avoided, as for the MRPs, by switching from the rotation vector to its shadow

$$
\boldsymbol{\vartheta}^S \equiv \left(1 - 2\pi\|\boldsymbol{\vartheta}\|^{-1}\right)\boldsymbol{\vartheta} \tag{9.53}
$$

which represents the same attitude. This can restrict the norm of the rotation vector to $\pi$ or less in theory, but in practice it is best to allow the norm to exceed $\pi$ by some amount before switching in order to avoid "chattering" between the rotation vector and its shadow.

The properties of the rotation vector are very similar to those of the MRPs, and it has no obvious advantages over the MRPs. It has the disadvantage of requiring transcendental function evaluations to compute the attitude matrix, so it is rarely used in practical applications.

## 9.7. Euler Angles

<span id="page-117-0"></span>An Euler angle representation parameterizes a rotation by the product of three rotations about coordinate frame unit vectors:

<span id="page-117-1"></span>

$$
\mathbf{A}_{ijk}(\phi,\theta,\psi) = \mathbf{A}(\mathbf{e}_k,\psi)\mathbf{A}(\mathbf{e}_j,\theta)\mathbf{A}(\mathbf{e}_i,\phi) \tag{9.54}
$$

where $\mathbf{e}_j$, $\mathbf{e}_j$, and $\mathbf{e}_j$ are selected from the set

$$
\mathbf{e}_1 = \begin{bmatrix} 1 & 0 & 0 \end{bmatrix}^T, \quad \mathbf{e}_2 = \begin{bmatrix} 0 & 1 & 0 \end{bmatrix}^T, \quad \mathbf{e}_3 = \begin{bmatrix} 0 & 0 & 1 \end{bmatrix}^T \tag{9.55}
$$

The possible choice of axes is constrained by the requirements $i \neq j$ and $j \neq k$, leaving six symmetric sets with $ijk$ equal to 121, 131, 232, 212, 313, and 323 and six asymmetric sets with $ijk$ equal to 123, 132, 231, 213, 312, and 321. Symmetric Euler angle sets are used in classical studies of rigid body motion [[29](16-bibliography.md#page-171-15), [36](16-bibliography.md#page-171-16), [43](16-bibliography.md#page-171-17), [59](16-bibliography.md#page-172-10), [87](16-bibliography.md#page-173-15)].

The asymmetric sets of angles are called the *Tait-Bryan* angles or *roll*, *pitch*, and *yaw* angles. The latter terminology originally described the motions of ships and then was carried over into aircraft and spacecraft. Roll is a rotation about the vehicle body axis that is closest to the vehicle's usual direction of motion, and hence would be perceived as a screwing motion. The roll axis is conventionally assigned index 1. Yaw is a rotation about the vehicle body axis that is usually closest to the direction of local gravity, and hence would be be perceived as a motion that points the vehicle left or right. The yaw axis is conventionally assigned index 3. Pitch is a rotation about the remaining vehicle body axis, and hence would be perceived as a motion that points the vehicle up or down. The pitch axis is conventionally assigned index 2. Note that Eq. [\(9.54\)](#page-117-1) assigns the variables $\phi$, $\theta$, and $\psi$ based on the order of rotations in the sequence, making no definite association between these variables and either the axis labels 1, 2, and 3 or the names roll, pitch and yaw. Many authors follow a different convention, denoting roll by $\phi$, pitch by $\theta$, and yaw by $\psi$. As always, the reader consulting any source should be careful to understand the conventions that it follows.

Using the product rule and Eq. [\(9.11\)](#page-110-4) to compute the time derivative of Eq. [\(9.54\)](#page-117-1) gives

$$
\begin{aligned}
-[\boldsymbol{\omega}\times]\mathbf{A}_{ijk}(\phi,\theta,\psi) = \Big\{ &-[(\dot{\psi}\mathbf{e}_k)\times] - \mathbf{A}(\mathbf{e}_k,\psi)[(\dot{\theta}\mathbf{e}_j)\times]\mathbf{A}^T(\mathbf{e}_k,\psi) \\
&-\mathbf{A}(\mathbf{e}_k,\psi)\mathbf{A}(\mathbf{e}_j,\theta)[(\dot{\phi}\mathbf{e}_i)\times]\mathbf{A}^T(\mathbf{e}_j,\theta)\mathbf{A}^T(\mathbf{e}_k,\psi)\Big\}\,\mathbf{A}_{ijk}(\phi,\theta,\psi)
\end{aligned} \tag{9.56}
$$

The identity $\mathbf{A}[\mathbf{x}\times]\mathbf{A}^T = [(\mathbf{A}\mathbf{x})\times]$, which holds for any proper orthogonal $\mathbf{A}$, gives

<span id="page-117-2"></span>

$$
\boldsymbol{\omega} = \dot{\psi}\,\mathbf{e}_k + \dot{\theta}\mathbf{A}(\mathbf{e}_k,\psi)\mathbf{e}_j + \dot{\phi}\mathbf{A}(\mathbf{e}_k,\psi)\mathbf{A}(\mathbf{e}_j,\theta)\mathbf{e}_i = \mathbf{A}(\mathbf{e}_k,\psi)\mathbf{M}[\dot{\phi}\ \ \dot{\theta}\ \ \dot{\psi}]^T \tag{9.57}
$$

where

$$
\mathbf{M} = [\mathbf{A}(\mathbf{e}_j,\theta)\mathbf{e}_i \quad \mathbf{e}_j \quad \mathbf{e}_k\,] \tag{9.58}
$$

The second equality in Eq. [\(9.57\)](#page-117-2) makes use of $\mathbf{A}(\mathbf{e}_k,\psi)\mathbf{e}_k = \mathbf{e}_k$. The Euler angle rates as functions of the angular velocity are

$$
[\dot{\phi}\ \ \dot{\theta}\ \ \dot{\psi}]^T = \mathbf{M}^{-1}\mathbf{A}^T(\mathbf{e}_k,\psi)\boldsymbol{\omega} \tag{9.59}
$$

<span id="page-118-1"></span>This kinematic equation is singular if the determinant of $\mathbf{M}$ is zero. Equation [\(9.7\)](#page-110-2) and the Euler axis requirement that $\mathbf{e}_i\cdot\mathbf{e}_j = \mathbf{e}_j\cdot\mathbf{e}_k = 0$ gives

$$
\det\mathbf{M} = [\mathbf{A}(\mathbf{e}_j,\theta)\mathbf{e}_i]\cdot(\mathbf{e}_j\times\mathbf{e}_k) = \cos\theta\,[\,\mathbf{e}_i\cdot(\mathbf{e}_j\times\mathbf{e}_k)] - \sin\theta\,(\mathbf{e}_i\cdot\mathbf{e}_k) \tag{9.60}
$$

The triple vector product $\mathbf{e}_i\cdot(\mathbf{e}_j\times\mathbf{e}_k)$ is zero for the symmetric Euler angles, so the kinematic equations of these representations are singular if $\sin\theta = 0$. The dot product $\mathbf{e}_i\cdot\mathbf{e}_k$ is zero for the asymmetric Euler angles, so the kinematics of these representations are singular if $\cos\theta = 0$. This singularity is known as *gimbal lock* and is caused by collinearity of the *physical* rotation axis vectors of the first and third rotations in the sequence. Note that the column vector representations of these rotation axes are always parallel for the symmetric Euler angle sequences and always perpendicular for the asymmetric sequences, but this neither causes nor prevents gimbal lock.

Because Euler angles are discussed in many references on rotational motion and because they are not widely used in navigation filters, they will not be discussed further here. Kinematic equations and explicit forms of the attitude matrices for all twelve sets can be found in Refs. [[36](16-bibliography.md#page-171-16), [43](16-bibliography.md#page-171-17), [59](16-bibliography.md#page-172-10), [87](16-bibliography.md#page-173-15)].

## 9.8. Additive EKF (AEKF)

<span id="page-118-0"></span>Three-component representations are the most natural representations for filtering, because only three parameters are needed to represent rotations. As was pointed out at the beginning of this Chapter, though, all three-parameter representations of the rotation group have discontinuities or singularities. Any filter using a three-dimensional attitude representation must provide some guarantee of avoiding these singular points, either by restricting the vehicle's attitude or by switching between different parameter sets if the representation approaches a discontinuity or singularity.

The earliest Kalman filters for spacecraft attitude estimation used a roll, pitch, yaw sequence of Euler or Tait-Bryan angles discussed in Section [9.7](#page-117-0) [[21](16-bibliography.md#page-170-17),[22](16-bibliography.md#page-171-18)]. This is a very useful representation if the middle angle of the sequence, generally the pitch angle, stays well away from $\pm 90^\circ$, and has been used for Earth-pointing spacecraft with small pitch angles. One disadvantage of this representation is its trigonometric function evaluations, but this is less of an issue with the computing power now available, especially in onboard computers.

An EKF can estimate three components of a quaternion, with the fourth component being determined by the quaternion unit norm constraint, as discussed at the end of Section [9.3](#page-111-0) [[53](16-bibliography.md#page-172-11)]. If the fourth component becomes small, it must be added to the set of estimated quaternion components, with one of the other components switched out. This switch should be made when the magnitude of the fourth component is is not too close to either end of the range from 0 and $1/2$ to avoid "chattering" between component sets. The switch must be accompanied by the following covariance matrix transformation. Assuming the three components in the pre-switch representation have indices $i, j, k$ in ascending order, their $3\times 3$ covariance matrix is the symmetric matrix

$$
\mathbf{P}_{3\times 3} = \begin{bmatrix} P_{ii} & P_{ij} & P_{ik} \\ P_{ji} & P_{jj} & P_{jk} \\ P_{ki} & P_{kj} & P_{kk} \end{bmatrix} \tag{9.61}
$$

The $4\times 4$ covariance matrix of the full quaternion is formed by adding the $\ell$th row and column, keeping the indices in ascending order. The needed covariance components, using using Eqs. [\(9.33\)](#page-114-2) and [\(9.34\)](#page-114-3), are

$$
P_{m\ell} = P_{\ell m} = -q_\ell^{-1}(q_i P_{im} + q_j P_{jm} + q_k P_{km}) \quad \text{for} \quad m = i, j, k \tag{9.62a}
$$

$$
P_{\ell\ell} = q_\ell^{-2}(q_i^2 P_{ii} + q_j^2 P_{jj} + q_k^2 P_{kk} + 2q_i q_j P_{ji} + 2q_i q_k P_{ik} + 2q_j q_k P_{jk}) \tag{9.62b}
$$

<span id="page-119-3"></span>Then the row and column corresponding to the quaternion component switched out of the representation are deleted to form the new $3\times 3$ covariance matrix.

The modified Rodrigues parameters (MRPs) are non-singular for rotations of less than $360^\circ$, and the singularity can be avoided by switching to an MRP in the shadow set, as discussed in Section [9.5.](#page-115-0) The switch to the shadow set is made at some angle greater than $180^\circ$ to avoid "chattering" between the two parameter sets. The switch must be accompanied by a covariance matrix transformation using Eq. [\(9.48\)](#page-116-3)

$$
\mathbf{P}_{pp}^S = \left[2\mathbf{p}^S(\mathbf{p}^S)^T - \|\mathbf{p}^S\|^2\,\mathbf{I}_3\right]\mathbf{P}_{pp}\left[2\mathbf{p}^S(\mathbf{p}^S)^T - \|\mathbf{p}^S\|^2\,\mathbf{I}_3\right] \tag{9.63}
$$

where $\mathbf{P}_{pp}$ is the covariance before the switch, and $\mathbf{P}_{pp}^S$ is the covariance of $\mathbf{p}^S$ after the switch [[45](16-bibliography.md#page-171-19)]. This covariance mapping is simpler than the corresponding mapping for the three-component quaternion representation, and the MRP representation avoids a square root computation. The appearance of $\vartheta/4$ in Eq. [\(9.41\)](#page-115-2) as opposed to $\vartheta/2$ in Eq. [\(9.17\)](#page-111-3) means that switching will be less frequent when the MRP representation is used. For these reasons the MRP representation has become the preferred three-parameter attitude filter when the attitude is unrestricted.

The Gibbs vector or Rodrigues parameter representation has been used in an EKF [[37](16-bibliography.md#page-171-20)], but it is not well suited to filtering because of its inability to represent $180^\circ$ rotations, as discussed in Section [9.4.](#page-114-0) It provides an excellent representation of small attitude errors, however. The rotation vector, discussed in Section [9.6,](#page-116-0) is also not recommended for application in an EKF, as it has no clear advantage over the MRPs and has the disadvantage of requiring transcendental function evaluations.

The nine-component attitude matrix and the four-component quaternion represent the entire rotation group without singularities or discontinuities, but the linear measurement update in EKFs employing these representations violates the orthogonality constraint on the attitude matrix or the unit norm constraint on the quaternion. Various methods have been proposed to circumvent this difficulty, but these are not without problems [[59](16-bibliography.md#page-172-10)]. At the very least, they are inefficient due to the larger dimesionality of the covariance matrix.

## 9.9. Multiplicative EKF (MEKF)

<span id="page-119-0"></span>The multiplicative EKF (MEKF) uses the nine-component attitude matrix or the four-component quaternion as the "global" attitude representation and a three-component vector $\boldsymbol{\delta\vartheta}$ for the "local" representation of attitude errors, so that the true attitude is represented as a product

<span id="page-119-1"></span>

$$
\mathbf{A}^{\text{true}} = \boldsymbol{\delta}\mathbf{A}(\boldsymbol{\delta\vartheta})\hat{\mathbf{A}} \tag{9.64a}
$$

$$
\mathbf{q}^{\text{true}} = \boldsymbol{\delta}\mathbf{q}(\boldsymbol{\delta\vartheta})\otimes\hat{\mathbf{q}} \tag{9.64b}
$$

The constraints on the representations are satisfied because $\mathbf{A}^{\text{true}}$, $\boldsymbol{\delta}\mathbf{A}$, and $\hat{\mathbf{A}}$ are all proper orthogonal matrices, and $\mathbf{q}^{\text{true}}$, $\boldsymbol{\delta}\mathbf{q}$, and $\hat{\mathbf{q}}$ all have unit norm. The MEKF avoids the attitude restrictions or switching required by additive attitude EKFs because the error vector $\boldsymbol{\delta\vartheta}$ is assumed to be small enough to completely avoid singularities in the parameterizations $\boldsymbol{\delta}\mathbf{A}(\boldsymbol{\delta\vartheta})$ or $\boldsymbol{\delta}\mathbf{q}(\boldsymbol{\delta\vartheta})$. In some sense, though, Eq. [\(9.64\)](#page-119-1) incorporates a continuous switching of the attitude reference.

Only the quaternion version of the MEKF, which is much more widely employed, is presented here. Reference [[53](16-bibliography.md#page-172-11)] reviews its history. Any three-component attitude representation that is related to first order in $\boldsymbol{\delta\vartheta}$ to the quaternion by

<span id="page-119-2"></span>

$$
\boldsymbol{\delta}\mathbf{q} \approx \begin{bmatrix} \boldsymbol{\delta\vartheta}/2 \\ 1 \end{bmatrix} \tag{9.65}
$$

<span id="page-120-3"></span>can be used as the error vector. Common choices are the rotation vector, as suggested by the notation of Eq. [\(9.64\)](#page-119-1), two times the vector part of the quaternion, two times the vector of Rodrigues parameters, four times the vector of MRPs, or a vector of suitably indexed roll, pitch, and yaw angles [[59](16-bibliography.md#page-172-10)].

The order of the factors on the right side of Eq. [\(9.64\)](#page-119-1) means that the attitude errors are in the body reference frame. This leads to a major advantage of the MEKF, that the covariance of the attitude error angles in the body frame has a transparent physical interpretation. The covariance of estimators using other attitude representations has a less obvious interpretation unless the attitude matrix is close to the identity matrix. It is possible to reverse the order of the factors on the right side of Eq. [\(9.64\)](#page-119-1) so the attitude errors are in the reference frame [[26](16-bibliography.md#page-171-21)]. The covariance can be mapped into the body frame if desired.

The MEKF estimates $\boldsymbol{\delta\vartheta}$ and any other state variables of interest. This discussion addresses only the attitude part, as the equations for the other components of the state vector obey the usual EKF equations. The MEKF proceeds by iteration of three steps: measurement update, state vector reset, and propagation to the next measurement time. The measurement update step updates the local error state vector. The reset moves the updated information from the local error state to the global attitude representation and resets the components of the local error state to zero. The propagation step propagates the global variables to the time of the next measurement. The local error state variables do not need to be propagated because they are identically zero over the propagation step. These three steps will be discussed in more detail.

### 9.9.1. Measurement Update

The observation model in given in terms of the true global state

$$
\mathbf{y} = \mathbf{h}(\mathbf{q}^{\text{true}}) + \mathbf{v} \tag{9.66}
$$

but the measurement sensitivity matrix is the partial derivative with respect to the local error state, so the measurement sensitivity matrix is

<span id="page-120-0"></span>

$$
\mathbf{H} = \frac{\partial\mathbf{h}}{\partial\mathbf{q}}\,\frac{\partial\mathbf{q}^{\text{true}}}{\partial(\boldsymbol{\delta\vartheta})} \tag{9.67}
$$

Equations [\(9.64\)](#page-119-1), [\(9.65\)](#page-119-2), [\(9.18b\)](#page-112-4), and [\(9.20\)](#page-112-3) give, to first order in the error vector,

<span id="page-120-1"></span>

$$
\mathbf{q}^{\text{true}} \approx \begin{bmatrix} \boldsymbol{\delta\vartheta}/2 \\ 1 \end{bmatrix}\otimes\hat{\mathbf{q}} = \hat{\mathbf{q}} + \frac{1}{2}\Xi(\hat{\mathbf{q}})\boldsymbol{\delta\vartheta} \tag{9.68}
$$

Inserting the partial derivative of this with respect to $\boldsymbol{\delta\vartheta}$ into Eq. [\(9.67\)](#page-120-0) then gives

$$
\mathbf{H} = \frac{1}{2}\frac{\partial\mathbf{h}}{\partial\mathbf{q}}\,\Xi(\hat{\mathbf{q}}) \tag{9.69}
$$

Simplifications are possible in some special cases.

The Kalman gain computation and covariance update have the standard Kalman filter forms. The error state update employs the first-order Taylor expansion

$$
E\{\mathbf{h}(\mathbf{q}^{\text{true}})\} \approx \mathbf{h}(\hat{\mathbf{q}}) + \mathbf{H}\boldsymbol{\delta}\hat{\boldsymbol{\vartheta}} \tag{9.70}
$$

giving

<span id="page-120-2"></span>

$$
\boldsymbol{\delta}\hat{\boldsymbol{\vartheta}}^{+} = \boldsymbol{\delta}\hat{\boldsymbol{\vartheta}}^{-} + \mathbf{K}\left[\mathbf{y} - E\{\mathbf{h}(\mathbf{q}^{\text{true}})\}\right] = (\mathbf{I} - \mathbf{K}\mathbf{H})\boldsymbol{\delta}\hat{\boldsymbol{\vartheta}}^{-} + \mathbf{K}\left[\mathbf{y} - \mathbf{h}(\hat{\mathbf{q}}^{-})\right] \tag{9.71}
$$

### 9.9.2. Reset

The discrete measurement update assigns a finite post-update value to $\boldsymbol{\delta}\hat{\boldsymbol{\vartheta}}^{+}$, but the global state still retains the value $\hat{\mathbf{q}}^{-}$. A reset procedure is used to move the update information to a post-update estimate global state vector $\hat{\mathbf{q}}^{+}$, while simultaneously resetting $\boldsymbol{\delta}\hat{\boldsymbol{\vartheta}}$ to $\mathbf{0}_3$, the three-component vector with all zero components. The reset does not change the overall estimate, so the reset must obey

$$
\hat{\mathbf{q}}^{+} = \boldsymbol{\delta}\mathbf{q}(\mathbf{0}_3)\otimes\hat{\mathbf{q}}^{+} = \boldsymbol{\delta}\mathbf{q}(\boldsymbol{\delta}\hat{\boldsymbol{\vartheta}}^{+})\otimes\hat{\mathbf{q}}^{-} \tag{9.72}
$$

Thus the reset moves information from one part of the estimate to another part.

Every EKF includes an additive reset of the global state vector, but this is usually implicit rather than explicit. The multiplicative quaternion reset is the special feature of the MEKF. This reset has to preserve the quaternion norm, so an exact unit-norm expression for the functional dependence of $\boldsymbol{\delta}\mathbf{q}$ on $\boldsymbol{\delta\vartheta}$ must be used, not the linear approximation of Eq. [\(9.65\)](#page-119-2). Using the Rodrigues parameter vector has the practical advantage that the reset operation for this parameterization is

$$
\hat{\mathbf{q}}^{+} = \boldsymbol{\delta}\mathbf{q}(\boldsymbol{\delta}\hat{\boldsymbol{\vartheta}}^{+})\otimes\hat{\mathbf{q}}^{-} = \frac{1}{\sqrt{1 + \|\boldsymbol{\delta}\hat{\boldsymbol{\vartheta}}^{+}/2\|^2}}\begin{bmatrix} \boldsymbol{\delta}\hat{\boldsymbol{\vartheta}}^{+}/2 \\ 1 \end{bmatrix}\otimes\hat{\mathbf{q}}^{-} \tag{9.73}
$$

Using an argument similar to Eq. [\(9.68\)](#page-120-1), this can be accomplished in two steps:

$$
\mathbf{q}' = \hat{\mathbf{q}}^{-} + \frac{1}{2}\Xi(\hat{\mathbf{q}}^{-})\boldsymbol{\delta}\hat{\boldsymbol{\vartheta}}^{+} \tag{9.74}
$$

followed by

$$
\hat{\mathbf{q}}^{+} = \frac{\mathbf{q}'}{\|\mathbf{q}'\|} \tag{9.75}
$$

The first step is just the usual linear Kalman update, and the second step is equivalent to a brute force normalization of the updated quaternion. Thus the MEKF using Rodrigues parameters for the error vector provides a theoretical justification for brute force renormalization, with the added advantage of completely avoiding the accumulation of quaternion norm errors after many updates. The Rodrigues parameters also have the conceptual advantage that they map the rotation group into three-dimensional Euclidean space, with the largest possible $180^\circ$ attitude errors mapped to points at infinity. Thus probability distributions with infinitely long tails, such as Gaussian distributions, make sense in Rodrigues parameter space.

If a measurement update immediately follows a reset or propagation, the $\boldsymbol{\delta}\hat{\boldsymbol{\vartheta}}^{-}$ term on the right side of Eq. [\(9.71\)](#page-120-2) can be omitted because $\boldsymbol{\delta}\hat{\boldsymbol{\vartheta}}^{-}$ is zero. The reset is often delayed for computational efficiency until all the updates for a set of simultaneous measurements have been performed, though, in which case $\boldsymbol{\delta}\hat{\boldsymbol{\vartheta}}^{-}$ may have a finite value and all the terms in Eq. [\(9.71\)](#page-120-2) must be included. It is imperative to perform a reset before beginning the time propagation, however, to avoid the necessity of propagating $\boldsymbol{\delta}\hat{\boldsymbol{\vartheta}}$ between measurements.

There is some controversy over the question of whether the reset affects the covariance. One argument holds that it doesn't because the covariance depends not on the actual measurements but on their assumed statistics. Measurement errors are assumed to have zero mean, so the mean reset is zero. But the reset is very different from the measurement update in that it changes the reference frame for the attitude covariance, which might be expected to modify the covariance even though it adds no new information. The change in the covariance of $\boldsymbol{\delta\vartheta}$ resulting from the effect of the actual update, rather than its zero expectation, can be computed to be [[57](16-bibliography.md#page-172-17), [71](16-bibliography.md#page-172-18)]

$$
\mathbf{P}_{\vartheta\vartheta}^{\text{reset}} = \left(\mathbf{I}_3 - [\boldsymbol{\delta}\hat{\boldsymbol{\vartheta}}^{+}\times]/2\right)\mathbf{P}_{\vartheta\vartheta}^{+}\left(\mathbf{I}_3 - [\boldsymbol{\delta}\hat{\boldsymbol{\vartheta}}^{+}\times]/2\right)^T \tag{9.76}
$$

<span id="page-122-3"></span>to first order in $\boldsymbol{\delta}\hat{\boldsymbol{\vartheta}}^{+}$. Comparison with Eq. [\(9.7\)](#page-110-2) shows that the covariance reset looks to this order like a rotation by $\boldsymbol{\delta}\hat{\boldsymbol{\vartheta}}^{+}/2$, but this equivalence does not hold in higher orders. Most applications omit this covariance reset, but Reynolds has found that it speeds convergence and adds robustness in the presence of large updates, and that omitting it can even lead to filter divergence in some cases [[71](16-bibliography.md#page-172-18)].

### 9.9.3. Propagation

An EKF must propagate the expectation and covariance of the state. The MEKF is unusual in propagating the expectation $\hat{\mathbf{q}}$ and the covariance of the error-state vector. The propagation of the attitude error is found by by differentiating Eq. [\(9.64\)](#page-119-1):

<span id="page-122-0"></span>

$$
\dot{\mathbf{q}}^{\text{true}} = \boldsymbol{\delta}\dot{\mathbf{q}}\otimes\hat{\mathbf{q}} + \boldsymbol{\delta}\mathbf{q}\otimes\dot{\hat{\mathbf{q}}} \tag{9.77}
$$

The true and estimated quaternions satisfy the kinematic equations

$$
\dot{\mathbf{q}}^{\text{true}} = \frac{1}{2}\begin{bmatrix} \boldsymbol{\omega}^{\text{true}} \\ 0 \end{bmatrix}\otimes\mathbf{q}^{\text{true}} \tag{9.78a}
$$

$$
\dot{\hat{\mathbf{q}}} = \frac{1}{2}\begin{bmatrix} \hat{\boldsymbol{\omega}} \\ 0 \end{bmatrix}\otimes\hat{\mathbf{q}} \tag{9.78b}
$$

where $\boldsymbol{\omega}^{\text{true}}$ and $\hat{\boldsymbol{\omega}}$ are the true and estimated angular rates, respectively. Substituting these equations and Eq. [\(9.64\)](#page-119-1) into Eq. [\(9.77\)](#page-122-0), multiplying on the right by $\hat{\mathbf{q}}^{-1}$, and rearranging terms gives [[53](16-bibliography.md#page-172-11)]

$$
\boldsymbol{\delta}\dot{\mathbf{q}} = \frac{1}{2}\left(\begin{bmatrix} \boldsymbol{\omega}^{\text{true}} \\ 0 \end{bmatrix}\otimes\boldsymbol{\delta}\mathbf{q} - \boldsymbol{\delta}\mathbf{q}\otimes\begin{bmatrix} \hat{\boldsymbol{\omega}} \\ 0 \end{bmatrix}\right) \tag{9.79}
$$

Substituting Eq. [\(9.65\)](#page-119-2) and $\boldsymbol{\omega}^{\text{true}} = \hat{\boldsymbol{\omega}} + \boldsymbol{\delta\omega}$, where $\boldsymbol{\delta\omega}$ is the angular velocity error, and multiplying by two leads to

<span id="page-122-1"></span>

$$
\begin{bmatrix} \boldsymbol{\delta}\dot{\boldsymbol{\vartheta}} \\ 0 \end{bmatrix} = \begin{bmatrix} \hat{\boldsymbol{\omega}} \\ 0 \end{bmatrix}\otimes\begin{bmatrix} \boldsymbol{\delta\vartheta}/2 \\ 1 \end{bmatrix} - \begin{bmatrix} \boldsymbol{\delta\vartheta}/2 \\ 1 \end{bmatrix}\otimes\begin{bmatrix} \hat{\boldsymbol{\omega}} \\ 0 \end{bmatrix} + \begin{bmatrix} \boldsymbol{\delta\omega} \\ 0 \end{bmatrix}\otimes\begin{bmatrix} \boldsymbol{\delta\vartheta}/2 \\ 1 \end{bmatrix} \tag{9.80}
$$

Ignoring products of the small terms $\boldsymbol{\delta\omega}$ and $\boldsymbol{\delta\vartheta}$, in the spirit of the (linearized) EKF, the first three components of Eq. [\(9.80\)](#page-122-1) are

<span id="page-122-2"></span>

$$
\boldsymbol{\delta}\dot{\boldsymbol{\vartheta}} = -\hat{\boldsymbol{\omega}}\times\boldsymbol{\delta\vartheta} + \boldsymbol{\delta\omega} \tag{9.81}
$$

and the fourth component is $0 = 0$. Equation [\(9.81\)](#page-122-2) is the equation needed to propagate the covariance of the attitude error-angle covariance.

The expectation of Eq. [\(9.81\)](#page-122-2) is

$$
\boldsymbol{\delta}\dot{\hat{\boldsymbol{\vartheta}}} = -\hat{\boldsymbol{\omega}}\times\boldsymbol{\delta}\hat{\boldsymbol{\vartheta}} \tag{9.82}
$$

because $\boldsymbol{\delta\omega}$ has zero expectation. This says that if $\boldsymbol{\delta}\hat{\boldsymbol{\vartheta}}$ is zero at the beginning of a propagation it will remain zero through the propagation, which is equivalent to saying that $\boldsymbol{\delta}\hat{\mathbf{q}}$ will be equal to the identity quaternion throughout the propagation.

---

[← Chapter 8. Factorization Methods](08-factorization-methods.md) · [Contents](README.md) · [Chapter 10. Usability Considerations →](10-usability-considerations.md)
