# Jarvis
Misc, 70

## Jarvis - Miscellaneous 70
>  Written by vbhaip
>  Tony Stark tried asking for a flag from Jarvis, but Jarvis became corrupted and only outputted these two files for some reason. Note, the flag is in the format "flag{message}" and the message only contains lowercase letters and underscores.
>  File 1 File 2

### Solution 1: Machine Learning

We are given a help.csv, and a flag.csv. After a bit of inference we can conclude that we have to train a machine learning model on help.csv, and predict values from flag.csv.

The first column in help.csv is the label (desired output) for the rest of the row.

We apply tensorflow learning to the CSVs, and predict the flag's bits.

Bravech modified the CSVs to include row headers at the top.

You can find them here:

[help.csv](https://pastebin.com/raw/Ay8x3K05)

[flag.csv](https://pastebin.com/raw/SjkZHArF)

```python
import pandas as pd
import tensorflow as tf

df = pd.read_csv('help.csv')

bit = df.pop('bit')
dataset = tf.data.Dataset.from_tensor_slices((df.values, bit.values))

train_dataset = dataset.shuffle(len(df)).batch(1)
print(train_dataset)

model = tf.keras.Sequential([
  tf.keras.layers.Dense(10, activation='relu'),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(10),
  tf.keras.layers.Dense(2)
])

loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

model.compile(optimizer='adam',
              loss=loss_fn,
              metrics=['accuracy'])

model.fit(train_dataset, epochs=15)

#predict
import numpy

my_data = numpy.genfromtxt('flag.csv', delimiter=',')

probability_model = tf.keras.Sequential([
  model,
  tf.keras.layers.Softmax()
])

predicted = probability_model(my_data)

bits = []
for x in predicted:
  if x[0] > x[1]:
    bits.append('0')
  else:
    bits.append('1')
    
tot = ''.join(bits)

import binascii

print(binascii.unhexlify('%x' % int(tot, 2)).decode())
```

The script prints out `flaG{mlWis_cool}` or some similar variation.

We can basically guess the actual flag from there on if submitting it doesn't work.

Flag: `flag{ml_is_cool}`

### Solution 2: AI is just IF statements
Go into help.csv and sort by the second column. We can see that there are a lot of 0s at the top and a lot of 1s at the bottom. In fact, if the value of the cell in the second column is greater than 60, the first column is guaranteed to be 1, and if the value of that cell is less than 40, the first column is guaranteed to be 0. Rinse and repeat on the other columns.

In the end, we come up with the following Excel formula:
```excel
=IF(A1>60,1,IF(A1<40,0,IF(B1>40,1,IF(B1<35,0,IF(C1<10,0,IF(C1>90,1,IF(D1<20,1,IF(D1>80,0,IF(E1<5,0,IF(E1>95,1,IF(F1>60,0,IF(F1<40,1,IF(G1>90,1,IF(G1<10,0,IF(H1>90,1,IF(H1<30,0,IF(I1<40,1,IF(I1>50,0,IF(J1<40,1,IF(J1>60,1,0))))))))))))))))))))
```

We fill this formula downwards and convert the resulting bits to ASCII to get the flag: `flag{ml_is_cool}`