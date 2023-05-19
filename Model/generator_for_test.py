import numpy as np
import math

class TrafficGenerator:
    def __init__(self, max_steps, n_cars_generated):
        self._n_cars_generated = n_cars_generated  # how many cars per episode
        self._max_steps = max_steps

    def generate_routefile(self, seed):
        """
        Generation of the route of every car for one episode
        """
        np.random.seed(seed)  # make tests reproducible

        # the generation of cars is distributed according to a weibull distribution
        timings = np.random.weibull(2, self._n_cars_generated)
        timings = np.sort(timings)

        # reshape the distribution to fit the interval 0:max_steps
        car_gen_steps = []
        min_old = math.floor(timings[1])
        max_old = math.ceil(timings[-1])
        min_new = 0
        max_new = self._max_steps
        for value in timings:
            car_gen_steps = np.append(car_gen_steps, ((max_new - min_new) / (max_old - min_old)) * (value - max_old) + max_new)
            
        car_gen_steps = np.rint(car_gen_steps)  # round every value to int -> effective steps when a car will be generated
        in_com=  ['WTL1','NTL1','NTL2','ETL2','WTL3','STL3','NTL4','STL4','STL5','ETL5']
        out_com= ['TL1W','TL1N','TL2N','TL2E','TL3W','TL3S','TL4N','TL4S','TL5S','TL5E']
        pos_route=[]
        # produce the file for cars generation, one car per line
        with open("test_inter/episode_routes.rou.xml", "w") as routes:
            print("""<?xml version="1.0" encoding="UTF-8"?>
            <routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">
            <vType accel="1.0" decel="4.5" id="standard_car" length="5.0" minGap="2.5" maxSpeed="25" sigma="0.5" />
            """, file=routes)
            count=1
            for i in range(10):
                for k in range(10):
                    if i!=k:
                        pos_route.append("{} {}".format(in_com[i],out_com[k]))
                        count+=1

            for car_counter, step in enumerate(car_gen_steps):
                route= np.random.randint(1, 90)  
                print('<trip id="t{}" depart="{}" from="{}" to="{}"  departSpeed="10" />'.format(car_counter,step,pos_route[route][:4],pos_route[route][5:]), file=routes)
            print("</routes>", file=routes)
