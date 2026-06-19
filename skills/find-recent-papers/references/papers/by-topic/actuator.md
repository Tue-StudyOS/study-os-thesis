# Papers For actuator

Last updated: 2026-06-13

### Sim-to-Real Transfer for Muscle-Actuated Robots via Generalized Actuator Networks
- Year: 2026
- Authors: Jan Schneider, Mridul Mahajan, Le Chen, Simon Guist, Bernhard Scholkopf, Ingmar Posner, Dieter Buchler
- Source: ArXiv.org
- DOI: 
- OpenAlex: https://openalex.org/W7154427156
- URL: https://arxiv.org/abs/2604.09487
- Keywords: Robot; Actuator; Pipeline (software); Computer science; Torque
- Thesis angle: Use this paper as evidence for a thesis conversation; refine the angle with the supervisor.
- Abstract: Tendon drives paired with soft muscle actuation enable faster and safer robots while potentially accelerating skill acquisition. Still, these systems are rarely used in practice due to inherent nonlinearities, friction, and hysteresis, which complicate modeling and control. So far, these challenges have hindered policy transfer from simulation to real systems. To bridge this gap, we propose a sim-to-real pipeline that learns a neural network model of this complex actuation and leverages established rigid body simulation for the arm dynamics and interactions with the environment. Our method, called Generalized Actuator Network (GenAN), enables actuation model identification across a wide range of robots by learning directly from joint position trajectories rather than requiring torque sensors. Using GenAN on PAMY2, a tendon-driven robot powered by pneumatic artificial muscles, we successfully deploy dynamic but precise goal-reaching, ball-in-a-cup, and table tennis policies, trained entirely in simulation. To the best of our knowledge, this result constitutes the first successful sim-to-real transfer for a four-degrees-of-freedom muscle-actuated robot arm.
