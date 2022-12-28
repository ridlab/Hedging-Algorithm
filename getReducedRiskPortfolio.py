def getReducedRiskPortfolio(aBasket, aHedgeConfig):
    
    myHedgedBasket = aBasket
    myHedgeConfig = aHedgeConfig
    
    if myHedgeConfig.closing == True:
        myHedgeConfig.maxDailyPLSwing = 0
        myHedgedBasket = getMinimumVolatilityPortfolio(aBasket, myHedgeConfig)
        
    else:
        myTolerance = myHedgeConfig.tolerance
        myGlobalTargetVolatility = (1 + myHedgeConfig.globalRiskReductionMultiplier) * myHedgeConfig.maxDailyPLSwing / np.sqrt(12 * 24)
        myIterations = 0
        
        if myHedgedBasket.volatility > myGlobalTargetVolatility * (1 + myTolerance) and sum(myHedgedBasket.smallPosition) < len(myHedgedBasket.smallPosition):
            
            
            while myHedgedBasket.volatility > myGlobalTargetVolatility * (1 + myTolerance):
                
                myBasketReductionPercentage = myGlobalTargetVolatility / myHedgedBasket.volatility - 1
                mySortedContributionToRisk, mySortID = zip(*sorted(zip(myHedgedBasket.contributionToRisk, range(len(myHedgedBasket.contributionToRisk))), key=lambda x: x[0], reverse=True))
                myReductionPercentage = [0] * len(mySortID)
                mySortedReductionPercentage = np.asarray([0] * len(mySortID))
                myReductionAllocated = 0
                myNrFundsIncluded = 1
                myContributionWeightDiff = [y - x for x, y in zip(mySortedContributionToRisk[:-1], mySortedContributionToRisk[1:])] + [0]
                myPercentageAllocated = 0
                
                while (myReductionAllocated == 0 or myNrFundsIncluded == len(mySortID)) and myNrFundsIncluded <= myHedgeConfig.maxNrOfOrders:
                    
                    if myBasketReductionPercentage <= myPercentageAllocated + myContributionWeightDiff[myNrFundsIncluded-1] * myNrFundsIncluded:
                        mySortedReductionPercentage[:myNrFundsIncluded] = mySortedReductionPercentage[:myNrFundsIncluded] + myContributionWeightDiff[myNrFundsIncluded-1]
                        
                    else:
                        
                        myRiskReductionToAllocate = myBasketReductionPercentage - myPercentageAllocated
                        mySortedReductionPercentage[:myNrFundsIncluded] = mySortedReductionPercentage[:myNrFundsIncluded] + myRiskReductionToAllocate/myNrFundsIncluded
                        myReductionAllocated = 1
                    
                    myPercentageAllocated = sum(mySortedReductionPercentage)
                    myNrFundsIncluded = myNrFundsIncluded + 1
                
                if myNrFundsIncluded > myHedgeConfig.maxNrOfOrders:
                    
                    myHedgedBasket = getMinimumVolatilityPortfolio(aBasket,myHedgeConfig):
                    break
                
                else:
                    
                    myReductionPercentage[mySortID] = mySortedReductionPercentage
                    myHedgedBasket.position = myHedgedBasket.position * np.asarray(1+myReductionPercentage)
                    myOrderSize = myHedgedBasket.position - aBasket.position
                    myClosePositionID = (np.abs(myOrderSize) < aBasket.minOrderSize) & \
                    (np.abs(myHedgedBasket.position) > aBasket.minOrderSize) & \
                    (np.abs(myHedgedBasket.position + myOrderSize) < aBasket.minOrderSize) & \
                    (np.abs(myHedgedBasket.position) * myHedgedBasket.constituentVolatility <= \
                    aHedgeConfig.maxConstituentVolatilityBeforeClosing)
                    
                    myHedgedBasket.position[myClosePositionID] = - aBasket.position[myClosePositionID]
                    myHedgedBasket.positionChange = myHedgedBasket.position - aBasket.position
                    mySmallPositionID = [abs(x) < y for x, y in zip(myHedgedBasket.position, myHedgedBasket.minOrderSize)]
                    for i in range(len(mySmallPositionID)):
                        if mySmallPositionID[i]:
                            myHedgedBasket.smallPosition[i] = 1
                    myHedgedBasket.variance = np.transpose(myHedgedBasket.position) * myHedgedBasket.covariance * myHedgedBasket.position
                    myHedgedBasket.volatility = np.sqrt(myHedgedBasket.variance)
                    myHedgedBasket = addRiskPerAsset(myHedgedBasket)
                    myIterations = myIterations+1
                
        else:
            
            myLocalTargetVolatility = (1+myHedgeConfig.localRiskReductionMultiplier)*myHedgeConfig.maxDailyPLSwing/sqrt(12*24)
            
            
            

    myClosePositionID = ((np.abs(aBasket.position) > aBasket.minOrderSize) & \
                        (myHedgedBasket.position. != aBasket.position) & \
                        ((np.abs(myHedgedBasket.position) <= myHedgedBasket.minOrderSize) | \
                        (np.abs(myHedgedBasket.position - aBasket.position) <= myHedgedBasket.minOrderSize))) 

    if sum(myClosePositionID) > 0:
        myHedgedBasket.position[myclosePositionID] = 0
        myHedgedBasket.positionChange = myHedgedBasket.position - aBasket.position
        myHedgedBasket.variance = np.transpose(myHedgedBasket.position)*myHedgedBasket.covarince * myHdegedBasket.position
        myHedgedBasket.volatility = np.sqrt(myHedgedBAsket.variance)
        myHedgedBasket = addRiskPerAsset(myHedgedBasket)
