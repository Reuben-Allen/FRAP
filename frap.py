"""
Author: Reuben Allen
Date: 3/6/2022
"""

# import python libraries
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.animation import FuncAnimation

class FRAP():
    def __init__(self,num_particles,mu,sigma,bleach_radius,max_radius):
        # initialize input values
        self.n = num_particles # number of particles to simulate
        self.norm_params = (mu,sigma) # parameters of normal distribution for displacements
        self.bleach_radius = bleach_radius # radius to use for laser bleaching
        self.max_radius = max_radius # boundary for particle motion
        self.initial_positions = np.zeros((2,self.n)) # array storing the initial coordinates of the particles
        self.bleached = np.zeros(self.n) # array for designating bleached particles

        # generate uniformly distributed points in max_radius 
        # get polar coordinates
        theta = np.random.uniform(0,2*np.pi,self.n)
        radius = np.random.uniform(0,self.max_radius**2, self.n) ** 0.5

        # designate as bleached or fluorescent
        self.bleached[radius < self.bleach_radius] = 1

        # convert to cartesian
        self.initial_positions[0,:] = radius * np.cos(theta)
        self.initial_positions[1,:] = radius * np.sin(theta)
    
    def brownian(self,iterations):
        # define coordinate array
        coordinates = np.zeros((2,self.n,iterations))
        coordinates[:,:,0] = self.initial_positions
        fluorescence = np.zeros((2,iterations))
        fluorescence[0,:] = np.array(range(iterations)) + 1

        for i in range(iterations-1):
            num_green = 0 # variable stores how many green particles within the bleached radius

            # use two independent gaussian processses to generate x and y displacements
            x = np.random.normal(self.norm_params[0],self.norm_params[1],self.n)
            y = np.random.normal(self.norm_params[0],self.norm_params[1],self.n)

            # use displacement to update particle position
            coordinates[0,:,i+1] = np.add(x,coordinates[0,:,i])
            coordinates[1,:,i+1] = np.add(y,coordinates[1,:,i])

            # find the direction of the vector to each new position
            theta_displacement = np.arctan2(coordinates[1,:,i+1],coordinates[0,:,i+1])

            # check the location of the particle in space
            for index, j in np.ndenumerate(np.hypot(coordinates[0,:,i+1],coordinates[1,:,i+1])):
                if j > self.max_radius:
                    # if the particle is outside the accepted radius make a step in the opposite direction
                    diff = self.max_radius - j
                    coordinates[0,index,i+1] = np.add(diff*np.cos(theta_displacement[index]),coordinates[0,index,i])
                    coordinates[1,index,i+1] = np.add(diff*np.sin(theta_displacement[index]),coordinates[1,index,i])

                elif j < self.bleach_radius and self.bleached[index] == 0:
                    # update green counter if a green particle is inside the inner radius
                    num_green += 1

                else:
                    continue
            
            fluorescence[1,i+1] = num_green # store fluorescent information
        return fluorescence,coordinates

    def animate(self,iterations):
        # get particle coordinates
        fluor,coordinates = self.brownian(iterations)

        # generate colormap based on bleaching
        color_list = ['lawngreen','slategray']
        cmap = ListedColormap(color_list)

        # initialize figure for plotting
        fig = plt.figure(figsize=(9,6))
        ax1 = plt.subplot(1,2,1)
        ax2 = plt.subplot(1,2,2)
        ax1.set(adjustable='box', aspect='equal')

        # setting plot limits and other aesthetics
        max_coord = np.max(coordinates)
        max_fluor = np.max(fluor[1,:])
        ax1.set_xlim(-1* max_coord, max_coord)
        ax1.set_ylim(-1* max_coord, max_coord)
        ax1.set(xticklabels=[])
        ax1.set(yticklabels=[])
        ax1.tick_params(left=False,bottom=False)
        ax2.set_xlim(0, iterations)
        ax2.set_ylim(0,max_fluor)
        ax2.set_xlabel("Time Units")
        ax2.set_ylabel("Fluorescence (Number of Particles)")
        ax2.set_title("Fluorescence in Bleached Region v.s. Time")

        # initializing a plot variables
        scat = ax1.scatter(coordinates[0,:,0],coordinates[1,:,0],c=self.bleached,cmap=cmap)
        line, = ax2.plot(fluor[0,0],fluor[1,0],color="lawngreen")
        plots = [scat,line]

        # update plot
        temp = self.initial_positions.T
        def frame(i):
            temp[:,0] = coordinates[0,:,i]
            temp[:,1] = coordinates[1,:,i]

            plots[0].set_offsets(temp)
            plots[1].set_data(fluor[0,0:i],fluor[1,0:i])
            return plots

        animation = FuncAnimation(fig, func = frame, frames = np.arange(1,iterations),interval=50)
        # line below saves the animation
        animation.save('frap.gif')
        plt.show()

if __name__ == "__main__":
    points = FRAP(1000,0,0.1,2,5)
    points.animate(200)
