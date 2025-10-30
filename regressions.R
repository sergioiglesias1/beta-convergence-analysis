library(car)

wdi <- read.csv("data/clean_wdi.csv", sep=",", dec=".")
wdi

wdi$developed <- ifelse(wdi$Group == "Developed", 1, 0)
wdi # with dummy var

### Regression nº1 ###
sreg1 <- lm(Stability_Growth..2014.2018._y ~ Recuperation_Growth..2009.2013._y, data=wdi)
summary(sreg1)

### Regression nº2 ###
sreg2 <- lm(Recent_Growth..2019.2024._y ~ Pre_Crisis_Growth..2004.2008._y, data=wdi)
summary(sreg2)

### Regression nº3 ###
sreg3 <- lm(Recuperation_Growth..2009.2013._y ~ Pre_Crisis_Growth..2004.2008._y, data=wdi)
summary(sreg3)

### Multiple Regression with Dummy & VIF
multimodel <- lm(Recuperation_Growth..2009.2013._y ~ 
                    developed +
                    Pre_Crisis_Growth..2004.2008._y,
                  data = wdi)
summary(multimodel)
car::vif(multimodel)