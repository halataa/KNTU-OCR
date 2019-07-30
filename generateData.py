#%%
import wikipedia
import re
wikipedia.set_lang("fa")
#%%
summaryNumber=1
for i in range (0,summaryNumber):
    summary=wikipedia.summary(wikipedia.random())
    pureSummary=re.sub('[^\s.،!؟?):/(٪|ء-ی|۰-۹|0-9]','',summary)  #eliminate english characters
puresummaryList=pureSummary.split(' ')





#%%
