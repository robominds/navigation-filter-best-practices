[← Appendix B. The Mathematics Behind the UDU Factorization](14-appendix-b-the-mathematics-behind-the-udu-factorization.md) · [Contents](README.md) · [Bibliography →](16-bibliography.md)

# <span id="page-160-0"></span>Appendix C. An Analysis of Dual Inertial-Absolute and Inertial-Relative Navigation Filters

*Contributed by Chris D'Souza*

This appendix describes a dual inertial-absolute state and dual inertial-relative state navigation filter trade study performed for Orion. The formulation of each of these filters is detailed, the advantages and disadvantages of each are discussed, and a recommendation to use the dual-inertial formulation is made. This appendix is reproduced from **CEV Flight Dynamics Technical Brief** Number FltDyn–CEV–07–141, dated December 21, 2007.

## C.1. Introduction

<span id="page-160-1"></span>Orion will need an efficient and well formulated relative navigation filter. Among the many possibilities, two of the most promising will be discussed in this report. The two are the dual inertial-absolute state navigation filter and the dual inertial-relative state navigation filter. The dual inertial-absolute state filter includes the absolute inertial state of both vehicles (with respect to the center of mass of the central body). The dual inertial-relative state navigation filter has as its states the absolute inertial state of the chaser (Orion) vehicle and the relative inertial state of the target with respect to the chaser ($\mathbf{x}_{rel} = \mathbf{x}_T - \mathbf{x}_C$).

## C.2. The Filter Dynamics

### <span id="page-160-2"></span>C.2.1. The Dual Inertial-Absolute Filter Dynamics

In general, the inertial states of the chaser vehicle can be expressed as

<span id="page-160-4"></span>

$$
\dot{\mathbf{x}}_C = \mathbf{f}_C(\mathbf{x}_C) + \mathbf{w}_C \tag{C.1}
$$

where $\mathbf{f}_C$ are the chaser nonlinear dynamics and $\mathbf{w}_C$ is the process (plant) noise (with statistics $E(\mathbf{w}_C(t)) = \mathbf{0}$[<sup>1</sup>](#page-160-3) and $E(\mathbf{w}_C(t)\mathbf{w}_C(\tau)) = Q_C\delta(t - \tau)$).

<span id="page-160-3"></span><sup>1</sup> The expectation operator $E(\cdot)$ for continuous random variables is defined as follows

$$
E(X) = \int_{-\infty}^{\infty} x \, p(x) \, dx
$$

where $p(x)$ is the probability density function.

Similarly, the inertial states of the target vehicle evolve according to

<span id="page-160-5"></span>

$$
\dot{\mathbf{x}}_T = \mathbf{f}_T(\mathbf{x}_T) + \mathbf{w}_T \tag{C.2}
$$

where $\mathbf{f}_T$ are the target nonlinear dynamics and $\mathbf{w}_T$ is the process (plant) noise (with statistics $E(\mathbf{w}_T(t)) = \mathbf{0}$ and $E(\mathbf{w}_T(t)\mathbf{w}_T(\tau)) = Q_T\delta(t-\tau)$). The nominal state dynamics can be expressed as

$$
\dot{\mathbf{x}}_{C_{nom}} = \mathbf{f}_C(\mathbf{x}_{C_{nom}}) \tag{C.3}
$$

$$
\dot{\mathbf{x}}_{T_{nom}} = \mathbf{f}_T(\mathbf{x}_{t_{nom}}) \tag{C.4}
$$

Defining

$$
\delta\mathbf{x}_C \triangleq \mathbf{x}_C - \mathbf{x}_{C_{nom}} \tag{C.5}
$$

$$
\delta\mathbf{x}_T \triangleq \mathbf{x}_T - \mathbf{x}_{T_{nom}} \tag{C.6}
$$

and taking derivatives and expanding to first-order, we get

$$
\delta\dot{\mathbf{x}}_C = A_C(\mathbf{x}_{C_{nom}})\,\delta\mathbf{x}_C + \mathbf{w}_C \tag{C.7}
$$

$$
\delta\dot{\mathbf{x}}_T = A_T(\mathbf{x}_{T_{nom}})\,\delta\mathbf{x}_T + \mathbf{w}_T \tag{C.8}
$$

where

$$
A_C(\mathbf{x}_{C_{nom}}) \triangleq \left( \frac{\partial \mathbf{f}_C}{\partial \mathbf{x}_C} \right)_{\mathbf{x}_C = \mathbf{x}_{C_{nom}}} \quad \text{and} \quad A_T(\mathbf{x}_{T_{nom}}) \triangleq \left( \frac{\partial \mathbf{f}_T}{\partial \mathbf{x}_T} \right)_{\mathbf{x}_T = \mathbf{x}_{T_{nom}}} \tag{C.9}
$$

Equivalently, we can express the filter errors as

$$
\delta\hat{\mathbf{x}}_C \triangleq \hat{\mathbf{x}}_C - \mathbf{x}_C \tag{C.10}
$$

$$
\delta\hat{\mathbf{x}}_T \triangleq \hat{\mathbf{x}}_T - \mathbf{x}_T \tag{C.11}
$$

where, with a bit of abuse of notation[<sup>2</sup>](#page-161-0)

$$
\hat{\mathbf{x}}_C \triangleq E(\mathbf{x}_C) \quad \text{and} \quad \hat{\mathbf{x}}_T \triangleq E(\mathbf{x}_T) \tag{C.12}
$$

so that the filter error dynamics evolve as

$$
\delta\dot{\hat{\mathbf{x}}}_C = A_C(\mathbf{x}_C)\,\delta\hat{\mathbf{x}}_C + \mathbf{w}_C \tag{C.13}
$$

$$
\delta\dot{\mathbf{x}}_T = A_T(\mathbf{x}_T)\,\delta\hat{\mathbf{x}}_T + \mathbf{w}_T \tag{C.14}
$$

<span id="page-161-0"></span><sup>2</sup> To be precise, $\hat{\mathbf{x}}_C$ should be written in terms of the conditional expectation

$$
\hat{\mathbf{x}}_{C_K} = E(\mathbf{x}_C \vert \mathbf{Z}_1, \cdots, \mathbf{Z}_k) \quad \text{and} \quad \hat{\mathbf{x}}_{T_K} = E(\mathbf{x}_T \vert \mathbf{Z}_1, \cdots, \mathbf{Z}_k)
$$

with measurements $\mathbf{Z}_1$ through $\mathbf{Z}_k$. At the initial time $\hat{\mathbf{x}}_{C_0} = E(\mathbf{x}_{C_0})$ and $\hat{\mathbf{x}}_{T_0} = E(\mathbf{x}_{T_0})$

We can, therefore, write the *inertial-absolute*[<sup>3</sup>](#page-161-1) filter error dynamics (dropping the functional dependence for compactness) as

$$
\begin{bmatrix} \delta\dot{\hat{\mathbf{x}}}_C \\ \delta\dot{\hat{\mathbf{x}}}_T \end{bmatrix} = \begin{bmatrix} A_C & \mathbf{0} \\ \mathbf{0} & A_T \end{bmatrix} \begin{bmatrix} \delta\hat{\mathbf{x}}_C \\ \delta\hat{\mathbf{x}}_T \end{bmatrix} + \begin{bmatrix} \mathbf{I} & \mathbf{0} \\ \mathbf{0} & \mathbf{I} \end{bmatrix} \begin{bmatrix} \mathbf{w}_C \\ \mathbf{w}_T \end{bmatrix} \tag{C.15}
$$

<span id="page-161-1"></span><sup>3</sup> In order to distinguish between the two filters, we call this filter the (dual) *inertial-absolute* filter because both the chaser and the target states are expressed in terms of absolute inertial coordinates.

Defining

$$
P_{IA} \triangleq E \left\{ \begin{bmatrix} \delta\hat{\mathbf{x}}_C \\ \delta\hat{\mathbf{x}}_T \end{bmatrix} \begin{bmatrix} \delta\hat{\mathbf{x}}_C^T & \delta\hat{\mathbf{x}}_T^T \end{bmatrix} \right\} = \begin{bmatrix} E[\delta\hat{\mathbf{x}}_C \delta\hat{\mathbf{x}}_C^T] & E[\delta\hat{\mathbf{x}}_C \delta\hat{\mathbf{x}}_T^T] \\ E[\delta\hat{\mathbf{x}}_T \delta\hat{\mathbf{x}}_C^T] & E[\delta\hat{\mathbf{x}}_T \delta\hat{\mathbf{x}}_T^T] \end{bmatrix} = \begin{bmatrix} P_{C,C} & P_{C,T} \\ P_{T,C} & P_{T,T} \end{bmatrix} \tag{C.16}
$$

where the subscript $IA$ denotes that this is the covariance associated with the inertial-absolute filter. The differential equation for the covariance (assuming that the plant/process noise for the two vehicles are independent and are independent of the states of the two vehicles) is

$$
\dot{P}_{IA} = A_{IA}P_{IA} + P_{IA}A_{IA}^T + G_{IA}Q_{IA}G_{IA}^T \tag{C.17}
$$

where

<span id="page-161-2"></span>

$$
A_{IA} = \begin{bmatrix} A_C & \mathbf{0} \\ \mathbf{0} & A_T \end{bmatrix}, \qquad G_{IA} = \begin{bmatrix} \mathbf{I} & \mathbf{0} \\ \mathbf{0} & \mathbf{I} \end{bmatrix}, \qquad Q_{IA} = \begin{bmatrix} Q_C & \mathbf{0} \\ \mathbf{0} & Q_T \end{bmatrix} \tag{C.18}
$$

with the initial condition

$$
P_{IA} = \begin{bmatrix} P_{C,C_0} & \mathbf{0} \\ \mathbf{0} & P_{T,T_0} \end{bmatrix} \tag{C.19}
$$

where $P_{C,C_0}$ and $P_{T,T_0}$ are the initial covariances of the chaser and target inertial (absolute) states, respectively. Finally, the covariance of the relative state is

$$
P_{rel,rel} = E\left[ (\delta\hat{\mathbf{x}}_C - \delta\hat{\mathbf{x}}_T)\,(\delta\hat{\mathbf{x}}_C - \delta\hat{\mathbf{x}}_T)^T \right] \tag{C.20}
$$

$$
= P_{C,C} + P_{T,T} - P_{T,C} - P_{C,T} = P_{C,C} + P_{T,T} - P_{T,C} - P_{T,C}^T \tag{C.21}
$$

### C.2.2. The Dual Inertial-Relative Filter Dynamics

Consistent with the earlier definitions, we define the inertial relative state as

$$
\mathbf{x}_{rel} \triangleq \mathbf{x}_T - \mathbf{x}_C \tag{C.22}
$$

Taking derivatives of this equation and substituting from Eqs. [\(C.1\)](#page-160-4) and [\(C.2\)](#page-160-5) yields

$$
\dot{\mathbf{x}}_{rel} = \mathbf{f}_T(\mathbf{x}_T) - \mathbf{f}_C(\mathbf{x}_C) + \mathbf{w}_T - \mathbf{w}_C \tag{C.23}
$$

Expanding this equation to first-order yields

$$
\delta\dot{\mathbf{x}}_{rel} = A_T(\mathbf{x}_T)\,\delta\hat{\mathbf{x}}_T - A_C(\mathbf{x}_C)\,\delta\hat{\mathbf{x}}_C + \mathbf{w}_T - \mathbf{w}_C \tag{C.24}
$$

$$
= A_T(\mathbf{x}_T)\,(\delta\hat{\mathbf{x}}_{rel} + \delta\hat{\mathbf{x}}_C) - A_C(\mathbf{x}_C)\,\delta\hat{\mathbf{x}}_C + \mathbf{w}_T - \mathbf{w}_C \tag{C.25}
$$

$$
= (A_T - A_C)\,\delta\hat{\mathbf{x}}_C + A_T\,\delta\hat{\mathbf{x}}_{rel} + (\mathbf{w}_T - \mathbf{w}_C) \tag{C.26}
$$

Therefore we write the *inertial-relative*[<sup>4</sup>](#page-162-0) filter error dynamics (once again dropping the functional dependence for compactness) as

$$
\begin{bmatrix} \delta\dot{\hat{\mathbf{x}}}_C \\ \delta\dot{\hat{\mathbf{x}}}_{rel} \end{bmatrix} = \begin{bmatrix} A_C & \mathbf{0} \\ A_T - A_C & A_T \end{bmatrix} \begin{bmatrix} \delta\hat{\mathbf{x}}_C \\ \delta\hat{\mathbf{x}}_T \end{bmatrix} + \begin{bmatrix} \mathbf{I} & \mathbf{0} \\ -\mathbf{I} & \mathbf{I} \end{bmatrix} \begin{bmatrix} \mathbf{w}_C \\ \mathbf{w}_T \end{bmatrix} \tag{C.27}
$$

<span id="page-162-0"></span><sup>4</sup> We refer to this filter as the *inertial-relative* filter to distinguish it from the prior *inertial-absolute* filter. In this formulation, the filter states consist of the inertial absolute chaser state and the inertial relative target state.

Defining, as before,

$$
P_{IR} \triangleq E \left\{ \begin{bmatrix} \delta\hat{\mathbf{x}}_C \\ \delta\hat{\mathbf{x}}_{rel} \end{bmatrix} \begin{bmatrix} \delta\hat{\mathbf{x}}_C^T & \delta\hat{\mathbf{x}}_{rel}^T \end{bmatrix} \right\} = \begin{bmatrix} E[\delta\hat{\mathbf{x}}_C\, \delta\hat{\mathbf{x}}_C^T] & E[\delta\hat{\mathbf{x}}_C\, \delta\hat{\mathbf{x}}_{rel}^T] \\ E[\delta\hat{\mathbf{x}}_{rel}\, \delta\hat{\mathbf{x}}_C^T] & E[\delta\hat{\mathbf{x}}_{rel}\, \delta\hat{\mathbf{x}}_{rel}^T] \end{bmatrix} \tag{C.28}
$$

$$
= \begin{bmatrix} P_{C,C} & P_{C,rel} \\ P_{rel,C} & P_{rel,rel} \end{bmatrix} \tag{C.29}
$$

where the subscript $IR$ denotes that this is the covariance associated with the inertial-relative filter. The differential equation for the covariance is

<span id="page-162-2"></span>

$$
\dot{P}_{IR} = A_{IR}P_{IR} + P_{IR}A_{IR}^T + G_{IR}Q_{IR}G_{IR}^T \tag{C.30}
$$

where

<span id="page-162-3"></span>

$$
A_{IR} = \begin{bmatrix} A_C & \mathbf{0} \\ A_T - A_C & A_T \end{bmatrix}, \qquad G_{IR} = \begin{bmatrix} \mathbf{I} & \mathbf{0} \\ -\mathbf{I} & \mathbf{I} \end{bmatrix}, \qquad Q_{IR} = \begin{bmatrix} Q_C & \mathbf{0} \\ \mathbf{0} & Q_T \end{bmatrix} \tag{C.31}
$$

where the initial covariance of the inertial-relative state is found to be[<sup>5</sup>](#page-162-1)

$$
P_{IR_0} = \begin{bmatrix} P_{C,C_0} & P_{C,rel_0} \\ P_{rel,C_0} & P_{rel,rel_0} \end{bmatrix} = \begin{bmatrix} P_{C,C_0} & -P_{C,C_0} \\ -P_{C,C_0} & P_{C,C_0} + P_{T,T_0} \end{bmatrix} \tag{C.32}
$$

in order to be consistent with the inertial-absolute formulation.

<span id="page-162-1"></span><sup>5</sup> We assume that at the initial time, the chaser and target initial error covariance matrices are uncorrelated.

We can also express Eqs. [\(C.30\)](#page-162-2) and [\(C.31\)](#page-162-3) as

$$
\dot{P}_{IR} = A_{IR}P_{IR} + P_{IR}A_{IR}^T + Q'_{IR} \tag{C.33}
$$

where

$$
Q'_{IR} = \begin{bmatrix} Q_C & -Q_C \\ -Q_C & Q_{rel} \end{bmatrix} \tag{C.34}
$$

where $Q_{rel} = Q_T + Q_C$. This *may* simplify tuning. While the covariance of the relative state is easily determined since it is the lower right partition of the covariance matrix ($P_{rel,rel}$), the covariance of the target vehicle (inertial) state is found (after a bit of manipulation) to be

$$
P_{T,T} = P_{rel,rel} + P_{C,C} + P_{rel,C} + P_{C,rel} = P_{rel,rel} + P_{C,C} + P_{rel,C} + P_{rel,C}^T \tag{C.35}
$$

## C.3. Incorporation of Measurements

<span id="page-163-0"></span>Whereas the previous section analyzed the filter error dynamics/propagation as it applies to the inertial-absolute and inertial-relative filter formulation, this section will analyze the difference in measurement processing between the two filters. Obviously, those measurements that are tied only to the chaser absolute inertial state have the same instantiation in both formulations. This section will only address those measurement types which have different formulations in the two filters. In particular, the measurement and the measurement partials will be discussed.

### C.3.1. The Dual Inertial-Absolute Measurement Formulations

#### C.3.1.1. The Target Inertial State Ground Update

There will be instances during which the onboard filter will need to process ground updates of the target vehicle. For the inertial-absolute formulation, the measurement takes the following expression

$$
\mathbf{z}_{T_{GU}}^{IA} = \mathbf{x}_T + \boldsymbol{\nu}_{T_{GU}} \quad \text{and} \quad \boldsymbol{\nu}_{T_{GU}} \sim N(\mathbf{0}, R_{T_{GU}}) \tag{C.36}
$$

Since the target state is a member of this filter's state-space, the measurement partials matrix associated with this measurement for the inertial-absolute formulation is

<span id="page-163-1"></span>

$$
H_{T_{GU}}^{IA} = \begin{bmatrix} \mathbf{0} & \mathbf{I} \end{bmatrix} \tag{C.37}
$$

#### C.3.1.2. Range Measurements

For the case of range measurements (either from the RF link or from the Lidar), the measurement equation can be written simply as

$$
\mathbf{z}_{range}^{IA} = \sqrt{(\mathbf{r}_T - \mathbf{r}_C) \cdot (\mathbf{r}_T - \mathbf{r}_C)} + b_{range} + \nu_{range} \tag{C.38}
$$

with the range (measurement) noise statistics $\nu_{range} \sim N(0, R_{range})$. Since the target state is a member of this filter's state-space, the measurement partials associated with this measurement for the inertial-absolute measurement are

$$
\frac{\partial \mathbf{z}_{range}^{IA}}{\partial \mathbf{r}_C} = -\mathbf{u}_{rel}^T \tag{C.39}
$$

$$
\frac{\partial \mathbf{z}_{range}^{IA}}{\partial \mathbf{v}_C} = \mathbf{0}_{1 \times 3} \tag{C.40}
$$

$$
\frac{\partial \mathbf{z}_{range}^{IA}}{\partial \mathbf{r}_T} = \mathbf{u}_{rel}^T \tag{C.41}
$$

$$
\frac{\partial \mathbf{z}_{range}^{IA}}{\partial \mathbf{v}_T} = \mathbf{0}_{1 \times 3} \tag{C.42}
$$

where

$$
\mathbf{u}_{rel} = \frac{(\mathbf{r}_T - \mathbf{r}_C)}{\lvert\mathbf{r}_T - \mathbf{r}_C\rvert} \tag{C.43}
$$

#### <span id="page-164-2"></span>C.3.1.3. Bearing Measurements

Bearing measurements, which can be obtained from either the star-tracker or the lidar, are

<span id="page-164-0"></span>

$$
\mathbf{z}_{bearing}^{IA} = \begin{bmatrix} \alpha \\ \delta \end{bmatrix} + \begin{bmatrix} b_\alpha \\ b_\delta \end{bmatrix} + \begin{bmatrix} \nu_\alpha \\ \nu_\delta \end{bmatrix} = \begin{bmatrix} \alpha \\ \delta \end{bmatrix} + \mathbf{b}_{bearing} + \boldsymbol{\nu}_{bearing} \tag{C.44}
$$

where the angles $\alpha$ and $\delta$, the azimuth and elevation angles in the sensor frame with biases $b_\alpha$ and $b_\delta$, and with noise characteristics

<span id="page-164-1"></span>

$$
E\left(\boldsymbol{\nu}_{bearing}\right) = \mathbf{0}_{2 \times 1} \quad \text{and} \quad E\left(\boldsymbol{\nu}_{bearing}\boldsymbol{\nu}_{bearing}^T\right) = \begin{bmatrix} R_{\alpha} & 0 \\ 0 & R_{\delta} \end{bmatrix} \tag{C.45}
$$

We can express $\alpha$ and $\delta$ in terms of the line-of-sight vector which is defined as

$$
\begin{bmatrix} \cos\alpha\,\cos\delta \\ \sin\alpha\,\cos\delta \\ \sin\delta \end{bmatrix} \triangleq \frac{1}{r} T_{SB}(q_{SB}) T_{BI}(q_{BI})\,(\mathbf{r}_T - \mathbf{r}_C) \tag{C.46}
$$

where $T_{SB}$ is the transformation matrix from the body (IMU) frame to the sensor frame (with $q_{SB}$ being the quaternion associated with the transformation from body frame to sensor frame) and $T_{BI}$ is the transformation matrix from the inertial frame to the body (IMU) frame (with $q_{BI}$ being the quaternion associated with the transformation from the inertial frame to the body frame).

With this in hand, the measurement partials can be obtained (after a bit of manipulation [1]) to be

$$
\frac{\partial \alpha}{\partial \mathbf{r}_C} = -\frac{\mathbf{u}_\alpha^T}{r} T_{SB}(q_{SB}) T_{BI}(q_{BI}) \tag{C.47}
$$

$$
\frac{\partial \alpha}{\partial \mathbf{v}_C} = \mathbf{0}_{1 \times 3} \tag{C.48}
$$

$$
\frac{\partial \alpha}{\partial \mathbf{r}_T} = \frac{\mathbf{u}_\alpha^T}{r} T_{SB}(q_{SB}) T_{BI}(q_{BI}) \tag{C.49}
$$

$$
\frac{\partial \alpha}{\partial \mathbf{v}_T} = \mathbf{0}_{1 \times 3} \tag{C.50}
$$

and

$$
\frac{\partial \delta}{\partial \mathbf{r}_C} = -\frac{\mathbf{u}_\delta^T}{r} T_{SB}(q_{SB}) T_{BI}(q_{BI}) \tag{C.51}
$$

$$
\frac{\partial \delta}{\partial \mathbf{v}_C} = \mathbf{0}_{1\times 3} \tag{C.52}
$$

$$
\frac{\partial \delta}{\partial \mathbf{r}_T} = \frac{\mathbf{u}_\delta^T}{r} T_{SB}(q_{SB}) T_{BI}(q_{BI}) \tag{C.53}
$$

$$
\frac{\partial \delta}{\partial \mathbf{v}_T} = \mathbf{0}_{1\times 3} \tag{C.54}
$$

where

$$
\mathbf{u}_\alpha = \frac{1}{\cos \delta} \begin{bmatrix} -\sin \alpha \\ \cos \alpha \\ 0 \end{bmatrix} \tag{C.55}
$$

$$
\mathbf{u}_\delta = \begin{bmatrix} -\cos \alpha \, \sin \delta \\ -\sin \alpha \, \sin \delta \\ \cos \delta \end{bmatrix} \tag{C.56}
$$

*Erratum (Markdown edition):* The source PDF prints the second component of (C.56) as $-\cos\alpha\,\cos\delta$. It is corrected here to $-\sin\alpha\,\sin\delta$, which is $\partial/\partial\delta$ of the line-of-sight vector in (C.46), is a unit vector, and agrees with the identical expression (C.74).

### C.3.2. The Dual Inertial-Relative Measurement Formulations

#### C.3.2.1. The Target Inertial State Ground Update

For the inertial-relative formulation, the measurement takes the following expression

$$
\mathbf{z}_{T_{GU}}^{IR} = \mathbf{x}_{rel} + \mathbf{x}_C + \boldsymbol{\nu}_{T_{GU}} \quad \text{and} \quad \boldsymbol{\nu}_{T_{GU}} \sim N(\mathbf{0}, R_{T_{GU}}) \tag{C.57}
$$

Since the target state is not a member of this filter's state-space, the measurement partials matrix associated with this measurement for the inertial-relative formulation is

<span id="page-165-1"></span>

$$
H_{T_{GU}}^{IR} = \begin{bmatrix} \mathbf{I} & \mathbf{I} \end{bmatrix} \tag{C.58}
$$

#### C.3.2.2. Range Measurements

For the case of range measurements with the inertial-relative filter, the measurement equation can be written simply as

$$
\mathbf{z}_{range}^{IA} = \sqrt{\mathbf{r}_{rel}^T \, \mathbf{r}_{rel}} + b_{range} + \nu_{range} \tag{C.59}
$$

with, as before, the range (measurement) noise statistics $\nu_{range} \sim N(0, R_{range})$. Since the relative state is a member of this filter's state-space, the measurement partials associated with this measurement for the inertial-relative measurement are

$$
\frac{\partial \mathbf{z}_{range}^{IA}}{\partial \mathbf{r}_C} = \mathbf{0}_{1 \times 3} \tag{C.60}
$$

$$
\frac{\partial \mathbf{z}_{range}^{IA}}{\partial \mathbf{v}_C} = \mathbf{0}_{1 \times 3} \tag{C.61}
$$

$$
\frac{\partial \mathbf{z}_{range}^{IA}}{\partial \mathbf{r}_{rel}} = \frac{\mathbf{r}_{rel}^T}{\lvert\mathbf{r}_{rel}\rvert} \tag{C.62}
$$

$$
\frac{\partial \mathbf{z}_{range}^{IA}}{\partial \mathbf{v}_{rel}} = \mathbf{0}_{1 \times 3} \tag{C.63}
$$

#### C.3.2.3. Bearing Measurements

Bearing measurements, as in the previous formulation (in Eqs. [\(C.44\)](#page-164-0) and [\(C.45\)](#page-164-1)), can be expressed in terms of the line-of-sight vector and the relative position vector which can be expressed as follows

<span id="page-165-0"></span>

$$
\begin{bmatrix} \cos\alpha\,\cos\delta \\ \sin\alpha\,\cos\delta \\ \sin\delta \end{bmatrix} = \frac{1}{r} T_{SB}(q_{SB}) T_{BI}(q_{BI})\,\mathbf{r}_{rel} \tag{C.64}
$$

the quantities in Eq. [\(C.64\)](#page-165-0) are defined in Section [C.3.1.3.](#page-164-2) The measurement partials are expressed as

$$
\frac{\partial \alpha}{\partial \mathbf{r}_C} = \mathbf{0}_{1 \times 3} \tag{C.65}
$$

$$
\frac{\partial \alpha}{\partial \mathbf{v}_C} = \mathbf{0}_{1 \times 3} \tag{C.66}
$$

$$
\frac{\partial \alpha}{\partial \mathbf{r}_{rel}} = \frac{\mathbf{u}_\alpha^T}{r} T_{SB}(q_{SB}) T_{BI}(q_{BI}) \tag{C.67}
$$

$$
\frac{\partial \alpha}{\partial \mathbf{v}_{rel}} = \mathbf{0}_{1 \times 3} \tag{C.68}
$$

and

$$
\frac{\partial \delta}{\partial \mathbf{r}_C} = \mathbf{0}_{1\times 3} \tag{C.69}
$$

$$
\frac{\partial \delta}{\partial \mathbf{v}_C} = \mathbf{0}_{1 \times 3} \tag{C.70}
$$

$$
\frac{\partial \delta}{\partial \mathbf{r}_{rel}} = \frac{\mathbf{u}_\delta^T}{r} T_{SB}(q_{SB}) T_{BI}(q_{BI}) \tag{C.71}
$$

$$
\frac{\partial \delta}{\partial \mathbf{v}_{rel}} = \mathbf{0}_{1 \times 3} \tag{C.72}
$$

where

$$
\mathbf{u}_\alpha = \frac{1}{\cos \delta} \begin{bmatrix} -\sin \alpha \\ \cos \alpha \\ 0 \end{bmatrix} \tag{C.73}
$$

$$
\mathbf{u}_\delta = \begin{bmatrix} -\cos \alpha \, \sin \delta \\ -\sin \alpha \, \sin \delta \\ \cos \delta \end{bmatrix} \tag{C.74}
$$

## C.4. Analysis of the Merits of the Inertial-Absolute and Inertial-Relative Filters

<span id="page-166-0"></span>The Flight Day 1 rendezvous trajectory and models as described in [2] were used to analyze the two filter formulations. Both formulations had the same driving dynamics and measurement models – only the covariance propagation and covariance updates were different. With this in mind, the comparison of the two filter formulation as it related to covariance operations were analyzed.

### C.4.1. Covariance Propagation

First it must be pointed out that the propagation of the filter dynamics are identical between both filter parameterizations. That is to say, in each filter, the inertial absolute states of both the chaser vehicle and the target vehicle will be propagated. The difference arises in the propagation of the covariance matrices associated with each of the filter paramerizations. In the *IA* filter, the covariances (and cross-covarinces) of the chaser inertial states and the target inertial states are computed. It should be noted that the *dynamics* of the two vehicles' states are inherently *un*-correlated (see $A_{IA}$ in Eq. [\(C.18\)](#page-161-2)). In contrast, for the *IR* filter the covariances (and cross-covariances) the chaser inertial states and the inertial relative states (of the target with respect to the chaser) are computed. It should be noted that the *dynamics* in this filter's states are inherently *correlated* (see $A_{IR}$ in Eq. [\(C.31\)](#page-162-3)). Hence, there are inherently more non-zero computations (both additions and multiplications) involved[<sup>6</sup>](#page-166-1). Hence, there is more room for round-off errors in the covariance propagation in the *IR* filter. In order to see this, Table 1 contains an analysis of the propagation error as a function of the propagation interval. This propagation is carried out without process noise on either the chaser or target states. In addition, the chaser and the target states are uncorrelated at the initial time. Hence, since there are no measurements which could correlate the two vehicles' states, the correlation coefficients should remain zero (i.e. $P_{C,T} = \mathbf{0}_{6\times 6}$) throughout the interval. This was verified to be the case. Because of the reduced number of computations inherent in the *IA* filter formulation, it was assumed that the *IA* filter propagation was the 'truth' and the *IR* filter was compared to it.

<span id="page-166-1"></span><sup>6</sup> First, notice that in the *IR* filter, the term $A_T - A_C$ will inherently cause a loss of precision. Second, assuming only the gravity gradient term in $A$, which is symmetric, $A_T - A_C$ involves 6 additions/subtractions. The term $(A_T - A_C)P_{CC}$ in Eqs. [\(C.30\)](#page-162-2) and [\(C.31\)](#page-162-3) involve 18 multiplications and 12 additions/subtractions. The term $(A_T - A_C)P_{C,rel}$ (or $P_{rel,C}(A_T - A_C)^T$) involve 27 multiplications and 18 additions/subtractions. The terms $(A_T - A_C)P_{CC} + A_T P_{rel,C}$ and $(A_T - A_C)P_{C,rel} + A_T P_{rel,rel}$ each involve 9 additions/subtractions. These total 45 multiplications and 54 additions/subtractions. This is doubled because of the symmetric nature of the covariance matrix. Therefore, there are 90 *additional* multiplications and 108 *additional* additions/subtractions *per function evaluation* in the *IR* filter formulation over the *IA* filter formulation. For a fourth-order Runge-Kutta integration method, the *IR* filter formulation results in an *additional* 360 multiplications and 432 additions/subtractions *per integration step.* Each of these operations results in a numerical loss of precision in finite-state machines.

| $\Delta t (sec)$ | $\vert P_{rel,rel}\vert_2$ | $\vert P_{T,T}\vert_2$ | $\vert\delta P_{rel,rel}\vert_2/\vert P_{rel,rel}\vert_2$ | $\vert\delta P_{T,T}\vert_2/\vert P_{T,T}\vert_2$ |
|-------|---------|---------|-----------|-----------|
| 100   | 1.010E7 | 4.150E3 | 1.529E-16 | 4.867E-13 |
| 1000  | 6.997E7 | 4.519E3 | 5.729E-9  | 8.869E-6  |
| 10000 | 1.239E9 | 7.943E4 | 1.926E-5  | 0.349     |

Table 1. Numerical Precision Comparison of the *IA* and *IR* filter formulations for propagation *without* process noise

| $\Delta t (sec)$ | $\vert P_{rel,rel}\vert_2$ | $\vert P_{T,T}\vert_2$ | $\vert\delta P_{rel,rel}\vert_2/\vert P_{rel,rel}\vert_2$ | $\vert\delta P_{T,T}\vert_2/\vert P_{T,T}\vert_2$ |
|-------|---------|---------|-----------|-----------|
| 100   | 1.010E7 | 4.150E3 | 1.236E-13 | 1.551E-7  |
| 1000  | 6.997E7 | 4.519E3 | 2.172E-8  | 2.320E-4  |
| 10000 | 1.239E9 | 7.943E4 | 1.905E-5  | 0.392     |

Table 2. Numerical Precision Comparison of the *IA* and *IR* filter formulations for propagation *with* process noise

It is clear that the additional non-zero multiplications and additions for the *IR* filter formulation compared to the *IA* formulation result in a build-up of round-off error. This has the effect of reducing the propagation accuracy of the *IR* filter vis-à-vis the *IA* filter. The additional operations, in concert with the accompanying loss of precision, make a strong case for the use of the *IA* filter formulation.

### C.4.2. Measurement Update

It should be apparent from comparing Eqs. [\(C.37\)](#page-163-1) and [\(C.58\)](#page-165-1) that for the case of the target ground-update, there are 18 more multiplications (because of the identity matrix) for the *IR* formulation than the *IA* formulation for each target ground-update.

For all other relative measurements, there are more operations for the *IA* filter formulation than for the *IR* formulation. In fact, for the range measurements, there are more 54 multiplications and 54 more additions for the *IA* formulation than the *IR* formulation for *each* range measurement update.

For bearing measurements, there are more 108 multiplications and 108 more additions for the *IA* formulation than the *IR* formulation for *each* bearing measurement update.

So, for relative sensor measurements, clearly there are more multiplications and more additions for the *IA* filter formulation than for the *IR* formulation.

## C.5. Conclusions

<span id="page-167-0"></span>While the inertial-absolute and inertial-relative filter formulations are mathematically equivalent, the implementation on finite-state machines influences the choice.

With regard to propagation of the covariance matrices, there are more computations for the *IR* filter than the (mathematically equivalent) *IA* filter. These additional computations, in concert with the types of operations, result in a (significant) loss of precision with regard to the propagation of the covariance matrices.

With regard to the measurement updates to the covariance matrices, for the case of relative navigation measurements, there are fewer non-zero operations for the *IR* filter than for the *IA* filter. This is one of the strengths of this filter (*IR*) formulation, and if the computation and precision with regard to the propagation of the covariance matrices were the same, the *IR* filter would be advantageous in terms of computations and precision.

---

[← Appendix B. The Mathematics Behind the UDU Factorization](14-appendix-b-the-mathematics-behind-the-udu-factorization.md) · [Contents](README.md) · [Bibliography →](16-bibliography.md)
