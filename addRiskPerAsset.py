def addRiskPerAsset(aBasket):
    myBasket = aBasket
    myBasket.marginalContribution = aBasket.constituentVolatility * \
        (np.sum(aBasket.position * aBasket.constituentVolatility * \
        aBasket.correlation, axis=1)) / aBasket.volatility
    myBasket.contributionToRisk = aBasket.position * \
        myBasket.marginalContribution / aBasket.volatility
    myBasket.correlationToBasket = np.sign(aBasket.position) * \
        np.sum(aBasket.position * aBasket.constituentVolatility * \
        aBasket.correlation, axis=1) / aBasket.volatility
    Basket = myBasket
    return myBasket
