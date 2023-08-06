# SIMPLE FREQUENCY COUNTER
Calculate word occurences in txt files inside a given folder.  

## Usage
```python
from  frequency_counter.counter  import  FrequenciesGenerator

fg = FrequenciesGenerator('my_test_folder')

# print occurences of the word 'example' in 'text1.txt'  
fg.get_frequency('example', 'text1.txt')

# print occurences of the word 'example' in all files 
fg.get_frequency('example')

# print similarity between two file depending on word overlap
fg.calculate_similarity('text2.txt','text1.txt' )
```