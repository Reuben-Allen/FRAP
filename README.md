# Fluorescence Recovery After Photobleaching (FRAP) Demo
This simulation is useful for demonstration purposes when teaching the principles of FRAP experiments used to assess molecular diffusion rates.  
To get started, simply run
```
points = FRAP(num_particles,mu,sigma,bleach_radius,max_radius)
```
where num_particles is the number of particules to simulate, mu and sigma are the mean and standard deviation, respectively, of the gaussian distribution used to simulate brownian motion, bleach_radius is the radius of the bleached region, and max_radius is roughly the edge of the allowed space. Lastly, call
```
points.animate(iterations)
```
## Example:
```
points = FRAP(1000,0,0.1,2,5)
points.animate(200)
```
![frap](https://user-images.githubusercontent.com/47088251/202988366-0f66c49d-f140-48db-9f04-5c0b75a71a2d.gif)
