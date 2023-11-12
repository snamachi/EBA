import math
import random

#Given number of aspects and items 
#Uniformly draws an aspect landscape
def generate(a_n,i_n):
	aspectscape=[]
	
	#Each item has at least one aspect
	for k in range(i_n):
		u=random.random()
		a_r=math.floor(u*a_n)
		aspectscape.append(set([a_r]))
	
	#Each aspect appears at least once
	for k in range(a_n):
		u=random.random()
		i_r=math.floor(u*i_n)
		aspectscape[i_r].add(k)
	
	#Completes remainder of assignments 
	for k in range(i_n):
		u=random.random()
		a_s=math.floor(u*(2**(a_n)))
		while a_s>0:
			a=math.floor(math.log(a_s,2))
			aspectscape[k].add(a)
			a_s=a_s-2**a
	return aspectscape
	
#Given an aspect landscape
#Returns its aspects
def aspectlst(aspectscape):
	aspects=[]
	for item in aspectscape:
		for aspect in item:
			if aspect not in aspects:
				aspects.append(aspect)
	return aspects

#Given aspects, scale, and info cost
#Returns pdf of Boltzmann distribution 
def make_pdf(aspects,scale,cost):
	def pdf(k):
		n=2**(scale(aspects[k])/cost) 
		d=sum([2**(scale(aspect)/cost) for aspect in aspects])
		return n/d
	return pdf

#Given a pdf
#Returns a cdf
def make_cdf(pdf):
	def cdf(k):
		sum=0
		for j in range(k):
			sum+=pdf(j)
		return sum
	return cdf

#Given aspects, scale, and info cost
#Simulates Boltzmann distribution
def simulate(aspects,scale,cost):
	pdf=make_pdf(aspects,scale,cost)
	cdf=make_cdf(pdf)
	u = random.random()
	k=0
	while True:
		(l,r) = (cdf(k),cdf(k+1))
		if l<u and u<=r:
			return aspects[k]
		k+=1
	
#Given an aspect landscape, a scale,
#a cooling function, and an info cost
#Returns choice output by EBA 
def EBA(aspectscape,scale,cool,cost):
	#Returns arbitray item when all
	#alternatives are identical 
	if all(items==aspectscape[0] for items in aspectscape):
		return aspectscape[0]
			
	#Eliminates items lacking an aspect 
	#drawn from Boltzmann distribution
	else:
		newscape=[]
		aspects=aspectlst(aspectscape)
		aspect=simulate(aspects,scale,cost)
		for item in aspectscape:
			if aspect in item:
				newscape.append(item)
		return EBA(newscape,scale,cool,cool(cost))

#Example
aspectscape=generate(5,3)
print(aspectscape)
def scale(n):
	return 2^n
def cool(cost):
	return cost		
choice=EBA(aspectscape,cool,scale,32)
print(choice)
