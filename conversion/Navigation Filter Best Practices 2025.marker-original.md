NASA/TP–2018–219822/Revision

![](_page_0_Picture_1.jpeg)

# Navigation Filter Best Practices

Edited By

J. Russell Carpenter Goddard Space Flight Center, Greenbelt, Maryland

Christopher N. D'Souza Johnson Space Center, Houston, Texas

## NASA STI Program Report Series

Since its founding, NASA has been dedicated to the advancement of aeronautics and space science. The NASA scientific and technical information (STI) program plays a key part in helping NASA maintain this important role.

The NASA STI Program operates under the auspices of the Agency Chief Information Officer. It collects, organizes, provides for archiving, and disseminates NASA's STI. The NASA STI Program provides access to the NTRS Registered and its public interface, the NASA Technical Report Server, thus providing one of the largest collections of aeronautical and space science STI in the world. Results are published in both non-NASA channels and by NASA in the NASA STI Report Series, which includes the following report types:

- TECHNICAL PUBLICATION. Reports of completed research or a major significant phase of research that present the results of NASA programs and include extensive data or theoretical analysis. Includes compilations of significant scientific and technical data and information deemed to be of continuing reference value. NASA counterpart of peer-reviewed formal professional papers, but having less stringent limitations on manuscript length and extent of graphic presentations.
- TECHNICAL MEMORANDUM. Scientific and technical findings that are preliminary or of specialized interest, e.g., quick release reports, working papers, and bibliographies that contain minimal annotation. Does not contain extensive analysis.
- CONTRACTOR REPORT. Scientific and technical findings by NASA-sponsored contractors and grantees.

- CONFERENCE PUBLICATION. Collected papers from scientific and technical conferences, symposia, seminars, or other meetings sponsored or co-sponsored by NASA.
- SPECIAL PUBLICATION. Scientific, technical, or historical information from NASA programs, projects, and missions, often concerned with subjects having substantial public interest.
- TECHNICAL TRANSLATION. Englishlanguage translations of foreign scientific and technical material pertinent to NASA's mission.

Specialized services also include organizing and publishing research results, distributing specialized research announcements and feeds, providing information desk and personal search support, and enabling data exchange services.

For more information about the NASA STI Program, see the following:

- Access the NASA STI program home page at http://www.sti.nasa.gov
- Help desk contact information: https://www.sti.nasa.gov/sti-contact-form/ and select the "General" help request type.

NASA/TP–2018–219822/Revision

![](_page_2_Picture_1.jpeg)

# Navigation Filter Best Practices

Edited By

J. Russell Carpenter Goddard Space Flight Center, Greenbelt, Maryland

Christopher N. D'Souza Johnson Space Center, Houston, Texas

National Aeronautics and Space Administration

NASA Engineering and Safety Center Hampton, Virginia 23681

The use of trademarks or names of manufacturers in this report is for accurate reporting and does not constitute an official endorsement, either expressed or implied, of such products or manufacturers by the National Aeronautics and Space Administration.

Available from:

NASA STI Program / Mail Stop 150 NASA Langley Research Center Hampton, VA 23681-2199

![](_page_4_Picture_0.jpeg)

## NASA Engineering and Safety Center

# Navigation Filter Best Practices

Second Edition

J. Russell Carpenter and Christopher N. D'Souza, Editors

with contributions from

Shyam Bhaskaran, J. Russell Carpenter, Christopher N. D'Souza, Cheryl J. Gramling, F. Landis Markley, James McCabe, Timothy McElrath, Lincoln Wood, Renato Zanetti

January 29, 2025

This material is declared a work of the US Government and is not subject to copyright protection in the United States, but may be subject to US Government copyright in other countries.

If there be two subsequent events, the probability of the second b/N and the probability of both together P/N, and it being first discovered that the second event has also happened, from hence I guess that the first event has also happened, the probability I am right is P/b.

Thomas Bayes, c. 1760

The explicit calculation of the optimal estimate as a function of the observed variables is, in general, impossible.

Rudolph Kalman, 1960.

The use of Kalman Filtering techniques in the on-board navigation systems for the Apollo Command Module and the Apollo Lunar Excursion Module was an important factor in the overwhelming success of the Lunar Landing Program.

Peter Kachmar, 2002.

Dedicated to the memory of Landis Markley, Gene Muller, Emil Schiesser, and Bill Lear.

## Contents

| Foreword Foreword Editors’ Editors’ Notational Chapter 1.1. 1.2. Chapter 2.1. 2.2. Chapter 3.1. 3.2. 3.3. 3.4. Chapter 4.1. 4.2. 4.3. 4.4. 4.5. Chapter | to the to the Preface Preface 1. The The 2. Batch Onboard 3. Metrics Covariance Covariance 4. Invariance Processing Filter Use of 5. | Second First to the to the Conventions The Extended Additive Multiplicative Batch-Sequential and The Covariance for Orbit Sigma-Point Processing Measurement to Vector Cascades Data from Measurement | Edition Edition Second First Extended Batch-Sequential Navigation Propagation Measurement Methods Latency the | Edition Edition Kalman Filter Kalman Filter Extended Kalman Filter Filters Filters Using Batch-Sequential Filters Matrix State Covariances Update Measurements Order of Measurement Processing Measurements Inertial Sensors Underweighting | v vii ix xi xv 1 1 6 9 9 10 15 15 21 31 33 35 35 36 37 38 38 41 |
|---------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------|
| 5.1.                                                                                                                                                    | Introduction                                                                                                                         |                                                                                                                                                                                                       |                                                                                                               |                                                                                                                                                                                                                                             | 41                                                              |
| 5.2.                                                                                                                                                    | Nonlinear                                                                                                                            | Effects                                                                                                                                                                                               | and                                                                                                           | the Need for Underweighting                                                                                                                                                                                                                 | 42                                                              |
| 5.3.                                                                                                                                                    | Underweighting                                                                                                                       |                                                                                                                                                                                                       | Measurements                                                                                                  |                                                                                                                                                                                                                                             | 46                                                              |
| 5.4.                                                                                                                                                    | Pre-Flight                                                                                                                           | Tuning                                                                                                                                                                                                | Aids                                                                                                          |                                                                                                                                                                                                                                             | 47                                                              |
| Chapter                                                                                                                                                 | 6. Bias                                                                                                                              | Modeling                                                                                                                                                                                              |                                                                                                               |                                                                                                                                                                                                                                             | 49                                                              |
| 6.1.                                                                                                                                                    | Zero-Input                                                                                                                           | Bias                                                                                                                                                                                                  | State                                                                                                         | Models                                                                                                                                                                                                                                      | 49                                                              |
| 6.2.                                                                                                                                                    | Single-Input                                                                                                                         | Bias                                                                                                                                                                                                  | State                                                                                                         | Models                                                                                                                                                                                                                                      | 51                                                              |
| 6.3.                                                                                                                                                    | Multi-Input                                                                                                                          | Bias                                                                                                                                                                                                  | State                                                                                                         | Models                                                                                                                                                                                                                                      | 56                                                              |

| Chapter 7.1. 7.2. 7.3. 7.4. 7.5. 7.6. Chapter 8.1. | 7. Selection Units Orbit Relative 8. Why | State of and Coordinate State Modeling Factorization Use the | Representations Solve-For State Variables for Estimation Precision and Time Systems Parameterizations Representations Inertial Components Methods UDU Factorization? | 61 61 61 61 62 62 66 71 71               |
|----------------------------------------------------|------------------------------------------|--------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------|
| 8.2.                                               |                                          | Preliminaries                                                |                                                                                                                                                                      | 72                                       |
| 8.3.                                               | The                                      | Time                                                         | Update of the Covariance                                                                                                                                             | 73                                       |
| 8.4.                                               | The                                      | Measurement                                                  | Update                                                                                                                                                               | 80                                       |
| 8.5.                                               |                                          | Conclusions                                                  |                                                                                                                                                                      | 84                                       |
| Chapter                                            | 9.                                       | Attitude                                                     | Estimation                                                                                                                                                           | 85                                       |
| 9.1.                                               | Attitude                                 | Matrix                                                       | Representation                                                                                                                                                       | 85                                       |
| 9.2.                                               | Euler                                    | Axis/Angle                                                   | Representation                                                                                                                                                       | 87                                       |
| 9.3.                                               |                                          | Quaternion                                                   | Representation                                                                                                                                                       | 88                                       |
| 9.4.                                               |                                          | Rodrigues                                                    | Parameter Representation                                                                                                                                             | 91                                       |
| 9.5.                                               | Modified                                 |                                                              | Rodrigues Parameters                                                                                                                                                 | 92                                       |
| 9.6.                                               | Rotation                                 | Vector                                                       | Representation                                                                                                                                                       | 93                                       |
| 9.7.                                               | Euler                                    | Angles                                                       |                                                                                                                                                                      | 94                                       |
| 9.8.                                               | Additive                                 | EKF                                                          | (AEKF)                                                                                                                                                               | 95                                       |
| 9.9.                                               |                                          | Multiplicative                                               | EKF (MEKF)                                                                                                                                                           | 96                                       |
| Chapter                                            | 10.                                      | Usability                                                    | Considerations                                                                                                                                                       | 101                                      |
| 10.1.                                              |                                          | Editing                                                      |                                                                                                                                                                      | 101                                      |
| 10.2.                                              |                                          | Reinitialization                                             | and Restarts                                                                                                                                                         | 106                                      |
| 10.3.                                              |                                          | Backup                                                       | Ephemeris                                                                                                                                                            | 106                                      |
| 10.4.                                              |                                          | Ground System                                                | Considerations                                                                                                                                                       | 110                                      |
| Chapter                                            | 11.                                      | Smoothing                                                    |                                                                                                                                                                      | 113                                      |
| Chapter                                            | 12.                                      | Advanced                                                     | Estimation Algorithms                                                                                                                                                | 117                                      |
| The                                                |                                          | Sigma-Point                                                  | Estimator                                                                                                                                                            | 117                                      |
| Appendix                                           | A.                                       | Models                                                       | and Realizations of Random Variables                                                                                                                                 | 123                                      |
| Appendix                                           | B.                                       | The                                                          | Mathematics Behind the UDU Factorization                                                                                                                             | 125                                      |
| B.1.                                               | The                                      | Partitioning                                                 | into Two Subproblems                                                                                                                                                 | 125                                      |
| B.2.                                               | The                                      | Mathematics                                                  | Behind the Second Subproblem                                                                                                                                         | 125                                      |
| B.3.                                               | The                                      | Agee-Turner                                                  | Rank-One Update                                                                                                                                                      | 127                                      |
| B.4.                                               |                                          | Decorrelating                                                | Measurements                                                                                                                                                         | 130                                      |
| B.5.                                               | The                                      | Carlson                                                      | Rank-One Update                                                                                                                                                      | 130                                      |
| Appendix                                           | C.                                       | An                                                           | Analysis of Dual Inertial-Absolute and                                                                                                                               | Inertial-Relative Navigation Filters 137 |
| C.1.                                               |                                          | Introduction                                                 |                                                                                                                                                                      | 137                                      |
| C.2.                                               | The                                      | Filter                                                       | Dynamics                                                                                                                                                             | 137                                      |
| C.3.                                               |                                          | Incorporation                                                | of Measurements                                                                                                                                                      | 140                                      |

| C.4. Analysis of the Merits of the Inertial-Absolute and Inertial-Relative Filters | 143 |
|------------------------------------------------------------------------------------|-----|
| C.5. Conclusions                                                                   | 144 |
| Bibliography                                                                       | 147 |
| Index of Best Practices                                                            | 151 |

![](_page_11_Picture_1.jpeg)

## Foreword to the Second Edition

<span id="page-12-0"></span>Many engineers have heard of Kalman filtering and many use Kalman filters in their state estimation work, especially those of us involved in navigation. The Kalman filter is a powerful tool in spacecraft navigation. Yet my experience is that many (if not most) of these same engineers do not fully understand the underlying mathematics, the basic assumptions, nor how to expertly analyze the estimation accuracies produced by the Kalman filter algorithms. This is especially true when the Kalman filter (which is based on linear system theory) is utilized in the more realistic stochastic non-linear setting. Its full potential and limitations are not always well understood especially when transitioning from its traditional linear formulation to non-linear systems, which is where the extended Kalman filter (EKF) comes into play. The extended Kalman filter is known to be an ad hoc algorithm and requires skill to properly tune to obtain realistic state estimation accuracies.

In practical scenarios, most systems are nonlinear, and we often linearize the system around the current state estimate using Jacobian matrices, but this linearization can introduce inaccuracies, especially when the underlying system is highly nonlinear. Because of this, the nonlinear filters can be unstable or inaccurate if the assumptions of small nonlinearities or well-behaved systems are violated. Tuning the filter becomes more complex, requiring an understanding of both the system dynamics and the noise characteristics. This is largely an art form.

What is critically important in applications utilizing EKFs and various variants of the Kalman filter based on linearization assumptions (such as Taylor series approximations) is that the state estimation error covariance matrix (which is an approximation due to the linearizations inherent in the algorithm) reflect reality as closely as possible. For example, during a spacecraft rendezvous where the state estimation accuracy is a key to the mission success, the state estimation error covariance provides insight into how the filter is performing. Sometimes engineers apply the filter without thoroughly analyzing the state estimation error covariances beforehand (typically employing high-fidelity computer simulations) potentially leading to overconfidence in the estimated states during actual operations.

Many of the tools the Apollo and Shuttle era navigators employed to analyze and tune the EKF have seemingly been lost in time. These include Monte Carlo analysis, error budgets, and sensitivity analysis and the development of suboptimal filters utilizing these tools. Additionally, questions around measurement underweighting and measurement editing and the role of measurement residuals in keeping the EKF stable are often overlooked.

Dr. Carpenter and Dr. D'Souza have assembled a text exploiting the wisdom of many experts in the field. Indeed, this book will guide you through a more clearly developed understanding of Kalman filters in practical applications. The material is presented from an engineering perspective – it is not a mathematics treatise. In that sense, it is a treasure for practitioners and will remain a key resource for engineers to truly understand how to create and tune nonlinear filters in state estimation applications. Also the authors present outstanding material for highly nonlinear systems employing other approaches like Unscented Kalman Filters (UKF) and Particle Filters (PF), which might provide more robust solutions.

In essence, while the Kalman filter and its variants are widely used, their correct application, particularly in nonlinear settings requires deep expertise and curiosity when the estimation errors don't meet expectations.

Robert H. Bishop, PhD, PE Vice Chancellor for Engineering, The Texas A&M University System Dean of Engineering, Texas A&M University Director, Texas A&M Engineering Experiment Station Harold J. Haynes Dean's Chair in Engineering October 2024

## Foreword to the First Edition

<span id="page-14-0"></span>It certainly should not come as a surprise to the reader that navigation systems are at the heart of almost all of NASA's missions, either on our launch vehicles, on robotic science spacecraft, or on our crewed human exploration vehicles. Clearly navigation is absolutely fundamental to operating our space systems across the wide spectrum of mission regimes. Safe and reliably performing navigation systems are essential elements needed for routine low Earth orbiting science missions, for rendezvous and proximity operation missions or precision formation flying missions (where relative navigation is a necessity), for navigation through the outer planets of the solar system, and for accomplishing pinpoint landing on planets/small bodies, and many more mission types.

I believe the reader will find that the navigation filter best practices the team has collected, documented, and shared in this first edition book will be of practical value in your work designing, developing, and operating modern navigation systems for NASA's challenging future missions. I want to thank the entire team that has diligently worked to create this NASA Engineering and Safety Center (NESC) GN&C knowledge capture report. I especially want to acknowledge the dedication, care, and attention to detail as well as the energy that both Russell Carpenter and Chris D'Souza, the report editors, have invested in producing this significant product for the GN&C community of practice. It was Russell and Chris who had the inspiration to create this report and they have done a masterful job in not only directly technically contributing to the report but also coordinating its overall development. It should be mentioned that some high-level limited work was previously performed under NESC sponsorship to capture the lessons learned over the course of the several decades NASA has been navigating space vehicles. This report however fills a unique gap by providing extensive technical details and, perhaps more importantly, providing the underlying rationale for each of the navigation filter best practices presented here. Capturing these rationales has proven to be a greatly needed but very challenging task. I congratulate the team for taking this challenge on.

The creation, and the wide dissemination of this report, is absolutely consistent with the NESC's commitment to engineering excellence by capturing and passing along, to NASA's next generation of engineers, the lessons learned emerging from the collective professional experiences of NASA's navigation system subject matter experts. I believe this book will not only provide relevant tutorial-type guidance for early career GN&C engineers that have limited real-world on the job experience but it should also serve as a very useful memory aid for more experienced GN&C engineers, especially as a handy reference to employ for technical peer reviews of navigation systems under development.

As the NASA Technical Fellow for GN&C I urge the reader (especially the "navigators" among you obviously) to invest the time to digest and consider how the best practices provided in this report should influence your own work developing navigation systems for the Agency's future missions. The editors and I recognize this will be a living document and we sincerely welcome your feedback on this first edition of the report, especially your constructive recommendations on ways to improve and/or augment this set of best practices.

Cornelius J. Dennehy NASA Technical Fellow for GN&C January 2018

## Editors' Preface to the Second Edition

<span id="page-16-0"></span>This second edition welcomes several new contributors, and features a new chapter on batch filtering for onboard applications, major augmentations to the chapters on factorization and usability, and numerous minor corrections. An index of best practices has also been added.

The Editors wish to thank the many readers whose feedback has resulted in the improvements to the present edition; in particular: Nathan Stacey, John Christian, Terry Sabaka, and Francesco Capolupo.

Among the main topics of feedback we received for the first edition concerned our failure to explicitly mention that the primary target application for these best practices is onboard, rather than ground-based navigation, although many of the best practices described here have mutual applicability to both domains. It is not our purpose here to recapitulate the pros and cons of onboard vs. ground-based navigation, or to discuss when one or the other approach is either necessary and/or desirable. For those interested in such topics, a number of standard texts [[5](#page-170-1), [62](#page-172-0)] discuss this trade space. Rather, herein we proceed from the notion that for a given application, the trade has resulted in a decision to implement onboard navigation. Thus, the best practices offered here pertain primarily to this context.

![](_page_17_Picture_1.jpeg)

## Editors' Preface to the First Edition

<span id="page-18-0"></span>As the era of commercial spaceflight begins, NASA must ensure that lessons the US has learned over the first 50 years of the Space Age will continue to positively influence the continuing exploration and development of space. Of the many successful strands of this legacy, onboard navigation stands out as an early triumph of technology whose continuous development and improvement remains as important to future exploration and commercial development as it was in the era of Gemini and Apollo. The key that opened the door to practical and reliable onboard navigation was the discovery and development of the extended Kalman filter (EKF) in the 1960s, a story that has been well-chronicled by Stanley Schmidt [[76](#page-173-0)], and Kalman filtering has far outgrown NASA's applications over the intervening decades. What are less well-documented are the accumulated art and lore, tips and tricks, and other institutional knowledge that NASA navigators have employed to design and operate EKFs in support of dozens of missions in the Gemini/Apollo era, well over one hundred Space Shuttle missions, and numerous robotic missions, without a failure ever attributed to an EKF. To document the best of these practices is the purpose that motivates the contributors of the present document.

Kernels of such best practices have appeared, scattered throughout the open technical literature, but such contributions are limited by organizational publication policies, and in some cases by technology export considerations. Even within NASA, there has heretofore not been any attempt to codify this knowledge into a readily available design handbook that could continue to evolve along with the navigation community of practice. As a result, even within the Agency, it is possible for isolated practitioners "not to know any better:" to fail to appreciate the subtleties of successful and robust navigation filter design, and to lack an understanding of the motivations for, and the implied cost/benefit trades, of many of the tried and true approaches to filter design.

Some limited progress toward filling this void has been made at a summary level in reports and briefings prepared for the NASA Engineering and Safety Center (NESC) [[20](#page-170-2)]. In particular, one of a series of recommendations in Reference [20](#page-170-2) "…directed towards the development of future non-human rated [rendezvous] missions…" included as its fourteenth recommendation the admonishment to "[u]tilize best practices for rendezvous navigation filter design." This recommendation listed eight such practices, as follows:

- a. Maintain an accurate representation of the target-chaser relative state estimation errors, including an accurate variance-covariance matrix. This allows the filter to compute an appropriate gain matrix. It also aids the filter in appropriately editing unsuitable measurements.
- b. Provide a capability for measurement underweighting that adapts to the current uncertainty in the filter's state estimation error, as required to be consistent with the suboptimality of the navigation filter's measurement update. Effective means for accomplishing this have been found to include:
  - i. Modified second-order Gaussian state update method [[38](#page-171-0)];

- ii. Multiplicative adjustment of the mapping of the state error covariance matrix into the measurement subspace, which occurs within the computation of the residual covariance [[91](#page-173-1)]; and
- iii. Schmidt-Kalman state update [[7](#page-170-3)] that utilizes the covariance matrix of "consider" parameters (i.e., states that the filter does not update, but for which it maintains a covariance).

Multiplicative adjustment of the measurement noise covariance matrix within the computation of the residual covariance (the "bump up R" method [[7](#page-170-3)]) has been found to be less effective, and is not recommended unless other methods are not feasible.

- c. Estimate states that model biases in sensor measurements and account for unmodeled accelerations. Gauss-Markov models for these biases have been found to be more effective than random constant or random walk models. Random constant models can become stale, and random walk models can overflow during long periods without measurement updates.
- d. Provide commands that allow for selective processing of individual measurement types. If the filter utilizes an automated residual edit process, then the recommended command capability should be able to override the residual edit test.
- e. Maintain a backup ephemeris, unaltered by measurement updates since initialization, which can be used to restart the filter without uplink of a new state vector.
- f. Provide a capability for reinitializing the covariance matrix without altering the current state estimate.
- g. Ensure tuning parameters are uplinkable to the spacecraft, and capable of being introduced to the filter without loss of onboard navigation data.
- h. Provide flexibility to take advantage of sensors' and sensor suites' full capability over all operating ranges.

A subsequent briefing given for an NESC webinar listed these as well as the following "additional considerations:"

- State Representation
  - Translational states ∗ Dual inertial ∗ Inertial/relative ∗ Relative-only
  - Attitude states, as required ∗ 3-parameter vs. 4-parameter ∗ Multiplicative vs. additive update
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

While this is a NASA document concerned with space navigation, it is likely that many of the principles would apply equally to the wider navigation community. That said, readers should keep in mind that hard-earned best practices of a particular discipline do not always carry over to others, even though they may be seemingly similar. To assume so is a classic example of the logical fallacy argumentum ad verecundiam, or the argument from [false] authority.

Finally, the contributors intend for this work to be a living document, which will continue to evolve with the state of the practice.

![](_page_21_Picture_1.jpeg)

## Notational Conventions

- <span id="page-22-0"></span>A A set a, α, A Scalars q,M An array of scalars, e.g. column, row, matrix x A point in an abstract vector space $\vec{r}$ A physical vector, i.e. an arrow in 3-D space F A coordinate frame M<sup>T</sup> The transpose of the array M ∥x∥ The (2-)norm of the vector x y A random variable z A random vector px
- (x) The probability density function of the random variable x evaluated at the realization x Pr(y < Y ) The probability that y < Y E[z] The expectation of the random vector z exp(t) The exponential function of t e t exp(t) written as Euler's number raised to the t power dx Leibniz' (total) differential of x dy dx (First) (total) derivative of y with respect to x d <sup>n</sup>y <sup>d</sup>x<sup>n</sup> = d n <sup>d</sup>x<sup>n</sup> y nth (total) derivative of y with respect to x <sup>F</sup>d n <sup>d</sup>t<sup>n</sup> $\vec{r}$ nth (total) derivative of $\vec{r}$ with respect to t in frame F ∂M ∂x (First) partial derivative of M with respect to x ∂M ∂x x<sup>o</sup> (First) partial of M with respect to x, evaluated at x<sup>o</sup> x,˙ x, ¨ etc. Overdots may be used as a shorthand for time derivatives

![](_page_23_Picture_1.jpeg)

#### CHAPTER 1

## <span id="page-24-0"></span>The Extended Kalman Filter

Contributed by J. Russell Carpenter

As described in the preface, use of the Extended Kalman Filter (EKF) for navigation has a long history of flight-proven success. The EKF thus forms the foundational best practice advocated by this work, and it forms the basis for many of the best practices later chapters describe. The purpose of the present chapter is not to derive the EKF and its relations, but rather to present them in a basic form, as a jumping off point for the rest of the material we shall present. As we shall show, while the EKF is a powerful and robust algorithm, it is based on a few ad hoc assumptions, which can lead to misuses and misunderstandings. Many of the best practices we shall describe are tricks of the trade that address such issues.

#### 1.1. The Additive Extended Kalman Filter

<span id="page-24-1"></span>The additive EKF is distinguished from the multiplicative EKF (MEKF) by the form of its measurement update. The additive EKF is the usual and original form of the EKF, and when we refer to the EKF without a modifier, one may assume we mean the additive form.

1.1.1. The Dynamics Model Suppose we have a list of n real quantities that we need to know in order to perform navigation, and we have a differential equation that tells us how these quantities evolve through time, such as

<span id="page-24-2"></span>
$$\dot{\mathbf{X}}(t) = \mathbf{f}(\mathbf{X}(t), t) \quad (1.1)$$

where X ∈ <sup>R</sup> n , which we call the state vector, contains the quantities of interest; we shall call f(X, t) the dynamics function. If we knew these quantities perfectly at any time, [\(1.1\)](#page-24-2) would allow us to know them at any other time. For a variety of reasons, this is not the case however; both the initial conditions and the dynamics function are corrupted by uncertainty.

Suppose instead that the quantities of interest are realizations of a random process, X(t), whose distribution at some initial time t<sup>o</sup> is known to us, and whose evolution (forward) in time follows the stochastic differential equation given by

<span id="page-24-3"></span>

| $d\mathbf{X}(t) = \mathbf{f}(\mathbf{X}(t), t) dt + \mathbf{B}(t) d\mathbf{w}(t)$ | (1.2) |
|-----------------------------------------------------------------------------------|-------|
|-----------------------------------------------------------------------------------|-------|

where the presence of the process noise dw(t) reflects uncertainty in the dynamics. To interpret [\(1.2\)](#page-24-3), imagine dw(t) as the limit of a discrete sequence of random increments, as the time between increments goes to zero. The result will be a continuous but non-differentiable process; hence the notation X˙ (t) has ambiguous meaning. Henceforth, we shall define our notation such that when we write

<span id="page-24-4"></span>
$$\dot{\mathbf{X}}(t) = \mathbf{f}(\mathbf{X}(t), t) + \mathbf{B}(t)\mathbf{w}(t) \quad (1.3)$$

Finally, suppose that at some earliest time, to, the initial distribution of X(to) is Gaussian, with mean and covariance given by

| $\mathbf{E}[\mathbf{X}(t_0)] = \bar{\mathbf{X}}_o$ | and | $\mathbf{E}[(\mathbf{X}(t_0) - \bar{\mathbf{X}}_o)(\mathbf{X}(t_0) - \bar{\mathbf{X}}_o)^T] = \mathbf{P}_o$ | (1.4) |
|----------------------------------------------------|-----|-------------------------------------------------------------------------------------------------------------|-------|
|                                                    |     |                                                                                                             |       |

and suppose that infinitesimal increments of w(t) are Gaussian, with

<span id="page-25-4"></span>

| $E[\mathbf{w}(t)] = \mathbf{0}$ | and | $E[\mathbf{w}(t)\mathbf{w}^T(\tau)] = \mathbf{Q}(t)\delta(t - \tau)$ | (1.5) |
|---------------------------------|-----|----------------------------------------------------------------------|-------|
|---------------------------------|-----|----------------------------------------------------------------------|-------|

where Q(t) is the power spectral density function of w(t), and δ(t − τ ) is the Dirac delta, a generalized function. We shall also assume that

<span id="page-25-0"></span>
$$E\left[\mathbf{X}(t_0) - \bar{\mathbf{X}}_0\right] = \mathbf{0}, \forall t$$

We shall take [\(1.3\)](#page-24-4) – [\(1.6\)](#page-25-0) to define the dynamics model for the additive EKF. Note that even though we have assumed X(to) and w(t) are Gaussian, we cannot assume that X(t) remains Gaussian for t > to, because f may be a nonlinear function.

1.1.2. The Measurement Model In an ideal world, we might have devices for measuring all of the state vector components directly; then state determination would be simply a matter of collecting enough such observations to reduce the state uncertainty to sufficient levels. Unfortunately, this is almost never the case. Instead, like Socrates' prisoners, we can usually only perceive noisy projections of the state elements, at discrete times, t<sup>i</sup> , in the form of measurements:

<span id="page-25-1"></span>
$$\mathbf{Y}(t_i) = \mathbf{h}(\mathbf{X}(t_i), t_i) + \mathbf{v}(t_i) \quad (1.7)$$

where h is a surjection from R n to R <sup>m</sup>. We shall assume that v(ti), which we call the measurement noise, is a Gaussian sequence, with mean and covariance given by

<span id="page-25-6"></span>

| $\mathbf{E}[\mathbf{v}(t_i)] = \mathbf{0}$ | $a_i$ | $\mathbf{E}[\mathbf{v}(t_i)\mathbf{v}(t_j)^\top] = \mathbf{R}(t_i)\delta_{ij}$ | (1.8) |
|--------------------------------------------|-------|--------------------------------------------------------------------------------|-------|
|                                            |       |                                                                                |       |

where δij is the Kronecker delta function. We shall also assume that

<span id="page-25-2"></span>

| $\mathbf{E}[\mathbf{v}(t_i)(\mathbf{X}(t_0) - \bar{\mathbf{X}}_0)^\top] = \mathbf{0}$ | and | $\mathbf{E}[\mathbf{w}(t)\mathbf{v}(t_i)^\top] = \mathbf{0}, \forall i, t$ | (1.9) |
|---------------------------------------------------------------------------------------|-----|----------------------------------------------------------------------------|-------|
|                                                                                       |     |                                                                            |       |

We shall take [\(1.7\)](#page-25-1) – [\(1.9\)](#page-25-2) to define the measurement model for the additive EKF. Note that we cannot assume that Y(ti) is Gaussian, because h may be a nonlinear function. For compactness of notation, we shall often suppress the time argument and write [\(1.7\)](#page-25-1) as

<span id="page-25-5"></span>
$$\mathbf{Y}_i = \mathbf{h}_i(\mathbf{X}_i) + \mathbf{v}_i \quad (1.10)$$

Bayes' Law, the Markov Property, and Observability Bayes' Law tells us how to update the conditional probability density function (PDF) of X(ti), given a realization Y (ti) of the random process Y(ti):

<span id="page-25-3"></span>
$$\mathbf{p}_{\mathbf{x}_i|\mathbf{y}_i}(\mathbf{X}_i|\mathbf{Y}_i) = \mathbf{p}_{\mathbf{y}_i|\mathbf{x}_i}(\mathbf{Y}_i|\mathbf{X}_i) \frac{\mathbf{p}_{\mathbf{x}_i}(\mathbf{X}_i)}{\mathbf{p}_{\mathbf{y}_i}(\mathbf{Y}_i)} \quad (1.11)$$

If all the PDFs in [\(1.11\)](#page-25-3) were known, it would be relatively simple to use [\(1.11\)](#page-25-3) to estimate the state vector from a single measurement; our best estimate of the state would simply be the mean of pXi|Y<sup>i</sup> (X<sup>i</sup> |Yi). But to apply [\(1.11\)](#page-25-3) to the navigation problem, where we have a time sequence of measurements, <sup>Y</sup><sup>i</sup> = {Y<sup>i</sup> ,Yi−1, . . . , Y1}, we need to consider how the state dynamics evolve.

Unlike [\(1.1\)](#page-24-2), our dynamics model, given by [\(1.3\)](#page-24-4), only runs forward in time. Hence, the state at any future time depends only on its history. Also, because the non-homogeneous inputs to [\(1.3\)](#page-24-4) are uncorrelated by the Dirac delta in [\(1.5\)](#page-25-4), the value of the state at any particular time in the future depends only on its present value, and its accumulated diffusion due to the process noise over the interval between now and the future time of interest. Random processes such as this are said to possess the Markov Property. Using this property, we can write [\(1.11\)](#page-25-3) in terms of the measurement history as follows:

<span id="page-26-0"></span>

| $\mathbf{p}\mathbf{x}_i \mathbf{y}_i(\mathbf{X}_i \mathbf{y}_i) = \mathbf{p}\mathbf{y}_i \mathbf{x}_i(\mathbf{Y}_i \mathbf{X}_i)$ | $\frac{\mathbf{p}\mathbf{x}_i \mathbf{y}_{i-1}(\mathbf{X}_i \mathbf{y}_{i-1})}{\mathbf{p}\mathbf{y}_i \mathbf{y}_{i-1}(\mathbf{Y}_i \mathbf{y}_{i-1})}$ | (1.12) |
|-----------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|--------|
|-----------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|--------|

Even if we could compute all of the PDFs in [\(1.12\)](#page-26-0), we are not guaranteed that the sequence of measurements provide sufficient information to reduce the initial uncertainty of all the modes of [\(1.1\)](#page-24-2). If the system given by [\(1.1\)](#page-24-2) and [\(1.10\)](#page-25-5) is such that use of [\(1.12\)](#page-26-0) results in uncertainty in all the modes going asymptotically to zero in finite time, from any initial condition, then we say the system is globally asymptotically observable. If at least all of the unstable modes are observable, then we say the system is detectable. Unfortunately, for nonlinear systems, there is no known way to compute global observability. At best, under certain restrictions on [\(1.1\)](#page-24-2) and [\(1.10\)](#page-25-5), we can in principle establish local observability, in the neighborhood of a particular initial condition. However, this is a laborious calculation, often numerically unstable to evaluate. Also, note that observability is a property of the structure of [\(1.1\)](#page-24-2) and [\(1.10\)](#page-25-5), and hence is dependent on how one chooses to represent the navigation problem. Hence, a system that is observable with one representation may be unobservable with a different representation.

Kalman's original filter, which we now usually call the linear Kalman filter (LKF), is the result when the dynamics and measurement models are linear, Markov, Gaussian, and observable. An appreciation of the linear Kalman filter is essential to understanding the strengths and weaknesses of the EKF, although it is almost never the case that such assumptions are valid for real-world navigation problems.

1.1.3. The Linear Kalman Filter Suppose the dynamics and measurements are given by the following discrete-time linear models:

<span id="page-26-2"></span>
$$\mathbf{x}_i = \Phi_{i,i-1}\mathbf{x}_{i-1} + \Gamma_i \mathbf{u}_i \quad (1.13)$$

<span id="page-26-3"></span>

| $\mathbf{y}_i = \mathbf{H}_i \mathbf{x}_i + \mathbf{v}_i$ | (1.14) |
|-----------------------------------------------------------|--------|
|-----------------------------------------------------------|--------|

with

| $\mathbf{E}[\mathbf{x}] = \bar{\mathbf{x}}_o$ | $and$ | $\mathbf{E}[(\mathbf{x}_o - \bar{\mathbf{x}}_o)(\mathbf{x}_o - \bar{\mathbf{x}}_o)^T] = \mathbf{P}_o$ | (1.15) |
|-----------------------------------------------|-------|-------------------------------------------------------------------------------------------------------|--------|
|-----------------------------------------------|-------|-------------------------------------------------------------------------------------------------------|--------|

| $\mathbf{E}[\mathbf{u}] = \mathbf{0}$ | and | $\mathbf{E}[\mathbf{\Gamma}_{\mathbf{u}}\mathbf{u}^T\mathbf{\Gamma}_T] = \mathbf{S}_i\delta_{ij}$ | (1.16) |
|---------------------------------------|-----|---------------------------------------------------------------------------------------------------|--------|
|                                       |     |                                                                                                   |        |

and the moments of v<sup>i</sup> as given by [\(1.8\)](#page-25-6). This system will be globally observable if the observability Gramian is strictly positive definite,

<span id="page-26-1"></span>

| $\mathbf{W}_k = \sum_{i=1}^k \Phi_{i,1}^{\text{T}} \mathbf{H}_i^{\text{T}} \mathbf{H}_i \Phi_{i,1} > 0$ | (1.17) |
|---------------------------------------------------------------------------------------------------------|--------|
|---------------------------------------------------------------------------------------------------------|--------|

i.e. it has full rank.

With such assumptions, Kalman showed [[44](#page-171-1)] that Algorithm [1.1](#page-27-0) provides an optimal (both minimum variance and maximum liklihood) estimate of the moments of the PDFs appearing in [\(1.11\)](#page-25-3). Note that in Algorithm [1.1,](#page-27-0) the covariance recursion given by [\(1.19\)](#page-27-1) and [\(1.22\)](#page-27-2) does not depend on the measurement history, and hence one may compute the gain sequence, K<sup>i</sup> , off-line and store it as a time-indexed table or schedule, along with Φi,i−<sup>1</sup> and H<sup>i</sup> . Also note that because the system is globally observable, there is no chance that it will fail to converge from any initial condition, except perhaps due to build up of numerical truncation and/or roundoff error.

If we further suppose the dynamics and measurements are given by linear time-invariant (LTI) models,

| $\mathbf{x}_i = \mathbf{\Phi}\mathbf{x}_{i-1} + \mathbf{\Gamma}\mathbf{u}_i$ | (1.23) |
|------------------------------------------------------------------------------|--------|
|------------------------------------------------------------------------------|--------|

## <span id="page-27-0"></span>Algorithm 1.1 The Linear Kalman Filter

<span id="page-27-3"></span>
$$\hat{\mathbf{x}}_i = \mathbf{\Phi}_{i,i} \hat{\mathbf{x}}_{i-1}^+, \quad \hat{\mathbf{x}}_0^+ = \bar{\mathbf{x}}_o \quad (1.18)$$

<span id="page-27-1"></span>
$$\mathbf{P}_i^+ = \mathbf{\Phi}_{i,i-1} \mathbf{P}_{i-1}^+ \mathbf{\Phi}_{i,i-1}^+ + \mathbf{S}_i, \quad \mathbf{P}_0^+ = \mathbf{P}_0. \quad (1.19)$$

| $\mathbf{K}_i = \mathbf{P}_i \mathbf{H}_i^\top (\mathbf{H}_i \mathbf{P}_i^{-1} \mathbf{H}_i^\top + \mathbf{R}_i)^{-1}$ | (1.20) |
|------------------------------------------------------------------------------------------------------------------------|--------|
|------------------------------------------------------------------------------------------------------------------------|--------|

$$\mathbf{i}_i = \mathbf{F}_i + \mathbf{H}_i \mathbf{H}_i^T \left( \mathbf{H}_i \mathbf{H}_i^T \mathbf{H}_i \right) \mathbf{F}_i, \quad (1.20)$$

<span id="page-27-2"></span>
$$\mathbf{P}_i^- = \mathbf{P}_i^- - \mathbf{K}_i \mathbf{H}_i \mathbf{P}_i^- \quad (1.22)$$

| $\mathbf{y}_i = \mathbf{H}\mathbf{x}_i + \mathbf{v}_i$ | (1.24) |
|--------------------------------------------------------|--------|
|--------------------------------------------------------|--------|

then we may test its global observability using a somewhat simpler calculation than [\(1.17\)](#page-26-1), as follows:

$$\mathbf{W} = \begin{bmatrix} \mathbf{H} \\ \mathbf{H}\Phi \\ \mathbf{H}\Phi^2 \\ \vdots \\ \mathbf{H}\Phi^{n-1} \end{bmatrix} > 0 \quad (1.25)$$

If the system is detectable, then it turns out that the covariance recursion given by [\(1.19\)](#page-27-1) and [\(1.22\)](#page-27-2) reaches a steady-state, which we denote P∞. The corresponding gain is K<sup>∞</sup> = P∞H<sup>T</sup>R−<sup>1</sup> . There exist numerous software packages that will compute such quantities, e.g. the Matlab Control Systems Toolbox, which may unfortunately lead to their misuse in inappropriate contexts. Perhaps worse, experts from other domains, who are familiar with techniques such as pole placement for control of LTI systems, may recognize that the steady-state linear Kalman filter is "just a pole placement algorithm," and may infer that the EKF is not much more than a clever pole placement algorithm as well. As we shall show below, this is far from being the case; the EKF operates directly on the nonlinear system of interest, for which such LTI concepts have dubious applicability.

1.1.4. The Linearized Kalman Filter An immediately apparent generalization of the linear Kalman Filter is to use it to solve for small corrections to a nonlinearly propagated fixed reference trajectory. While such an approach may have certain applications over limited time horizons, and/or for ground-based applications where an operator can periodically intervene, experience with onboard navigation systems has shown that such corrections can fail to remain small enough to justify the required approximations.

1.1.5. The Extended Kalman Filter There are a number of ways to proceed from Algorithm [1.1](#page-27-0) to "derive" the EKF, but all contain a variety of ad hoc assumptions that are not guaranteed to hold in all circumstances. Most weaknesses and criticisms of the EKF arise from such assumptions. Rather than reproduce one or more of such derivations, we will simply point out that if one replaces [\(1.18\)](#page-27-3) with an integral of [\(1.1\)](#page-24-2) over the time between measurements, and computes the coefficient matrices appearing in [\(1.13\)](#page-26-2) and [\(1.14\)](#page-26-3) as Jacobians evaluated at the current solution of [\(1.1\)](#page-24-2), then the result is Algorithm [1.2,](#page-28-0) which bears more than a passing resemblance to the Kalman filter.

Several observations are in order regarding Algorithm [1.2.](#page-28-0)

## <span id="page-28-0"></span>Algorithm 1.2 A Naive Extension of the Kalman Filter

<span id="page-28-1"></span>
$$\hat{\mathbf{X}}_i^- = \hat{\mathbf{X}}_{i-1}^+ + \int_{t_{i-1}}^{t_i} \mathbf{f}(\mathbf{X}(\tau), \tau) \, d\tau, \quad \hat{\mathbf{X}}_0^+ = \bar{\mathbf{X}}_0 \quad (1.26)$$

$$\mathbf{A}(t) = \frac{\partial \mathbf{f}}{\partial \mathbf{X}} \Big|_{\dot{\mathbf{X}}(t)}, \quad \mathbf{H}_i = \frac{\partial \mathbf{h}_i}{\partial \mathbf{X}} \Big|_{\dot{\mathbf{X}}_i} \quad (1.27)$$

<span id="page-28-6"></span>
$$^{IA}(r)$$
       $^{IA}_i$       (1.28)

<span id="page-28-5"></span>
$$\Phi(t_i, \tau) \mathbf{B}(\tau) \mathbf{E}[\mathbf{w}(\tau) \mathbf{w}^T(\sigma)] \mathbf{B}^T(\sigma) \Phi^T(t_i, \sigma) d\tau d\sigma$$
 (1.29)

<span id="page-28-7"></span>
$$\mathbf{P}_i^- = \mathbf{\Phi}(t_i, t_{i-1}) \mathbf{P}_{i-1}^+ \mathbf{\Phi}^\top(t_i, t_{i-1}) + \mathbf{S}_i, \quad \mathbf{P}_0^+ = \mathbf{P}_0. \quad (1.30)$$

<span id="page-28-4"></span>

| $\mathbf{K}_i = \mathbf{P}_i \mathbf{H}_i^\top (\mathbf{H}_i \mathbf{P}_i^\top \mathbf{H}_i^\top + \mathbf{R}_i)^{-1}$ | (1.31) |
|------------------------------------------------------------------------------------------------------------------------|--------|
|------------------------------------------------------------------------------------------------------------------------|--------|

<span id="page-28-2"></span>
$$\hat{\mathbf{X}}_i^+ = \hat{\mathbf{X}}_i^- + \mathbf{K}_i \left( \mathbf{Y}_i - \mathbf{h}_i(\hat{\mathbf{X}}_i^-) \right) \quad (1.32)$$

<span id="page-28-3"></span>
$$\mathbf{P}_i^- = \mathbf{P}_i^- - \mathbf{K}_i \mathbf{H}_i \mathbf{P}_i^- \quad (1.33)$$

- One might infer from [\(1.26\)](#page-28-1) that Xˆ <sup>−</sup> <sup>i</sup> = E[X|<sup>Y</sup>i−1]. This would be a somewhat problematic inference however, since in general

$$\int_{t_{i-1}}^{t_i} \mathbf{f}(\mathbf{E}[\mathbf{X}(\tau)], \tau) \, \mathrm{d}\tau \neq \mathbf{E} \left[ \int_{t_{i-1}}^{t_i} \mathbf{f}(\mathbf{X}(\tau), \tau) \, \mathrm{d}\tau \right] \quad (1.34)$$

This implies that an initially Gaussian distribution for the state cannot in general remain Gaussian. At best, all we can hope is that Xˆ <sup>−</sup> <sup>i</sup> ≈ E[X|<sup>Y</sup>i−1].

- Let us define the estimation error as e(t) = X(t)−Xˆ (t). Then since Xˆ (t) ̸= E[X(t)|<sup>Y</sup>i−1],

$$\mathbf{P}(t) \neq \mathbf{E}[\mathbf{e}(t)\mathbf{e}^T(t)|\mathbb{Y}_{i-1}] \quad (1.35)$$

At best, all we can hope is that P(t) ≈ E[e(t)e T (t)|<sup>Y</sup>i−1].

- Let us define the innovation as r<sup>i</sup> = Y<sup>i</sup> − h(Xˆ <sup>−</sup> i ). Then since h(Xˆ <sup>−</sup> i ) ̸= E[Y],

| $\mathbf{H} \mathbf{P}_i^\top \mathbf{H}_i^\top + \mathbf{R}_i \neq \mathbf{E}[\mathbf{r}_i^\top]$ | (1.36) |
|----------------------------------------------------------------------------------------------------|--------|
|----------------------------------------------------------------------------------------------------|--------|

At best, all we can hope is that the above will hold approximately.

- Taken together, the approximations listed above imply that [\(1.32\)](#page-28-2) and [\(1.33\)](#page-28-3) can at best satisfy [\(1.12\)](#page-26-0) only approximately, not only because the mean and covariance are approximations, but also because the PDFs fail to remain Gaussian, and hence fail to be characterized completely by only their first two moments.
- Even if all of the above are reasonable approximations, there is a problem with [\(1.33\)](#page-28-3). The posterior covariance should be approximated by

$$\mathbf{P}_i^+ \approx \mathbf{E}[\mathbf{e}_i^+(\mathbf{e}_i^+)^\top | \mathbb{Y}_i] \quad (1.37)$$

Let us assume that

$$\mathbf{Y}_i - \mathbf{h}_i(\hat{\mathbf{X}}_i^{-}) \approx \mathbf{H}_i\mathbf{e}_i + \mathbf{v}_i \quad (1.38)$$

$$\mathbf{Y}_i - \mathbf{h}_i(\hat{\mathbf{X}}_i^-) \approx \mathbf{H}_i\mathbf{e}_i^- + \mathbf{v}_i \quad (1.38)$$

Then [\(1.32\)](#page-28-2) implies that

$$\mathbf{e}_i^+ = \mathbf{e}_i^- - \mathbf{K}_i \mathbf{H}_i \mathbf{e}_i^- - \mathbf{K}_i \mathbf{v}_i \quad (1.39)$$

$$\mathbf{e}_i^+ = \mathbf{e}_i^- - K_i \mathbf{H}_i \mathbf{e}_i^- - K_i \mathbf{v}_i \quad (1.39)$$

and by our prior assumption that E e − i v T i = 0,

$$\mathbf{P}_i^+ \approx \mathbf{E}[\mathbf{e}_i^+(\mathbf{e}_i^+)^\top | \mathbf{Y}_i] \quad (1.40)$$

| $= (\mathbf{I} - \mathbf{K}_i \mathbf{H}_i) \mathbf{P}_i^T (\mathbf{I} - \mathbf{K}_i \mathbf{H}_i)^T + \mathbf{K}_i \mathbf{R}_i \mathbf{K}_i^T$ | (1.41) |
|---------------------------------------------------------------------------------------------------------------------------------------------------|--------|
|---------------------------------------------------------------------------------------------------------------------------------------------------|--------|

Equation [\(1.41\)](#page-29-1) is Joseph's Formula, and it holds for any gain K<sup>i</sup> . Only for the optimal gain and true covariance does [\(1.41\)](#page-29-1) reduce to [\(1.33\)](#page-28-3). Since [\(1.31\)](#page-28-4) was computed with only an approximate covariance, and due to the various other approximations listed above as well, K<sup>i</sup> cannot be the optimal gain, so at best, [\(1.33\)](#page-28-3) will only hold approximately. At worst, such approximations may lead to P + i becoming non-positive definite, which is a significant issue. Because of its symmetric and additive form, [\(1.41\)](#page-29-1) is much less likely (but not impossible!) to produce a non-positive definite P + .

- <span id="page-29-1"></span>i
- By our assumption that E[w(t)w<sup>T</sup> (τ )] = Q(t)δ(t−τ ), one of the integrals in [\(1.29\)](#page-28-5) should be annihilated by the Dirac delta, resulting in

<span id="page-29-2"></span>
$$\mathbf{S}_i = \int_{t_{i-1}}^{t_i} \Phi(t_i, \tau) \mathbf{B}(\tau) \mathbf{Q}(\tau) \mathbf{B}^T(\tau) \Phi^T(t_i, \tau) d\tau \quad (1.42)$$

In any case, unlike for a discrete time dynamics model,

$$\begin{aligned} & E \left[ \int_{t_{i-1}}^{t_i} \int_{t_{i-1}}^{t_i} \Phi(t_i, \tau) \mathbf{B}(\tau) \mathbf{w}(\tau) \mathbf{w}^\top(\sigma) \mathbf{B}^\top(\sigma) \Phi^\top(t_i, \sigma) d\tau d\sigma \right] \\ & \neq E \left[ \int_{t_{i-1}}^{t_i} \Phi(t_i, \tau) \mathbf{B}(\tau) \mathbf{w}(\tau) d\tau \int_{t_{i-1}}^{t_i} \mathbf{w}^\top(\tau) \mathbf{B}^\top(\tau) \Phi^\top(t_i, \tau) d\tau \right] \quad (1.43) \end{aligned}$$

- In general, one would need to simultaneously integrate [\(1.26\)](#page-28-1) and [\(1.28\)](#page-28-6) due to their interdependence via the Jacobian A. If the time between measurements is small enough, then if one were to employ a suitable approximation for [\(1.28\)](#page-28-6), perhaps as simple as

$$\Phi(t_i, t_{i-1}) \approx \mathbf{I} + \mathbf{A}(t_i)(t_i - t_{i-1}) \quad (1.44)$$

then one may reasonably expect that a carefully chosen approximation would be no worse than the many other approximations inherent in the EKF. One may also consider the same or simpler approximations when considering approximations to [\(1.42\)](#page-29-2).

- Because there is no way to prove global observability for a nonlinear system, the EKF may fail to converge from some initial conditions, even if the system is locally observable in particular neighborhoods.

In light of the above observations, we conclude this section by presenting a slightly improved version of the EKF as Algorithm [1.3.](#page-30-0) In subsequent chapters, we shall describe additional improvements to the EKF.

#### 1.2. The Multiplicative Extended Kalman Filter

<span id="page-29-0"></span>An interesting variation on the EKF is possible in the context of estimating attitude parameters. An attitude correction may be viewed as a small-angle rotation from a frame associated with the previous estimate to a frame associated with a current estimate. In this context, one may use the previous attitude estimate as a linearization reference for a linearized Kalman Filter's Jacobian matrices, and estimate the small-angle correction as the filter state. After each state update, one performs a rectification of the attitude reference by applying the small-angle correction. Since for many attitude representations, a frame rotation is multiplicative operation, this procedure has become known as the multiplicative EKF. Chapter [9](#page-108-0) covers this subject.

## <span id="page-30-0"></span>Algorithm 1.3 A Slightly Improved Extension of the Kalman Filter

<span id="page-30-1"></span>
$$\hat{\mathbf{X}}_i^- = \hat{\mathbf{X}}_{i-1}^+ + \int_{t_{i-1}}^{t_i} \mathbf{f}(\mathbf{X}(\tau), \tau) \, d\tau, \quad \hat{\mathbf{X}}_0^+ = \bar{\mathbf{X}}_0 \quad (1.45)$$

$$\mathbf{A}(t) = \left. \frac{\partial \mathbf{f}}{\partial \mathbf{X}} \right|_{\dot{\mathbf{X}}(t)}, \quad \mathbf{H}_i = \left. \frac{\partial \mathbf{h}_i}{\partial \mathbf{X}} \right|_{\dot{\mathbf{X}}_i^-} \quad (1.46)$$

| $\Phi(t_i, t_{i-1}) = \text{a suitable approximation to (1.28)}$ | $x_i^*$ | $(1.47)$ |
|------------------------------------------------------------------|---------|----------|
|                                                                  |         |          |

| $\mathbf{S}_i = \text{a suitable approximation to (1.42)}$ | (1.48) |
|------------------------------------------------------------|--------|
|------------------------------------------------------------|--------|

<span id="page-30-2"></span>
$$\mathbf{P}_i = \mathbf{\Phi}(t_i, t_{i-1}) \mathbf{P}_{i-1}^+ \mathbf{\Phi}^\top(t_i, t_{i-1}) + \mathbf{S}_i, \quad \mathbf{P}_0^+ = \mathbf{P}_0 \quad (1.49)$$

$$\mathbf{K}_i = \mathbf{P}_i^\top \mathbf{H}_i^\top (\mathbf{H}_i \mathbf{P}_i^\top \mathbf{H}_i^\top + \mathbf{R}_i)^{-1} \quad (1.50)$$

$$\hat{\mathbf{X}}_i^+ = \hat{\mathbf{X}}_i^- + \mathbf{K}_i \left( \mathbf{Y}_i - \mathbf{h}_i(\hat{\mathbf{X}}_i^-) \right) \quad (1.5)$$

$$\mathbf{P}_i^* = (\mathbf{I} - \mathbf{K}_i\mathbf{H}_i)\mathbf{P}_i^* (\mathbf{I} - \mathbf{K}_i\mathbf{H}_i)^T + \mathbf{K}_i\mathbf{R}_i\mathbf{K}_i^T \quad (1.52)$$

![](_page_31_Picture_1.jpeg)

## Batch-Sequential Filters

<span id="page-32-2"></span><span id="page-32-0"></span>Contributed by Lincoln Wood, Shyam Bhaskaran, and Timothy McElrath

Most of this document discusses on-board navigation filter best practices in the context of continuously running filters, with measurements processed upon becoming available. In some space applications, however, it may be advantageous to accumulate a batch of measurements taken over a range of times, before processing the accumulated collection all at once. This may lead to improved computational efficiency if the time interval between measurements is short compared to the characteristic times associated with spacecraft translational dynamics, for example. It may also provide decreased solution sensitivity to bad measurement data, since bad data may be more readily identified when processing many data points simultaneously, rather than one at a time.

## 2.1. Batch and Batch-Sequential Filters

<span id="page-32-1"></span>In the context of earlier sections of this document, consider an m-dimensional measurement vector y, which is linearly related to the n-dimensional vector x and corrupted by measurement noise v:

| $\mathbf{y} = \mathbf{H}\mathbf{x} + \mathbf{v}$ | (2.1) |
|--------------------------------------------------|-------|
|--------------------------------------------------|-------|

where H is an m × n matrix and

| $E[\mathbf{v}] = 0$ | (2.2) |
|---------------------|-------|
|---------------------|-------|

| $E[\mathbf{v}^T] = \mathbf{R}$ | (2.3) |
|--------------------------------|-------|
|--------------------------------|-------|

with R an m × m positive-definite matrix. Then if we choose x to minimize the least-squares performance function

| $J(\mathbf{x}) = (\mathbf{y} - \mathbf{H}\mathbf{x})^T \mathbf{R}^{-1} (\mathbf{y} - \mathbf{H}\mathbf{x})$ | (2.4) |
|-------------------------------------------------------------------------------------------------------------|-------|
|-------------------------------------------------------------------------------------------------------------|-------|

we find that the minimizing value ˆx<sup>+</sup> satisfies the normal equation

| $H^T R^{-1} H \hat{x}^+ = H^T R^{-1} y.$ | (2.5) |
|------------------------------------------|-------|
|------------------------------------------|-------|

This equation can be solved uniquely for ˆx<sup>+</sup> if H<sup>T</sup>R−1H is nonsingular. (Of course, there are potential numerical problems associated with these mathematical operations.) In addition, the error covariance matrix associated with ˆx<sup>+</sup> is the inverse of the information matrix H<sup>T</sup>R−1H. This is, so far, a simpler estimation problem than was considered in the previous chapter in that we have said nothing yet about dynamics – we are dealing with a static estimation problem.

Now let us suppose that some a priori information was available about x before the processing of the measurements y in the form of an estimate ˆx<sup>−</sup> and an n × n weighting matrix Λ<sup>−</sup> characterizing the accuracy of the estimate (with large eigenvalues of Λ<sup>−</sup> indicating good knowledge of certain linear combinations of components of x and small eigenvalues indicating poor knowledge). We shall assume that

$$\mathbf{E}[(\mathbf{x} - \hat{\mathbf{x}}^-)\mathbf{v}^\top] = 0. \quad (2.6)$$

Then the least-squares performance function that was minimized above to provide an estimate of x after the processing of the measurements can now be generalized to

$$J(\mathbf{x}) = (\mathbf{x} - \hat{\mathbf{x}}^-)^T \mathbf{\Lambda}^- (\mathbf{x} - \hat{\mathbf{x}}^-) + (\mathbf{y} - \mathbf{H}\mathbf{x})^T \mathbf{R}^{-1} (\mathbf{y} - \mathbf{H}\mathbf{x}). \quad (2.7)$$

$$J(\mathbf{x}) = (\mathbf{x} - \hat{\mathbf{x}}^-)^T \Lambda^- (\mathbf{x} - \hat{\mathbf{x}}^-) + (\mathbf{y} - \mathbf{H}\mathbf{x})^T \mathbf{R}^{-1} (\mathbf{y} - \mathbf{H}\mathbf{x}). \quad (2.7)$$

Minimization of this quantity with respect to x yields the quantity ˆx<sup>+</sup>, which satisfies the modified normal equation

$$(\Lambda^- + H^- R^{-1} H) \hat{x}^+ = \Lambda^- \hat{x}^- + H^- R^{-1} y \quad (2.8)$$

| $(\Lambda^- + H^I R^{-1} H) \hat{x}^+ = \Lambda^- \hat{x}^- + H^I R^{-1} y$ | (2.8) |
|-----------------------------------------------------------------------------|-------|
|-----------------------------------------------------------------------------|-------|

or

<span id="page-33-1"></span>
$$(\Lambda^- + H^T R^{-1} H)(\hat{\mathbf{x}}^+ - \hat{\mathbf{x}}^-) = H^T R^{-1} (\mathbf{y} - H\hat{\mathbf{x}}^-). \quad (2.9)$$

$$(\Lambda^- + H^T R^{-1} H)(\hat{\mathbf{x}}^+ - \hat{\mathbf{x}}^-) = H^T R^{-1} (\mathbf{y} - H\hat{\mathbf{x}}^-). \quad (2.9)$$

Assuming that Λ<sup>−</sup> has full rank, it can be inverted, with its inverse being the error covariance matrix associated with the a priori estimate ˆx−. If the updated information matrix, Λ−+H<sup>T</sup>R−1H, is invertible, Eq. [2.9](#page-33-1) may be solved for ˆx<sup>+</sup>. The error covariance matrix associated with the solution ˆx<sup>+</sup> is the inverse of the updated information matrix. This updated error covariance matrix is mathematically (though not numerically) equivalent to equations for the covariance update in earlier chapters, such as Eqs. [\(1.31\)](#page-28-4) and [\(1.33\)](#page-28-3), although if there is process noise, Λ<sup>−</sup> could be different.

The equations above can be extended to accommodate parameters that are not estimated, but whose uncertainties are considered by the estimator. This topic is covered in the context of batchsequential estimators in many textbooks, including Bierman's Section VIII.2 [[5](#page-170-1)].

In real spacecraft navigation problems, of course, the available measurements are unlikely to be simple linear functions of the quantities to be estimated and may be time dependent as well. Thus, given measurements of the form

$$\mathbf{y}(t_i) = \mathbf{h}(\mathbf{x}(t_i), t_i) + \mathbf{v}(t_i) \quad (2.10)$$

$$\mathbf{y}(t_i) = \mathbf{h}(\mathbf{x}(t_i), t_i) + \mathbf{v}(t_i) \quad (2.10)$$

quantities of the form Hx above would be more generally replaced by h(x(ti), ti) with the matrix <sup>H</sup> replaced elsewhere by the partial derivative matrix <sup>∂</sup>h(x(ti),ti) ∂x(ti) .

Measurements that are accumulated over some time interval may be referenced back to the estimated parameters at the start of that time interval. In [4.1,](#page-58-1) this document addresses the situation in which measurement time tags are not equal to the current filter epoch. The situation under discussion there is that in which some latency is associated with the measurements, so that the measurement times are earlier than the current state epoch. However, the mathematical development there is also applicable to the situation of interest here, in which the measurement times are later than the state epoch, corresponding to the state epoch being held fixed (at least temporarily) as measurements are accumulated.

If the state epoch is never advanced, the estimator is referred to as a batch filter. If the epoch is advanced periodically, the estimator is referred to as a batch-sequential filter. The use of a batchsequential filter allows process noise effects to be treated more effectively than is the case with a simpler batch filter, as discussed in Bierman's Chapters VI and X [[5](#page-170-1)]. When all measurements within some time interval have been processed, the parameter estimates and associated error covariance may be propagated forward to a new reference time (as in [\(1.26\)](#page-28-1) and [\(1.30\)](#page-28-7) or [\(1.45\)](#page-30-1) and [\(1.49\)](#page-30-2)), which then serves as the beginning of the next batch of measurements.

## 2.2. Onboard Navigation Using Batch-Sequential Filters

<span id="page-33-0"></span>While navigational computations have been performed on the ground in the great majority of NASA's missions, a few robotic planetary exploration missions have required on-board autonomous navigation over brief time intervals to achieve a satisfactory return of scientific data or to survive passage through a difficult flight regime. In these instances, mission objectives could not be fulfilled using ground-based navigation alone, due to round-trip light time delays and their effect on navigational accuracies. The first onboard navigation filter used for deep space missions was developed for the Deep Space 1 mission (DS1, launched in 1998); and versions of the software (called AutoNav) were subsequently flown on the Stardust (launched in 1999) and Deep Impact (DI, launched in 2004) missions. Other subsequent deep space missions have relied on sequential Kalman-like filtering approaches of the sort described elsewhere in this document.

For DS1, onboard navigation in the cruise phase was done autonomously by imaging "beacon" asteroids, one at a time, relative to star backgrounds. Each such measurement gave a twodimensional position fix for the spacecraft to some level of accuracy. Subsequent measurements in different directions provided different two-dimensional position fixes. Several clusters of such sightings were incorporated into a least-squares filter to obtain an orbit determination (OD) solution. The on-board dynamical model of the spacecraft included gravitational attractions of the major bodies of the solar system, solar radiation pressure, thrust forces due to the ion propulsion system or the hydrazine attitude control thrusters, and a three-dimensional bias acceleration to account for small unmodeled forces. The propagation of the spacecraft motion was done in a heliocentric coordinate system using a 7-8th order Runge-Kutta numerical integrator. The reason for selecting this propagator was largely pragmatic: comparisons between this propagator and the one used by the Orbit Determination Program, used for all ground-based navigation of JPL's deep space missions at that time, indicated that errors when integrating a low-thrust trajectory for several months were on the order of meters, well below the sensing ability of the optical data. This integrator was readily available and could easily be coded. Orbit determination solutions were obtained by linearizing about a nominal trajectory and estimating corrections to parameters that minimized the data residuals in a weighted least-squares sense, using the U-D covariance factorization method for solving the normal equations. The accuracy of the autonomous navigation system was assessed by comparison to the results of a standard full, ground-based orbit determination process [[4](#page-170-4)], [[2](#page-170-5)].

From its initial inception, the DS1 navigation filter was designed as a batch processor. The primary reason for this was the sporadic nature of the measurements, in which a batch of 12-16 images would be taken for OD approximately once every week. In addition, the data arc for which the OD was performed spanned multiple weeks. This was needed to build up enough accumulated thrust from the ion engines such that the change in orbit could be observable in the optical data, and any trajectory deviations could then be corrected in upcoming thrusting cycles. For robust operations over these long durations, AutoNav would periodically "wake up" when the burst of images became available, perform an OD solution, update the future maneuvers, and then return to a hibernation state. The OD arcs were overlapping. The filter was only invoked after about four weeks of data were accumulated; and when an additional week of data was taken, the epoch would move forward a week, with the OD performed on the current four-week arc. Each week's OD fit was initialized with essentially an open a priori covariance; in other words, the post-fit covariance from the previous solution was effectively thrown away and the filter started anew (however, using the previous OD solution itself as the new reference). This ensured that the covariances did not end up overly constraining the solution, as early simulations indicated could easily happen. The initialization of the reference was first done from the ground; subsequently, it was obtained from the previous OD fit.

Data editing was an important step in the process, but had to be tailored for each specific scenario. For the DS1 cruise, the editing was fairly straightforward: the mean and standard deviation of the residuals between the observed measurement data and those computed from the latest, best OD solution for each batch of 12-16 images were computed, and any point above a pre-specified limit was deleted. The limit was a parameter that could be set, and typically values of 2.5 or 3 <span id="page-35-0"></span>sigma were used. Once the data passed this test, the data were never removed but reprocessed in the filter for each OD arc. This way, rigorous quality checking could occur on the data by comparing the prefit residuals against the best OD from the previous fit, and this process was greatly facilitated by use of the batch filter. The overall philosophy was to never allow bad data to corrupt the filter, so that each OD update could be largely guaranteed to be accurate. Consequently, if a situation occurred where no good data were obtained, the latest successful OD could always be used as a starting point when good data were available. This document more fully addresses the topic of editing in Section [10.1.](#page-124-1)

A modified version of AutoNav was used in a more limited scenario on the DI mission. On DI, the cruise portion was navigated using standard ground practices, but the mission's goal impacting the nucleus of comet 9P/Tempel 1 at a speed of over 10 km/s with one spacecraft, while tracking the nucleus through the impact time frame with a second, flyby spacecraft - could not have been accomplished from the ground. Thus, the DS1 AutoNav system was adapted to DI's mission needs, which maintained the basic filter functionality, changing primarily the time frame of the imaging cadence and OD updates [[47](#page-171-2)].

For the Tempel 1 encounter, AutoNav was initialized on the impactor spacecraft 2 hours prior to encounter with the best ground-based information to that point. Images were accumulated every 15 seconds; but for the first 10 minutes, no filter update was performed. Instead, the observation residuals against the reference trajectory were first checked for bad data, and any outliers removed. The editing scheme used was relatively simple: an absolute cutoff for any residual over a set number of pixels (adjustable and set in practice to about half the total camera field-of-view) was employed to protect against events such as a large, bright, comet outgassing event, or stray light in the camera. With the cleaned-up data, a batch estimate was performed. Subsequently, each image would trigger an OD update, using all accumulated data, and always checking for bad data/outliers by examining the prefit residuals against the previous OD solution. After 20 minutes, the filter epoch was moved forward to always maintain a 20-minute data arc. As was described for DS1 above, each OD would also start with an essentially open a priori state covariance; and the filter was never constrained by using the post-fit covariance from a previous OD run. Since the impactor's purpose was to hit the nucleus, the OD solutions were used to compute three impulsive maneuvers (at 90, 30, and 12 minutes prior to impact); after each maneuver, all previous data were thrown away and the filter re-initialized and the OD process repeated as before. The identical software was also used on the flyby spacecraft (without the maneuvers) to track the nucleus, and the impact event, as it flew by. This experience was successfully repeated in a flyby of comet 103P/Hartley 2 in 2010.

The use of the moving data arc window, starting with an open a priori covariance for each arc, and re-starting the filter after maneuvers, was in general found to be the best practice for these particular onboard scenarios, namely the relative infrequency of data (every 15 seconds at best as compared to, for example, Doppler data which are generated at 10 Hz), the slow dynamics (cruise in interplanetary space and fast encounters of small bodies with little gravitational bending), and highly unknown characteristics of the observed bodies (size, shape) which could induce unpredictable signatures in the observations. The practices and filter parameters (such as the data editing criteria) were arrived at through testing in many thousand Monte Carlo simulation runs, adjusting parameters until, heuristically, a reasonably optimal solution was found that balanced risk and probability of success. The choices were validated by the fact that the end result proved successful on multiple occasions on three different spacecraft.

In addition to the mainline filter used by DI, and by DS1 in the cruise portion of the mission, a stripped down filter was also developed specifically for flybys of small bodies, which was also part of the mission plan for DS1. This filter, dubbed Reduced State Encounter Navigation (RSEN), was intended for use during the tens of minutes surrounding the flyby to update the target-relative spacecraft state, which could then be used to improve instrument pointing to maintain lock on the target during the high speed flyby [[3](#page-170-6)]. Unlike the mainline filter, this was originally developed as a standard Kalman filter since the state update had to occur quickly, with each measurement being immediately ingested to update the state and no data editing. The assumption at the time was that the signal of the target body would be extremely bright, and so little was done to prevent bad data from being ingested into the filter; in retrospect, this was obviously a very bad assumption.

Unfortunately, in its first use during the flyby of the asteroid Braille, the software failed to track the target during the encounter. It was determined after the fact that the very first observation it received was bad data (presumably from a cosmic ray hit); this spurious signal appeared above the detection threshold level before Braille itself exceeded that level, causing the initial on-board orbit solution to shift by 30 km. The filter never recovered thereafter, always causing the imaging system to point in the wrong direction [[2](#page-170-5)] and never detecting Braille.

After the Braille experience, the RSEN code was reformulated in the same batch formulation as the mainline code. Although in principle the same Kalman filter could have been used with a front-end data editor, the familiarity, experience, and successful implementation of the batch setup warranted the change. Starting 32 minutes prior to closest approach, data were allowed to be accumulated (at a rate of once every 30 seconds) without a filter update. These data were rigorously checked for consistency, using a somewhat complicated editing scheme where residual points were checked three at a time in a moving window, rejecting points which did not match their neighbors within a threshold more than once. The reason this scheme, rather than a simpler mean and standard deviation check, was used was because the signature of the optical residuals during the flyby was not flat, but sloped considerably due to parallax as the spacecraft approached the asteroid. At 10 minutes before encounter, the batch filter was invoked to update the targetrelative trajectory. Each subsequent image would trigger a new solution, starting from the previous OD, but still using all the accumulated data. This new formulation was employed in the encounter with comet 19P/Borrelly in 2001, successfully capturing high resolution images of the nucleus. The final image was shuttered 166 seconds before encounter. This same system was, with some minor modifications to the filter starting time and update point, used on the Stardust mission to track the asteroid 5535 Annefrank (2002), and the comets 81P/Wild 2 (2004) and 9P/Tempel 1 (2011) [[3](#page-170-6)].

While the three previous mission examples describe the use of autonomous navigation in small-body flyby or impacting missions, substantially different issues arise in autonomously landing on Mars, one of which will be described here. The Mars Science Laboratory (MSL) mission used data from its Terminal Descent Sensor (TDS), a multi-beam radar that provided velocity and range measurements [[16](#page-170-7)]. The parameters of interest were vertical position and all three velocity components, allowing a touchdown at a constant vertical velocity of 0.60 m/s and a horizontal velocity of 0.12 m/s. Generally speaking, the navigation system design was heavily focused on being robust and facilitating a survivable landing, rather than on accuracy per se or other performance measures. Rather than expecting the hardware to be perfect, the plan was to build a filter that could be made robust to a variety of measurement error modes, as well as to hardware failures in flight (e.g., losing one of the radar beams). The TDS was extensively characterized, including tests with aircraft that largely duplicated the MSL flight profile. While largely successful, the testing revealed that there was an ambiguity resolution failure that could lead to spurious 40 m/s velocity residuals for a small fraction of the measurements (compared to a residual RMS of 1 m/s or less for the good data points). The MSL navigation filter had tuning parameters that easily handled this data error and also demonstrated in testing that it could survive a complete beam failure.

The navigation filter architecture actually used three different batch filters, running in parallel. Each filter drew from a buffer of 20-some minimally checked TDS measurements. Up until rover detachment, each used a fixed-length, sliding-window mode (each filter using a different length); and afterwards, each ran in fixed-epoch, increasing-length mode. One filter's output was used for the velocity estimate, and two different filters contributed altitude estimates. The altitude estimates were stored in a buffer, and their mean was used by the control system. Each filter performed a finite number of recursive data editing steps to remove the velocity outliers mentioned above and (hopefully) any other data artifacts. After rover detachment from the descent stage (with the rover descending on a tether), concerns that the rover or debris from the approaching surface would interfere with the vertical beams limited the radar data to usage in the horizontal velocity estimate, with the vertical state proceeding on inertial measurement unit propagation. (As it turned out, the radar did generate some measurements of blowing dust near the surface, and these were ingested for MSL landing with some loss of accuracy. For the later Mars 2020 landing, the editing parameters were adjusted to reject these data, with better results.) Each stage of the landing process had the capability to use a unique set of filter parameters. All together, the heavily defensive solution approach succeeded in the actual landing and in passing many stress and failure tests during development. This focus on being highly resistant to problems (while still being good enough to land) is very appropriate for this sort of critical application.

## <span id="page-38-0"></span>The Covariance Matrix

Contributed by J. Russell Carpenter

As Chapter [1](#page-24-0) pointed out, the EKF estimate Xˆ (t) is at best an approximation for E[X(t)|Y], and hence the EKF symbol P(t) is at best an approximation for E[e(t)e T (t)|Y]. In the present Chapter we discuss best practices for maintaining such approximations, and henceforth we will simply refer to P(t) as the covariance matrix.

## 3.1. Metrics for Orbit State Covariances

<span id="page-38-1"></span>To discuss what makes one covariance approximation better or worse than another, we must be able to compare matrices to one another, and hence we must adopt metrics. For matrices that serve as coefficients, there exist various matrix norms that serve as distance-like metrics for the strength of the coefficient. For covariance matrices, we are usually more interested in measures of the range of possible realizations that could be drawn from the probability distribution characterized by the covariance. The square root of the trace of the covariance is often a reasonable choice, since it is the root sum squared (RSS) formal estimation error. A drawback to the trace for orbital applications is that coordinates and their derivatives typically differ by several orders of magnitude, so that for example the RSS position error will dominate the RSS velocity error if the trace is taken over a 6 × 6 Cartesian position and velocity state error covariance, unless some scaling is introduced. Although arbitrary scalings are possible, we discuss several metrics herein that have been found to be especially suitable to space applications.

Orbit determination is distinguishable from other types of positioning and navigation not only by the use of dynamics suitable to orbiting bodies, but also by a fundamental need to produce states that predict accurately. This need arises because spacecraft operations require accurate predictions for acquisition by communications assets, for planning future activities such as maneuvers and observations, for predicting conjunctions with other space objects, etc. For closed, i.e. elliptical, orbits about most planetary bodies, the two-body potential dominates all other forces by several orders of magnitude. Thus, in most cases, the ability of an orbit estimate to predict accurately is dominated by semi-major axis (SMA) error, δa. This is because SMA error translates into period error through Kepler's third law, and an error in orbit period translates into a secularly increasing error in position along the orbit track. As Reference [[10](#page-170-8)] shows, the along-track drift per orbit revolution, δs, for an elliptical orbit with eccentricity e is bounded by

$$\delta s = -3\pi\sqrt{\frac{1+e}{1-e}}\delta a$$
 from periapse to periapse (3.1)

$$\delta s = -3\pi \sqrt{\frac{1-e}{1+e}} \delta a \quad \text{from apoapse to apoapse} \quad (3.2)$$

This phenomenon is especially significant for rendezvous and formation flying applications, where relative positions must be precisely controlled.

For a central body whose gravitational constant is µ, the SMA of a closed Keplerian orbit, a, may be found from the vis viva equation,

<span id="page-39-0"></span>
$$-\frac{\mu}{2a} = -\frac{\mu}{r} + \frac{v^2}{2} \quad (3.3)$$

from which one can see that achieving SMA accuracy requires good knowledge of both radius, r, and speed, v. What is less obvious from [\(3.3\)](#page-39-0) is that radius and speed errors must also be both well-balanced and well-correlated to maximize SMA accuracy [[10](#page-170-8),[13](#page-170-9),[35](#page-171-3)], as Figure [3.1](#page-39-1) illustrates. In this figure, radius standard deviation, or formal error, σr, has been normalized by the squared

![](_page_39_Figure_6.jpeg)

<span id="page-39-1"></span>Figure 3.1. Formal error in semi-major axis depends on formal errors in radius, speed, their correlation, and their balance. All scales are in units of position.

ratio of radius to SMA, and speed formal error, σv, has been normalized by nvc/v, where the orbital rate is n = p µ/a<sup>3</sup>, and the circular speed is v<sup>c</sup> = p µ/a, to make the relationships illustrated be independent of any particular point in any particular closed orbit. Figure [3.1'](#page-39-1)s contours of constant SMA error, σa, show that σ<sup>a</sup> is dominated by radius error below a diagonal region, and dominated by speed error above the diagonal. When radius and speed errors are balanced, along the diagonal, SMA accuracy can be substantially improved by increasing (negative) correlation. Experience has shown that σ<sup>a</sup> is one of the more useful figures of merit for evaluating orbit determination performance, particularly for relative navigation applications.

In fact, it is easy to show that any function of two (scalar) random variables possesses a similar correlation and balance structure, at least to first order. For example, navigation requirements for atmospheric entry are often stated in terms of flight-path angle error, δγ. Since sin γ = $\vec{r}$/∥$\vec{r}$∥ · $\vec{v}$/∥ $\vec{v}$∥, then from geometrical considerations we should expect that δγ depends on the component of position error which is in the local horizontal plane, in the direction of the velocity vector, and on the component of velocity error that is normal to both velocity and angular momentum, i.e. binormal to the velocity vector. These are of course the in-plane components of position and velocity that are normal to radius and speed. Thus by using the pair δa and δγ as metrics, we can fully characterize the correlation and balance of the in-plane covariance components. The following subsections derive these relationships.

3.1.1. Variance of an Arbitrary Function of Two Random Variables Suppose there exists a random variable z which is a possibly nonlinear function[<sup>1</sup>](#page-40-0) of two other random variables, x and y, such that

| $z = f(x, y)$ | (3.4) |
|---------------|-------|
|---------------|-------|

and let the joint covariance of x and y be given by

$$\mathbf{P} = \begin{bmatrix} \sigma_x^2 & \rho_{xy}\sigma_x\sigma_y \\ \rho_{xy}\sigma_x\sigma_y & \sigma_y^2 \end{bmatrix} \quad (3.5)$$

The variance of z is given by

$$\sigma_z^2 = E[(z - E[z])^2] \quad (3.6)$$

where

$$E[z] = \int_{-\infty}^{\infty} \zeta \, p_z(\zeta) \, d\zeta = \int_{-\infty}^{\infty} \int_{-\infty}^{\infty} f(\xi, \eta) \, p_z(f(\xi, \eta)) \, d\xi \, d\eta \quad (3.7)$$

Let xˆ = E[x] and yˆ = E[y]. Then E[x − xˆ] = 0 and E[y − yˆ] = 0. Expanding f(x, y) around f(ˆx, yˆ) in a Taylor series to first order, we find that

$$f(x, y) \approx f(\hat{x}, \hat{y}) + f_x \cdot (x - \hat{x}) + f_y \cdot (y - \hat{y}) \quad (3.8)$$

where f<sup>x</sup> and f<sup>y</sup> are the partials of f with respect to x and y, respectively; so, to first order,

$$\hat{z} = E[z] = E[f(x, y)] \approx f(\hat{x}, \hat{y}) \quad (3.9)$$

Now let us similarly expand (z − E[z])<sup>2</sup> to first order:

$$(x - E[z])^2 = (f(x, y) - f(\hat{x}, \hat{y}))^2 \quad (3.10)$$

$$\approx f_x^2 \cdot (x - \hat{x})^2 + 2f_x f_y \cdot (x - \hat{x})(y - \hat{y}) + f_y^2 \cdot (y - \hat{y})^2 \quad (3.11)$$

Taking expectations on both sides yields

$$\mathbb{E}[(z - E[z])^2] = f_x^2 \mathbb{E}[(x - \hat{x})^2] + 2f_x f_y \mathbb{E}[(x - \hat{x})(y - \hat{y})] + f_y^2 \mathbb{E}[(y - \hat{y})^2] \quad (3.1)$$

$$\sigma_2^2 = f_x^2 \sigma_x^2 + 2f_x f_y \rho_{xy} \sigma_x \sigma_y + f_y^2 \sigma_y^2 \quad (3.1)$$

$$\sigma_z^2 = f_x^2 \sigma_x^2 + 2 f_x f_y \rho_{xy} \sigma_x \sigma_y + f_y^2 \sigma_y^2 \quad (3.1)$$

| $= \mathbf{FFF}^T$ | (3.14) |
|--------------------|--------|
|--------------------|--------|

where F = [fx, fy]. Since −1 < ρxy < 1, it is clear that a high negative correlation between x and y will minimize σ<sup>z</sup> for given values of σ<sup>x</sup> and σy, but if either fxσ<sup>x</sup> >> fyσ<sup>y</sup> or fxσ<sup>x</sup> << fyσy, the impact of the negative correlation will be insignificant. Thus, the only way to simultaneously

<span id="page-40-0"></span><sup>1</sup> If the function is nonlinear, the variance formula here is an approximate, first-order result.

achieve σ<sup>z</sup> << fxσ<sup>x</sup> and σ<sup>z</sup> << fyσ<sup>y</sup> is when ρxy ≈ −1 and fxσ<sup>x</sup> ≈ fyσy, which are the correlation and balance conditions mentioned above, and which occur along the diagonal of Figure [3.1.](#page-39-1)

Note also that by defining new variables scaled by their respective partial derivatives, x˜ = xf<sup>x</sup> and y˜ = yfy, and correspondingly σ˜<sup>x</sup> = fxσ<sup>x</sup> and σ˜<sup>y</sup> = fyσy, then a normalization of the fashion described above is also possible:

$$\sigma_z = \sqrt{\tilde{\sigma}_x^2 + 2\rho_{xy}\tilde{\sigma}_x\tilde{\sigma}_y + \tilde{\sigma}_y^2} \quad (3.15)$$

3.1.2. Semi-Major Axis Variance To derive a relationship for semi-major axis variance, let us take variations on [\(3.3\)](#page-39-0), which results in

$$\frac{\delta a}{a^2} = \frac{2\delta r}{r^2} + \frac{2v\delta v}{\mu} \quad (3.16)$$

If we replace the variations with deviations of random variables from their expectations, and the non-deviated terms with their expected values, we find that

$$(a - \hat{a}) = 2\hat{a}^2 \left( \frac{(r - \hat{r})}{\hat{r}^2} + \frac{\hat{v}(\mathbf{v} - \hat{v})}{\mu} \right) \quad (3.17)$$

which by squaring and taking expectation yields the following linearized approximation for the SMA variance:

<span id="page-41-0"></span>
$$\sigma_a^2 = 4\hat{a}^4 \left\{ \frac{1}{\hat{r}^4} \sigma_r^2 + 2 \frac{\hat{v}}{\mu \hat{r}^2} \rho_{rv} \sigma_r \sigma_v + \frac{\hat{v}^2}{\mu^2} \sigma_v^2 \right\} \quad (3.18)$$

For the normalization used in Figure [3.1,](#page-39-1) rewrite [\(3.18\)](#page-41-0) as

$$\sigma_a = 2\sqrt{\left(\frac{\sigma_r}{\hat{r}^2/\hat{a}^2}\right)^2 + 2\rho_{rv}\left(\frac{\sigma_r}{\hat{r}^2/\hat{a}^2}\right)\left(\frac{\sigma_v}{\mu/(\hat{a}^2\hat{v})}\right) + \left(\frac{\sigma_v}{\mu/(\hat{a}^2\hat{v})}\right)^2} \quad (3.19)$$

and note that µ/(ˆa <sup>2</sup>vˆ) = ˆnvˆc/vˆ. As mentioned above, normalizing radius and speed standard deviation in this manner permits comparison of data across all points in all closed orbits.

If the orbit is exactly circular, then further simplification of [\(3.18\)](#page-41-0) is possible. In this case, a = r and v/µ = Tp/2π, where T<sup>p</sup> is the orbit period. Then [\(3.18\)](#page-41-0) may be rewritten as

$$\sigma_a = 2\sqrt{\sigma_r^2 + 2\left(\frac{T_p}{2\pi}\right)\rho_{rv}\sigma_r\sigma_v + \left(\frac{T_p}{2\pi}\right)^2\sigma_v^2} \quad (3.20)$$

For orbit determination applications, the state representation most often chosen is a Cartesian inertial state vector, x = [ $\vec{r}$ T , $\vec{v}$ T ] T . Rewriting [\(3.3\)](#page-39-0) as

$$a(\mathbf{x}) = \left( \frac{2}{\|\mathbf{r}'\|} - \frac{\|\mathbf{v}\|^2}{\mu} \right)^{-1} \quad (3.21)$$

and taking partials yields

$$\left. \frac{\partial a}{\partial \mathbf{x}} \right|_{\hat{\mathbf{x}}} = \mathbf{F}_a(\hat{\mathbf{x}}) = 2\hat{a}^2 \left[ \frac{\hat{\mathbf{r}}^\top}{\hat{r}^3} - \frac{\hat{\mathbf{v}}^\top}{\mu} \right] \quad (3.22)$$

so that

$$\sigma_a^2 = \mathbf{F}_a(\hat{\mathbf{x}})\mathbf{P}_{\mathbf{x}}\mathbf{F}_a^{\mathbf{T}}(\hat{\mathbf{x}}) \quad (3.23)$$

3.1.3. Flight-Path Angle Variance The flight-path angle, γ, is the angle between the velocity vector and the local horizontal plane; it is therefore the complement of the angle between the position and velocity vectors, so that

$$\gamma = \arcsin(\mathbf{u}_{\mathcal{F}} \cdot \mathbf{u}_{\mathcal{V}}) \quad (3.24)$$

where u $\vec{r}$ = $\vec{r}$/r and u $\vec{v}$ = $\vec{v}$/v. Taking partials with respect to x, we find that

$$F_{\gamma}(\hat{\mathbf{x}}) = \frac{\partial \gamma}{\partial \mathbf{x}} \Big|_{\hat{\mathbf{x}}} = \frac{1}{\sqrt{1 - \sin^2 \hat{\gamma}}} \left[ \frac{\mathbf{u}_{\hat{\mathbf{x}}} - \sin \hat{\gamma} \mathbf{u}_{\hat{\mathbf{x}}}^T}{\hat{\mathbf{r}}} - \frac{\mathbf{u}_{\hat{\mathbf{r}}}^T - \sin \hat{\gamma} \mathbf{u}_{\hat{\mathbf{r}}}^T}{\hat{\mathbf{v}}} \right], \quad -\frac{\pi}{2} < \hat{\gamma} < \frac{\pi}{2} \quad (3.25)$$

so that

<span id="page-42-0"></span>
$$\sigma_\gamma^2 = \mathbf{F}_\gamma(\hat{\mathbf{x}})\mathbf{P}_\gamma\mathbf{F}_\gamma^\top(\hat{\mathbf{x}}) \quad (3.26)$$

which is a form suitable for use in an OD filter estimating a Cartesian inertial state.

For analysis, a simpler form of [\(3.26\)](#page-42-0) is as follows. Let us define two vectors that are normal to both the position vector and a vector normal to the orbit plane, $\vec{n}$ : the unit in-track vector,

$$\mathbf{u}_{\Delta \vec{v}} = \mathbf{u}_{\vec{n}} \times \mathbf{u}_{\vec{r}} = \frac{\mathbf{u}_{\vec{v}} - \mathbf{u}_{\vec{r}} \sin \gamma}{\sqrt{1 - \sin^2 \gamma}} \quad (3.27)$$

which defines a unit vector in the orbit plane that is along the orbit track at apoapsis and periapsis, and the unit bi-normal vector,

$$u_{\bar{v}}^{-} = u_{\bar{v}} \times u_{\bar{n}} = \frac{u_{\bar{r}} - u_{\bar{v}} \sin \gamma}{\sqrt{1 - \sin^2 \gamma}} \quad (3.28)$$

which defines a unit vector in the orbit plane that is along the position vector at apoapsis and peripasis. Let us next define a composite transformation matrix as follows. Let

$$M_{rtn} = [u_{\vec{r}_I} \quad u_{\Delta \vec{r}_I} \quad u_{\vec{n}_I}] \quad (3.29)$$

where the subscript I indicates that the specified vector is expressed in an inertial basis. The unitary matrix M<sup>T</sup> rtn thus transforms coordinates of vectors in physical space, which are given in the frame I, to a coordinates defined in the basis given by the the radial, transverse, and normal unit vectors. Similarly, define Mvnb as

| $\mathbf{M}_{vnb} = [\mathbf{u}_{ \vec{v}_I}]$ | $\mathbf{u}_{\vec{n}_I}$ | $\mathbf{u}_{\vec{b}_I}$ | (3.30) |
|-----------------------------------------------|--------------------------|--------------------------|--------|
|-----------------------------------------------|--------------------------|--------------------------|--------|

Now define the block diagonal transformation matrix M as

<span id="page-42-1"></span>
$$\mathbf{M} = \begin{bmatrix} \mathbf{M}_{rtn} & \mathbf{0}_{3x3} \\ \mathbf{0}_{3x3} & \mathbf{M}_{vnb} \end{bmatrix} \quad (3.31)$$

Using the matrix M, we can transform the state error covariance, given in inertial coordinates, such that its position error covariance is expressed in the "RTN" frame, and its velocity error covariance is in the "VNB" frame. Using the preceding results in [\(3.26\)](#page-42-0) results in considerable simplification:

| $\sigma_\gamma^2 = [\mathbf{u}_{\hat{t}}^\dagger \hat{r} \quad \mathbf{u}_{\hat{b}}^\dagger \hat{v}]$ | $\begin{bmatrix} \mathbf{M}_{rtn}^\dagger & \mathbf{0}_{3\times 3} \\ \mathbf{0}_{3\times 3} & \mathbf{M}_{vnb}^\dagger \end{bmatrix}$ | $\mathbf{P}_\times$ | $\begin{bmatrix} \mathbf{M}_{rtn} & \mathbf{0}_{3\times 3} \\ \mathbf{0}_{3\times 3} & \mathbf{M}_{vnb} \end{bmatrix}$ | $\begin{bmatrix} \mathbf{u}_{\hat{t}}^\dagger \hat{r} \\ \mathbf{u}_{\hat{b}}^\dagger \hat{v} \end{bmatrix}$ | (3.32) |
|-------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------|---------------------|------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------|--------|
|                                                                                                       |                                                                                                                                        |                     |                                                                                                                        |                                                                                                              |        |

$$= \left( \frac{\sigma_{\mathbf{r}_t}}{\hat{r}} \right)^2 + 2\rho_{\mathbf{r}_t}\mathbf{v}_b \left( \frac{\sigma_{\mathbf{r}_t}}{\hat{r}} \right) \left( \frac{\sigma_{\mathbf{v}_b}}{\hat{v}} \right) + \left( \frac{\sigma_{\mathbf{v}_b}}{\hat{v}} \right)^2 \quad (3.33)$$

which demonstrates the aforementioned assertion that flight-path angle error depends on the intrack component of position error, and the bi-normal component of velocity error. Note that [\(3.33\)](#page-42-1) possesses the desirable feature that the relevant covariance information (in-track position variance and bi-normal velocity variance) is normalized by radius and speed, allowing differing orbital <span id="page-43-1"></span>conditions to be readily compared with one another. In most applications, σr<sup>t</sup> << rˆ and σv<sup>b</sup> << vˆ so that these ratios can be taken as small angles and expressed in angular measures commensurate with the units chosen for flight-path angle itself. Figure [3.2](#page-43-0) employs this convention.

![](_page_43_Figure_3.jpeg)

<span id="page-43-0"></span>Figure 3.2. Formal error in flight-path angle depends on formal errors of in-track component of position, bi-normal component of velocity, their correlation, and their balance.

3.1.4. Summary of Orbit Determination Covariance Metrics A recommended best practice for comparison of OD covariances is to use the semi-major axis standard deviation as a metric for most applications, with a secondary emphasis on flight-path angle standard deviation. For entry applications, a best practice is to use flight-path angle standard deviation at entry interface as the primary metric. In using these metrics, one should keep in mind that when computed in the manner shown here, they are nonlinear functions of the state variables, and hence do not preserve properties of the underlying state error distributions. A summary of these metrics is as follows.

<span id="page-44-3"></span>For orbits that are very close to circular:

$$\sigma_a = 2\sqrt{\sigma_r^2 + 2\left(\frac{T_p}{2\pi}\right)\rho_{rv}\sigma_r\sigma_v + \left(\frac{T_p}{2\pi}\right)^2\sigma_v^2} \quad (3.34)$$

For elliptical orbits:

$$\sigma_a = 2\hat{a}^2 \sqrt{\frac{1}{\hat{r}^4} \sigma_r^2 + 2 \frac{\hat{v}}{\mu \hat{r}^2} \rho_{rv} \sigma_r \sigma_v} + \frac{\hat{v}^2}{\mu^2} \sigma_v^2 \quad (3.35)$$

For normalization of radius and speed standard deviations across points in closed orbits:

$$\sigma_a = 2 \sqrt{\left(\frac{\sigma_r}{\hat{r}^2/\hat{a}^2}\right)^2 + 2\rho_{rv}\left(\frac{\sigma_r}{\hat{r}^2/\hat{a}^2}\right)\left(\frac{\sigma_v}{\hat{n}\hat{v}_c/\hat{v}}\right) + \left(\frac{\sigma_v}{\hat{n}\hat{v}_c/\hat{v}}\right)^2} \quad (3.36)$$

For entry applications, and as a secondary metric:

$$\sigma_\gamma = \sqrt{\left(\frac{\sigma_{\mathbf{r}_t}}{\hat{r}}\right)^2 + 2\rho_{\mathbf{r}_t\mathbf{v}_b}\left(\frac{\sigma_{\mathbf{r}_t}}{\hat{r}}\right)\left(\frac{\sigma_{\mathbf{v}_b}}{\hat{v}}\right) + \left(\frac{\sigma_{\mathbf{v}_b}}{\hat{v}}\right)^2} \quad (3.37)$$

For use in an OD filter that is estimating a Cartesian inertial state vector:

$$\sigma_a = \sqrt{\mathbf{F}_a(\hat{\mathbf{x}})\mathbf{P}_{\mathbf{x}}\mathbf{F}_a^{\mathbf{T}}(\hat{\mathbf{x}})}, \quad \mathbf{F}_a(\hat{\mathbf{x}}) = 2\hat{a}^2 \begin{bmatrix} \hat{\mathbf{r}}^{\mathbf{T}} & \hat{\mathbf{v}}^{\mathbf{T}} \\ \hat{r}^2 & \frac{\mu}{\mu} \end{bmatrix} \quad (3.38)$$

$$\sigma_\gamma = \sqrt{\mathbf{F}_\gamma(\hat{\mathbf{x}})\mathbf{P}_{\mathbf{x}}\mathbf{F}_\gamma^\top(\hat{\mathbf{x}})}, \quad \mathbf{F}_\gamma(\hat{\mathbf{x}}) = \begin{bmatrix} \frac{\mathbf{u}_t^\top}{\hat{r}} & \frac{\mathbf{u}_b^\top}{\hat{v}} \end{bmatrix} \quad (3.39)$$

#### 3.2. Covariance Propagation

<span id="page-44-0"></span>This section discusses best practices for implementing the covariance propagation recursion

<span id="page-44-1"></span>
$$\mathbf{P}_i^* = \mathbf{\Phi}(t_i, t_{i-1})\mathbf{P}_{i-1}^* \mathbf{\Phi}^\top(t_i, t_{i-1}) + \mathbf{S}_i, \quad \mathbf{P}_0^* = \mathbf{P}_0, \quad (3.40)$$

As Chapter [1](#page-24-0) mentions, to achieve this goal we need suitable approximations for the state transition matrix, Φ(t<sup>i</sup> , ti−1), and the process noise covariance, S<sup>i</sup> . However, the suitability of a given set of approximations is strongly dependent on specifics of the application. For example, if a set of measurements from which the state is fully observable are available at an interval that is a small fraction of the orbit period, without significant drop-outs, and prediction of the covariance far into the future of the time of availability of the measurements is not required, then simple models such as those to which Chapter [1](#page-24-0) alluded have been successfully employed. Selection of appropriate covariance propagation approximations also depends strongly on the choice of state representation, which is the subject of Chapter [7.](#page-84-0) Therefore, this section will discuss the merits of some of the more common and generally applicable approaches, in the context of orbit determination.

3.2.1. Matrix Riccati Equation Many textbooks on Kalman filtering derive [\(3.40\)](#page-44-1) as the solution of a matrix Riccati equation; using the notation of Chapter [1,](#page-24-0) this takes the following form:

<span id="page-44-2"></span>
$$\dot{\mathbf{P}}(t) = \mathbf{A}(t)\mathbf{P}(t) + \mathbf{P}(t)\mathbf{A}^T(t) + \mathbf{Q}(t) \quad (3.41)$$

Use of [\(3.41\)](#page-44-2) would seem to avoid the need to perform the integrations required to compute the state transition matrix (STM) and process noise covariance (PNC). In orbit determination practice however, [\(3.40\)](#page-44-1) has been found to be more numerically stable and also, despite the need to compute or approximate the state transition and process noise integrals, more efficient than [\(3.41\)](#page-44-2).

<span id="page-45-4"></span>3.2.2. State Transition Matrix A common approach in ground-based OD, especially in the batch least squares context, is to simultaneously integrate the STM along with the state vector,

<span id="page-45-0"></span>
$$\dot{\mathbf{X}}(t) = \mathbf{f}(\mathbf{X}(t), t), \quad \mathbf{X}(t_0) = \mathbf{X}_0 \quad (3.42)$$

$$\dot{\Phi}(t, t_0) = \mathbf{A}(t) \Phi(t, t_0), \quad \Phi(t_0, t_0) = \mathbf{I} \quad (3.43)$$

When coupled with a good numerical integration algorithm, this method has excellent fidelity, which is rarely necessary in onboard OD applications. Lear [[50](#page-172-1)] studied a number of practical methods for computing the STM in the onboard OD context. As his report is not widely available, we will summarize some key findings here.

Lear's approach was to compare various orders of truncated Taylor series and Runge-Kutta approximations to the solution of [\(3.43\)](#page-45-0). He used these STM approximations to propagate an initially diagonal covariance for one revolution in a two-body circular orbit around a point mass with the GM of Earth. By comparing these results to those he obtained using an analytic STM, Lear could compute the maximum step size that would result in a given relative accuracy for radius and speed formal standard deviations. Table [1](#page-45-1) lists a few of Lear's results. Notably, Method H

| Description Method A. 1 st -order Taylor I + A i ∆ t B. 2 nd -order Taylor, ignoring A I ˙ + A i ∆ t + A 2 |      |         | Max. Step [sec] 0.125 |
|------------------------------------------------------------------------------------------------------------|------|---------|-----------------------|
| i ∆ t                                                                                                      |      |         |                       |
| 2 / 2                                                                                                      |      |         | 1.0                   |
| C. 2 nd -order Taylor I + A i ∆ t + ( A ˙                                                                  |      |         |                       |
| i + A 2                                                                                                    |      |         |                       |
| )∆                                                                                                         | t    |         |                       |
| i                                                                                                          |      | 2 / 2   | 16                    |
| F. 1 st -order Runge-Kutta I + A i + 5 ∆ t                                                                 |      |         | 0.14                  |
| G. 2 nd -order Runge-Kutta, with one                                                                       |      |         |                       |
| evaluation of A                                                                                            |      |         |                       |
| I + A i + 5 ∆ t + A 2                                                                                      |      |         |                       |
| i + 5 ∆ t                                                                                                  |      |         |                       |
| 2                                                                                                          | /    | 2       | 14                    |
| H. 2 nd -order Runge-Kutta, with two                                                                       |      |         |                       |
| evaluations of A                                                                                           |      |         |                       |
| I +( A i + A i +1 )∆ t/ 2+ A                                                                               | i +1 | A i ∆ t |                       |
|                                                                                                            |      | 2 / 2   | 16                    |

<span id="page-45-1"></span>Table 1. A few of Lear's STM Comparison Results, for 1% relative error.

has the desirable feature that simply saving the value of the state Jacobian from the previous propagation step allows for more than an order of magnitude increase in allowable time step, with essentially the same computational burden as Method B. If it is not too burdensome to compute A at the midpoint of the propagation step, then Method G offers nearly equivalent performance without the need to retain the previous value of A. For higher-rate propagations, Method B offers far more accuracy than Method A with only a small additional computational burden. While Method A appears to be a poor choice for many applications, it does play a central role in some useful approximations to the process noise covariance, as the sequel shows.

3.2.3. Process Noise Covariance As stated in Chapter [1,](#page-24-0) nearly all practical methods for computing the process noise covariance assume that E[w(t)w<sup>T</sup> (τ )] = Q(t)δ(t − τ ), so that [\(1.29\)](#page-28-5) simplifies to a single integral for the process noise covariance[<sup>2</sup>](#page-45-2) , given by [\(1.42\)](#page-29-2), and repeated here:

<span id="page-45-3"></span>
$$\mathbf{S}_i = \int_{t_{i-1}}^{t_i} \Phi(t_i, \tau) \mathbf{B}(\tau) \mathbf{Q}(\tau) \mathbf{B}^T(\tau) \boldsymbol{\Phi}^T(t_i, \tau) d\tau \quad (3.44)$$

<span id="page-45-2"></span><sup>2</sup>A notable exception is the work of Wright [[89](#page-173-2)], which describes a correlated process noise model that is intended to account for gravity modeling errors in a "physically realistic" manner. Although this method has had occasional onboard application, it is more widely known for its inclusion in commercial-off-the-shelf software for ground-based OD.

Tapley, Schutz, and Born [[81](#page-173-3)] describe two approximations to the portion of [\(3.44\)](#page-45-3) which corresponds to position and velocity state noise, which have proven useful in both ground- and onboard-OD applications. Reference [81](#page-173-3) refers to these methods as "State Noise Compensation" (SNC) and "Dynamic Model Compensation" (DMC). Before describing SNC and DMC however, we will consider some inappropriate models.

Chapter [1](#page-24-0) pointed out that

$$\begin{aligned} & \mathbb{E} \left[ \int_{t_{i-1}}^{t_i} \int_{t_{i-1}}^{t_i} \Phi(t_i, \tau) \mathbf{B}(\tau) \mathbf{w}(\tau) \mathbf{w}^\top(\sigma) \mathbf{B}^\top(\sigma) \Phi^\top(t_i, \sigma) d\tau d\sigma \right] \\ & \neq \mathbb{E} \left[ \int_{t_{i-1}}^{t_i} \Phi(t_i, \tau) \mathbf{B}(\tau) \mathbf{w}(\tau) d\tau \int_{t_{i-1}}^{t_i} \mathbf{w}^\top(\tau) \mathbf{B}^\top(\tau) \Phi^\top(t_i, \tau) d\tau \right] \quad (3.45) \end{aligned}$$

Let us explore the implications of assuming equality of the expression above. Suppose we assume that the process noise increments are approximately constant over some particular interval ∆t = t<sup>i</sup> − ti−1, and that E[w(ti)w<sup>T</sup> (t<sup>j</sup> )] = W(ti)δij , where δij denotes the Kronecker delta function. Then,

$$\begin{aligned} & \mathbb{E} \left[ \int_{t_{i-1}}^{t_i} \Phi(t_i, \tau) \mathbf{B}(\tau) \mathbf{w}(\tau) \, \mathrm{d}\tau \int_{t_{i-1}}^{t_i} \mathbf{w}^\top(\tau) \mathbf{B}^\top(\tau) \Phi^\top(t_i, \tau) \, \mathrm{d}\tau \right] \\ &= \int_{t_{i-1}}^{t_i} \Phi(t_i, \tau) \mathbf{B}(\tau) \, \mathrm{d}\tau \mathbb{E}[\mathbf{w}(t_i) \mathbf{w}(t_i)^\top] \int_{t_{i-1}}^{t_i} \mathbf{B}^\top(\tau) \Phi^\top(t_i, \tau) \, \mathrm{d}\tau \\ &= \mathbf{\Gamma}_i \mathbf{W}_i \mathbf{\Gamma}_i^\top \end{aligned} \quad (3.46)$$

There is a subtlety with [\(3.46\)](#page-46-0) that can lead to issues: if the time interval associated with the assumption that E[w(ti)w<sup>T</sup> (t<sup>j</sup> )] = W(ti)δij is not the same as the time interval associated with the integral Γ<sup>i</sup> = R ti ti−<sup>1</sup> Φ(t<sup>i</sup> , τ )B(τ ) dτ , then the process noise will not be consistently applied. For example, if the EKF is tuned at a particular time step using a particular noise covariance W, and then for some reason the time step is changed, then one must retune the value of W.

A similar issue occurs when the process noise covariance is chosen without regard for the dynamics, e.g. by setting it equal to a diagonal matrix of user-specified parameters. Whatever careful tuning has been done to choose such parameters will be invalidated by a change in the time step.

3.2.3.1. State Noise Compensation For SNC, as applied to OD, we assume velocity error is an uncorrelated random walk with fixed intensity in orbit-fixed coordinates, such as the RTN or VNB coordinates described above. Thus, assuming RTN coordinates without loss of generality, the process noise spectral density matrix becomes

<span id="page-46-0"></span>
$$\mathbf{Q}(t) = \mathbf{Q}_{rtn} = \begin{bmatrix} q_r & 0 & 0 \\ 0 & q_t & 0 \\ 0 & 0 & q_n \end{bmatrix} \quad (3.47)$$

We assume the transformation from orbit-fixed coordinates to the coordinates used for navigation, which are typically inertial coordinates, is approximately constant over the interval ∆t = ti−ti−1, and ignore the correlation-inducing dependence of this transformation on the estimated position and velocity. This results in

$$\mathbf{B}(t) = \mathbf{B}_{rtn} = \begin{bmatrix} \mathbf{0}_{3 \times 3} \\ \mathbf{M}_{rtn} \end{bmatrix} \quad (3.48)$$

<span id="page-47-0"></span>We also assume that ∆t is small enough that a 1st-order Taylor series truncation (Lear's Model A) is adequate for modeling the STM Φ(t<sup>i</sup> , τ ) in the integrand of [\(3.44\)](#page-45-3), and that Mrtn is constant. With these assumptions, [\(3.44\)](#page-45-3) becomes

$$\mathbf{S}_i = \begin{bmatrix} \tilde{\mathbf{Q}} \frac{\Delta t^3}{3} & \tilde{\mathbf{Q}} \frac{\Delta t^2}{2} \\ \tilde{\mathbf{Q}} \frac{\Delta t^2}{2} & \tilde{\mathbf{Q}} \Delta t \end{bmatrix} \quad (3.49)$$

where <sup>Q</sup>˜ <sup>=</sup> <sup>M</sup>rtnQrtnM<sup>T</sup> rtn. Note that with the SNC model, velocity covariance grows linearly with time, as expected for a random walk model, and hence we should expect the units of √<sup>q</sup> i , i = r, t, n to be meters per second3/2. Reference [[79](#page-173-4)] provides alternative approximations to [\(3.44\)](#page-45-3) for an orbital element state representation, and for relative spacecraft states at both small and large interspacecraft separations.

3.2.3.2. State Noise Compensation for Maneuvers During powered flight, it is often necessary to include additional process noise to accommodate maneuver magnitude and direction errors. One approach is to simply define an additional SNC process noise covariance, with intensities that are sized to the maneuvering errors. While this works fine for modeling maneuver magnitude errors, direction errors may be more accurately modeled by recognizing that a misaligned maneuver vector may be represented by (I<sup>3</sup> −δθ <sup>×</sup>)∆ $\vec{v}$, where δθ <sup>×</sup> represents a skew-symmetric matrix of small angle misalignments, and ∆ $\vec{v}$ is the nominal maneuver vector. Thus, ∆ $\vec{v}$ × nomδθ is the error in the velocity increment due to maneuver direction errors, or if sensed accelerations are being fed-forward into the dynamics, due to IMU misalignments. To model these direction errors as a process noise term, let

$$\mathbf{B}(t) = \begin{bmatrix} \mathbf{0}_{3 \times 3} \\ \Delta \vec{v}_{nom}^\times \end{bmatrix} \quad (3.50)$$

and let q<sup>θ</sup> be the intensity of the maneuver direction noise. Then the SNC-style process noise for accommodating maneuver direction errors becomes

$$\mathbf{S}_i = q_\theta \begin{bmatrix} -(\Delta \vec{v}_{nom}^\times)^2 \frac{\Delta t^3}{3} & -(\Delta \vec{v}_{nom}^\times)^2 \frac{\Delta t^2}{2} \\ -(\Delta \vec{v}_{nom}^\times)^2 \frac{\Delta t^2}{2} & -(\Delta \vec{v}_{nom}^\times)^2 \Delta t \end{bmatrix} \quad (3.51)$$

since ∆ $\vec{v}$ × nom∆ $\vec{v}$ ×<sup>T</sup> nom = −(∆ $\vec{v}$ × nom) 2 . A version of this method was used by the Space Shuttle during powered flight with IMU-sensed accelerations.

3.2.3.3. Dynamic Model Compensation The DMC approach assumes the presence of exponentiallycorrelated acceleration biases, which are included as additional solve-fors in the filter state. As Chapter [6](#page-72-0) and Appendix [A](#page-146-0) discuss, a model for such biases is given by

$$b(t + \Delta t) = e^{-\frac{\Delta t}{\tau}} b(t) + \varpi(t) \quad (3.52)$$

where b(to) ∼ N(0, pbo), and ϖ(t) ∼ N(0, qτ 2 1 − e − 2∆<sup>t</sup> τ ). As Chapter [6](#page-72-0) discusses, τ is a time constant controlling the "smoothness" of the random process, and q is a power spectral density that describes the intensity of the random input. While Chapter [6](#page-72-0) discusses a variety of other bias models that might be used, the exponentially-correlated model has proved to be a best practice for applications in which there are measurements continually available to persistently excite it. Refer to Chapter [6](#page-72-0) for a fuller discussion of the relative merits of various bias modeling approaches.

As above, without loss of generality we can assume the acceleration biases are aligned with the RTN frame, and again assume that ∆t is small enough that a 1st-order Taylor series truncation is adequate for modeling the portion of the STM corresponding to position and velocity errors. With these assumptions, the terms appearing the integrand of [\(3.44\)](#page-45-3) become

$$\mathbf{B}(t) = \mathbf{B}_{rtn} = \begin{bmatrix} \mathbf{0}_{3 \times 3} \\ \mathbf{0}_{3 \times 3} \\ \mathbf{M}_{rtn} \end{bmatrix} \quad (3.5)$$

and

$$\Phi(t + \Delta t, t) = \begin{bmatrix} \mathbf{I}_3 & \Delta t \mathbf{I}_3 & \{ \tau \Delta t - \tau^2(1 - e^{-\Delta t/\tau}) \} \mathbf{I}_3 \\ \mathbf{0}_{3 \times 3} & \mathbf{I}_3 & \tau(1 - e^{-\Delta t/\tau}) \mathbf{I}_3 \\ \mathbf{0}_{3 \times 3} & \mathbf{0}_{3 \times 3} & e^{-\Delta t/\tau} \mathbf{I}_3 \end{bmatrix} \quad (3.54)$$

and the process noise covariance becomes[<sup>3</sup>](#page-48-0)

<span id="page-48-1"></span>
$$\mathbf{S}_i = \begin{bmatrix} \gamma_{pp} \hat{\mathbf{Q}} & \gamma_{pv} \hat{\mathbf{Q}} & \gamma_{pa} \hat{\mathbf{Q}} \\ \gamma_{pv} \hat{\mathbf{Q}} & \gamma_{vv} \hat{\mathbf{Q}} & \gamma_{va} \hat{\mathbf{Q}} \\ \gamma_{pa} \hat{\mathbf{Q}} & \gamma_{va} \hat{\mathbf{Q}} & \end{bmatrix} \quad (3.55)$$

with

$$\gamma_{pp} = \frac{\tau^5}{2} \left\{ \left( 1 - e^{-2\Delta t/\tau} \right) + \frac{2\Delta t}{\tau} \left( 1 - 2e^{-\Delta t/\tau} \right) - 2 \left( \frac{\Delta t}{\tau} \right)^2 + \frac{2}{3} \left( \frac{\Delta t}{\tau} \right)^3 \right\} \quad (3.56)$$

$$\gamma_{pv} = \frac{\tau^4}{2} \left\{ \left( e^{-2\Delta t/\tau} - 1 \right) - 2 \left( e^{-\Delta t/\tau} - 1 \right) + \frac{2\Delta t}{\tau} \left( e^{-\Delta t/\tau} - 1 \right) + \left( \frac{\Delta t}{\tau} \right)^2 \right\} \quad (3.57)$$

$$\gamma_{pa} = \frac{\tau^3}{2} \left\{ \left( 1 - e^{-2\Delta t/\tau} \right) - \frac{2\Delta t}{\tau} e^{-\Delta t/\tau} \right\} \quad (3.58)$$

$$\gamma_{vv} = \frac{\tau^3}{2} \left\{ \left( 1 - e^{-2\Delta t/\tau} \right) - 4 \left( 1 - e^{-\Delta t/\tau} \right) + 2\Delta t/\tau \right\} \quad (3.59)$$

$$\gamma_{va} = \frac{\tau^2}{2} \left(1 - e^{-\Delta t/\tau}\right)^2 \quad (3.60)$$

$$\gamma_{aa} = \frac{\tau}{2} \left( 1 - e^{-2\Delta t/\tau} \right) \quad (3.61)$$

This analytic result for the DMC model first appeared in [[18](#page-170-10)].

3.2.3.4. Explicit Dynamic Biases While the DMC approach allows for quite general estimation of otherwise unmodeled forces on the spacecraft, it is often the case that the domain of application provides context that can narrow the filter designer's focus. For example, it may be the case that the only under-modeled force of appreciable significance on the spacecraft is drag, or perhaps solar radiation pressure, within the context of the application. Alternatively, the application may require much higher resolution models than DMC, which might necessitate estimation of smaller forces with larger uncertainties such as Earth radiation pressure, spacecraft thermal emission, etc., or panel-based modeling of drag and/or solar radiation pressure, etc. In such cases, it is often useful to tailor the DMC approach so that it estimates model-specific biases, such a drag or SRP corrections, rather than modeling three general RTN biases. Similarly, during powered flight, maneuver magnitude and direction errors might be more successfully modeled explicitly.

As an example of an explicit bias, consider estimating a multiplicative correction to the density; a similar approach may be used for drag or solar radiation pressure coefficients. Let t denote geocentric coordinate time. Let R denote a planetary-body-fixed, body-centric system of coordinates, aligned with the central body's rotation axis. Let I denote a body-centric, celestially-referenced system of coordinates, aligned with R at an epoch to. Let $\vec{r}$ represent the position of the center

<span id="page-48-0"></span><sup>3</sup> In [\(3.55\)](#page-48-1), the matrix <sup>Q</sup>˜ has the same form as it does for the SNC method, but with √<sup>q</sup> i , i = r, t, n now representing acceleration intensities, with units of meters per second5/2. Also note that [\(3.55\)](#page-48-1) assumes the same time constant is applicable to all three acceleration channels. While this is usually sufficient, it is straightforward to extend [\(3.55\)](#page-48-1) to accommodate separate time constants for each channel.

of gravity of a satellite, expressed in I. Let $\vec{v}$ represent the satellite's velocity within I. Let $\vec{v}$<sup>r</sup> represent the satellite's velocity within frame R. Assume that $\vec{r}$ evolves with respect to t and I in the vicinity of t<sup>o</sup> according to

$$\frac{z_D^2}{dt^2} \vec{r} = -\frac{\mu}{r^3} \vec{r} - \frac{1}{2} C_D \frac{A}{m} \rho \left( 1 + \frac{\delta\rho}{\rho} \right) v_r \vec{v}_r \quad (3.6.2)$$

where r = ∥$\vec{r}$∥, v<sup>r</sup> = ∥ $\vec{v}$∥, δρ is an atmospheric density disturbance, ρ is the undisturbed atmospheric density, A is the area of the satellite in a plane normal to $\vec{v}$, m is the satellite mass, and C<sup>D</sup> is the satellite's coefficient of drag. Assume that δρ/ρ is a random process that formally evolves as a first-order Gauss-Markov process, similar to a DMC bias:

$$\frac{d}{dt} \left( \frac{\delta\rho}{\rho} \right) = -\frac{1}{\tau} \left( \frac{\delta\rho}{\rho} \right) + w_\rho \quad (3.63)$$

where q<sup>ρ</sup> is the intensity of wρ. Let the state vector be x = [$\vec{r}$ ′ , $\vec{v}$ ′ ,(δρ/ρ)]′ . With these assumptions, the state dynamics and noise input partials are

| $\mathbf{A}(t) =$ | $\mathbf{0}_{3 \times 3}$         | $\mathbf{I}_3$            | $\mathbf{0}_{\vec{3} \times 1}$ | $\mathbf{I}_{3 \times 1}$ | $\mathbf{B}(t) = \begin{bmatrix} \mathbf{0}_{3 \times 1} \\ \mathbf{0}_{3 \times 1} \\ 1 \end{bmatrix}$ | (3.6) |
|-------------------|-----------------------------------|---------------------------|---------------------------------|---------------------------|---------------------------------------------------------------------------------------------------------|-------|
|                   | $\mathbf{G}(t) + \mathbf{D}_r(t)$ | $\mathbf{D}_v(t)$         | $\mathbf{d}(t)$                 |                           |                                                                                                         |       |
|                   | $\mathbf{0}_{1 \times 3}$         | $\mathbf{0}_{1 \times 3}$ | $-1/\tau$                       |                           |                                                                                                         |       |

where G(t) is the gravity gradient matrix, $\vec{d}$(t) = − 1 <sup>2</sup>C<sup>D</sup> A m ρvr $\vec{v}$<sup>r</sup> is the nominal drag acceleration, and D<sup>r</sup> and D<sup>v</sup> are partials of the drag acceleration with respect to position and velocity, respectively[<sup>4</sup>](#page-49-0) .

Using the DMC results from above, with the assumption that the nominal drag acceleration is approximately constant over the integration time, ∆t, the term Φ(t+ ∆t, t)B(t) appearing in the integrand of [\(3.44\)](#page-45-3) becomes

$$\Phi(t + \Delta, t)\mathbf{B}(t) = \begin{bmatrix} \{ \tau\Delta t - \tau^2(1 - e^{-\Delta t/\tau}) \} \vec{\mathbf{d}} \\ \tau(1 - e^{-\Delta t/\tau}) \vec{\mathbf{d}} \\ e^{-\Delta t/\tau} \end{bmatrix} \quad (3.65)$$

and the process noise for a proportional density bias becomes

$$\mathbf{S}_i = q_P \begin{bmatrix} \gamma_{pp} \vec{d} \vec{d}' & \gamma_{pv} \vec{d} \vec{d}' & \gamma_{pa} \vec{d} \\ \gamma_{pv} \vec{d} \vec{d}' & \gamma_{vv} \vec{d} \vec{d}' & \gamma_{va} \vec{d} \\ \gamma_{pa} \vec{d}' & \gamma_{va} \vec{d}' & \gamma_{aa} \end{bmatrix} \quad (3.66)$$

3.2.3.5. Episodic Dynamic Biases It has sometimes been found to be the case, particularly for crewed missions, that episodic spacecraft activities can produce un-modeled accelerations. In the early days of manned spaceflight, events such as vents, momentum unloads, thruster-based attitude control firings, etc. that may perturb a spacecraft's trajectory were not well modeled, and came to be described as FLAK, which was supposed to be an acronym for (un)-Fortunate Lack of Acceleration Knowledge.

<span id="page-49-0"></span><sup>4</sup>The sensitivity D<sup>r</sup> contains terms that are roughly proportional to the drag acceleration magnitude divided by the atmospheric scale height, and to the product of drag acceleration magnitude and the ratio of planetary rotation rate to speed relative to the atmosphere. For nearly all spacecraft, these terms will be many orders magnitude smaller than the gravity gradient, which is proportional to the gravity acceleration divided by the radius. So D<sup>r</sup> can usually be neglected. For reference, D<sup>v</sup> = − <sup>2</sup>C<sup>D</sup> A <sup>m</sup> ρvr( $\vec{u}$ <sup>v</sup>r $\vec{u}$ ′ <sup>v</sup><sup>r</sup> + I3), and D<sup>r</sup> = d/Rs( $\vec{u}$ <sup>r</sup> $\vec{u}$ ′ vr ) − Dv $\vec{ω}$ <sup>×</sup>, where $\vec{ω}$ <sup>×</sup> is the skew-symmetric "cross-product" matrix formed from the central body's rotation rate vector, and the notation $\vec{u}$ (·) indicates the unit vector of its subscript.

If the mean time between such activities can be characterized, along with the expected intensity of the acceleration, a compound Poisson-Gaussian process noise model may be effective. Conveniently, it turns out that the covariance of a linear system driven by a train of Gaussiandistributed impulses whose arrival times follow a Poisson distribution is the same as the covariance of the same system driven by a white noise input process, except for the scaling of the process noise covariance by the Poisson process rate parameter [[32](#page-171-4)].

To understand this result, consider a linear model of the error in a spacecraft trajectory as follows

$$\dot{\mathbf{x}}(t) = \mathbf{A}(t)\mathbf{x}(t) + \mathbf{B}(t)\mathbf{u}(t) \quad (3.67)$$

where x represents the deviation of the actual position/velocity state from its estimated or nominal value, and u represents the FLAK acceleration bias. Then, if we make use of inertial coordinates,

$$\mathbf{A}(t) = \begin{bmatrix} \mathbf{0} & \mathbf{1} \\ \mathbf{G}(t) & \mathbf{0} \end{bmatrix}, \quad \mathbf{B}(t) = \begin{bmatrix} \mathbf{0} \\ \mathbf{M}(t) \end{bmatrix} \quad (3.68)$$

where G represents the gravity gradient matrix, and M is the direction cosine matrix rotating the supposed body-fixed FLAK into the inertial frame. There is no general solution to this differential equation, but over short time intervals, we can assume that

$$\mathbf{x}(t_k) = \Phi(t_k, t_{k-1})\mathbf{x}_{k-1} + \int_{t_{k-1}}^{t_k} \Phi(t_k, \tau)\mathbf{B}(\tau)\mathbf{u}(\tau) \, d\tau \quad (3.69)$$

where

$$\Phi(t_k, t_{k-1}) = \mathbf{I} + \mathbf{A}(t_k)(t_k - t_{k-1}) \quad (3.70)$$

We assume the input is a sequence of velocity impulses of (random) length nk,

$$\mathbf{u}(t) = \sum_{i=1}^{n_k} \mathbf{u}_i \delta(t - t_i) \quad (3.71)$$

with tk−<sup>1</sup> < t<sup>i</sup> < tk. The delta functions annihilate the integral and our model becomes (with ∆t<sup>i</sup> = t<sup>k</sup> − ti):

$$\mathbf{x}(t_k) = \Phi(t_k, t_{k-1})\mathbf{x}_{k-1} + \sum_{i=1}^{n_k} \begin{bmatrix} \vec{\kappa}_i \Delta t_i \\ \vec{\kappa}_i \end{bmatrix} \|\mathbf{u}_i\| \quad (3.72)$$

where $\vec{x}$ <sup>i</sup> is the unit inertial direction vector for the FLAK event. Note that the input response is in some sense fundamentally an increment to the entire state vector at each tk; we can however compute an equivalent zero-order hold acceleration by dividing the velocity increment by the time step t<sup>k</sup> − tk−1.

Since we assume each impulse is zero-mean and Gaussian, the input response has zero mean. To find a tractable form for the covariance, assume that the direction of the FLAK event is constant over each interval t<sup>k</sup> − tk−1. This assumption assures that the impulses are identically distributed over each sampling interval. Then, the process noise covariance is given by Reference [32](#page-171-4):

$$\mathbf{S}(t_k) = q\lambda \int_{t_{k-1}}^{t_k} \left[ \frac{\vec{\kappa}'_k(t_k - \tau)}{\vec{\kappa}'_k} \right] [\vec{\kappa}'_k(t_k - \tau), \vec{\kappa}'_k] \, d\tau \quad (3.73)$$

where q is the variance of the discrete Gaussian velocity impulses and λ is the rate parameter of the Poisson process. Carrying out the integration results in

$$\mathbf{S}(t_k) = q\lambda \begin{bmatrix} \vec{\kappa}_k \vec{\kappa}'_k \Delta t^3/3 & \vec{\kappa}_k \vec{\kappa}'_k \Delta t^2/2 \\ \vec{\kappa}_k \vec{\kappa}'_k \Delta t^2/2 & \vec{\kappa}_k \vec{\kappa}'_k \Delta t \end{bmatrix} \quad (3.7)$$

3.2.3.6. Computational Considerations The primary computational issues that can affect covariance propagation may be broadly characterized as underflow and overflow. Underflow can occur especially because many of the process noise parameters described above may often have values that approach computational truncation limits, which can lead to non-positive-definite process noise covariances. Overflow can similarly occur when truncation limits are approached by very large covariance values such as can occur with long propagation times. Because the orbital dynamics are at best marginally stable, even propagating without process noise can result in differences of many orders of magnitude between largest and smallest eigenvalues. This problem will be exacerbated if process noise is present, since all of the process noise models described above introduce unbounded position covariance error growth[<sup>5</sup>](#page-51-0) .

Simple tricks like enforcing symmetry, or adding a small positive diagonal matrix, will not always ensure positive eigenvalues in such cases. A better solution is to maintain the covariance in factorized form, for example as Chapter [8](#page-94-0) describes. In lieu of a fully factorized filtering approach, process noise factors may be computed from their factorizations. Chapter [6](#page-72-0) shows a few examples of Cholesky factorizations that may be employed in this fashion.

3.2.4. Tuning the Covariance Propagation Since even the best practices this Chapter has discussed are at best approximations, it is inevitable that EKF designers must perform some artful tuning of the free parameters to achieve acceptable results. Furthermore, computational limitations of flight computers often lead to the need for compromises in modeling fidelity. What one generally hopes to accomplish via tuning of the covariance propagation is that any approximations or compromises the EKF has had to endure to be implementable have not impaired its covariance's accuracy too much. In particular, one would like to compute an idealized "truth" covariance matrix, based on the best-available models and data, and adjust the EKF's "formal" covariance via the tuning process to yield some semblance of a match.

In some cases, it is possible to compute the true covariance. In particular, if we are studying a linear system, and the random components have zero-mean Gaussian distributions, then the mean errors will be zero, and we can use linear covariance analysis [[27](#page-171-5), [58](#page-172-2), [60](#page-172-3)] to compute the covariances. It is often possible to approximate the performance for a nonlinear system with this technique by linearization. This is often a first step in early conceptual design studies.

One may divide tuning of the covariance propagation into those activities a designer performs (1) during the detailed development of a system, prior to the collection of any flight data, and (2) during the commissioning of a new system or an existing system in a new application, when flight data are available. For pre-flight detailed design studies, one generally simulates the system, so one has access to truth data. One can also run the mission simulation many times, generating an ensemble of parallel results, performing a Monte Carlo analysis. During and after the actual mission, we never have access to truth data. At best, we can reconstruct the trajectory after the fact using more sophisticated processing and additional data that were not available in real-time. For near real-time analysis, we can compare current state estimates to predictions from previous epochs. These predictions can come from either mission products generated in real-time at a past epoch, or past reconstructions of the trajectory. In all cases, the best we have are differences between estimates, not errors from the truth. There are several empirical approximations to the true covariance that one might use in these situations.

<span id="page-51-0"></span><sup>5</sup>Reference [11](#page-170-11) proposes an approximate "solution" to this problem via a Floquet analysis of a modified set of covariance propagation dynamics that include artificially-introduced damping.

3.2.4.1. Empirical Approximations of the True Covariance Let e<sup>j</sup> (ti)represent the random error vector at time t<sup>i</sup> for case j from a Monte Carlo simulation, and {e(ti)} be the set of all cases at time t<sup>i</sup> . Assume the total number of cases is K, and the total number of time samples is N.

Time Series Expectation: We can take statistics of the error realizations across time for each case, e<sup>j</sup> (ti), to get the time series expectations for each case:

$$\hat{\mathbf{E}}_t(\mathbf{e}_j) = \frac{1}{N} \sum_{i=1}^N e_j(t_i) \quad (3.75)$$

$$\hat{\mathbf{E}}_t(\mathbf{e}_j\mathbf{e}_j^\top) = \frac{1}{N-1} \sum_{i=1}^N \mathbf{e}_j(t_i) \mathbf{e}_j^\top(t_i) \quad (3.76)$$

If the data are stationary[<sup>6</sup>](#page-52-0) , the time series statistics are usually an adequate approximation, if we have considered a long enough time span. In some systems, described as ergodic, a long time series is in some sense equivalent to a large number of shorter Monte Carlo cases.

Ensemble Expectation: We can take statistics of the error realizations over all the cases at each time sample to get the ensemble expectations:

$$\hat{\mathbf{E}}_e\{\mathbf{e}(t_i)\} = \frac{1}{K} \sum_{j=1}^K \mathbf{e}_j(t_i) \quad (3.77)$$

$$\hat{\mathbf{E}}_e\{\mathbf{e}(t_i)\mathbf{e}^\top(t_i)\} = \frac{1}{K-1} \sum_{j=1}^K \mathbf{e}_j(t_i)\mathbf{e}_j^\top(t_i) \quad (3.78)$$

The ensemble statistics will generally give the best indication of performance if the data are non-stationary, so long as we use an adequate number of Monte Carlo cases.

Since there is nothing analogous to an ensemble of Monte Carlo cases for flight data, we cannot use ensemble statistics as defined above. Let d represent the random difference vector between the quantity of interest and its comparison value. We can apply time series statistics, but as the mission evolves, the span of the time series continually extends, so we have to decide which subsets of the entire mission span to use, e.g. the time series extending back over the entire history of the mission, extending back only over some shorter interval, etc., and also how frequently to recompute the time series statistics, e.g. continuously, once per day, etc. There are some other approximations to the expectation that we might use here.

Sliding Window Time Series Expectation: We can take statistics of the difference realizations, d(ti), across a sliding window extending ∆t into the past from each observation, for each case, to get the ∆t-sliding window time series expectations:

$$\hat{\mathbf{E}}_{t,\Delta t}(\mathbf{d}) = \frac{1}{\Delta n} \sum_{i=0}^{\Delta n-1} \mathbf{d}(t_{N-i}) \quad (3.79)$$

$$\hat{\mathbf{E}}_{t,\Delta t}(\mathbf{d}\mathbf{d}^T) = \frac{1}{\Delta n - 1} \sum_{i=0}^{\Delta n-1} \mathbf{d}(t_{N-i}) \mathbf{d}(t_{N-i})^T \quad (3.80)$$

where ∆n is the number of time samples in the window ∆t.

<span id="page-52-0"></span><sup>6</sup> Stationary data are those for which the statistics do not change when the time origin shifts.

Period-Folding Expectation: If the data are periodic, we can break up the data into K spans of one period in duration each, and shift the time origin of each span so that the data are "folded" into the same, one-period-long interval. We can then take ensemble statistics over times at the same phase angle, tϕi, within each period.

$$\hat{E}_f\{\mathbf{d}(t_{\phi i})\} = \frac{1}{K} \sum_{j=1}^K \mathbf{d}_j(t_{\phi i}) \quad (3.81)$$

$$\hat{\mathbf{E}}_f\{\mathbf{d}(t_{\phi i})\mathbf{d}(t_{\phi i})^T\} = \frac{1}{K-1} \sum_{j=1}^K \mathbf{d}_j(t_{\phi i})\mathbf{d}_j^T(t_{\phi i}) \quad (3.8)$$

It is often useful to fold the data into bins of equal mean anomaly. This is especially useful for orbits with notable eccentricity, since it ensures that a roughly equal number of time points will be present in each bin.

Sliding Window Period-Folding Expectation: Period-folding can obviously be applied over a sliding window as well, with each window extending n periods into the past.

$$\hat{E}_{f,n}\{\mathbf{d}(t_{\phi i})\} = \frac{1}{n} \sum_{j=0}^{n-1} \mathbf{d}_{K-j}(t_{\phi i}) \quad (3.83)$$

$$\hat{\mathbf{E}}_{f,n}\{\mathbf{d}(t_{\phi i})\mathbf{d}(t_{\phi i})^\top\} = \frac{1}{n-1} \sum_{j=0}^{n-1} \mathbf{d}_{K-j}(t_{\phi i})\mathbf{d}_{K-j}^\top(t_{\phi i}) \quad (3.84)$$

This is especially useful for identifying secular trends in periodic data sets.

3.2.4.2. Tuning for Along-track Error Growth As described above, the position error component along the orbit track will dominate covariance propagation error, and so the most important step in tuning the covariance propagation is to ensure that this component grows no faster or slower than it should based on the truncations and approximations that the EKF design has employed. One may use any of the analytical or empirical methods described above to estimate the "true" covariance. For example, for preflight analysis, one may generate a time series or ensemble of time series of differences between states propagated using the formal models the filter employs, and a best available "truth" model of the system. One can then compare the appropriate empirical covariance computed from this data set to the filter's formal covariance, and adjust the process noise intensities until a reasonable match occurs. For flight data analysis, one may similarly difference across overlaps between predictive and definitive states, and compare these empirical covariances of these differences to the sum of the predictive and definitive formal covariances from the filter.

If one uses the SNC method, the primary "knob" for tuning the alongtrack covariance growth rate is the corresponding alongtrack component of the process noise intensity q<sup>T</sup> or q<sup>V</sup> , depending on whether RTN or VNB components are used, respectively. Essentially, an impulse along the velocity vector, or change in speed, causes a change in SMA, corresponding to a change in period, and hence a secular growth in position error along the orbit, as discussed at the beginning of this Chapter. This mechanism is especially transparent for near-circular orbits, and some simple analysis yields a good starting point. One may find a fuller exposition of the following result in Reference [28](#page-171-6).

<span id="page-54-1"></span>For near-circular orbits, the position components of the integrand in [\(3.44\)](#page-45-3) become, in RTN coordinates,

| $\Phi_{rv}(\Delta t)$ | $\begin{bmatrix} q_R & 0 & 0 \\ 0 & q_T & 0 \\ 0 & 0 & q_N \end{bmatrix}$ | $\Phi_{rv}^T(\Delta t)$ | (3.85) |
|-----------------------|---------------------------------------------------------------------------|-------------------------|--------|
|-----------------------|---------------------------------------------------------------------------|-------------------------|--------|

where Φrv(∆t) is given, per Hill, Clohessy, and Wiltshire, by

| $\Phi_{rv}(\Delta t) = \begin{bmatrix} \sin(n\Delta t)/n & 2(1 - \cos(n\Delta t))/n & 0 \\ 2(\cos(n\Delta t) - 1)/n & 4\sin(n\Delta t)/n - 3\Delta t & 0 \\ 0 & 0 & \sin(n\Delta t)/n \end{bmatrix}$ | (3.86) |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|

Retaining only secular terms and carrying out the integral, the along-track component of the process noise covariance becomes

| $S_T(\Delta t) \approx 3\Delta t^3 q_T$ | (3.87) |
|-----------------------------------------|--------|
|-----------------------------------------|--------|

an approximation which holds for ∆t > Tp. Thus, one may use an empirical covariance of the along-track error after one orbit period, such as σˆ 2 δs <sup>=</sup> Eˆ <sup>f</sup> {δs<sup>2</sup>}, to derive a starting point from which to tune q<sup>T</sup> , as

$$q_T = \frac{\hat{\sigma}_{\delta s}^2}{3T_p^3} \quad (3.88)$$

#### 3.3. Covariance Measurement Update

<span id="page-54-0"></span>This section discusses methods for implementing the covariance measurement update. Some of the most important of these best practices are related to factorization methods and underweighting, which are topics of enough significance to warrant their own chapters.

3.3.1. "Stable Form" of non-Joseph Covariance Update As Chapter [1](#page-24-0) pointed out, only for the optimal gain and true covariance does the Joseph form of the covariance measurement update, [\(1.41\)](#page-29-1),

$$\mathbf{P}_i^+ = (\mathbf{I} - \mathbf{K}_i\mathbf{H}_i) \mathbf{P}_i^+ (\mathbf{I} - \mathbf{K}_i\mathbf{H}_i)^T + \mathbf{K}_i\mathbf{R}_i\mathbf{K}_i^T \quad (3.89)$$

reduce to [\(1.33\)](#page-28-3),

$$\mathbf{P}_i^+ = \mathbf{P}_i^- - \mathbf{K}_i \mathbf{H}_i \mathbf{P}_i^- \quad (3.90)$$

While this assertion is strictly true, the cancellations that produce the above results will still occur so long as the EKF algorithm is internally consistent with truncating and approximating its various terms. The resulting "covariance" will not accurately represent E e + i (e + i ) T |<sup>Y</sup><sup>i</sup> , but the fact that these truncations and approximations have produced a suboptimal gain will, in themselves, provide no computational issues. In effect, the resulting suboptimal gain remains "optimal" with respect to the internally consistent set of approximations and truncations internal to the filter.

However, even if the gain is optimal, the stability of the non-Joseph form depends on the order of multiplication, as Schmidt points out [[75](#page-173-5)]. He describes a "stable form" of the non-Joseph update, given by Algorithm [3.1,](#page-55-0) which was successfully used by the Space Shuttle. Algorithm [3.1](#page-55-0) processes each jth scalar element of the measurement vector one at a time, using only the jth row of the measurement partials matrix, h<sup>j</sup> , and the (j, j) diagonal element of the measurement noise covariance, r<sup>j</sup> , assuming R<sup>i</sup> is a diagonal matrix. In comparison with P + <sup>i</sup> = (I − KiHi)P − i , use of Algorithm [3.1](#page-55-0) also reduces the computational burden from O(n 3 ) to O(n <sup>2</sup>/2), where n is the state dimension.

Although Algorithm [3.1](#page-55-0) does not show the state update, it may also be sequentially updated as part of the iteration. However, the order in which the scalar measurements update the state can affect the outcome, if the measurement partials are computed one row at a time, corresponding

## <span id="page-55-0"></span>Algorithm 3.1 "Stable form" of the non-Joseph Covariance Measurement Update

P<sup>1</sup> = P i for each scalar measurement j = 1 through k do

−

$$\mathbf{h}_j = j^{\text{th}} \text{ row of } \mathbf{H}_i$$

$$r_j = (j, j)$$
 element of  $\mathbf{R}_i$ 

$$\mathbf{b}_j = \mathbf{P}_j \mathbf{h}_j^\top$$

$$\mathbf{k}_j = \mathbf{b}_j / (\mathbf{h}_j \mathbf{b}_j + r_j)$$

$$\mathbf{P}_j \leftarrow \mathbf{P}_j - \mathbf{k}_j \mathbf{b}_j^T$$

end for

P <sup>i</sup> = P<sup>k</sup> Only the non-redundant (upper or lower triangular) portions of the covariance should be updated, and then the other redundant elements set equal to the ones that have been computed.

+

with each scalar update. This may produce undesirable or even unstable outcomes. Chapter [4](#page-58-0) will discuss such issues further.

Despite the extensive and successful flight heritage of Algorithm [3.1,](#page-55-0) it cannot guarantee numerical stability and positive definiteness of the covariance. Chapter [8](#page-94-0) describes a recommended best practice for the covariance update, the UD-factorization, which makes checking for positive definiteness transparently easy.

3.3.2. Use of Consider States It may often be the case that unobservable states are present in the system being estimated. Most commonly, such states will be parameters whose values are unknown or uncertain. Inclusion of such parameters as solve-for states in the EKF is a not a recommended practice. However, if the EKF completely ignores the uncertainty that such parameters introduce, its covariance can become overly optimistic, a condition sometimes known as "filter smugness." One approach to addressing this problem was introduced by Schmidt [[75](#page-173-5)], originally in the context of reducing the computational burden that the EKF imposed on flight computers of the 1960's. Schmidt's idea is essentially for the EKF to maintain a covariance containing all of the states whose uncertainties are significant enough to affect filter performance, but only to update a subset of those states. The states which are not updated in this framework are typically known as "consider" parameters, and such a filter has been called a "consider filter" or a "Schmidt-Kalman" filter. Although most commonly the state space is simply partitioned by selecting states as either solve-for or consider states, Reference [58](#page-172-2) points out that partitioning using linear combinations of the full state space is also possible.

Following Reference [58](#page-172-2), suppose the filter produces estimates for a subset of n<sup>s</sup> solve-for states, out of the full state of size n. The filter does not estimate the remaining n<sup>c</sup> = n − n<sup>s</sup> consider states. Denote the true solve-for vector by s(t), and the true consider vector by c(t). Assume that these are linear combinations of the true states, according to the following:

<span id="page-55-1"></span>

| $\mathbf{s}(t) = \mathbf{S}(t)\mathbf{x}(t)$ | and | $\mathbf{c}(t) = \mathbf{C}(t)\mathbf{x}(t)$ | (3.91) |
|----------------------------------------------|-----|----------------------------------------------|--------|
|----------------------------------------------|-----|----------------------------------------------|--------|

where the n<sup>s</sup> × n matrix S(t) and the n<sup>c</sup> × n matrix C(t) are such that the matrix

$$\mathbf{M} = \begin{bmatrix} \mathbf{S} \\ \mathbf{C} \end{bmatrix} \quad (3.92)$$

is non-singular. The inverse of M is partitioned into an n × n<sup>s</sup> matrix S˜ and an n × n<sup>c</sup> matrix C˜ :

$$\mathbf{M}^{-1} = \begin{bmatrix} \tilde{\mathbf{S}} & \tilde{\mathbf{C}} \end{bmatrix}. \quad (3.93)$$

The properties of the matrix inverse then lead immediately to the identities

| $\mathbf{S}\tilde{\mathbf{S}} = \mathbf{I}_{n_s}$ | $\mathbf{C}\tilde{\mathbf{C}} = \mathbf{I}_{n_c}$ | $\mathbf{S}\tilde{\mathbf{C}} = \mathbf{0}_{n_s \times n_c}$ | $\mathbf{C}\tilde{\mathbf{S}} = \mathbf{0}_{n_c \times n_s}$ | (3.94) |
|---------------------------------------------------|---------------------------------------------------|--------------------------------------------------------------|--------------------------------------------------------------|--------|
|                                                   |                                                   |                                                              |                                                              |        |

| $\mathbf{S}\tilde{\mathbf{S}} = \mathbf{I}_{n_s}$ | $\mathbf{C}\tilde{\mathbf{C}} = \mathbf{I}_{n_c}$ | $\mathbf{S}\tilde{\mathbf{C}} = \mathbf{0}_{n_s \times n_c}$ | $\mathbf{C}\tilde{\mathbf{S}} = \mathbf{0}_{n_c \times n_s}$ | (3.9) |
|---------------------------------------------------|---------------------------------------------------|--------------------------------------------------------------|--------------------------------------------------------------|-------|
|---------------------------------------------------|---------------------------------------------------|--------------------------------------------------------------|--------------------------------------------------------------|-------|

and

<span id="page-56-1"></span> $\tilde{\mathbf{S}} + \tilde{\mathbf{C}}\mathbf{C} = \mathbf{I}_n.$  (3.95)

$$\tilde{\mathbf{S}} + \tilde{\mathbf{C}}\mathbf{C} = \mathbf{I}_n. \quad (3.95)$$

In the usual case that the elements of the solve-for and consider vectors are merely selected and possibly permuted components of the state vector, the matrix M is an orthogonal permutation matrix. In this case, and in any case for which M is orthogonal, the matrices S˜ and C˜ are just the transposes of S and C, respectively, which makes inversion of M unnecessary and simplifies many of the following equations.

It follows from Eqs. [3.91](#page-55-1) and [3.95](#page-56-1) that

$$\mathbf{x}(t) = \hat{\mathbf{S}}(t)\mathbf{s}(t) + \hat{\mathbf{C}}(t)\mathbf{c}(t). \quad (3.96)$$

$$\mathbf{x}(t) = \hat{\mathbf{S}}(t)\mathbf{s}(t) + \tilde{\mathbf{C}}(t)\mathbf{c}(t). \quad (3.96)$$

Relations similar to Eq. [3.91](#page-55-1) give the estimated solve-for vector ˆs(t) and the assumed consider vector ˆc(t) in terms of the estimated state ˆx(t). Thus, errors in the solve-for and consider states are given by

 $\mathbf{e}_s(t) = \mathbf{s}(t) - \hat{\mathbf{s}}(t) = \mathbf{S}(t)\mathbf{e}(t)$  (3.97)

 $\mathbf{e}_c(t) = \mathbf{c}(t) - \hat{\mathbf{c}}(t) = \mathbf{C}(t)\mathbf{e}(t)$  (3.98)

and the true error may be written in terms of the solve-for and consider errors by

$$\mathbf{e}(t) = \tilde{\mathbf{S}}(t)\mathbf{e}_s(t) + \tilde{\mathbf{C}}(t)\mathbf{e}_c(t). \quad (3.99)$$

$$\mathbf{e}(t) = \tilde{\mathbf{S}}(t)\mathbf{e}_s(t) + \tilde{\mathbf{C}}(t)\mathbf{e}_c(t). \quad (3.99)$$

In terms of this notation, the EKF update has the form

ˆs + <sup>i</sup> = ˆs − <sup>i</sup> + Kir

− i

$$\mathbf{r}_i^- = \mathbf{y}_i - \mathbf{h}(\hat{\mathbf{x}}_i^-) = \mathbf{H}_i \mathbf{e}_i^- + \mathbf{v}_i, \quad (3.101)$$

(3.100)

where

$$\mathbf{r}_i = \mathbf{y}_i - \mathbf{h}(\hat{\mathbf{x}}_i^-) = \mathbf{H}_i \mathbf{e}_i^- + \mathbf{v}_i, \quad (3.101)$$

and the subscript i is a shorthand for the time argument t<sup>i</sup> . The usual EKF will not contain the full covariance, but only its solve-for part

| $\mathbf{P}_{ss}(t) = \mathbf{E}[\mathbf{e}_s(t)\mathbf{e}_s^T(t)]$ | (3.102) |
|---------------------------------------------------------------------|---------|
|---------------------------------------------------------------------|---------|

$$\mathbf{P}_{ss}(t) = \mathbf{E}[\mathbf{e}_s(t)\mathbf{e}_s^T(t)] \quad (3.102)$$

By contrast, the Schmidt-Kalman filter will use the full covariance, P(t). In the usual case, the Kalman gain is given by

$$\mathbf{K}_i = \mathbf{P}_{ssi} \mathbf{H}_i^\top [\mathbf{H}_{si} \mathbf{P}_{ssi} \mathbf{H}_i^\top + \mathbf{R}_i]^{-1} \quad (3.103)$$

$$\mathbf{K}_i = \mathbf{P}_{si}^{-1} \mathbf{H}_i^T [\mathbf{H}_s \mathbf{P}_{si}^{-1} \mathbf{H}_s^T + \mathbf{R}_i]^{-1} \quad (3.103)$$

where

| $\mathbf{H}_{si} = \mathbf{H}_i \tilde{\mathbf{S}}_i$ | (3.104) |
|-------------------------------------------------------|---------|
|-------------------------------------------------------|---------|

In the Schmidt-Kalman case,

$$\mathbf{K}_i = \mathbf{S}_i \mathbf{P}_i \mathbf{H}_i^\top [\mathbf{H}_i \mathbf{P}_i \mathbf{H}_{si}^\top + \mathbf{R}_i]^{-1} \quad (3.105)$$

$$\mathbf{K}_i = \mathbf{S}_i \mathbf{P}_i^{-1} \mathbf{H}_i^{-1} [\mathbf{H}_i \mathbf{P}_i^{-1} \mathbf{H}_{si}^{-1} + \mathbf{R}_i]^{-1} \quad (3.105)$$

Thus, the Schmidt-Kalman gain matrix is computed from the full covariance, but only applies measurement innovations to the solve-for states.

## 3.4. Sigma-Point Methods

<span id="page-56-0"></span>Before concluding this Chapter, it is worth noting that a promising method for propagating and updating the covariance that is coming into greater use and acceptance within the navigation community is the use of sigma-point methods, also known as "unscented" transforms. A subsequent chapter covering Advanced Topics will cover these topics in a section on sigma-point filtering.

![](_page_57_Picture_1.jpeg)

## Processing Measurements

<span id="page-58-2"></span><span id="page-58-0"></span>Contributed by Christopher N. D'Souza and J. Russell Carpenter

This chapter will discuss how to handle real-world measurement processing issues. In particular, being able to handle measurements that aren't synchronous is of paramount importance to running filters in a real-time environment. As well, the performance of navigation filters which have nonlinear measurement models are susceptible to divergence depending on the order of processing of measurements which occur at the same epoch. Therefore, a technique which provides invariance to measurement processing is detailed. A technique for processing correlated measurements is presented, and brief comments on filter cascading and processing of inertial data are offered.

## 4.1. Measurement Latency

<span id="page-58-1"></span>In general, the measurement time tags are not going to be equal to the current filter epoch time, tk. To state it another way, the measurements do not come in at the current filter time. Rather, they may be latent by up to p seconds. Thus, a situation will arise where the filter has propagated its state and covariance to time t = t<sup>k</sup> from time t = tk−1, and is subsequently given a measurement to be filtered (denoted by subscript m) that corresponds to the time t = tm, where

t<sup>m</sup> ≤ t<sup>k</sup> (4.1)

If ∆t = t<sup>m</sup> − t<sup>k</sup> is not insignificant, the time difference between the measurement and the filter state and covariance will need to be accounted for during filtering in order to accurately process the measurement. This can be done in much the same way a batch filter operates (see pages 196- 197 of Tapley [[81](#page-173-3)]). If the measurement at time t = t<sup>m</sup> is denoted as ym, the nominal filter state at that time is given by X ∗ <sup>m</sup> ≡ X ∗ (tm) (∗ denotes the nominal), and the measurement model is denoted as h<sup>m</sup> (Xm, tm), then one can expand the measurement model to first order about the nominal filter state to get

$$h_m(\mathbf{X}_m, t_m) = h_m(\mathbf{X}_m^*, t_m) + \mathbf{H}_m \mathbf{x}_m + \nu_m \quad (4.2)$$

where x<sup>m</sup> = X<sup>m</sup> − X ∗ <sup>m</sup> and H<sup>m</sup> is defined as

$$\mathbf{H}_m \triangleq \left( \frac{\partial h_m(\mathbf{X}, t_m)}{\partial \mathbf{X}} \right)_{\mathbf{X}=\mathbf{X}_m^*} \quad (4.3)$$

The perturbed state at time t<sup>m</sup> can be written in terms of the state at time t<sup>k</sup> as follows

$$\mathbf{x}_m = \boldsymbol{\Phi}(t_m, t_k) \mathbf{x}_k + \boldsymbol{\Gamma}_m \mathbf{w}_m \quad (4.4)$$

so we can compute the measurement as

| $h_m(\mathbf{X}_m, t_m) = h_m(\mathbf{X}_m^*, t_m) + \mathbf{H}_m \Phi(t_m, t_k) \mathbf{x}_k + \mathbf{H}_m \boldsymbol{\Gamma}_m \mathbf{w}_m + \nu_m$ | (4.5) |
|----------------------------------------------------------------------------------------------------------------------------------------------------------|-------|
|----------------------------------------------------------------------------------------------------------------------------------------------------------|-------|

where the measurement noise has the characteristics E[νm] = 0 and E ν 2 m = Rm, the state process noise from t = t<sup>m</sup> to t = t<sup>k</sup> has the characteristics E[wm] = 0 and E[wmw<sup>T</sup> <sup>m</sup>] = Qm, and the state deviation is given by

$$\mathbf{x}_k = \delta \mathbf{X}_k = \mathbf{X}_k - \mathbf{X}_k^* \quad (4.6)$$

(Note that the effect of the state process noise would be to increase the measurement noise variance. However, because the process noise term is very small over time periods of a few seconds, it can safely be neglected for the remainder of this analysis.)

Upon taking the conditional expectation of the measurement equation and rearranging, the scalar residual of the measurement is given by

| $y_m - \tilde{\mathbf{H}}_m \hat{\mathbf{x}}_t(-) = \mathbf{Y}_m - h_m(\mathbf{X}_{*m}^t, t_m) - \mathbf{H}_m \Phi(t_m, t_k) \hat{\mathbf{x}}_t(-)$ | (4.7) |
|-----------------------------------------------------------------------------------------------------------------------------------------------------|-------|
|-----------------------------------------------------------------------------------------------------------------------------------------------------|-------|

where ˆ· denotes an estimated value,

| $y_m$                   | $\mathbf{Y}_m - h_m(\mathbf{X}_m^*, t_m)$ |       |
|-------------------------|-------------------------------------------|-------|
| $\hat{\mathbf{x}}_k(-)$ | $\hat{\mathbf{X}}_k(-) - \mathbf{X}_k^*$  | (4.8) |

The measurement partials that are used in the update, which map the measurement to the state at time t = tk, are given by

<span id="page-59-1"></span>
$$\tilde{\mathbf{H}}_m = \mathbf{H}_m \boldsymbol{\Phi}(t_m, t_k) \quad (4.9)$$

Eq. [4.9](#page-59-1) was derived by noting that

| $\mathbf{H}_m \hat{\mathbf{x}}_m = \mathbf{H}_m \Phi(t_m, t_k) \hat{\mathbf{x}}_k$<br>$= \tilde{\mathbf{H}}_m \hat{\mathbf{x}}_k$ | (4.10) |
|-----------------------------------------------------------------------------------------------------------------------------------|--------|
|-----------------------------------------------------------------------------------------------------------------------------------|--------|

From the above discussion, it is evident that the unknown quantities needed to update the state at time t = t<sup>k</sup> with a measurement from time t = t<sup>m</sup> are the nominal state at the measurement time, X ∗ <sup>m</sup>, and the state transition matrix relating the two times, Φ(tm, tk). Given those values, h<sup>m</sup> (X ∗ <sup>m</sup>, tm) and <sup>H</sup>e <sup>m</sup> can be calculated.

Thus the nominal state at the measurement time is calculated by back-propagating the filter state from time t<sup>k</sup> to time tm. The same thing is done to calculate the required state transition matrix. The same propagation algorithms used in forward propagation ought to be utilized for the back-propagation, with the exception that the smaller time step allows for a 1 st-order approximation of the matrix exponential used to update the state transition matrix.

## 4.2. Invariance to the Order of Measurement Processing

<span id="page-59-0"></span>It has long been known that the performance of an EKF is dependent on the order in which one processes measurements. This is of particular import in the case when there is powerful measurement coupled with a large a priori error. The state (and covariance) update will be large, very likely out of the linear range. Subsequent measurements which are processed may well be outside the residual edit thresholds, and hence will be rejected. In order to remedy this, we employ a hybrid Linear/Extended Kalman Filter measurement update. Recall that in an Extended Kalman Filter, the state is updated / relinearized / rectified after each measurement is processed, regardless of whether the measurements occur at the same time. Hence, the solution is highly dependent on the order in which the measurements are processed. This is not a desirable situation in which to be.

We obviate this difficulty simply by not updating the state until all the measurements at a given time are processed. We accumulate the state updates in state deviations x, using Algorithm [4.1.](#page-60-1) This algorithm makes use of the fact that, in the absence of process noise, a batch/least squares algorithm is mathematically equivalent to a linear Kalman Filter [[33](#page-171-7)]. Algorithm [4.1](#page-60-1) is <span id="page-60-2"></span>a recommended best practice. Algorithm [4.1](#page-60-1) may readily be combined with the residual mapping

## <span id="page-60-1"></span>Algorithm 4.1 Measurement Update Invariant to Order of Processing

for each (scalar) measurement j = 1 through k do

$$\mathbf{y}_j = \mathbf{Y}_j - h_j(\mathbf{X}_m^*, t_m)$$

∗

$$\mathbf{K}_j = \mathbf{P}_j \mathbf{H}_j^\top (\mathbf{H}_j \mathbf{P}_j \mathbf{H}_j^\top + R_j)^{-1}$$

$$\hat{\mathbf{x}}_j \leftarrow \hat{\mathbf{x}}_j + \mathbf{K}_j (y_j - \mathbf{H}_j \hat{\mathbf{x}}_j)$$

$$\mathbf{P}_j \leftarrow (\mathbf{I} - \mathbf{K}_j \mathbf{H}_j) \mathbf{P}_j (\mathbf{I} - \mathbf{K}_j \mathbf{H}_j)^T + \mathbf{K}_j R_j \mathbf{K}_j^T$$

end for  

$$\mathbf{X}_m \leftarrow \mathbf{X}_m^* + \hat{\mathbf{x}}_j$$

approach described above when the measurements are asynchronous. Algorithm [4.1](#page-60-1) may also be readily combined with Algorithm [3.1,](#page-55-0) for cases in which the preferred factorized covariance methods are precluded.

## 4.3. Processing Vector Measurements

<span id="page-60-0"></span>If the UDU factorization is used, the measurements are usually processed as scalars. If the vector measurements are correlated, one option is to assume they are uncorrelated and ignore the correlations between the measurements.

However, there is a better alternative. Given the measurement equation (Y<sup>j</sup> = H<sup>j</sup> (X<sup>j</sup> , t<sup>j</sup> ) + ν<sup>j</sup> ) with measurement error covariance matrix, R<sup>i</sup> , first decompose the matrix with a Cholesky factorization as

| $\mathbf{R}_i$ | $=$ | $\mathbf{E}[\boldsymbol{\nu}_j \boldsymbol{\nu}_j^\top] = \mathbf{R}_i^{1/2} \mathbf{R}_i^{1/2}$ | (4.11) |
|----------------|-----|--------------------------------------------------------------------------------------------------|--------|
|----------------|-----|--------------------------------------------------------------------------------------------------|--------|

and premultiply the measurement equation by R −1/2 i to yield

$$\mathbf{Y}_j = \tilde{\mathbf{H}}_j(\mathbf{X}_j, t_j) + \tilde{\boldsymbol{\nu}}_j \quad (4.12)$$

with

| $\mathbf{\tilde{Y}}_j = \mathbf{R}_i^{-1/2} \mathbf{Y}_j$ | (4.13) |
|-----------------------------------------------------------|--------|
|-----------------------------------------------------------|--------|

$$\mathbf{\tilde{Y}}_j = \mathbf{R}_j^{-1/2} \mathbf{Y}_j \quad (4.13)$$

| $\bar{\mathbf{H}}_j(\mathbf{X}_j, t_j)$ | $=$ | $\mathbf{R}_i^{-1/2} \mathbf{H}_j(\mathbf{X}_j, t_j)$ | (4.14) |
|-----------------------------------------|-----|-------------------------------------------------------|--------|
|-----------------------------------------|-----|-------------------------------------------------------|--------|

$$\tilde{\nu}_j = \mathbf{R}_i^{-1/2} \boldsymbol{\nu}_j \quad (4.15)$$

so that E[ν˜jν˜<sup>j</sup> ] = I. Thus, the new measurement equation has errors which are now decorrelated.

Alternatively, one can decompose the m × m measurement error covariance matrix with a UDU decomposition as R<sup>i</sup> = UR<sup>i</sup> DRiU<sup>T</sup> R<sup>i</sup> so that using a similar reasoning, we premultiply the measurement equation by U−<sup>1</sup> R<sup>i</sup> so that in this case

$$\mathbf{\hat{Y}}_j = \mathbf{U}_{R_j}^{-1} \mathbf{Y}_j \quad (4.16)$$

$$\bar{\mathbf{H}}_j(\mathbf{X}_j, t_j) = \mathbf{U}_{R_j}^{-1} \mathbf{H}_j(\mathbf{X}_j, t_j) \quad (4.17)$$

$$\tilde{\nu}_j = \mathbf{U}_{R_i}^{-1} \boldsymbol{\nu}_j \quad (4.18)$$

so that E[ν˜jν˜<sup>j</sup> ] = DR<sup>i</sup> where DR<sup>i</sup> is a diagonal matrix and, as in the case of the Cholesky decomposition, the new measurement model has decorrelated measurement errors.

## 4.4. Filter Cascades

## Contributed by James McCabe

<span id="page-61-3"></span><span id="page-61-0"></span>It is often tempting to ingest the output of one navigation filter, an "upstream" filter, into another filter, a "downstream" filter. This is commonly proposed for systems equipped with sensors that furnish, in one sense or another, a post-processed data source, such as a Global Navigation Satellite System Position-Velocity-Time output, a derived measurement produced via an image processing algorithm such as seen in terrain relative navigation, or a pose solution from a lidar utilizing model matching. However, one of the few key, and often overlooked, assumptions critical to ensuring a Kalman filter's performance is that the measurement noise is white, i.e. uncorrelated in time. Many of these post-processed data sources employ online iterative procedures, many times themselves being Kalman filters, to produce the output. In this case, the measurement source has errors that are guaranteed to be time-correlated, and, if a practitioner is not careful, the system inherits a dangerous upstream filter/downstream filter relationship that can cause serious issues during runtime. If the downstream filter was provided or had a priori knowledge of the correlation this would not be an issue, but it is almost always impossible to directly quantify it. As such, the downstream Kalman filter is assuming a white noise signature, yet the input errors are time-correlated, and the resulting downstream estimates are flawed and, in practice, promote filter divergence (or, at minimum, a biased result). It is important to emphasize that, while this is often dismissed as a mere academic detail, cascades drastically increase overall navigation system risk.

This inadvertent relationship between assumed and real-world statistics is easy to accidentally happen into, especially considering that sensor vendors are manufacturing ever smarter and smarter sensors that employ "in the box" post-processing of their data to produce a convenient output for their customers. However, these outputs are often inconsistent with the Kalman filter's white noise assumption, even if the noise statistics provided on a specifications sheet are accurate. As such, a navigation practitioner is cautioned against presuming a post-processed output from any "navigation in a box" solution provided by a vendor can be naively ingested into a Kalman filter. Note that there are methods to aid in combating the negative effects of time-correlated measurement errors, often through the use of additional exponentially correlated random variable (ECRV) states in the filter to accommodate the bias-like effects of the time correlations, but the variances and time constants of these ECRVs become design variables that must be selected during tuning pre-flight, adding design complexity.

It is worth noting that there are cases where filter cascades have been utilized successfully despite their flaws, such as carrier-smoothing via pre-filtering of noisy high-rate data or direct ingestion of quaternion output from star tracker systems,[<sup>1</sup>](#page-61-2) but a navigator must be extremely careful in understanding the error signature in these signals to guarantee that the time history of the measurement errors are approximately white or appropriately treated within the filter formulation to account for time correlation. The success of these systems typically relies upon the upstream process producing a result that is, on the whole, fairly unbiased such that the signal appears to be corrupted by an approximately-white, zero-mean noise process.

## 4.5. Use of Data from Inertial Sensors

<span id="page-61-1"></span>Inertial measurement units (IMUs), consisting of gyros and accelerometers, sense rotational and translational accelerations. While in principle these high-rate data could be processed as observations in the navigation filter, it is often sufficient instead to use this data in model replacement mode, which Brown and Hwang [[7](#page-170-3)] compare to complementary filtering. In this approach, the

<span id="page-61-2"></span><sup>1</sup>Note that some, but not all, quaternion outputs from such systems do not exhibit time-correlated errors, but this must be treated on a case-by-base basis.

sensed accelerations are fed forward as deterministic inputs to the navigation filter's dynamics model. Biases affecting the IMU data usually must be estimated by the filter. Thresholding the IMU accelerations is also usually necessary to avoid the introduction of unfiltered IMU noise into the filter state propagation. Chapter [7](#page-84-0) describes best practices for modeling the structures associated with IMU data.

![](_page_63_Picture_1.jpeg)

## CHAPTER 5

## <span id="page-64-0"></span>Measurement Underweighting

Contributed by Renato Zanetti

## 5.1. Introduction

<span id="page-64-1"></span>Given an m-dimensional random measurement y which is somehow related to an unknown, n-dimensional random vector x the family of affine estimators of x from y is

$$\hat{x} = a + \mathbf{K} \mathbf{y} \qquad (5.1)$$

$$\hat{x} = a + \mathbf{K}\mathbf{y} \quad (5.1)$$

where a ∈ ℜ<sup>n</sup> and K ∈ ℜ<sup>n</sup>×<sup>m</sup>. The optimal, in a Minimum Mean Square Error sense, affine estimator has

| $\mathbf{K} = \mathbf{P}_{xy} \mathbf{P}_{yy}^{-1}$ | (5.2) |
|-----------------------------------------------------|-------|
|-----------------------------------------------------|-------|

$$\mathbf{K} = \mathbf{P}_{xy} \mathbf{P}_{yy}^{-1} \quad (5.2)$$

| $a = E[\mathbf{x}] - \mathbf{K}$ | $E[\mathbf{y}]$ | (5.3) |
|----------------------------------|-----------------|-------|
|----------------------------------|-----------------|-------|

| $a = E[\mathbf{x}] - K E[\mathbf{y}]$ | (5.3) |
|---------------------------------------|-------|
|---------------------------------------|-------|

where

$$\mathbf{P}_{xy} = \mathbb{E} \left[ \left( \mathbf{x} - \mathbb{E}[\mathbf{x}] \right) \left( \mathbf{y} - \mathbb{E}[\mathbf{y}] \right)^T \right] \quad (5.4)$$

$$\mathbf{P}_{yy} = \mathbb{E} \left[ \left( \mathbf{y} - \mathbf{E}[\mathbf{y}] \right) \left( \mathbf{y} - \mathbf{E}[\mathbf{y}] \right)^T \right] \quad (5.5)$$

In the presence of nonlinear measurements of the state,

$$\mathbf{y} = \mathbf{h}(\mathbf{x}) + \mathbf{v}$$
 (5.6)

(where v is zero-mean measurement noise) the extended Kalman filter (EKF) [[27](#page-171-5)] approximates all moments of y by linearization of the measurement function centered on the mean of x. This methodology has proven very effective and produces very satisfactory results in most cases. Approaches other than the EKF exist, for example the Unscented Kalman Filter [[40](#page-171-8)] approximates the same quantities via stochastic linearization using a deterministic set of Sigma Points. High order truncations of the Taylor series are also possible. Underweighting [[46](#page-171-9),[50](#page-172-1)] is an ad-hoc technique to compensating for nonlinearities in the measurement models that are neglected by the EKF and successfully flew on the Space Shuttle, on Orion Exploration Flight Test 1, and the Artemis I mission.

The commonly implemented method for the underweighting of measurements for human space navigation was introduced by Lear [[48](#page-171-10)] for the Space Shuttle navigation system. In 1966 Denham and Pines showed the possible inadequacy of the linearization approximation when the effect of measurement nonlinearity is comparable to the measurement error [[19](#page-170-12)]. To compensate for the nonlinearity Denham and Pines proposed to increase the measurement noise covariance by a constant amount. In the early seventies, in anticipation of Shuttle flights, Lear and others developed relationships which accounted for the second-order effects in the measurements [[50](#page-172-1)].

It was noted that in situations involving large state errors and very precise measurements, application of the standard extended Kalman filter mechanization leads to conditions in which the state estimation error covariance decreases more rapidly than the actual state errors. Consequently the extended Kalman filter begins to ignore new measurements even when the measurement residual is relatively large. Underweighting was introduced to slow down the convergence of the state estimation error covariance thereby addressing the situation in which the error covariance becomes overly optimistic with respect to the actual state errors. The original work on the application of second-order correction terms led to the determination of the underweighting method by trialand-error [[48](#page-171-10)].

More recently, studies on the effects of nonlinearity in sensor fusion problems with application to relative navigation have produced a so-called "bump-up" factor. [[23](#page-171-11), [54](#page-172-4), [67](#page-172-5), [69](#page-172-6)]. While Ferguson [[23](#page-171-11)] seems to initiate the use of the bump-up factor, the problem of mitigating filter divergence was more fully studied by Plinval [[69](#page-172-6)] and subsequently by Mandic [[54](#page-172-4)]. Mandic generalized Plinval's bump-up factor to allow flexibility and notes that the value selected influences the steady-state convergence of the filter. In essence, it was found that a larger factor keeps the filter from converging to the level that a lower factor would permit. This finding prompted Mandic to propose a two-step algorithm in which the bump-up factor is applied for a certain number of measurements only, upon which the factor was completely turned off. Finally, Perea, et al. [[67](#page-172-5)] summarize the findings of the previous works and introduce several ways of computing the applied factor. In all cases, the bump-up factor amounts in application to the underweighting factor introduced in Lear [[48](#page-171-10)]. Save for the two-step procedure of Mandic, the bump-up factor is allowed to persistently affect the Kalman gain which directly influences the obtainable steady-state covariance. Effectively, the ability to remove the underweighting factor autonomously and under some convergence condition was not introduced.

The work of Lear [[12](#page-170-13),[49](#page-171-12)] is not well known as it is mostly only documented in internal NASA memos [[48](#page-171-10),[50](#page-172-1)]. Kriegsman and Tau [[46](#page-171-9)] mention underweighting in their 1975 Shuttle navigation paper without a detailed explanation of the technique.

## 5.2. Nonlinear Effects and the Need for Underweighting

<span id="page-65-0"></span>We review briefly the three state estimate update approaches assuming a linear time-varying measurement model leading to the classical Kalman filter, a nonlinear measurement model with first-order linearization approximations leading the widely used extended Kalman filter, and a nonlinear model with second-order approximations leading to the second-order extended Kalman filter.

5.2.1. Linear Measurement Model and the Classical Kalman Filter Update Let's briefly recap the linear Kalman filter. The measurement model is

$$y_i = \mathbf{H}_i \mathbf{x}_i + \mathbf{v}_i, \quad (5.7)$$

where y<sup>i</sup> ∈ <sup>R</sup> <sup>m</sup> are the m measurements at each time t<sup>i</sup> , x<sup>i</sup> ∈ <sup>R</sup> n is the n-dimensional state vector, H<sup>i</sup> ∈ <sup>R</sup> m×n is the known measurement mapping matrix, v<sup>i</sup> ∈ <sup>R</sup> <sup>m</sup> is modeled as a zeromean white-noise sequence with E[v<sup>i</sup> ] = 0, ∀ k and E h viv T j i = Riδkj where R<sup>i</sup> > 0 ∀ k and δkj = 1 when k = j and δkj = 0 when k ̸= j. The Kalman filter state update algorithm provides an optimal blending of the a priori estimate xˆ − i and the measurement y<sup>i</sup> at time t<sup>i</sup> to obtain the a posteriori state estimate xˆ + i via

<span id="page-65-1"></span>
$$\hat{x}_i^+ = \hat{x}_i^- + \mathbf{K}_i [\mathbf{y}_i - \mathbf{H}_i \hat{x}_i^-] , \quad (5.8)$$

Defining the a priori estimation error as e − <sup>i</sup> = x<sup>i</sup> − xˆ − i and the a posteriori estimation error as e + <sup>i</sup> = x<sup>i</sup> − xˆ + i and assuming these errors to be zero mean, the associated symmetric, positive definite a priori and a posteriori estimation error covariances are P − <sup>i</sup> = Eh e − i e − i T i and P + <sup>i</sup> = E h e + i e + i T i , respectively. Using Eq. [\(5.8\)](#page-65-1) and the definitions of the state estimation errors and error covariances, we obtain the a posteriori state estimation error covariance via the well-known Joseph formula

<span id="page-66-1"></span>
$$\mathbf{P}_i^+ = [\mathbf{I} - \mathbf{K}_i\mathbf{H}_i]\mathbf{P}_i^+ [\mathbf{I} - \mathbf{K}_i\mathbf{H}_i]^\top + \mathbf{K}_i\mathbf{R}_i\mathbf{K}_i^\top, \quad (5.9)$$

which is valid for any K<sup>i</sup> . If the gain K<sup>i</sup> is chosen so as to minimize the trace of the a posteriori estimation error, we call that gain the Kalman gain which is given by

<span id="page-66-0"></span>
$$\mathbf{K}_i = \mathbf{P}_i \mathbf{H}_i^\top \left[ \mathbf{H}_i \mathbf{P}_i^{-1} \mathbf{H}_i^\top + \mathbf{R}_i \right]^{-1}. \quad (5.10)$$

$$\mathbf{K}_i = \mathbf{P}_i \mathbf{H}_i^\top [\mathbf{H}_i \mathbf{P}_i^\top \mathbf{H}_i^\top + \mathbf{R}_i]^{-1}. \quad (5.10)$$

The trace of the state estimation error covariance is generally not a norm but is equivalent to the nuclear norm (the matrix Shatten 1-norm) for symmetric semi-positive matrices. If the gain given in Eq. [\(5.10\)](#page-66-0) is applied to the state estimation error covariance of Eq. [\(5.9\)](#page-66-1), then the update equation can be rewritten after some manipulation as

<span id="page-66-3"></span>
$$\mathbf{P}_i^+ = [\mathbf{I} - \mathbf{K}\mathbf{H}_i] \mathbf{P}_i^-, \quad (5.11)$$

or equivalently,

<span id="page-66-4"></span>
$$\mathbf{P}_i^+ = \mathbf{P}_i^- - \mathbf{K}_i[\mathbf{H}_i\mathbf{P}_i^-\mathbf{H}_i^\top + \mathbf{R}_i]\mathbf{K}_i^\top. \quad (5.12)$$

$$\mathbf{P}_i^+ = \mathbf{P}_i^- - \mathbf{K}_i[\mathbf{H}_i\mathbf{P}_i^-\mathbf{H}_i^\top + \mathbf{R}_i]\mathbf{K}_i^\top. \quad (5.12)$$

Under the assumptions of the Kalman filter development (linear, time-varying measurement model with a zero-mean white-noise sequence corrupting the measurements, unbiased a priori estimation errors, known dynamics and measurement models, etc.), the state estimate and state estimation error covariance updates are optimal and we expect no filter divergence issues. The estimation error covariance will remain positive definite for all t<sup>i</sup> and the estimation error covariance will be consistent with the true errors. In practice, the measurements are usually nonlinear functions of the state, leading to a variety of engineering solutions that must be carefully designed to ensure acceptable state estimation performance. Underweighting is one such method to improve the performance of the extended Kalman filter in practical settings.

5.2.2. The Nonlinear Measurement Model and the Extended Kalman Filter Update In the nonlinear setting, consider the measurement model given by

$$y_i = h(x_i, t_i) + v_i, \quad (5.1)$$

where h(xi) ∈ <sup>R</sup> <sup>m</sup> is a vector-valued differentiable nonlinear function of the state vector x<sup>i</sup> ∈ <sup>R</sup> n . The idea behind the extended Kalman filter (EKF) is to utilize Taylor series approximations to obtain linearized models in such a fashion that the EKF state update algorithm has the same general form as the Kalman filter.

<span id="page-66-5"></span>
$$y_i \simeq h(\hat{x}_i, t_i) + \mathbf{H}_i \mathbf{e}_i^- + \mathbf{v}_i, \quad (5.14)$$

where

<span id="page-66-2"></span>
$$\mathbf{H}_i \triangleq \left[ \frac{\partial \mathbf{h}(\mathbf{x}_i, t_i)}{\partial \mathbf{x}_i} \Big|_{\mathbf{x}_i = \hat{\mathbf{x}}_i^-} \right]. \quad (5.15)$$

Since the estimation error is (approximately) zero mean and the measurement noise is zero mean, it follows that

$$\mathbf{E}[\mathbf{y}] \simeq \mathbf{h}(\hat{\mathbf{x}}_i^-, t_i), \quad (5.16)$$

where all expectations are conditioned on past measurements and we find that the state estimate update is given by [[27](#page-171-5)]

<span id="page-67-0"></span>
$$\hat{x}_i^+ = \hat{x}_i^- + \mathbf{K}_i[\mathbf{y}_i - \mathbf{h}(\hat{x}_i^-)]. \quad (5.17)$$

Similarly, the measurement residual is given by

$$r_i = y_i - h(\hat{x}_i^-) \simeq H_i e_i^- + v_i, \quad (5.18)$$

Computing the measurement residual covariance E[rir T i ] yields

<span id="page-67-3"></span>
$$\mathbf{W}_i = \mathbf{H}_i \mathbf{P}_i^{-1} \mathbf{H}_i^{\top} + \mathbf{R}_i. \quad (5.19)$$

The state estimation error covariance and Kalman gain are the same as in Eqs. [\(5.9\)](#page-66-1) and [\(5.10\)](#page-66-0), respectively, with H<sup>i</sup> given as in Eq. [\(5.15\)](#page-66-2). The state estimation error covariances in the forms shown in Eqs. [\(5.11\)](#page-66-3) and [\(5.12\)](#page-66-4) also hold in the nonlinear setting with H<sup>i</sup> as in Eq. [\(5.15\)](#page-66-2).

From Eqs. [\(5.12\)](#page-66-4) and [\(5.17\)](#page-67-0), it is seen that reducing the Kalman gain leads to a smaller update in both the state estimation error covariance and the state estimate, respectively. Reducing the gain and hence the update is the essence of underweighting and the need for this adjustment is illuminated in the following discussion.

Adopting the viewpoint that the state estimation error covariance matrix represents the level of uncertainty in the state estimate, we expect that when we process a measurement (adding new information) the uncertainty would decrease (or at least, not increase). This is, in fact, the case and can be seen in Eq. [\(5.12\)](#page-66-4). Under the assumption that the symmetric matrices P − <sup>i</sup> > 0 and R<sup>i</sup> > 0, it follows that

$$\mathbf{K}[\mathbf{H}_i\mathbf{P}_i^{-1}\mathbf{H}_i^T + \mathbf{R}_i]\mathbf{K}_i^T \geq 0, \quad (5.20)$$

and we can find a number α<sup>i</sup> ≥ 0 at each time t<sup>i</sup> such that

$$\mathbf{P}_i^- - \mathbf{P}_i^+ \geq \alpha_i I, \quad (5.21)$$

which shows that the P − <sup>i</sup> − P + i is non-negative definite. The same argument can be made from the viewpoint of comparing the trace (or the matrix norm) of the a posteriori and a priori state estimation error covariances. As each new measurement is processed by the EKF, we expect the uncertainty in the estimation error to decrease. The question is, does the a posteriori uncertainty as computed by the EKF represent the actual uncertainty, or in other words, is the state estimation error covariance matrix always consistent with the actual state errors? In the nonlinear setting when there is a large a priori uncertainty in the state estimate and a very accurate measurement, it can happen that the state estimation error covariance reduction at the measurement update is too large. Underweighting is a method to address this situation by limiting the magnitude of the state estimation error covariance update with the goal of retaining consistency of the filter covariance and the actual state estimation error through situations of high nonlinearity of the measurements.

Pre- and post-multiplying the a posteriori state estimation error covariance in Eq. [\(5.12\)](#page-66-4) by H<sup>i</sup> and H<sup>T</sup> i , respectively, yields (after some manipulation)

<span id="page-67-1"></span>
$$\mathbf{H}_i\mathbf{P}_i^\top\mathbf{H}_i^\top = \mathbf{H}_i\mathbf{P}_i^\top\mathbf{H}_i^\top(\mathbf{H}_i\mathbf{P}_i^\top\mathbf{H}_i^\top + \mathbf{R}_i)^{-1}\mathbf{R}_i. \quad (5.22)$$

In Eq. [\(5.22\)](#page-67-1), we see that if HiP − <sup>i</sup> H<sup>T</sup> <sup>i</sup> ≫ R<sup>i</sup> then it follows that

<span id="page-67-2"></span>
$$\mathbf{H}_i \mathbf{P}_i^\dagger \mathbf{H}_i^\top \simeq \mathbf{R}_i. \quad (5.23)$$

The result in Eq. [\(5.23\)](#page-67-2) is of fundamental importance and is the motivation behind underweighting. What this equation express is the fact that when the a priori estimated state uncertainty HiP − <sup>i</sup> H<sup>T</sup> i is much larger than the measurement error covariance R<sup>i</sup> , the Kalman filter largely neglects the prior information and relies heavily on the measurement. Therefore the a posteriori estimated state uncertainty HiP + <sup>i</sup> H<sup>T</sup> i is approximately equal to R<sup>i</sup> .

<span id="page-68-2"></span>5.2.3. The Nonlinear Measurement Model and the 2nd-Order Kalman Filter Update Whereas Eq. [\(5.14\)](#page-66-5) truncates the Taylor series expansion of the nonlinear measurement function to first order, carrying it to second order we obtain

$$\mathbf{y}_i \simeq \mathbf{h}(\hat{\mathbf{x}}_i^-, t_i) + \mathbf{H}_i \mathbf{e}_i^- + \sum_{k=1}^m \left( \frac{\partial^2 \mathbf{h}(\mathbf{x}_i, t_i)}{\partial \mathbf{x}_i \partial x_i(k)} \Big|_{\mathbf{x}_i=\hat{\mathbf{x}}_i^-} e_i(k) \mathbf{e}_i \right) + \mathbf{v}_i \quad (5.24)$$

$$= h(\hat{x}_i, t_i) + \mathbf{H}_i \ e_i^- + b_i + v_i, \quad (5.25)$$

where ei(k) and xi(k) are the k-th elements of vectors e<sup>i</sup> and x<sup>i</sup> , respectively. The expected value of the measurement now includes contributions from the second order terms, denoted as ˆb<sup>i</sup>

$$E[\mathbf{y}_i] \simeq \mathbf{h}(\hat{\mathbf{x}}_i^-, t_i) + \hat{\mathbf{b}}_i \quad (5.26)$$

Define

$$\mathbf{H}_{i,k}^{\top} \triangleq \left[ \frac{\partial^2 h_i(\mathbf{x}_i)}{\partial \mathbf{x}_i \partial \mathbf{x}_i^{\top}} \middle|_{\mathbf{x}_i = \hat{\mathbf{x}}_i^{-}} \right],$$

where hi(xi) is the k-th component of h(xi). Then the k-th component of b<sup>i</sup> is given by

$$b_{i,k} = \frac{1}{2} (\mathbf{e}_i)^\top \mathbf{H}_{i,k}^\top \mathbf{e}_i = \frac{1}{2} \text{tr}(\mathbf{H}_{i,k}^\top \mathbf{e}_i^- (\mathbf{e}_i^-)^\top). \quad (5.27)$$

where tr denotes the trace. To keep the filter unbiased, the k-th component of ˆb<sup>i</sup> is given by

$$\hat{b}_{i,k} = 1/2 \operatorname{tr}(\mathbf{H}_{i,k}^\top \mathbf{P}_i^-).$$

The measurement residual is

<span id="page-68-0"></span>
$$r_i = y_i - E[y_i] \quad (5.28)$$

Expanding Eq. [\(5.28\)](#page-68-0), the k-th component of the residual is obtained to be

$$r_{i,k} = \mathbf{h}_{i,k}^\top \mathbf{e}_i + 1/2 \operatorname{tr}(\mathbf{H}_i^\top(\mathbf{t}_i)\mathbf{e}_i(\mathbf{e}_i)^\top) - 1/2 \operatorname{tr}(\mathbf{H}_i^\top(\mathbf{t}_i)\mathbf{P}_i) + v_{i,k}, \quad (5.29)$$

where h T i,k is the ik-th row of the measurement Jacobian and vi,k is the k-th component of the measurement noise v<sup>i</sup> . Computing the measurement residual covariance E[rir T i ] yields

<span id="page-68-1"></span>

| $\mathbf{W}_i = \mathbf{H}_i \mathbf{P}_i^{-1} \mathbf{H}_i^T + \mathbf{B}_i + \mathbf{R}_i$ , | (5.30) |
|------------------------------------------------------------------------------------------------|--------|
|------------------------------------------------------------------------------------------------|--------|

where matrix B<sup>i</sup> is the contribution of the second order effects and its (kj)-th component is given by

| $B_{i,kj} \triangleq 1/4 E[\text{tr}(\mathbf{H}_i^\top(t_i) \mathbf{e}_i^\top(\mathbf{e}_i^\top)^\top) \text{tr}(\mathbf{H}_i^\top(t_i) \mathbf{e}_i^\top(\mathbf{e}_i^\top)^\top)]$ $- 1/4 \text{tr}(\mathbf{H}_i^\top(t_i) \mathbf{P}_i^\top) \text{tr}(\mathbf{H}_i^\top(t_i) \mathbf{P}_i^\top).$ |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

where it was assumed that the third order central moments are all zeros. Assuming the prior estimation error is distributed as a zero-mean gaussian distribution with covariance P − i , the ijth component of B<sup>i</sup> is given by

$$B_{i,kj} = \frac{1}{2} \text{tr}(\mathbf{H}_{i,k}^{\text{T}} \mathbf{P}_i^{-1} \mathbf{H}_{i,j}^{\text{T}} \mathbf{P}_i^{-1}). \quad (5.31)$$

Comparing the measurement residual covariance for the EKF in Eq. [\(5.19\)](#page-67-3) with the measurement residual covariance for the second-order filter in Eq. [\(5.30\)](#page-68-1), we see that when the nonlinearities lead to significant second-order terms which should not be neglected, then the EKF tends to provide residual covariance estimates that are not consistent with the actual errors. Typically, we address this by tuning the EKF using R<sup>i</sup> as a parameter to be tweaked. If the contribution of the a priori estimation error HiP − <sup>i</sup> H<sup>T</sup> i to the residuals covariance is much larger than the contribution of the measurement error R<sup>i</sup> , the EKF algorithm will produce HiP + <sup>i</sup> H<sup>T</sup> <sup>i</sup> ≃ R<sup>i</sup> . If B<sup>i</sup> is of comparable magnitude to R<sup>i</sup> then the actual covariance of the posterior measurement estimate should be HiP + <sup>i</sup> H<sup>T</sup> <sup>i</sup> ≃ R<sup>i</sup> + B<sup>i</sup> . Therefore, a large underestimation of the a posteriori covariance can occur in the presence of nonlinearities when the estimated measurement error covariance is much larger than the measurement error covariance.

The covariance update is given by the modified Gaussian second order filter update [[38](#page-171-0)]

$$\mathbf{P}_i^* = \mathbf{P}_i^- - \mathbf{H}_i \mathbf{P}_i^- \mathbf{W}_i^{-1} (\mathbf{H}_i \mathbf{P}_i^-)^T, \quad (5.32)$$

where the residual covariance W<sup>i</sup> is given by Eq. [\(5.30\)](#page-68-1).

#### 5.3. Underweighting Measurements

<span id="page-69-0"></span>In the prior section we saw that when "large" values of HiP − <sup>i</sup> H<sup>T</sup> i exist (or similarly, large values of P − i ), and possibly "small" values of R<sup>i</sup> , the EKF is at risk underestimating the posterior estimation error covariance matrix. We must repeat that this can only happen in the presence of "large" nonlinearities. The larger P − i is, the larger the domain of possible values of the true state x, hence the more likely the higher order terms of the expansion of the nonlinear measurement functions will become relevant. If a measurement function is largely non-linear, but the prior estimate is very precise, the EKF algorithm and linearization are likely sufficiently accurate since:

- (1) The posterior measurement will rely heavily on the prior and rely less on the measurement
- (2) Since the error is small, while the Hessian matrix might be relatively large, the actual contributions of the second order effects is likely to remain small

Underweighting is the process of modifying the residual covariance to reduce the update and compensate for the second-order effects described above. In this section, we describe three common methods for performing underweighting with the EKF algorithm.

5.3.1. Additive Compensation Method The most straightforward underweighting scheme is to add an underweighting factor U<sup>i</sup> as

$$\mathbf{W}_i = \mathbf{H}_i \mathbf{P}_i^{-1} \mathbf{H}_i^{-1} + \mathbf{R}_i + \mathbf{U}_i. \quad (5.33)$$

$$W_i = \mathbf{H}_i \mathbf{P}_i^\top \mathbf{H}_i^\top + \mathbf{R}_i + \mathbf{U}_i. \quad (5.33)$$

With the Kalman gain given by

$$\mathbf{K}_i = \mathbf{P}_i^{-1} \mathbf{H}_i^\top \mathbf{W}_i^{-1}, \quad (5.34)$$

$$K_i = P_i^- H_i^\top W_i^{-1}, \quad (5.34)$$

we see that the symmetric, positive-definite underweighting factor U<sup>i</sup> decreases the Kalman gain, thereby reducing the state estimate and state estimation error covariance updates. One choice is to select U<sup>i</sup> = B<sup>i</sup> , which is the contribution to the covariance assuming the prior distribution of the estimation error is Gaussian. The advantage of this choice is its theoretical foundation based on analyzing the second-order terms of the Taylor series expansions. The disadvantages include higher computational costs to calculate the second-order partials and the reliance on the assumption that the estimation errors possess Gaussian distributions. In practical applications, the matrix U<sup>i</sup> needs to be tuned appropriately for acceptable overall performance of the EKF. The process of tuning a positive definite matrix is less obvious than tuning a single scalar parameter.

5.3.2. Scaling the Measurement Error Covariance Another possible underweighting approach is to scale the measurement noise by choosing

| $\mathbf{U}_i = \gamma \mathbf{R}_i$ , | (5.35) |
|----------------------------------------|--------|
|----------------------------------------|--------|

 $U_i = \gamma \mathbf{R}_i$ , (5.35)

where γ > 0 is a scalar parameter selected in the design process. This approach has been successfully used [[39](#page-171-13)]; however, it is not recommended from both a conceptual and a practical reason. Recalling that the underweighting is necessary because of neglecting the second-order terms of the Taylor series expansion of the measurement function, it seems more natural to express the underweighting as a function of the a priori estimation error covariance. Choosing a constant coefficient to scale R<sup>i</sup> seems less practical and will probably lead to a more complicated tuning procedure. As long as the measurement noise is white the contributions of the second order effects are not a function of the measurement error covariance, therefore making them a fraction or a multiple of the measurement noise (an unrelated quantity) is likely not the best choice.

5.3.3. Lear's Method Lear's choice was to make U<sup>i</sup> a percentage of the a priori estimation error covariance via [[48](#page-171-10)]

$$\mathbf{U}_i = \beta \mathbf{H}_i \mathbf{P}_i^{-1} \mathbf{H}_i^{\top}. \quad (5.36)$$

Let <sup>P</sup>¯ <sup>−</sup> <sup>i</sup> ∈ <sup>R</sup> <sup>3</sup>×<sup>3</sup> be the partition of the state estimation error covariance associated with the position error states. The Space Shuttle employs underweighting when q tr <sup>P</sup>¯ <sup>−</sup> <sup>i</sup> > α. The positive scalars α and β are design parameters. For the Space Shuttle, α is selected to be 1000 meters and <sup>β</sup> is selected to be <sup>0</sup>.<sup>2</sup> [[48](#page-171-10)]. When q tr <sup>P</sup>¯ <sup>−</sup> <sup>i</sup> > 1000 m, then β = 0.2, otherwise β = 0.

Orion employs a slightly different approach, underweighting is applied when HiP − <sup>i</sup> H<sup>T</sup> <sup>i</sup> > α, where α is a tunable flight software parameter.

This choice of underweighting scheme is sound since it assumes that the higher order effects are a fraction (or a multiple) of the first order effects, which are a related quantity. There may exist some unusual nonlinear measurement cases where the measurement Jacobian evaluates to zero, or a small value, while at the same time the Hessian does not vanish; these cases are not appropriately handled by underweighting.

### 5.4. Pre-Flight Tuning Aids

<span id="page-70-0"></span>In this section, a technique to aid the tuning of the underweighting coefficient during pre-flight analysis is presented. When the nonlinearities lead to second-order terms that cannot be neglected, we find that the measurement residual covariance is more accurately given by (see Eq. [\(5.30\)](#page-68-1))

<span id="page-70-1"></span>
$$\mathbf{W}_i = \mathbf{H}_i \mathbf{P}_i^{-1} \mathbf{H}_i^{-1} + \mathbf{R}_i + \mathbf{B}_i. \quad (5.37)$$

Following Lear's approach to underweighting, we have that

<span id="page-70-2"></span>
$$\mathbf{W}_{U,i} = (1 + \beta)\mathbf{H}_i\mathbf{P}_i^-\mathbf{H}_i^\top + \mathbf{R}_i. \quad (5.38)$$

Comparing Eqs. [\(5.37\)](#page-70-1) and [\(5.38\)](#page-70-2), the desired effect is to have

| $\text{tr } \mathbf{W}_{U,i} \geq \text{tr } \mathbf{W}_i$ | (5.39) |
|------------------------------------------------------------|--------|
|------------------------------------------------------------|--------|

This leads us to choose the underweighting coefficient β<sup>i</sup> such that

| $\beta \geq \text{tr } \mathbf{B}_i / \text{tr } \mathbf{H}_i \mathbf{P}_i^{-1} \mathbf{H}_i^T$ | $\forall i.$ | (5.40) |
|-------------------------------------------------------------------------------------------------|--------------|--------|
|                                                                                                 |              |        |

The designer can run simulations before the flight and calculate the time history oftr Bi/ tr HiP − <sup>i</sup> H<sup>T</sup> i and choose an appropriate value of β. It is unlikely that higher order terms than B<sup>i</sup> will need to be considered in designing the value of β.

![](_page_71_Picture_1.jpeg)

#### CHAPTER 6

## Bias Modeling

Contributed by J. Russell Carpenter

<span id="page-72-0"></span>A general model for a measurement error is as follows:

| $e = b + v$ | (6.1) |
|-------------|-------|
|-------------|-------|

where b models the systematic errors, and v models the measurement noise. We assume that the measurement noise is a discrete sequence of uncorrelated random numbers. Variables such as v are known as random variables, and Appendix [A](#page-146-0) describes how to model them. This Chapter describes models for the systematic errors.

The discussion of systematic errors treats such errors as scalar quantities to simplify the exposition; generalization to the vector case is straightforward. Note that if the measurement is nonscalar, but the errors in the component measurements are independent of one another, then we can model each measurement independently, so modeling the biases as a vector is not required. If the measurement errors are not independent, then many estimators require that we apply a transformation to the data prior to processing so that the data input to the estimator have independent measurement errors; Appendix [A](#page-146-0) describes some ways to accomplish this transformation.

## 6.1. Zero-Input Bias State Models

<span id="page-72-1"></span>The simplest non-zero measurement error consists only of measurement noise. The next simplest class of measurement errors consists of biases which are either themselves constant, or are the integrals of constants. We can view such biases as the output of a system which has zero inputs, and which may have internal states. In the sequel, we will consider cases where there are random inputs to the system.

In cases where the bias is the output of a system with internal states, the estimator may treat the internal states as solve-for or consider parameters. In such cases, the estimator requires a measurement partials matrix. Otherwise, the "measurement partial" is just H = ∂b/∂b = 1.

6.1.1. Random Constant The simplest type of systematic error is a constant bias on the measurement. There are two types of such biases: deterministic constants, which are truly constant for all time, and random constants, which are constant or very nearly so over a particular time of interest. For example, each time a sensor is power-cycled, a bias associated with it may change in value, but so long as the sensor remains powered on, the bias will not change.

In some cases, we may have reason to believe that a particular systematic error source truly is a deterministic bias, but due to limited observability, we do not have knowledge of its true value. In such cases, we may view our estimate of the bias as a random constant, and its variance as a measure of the imprecision of our knowledge.

Thus, we may view all constants that could be solve-for or consider parameters in orbit determination as random constants. A model for a random constant is

$$\dot{b}(t) = 0, \quad b(t_0) \sim N(0, p_{b0}). \quad (6.2)$$

Thus the unconditional mean of b(t) is zero for all time, and its unconditional covariance is constant for all time as well. If b(t) is a filter solve-for variable that is observable, then its covariance conditioned on the measurement sequence will reach zero in the limit as t → ∞. This is an undesirable characteristic for application in a sequential navigation filter.

To simulate a realization of the random constant, we need only generate a random number according to N(0, pbo), as the previous subsection described.

6.1.2. Random Ramp The random ramp model assumes that the rate of change of the bias is itself a random constant; thus the random ramp model is

$$\dot{b}(t) = 0, \dot{b}(t_0) \sim N(0, p_{\dot{b}_0}). \quad (6.3)$$

Thus, the initial condition ˙b(to)is a random constant. For a pure random ramp, the initial condition on b(to) and its covariance are taken to be zero, but an obvious and common generalization is to allow b(to) to also be a random constant.

It is convenient to write this model as a first-order vector system as follows:

$$\begin{bmatrix} \dot{b}(t) \\ \ddot{b}(t) \end{bmatrix} = \begin{bmatrix} \dot{b}(t) \\ \dot{d}(t) \end{bmatrix} = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix} \begin{bmatrix} b(t) \\ d(t) \end{bmatrix} \quad (6.4)$$

$$\dot{\mathbf{x}}(t) = \mathbf{A}\mathbf{x}(t)$$
 (6.5)

where d(t) = ˙b(t). The resulting output equation for the total measurement error is

| $\mathbf{e} = \begin{bmatrix} 1 & 0 \end{bmatrix} \mathbf{x} + \mathbf{v}$ | (6.6) |
|----------------------------------------------------------------------------|-------|
|----------------------------------------------------------------------------|-------|

$$= Hx + v \quad (6.7)$$

Note that the ensemble of realizations of x(t) has zero-mean for all time. The unconditional covariance evolves in time according to

$$\mathbf{P}_{\mathbf{x}}(t) = \mathbf{\Phi}(t - t_0)\mathbf{P}_{\mathbf{x}_0}\mathbf{\Phi}^T(t - t_0) \quad (6.8)$$

where

$$\Phi(t) = \begin{bmatrix} 1 & t \\ 0 & 1 \end{bmatrix} \text{ and } \mathbf{P}_{xo} = \begin{bmatrix} p_{bo} & 0 \\ 0 & p_{bo} \end{bmatrix} \quad (6.9)$$

which we can also write in recursive form as

$$\mathbf{P}_{\mathbf{x}}(t + \Delta t) = \Phi(\Delta t)\mathbf{P}_{\mathbf{x}}(t)\Phi^T(\Delta t) \quad (6.10)$$

Thus, we can generate realizations of the random ramp with either x(t) ∼ N(0, Px(t)) or recursively from

$$x(t + \Delta t) = \Phi(\Delta t)x(t) \quad (6.11)$$

Note that the norm of the unconditional covariance becomes infinite as t <sup>2</sup> becomes infinite. This could lead to an overflow of the representation of the covariance in a computer program if the propagation time between measurements is large, if the bias is unobservable, or if the bias is a consider parameter, and could also lead to the representation of the covariance losing either its symmetry and/or its positive definiteness due to roundoff and/or truncation. If the bias and drift are filter solve-for variables, then the norm of their covariance conditioned on the measurement sequence will reach zero in the limit as t → ∞. These are all undesirable characteristics for application in a sequential navigation filter.

<span id="page-74-2"></span>6.1.3. Higher-Order Derivatives of Random Constants In principle, a random constant may be associated with any derivative of the bias in a straightforward extension of the models above. In practice, it is rare to need more than two or three derivatives. Conventional terminology does not appear in the literature for derivatives of higher order than the random ramp. The slope of the bias is most commonly described as the "bias drift," so that a "drift random ramp" would be one way to describe a bias whose second derivative is a random constant. The measurement partials matrix needs to be accordingly padded with trailing zeros for the derivatives of the bias in such cases.

### 6.2. Single-Input Bias State Models

<span id="page-74-0"></span>The simplest non-constant systematic errors are systems with a single input that is a random process. We can think of a random process as the result of some kind of limit in which the intervals between an uncorrelated sequence of random variables get infinitesimally small. In this limit, each random increment instantaneously perturbs the sequence, so that the resulting process is continuous but non-differentiable. We call this kind of a random input "process noise."

Although such random processes are non-differentiable, there are various techniques for generalizing the concept of integration so that something like integrals of the process noise exist, and hence so do the differentials that appear under the integral signs. It turns out that so long as any coefficients of the process noise are non-random, these differentials behave for all practical purposes as if they were differentiable.

6.2.1. Random Walk The random walk is the simplest random process of the type described above. In terms of the "formal derivatives" mentioned above, the random walk model for a measurement bias is

$$\dot{b}(t) = w(t), \quad w(t) \sim N(0, q\delta(t-s)) \quad (6.12)$$

The input noise process on the right hand side is known as "white noise," and the Dirac delta function that appears in the expression for its variance indicates that the white noise process consists of something like an infinitely-tightly spaced set of impulses. The term q that appears along with the delta function is the intensity of each impulse[<sup>1</sup>](#page-74-1) . The initial condition b(to) is an unbiased random constant. Since b(to) and w(t) are zero-mean, then b(t) is also zero-mean for all time. The unconditional variance of b evolves in time according to

$$p_b(t) = p_{bo} + q(t - t_o) \quad (6.13)$$

which we can also write in recursive form as

| $p_b(t + \Delta t) = p_b(t) + q\Delta t$ | (6.14) |
|------------------------------------------|--------|
|------------------------------------------|--------|

Thus, to generate a realization of the random walk at time t, we need only generate a random number according to N(0, pb(t)). Equivalently, we could also generate realizations of ϖ(t) ∼ N(0, q∆t), and recursively add these discrete noise increments to the bias as follows:

| $b(t + \Delta t) = b(t) + \varpi(t)$ | (6.15) |
|--------------------------------------|--------|
|--------------------------------------|--------|

Note that the unconditional variance becomes infinite as t becomes infinite. This could lead to an overflow of the representation of p<sup>b</sup> if q is large in the following circumstances: in a long gap between measurements, if the bias is unobservable, or if the bias is a consider parameter. These are all somewhat undesirable characteristics for application in a sequential navigation filter. However, because the process is persistently stimulated by the input, its variance conditioned on a measurement history will remain positive for all time. Hence the random walk finds frequent application

<span id="page-74-1"></span><sup>1</sup>Another way to imagine the input sequence, in terms of a frequency domain interpretation, is that it is a noise process whose power spectral density, q, is non-zero at all frequencies, which implies infinite bandwidth.

in sequential navigation filters, particularly when continuous measurements from which the bias is observable are generally available, such as often occurs for GPS data.

6.2.2. Random Run The random run model assumes that the rate of change of the bias is itself a random walk; thus the random run model is

$$\dot{b}(t) = w(t), \quad w(t) \sim N(0, q\delta(t-s)) \quad (6.16)$$

The initial condition ˙b(to) is a random constant. For a pure random run, the initial condition on b(to) and its covariance are taken to be zero, but an obvious and common generalization is to allow b(to) to also be a random constant.

It is convenient to write this model as a first-order vector system as follows:

$$\begin{bmatrix} \dot{\mathbf{b}}(t) \\ \ddot{\mathbf{b}}(t) \end{bmatrix} = \begin{bmatrix} \dot{\mathbf{b}}(t) \\ \ddot{\mathbf{d}}(t) \end{bmatrix} = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix} \begin{bmatrix} \mathbf{b}(t) \\ \mathbf{d}(t) \end{bmatrix} + \begin{bmatrix} 0 \\ 1 \end{bmatrix} \mathbf{w}(t) \quad (6.17)$$

$$\dot{\mathbf{x}}(t) = \mathbf{A}\mathbf{x}(t) + \mathbf{B}\mathbf{w}(t)$$
 (6.18)

The measurement partial is the same as for the random ramp. The initial condition x(to) is an unbiased random constant. Since x(to) and w(t) are zero-mean, then x(t) is also zero-mean for all time. The covariance evolves in time according to

$$\mathbf{P}_{\mathbf{x}}(t) = \mathbf{\Phi}(t - t_0)\mathbf{P}_{\mathbf{x}}\mathbf{\Phi}^T(t - t_0) + \mathbf{S}(t - t_0) \quad (6.19)$$

where

$$\Phi(t - t_0) = \begin{bmatrix} 1 & t \\ 0 & 1 \end{bmatrix} \text{ and } \mathbf{P}_{\mathbf{x}_0} = \begin{bmatrix} p_{b0} & 0 \\ 0 & p_{b0} \end{bmatrix} \quad (6.20)$$

and

$$\mathbf{S}(t) = q \begin{bmatrix} t^3/3 & t^2/2 \\ t^2/2 & t \end{bmatrix} \quad (6.21)$$

which we can also write in recursive form as

$$\mathbf{P}_{\mathbf{x}}(t + \Delta t) = \mathbf{\Phi}(\Delta t)\mathbf{P}_{\mathbf{x}}(t)\mathbf{F}^{\top}(\Delta t) + \mathbf{S}(\Delta t) \quad (6.22)$$

Thus, we can generate realizations of the random run with either x(t) ∼ N(0, Px(t) ) or recursively from

$$x(t + \Delta t) = \Phi(\Delta t)x(t) + \varpi(t) \quad (6.23)$$

where ϖ(t) ∼ N(0, S(∆t)) is a noise sample vector arising from formal integration of the scalar noise input process over the sample time. A Cholesky decomposition of S(t) useful for sampling is

$$\sqrt[c]{\mathbf{S}(t)} = \begin{bmatrix} \sqrt{3t^3}/3 & 0 \\ \sqrt{3t/2} & \sqrt{t/2} \end{bmatrix} \quad (6.24)$$

Note that the norm of the unconditional covariance becomes infinite as t <sup>3</sup> becomes infinite, and the process is persistently stimulated by the input, so its covariance conditioned on a measurement history will remain positive definite for all time. Hence, the random run shares similar considerations with the random walk for application in sequential navigation filters.

6.2.3. Higher-Order Derivatives of Random Walks In principle, a random walk may be associated with any derivative of the bias in a straightforward extension of the models above. In practice, it is rare to need more than two or three derivatives. Conventional terminology does not appear in the literature for derivatives of higher order than the random run. A "drift random run" would be one way to describe a bias whose second derivative is a random walk. Below, we will refer to such a model as a "random zoom."

<span id="page-76-1"></span>6.2.4. First-Order Gauss-Markov The first-order Gauss-Markov (FOGM) process is one of the simplest random processes that introduces time correlation between samples. In terms of a frequency domain interpretation, we can view it as white noise passed through a low-pass filter. Since such noise, often called "colored noise," has finite bandwidth, it is physically realizable, unlike white noise. In the notation of formal derivatives, the FOGM model is

$$\dot{b}(t) = -\frac{1}{\tau} b(t) + w(t), \quad (6.25)$$

where, as with the random walk, b(to) ∼ N(0, pbo), and w(t) ∼ N(0, qδ(t−s)). The time constant, τ gives the correlation time, or the time over which the intensity of the time correlation will fade to 1/ e of its prior value[<sup>2</sup>](#page-76-0) . Note that as τ → ∞, the FOGM approximates a random walk.

Since b(to) and w(t) are zero-mean, then b(t) is also zero-mean for all time. The covariance evolves in time according to

$$p_b(t) = e^{-\frac{2}{\tau}(t-t_0)} p_{b0} + s(t-t_0) \quad (6.26)$$

where

$$s(t - t_o) = \frac{q^\tau}{2} \left( 1 - e^{-\frac{2}{\tau}(t - t_o)} \right) \quad (6.27)$$

which we can also write in recursive form as

$$p_b(t + \Delta t) = e^{-\frac{2\Delta t}{\tau}} p_b(t) + s(\Delta t) \quad (6.28)$$

Thus, to generate discrete samples of a particular realization of the FOGM, we can either generate samples from b(t) ∼ N(0, pb(t)), or generate a realization of the initial bias value, and then at each sample time generate realizations of ϖ(t) ∼ N(0, s(∆t)), and recursively add these discrete noise sample increments to the bias sample history as follows:

$$b(t + \Delta t) = e^{-\frac{\Delta t}{\tau}} b(t) + \varpi(t) \quad (6.29)$$

Note that p<sup>b</sup> approaches a finite steady-state value equal to qτ /2 as t becomes infinite. One can choose the parameters of the FOGM so that this steady-state value avoids any overflow of the representation of p<sup>b</sup> in a computer program, and such that the FOGM's covariance evolution prior to reaching steady-state closely mimics that of a random walk. For these reasons, the FOGM is recommended as a best practice for bias modeling in sequential navigation filters.

6.2.5. Integrated First-Order Gauss-Markov Model As with the random walk and random constant models, any number of derivatives of the bias may be associated with a FOGM process. However, integration of the FOGM destroys its stability. For example, the singly integrated first-order Gauss-Markov model is given by

$$\begin{bmatrix} \dot{b}(t) \\ \dot{d}(t) \end{bmatrix} = \begin{bmatrix} 0 & 1 \\ 0 & -1/\tau \end{bmatrix} \begin{bmatrix} b(t) \\ d(t) \end{bmatrix} + \begin{bmatrix} 0 \\ w(t) \end{bmatrix}, \quad (6.30)$$

which leads to the following state transition matrix,

$$\Phi(t) = \begin{bmatrix} 1 & \tau (1 - e^{-t/\tau}) \\ 0 & e^{-t/\tau} \end{bmatrix}, \quad (6.31)$$

<span id="page-76-0"></span><sup>2</sup>One sometimes sees τ described as the "half-life," but since 1/ e < 1/2, this is not an accurate label.

and process noise covariance[<sup>3</sup>](#page-77-0) ,

<span id="page-77-1"></span>
$$\mathbf{S}(t) = \frac{q\tau}{2} \left[ \frac{\tau^2 \left\{ (1 - e^{-2t/\tau}) - 4(1 - e^{-t/\tau}) + 2t/\tau \right\}}{\tau (1 - e^{-t/\tau})^2} \tau (1 - e^{-2t/\tau}) \right]. \quad (6.32)$$

Clearly, this is an unstable model, as the bias variance increases linearly with elapsed time. As an alternative, the following second-order model is available.

6.2.6. Second-Order Gauss-Markov The model for a second-order Gauss-Markov (SOGM) random process is

$$\dot{b}(t) = -2\zeta\omega_b\dot{b}(t) - \omega_n^2b(t) + w(t), \quad w(t) \sim N(0, qd(t-s)) \quad (6.33)$$

The initial conditions b(to) and ˙b(to) are random constants. It is convenient to write this model as a first-order vector system as follows:

$$\begin{bmatrix} b(t) \\ b(t) \end{bmatrix} = \begin{bmatrix} b(t) \\ d(t) \end{bmatrix} = \begin{bmatrix} 0 & 1 \\ -\omega_n^2 & -2\zeta\omega_n \end{bmatrix} \begin{bmatrix} b(t) \\ d(t) \end{bmatrix} + \begin{bmatrix} 0 \\ 1 \end{bmatrix} w(t) \quad (6.34)$$

$$\dot{\mathbf{x}}(t) = \mathbf{A}\mathbf{x}(t) + \mathbf{B}\mathbf{w}(t)$$
 (6.35)

The measurement partial is the same as for the random ramp. The initial condition x(to) is an unbiased random constant vector. Since x(to) and w(t) are zero-mean, then x(t) is also zero-mean for all time.

The covariance evolves in time according to

$$\mathbf{P}_{\mathbf{x}}(t) = \mathbf{\Phi}(t - t_0)\mathbf{P}_{\mathbf{x}}\mathbf{\Phi}^T(t - t_0) + \mathbf{S}(t - t_0) \quad (6.36)$$

which we can also write in recursive form as

$$\mathbf{P}_{\mathbf{x}}(t + \Delta t) = \mathbf{\Phi}(\Delta t)\mathbf{P}_{\mathbf{x}}(t)\mathbf{F}^{\top}(\Delta t) + \mathbf{S}(\Delta t) \quad (6.37)$$

Thus, we can generate realizations of the SOGM with either x(t) ∼ N(0, Px(t)) or recursively from

$$\mathbf{x}(t + \Delta t) = \boldsymbol{\Phi}(\Delta t)\mathbf{x}(t) + \boldsymbol{\varpi}(t) \quad (6.38)$$

where ϖ(t) ∼ N(0, S(∆t)).

For the underdamped case (ζ < 1), the state transition matrix and discrete process noise covariance are given by Reference [86](#page-173-6):

$$\Phi(t) = \frac{e^{-\zeta \omega_n t}}{\omega_d} \left[ \frac{(\omega_d \cos \omega_d t + \zeta \omega_n \sin \omega_d t)}{-\omega_n^2 \sin \omega_d t} (\omega_d \cos \omega_d t - \zeta \omega_n \sin \omega_d t) \right] \quad (6.39)$$

and

$$\mathbf{S}_{(1,1)}(t) = \frac{q}{4\zeta\omega_n^3} \left[ 1 - \frac{e^{-2\zeta\omega_n t}}{w_d^2} (\omega_d^2 + 2\zeta\omega_n\omega_d \cos\omega_d t \sin\omega_d t + 2\zeta^2\omega_n^2 \sin^2\omega_d t) \right] \quad (6.40)$$

$$\mathbf{S}_{(2,2)}(t) = \frac{q}{4\zeta\omega_n} \left[ 1 - \frac{e^{-2\zeta\omega_n t}}{w_d^2} (\omega_d^2 - 2\zeta\omega_n\omega_d \cos\omega_d t \sin\omega_d t + 2\zeta^2\omega_n^2 \sin^2\omega_d t) \right] \quad (6.41)$$

$$\mathbf{S}_{(1,2)}(t) = \frac{q}{2\omega_d^2} e^{-2\zeta\omega_n t} \sin^2 \omega_d t, \quad (6.42)$$

| $\mathbf{S}_{(2,1)}(t) = \mathbf{S}_{(1,2)}(t)$ | (6.43) |
|-------------------------------------------------|--------|
|-------------------------------------------------|--------|

<span id="page-77-0"></span><sup>3</sup>Note that [\(6.32\)](#page-77-1) corrects an error in Reference [14](#page-170-14).

where ω<sup>d</sup> = ω<sup>n</sup> p 1 − ζ <sup>2</sup>. In the over-damped case (ζ > 1), replace sin and cos with sinh and cosh, respectively. In the critically-damped case,

$$\Phi(t) = \begin{bmatrix} e^{-\omega_n t} (1 + \omega_n t) & t e^{-\omega_n t} \\ -\omega_n^2 t e^{-\omega_n t} & e^{-\omega_n t} (1 - \omega_n t) \end{bmatrix} \quad (6.44)$$

and

$$\mathbf{S}_{(1,1)}(t) = \frac{q}{4\omega_n^3} [1 - e^{-2\omega_n t} (1 + 2\omega_n t + 2\omega_n^2 t^2)] \quad (6.45)$$

$$\mathbf{S}_{(2,2)}(t) = \frac{q}{4\omega_n} [1 - e^{-2\omega_n t} (1 - 2\omega_n t + 2\omega_n^2 t^2)] \quad (6.46)$$

$$\mathbf{S}_{(2,1)}(t) = \mathbf{S}_{(1,2)}(t) = \frac{qt^2}{2} e^{-2\omega_n t} \quad (6.47)$$

Note that for any damping ratio, ∥Px∥ remains finite, since as t → ∞,

$$\mathbf{P}_{\mathbf{x}}(t \rightarrow \infty) = \frac{q}{4\zeta\omega_n} \begin{bmatrix} 1/\omega_n^2 & 0 \\ 0 & 1 \end{bmatrix}. \quad (6.48)$$

Thus, the ratio of the steady-state standard deviations of the bias and drift will be

$$\frac{\sigma_d}{\sigma_b} = \omega_n, \quad (6.49)$$

and these are related to the power spectral density by

$$q = 4\zeta \frac{\sigma_b^3}{\sigma_b}. \quad (6.50)$$

Hence, we can choose the parameters of the SOGM so that we avoid any overflow, loss of symmetry and/or positive definiteness of P<sup>x</sup> due to roundoff and/or truncation. For these reasons, the SOGM is recommended as a best practice for bias drift modeling in sequential navigation filters.

6.2.7. Vasicek Model A criticism of the FOGM process is that as t → ∞, E[b(t)] → 0. In the filtering context, this implies that a data outage that is long relative to the time constant, τ , can result in the filter's bias estimate decaying toward zero, which may be undesirable. To address this concern, Seago et al. [[77](#page-173-7)] proposed that biases the filter should retain across such outages might be modeled instead with a model proposed by Vasicek [[85](#page-173-8)] for modeling interest rates:

<span id="page-78-0"></span>
$$\dot{\mathbf{b}}(t) = -\frac{1}{\tau}(\mathbf{b}(t) - \mathbf{b}_\infty) + \mathbf{w}(t), \quad (6.51)$$

where, as previously, b(to) ∼ N(0, Pbo), and w(t) ∼ N(0, qδ(t − s)). A formal solution to [\(6.51\)](#page-78-0) gives

$$\mathbf{b}(t) = \mathbf{b}(t_o) e^{-\frac{t-t_o}{\tau}} + b_\infty(1 - e^{-\frac{t-t_o}{\tau}}) + \int_{t_o}^t e^{-\frac{s}{\tau}} \mathbf{w}(s) ds \quad (6.52)$$

Since b(to) and w(t) are zero-mean, then

$$E[b(t)] = b_\infty(1 - e^{-\frac{t-t_0}{\tau}}) \quad (6.53)$$

and E[b(t)] = b<sup>∞</sup> as t → ∞. Since E[b(t)]<sup>2</sup> is subtracted from E b(t) 2 to get the covariance, the covariance evolves in time identically to the FOGM,

$$p_b(t) = e^{-\frac{2}{\tau}(t-t_0)} p_{b0} + s(t-t_0) \quad (6.54)$$

where as before

$$s(t - t_o) = \frac{q\tau}{2} \left( 1 - e^{-\frac{2}{\tau}(t - t_o)} \right) \quad (6.55)$$

Thus, to generate a realization of the Vasicek Model at particular time t, we could generate a realization of the initial bias value, and then at each sample time generate realizations of ϖ(t) ∼ N(0, s(∆t)), and recursively add these discrete noise sample increments to the bias sample history as follows:

| $b(t + \Delta t) = b(t) e^{-\frac{\Delta t}{\tau}} + b_\infty(1 - e^{-\frac{\Delta t}{\tau}}) + \varpi(t)$ | (6.56) |
|------------------------------------------------------------------------------------------------------------|--------|
|------------------------------------------------------------------------------------------------------------|--------|

or we could generate a random realization of N(0, pb(t)) and add this to b∞(1 − e − t−to <sup>τ</sup> ).

To configure or "tune" the Vasicek model, one chooses the time constant τ and the noise PSD q in a manner analogous to the FOGM process; it is less clear how one might choose b∞. Seago et al. [[77](#page-173-7)] proposed that b<sup>∞</sup> be estimated as a random constant filter state. Casting the Vasicek model into such a two-state form results in the following model:

$$\begin{bmatrix} \dot{b}(t) \\ \dot{b}_\infty \end{bmatrix} = \begin{bmatrix} -1/\tau & 1/\tau \\ 0 & 0 \end{bmatrix} \begin{bmatrix} b(t) \\ b_\infty \end{bmatrix} + \begin{bmatrix} w(t) \\ 0 \end{bmatrix}, \quad (6.57)$$

which leads to the following state transition matrix and process noise covariance:

$$\Phi(t) = \begin{bmatrix} e^{-t/\tau} & 1 - e^{-t/\tau} \\ 0 & 1 \end{bmatrix}, \quad \mathbf{S}(t) = \begin{bmatrix} \frac{q\tau}{2} \left(1 - e^{-\frac{2t}{\tau}}\right) & 0 \\ 0 & 0 \end{bmatrix}. \quad (6.58)$$

While the Vasicek Model shares with the FOGM the desirable feature that p<sup>b</sup> → qτ /2 as t → ∞, in the two-state form just described, it also has the undesirable feature that the variance of b<sup>∞</sup> goes to zero as t → ∞. Modeling b<sup>∞</sup> with process noise, e.g. as a random walk with PSD of q∞, introduces an unstable integral of the process noise as occurs for the integrated FOGM:

$$\mathbf{S}(t) = \left[ q_{\infty} \left( t - \frac{3\tau}{2} + 2\tau e^{-\frac{t}{\tau}} - \frac{2t}{2} e^{-\frac{2t}{\tau}} \right) + \frac{q\tau}{2} \left( 1 - e^{-\frac{2t}{\tau}} \right) - q_{\infty} t - q_{\infty} \tau \left( 1 - e^{-\frac{t}{\tau}} \right) \right], \quad (6.59)$$

although choosing q<sup>∞</sup> appropriately small may mitigate this concern. In any case, retaining a steady-state bias across long data gaps may not always be warranted, depending on the context. And if long measurement gaps are not present, the need to retain such a bias, with the accompanying complexity of maintaining an additional state, may not be necessary. We will consider further such multi-input bias models in the sequel.

#### 6.3. Multi-Input Bias State Models

<span id="page-79-0"></span>We may combine any of the above models to create multi-input bias models; for example the bias could be a second-order Gauss-Markov, and the bias rate could be a first-order Gauss-Markov. In practice, the most useful combinations have been found to be the following.

6.3.1. Bias and Drift Random Walks (Random Walk + Random Run) A common model for biases in clocks, gyros, and accelerometers is that the bias is driven by both its own white noise input, and also by the integral of the white noise of its drift. Such models derive from observations that the error magnitudes of these devices depend on the time scale over which the device is observed. They are often characterized by Allan deviation specifications, which may be heuristically associated with the white noise power spectral densities. The model is as follows:

$$\begin{bmatrix} \dot{b}(t) \\ \dot{d}(t) \end{bmatrix} = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix} \begin{bmatrix} b(t) \\ d(t) \end{bmatrix} + \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix} \begin{bmatrix} w_b(t) \\ w_d(t) \end{bmatrix} \quad (6.60)$$

$$\dot{\mathbf{x}}(t) = \mathbf{A}\mathbf{x}(t) + \mathbf{B}\mathbf{w}(t) \quad (6.61)$$

The measurement partial is the same as for the random ramp. The initial condition x(to) is an unbiased random constant. Since x(to) and w(t) are zero-mean, then x(t) is also zero-mean for all time. The covariance evolves in time according to

$$\mathbf{P}_{\mathbf{x}}(t) = \mathbf{\Phi}(t - t_0)\mathbf{P}_{\mathbf{x}_0}\mathbf{\Phi}^T(t - t_0) + \mathbf{S}(t - t_0) \quad (6.62)$$

where

$$\Phi(t) = \begin{bmatrix} 1 & t \\ 0 & 1 \end{bmatrix} \text{ and } \mathbf{P}_{\mathbf{x}o} = \begin{bmatrix} p_{bo} & 0 \\ 0 & p_{bo} \end{bmatrix} \quad (6.63)$$

and

$$\mathbf{S}(t) = \begin{bmatrix} q_b t + q_d t^3/3 & q_d t^2/2 \\ q_d t^2/2 & q_d t \end{bmatrix} \quad (6.64)$$

which we can also write in recursive form as

| $\mathbf{P}_x(t + \Delta t) = \Phi(\Delta t)\mathbf{P}_x(t)\Phi^T(\Delta t) + \mathbf{S}(\Delta t)$ | (6.65) |
|-----------------------------------------------------------------------------------------------------|--------|
|-----------------------------------------------------------------------------------------------------|--------|

Thus, we can generate realizations of the random run with either x(t) ∼ N(0, Px(t)) or recursively from

| $x(t + \Delta t) = \Phi(\Delta t)x(t) + \varpi(t)$ | (6.66) |
|----------------------------------------------------|--------|
|----------------------------------------------------|--------|

where ϖ(t) ∼ N(0, S(∆t)). Note that a Cholesky decomposition of S(t) is

$$\sqrt[c]{\mathbf{S}(t)} = \left[ \frac{\sqrt{q_b t + q_d t^3/12}}{0} \quad \frac{\sqrt{q_d t^3/2}}{\sqrt{q_d t}} \right] \quad (6.67)$$

As with its constituent models, the norm of the unconditional covariance becomes infinite as t <sup>3</sup> becomes infinite, while the process is persistently stimulated by the input, so its covariance conditioned on a measurement history will remain positive definite for all time. Hence, this model shares similar considerations with its constituents for application in sequential navigation filters.

6.3.2. Bias, Drift, and Drift Rate Random Walks (Random Walk + Random Run + Random Zoom) Another model for biases in very-high precision clocks, gyros, and accelerometers is that the bias is driven by two integrals of white noise in addition to its own white noise input. Such models are often characterized by Hadamard deviation specifications, which may be heuristically associated with the white noise power spectral densities. The model is as follows:

$$\begin{bmatrix} \dot{b}(t) \\ \dot{d}(t) \\ \ddot{d}(t) \end{bmatrix} = \begin{bmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ 0 & 0 & 0 \end{bmatrix} \begin{bmatrix} b(t) \\ d(t) \\ d(t) \end{bmatrix} + \begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} w_b(t) \\ w_d(t) \\ w_d(t) \end{bmatrix} \quad (6.68)$$

$$\dot{\mathbf{x}}(t) = \mathbf{A}\mathbf{x}(t) + \mathbf{B}\mathbf{w}(t)$$
 (6.69)

The resulting output equation is

| $e = [1 \ 0 \ 0] \mathbf{x} + \mathbf{v}$ | (6.70) |
|-------------------------------------------|--------|
|-------------------------------------------|--------|

$$= \mathbf{H}\mathbf{x} + \mathbf{v} \quad (6.71)$$

The initial condition x(to) is an unbiased random constant. Since x(to) and w(t) are zero-mean, then x(t) is also zero-mean for all time. The covariance evolves in time according to

$$\mathbf{P}_{\mathbf{x}}(t) = \mathbf{\Phi}(t - t_0)\mathbf{P}_{\mathbf{x}}\mathbf{\Phi}^T(t - t_0) + \mathbf{S}(t - t_0) \quad (6.72)$$

where

$$\Phi(t) = \begin{bmatrix} 1 & t & t^2/2 \\ 0 & 1 & t \\ 0 & 0 & 1 \end{bmatrix} \text{ and } \mathbf{P}_{xo} = \begin{bmatrix} p_{bo} & 0 & 0 \\ 0 & p_{do} & 0 \\ 0 & 0 & p_{do} \end{bmatrix} \quad (6.73)$$

and

| $\mathbf{S}(t) = \begin{bmatrix} q_t b + q_d t^3 / 3 + q_d t^5 / 5 & q_d t^2 / 2 + q_d t^4 / 8 & q_d t^3 / 6 \\ q_d t^2 / 2 + q_d t^4 / 8 & q_d t + q_d t^3 / 3 & q_d t^2 / 2 \\ q_d t^3 / 6 & q_d t^2 / 2 & q_d t \end{bmatrix}$ | (6.7) |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|

which we can also write in recursive form as

| $\mathbf{P}_x(t + \Delta t) = \Phi(\Delta t)\mathbf{P}_x(t)\Phi^T(\Delta t) + \mathbf{S}(\Delta t)$ | (6.75) |
|-----------------------------------------------------------------------------------------------------|--------|
|-----------------------------------------------------------------------------------------------------|--------|

Thus, we can generate realizations of the random run with either x(t) ∼ N(0, Px(t)) or recursively from

$$x(t + \Delta t) = \Phi(\Delta t)x(t) + \varpi(t) \quad (6.76)$$

where ϖ(t) ∼ N(0, S(∆t)). Note that a Cholesky decomposition of S(t) is

$$\sqrt{\mathbf{S}(t)} = \begin{bmatrix} \sqrt{q_b t + q_d t^3/12 + q_d t^5/720} & t/2\sqrt{q_d t + q_d t^3/12} & t^2/6\sqrt{q_d t} \\ 0 & \sqrt{q_d t + q_d t^3/12} & t/2\sqrt{q_d t} \\ 0 & 0 & \sqrt{q_d t} \end{bmatrix} \quad (6.77)$$

Similar to its constituent models, the norm of the unconditional covariance becomes infinite as t <sup>5</sup> becomes infinite, while the process is persistently stimulated by the input, so its covariance conditioned on a measurement history will remain positive definite for all time. Hence, this model shares similar considerations with its constituents for application in sequential navigation filters.

6.3.3. Bias and Drift Coupled First- and Second-Order Gauss-Markov The following model provides a stable alternative, developed in Reference [14](#page-170-14), to the "Random Walk + Random Run" model. Note that the following description corrects a sign error in the process noise crosscovariance results of the cited work. The transient response of the stable alternative can be tuned to approximate the Random Walk + Random Run model, and its stable steady-state response can be used to avoid computational issues with long propagation times, observability, consider states, etc. Although this model has received limited application as of the time of this writing, due to its stability, it shows promising potential to evolve into a best practice for sequential navigation filtering applications.

The coupled first- and second-order Gauss-Markov model is as follows.

$$\begin{bmatrix} b(t) \\ d(t) \end{bmatrix} = \begin{bmatrix} -1/\tau & 1 \\ -\omega_n^2 & -2\zeta\omega_n \end{bmatrix} \begin{bmatrix} b(t) \\ d(t) \end{bmatrix} + \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix} \begin{bmatrix} w_b(t) \\ w_d(t) \end{bmatrix} \quad (6.78)$$

| $\dot{\mathbf{x}}(t) =$ | $\mathbf{A}\mathbf{x}(t) + \mathbf{B}\mathbf{w}(t)$ | (6.79) |
|-------------------------|-----------------------------------------------------|--------|
|-------------------------|-----------------------------------------------------|--------|

The measurement partial is the same as for the random ramp. The initial condition x(to) is an unbiased random constant. Since x(to) and w(t) are zero-mean, then x(t) is also zero-mean for all time. The covariance evolves in time according to

$$\mathbf{P}_{\mathbf{x}}(t) = \mathbf{\Phi}(t - t_0)\mathbf{P}_{\mathbf{x}}\mathbf{\Phi}^T(t - t_0) + \mathbf{S}(t - t_0) \quad (6.80)$$

where

$$\Phi(t) = \frac{e^{\eta t}}{\nu} \left[ \nu \cos \nu t + (\eta^2 + 2\zeta \omega_n) \sin \nu t - \omega_n^2 \sin \nu t - \nu \cos \nu t + (\eta + \beta) \sin \nu t \right] \quad (6.81)$$

<span id="page-82-0"></span>with

| $\beta = 1/\tau,$ | (6.8) |
|-------------------|-------|
|-------------------|-------|

| $\beta = 1/\tau$ | (6.82) |
|------------------|--------|
|------------------|--------|

$$\eta = -\frac{1}{2} (\beta + 2\zeta \omega_n), \quad (6.83)$$

$$\eta = -\frac{2}{2}(\beta + 2\zeta w_n), \quad (6.83)$$

$$\nu = \sqrt{\omega_d^2 + \beta\zeta\omega_n - \frac{1}{4}\beta^2}, \quad (6.84)$$

$$\omega_d = \omega_n \sqrt{1 - \zeta^2} \quad (6.85)$$

and we assume that ν <sup>2</sup> > 0. Let

$$\kappa = -\frac{\beta}{2} + \zeta \omega_n$$

Then, the process noise covariance is given by the following:

$$\mathbf{S}_{(1,1)}(t) = q_b \left[ \frac{e^{2\eta t} - 1}{4\eta} \left( 1 + \frac{\kappa^2}{\nu^2} \right) + \frac{e^{2\eta t} \sin 2\nu t}{4(\eta^2 + \nu^2)} \left( \frac{\nu^2 - \kappa^2 + \eta\kappa}{\nu} \right) \right. \\ \left. + \frac{e^{2\eta t} \cos 2\nu t - 1}{4(\eta^2 + \nu^2)} \left( \frac{\eta\nu^2 - \eta\kappa^2 + 2\nu^2\kappa}{\nu^2} \right) \right] \quad (6.86) \\ + \frac{q_d}{\nu^2} \left( \frac{e^{2\eta t} - 1}{4\eta} - \frac{e^{2\eta t}(\nu \sin 2\nu t + \eta \cos 2\nu t) - \eta}{4(\eta^2 + \nu^2)} \right)$$

$$\mathbf{S}_{(2,2)}(t) = q_d \left[ \frac{e^{2\eta t} - 1}{4\eta} \left( 1 + \frac{\kappa^2}{\nu^2} \right) + \frac{e^{2\eta t} \sin 2\nu t}{4(\eta^2 + \nu^2)} \left( \frac{\nu^2 - \kappa^2 + \eta\kappa}{\nu} \right) + \frac{e^{2\eta t} \cos 2\nu t - 1}{4(\eta^2 + \nu^2)} \left( \frac{\eta\nu^2 - \eta\kappa^2 + 2\nu^2\kappa}{\nu^2} \right) \right] \quad (6.87)$$

$$+ \frac{q_b \omega_n^4}{\nu^2} \left( \frac{e^{2\eta t} - 1}{4\eta} - \frac{e^{2\eta t}(\nu \sin 2\nu t + \eta \cos 2\nu t) - \eta}{4(\eta^2 + \nu^2)} \right)$$

$$\mathbf{S}_{(1,2)}(t) = \frac{q_b \omega_n^2}{\nu^2} \left[ \frac{\kappa}{4\eta} (1 - e^{2\eta t}) + \frac{e^{2\eta t} [(\nu\kappa - \eta\nu) \sin 2\nu t + (\eta\kappa + \nu^2) \cos 2\nu t] - (\eta\kappa + \nu^2)}{4(\eta^2 + \nu^2)} \right] + \frac{q_d}{\nu^2} \left[ \frac{\kappa}{4\eta} (1 - e^{2\eta t}) + \frac{e^{2\eta t} [(\eta\nu + \nu\kappa) \sin 2\nu t + (\eta\kappa - \nu^2) \cos 2\nu t] - (\eta\kappa - \nu^2)}{4(\eta^2 + \nu^2)} \right] \quad (6.88)$$

| $\mathbf{S}_{(2,1)}(t) = \mathbf{S}_{(1,2)}(t)$ | (6.89) |
|-------------------------------------------------|--------|
|-------------------------------------------------|--------|

Examining the solution given above, we see that the parameter η governs the rate of decay of all of the exponential terms. Therefore, we define the "rise time" as that interval within which the transient response of the covariance will reach a close approximation to the above steady-state value; thus, we define the rise time as follows:

| $t_r = -\frac{3}{\eta}$ | (6.90) |
|-------------------------|--------|
|-------------------------|--------|

Next, we note that all of the trigonometric terms are modulated by 2ν; thus we may view this value as a characteristic damped frequency of the coupled system. The period of the oscillation, Π, is then

| $\Pi = \pi/\nu$ | (6.91) |
|-----------------|--------|
|-----------------|--------|

<span id="page-83-0"></span>In the limit as t → ∞, all the exponential terms in the analytical solution die out, so that the steady-state value of the covariance simplifies to:

$$\mathbf{P}(\infty) = -\frac{1}{4\eta(\eta^2 + \nu^2)} \begin{bmatrix} q_d + (2\eta^2 + \nu^2 + \kappa^2 - \eta\kappa)q_b & q_b\omega_n^2(\eta - \kappa) - q_d(\eta + \kappa) \\ q_b\omega_n^2(\eta - \kappa) - q_d(\eta + \kappa) & (2\eta^2 + \nu^2 + \kappa^2 + \eta\kappa)q_d + q_b\omega_n^4 \end{bmatrix} \quad (6.92)$$

which may be expressed in terms of the original parameters as

$$P(\infty) = \frac{1}{4\omega_n(\omega_n + 2\beta\zeta)(\zeta\omega_n + \beta/2)} \left[ \frac{q_d + (\omega_n^2 + 2\beta\zeta\omega_n + 4\zeta^2\omega_n^2)q_b}{q_d\beta - 2\zeta\omega_n^3q_b} \frac{q_d\beta - 2\zeta\omega_n^3q_b}{(\omega_n^2 + 2\beta\zeta\omega_n + \beta^2)q_d + \omega_n^4q_b} \right] \quad (6.93)$$

## State Representations

<span id="page-84-4"></span><span id="page-84-0"></span>Contributed by J. Russell Carpenter and Christopher N. D'Souza

This Chapter discusses state representation, primarily for translations; attitude representations are discussed in Chapter [9.](#page-108-0)

## 7.1. Selection of Solve-For State Variables for Estimation

<span id="page-84-1"></span>As has been discussed in Chapter [3,](#page-38-0) it not good practice to include unobservable states in the EKF solve-for vector, particularly if this introduces unstable dynamical modes. Nonetheless, during the early stages of designing a navigation filter, it may not be clear to the designer which states to include. There are essentially two approaches to addressing this question, which we may describe as the additive and subtractive methods. With the additive approach, one begins with the smallest possible set of states, adding additional models as one deems them necessary. The problem with this approach is essentially that it is not possible to foresee how additional states will affect the system until they are added; one cannot analyze the sensitivity of the filter's performance to states which are not present in the analysis. The preferred, subtractive, approach is instead to start with a design of as high a fidelity as practical, including even modes which one may suspect are unobservable and possibly destabilizing. A designer may then readily perform sensitivity and covariance analysis [[27](#page-171-5), [60](#page-172-3)] to winnow the solve-for state to as parsimonious a set of observable states as needed to achieve design requirements.

## 7.2. Units and Precision

<span id="page-84-2"></span>In the early days of ground-based orbit determination, canonical units were preferred due to the limited word lengths that were available for computation. Factorized filtering methods largely eliminated the need for canonical units even before "modern" double-precision word lengths became available in onboard processors. A renewed interest in single-precision computations has emerged however as the desire to utilize processors based on Field Programmable Gate Arrays has become widespread. Thus, the possibility of overflow, truncation, and roundoff errors must still be considered. Wherever possible, filter computations, especially those involving the covariance matrix (even when it is factorized!), should be done in double precision, and time should be maintained in either two double-precision variables, or in quadruple precision if available. For low-Earth orbit navigation in an Earth-centered frame, position/velocity units based on meters and seconds are often adequate; for applications that may reach into cislunar space and beyond, units based on kilometers and seconds are preferred.

## 7.3. Coordinate and Time Systems

<span id="page-84-3"></span>For most orbital navigation applications, use of an "inertial" coordinate frame, such as the International Celestial Reference Frame, the "J2000" (FK5) frame, etc., will be desirable, since onboard computations utilizing navigation filter state estimates will typically most naturally occur in an inertial setting. It is usually convenient to choose a frame whose origin is at the center of the primary gravitational body. Some missions, such as cislunar and interplanetary missions, will occur within the Hill spheres of more than one celestial body, and some mechanism for changing the coordinate system origin without requiring reset of the filter should be considered.

In some cases, consideration may be given to central-body-fixed frames, such as the International Terrestrial Reference Frame, World Geodetic System of 1984, etc., particularly for applications that rely primarily on Global Navigation Satellite Systems (GNSS), and/or ground-based tracking systems. Although integrating the equations of motion in such systems necessitates additional calculations of Coriolis and centripetal acceleration, such calculations are relatively trivial in comparison to the computations required to accurately maintain a transformation between central-body-fixed and inertial frames. Computations of higher-order gravity acceleration are simplified, and maintenance of polar motion coefficients is also eliminated. Several of NASA's early Global Positioning System relative navigation experiments used such a formulation successfully [[66](#page-172-7), [74](#page-172-8)]. If other onboard applications require inertial states, but are indifferent as to which inertial frame is provided, it may be prudent to consider defining a fixed, true-of-date inertial frame which is identical to the body-fixed frame at the initial power-up of the navigation system, and which is henceforth related to the body-fixed frame by a simple single-axis polar rotation. Such an approach will permit navigation in the body-fixed frame without the difficulties of maintaining a relationship onboard the spacecraft to one of the conventional inertial frames.

With regard to time systems, navigation filter designs should strongly avoid dependence upon discontinuous time scales, such as Coordinated Universal Time ("UTC"). While ground-based applications will generally prefer UTC, it is far easier for the mission's ground system to manage leap seconds than it is to robustly test and maintain discontinuous time scales in an autonomous onboard navigation setting. The filter designer should strive to ensure that a misapplication of leap second logic can never affect filter performance. If requirements for maintenance of UTC onboard cannot be avoided, all such calculations should occur independently from the uniform continuous time scale that the filter uses internally. Time-tagged commands that affect filter performance should also utilize the same internal, continuous time scale.

## 7.4. Orbit Parameterizations

<span id="page-85-0"></span>For orbital navigation applications, orbital elements are geometrically appealing as a state representation, and there exist various "semi-analytic" theories for improving their usefulness as ephemeris representations for real-world orbits, such as the GPS broadcast ephemeris model, twoline elements, etc. Furthermore, long-term evolution of the orbital error covariance more naturally occurs in element representations, which may be especially relevant to conjunction analysis. However, NASA's experience has been that Cartesian parameters generally offer computational efficiencies for high-fidelity measurement and dynamics models, including for the Jacobian matrices required in estimation algorithms. Cartesian coordinates are also free of singularities.

## 7.5. Relative State Representations

<span id="page-85-1"></span>Although the subject of this Section implies the need for relative state knowledge, it is not necessarily the case that this implies estimation of the relative states directly. For example, if each spacecraft's only sensor is a GNSS receiver, and there is no method for exchanging the GNSS data between spacecraft, then each satellite's measurement errors will be largely uncorrelated, assuming that errors in the GNSS constellation data are minimal. Furthermore, there may be no common sources of dynamical error, such as might arise from common yet imperfect models of atmospheric density for low Earth orbiters. In such cases, mission requirements may be met simply be performing isolated state estimation onboard each satellite, and simply differencing the estimated state vectors. In such cases, the covariance of the relative state error between any two spacecraft is given by

$$P_{\text{rel}} = E[(e_2 - e_1)(e_2 - e_1)^T] = P_1 + P_2 \quad (7.1)$$

where e<sup>i</sup> denotes the estimation error for spacecraft i, since (by assumption) E[e1e T 2 ] = 0. For many other applications, either the measurements or the dynamics or both will induce a correlation structure, making it necessary to simultaneously estimate some combination of Earthcentered (a.k.a. "absolute" or "inertial") states and spacecraft-to-spacecraft relative states. The choice of state representation and associated dynamical model for each application can have significant impacts on efficiency and accuracy, and requires careful consideration.

Aside from the choice of orbit parameterization, there are at least three choices for estimating a relative orbit. The most obvious choice is to solve directly for the differences between the parameters chosen for the orbit representation; that is, to solve for relative position and relative velocity, or relative orbital elements. In some contexts, such as nearly circular orbits, efficient dynamics, such as the linear time-invariant Hill-Clohessy-Wilshire model [[17](#page-170-15), [34](#page-171-14)], become available with a choice to solve directly for relative Cartesian states. In many other contexts, higher fidelity may be required, and furthermore, models for drag, solar radiation pressure, the ephemerides of other gravitational bodies, etc. may require knowledge of the Earth-centered (Cartesian) state of one or more of the spacecraft. In such cases, the estimator may solve for a combination of pure absolute/inertial states, or some combination of absolute and relative states. The architecture originally developed for NASA's Apollo missions was the former "dual-inertial" formulation [[63](#page-172-9)]. While the absolute/relative formulation may appear to be mathematically equivalent, computational considerations may choose one or the other to be favored in various application contexts. A general observation is that the dual-inertial formulation may be favorable for computations involving the state and state error covariance, and for "absolute" measurements such as undifferenced GPS pseudorange, while the absolute/relative formulation may be favorable for computations involving satellite-to-satellite relative measurements. Reference [[63](#page-172-9)] provides a comprehensive mathematical description of the dual-inertial formulation in the context of relative range, Doppler, and bearing measurements that one may easily adapt to any other measurement types.

7.5.1. Dual Inertial State Representation Here, we consider only two spacecraft, but the results are easily generalized. Let x<sup>i</sup> = [r T i , v<sup>T</sup> i T , i = 1, 2 denote the true state of spacecraft i, with r<sup>i</sup> , v<sup>i</sup> the position and velocity vectors expressed in non-rotating coordinates centered on the primary central gravitational body. Based on mission requirements, any appropriate fidelity of dynamics may be directly utilized, e.g.

$$\dot{x}_i = \left[ -\frac{\mu}{\|r_i\|^3} r_i + \sum_j f_j \right] \quad (7.2)$$

where the specific forces f<sup>j</sup> may include thrust, higher-order gravity, drag, solar radiation pressure, gravity from non-central bodies such as the moon and the sun, etc.

Let e<sup>i</sup> = ˆx<sup>i</sup> − x<sup>i</sup> , where xˆ<sup>i</sup> is an estimate for the state of spacecraft i. Then, the error in the state estimate xˆ = [ˆx T 1 , xˆ T 2 ] T is e = [e T 1 , e<sup>T</sup> 2 T , and the error covariance is

$$P = E[ee^T] = \begin{bmatrix} P_1 & P_{12} \\ P_{12}^T & P_2 \end{bmatrix} \quad (7.3)$$

<span id="page-87-0"></span>Any linear unbiased estimate of x will have the following measurement update equation:

$$\hat{x}^+ = \hat{x}^- + K(y - h(\hat{x}^-)) \quad (7.4)$$

where xˆ <sup>−</sup> is the value of xˆ immediately prior to incorporating the observation, y, and h(ˆx <sup>−</sup>) is an unbiased prediction of the measurement's value. The optimal gain is

| $K = PH^\top(HPH^\top + R)^{-1}$ | (7.5) |
|----------------------------------|-------|
|----------------------------------|-------|

where R is the measurement noise covariance and H = ∂h(x)/∂x|xˆ<sup>−</sup> . Partition the update as follows:

$$\begin{bmatrix} \hat{x}_1^+ \\ \hat{x}_2^+ \end{bmatrix} = \begin{bmatrix} \hat{x}_1^- \\ \hat{x}_2^- \end{bmatrix} + \begin{bmatrix} K_1 \\ K_2 \end{bmatrix} (y - h(\hat{x}^-)) \quad (7.6)$$

$$= \begin{bmatrix} \hat{x}_1 \\ \hat{x}_2 \end{bmatrix} + \begin{bmatrix} P_1 H_1^\top + P_{12} H_2^\top \\ P_{12}^\top H_1^\top + P_2 H_2^\top \end{bmatrix} (HPH^\top + R)^{-1}(y - h(\hat{x}^-)) \quad (7.7)$$

from which it is clear that the optimal update for the relative state xˆrel = ˆx<sup>2</sup> − xˆ<sup>1</sup> is

$$\hat{x}_{\text{rel}}^+ = \hat{x}_{\text{rel}}^+ + (P_2 H_2^\top - P_1 H_1^\top - P_{12} H_2^\top + P_{12}^\top H_1^\top)(H P H^\top + R)^{-1}(y - h(\hat{x}^\top)) \quad (7.8)$$

with corresponding relative error covariance

| $P_{\text{rel}} = P_1 + P_2 - P_{12} - P_{12}^T$ | (7.9) |
|--------------------------------------------------|-------|
|--------------------------------------------------|-------|

Noting that it must be true that h(xrel) = h(x) and hence that ∂h(xrel)/∂xrel = ∂h(x2)/∂x<sup>2</sup> = −∂h(x1)/∂x1, let Hrel = H<sup>2</sup> = −H1. Then it is clear that

$$P_{\text{rel}} r_{\text{rel}}^{\top} = P_2 H_2^{\top} - P_1 H_1^{\top} - P_{12} H_2^{\top} + P_{12} H_1^{\top} \quad (7.10)$$

and that

| $H_{\text{rel}}P_{\text{rel}}H_{\text{rel}}^{\text{T}} = HPH^{\text{T}}$ | (7.11) |
|--------------------------------------------------------------------------|--------|
|                                                                          |        |

and hence

$$\hat{x}_{\text{rel}}^+ = \hat{x}_{\text{rel}}^- + p_{\text{rel}} H_{\text{rel}}^{\text{T}} (H_{\text{rel}} p_{\text{rel}} H_{\text{rel}}^{\text{T}} + R)^{-1} (y - h(\hat{x}_{\text{rel}}^-)) \quad (7.12)$$

Therefore, the dual inertial state update is mathematically (although perhaps not computationally) equivalent to a direct update of the relative state.

Appendix [C](#page-160-0) reproduces a memorandum that further details the benefits of the dual inertial formulation.

7.5.2. Linearized Relative State Representation While it is sometimes useful to employ a linear model of the relative dynamics, especially for close proximity operations in near-circular orbits, there is significant benefit to casting the equations of motion in spherical coordinates. The following derivation of the Hill-Clohessy-Wiltshire equations in spherical coordinates is derived from notes from a lecture given by Robert H. Bishop. Let the position of a spacecraft be given by a set of right-handed spherical coordinates

$$r = \rho \begin{bmatrix} \cos \phi \sin \theta \\ \sin \phi \\ \cos \phi \cos \theta \end{bmatrix} \quad (7.13)$$

where ρ is the distance from the central body to the spacecraft, θ is measured along some specified great circle of the central body, and ϕ is measured along a great circle of the central body that is normal to the former great circle, and contains the position vector, as Figure [7.1](#page-88-0) depicts. Define

![](_page_88_Picture_2.jpeg)

Figure 7.1. Spherical coordinates.

a state vector as follows: x = [ρ, ρ, θ, ˙ ˙θ, ϕ, ϕ˙ ]. If the only force on the spacecraft is point-mass gravity from the central body, then the equations of motion are given by

<span id="page-88-1"></span><span id="page-88-0"></span>
$$\dot{x} = f(x) = \begin{bmatrix} \dot{\rho} \\ -\mu/\rho^2 + \rho\dot{\phi}^2 + \rho\dot{\theta}^2 \cos^2 \phi \\ \dot{\theta} \\ -2\dot{\rho}\dot{\theta}/\rho + 2\dot{\phi}\dot{\theta} \tan \phi \\ \dot{\phi} \\ -2\dot{\rho}\dot{\phi}/\rho - \dot{\theta}^2 \cos \phi \sin \phi \end{bmatrix} \quad (7.14)$$

Now consider a circular reference orbit, with radius ρ∗, which is in the plane of the great circle containing the θ coordinate. Let ω<sup>∗</sup> = p µ/ρ<sup>3</sup> ∗ . Then, the state of an object following the circular reference orbit at any time t > t<sup>o</sup> will be x∗(t) = [ρ∗, 0, ω∗(t − to) − θo, ω∗, 0, 0]. Without loss of generality, take θ<sup>o</sup> = t<sup>o</sup> = 0. Letting δx = x − x∗, linearization of [\(7.14\)](#page-88-1) in the neighborhood of x<sup>∗</sup> yields

$$\delta \dot{x}(t) = \frac{\partial f(x)}{\partial x} \Big|_{x_*(t)} \delta x(t) = \begin{bmatrix} 0 & 1 & 0 & 0 & 0 & 0 \\ 3\omega_*^2 & 0 & 0 & 2\omega_* \rho_* & 0 & 0 \\ 0 & 0 & 0 & 1 & 0 & 0 \\ 0 & -2\omega_*/\rho_* & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 1 \\ 0 & 0 & 0 & 0 & -\omega_*^2 & 0 \end{bmatrix} \delta x(t) \quad (7.15)$$

In this context, it is useful to redefine the state vector x˜ = [ρ, ρ, ρ ˙ <sup>∗</sup>θ, ρ<sup>∗</sup> ˙θ, ρ∗ϕ, ρ∗ϕ˙ ] so that angles are replaced by arc lengths. Then, the linearized equations of motion become

$$\delta \dot{\tilde{x}}(t) = \begin{bmatrix} 0 & 1 & 0 & 0 & 0 \\ 3\omega_*^2 & 0 & 0 & 2\omega_* & 0 \\ 0 & 0 & 0 & 1 & 0 \\ 0 & -2\omega_* & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 1 \\ 0 & 0 & 0 & -\omega_*^2 & 0 \end{bmatrix} \delta \tilde{x}(t) \quad (7.16)$$

If linearized relative dynamics are to be used for relative navigation in near-circular orbits, then interpreting the motion along the orbit track, and normal to the orbit track, as arc lengths, per the derivation above, is desirable since it will preserve the linearity of the approximation over a much wider range than if the along-track and cross-track coordinates are taken as rectilinear tangents to the reference orbit position.

## 7.6. Modeling Inertial Components

<span id="page-89-0"></span>Many onboard navigation systems employ inertial components consisting of gyros and/or accelerometers. In some applications, an external algorithm will process the increments of rotational and/or translational motion that these devices inherently measure, and produce an acceleration vector that the filter can directly incorporate into its computation of the equations of motion. However, it will often be the case that biases affecting these devices should be estimated by the filter. This section describes some recommended models for such biases, as well as the computations that need to be performed to accumulate the inertial measurement unit's (IMU) angle and velocity increments.

7.6.1. The Gyro Model The gyro is modeled in terms of the bias, scale factor and nonorthogonality. The IMU case frame is defined such that the x-axis of the gyro is the reference direction with the x − y plane being the reference plane; the y- and z-axes are not mounted perfectly orthogonal to it (this is why we don't have a full misalignment/nonorthogonality matrix as we will in the accelerometer model). The errors in determining these misalignments are the so-called non-orthogonality errors, expressed as a matrix Γ, as

$$\Gamma \triangleq \begin{bmatrix} 0 & 0 & 0 \\ \gamma_{yx} & 0 & 0 \\ \gamma_{zx} & \gamma_{zy} & 0 \end{bmatrix}$$

The gyro scale factor represents the error in conversion from raw sensor outputs (gyro digitizer pulses) to useful units. In general we model the scale-factor error as a first-order Markov (or a Gauss-Markov) process in terms of a diagonal matrix given as

$$\mathbf{S}^g = \begin{bmatrix} s_x^g & 0 & 0 \\ 0 & s_y^g & 0 \\ 0 & 0 & s_z^g \end{bmatrix}$$

Similarly, the gyro bias errors are modeled as as first-order vector Gauss-Markov processes as

$$b^g = \begin{bmatrix} b_x^g \\ b_y^g \\ b_z^g \end{bmatrix}$$

Finally, the gyro noise is represented by ϵg. Hence

$$\omega_m^\mathcal{C} = (\mathbf{I}_3 + \mathbf{\Gamma} + \mathbf{S}^g) (\omega^\mathcal{C} + b_g + \epsilon_g) \quad (7.17)$$

where I<sup>3</sup> is a 3×3 identity matrix, the superscript C indicates that this is an inertial measurement at the "box-level" expressed in case-frame co-ordinates, and ω C is the 'true' angular velocity in the case frame. If we let <sup>∆</sup><sup>g</sup> <sup>∆</sup><sup>=</sup> <sup>Γ</sup>+<sup>S</sup> g and (I+∆<sup>g</sup> ) <sup>−</sup><sup>1</sup> ≈ I−∆<sup>g</sup> [‡](#page-89-1) , we can express the actual angular

$$(\mathbf{A} + \mathbf{UCV})^{-1} = \mathbf{A}^{-1} - \mathbf{A}^{-1}\mathbf{U}(\mathbf{C}^{-1} + \mathbf{V}\mathbf{A}^{-1}\mathbf{U})^{-1} \mathbf{V}\mathbf{A}^{-1}.$$

$$(\mathbf{I} + \Delta)^{-1} = \mathbf{I} - \Delta (\mathbf{I} + \Delta)^{-1}$$

$$(\mathbf{I} + \Delta)^{-1} = \mathbf{I} - \Delta + \Delta^2 - \Delta^3 + \Delta^4 - \Delta^5 + \dots$$

$$(\mathbf{I} + \Delta)^{-1} \approx \mathbf{I} - \Delta$$

<span id="page-89-1"></span><sup>‡</sup>In order to evaluate (I + ∆) <sup>−</sup><sup>1</sup> we recall the Woodbury matrix identity

Using this, we obtain the following relation (with A = I, U = ∆, C = I and V = I),

which, worked recursively, yields the following approximation

Therefore, to first-order (neglecting second-order and higher terms in the above equation), we get

velocity in terms of the measured angular velocity as

$$\omega^{\mathcal{C}} = (\mathbf{I}_3 - \boldsymbol{\Delta}^g) \omega_{me}^{\mathcal{C}} - \mathbf{b}_g - \epsilon_g \quad (7.18)$$

7.6.2. The Accumulated ∆θ In order to find the accumulated angle (not as a function of the measurement, but purely as a function of the true angular velocity), we define ∆θ as

$$\left(\Delta \theta_{C_{k-1}}^{C_k}\right)_m \triangleq \int_{t_{k-1}}^{t_k} \left\{ \omega_m^C(\tau) + \frac{1}{2} \phi_{C_{ref}}^C \times \omega_m^C(\tau) \right\} d\tau \quad (7.19)$$

$$= \int_{t_{k-1}}^{t_k} \left\{ \omega_m^{\mathcal{C}}(\tau) + \frac{1}{2} \left[ \int_{t_{k-1}}^{\tau} \dot{\phi}_{ref}^{\mathcal{C}}(\chi) d\chi \right] \times \omega_m^{\mathcal{C}}(\tau) \right\} d\tau \quad (7.20)$$

$$= \int_{t_{k-1}}^{t_k} \left\{ \omega_m^c(\tau) + \frac{1}{2} \left[ \int_{t_{k-1}}^{\tau} \left( \omega_m^c(\chi) + \frac{1}{2} \phi_{c_{ref}}^c \times \omega_m^c(\chi) \right) d\chi \right] \times \omega_m^c(\tau) \right\} d\tau$$

Ignoring second-order terms, we get

$$\left( \Delta \theta_{C_{k-1}}^{C_k} \right)_m = \int_{t_{k-1}}^{t_k} \left[ \omega_m^{\mathcal{C}}(\tau) + \frac{1}{2} \int_{t_{k-1}}^{\tau} \omega_m^{\mathcal{C}}(\chi) \, d\chi \times \omega_m^{\mathcal{C}}(\tau) \right] d\tau \quad (7.21)$$

With this expression, we find that, by analogy, we can express ∆θ Ck Ck−<sup>1</sup> as

$$\left( \Delta \theta_{C_{k-1}}^{C_k} \right) = \int_{t_{k-1}}^{t_k} \left[ \omega^C(\tau) + \frac{1}{2} \int_{t_{k-1}}^{\tau} \omega^C(\chi) d\chi \times \omega^C(\tau) \right] d\tau \quad (7.22)$$

7.6.3. The Accelerometer Model The accelerometer package will likely be misaligned relative to the IMU reference frame. This is due to the fact that the three accelerometers (contained in the accelerometer package) are not mounted orthogonal to each other and these errors are expressed in terms of six different small angles as:

$$\Xi^a = \begin{bmatrix} 0 & \xi_{xy} & \xi_{xz} \\ \xi_{yx} & 0 & \xi_{yz} \\ \xi_{zx} & \xi_{zy} & 0 \end{bmatrix}$$

As with the gyros, the accelerometer scale factor represents the error in conversion from raw sensor outputs (accelerometer digitizer pulses) to useful units. In general we model the scale-factor error as a first-order (Gauss-) Markov process in terms of a diagonal matrix given as

$$\mathbf{S}^a = \begin{bmatrix} s_x^a & 0 & 0 \\ 0 & s_y^a & 0 \\ 0 & 0 & s_z^a \end{bmatrix}$$

Similarly, the bias errors are modeled as first-order Gauss-Markov processes as

$$b^a = \begin{bmatrix} b_x^a \\ b_y^a \\ b_z^a \end{bmatrix}$$

So, the accelerometer measurements, a C <sup>m</sup> are modeled as:

$$\mathbf{a}_m^C = (\mathbf{I}_3 + \mathbf{\Xi}^a) (\mathbf{I}_3 + \mathbf{S}^a) (\mathbf{a}^C + b^a + \mathbf{v}_a) \quad (7.23)$$

where I<sup>3</sup> is a 3×3 identity matrix, the superscript C indicates that this is an inertial measurement at the 'box-level' expressed in case-frame co-ordinates, and A<sup>C</sup> is the 'true' non-gravitational acceleration in the case frame. The quantity υ<sup>a</sup> is the velocity random walk, a zero-mean white sequence on acceleration that integrates into a velocity random walk, which is the 'noise' on the accelerometer output. If we assume that the errors are small, then to first-order

$$(\mathbf{I}_3 + \mathbf{\Xi}^a) (\mathbf{I} + \mathbf{S}^a) \approx \mathbf{I} + \mathbf{\Xi}^a + \mathbf{S}^a$$

So, the linear accelerometer measurements (in the case frame) are:

<span id="page-91-1"></span>
$$\mathbf{a}_m^C = (\mathbf{I}_3 + \mathbf{\Xi}^a + \mathbf{S}^a) (\mathbf{a}^C + \mathbf{b}^a + \mathbf{v}_a) \quad (7.24)$$

7.6.4. Accumulated ∆v We note that the measured ∆v in the case frame, ∆v C <sup>m</sup>, is mapped to the end of its corresponding time interval by the sculling algorithm within the IMU firmware, so that we can write

$$(\Delta \mathbf{v}_m^C)_k = \int_{t_{k-1}}^{t_k} \mathbf{T}_{C(t)}^{\mathbf{C}_k} \mathbf{a}_m^{\mathbf{C}(t)} dt \quad (7.25)$$

where ∆v C m k covers the time interval from tk−<sup>1</sup> to t<sup>k</sup> (t<sup>k</sup> > tk−1) and C(t) is the instantaneous case frame[§](#page-91-0) . We recall that a transformation matrix can be written in terms of the Euler axis/angle as

$$T(\phi) = \cos(\phi)\mathbf{I} - \frac{\sin \phi}{\phi} [\phi \times] + \frac{1 - \cos \phi}{\phi^2} \phi \phi^T \quad (7.28)$$

$$= \mathbf{I} - \frac{\sin \phi}{\phi} [\phi \times] + \frac{1 - \cos \phi}{\phi^2} [\phi \times] [\phi \times] \quad (7.29)$$

which, for ϕ ∼ 0, can be approximated as

| $T(\phi) = \mathbf{I} - [\phi \times]$ | (7.30) |
|----------------------------------------|--------|
|----------------------------------------|--------|

With this in mind, T Ck <sup>C</sup>(t) <sup>=</sup> <sup>I</sup><sup>3</sup> − h θ Ck <sup>C</sup>(t)× i , and ∆v C m k , using Eq. [\(7.24\)](#page-91-1), becomes

$$(\Delta \mathbf{v}_m^C)_k = \int_{t_{k-1}}^{t_k} \left[ \mathbf{I}_3 - \left[ \boldsymbol{\theta}_{C(t)}^{\boldsymbol{\theta}_k} \times \right] \right] \left[ (\mathbf{I}_3 + \boldsymbol{\Delta}^a) \mathbf{a}^C + \mathbf{b}^a + \mathbf{v}_a \right] dt \quad (7.31)$$

We can expand this equation, neglecting terms of second-order, as follows

<span id="page-91-2"></span>
$$(\Delta \mathbf{v}_m^C)_k = \int_{t_{k-1}}^{t_k} \left[ \mathbf{I}_3 - \left[ \boldsymbol{\theta}_{C(t)}^C \times \right] \right] \mathbf{a}^C dt + \int_{t_{k-1}}^{t_k} (\mathbf{b}^a + \mathbf{v}_a) dt + \int_{t_{k-1}}^{t_k} \Delta^a \mathbf{a}^C dt \quad (7.32)$$

$$\left( \Delta \mathbf{v}_m^B \right)_k = \int_{t_{k-1}}^{t_k} \mathbf{T}_{B(t)}^{B_k} \mathbf{a}_m^{B(t)} dt \quad (7.26)$$

But since T B<sup>k</sup> <sup>B</sup>(t) ≈ I<sup>3</sup> − h ϕ B<sup>k</sup> <sup>B</sup>(t)× i , we find

$$\left( \Delta \mathbf{v}_m^B \right)_k = \int_{t_{k-1}}^{t_k} \left[ \mathbf{I}_3 - \left[ \boldsymbol{\phi}_{B(t)}^{B_k} \times \right] \right] \mathbf{a}_m^{B(t)} dt \quad (7.27)$$

<span id="page-91-0"></span><sup>§</sup>Or equivalently,

<span id="page-92-0"></span>The first term in the above equation (Eq. [\(7.32\)](#page-91-2)) becomes

$$\int_{t_{k-1}}^{t_k} \left[ \mathbf{I}_3 - \begin{bmatrix} \boldsymbol{\theta}_{C(t)}^{\mathcal{C}_k} \times \end{bmatrix} \right] \mathbf{a}^C dt = (\Delta \mathbf{v}^C)_k \quad (7.33)$$

and the third term becomes

$$\int_{t_{k-1}}^{t_k} \Delta^a \mathbf{a}^c dt = \Delta^a \int_{t_{k-1}}^{t_k} \mathbf{a}^c dt \approx \Delta^a (\Delta \mathbf{v}^c)_k \quad (7.34)$$

Finally, the accelerometer noise, which is a zero-mean process with spectral density S<sup>a</sup> becomes

$$\int_{t_k}^{t_{k+1}} v_a dt = \mathbf{u}_a \quad (7.35)$$

where u<sup>a</sup> is a random vector with covariance Sa(t<sup>k</sup> − tk−1). So, Eq. [\(7.32\)](#page-91-2) becomes

| $(\Delta \mathbf{v}_m^C)_k = [\mathbf{I}_3 + \Delta^a] (\Delta \mathbf{v}^C)_k + b^a \Delta t + \mathbf{v}_a \Delta t$ | (7.36) |
|------------------------------------------------------------------------------------------------------------------------|--------|
|------------------------------------------------------------------------------------------------------------------------|--------|

Since we have established that [I<sup>3</sup> + ∆<sup>a</sup> ] <sup>−</sup><sup>1</sup> ≈ [I<sup>3</sup> − <sup>∆</sup><sup>a</sup> ], and neglecting terms of second-order,

$$(\Delta \mathbf{v}^C)_k = [\mathbf{I}_3 - \Delta^A] (\Delta \mathbf{v}_m^C)_k - b^A \Delta t - \mathbf{v}_a \Delta t \quad (7.37)$$

The average acceleration in the case frame is

$$\mathbf{a}_{ave}^C = \frac{(\Delta \mathbf{v}^C)_k}{\Delta t} \quad (7.38)$$

and the average measured acceleration in the case frame is

$$(\mathbf{a}_m^c)_{ave} = \frac{(\Delta \mathbf{v}_m^c)_k}{\Delta t} \quad (7.39)$$

so we find that

$$\mathbf{a}_{ave}^C = [\mathbf{I}_3 - \Delta^A] (\mathbf{a}_m^C)_{ave} - \mathbf{b}^A - \mathbf{v}_a \quad (7.40)$$

Recalling that the IMU measures accelerations except for gravity, total acceleration is

$$\mathbf{a}^I = \mathbf{g}^I(\mathbf{r}) + \left( \mathbf{T}_{B_{ref}}^I \right)_k \mathbf{T}_B^{B_{ref}} \mathbf{T}_C^B \mathbf{a}_{ave}^C \quad (7.41)$$

7.6.5. The Gravity Call One of the more expensive computations involving the propagation of the trajectory with IMU data is the gravity calculation. This is particularly acute when the gravity field used is of high order. The gravity gradient matrix requires even more computation. Hence it goes without saying that if a way is found to minimize the gravity calls, that would make the navigation software more tractable. Taking advantage of the fact that propagation of the trajectory using IMU data occurs at a high rate (usually at 40 Hz or higher), we expand the gravity vector in terms of a Taylor series about r ∗ as

| $\mathbf{g}(\mathbf{r}) = \mathbf{g}(\mathbf{r}^*) + \frac{\partial \mathbf{g}}{\partial \mathbf{r}} \bigg _{\mathbf{r}=\mathbf{r}^*} [\mathbf{r} - \mathbf{r}^*] + \frac{1}{2} [\mathbf{r} - \mathbf{r}^*]^T \frac{\partial^2 \mathbf{g}}{\partial \mathbf{r}^2} \bigg _{\mathbf{r}=\mathbf{r}^*} [\mathbf{r} - \mathbf{r}^*] + \dots \quad (7.42)$ |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

Knowing that the gravity gradient matrix, G, is

$$\mathbf{G}(\mathbf{r}^*) = \frac{\partial \mathbf{g}}{\partial \mathbf{r}} \bigg|_{\mathbf{r}=\mathbf{r}^*} \quad (7.43)$$

and truncating after the first-order in r, we find that

| $\mathbf{g}(\mathbf{r}) \approx \mathbf{g}(\mathbf{r}^*) + \mathbf{G}(\mathbf{r}^*)[\mathbf{r} - \mathbf{r}^*]$ | (7.44) |
|-----------------------------------------------------------------------------------------------------------------|--------|
|-----------------------------------------------------------------------------------------------------------------|--------|

$$\approx \mathbf{G}(\mathbf{r}^*)\mathbf{r} + [\mathbf{g}(\mathbf{r}^*) - \mathbf{G}(\mathbf{r}^*)\mathbf{r}^*] \quad (7.45)$$

where now the gravity vector and the gravity gradient matrix need only to be evaluated at the beginning of the major cycle.

## <span id="page-94-0"></span>Factorization Methods

Contributed by Christopher D'Souza

Of the various covariance factorization methods[<sup>∗</sup>](#page-94-2) , the UDU covariance factorization technique is among the most commonly used covariance matrix factorization methodologies used in practice. For example, it is implemented in the Goddard Enhanced Onboard Navigation System (GEONS), which has flown on several robotic missions, and is the heart of the Orion Absolute Navigation System. This chapter is intended to present the UDU triangular factorization method and the rationale for its use.

Above all, we demonstrate that the UDU factorization results in a significant reduction in the arithmetic operations (specifically adds and multiplies) compared with the usual (P − <sup>k</sup>+1 = Φ(tk, tk+1)PkΦ<sup>T</sup> (tk, tk+1) + Q<sup>k</sup> ) time update and the Joseph measurement update.

In the next section, we present some notational and preliminary operations for the matrix factors U and D. In the section that follows, we will derive the time update equations for the aforementioned covariance matrix factors. Next, we will derive the measurement update equations for the covariance matrix factors. Finally, we will present some concluding comments.

## 8.1. Why Use the UDU Factorization?

<span id="page-94-1"></span>The usual Kalman filter equations work well for rather simple problems. But once the statespace becomes large, the condition number of the covariance matrix becomes large and nonlinear effects begin to affect the numerical characteristics, problems such as filter divergence and nonpositive definiteness of the covariance matrix occur. These issues began to be observed almost as soon as Kalman filters began to be used in real problems. Matrix factorization techniques were introduced to solve (at least) some of these issues. The earliest was the Potter Square Root Factorization, which was used in the on-board Apollo navigation filters.

In fact Bierman and Thornton, in a 1976 JPL Report, rather cheekily compare those who insist on using the conventional Kalman filtering and batch least-squares algorithms (contra the matrix factorization algorithms) to unrepentant smokers by describing "an attitude often encountered among estimation practitioners [is] that they will switch to the more accurate and stable algorithms if and when numerical problems occur. An analogy comes to mind of a smoker who promises to stop when cancer or heart ailment symptoms are detected. To expand on the analogy, one may note the following:

- Most smokers do not get cancer or heart disease. (Most applications of the Kalman algorithms work.)
- Even when catastrophic illness does not occur, there is diminished health. (Even when algorithms work, performance may be degraded.)

<span id="page-94-2"></span><sup>∗</sup>Other options include the Square Root Covariance Factorization and the Square Root Information Filter (SRIF).

- Smokers can take precautions to lessen the danger, such as smoking low tar or filtered cigarettes. (Engineers can scale their variables to reduce the dynamic range or use double-precision arithmetic.)
- Lung cancer may not be diagnosed until it is too advanced for treatment. (Numerical problems may not be detected in time to be remedied.) " [[83](#page-173-9)]

In addition, a little advertised, but incredibly useful feature of the UDU factorization is the ability to interrogate for the positive definiteness of the covariance matrix for 'free', because the condition required for positive definiteness of P is that the entries of D are positive[††](#page-95-1) .

This sets the stage for the need for the matrix factorization techniques and the UDU technique in particular.

### 8.2. Preliminaries

<span id="page-95-0"></span>Let us factor a covariance matrix, P, into the following form

P = UDU<sup>T</sup> (8.1)

where U is a upper triangular matrix with 1's on the diagonals and 0's on the lower portion of the matrix, D is a diagonal matrix. We can write U and D compactly as

<span id="page-95-2"></span>

| $\mathbf{U} = \{u_{ij}\}, i < j$ | (8.2) |
|----------------------------------|-------|
|----------------------------------|-------|

| $\mathbf{D} = \{d_{ii}\}$ | (8.3) |
|---------------------------|-------|
|---------------------------|-------|

as well

| $u_{ii} = 1$ | (8.4) |
|--------------|-------|
|--------------|-------|

It should be noted that Eq. [\(8.2\)](#page-95-2) gives the upper triangular portion of the covariance; the lower triangular matrix can be obtained by reflection or by evaluation of Eq. [\(8.2\)](#page-95-2), with ulm = 0 for l > m.

With this in hand, the off-diagonal elements of P are

$$p_{ij} = \sum_{k=j}^n u_{ik} d_{kk} u_{jk}, \quad i < j \quad (8.5)$$

and for the diagonals we find,

$$p_{ii} = \sum_{k=j}^n u_{ik}^2 d_{kk} \quad (8.6)$$

$$\mathbf{x}^T \mathbf{P} \mathbf{x} > 0$$

for any x, so that if we can factor the (symmetric) covariance matrix in terms of its eignevectors (E) and eigenvalues (Λ) we find that

$$\mathbf{x}^T\mathbf{P}\mathbf{x} = \mathbf{x}^T\mathbf{E}\mathbf{\Lambda}\mathbf{E}^T\mathbf{x} = \mathbf{y}^T\mathbf{\Lambda}\mathbf{y} > 0$$

where y = E <sup>T</sup>x. As well, we can also factor the covariance matrix in terms of its UDU factors as

$$\mathbf{x}^T \mathbf{P} \mathbf{x} = \mathbf{x}^T \mathbf{U} \mathbf{D} \mathbf{U}^T \mathbf{x} = \mathbf{z}^T \mathbf{D} \mathbf{z} > 0$$

where z = U<sup>T</sup>x. Since, in general U ̸= E, this means that D ̸= Λ and the eigenvalues of P are not the entries of D. However, since D is a diagonal matrix, for positive definiteness of the covariance matrix we must have dii > 0.

<span id="page-95-1"></span><sup>††</sup>The positive definiteness of the covariance matrix, P, can be determined by interrogating the entries of D. It must be noted that the elements of D are not the eigenvalues of P. To see this we begin with the definition of positive definiteness of a matrix

So, given an n×n symmetric, positive semi-definite matrix P, the unit upper triangular factor U and the diagonal factor D (such that P = UDU<sup>T</sup> ) is obtained using the following equations. We begin with the (n, n) element and work upwards (along the columns).

The algorithm is as follows:

for j = n : −1 : 2 do dj,j = pj,j one over d = 0.0 if dj,j > ϵ then one over d = 1.0/djj else dj,j = 0.0 end if uj,j = 1.0 for k = 1 : j − 1 do β = pk,j uk,j = β · one over d for i = 1 : k do pi,k = pi,k − ui,j · β end for end for end for

A word of caution: Maybeck [[60](#page-172-3)] on page 392, rather uncharacteristically, calls the matrix U a unitary matrix, ostensibly because there are 1's on the diagonals. Strictly speaking a if U were a unitary matrix, UU<sup>T</sup> = U<sup>T</sup>U = I, which is clearly not the case for the U in the UDU factorization.

In practice, particularly when storage limitations are driving the design, the n × n matrix D, which is a diagonal matrix comprising of non-zero entries (for a positive definite matrix P), can be stored as a n−vector. Likewise, the matrix n × n matrix U which is upper triangular with 1's on the diagonal, can be stored as a n(n − 1)/2 vector. The storage savings can be particularly significant as n increases. Of course the algorithms need to be designed to ensure that the entries of U above the diagonal are the only ones used in the computations.

## 8.3. The Time Update of the Covariance

<span id="page-96-0"></span>As is necessary in Kalman Filtering, we wish to propagate the UDU factorization of the covariance matrix. We loosely follow Maybeck [[60](#page-172-3)] in this development. First, we will pose the more general problem and then we will specialize it for navigation problems with a large number of sensor biases.

We begin by expressing the equations for the general time update problem. Next, we specialize the general problem to the case where a subset of states, which we will call 'parameters', whose dynamics are uncorrelated with any other state other than themselves. Finally, we present the arithmetic operation (numbers of adds, multiplies, and divides) of the time update of the covariance matrix.

8.3.1. The General Time Update Problem Given a state, x, that evolves according to

$$\mathbf{x}(t_k) = \Phi(t_k, t_{k-1})\mathbf{x}(t_{k-1}) + \mathbf{G}_k \mathbf{w}_k$$

where w<sup>k</sup> is the process noise at time tk, where x is an n × 1 vector, and w is an m × 1 vector. With this in hand, the general problem is as follows [[82](#page-173-10)]: we wish to propagate the covariance matrix defined by

<span id="page-97-0"></span>

| $\bar{\mathbf{P}}(t_k) = \mathbf{\Phi}(t_k, t_{k-1})\mathbf{P}(t_{k-1})\mathbf{F}^{\mathbf{T}}(t_k, t_{k-1}) + \mathbf{G}_k\mathbf{Q}_k\mathbf{G}_k^{-1}$ | (8.7) |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------|-------|
|-----------------------------------------------------------------------------------------------------------------------------------------------------------|-------|

where P is the propagated covariance (the overbar indicates a propagated quantity) and P is the updated covariance at the prior time step, Q<sup>k</sup> is the diagonal process noise covariance matrix and G<sup>k</sup> is the n × m mapping matrix of the noise to the state. To save memory, since Q<sup>k</sup> and D<sup>k</sup> are diagonal matrices, in the implementation, we pass Q<sup>k</sup> and D<sup>k</sup> as vectors.

We want to find the propagated factors U<sup>−</sup> k and D<sup>−</sup> k , such that P − k <sup>∆</sup><sup>=</sup> <sup>U</sup><sup>−</sup> <sup>k</sup> <sup>D</sup><sup>−</sup> <sup>k</sup> U −T k . For compactness, we now drop the time subscripts. Given the UDU factorization of covariance matrices, we can write Eq. [\(8.7\)](#page-97-0) as

<span id="page-97-1"></span>

| $\mathbf{U}_k \mathbf{D}_k \mathbf{U}_k^{-T} = \mathbf{\Phi}_k \mathbf{U}_{k-1} \mathbf{D}_{k-1} \mathbf{U}_{k-1}^T \mathbf{\Phi}_k^T + \mathbf{G}_k \mathbf{Q}_k \mathbf{G}_k^T$ | (8.8) |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|

$$= \begin{bmatrix} \Phi_k \mathbf{U}_{k-1} & \mathbf{G}_k \end{bmatrix} \begin{bmatrix} \mathbf{D}_{k-1} & \mathbf{0} \\ \mathbf{0} & \mathbf{Q}_k \end{bmatrix} \begin{bmatrix} \Phi_k \mathbf{U}_{k-1} & \mathbf{G}_k \end{bmatrix}^T \quad (8.9)$$

Since x is an n×1 vector, and w is an m×1 vector, Φ<sup>k</sup> is an n×n matrix, G<sup>k</sup> is an n×m matrix, and Q<sup>k</sup> is an m × m matrix.

We recall that both U<sup>−</sup> k and Uk−<sup>1</sup> are n×n upper triangular matrices, with 1's on the diagonal and D<sup>−</sup> and D are purely diagonal matrices. So, we have some work to do on Eq, [\(8.9\)](#page-97-1) because -ΦkUk−<sup>1</sup> G<sup>k</sup> is an <sup>n</sup>×(n+m) matrix and Dk−<sup>1</sup> 0 0 Q<sup>k</sup> is an (n+m)×(n+m) diagonal matrix.

Defining the first matrix (-ΦkUk−<sup>1</sup> G<sup>k</sup> which is an n × (n + m) matrix) on the right hand side of Eq.[\(8.9\)](#page-97-1) as

$$\mathbf{Y} \triangleq \begin{bmatrix} \Phi_k \mathbf{U}_{k-1} & \mathbf{G}_k \end{bmatrix} \quad (8.10)$$

we seek a matrix T<sup>k</sup> that transforms Y<sup>k</sup> such that

$$\mathbf{Y}_k \mathbf{T}_k^{-1} = \begin{bmatrix} \mathbf{U}_k^{-1} & \mathbf{0}_{n \times m} \end{bmatrix} \quad (8.11)$$

where U<sup>−</sup> k is an n×n upper triangular matrix with 1's on the diagonal. T<sup>k</sup> is an (n+m)×(n+m) orthogonal matrix with (n + m) × 1 basis vectors b<sup>i</sup> , i = 1, · · · , n + m as

| $\mathbf{T}_k = [ \mathbf{b}_1 \quad \mathbf{b}_2 \quad \mathbf{b}_3 \quad \cdots \quad \mathbf{b}_n \quad \mathbf{b}_{n+1} \quad \cdots \quad \mathbf{b}_{n+m} ]$ | (8.12) |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|

In order to find the desired matrix T<sup>k</sup> we perform a modified weighted Gram-Schmidt orthogonalization[‡](#page-97-2) . We define the diagonal matrix <sup>D</sup>e <sup>k</sup> as

$$\tilde{\mathbf{D}}_k \triangleq \begin{bmatrix} \mathbf{D}_{k-1} & \mathbf{0} \\ \mathbf{0} & \mathbf{Q}_k \end{bmatrix} \quad (8.13)$$

which will be important as we define the weighted inner product in the Gram-Schmidt Orthogonalization. Eq. [\(8.9\)](#page-97-1) which was

$$\mathbf{U}_k \mathbf{D}_k^{-1} \mathbf{U}_k^{-T} = \mathbf{Y}_k \hat{\mathbf{D}}_k \mathbf{Y}_k^T \quad (8.14)$$

can now be rewritten as

| $\mathbf{U}_k \mathbf{D}_k \mathbf{U}_k^{-T}$ | $=$ | $\mathbf{Y}_k \mathbf{T}_k^{-T} \left[ \mathbf{T}_k^T \tilde{\mathbf{D}}_k \mathbf{T}_k \right] \mathbf{T}_k^{-1} \mathbf{Y}_k^{-T}$ | (8.15) |
|-----------------------------------------------|-----|--------------------------------------------------------------------------------------------------------------------------------------|--------|
|-----------------------------------------------|-----|--------------------------------------------------------------------------------------------------------------------------------------|--------|

<span id="page-97-2"></span><sup>‡</sup>Whereas we can use a qr factorization, we specifically perform a modified weighted Gram-Schmidt factorization specialized to the UDU factorization on the non-parameter states.

We note that the matrix h T<sup>T</sup> kDe <sup>k</sup>T<sup>k</sup> i is a diagonal matrix.

"All" that remains is to find Tk. This is where we harness the power of the modified Gram-Schmidt orthogonalization process which provides us with what we were after: U<sup>−</sup> k and D<sup>−</sup> k .

8.3.1.1. The Modified Gram-Schmidt Algorithm

Given the n × (n + m) matrix Y<sup>k</sup> = -ΦkUk−<sup>1</sup> G<sup>k</sup> , ΦkUk−<sup>1</sup> can be constructed taking advantage of the structure of Uk−<sup>1</sup> which is an upper triangular matrix with 1's on the diagonal, with <sup>1</sup> 2 (n <sup>3</sup>−n 2 ) adds and <sup>1</sup> 2 (n <sup>3</sup>−n 2 ) multiplies. We recall that Y<sup>k</sup> is an n×(n+m) matrix and b<sup>i</sup> are the (n + m) × 1 basis vectors. In the following algorithm, the number of adds, multiplies and divides as a consequence of each operation is expressed in terms of '[adds, multiplies, divides]'. We only go to j = 2 because U<sup>−</sup> <sup>11</sup> = 1. The MGS algorithm can be expressed as:

for l = n, · · · , 2 do b<sup>l</sup> = Y<sup>l</sup>

end for

for j = n, · · · , 2 do

<sup>f</sup> <sup>j</sup> <sup>=</sup> Dbe <sup>j</sup> [0, n(<sup>n</sup> <sup>+</sup> <sup>m</sup>), 0]

D<sup>−</sup>

| $\mathbf{D}_{jj}^- = \mathbf{b}_j^T \mathbf{f}_j$ | $[n(n+m), n(n+m), 0]$ |
|---------------------------------------------------|-----------------------|
| $\mathbf{f}_j = \mathbf{f}_j / \mathbf{D}_{jj}^-$ | $[0, 0, (n+m)(n-1)]$  |

T j

f <sup>j</sup> [n(n + m), n(n + m), 0]

for i = 1, · · · , j − 1 do

U<sup>−</sup> ij = b T i

f <sup>j</sup> [(n + m)

(n <sup>2</sup>−n) 2

,(n + m)

(n <sup>2</sup>−n) 2

, 0]

b<sup>i</sup> = b<sup>i</sup> − U<sup>−</sup> end for

ijb<sup>j</sup> [(n + m)

(n <sup>2</sup>−n) 2

,(n + m)

(n <sup>2</sup>−n) 2

, 0]

U<sup>−</sup> <sup>11</sup> = 1 <sup>f</sup> <sup>1</sup> <sup>=</sup> Dbe <sup>1</sup>

D<sup>−</sup> <sup>11</sup> = b end for

T 1 f 1

Thus, the algorithm not only provides the orthogonal basis vectors, b<sup>j</sup> , j = 1, · · · , nx, but it also provides the triangular matrix factors U<sup>−</sup> and D−.

Since we are also interested in the arithmetic operations, we find that there are n 3 <sup>x</sup> + n 2 <sup>x</sup>m<sup>x</sup> adds, nx(n<sup>x</sup> + 1)(n<sup>x</sup> +mx) multiplies and (n<sup>x</sup> +mx)(n<sup>x</sup> −1)divides. For the case when m<sup>x</sup> = 0, i.e. no process noise, we have n 3 x adds and n 3 <sup>x</sup> + n 2 <sup>x</sup> multiplies and n 2 <sup>x</sup> − n<sup>x</sup> divides.

Finally, the entire covariance update algorithm, including the computation of Y<sup>k</sup> uses 1.5n 3 <sup>x</sup>+ 0.5n 2 x (2m<sup>x</sup> −1) adds, 0.5n 2 x (3n<sup>x</sup> + 1)+nxmx(n<sup>x</sup> + 1) mulitplies and (n<sup>x</sup> +mx)(n<sup>x</sup> −1) divides.

The Modified Gram-Schmidt orthogonalization process makes no assumptions regarding the structure of Φ. For a large number of states (say, n<sup>x</sup> = 35 with process noise inputs, m<sup>x</sup> = 35), most of which might be biases (or Gauss Markov processes), much of this is wasted considering the sparseness of Φ. In Appendix B.1, we show that we use [n 3 <sup>x</sup> + n 2 <sup>x</sup>mx] adds and [nx(n<sup>x</sup> + 1)(n<sup>x</sup> + mx)] multiplies to obtain U<sup>−</sup> k and D<sup>−</sup> k . For n<sup>x</sup> = 35 and m<sup>x</sup> = 35, we require 85,750 adds and 88,200 multiplies – quite a large number of computations. We can stop here and all will be well – if we are willing to pay the heavy computational price.

But we can do better! We can vastly improve (reduce) on the number of computations by partitioning the original state vector into 'states' and 'parameters', where the parameters will be modeled as first-order Gauss-Markov processes. Unlike the parameters, the states can vary in any manner. This motivates the next section.

8.3.2. An Improvement for the Case of Parameters As stated earlier, for a large number of states (say, n<sup>x</sup> = 35), the UDU time update for the full covariance matrix (a la Gram-Schmidt ` orthogonalization) is computationally expensive, requiring 2n 3 <sup>x</sup> + 2n 2 <sup>x</sup> multiplies and additions. This is not competitive with the "standard" (P − <sup>k</sup>+1 = Φ(tk, tk+1)P + <sup>k</sup> Φ<sup>T</sup> (tk, tk+1) + GkQkG<sup>T</sup> k ) formulation (which uses 2n 3 <sup>x</sup> multiplies). However, one might guess that an improvement can be made. This is particularly significant because, normally, most of the states are biases or ECRVs (Exponentially Correlated Random Variables) or first-order Gauss-Markov processes. In order to generalize the development, we assume ECRVs for the 'parameter' (or bias) states.

For most space-borne navigation applications, we can usually partition the states into position, velocity, attitude (if applicable) and clock states, all of which we group together and denote as x, and parameter states which usually comprise the sensor biases, scale factors, etc., which we denote as p. This means that the full state space is

$$\mathcal{X} = \begin{bmatrix} \mathbf{x} \\ \mathbf{p} \end{bmatrix} \quad (8.16)$$

The 'states' partition must comprise all those quantities whose time evolution cannot be described as purely self-auto correlated processes. With this in hand, we partition U and D as

$$\mathbf{U} = \begin{bmatrix} \mathbf{U}_{xx} & \mathbf{U}_{xp} \\ \mathbf{0} & \mathbf{U}_{pp} \end{bmatrix} \quad \mathbf{D} = \begin{bmatrix} \mathbf{D}_{xx} & \mathbf{0} \\ \mathbf{0} & \mathbf{D}_{pp} \end{bmatrix} \quad (8.17)$$

Also, partition Φ<sup>k</sup> according to

$$\Phi(t_{k+1}, t_k) = \Phi_k = \begin{bmatrix} \Phi_{xxk} & \Phi_{xpk} \\ 0 & M \end{bmatrix} = \begin{bmatrix} I & 0 \\ 0 & M \end{bmatrix} \begin{bmatrix} \Phi_{xxk} & \Phi_{xpk} \\ 0 & I \end{bmatrix} = \Phi_{2k} \Phi_{1k} \quad (8.18)$$

where M is a diagonal matrix, representing an ECRV whose propagation for p<sup>k</sup> is

$$p_k^- = e^{-\Delta t/\tau} p_{k-1}^+ \quad (8.19)$$

so that

| $\mathbf{M}(i, i) = m_i = e^{-\Delta t/\tau_i}$ | (8.20) |
|-------------------------------------------------|--------|
|-------------------------------------------------|--------|

where τ<sup>i</sup> is the time constant of the i th ECRV state.

Likewise Q<sup>k</sup> is partitioned according to

$$Q_k = \begin{bmatrix} G_{xxk} Q_{xxk} G_{xxk}^T & 0 \\ 0 & Q_{ppk} \end{bmatrix} = \begin{bmatrix} G_{xxk} Q_{xxk} G_{xxk}^T & 0 \\ 0 & 0 \end{bmatrix} + \begin{bmatrix} 0 & 0 \\ 0 & Q_{ppk} \end{bmatrix} \quad (8.21)$$

where we assume that the parameters are ECRVs and hence Qpp is a diagonal matrix.

Recall that the original propagation equation was

| $\mathbf{U}_{k+1}\mathbf{D}_{k+1}\mathbf{U}_{k+1}^T = \mathbf{\Phi}_k\mathbf{U}_k^T\mathbf{D}_k\mathbf{U}_k^{++}\mathbf{\Phi}_k^T + \mathbf{G}_k\mathbf{Q}_k\mathbf{G}_k^T$ | (8.22) |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|

Harnessing the development in Appendix [B.1,](#page-148-1) U<sup>−</sup> <sup>k</sup>+1 <sup>D</sup><sup>−</sup> <sup>k</sup>+1 U −T <sup>k</sup>+1 becomes

| $\mathbf{U}_{k+1} \mathbf{D}_{k+1} \mathbf{U}_{k+1}^T =$ | $\mathbf{U}_{2k} [\mathbf{U}_{1k} \mathbf{U}_{k+1}^T \mathbf{D}_k^T \mathbf{U}_{k+1}^T \mathbf{U}_{1k}^T \mathbf{D}_k^T \mathbf{U}_{1k}^T + \mathbf{Q}_{1k}] \mathbf{U}_{2k}^T + \mathbf{Q}_{2k}$ | (8.23) |
|----------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|
|----------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|

This suggests the following two-step process:

1) Find <sup>U</sup>e and <sup>D</sup>e from

<span id="page-100-0"></span>
$$\tilde{\mathbf{U}}_k \tilde{\mathbf{D}}_k \tilde{\mathbf{U}}_k^\top = \boldsymbol{\Phi}_{1k} \mathbf{U}_k^\top \mathbf{D}_k^+ \mathbf{U}_k^{*\top} \boldsymbol{\Phi}_{1k}^\top + \mathbf{Q}_{1k} \quad (8.24)$$

2) Find U<sup>−</sup> <sup>k</sup>+1 and <sup>D</sup><sup>−</sup> <sup>k</sup>+1 from

<span id="page-100-5"></span>
$$\mathbf{U}_{k+1} \mathbf{D}_{k+1} \mathbf{U}_{k+1}^{-T} = \Phi_{2k} \tilde{\mathbf{U}}_k \tilde{\mathbf{D}}_k \tilde{\mathbf{U}}_k^{-T} \Phi_{2k}^{-1} + \mathbf{Q}_{2k} \quad (8.25)$$

The following sub-sections will describe each of these steps.

8.3.2.1. *The First Sub-Problem* (
$$\Phi_1 \mathbf{U}_k^\top \mathbf{D}_k^\top \mathbf{U}_k^\top \mathbf{T}_1 \Phi_1^\top + \mathbf{Q}_{1k}$$
)

Lets look at 1). The left hand side of Eq. [\(8.24\)](#page-100-0) is

<span id="page-100-1"></span>
$$\tilde{\mathbf{U}}_k \tilde{\mathbf{D}}_k \tilde{\mathbf{U}}_k^\top = \begin{bmatrix} \tilde{\mathbf{U}}_{\mathbf{xx}_k} \tilde{\mathbf{D}}_{\mathbf{xx}_k} \tilde{\mathbf{U}}_{\mathbf{xx}_k}^\top + \tilde{\mathbf{U}}_{\mathbf{xp}_k} \tilde{\mathbf{D}}_{\mathbf{pp}_k} \tilde{\mathbf{U}}_{\mathbf{xp}_k}^\top & \tilde{\mathbf{U}}_{\mathbf{xp}_k} \tilde{\mathbf{D}}_{\mathbf{pp}_k} \tilde{\mathbf{U}}_{\mathbf{pp}_k}^\top \\ \tilde{\mathbf{U}}_{\mathbf{pp}_k} \tilde{\mathbf{D}}_{\mathbf{pp}_k} \tilde{\mathbf{U}}_{\mathbf{xp}_k}^\top & \tilde{\mathbf{U}}_{\mathbf{pp}_k} \tilde{\mathbf{D}}_{\mathbf{pp}_k} \tilde{\mathbf{U}}_{\mathbf{pp}_k}^\top \end{bmatrix} \quad (8.26)$$

The right hand side of Eq. [\(8.24\)](#page-100-0) is

<span id="page-100-2"></span>
$$\tilde{\mathbf{U}}_k \tilde{\mathbf{D}}_k \tilde{\mathbf{U}}_k^T = \begin{bmatrix} \Phi_{\mathbf{xx}_k} \left( \mathbf{U}_{\mathbf{xx}_k}^+ \mathbf{D}_{\mathbf{xx}_k}^+ \mathbf{U}_{\mathbf{xx}_k}^+ + \mathbf{U}_{\mathbf{xp}_k}^+ \mathbf{D}_{\mathbf{pp}_k}^+ \mathbf{U}_{\mathbf{xp}_k}^+ \right) \Phi_{\mathbf{xx}_k}^T & \Phi_{\mathbf{xx}_k} \mathbf{U}_{\mathbf{xp}_k}^+ \mathbf{D}_{\mathbf{pp}_k}^+ \mathbf{U}_{\mathbf{pp}_k}^+ & \Phi_{\mathbf{xp}_k}^T \\ + \Phi_{\mathbf{xx}_k} \mathbf{U}_{\mathbf{xp}_k}^+ \mathbf{D}_{\mathbf{pp}_k}^+ \mathbf{U}_{\mathbf{pp}_k}^+ \Phi_{\mathbf{xp}_k}^T & + \Phi_{\mathbf{xp}_k} \mathbf{U}_{\mathbf{pp}_k}^+ \mathbf{D}_{\mathbf{pp}_k}^+ \mathbf{U}_{\mathbf{pp}_k}^+ & \Phi_{\mathbf{xp}_k}^T \\ + \Phi_{\mathbf{xp}_k} \mathbf{U}_{\mathbf{pp}_k}^+ \mathbf{D}_{\mathbf{pp}_k}^+ \mathbf{U}_{\mathbf{pp}_k}^+ \Phi_{\mathbf{xp}_k}^T & + \Phi_{\mathbf{xp}_k} \mathbf{U}_{\mathbf{pp}_k}^+ \mathbf{D}_{\mathbf{pp}_k}^+ \mathbf{U}_{\mathbf{pp}_k}^+ \Phi_{\mathbf{xp}_k}^T & \Phi_{\mathbf{xp}_k}^T \\ + \Phi_{\mathbf{xp}_k} \mathbf{U}_{\mathbf{pp}_k}^+ \mathbf{D}_{\mathbf{pp}_k}^+ \mathbf{U}_{\mathbf{pp}_k}^+ \Phi_{\mathbf{xp}_k}^T & + \Phi_{\mathbf{xp}_k} \mathbf{U}_{\mathbf{pp}_k}^+ \mathbf{D}_{\mathbf{pp}_k}^+ \mathbf{U}_{\mathbf{pp}_k}^+ \Phi_{\mathbf{xp}_k}^T & \Phi_{\mathbf{xp}_k}^T \\ + \Phi_{\mathbf{xp}_k} \mathbf{U}_{\mathbf{pp}_k}^+ \mathbf{D}_{\mathbf{pp}_k}^+ \mathbf{U}_{\mathbf{xp}_k}^+ \Phi_{\mathbf{xx}_k}^T & + \Phi_{\mathbf{xp}_k} \mathbf{U}_{\mathbf{pp}_k}^+ \mathbf{D}_{\mathbf{pp}_k}^+ \mathbf{U}_{\mathbf{pp}_k}^+ \Phi_{\mathbf{xp}_k}^T & \Phi_{\mathbf{xp}_k}^T \\ + \Phi_{\mathbf{xp}_k} \mathbf{U}_{\mathbf{pp}_k}^+ \mathbf{D}_{\mathbf{pp}_k}^+ \mathbf{U}_{\mathbf{xp}_k}^+ \Phi_{\mathbf{xx}_k}^T & + \Phi_{\mathbf{xp}_k} \mathbf{U}_{\mathbf{pp}_k}^+ \mathbf{D}_{\mathbf{pp}_k}^+ \mathbf{U}_{\mathbf{pp}_k}^+ \Phi_{\mathbf{xp}_k}^T & \Phi_{\mathbf{xp}_k}^T \\ + \Phi_{\mathbf{xp}_k} \mathbf{U}_{\mathbf{pp}_k}^+ \mathbf{D}_{\mathbf{pp}_k}^+ \mathbf{U}_{\mathbf{xp}_k}^+ \Phi_{\mathbf{xx}_k}^T & + \Phi_{\mathbf{xp}_k} \mathbf{U}_{\mathbf{pp}_k}^+ \mathbf{D}_{\mathbf{pp}_k}^+ \mathbf{U}_{\mathbf{pp}_k}^+ \Phi_{\mathbf{xp}_k}^T & \Phi_{\mathbf{xp}_k}^T \\ + \Phi_{\mathbf{xp}_k} \mathbf{U}_{\mathbf{pp}_k}^+ \mathbf{D}_{\mathbf{pp}_k}^+ \mathbf{U}_{\mathbf{xp}_k}^+ \Phi_{\mathbf{xx}_k}^T & + \Phi_{\mathbf{xp}_k} \mathbf{U}_{\mathbf{pp}_k}^+ \mathbf{D}_{\mathbf{pp}_k}^+ \mathbf{U}_{\mathbf{pp}_k}^+ \Phi_{\mathbf{xp}_k}^T & \Phi_{\mathbf{xp}_k}^T \\ + \Phi_{\mathbf{xp}_k} \mathbf{U}_{\mathbf{pp}_k}^+ \mathbf{D}_{\mathbf{pp}_k}^+ \mathbf{U}_{\mathbf{xp}_k}^+ \Phi_{\mathbf{xx}_k}^T & + \Phi_{\mathbf{xp}_k} \mathbf{U}_{\mathbf{pp}_k}^+ \mathbf{D}_{\mathbf{pp}_k}^+ \mathbf{U}_{\mathbf{pp}_k}^+ \Phi_{\mathbf{xp}_k}^T & \Phi_{\mathbf{xp}_k}^T \\ + \Phi_{\mathbf{xp}_k} \mathbf{U}_{\mathbf{pp}_k}^+ \mathbf{D}_{\mathbf{pp}_k}^+ \mathbf{U}_{\mathbf{xp}_k}^+ \Phi_{\mathbf{xx}_k}^T & + \Phi_{\mathbf{xp}_k} \mathbf{U}_{\mathbf{pp}_k}^+ \mathbf{D}_{\mathbf{pp}_k}^+ \mathbf{U}_{\mathbf{pp}_k}^+ \Phi_{\mathbf{xp}_k}^T & \Phi_{\mathbf{xp}_k}^T \\ + \Phi_{\mathbf{xp}_k} \mathbf{U}_{\mathbf{pp}_k}^+ \mathbf{D}_{\mathbf{pp}_k}^+ \mathbf{U}_{\mathbf{xp}_k}^+ \Phi_{\mathbf{xx}_k}^T & + \Phi_{\mathbf{xp}_k} \mathbf{U}_{\mathbf{pp}_k}^+ \mathbf{D}_{\mathbf{pp}_k}^+ \mathbf{U}_{\mathbf{pp}_k}^+ \Phi_{\mathbf{xp}_k}^T & \Phi_{\mathbf{xp}_k}^T \\ + \Phi_{\mathbf{xp}_k} \mathbf{U}_{\mathbf{pp}_k}^+ \mathbf{D}_{\mathbf{pp}_k}^+ \mathbf{U}_{\mathbf{xp}_k}^+ \Phi_{\mathbf{xx}_k}^T & + \Phi_{\mathbf{xp}_k} \mathbf{U}_{\mathbf{pp}_k}^+ \mathbf{D}_{\mathbf{pp}_k}^+ \mathbf{U}_{\mathbf{pp}_k}^+ \Phi_{\mathbf{xp}_k}^T & \Phi_{\mathbf{xp}_k}^T \\ + \Phi_{\mathbf{xp}_k} \mathbf{U}_{$$

Equating each component of the matrix in Eqs [\(8.26\)](#page-100-1) and [\(8.27\)](#page-100-2), we find that the (2, 2) component yields

<span id="page-100-3"></span>
$$\tilde{\mathbf{U}}_{\text{PP}_k} = \mathbf{U}_{\text{PP}_k}^+ \quad (8.28)$$

$$\tilde{\mathbf{U}}_{\text{pp}_k} = \mathbf{U}_{\text{pp}_k}^{+} \quad (8.28)$$

$$\tilde{\mathbf{D}}_{\text{pp}_k} = \mathbf{D}_{\text{pp}_k}^+ \quad (8.29)$$

Equating the (1, 2) (or (2, 1)) component yields

<span id="page-100-4"></span>
$$\bar{\mathbf{U}}_{\mathbf{xp}_k} = \mathbf{F}_{\mathbf{xx}_k} \mathbf{U}_{\mathbf{xp}_k}^+ + \mathbf{F}_{\mathbf{xp}_k} \mathbf{U}_{\mathbf{pp}_k}^+ \quad (8.30)$$

Finally, equating the (1, 1) components of Eqs. [\(8.26\)](#page-100-1) and [\(8.27\)](#page-100-2), and using Eqs. [\(8.28\)](#page-100-3), [\(8.29\)](#page-100-3) and [\(8.30\)](#page-100-4), we find that

$$\tilde{\mathbf{U}}_{xx_{xk}} \tilde{\mathbf{D}}_{xx_{xk}} \tilde{\mathbf{U}}_{xx_{xk}}^T = \mathbf{\Phi}_{xx_{xk}} \mathbf{U}_{xx_{xk}}^T \mathbf{D}_{xx_{xk}}^T \mathbf{U}_{xx_{xk}}^T \mathbf{\Phi}_{xx_{xk}}^T + \mathbf{Q}_{xx_{xk}} \quad (8.31)$$

Since we have partitioned the states such that x comprises the position, velocity, attitude and clock states (or others, as appropriate), we use the modified Gram-Schmidt algorithm to update <sup>U</sup>e xx<sup>k</sup> and <sup>D</sup>e xx<sup>k</sup> . And then we compute <sup>U</sup>e pp<sup>k</sup> , <sup>D</sup>e pp<sup>k</sup> and <sup>U</sup>e xp<sup>k</sup> according to Eqs. [\(8.28\)](#page-100-3) - [\(8.30\)](#page-100-4).

Thus, given n<sup>x</sup> states with m<sup>x</sup> process noise parameters associated with those states, the number of computations associated with the the first sub-problem is: [1.5n 3 <sup>x</sup> + 0.5n 2 x (2m<sup>x</sup> − 1)] adds, [0.5n 2 x (3n<sup>x</sup> + 1) + nxmx(n<sup>x</sup> + 1)] multiplies, and [(n<sup>x</sup> + mx)(n<sup>x</sup> − 1)] divides.

8.3.2.2. The Second Sub-Problem (Φ2k<sup>U</sup>e <sup>k</sup><sup>D</sup>e <sup>k</sup><sup>U</sup>e T kΦ<sup>T</sup> <sup>2</sup><sup>k</sup> + Q2<sup>k</sup> )

Now we look at 2). We now partition <sup>U</sup>e <sup>k</sup> and <sup>D</sup>e <sup>k</sup> as

$$\tilde{\mathbf{U}}_k = \begin{bmatrix} \tilde{\mathbf{U}}_{aa_k} & \tilde{\mathbf{U}}_{ab_k} & \tilde{\mathbf{U}}_{ac_k} \\ \mathbf{0} & 1 & \tilde{\mathbf{U}}_{bc_k} \\ \mathbf{0} & \mathbf{0} & \tilde{\mathbf{U}}_{cc_k} \end{bmatrix} \begin{bmatrix} n_a & & & \\ 1 & & & \\ n_c & & & \end{bmatrix} \text{ and } \tilde{\mathbf{D}}_k = \begin{bmatrix} \tilde{\mathbf{D}}_{aa_k} & \mathbf{0} & \mathbf{0} \\ \mathbf{0} & \tilde{d}_{bk} & \mathbf{0} \\ \mathbf{0} & \mathbf{0} & \tilde{\mathbf{D}}_{cc_k} \end{bmatrix} \begin{bmatrix} n_a \\ 1 \\ n_c \end{bmatrix} \quad (8.32)$$

in order to isolate a parameter. Correspondingly,

| $\Phi_{2k} = \begin{bmatrix} \mathbf{I} & \mathbf{0} & \mathbf{0} \\ \mathbf{0} & 1 & \mathbf{0} \\ \mathbf{0} & \mathbf{0} & \mathbf{M}_{c_k} \end{bmatrix} \begin{bmatrix} \mathbf{I} & \mathbf{0} & \mathbf{0} \\ \mathbf{0} & \mathbf{M}_{b_k} & \mathbf{0} \\ \mathbf{0} & \mathbf{0} & \mathbf{I} \end{bmatrix} = \Phi_{c_k} \Phi_{b_k} \quad (8.33)$ |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

and since the process noise of an ECRV is constant Q2<sup>k</sup> = Q<sup>2</sup> so that Q<sup>2</sup> is

| $Q_2 = \begin{bmatrix} 0 & 0 & 0 \\ 0 & q_b & 0 \\ 0 & 0 & 0 \end{bmatrix} + \begin{bmatrix} 0 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & Q_c \end{bmatrix} = Q_b + Q_c \quad (8.34)$ |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

As in the previous section, we note that Φ−<sup>1</sup> <sup>c</sup><sup>k</sup> <sup>Q</sup>bΦ−<sup>T</sup> <sup>c</sup><sup>k</sup> = Q<sup>b</sup> . So, now Eq. [\(8.25\)](#page-100-5) becomes

<span id="page-101-0"></span>

| $\mathbf{U}_{k+1} \mathbf{D}_{k+1} \mathbf{U}_{k+1}^T = \mathbf{\Phi}_{\mathbf{c}_k} \left[ \mathbf{B}_{b_k} \tilde{\mathbf{U}}_k \tilde{\mathbf{D}}_k \tilde{\mathbf{U}}_k^T \mathbf{\Phi}_{b_k}^T + \mathbf{Q}_b \right] \mathbf{\Phi}_{\mathbf{c}_k}^T + \mathbf{Q}_c$ | (8.35) |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|

The term in the square bracket in Eq. [\(8.35\)](#page-101-0) is

$$\check{\mathbf{U}}_k \check{\mathbf{D}}_k \check{\mathbf{U}}_k^T = \mathbf{\Phi}_{\mathbf{b}_k} \check{\mathbf{U}}_k \check{\mathbf{D}}_k \check{\mathbf{U}}_k^T \mathbf{\Phi}_{\mathbf{b}_k}^T + \mathbf{Q}_b \quad (8.36)$$

In Appendix B, the equation above is expanded until we find that

| $\tilde{\mathbf{U}}_{ac_k} = \tilde{\mathbf{U}}_{ac_k},$ | $\tilde{\mathbf{D}}_{cc_k} = \tilde{\mathbf{D}}_{cc_k},$ | $\tilde{\mathbf{U}}_{cc_k}^T = \tilde{\mathbf{U}}_{cc_k}^T$ | (8.37) |
|----------------------------------------------------------|----------------------------------------------------------|-------------------------------------------------------------|--------|
|                                                          |                                                          |                                                             |        |

Additionally,

<span id="page-101-4"></span>
$$\tilde{\mathbf{U}}_{bc_k} = m_{b_k} \tilde{\mathbf{U}}_{bc_k} \quad (8.38)$$

and

<span id="page-101-2"></span>

| $\tilde{d}_{b_k} = m_{b_k}^2 \tilde{d}_{b_k} + q_b$ | (8.39) |
|-----------------------------------------------------|--------|
|-----------------------------------------------------|--------|

and

<span id="page-101-3"></span>
$$\check{\mathbf{U}}_{\mathbf{ab}_k} = m_{b_k} \frac{\tilde{d}_{b_k}}{\tilde{d}_{b_k}} \check{\mathbf{U}}_{\mathbf{ab}_k} \quad (8.40)$$

Finally, we find that

<span id="page-101-1"></span>
$$\tilde{\mathbf{U}}_{aa_k} \tilde{\mathbf{D}}_{aa_k} \tilde{\mathbf{U}}_{aa_k}^T = \tilde{\mathbf{U}}_{aa_k} \tilde{\mathbf{D}}_{aa_k} \tilde{\mathbf{U}}_{aa_k}^T + \left( \frac{\tilde{d}_{b_k} q_b}{\tilde{d}_{b_k}} \right) \tilde{\mathbf{U}}_{ab_k} \tilde{\mathbf{U}}_{ab_k}^T \quad (8.41)$$

We note that <sup>U</sup>e ab<sup>k</sup> is a column vector (and is thereby of rank 1) so Eq. [\(8.41\)](#page-101-1) constitutes a 'rank one' update. Since ˘db<sup>k</sup> , de bk and q<sup>b</sup> are all positive (assuming mb<sup>k</sup> is a positive quantity), we can use the Agee-Turner Rank One update [[1](#page-170-16)]. It should be pointed out that as the algorithm proceeds down the 'list' of parameters, the size of the states a increases by one (and consequently the size of the parameters c decreases by one. Hence U˘ aa<sup>k</sup> and D˘ aa<sup>k</sup> begins with a dimension of n<sup>x</sup> and concludes with dimension n<sup>x</sup> + n<sup>p</sup> − 1.

Therefore, this is done recursively for all the (sensor) parameters p which are of size np.

#### The Algorithm for <sup>Φ</sup>2k<sup>U</sup>e <sup>k</sup><sup>D</sup>e <sup>k</sup><sup>U</sup>e T kΦ<sup>T</sup> <sup>2</sup><sup>k</sup> + Q2<sup>k</sup>

The algorithm can be expressed as follows (with the arithmetic operations (adds, multiplies, divides) in square brackets per k ):

for 
$$k = 1, \dots, n_p$$
 do  $\check{\mathbf{D}}(n_x + k, n_x + k) = \mathbf{M}(k, k)^2 \check{\mathbf{D}}(n_x + k, n_x + k) + \mathbf{Q}_{pp}(k, k)$  (Eq. (8.39)) [1, 2, 0]

$$\alpha = \mathbf{M}(k, k) \frac{\tilde{\mathbf{D}}(n_{\mathbf{x}}+k, n_{\mathbf{x}}+k)}{\tilde{\mathbf{D}}(n_{\mathbf{x}}+k, n_{\mathbf{x}}+k)} \quad [0, 1, 1]$$

| <b>for</b> $i = 1, \dots, (n_x + k - 1)$                                 | <b>do</b> |                                    |
|--------------------------------------------------------------------------|-----------|------------------------------------|
| $\tilde{\mathbf{U}}(i, n_x + k) = \alpha \tilde{\mathbf{U}}(i, n_x + k)$ |           | (Eq. (8.40)) $[0, n_x + k - 1, 0]$ |

end for

for 
$$j = n_x + k + 1, \dots, (n_x + n_p)$$
 do

| $\text{for } j = n_x + k + 1, \dots, (n_x + n_p) \text{ do}$ |              |                   |
|--------------------------------------------------------------|--------------|-------------------|
| $\tilde{U}(n_x + k, j) = M(k, k)\tilde{U}(n_x + k, j)$       | (Eq. (8.38)) | $[0, n_p - k, 0]$ |

**end for**  
Solve for 
$$\check{\mathbf{U}}_{\mathbf{xx}}^{(k)}, \check{\mathbf{D}}_{\mathbf{xx}}^{(k)}$$
 using<sup>1</sup> the Rank-One update  $[n_{\mathbf{x}} + k]^2, (n_{\mathbf{x}} + k)^2 + 3(n_{\mathbf{x}} + k) + 2, 0$  and for

end for

Thus, the arithmetic operations are as follows:

Adds:

| $n_{\text{p}}$ | $\sum_{k=1}^{n_{\text{p}}} ((n_{\text{x}} + k)^2 + 1) = n_{\text{x}}^2 n_{\text{p}} + n_{\text{p}} + n_{\text{x}}(n_{\text{p}} + 1)n_{\text{p}} + \sum_{k=1}^{n_{\text{p}}} k^2$ | (8.42) |
|----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|
|----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|

Multiplies:

$$\sum_{k=1}^{n_{\text{p}}} (3 + (n_{\text{x}} + k - 1) + n_{\text{p}} - k + (n_{\text{x}} + k)^2 + 3(n_{\text{x}} + k) + 2) = (5.5 + 5n_{\text{x}} + n_{\text{x}}^2)n_{\text{p}} \\ + \frac{1}{2}(2n_{\text{x}} + 5)n_{\text{p}}^2 + \sum_{k=1}^{n_{\text{p}}} k^2 \quad (8.43)$$

and n<sup>p</sup> divides.

## The Agee-Turner Rank One Update Algorithm

Appendix [B.3](#page-150-0) contains the development of the Agee-Turner Rank-One update which is the key to reducing the numerical operations on the UDU Time Update. Given U and D, along with c, and the vector <sup>x</sup>, we are interested in obtaining <sup>U</sup>e and <sup>D</sup>e along the lines of

$$\tilde{\mathbf{U}}\tilde{\mathbf{D}}\tilde{\mathbf{U}}^\top = \mathbf{UD}\mathbf{U}^\top + c_{xx}\mathbf{T} \quad (8.44)$$

where c > 0 is a specified scalar term.

The algorithm to compute <sup>U</sup>eij and <sup>D</sup>eii is:

<span id="page-102-0"></span><sup>1</sup>We are using the nomenclature U(k) and D(k) to denote the upper left n<sup>x</sup> + k − 1 rows and columns of the U and D matrices

$$\mathcal{C}^n = c$$

| $\mathcal{C}^n = c$                              |                                               |
|--------------------------------------------------|-----------------------------------------------|
| <b>for</b> $j = n, \cdots, 2$ <b>do</b>          |                                               |
| $\tilde{D}_{jj} = D_{jj} + \mathcal{C}^j x_j^2,$ | $[n-1, 2(n-1), 0]$                            |
| $\tilde{U}_{jj} = 1$                             |                                               |
| $\beta_j = \mathcal{C}^j / \tilde{D}_{jj}$       | $[0, 0, (n-1)]$                               |
| $v_j = \beta_j x_j$                              | $[0, (n-1), 0]$                               |
| <b>for</b> $i = 1, \cdots, j-1$ <b>do</b>        |                                               |
| $x_i := x_i - U_{ij} x_j$                        | $[\frac{1}{2}(n^2-n), \frac{1}{2}(n^2-n), 0]$ |
| $\tilde{U}_{ij} = U_{ij} + x_i v_j$              | $[\frac{1}{2}(n^2-n), \frac{1}{2}(n^2-n), 0]$ |
| <b>end for</b>                                   |                                               |
| $\mathcal{C}^{j-1} = \beta_j D_{jj}$             | $[0, (n-1), 0]$                               |
| <b>end for</b>                                   |                                               |
| $\tilde{D}_{11} = D_{11} + \mathcal{C}^1 x_1^2$  | $[1, 2, 0]$                                   |

This algorithm has n 2 adds, (n <sup>2</sup> + 3n + 2) multiplies and n − 1 divides.

8.3.3. Arithmetic Operations for Time Update For the time update of the covariance matrix, we have the following arithmetic operations:

Adds : 
$$1.5n_x^3 + n_x^2m_x + n_x^2n_p - 0.5n_x^2 + n_p + n_x(n_p + 1)n_p + \sum_{k=1}^{n_p} k^2$$

Multiplies : 
$$0.5n_x^2(3n_x + 1) + n_x m_x(n_x + 1) + (5.5 + 5n_x + n_x^2)n_p + \frac{1}{2}(2n_x + 5)n_p^2 + \sum_{k=1}^{n_p} k^2$$

Divides : 
$$(n_x + m_x)(n_x - 1) + n_p$$

For n<sup>x</sup> = 9, m<sup>x</sup> = 9, n<sup>p</sup> = 26, we will utilize 16,407 adds, 19,338 multiplies, and 170 divides. In contrast, if we did the MGS on all 35 states (n<sup>x</sup> = 35, m<sup>x</sup> = 35 and n<sup>p</sup> = 0), we would use 85,750 adds, 88,200 multiplies, and 34 divides. Finally, if the covariance were updated (without any consideration given to the structure of Φ<sup>k</sup> from ΦkP − <sup>k</sup> Φ<sup>T</sup> <sup>k</sup> + Q<sup>k</sup> ) in the conventional manner, with n<sup>x</sup> = 35, m<sup>x</sup> = 35, it would cost 84,525 adds, 85,750 multiplies and no divides[†](#page-103-1) . Thus, a very strong case is made for using the UDU factorization and harnessing the benefit of updating the sensor parameters using the Agee-Turner Rank-One update. Thus, the UDU time update taking advantage of the fact that most of the states are sensor parameters results in nearly five times fewer adds and multiplies and 170 more divides that if we operated on the full covariance matrix.

## 8.4. The Measurement Update

<span id="page-103-0"></span>The UDU factorization requires that we process the measurements one-at-a-time [[5](#page-170-1)]. This should not be construed as a weakness of the formulation. If the measurements are correlated, they can be 'decorrelated' as in Appendix [B.4](#page-153-0)

C = AB (8.45)

<span id="page-103-1"></span><sup>†</sup>For matrices, A and B of dimension n × m and m × p, respectively, the product

We remind ourselves that the covariance update equation is

| $P^+ = P^- - \text{KHP}^-$ | (8.46) |
|----------------------------|--------|
|----------------------------|--------|

where K is the Kalman Gain matrix, H is the measurement partial, P <sup>−</sup> is the a priori covariance, and P <sup>+</sup> is the a posteriori covariance matrix. Using the covariance factors U and D, we rewrite the above equation as

<span id="page-104-0"></span>
$$\mathbf{U}^{\dagger \dagger} \mathbf{D}^{\dagger} \mathbf{U}^{\dagger \dagger} = \mathbf{U}^{-\dagger} \mathbf{D}^{-\dagger} \mathbf{U}^{-\dagger} - \mathbf{K} \mathbf{H} \mathbf{U}^{-\dagger} \mathbf{D}^{-\dagger} \mathbf{U}^{-\dagger} \quad (8.47)$$

We note that U and U<sup>−</sup> and D and D<sup>−</sup> are n×n matrices, and because we are using the paradigm of processing the measurements one at a time, H is an 1 × n vector and K is an n × 1 vector. Recalling that K is defined as

$$\mathbf{K} = \mathbf{P}^{-\mathbf{H}^T} (\mathbf{H}\mathbf{P}^{-\mathbf{H}^T} + \mathbf{R})^{-1} = \frac{\mathbf{U}^{-} \mathbf{D}^{-} \mathbf{U}^{-T} \mathbf{H}^T}{\mathbf{H}\mathbf{U}^{-} \mathbf{D}^{-} \mathbf{U}^{-T} \mathbf{H}^T + \mathbf{R}} = \frac{\mathbf{U}^{-} \mathbf{D}^{-} \mathbf{U}^{-T} \mathbf{H}^T}{\alpha} \quad (8.48)$$

where the scalar α is defined to be

$$\alpha \triangleq \mathbf{H}\mathbf{U}^{-1}\mathbf{D}^{-1}\mathbf{U}^{-1}\mathbf{H}^T + \mathbf{R} \quad (8.49)$$

We find that Eq. [\(8.47\)](#page-104-0) becomes

<span id="page-104-1"></span>
$$\mathbf{U}^+\mathbf{D}^+\mathbf{U}^{+\top} = \mathbf{U}^- \left[ \mathbf{D}^- - \frac{\mathbf{D}^- \mathbf{U}^{-\top} \mathbf{H}^\top}{\alpha} \mathbf{H} \mathbf{U}^- \mathbf{D}^- \right] \mathbf{U}^{-\top} \quad (8.50)$$

If we define the n × 1 vector v as

| $\mathbf{v} \triangleq \mathbf{D}^{-1} \mathbf{U}^{-1} \mathbf{H}^T$ | (8.51) |
|----------------------------------------------------------------------|--------|
|----------------------------------------------------------------------|--------|

Eq. [\(8.50\)](#page-104-1) becomes

<span id="page-104-2"></span>
$$\mathbf{U}^{+\mathbf{D}+\mathbf{D}+\mathbf{U}^{+\mathbf{T}}} = \mathbf{U}^{-} \left[ \mathbf{D}^{-} - \frac{1}{\alpha} \mathbf{v}\mathbf{v}^{\mathbf{T}} \right] \mathbf{U}^{-\mathbf{T}} \quad (8.52)$$

We now analyze the bracketed term in Eq. [\(8.52\)](#page-104-2) and find that we can define

<span id="page-104-3"></span>
$$\tilde{\mathbf{U}}\tilde{\mathbf{D}}\tilde{\mathbf{U}}^{\text{T}} \triangleq \mathbf{D}^{-1} \frac{1}{\alpha} \mathbf{v} \mathbf{v}^{\text{T}} \quad (8.53)$$

Therefore,

| $\mathbf{U}^+ = \mathbf{U}^- \tilde{\mathbf{U}}$ | and | $\mathbf{D}^+ = \tilde{\mathbf{D}}$ | (8.54) |
|--------------------------------------------------|-----|-------------------------------------|--------|
|                                                  |     |                                     |        |

So, how do we proceed? This has all the marks of a rank-one update, for after all v is of rank one. We can proceed by using the Agee-Turner rank-one update. Except for one thing – that pesky minus sign in Eq. [\(8.53\)](#page-104-3). That minus sign portends all sorts of numerical issues because there is a possibility that we can lose numerical precision if the Agee-Turner update is used blindly. It turns out that we can have 'our cake and eat it too'; Neil Carlson developed a rank-one update to precisely remedy our issue. The mathematical development of this algorithm is detailed in Appendix [B.5.](#page-153-1)

The algorithm is as follows: Given U−, D−, R, and H

$$\mathbf{f} = \mathbf{U}^{-T}\mathbf{H}^T \quad \text{where} \quad \mathbf{f} = \begin{bmatrix} f_1 & f_2 & \cdots & f_n \end{bmatrix}^T \quad \begin{bmatrix} \frac{1}{2}(n_x^2 - n_x), & \frac{1}{2}(n_x^2 - n_x), & 0 \end{bmatrix}, \\ \mathbf{v} = \mathbf{D}^{-T}\mathbf{f} \quad \text{where} \quad \mathbf{v} = \begin{bmatrix} \bar{d}_1 f_1 & \bar{d}_2 f_2 & \cdots & \bar{d}_n f_n \end{bmatrix}^T, \\ \bar{\mathbf{K}}_1 = \begin{bmatrix} v_1 & 0 & \cdots & \bar{0} \end{bmatrix}^T, \\ \alpha_1 = \mathbf{R} + v_1 f_1 & & & & [1, 1, 0] \end{bmatrix}.$$

$$d_1 = \left(\frac{\mathbf{R}}{\alpha_1}\right) \bar{d}_1$$

| $d_1 = \left(\frac{\mathbf{R}}{\alpha_1}\right) \bar{d}_1$           | $[0, 1, 1]$                                                                                           |
|----------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|
| <b>for</b> $j = 2, \dots, n$ <b>do</b>                               |                                                                                                       |
| $\alpha_j = \alpha_{j-1} + v_j f_j$                                  | $[n_{\mathbf{x}} - 1, n_{\mathbf{x}} - 1, 0]$                                                         |
| $d_j = \left(\frac{\alpha_{j-1}}{\alpha_j}\right) \bar{d}_j$         | $[0, n_{\mathbf{x}} - 1, n_{\mathbf{x}} - 1]$                                                         |
| $\lambda_j = -(f_j/\alpha_{j-1})$                                    | $[0, 0, n_{\mathbf{x}} - 1]$                                                                          |
| $\mathbf{U}_j^+ = \mathbf{U}_j^- + \lambda_j \bar{\mathbf{K}}_{j-1}$ | $[\frac{1}{2}(n_{\mathbf{x}}^2 - n_{\mathbf{x}}), \frac{1}{2}(n_{\mathbf{x}}^2 - n_{\mathbf{x}}), 0]$ |
| $\bar{\mathbf{K}}_j = \bar{\mathbf{K}}_{j-1} + v_j \mathbf{U}_j^-$   | $[\frac{1}{2}(n_{\mathbf{x}}^2 - n_{\mathbf{x}}), \frac{1}{2}(n_{\mathbf{x}}^2 - n_{\mathbf{x}}), 0]$ |
| <b>end for</b>                                                       |                                                                                                       |
| $\mathbf{K} = \bar{\mathbf{K}}_n/\alpha$                             | $[0, 0, n_{\mathbf{x}}]$                                                                              |

Thus, taking advantage of the triangularity of the U<sup>−</sup> matrix (and the fact that U <sup>−</sup><sup>T</sup>H<sup>T</sup> and λjKj−<sup>1</sup> and vjU<sup>−</sup> j use nx(n<sup>x</sup> −1)/2multiplies and adds), for each measurement processed, the covariance update results in 1.5n 2 <sup>x</sup> − 0.5n<sup>x</sup> adds, 1.5n 2 <sup>x</sup> + 1.5n<sup>x</sup> multiplies and 3n<sup>x</sup> − 1 divides.

For the normal, Joseph Kalman filter update, for a scalar measurement, we find that if we use efficient methods of calculating and storing quantities [[5](#page-170-1)], we use 4.5n 2 <sup>x</sup>+3.5n<sup>x</sup> adds, 4n 2 <sup>x</sup>+4.5n<sup>x</sup> multiplies and 1 divide.

For the "Conventional" Kalman filter update (P = P <sup>−</sup> − KHP<sup>−</sup> in Eq.(61)), for a scalar measurement, we find that [[5](#page-170-1)] we use 1.5n 2 <sup>x</sup> + 1.5n<sup>x</sup> adds, 1.5n 2 <sup>x</sup> + 0.5n<sup>x</sup> multiplies and 1 divide.

Thus, for n<sup>x</sup> = 35, the covariance update due to measurement processing with the UDU factorization uses 1820 adds, 1890 divides and 104 divides compared with 5635 adds, 5058 multiplies and 1 divide for the efficient Joseph update. The "Conventional" Kalman update uses 1890 adds, 1855 multiplies, and 1 divide.

Hence there is almost a factor of 2.5 improvement in the adds and multiplies using the triangular (UDU) update compared with the Joseph update. This rivals the efficiency of the "conventional" Kalman Filter update.

8.4.1. Consider Covariance and its Implementation in the UDU Filter 'Consider' Analysis was first introduced by S. F. Schmidt of NASA Ames in the mid 1960s as a means to account for errors in both the dynamic and measurement models due to uncertain parameters [[75](#page-173-5)]. The Consider Kalman Filter, also called the Schmidt-Kalman Filter, resulted from this body of work. The consider approach is especially useful when parameters have low observability.

We partition the state-vector, x into the ns"estimated states", s, and the n<sup>p</sup> "consider" parameters, p, as

$$\mathbf{x} \triangleq \begin{bmatrix} \mathbf{s} \\ \mathbf{p} \end{bmatrix} \quad (8.55)$$

so that

$$\mathbf{P} = \begin{bmatrix} \mathbf{P}_{ss} & \mathbf{P}_{sp} \\ \mathbf{P}_{ps} & \mathbf{P}_{pp} \end{bmatrix}, \quad \mathbf{H} = \begin{bmatrix} \mathbf{H}_s & \mathbf{H}_p \end{bmatrix} \quad (8.5)$$

$$\mathbf{K}_{opt} = \begin{bmatrix} \mathbf{K}_{s,opt} \\ \mathbf{K}_{p,opt} \end{bmatrix} = \begin{bmatrix} \mathbf{P}_{ss}^{-1} \mathbf{H}_s^\top + \mathbf{P}_{sp}^{-1} \mathbf{H}_p^\top \\ \mathbf{P}_{ps}^{-1} \mathbf{H}_s^\top + \mathbf{P}_{pp}^{-1} \mathbf{H}_p^\top \end{bmatrix} \mathbf{W}^{-1} \quad (8.57)$$

where Kopt is the optimal Kalman gain computed for the full state, x, and W is

| <b>W</b> | <b>=</b> | $\mathbf{H_SP_{SS}H_S^T} + \mathbf{H_SP_{SP}H_P^T} + \mathbf{H_PP_{PS}H_S^T} + + \mathbf{H_PP_{PP}H_P^T}$ | (8.5) |
|----------|----------|-----------------------------------------------------------------------------------------------------------|-------|
|----------|----------|-----------------------------------------------------------------------------------------------------------|-------|

Therefore, if we now choose the K<sup>s</sup> and K<sup>p</sup> carefully such that the K<sup>s</sup> = Ks,opt, the a posteriori covariance matrix is

$$\mathbf{P}^+ = \begin{bmatrix} \mathbf{P}_{\text{ss}}^- - \mathbf{K}_s \mathbf{W}\mathbf{K}_s^\top & \mathbf{P}_{\text{sp}}^- - \mathbf{K}_s \mathbf{H} \begin{bmatrix} \mathbf{P}_{\text{sp}}^- \\ \mathbf{P}_{\text{pp}}^- \end{bmatrix} \\ \mathbf{P}_{\text{ps}}^- - \begin{bmatrix} \mathbf{P}_{\text{sp}}^- \\ \mathbf{P}_{\text{pp}}^- \end{bmatrix}^\top \mathbf{H}^\top \mathbf{K}_s^\top & \mathbf{P}_{\text{pp}}^- - \mathbf{K}_p \mathbf{W}\mathbf{K}_p^\top \end{bmatrix} \quad (8.59)$$

This equation is valid for any value of Kp. Notice that there is no K<sup>p</sup> in the correlation terms of the covariance matrix. Therefore, what is remarkable about this equation is that once the optimal K<sup>s</sup> is chosen, the correlation between s and p is independent of the choice of Kp.

In its essence, the consider parameters are not updated; therefore, the Kalman gain associated with the consider parameters, p, is zero, i.e. K<sup>p</sup> = 0. However, several comments are in order:

- (1) When using the Schmidt-Kalman filter, the a priori and a posteriori covariance of the parameters (Ppp) are the same.
- (2) The a posteriori covariance matrix of the states and the correlation between the states and the parameters are the same regardless of whether one uses the Schmidt-Kalman filter or the optimal Kalman update

Therefore, the consider covariance, P + con is

$$\mathbf{P}_{con}^+ = \begin{bmatrix} \mathbf{P}_{ss}^- - \mathbf{K}_s \mathbf{W} \mathbf{K}_s^\top & \mathbf{P}_{sp}^- - \mathbf{K}_s \mathbf{H} \begin{bmatrix} \mathbf{P}_{sp}^- \\ \mathbf{P}_{BS}^- \end{bmatrix} \\ \mathbf{P}_{ps}^- - \begin{bmatrix} \mathbf{P}_{sp}^- \\ \mathbf{P}_{pp}^- \end{bmatrix}^\top \mathbf{H}^\top \mathbf{K}_s^\top & \mathbf{P}_{pp}^- \end{bmatrix} \quad (8.60)$$

Of course, the "full" optimal covariance matrix update is

$$\mathbf{P}_{opt}^+ = \begin{bmatrix} \mathbf{P}_{ss}^- - \mathbf{K}_{s,opt} \mathbf{W}_{s,opt}' & \mathbf{P}_{sp}^- - \mathbf{K}_{s,opt} \mathbf{H} \begin{bmatrix} \mathbf{P}_{sp}^- \\ \mathbf{P}_{pp}^- \end{bmatrix} \\ \mathbf{P}_{ps}^- - \begin{bmatrix} \mathbf{P}_{sp}^- \\ \mathbf{P}_{pp}^- \end{bmatrix}^\top \mathbf{H}^\top \mathbf{K}_{s,opt}' & \mathbf{P}_{pp}^- - \mathbf{K}_{p,opt} \mathbf{W}_{p,opt}' \end{bmatrix} \quad (8.61)$$

The UDU formulation, while numerically stable and tight, is quite inflexible to making any changes in the framework. At first blush, it would seem that the consider analysis would not fit into the framework. However, all is not in vain. With some clever rearrangements, we can allow for a rank-one update to include consider states in the measurement update. The measurement update, expressed in terms of the consider covariance [[92](#page-173-11)], is

<span id="page-106-0"></span>
$$\mathbf{P}_{opt}^+ = \mathbf{P}_{con}^+ - (\mathbf{SK}_{opt}) \mathbf{W} (\mathbf{SK}_{opt})' \quad (8.62)$$

where S is an n<sup>x</sup> × n<sup>x</sup> matrix (defining n<sup>x</sup> <sup>∆</sup><sup>=</sup> <sup>n</sup><sup>s</sup> <sup>+</sup> <sup>n</sup>p, where <sup>n</sup><sup>x</sup> is the total number of states, <sup>n</sup><sup>p</sup> is the number of consider states, and n<sup>s</sup> is the number of "non-consider" states) defined as

$$\mathbf{S} \triangleq \begin{bmatrix} \mathbf{0}_{n_s \times n_s} & \mathbf{0}_{n_s \times n_p} \\ \mathbf{0}_{n_p \times n_s} & \mathbf{I}_{n_p \times n_p} \end{bmatrix} \quad (8.63)$$

Since we are processing scalar measurements, we note that W = 1 α is a scalar and Kopt is an n<sup>x</sup> ×1 vector. Therefore SKopt is an n<sup>x</sup> ×1 vector. Therefore, solving for the consider covariance,

$$\mathbf{P}_{con}^+ = \mathbf{P}_{opt}^+ + W(\mathbf{SK}_{opt})(\mathbf{SK}_{opt})^T \quad (8.64)$$

Eq. [\(8.62\)](#page-106-0) has the same form as the original rank-one update i.e. P <sup>+</sup> = P <sup>−</sup>+caa<sup>T</sup> , with a = SKopt and c = 1 α . With this in mind, we can use the (un-modified) rank-one update which is a backwardrecursive update [[1](#page-170-16)]. If, for example, all the consider parameters are in the lower part of the statespace, we can effectively reduce the computations by ending the update when the covariance of the state of the last consider parameter is updated.

Therefore, the procedure is as follows: first perform a complete Carlson rank-one measurement update with the optimal Kalman Gain (Kopt) on the full covariance matrix. Second, perform another rank-one update with a = SKopt and c = 1 α , according to the Agee-Turner rank-one update (as in Table 1).

Therefore, since there is an additional rank-one update associated with the consider states and if no rearrangements of the consider states are performed, then there will be an additional n 2 x adds, n 2 <sup>x</sup> + 3n<sup>x</sup> + 2 multiplies, and n<sup>x</sup> − 1 divides per measurement.

The use of the "consider state" option, if it is exercised, is likely to be used in "consider"ing the attitude states, particularly during entry. The rationale for this is that in certain degenerate cases, like when GPS satellites are reacquired after entry blackout, the attitude estimate could be adversely affected. So, to protect against this, the "consider" option may be exercised with respect to the attitude states.

## 8.5. Conclusions

<span id="page-107-0"></span>Matrix factorization methods, particularly the UDU factorization, are very useful – indeed essential – for onboard navigation algorithms. They are numerically stable and computationally efficient, competitive with the classic Kalman filter implementation. In addition, they allow the navigation designer to investigate the positive definiteness of the covariance matrix for "free," since by inspecting the entries of D, if any elements of D are negative, then the covariance matrix will not be positive semi-definite.

## Attitude Estimation

Contributed by F. Landis Markley

<span id="page-108-0"></span>The particular complications of attitude estimation arise from a fundamental difference between rotational kinematics and translational kinematics. The translational state of motion can be completely specified in a nonsingular way by the cartesian components of the position vector r(t) and the velocity vector v(t). The integral of any reasonable function v(t) between two times gives the translational displacement of r(t) between these two times. Other parameterizations of the translational state may be singular; the classical Keplerian orbit elements are singular for zero inclination or zero eccentricity, for example. It is the case, however, that globally nonsingular six-parameter representations exist.

Rotations in three-dimensional space have three degrees of freedom, just like translations in three dimensions, and the angular velocity vector ω(t) is the rotational analog of the velocity vector. However, two different time histories ω(t) that have the same integral over a time interval can result in different rotational displacements over the interval. This is because the order in which rotations are performed is significant, unlike the order in which translations are performed. Thus integration of ω(t) does not result in a three-vector rotational analog of the position vector. In fact, it can be proven that no global three-component parameterization of rotations without singular points exists [[80](#page-173-12)]. Rotational analysis is forced to deal with either higher-dimensional representations of rotations or with three-dimensional representations possessing singularities or discontinuities. The following seven sections will briefly present a nine-parameter representation, two four-parameter representations, and five three-parameter representations. Fuller discussions can be found in Refs. [[59](#page-172-10),[78](#page-173-13)]. The discussion of attitude representations is followed by two sections on extended Kalman filters for attitude estimation.

## 9.1. Attitude Matrix Representation

<span id="page-108-1"></span>Attitude representations are the methods of representing the orientation of an orthonormal triad of basis vectors in one reference frame with respect to an orthonormal triad in some other reference frame. The attitude matrix, in particular, represents the orientation of a vehicle's body frame with respect to a frame that is often, but not always, an inertial frame. The attitude determination of earth-pointing spacecraft, for example, typically employs a reference frame in which one basis vector is pointed from the spacecraft toward the center of the earth and another points opposite to the orbital angular velocity. The body frame of a rigid vehicle is simply defined as a frame fixed in the vehicle. No vehicle is completely rigid, though, so it is quite common to define the body frame operationally as the orientation of some navigation base, a sufficiently rigid subsystem of the spacecraft including the most critical attitude sensors and payload instruments.

For actual applications, representations are 3×3 matrices that transform the representations of vectors in one frame, i.e. their components along the basis vectors in that frame, to their representations in a different frame. Thus attitude representations describe a fixed physical vector in a rotated frame rather than a rotated vector. This is the passive interpretation of a transformation, also known as the alias sense (from the Latin word for "otherwise," in the sense of "otherwise known as") [[78](#page-173-13)]. The alternative active interpretation (also known as the alibi sense from the Latin word for "elsewhere") considers the representation in a fixed reference frame of a rotated physical vector. It is crucial to keep this distinction in mind, because an active rotation in one direction corresponds to a passive rotation in the opposite direction. Overlooking this point has led to errors in flight software.[<sup>1</sup>](#page-109-0)

Now consider transforming the representation of a vector $\vec{x}$ in a frame F to its representation in a frame G and then from frame G to frame H or directly from frame F to frame H, so

$$\mathbf{x}_{\mathcal{H}} = \mathbf{A}_{\mathcal{H}}\mathbf{x}_{\mathcal{G}} = \mathbf{A}_{\mathcal{H}}(\mathbf{A}_{\mathcal{G}}\mathbf{x}_{\mathcal{F}}) = \mathbf{A}_{\mathcal{H}}\mathbf{x}_{\mathcal{F}} \quad (9.1)$$

These transformations must be equivalent for any vector x<sup>F</sup> , so successive transformations are accomplished by simple matrix multiplication:

<span id="page-109-1"></span>AHF = AHGAGF (9.2)

This may appear to be an obvious result, but only one other attitude representation has such a simple composition rule. Matrix multiplication is associative, meaning that AHG(AGFAFE ) = (AHGAGF )AFE . Matrix multiplication is not commutative, however, which means that AHGAGF ̸= AGFAHG in general. The non-commutativity of matrix multiplication is at the heart of the problem of finding a suitable attitude representation.

Transforming from frame F to frame G and back to frame F is effected by the matrix AF F = AFGAGF , which must be the identity matrix. Rotations must also preserve inner products and norms of vectors, so

| $\mathbf{x}_f \cdot \mathbf{y}_f = \mathbf{x}_g \cdot \mathbf{y}_g = (\mathbf{A}_{ff} \mathbf{x}_f)^T \mathbf{A}_{fg} \mathbf{y}_f = \mathbf{x}_f^T \mathbf{A}_{gf}^T \mathbf{A}_{gf} \mathbf{y}_f$ | (9.3) |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|

These two observations mean that

$$\mathbf{A}_{GF}^\top = \mathbf{A}_{GF}^{-1} = \mathbf{A}_{FG} \quad (9.4)$$

A matrix with its transpose is equal to its inverse is called an orthogonal matrix, and its determinant must equal ±1. The attitude matrix must be a proper orthogonal matrix, i.e. have determinant +1, in order to transform a right-handed coordinate frame to a right-handed coordinate frame.

The nine-component attitude matrix is in some ways the ideal representation of a vehicle's attitude. It has a 1:1 correspondence with physical attitudes, it varies smoothly as the physical attitude varies smoothly, its elements all have magnitudes less than or equal to one, and it follows a simple rule for combining successive rotations. It is not an efficient representation, though; only three of its nine parameters are independent because the orthogonality constraint is equivalent to six independent scalar constraints. This provides the opportunity to specify an attitude or an attitude matrix using only three parameters, but not, as was pointed out above, in a globally continuous and nonsingular fashion.

<span id="page-109-0"></span><sup>1</sup>One example is an incorrect sign for the velocity aberration correction for star tracker measurements on the Wilkinson Microwave Anisotropy Probe (WMAP) spacecraft, which fortunately was easily corrected.

#### 9.2. Euler Axis/Angle Representation

<span id="page-110-0"></span>The Euler axis/angle representation of a rotation matrix is based on Euler's Theorem, which states that the general displacement of a rigid body with one point fixed is a rotation about a fixed axis [[29](#page-171-15)]. Specify the axis by a unit vector $\vec{e}$ and the rotation angle by ϑ, and denote the matrix that maps the representations of vectors from frame F to frame G by AGF (e, ϑ). The rotation axis is fixed, so e can be its representation in either frame F or frame G, which are identical. Consider the mapping of a vector $\vec{x}$ whose representation in frame F is

| $\mathbf{x}_{\mathcal{F}} = (\mathbf{e}\mathbf{e}^T)\mathbf{x}_{\mathcal{F}} + (\mathbf{I}_3 - \mathbf{e}\mathbf{e}^T)\mathbf{x}_{\mathcal{F}}$ | (9.5) |
|-------------------------------------------------------------------------------------------------------------------------------------------------|-------|
|-------------------------------------------------------------------------------------------------------------------------------------------------|-------|

where I<sup>n</sup> denotes the n×n identity matrix. The first term on the right side is parallel and the second is perpendicular to to the rotation axis. The rotation does not affect the parallel component and rotates the perpendicular component through an angle ϑ around the rotation axis out of the plane defined by that axis and x<sup>F</sup> , so

<span id="page-110-1"></span>
$$\mathbf{x}_G = \mathbf{A}_G(\mathbf{e}, \vartheta)\mathbf{x}_F = (\mathbf{e}^T)\mathbf{x}_F + \cos \vartheta(\mathbf{I}_3 - \mathbf{e}^T)\mathbf{x}_F - \sin \vartheta(\mathbf{e} \times \mathbf{x}_F) \quad (9.6)$$

This formula preserves the norm of x<sup>F</sup> because e×x<sup>F</sup> and (I3−e e<sup>T</sup> )x<sup>F</sup> are orthogonal and have equal magnitude. Since x<sup>F</sup> is an arbitrary vector, Eq. [\(9.6\)](#page-110-1) means that

<span id="page-110-2"></span>

| $\mathbf{A}(\mathbf{e}, \vartheta) = (\cos \vartheta) \mathbf{I}_3 - \sin \vartheta [\mathbf{e} \times] + (1 - \cos \vartheta) \mathbf{e} \mathbf{e}^T$ | (9.7) |
|---------------------------------------------------------------------------------------------------------------------------------------------------------|-------|
|---------------------------------------------------------------------------------------------------------------------------------------------------------|-------|

where [e×] is the cross-product matrix:

| $[\mathbf{e} \times] \equiv \begin{bmatrix} 0 & -e_3 & e_2 \\ e_3 & 0 & -e_1 \\ -e_2 & e_1 & 0 \end{bmatrix}$ | (9.8) |
|---------------------------------------------------------------------------------------------------------------|-------|
|---------------------------------------------------------------------------------------------------------------|-------|

The cross-product matrix is defined so that [x×] y = x×y. Equation [\(9.7\)](#page-110-2) is the Euler axis/angle parameterization of an attitude matrix, with explicit frame indices omitted. It requires four parameters, but only three are independent because of the unit vector constraint ∥e∥ = 1.

The sin ϑ terms in Eqs. [\(9.6\)](#page-110-1) and [\(9.7\)](#page-110-2) are negative because the rotation in Euler's theorem is an active rotation of the frame G relative to the frame F, while the rotation matrix A(e, ϑ) specifies the passive mapping of the representation of $\vec{x}$ from frame F to frame G.

The Euler axis/angle representation can be used to find the time dependence of the rotation matrix. The fundamental definition of a derivative gives

$$\begin{aligned} \dot{\mathbf{A}}_{\mathcal{GF}}(t) &\equiv \lim_{\Delta t \rightarrow 0} \frac{\mathbf{A}_{\mathcal{GF}}(t + \Delta t) - \mathbf{A}_{\mathcal{GF}}(t)}{\Delta t} \\ &= \left( \lim_{\Delta t \rightarrow 0} \frac{\mathbf{A}_{\mathcal{GF}}(t + \Delta t) \mathbf{A}_{\mathcal{G}}(t) - \mathbf{I}_3}{\Delta t} \right) \mathbf{A}_{\mathcal{GF}}(t) \end{aligned} \quad (9.9)$$

because AFG(t)AGF (t) is equal to the identity matrix. For small ∆t, the matrix product AGF (t+ ∆t)AFG(t) differs from the identity matrix by a small rotation, so it can be represented by a small angle approximation of Eq. [\(9.7\)](#page-110-2):

| $\mathbf{A}_{\mathcal{F}}(t + \Delta t)\mathbf{A}_{\mathcal{F}}(t) \approx \mathbf{I}_3 - \vartheta [\mathbf{e} \times]$ | (9.10) |
|--------------------------------------------------------------------------------------------------------------------------|--------|
|--------------------------------------------------------------------------------------------------------------------------|--------|

Inserting this into Eq. [\(9.9\)](#page-110-3), taking the limit of as ∆t goes to zero, and omitting time arguments gives

<span id="page-110-4"></span><span id="page-110-3"></span>
$$\dot{\mathbf{A}}_{GF} = -[\mathbf{g}_G^{GF} \times \mathbf{A}_{GF}] \quad (9.11)$$

where

<span id="page-110-5"></span>
$$\omega_G^{\mathcal{GF}} \equiv \lim_{\Delta t \rightarrow 0} \frac{\vartheta \mathbf{e}}{\Delta t} \quad (9.12)$$

is the vector representation in frame G of the angular velocity of frame G with respect to frame F. The angular velocity is known to be represented in frame G because the product AGF (t + ∆t)AFG(t) is a rotation from frame G at one time to frame G at a different time, and these two frames coincide in the limit that ∆t goes to zero. The angular velocity is usually written simply as ω, with the frames understood. Its units are rad/sec, assuming that time is measured in seconds, because radian measure was assumed in taking the small angle limit of sin ϑ.

Equation [\(9.11\)](#page-110-4) is the fundamental equation of attitude kinematics. It does not distinguish between the situations where frame F or frame G or both frames are rotating in an absolute sense; it only cares about the relative rotation between the two frames. This equation can also be written as

$$\mathbf{A}_{\mathcal{G}} = -\mathbf{A}_{\mathcal{G}}\mathbf{A}_{\mathcal{F}}[\omega_{\mathcal{G}}^{\mathcal{F}} \times \mathbf{A}_{\mathcal{I}}^{\mathcal{F}}] = -\mathbf{A}_{\mathcal{G}}[\mathbf{A}_{\mathcal{F}}\omega_{\mathcal{G}}^{\mathcal{F}} \times \mathbf{A}_{\mathcal{I}}] = -\mathbf{A}_{\mathcal{G}}[\omega_{\mathcal{F}}^{\mathcal{F}} \times \mathbf{A}_{\mathcal{I}}] \quad (9.13)$$

which expresses the kinematics in terms of the representation in frame F of ω GF . The second equality uses an identity that holds for any proper orthogonal matrix. These kinematic equations, if integrated exactly, preserve the orthogonality of the attitude matrix.

The Euler axis/angle representation is fundamental for analysis, as demonstrated above, but it has been entirely superseded for practical applications by a superior four-parameter representation described in the next section.

#### 9.3. Quaternion Representation

<span id="page-111-0"></span>Applying trigonometric half-angle identities to Eq. [\(9.7\)](#page-110-2) gives

| $\mathbf{A}(\mathbf{q}) = (q_4^2 - \ \mathbf{q}_{1:3}\ ^2) \mathbf{I}_3 - 2q_4[\mathbf{q}_{1:3} \times] + 2 \mathbf{q}_{1:3} \mathbf{q}_{1:3}^\top \quad (9.14)$ |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|------------------------------------------------------------------------------------------------------------------------------------------------------------------|

where the three-component vector q1:3 and the scalar q<sup>4</sup> are defined by

| $\mathbf{q}_{1:3} = \mathbf{e} \sin(\vartheta/2)$ | (9.15a) |
|---------------------------------------------------|---------|
|---------------------------------------------------|---------|

<span id="page-111-2"></span>

| $q_4 = \cos(\vartheta/2)$ | (9.15b) |
|---------------------------|---------|
|---------------------------|---------|

This representation has the advantage over the Euler axis/angle representation of requiring no trigonometric function evaluations, and its four components are more economical than the ninecomponent attitude matrix.

The four parameters of this representation were first considered by Euler but their full significance was revealed by Rodrigues, so they are often referred to as the Euler symmetric parameters or Euler-Rodrigues parameters. This representation is called the quaternion representation and denoted A(q) because the four parameters can be regarded as the components of a quaternion

$$\mathbf{q} = \begin{bmatrix} \mathbf{q}_{1:3} \\ q_4 \end{bmatrix} \quad (9.16)$$

with vector part q1:3 and scalar q4. A quaternion is basically four-component vector with some additional operations defined for it.[<sup>2</sup>](#page-111-1) The attitude quaternion

<span id="page-111-3"></span>
$$\mathbf{q}(\mathbf{e}, \vartheta) = \begin{bmatrix} \mathbf{e} \sin(\vartheta/2) \\ \cos(\vartheta/2) \end{bmatrix} \quad (9.17)$$

is a unit quaternion, obeying the norm constraint ∥q∥ = 1, but not all quaternions are unit quaternions. It is clear from Eq. [\(9.14\)](#page-111-2) that q and −q give the same attitude matrix. This 2:1 mapping

<span id="page-111-1"></span><sup>2</sup>This is conceptually different from the quaternion introduced by Hamilton in 1844, before the introduction of vector notation, as a hypercomplex extension q = q<sup>0</sup> + iq<sup>1</sup> + jq<sup>2</sup> + kq<sup>3</sup> of a complex number z = x + iy. The scalar part of a quaternion is often labeled q<sup>0</sup> and put at the top of the column vector. Care must be taken to thoroughly understand the conventions embodied in any quaternion equation that one chooses to reference.

of quaternions to rotations is a minor annoyance that cannot be removed without introducing discontinuities in the representation.

The most important added quaternion operations are two different products of two quaternions q and q¯. They can be implemented in matrix form similar to the matrix form of the vector cross product:[<sup>3</sup>](#page-112-0)

<span id="page-112-4"></span>
$$\mathbf{q} \otimes \bar{\mathbf{q}} = [\Psi(\mathbf{q}) \ \mathbf{q}] \bar{\mathbf{q}} \quad (9.18a)$$

<span id="page-112-1"></span>q ⊙ q¯ = [Ξ(q) q ] q¯ (9.18b)

where Ψ(q) and Ξ(q) are the 4 × 3 matrices

$$\Psi(\mathbf{q}) \equiv \begin{bmatrix} q_4 \mathbf{I}_3 - \begin{bmatrix} \mathbf{q}_{1:3} \times \end{bmatrix} \\ -\mathbf{q}_{1:3}^T \end{bmatrix} \quad (9.19a)$$

$$\Xi(\mathbf{q}) \equiv \begin{bmatrix} q_4 \mathbf{I}_3 + \begin{bmatrix} \mathbf{q}_{1:3} \times \end{bmatrix} \\ -\mathbf{q}_{1:3} \end{bmatrix} \quad (9.19b)$$

Unlike the vector cross product, though, the norm of either product of two quaternions is equal to the product of their norms.

Both quaternion products are associative but not commutative in general, in parallel with matrix products. The two product definitions differ only in the signs of the cross product matrices in Eqs. [\(9.19a\)](#page-112-1) and [\(9.19b\)](#page-112-2), from which it follows that

<span id="page-112-3"></span><span id="page-112-2"></span>
$$\mathbf{q} \otimes \bar{\mathbf{q}} = \bar{\mathbf{q}} \odot \mathbf{q}$$
 (9.20)

The identity quaternion

$$\mathbf{I}_{\mathbf{I}} \equiv [0 \quad 0 \quad 0 \quad 1]^T \quad (9.21)$$

acts in quaternion multiplication like the identity matrix in matrix multiplication. The conjugate q <sup>∗</sup> of a quaternion is obtained by changing the sign of its vector part:

$$\mathbf{q}^* = \begin{bmatrix} \mathbf{q}_{1:3} \\ \mathbf{q}_4 \end{bmatrix}^* \equiv \begin{bmatrix} -\mathbf{q}_{1:3} \\ \mathbf{q}_4 \end{bmatrix} \quad (9.22)$$

Either product of a quaternion with its conjugate is equal to the square of its norm times the identity quaternion.

The inverse of any quaternion having nonzero norm is defined by

| $\mathbf{q}^{-1} \equiv \mathbf{q}^* / \ \mathbf{q}\ ^2$ | (9.23) |
|----------------------------------------------------------|--------|
|----------------------------------------------------------|--------|

A unit quaternion, such as the attitude quaternion, always has an inverse, which is identical with its conjugate. The conjugate of the product of two quaternions is equal to the product of their conjugates in the opposite order: (q¯ ⊗ q) <sup>∗</sup> = q <sup>∗</sup> ⊗ q¯ ∗ . The same relationship holds for the other product definition and with conjugates replaced by inverses.

Equation [\(9.14\)](#page-111-2) can be compactly written as

| $\mathbf{A}(\mathbf{q}) = \Xi^T(\mathbf{q})\Psi(\mathbf{q})$ | (9.24) |
|--------------------------------------------------------------|--------|
|--------------------------------------------------------------|--------|

<span id="page-112-0"></span><sup>3</sup>The notation q ⊗ q¯ was introduced in Ref. [[53](#page-172-11)], and q ⊙ q¯ is a modification of notation introduced in Ref. [[68](#page-172-12)]. Hamilton's product qq¯corresponds to q⊙q¯, but q⊗q¯ has proven to be more useful in attitude analysis. The order of the quaternion products in Eqs. [\(9.27\)](#page-113-0) and [\(9.28\)](#page-113-1) would be reversed with the classical definition of quaternion multiplication.

Now consider, for a unit quaternion q, the product

$$\begin{aligned} \mathbf{q} \otimes \begin{bmatrix} \mathbf{x} \\ 0 \end{bmatrix} \otimes \mathbf{q}^* &= \mathbf{q}^* \odot \left( \mathbf{q} \otimes \begin{bmatrix} \mathbf{x} \\ 0 \end{bmatrix} \right) = [\Xi(\mathbf{q}^*) \quad \mathbf{q}^*] [\Psi(\mathbf{q}) \quad \mathbf{q}] \begin{bmatrix} \mathbf{x} \\ 0 \end{bmatrix} \\ &= \begin{bmatrix} \Xi^T(\mathbf{q}) \\ \mathbf{q}^T \end{bmatrix} \Psi(\mathbf{q}) \mathbf{x} = \begin{bmatrix} \mathbf{A}(\mathbf{q}) \mathbf{x} \\ 0 \end{bmatrix} \end{aligned} \quad (9.25)$$

Applying a transformation by a second quaternion q¯ gives

$$\begin{aligned}\bar{\mathbf{q}} \otimes \left( \mathbf{q} \otimes \begin{bmatrix} \mathbf{x} \\ 0 \end{bmatrix} \otimes \mathbf{q}^* \right) \otimes \bar{\mathbf{q}}^* &= \bar{\mathbf{q}} \otimes \begin{bmatrix} \mathbf{A}(\mathbf{q}) \mathbf{x} \\ 0 \end{bmatrix} \otimes \bar{\mathbf{q}}^* = \begin{bmatrix} \mathbf{A}(\bar{\mathbf{q}}) \mathbf{A}(\mathbf{q}) \mathbf{x} \\ 0 \end{bmatrix} \\ &= (\bar{\mathbf{q}} \otimes \mathbf{q}) \otimes \begin{bmatrix} \mathbf{x} \\ 0 \end{bmatrix} \otimes (\bar{\mathbf{q}} \otimes \mathbf{q})^* = \begin{bmatrix} \mathbf{A}(\bar{\mathbf{q}} \otimes \mathbf{q}) \mathbf{x} \\ 0 \end{bmatrix} \quad (9.26)\end{aligned}$$

Because this must hold for any x, it shows that

<span id="page-113-0"></span>

| $\mathbf{A}(\bar{\mathbf{q}} \otimes \mathbf{q}) = \mathbf{A}(\bar{\mathbf{q}})\mathbf{A}(\mathbf{q})$ | (9.27) |
|--------------------------------------------------------------------------------------------------------|--------|
|--------------------------------------------------------------------------------------------------------|--------|

This and Eq. [\(9.2\)](#page-109-1) mean that the quaternion corresponding to successive rotations is just the product

<span id="page-113-1"></span>
$$\mathbf{q}_{\mathcal{H}\mathcal{F}} = \mathbf{q}_{\mathcal{H}\mathcal{G}} \otimes \mathbf{q}_{\mathcal{G}\mathcal{F}} \quad (9.28)$$

A simple bilinear composition rule of this type holds only for the attitude matrix and quaternion representations, a major reason for the popularity of quaternions.

Representing the rotation between times t and t + ∆t by an Euler axis and angle, Eqs. [\(9.28\)](#page-113-1), [\(9.17\)](#page-111-3), [\(9.20\)](#page-112-3), and [\(9.18b\)](#page-112-4) give

$$\begin{aligned} \mathbf{q}(t + \Delta t) &= \begin{bmatrix} \mathbf{e} \sin(\vartheta/2) \\ \cos(\vartheta/2) \end{bmatrix} \otimes \mathbf{q}(t) = \cos(\vartheta/2)\mathbf{q}(t) + \sin(\vartheta/2)\begin{bmatrix} \mathbf{e} \\ 0 \end{bmatrix} \otimes \mathbf{q}(t) \\ &= \cos(\vartheta/2)\mathbf{q}(t) + \sin(\vartheta/2)\Xi(\mathbf{q}(t))\mathbf{e} \end{aligned} \quad (9.29)$$

This quaternion propagation equation has proven to be very useful. It preserves the unity norm of the attitude quaternion. If the angular velocity is well approximated as constant over the time interval, then ϑ = ∥ω∥∆t and e = ω/∥ω∥. Alternatively, and particularly for onboard applications, ϑe can be computed by differencing the outputs of rate-integrating gyroscopes.

Using small angle approximations for the sine and cosine leads to the kinematic equation for the quaternion:

<span id="page-113-2"></span>
$$\mathbf{q} \equiv \lim_{\Delta t \rightarrow 0} \frac{\mathbf{q}(t + \Delta t) - \mathbf{q}(t)}{\Delta t} = \frac{1}{2} \begin{bmatrix} \omega \\ 0 \end{bmatrix} \otimes \mathbf{q} = \frac{1}{2} \Xi(\mathbf{q}) \boldsymbol{\omega} \quad (9.30)$$

where ω is defined by Eq. [\(9.12\)](#page-110-5) and several time arguments have been omitted. Exact integration of this equation preserves the unit norm of the quaternion. The inverse of Eq. [\(9.30\)](#page-113-2) is often useful:

| $\omega = 2\Xi^{\text{T}}(\mathbf{q})\dot{\mathbf{q}}$ | (9.31) |
|--------------------------------------------------------|--------|
|--------------------------------------------------------|--------|

The quaternion representation of a given attitude matrix A can be found by normalizing any one of the four vectors [[56](#page-172-13)]

| $\begin{bmatrix} 1 + 2A_{11} - \text{tr}\mathbf{A} \\ A_{12} + A_{21} \\ A_{13} + A_{31} \\ A_{23} - A_{32} \end{bmatrix} = 4q_1\mathbf{q},$ | $\begin{bmatrix} A_{21} + A_{12} \\ 1 + 2A_{22} - \text{tr}\mathbf{A} \\ A_{23} + A_{32} \\ A_{31} - A_{13} \end{bmatrix}$ | $= 4q_2\mathbf{q}$ | $\begin{bmatrix} A_{23} - A_{32} \\ A_{31} - A_{13} \\ A_{12} - A_{21} \\ 1 + \text{tr}\mathbf{A} \end{bmatrix} = 4q_4\mathbf{q}$ | $(9.32)$ |
|----------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------|--------------------|-----------------------------------------------------------------------------------------------------------------------------------|----------|
|                                                                                                                                              |                                                                                                                            |                    |                                                                                                                                   |          |

Numerical errors are minimized by choosing the vector with the greatest norm, which can be found by the following procedure. Find the largest of trA and the three diagonal elements of A. If trA is the largest, then |q4| is the largest of the |q<sup>i</sup> |, otherwise the largest value of |q<sup>i</sup> | is the one with the same index as the largest diagonal element of A. The overall sign of the normalized vector is not determined, reflecting the twofold ambiguity of the quaternion representation.

Extracting many of the other parameterizations from an attitude matrix is most easily accomplished by first extracting a quaternion and then converting to the desired representation. The kinematic equations of these other representations can also be readily derived through the intermediary of the quaternion representation.

A three-parameter representation can be obtained by using only three components of the quaternion, say the i, j, k components, with the fourth component given by

<span id="page-114-2"></span>
$$q_\ell = \pm \sqrt{1 - q_i^2 - q_j^2 - q_k^2} \quad (9.33)$$

The sign is not arbitrary, but is determined by the four-component quaternion being represented by three of its components. Once so determined, the sign will not change if the quaternion varies smoothly unless q<sup>ℓ</sup> passes through zero. To avoid a sign error if |q<sup>ℓ</sup> | becomes small, the representation is switched to make q<sup>ℓ</sup> one of three components in the three-parameter representation, replacing one of the other components, which is then given by the square root with the correct sign. The unit norm constraint on the attitude quaternion means that at least one of its components must have magnitude 1/2 or greater. To minimize switching, it should be done when |q<sup>ℓ</sup> | is significantly less than 1/2, and the component replaced by q<sup>ℓ</sup> in the three-component representation should have magnitude no smaller than 1/2. To first order in the errors, the error in the fourth component of the quaternion is

<span id="page-114-3"></span>
$$\Delta q_\ell = -q_\ell^{-1}(q_i\Delta q_i + q_j\Delta q_j + q_k\Delta q_k) \quad (9.34)$$

This approaches the indeterminate quantity 0/0 as |q<sup>ℓ</sup> | → 0, providing another reason for switching.

## 9.4. Rodrigues Parameter Representation

<span id="page-114-0"></span>The three Rodrigues parameters appeared in 1840 [[72](#page-172-14)], but were first arranged in a vector by Gibbs, who invented modern vector notation. For this reason, the vector of Rodrigues parameters is often called the Gibbs vector and denoted by g. The Rodrigues parameters are related to the Euler axis/angle and the quaternion by

<span id="page-114-1"></span>

| $\mathbf{g} = \mathbf{e} \tan(\vartheta/2) = \frac{\mathbf{q}_{1:3}}{\mathbf{q}_4}$ | (9.35) |
|-------------------------------------------------------------------------------------|--------|
|-------------------------------------------------------------------------------------|--------|

The quaternion as a function of the Gibbs vector is

$$\mathbf{q} = \frac{\pm 1}{\sqrt{1 + \|\mathbf{g}\|^2}} \begin{bmatrix} \mathbf{g} \\ 1 \end{bmatrix} \quad (9.36)$$

It is clear from Eq. [\(9.35\)](#page-114-1) that q and −q map to the same Gibbs vector, so the Rodrigues parameters provide a 1:1 mapping of rotations. The price paid for this is that the Gibbs vector is infinite for a 180◦ rotation. Thus this parameterization is not recommended as a global attitude representation, but it provides an excellent representation of small rotations.

The Rodrigues parameter representation of the attitude matrix is

$$\mathbf{A}(\mathbf{g}) = \mathbf{I}_3 + 2 \frac{[\mathbf{g} \times]^2 - [\mathbf{g} \times]}{1 + \|\mathbf{g}\|^2} \quad (9.37)$$

This resembles the quaternion representation in requiring no transcendental function evaluations, but it is a rational function rather than a simple polynomial.

The composition rule for the Rodrigues parameters corresponding to the quaternion product q¯ ⊗ q is

$$\bar{\mathbf{g}} \boxtimes \mathbf{g} \equiv \frac{\bar{\mathbf{g}} + \mathbf{g} - \bar{\mathbf{g}} \times \mathbf{g}}{1 - \bar{\mathbf{g}} \cdot \mathbf{g}} \quad (9.38)$$

This composition law is associative but not commutative in general, in parallel with matrix and quaternion products. Because it is not a bilinear function of the constituent Gibbs vectors, it cannot be represented as a matrix product like quaternion composition.

The kinematic equation for the Rodrigues parameters is

$$\mathbf{g} = (1/2) (\mathbf{I}_3 + [\mathbf{g} \times ] + \mathbf{g} \mathbf{g}^T) \boldsymbol{\omega} \quad (9.39)$$

with the inverse

$$\omega = 2 \left( 1 + \|\mathbf{g}\|^2 \right)^{-1} (\hat{\mathbf{g}} - \mathbf{g} \times \hat{\mathbf{g}}) \quad (9.40)$$

## 9.5. Modified Rodrigues Parameters

<span id="page-115-0"></span>The modified Rodrigues parameters (MRPs) were invented by T. F. Wiener in 1962 [[88](#page-173-14)], rediscovered by Marandi and Modi in 1987 [[55](#page-172-15)], and have been championed by Junkins and Schaub [[73](#page-172-16)]. The vector of MRPs is related to the Euler axis/angle and the quaternion by

<span id="page-115-2"></span>
$$\mathbf{p} = \mathbf{e} \tan(\vartheta/4) = \frac{\mathbf{q}_{1:3}}{1 + q_4} \quad (9.41)$$

The quaternion as a function of the MRPs is

$$\mathbf{q} = \frac{1}{1 + \|\mathbf{p}\|^2} \begin{bmatrix} 2\mathbf{p} \\ 1 - \|\mathbf{p}\|^2 \end{bmatrix} \quad (9.42)$$

and the attitude matrix is given by

$$\mathbf{A}(\mathbf{p}) = \mathbf{I}_3 + \frac{8[\mathbf{p} \times \mathbf{I}]^2 - 4(1 - \|\mathbf{p}\|^2)[\mathbf{p} \times \mathbf{I}]}{(1 + \|\mathbf{p}\|^2)^2} \quad (9.43)$$

Every vector of MRPs has a shadow

<span id="page-115-1"></span>
$$\mathbf{p}^S \equiv -\frac{\mathbf{p}}{\|\mathbf{p}\|^2} = \frac{-\mathbf{q}_{1:3}}{1 - q_4} \quad (9.44)$$

An MRP vector and its shadow represent the same attitude because q and −q represent the same attitude, so the MRPs are a 2:1 mapping of the rotations just as the quaternions are. It is clear from Eq. [\(9.44\)](#page-115-1) that ∥p <sup>S</sup>∥∥p∥ = 1, so every attitude can be represented by either an MRP vector with ∥p∥ ≤ 1 or an equivalent MRP vector in the shadow set of MRPs with ∥p∥ ≥ 1.

The MRP vector corresponding to the quaternion product q¯ ⊗ q follows the composition rule

$$\bar{\mathbf{p}} \cdot \square \mathbf{p} \equiv \frac{(1 - \|\mathbf{p}\|^2) \bar{\mathbf{p}} + (1 - \|\bar{\mathbf{p}}\|^2) \mathbf{p} - 2 \bar{\mathbf{p}} \times \mathbf{p}}{1 + \|\mathbf{p}\|^2 \|\bar{\mathbf{p}}\|^2 - 2 \bar{\mathbf{p}} \cdot \mathbf{p}} \quad (9.45)$$

This composition law is associative but not commutative in general, in parallel with matrix and quaternion products. It cannot be represented as a matrix product.

The kinematic equation for the MRPs is

<span id="page-116-1"></span>
$$\dot{\mathbf{p}} = \frac{1 + \|\mathbf{p}\|^2}{4} \left( \mathbf{I}_3 + 2 \frac{[\mathbf{p} \times ]^2 + [\mathbf{p} \times ]}{1 + \|\mathbf{p}\|^2} \right) \boldsymbol{\omega} \quad (9.46)$$

The matrix in parentheses is orthogonal, so the inverse of Eq. [\(9.46\)](#page-116-1) is

$$\omega = \frac{4}{1 + \|\mathbf{p}\|^2} \left( \mathbf{I}_3 + 2 \frac{[\mathbf{p} \times ]^2 - [\mathbf{p} \times ]}{1 + \|\mathbf{p}\|^2} \right) \dot{\mathbf{p}} \quad (9.47)$$

The norm of an MRP vector can grow without limit during dynamic propagation or attitude estimation; Eq. [\(9.41\)](#page-115-2) shows that the norm is infinite for ϑ = 2π. This singularity can be avoided by switching from the MRP vector to its shadow. The norm can be restricted to be less than or equal to unity in theory, but in practice it is best to allow the norm to exceed unity by some amount before switching in order to avoid "chattering" between the MRP and its shadow. An error ∆p in an MRP vector corresponds to an error

<span id="page-116-3"></span>
$$\Delta \mathbf{p}^S = \frac{\partial \mathbf{p}^S}{\partial \mathbf{p}} \Delta \mathbf{p} = \frac{2\mathbf{p}\mathbf{p}^T - \|\mathbf{p}\|^2 \mathbf{I}_3}{\|\mathbf{p}\|^4} \Delta \mathbf{p} = [2\mathbf{p}^S(\mathbf{p}^S)^T - \|\mathbf{p}^S\|^2 \mathbf{I}_3] \Delta \mathbf{p} \quad (9.48)$$

in its shadow. This relation is useful for mapping covariance matrices into and out of the shadow set. The 2:1 four-component quaternion representation does not have these complications because the two quaternions representing the same attitude both have unit norm, so there is no need to switch between them.

#### 9.6. Rotation Vector Representation

<span id="page-116-0"></span>It is convenient for analysis, but not for computations, to combine the Euler axis and angle into the three-component rotation vector

$$\boldsymbol{\vartheta} \equiv \boldsymbol{\vartheta} \mathbf{e} = 2(\cos^{-1} q_4) \frac{\mathbf{q}_{1:3}}{\|\mathbf{q}_{1:3}\|} \quad (9.49)$$

This leads to the very elegant expression

$$\mathbf{A}(\boldsymbol{\vartheta}) = \exp(-[\boldsymbol{\vartheta} \times]) \qquad (9.50)$$

where exp(·)is the matrix exponential. This equation can be verified by expansion of it and Eq. [\(9.7\)](#page-110-2) as Taylor series in ϑ and repeated applications of the identity [e×] <sup>2</sup> = ee<sup>T</sup> − I3.

The kinematic equation for the rotation vector is

<span id="page-116-2"></span>
$$\dot{\boldsymbol{\vartheta}} = \boldsymbol{\omega} + \frac{1}{2} \boldsymbol{\vartheta} \times \boldsymbol{\omega} + \frac{1}{\vartheta^2} \left( 1 - \frac{\vartheta}{2} \cot \frac{\vartheta}{2} \right) \boldsymbol{\vartheta} \times (\boldsymbol{\vartheta} \times \boldsymbol{\omega}) \quad (9.51)$$

The coefficient of ϑ × (ϑ × ω) goes to 1/12 as ϑ goes to zero, but it is singular for ϑ equal to any nonzero multiple of 2π. The inverse of Eq. [\(9.51\)](#page-116-2) is

$$\omega = \dot{\vartheta} - \frac{1 - \cos \vartheta}{\vartheta^2} \dot{\vartheta} \times \dot{\vartheta} + \frac{\vartheta - \sin \vartheta}{\vartheta^3} \dot{\vartheta} \times (\dot{\vartheta} \times \dot{\vartheta}) \quad (9.52)$$

The rotation vector is useful for the analysis of small rotations, but not for large rotations, because of both the computational cost of evaluating the matrix exponential and the kinematic <span id="page-117-3"></span>singularity for ∥ϑ∥ = 2π. This singularity can be avoided, as for the MRPs, by switching from the rotation vector to its shadow

$$\vartheta^S \equiv (1 - 2\pi \|\vartheta\|^{-1})\vartheta \qquad (9.53)$$

which represents the same attitude. This can restrict the norm of the rotation vector to π or less in theory, but in practice it is best to allow the norm to exceed π by some amount before switching in order to avoid "chattering" between the rotation vector and its shadow.

The properties of the rotation vector are very similar to those of the MRPs, and it has no obvious advantages over the MRPs. It has the disadvantage of requiring transcendental function evaluations to compute the attitude matrix, so it is rarely used in practical applications.

#### 9.7. Euler Angles

<span id="page-117-0"></span>An Euler angle representation parameterizes a rotation by the product of three rotations about coordinate frame unit vectors:

<span id="page-117-1"></span>

| $\mathbf{A}_{ijk}(\phi, \theta, \psi) = \mathbf{A}(\mathbf{e}_i, \psi)\mathbf{A}(\mathbf{e}_j, \theta)\mathbf{A}(\mathbf{e}_i, \phi)$ | (9.54) |
|---------------------------------------------------------------------------------------------------------------------------------------|--------|
|---------------------------------------------------------------------------------------------------------------------------------------|--------|

where e<sup>j</sup> , e<sup>j</sup> , and e<sup>j</sup> are selected from the set

| $\mathbf{e}_1 = [1 \ 0 \ 0]^T$ , $\mathbf{e}_2 = [0 \ 1 \ 0]^T$ , $\mathbf{e}_3 = [0 \ 0 \ 1]^T$ | (9.5) |
|--------------------------------------------------------------------------------------------------|-------|
|--------------------------------------------------------------------------------------------------|-------|

The possible choice of axes is constrained by the requirements i ̸= j and j ̸= k, leaving six symmetric sets with ijk equal to 121, 131, 232, 212, 313, and 323 and six asymmetric sets with ijk equal to 123, 132, 231, 213, 312, and 321. Symmetric Euler angle sets are used in classical studies of rigid body motion [[29](#page-171-15), [36](#page-171-16), [43](#page-171-17), [59](#page-172-10), [87](#page-173-15)].

The asymmetric sets of angles are called the Tait-Bryan angles or roll, pitch, and yaw angles. The latter terminology originally described the motions of ships and then was carried over into aircraft and spacecraft. Roll is a rotation about the vehicle body axis that is closest to the vehicle's usual direction of motion, and hence would be perceived as a screwing motion. The roll axis is conventionally assigned index 1. Yaw is a rotation about the vehicle body axis that is usually closest to the direction of local gravity, and hence would be be perceived as a motion that points the vehicle left or right. The yaw axis is conventionally assigned index 3. Pitch is a rotation about the remaining vehicle body axis, and hence would be perceived as a motion that points the vehicle up or down. The pitch axis is conventionally assigned index 2. Note that Eq. [\(9.54\)](#page-117-1) assigns the variables ϕ, θ, and ψ based on the order of rotations in the sequence, making no definite association between these variables and either the axis labels 1, 2, and 3 or the names roll, pitch and yaw. Many authors follow a different convention, denoting roll by ϕ, pitch by θ, and yaw by ψ. As always, the reader consulting any source should be careful to understand the conventions that it follows.

Using the product rule and Eq. [\(9.11\)](#page-110-4) to compute the time derivative of Eq. [\(9.54\)](#page-117-1) gives

$$-[\boldsymbol{\omega} \times \mathbf{A}_{ijk}(\phi, \theta, \psi) = \left\{ -[(\dot{\psi}\mathbf{e}_k) \times \mathbf{A}(\mathbf{e}_k, \psi)[(\dot{\theta}\mathbf{e}_j) \times \mathbf{A}^T(\mathbf{e}_k, \psi) - \mathbf{A}(\mathbf{e}_k, \psi)\mathbf{A}(\mathbf{e}_j, \theta)[(\dot{\phi}\mathbf{e}_i) \times \mathbf{A}^T(\mathbf{e}_j, \theta)\mathbf{A}^T(\mathbf{e}_k, \psi) \right\} \mathbf{A}_{ijk}(\phi, \theta, \psi) \quad (9.56)$$

The identity A[x×]A<sup>T</sup> = [(Ax)×], which holds for any proper orthogonal A, gives

<span id="page-117-2"></span>
$$\omega = \psi \mathbf{e}_k + \dot{\theta} \mathbf{A}(\mathbf{e}_k, \psi) \mathbf{e}_j + \dot{\phi} \mathbf{A}(\mathbf{e}_k, \psi) \mathbf{A}(\mathbf{e}_j, \theta) \mathbf{e}_i = \mathbf{A}(\mathbf{e}_k, \psi) \mathbf{M}(\dot{\phi} - \dot{\theta} - \psi)^T \quad (9.57)$$

where

| $\mathbf{M} = [\mathbf{A}(\mathbf{e}_j, \theta)\mathbf{e}_i \quad \mathbf{e}_j \quad \mathbf{e}_k]$ | (9.58) |
|-----------------------------------------------------------------------------------------------------|--------|
|-----------------------------------------------------------------------------------------------------|--------|

The second equality in Eq. [\(9.57\)](#page-117-2) makes use of A(ek, ψ)e<sup>k</sup> = ek. The Euler angle rates as functions of the angular velocity are

$$[\phi \ \theta \ \psi]^\top = \mathbf{M}^{-1} \mathbf{A}^\top (\mathbf{e}_k, \psi) \boldsymbol{\omega} \quad (9.59)$$

<span id="page-118-1"></span>This kinematic equation is singular if the determinant of M is zero. Equation [\(9.7\)](#page-110-2) and the Euler axis requirement that e<sup>i</sup> · e<sup>j</sup> = e<sup>j</sup> · e<sup>k</sup> = 0 gives

$$\det \mathbf{M} = [\mathbf{A}(\mathbf{e}_j, \boldsymbol{\theta})\mathbf{e}_i] \cdot (\mathbf{e}_j \times \mathbf{e}_k) = \cos \theta [\mathbf{e}_i \cdot (\mathbf{e}_j \times \mathbf{e}_k)] - \sin \theta (\mathbf{e}_i \cdot \mathbf{e}_k) \quad (9.60)$$

The triple vector product e<sup>i</sup> · (e<sup>j</sup> × ek) is zero for the symmetric Euler angles, so the kinematic equations of these representations are singular if sin θ = 0. The dot product e<sup>i</sup> · e<sup>k</sup> is zero for the asymmetric Euler angles, so the kinematics of these representations are singular if cos θ = 0. This singularity is known as gimbal lock and is caused by collinearity of the physical rotation axis vectors of the first and third rotations in the sequence. Note that the column vector representations of these rotation axes are always parallel for the symmetric Euler angle sequences and always perpendicular for the asymmetric sequences, but this neither causes nor prevents gimbal lock.

Because Euler angles are discussed in many references on rotational motion and because they are not widely used in navigation filters, they will not be discussed further here. Kinematic equations and explicit forms of the attitude matrices for all twelve sets can be found in Refs. [[36](#page-171-16), [43](#page-171-17), [59](#page-172-10), [87](#page-173-15)].

#### 9.8. Additive EKF (AEKF)

<span id="page-118-0"></span>Three-component representations are the most natural representations for filtering, because only three parameters are needed to represent rotations. As was pointed out at the beginning of this Chapter, though, all three-parameter representations of the rotation group have discontinuities or singularities. Any filter using a three-dimensional attitude representation must provide some guarantee of avoiding these singular points, either by restricting the vehicle's attitude or by switching between different parameter sets if the representation approaches a discontinuity or singularity.

The earliest Kalman filters for spacecraft attitude estimation used a roll, pitch, yaw sequence of Euler or Tait-Bryan angles discussed in Section [9.7](#page-117-0) [[21](#page-170-17),[22](#page-171-18)]. This is a very useful representation if the middle angle of the sequence, generally the pitch angle, stays well away from ±90◦ , and has been used for Earth-pointing spacecraft with small pitch angles. One disadvantage of this representation is its trigonometric function evaluations, but this is less of an issue with the computing power now available, especially in onboard computers.

An EKF can estimate three components of a quaternion, with the fourth component being determined by the quaternion unit norm constraint, as discussed at the end of Section [9.3](#page-111-0) [[53](#page-172-11)]. If the fourth component becomes small, it must be added to the set of estimated quaternion components, with one of the other components switched out. This switch should be made when the magnitude of the fourth component is is not too close to either end of the range from 0 and 1/2 to avoid "chattering" between component sets. The switch must be accompanied by the following covariance matrix transformation. Assuming the three components in the pre-switch representation have indices i, j, k in ascending order, their 3×3 covariance matrix is the symmetric matrix

$$\mathbf{P}_{3 \times 3} = \begin{bmatrix} P_{ii} & P_{ij} & P_{ik} \\ P_{ji} & P_{jj} & P_{jk} \\ P_{ki} & P_{kj} & P_{kk} \end{bmatrix} \quad (9.61)$$

The 4×4 covariance matrix of the full quaternion is formed by adding the ℓth row and column, keeping the indices in ascending order. The needed covariance components, using using Eqs. [\(9.33\)](#page-114-2) and [\(9.34\)](#page-114-3), are

| $P_{ml} = P_{lm} = -q_l^{-1}(q_i P_{im} + q_j P_{jm} + q_k P_{km})$ | for | $m = i, j, k$ | (9.6a) |
|---------------------------------------------------------------------|-----|---------------|--------|
|---------------------------------------------------------------------|-----|---------------|--------|

$$P_{\ell\ell} = q_\ell^{-2}(q_\ell^2 P_{ii} + q_j^2 P_{jj} + q_k^2 P_{kk} + 2q_i q_j P_{ji} + 2q_i q_k P_{ik} + 2q_j q_k P_{jk}) \quad (9.6b)$$

<span id="page-119-3"></span>Then the row and column corresponding to the quaternion component switched out of the representation are deleted to form the new 3×3 covariance matrix.

The modified Rodrigues parameters (MRPs) are non-singular for rotations of less than 360◦ , and the singularity can be avoided by switching to an MRP in the shadow set, as discussed in Section [9.5.](#page-115-0) The switch to the shadow set is made at some angle greater than 180◦ to avoid "chattering" between the two parameter sets. The switch must be accompanied by a covariance matrix transformation using Eq. [\(9.48\)](#page-116-3)

$$\mathbf{P}_{pp}^S = [2\mathbf{p}^S(\mathbf{p}^S)^T - \|\mathbf{p}^S\|^2 \mathbf{I}_3] \mathbf{P}_{pp} [2\mathbf{p}^S(\mathbf{p}^S)^T - \|\mathbf{p}^S\|^2 \mathbf{I}_3] \quad (9.63)$$

where Ppp is the covariance before the switch, and P S pp is the covariance of p S after the switch [[45](#page-171-19)]. This covariance mapping is simpler than the corresponding mapping for the three-component quaternion representation, and the MRP representation avoids a square root computation. The appearance of ϑ/4 in Eq. [\(9.41\)](#page-115-2) as opposed to ϑ/2 in Eq. [\(9.17\)](#page-111-3) means that switching will be less frequent when the MRP representation is used. For these reasons the MRP representation has become the preferred three-parameter attitude filter when the attitude is unrestricted.

The Gibbs vector or Rodrigues parameter representation has been used in an EKF [[37](#page-171-20)], but it is not well suited to filtering because of its inability to represent 180◦ rotations, as discussed in Section [9.4.](#page-114-0) It provides an excellent representation of small attitude errors, however. The rotation vector, discussed in Section [9.6,](#page-116-0) is also not recommended for application in an EKF, as it has no clear advantage over the MRPs and has the disadvantage of requiring transcendental function evaluations.

The nine-component attitude matrix and the four-component quaternion represent the entire rotation group without singularities or discontinuities, but the linear measurement update in EKFs employing these representations violates the orthogonality constraint on the attitude matrix or the unit norm constraint on the quaternion. Various methods have been proposed to circumvent this difficulty, but these are not without problems [[59](#page-172-10)]. At the very least, they are inefficient due to the larger dimesionality of the covariance matrix.

#### 9.9. Multiplicative EKF (MEKF)

<span id="page-119-0"></span>The multiplicative EKF (MEKF) uses the nine-component attitude matrix or the four-component quaternion as the "global" attitude representation and a three-component vector δϑ for the "local" representation of attitude errors, so that the true attitude is represented as a product

<span id="page-119-1"></span>
$$\mathbf{A}^{\text{true}} = \delta \mathbf{A}(\delta \vartheta) \hat{\mathbf{A}} \qquad (9.64)$$

$$\mathbf{q}^{\text{true}} = \delta \mathbf{q}(\delta \vartheta) \otimes \hat{\mathbf{q}} \quad (9.64)$$

The constraints on the representations are satisfied because Atrue , δA, and Aˆ are all proper orthogonal matrices, and q true , δq, and qˆ all have unit norm. The MEKF avoids the attitude restrictions or switching required by additive attitude EKFs because the error vector δϑ is assumed to be small enough to completely avoid singularities in the parameterizations δA(δϑ) or δq(δϑ). In some sense, though, Eq. [\(9.64\)](#page-119-1) incorporates a continuous switching of the attitude reference.

Only the quaternion version of the MEKF, which is much more widely employed, is presented here. Reference [[53](#page-172-11)] reviews its history. Any three-component attitude representation that is related to first order in δϑ to the quaternion by

<span id="page-119-2"></span>
$$\delta \mathbf{q} \approx \begin{bmatrix} \delta \vartheta/2 \\ 1 \end{bmatrix} \quad (9.65)$$

can be used as the error vector. Common choices are the rotation vector, as suggested by the notation of Eq. [\(9.64\)](#page-119-1), two times the vector part of the quaternion, two times the vector of Rodrigues <span id="page-120-3"></span>parameters, four times the vector of MRPs, or a vector of suitably indexed roll, pitch, and yaw angles [[59](#page-172-10)].

The order of the factors on the right side of Eq. [\(9.64\)](#page-119-1) means that the attitude errors are in the body reference frame. This leads to a major advantage of the MEKF, that the covariance of the attitude error angles in the body frame has a transparent physical interpretation. The covariance of estimators using other attitude representations has a less obvious interpretation unless the attitude matrix is close to the identity matrix. It is possible to reverse the order of the factors on the right side of Eq. [\(9.64\)](#page-119-1) so the attitude errors are in the reference frame [[26](#page-171-21)]. The covariance can be mapped into the body frame if desired.

The MEKF estimates δϑ and any other state variables of interest. This discussion addresses only the attitude part, as the equations for the other components of the state vector obey the usual EKF equations. The MEKF proceeds by iteration of three steps: measurement update, state vector reset, and propagation to the next measurement time. The measurement update step updates the local error state vector. The reset moves the updated information from the local error state to the global attitude representation and resets the components of the local error state to zero. The propagation step propagates the global variables to the time of the next measurement. The local error state variables do not need to be propagated because they are identically zero over the propagation step. These three steps will be discussed in more detail.

9.9.1. Measurement Update The observation model in given in terms of the true global state

| $\mathbf{y} = \mathbf{h}(\mathbf{q}^{\text{true}}) + \mathbf{v}$ | (9.6) |
|------------------------------------------------------------------|-------|
|------------------------------------------------------------------|-------|

but the measurement sensitivity matrix is the partial derivative with respect to the local error state, so the measurement sensitivity matrix is

<span id="page-120-0"></span>
$$\mathbf{H} = \frac{\partial \mathbf{h}}{\partial \mathbf{q}} \frac{\partial \mathbf{q}^{\text{true}}}{\partial (\delta \boldsymbol{\vartheta})} \quad (9.67)$$

Equations [\(9.64\)](#page-119-1), [\(9.65\)](#page-119-2), [\(9.18b\)](#page-112-4), and [\(9.20\)](#page-112-3) give, to first order in the error vector,

<span id="page-120-1"></span>
$$\mathbf{q}^{\text{true}} \approx \begin{bmatrix} \delta \vartheta / 2 \\ 1 \end{bmatrix} \otimes \hat{\mathbf{q}} = \hat{\mathbf{q}} + \frac{1}{2} \Xi(\hat{\mathbf{q}}) \delta \vartheta \quad (9.68)$$

Inserting the partial derivative of this with respect to δϑ into Eq. [\(9.67\)](#page-120-0) then gives

$$\mathbf{H} = \frac{1}{2} \frac{\partial \mathbf{h}}{\partial \mathbf{q}} \Xi(\hat{\mathbf{q}}) \quad (9.69)$$

Simplifications are possible in some special cases.

The Kalman gain computation and covariance update have the standard Kalman filter forms. The error state update employs the first-order Taylor expansion

$$E\{\mathbf{h}(\mathbf{q}^{\text{true}})\} \approx \mathbf{h}(\hat{\mathbf{q}}) + \mathbf{H}\boldsymbol{\vartheta}\hat{\boldsymbol{\vartheta}} \quad (9.70)$$

giving

<span id="page-120-2"></span>
$$\delta \hat{\vartheta}^\dagger = \delta \hat{\vartheta}^- + \mathbf{K} [\mathbf{y} - E\{\mathbf{h}(\mathbf{q}^{\text{true}})\}] = (\mathbf{I} - \mathbf{K}\mathbf{H})\delta\hat{\vartheta}^- + \mathbf{K} [\mathbf{y} - \mathbf{h}(\hat{\mathbf{q}}^-)] \quad (9.71)$$

9.9.2. Reset The discrete measurement update assigns a finite post-update value to δϑˆ + , but the global state still retains the value qˆ <sup>−</sup>. A reset procedure is used to move the update information to a post-update estimate global state vector qˆ <sup>+</sup>, while simultaneously resetting δϑˆ to 03, the three-component vector with all zero components. The reset does not change the overall estimate, so the reset must obey

$$\hat{\mathbf{q}}^+ = \delta \mathbf{q}(\mathbf{0}_3) \otimes \hat{\mathbf{q}}^+ = \delta \mathbf{q}(\delta \hat{\mathbf{v}}^+) \otimes \hat{\mathbf{q}}^- \quad (9.72)$$

Thus the reset moves information from one part of the estimate to another part.

Every EKF includes an additive reset of the global state vector, but this is usually implicit rather than explicit. The multiplicative quaternion reset is the special feature of the MEKF. This reset has to preserve the quaternion norm, so an exact unit-norm expression for the functional dependence of δq on δϑ must be used, not the linear approximation of Eq. [\(9.65\)](#page-119-2). Using the Rodrigues parameter vector has the practical advantage that the reset operation for this parameterization is

$$\hat{\mathbf{q}}^+ = \delta \mathbf{q}(\delta \hat{\boldsymbol{\vartheta}}^+) \otimes \hat{\mathbf{q}}^- = \frac{1}{\sqrt{1 + \|\delta \hat{\boldsymbol{\vartheta}}^+/2\|^2}} \begin{bmatrix} \delta \hat{\boldsymbol{\vartheta}}^+/2 \\ 1 \end{bmatrix} \otimes \hat{\mathbf{q}}^- \quad (9.73)$$

Using an argument similar to Eq. [\(9.68\)](#page-120-1), this can be accomplished in two steps:

$$\mathbf{q}' = \hat{\mathbf{q}}^- + \frac{1}{2}\Xi(\hat{\mathbf{q}}^-)\boldsymbol{\delta}\hat{\boldsymbol{\vartheta}}^+ \quad (9.74)$$

followed by

$$\hat{\mathbf{q}}^+ = \frac{\mathbf{q}'}{\|\mathbf{q}'\|} \quad (9.75)$$

The first step is just the usual linear Kalman update, and the second step is equivalent to a brute force normalization of the updated quaternion. Thus the MEKF using Rodrigues parameters for the error vector provides a theoretical justification for brute force renormalization, with the added advantage of completely avoiding the accumulation of quaternion norm errors after many updates. The Rodrigues parameters also have the conceptual advantage that they map the rotation group into three-dimensional Euclidean space, with the largest possible 180◦ attitude errors mapped to points at infinity. Thus probability distributions with infinitely long tails, such as Gaussian distributions, make sense in Rodrigues parameter space.

If a measurement update immediately follows a reset or propagation, the δϑˆ − term on the right side of Eq. [\(9.71\)](#page-120-2) can be omitted because δϑˆ − is zero. The reset is often delayed for computational efficiency until all the updates for a set of simultaneous measurements have been performed, though, in which case δϑˆ − may have a finite value and all the terms in Eq. [\(9.71\)](#page-120-2) must be included. It is imperative to perform a reset before beginning the time propagation, however, to avoid the necessity of propagating δϑˆ between measurements.

There is some controversy over the question of whether the reset affects the covariance. One argument holds that it doesn't because the covariance depends not on the actual measurements but on their assumed statistics. Measurement errors are assumed to have zero mean, so the mean reset is zero. But the reset is very different from the measurement update in that it changes the reference frame for the attitude covariance, which might be expected to modify the covariance even though it adds no new information. The change in the covariance of δϑ resulting from the effect of the actual update, rather than its zero expectation, can be computed to be [[57](#page-172-17), [71](#page-172-18)]

$$\mathbf{P}_{\vartheta\vartheta}^{\text{reset}} = \left( \mathbf{I}_3 - [\delta \hat{\vartheta}^+ \times ]/2 \right) \mathbf{P}_{\vartheta\vartheta}^+ \left( \mathbf{I}_3 - [\delta \hat{\vartheta}^+ \times ]/2 \right)^T \quad (9.76)$$

to first order in δϑˆ + . Comparison with Eq. [\(9.7\)](#page-110-2) shows that the covariance reset looks to this order like a rotation by δϑˆ + /2, but this equivalence does not hold in higher orders. Most applications omit this covariance reset, but Reynolds has found that it speeds convergence and adds robustness <span id="page-122-3"></span>in the presence of large updates, and that omitting it can even lead to filter divergence in some cases [[71](#page-172-18)].

9.9.3. Propagation An EKF must propagate the expectation and covariance of the state. The MEKF is unusual in propagating the expectation qˆ and the covariance of the error-state vector. The propagation of the attitude error is found by by differentiating Eq. [\(9.64\)](#page-119-1):

<span id="page-122-0"></span>
$$\dot{\mathbf{q}}^{\text{true}} = \delta \dot{\mathbf{q}} \otimes \hat{\mathbf{q}} + \delta \mathbf{q} \otimes \hat{\mathbf{q}} \quad (9.77)$$

The true and estimated quaternions satisfy the kinematic equations

$$\mathbf{q}^{true} = \frac{1}{2} \begin{bmatrix} \omega^{true} \\ 0 \end{bmatrix} \otimes \mathbf{q}^{true} \quad (9.78a)$$

$$\dot{\mathbf{q}} = \frac{1}{2} \begin{bmatrix} \hat{\omega} \\ 0 \end{bmatrix} \otimes \hat{\mathbf{q}} \quad (9.78b)$$

where ω true and ωˆ are the true and estimated angular rates, respectively. Substituting these equations and Eq. [\(9.64\)](#page-119-1) into Eq. [\(9.77\)](#page-122-0), multiplying on the right by qˆ −1 , and rearranging terms gives [[53](#page-172-11)]

$$\delta \dot{\mathbf{q}} = \frac{1}{2} \left( \begin{bmatrix} \omega^{\text{true}} \\ 0 \end{bmatrix} \otimes \delta \mathbf{q} - \delta \mathbf{q} \otimes \begin{bmatrix} \hat{\omega} \\ 0 \end{bmatrix} \right) \quad (9.79)$$

Substituting Eq. [\(9.65\)](#page-119-2) and ω true = ωˆ +δω, where δω is the angular velocity error, and multiplying by two leads to

$$\begin{bmatrix} \boldsymbol{\vartheta} \dot{\boldsymbol{\theta}} \\ \boldsymbol{0} \end{bmatrix} = \begin{bmatrix} \boldsymbol{\omega} \\ \boldsymbol{0} \end{bmatrix} \otimes \begin{bmatrix} \boldsymbol{\vartheta} \boldsymbol{\vartheta}/2 \\ 1 \end{bmatrix} - \begin{bmatrix} \boldsymbol{\vartheta} \boldsymbol{\vartheta}/2 \\ 1 \end{bmatrix} \otimes \begin{bmatrix} \boldsymbol{\omega} \\ \boldsymbol{0} \end{bmatrix} + \begin{bmatrix} \boldsymbol{\vartheta} \boldsymbol{\omega} \\ \boldsymbol{0} \end{bmatrix} \otimes \begin{bmatrix} \boldsymbol{\vartheta} \boldsymbol{\vartheta}/2 \\ 1 \end{bmatrix} \quad (9.80)$$

Ignoring products of the small terms δω and δϑ, in the spirit of the (linearized) EKF, the first three components of Eq. [\(9.80\)](#page-122-1) are

<span id="page-122-2"></span><span id="page-122-1"></span>
$$\delta \dot{\theta} = -\hat{\omega} \times \delta \theta + \delta \omega \quad (9.81)$$

and the fourth component is 0 = 0. Equation [\(9.81\)](#page-122-2) is the equation needed to propagate the covariance of the attitude error-angle covariance.

The expectation of Eq. [\(9.81\)](#page-122-2) is

$$\delta \hat{\boldsymbol{\theta}} = -\hat{\boldsymbol{\omega}} \times \delta \hat{\boldsymbol{\theta}} \qquad (9.82)$$

because δω has zero expectation. This says that if δϑˆ is zero at the beginning of a propagation it will remain zero through the propagation, which is equivalent to saying that δqˆ will be equal to the identity quaternion throughout the propagation.

![](_page_123_Picture_1.jpeg)

## <span id="page-124-0"></span>Usability Considerations

Contributed by Cheryl J. Gramling

This chapter is written to address best practices for mechanisms like selective processing of measurements, reinitializations and restarts, backup ephemeris, and the availability of a ground system corollary to a flight filter implementation. These become key considerations when using filtering techniques for navigation solutions operationally, and are especially pertinent to autonomous operations.

## 10.1. Editing

<span id="page-124-1"></span>Let r = y−h(x), where y is the observed measurement, h(x) is the value of the measurement computed from the state x, y = h(x) + v, and v is the measurement noise, E[v] = 0, E[vv<sup>T</sup> ] = R. The quantity r is known as the innovation or sometimes the pre-fit residual. The covariance of r is given by

| $\mathbf{W} = \text{HPH}^T + \mathbf{R}$ | (10.1) |
|------------------------------------------|--------|
|------------------------------------------|--------|

 $\mathbf{W} = \mathbf{HPH}^T + \mathbf{R}$  (10.1)

where P = E[ee<sup>T</sup> ], H = ∂h(x)/∂x, and e is the error in the estimate of x. The squared Mahalanobis distance associated with r,

$$m_r^2 = r^T \mathbf{W}^{-1} r \quad (10.2)$$

$$m_{\mathbf{r}}^2 = \mathbf{r}^T \mathbf{W}^{-1} \mathbf{r} \quad (10.2)$$

has a χ <sup>2</sup> distribution with degrees of freedom equal to the number of measurements contained in the vector y. The statistic m<sup>2</sup> r , also known as the squared residual or innovations ratio, may be compared to a χ 2 statistic with a given probability in order to edit outlying measurements. For a purely linear estimation scheme, such editing is unnecessary, but for an ad hoc linearization such as the EKF, editing is essential to prevent large innovations that would violate Taylor series truncations used to develop the EKF approximation, even in the unlikely scenario in which sensors produced measurements with noise characteristics that perfectly followed their assumed (Gaussian) probability distributions.

Experience has shown that it is beneficial to provide for a command-able capability to selectively apply a three-way editing flag to each measurement type. This flag may be enumerated with the labels "accept," "inhibit," and "force," or similar. The "accept" label denotes use of the measurement, if it is accepted by the aforementioned edit test (in the parlance used by Shuttle and Orion, this flag is labeled "auto"). The "inhibit" flag indicates that the measurement should be rejected regardless of the status of the edit test. The "force" flag correspondingly indicates that the measurement should be ingested regardless of the edit test result.

Additional measurement edit or selection parameters may be considered to identify invalid measurements for filter processing and state update, as applicable to the orbit regime or application. The following categories capture a representative set of these criteria:

- Satisfying time constraints. For example, elapsed time from the last successful measurement update is greater than or equal to a threshold value, such as the expected measurement sampling interval.
- Satisfying transmitter or sensor performance and operability criteria. For example, transmitter or sensor are not available, or enabled, and/or have no valid state vector or ephemeris, or exhibits an errant telemetry value that violates a specified tolerance.
- Acceptance for processing measurements that occur during a maneuver time span. NOTE: This criteria type strongly depends on the procedure for process noise adjustments to accommodate maneuvers. If a maneuver is known to occur, then the filter operator may elect to introduce additional process noise to allow state update from the measurements during or soon after the maneuver span and reflect a more representative covariance during that period. Depending on the filter tuning, measurement processing for a state update across or after a small maneuver may not need an increase in process noise.
- Satisfying measurement-type specific selection criteria. For example, include only valid measurements: according to the GNSS receiver selection criteria for GPS space vehicles; that meet radial distance constraints to achieve minimum signal-to-noise ratio (SNR); when the receiving antenna boresight angle falls within the specified minimum and maximum constraints.
- Satisfying visibility criteria.

Visibility tests may take on different forms, but can generally be categorized as criteria that interrupt or corrupt the line of sight for the sensed observation. Editing accommodation may be needed to handle scenarios where the line of sight between a source (e.g. transmitter, celestial body for imaging) and the measuring sensor (e.g. receiver, camera) is

- interrupted by an occultation, e.g. the Moon blocks the view to Earth;
- corrupted by an element known to introduce multipath reflections, like a spacecraft appendage; or
- degraded by expected interference in sensor performance, such as an angular keep-out zone to ensure the Sun-Earth-Probe angle meets the minimum threshold for signal-tonoise for a viable measurement.

One common example for visibility editing criteria occurs when the line of sight of the received signal from the transmission source travels through a path of ionospheric or atmospheric disturbance above a specified tolerance. To avoid these corrupted observations adversely influencing the filter solution accuracy, it may be suitable to preclude these observations from a state update. Relevant editing schemes include Height of Ray Path (HORP) and Transmit-to-Receive elevation angle.

10.1.1. Height of Ray Path Editing The HORP test is useful for measurements obtained from a signal between two orbiting assets. The edit test is predicated on defining the distance of the transmission path, or ray path, between the two orbiting assets with respect to the central body radius, followed by a comparison of that distance to the sum of the central body radius plus defined altitudes for the atmospheric interference zone. Figure [10.1](#page-126-0) portrays a case where the signal ray path incurs no violation, while in Figure [10.2](#page-126-1) the signal ray path passes through the defined atmospheric region to be considered for edit. The HORP test can be used to identify and edit for occultations by using an altitude of zero km above the occulting body.

![](_page_126_Diagram_2.jpeg)

Figure 10.1. Signal Ray Path Above the Defined Atmosphere Region

<span id="page-126-0"></span>![](_page_126_Diagram_4.jpeg)

<span id="page-126-1"></span>Figure 10.2. Signal Ray Path Transits Through the Defined Atmosphere Region

The HORP editing test starts by computing the distance between the two orbiters at the specific time instance:

$$d = \|\vec{d}\| = \left\| \vec{R}_s - \frac{\vec{x}(\vec{x} \cdot \vec{R}_s)}{x^2} \right\| \quad (10.3)$$

where x = ∥ $\vec{x}$∥,

$$\vec{x} = \vec{R} - \vec{R}_s \quad (10.4)$$

and

$\vec{R}$ <sup>s</sup> = transmitter satellite position vector at the measurement time

$\vec{R}$ = receiver position vector at the measurement time

<span id="page-127-1"></span>Accept the measurement if d ≥ R<sup>e</sup> + h, [Figure [10.1\]](#page-126-0), where R<sup>e</sup> equals the mean equatorial radius of the Earth (or relevant central body) and h is the height of the atmosphere (a configurable parameter, based on the atmosphere applicable to the central body).

If d < R<sup>e</sup> + h [Figure [10.2\]](#page-126-1), compute

$$\delta = x' - \sqrt{(R_e + h)^2 - d^2} \quad (10.5)$$

where

$$x' = \begin{vmatrix} \vec{x} \cdot \vec{R}_s \\ x \end{vmatrix} \quad (10.6)$$

If x ′ ≤ δ, accept the measurement.

If x ′ > δ, accept the measurement if α < αmax, where αmax is the maximum central angle, a configurable parameter, nominally equal to 70 degrees for Earth as a central body, given by

$$\alpha = \cos^{-1} \left( \frac{\vec{R}_s \cdot \vec{R}}{R_s R} \right) \quad (10.7)$$

and R<sup>s</sup> = ∥$\vec{R}$ <sup>s</sup>∥, R = ∥ $\vec{R}$ ∥.

10.1.2. Elevation Angle Editing An elevation angle editing test can be used to identify measurements that may be impacted by a known multipath source, a long path through the atmosphere between a ground antenna and the spacecraft, a lower SNR from a spill-over signal that may originate beyond an antenna pattern threshold, or other impacting sources that can be defined through an angular constraint. Figure [10.3](#page-127-0) depicts an example used herein, which represents editing for when the line of sight between a ground station and spacecraft falls below a local horizon minimum elevation. Case A represents accepted measurements and Case B represents measurements for editing.

![](_page_127_Figure_12.jpeg)

<span id="page-127-0"></span>Figure 10.3. Elevation Angle Test, Represented for Ground Station to Spacecraft Atmosphere Transit

Compute the instantaneous line-of-sight vector from the receiving satellite to the ith transmitting ground station (GS) as follows:

$$\bar{\rho}^i = \bar{R}(t_k) - \bar{R}_{\text{GS}}^i(t_k) \quad (10.8)$$

where

---

$$\vec{R}(t_k) =$$
 position vector of the receiving satellite at time  $t_k$   
 $\vec{R}^i_{\text{GS}}(t_k) =$  position vector of the  $i$ th transmitting GS at time  $t_k$ 

The editing test is based on whether the elevation angle, E, of the line-of-sight vector with respect to the local horizon is greater than a minimum elevation angle, Emin. The measurement is accepted (Fig [10.3,](#page-127-0) Case A) if the following is true:

| $\sin E > \sin E_{\min}$ | (10.9) |
|--------------------------|--------|
|--------------------------|--------|

where Emin is a commandable minimum elevation angle within the ±90 degrees range, and Emin and E are positive above the local horizon and negative below the horizon. In addition, sin E is computed as:

$$\sin E = \frac{\vec{\rho}^i \cdot \vec{R}_{\text{GS}}^i(t_k)}{\|\vec{\rho}^i\| \|\vec{R}_{\text{GS}}^i(t_k)\|} \quad (10.10)$$

Otherwise, the measurement is edited and not used to update the state.

10.1.3. General Angle Editing One can apply angular editing tests to other mission constraints, such as an angle between the signal source-to-sun vector and the signal source-to-spacecraft to avoid solar scintillation impacts on the signal that may corrupt the navigation observable. A common application is when the signal source is a ground station on Earth; then the resultant angle is referred to as the Sun-Earth-Probe angle. In this example shown in Figure [10.4,](#page-128-0) this angle is denoted as α. Note that the signal source may be a relay spacecraft or a GNSS space vehicle. The threshold angle, αmin, is a configurable parameter and may vary depending on the spacecraft's distance to the sun and the power-level of the signal between the spacecraft and source.

$$\alpha(t_k) = \cos^{-1} \left( \frac{\vec{R}_S(t_k) \cdot \vec{R}_{\text{GS-SC}}(t_k)}{R_S(t_k) R_{\text{GS-SC}}(t_k)} \right) \quad (10.11)$$

where

---

$$\vec{R}_S(t_k) =$$
 Ground Station to Sun vector at the measurement time,  $t_k$ 
 $\vec{R}_{\text{GS-SC}}(t_k) =$  Ground Station to Spacecraft vector at the measurement time,  $t_k$ 

---

Accept the measurement if α > αmin. Otherwise, the measurement is edited and not used to update the state.

![](_page_128_Diagram_14.jpeg)

<span id="page-128-0"></span>Figure 10.4. General Angle Editing Test Applied to Sun-Earth-Probe Angle

## 10.2. Reinitialization and Restarts

<span id="page-129-0"></span>Since no EKF can be guaranteed to remain converged, it is prudent to provide for features that can ease the process of recovering nominal filter operation . While to a large extent the particulars of each application will guide a designer to select among a variety of filter recovery features, a few general design principles are broadly relevant.

Experience has shown that the fairly drastic step of completely re-initializing the filter may not always be necessary or prudent. In particular, under conditions in which it is reasonably clear that the filter has begun to edit measurements because its covariance matrix has become overly optimistic, but there remains reason to believe that the state estimate has not yet become corrupted, it may be beneficial to reinitialize the covariance while retaining the current state estimate. It may also be desirable to retain flexibility to retain only the position/velocity state components, while reinitializing the various bias components.

If the filter has halted for some reason other than divergence (e.g. a flight computer reset), or if the start of the divergence can be reliably determined, it may be useful to "restart" the filter from a previously saved state and covariance, especially if there would otherwise be a long time required for re-convergence. To enable such a restart capability, the full state and covariance must have been periodically saved, and then they must be propagated to the restart time.

## 10.3. Backup Ephemeris

<span id="page-129-1"></span>A backup ephemeris can be a useful tool with navigation filters, serving as:

- a comparison to the filtered estimate, providing an input to fault detection based on commandable tolerances to detect degraded filter performance;
- a reinitialization state, if needed by an onboard filter based on mission-defined tolerance violation, or a previously identified fault response, or when a ground uplink is known to not be available in a timely manner;
- an alternative navigation estimate that can be reliably propagated without any measurement updates to maintain spacecraft orbit knowledge for health and safety and communication link pointing, e.g. in case of a safe-mode trigger or other case whereby the onboard filter is disabled.

Backup ephemeris can be instantiated by several representations, and the selected representation should be based on the mission operations concept, data systems employed, risk level, and requirements. In addition, the selected mean element variable set must align with the proper mean theory [[84](#page-173-16), Section 9.7.3]. Backup ephemerides based on Brouwer-Lyddane mean orbital elements and rates offer a mean representation of the orbit over a defined time period. The mean element representation given in Table [1](#page-130-0) has been used successfully on near-circular LEO and GEO missions (not at the critical inclination of 63.483 degrees), and used onboard to support navigation fault detection, isolation, and recovery [[31](#page-171-22)]. To obtain a backup ephemeris from a filtered estimate, the process usually involves converting the predicted osculating elements to Brouwer-Lyddane mean elements. The Brouwer-Lyddane mean elements will deteriorate over time, especially if the propagation or conversion does not account for the non-gravitational perturbations, such as atmospheric drag for a LEO orbit or solar radiation pressure for a GEO orbit. When used as a backup ephemeris, the accuracy expected from Brouwer-Lyddane mean elements, along with the expected coverage period and update rate for the orbital element set, must be taken into consideration according to the use case.

Chebyshev polynomials provide another option to represent a backup ephemeris, and may offer a consistent representation format for the spacecraft as well as celestial bodies. The Spacecraft

<span id="page-130-0"></span>Table 1. Brouwer-Lyddane Mean Elements

| Element | Unit  | Description                              |
|---------|-------|------------------------------------------|
| T       | days  | Epoch of the elements                    |
| a       | m     | Semi-major axis                          |
| e       | n/a   | Eccentricity                             |
| i       | deg   | Inclination                              |
| ω       | deg   | Argument of periapsis                    |
| Ω       | deg   | Right Ascension of Ascending Node (RAAN) |
| M       | deg   | Mean anomaly                             |
| a ˙     | m/s   | Semi-major axis rate                     |
| ω ˙     | deg/s | Argument of periapsis rate               |
| Ω˙      | deg/s | RAAN rate                                |
| M ˙     | deg/s | Mean anomaly rate a                      |

<span id="page-130-1"></span>a In Reference [[31](#page-171-22)], the mean anomaly rate, M˙ , for a LEO polar orbiting case combined mean anomaly and argument of periapsis as

$$\dot{M} = \frac{[M(t_2) + \omega(t_2)] - [M(t_1) + \omega(t_1)]}{t_2 - t_1}$$

whereas, for the GEO low inclination case, M˙ also includes RAAN to give

$$\dot{M} = \frac{[M(t_2) + \omega(t_2) + \Omega(t_2)] - [M(t_1) + \omega(t_1) + \Omega(t_1)]}{t_2 - t_1}$$

The expected accuracy of the Brouwer-Lyddane elements for the respective orbit representations are on the order of tens of kilometers, which serves the purposes for the mission.

Planet Instrument C-matrix Events [\(SPICE\)](https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/req/spk.html) toolkit offered by NASA's Navigation and Ancillary Information Facility [\(NAIF\)](https://naif.jpl.nasa.gov/naif/index.html) provides commonly accepted utilities for Chebyshev polynomials from an ephemeris (Types 2, 3, 14, and 20), as well as Hermite interpolators to evaluate the polynomial at a selected epoch (Types 12 and 13). While it is possible to compute mean elements or Chebyshev polynomials onboard, the computational overhead may induce a mission to periodically upload these types of backups from the ground.

In some applications, such as use of measurements from a Global Navigation Satellite System receiver, the receiver's independent "point solution" may serve as a useful comparison source. The periodically saved filter state that contains the full state and covariance, discussed as a means to restart the filter, also provides capability to maintain a backup ephemeris. For flight phases of limited duration, the backup ephemeris may be propagated inertially without any measurement updates. For extended operations, it will usually be necessary to re-seed the backup with a current filter state at periodic intervals.

Averaged equinoctial elements offer a more accurate backup that aligns with autonomous operations and onboard processing capabilities, and more readily accommodate all trajectory types because they avoid the singularities found in classical elements. In particular, an equinoctial system of elements can be defined to represent any inclination or eccentricity, including e = 0 and e > 1. Selecting equinoctial elements and rates that vary slowly can be especially useful in a mission with variable or low-thrust. Lastly, equinoctial elements can be transformed to Cartesian or Keplerian elements. Elements averaged over a period of time that sufficiently represents the trajectory based on the filter estimates can serve as a state for comparison or to reinitialize a navigation filter to start state estimation.

The following set of equinoctial elements [[6](#page-170-18), [15](#page-170-19)], have been successfully implemented and operationally used in onboard filters. Table [2](#page-131-0) provides a definition of the equinoctial elements (a, h, k, p, q, λ), based on the classical Keplerian elements (a, e, i, Ω, ω, M). As Table [2](#page-131-0) describes, the equinoctial elements can be interpreted in terms of an equinoctial coordinate frame, whose principal direction, xˆep, is the "origin of longitudes" as shown in Figure [10.5.](#page-132-0)

<span id="page-131-0"></span>Table 2. Equinoctial Element System

| Element Definition                                                                | Conversion from    |
|-----------------------------------------------------------------------------------|--------------------|
|                                                                                   | Keplerian Elements |
| a Semi-major axis a                                                               |                    |
| h Projection of the eccentricity vector $\vec{e}$ on the y ˆ ep axis e sin(             | ω + Ω)             |
| k Projection of the eccentricity vector $\vec{e}$ on the x ˆ ep axis e cos(             | ω + Ω)             |
| p Projection of the nodal vector $\vec{N}$ on the y ˆ ep axis                           |                    |
| tan                                                                               |                    |
|                                                                                   |  j               |
|                                                                                   | sin Ω              |
| q Projection of the nodal vector $\vec{N}$ on the x ˆ ep axis                           |                    |
| tan                                                                               |                    |
|                                                                                   |  j               |
|                                                                                   | cos Ω              |
| λ Mean longitude M +                                                              | ω + Ω              |
| $\vec{e}$ = eccentricity vector pointing in the direction of the x ˆ p axis (perifocus) | with a magnitude   |
| equal to the orbital eccentricity                                                 |                    |
| $\vec{N}$ = nodal vector pointing in the direction of the ascending node with a         | magnitude equal to |
| tan                                                                               |                    |
|  j                                                                              |                    |
| where i denotes the orbital inclination and j is defined                          | as:                |
| j = 1 for direct orbits (0 ≤ i ≤ 90 ◦                                             |                    |
| ) ; j = − 1 for retrograde orbits                                                 | (90 < i ≤ 180 ◦    |

These equinoctial elements can be averaged over more than one orbital period to define an averaged set of elements and associated rates.

$$\overline{(E_i)}_{\text{ref}}^0 = \frac{1}{N+1} \sum_{n=0}^N E_i(t_0 + n \delta t), i = 1, 5 \quad (10.12)$$

$$\overline{(E_6)}_{\text{ref}}^0 = \lambda(t_{\text{ref}}) \quad (10.13)$$

<span id="page-132-1"></span>![](_page_132_Diagram_2.jpeg)

<span id="page-132-0"></span>Figure 10.5. The Equinoctial Coordinate Frame

where

(Ei)

0 ref <sup>=</sup> reference averaged equinoctial element vector (a¯, <sup>h</sup>¯, ¯k, p¯, q¯, λ¯) associated with the current reference time, tref tref = reference time for a new set of reference averaged equinoctial elements, equal to the center of the averaging interval t<sup>0</sup> = time of the first point in the current summation interval Ei(t) = component of osculating equinoctial element vector at time t obtained from the osculating position and velocity vectors N = number of osculating equinoctial element sets included in the summation δt = time interval between successive osculating equinoctial elements included in the summation, commandable parameter (recommended to be on the order of

one (1) second

The value of N should be chosen so the average is performed over one spacecraft orbital period to within a commandable tolerance.

$$N = 2 \left( \text{int} \left[ \frac{P + \delta t}{2\delta t} \right] \right) \quad (10.14)$$

where

$$P = 2\pi \sqrt{\frac{\left(a_{\text{ref}}^{-1}\right)^3}{\mu_{\text{CB}}}} \quad (10.15)$$

and

µCB = gravitation constant of the central body

a −1 ref = reference averaged semi-major axis associated with the prior set of reference

averaged equinoctial elements

Equinoctial element rates for semi-major axis and mean longitude are computed as follows using the average for each element over the current and previous orbital periods:

$$\overline{a}_{\text{ref}}^0 = \frac{1}{t_{\text{ref}} - t_{\text{ref}}^{-1}} \left[ a_{\text{ref}}^0 - a_{\text{ref}}^{-1} \right] \quad (10.16)$$

$$\bar{\lambda}_{\text{ref}}^0 = \frac{1}{t_{\text{ref}} - t_{\text{ref}}^{-1}} \left[ \bar{\lambda}_{\text{ref}}^0 - \bar{\lambda}_{\text{ref}}^{-1} + 2\pi \right] \quad (10.17)$$

Averaged equinoctial elements assume that there is not a large change in the eccentricity vector or node over successive orbital periods; hence they should not be used over large discrete maneuvers unless special care is taken. Therefore, generally, rates for the other elements are assumed to be zero. If a maneuver does occur, the computation should be restarted.

To obtain the averaged equinoctial state vector at the current time, tc, perform the computation as follows:

$$\overline{E(t_c)} = \overline{E_{\text{ref}}^{-2}} + \frac{\overline{E_{\text{ref}}^{-2}}}{E_{\text{ref}}} \Delta t \quad (10.18)$$

where

E(tc) = vector of averaged equinoctial elements (listed in Table [2\)](#page-131-0) evaluated at time t<sup>c</sup> E −2 ref = vector of reference averaged equinoctial elements at reference time t −2 ref ˙E −2 ref = vector of reference averaged equinoctial element rates at reference time t −2 ref t −2 ref = reference time of the reference equinoctial elements and rates computed over the orbital period prior to the last ∆t = the time difference between the current time and the time of the reference equinoctial elements and rates two orbits prior, t<sup>c</sup> − t −2 ref

#### 10.4. Ground System Considerations

<span id="page-133-0"></span>The operations concept, requirements on the onboard filter performance and products derived from the filter estimate, whether derived onboard or on the ground, filter commissioning, anomaly resolution, and performance monitoring are critical factors to consider in designing a ground system commensurate with the mission needs. The command and telemetry parameters necessary to understand filter performance and the derived products need to be designed into the mission as early in the design life cycle as possible. Filter operation, expected performance, known signatures or constraints on operation, and any maintenance at the requisite cadence should be documented and maintained throughout the mission lifetime. Default and current filter tuning parameters and variables that effect operating modes should be archived for ready access in case of a cold restart or for troubleshooting. While it may seem intuitive that all parameters affecting filter performance should be available for re-tuning from the ground via mechanisms such as commands, table uploads, etc., experience has shown that decisions about ground system design and telemetry and commanding constraints often limit the accessibility of key tuning parameters. Adequate bandwidth in telemetry for full insight into filter performance, including access to full covariance data, the restart record discussed above, and the backup ephemeris must be available, if only for limited periods during commissioning and/or troubleshooting activities. As a best practice, a comprehensive snapshot of the filter performance including the restart record (full state and covariance), and performance metrics on editing, measurement update, and tolerance parameters should be made available in telemetry at a regularly defined cadence commensurate with the mission concept and orbit regime .

The complementary side is that the ground system must be able to reproduce the onboard filter's performance when provided with corresponding input data via downlinked telemetry. Empirical evidence recommends that the ground system include the ability to use a high-fidelity and tunable representation of the filter to address current performance, analyses, and troubleshooting for anomaly resolution. This includes access to default, current, and prior upload parameters for modeling and tuning.

Often, the filter estimate developed onboard is used by the ground system to create subsequent products for the mission. This includes the use of the as-telemetered filter state for predictive planning products or analysis for covariance realism. In some cases, it may be necessary to develop a best estimated trajectory (BET), the generation of which may require alternate tuning or additional processing (e.g. through the use of smoothing algorithms) on the ground to achieve the most accurate orbit knowledge. The BET can be used to comparatively analyze filter performance, or may be a source for predictive products for mission objective planning or projected filter performance under alternative scenarios.

Careful consideration should be given to comprehensive operations concepts and usage for onboard filters. These include editing methods, availability of restart records, the need for and type of backup ephemeris, appropriate access for tuning and modeling changes, adequate information content available in telemetry, and the appropriate instantiation of a ground system for filter commissioning and performance monitoring throughout the mission lifetime.

![](_page_135_Picture_1.jpeg)

## Smoothing

<span id="page-136-0"></span>Contributed by Christopher N. D'Souza and J. Russell Carpenter

Since this work is primarily concerned with onboard navigation filters, one might question the need for a chapter on best practices for smoothing. While the addition of a smoother to an onboard navigation system has usually proved unnecessary, smoothing has nonetheless proved to be a useful ancillary capability for trajectory reconstruction by ground-based analysts. Smoothed trajectories form the basis for our best proxies for truth, in the form of "best estimated trajectories," (BET) and McReynold's "filter-smoother consistency test," propagated by Jim Wright [[90](#page-173-17)], has proven to be a useful aid to tuning a filter using flight data. Also, sequential smoothing techniques can provide optimal estimates of the process noise sequence, as Appendix X of Bierman's text [[5](#page-170-1)] shows. These estimates may prove useful as part of the filter tuning process.

It is also worth mentioning the topic of "smoothability." As described in for example Gelb [[27](#page-171-5)], only states that are controllable from the process noise will be affected by smoothing. So for example, estimates of random constant measurement biases cannot be improved by smoothing.

In point of fact there are three types of smoothing: fixed-interval smoothing, fixed-lag smoothing, and fixed-point smoothing. The context described above is concerned with fixed-interval smoothing. Maximum likelihood estimation (MLE) of states over a fixed interval has been subject of investigation ever since the advent of the Kalman filter [[44](#page-171-1)] in 1961. In 1962, Bryson and Frazier first approached the problem from a continuous time perspective [[8](#page-170-20)] and obtained the smoother equations as necessary conditions of an optimal control problem[†](#page-136-1) . In 1965, Rauch, Tung and Striebel [[70](#page-172-19)] (RTS) continued the development of the MLE filters but from a discrete time perspective. Their smoother, soon called the RTS smoother, was widely used because of its ease of implementation. However, as Bierman [[5](#page-170-1)] and others [[61](#page-172-20)] pointed out, there can sometimes arise numerical difficulties in implementing the RTS smoother. A short time later Fraser and Potter [[24](#page-171-23), [25](#page-171-24)] approached the problem a bit differently, looking at smoothing as a optimal combination of two optimal linear filters and obtained different, yet equivalent, equations. Bierman's Square-Root Information Filter [[5](#page-170-1)] (SRIF) also has an accompanying smoother form, suitable for applications utilizing the SRIF. Since the Fraser-Potter form avoids the numerical issues of the RTS form, and since it can be easily adapted from existing onboard Kalman-type forward filtering algorithms, it is generally to be preferred.

The boundary conditions for the Fraser-Potter (FP) smoother require the backward covariance at the final time to be infinite, and the backward filter's final state to be zero. Fraser and Potter avoided the infinity by maintaining the backward filter covariance in information form, so that both the information matrix and the information vector are zero. As Brown points out [[7](#page-170-3)], the

<span id="page-136-1"></span><sup>†</sup>The Bryson-Frazier smoother is a continuous time instantiation of the smoother. It won't be considered here for we are interested in discrete smoothers. [[8](#page-170-20)]

backward filter may be retained in covariance form, and the infinite boundary condition covariance replaced by either a covariance that is many multiples of the forward filter's initial covariance, or by the covariance and state from a short batch least-squares solution using the final few measurements. Many practical smoother implementations used by NASA have followed an approach of this sort.

Thus, a practical covariance form of the FP smoother results from running whatever implementation of Algorithm [1.3](#page-30-0) has proved suitable for the application at hand, but in reverse time, and combining the backward filter results with the forward filter results at each measurement time. Given the forward filter state and covariance, Xˆ <sup>+</sup> F<sup>i</sup> and P + F<sup>i</sup> , which include the measurement at t<sup>i</sup> , and the backward filter state and covariance, Xˆ <sup>−</sup> B<sup>i</sup> and P − B<sup>i</sup> , which do not include the measurement at t<sup>i</sup> , the optimally smoothed state and covariance at t<sup>i</sup> are given by

$$\hat{\mathbf{X}}_i^S = \mathbf{P}_i^S \left[ (\mathbf{P}_{\mathbf{F}_i})^{-1} \hat{\mathbf{X}}_i^+ + (\mathbf{P}_{\mathbf{B}_i})^{-1} \hat{\mathbf{X}}_{\mathbf{B}_i} \right] \quad (11.1)$$

$$\mathbf{P}_i^S = \left[ (\mathbf{P}_{F_i}^+)^{-1} + (\mathbf{P}_{B_i}^-)^{-1} \right]^{-1} \quad (11.2)$$

If covariance form is to be retained, the tedious number of inverses apparent in Eqs. [\(11.1\)](#page-137-0) and [\(11.2\)](#page-137-1) may be avoided as follows. Suppose we define the smoothed state as a linear fusion of the forward and backward filter states:

<span id="page-137-4"></span><span id="page-137-1"></span><span id="page-137-0"></span>
$$\hat{\mathbf{X}}_i^S = \mathbf{W}_{F_i} \hat{\mathbf{X}}_i^+ + \mathbf{W}_{B_i} \hat{\mathbf{X}}_i^- \quad (11.3)$$

For Xˆ <sup>S</sup> i to be unbiased, we must choose either WF<sup>i</sup> = I − WB<sup>i</sup> or WB<sup>i</sup> = I − WF<sup>i</sup> . Choosing the latter, the smoothed state becomes

$$\hat{\mathbf{X}}_i^S = \mathbf{W}_{F_i} \hat{\mathbf{X}}_{F_i}^+ + (\mathbf{I} - \mathbf{W}_{F_i}) \hat{\mathbf{X}}_{F_i}^- \quad (11.4)$$

Given the enforced lack of correlation between the forward and backward filters, the fused (smoothed) covariance is given by

$$\mathbf{P}_i^S = \mathbf{W}_F \mathbf{P}_F^T \mathbf{W}_F^T + \mathbf{W}_B \mathbf{P}_B^T \mathbf{P}_B^T \mathbf{W}_B^T \quad (11.5)$$

$$= \mathbf{W}_{F_i} \mathbf{P}_{F_i}^{-1} \mathbf{W}_{F_i}^T + (\mathbf{I} - \mathbf{W}_{F_i}) \mathbf{P}_{B_i}^{-1} (\mathbf{I} - \mathbf{W}_{F_i})^T \quad (11.6)$$

Choosing WF<sup>i</sup> to minimize the trace of P S i results in

$$\mathbf{W}_{F_i} = \mathbf{P}_{B_i}^-(\mathbf{P}_{F_i}^+ + \mathbf{P}_{B_i}^-)^{-1} \quad (11.7)$$

To see that Eq. [\(11.6\)](#page-137-2), with Eq. [\(11.7\)](#page-137-3), is equal to Eq. [\(11.2\)](#page-137-1), expand Eq. [\(11.6\)](#page-137-2), substituting Eq. [\(11.7\)](#page-137-3), and recall Woodbury's identity:

$$\left[ (\mathbf{P}_{F_i}^+)^{-1} + (\mathbf{P}_{B_i}^-)^{-1} \right]^{-1} = \mathbf{P}_{B_i}^- - \mathbf{P}_{B_i}^- (\mathbf{P}_{F_i}^+ + \mathbf{P}_{B_i}^-)^{-1} \mathbf{P}_{B_i}^- \quad (11.8)$$

<span id="page-137-6"></span><span id="page-137-5"></span><span id="page-137-3"></span><span id="page-137-2"></span>
$$= \mathbf{P}_{F_1}^+ - \mathbf{P}_{F_1}^+(\mathbf{P}_{F_1}^+ + \mathbf{P}_{B_1})^{-1}\mathbf{P}_{F_1}^+ \quad (11.9)$$

To see that Eq. [\(11.4\)](#page-137-4), with Eq. [\(11.7\)](#page-137-3), is equal to Eq. [\(11.1\)](#page-137-0), use Eq. [\(11.8\)](#page-137-5) to show that P S i (P − B<sup>i</sup> ) <sup>−</sup><sup>1</sup> = WB<sup>i</sup> and use Eq. [\(11.9\)](#page-137-6) to show that P S i (P + ) <sup>−</sup><sup>1</sup> <sup>=</sup> <sup>W</sup>F<sup>i</sup> .

F<sup>i</sup> In a typical application, the forward filter has been running continuously onboard the vehicle, and ground-based analysts will periodically wish to generate a BET over a particular span of recently downlinked data. If the telemetry system has recorded and downlinked the full state and covariance at each measurement time, along with the measurements, the ground system need only run a "copy" of the forward filter backwards through the measurements and fuse the data according to Eqs. [\(11.1\)](#page-137-0) and [\(11.2\)](#page-137-1). Care must be taken that regeneration of the state transition matrices and process noise covariances is consistent with the forward filter's modeling, and with the negative flow of time.

For various reasons, it may be necessary or desirable to run the forward filter on the ground as well, e.g. with higher-fidelity modeling than the onboard implementation permits. If so, it is efficient to store the state transition matrices and process noise covariances computed in the forward pass for use in the backward filter. In this case, Brown shows that the backward covariance may be propagated using

$$\mathbf{P}_{B_i} = \mathbf{\Phi}_{i+1, i}^{-1} \left[ \mathbf{P}_{B_{i+1}}^+ + \mathbf{S}_{i+1} \right] \mathbf{\Phi}_{i+1, i}^{-1} \quad (11.10)$$

![](_page_139_Picture_1.jpeg)

## Advanced Estimation Algorithms

<span id="page-140-0"></span>This chapter will describe advanced estimation algorithms that have yet to achieve the status of best practices, but which appear to the contributors to have good potential for someday reaching such status.

> <span id="page-140-1"></span>The Sigma-Point Estimator Contributed by J. Russell Carpenter

Derivative-free state estimation techniques have received increasing attention in recent years. A particular class of such estimators make use of the columns of the factors of the estimators' error covariance matrices, which are scaled to form vectors that have become generally known as "sigma points." The so-called "Unscented Kalman Filter" [[41](#page-171-25), [42](#page-171-26), [52](#page-172-21)] is a particular example of a sigma-point filter. A more general form is the divided-difference sigma-point filter, which is a sequential estimator that replaces first-order truncations of Taylor series approximations with second-order numerical differencing equations to approximate nonlinear dynamics and measurement models [[64](#page-172-22), [65](#page-172-23)]. If the process and measurement noise enter the system additively, Lee and Alfriend showed that several simplifications are possible, including a substantial reduction in the number of sigma-points [[51](#page-172-24)]. They refer to this construction as the Additive Divided Difference Sigma-Point Filter (ADDSPF).

This section highlights some broad aspects of sigma-point filtering, then briefly reviews how the ADDSPF works. It concludes with some brief comments comparing the ADDSPF to other sequential filters.

The Sigma-Point Filter In its most general form, the sigma-point filter performs sequential estimation of the n-dimensional state, x, whose nonlinear dynamics over the time interval [tk, tk+1] are given by

| $\mathbf{x}_{k+1} = \mathbf{f}(\mathbf{x}_k, \mathbf{w}_k)$ | (12.1) |
|-------------------------------------------------------------|--------|
|-------------------------------------------------------------|--------|

The process noise input, w, consists of independent increments whose first two moments are E[wk] = 0 and E[wkw<sup>ℓ</sup> ] = Q<sup>k</sup> δkℓ, where δkℓ is the Kronecker delta. Although the second moment may be a function of the time index, this estimator assumes that all of the samples of w arise from the same type of distribution, and this work further assumes that this distribution is Gaussian, so that higher-order moments may be neglected.

The filter sequentially processes an ordered set of measurements, <sup>Y</sup><sup>k</sup> = [y<sup>0</sup> , y<sup>1</sup> , ..., y<sup>k</sup> ] of the form

| $\mathbf{y}_k = \mathbf{h}(\mathbf{x}_k, \mathbf{v}_k)$ | (12.2) |
|---------------------------------------------------------|--------|
|---------------------------------------------------------|--------|

where the measurement noise input, v, consists of independent and identically distributed (again, in this work, Gaussian) increments whose first two moments are E[vk] = 0 and E[vkv<sup>ℓ</sup> ] = Rkδkℓ.

By contrast, the ADDSPF utilizes models where the noise sources enter additively:

$$\mathbf{x}_{k+1} = \mathbf{f}(\mathbf{x}_k) + \mathbf{g}(\mathbf{x}_k)\mathbf{w}_k \quad (12.3)$$

and

$$\mathbf{y}_k = \mathbf{h}(\mathbf{x}_k) + \mathbf{v}_k. \quad (12.4)$$

All sigma-point filters utilize a linear measurement update equation of the form

<span id="page-141-0"></span>
$$\hat{\mathbf{x}}_k^+ = \hat{\mathbf{x}}_k + \mathbf{K}_k \left( \mathbf{y}_k - \hat{\mathbf{y}}_k^- \right) \quad (12.5)$$

where the accented variables in Eq. [\(12.5\)](#page-141-0) denote conditional expectations, as in the Kalman filter:

$$\hat{\mathbf{x}}_k^+ = \mathbf{E}[\mathbf{x}_k|\mathbf{Y}_k] \quad (12.6)$$

$$\hat{\mathbf{x}}_k^- = \mathbf{E}[\mathbf{x}_k|\mathbb{Y}_{k-1}] \quad (12.7)$$

$$\hat{\mathbf{y}}_k^- = \mathbf{E}[\mathbf{y}_k|\mathbb{Y}_{k-1}] \quad (12.8)$$

The gain matrix, K, is based on conditional covariances, as in the Kalman filter:

$$\mathbf{K}_k = \mathbf{P}_{xy_k} \left( \mathbf{P}_{yy_k}^{-1} \right)^{-1} \quad (12.9)$$

$$\mathbf{P}_k^- = \mathbf{P}_{xx_k}^- = \mathbf{E} \left[ (\mathbf{x}_k - \hat{\mathbf{x}}_k) (\mathbf{x}_k - \hat{\mathbf{x}}_k)^T | \mathbf{y}_{k-1} \right] \quad (12.10)$$

$$\mathbf{P}_{xyk} = \mathbf{E} \left[ \left( \mathbf{x}_{\mathbf{x}} - \hat{\mathbf{x}}_{\mathbf{x}} \right) \left( \mathbf{y}_{\mathbf{y}} - \hat{\mathbf{y}}_{\mathbf{y}} \right)^T | \mathbf{y}_{\mathbf{y}} \right] \quad (12.11)$$

$$xy_k = [x^k, y^k]^T$$

$$\mathbf{P}_{yyk_1} = \mathbf{E} \left[ \left( \mathbf{y}_{\mathbf{k}} - \hat{\mathbf{y}}_{\mathbf{k}} \right) \left( \mathbf{y}_{\mathbf{k}} - \hat{\mathbf{y}}_{\mathbf{k}} \right)^T \left\| \mathbf{y}_{\mathbf{k}-1} \right\| \right] \quad (12.12)$$

<span id="page-141-1"></span>(12.13)

and the covariance associated with state estimate xˆ + k is

$$\mathbf{P}_k^+ = \mathbf{P}_{x_k}^+ = \mathbf{E} \left[ (\mathbf{x}_k - \hat{\mathbf{x}}_k^+) (\mathbf{x}_k - \hat{\mathbf{x}}_k^+)^T | \mathbb{Y}_k \right] \quad (12.14)$$

Hereafter, equations will suppress the time index if it is the same for all variables in the equation.

Estimators such as the Kalman filter estimate these conditional expectations by approximating the nonlinear functions f and h with first-order Taylor series truncations, e.g.:

$$\mathbf{f}(\mathbf{x}) \approx \mathbf{f}(\hat{\mathbf{x}}^-) + \mathbf{f}'(\mathbf{x})(\mathbf{x} - \hat{\mathbf{x}}^-) \quad (12.15)$$

where f ′ is an exact gradient. By contrast, the divided difference filter uses a second-order truncation along with numerical differencing formulas for the derivatives:

$$\mathbf{f}(\mathbf{x}) \approx \mathbf{f}(\hat{\mathbf{x}}^-) + \tilde{\mathbf{D}}_{\Delta \mathbf{x}}^{(1)} \mathbf{f}(\hat{\mathbf{x}}^-) + \tilde{\mathbf{D}}_{\Delta \mathbf{x}}^{(2)} \mathbf{f}(\hat{\mathbf{x}}^-) \quad (12.16)$$

where the divided difference operators, D˜ (i) ∆x f(xˆ <sup>−</sup>), approximate the coefficients of the multidimensional Taylor series expansion using Stirling interpolations. These interpolators difference perturbations of f(xˆ <sup>−</sup>) across a (dimensionless) interval, h, over a spanning basis set. Whether they are first-order, such as the unscented filter, or second order, sigma-point filters choose the interval so as to better approximate the moments required for the gain calculation, and choose as the spanning basis a set of sigma points, which are derived from xˆ <sup>−</sup> and the columns of the Cholesky factors of P <sup>−</sup> as follows.

The ADDSPF Let Xˆ denote the array whose columns are a particular ordering of the sigma points derived from xˆ and its corresponding covariance, P. Then

$$\hat{\mathcal{X}} = \left[ \hat{\mathbf{x}}, \hat{\mathbf{x}} + h \sqrt[n]{\mathbf{P}}_{(:,1)}, \hat{\mathbf{x}} + h \sqrt[n]{\mathbf{P}}_{(:,2)}, \dots, \hat{\mathbf{x}} - h \sqrt[n]{\mathbf{P}}_{(:,1)}, \hat{\mathbf{x}} - h \sqrt[n]{\mathbf{P}}_{(:,2)}, \dots \right] \quad (12.17)$$

where the subscript (:, i) denotes column i of the corresponding array, and P = √c P √c P T denotes a Cholesky factorization. In the sequel, the shorthand notation xˆ ± h √<sup>c</sup> <sup>P</sup> will denote the array on the right-hand side of the equation above. Then, for the ADDSPF, Ref. [51](#page-172-24) shows that as each new measurement becomes available, an array of sigma points generated from the prior update should be propagated to the new measurement time:

$$\hat{\chi}_k = \mathbf{f}(\hat{\chi}_{k-1}^+) \quad (12.18)$$

These propagated sigma points are then merged to form the state estimate just prior to incorporating the new measurement as follows:

$$\hat{\mathbf{x}}^- = \mu_h(\hat{\mathcal{X}}^-) = \frac{h^2 - n}{h^2} \hat{\mathcal{X}}_{(:,1)}^- + \frac{1}{2h^2} \sum_{i=2}^{2n+1} \hat{\mathcal{X}}_{(:,i)}^- \quad (12.19)$$

To form an associated covariance, the following divided-differences are next computed:

$$\tilde{D}_{\Delta x}^{(1)} \mathbf{f}(\hat{\mathbf{x}}^-)(:, i) = \frac{1}{2h} \left[ \hat{\mathbf{x}}_{(:, i+1)}^- - \hat{\mathbf{x}}_{(:, i+1+n)}^- \right] \quad (12.20)$$

$$\tilde{D}_{\Delta x}^{(2)} \mathbf{f}(\hat{\mathbf{x}}^-)_{(:,i)} = \frac{\sqrt{h^2-1}}{2h^2} \left[ \hat{\mathcal{X}}_{(:,i+1)}^- + \hat{\mathcal{X}}_{(:,i+1+n)}^- - 2\hat{\mathcal{X}}_{(:,1)}^- \right] \quad (12.21)$$

Ref. [51](#page-172-24) shows that the covariance may then be computed from

<span id="page-142-0"></span>
$$\mathbf{P}^- = \left[ \tilde{\mathbf{D}}_{\Delta \mathbf{x}}^{(1)} \mathbf{f}(\hat{\mathbf{x}}^-), \tilde{\mathbf{D}}_{\Delta \mathbf{x}}^{(2)} \mathbf{f}(\hat{\mathbf{x}}^-), \sqrt[n]{\mathbf{Q}_d} \right] \left[ \tilde{\mathbf{D}}_{\Delta \mathbf{x}}^{(1)} \mathbf{f}(\hat{\mathbf{x}}^-), \tilde{\mathbf{D}}_{\Delta \mathbf{x}}^{(2)} \mathbf{f}(\hat{\mathbf{x}}^-), \sqrt[n]{\mathbf{Q}_d} \right]^T \quad (12.22)$$

One advantage of sigma-point filters is that the full covariance need not be maintained, but rather only its Cholesky factor. Although the factors in square brackets in Eq. [\(12.22\)](#page-142-0) are not Cholesky factors, since each is a full n × 3n matrix, one may extract an n × n triangular factor from it using the so-called "thin" version [[30](#page-171-27)] of the QR decomposition[<sup>1</sup>](#page-142-1) , or alternatively using a Householder factorization [[5](#page-170-1)]. Thus,

$$\mathbf{M} \begin{bmatrix} \sqrt[c]{\mathbf{P}^{-T}} \\ \mathbf{O}_{2n \times n} \end{bmatrix} = \begin{bmatrix} \tilde{\mathbf{D}}_{\Delta \mathbf{x}}^{(1)} \mathbf{f}(\hat{\mathbf{x}}^-), \tilde{\mathbf{D}}_{\Delta \mathbf{x}}^{(2)} \mathbf{f}(\hat{\mathbf{x}}^-), & \sqrt[c]{\mathbf{Q}_d} \end{bmatrix}^T \quad (12.23)$$

where M is a full 3n × 3n orthonormal matrix, and O2n×<sup>n</sup> is a 2n × n matrix of zeros.

For the measurement update, a new array of sigma points must be generated from xˆ <sup>−</sup> and P −; this array is denoted Xˆ<sup>∗</sup> . These sigma points are used to generate a set of sigma points representing the measurement:

$$\hat{\mathcal{Y}}^- = \mathbf{h}(\hat{\mathcal{X}}^*) \qquad (12.24)$$

In similar fashion to the time update, the sigma points of the measurement are then merged to form the estimated measurement:

$$\hat{y}^- = \mu_h(\hat{\mathcal{D}}^-) \quad (12.25)$$

<span id="page-142-1"></span><sup>1</sup> For Matlab users, this may be accomplished in several ways, e.g. by passing the transpose of this matrix to the qr function, then keeping the first n non-zero rows from the second output, and transposing this result.

the corresponding divided-differences are computed as:

$$\tilde{D}_{\Delta \mathbf{x}}^{(1)}\mathbf{h}(\hat{\mathbf{x}}^-)_{(:,i)} = \frac{1}{2h} \left[ \hat{\mathbf{y}}_{(:,i+1)}^- - \hat{\mathbf{y}}_{(:,i+1+n)}^- \right] \quad (12.26)$$

$$\tilde{D}_{\Delta x}^{(2)} \mathbf{h}(\hat{\mathbf{x}}^-)_{(:,i)} = \frac{\sqrt{h^2 - 1}}{2h^2} \left[ \hat{\mathcal{Y}}_{(:,i+1)}^- + \hat{\mathcal{Y}}_{(:,i+1+n)}^- - 2\hat{\mathcal{Y}}_{(:,1)}^- \right] \quad (12.27)$$

and the covariances required for the gain calculation may then be computed from

$$\mathbf{P}_{yy}^- = \left[ \tilde{\mathbf{D}}_{\Delta x}^{(1)} \mathbf{h}(\hat{\mathbf{x}}^-), \tilde{\mathbf{D}}_{\Delta x}^{(2)} \mathbf{h}(\hat{\mathbf{x}}^-), \sqrt[\sqrt{R}]{\mathbf{R}} \right] \left[ \tilde{\mathbf{D}}_{\Delta x}^{(1)} \mathbf{h}(\hat{\mathbf{x}}^-), \tilde{\mathbf{D}}_{\Delta x}^{(2)} \mathbf{h}(\hat{\mathbf{x}}^-), \sqrt[\sqrt{R}]{\mathbf{R}} \right]^T \quad (12.28)$$

$$\mathbf{P}_{xy}^- = \sqrt{\mathbf{P}^-} \left[ \tilde{\mathbf{D}}_{\Delta x}^{(1)} \mathbf{h}(\hat{\mathbf{x}}^-) \right]^{\text{T}} \quad (12.29)$$

Note that the second-order divided difference for the measurement function, D˜ (2) <sup>∆</sup>xh(xˆ <sup>−</sup>), does not appear in the cross-covariance update. As with the time update, through the use of the thin QR factorization, only triangular factors need be maintained for P − yy [2](#page-143-0) :

$$\mathbf{M}_{yy} \left[ \sqrt[c]{\mathbf{P}_{yy}^{-T}} \right] = \left[ \tilde{\mathbf{D}}_{\Delta \mathbf{x}}^{(1)} \mathbf{h}(\hat{\mathbf{x}}^-), \tilde{\mathbf{D}}_{\Delta \mathbf{x}}^{(2)} \mathbf{h}(\hat{\mathbf{x}}^-), \sqrt[c]{\mathbf{R}} \right]^T \quad (12.30)$$

Now, all of the terms required for the state update (Eqs. [12.5](#page-141-0) and [12.9\)](#page-141-1), are available. Ref. [51](#page-172-24) shows that the corresponding Cholesky factor of the covariance is extracted from

$$\mathbf{M}^+ \begin{bmatrix} \sqrt[v]{\mathbf{P}^+} \\ \mathbf{O}_{2n \times n} \end{bmatrix} = \begin{bmatrix} \sqrt[v]{\mathbf{P}^-} - \mathbf{K} \tilde{\mathbf{D}}_{\Delta x}^{(1)} \mathbf{h}(\hat{\mathbf{x}}^-), & \mathbf{K} \begin{bmatrix} \tilde{\mathbf{D}}_{\Delta x}^{(2)} \mathbf{h}(\hat{\mathbf{x}}^-), & \sqrt[v]{\mathbf{R}} \end{bmatrix} \end{bmatrix} \quad (12.31)$$

The ADDSPF vs. Other Sequential Filters To conclude this section, some observations concerning the ADDSPF in comparison to other filters are offered. These observations concern the number of sigma points, the order of approximation, and the existence and method of choice of free parameters in the algorithms.

Although in many problems of practical interest the noise enters the system additively, if this is not the case, then either the original divided difference filter or the unscented filter may provide superior results to the ADDSPF, at the cost of requiring more sigma points. In both of the former algorithms, the nonlinear functions must be perturbed not only over a basis spanning the state space, but also over the discrete process noise and measurement noise spaces. Thus, rather than 2n + 1 sigma points, the more general algorithms require 2n<sup>a</sup> + 1, where n<sup>a</sup> = n + n<sup>w</sup> + nv, and n<sup>w</sup> and n<sup>v</sup> are the dimensions of the discrete process noise and measurement noise inputs.

The Kalman filter is an exact algorithm for linear stochastic systems driven by Gaussian noise, and nothing is to be gained from the use the sigma-point filters for such purely linear systems. First-order sigma-point filters such as the UKF retain the Kalman filter's first-order truncation, but avoid the need for the designer to supply explicit gradients. The divided difference filter is comparable to a derivative-free version of the modified second-order Gaussian filter [[38](#page-171-0)] in that, for symmetric distributions, it retains some terms as high as order four.

Unlike the Kalman filter, for which all of the parameters in principle can be associated with properties of the underlying stochastic system, all of the sigma point filters involve at least one free parameter. In the unscented filter, the weights for combining the sigma points involve three parameters whose physical interpretation is perhaps less clear than with the single parameter in

<span id="page-143-0"></span><sup>2</sup>Although it might seem that the full matrix P − yy is required for the gain computation of Eq. [\(12.9\)](#page-141-1), Ref. [64](#page-172-22) points out that, rather than inverting the product of the factors to compute the gain, the gain may be solved from forward and back substitution directly using the Cholesky factor.

the divided difference algorithms, where the free parameter h is clearly associated with the size of the perturbation in the numerical differencing formulae. Ref. [64](#page-172-22) shows that h should be bounded below by h > <sup>1</sup>, and that for symmetric distributions, √ h should be equal to the kurtosis, which for a Gaussian distribution is three[<sup>3</sup>](#page-144-0) .

<span id="page-144-0"></span><sup>3</sup> Some authors subtract three from the definition of kurtosis, so that Gaussian distributions have zero kurtosis.

![](_page_145_Picture_1.jpeg)

## <span id="page-146-0"></span>Models and Realizations of Random Variables

Contributed by J. Russell Carpenter

A continuous random variable is a function that maps the outcomes of random events to the real line. Realizations of random variables are thus real numbers. A vector of n random variables maps outcomes of random events to R n . For our purposes, random variables will always be associated with a probability density function that indicates the likelihood that a realization occurs within a particular interval of the real line, or within a particular subspace of R n for the vector case. It is common to assume that this density is the normal or Gaussian density. For the vector case, the normal probability density function is

$$p_{\mathbf{x}}(\mathbf{x}) = \frac{1}{\sqrt{|2\pi\mathbf{P}|}} e^{-\frac{1}{2}(\mathbf{x}-\boldsymbol{\mu})^T\mathbf{P}^{-1}(\mathbf{x}-\boldsymbol{\mu})} \quad (\text{A.1})$$

where µ is a vector of mean values for each component of x, and P is a matrix that contains the variances of each component of x along its diagonal, and the covariances between each component as its off-diagonal components. The covariances indicate the degree of correlation between the random variables composing x. The matrix P is thus called the variance-covariance matrix, which we will hereafter abbreviate to just "covariance matrix," or "covariance." Since the normal density is completely characterized by its mean and covariance, we will use the following notation as a shorthand to describe drawing a realization from a normally-distributed random vector:

| $\mathbf{x} \sim N(\boldsymbol{\mu}, \mathbf{P})$ | (A.2) |
|---------------------------------------------------|-------|
|                                                   |       |

Thus, the model for realizations of a measurement noise vector is

| $\mathbf{v} \sim N(\mathbf{0}, \mathbf{R})$ | (A.3) |
|---------------------------------------------|-------|
|---------------------------------------------|-------|

For the scalar case, or for the vector case when the covariance is diagonal, we may directly generate realizations of a normally-distributed random vector from normal random number generators available in most software libraries. If P has non-zero off-diagonal elements, we must model the specified correlations when we generate realizations. If P is strictly positive definite, we can factor it as follows:

$$\mathbf{P} = \sqrt[3]{\mathbf{P}} \sqrt[3]{\mathbf{P}^T} \quad (\text{A.4})$$

where √<sup>C</sup> <sup>P</sup> is a triangular matrix known as a Cholesky factor; this can be viewed as a "matrix square root." The Cholesky factorization is available in many linear algebra libraries. We can then use √<sup>C</sup> <sup>P</sup> to generate correlated realizations of <sup>x</sup> as follows. Let <sup>z</sup> be a realization of a normallydistributed random vector of the same dimension as x, with zero mean and unit variance, that is

| $z \sim N(\mathbf{0}, \mathbf{I})$ | (A.5) |
|------------------------------------|-------|
|------------------------------------|-------|

Then, with

$$x = \sqrt{P}z \quad (\text{A.6})$$

we can generate properly correlated realizations of x. We can also use a Cholesky factorization of the measurement noise covariance R, if R is non-diagonal, to transform correlated measurements into uncorrelated auxiliary measurements for cases in which the estimator cannot handle correlated measurement data.

If P is only non-negative definite, i.e. P ≥ 0 rather than P > 0 as above, the Cholesky factorization does not exist. In this case, since P's eigenvalues are real and distinct, it has a diagonal factorization:

| $\mathbf{P} = \mathbf{VDV}^T$ | (A.7) |
|-------------------------------|-------|
|                               |       |

where V is a matrix of eigenvectors and D is a diagonal matrix of eigenvalues. Then, with z as above,

| $x = \mathbf{V}\sqrt{D}z$ | (A.8) |
|---------------------------|-------|
|---------------------------|-------|

where √ D implies taking the square roots of each diagonal element.

## <span id="page-148-0"></span>The Mathematics Behind the UDU Factorization

Contributed by Chris D'Souza

## B.1. The Partitioning into Two Subproblems

<span id="page-148-1"></span>We can find that the update equation is

$$\mathbf{U}_{k+1}\mathbf{D}_{k+1}\mathbf{U}_{k+1}^{-1} = \mathbf{\Phi}_k\mathbf{U}_k^{+1}\mathbf{D}_k^{+1}\mathbf{U}_k^{+1}\mathbf{\Phi}_k^{-1} + \mathbf{Q}_k \quad (\text{B.1})$$

$$\begin{aligned} & - {}_{k+1}^- \mathbf{U}_{k+1}^{-1} = \Phi_k \mathbf{U}_k^\top \mathbf{D}_k^\top \mathbf{U}_k^\top \Phi_k^\top + \mathbf{Q}_k \\ &= \Phi_{2k} \Phi_{1k} \mathbf{U}_k^\top \mathbf{D}_k^\top \mathbf{U}_k^{\top T} \Phi_{1k}^\top \Phi_{2k}^\top + \mathbf{Q}_{1k} + \mathbf{Q}_{2k} \\ &= \Phi_{2k} [\Phi_{1k} \mathbf{U}_k^\top \mathbf{D}_k^\top \mathbf{U}_k^{\top T} \Phi_{1k}^\top] \Phi_{2k}^\top + \mathbf{Q}_{1k} + \mathbf{Q}_{2k} \end{aligned} \quad (\text{B.2})$$

Recalling that Q1<sup>k</sup> = Φ2kΦ −1 <sup>2</sup><sup>k</sup> Q1kΦ −T 2<sup>k</sup> Φ<sup>T</sup> 2<sup>k</sup> and

$$\Phi_{2_k}^{-1} = \begin{bmatrix} \mathbf{I} & \mathbf{0} \\ \mathbf{0} & \mathbf{M}_k^{-1} \end{bmatrix} \quad (\text{B.3})$$

where M−<sup>1</sup> <sup>k</sup> = diag(1/m<sup>k</sup><sup>i</sup> ), i = 1, 2, 3, · · · , np. We note that

$$\Phi_{2k}^{-1} \mathbf{Q}_{1_k} \Phi_{2_k}^{-\tau} = \begin{bmatrix} \mathbf{I} & \mathbf{0} \\ \mathbf{0} & M_k^{-1} \end{bmatrix} \begin{bmatrix} \mathbf{Q}_{xxx_k} & \mathbf{0} \\ \mathbf{0} & \mathbf{0} \end{bmatrix} \begin{bmatrix} \mathbf{I} & \mathbf{0} \\ \mathbf{0} & M_k^{-1} \end{bmatrix} = \begin{bmatrix} \mathbf{Q}_{xx_k} & \mathbf{0} \\ \mathbf{0} & \mathbf{0} \end{bmatrix} = \mathbf{Q}_{1_k} \quad (\text{B.4})$$

## B.2. The Mathematics Behind the Second Subproblem

<span id="page-148-2"></span>Recall that we partitoned <sup>U</sup>e and <sup>D</sup>e as

$$\tilde{\mathbf{U}}_k = \begin{bmatrix} \tilde{\mathbf{U}}_{\text{aa}_k} & \tilde{\mathbf{U}}_{\text{ab}_k} & \tilde{\mathbf{U}}_{\text{ac}_k} \\ \mathbf{0} & 1 & \tilde{\mathbf{U}}_{\text{bc}_k} \\ \mathbf{0} & \mathbf{0} & \tilde{\mathbf{U}}_{\text{cc}_k} \end{bmatrix} \begin{bmatrix} n_a & & & \\ 1 & & & \\ & \text{and} & \tilde{\mathbf{D}}_k = \begin{bmatrix} \tilde{\mathbf{D}}_{\text{aa}_k} & \mathbf{0} \\ \mathbf{0} & \tilde{\mathbf{D}}_{\text{b}_k} \\ \mathbf{0} & \mathbf{0} \end{bmatrix} & \begin{bmatrix} n_a \\ 1 \\ n_c \end{bmatrix} \\ & & & \\ & & & \text{(B.5)} \end{bmatrix}$$

in order to isolate a parameter. In fact, the state we choose to isolate is one of the Gauss-Markov states (likely associated with a sensor). Let

| $\Phi_{2k} = \begin{bmatrix} \mathbf{I} & \mathbf{0} & \mathbf{0} \\ \mathbf{0} & 1 & \mathbf{0} \\ \mathbf{0} & \mathbf{0} & \mathbf{M}_{c_k} \end{bmatrix} \begin{bmatrix} \mathbf{I} & \mathbf{0} & \mathbf{0} \\ \mathbf{0} & m_{b_k} & \mathbf{0} \\ \mathbf{0} & \mathbf{0} & \mathbf{I} \end{bmatrix} = \Phi_{c_k} \Phi_{b_k} \quad (\text{B.6})$ |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

and

$$\mathbf{Q}_{2_k} = \begin{bmatrix} \mathbf{0} & \mathbf{0} & \mathbf{0} \\ \mathbf{0} & q_{b_k} & \mathbf{0} \\ \mathbf{0} & \mathbf{0} & \mathbf{0} \end{bmatrix} + \begin{bmatrix} \mathbf{0} & \mathbf{0} & \mathbf{0} \\ \mathbf{0} & \mathbf{0} & \mathbf{0} \\ \mathbf{0} & \mathbf{0} & \mathbf{Q}_{c_k} \end{bmatrix} = \mathbf{Q}_{b_k} + \mathbf{Q}_{c_k} \quad (\text{B.7})$$

As in the previous exercise, we note that Φ−<sup>1</sup> <sup>c</sup><sup>k</sup> <sup>Q</sup>bkΦ−<sup>T</sup> <sup>c</sup><sup>k</sup> = Qb<sup>k</sup> . So, now Eq. [\(8.25\)](#page-100-5) becomes

<span id="page-149-0"></span>
$$\mathbf{U}_{k+1}^{-} \mathbf{D}_{k+1}^{-} \mathbf{U}_{k+1}^{-T} = \Phi_{ck} \left[ \Phi_{b_k} \tilde{\mathbf{U}}_k \tilde{\mathbf{D}}_k \tilde{\mathbf{U}}_k^{-T} \Phi_{b_k}^{-T} + \mathbf{Q}_{b_k} \right] \Phi_{ck}^{-T} + \mathbf{Q}_{ck} \quad (\text{B.8})$$

The term in the square bracket in Eq. [\(B.8\)](#page-149-0) is

<span id="page-149-1"></span>
$$\tilde{\mathbf{U}}_{\mathbf{k}} \tilde{\mathbf{D}}_{\mathbf{k}} \tilde{\mathbf{U}}_{\mathbf{k}}^T = \mathbf{\Phi}_{\mathbf{b}_{\mathbf{k}}} \tilde{\mathbf{U}}_{\mathbf{k}} \tilde{\mathbf{D}}_{\mathbf{k}} \tilde{\mathbf{U}}_{\mathbf{k}}^T \mathbf{\Phi}_{\mathbf{b}_{\mathbf{k}}}^T + \mathbf{Q}_{\mathbf{b}_{\mathbf{k}}} \quad (\text{B.9})$$

The left side of Eq. [\(B.9\)](#page-149-1) (recalling that U˘ bb<sup>k</sup> = 1) is

<span id="page-149-2"></span>

| $\check{\mathbf{U}}_k \check{\mathbf{D}}_k \check{\mathbf{U}}_k^T =$ | $\check{\mathbf{U}}_{\mathbf{aa}_k} \check{\mathbf{D}}_{\mathbf{aa}_k} \check{\mathbf{U}}_{\mathbf{aa}_k}^T$<br>$+ \check{\mathbf{U}}_{\mathbf{ab}_k} \check{\mathbf{d}}_{b_k} \check{\mathbf{U}}_{\mathbf{ab}_k}^T$<br>$\check{\mathbf{U}}_{\mathbf{ac}_k} \check{\mathbf{D}}_{\mathbf{cc}_k} \check{\mathbf{U}}_{\mathbf{ac}_k}^T$<br><br>$\check{\mathbf{d}}_{b_k} \check{\mathbf{U}}_{\mathbf{ab}_k}^T$<br>$\check{\mathbf{U}}_{bc_k} \check{\mathbf{D}}_{\mathbf{cc}_k} \check{\mathbf{U}}_{\mathbf{ac}_k}^T$<br><br>$\check{\mathbf{U}}_{\mathbf{cc}_k} \check{\mathbf{D}}_{\mathbf{cc}_k} \check{\mathbf{U}}_{\mathbf{ac}_k}^T$ | $\check{\mathbf{U}}_{\mathbf{ac}_k} \check{\mathbf{D}}_{\mathbf{cc}_k} \check{\mathbf{U}}_{\mathbf{ac}_k}^T$<br>$+ \check{\mathbf{U}}_{\mathbf{ab}_k} \check{\mathbf{d}}_{b_k}$ | $\check{\mathbf{U}}_{\mathbf{ac}_k} \check{\mathbf{D}}_{\mathbf{cc}_k} \check{\mathbf{U}}_{\mathbf{cc}_k}^T$ | (B.10) |  |
|----------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------|--------|--|
|                                                                      | $\check{\mathbf{d}}_{b_k} + \check{\mathbf{U}}_{bc_k} \check{\mathbf{D}}_{\mathbf{cc}_k} \check{\mathbf{U}}_{bc_k}^T$                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |                                                                                                                                                                                 | $\check{\mathbf{U}}_{bc_k} \check{\mathbf{D}}_{\mathbf{cc}_k} \check{\mathbf{U}}_{\mathbf{cc}_k}^T$          |        |  |
|                                                                      |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |                                                                                                                                                                                 |                                                                                                              |        |  |
|                                                                      | $\check{\mathbf{U}}_{\mathbf{cc}_k} \check{\mathbf{D}}_{\mathbf{cc}_k} \check{\mathbf{U}}_{\mathbf{ac}_k}^T$                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | $\check{\mathbf{U}}_{\mathbf{cc}_k} \check{\mathbf{D}}_{\mathbf{cc}_k} \check{\mathbf{U}}_{bc_k}^T$                                                                             | $\check{\mathbf{U}}_{\mathbf{cc}_k} \check{\mathbf{D}}_{\mathbf{cc}_k} \check{\mathbf{U}}_{\mathbf{cc}_k}^T$ |        |  |

The right side of Eq. [\(B.9\)](#page-149-1), once again recalling that <sup>U</sup>e bb<sup>k</sup> = 1, is

$$\Phi_{b_k} \tilde{\mathbf{U}}_k \tilde{\mathbf{D}}_k \tilde{\mathbf{U}}_k^\top \Phi_{b_k}^\top + \mathbf{Q}_{b_k} = \begin{bmatrix} \tilde{\mathbf{U}}_{\mathbf{a}\mathbf{a}_k} \tilde{\mathbf{D}}_{\mathbf{a}\mathbf{a}_k} \tilde{\mathbf{U}}_{\mathbf{a}\mathbf{a}_k}^\top & m_{b_k} \tilde{\mathbf{U}}_{\mathbf{a}\mathbf{c}_k} \tilde{\mathbf{D}}_{\mathbf{c}\mathbf{c}_k} \tilde{\mathbf{U}}_{\mathbf{a}\mathbf{c}_k}^\top & \tilde{\mathbf{U}}_{\mathbf{a}\mathbf{c}_k} \tilde{\mathbf{D}}_{\mathbf{c}\mathbf{c}_k} \tilde{\mathbf{U}}_{\mathbf{c}\mathbf{c}_k}^\top \\ + \tilde{\mathbf{U}}_{\mathbf{a}b_k} \tilde{\mathbf{d}}_{b_k} \tilde{\mathbf{U}}_{\mathbf{a}b_k}^\top & + m_{b_k} \tilde{\mathbf{U}}_{\mathbf{a}b_k} \tilde{\mathbf{d}}_{b_k} & \\ \tilde{\mathbf{U}}_{\mathbf{a}\mathbf{c}_k} \tilde{\mathbf{D}}_{\mathbf{c}\mathbf{c}_k} \tilde{\mathbf{U}}_{\mathbf{a}\mathbf{c}_k}^\top & & \\ \hline m_{b_k} \tilde{\mathbf{d}}_{b_k} \tilde{\mathbf{U}}_{\mathbf{a}b_k}^\top & m_{b_k}^2 \tilde{\mathbf{U}}_{\mathbf{b}\mathbf{c}_k} \tilde{\mathbf{D}}_{\mathbf{c}\mathbf{c}_k} \tilde{\mathbf{U}}_{\mathbf{b}\mathbf{c}_k}^\top & m_{b_k} \tilde{\mathbf{U}}_{\mathbf{b}\mathbf{c}_k} \tilde{\mathbf{D}}_{\mathbf{c}\mathbf{c}_k} \tilde{\mathbf{U}}_{\mathbf{c}\mathbf{c}_k}^\top \\ + m_{b_k} \tilde{\mathbf{U}}_{\mathbf{b}\mathbf{c}_k} \tilde{\mathbf{D}}_{\mathbf{c}\mathbf{c}_k} \tilde{\mathbf{U}}_{\mathbf{a}\mathbf{c}_k}^\top & + m_{b_k}^2 \tilde{\mathbf{d}}_{b_k} + q_{b_k} & \\ \hline \tilde{\mathbf{U}}_{\mathbf{c}\mathbf{c}_k} \tilde{\mathbf{D}}_{\mathbf{c}\mathbf{c}_k} \tilde{\mathbf{U}}_{\mathbf{a}\mathbf{c}_k}^\top & m_{b_k} \tilde{\mathbf{U}}_{\mathbf{c}\mathbf{c}_k} \tilde{\mathbf{D}}_{\mathbf{c}\mathbf{c}_k} \tilde{\mathbf{U}}_{\mathbf{b}\mathbf{c}_k}^\top & \tilde{\mathbf{U}}_{\mathbf{c}\mathbf{c}_k} \tilde{\mathbf{D}}_{\mathbf{c}\mathbf{c}_k} \tilde{\mathbf{U}}_{\mathbf{c}\mathbf{c}_k}^\top \end{bmatrix} \quad (\text{B.11})$$

Equating the components in Eqs. [\(B.10\)](#page-149-2) and [\(B.11\)](#page-149-3), from the (1,3) and (3,3) element, we find

| $\tilde{\mathbf{U}}_{ac_k} = \tilde{\mathbf{U}}_{ac_k},$ | $\tilde{\mathbf{D}}_{cc_k} = \tilde{\mathbf{D}}_{cc_k},$ | $\tilde{\mathbf{U}}_{cc_k}^T = \tilde{\mathbf{U}}_{cc_k}^T$ | (B.12) |
|----------------------------------------------------------|----------------------------------------------------------|-------------------------------------------------------------|--------|
|                                                          |                                                          |                                                             |        |

From the (2,3) element we get,

<span id="page-149-4"></span><span id="page-149-3"></span>
$$\check{\mathbf{U}}_{bc_k} = m_{b_k} \check{\mathbf{U}}_{bc_k} \quad (\text{B.13})$$

From the (2,2) element and using the results of Eq. [\(B.13\)](#page-149-4), we find that

$$\tilde{d}_{b_k} = m_{b_k}^2 \tilde{d}_{b_k} + q_{b_k} \quad (\text{B.14})$$

The (2,1) element yields

$$\check{\mathbf{U}}_{\mathbf{a}\mathbf{b}_k} = m_{b_k} \frac{\tilde{d}_{b_k}}{\tilde{d}_{b_k}} \tilde{\mathbf{U}}_{\mathbf{a}\mathbf{b}_k} \quad (\text{B.15})$$

What finally remains is the (1,1) element and it is on this we focus. Using the relations in the previous equations, we find that

<span id="page-150-1"></span>
$$\check{\mathbf{U}}_{aa_k} \check{\mathbf{D}}_{aa_k} \check{\mathbf{U}}_{aa_k}^T = \tilde{\mathbf{U}}_{aa_k} \tilde{\mathbf{D}}_{aa_k} \tilde{\mathbf{U}}_{aa_k}^T + \left[ \tilde{d}_{b_k} - m_{b_k}^2 \frac{\tilde{d}_{b_k}}{\tilde{d}_{b_k}} \right] \tilde{\mathbf{U}}_{ab_k} \tilde{\mathbf{U}}_{ab_k}^T \quad (\text{B.16})$$

The term in the bracket can be simplified as

$$\begin{bmatrix} \tilde{d}_{b_k} - m_{b_k}^2 \frac{\tilde{d}_{b_k}}{\tilde{d}_{b_k}} \end{bmatrix} = \frac{m_{b_k}^2 \frac{\tilde{d}_{b_k}^2}{m_{b_k}^2 \tilde{d}_{b_k}} + q_{b_k} \frac{\tilde{d}_{b_k}}{\tilde{d}_{b_k}} - m_{b_k}^2 \frac{\tilde{d}_{b_k}^2}{m_{b_k}^2 \tilde{d}_{b_k}} = \frac{\tilde{d}_{b_k} q_{b_k}}{m_{b_k}^2 \tilde{d}_{b_k}} = \frac{\tilde{d}_{b_k} q_{b_k}}{\tilde{d}_{b_k}} \quad (\text{B.17})$$

so Eq. [\(B.16\)](#page-150-1) becomes

<span id="page-150-2"></span>
$$\tilde{\mathbf{U}}_{aa_k} \tilde{\mathbf{D}}_{aa_k} \tilde{\mathbf{U}}_{aa_k}^T = \tilde{\mathbf{U}}_{aa_k} \tilde{\mathbf{D}}_{aa_k} \tilde{\mathbf{U}}_{aa_k}^T + \left( \frac{\tilde{d}_{b_k} q_{b_k}}{\tilde{d}_{b_k}} \right) \tilde{\mathbf{U}}_{ab_k} \tilde{\mathbf{U}}_{ab_k}^T \quad (\text{B.18})$$

We note that <sup>U</sup>e ab<sup>k</sup> is a column vector so Eq. [\(B.18\)](#page-150-2), and hence is of rank 1, constitutes a 'rank one' update. Since ˘db<sup>k</sup> , de bk and qb<sup>k</sup> are all positive (assuming mb<sup>k</sup> is a positive quantity), we can use the Agee-Turner Rank One update [[1](#page-170-16)]. It should be pointed out that as the algorithm proceeds down the 'list' of parameters, the size of the states a increases by one (and consequently the size of the parameters c decreases by one. Hence U˘ aa<sup>k</sup> and D˘ aa<sup>k</sup> begin with a dimension of n<sup>x</sup> and conclude with dimension n<sup>x</sup> + n<sup>p</sup> − 1.

Therefore, this is done recursively for all the (sensor) parameters p which are of size np.

## B.3. The Agee-Turner Rank-One Update

<span id="page-150-0"></span>In trying to get an efficient algorithm for performing the time update of the covariance matrix, we were faced with Eq. [\(8.41\)](#page-101-1), which is of the form

$$\tilde{\mathbf{U}}\tilde{\mathbf{D}}\tilde{\mathbf{U}}^\top = \mathbf{UD}\mathbf{U}^\top + \mathbf{c}\mathbf{x}\mathbf{x}^\top \quad (\text{B.19})$$

This is called a 'rank one' update because we are updating the matrix factors U and D based upon products of x which is of rank 1.

In order to reduce the number of mathematical operations (adds/subtracts, multiplies and divides), for the case of parameter or ECRV/First-order Gauss Markov processes, for sensor parameters, we consider the rank-one update first introduced by Agee and Turner (of the White Sands Missile Range (WSMR)) in 1972.

Consider a covariance matrix update of the form,

| $\tilde{\mathbf{P}} = \mathbf{P} + c \mathbf{x} \mathbf{x}^T$ | (B.20) |
|---------------------------------------------------------------|--------|
|---------------------------------------------------------------|--------|

or

$$\tilde{\mathbf{U}}\tilde{\mathbf{D}}\tilde{\mathbf{U}}^\top = \mathbf{UD}\mathbf{U}^\top + \mathbf{c}\mathbf{x}\mathbf{x}^\top \quad (\text{B.21})$$

so, <sup>p</sup>eij can be expressed (and defined) as

<span id="page-150-3"></span>
$$\widetilde{p}_{ij} \triangleq \sum_{k=j}^n \widetilde{u}_{ik} \widetilde{d}_{kk} \widetilde{u}_{jk} = \sum_{k=j}^n u_{ik} d_{kk} u_{jk} + cx_i x_j \quad (\text{B.22})$$

and

$$\tilde{p}_{ii} = \sum_{k=i}^n \tilde{u}_{ik}^2 \tilde{d}_{kk} = \sum_{k=i}^n u_{ik}^2 d_{kk} + cx_i^2 \quad (\text{B.23})$$

We recall that <sup>u</sup>eii <sup>=</sup> <sup>u</sup>ii = 1 and thus, for an <sup>n</sup> <sup>×</sup> <sup>n</sup> matrix, for <sup>j</sup> <sup>=</sup> <sup>n</sup> (i.e. the last column),

| $\tilde{d}_{nn} = d_{nn} + cx_n^2$ | (B.24) |
|------------------------------------|--------|
|------------------------------------|--------|

| $\tilde{p}_{in} = \tilde{u}_{in}\tilde{d}_{in}\tilde{u}_{in}$ | $=$ | $d_{in}u_{in}u_{in} + cx_ix_n$ | (B.25) |
|---------------------------------------------------------------|-----|--------------------------------|--------|
|                                                               |     |                                |        |

so that

<span id="page-151-0"></span>
$$\tilde{w}_{in} = \frac{1}{\tilde{d}_{nn}} (d_{nn} u_{in} + cx_i x_n) \quad (\text{B.26})$$

The second-to-the-last (n − 1-th) column of U can now be can be operated on, by means of the following decomposition of Eq. [\(B.22\)](#page-150-3), as

<span id="page-151-1"></span>

| $n-1$ | $\sum \tilde{u}_{ik} \tilde{d}_{kk} \tilde{u}_{jk} + \tilde{u}_{in} \tilde{d}_{mn} \tilde{u}_{jn} = \sum_{k=j}^{n-1} u_{ik} d_{kk} u_{jk} + u_{in} d_{mn} u_{jn} + cx_i x_j$ | (B.27) |
|-------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|
|       |                                                                                                                                                                              |        |

which leads to

$$\sum_{k=j}^{n-1} \tilde{u}_{ik} \tilde{d}_{kk} \tilde{u}_{jk} = \sum_{k=j}^{n-1} u_{ik} d_{kk} u_{jk} + \Upsilon_n \quad (\text{B.28})$$

If we work on the terms outside the two summations, using Eq. [\(B.26\)](#page-151-0) for <sup>u</sup>ein and <sup>u</sup>ejn, <sup>Υ</sup><sup>n</sup> becomes

$$\begin{aligned} \Upsilon_n &= -\tilde{u}_{in}\tilde{d}_{nn}\tilde{u}_{jn} + u_{in}d_{nn}u_{jn} + cx_ix_j \\ &= -\frac{1}{\tilde{d}_{nn}} [d_{nn}u_{in} + cx_ix_n] [d_{nn}u_{jn} + cx_jx_n] \\ &\quad + \frac{d_{nn} + cx_n^2}{\tilde{d}_{nn}} (u_{in}d_{nn}u_{jn} + cx_ix_j) \\ &= \frac{1}{\tilde{d}_{nn}} [-cd_{nn}u_{jn}x_nx_i - cd_{nn}u_{in}x_nx_j + cd_{nn}x_ix_j + cd_{nn}x_n^2u_{in}u_{jn}] \\ &= \frac{cd_{nn}}{\tilde{d}_{nn}} (x_i - u_{in}x_n) (x_j - u_{jn}x_n) \end{aligned} \quad (\text{B.29})$$

Therefore, Eq. [\(B.27\)](#page-151-1) can be written as

<span id="page-151-2"></span>

| $n-1$                                                                                                                                                                           | $n-1$  |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|
| $\sum_{k=j}^{n-1} \tilde{u}_{ik} \tilde{d}_{kk} \tilde{u}_{jk} = \sum_{k=j}^{n-1} u_{ik} d_{kk} u_{jk} + \frac{c d_{nn}}{\tilde{d}_{nn}} (x_i - u_{in} x_n) (x_j - u_{jn} x_n)$ | (B.30) |

Now, if we operate a bit more on the quantity <sup>u</sup>ein, we find from Eq. [\(B.26\)](#page-151-0), that we get

$$\tilde{w}_{in} = \frac{d_{nn}}{\tilde{d}_{nn}} u_{in} + \frac{c}{\tilde{d}_{nn}} x_i x_n \quad (\text{B.31})$$

$$= \frac{\tilde{d}_{nn} - c x_n^2}{\tilde{d}_{nn}} u_{in} + \frac{c}{\tilde{d}_{nn}} x_i x_n \quad (\text{B.32})$$

$$= u_{in} + (x_i - u_{in}x_n) \frac{c x_n}{d_{nn}} \quad (\text{B.33})$$

and if we define α<sup>i</sup> and v<sup>n</sup> as

| $\alpha_i$ | $\triangleq$ | $(x_i - u_{in}x_n)$ | (B.34) |
|------------|--------------|---------------------|--------|
|            |              |                     |        |

$$v_n \triangleq \frac{\Delta}{\tilde{d}_{nn}} \quad (\text{B.35})$$

<sup>u</sup>ein can be rewritten as

$$\tilde{u}_{in} = u_{in} + \alpha_i v_n \quad (\text{B.36})$$

If we want to generalize this, we can write Eq. [\(B.30\)](#page-151-2) as

<span id="page-152-0"></span>
$$\sum_{k=j}^{n-1} \tilde{u}_{ik} \tilde{d}_{kk} \tilde{u}_{jk} = \sum_{k=j}^{n-1} u_{ik} d_{kk} u_{jk} + \mathcal{C}^n \mathcal{X}_i^n \mathcal{X}_j^n \quad (\text{B.37})$$

where

$$\mathcal{C}^n \triangleq \frac{c d_{nn}}{\tilde{d}_{nn}} \quad (\text{B.38})$$

$$\mathcal{X}_i^n \triangleq x_i - u_{in}x_n \quad (\text{B.39})$$

with

$$\begin{aligned}\tilde{u}_{in} &= u_{in} + \alpha_i^n v_n \\ \alpha_i^n &= x_i - u_{in}x_n \\ v_n &= \frac{cx_n}{\tilde{d}_{nn}} \\ \tilde{d}_{nn} &= d_{nn} + cx_n^2\end{aligned}$$

Thus, for the third-to-the-last column (j = n − 2), we expand Eq. [\(B.37\)](#page-152-0) as

$$\begin{aligned} \sum_{k=j}^{n-2} \tilde{u}_{ik} \tilde{d}_{kk} \tilde{u}_{jk} + \tilde{u}_{i,n-1} \tilde{d}_{n-1,n-1} \tilde{u}_{j,n-1} &= \sum_{k=j}^{n-2} u_{ik} d_{kk} u_{jk} \\ &\quad + u_{i,n-1} d_{n-1,n-1} u_{j,n-1} \\ &\quad + \mathcal{C}^n \mathcal{X}_i^n \mathcal{X}_j^n \end{aligned} \quad (\text{B.40})$$

which produces

$$\sum_{k=j}^{n-2} \tilde{u}_{ik} \tilde{d}_{kk} \tilde{u}_{jk} = \sum_{k=j}^{n-2} u_{ik} d_{kk} u_{jk} + \frac{C^n d_{n-1,n-1}}{\tilde{d}_{n-1,n-1}} [\mathcal{X}_i^n - u_{i,n-1} \mathcal{X}_n^n] [\mathcal{X}_j^n - u_{j,n-1} \mathcal{X}_n^n] \quad (\text{B.41})$$

so that using the same machinery as above, we get

$$\sum_{k=j}^{n-2} \tilde{u}_{ik} \tilde{d}_{kk} \tilde{u}_{jk} = \sum_{k=j}^{n-2} u_{ik} d_{kk} u_{jk} + \mathcal{C}^{n-1} \chi_i^{n-1} \chi_j^{n-1} \quad (\text{B.42})$$

$$\mathcal{C}^{n-1} = \frac{\mathcal{C}^n d_{n-1,n-1}}{\tilde{d}_{n-1,n-1}} \quad (\text{B.43})$$

$$\chi_i^{n-1} = \chi_i^{n-1} = \chi_i^n - u_{i,n-1} \chi_n^n \quad (\text{B.44})$$

$$v_{n-1} = \frac{\mathcal{C}^n \mathcal{X}_i^n}{\tilde{d}_{n-1,n-1}} \quad (\text{B.45})$$

$$\tilde{w}_{i,n-1} = u_{i,n-1} + \mathcal{X}_i^{n-1} v_{n-1} \quad (\text{B.46})$$

$$\tilde{d}_{n-1,n-1} = d_{n-1,n-1} + \mathcal{C}^n x_{n-1}^2 \quad (\text{B.47})$$

We also are reminded that <sup>u</sup>ei,i = 1.

#### B.4. Decorrelating Measurements

<span id="page-153-0"></span>We normalize the (original) measurement equation

$$\mathbf{z}_{orig} = \mathbf{H}_{orig} \mathbf{x} + \boldsymbol{\nu}_{orig} \quad (\text{B.48})$$

where the measurement noise has statistics

| $E[\nu_{orig}]$ | $=$ | 0 | (B.49) |
|-----------------|-----|---|--------|
|                 |     |   |        |

| $E[\nu_{orig}\nu_{orig}^T]$ | $=$ | $\mathbf{R}_{orig}$ | (B.50) |
|-----------------------------|-----|---------------------|--------|
|                             |     |                     |        |

where Rorig is the measurement noise.

We now change variables so that

| $\mathbf{z}$ | $\triangleq$ | $R_{orig}^{-1/2} \mathbf{z}_{orig}$ | (B.51) |
|--------------|--------------|-------------------------------------|--------|
|              |              |                                     |        |

| $\mathbf{H}$ | $\triangleq$ | $\mathbf{R}_{orig}^{-1/2} \mathbf{H}_{orig}$ | (B.52) |
|--------------|--------------|----------------------------------------------|--------|
|--------------|--------------|----------------------------------------------|--------|

$$\nu \triangleq \mathbf{R}_{orig}^{-1/2} \boldsymbol{\nu}_{orig} \quad (\text{B.53})$$

where R −1/2 orig is the inverse of the Cholesky factor of Rorig ( = R 1/2 origR T /2 orig). With this, the new normalized measurement equation is

| $\mathbf{z} = \mathbf{H}\mathbf{x} + \boldsymbol{\nu}$ | (B.54) |
|--------------------------------------------------------|--------|
|--------------------------------------------------------|--------|

where E[ν] = 0 and E[νν<sup>T</sup> ] = I. This is sometimes referred to as pre-whitening or decorrelation, because if the original measurements were correlated, the normalized measurements are now uncorrelated (via the Cholesky decomposition of Rorig).

Alternatively, we can decorrelate the measurements by using a UDU factorization on the measurement noise covariance matrix as

| $\mathbf{R}_{orig} = \mathbf{U}_R \mathbf{D}_R \mathbf{U}_R^T$ | (B.55) |
|----------------------------------------------------------------|--------|
|                                                                |        |

so that the measurement equation, the measurement partial and the measurement noise are

| $\mathbf{z}$ | $\triangleq \mathbf{U}_R^{-1}\mathbf{z}_{orig}$ | (B.56) |
|--------------|-------------------------------------------------|--------|
|--------------|-------------------------------------------------|--------|

| $\mathbf{H}$ | $\triangleq$ | $\mathbf{U}_R^{-1}\mathbf{H}_{orig}$ | (B.57) |
|--------------|--------------|--------------------------------------|--------|
| <hr/>        |              |                                      |        |

$$\boldsymbol{\nu} \triangleq \mathbf{U}_R^{-1} \boldsymbol{\nu}_{orig} \quad (\text{B.58})$$

where the new/modified measurement equation is now uncorrelated with E[ν] = 0 and E[νν<sup>T</sup> ] = DR.

## B.5. The Carlson Rank-One Update

<span id="page-153-1"></span>The Carlson rank-one update [[9](#page-170-21)], introduced in 1973, addresses the problem of updating the covariance due to a loss of precision involved in the differencing of two positive quantities which are nearly equal. In particular, the diagonal elements dii have the potential of going negative in certain cases if the Agee-Turner rank-one update is blindly used. Thankfully, we resort to the Carlson rank-one update to compute the measurement update without losing numerical precision.

We recall that α and v were defined earlier. We also define the n × 1 vector f as

$$f \triangleq \mathbf{U}^{-T}\mathbf{H}^T \quad (\text{B.59})$$

Therefore, since f is an n × 1 vector and D is a diagonal matrix, we can express α as

| $\alpha = \alpha_n = R + \sum_{i=1}^n f_i^2 d_{ii} \quad (\text{B.60})$ |  |
|-------------------------------------------------------------------------|--|
|-------------------------------------------------------------------------|--|

so that

$$\alpha_j = R + \sum_{i=1}^j f_i^2 d_{ii} = \alpha_{j-1} + f_j^2 d_{jj} \quad (\text{B.61})$$

Since v can be written as

| $\mathbf{v} = \text{Df}$ | (B.62) |
|--------------------------|--------|
|--------------------------|--------|

we can also write

$$v_j = d_{jj}f_j \quad (\text{B.63})$$

and we can write α<sup>j</sup> as

<span id="page-154-3"></span>
$$\alpha_j = \alpha_{j-1} + \frac{v_j^2}{d_{jj}} \quad (\text{B.64})$$

$$\tilde{\mathbf{U}}_k \tilde{\mathbf{D}}_k \tilde{\mathbf{U}}_k^T \triangleq \mathbf{a}^T \mathbf{D} - \frac{1}{\alpha} \mathbf{v} \mathbf{v}^T \quad (\text{B.65})$$

which can be rewritten as:

$$\tilde{\mathbf{U}}_k \tilde{\mathbf{D}}_k \tilde{\mathbf{U}}_k^T \triangleq a_r \mathbf{U} a_r \mathbf{D} a_r \mathbf{U}^T - \frac{1}{\alpha} \mathbf{v} \mathbf{v}^T \quad (\text{B.66})$$

where arU = I. Following the reasoning in the description for the Rank-One update earlier in this Appendix,

<span id="page-154-0"></span>
$$\tilde{p}_{ij} \triangleq \sum_{k=j}^n \tilde{u}_{ik} \tilde{d}_{kk} \tilde{u}_{jk} = -\frac{1}{\alpha} v_i v_j \quad (\text{B.67})$$

and

<span id="page-154-1"></span>
$$\tilde{p}_{ii} = \sum_{k=i}^n \tilde{u}_{ik}^2 \tilde{d}_{kk} = d_{ii} - \frac{1}{\alpha} v_i^2 \quad (\text{B.6})$$

For j = n, Eq. [\(B.67\)](#page-154-0) becomes

$$\tilde{u}_{in}\tilde{d}_{nn}\tilde{u}_{nn} = -\frac{1}{\alpha}v_iv_n \quad (\text{B.6})$$

and from Eq. [\(B.68\)](#page-154-1),

$$\tilde{u}_{nn}^2 \tilde{d}_{nn} = d_{nn} - \frac{1}{\alpha} v_n^2 \quad (\text{B.70})$$

Recalling that <sup>u</sup>enn = 1, we get

$$\tilde{d}_{nn} = d_{nn} - \frac{1}{\alpha} v_n^2 \quad (\text{B.71})$$

and

<span id="page-154-2"></span>
$$\tilde{u}_{in} = -\frac{1}{\alpha \tilde{d}_{nn}} v_i v_n \quad (\text{B.72})$$

So, Eq. [\(B.67\)](#page-154-0) can be written as

<span id="page-155-5"></span>
$$\sum_{k=j}^{n-1} \tilde{u}_{ik} \tilde{d}_{kk} \tilde{u}_{jk} + \tilde{u}_{in} \tilde{d}_{nn} \tilde{u}_{jn} = -\frac{1}{\alpha} v_i v_j \quad (\text{B.73})$$

Substituting for <sup>u</sup>ein and <sup>u</sup>ein from Eq. [\(B.72\)](#page-154-2), we find

<span id="page-155-0"></span>
$$\sum_{k=j}^{n-1} \tilde{u}_{ik} \tilde{d}_{kk} \tilde{u}_{jk} = -\frac{1}{\alpha} \left[ 1 + \frac{1}{\alpha \tilde{d}_{nn}} v_n^2 \right] v_i v_j \quad (\text{B.74})$$

But since

$$\left[1 + \frac{1}{\alpha \tilde{d}_{nn}} v_n^2\right] = \frac{d_{nn}}{\tilde{d}_{nn}} \quad (\text{B.75})$$

Eq. [\(B.74\)](#page-155-0) becomes

<span id="page-155-1"></span>
$$\sum_{k=j}^{n-1} \tilde{u}_{ik} \tilde{d}_{kk} \tilde{u}_{jk} = -\frac{1}{\alpha} \frac{d_{mn}}{d_{mn}} v_i v_j \quad (\text{B.76})$$

So, we can expand Eq. [\(B.76\)](#page-155-1) as

<span id="page-155-4"></span>
$$\sum_{k=j}^{n-2} \tilde{u}_{ik} \tilde{d}_{kk} \tilde{u}_{jk} + \tilde{u}_{i,n-1} \tilde{d}_{n-1,n-1} \tilde{u}_{j,n-1} = -\frac{1}{\alpha} \frac{d_{mn}}{\tilde{d}_{mn}} v_i v_j \quad (\text{B.77})$$

We need to obtain <sup>u</sup>ei,n−<sup>1</sup> and <sup>d</sup>en−1,n−1. First we work on <sup>u</sup>ei,n−1<sup>d</sup>en−1,n−<sup>1</sup> from Eq. [\(B.67\)](#page-154-0) with i = n − 1 as follows:

$$\tilde{w}_{n-1,n-1}^2 \tilde{d}_{n-1,n-1} + \tilde{w}_{n-1,n}^2 \tilde{d}_{n,n} = d_{n-1} - \frac{1}{\alpha} v_{n-1}^2 \quad (\text{B.78})$$

Recalling that <sup>u</sup>en−1,n−<sup>1</sup> = 1 and <sup>u</sup>en−1,n was obtained (with <sup>i</sup> <sup>=</sup> <sup>n</sup> <sup>−</sup> <sup>1</sup>) in Eq. [\(B.72\)](#page-154-2), we get

$$\tilde{d}_{n-1,n-1} = d_{n-1,n-1} - \frac{1}{\alpha} \left[ 1 + \frac{1}{\alpha \tilde{d}_{n,n}} v_n^2 \right] v_{n-1}^2 \quad (\text{B.79})$$

Knowing that

<span id="page-155-3"></span>
$$\left[ 1 + \frac{1}{\alpha \tilde{d}_{n,n}} v_n^2 \right] = \frac{d_{n,n}}{\tilde{d}_{n,n}} \quad (\text{B.80})$$

<sup>d</sup>en−1,n−<sup>1</sup> becomes

<span id="page-155-2"></span>
$$\tilde{d}_{n-1,n-1} = d_{n-1,n-1} - \frac{1}{\alpha} \left( \frac{d_{n,n}}{\tilde{d}_{n,n}} \right) v_{n-1}^2 \quad (\text{B.61})$$

Now we work on <sup>u</sup>ei,n−1. We recall that from Eq. [\(B.68\)](#page-154-1), with <sup>j</sup> <sup>=</sup> <sup>n</sup> <sup>−</sup> <sup>1</sup>, we find that

$$\tilde{u}_{i,n-1}\tilde{d}_{n-1,n-1}\tilde{u}_{n-1,n-1} + \tilde{u}_{i,n}\tilde{d}_{n,n}\tilde{u}_{n-1,n} = -\frac{1}{\alpha}v_iv_{n-1} \quad (\text{B.82})$$

We substitute for <sup>d</sup>en−1,n−<sup>1</sup> from Eq. [\(B.81\)](#page-155-2), for <sup>u</sup>ei,n and <sup>u</sup>en−1,n from Eq. [\(B.72\)](#page-154-2) and noting that <sup>u</sup>en−1,n−<sup>1</sup> = 1, we get

$$\tilde{u}_{i,n-1} = -\frac{1}{\alpha\tilde{d}_{n-1,n-1}} \left[ 1 + \frac{1}{\alpha\tilde{d}_{n,n}} v_n^2 \right] v_i v_{n-1} \quad (\text{B.83})$$

Using Eq. [\(B.80\)](#page-155-3), <sup>u</sup>ei,n−<sup>1</sup> becomes

$$\tilde{u}_{i,n-1} = -\frac{1}{\alpha \tilde{d}_{n-1,n-1}} \left( \frac{d_{n,n}}{\tilde{d}_{n,n}} \right) v_i v_{n-1} \quad (\text{B.84})$$

With this in mind, we are now prepared to work on Eq. [\(B.77\)](#page-155-4), and we find that

$$\begin{aligned} \sum_{k=j}^{n-2} \tilde{u}_{ik} \tilde{d}_{kk} \tilde{u}_{jk} &= - \left( \frac{d_{n,n}}{\alpha \tilde{d}_{n,n}} \right) \left[ \frac{d_{n,n}}{\alpha \tilde{d}_{n,n}} v_{n-1}^2 - 1 \right] v_i v_j \\ &= - \left( \frac{d_{n,n}}{\alpha \tilde{d}_{n,n}} \right) \left( \frac{d_{n-1,n-1}}{\tilde{d}_{n-1,n-1}} \right) v_i v_j \end{aligned} \quad (\text{B.85})$$

This has the same form as Eq. [\(B.73\)](#page-155-5), so this suggests a recursion as follows:

With C<sup>n</sup> = −1/α for j = n, · · · , 1:

<span id="page-156-0"></span>
$$\tilde{d}_{jj} = d_{jj} + \mathcal{C} v_j^2 \quad (\text{B.6})$$

| $\tilde{u}_{ij}$ | $=$ | $\mathcal{C}^j v_i v_j / \tilde{d}_{jj}$ , | $k = 1, \dots, j-1$ | (B.87) |
|------------------|-----|--------------------------------------------|---------------------|--------|
|------------------|-----|--------------------------------------------|---------------------|--------|

| $c_{jj}^{jj}$ | $=$ | $C^j d_{jj}/\tilde{d}_{jj}$ | $c_{jj}^{jj}$ | $d_{jj}^j$       | $c_{jj}^{jj}$ | $d_{jj}^j$ | $c_{jj}^{jj}$    | $d_{jj}^j$    | $c_{jj}^{jj}$ | $d_{jj}^j$       | $c_{jj}^{jj}$ | $d_{jj}^j$ | $c_{jj}^{jj}$    | $d_{jj}^j$    |            |
|---------------|-----|-----------------------------|---------------|------------------|---------------|------------|------------------|---------------|---------------|------------------|---------------|------------|------------------|---------------|------------|
| $C^{j-1}$     | $=$ | $C^j$                       | $d_{jj}^j$    | $\tilde{d}_{jj}$ | $c_{jj}^{jj}$ | $d_{jj}^j$ | $\tilde{d}_{jj}$ | $c_{jj}^{jj}$ | $d_{jj}^j$    | $\tilde{d}_{jj}$ | $c_{jj}^{jj}$ | $d_{jj}^j$ | $\tilde{d}_{jj}$ | $c_{jj}^{jj}$ | $d_{jj}^j$ |

From Eq. [\(B.86\)](#page-156-0), we get

$$\widetilde{d}_{jj} = d_{jj} + \mathcal{C}^j v_j^2$$

and from Eq. [\(B.88\)](#page-156-0), we find that

$$\mathcal{C}^{j-1} = \mathcal{C}^j \frac{d_{jj}}{\tilde{d}_{jj}} = \frac{\mathcal{C}^j d_{jj}}{d_{jj} + C^j v_j^2} = \frac{d_{jj}}{\frac{d_{jj}}{C^j} + v_j^2} \quad (\text{B.89})$$

This can be written as

$$\frac{1}{\mathcal{C}^{j-1}} = \frac{1}{\mathcal{C}^j} + \frac{v_j^2}{d_{jj}} \quad (\text{B.90})$$

or

<span id="page-156-1"></span>
$$-\frac{1}{C^j} = -\frac{1}{C^{j-1}} + \frac{v_j^2}{d_{jj}} \quad (\text{B.91})$$

Comparing Eqs. [\(B.64\)](#page-154-3) and Eq. [\(B.91\)](#page-156-1) we find that

<span id="page-156-3"></span>
$$\alpha_j = -\frac{1}{Cj} \quad (\text{B.92})$$

Using this equation, we find that

<span id="page-156-2"></span>
$$\tilde{d}_{jj} = d_{jj} \left( \frac{\alpha_{j-1}}{\alpha_j} \right) \quad (\text{B.93})$$

From Eq. [\(B.87\)](#page-156-0) and using Eqs. [\(B.93\)](#page-156-2) and [\(B.92\)](#page-156-3), we can express <sup>u</sup>eij as

$$\tilde{u}_{ij} = -\frac{v_i v_j}{d_{jj} \alpha_{j-1}} \quad (\text{B.94})$$

Recalling that v<sup>j</sup> = djjf<sup>j</sup> ,

$$\tilde{u}_{ij} = -\frac{v_i f_j}{\alpha_{j-1}} \quad (\text{B.95})$$

If we define λ<sup>j</sup> as

$$\lambda_j \triangleq -\frac{f_j}{\alpha_{j-1}} \quad (\text{B.96})$$

<sup>u</sup>eij becomes

| $\tilde{u}_{ij}$ | $=$ | $\lambda_j v_i$ | (B.97) |
|------------------|-----|-----------------|--------|
|                  |     |                 |        |

<sup>U</sup>eij has the structure

| $\tilde{\mathbf{U}}_k =$ | 1        | $\lambda_1 v_1$ | $\lambda_3 v_1$ | $\lambda_4 v_1$ | $\cdots$ | $\lambda_n v_1$ | (B.98) |
|--------------------------|----------|-----------------|-----------------|-----------------|----------|-----------------|--------|
|                          | 0        | 1               | $\lambda_3 v_2$ | $\lambda_4 v_2$ | $\cdots$ | $\lambda_n v_2$ |        |
| $\tilde{\mathbf{U}}_k =$ | 0        | 0               | 1               | $\lambda_4 v_3$ | $\cdots$ | $\lambda_n v_3$ |        |
|                          | 0        | 0               | 0               | 1               | $\cdots$ | $\lambda_n v_4$ |        |
|                          | $\vdots$ | $\vdots$        | $\vdots$        | $\vdots$        | $\vdots$ | $\vdots$        |        |
|                          | $\vdots$ | $\vdots$        | $\vdots$        | $\vdots$        | $\vdots$ | $\vdots$        |        |
|                          | 0        | 0               | 0               | 0               | $\cdots$ | 1               |        |

We can rewrite <sup>U</sup>e as

| $\tilde{\mathbf{U}}_k = \mathbf{I}_n + [ \mathbf{0}_{n \times 1} \quad \lambda_1 \mathbf{v}^{(1)} \quad \lambda_3 \mathbf{v}^{(2)} \quad \lambda_4 \mathbf{v}^{(3)} \quad \dots \quad \lambda_n \mathbf{v}^{(n-1)} ]$ | (B.99) |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|
|                                                                                                                                                                                                                       |        |

where v (j) is an n × 1 vector defined as

$$\mathbf{v}^{(j)} \triangleq \begin{bmatrix} v_1 & v_2 & v_3 & \cdots & v_j & 0 & \cdots & 0 \end{bmatrix}^T \quad (\text{B.100})$$

We recall that

$$\mathbf{UD}\mathbf{U}^T = \mathbf{U}^{-} \left[ \mathbf{D}^{-} - \frac{1}{\alpha} \mathbf{v}\mathbf{v}^T \right] \mathbf{a}^T \mathbf{U}^T$$

and

$$\tilde{\mathbf{U}}_k \tilde{\mathbf{D}}_k \tilde{\mathbf{U}}_k^\top \triangleq \mathbf{D}^- - \frac{1}{\alpha} \mathbf{v} \mathbf{v}^\top$$

and

$$\mathbf{U} = \mathbf{U}^{-\tilde{\mathbf{U}}_k}$$
 and  $\mathbf{D} = \tilde{\mathbf{D}}$ 

With this in mind, U is

| $\mathbf{U} = \mathbf{U}^- + \mathbf{U}^- \left[ \mathbf{0}_{\times 1}, \lambda_2 \mathbf{v}^{(1)}, \lambda_3 \mathbf{v}^{(3)}, \lambda_4 \mathbf{v}^{(3)}, \dots, \lambda_n \mathbf{v}^{(n-1)} \right]$ | (B.101) |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|
|                                                                                                                                                                                                          |         |

If we denote U(j) and <sup>U</sup>−<sup>j</sup> as the jth columns of U and U−, respectively, we find that

$$\mathbf{U}^{(j)} = \mathbf{U}^{-j} + \lambda_j \mathbf{K}_{j-1} \quad (\text{B.102})$$

where

| $\bar{\mathbf{K}}_j = \mathbf{U}^{-}\mathbf{v}^{(j)} = \bar{\mathbf{K}}_{j-1} + v_j\mathbf{U}^{-j}$ | with | $\bar{\mathbf{K}}_0 = \mathbf{0}_{n \times 1}$ | (B.103) |
|-----------------------------------------------------------------------------------------------------|------|------------------------------------------------|---------|
|                                                                                                     |      |                                                |         |

Finally,

$$K = \frac{1}{\alpha_n} \overline{K}_n$$

K<sup>n</sup> (B.104)

![](_page_159_Picture_1.jpeg)

## <span id="page-160-0"></span>An Analysis of Dual Inertial-Absolute and Inertial-Relative Navigation Filters

Contributed by Chris D'Souza

This appendix describes a dual inertial-absolute state and dual inertial-relative state navigation filter trade study performed for Orion. The formulation of each of these filters is detailed, the advantages and disadvantages of each are discussed, and a recommendation to use the dual-inertial formulation is made. This appendix is reproduced from CEV Flight Dynamics Technical Brief Number FltDyn–CEV–07–141, dated December 21, 2007.

## C.1. Introduction

<span id="page-160-1"></span>Orion will need an efficient and well formulated relative navigation filter. Among the many possibilities, two of the most promising will be discussed in this report. The two are the dual inertial-absolute state navigation filter and the dual inertial-relative state navigation filter. The dual inertial-absolute state filter includes the absolute inertial state of both vehicles (with respect to the center of mass of the central body). The dual inertial-relative state navigation filter has as its states the absolute inertial state of the chaser (Orion) vehicle and the relative inertial state of the target with respect to the chaser (xrel = x<sup>T</sup> − xC).

## C.2. The Filter Dynamics

<span id="page-160-2"></span>C.2.1. The Dual Inertial-Absolute Filter Dynamics In general, the inertial states of the chaser vehicle can be expressed as

<span id="page-160-4"></span>
$$\dot{\mathbf{x}}_C = \mathbf{f}_C(\mathbf{x}_C) + \mathbf{w}_C \quad (\text{C.1})$$

where f<sup>C</sup> are the chaser nonlinear dynamics and w<sup>C</sup> is the process (plant) noise (with statistics E(wC(t)) = 0 [1](#page-160-3) and E(wC(t)wC(τ )) = QCδ(t − τ )). Similarly, the inertial states of the target vehicle evolve according to

<span id="page-160-5"></span>
$$\dot{\mathbf{x}}_T = \mathbf{f}_T(\mathbf{x}_T) + \mathbf{w}_T \quad (\text{C.2})$$

where f<sup>T</sup> are the target nonlinear dynamics and w<sup>T</sup> is the process (plant) noise (with statistics E(w<sup>T</sup> (t)) = 0 and E(w<sup>T</sup> (t)w<sup>T</sup> (τ )) = Q<sup>T</sup> δ(t−τ )). The nominal state dynamics can be expressed as

$$\dot{\mathbf{x}}_{C_{nom}} = \mathbf{f}_C(\mathbf{x}_{C_{nom}}) \quad (\text{C.3})$$

$$\dot{\mathbf{x}}_{Tnom} = \mathbf{f}_T(\mathbf{x}_{Tnom}) \quad (\text{C.4})$$

$$E(X) = \int_{-\infty}^{\infty} x \, p(x) \, dx$$

<span id="page-160-3"></span><sup>1</sup>The expectation operator E(·) for continuous random variables is defined as follows

Defining

$$\delta x_C \triangleq x_C - x_{C_{nom}} \quad (\text{C.5})$$

$$\delta \mathbf{x}_T \triangleq \mathbf{x}_T - \mathbf{x}_{T_{nom}} \quad (\text{C.6})$$

and taking derivatives and expanding to first-order, we get

$$\delta \dot{\mathbf{x}} = A_C(\mathbf{x}_{nom}) \delta \mathbf{x} + \mathbf{w}_C \quad (C.7)$$

$$\delta \dot{\mathbf{x}} = A_T(\mathbf{x}_{T_{nom}}) \delta \mathbf{x}_T + \mathbf{w}_T \quad (\text{C.8})$$

where

$$A_C(\mathbf{x}_{C_{nom}}) \triangleq \left( \frac{\partial \mathbf{f}_C}{\partial \mathbf{x}_C} \right)_{\mathbf{x}_C = \mathbf{x}_{C_{nom}}} \quad \text{and} \quad A_T(\mathbf{x}_{T_{nom}}) \triangleq \left( \frac{\partial \mathbf{f}_T}{\partial \mathbf{x}_T} \right)_{\mathbf{x}_T = \mathbf{x}_{T_{nom}}} \quad (\text{C.9})$$

Equivalently, we can express the filter errors as

$$\delta \hat{\mathbf{x}}_C \triangleq \hat{\mathbf{x}}_C - \mathbf{x}_C \quad (\text{C.10})$$

$$\delta \hat{\mathbf{x}}_T \triangleq \hat{\mathbf{x}}_T - \mathbf{x}_T \quad (\text{C.11})$$

where, with a bit of abuse of notation[<sup>2</sup>](#page-161-0)

$$\hat{\mathbf{x}}_{\mathcal{C}} \triangleq E(\mathbf{x}_{\mathcal{C}}) \quad \text{and} \quad \hat{\mathbf{x}}_{\mathcal{T}} \triangleq E(\mathbf{x}_{\mathcal{T}}) \quad (\text{C.12})$$

so that the filter error dynamics evolve as

$$\delta\hat{\mathbf{x}} = A_C(\mathbf{x}_C) \delta\hat{\mathbf{x}} + \mathbf{w}_C \quad (\text{C.13})$$

$$\delta \dot{\mathbf{x}} = A_T(\mathbf{x}_T) \delta \hat{\mathbf{x}} + \mathbf{w}_T \quad (\text{C.14})$$

We can, therefore, write the inertial-absolute[<sup>3</sup>](#page-161-1) filter error dynamics (dropping the functional dependence for compactness) as

$$\begin{bmatrix} \hat{\mathbf{x}}_C \\ \hat{\mathbf{x}}_T \end{bmatrix} = \begin{bmatrix} A_C & \mathbf{0} \\ \mathbf{0} & A_T \end{bmatrix} \begin{bmatrix} \hat{\mathbf{x}}_C \\ \hat{\mathbf{x}}_T \end{bmatrix} + \begin{bmatrix} \mathbf{I} & \mathbf{0} \\ \mathbf{0} & \mathbf{I} \end{bmatrix} \begin{bmatrix} \mathbf{w}_C \\ \mathbf{w}_T \end{bmatrix} \quad (\text{C.15})$$

Defining

$$P_{IA} \triangleq E \left\{ \begin{bmatrix} \delta \hat{\mathbf{x}}_C \\ \delta \hat{\mathbf{x}}_T \end{bmatrix} \begin{bmatrix} \delta \hat{\mathbf{x}}_C^T & \delta \hat{\mathbf{x}}_T^T \end{bmatrix} \right\} = \begin{bmatrix} E[\delta \hat{\mathbf{x}}_C \delta \hat{\mathbf{x}}_C^T] & E[\delta \hat{\mathbf{x}}_C \delta \hat{\mathbf{x}}_T^T] \\ E[\delta \hat{\mathbf{x}}_T \delta \hat{\mathbf{x}}_C^T] & E[\delta \hat{\mathbf{x}}_T \delta \hat{\mathbf{x}}_T^T] \end{bmatrix} = \begin{bmatrix} P_{C,C} & P_{C,T} \\ P_{T,C} & P_{T,T} \end{bmatrix} \quad (\text{C.16})$$

where the subscript IA denotes that this is the covariance associated with the inertial-absolute filter. The differential equation for the covariance (assuming that the plant/process noise for the two vehicles are independent and are independent of the states of the two vehicles) is

$$\dot{P}_{IA} = A_{IA}P_{IA} + P_{IA}A_{IA}^T + G_{IA}Q_{IA}G_{IA}^T \quad (\text{C.17})$$

where

<span id="page-161-2"></span>

| $A_{IA} = \begin{bmatrix} A_{CI} & \mathbf{0} \\ \mathbf{0} & A_{TI} \end{bmatrix}$ , | $G_{IA} = \begin{bmatrix} \mathbf{1} & \mathbf{0} \\ \mathbf{0} & \mathbf{1} \end{bmatrix}$ , | $Q_{IA} = \begin{bmatrix} Q_{CI} & \mathbf{0} \\ \mathbf{0} & Q_{TI} \end{bmatrix}$ | (C.18) |
|---------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------|--------|
|---------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------|--------|

$$\hat{\mathbf{x}}_{C_K} = E(\mathbf{x}_C | \mathbf{Z}_1, \dots, \mathbf{Z}_K) \quad \text{and} \quad \hat{\mathbf{x}}_{T_K} = E(\mathbf{x}_T | \mathbf{Z}_1, \dots, \mathbf{Z}_K)$$

<span id="page-161-0"></span><sup>2</sup>To be precise, xˆ<sup>C</sup> should be written in terms of the conditional expectation

with measurements Z<sup>1</sup> through Zk. At the initial time xˆ<sup>C</sup><sup>0</sup> = E(x<sup>C</sup><sup>0</sup> ) and xˆ<sup>T</sup><sup>0</sup> = E(x<sup>T</sup><sup>0</sup> )

<span id="page-161-1"></span><sup>3</sup> In order to distinguish between the two filters, we call this filter the (dual) inertial-absolute filter because both the chaser and the target states are expressed in terms of absolute inertial coordinates.

with the initial condition

$$P_{IA} = \begin{bmatrix} P_{C,C_0} & \mathbf{0} \\ \mathbf{0} & P_{T,T_0} \end{bmatrix} \quad (\text{C.19})$$

where PC,C<sup>0</sup> and PT,T<sup>0</sup> are the initial covariances of the chaser and target inertial (absolute) states, respectively. Finally, the covariance of the relative state is

$$P_{rel,rel} = E \left[ (\hat{\mathbf{x}}\hat{\mathbf{x}}_C - \hat{\mathbf{x}}\hat{\mathbf{x}}_T) (\hat{\mathbf{x}}\hat{\mathbf{x}}_C - \hat{\mathbf{x}}\hat{\mathbf{x}}_T)^T \right] \quad (\text{C.20})$$

$$= P_{C,C} + P_{T,T} - P_{T,C} - P_{C,T} = P_{C,C} + P_{T,T} - P_{T,C} - P_{T,C}^T \quad (\text{C.21})$$

C.2.2. The Dual Inertial-Relative Filter Dynamics Consistent with the earlier definitions, we define the inertial relative state as

$$\mathbf{x}_{rel} \triangleq \mathbf{x}_T - \mathbf{x}_C \quad (\text{C.22})$$

Taking derivatives of this equation and substituting from Eqs. [\(C.1\)](#page-160-4) and [\(C.2\)](#page-160-5) yields

$$\dot{\mathbf{x}}_{rel} = \mathbf{f}_T(\mathbf{x}_T) - \mathbf{f}_C(\mathbf{x}_C) + \mathbf{w}_T - \mathbf{w}_C \quad (\text{C.23})$$

Expanding this equation to first-order yields

$$\delta \mathbf{x}_{rel} = A_T(\mathbf{x}_T) \delta \hat{\mathbf{x}}_T - A_C(\mathbf{x}_C) \delta \hat{\mathbf{x}}_C + \mathbf{w}_T - \mathbf{w}_C \quad (C.24)$$

| $=$ | $A_T(\mathbf{x}_T) (\delta \hat{\mathbf{x}}_{rel} + \delta \hat{\mathbf{x}}_C) - A_C(\mathbf{x}_C) \delta \hat{\mathbf{x}}_C + \mathbf{w}_T - \mathbf{w}_C$ | (C.25) |
|-----|-------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|
|-----|-------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|

$$= (A_T - A_C) \hat{\mathbf{d}}\hat{\mathbf{x}}_C + A_T \hat{\mathbf{d}}\hat{\mathbf{x}}_{rel} + (\mathbf{w}_T - \mathbf{w}_C) \quad (\text{C.26})$$

Therefore we write the inertial-relative[<sup>4</sup>](#page-162-0) filter error dynamics (once again dropping the functional dependence for compactness) as

$$\begin{bmatrix} \delta \hat{\mathbf{x}}_C \\ \delta \hat{\mathbf{x}}_{rel} \end{bmatrix} = \begin{bmatrix} A_C & \mathbf{0} \\ A_T - A_C & A_T \end{bmatrix} \begin{bmatrix} \delta \hat{\mathbf{x}}_C \\ \delta \hat{\mathbf{x}}_T \end{bmatrix} + \begin{bmatrix} \mathbf{I} & \mathbf{0} \\ -\mathbf{I} & \mathbf{I} \end{bmatrix} \begin{bmatrix} \mathbf{w}_C \\ \mathbf{w}_T \end{bmatrix} \quad (\text{C.27})$$

Defining, as before,

$$P_{IR} \triangleq E \left\{ \left[ \begin{matrix} \delta \hat{\mathbf{x}}_C \\ \delta \hat{\mathbf{x}}_{rel} \end{matrix} \right] \left[ \begin{matrix} \delta \hat{\mathbf{x}}_C^T \\ \delta \hat{\mathbf{x}}_{rel}^T \end{matrix} \right] \right\} = \left[ \begin{matrix} E[\delta \hat{\mathbf{x}}_C \delta \hat{\mathbf{x}}_C^T] & E[\delta \hat{\mathbf{x}}_C \delta \hat{\mathbf{x}}_{rel}^T] \\ E[\delta \hat{\mathbf{x}}_{rel} \delta \hat{\mathbf{x}}_C^T] & E[\delta \hat{\mathbf{x}}_{rel} \delta \hat{\mathbf{x}}_{rel}^T] \end{matrix} \right] \quad (\text{C.28})$$

$$= \begin{bmatrix} P_{C,C} & P_{C,rel} \\ P_{rel,C} & P_{rel,rel} \end{bmatrix} \quad (\text{C.29})$$

where the subscript IR denotes that this is the covariance associated with the inertial-relative filter. The differential equation for the covariance is

<span id="page-162-2"></span>
$$\dot{P}_{IR} = A_{IR}P_{IR} + P_{IR}A_{IR}^T + G_{IR}Q_{IR}G_{IR}^T \quad (\text{C.30})$$

where

<span id="page-162-3"></span>

| $A_{IR} = \begin{bmatrix} A_C & \mathbf{0} \\ A_T - A_C & A_T \end{bmatrix}$ , | $G_{IR} = \begin{bmatrix} \mathbf{I} & \mathbf{0} \\ -\mathbf{I} & \mathbf{I} \end{bmatrix}$ , | $Q_{IR} = \begin{bmatrix} Q_C & \mathbf{0} \\ \mathbf{0} & Q_T \end{bmatrix}$ | (C31) |
|--------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------|-------|
|--------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------|-------|

where the initial covariance of the inertial-relative state is found to be[<sup>5</sup>](#page-162-1)

$$P_{IR_0} = \begin{bmatrix} P_{C,C_0} & P_{C,rel_0} \\ P_{rel,C_0} & P_{rel,rel_0} \end{bmatrix} = \begin{bmatrix} P_{C,C_0} & -P_{C,C_0} \\ -P_{C,C_0} & P_{C,C_0} + P_{T,T_0} \end{bmatrix} \quad (\text{C.32})$$

<span id="page-162-0"></span><sup>4</sup>We refer to this filter as the inertial-relative filter to distinguish it from the prior inertial-absolute filter. In this formulation, the filter states consist of the inertial absolute chaser state and the inertial relative target state.

<span id="page-162-1"></span><sup>5</sup>We assume that at the initial time, the chaser and target initial error covariance matrices are uncorrelated.

in order to be consistent with the inertial-absolute formulation. We can also express Eqs. [\(C.30\)](#page-162-2) and [\(C.31\)](#page-162-3) as

$$\dot{P}_{IR} = A_{IR}P_{IR} + P_{IR}A_{IR}^T + Q_{IR}^T \quad (\text{C.33})$$

where

$$Q'_{IR} = \begin{bmatrix} Q_C & -Q_C \\ -Q_C & Q_{rel} \end{bmatrix} \quad (\text{C.34})$$

where Qrel = Q<sup>T</sup> + QC. This may simplify tuning. While the covariance of the relative state is easily determined since it is the lower right partition of the covariance matrix (Prel,rel), the covariance of the target vehicle (inertial) state is found (after a bit of manipulation) to be

$$P_{t,T} = P_{rel,rel} + P_{C,C} + P_{rel,C} + P_{C,rel} = P_{rel,rel} + P_{C,C} + P_{rel,C} + P_{rel,C}^T \quad (\text{C35})$$

#### C.3. Incorporation of Measurements

<span id="page-163-0"></span>Whereas the previous section analyzed the filter error dynamics/propagation as it applies to the inertial-absolute and inertial-relative filter formulation, this section will analyze the difference in measurement processing between the two filters. Obviously, those measurements that are tied only to the chaser absolute inertial state have the same instantiation in both formulations. This section will only address those measurement types which have different formulations in the two filters. In particular, the measurement and the measurement partials will be discussed.

#### C.3.1. The Dual Inertial-Absolute Measurement Formulations

C.3.1.1. The Target Inertial State Ground Update There will be instances during which the onboard filter will need to process ground updates of the target vehicle. For the inertial-absolute formulation, the measurement takes the following expression

| $\mathbf{z}_{TGU}^I = \mathbf{x}_T + \boldsymbol{\nu}_{TGU}$ | $\mathbf{x}_T$ | $\boldsymbol{\nu}_{TGU} \sim N(\mathbf{0}, R_{TGU})$ | (C.36) |
|--------------------------------------------------------------|----------------|------------------------------------------------------|--------|
|--------------------------------------------------------------|----------------|------------------------------------------------------|--------|

Since the target state is a member of this filter's state-space, the measurement partials matrix associated with this measurement for the inertial-absolute formulation is

<span id="page-163-1"></span>
$$H_{T_{GU}}^{IA} = \begin{bmatrix} \mathbf{0} & \mathbf{1} \end{bmatrix} \quad (C.37)$$

C.3.1.2. Range Measurements For the case of range measurements (either from the RF link or from the Lidar), the measurement equation can be written simply as

$$\mathbf{z}_{range}^{IA} = \sqrt{(\mathbf{r}_T - \mathbf{r}_C) \cdot (\mathbf{r}_T - \mathbf{r}_C)} + b_{range} + \nu_{range} \quad (\text{C.38})$$

with the range (measurement) noise statistics νrange ∼ N(0, Rrange). Since the target state is a member of this filter's state-space, the measurement partials associated with this measurement for the inertial-absolute measurement are

$$\frac{\partial \mathbf{z}_{range}^{IA}}{\partial \mathbf{r}_C} = -\mathbf{u}_{rel}^T \quad (\text{C.39})$$

$$\frac{\partial \mathbf{z}_{range}^{IA}}{\partial \mathbf{v}_C} = \mathbf{0}_{1 \times 3} \quad (\text{C.40})$$

$$\frac{\partial \mathbf{z}_{range}^{IA}}{\partial \mathbf{r}_T} = \mathbf{u}_{rel}^T \quad (\text{C.41})$$

| $\partial_T \mathbf{z}_{range}^{IA} = \mathbf{0}_{1 \times 3}$ | (C.42) |
|----------------------------------------------------------------|--------|
|----------------------------------------------------------------|--------|

where

$$\mathbf{u}_{rel} = \frac{(\mathbf{r}_T - \mathbf{r}_C)}{|\mathbf{r}_T - \mathbf{r}_C|} \quad (\text{C.43})$$

<span id="page-164-2"></span>C.3.1.3. Bearing Measurements Bearing measurements, which can be obtained from either the star-tracker or the lidar, are

<span id="page-164-0"></span>
$$\mathbf{z}_{bearing}^{IA} = \begin{bmatrix} \alpha \\ \delta \end{bmatrix} + \begin{bmatrix} b_\alpha \\ b_\delta \end{bmatrix} + \begin{bmatrix} \nu_\alpha \\ \nu_\delta \end{bmatrix} = \begin{bmatrix} \alpha \\ \delta \end{bmatrix} + \mathbf{b}_{bearing} + \boldsymbol{\nu}_{bearing} \quad (\text{C.44})$$

where the angles α and δ, the azimuth and elevation angles in the sensor frame with biases b<sup>α</sup> and bδ, and with noise characteristics

<span id="page-164-1"></span>
$$E(\boldsymbol{\nu}_{bearing}) = \mathbf{0}_{2 \times 1} \quad \text{and} \quad E(\boldsymbol{\nu}_{bearing}\boldsymbol{\nu}_{bearing}^T) = \begin{bmatrix} R_{\alpha} & 0 \\ 0 & R_{\delta} \end{bmatrix} \quad (\text{C.45})$$

We can express α and δ in terms of the line-of-sight vector which is defined as

$$\begin{bmatrix} \cos \alpha & \cos \delta \\ \sin \alpha & \cos \delta \\ \sin \delta & 1 \end{bmatrix} \triangleq \frac{1}{r} T_{SB}(q_{SB}) T_{BI}(q_{BI}) (\mathbf{r}_T - \mathbf{r}_C) \quad (\text{C.46})$$

where TSB is the transformation matrix from the body (IMU) frame to the sensor frame (with qSB being the quaternion associated with the transformation from body frame to sensor frame) and TBI is the transformation matrix from the inertial frame to the body (IMU) frame (with qBI being the quaternion associated with the transformation from the inertial frame to the body frame).

With this in hand, the measurement partials can be obtained (after a bit of manipulation [1]) to be

$$\frac{\partial \alpha}{\partial r_C} = -\frac{\mathbf{u}_\alpha^T}{r} T_{SB}(q_{SB}) T_{BI}(q_{BI}) \quad (\text{C.47})$$

$$\frac{\partial \alpha}{\partial \mathbf{v}_C} = \mathbf{0}_{1 \times 3} \quad (\text{C.48})$$

$$\frac{\partial \alpha}{\partial \mathbf{r}_T} = \frac{\mathbf{u}_\alpha^T}{r} T_{SB}(q_{SB}) T_{BI}(q_{BI}) \quad (\text{C.49})$$

$$\frac{\partial \alpha}{\partial \mathbf{v}_T} = \mathbf{0}_{1 \times 3} \quad (\text{C.50})$$

and

$$\frac{\partial \delta}{\partial \mathbf{r}_C} = -\frac{\mathbf{u}_\delta^T}{r} T_{SB}(q_{SB}) T_{BI}(q_{BI}) \quad (\text{C.51})$$

$$\frac{\partial \delta}{\partial \mathbf{v}_C} = \mathbf{0}_{1\times 3} \quad (\text{C.52})$$

$$\frac{\partial \bar{r}}{\partial \mathbf{r}_T} = \frac{\mathbf{u}_\delta^T}{r} T_{SB}(q_{SB}) T_{BI}(q_{BI}) \quad (\text{C.53})$$

$$\frac{\partial \delta}{\partial \mathbf{v}_T} = \mathbf{O}_{1\times 3} \quad (\text{C.54})$$

where

$$\mathbf{u}_\alpha = \frac{1}{\cos \delta} \begin{bmatrix} -\sin \alpha \\ \cos \alpha \\ 0 \end{bmatrix} \quad (\text{C.55})$$

$$\mathbf{u}_\delta = \begin{bmatrix} -\cos \alpha \sin \delta \\ -\cos \alpha \cos \delta \\ \cos \delta \end{bmatrix} \quad (\text{C.56})$$

## C.3.2. The Dual Inertial-Relative Measurement Formulations

C.3.2.1. The Target Inertial State Ground Update For the inertial-relative formulation, the measurement takes the following expression

$$\mathbf{z}_{TGU}^{IR} = \mathbf{x}_{rel} + \mathbf{x}_C + \boldsymbol{\nu}_{TGU} \quad \text{and} \quad \boldsymbol{\nu}_{TGU} \sim N(\mathbf{0}, R_{TGU}) \quad (\text{C.57})$$

Since the target state is not a member of this filter's state-space, the measurement partials matrix associated with this measurement for the inertial-relative formulation is

<span id="page-165-1"></span>
$$H_{TGU}^{IR} = \begin{bmatrix} \mathbf{I} & \mathbf{I} \end{bmatrix} \quad (\text{C.58})$$

C.3.2.2. Range Measurements For the case of range measurements with the inertial-relative filter, the measurement equation can be written simply as

$$\mathbf{z}_{range}^{IA} = \sqrt{\mathbf{r}_{rel}^T \mathbf{r}_{rel} + b_{range} + \nu_{range}} \quad (\text{C.59})$$

with, as before, the range (measurement) noise statistics νrange ∼ N(0, Rrange). Since the relative state is a member of this filter's state-space, the measurement partials associated with this measurement for the inertial-relative measurement are

$$\frac{\partial \mathbf{z}_{range}^{IA}}{\partial \mathbf{r}_C} = \mathbf{0}_{1 \times 3} \quad (\text{C.60})$$

$$\frac{\partial \mathbf{z}_{range}^{IA}}{\partial \mathbf{v}_C} = \mathbf{0}_{1 \times 3} \quad (\text{C.61})$$

$$\frac{\partial \mathbf{z}_{range}^{IA}}{\partial \mathbf{r}_{rel}} = \frac{\mathbf{r}_{rel}^T}{|\mathbf{r}_{rel}|} \quad (\text{C.62})$$

$$\frac{\partial \mathbf{z}_{range}^{IA}}{\partial \mathbf{v}_{rel}} = \mathbf{0}_{1 \times 3} \quad (\text{C.63})$$

C.3.2.3. Bearing Measurements Bearing measurements, as in the previous formulation (in Eqs. [\(C.44\)](#page-164-0) and [\(C.45\)](#page-164-1)), can be expressed in terms of the line-of-sight vector and the relative position vector which can be expressed as follows

<span id="page-165-0"></span>
$$\begin{bmatrix} \cos \alpha & \cos \delta \\ \sin \alpha & \cos \delta \\ \sin \delta & 1 \end{bmatrix} = \frac{1}{r} T_{SB}(q_{SB}) T_{BI}(q_{BI}) \mathbf{r}_{rel} \quad (\text{C.64})$$

the quantities in Eq. [\(C.64\)](#page-165-0) are defined in Section [C.3.1.3.](#page-164-2) The measurement partials are expressed as

$$\frac{\partial \alpha}{\partial \mu_{\text{per}}} = 0_{1 \times 3} \quad (\text{C.6})$$

| $\frac{\partial \mathbf{r}_C}{\partial \mathbf{a}} = \mathbf{0}_{1 \times 3}$ | $(C.6)$ |
|-------------------------------------------------------------------------------|---------|
|                                                                               |         |

$$\frac{\partial \alpha}{\partial \mathbf{r}_{rel}} = \frac{\mathbf{u}_\alpha^T}{r} T_{SB}(q_{SB}) T_{BI}(q_{BI}) \quad (\text{C.67})$$

$$\frac{\partial \alpha}{\partial \mathbf{v}_{rel}} = \mathbf{0}_{1 \times 3} \quad (\text{C.6})$$

and

$$\frac{\partial \delta}{\partial \mathbf{r}_C} = \mathbf{O}_{1\times 3} \quad (\text{C.69})$$

$$\frac{\partial \delta}{\partial \mathbf{v}_C} = \mathbf{0}_{1 \times 3} \quad (\text{C.70})$$

$$\frac{\partial \delta}{\partial r_{rel}} = \frac{\mathbf{u}_\delta^T}{r} T_{SB}(q_{SB}) T_{BI}(q_{BI}) \quad (\text{C.71})$$

$$\frac{\partial \delta}{\partial \mathbf{v}_{rel}} = \mathbf{0}_{1 \times 3} \quad (\text{C.72})$$

where

$$\mathbf{u}_\alpha = \frac{1}{\cos \delta} \begin{bmatrix} -\sin \alpha \\ \cos \alpha \\ 0 \end{bmatrix} \quad (\text{C.73})$$

$$\mathbf{u}_\delta = \begin{bmatrix} -\cos \alpha \sin \delta \\ -\sin \alpha \sin \delta \\ \cos \delta \end{bmatrix} \quad (\text{C.74})$$

## C.4. Analysis of the Merits of the Inertial-Absolute and Inertial-Relative Filters

<span id="page-166-0"></span>The Flight Day 1 rendezvous trajectory and models as described in [2] were used to analyze the two filter formulations. Both formulations had the same driving dynamics and measurement models – only the covariance propagation and covariance updates were different. With this in mind, the comparison of the two filter formulation as it related to covariance operations were analyzed.

C.4.1. Covariance Propagation First it must be pointed out that the propagation of the filter dynamics are identical between both filter parameterizations. That is to say, in each filter, the inertial absolute states of both the chaser vehicle and the target vehicle will be propagated. The difference arises in the propagation of the covariance matrices associated with each of the filter paramerizations. In the IA filter, the covariances (and cross-covarinces) of the chaser inertial states and the target inertial states are computed. It should be noted that the dynamics of the two vehicles' states are inherently un-correlated (see AIA in Eq. [\(C.18\)](#page-161-2)). In contrast, for the IR filter the covariances (and cross-covariances) the chaser inertial states and the inertial relative states (of the target with respect to the chaser) are computed. It should be noted that the dynamics in this filter's states are inherently correlated (see AIR in Eq. [\(C.31\)](#page-162-3)). Hence, there are inherently more non-zero computations (both additions and multiplications) involved[<sup>6</sup>](#page-166-1) . Hence, there is more room for round-off errors in the covariance propagation in the IR filter. In order to see this, Table 1 contains an analysis of the propagation error as a function of the propagation interval. This propagation is carried out without process noise on either the chaser or target states. In addition,

<span id="page-166-1"></span><sup>6</sup> First, notice that in the IR filter, the term A<sup>T</sup> − A<sup>C</sup> will inherently cause a loss of precision. Second, assuming only the gravity gradient term in A, which is symmetric, A<sup>T</sup> − A<sup>C</sup> involves 6 additions/subtractions. The term (A<sup>T</sup> − A<sup>C</sup> )PCC in Eqs. [\(C.30\)](#page-162-2) and [\(C.31\)](#page-162-3) involve 18 multiplications and 12 additions/subtractions. The term (A<sup>T</sup> − A<sup>C</sup> )PC,rel (or Prel,C (A<sup>T</sup> − A<sup>C</sup> ) T ) involve 27 multiplications and 18 additions/subtractions. The terms (A<sup>T</sup> −A<sup>C</sup> )PCC +A<sup>T</sup> Prel,C and (A<sup>T</sup> −A<sup>C</sup> )PC,rel +A<sup>T</sup> Prel,rel each involve 9 additions/subtractions. These total 45 multiplications and 54 additions/subtractions. This is doubled because of the symmetric nature of the covariance matrix. Therefore, there are 90 additional multiplications and 108 additional additions/subtractions per function evaluation in the IR filter formulation over the IA filter formulation. For a fourth-order Runge-Kutta integration method, the IR filter formulation results in an additional 360 multiplications and 432 additions/subtractions per integration step. Each of these operations results in a numerical loss of precision in finite-state machines.

the chaser and the target states are uncorrelated at the initial time. Hence, since there are no measurements which could correlate the two vehicles' states, the correlation coefficients should remain zero (i.e. PC,T = 06×6) throughout the interval. This was verified to be the case. Because of the reduced number of computations inherent in the IA filter formulation, it was assumed that the IA filter propagation was the 'truth' and the IR filter was compared to it.

| ∆ t ( sec | )   P rel,rel | 2   P T,T   2 | δP rel,rel   2 /   P rel,rel | 2   δP T,T   2 /   P T,T   2 |
|-----------|---------------|---------------|------------------------------|------------------------------|
| 100       | 1.010E7       | 4.150E3       | 1.529E-16                    | 4.867E-13                    |
| 1000      | 6.997E7       | 4.519E3       | 5.729E-9                     | 8.869E-6                     |
| 10000     | 1.239E9       | 7.943E4       | 1.926E-5                     | 0.349                        |

Table 1. Numerical Precision Comparison of the IA and IR filter formulations for propagation without process noise

| ∆ t ( sec | )   P rel,rel | 2   P T,T   2 | δP rel,rel   2 /   P rel,rel | 2   δP T,T   2 /   P T,T   2 |
|-----------|---------------|---------------|------------------------------|------------------------------|
| 100       | 1.010E7       | 4.150E3       | 1.236E-13                    | 1.551E-7                     |
| 1000      | 6.997E7       | 4.519E3       | 2.172E-8                     | 2.320E-4                     |
| 10000     | 1.239E9       | 7.943E4       | 1.905E-5                     | 0.392                        |

Table 2. Numerical Precision Comparison of the IA and IR filter formulations for propagation with process noise

It is clear that the additional non-zero multiplications and additions for the IR filter formulation compared to the IA formulation result in a build-up of round-off error. This has the effect of reducing the propagation accuracy of the IR filter vis-a-vis the ` IA filter. The additional operations, in concert with the accompanying loss of precision, make a strong case for the use of the IA filter formulation.

C.4.2. Measurement Update It should be apparent from comparing Eqs. [\(C.37\)](#page-163-1) and [\(C.58\)](#page-165-1) that for the case of the target ground-update, there are 18 more multiplications (because of the identity matrix) for the IR formulation than the IA formulation for each target ground-update.

For all other relative measurements, there are more operations for the IA filter formulation than for the IR formulation. In fact, for the range measurements, there are more 54 multiplications and 54 more additions for the IA formulation than the IR formulation for each range measurement update.

For bearing measurements, there are more 108 multiplications and 108 more additions for the IA formulation than the IR formulation for each bearing measurement update.

So, for relative sensor measurements, clearly there are more multiplications and more additions for the IA filter formulation than for the IR formulation.

## C.5. Conclusions

<span id="page-167-0"></span>While the inertial-absolute and inertial-relative filter formulations are mathematically equivalent, the implementation on finite-state machines influences the choice.

With regard to propagation of the covariance matrices, there are more computations for the IR filter than the (mathematically equivalent) IA filter. These additional computations, in concert with the types of operations, result in a (significant) loss of precision with regard to the propagation of the covariance matrices.

With regard to the measurement updates to the covariance matrices, for the case of relative navigation measurements, there are fewer non-zero operations for the IR filter than for the IA filter. This is one of the strengths of this filter (IR) formulation, and if the computation and precision with regard to the propagation of the covariance matrices were the same, the IR filter would be advantageous in terms of computations and precision.

![](_page_169_Picture_1.jpeg)

## Bibliography

<span id="page-170-21"></span><span id="page-170-20"></span><span id="page-170-19"></span><span id="page-170-18"></span><span id="page-170-17"></span><span id="page-170-16"></span><span id="page-170-15"></span><span id="page-170-14"></span><span id="page-170-13"></span><span id="page-170-12"></span><span id="page-170-11"></span><span id="page-170-10"></span><span id="page-170-9"></span><span id="page-170-8"></span><span id="page-170-7"></span><span id="page-170-6"></span><span id="page-170-5"></span><span id="page-170-4"></span><span id="page-170-3"></span><span id="page-170-2"></span><span id="page-170-1"></span><span id="page-170-0"></span>[1] W. S. Agee and R. H. Turner. Triangular decomposition of a positive definite matrix plus a symmetric dyad with application to kalman filtering. White Sands Missile Range Tech. Rep. No. 38, 1972. [2] Shyam Bhaskaran, Shailen Desai, Philip Dumont, Brian Kennedy, George Null, William Owen Jr, Joseph E. Riedel, Stephen P. Synnott, and Robert A. Werner. Orbit determination performance evaluation of the deep space 1 autonomous navigation system. Proceedings of the AIAA/AAS Astrodynamics Specialist Conference, Feb. 1998. [3] Shyam Bhaskaran, Joseph E. Riedel, and Stephen P. Synnott. Autonomous target tracking of small bodies during flybys. Advances in the Astronautical Sciences: Spaceflight Mechanics 2004, 2005. [4] Shyam Bhaskaran, Joseph E. Riedel, Stephen P. Synnott, and Tseng chan Wang. The deep space 1 autonomous navigation system - a post-flight analysis. Proceedings of the AIAA/AAS Astrodynamics Specialist Conference, August 2000. [5] G. J. Bierman. Factorization Methods for Discrete Sequential Estimation. Academic Press, Dover Publications, New York, 1977, 2006. [6] R. A. Broucke and P. J. Cefola. On the equinoctial orbit elements. Celestial mechanics, 5(3):303–310, 1972. [7] Robert G. Brown and Patrick Y.C. Hwang. Introduction to Random Signals and Applied Kalman Filtering. John Wiley and Sons, Inc., New York, NY, 3rd edition, 1997. [8] A. E. Bryson and M. Frazier. Smoothing for linear and nonlinear dynamic systems. Technical Report TDR-63-119, Aeronautical Systems Division, Wright-Patterson Air Force Base, Ohio, Sept. 1962. [9] N.A. Carlson. Fast triangular factorization of the square root filter. AIAA Journal, 11(9):1259–1265, September 1973. [10] J. R. Carpenter and K. T. Alfriend. Navigation accuracy guidelines for orbital formation flying. Journal of the Astronautical Sciences, 53(2):207–219, 2006. Also appears as AIAA Paper 2003–5443. [11] J. Russell Carpenter and Kevin Berry. Artificial damping for stable long-term orbital covariance propagation. In Astrodynamics 2007, volume 129 of Advances in the Astronautical Sciences, pages 1697–1707. Univelt, 2008. [12] J. Russell Carpenter, T. James Blucker, John L. Goodman, James S. McCabe, and Thomas D. Bruchmiller. William lear's pioneering contributions to spacecraft navigation filtering. In Guidance, Navigation, and Control 2020, volume 172 of Advances in the Astronautical Sciences, pages 453–480. Univelt, 2020. [13] J. Russell Carpenter and Emil R. Schiesser. Semimajor axis knowledge and gps orbit determination. NAVIGATION: Journal of The Institute of Navigation, 48(1):57–68, Spring 2001. Also appears as AAS Paper 99–190. [14] Russell Carpenter and Taesul Lee. A stable clock error model using coupled first- and second-order gauss-markov processes. In AAS/AIAA 18th Spaceflight Mechanics Meeting, volume 130, pages 151–162. Univelt, 2008. [15] Paul Cefola. Equinoctial orbit elements - application to artificial satellite orbits. In Astrodynamics Conference. AIAA, Palo Alto, CA, 11-12 September 1972. [16] C. W. Chen and B. D. Pollard. Radar terminal descent sensor performance during mars science laboratory landing. Journal of Spacecraft and Rockets, 51:1208–1216, July-Aug. 2014. [17] W. H. Clohessy and R. S. Wiltshire. Terminal guidance for satellite rendezvous. Journal of the Aerospace Sciences, 27(5):653–658, 674, 1960. [18] D. Cruickshank. Genetic Model Compensation: Theory and Applications. PhD thesis, University of Colorado Boulder, 1998. [19] W. F. Denham and S. Pines. Sequential estimation when measurement function nonlinearity is comparable to measurement error. AIAA Journal, 4(6):1071–1076, June 1966. [20] Cornelius J. Dennehy and J. Russell Carpenter. A summary of the rendezvous, proximity operations, docking, and undocking (rpodu) lessons learned from the defense advanced research project agency (darpa) orbital express (oe) demonstration system mission. NASA Technical Memorandum 2011-217088, NASA Engineering and Safety Center, 2011. [21] J. L. Farrell. Attitude determination by Kalman filtering. Automatica, 6:419–430, 1970.

<span id="page-171-27"></span><span id="page-171-26"></span><span id="page-171-25"></span><span id="page-171-24"></span><span id="page-171-23"></span><span id="page-171-22"></span><span id="page-171-21"></span><span id="page-171-20"></span><span id="page-171-19"></span><span id="page-171-18"></span><span id="page-171-17"></span><span id="page-171-16"></span><span id="page-171-15"></span><span id="page-171-14"></span><span id="page-171-13"></span><span id="page-171-12"></span><span id="page-171-11"></span><span id="page-171-10"></span><span id="page-171-9"></span><span id="page-171-8"></span><span id="page-171-7"></span><span id="page-171-6"></span><span id="page-171-5"></span><span id="page-171-4"></span><span id="page-171-3"></span><span id="page-171-2"></span><span id="page-171-1"></span><span id="page-171-0"></span>[22] James L. Farrell. Attitude determination by Kalman filtering. Contractor Report NASA-CR-598, NASA Goddard Space Flight Center, Washington, DC, Sept. 1964. [23] P. Ferguson and J. How. Decentralized estimation algorithms for formation flying spacecraft. In AIAA Guidance, Navigation and Control Conference, 2003. [24] Donald C. Fraser. A New Technique for the Optimal Smoothing of Data. Sc.D. thesis, Massachusetts Institute of Technology, Cambridge, Massachusetts, 1967. [25] Donald C. Fraser and James E. Potter. The optimum smoother as a combination of two opimum linear filters. IEEE Transactions on Automatic Control, AC-14(4):387–390, Aug. 1969. [26] Eliezer Gai, Kevin Daly, James Harrison, and Linda Lemos. Star-sensor-based attiude/attitude rate estimator. Journal of Guidance, Control, and Dynamics, 8(5):560–565, Sept.-Oct. 1985. [27] Arthur Gelb, editor. Applied Optimal Estimation. The MIT Press, Cambridge, MA, 1974. [28] David K. Geller. Orbital rendezvous: When is autonomy required? Journal of Guidance, Control and Dynamics, 30(4):974–981, July–August 2007. [29] Herbert Goldstein. Classical Mechanics. Addison-Wesley Publishing Company, Reading, MA, 2nd edition, 1980. [30] Gene Howard Golub and Charles F. Van Loan. Matrix Computations. JHU Press, 3rd edition, 1996. [31] C. Gramling, J. Lorah, E. Santoro, K. Work, and R. Chambers. Preliminary operational results of the TDRSS onboard navigation system (TONS) for the Terra mission. In 15th International Symposium on Spaceflight Dynamics, Biarritz, FR, 26-30 June 2000. [32] M. Grigoriu. Response of dynamic systems to poisson white noise. Journal of Sound and Vibration, 195(3):375–389, 1996. [33] C. F. Hanak. Reducing the effects of measurement ordering on the gkf algorithm via a hybrid linear/extended kalman filter. Technical Report FltDyn-CEV-06-0107, NASA Johnson Space Center, August 2006. [34] G. W. Hill. Researches in the lunar theory. American Journal of Mathematics, 1(1):5–26, 129–147, 245–260, 1878. [35] Jonathan P. How, Louis S. Breger, Megan Mitchell, Kyle T. Alfriend, and Russell Carpenter. Differential semimajor axis estimation performance using carrier-phase differential global positioning system measurements. Journal of Guidance, Control, and Dynamics, 30(2):301–313, Mar-Apr 2007. [36] Peter C. Hughes. Spacecraft Attitude Dynamics. Wiley, New York, NY, 1986. [37] M. Idan. Estimation of Rodrigues parameters from vector observations. IEEE Transactions on Aerospace and Electronic Systems, 32(2):578–586, April 1996. [38] Andrew H. Jazwinski. Stochastic Processes and Filtering Theory. Academic Press, Inc., and Dover Publications, Inc., New York, NY, and Mineola, NY, 1970 and 2007. [39] S. C. Jenkins and D. K. Geller. State estimation and targeting for autonomous rendezvous and proximity operations. In Proceedings of the AAS/AIAA Astrodynamics Specialists Conference. Mackinac Island, MI, August 19–23 2007. [40] S. J. Julier and J. K. Uhlmann. A new extension of the kalman filter to nonlinear systems. In Int. Symp. Aerospace/Defense Sensing, Simul. and Controls, Orlando, FL, 1997. [41] Simon Julier and Jeffrey Uhlmann. Authors' reply. IEEE Transactions on Automatic Control, 47(8):1408–1409, August 2002. [42] Simon Julier, Jeffrey Uhlmann, and Hugh F. Durrant-Whyte. A new method for the nonlinear transformation of means and covariances in filters and estimators. IEEE Transactions on Automatic Control, 45(3):477–482, March 2000. [43] John L. Junkins and J. D. Turner. Optimal Spacecraft Rotational Maneuvers. Elsevier, New York, NY, 1986. [44] R. E. Kalman. A new approach to linear filtering and prediction problems. Transactions of the ASME – Journal of Basic Engineering, 82:35–45, 1960. [45] Christopher D. Karlgaard and Hanspeter Schaub. Nonsingular attitude filtering using modified Rodrigues parameters. The Journal of the Astronautical Sciences, 57(4):777–791, Oct.-Dec. 2010. [46] B. A. Kriegsman and Y. C. Tau. Shuttle navigation system for entry and landing mission phases. Journal of Spacecraft, 12(4):213–219, April 1975. [47] Dan Kubitschek, Nick Mastrodemos, Robert A. Werner, Brian Kennedy, Stephen P. Synnott, George Null, Shyam Bhaskaran, Joseph E. Riedel, and Andrew Vaughan. Deep impact autonomous navigation: The trials of targeting the unknown. AAS Guidance and Control Conference, Feb. 2006. [48] W. M. Lear. Multi-phase navigation program for the space shuttle orbiter. Internal Note No. 73-FM-132, NASA Johnson Space Center, Houston, TX, 1973. [49] William M. Lear. Onboard navigation of the space shuttle. In 11th International Symposium on Space Technology and Science, pages 737–742, Tokyo, Japan, June 30 – July 4 1975.

<span id="page-172-24"></span><span id="page-172-23"></span><span id="page-172-22"></span><span id="page-172-21"></span><span id="page-172-20"></span><span id="page-172-19"></span><span id="page-172-18"></span><span id="page-172-17"></span><span id="page-172-16"></span><span id="page-172-15"></span><span id="page-172-14"></span><span id="page-172-13"></span><span id="page-172-12"></span><span id="page-172-11"></span><span id="page-172-10"></span><span id="page-172-9"></span><span id="page-172-8"></span><span id="page-172-7"></span><span id="page-172-6"></span><span id="page-172-5"></span><span id="page-172-4"></span><span id="page-172-3"></span><span id="page-172-2"></span><span id="page-172-1"></span><span id="page-172-0"></span>[50] William M. Lear. Kalman Filtering Techniques. Technical Report JSC-20688, NASA Johnson Space Center, Houston, TX, 1985. [51] Deok-Jin Lee and Kyle T. Alfriend. Additive divided difference filtering for attitude estimation using modified rodrigues parameters. In John L. Crassidis et al., editors, Proceedings of the F. Landis Markley Astronautics Symposium, volume 132 (CD–ROM Supplement) of Advances in the Astronautical Sciences. American Astronautical Society, Univelt, 2008. [52] Tine Lefebvre, Herman Bruyninckx, and Joris De Schutter. Comment on 'a new method for the nonlinear transformation of means and covariances in filters and estimators'. IEEE Transactions on Automatic Control, 47(8):1406– 1408, August 2002. [53] Eugene J. Lefferts, F. Landis Markley, and Malcolm D. Shuster. Kalman filtering for spacecraft attitude estimation. Journal of Guidance, Control, and Dynamics, 5(5):417–429, Sept.-Oct. 1982. doi:10.2514/3.56190. [54] M. Mandic. Distributed estimation architectures and algorithms for formation flying spacecraft. Master's thesis, Massachusetts Institute of Technology, 2006. [55] S. R. Marandi and V. J. Modi. A preferred coordinate system and the associated orientation representation in attitude dynamics. Acta Astronautica, 15(11):833–843, Nov. 1987. [56] F. Landis Markley. Unit quaternion from rotation matrix. Journal of Guidance, Control, and Dynamics, 31(2):440– 442, March-April 2008. [57] F. Landis Markley. Lessons learned. The Journal of the Astronautical Sciences, 57(1 & 2):3–29, Jan.-June 2009. [58] F. Landis Markley and J. Rusell Carpenter. Generalized linear covariance analysis. The Journal of the Astronautical Sciences, 57(1 & 2):233–260, Jan.-June 2009. [59] F. Landis Markley and John L. Crassidis. Fundamentals of Spacecraft Attitude Determination and Control, pages 46, 257–260, 263–269. Springer, New York, NY, 2014. doi:10.1007/978-1-4939-0802-8. [60] Peter S. Maybeck. Stochastic Models, Estimation and Control, Vol. 1. Academic Press, New York, NY, 1979. [61] Peter S. Maybeck. Stochastic Models, Estimation and Control, Vol. 2. Academic Press, New York, NY, 1979. [62] Oliver Montenbruck and Eberhard Gill. Satellite Orbits: Models, Methods, and Applications. Springer, Berlin Heidelberg New York, 2000. [63] Eugene S. Muller and Peter M. Kachmar. A new approach to on-board orbit navigation. Navigation: Journal of the Institute of Navigation, 18(4):369–385, Winter 1971–72. [64] Magnus Nørgaard, Niels K. Poulsen, and Ole Ravn. Advances in derivative-free state estimation for nonlinear systems. Technical Report IMM–REP–1998–15, Technical University of Denmark, 2800 Lyngby, Denmark, April 7, 2000. [65] Magnus Nørgaard, Niels K. Poulsen, and Ole Ravn. New developments in state estimation for nonlinear estimation problems. Automatica, 36(11):1627–1638, November 2000. [66] Young W. Park, Jack P. Brazzel, J. Russell Carpenter, Heather D. Hinkel, and James H. Newman. Flight test results from real-time relative gps experiment on sts-69. In SPACEFLIGHT MECHANICS 1996, volume 93 of Advances in the Astronautical Sciences, pages 1277–1296, San Diego, CA, 1996. Univelt. [67] L. Perea, J. How, L. Breger, and P. Elosegui. Nonlinearity in sensor fusion: Divergence issues in ekf, modified truncated sof, and ukf. In AIAA Guidance, Navigation and Control Conference and Exhibit, Hilton Head, SC, August 20–23, 2007. [68] Mark E. Pittelkau. Kalman filtering for spacecraft system alignment calibration. Journal of Guidance, Control and Dynamics, 24(6), Nov.-Dec. 2001. [69] H. Plinval. Analysis of relative navigation architectures for formation flying spacecraft. Master's thesis, Massachusetts Institute of Technology, 2006. [70] H. E. Rauch, F. Tung, and C. T. Striebel. Maximum likelihood estimates of linear dynamic systems. AIAA Journal, 3(8):1445–1450, Aug. 1965. [71] Reid G. Reynolds. Asymptotically optimal attitude filtering with guaranteed covergence. Journal of Guidance, Control, and Dynamics, 31(1):114–122, Jan.-Feb. 2008. [72] Olinde Rodrigues. Des lois geom´ etriques qui r ´ egissent les d ´ eplacements d'un syst ´ eme solide dans l'espace, et de ` la variation des coordonnees provenant de ces d ´ eplacements consid ´ er´ es ind ´ ependamment des causes qui peuvent ´ les produire. Journal de Mathematiques Pures et Appliqu ´ ees ´ , 5:380–440, 1840. [73] Hanspeter Schaub and John L. Junkins. Analytical Mechanics of Aerospace Systems. American Institute of Aeronautics and Astronautics, Inc., New York, NY, 2nd edition, 2009. [74] Emil Schiesser, Jack P. Brazzel, J. Russell Carpenter, and Heather D. Hinkel. Results of sts-80 relative gps navigation flight experiment. In SPACEFLIGHT MECHANICS 1998, volume 99 of Advances in the Astronautical Sciences, pages 1317–1334, San Diego, CA, 1998. Univelt.

- <span id="page-173-5"></span><span id="page-173-0"></span>[75] S. F. Schmidt. Application of state-space methods to navigation problems. In C. T. Leondes, editor, Advances in Control Systems: Theory and Applications, volume 3, pages 293–340. Academic Press, New York, 1966. [76] Stanley. F. Schmidt. The kalman filter - its recognition and development for aerospace applications. Journal of Guidance, Control, and Dynamics, 4(1):4–7, 2016/01/09 1981. [77] John H. Seago, Jacob Griesback, James W. Woodburn, and David A. Vallado. Sequential orbit-estimation with sparse tracking. In Space Flight Mechanics 2011, volume 140 of Advances in the Astronautical Sciences, pages 281–
- <span id="page-173-17"></span><span id="page-173-16"></span><span id="page-173-15"></span><span id="page-173-14"></span><span id="page-173-13"></span><span id="page-173-12"></span><span id="page-173-11"></span><span id="page-173-10"></span><span id="page-173-9"></span><span id="page-173-8"></span><span id="page-173-7"></span><span id="page-173-6"></span><span id="page-173-4"></span><span id="page-173-3"></span><span id="page-173-2"></span><span id="page-173-1"></span>299. Univelt, 2011. [78] Malcolm D. Shuster. A survey of attitude representations. The Journal of the Astronautical Sciences, 41(4):439–517, Oct.-Dec. 1993. [79] Nathan Stacey and Simone D'Amico. Analytical process noise covariance modeling for absolute and relative orbits. Acta Astronautica, 194:34–47, 2022. [80] John Stuelpnagel. On the parametrization of the three-dimensional rotation group. SIAM Review, 6(4):422–430, Oct. 1964. [81] Byron D. Tapley, Bob E. Schutz, and George R. Born. Statistical Orbit Determination. Academic Press, 2004. [82] C.L Thornton and G.J. Bierman. Gram-schmidt algorithms for covariance propagation. IEEE Conference on Decision and Control, pages 489–498, 1975. [83] C.L Thornton and G.J. Bierman. Numerical comparison of discrete kalman filtering algorithms: An orbit determination case study. JPL Technical Memorandum, 33-771, June 1976. [84] David A. Vallado. Fundamentals of Astrodynamics and Applications. Microcosm Press, Hawthorne, CA and Springer, New York, NY, 2nd edition, 2004. [85] Oldrich Vasicek. An equilibrium characterization of the term structure. J. Financial Economics, 5(2):177–188, November 1977. [86] M. C. Wang and G. E. Uhlenbeck. On the theory of brownian motion ii. In N. Wax, editor, Selected Papers on Noise and Stochastic Processes, pages 113–132. Dover, 1954. [87] James R. Wertz, editor. Spacecraft Attitude Determination and Control. Kluwer Academic Publishers, The Netherlands, 1978. [88] Thomas F. Wiener. Theoretical Analysis of Gimballess Inertial Reference Equipment Using Delta-Modulated Instruments. Ph.D. dissertation, Massachusetts Institute of Technology, Cambridge, MA, 1962. [89] J. R. Wright. Sequential orbit determination with auto-correlated gravity modeling errors. Journal of Guidance and Control, 4(3):304–309, May–June 1980. [90] James R. Wright. Optimal orbit determination. In Kyle T. Alfriend et al., editor, Space Flight Mechanics 2002, volume 112 of Advances in the Astronautical Sciences, pages 1123–134. Univelt, 2002. [91] Renato Zanetti, Kyle J. DeMars, and Robert H. Bishop. Underweighting nonlinear measurements. Journal of Guidance, Control and Dynamics, 33(5):1670–1675, September–October 2010. [92] Renato Zanetti and Christopher D'Souza. Recursive implementations of the consider filter. Proceedings of the 2012 AAS Jer-Nan Juang Symposium, 2012.

## Index of Best Practices

<span id="page-174-0"></span>Attitude Error Representations Kalman Filtering, [94](#page-117-3) Attitude Estimation Kalman Filter Formulation Measurement Update, [95](#page-118-1) Propagation, [97](#page-120-3) Reset, [95](#page-118-1) avoidance of discontinuous time scales leap seconds, [60](#page-83-0) avoidance of filter cascades, [38](#page-61-3) backup ephemeris, [104](#page-127-1) batch filter moving data arc, [12](#page-35-0) batch filter, applicability to onboard, [9](#page-32-2) coordinate system origin changes, [60](#page-83-0) covariance measurement update, [31](#page-54-1) covariance propagation, [21](#page-44-3) decorrelating vector measurements, [37](#page-60-2) double precision, [59](#page-82-0) dual-inertial state representation, [61](#page-84-4) editing, [99](#page-122-3) first-order Gauss-Markov bias model exponentially-correlated bias model, [24,](#page-47-0) [51](#page-74-2) flight-path angle standard deviation at entry interface as a metric, [20](#page-43-1) ground support system, [109](#page-132-1) inertial component bias modeling, [64](#page-87-0) inertial data incorporation, [38](#page-61-3) measurement latency, [35](#page-58-2) measurement underweighting (Lear method), [45](#page-68-2) measurement update invariant to processing order, [37](#page-60-2) multiplicative EKF (MEKF), [94](#page-117-3) process noise covariance approximation, [22](#page-45-4)

## Quaternion

Kinematics, [97](#page-120-3)

recovery

divergence , restar[t104](#page-127-1)

Rodrigues Parameters, [96](#page-119-3)

second-order Gauss-Markov bias model, [53](#page-76-1) second-order Runge-Kutta state transition matrix approximation, [22](#page-45-4) selective measurement processing, [99](#page-122-3)

semi-major axis standard deviation as a metric, [20](#page-43-1)

time representation, [59](#page-82-0)

UDU factorization, [69](#page-92-0)
