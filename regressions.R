library(sandwich)
library(lmtest)

df_wdi <- read.csv("C:/Users/Usuario/Downloads/beta-convergence-analysis/data/clean_data.csv", sep=",", dec=".")

df_wdi$developed <- ifelse(df_wdi$Group == "Developed", 1, 0)
df_wdi # with dummy variable

# Regression nº1
sreg1 <- lm(Stability..2014.2018. ~ Recuperation..2009.2013., data=df_wdi)
summary(sreg1)
coeftest(sreg1, vcov = vcovHC(sreg1, type="HC1"))

# Regression nº2
sreg2 <- lm(Recent..2019.2024. ~ Pre_Crisis..2004.2008., data=df_wdi)
summary(sreg2)
coeftest(sreg2, vcov = vcovHC(sreg2, type="HC1"))


# Regression nº3
sreg3 <- lm(Recuperation..2009.2013. ~ Pre_Crisis..2004.2008., data=df_wdi)
summary(sreg3)
coeftest(sreg3, vcov = vcovHC(sreg3, type="HC1"))


### Generalized Linear Model, VIF and robust stderr
mreg <- glm(developed ~ Pre_Crisis..2004.2008. + 
                    Recuperation..2009.2013.,
                  data=df_wdi)
summary(mreg)
car::vif(mreg)
coeftest(mreg, vcov = vcovHC(mreg, type="HC1")) 
