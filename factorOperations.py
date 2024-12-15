# factorOperations.py
# -------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

from typing import List
from bayesNet import Factor
import functools
from util import raiseNotDefined

def joinFactorsByVariableWithCallTracking(callTrackingList=None):


    def joinFactorsByVariable(factors: List[Factor], joinVariable: str):
        """
        Input factors is a list of factors.
        Input joinVariable is the variable to join on.

        This function performs a check that the variable that is being joined on 
        appears as an unconditioned variable in only one of the input factors.

        Then, it calls your joinFactors on all of the factors in factors that 
        contain that variable.

        Returns a tuple of 
        (factors not joined, resulting factor from joinFactors)
        """

        if not (callTrackingList is None):
            callTrackingList.append(('join', joinVariable))

        currentFactorsToJoin =    [factor for factor in factors if joinVariable in factor.variablesSet()]
        currentFactorsNotToJoin = [factor for factor in factors if joinVariable not in factor.variablesSet()]

        # typecheck portion
        numVariableOnLeft = len([factor for factor in currentFactorsToJoin if joinVariable in factor.unconditionedVariables()])
        vars_on_left = [factor for factor in currentFactorsToJoin if joinVariable in factor.unconditionedVariables()]
        if numVariableOnLeft > 1:
            print("Factor failed joinFactorsByVariable typecheck: ", vars_on_left)
            raise ValueError("The joinBy variable can only appear in one factor as an \nunconditioned variable. \n" +  
                               "joinVariable: " + str(joinVariable) + "\n" +
                               ", ".join(map(str, [factor.unconditionedVariables() for factor in currentFactorsToJoin])))
        
        joinedFactor = joinFactors(currentFactorsToJoin)
        return currentFactorsNotToJoin, joinedFactor

    return joinFactorsByVariable

joinFactorsByVariable = joinFactorsByVariableWithCallTracking()

########### ########### ###########
########### QUESTION 2  ###########
########### ########### ###########

def joinFactors(factors):
    factors = list(factors)

    if not factors:
        return None
    if len(factors) == 1:
        return factors[0]
        
    unconditioned = set()
    conditioned = set()
    
    for factor in factors:
        unconditioned.update(factor.unconditionedVariables())
        conditioned.update(factor.conditionedVariables())
    
    conditioned = conditioned - unconditioned
    
    variableDomainsDict = factors[0].variableDomainsDict()
    

    newFactor = Factor(list(unconditioned), list(conditioned), variableDomainsDict)
    

    for assignment in newFactor.getAllPossibleAssignmentDicts():

        probability = 1.0
        for factor in factors:
            probability *= factor.getProbability(assignment)
        newFactor.setProbability(assignment, probability)
        
    return newFactor

########### ########### ###########
########### QUESTION 3  ###########
########### ########### ###########

def eliminateWithCallTracking(callTrackingList=None):

    def eliminate(factor: Factor, eliminationVariable: str):
        """
        Input factor is a single factor.
        Input eliminationVariable is the variable to eliminate from factor.
        """
        unconditioned = factor.unconditionedVariables() - {eliminationVariable}
        conditioned = factor.conditionedVariables()
        
        newFactor = Factor(list(unconditioned), list(conditioned), factor.variableDomainsDict())
        
        for newAssignment in newFactor.getAllPossibleAssignmentDicts():
            total = 0.0
            for elimValue in factor.variableDomainsDict()[eliminationVariable]:
                fullAssignment = newAssignment.copy()
                fullAssignment[eliminationVariable] = elimValue
                total += factor.getProbability(fullAssignment)
            newFactor.setProbability(newAssignment, total)
            
        return newFactor

    return eliminate

eliminate = eliminateWithCallTracking()

