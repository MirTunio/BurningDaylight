#Following book now
#1D Plasma model using particle mesh method
#
# Vlasov eqn:
# (Df/Dt) = (df/dt) + v.(df/dx)+ (F/m).(df/dv) = 0                        (2-1) 
#
# Electrostatic force for potential phi, field E and force F:
# (DEL**2)phi = -(rho)/(epsilon nought), F = qE = -q(DEL)phi              (2-2)
#
# Positive ions treated as fixed. (rho nought)
# rho(x) = q[integral: f.dv]+(rho nought)                                 (2-3)
# 
# Assumptions:
# No charge exchange (electron charge conserved)
# Electron gas is collisionless (KE >> PE)
# Disturbances from equil. are para. to electric field (electrostatic approx.)
# Velocities are much less than speed of light
# 
# What is this model good for?:
# Studying electron oscillations on:
#   - a length scale >> avg. electron spacing
#   - time scale << electron collision time
#   - time scale << ion motion
#
# Mathematically collapse to 1D by:
#   - rho, phi and E depend only on x
#   - in y and z the plasma is uniform and infinite
#
# we get:
# (df/dt)+ v(df/dx)+(F/m)(df/dv) = 0                             (2-1) -> (2-4)
# d^2p(phi)/dx^2 = -rho/(epsilon nought), E = -d(phi)/dx, F = qE (2-2) -> (2-5)
# rho(x) = q[integra;: f(x,v,t)dv]+(rho nought)
#
# Some next shit(bottom pg 25)
# 
# And now we attempt to discretize the sytem:
# 
# Superparticle Equations:
# The first step is to replace (2-4) by its characteristic equations
# divide x&v phase space into a regular array of infinitesimal  cells of ...
# volume  d(tau) = dx*dv, where d(tau) is sufficiently small for not more ...
# than one elcetron to occupy it. Then f(x,v,t) yields probability that the ...
# cell at (x,v) is occupied at time t.
# IF there is an electron in a cell (x,v) it follows that there will be ...
# one in the cell at (x',v') at time t' where (x',v') are given by:
# x' = x + [integral: vdt]{t,t'}   &  v' = v + [integral: qEdt/m]{t,t'}  (2-12)
# Generally: f(x',v',t') = f(x,v,t)                                      (2-13)
# Thus if we knew values for f for each infinitesimal cell in phase space ...
# and time t, we can map forward to any later time by integrating the EOM.
#
# Now, to map for every cell is fucking crazy
# So we consider sample of points: {xi,vi :: i = 1,Np}, where each particle ...
# represents an element i of phase space fluid corresponding to ...
# Ns = [integral: f dx dv]{over i} plasma electrons per unit area in the y-z plane.
# 
# Orbits: (dxi/dt) = vi, M*(dvi/dt) = F(xi), where: M = Ns*me.           (2-14)
# 
# IF the density of superparticles (sample points) is sufficiently great, ...
# then no explicit reference to the distribution function needs to be made ...
# n the discrete model. Approximations to the moments of f are construted ...
# directly from the coordinataes of the superparticles. For instance ...
# moments of velocity may be approximated by:
# [int: v^n f dv] ~= (Ns/(lambda))[int:dx]{x +/- lambda/2}*[int:v^n~fdv] ...
# = (Ns/Lambda)[sum:v^n_i]{i}, where ~f = [sum:delta(x-xi)delta(v-vi)]{i=1,Np}
# note: The local average is necessary if we are to represent a smooth ...
# distribution function, otherwise superparticles would behave like ...
# strongly correlated charged particles rather than as samples of a ...
# continuous smoothly varying phase fluid.
# 
# What determines the density for superparticles to be applicable? Well ... 
# the characteristic oscillations of electrostatic oscillataions is the ...
# Debye length (lambda)_D.
# We require the averaging length be less than or the same order as (lambda)_D
# The no. of particles in the avging length (lambda) ~ (lambda)_D must be ...
# large enough (say ~10) for statistical fluctuations of the moments to be ...
# small. THIS: suitable density such that no of particles in Debye length large
#
# So (2-14) with discretized time, with leapfrog scheme over level DT is:
# x_i^(n+1) - x_i^(n) = v_i^(n+1/2)*DT, 
# v_i^(n+1/2) - v_i^(n-1/2) = F(x_i^n)DT/mi
# Positions and Fields at: (0,Dt,2DT...), Velocities at: ((1/2)DT,(3/2)DT...)
# note: DT must be chosen to allow plasma oscillations freq ~ wp to be rep, ...
# ie: wp*DT << 2
#
# Field Equations:
# The region of space spanned by the simulation model is k/a the comp. box
# Boundary conditions are specified at x = 0 and x = L of the box. If the ...
# surfaces were earthed metal plates, then we would require that phi = 0 at ...
# the surfaces. Given potentials at the surfaces and the charge density ...
# distribution within the computational box, Poisson's eqn. (2-5) ...
# completely specifies the potential. 
# More appropriate BC for the present example is: phi(x) = phi(x+L)
# Yield same dispersion relation (2-7, which was next shit), as for the ...
# infinite system, except that the continuum of wavenumbers is repacled by ...
# a discrete set of k = (2Pil)/L, whose wavelengths (lambda) are such that ...
# L = l(lambda); l = integer
# (d/dx)*f(x) = [lim: (f(x+h/2)-f(x-h/2))/h]{h->0}
# Usually take limit not to 0 but to H, with a tradeoff
# for the plasma model H <= (lambda)_D 
# Thus, charge density, potential, E are represented by a set of values ...
# spaced at intervals H throughout the box. The points at which these are ...
# recorded arae known as the mesh or grid points. Mesh points lie at the ...
# center of cells of width H. If origin at point 0, the position of mesh ...
# point p is at xp - pH. An integral number of cell widths H fit into the ...
# computational box L. For periodic boundary conditions, the number of ...
# cells is equal to no. of grid points Ng. L - NgH
#
# GOLD:
# And derivatives are replaced by:
# d^2(ph)/dx^2 @xp = (phi(x[p+1])-2phi(x[p]) + phi(x[p-1]))/H^2          (2-21)
# d(phi)/dx @xp = (phi(x[p+1]) - phi(x[p-1]))/2H                         (2-22)
#
# The field eqns are:
# (phi[p+1] - 2phi[p] + phi[p-1])/H^2 = -(rho)/(epsilon nought)          (2-23)
# Ep =  (phi[p-1] - phi[p+1])/2H                                         (2-24)
# where phi[p] = phi(x[p])
#
# Now some other goodies:
#
# Charge Assignment and Force Interpolation:
# Charge density is charge per unit volume
# For charge density at mesh point p is the total charge div by cell vol.
# (rho)_p = (1/H) [sum: q*N_s]{particles i in cell p} + (rho nought)     (2-25)
# This the NGP charge assignment scheme, it is identical to the method for ...
# constructing approx moments of the dist function from the superparticle ... 
# coordinates. (see proof pg30 end)
# Another useful method is (rho)_p = (rho)[x] @ x = xp
# 
# NGP force interp scheme:
# The force on particle i at x_i is:
# F(xi) = Ns*q*E(xp), where xp-H/2 < xi <= xp+H/2
# or ito of W: F9xi) = Ns*q*[sum: W(xi-xp)*Ep]{0,Ng-1}
# where: W = 1 if |x| < H/2 or x = H/2 else = 0
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#
# Summary: (2-32:37) [bottom pg 31]
# 1. Charge Assignment:
#       (rho)^n_p = (q*Ns/H)*[sum: W(x^n_i-x_p)*Ep]{p = 0, Ng-1}
# 2. Field Equations:
#       (phi^n[p-1] - 2*phi^n[p] + phi^n[p+1] ) / H^2 = -(rho)^n_p/(eps nought)
#       E^n[p] = (phi^n[p-1] - phi^n[p+1])/ 2H
# 3. Force interp:
#       F^(n)[i] = F(x^n[i]) = Nsq*[sum: W(x^(n)[i] - x[p])]*E^(n)[p]
# 4. EOM:
#       (v ^(n+1/2)[i] - v^(n-1/2)[i]) / DT = F(x^n[i])/Ns*me
#       (x^(n+1)[i] - x^(n)[i]) /DT = v^(n+1/2)[i]
#
# With the following constraints:
# 1. H < Debye Length (lambda)_D
# 2. Wp*DT << 2
# 3. L >> (lambda)_D
# 4. Np*(lamda)_D >> L
# So that plasma waves adequately represented and model is collisionless
# 
# Good metric is total energy. If it is conserved, you are conserved..
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
