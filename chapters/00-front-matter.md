[Contents](README.md) · [Chapter 1. The Extended Kalman Filter →](01-the-extended-kalman-filter.md)

NASA/TP–2018–219822/Revision

![](../_page_0_Picture_1.jpeg)

# Navigation Filter Best Practices

*Edited By*

*J. Russell Carpenter*  
*Goddard Space Flight Center, Greenbelt, Maryland*

*Christopher N. D'Souza*  
*Johnson Space Center, Houston, Texas*

National Aeronautics and Space Administration  
NASA Engineering and Safety Center  
Hampton, Virginia 23681

March 2025

## NASA STI Program Report Series

Since its founding, NASA has been dedicated to the advancement of aeronautics and space science. The NASA scientific and technical information (STI) program plays a key part in helping NASA maintain this important role.

The NASA STI Program operates under the auspices of the Agency Chief Information Officer. It collects, organizes, provides for archiving, and disseminates NASA's STI. The NASA STI Program provides access to the NTRS Registered and its public interface, the NASA Technical Report Server, thus providing one of the largest collections of aeronautical and space science STI in the world. Results are published in both non-NASA channels and by NASA in the NASA STI Report Series, which includes the following report types:

- TECHNICAL PUBLICATION. Reports of completed research or a major significant phase of research that present the results of NASA programs and include extensive data or theoretical analysis. Includes compilations of significant scientific and technical data and information deemed to be of continuing reference value. NASA counterpart of peer-reviewed formal professional papers, but having less stringent limitations on manuscript length and extent of graphic presentations.
- TECHNICAL MEMORANDUM. Scientific and technical findings that are preliminary or of specialized interest, e.g., quick release reports, working papers, and bibliographies that contain minimal annotation. Does not contain extensive analysis.
- CONTRACTOR REPORT. Scientific and technical findings by NASA-sponsored contractors and grantees.
- CONFERENCE PUBLICATION. Collected papers from scientific and technical conferences, symposia, seminars, or other meetings sponsored or co-sponsored by NASA.
- SPECIAL PUBLICATION. Scientific, technical, or historical information from NASA programs, projects, and missions, often concerned with subjects having substantial public interest.
- TECHNICAL TRANSLATION. English-language translations of foreign scientific and technical material pertinent to NASA's mission.

Specialized services also include organizing and publishing research results, distributing specialized research announcements and feeds, providing information desk and personal search support, and enabling data exchange services.

For more information about the NASA STI Program, see the following:

- Access the NASA STI program home page at http://www.sti.nasa.gov
- Help desk contact information: https://www.sti.nasa.gov/sti-contact-form/ and select the "General" help request type.

---

The use of trademarks or names of manufacturers in this report is for accurate reporting and does not constitute an official endorsement, either expressed or implied, of such products or manufacturers by the National Aeronautics and Space Administration.

Available from:

NASA STI Program / Mail Stop 150  
NASA Langley Research Center  
Hampton, VA 23681-2199

---

![](../_page_4_Picture_0.jpeg)

NASA Engineering and Safety Center

**Navigation Filter Best Practices**

Second Edition

*J. Russell Carpenter and Christopher N. D'Souza, Editors*

with contributions from

Shyam Bhaskaran, J. Russell Carpenter, Christopher N. D'Souza, Cheryl J. Gramling, F. Landis Markley, James McCabe, Timothy McElrath, Lincoln Wood, Renato Zanetti

January 29, 2025

This material is declared a work of the US Government and is not subject to copyright protection in the United States, but may be subject to US Government copyright in other countries.

---

> If there be two subsequent events, the probability of the second $b/N$ and the probability of both together $P/N$, and it being first discovered that the second event has also happened, from hence I guess that the first event has also happened, the probability I am right is $P/b$.
>
> — Thomas Bayes, c. 1760

> The explicit calculation of the optimal estimate as a function of the observed variables is, in general, impossible.
>
> — Rudolph Kalman, 1960.

> The use of Kalman Filtering techniques in the on-board navigation systems for the Apollo Command Module and the Apollo Lunar Excursion Module was an important factor in the overwhelming success of the Lunar Landing Program.
>
> — Peter Kachmar, 2002.

*Dedicated to the memory of Landis Markley, Gene Muller, Emil Schiesser, and Bill Lear.*

# Contents

| Section | Page |
|---|---|
| Foreword to the Second Edition | v |
| Foreword to the First Edition | vii |
| Editors' Preface to the Second Edition | ix |
| Editors' Preface to the First Edition | xi |
| Notational Conventions | xv |
| **Chapter 1. The Extended Kalman Filter** | 1 |
| &emsp;1.1. The Additive Extended Kalman Filter | 1 |
| &emsp;1.2. The Multiplicative Extended Kalman Filter | 6 |
| **Chapter 2. Batch-Sequential Filters** | 9 |
| &emsp;2.1. Batch and Batch-Sequential Filters | 9 |
| &emsp;2.2. Onboard Navigation Using Batch-Sequential Filters | 10 |
| **Chapter 3. The Covariance Matrix** | 15 |
| &emsp;3.1. Metrics for Orbit State Covariances | 15 |
| &emsp;3.2. Covariance Propagation | 21 |
| &emsp;3.3. Covariance Measurement Update | 31 |
| &emsp;3.4. Sigma-Point Methods | 33 |
| **Chapter 4. Processing Measurements** | 35 |
| &emsp;4.1. Measurement Latency | 35 |
| &emsp;4.2. Invariance to the Order of Measurement Processing | 36 |
| &emsp;4.3. Processing Vector Measurements | 37 |
| &emsp;4.4. Filter Cascades | 38 |
| &emsp;4.5. Use of Data from Inertial Sensors | 38 |
| **Chapter 5. Measurement Underweighting** | 41 |
| &emsp;5.1. Introduction | 41 |
| &emsp;5.2. Nonlinear Effects and the Need for Underweighting | 42 |
| &emsp;5.3. Underweighting Measurements | 46 |
| &emsp;5.4. Pre-Flight Tuning Aids | 47 |
| **Chapter 6. Bias Modeling** | 49 |
| &emsp;6.1. Zero-Input Bias State Models | 49 |
| &emsp;6.2. Single-Input Bias State Models | 51 |
| &emsp;6.3. Multi-Input Bias State Models | 56 |
| **Chapter 7. State Representations** | 61 |
| &emsp;7.1. Selection of Solve-For State Variables for Estimation | 61 |
| &emsp;7.2. Units and Precision | 61 |
| &emsp;7.3. Coordinate and Time Systems | 61 |
| &emsp;7.4. Orbit Parameterizations | 62 |
| &emsp;7.5. Relative State Representations | 62 |
| &emsp;7.6. Modeling Inertial Components | 66 |
| **Chapter 8. Factorization Methods** | 71 |
| &emsp;8.1. Why Use the UDU Factorization? | 71 |
| &emsp;8.2. Preliminaries | 72 |
| &emsp;8.3. The Time Update of the Covariance | 73 |
| &emsp;8.4. The Measurement Update | 80 |
| &emsp;8.5. Conclusions | 84 |
| **Chapter 9. Attitude Estimation** | 85 |
| &emsp;9.1. Attitude Matrix Representation | 85 |
| &emsp;9.2. Euler Axis/Angle Representation | 87 |
| &emsp;9.3. Quaternion Representation | 88 |
| &emsp;9.4. Rodrigues Parameter Representation | 91 |
| &emsp;9.5. Modified Rodrigues Parameters | 92 |
| &emsp;9.6. Rotation Vector Representation | 93 |
| &emsp;9.7. Euler Angles | 94 |
| &emsp;9.8. Additive EKF (AEKF) | 95 |
| &emsp;9.9. Multiplicative EKF (MEKF) | 96 |
| **Chapter 10. Usability Considerations** | 101 |
| &emsp;10.1. Editing | 101 |
| &emsp;10.2. Reinitialization and Restarts | 106 |
| &emsp;10.3. Backup Ephemeris | 106 |
| &emsp;10.4. Ground System Considerations | 110 |
| **Chapter 11. Smoothing** | 113 |
| **Chapter 12. Advanced Estimation Algorithms** | 117 |
| &emsp;The Sigma-Point Estimator | 117 |
| **Appendix A. Models and Realizations of Random Variables** | 123 |
| **Appendix B. The Mathematics Behind the UDU Factorization** | 125 |
| &emsp;B.1. The Partitioning into Two Subproblems | 125 |
| &emsp;B.2. The Mathematics Behind the Second Subproblem | 125 |
| &emsp;B.3. The Agee-Turner Rank-One Update | 127 |
| &emsp;B.4. Decorrelating Measurements | 130 |
| &emsp;B.5. The Carlson Rank-One Update | 130 |
| **Appendix C. An Analysis of Dual Inertial-Absolute and Inertial-Relative Navigation Filters** | 137 |
| &emsp;C.1. Introduction | 137 |
| &emsp;C.2. The Filter Dynamics | 137 |
| &emsp;C.3. Incorporation of Measurements | 140 |
| &emsp;C.4. Analysis of the Merits of the Inertial-Absolute and Inertial-Relative Filters | 143 |
| &emsp;C.5. Conclusions | 144 |
| **Bibliography** | 147 |
| **Index of Best Practices** | 151 |

# Foreword to the Second Edition

<span id="page-12-0"></span>Many engineers have heard of Kalman filtering and many use Kalman filters in their state estimation work, especially those of us involved in navigation. The Kalman filter is a powerful tool in spacecraft navigation. Yet my experience is that many (if not most) of these same engineers do not fully understand the underlying mathematics, the basic assumptions, nor how to expertly analyze the estimation accuracies produced by the Kalman filter algorithms. This is especially true when the Kalman filter (which is based on linear system theory) is utilized in the more realistic stochastic non-linear setting. Its full potential and limitations are not always well understood especially when transitioning from its traditional linear formulation to non-linear systems, which is where the extended Kalman filter (EKF) comes into play. The extended Kalman filter is known to be an *ad hoc* algorithm and requires skill to properly tune to obtain realistic state estimation accuracies.

In practical scenarios, most systems are nonlinear, and we often linearize the system around the current state estimate using Jacobian matrices, but this linearization can introduce inaccuracies, especially when the underlying system is highly nonlinear. Because of this, the nonlinear filters can be unstable or inaccurate if the assumptions of small nonlinearities or well-behaved systems are violated. Tuning the filter becomes more complex, requiring an understanding of both the system dynamics and the noise characteristics. This is largely an art form.

What is critically important in applications utilizing EKFs and various variants of the Kalman filter based on linearization assumptions (such as Taylor series approximations) is that the state estimation error covariance matrix (which is an approximation due to the linearizations inherent in the algorithm) reflect reality as closely as possible. For example, during a spacecraft rendezvous where the state estimation accuracy is a key to the mission success, the state estimation error covariance provides insight into how the filter is performing. Sometimes engineers apply the filter without thoroughly analyzing the state estimation error covariances beforehand (typically employing high-fidelity computer simulations) potentially leading to overconfidence in the estimated states during actual operations.

Many of the tools the Apollo and Shuttle era navigators employed to analyze and tune the EKF have seemingly been lost in time. These include Monte Carlo analysis, error budgets, and sensitivity analysis and the development of suboptimal filters utilizing these tools. Additionally, questions around measurement underweighting and measurement editing and the role of measurement residuals in keeping the EKF stable are often overlooked.

Dr. Carpenter and Dr. D'Souza have assembled a text exploiting the wisdom of many experts in the field. Indeed, this book will guide you through a more clearly developed understanding of Kalman filters in practical applications. The material is presented from an engineering perspective – it is not a mathematics treatise. In that sense, it is a treasure for practitioners and will remain a key resource for engineers to truly understand how to create and tune nonlinear filters in state estimation applications. Also the authors present outstanding material for highly nonlinear systems employing other approaches like Unscented Kalman Filters (UKF) and Particle Filters (PF), which might provide more robust solutions.

In essence, while the Kalman filter and its variants are widely used, their correct application, particularly in nonlinear settings requires deep expertise and curiosity when the estimation errors don't meet expectations.

Robert H. Bishop, PhD, PE  
Vice Chancellor for Engineering, The Texas A&M University System  
Dean of Engineering, Texas A&M University  
Director, Texas A&M Engineering Experiment Station  
Harold J. Haynes Dean's Chair in Engineering  
October 2024

# Foreword to the First Edition

<span id="page-14-0"></span>It certainly should not come as a surprise to the reader that navigation systems are at the heart of almost all of NASA's missions, either on our launch vehicles, on robotic science spacecraft, or on our crewed human exploration vehicles. Clearly navigation is absolutely fundamental to operating our space systems across the wide spectrum of mission regimes. Safe and reliably performing navigation systems are essential elements needed for routine low Earth orbiting science missions, for rendezvous and proximity operation missions or precision formation flying missions (where relative navigation is a necessity), for navigation through the outer planets of the solar system, and for accomplishing pinpoint landing on planets/small bodies, and many more mission types.

I believe the reader will find that the navigation filter best practices the team has collected, documented, and shared in this first edition book will be of practical value in your work designing, developing, and operating modern navigation systems for NASA's challenging future missions. I want to thank the entire team that has diligently worked to create this NASA Engineering and Safety Center (NESC) GN&C knowledge capture report. I especially want to acknowledge the dedication, care, and attention to detail as well as the energy that both Russell Carpenter and Chris D'Souza, the report editors, have invested in producing this significant product for the GN&C community of practice. It was Russell and Chris who had the inspiration to create this report and they have done a masterful job in not only directly technically contributing to the report but also coordinating its overall development. It should be mentioned that some high-level limited work was previously performed under NESC sponsorship to capture the lessons learned over the course of the several decades NASA has been navigating space vehicles. This report however fills a unique gap by providing extensive technical details and, perhaps more importantly, providing the underlying rationale for each of the navigation filter best practices presented here. Capturing these rationales has proven to be a greatly needed but very challenging task. I congratulate the team for taking this challenge on.

The creation, and the wide dissemination of this report, is absolutely consistent with the NESC's commitment to engineering excellence by capturing and passing along, to NASA's next generation of engineers, the lessons learned emerging from the collective professional experiences of NASA's navigation system subject matter experts. I believe this book will not only provide relevant tutorial-type guidance for early career GN&C engineers that have limited real-world on the job experience but it should also serve as a very useful memory aid for more experienced GN&C engineers, especially as a handy reference to employ for technical peer reviews of navigation systems under development.

As the NASA Technical Fellow for GN&C I urge the reader (especially the "navigators" among you obviously) to invest the time to digest and consider how the best practices provided in this report should influence your own work developing navigation systems for the Agency's future missions. The editors and I recognize this will be a living document and we sincerely welcome your feedback on this first edition of the report, especially your constructive recommendations on ways to improve and/or augment this set of best practices.

Cornelius J. Dennehy  
NASA Technical Fellow for GN&C  
January 2018

# Editors' Preface to the Second Edition

<span id="page-16-0"></span>This second edition welcomes several new contributors, and features a new chapter on batch filtering for onboard applications, major augmentations to the chapters on factorization and usability, and numerous minor corrections. An index of best practices has also been added.

The Editors wish to thank the many readers whose feedback has resulted in the improvements to the present edition; in particular: Nathan Stacey, John Christian, Terry Sabaka, and Francesco Capolupo.

Among the main topics of feedback we received for the first edition concerned our failure to explicitly mention that the primary target application for these best practices is onboard, rather than ground-based navigation, although many of the best practices described here have mutual applicability to both domains. It is not our purpose here to recapitulate the pros and cons of onboard vs. ground-based navigation, or to discuss when one or the other approach is either necessary and/or desirable. For those interested in such topics, a number of standard texts [[5](16-bibliography.md#page-170-1), [62](16-bibliography.md#page-172-0)] discuss this trade space. Rather, herein we proceed from the notion that for a given application, the trade has resulted in a decision to implement onboard navigation. Thus, the best practices offered here pertain primarily to this context.

# Editors' Preface to the First Edition

<span id="page-18-0"></span>As the era of commercial spaceflight begins, NASA must ensure that lessons the US has learned over the first 50 years of the Space Age will continue to positively influence the continuing exploration and development of space. Of the many successful strands of this legacy, onboard navigation stands out as an early triumph of technology whose continuous development and improvement remains as important to future exploration and commercial development as it was in the era of *Gemini* and *Apollo*. The key that opened the door to practical and reliable onboard navigation was the discovery and development of the extended Kalman filter (EKF) in the 1960s, a story that has been well-chronicled by Stanley Schmidt [[76](16-bibliography.md#page-173-0)], and Kalman filtering has far outgrown NASA's applications over the intervening decades. What are less well-documented are the accumulated art and lore, tips and tricks, and other institutional knowledge that NASA navigators have employed to design and operate EKFs in support of dozens of missions in the *Gemini/Apollo* era, well over one hundred Space Shuttle missions, and numerous robotic missions, without a failure ever attributed to an EKF. To document the best of these practices is the purpose that motivates the contributors of the present document.

Kernels of such best practices have appeared, scattered throughout the open technical literature, but such contributions are limited by organizational publication policies, and in some cases by technology export considerations. Even within NASA, there has heretofore not been any attempt to codify this knowledge into a readily available design handbook that could continue to evolve along with the navigation community of practice. As a result, even within the Agency, it is possible for isolated practitioners "not to know any better:" to fail to appreciate the subtleties of successful and robust navigation filter design, and to lack an understanding of the motivations for, and the implied cost/benefit trades, of many of the tried and true approaches to filter design.

Some limited progress toward filling this void has been made at a summary level in reports and briefings prepared for the NASA Engineering and Safety Center (NESC) [[20](16-bibliography.md#page-170-2)]. In particular, one of a series of recommendations in Reference [20](16-bibliography.md#page-170-2) "…directed towards the development of future non-human rated [rendezvous] missions…" included as its fourteenth recommendation the admonishment to "[u]tilize best practices for rendezvous navigation filter design." This recommendation listed eight such practices, as follows:

- a. **Maintain an accurate representation of the target-chaser relative state estimation errors, including an accurate variance-covariance matrix.** This allows the filter to compute an appropriate gain matrix. It also aids the filter in appropriately editing unsuitable measurements.
- b. **Provide a capability for measurement underweighting that adapts to the current uncertainty in the filter's state estimation error, as required to be consistent with the suboptimality of the navigation filter's measurement update.** Effective means for accomplishing this have been found to include:
  - i. Modified second-order Gaussian state update method [[38](16-bibliography.md#page-171-0)];
  - ii. Multiplicative adjustment of the mapping of the state error covariance matrix into the measurement subspace, which occurs within the computation of the residual covariance [[91](16-bibliography.md#page-173-1)]; and
  - iii. Schmidt-Kalman state update [[7](16-bibliography.md#page-170-3)] that utilizes the covariance matrix of "consider" parameters (i.e., states that the filter does not update, but for which it maintains a covariance).

  Multiplicative adjustment of the measurement noise covariance matrix within the computation of the residual covariance (the "bump up R" method [[7](16-bibliography.md#page-170-3)]) has been found to be less effective, and is not recommended unless other methods are not feasible.
- c. **Estimate states that model biases in sensor measurements and account for unmodeled accelerations.** Gauss-Markov models for these biases have been found to be more effective than random constant or random walk models. Random constant models can become stale, and random walk models can overflow during long periods without measurement updates.
- d. **Provide commands that allow for selective processing of individual measurement types.** If the filter utilizes an automated residual edit process, then the recommended command capability should be able to override the residual edit test.
- e. **Maintain a backup ephemeris, unaltered by measurement updates since initialization, which can be used to restart the filter without uplink of a new state vector.**
- f. **Provide a capability for reinitializing the covariance matrix without altering the current state estimate.**
- g. **Ensure tuning parameters are uplinkable to the spacecraft, and capable of being introduced to the filter without loss of onboard navigation data.**
- h. **Provide flexibility to take advantage of sensors' and sensor suites' full capability over all operating ranges.**

A subsequent briefing given for an NESC webinar listed these as well as the following "additional considerations:"

- State Representation
  - Translational states
    - Dual inertial
    - Inertial/relative
    - Relative-only
  - Attitude states, as required
    - 3-parameter vs. 4-parameter
    - Multiplicative vs. additive update
- Covariance Factorization (or not)
  - U-D
  - "Square Root" Methods
- Measurement Correlation
- Non-simultaneous Measurements
- Backward smoothing (for [Best Estimated Trajectories/Reconstructions])
- Error Budgets
- Sensitivity Analysis
- [Inertial Measurement Unit]/Accelerometer Processing
- Observability

While these summary-level lists give the community a place to start, they are lacking in some respects. They lack sufficient rationale that would motivate a designer to adopt them. Even if so motivated, a designer needs much more detailed information concerning how to implement the recommendations.

The present work is an attempt to address these shortcomings. Each contributor has selected one aspect of navigation filter design, or several closely related ones, as the basis of a chapter. Each chapter clearly identifies best practices, where a consensus of the community of practice exists. While it is sometimes difficult to cast aside one's opinions and express such a consensus, each contributor has made a best effort in this regard. Where a diversity of opinion exists, the chapter will summarize the arguments for and against each approach. Also, if promising new developments are currently afoot, the chapter will assess their prospects.

While the contributors strive for consistency of convention and notation, each has his own preferences, and readers may need to accommodate subtle differences along these lines as they traverse the book. The first chapter, which summarizes the EKF, sets the stage, and should be briefly perused by even seasoned navigators in order to become familiar with the conventions adopted for this work. Subsequent chapters should stand on their own, and may be consulted in any order.

While this is a NASA document concerned with space navigation, it is likely that many of the principles would apply equally to the wider navigation community. That said, readers should keep in mind that hard-earned best practices of a particular discipline do not always carry over to others, even though they may be seemingly similar. To assume so is a classic example of the logical fallacy *argumentum ad verecundiam*, or the argument from [false] authority.

Finally, the contributors intend for this work to be a living document, which will continue to evolve with the state of the practice.

# Notational Conventions

<span id="page-22-0"></span>

| Symbol | Meaning |
|:---:|---|
| $\mathbb{A}$ | A set |
| $a, \alpha, A$ | Scalars |
| $\mathbf{q}, \mathbf{M}$ | An array of scalars, e.g. column, row, matrix |
| $\boldsymbol{x}$ | A point in an abstract vector space |
| $\vec{\boldsymbol{r}}$ | A physical vector, i.e. an arrow in 3-D space |
| $\mathcal{F}$ | A coordinate frame |
| $\mathbf{M}^{\mathsf{T}}$ | The transpose of the array $\mathbf{M}$ |
| $\lVert \boldsymbol{x} \rVert$ | The (2-)norm of the vector $\boldsymbol{x}$ |
| $\mathsf{y}$ | A random variable |
| $\boldsymbol{\mathsf{z}}$ | A random vector |
| $\mathrm{p}_{\mathsf{x}}(x)$ | The probability density function of the random variable $\mathsf{x}$ evaluated at the realization $x$ |
| $\Pr(\mathsf{y} < Y)$ | The probability that $\mathsf{y} < Y$ |
| $\mathrm{E}[\boldsymbol{\mathsf{z}}]$ | The expectation of the random vector $\boldsymbol{\mathsf{z}}$ |
| $\exp(t)$ | The exponential function of $t$ |
| $\mathrm{e}^{t}$ | $\exp(t)$ written as Euler's number raised to the $t$ power |
| $\mathrm{d}x$ | Leibniz' (total) differential of $x$ |
| $\dfrac{\mathrm{d}y}{\mathrm{d}x}$ | (First) (total) derivative of $y$ with respect to $x$ |
| $\dfrac{\mathrm{d}^{n}y}{\mathrm{d}x^{n}} = \dfrac{\mathrm{d}^{n}}{\mathrm{d}x^{n}}\,y$ | $n$th (total) derivative of $y$ with respect to $x$ |
| $\dfrac{{}^{\mathcal{F}}\mathrm{d}^{n}}{\mathrm{d}t^{n}}\,\vec{\boldsymbol{r}}$ | $n$th (total) derivative of $\vec{\boldsymbol{r}}$ with respect to $t$ in frame $\mathcal{F}$ |
| $\dfrac{\partial \mathbf{M}}{\partial \boldsymbol{x}}$ | (First) partial derivative of $\mathbf{M}$ with respect to $\boldsymbol{x}$ |
| $\left.\dfrac{\partial M}{\partial x}\right\rvert_{x_o}$ | (First) partial of $M$ with respect to $x$, evaluated at $x_o$ |
| $\dot{x}, \ddot{x}$, etc. | Overdots may be used as a shorthand for time derivatives |

---

[Contents](README.md) · [Chapter 1. The Extended Kalman Filter →](01-the-extended-kalman-filter.md)
