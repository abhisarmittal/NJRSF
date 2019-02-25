# python code for the alogorithm

import random
import sys
import os


plant = input("What is your plant type?: ")
location = input("Where are your plants located?")
mois = int(input("What is the soil moisture percentage?Please write the number: "))
temp = int(input("What is the temperature in degrees?: "))
fcast = input("What is the upcoming forecast- is it going to be rainy, sunny, or cloudy?: ")
if plant in ["beans","citrus", "cotton", "groundnut", "maize", "sorghum", "soybeans", "sunflower"]:
    if plant in "cotton" and mois >= 4.5 and mois <= 6.5:# Yuvanshu I checked the moisture percentages and we were way off adjusting now
        if temp > 60 and fcast in "sunny":
            print("Your " + plant + " plant located in the " + location + " needs water since it may become crinkly if there is more loss in moisture. This is because the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%")
        elif temp > 60 and fcast in "rainy":
            print("Your " + plant + " plant located in the " + location + " doesn't need water since the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.")
        elif temp > 60 and fcast in "cloudy":
            print("Your " + plant + " plant located in the " + location + " needs water since the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.")
        elif temp <= 60 and fcast in ["sunny", "rainy", "cloudy"]:
            print("Your " + plant + " plant located in the " + location + " doesn't need water since the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.")
    if plant in "cotton" and mois > 10:
        if temp > 60 and fcast in ["sunny", "rainy", "cloudy"]:
            print("Your " + plant + " plant located in the " + location + " doesn't need water since the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.")
        elif temp <= 60 and fcast in ["sunny", "rainy", "cloudy"]:
            print("Your " + plant + " plant located in the " + location + " doesn't need water since the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.")
    if plant in "cotton" and mois <4.5 :
        if temp > 60 and fcast in ["sunny", "cloudy"]:
            print("Your " + plant + " plant located in the " + location + " needs water since the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.")
        elif temp > 60 and fcast in "rainy":
            print("Your " + plant + " plant located in the " + location + " doesn't need water since the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.")
        elif temp <= 60 and fcast in ["sunny", "cloudy"]:
            print("Your " + plant + " plant located in the " + location + " needs water since the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.")
        elif temp <= 60 and fcast in "rainy":
            print("Your " + plant + " plant located in the " + location + " doesn't need water since the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.")
    elif plant in "maize" and mois >= 20 and mois <= 25:#for mature corn
        if temp > 60 and fcast in "sunny":
            print("Your " + plant + " plant located in the " + location + " needs water since the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.")
        elif temp > 60 and fcast in "rainy":
            print("Your " + plant + " plant located in the " + location + " doesn't need water since the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.")
        elif temp > 60 and fcast in "cloudy":
            print("Your " + plant + " plant located in the " + location + " doesn't need water since the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.")
        elif temp <= 60 and fcast in ["sunny", "rainy", "cloudy"]:
            print("Your " + plant + " plant located in the " + location + " doesn't need water since the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.")
    if plant in "maize" and mois >26:
        if temp > 60 and fcast in ["sunny", "rainy", "cloudy"]:
            print("Your " + plant + " plant located in the " + location + " doesn't need water since the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.")
        elif temp <= 60 and fcast in ["sunny", "rainy", "cloudy"]:
            print("Your " + plant + " plant located in the " + location + " doesn't need water since the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.")
    if plant in "maize" and mois < 20 and >=15:
        if temp > 60 and fcast in ["sunny", "cloudy"]:
            print("Your " + plant + " plant located in the " + location + " needs water since the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.")
        elif temp > 60 and fcast in "rainy":
            print("Your " + plant + " plant located in the " + location + " doesn't need water since the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.")
        elif temp <= 60 and fcast in ["sunny", "cloudy"]:
            print("Your " + plant + " plant located in the " + location + " needs water since the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.")
        elif temp <= 60 and fcast in "rainy":
            print("Your " + plant + " plant located in the " + location + " doesn't need water since the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.")
    if plant in "maize" and mois< 15:
            print ("Your " + plant + " plant located in the " + location + " needs water since the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.")
    if plant in "soybeans" and mois >= 12 and mois <= 13:
        if temp > 60 and fcast in "sunny":
            print("Your " + plant + " plant located in the " + location + " needs water since the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.")
        elif temp > 60 and fcast in "rainy":
            print("Your " + plant + " plant located in the " + location + " doesn't need water since the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.")
        elif temp > 60 and fcast in "cloudy":
            print("Your " + plant + " plant located in the " + location + " doesn't need water since the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.")
        elif temp <= 60 and fcast in ["sunny", "rainy", "cloudy"]:
            print("Your " + plant + " plant located in the " + location + " doesn't need water since the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.")
    if plant in "soybeans" and mois > 13 and <=15:
        if temp > 60 and fcast in ["sunny", "rainy", "cloudy"]:
            print("Your " + plant + " plant located in the " + location + " doesn't need water since the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.")
        elif temp <= 60 and fcast in ["sunny", "rainy", "cloudy"]:
            print("Your " + plant + " plant located in the " + location + " doesn't need water since the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.")
    if plant in "soybeans" and mois >15 :
        if temp > 60 and fcast in ["sunny", "cloudy"]:
            print("Your " + plant + " plant located in the " + location + " doesn't need water since the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.")
        elif temp > 60 and fcast in "rainy":
            print("Your " + plant + " plant located in the " + location + " doesn't need water since the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.")
        elif temp <= 60 and fcast in ["sunny", "cloudy"]:
            print("Your " + plant + " plant located in the " + location + " doesn't need water since the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.")
        elif temp <= 60 and fcast in "rainy":
            print("Your " + plant + " plant located in the " + location + " doesn't need water since the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.")
    if plant in "soybeans" and mois <=12 and >=10:
        if temp >60 and fcast in["sunny","cloudy"]:
            print ("Your " + plant + " plant located in the " + location + " needs water since the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.")
        elif temp<70 and fcast in "rainy":
            print ("Your " + plant + " plant located in the " + location + " doesn't need water since the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.") 
    if plant in "soybeans" and mois<10:
        if fcast in["sunny", "cloudy", "rainy"]:
            print ("Your " + plant + " plant located in the " + location + " needs water since the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.") 
            
    if plant in "wheat" and mois >=14 and <=24:
        if temp >=80 and fcast in ["sunny", "cloudy"]:
            print ("Your " + plant + " plant located in the " + location + " needs water periodically throughout the day if conditions remain. since the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.")
    elif temp=>80 and fcast in "rainy":
        print ("Your " + plant + " plant located in the " + location + " doesn't need water since the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.") 
    if plant in "wheat" and mois <=14 and >=10:
        if temp =>80 and fcast ["sunny", "cloudy"]:
            print ("Your " + plant + " plant located in the " + location + " needs water periodically throughout the day since the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.")
    elif temp <80 and fcast in ["rainy", "cloudy"]:
        print ("Your " + plant + " plant located in the " + location + " doesn't need water since the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.")
    elif temp <80 and >=60 and fcast in "sunny":
        print ("Your " + plant + " plant located in the " + location + " doesn't need water since the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.")
    elif temp < 60 and fcast["sunny","cloudy","rainy"]:
        print ("Your " + plant + " plant located in the " + location + " doesn't need water since the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.")
    if plant in "wheat" and mois >24:
        if temp <60 and <90 andfcast in ["rainy","cloudy", "sunny"]:
            print ("Your " + plant + " plant located in the " + location + " doesn't need water since the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.")
    elif temp >=90:
        print ("Your " + plant + " plant located in the " + location + " needs water periodically about once every two hours since the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.")
    if plant in "wheat" and mois < 14 and >=10:
        if temp >60 and fcast["sunny","cloudy"]:
            print ("Your " + plant + " plant located in the " + location + " needs water since the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.")
    elif temp >=60 and fcast "rainy":
        print ("Your " + plant + " plant located in the " + location + "  doesn't need water since the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.")
    elif temp<60 and fcast ["sunny","cloudy"]:
        print("Your " + plant + " plant located in the " + location + " needs water since the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.")
    elif temp <60 and fcast"rainy":
        print("Your " + plant + " plant located in the " + location + " doesn't need water since the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.")
    if plant in "wheat" and mois < 10:
        if fcast ["sunny","cloudy","rainy"]:
            print("Your " + plant + " plant located in the " + location + " needs water since the plant enzymes could break down. This is because, the temperature is",temp,"degrees Fahrenheit, the weather forecast is " + fcast + " and the soil moisture percentage is",mois, "%.")
            
            
            
            

            
            
            
            
            
            
            
            
            
            
