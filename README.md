## Quering Datasets using LLMs

This application provides a web interface to load a CSV file so it can be explored conversationally using OpenAI API. The following is a typical example of usage: 

<img src="https://github.com/raul-arrabales/LLM_Dataset_Quering/blob/main/media/QG_ChatGPT.JPG" width="320">

```python
df.Gender.value_counts()
```
```
Gender
2    833
1    149
3     28
Name: count, dtype: int64
```
```python
gender_dict = {2:'Female', 1:'Male', 3:'Undetermined'}
```
```python
gender_counts = df.Gender.value_counts().rename_axis('gender').reset_index(name='count')
```
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
