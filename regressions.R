library(car)
library(lmtest)

wdi <- read.csv("C:/Users/Usuario/Downloads/DB/clean_wdi.csv", sep=",", dec=".")

wdi$developed <- ifelse(wdi$Group == "Developed", 1, 0)
wdi # with dummy var

# Regression nº1
sreg1 <- lm(Stability_Growth..2014.2018._y ~ Recuperation_Growth..2009.2013._y, data=wdi)
summary(sreg1)
coeftest(sreg1, vcov = vcovHC(sreg1, type="HC1"))

# Regression nº2
sreg2 <- lm(Recent_Growth..2019.2024._y ~ Pre_Crisis_Growth..2004.2008._y, data=wdi)
summary(sreg2)
coeftest(sreg2, vcov = vcovHC(sreg2, type="HC1"))


# Regression nº3
sreg3 <- lm(Recuperation_Growth..2009.2013._y ~ Pre_Crisis_Growth..2004.2008._y, data=wdi)
summary(sreg3)
coeftest(sreg3, vcov = vcovHC(sreg3, type="HC1"))


### Generalized Linear Model, VIF and robust stderr
multimodel <- glm(developed ~ Pre_Crisis_Growth..2004.2008._y + 
                    Recuperation_Growth..2009.2013._y,
                  data=wdi)
summary(multimodel)
car::vif(multimodel)
coeftest(multimodel, vcov = vcovHC(multimodel, type="HC1")) 
