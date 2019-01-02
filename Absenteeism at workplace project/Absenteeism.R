rm(list=ls())
setwd("G:/data science project")
employee= read_xls("Absenteeism_at_work_Project.xls", col_names=T)
employee=as.data.frame(employee)

colnames(employee)=tolower(gsub(' ','_',colnames(employee)))
colnames(employee)
names(employee)[10]="work_load_average_per_day"
table(employee$reason_for_absence)
employee=employee[!employee$reason_for_absence==0,]
table(employee$absenteeism_time_in_hours)
employee=employee[!employee$absenteeism_time_in_hours==0,]
employee=employee[,-1]
for (i in c(1,2,3,4,11,12,14,15,20))
{
  employee[,i]=as.factor(employee[,i])
}

#library("DMwR")
missing_percentage=data.frame(colSums(is.na(employee))/nrow(employee))*100
names(missing_percentage)[1]="missing_percentage"
View(missing_percentage)
employee=knnImputation(employee,k=5)


#library(ggplot2)
numeric_index=sapply(employee,is.numeric)
numeric_data=employee[,numeric_index]
cnames=colnames(numeric_data)
cnames


for(i in 1:length(cnames))
{assign(paste0("gn", i),ggplot(aes_string(y = (cnames[i]),x = "absenteeism_time_in_hours")
                               ,data = subset(employee))+ stat_boxplot(geom = "errorbar", width = 0.5)+
          geom_boxplot(outlier.colour="RED",
                       fill ="grey", outlier.shape = 18, outlier.size = 1, notch = FALSE)+theme(legend.position = 'bottom')
        +
          labs(y = cnames[i],x = 'Absenteeism')+ 
          ggtitle(paste("Box plot of Absenteeism for", cnames[i])))}

#library(gridExtra)
gridExtra::grid.arrange(gn1,gn2,gn3,ncol = 3)
gridExtra::grid.arrange(gn4,gn5,gn6,ncol = 3)
gridExtra::grid.arrange(gn7,gn8,gn9,ncol = 3)
gridExtra::grid.arrange(gn10,gn11,ncol = 2)


for(i in cnames)
{val = employee[,i][employee[,i]%in%
                      boxplot.stats(employee[,i])$out]
employee[,i][employee[,i]%in%val]=NA}
employee = knnImputation(employee, k = 3)

correlation=cor(employee[,numeric_index])
correlation
corrplot.mixed(correlation,tl.offset=0.01,tl.cex=0.01)
findCorrelation(correlation,cutoff = 0.6)
cnames





factor_index=sapply(employee,is.factor)
factor_data=employee[,factor_index]
for(i in 1:8)
{print(names(factor_data)[i])
  print(chisq.test(table(factor_data$absenteeism_time_in_hours,factor_data[,i])))}
colnames(employee)
new_data=employee[,-c(7,12,15,17,18,16)]
colnames(new_data)
new_data$absenteeism_time_in_hours=as.numeric(new_data$absenteeism_time_in_hours)
new_data$absenteeism_time_in_hours=ifelse(new_data$absenteeism_time_in_hours<4,"less than 4","greater than 4")
new_data$absenteeism_time_in_hours=as.factor(new_data$absenteeism_time_in_hours)
View(new_data)
index=sample(nrow(new_data),0.7*nrow(new_data))
train=new_data[index,]
test=new_data[-index,]
rf=randomForest(absenteeism_time_in_hours~.,data = train,ntree=500)
predictions=predict(rf,test)
confmatrix_rf=table(test$absenteeism_time_in_hours,predictions)
confusionMatrix(confmatrix_rf)
colnames(train)
install.packages("inTrees")
library(inTrees)
treelist=RF2List(rf)
exec=extractRules(treelist,train[,-14])
exec[1:2,]
readableRules=presentRules(exec,colnames(train))
readableRules[1:2,]
rulemetric=getRuleMetric(exec,train[,-14],train$absenteeism_time_in_hours)
rulemetric[1:2,]

q()
