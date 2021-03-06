#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  abl_plot_example.py
#  
#  Copyright 2018 Martinez <lmartin1@LMARTIN1-31527S>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import numpy as np
import matplotlib.pyplot as plt
import netCDF4 as ncdf
from scipy import interpolate

def main(args):
    '''
    Read in a netCDF file generated by Nalu and post-process.
    '''
    # Load the data
    data = ABLStatsFileClass(stats_file='abl_statistics.nc')

    '''
    Plot time-history for different heights
    '''
    # The heights to plot [m]
    heights = [70, 100, 150, 300]

    # The time vector
    time = data.time

    plt.clf()
    # Loop through all the heights
    for z in heights:

        # Velocity as function of time
        u = data.u_h(z)
        v = data.v_h(z)
        # Velocity magnitude
        u_mag = np.sqrt(u**2 + v**2)

        plt.plot(time, u_mag, label=r'$U_{\rm mag},$ $z=$'+str(z)+' [m]')

    plt.legend(loc='best')
    plt.xlabel('Time [s]')
    plt.ylabel('Velocity [m/s]')
    plt.savefig('Velocity.pdf')

    '''
    Plot time-averaged profiles for all heights
    '''
    # Velocity
    z = data.heights
    u = data.time_average(field='velocity', index=0, times=[0, 1500])
    v = data.time_average(field='velocity', index=1, times=[0, 1500])
    u_mag = np.sqrt(u**2 + v**2)

    plt.clf()
    plt.plot(u, z, '-o', label='U')
    plt.plot(v, z, '-o', label='V')
    plt.plot(u_mag, z, '-o', label='U mag')
    plt.legend(loc='best')
    plt.xlabel('Velocity [m/s]')
    plt.ylabel('z [m]')
    plt.savefig('Velocity_average.pdf')

    # Resolved Stress
    uu = data.time_average(field='resolved_stress', index=0, times=[0, 1500])
    vv = data.time_average(field='resolved_stress', index=2, times=[0, 1500])

    plt.clf()
    plt.plot(uu, z, '-o', label='U')
    plt.plot(vv, z, '-o', label='V')
    plt.legend(loc='best')
    plt.xlabel("Resolved Stress [m$^2$/s$^2$]")
    plt.ylabel('z [m]')
    plt.savefig('rs_average.pdf')

class ABLStatsFileClass():
    '''
    Interface to ABL Statistics NetCDF file
    '''

    def __init__(self, stats_file='abl_statistics.nc'):
        '''
        Args:
            stats_file (path): Absolute path to the NetCDF file
        '''
        # Read in the file using netcdf
        self.abl_stats = ncdf.Dataset(stats_file)

        print('The netcdf file contains the variables:')
        for key in self.abl_stats.variables.keys(): 
            print(key, np.shape(self.abl_stats[key]))

        # Extract the heights
        self.heights = self.abl_stats['heights']
    
        # Extract the time
        self.time = self.abl_stats.variables['time']
    
        # Velocity
        # Index - [time, height, (x, y, z)]
        velocity = self.abl_stats.variables['velocity']

        # Velocity components as a function of time for given height
        self.u_h = interpolate.interp1d(self.heights, velocity[:, :, 0], axis=1)
        self.v_h = interpolate.interp1d(self.heights, velocity[:, :, 1], axis=1)
        self.w_h = interpolate.interp1d(self.heights, velocity[:, :, 2], axis=1)

    def time_average(self, field='velocity', index=0, times=[0., 100]):
        '''
        Provide field time average
        field - the field to time-average
        index - the component index (for example: velocity has 3 components)
        times - the times to average
        '''
        
        # Filter the field based on the times
        filt = ((self.time[:] >= times[0]) & (self.time[:] <= times[1]))
        # Filtered time
        t = self.time[filt]
        # The total time
        dt = np.amax(t) - np.amin(t)

        # Filtered field
        f = self.abl_stats[field][filt,:,index]

        # Compute the time average as an integral
        integral = np.trapz(f, x=t, axis=0) / dt

        return integral

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
