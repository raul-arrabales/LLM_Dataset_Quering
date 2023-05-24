# Quering Datasets using Natural Language

<p align="left">    
  <a href="https://github.com/raul-arrabales/LLM_Dataset_Quering/blob/main"> 
   <img alt="Last Commit" src="https://img.shields.io/github/last-commit/raul-arrabales/LLM_Dataset_Quering" target="_blank" />
  </a> 
   <a href="https://github.com/raul-arrabales/LLM_Dataset_Quering/blob/main/LICENSE">
    <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-yellow.svg" target="_blank" />
  </a> 
  <a href="https://github.com/raul-arrabales/LLM_Dataset_Quering/blob/main">
    <img alt="Python ver" src="https://img.shields.io/github/pipenv/locked/python-version/raul-arrabales/LLM_Dataset_Quering" target="_blank" />
  </a> 
   <a href="https://github.com/raul-arrabales/LLM_Dataset_Quering/blob/main">
    <img alt="Release" src="https://img.shields.io/github/v/tag/raul-arrabales/LLM_Dataset_Quering" target="_blank"/>
  </a>
  <a href="https://github.com/raul-arrabales">
    <img alt="Follow Me" src="https://img.shields.io/github/followers/raul-arrabales" target="_blank"/>
  </a>
</p>


### Leveraging ChatGPT to have a conversational interface for a non-expert to explore a dataset

This application provides a web interface to load a CSV file so it can be explored conversationally (using OpenAI API and LangChain Python DataFrame Agent, see below for technical details and documentation links).
<br>&nbsp;<br>
___
### 5 minutes demo

<a href="http://www.youtube.com/watch?feature=player_embedded&v=prbl_cM3iJk" target="_blank">
<img src="http://img.youtube.com/vi/prbl_cM3iJk/mqdefault.jpg" alt="Watch the video" width="80" border="10" align="top"/>
Quering CSV using ChatGPT - 5 min. demo - English - YouTube
</a>
<p>&nbsp;</p>
<a href="http://www.youtube.com/watch?feature=player_embedded&v=IcWfYAYp-lw" target="_blank">
<img src="http://img.youtube.com/vi/IcWfYAYp-lw/mqdefault.jpg" alt="Watch the video" width="80" border="10" align="top"/>
Quering CSV using ChatGPT - 8 min. demo (featuring some ChatGPT Hallucinations) - Spanish - YouTube
</a>

___

#### The following is a typical example of usage:<br>
Let's say that we have a dataset and we want to know how different genders are represented in our sample, using the chat we could simply go like this: 

- Load the dataset (CSV file) using the web interface: 

<img src="https://github.com/raul-arrabales/LLM_Dataset_Quering/blob/main/media/QG_Streamlit.JPG" width="520">

- Ask the question about gender representation (please, note that how each gender type is encoded in the dataset is not obvious, but we can also provide that specific information to the chatbot): 

<img src="https://github.com/raul-arrabales/LLM_Dataset_Quering/blob/main/media/QG_ChatGPT.JPG" width="520">

- The very same query in Python might look something like this (note that it'll take some Python and Pandas expertise to obtain the very same information that was easily obtained just by asking the chatbot): 

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
```python
print(gender_counts.to_string(index=False))
```
```
gender	count
2       833
1       149
3       28
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
As we can see it takes some coding effort to obtain this insight, while it can be obtained quite naturally by talking to the OpenAI model (or any other LLM). In this case, we're using a LangChain agent - [Python DataFrame Agent](https://python.langchain.com/en/latest/modules/agents/toolkits/examples/pandas.html) - and [OpenAI API](https://platform.openai.com/docs/api-reference/chat). <br>

___

### Build application
Using the included Dockerfile you can build a docker image for this application using: 
```
docker build -t chatcsv .
```
___

### Run application
Once the docker image is built you can run the app as follows (after adding your own OpenAI API Key to the *"ChatGPT_QueryCSV_env.txt"* file): 
```
docker run --env-file .\ChatGPT_QueryCSV_env.txt -p 8501:8501 chatcsv
```
___

For more examples using a similar approach see: 
- [ChatwithGPT project](https://github.com/bijucyborg/chatwithcsv)
- [Minimal Streamlit UI for ChatGPT](https://github.com/marshmellow77/streamlit-chatgpt-ui/)

