# -*- coding: utf-8 -*-
'''
Name: Chillers
Description: Script to calculate chiller energy consumption
JSM
V0.1
10.16.2012

Status
v0 - Created class for simple fan

'''
import os, math, partLoadCurves
from numpy import *

class SimpleChiller:

   def __init__(self):
       #--------------------------------------------------------------         
       #Inputs
       #--------------------------------------------------------------
	
	# Function to calculate chiller power from DOE-2.2 part load methodology
	def calcChillerPower( t1,t2,clrLoad,clrCap,EIR,clrCapCoeffs,clrEIRTCoeffs,clrEIRPLCoeffs ):
		"Calculates part load chiller power from current and design flow rates"
		CAPf = calcBiQuadCurve(t1,t2,clrCapCoeffs)
		Cap_hour = clrCap*CAPf   
		dT = t2-t1
		PLR = clrLoad/Cap_hour
		EIRTf = calcBiQuadCurve(t1,t2,clrEIRTCoeffs)
		EIRPLf = calcBiQuadCurve(PLR,dT,clrEIRPLCoeffs)
		Elechour = Cap_hour*EIR*EIRTf*EIRPLf/3413 # Calculate electricity usage in kW from capacity in Btu/hr 
		return Elechour

#--------------------------------------------------------------
# End of Class    
#--------------------------------------------------------------

class ChillerElectricEIR:
	#Based on EnergyPlus Chiller:Electric:EIR which is based on DOE-2.1 compression chiller model (COMREF).
	
	def __init__(self):
		#--------------------------------------------------------------         
		#Inputs
		#--------------------------------------------------------------
		
		#Chiller capacity and EIR performance coefficients
		capTempCoeffs = 0 		#Temperature capacity coefficients
		EIRTempCoeffs = 0		#Temperature EIR coefficients
		EIRFPLRCoeffs = 0		#Part load ratio EIR coefficients
		
		#Capacity and load
		loadReq = 0				#Load required to be met by chiller
		ratedCap = 0			#Rated capacity
		ratedPower = 0			#Rated power consumption
		ratedCOP = 0			#Rated coefficient of performance
		availCap = 0			#Available capacity
		actPower = 0			#Actual power consumption
		PLR = 0					#Part load ratio
		PLRmax = 0				#maximum part load ratio
		CapFTemp = 0
		EIRFTemp = 0
		EIRFPLR = 0
		
		#Fluid properties  - THIS SHOULD BE IN ITS OWN CLASS (FLUID PROPERTIES)
		condWtrSpecHeat = 0 	#Condenser water specific heat
		chWtrDensity = 0		#Chilled water density
		chWtrSpecHeat = 0		#Chilled water specific heat
		chWtrDensity = 0		#Chilled water density
		
		#Fluid temperatures - THIS SHOULD BE IN ITS OWN CLASS (FLUID LOOP)
		condWtrEntTemp = 0		#Condenser water entering temperature
		condWtrLvgTemp = 0		#Condenser water leaving temperature
		chWtrEntTemp = 0		#Chilled water entering temperature
		chWtrLvgTemp = 0		#Chilled water leaving temperature
		
		#Mass flow rates - THIS SHOULD BE IN ITS OWN CLASS (FLUID LOOP)
		evapMassFlow = 0		#Evaporator mass flow rate
		
		
	#--------------------------------------------------------------

		
	def calcChillerCapacity(self):
		calcBiQuadCurve(condWtrTempIn,condWtrTempOut,clrEIRTCoeffs)
	#--------------------------------------------------------------

#--------------------------------------------------------------
# End of Class    
#--------------------------------------------------------------

