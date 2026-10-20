# Bacteria movement notes

References:

- [Cell motility empowers bacterial contact weapons (2024)](https://doi.org/10.1093/ismejo/wrae141)
- [Bacterial twitching motility is coordinated by a two-dimensional tug-of-war with directional memory (2014)](https://doi.org/10.1038/ncomms4759)

Assume constant speed $s$. Let $\theta$ be the direction, $\tau$ the mean time between turns, $\Delta t$ the time step, and $L$ the environment width. Use $\Delta t \ll \tau$.

Probability of turning in one step:

$$
p = 1-e^{-\Delta t/\tau}
$$

Keep the old direction with probability $1-p$. Otherwise, choose a new direction uniformly from $[0,2\pi)$.

Velocity and position, using the updated direction:

$$
v_x=s\cos\theta,\qquad v_y=s\sin\theta
$$

$$
x_{\mathrm{new}}=(x_{\mathrm{old}}+v_x\Delta t)\bmod L,\qquad
y_{\mathrm{new}}=(y_{\mathrm{old}}+v_y\Delta t)\bmod L
$$

Dead or dividing bacteria stay in place and keep their direction unchanged.

For now, we can assume that bacteria move forward for some time step and then randomly turn to another dirction. We mainly want to see how movement changes contact and survival, so constant speed is enough for the first version.
