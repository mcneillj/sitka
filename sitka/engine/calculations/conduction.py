import numpy as np
import pandas as pd

class FiniteDifferenceMethod1D:
    def __init__(self, time, surface, zone_air):
        # Explicit solver

        # General properties
        self.time = time
        self.surface = surface
        self.zone_air = zone_air

        # Stored variables
        self.temperature_array = None
        self.time_array = None

        # Number of internal points
        self.Nx = len(self.surface.layers)

        # Calculate Spatial Step-Size
        self.thickness = self.surface.thickness
        self.dx = self.thickness/self.Nx
        kx = self.dx/2

        # Create grid-points on x axis
        self.x = np.linspace(0,1,self.Nx+2)
        self.x = self.x[1:-1]

        # FD matrix
        self.A = None
        self.b = None
        self.u = None

        # Initial methods
        self.update_calculated_values()

    def update_calculated_values(self):
        self.setup_finite_difference_matrix()
        self.initialize_arrays()

    def setup_finite_difference_matrix(self):
        R = np.array(self.surface.thermal_resistance_array)
        C = np.array(self.surface.thermal_capacitance_array)
        dt = self.time.time_step
        Nx = self.Nx

        A1 = dt/(R[:-1]*C)
        A2 = 1-(dt/C)*(1/R[1:]+1/R[:-1])
        A3 = dt/(R[1:]*C)

        A = np.zeros((Nx,Nx+2))
        A[:,:-2] += np.diag(A1)
        A[:,1:-1] += np.diag(A2)
        A[:,2:] += np.diag(A3)

        self.A = A

    def initialize_arrays(self):
        #self.temperature_array = np.zeros((len(self.time.time_range),len(self.x)))
        #self.time_array = np.zeros(len(self.time.time_range))

        df = pd.DataFrame()
        for x in self.x:
            df[str(x)] = np.ones(self.time.length)*self.zone_air.initial_zone_air_temperature
        #df.index = self.time.time_range
        self.temperature_array = df
        self.time_array = pd.Series(self.time.time_range)

    def run_solver(self, iteration, time_index):
        surface = self.surface
        #t = self.time.time_range[start_time_step:end_time_step]
        x = self.x

        #for sim_index, time_index in enumerate(self.time_array[start_time_step:end_time_step].index):
        #array_index = start_time_step + sim_time_step
        if time_index > 0 and iteration == 0:
            b = np.array(self.temperature_array.loc[time_index-1])
        else:
            b = np.array(self.temperature_array.loc[time_index])

        # Boundary conditions
        inside_temperature = self.zone_air.zone_air_temperature.iloc[time_index]
        outside_temperature = self.surface.weather.dry_bulb_temperature.iloc[time_index]

        # Solve timestep
        self.solve_timestep(time_index, b, outside_temperature, inside_temperature)

    def solve_timestep(self, time_index, temperature_array, outside_temperature, inside_temperature):
        # Boundary Conditions
        T = outside_temperature
        b = np.insert(temperature_array,0,T,axis=0)
        b = np.append(b, inside_temperature)

        # Solve
        u = np.dot(self.A,b)
        b = np.array(u)

        # Store values in object
        self.temperature_array.iloc[time_index] = u
