# Quering Datasets using Natural Lanaguage

### Leveraging ChatGPT to have a conversational interface for a non-expert to explore a dataset

This application provides a web interface to load a CSV file so it can be explored conversationally (using OpenAI API and LangChain Python DataFrame Agent, see below for technical details and documentation links).
<br>&nbsp;<br>

<img src="https://github.com/raul-arrabales/LLM_Dataset_Quering/blob/main/media/QG_Streamlit.JPG" width="520">

#### The following is a typical example of usage:<br>
Let's say that we have a dataset and we want to know how different genders are represented in our sample, using the chat we could simply go like this: 

<img src="https://github.com/raul-arrabales/LLM_Dataset_Quering/blob/main/media/QG_ChatGPT.JPG" width="520">

The very same query in Python might look something like this: 

```python
# Get a summary of the gender column
df.Gender.value_counts()
```
```
Gender
2    833
1    149
3     28
Name: count, dtype: int64
```
We see the gender is coded with values 1, 2, and 3.<br>
Let's assume we know that 1 corresponds to male, 2 stands for female and 3 is the code for other gender identification.
```python
gender_dict = {2:'Female', 1:'Male', 3:'Undetermined'}
```
Now, we need to obtain the counts in a way that can be used to calculate the percentages:
```python
# A dataframe with the gender counts
gender_counts = df.Gender.value_counts().rename_axis('gender').reset_index(name='count')
```
And finally we can get our desired output, the percentage of each gender as represented in this dataset: 
```python
for i,c in gender_counts.iterrows():
    gender_str = gender_dict.get(c['gender'])
    pct = c['count']/len(df) * 100
    print(f'{gender_str}: {pct:.2f}%')
```
```
Female: 82.48%
Male: 14.75%
Undetermined: 2.77%
```
As we see it takes some coding effort to obtain this insight, while it can be obtained quite naturally by talking to ChatGPT (or any other LLM). In this case, we're using a LangChain agent - [Python DataFrame Agent](https://python.langchain.com/en/latest/modules/agents/toolkits/examples/pandas.html) - and [OpenAI API](https://platform.openai.com/docs/api-reference/chat). 

