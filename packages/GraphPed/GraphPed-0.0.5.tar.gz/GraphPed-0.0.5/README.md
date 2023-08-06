# GraphPed
> A novel graph-based visualization method for large and complex pedigrees


Author: Yin Huang

Citation:

## Features
- It can deal with complex families, wrong pedigrees, and multiple groups in a family.

- It can help to check pedigrees. 

- It can show multiple traits or status in one pedigree.

- It can show pedigrees in jupyter notebook and output as common image format (pdf, svg, png).

## Install

`pip install graphped`

## How to use

#### 1. In command line

```
!GraphPed -h
```

    usage: GraphPed [-h] [-p PED] [-o OUTPUT] [-f FORMAT] [-a ATTRIBUTES]
                    [-e ENGINE]
    
    The arguments of graphped
    
    options:
      -h, --help            show this help message and exit
      -p PED, --ped PED     a ped file or an extended ped file (default: None)
      -o OUTPUT, --output OUTPUT
                            output folder (default: ./)
      -f FORMAT, --format FORMAT
                            the format of the output picture (default: svg)
      -a ATTRIBUTES, --attributes ATTRIBUTES
                            the attributes of the output picture (default: None)
      -e ENGINE, --engine ENGINE
                            the engine of graphviz rendering the output picture
                            (default: dot)


- 1. standard pedigrees in the ped file

```
GraphPed -p data/example_fam.ped -o data/cli/ -f pdf
```


- 2. extended pedigrees in the ped file

```
GraphPed -p data/example_fam_ext.ped -o data/cli/ -f svg -a data/default.yaml 
```

#### 2.In jupyter notebook

```
from graphped.plot import *
```

```
fam=readped('data/example_fam.ped')
plotped(fam)
```




    
![svg](docs/images/output_10_0.svg)
    



Or

```
show(GraphPed(fam))
```


    
![svg](docs/images/output_12_0.svg)
    


`GraphPed` function can plot all the pedigrees in the fam dataframe.

Adding self-defined attributes. the number of traits in the input file should match with the number of traits in the attribute yaml file.

```
attrs=load_attributes('data/default.yaml')
famext=readped('data/example_fam_ext.ped',attrs)
plotped(famext,attrs)
```




    
![svg](docs/images/output_14_0.svg)
    



Write to output folder with pdf format

```
plotped(famext,attrs,output='data/jpn',format='pdf')
```

Or output multiple pedigrees.

```
GraphPed(famext,attrs,output='data/jpn',format='pdf')
```

## Tutorial

### Setting the attribute yaml file

- reference: 
    - fillcolor https://graphviz.org/docs/attrs/fillcolor/
    - style https://graphviz.org/docs/attrs/style/
    - fontcolor https://graphviz.org/docs/attrs/fontcolor/
    - ... https://graphviz.org/doc/info/attrs.html

For one trait ped file, if the trait values are affected status, which should be coded as follows: -9 or 0 is missing,1 is unaffected, and 2 is affected. you don't need to set the attribute file. Otherwise, you need to set your attribute file by following:

The format of the attribute of yaml file
```
trait name:
    attribute name:
        (the pairs of tait value and attribute value)
        tait value1: attribute value1
        tait value2: attribute value2
        ...
```
If you have more than one traits, you need to set each trait separately in the yaml file.
The following is an example.

```
%%writefile data/default.yaml

trait1:
    fillcolor:
        1: 'white'
        2: 'dimgrey'
        -9: 'aquamarine3'

trait2:
    style:
        True: filled,setlinewidth(4)
        False: filled
    

trait3:
    fontcolor:
        True: darkorange
        False: black
    
```

    Overwriting data/default.yaml


```
attrs=load_attributes('data/default.yaml')
```

```
attrs
```




    {'trait1': {'fillcolor': {1: 'white', 2: 'dimgrey', -9: 'aquamarine3'}},
     'trait2': {'style': {True: 'filled,setlinewidth(4)', False: 'filled'}},
     'trait3': {'fontcolor': {True: 'darkorange', False: 'black'}}}



### Two example pedigrees
one is standard, one is extended with 3 traits.

#### Standard ped file

```
%%writefile data/example_fam.ped
Fam	F4	P3	F1	1	1
Fam	F3	P3	F1	2	1
Fam	F2	P3	F1	2	1
Fam	F1	P1	P2	2	2
Fam	P3	0	0	1	2
Fam	P1	0	0	1	-9
Fam	P2	0	0	2	-9
```

    Overwriting data/example_fam.ped


```
fam=readped('data/example_fam.ped')
```

```
fam
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>fid</th>
      <th>iid</th>
      <th>fathid</th>
      <th>mothid</th>
      <th>sex</th>
      <th>trait</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Fam</td>
      <td>F4</td>
      <td>P3</td>
      <td>F1</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Fam</td>
      <td>F3</td>
      <td>P3</td>
      <td>F1</td>
      <td>2</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Fam</td>
      <td>F2</td>
      <td>P3</td>
      <td>F1</td>
      <td>2</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Fam</td>
      <td>F1</td>
      <td>P1</td>
      <td>P2</td>
      <td>2</td>
      <td>2</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Fam</td>
      <td>P3</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>2</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Fam</td>
      <td>P1</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>-9</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Fam</td>
      <td>P2</td>
      <td>0</td>
      <td>0</td>
      <td>2</td>
      <td>-9</td>
    </tr>
  </tbody>
</table>
</div>



```
plotped(fam)
```




    
![svg](docs/images/output_30_0.svg)
    



```
plotped(fam)
```




    
![svg](docs/images/output_31_0.svg)
    



#### Extended ped file

```
%%writefile data/example_fam_ext.ped
Fam1	F4	P3	F1	1	1	True	False
Fam1	F3	P3	F1	2	1	True	True
Fam1	F2	P3	F1	2	1	True	False
Fam1	F1	P1	P2	2	2	True	False
Fam1	P3	0	0	1	2	True	False
Fam1	P1	0	0	1	-9	False	True
Fam1	P2	0	0	2	-9	False	True
```

    Overwriting data/example_fam_ext.ped


```
famext=readped('data/example_fam_ext.ped',attrs)
```

```
famext
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>fid</th>
      <th>iid</th>
      <th>fathid</th>
      <th>mothid</th>
      <th>sex</th>
      <th>trait1</th>
      <th>trait2</th>
      <th>trait3</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Fam1</td>
      <td>F4</td>
      <td>P3</td>
      <td>F1</td>
      <td>1</td>
      <td>1</td>
      <td>True</td>
      <td>False</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Fam1</td>
      <td>F3</td>
      <td>P3</td>
      <td>F1</td>
      <td>2</td>
      <td>1</td>
      <td>True</td>
      <td>True</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Fam1</td>
      <td>F2</td>
      <td>P3</td>
      <td>F1</td>
      <td>2</td>
      <td>1</td>
      <td>True</td>
      <td>False</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Fam1</td>
      <td>F1</td>
      <td>P1</td>
      <td>P2</td>
      <td>2</td>
      <td>2</td>
      <td>True</td>
      <td>False</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Fam1</td>
      <td>P3</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>2</td>
      <td>True</td>
      <td>False</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Fam1</td>
      <td>P1</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>-9</td>
      <td>False</td>
      <td>True</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Fam1</td>
      <td>P2</td>
      <td>0</td>
      <td>0</td>
      <td>2</td>
      <td>-9</td>
      <td>False</td>
      <td>True</td>
    </tr>
  </tbody>
</table>
</div>



```
plotped(famext,attrs)
```




    
![svg](docs/images/output_36_0.svg)
    



```
dots=GraphPed(fam)
```

```
show(dots)
```


    
![svg](docs/images/output_38_0.svg)
    


### Write out plots

```
plotped(fam,output='data/exampleplots',format='png')
```

Show the plot from `data/exampleplots/Fam.png`

![data/exampleplots/Fam.png](nbs/data/exampleplots/Fam.png "Fam.png")

## Real data examples

```
all_fam=readped('data/Fig_2_3_fam.ped')
```

```
all_fam
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>fid</th>
      <th>iid</th>
      <th>fathid</th>
      <th>mothid</th>
      <th>sex</th>
      <th>trait</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>25_2</td>
      <td>25_2_33</td>
      <td>25_2_49</td>
      <td>25_2_50</td>
      <td>2</td>
      <td>2</td>
    </tr>
    <tr>
      <th>1</th>
      <td>25_2</td>
      <td>25_2_28c1</td>
      <td>0</td>
      <td>0</td>
      <td>2</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>25_2</td>
      <td>25_2_25</td>
      <td>25_2_49</td>
      <td>25_2_50</td>
      <td>1</td>
      <td>2</td>
    </tr>
    <tr>
      <th>3</th>
      <td>25_2</td>
      <td>25_2_28</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>2</td>
    </tr>
    <tr>
      <th>4</th>
      <td>25_2</td>
      <td>25_2_29</td>
      <td>25_2_49</td>
      <td>25_2_50</td>
      <td>2</td>
      <td>2</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>401</th>
      <td>10R_R99</td>
      <td>10R_R99_22</td>
      <td>10R_R99_29</td>
      <td>10R_R99_15</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>402</th>
      <td>10R_R99</td>
      <td>10R_R99_29</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>2</td>
    </tr>
    <tr>
      <th>403</th>
      <td>10R_R99</td>
      <td>10R_R99_7</td>
      <td>0</td>
      <td>0</td>
      <td>2</td>
      <td>2</td>
    </tr>
    <tr>
      <th>404</th>
      <td>10R_R99</td>
      <td>10R_R99_8</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>405</th>
      <td>10R_R99</td>
      <td>10R_R99_8</td>
      <td>10R_R99_19</td>
      <td>10R_R99_5</td>
      <td>2</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
<p>406 rows × 6 columns</p>
</div>



#### Fig.1 The workflow of GraphPed

show workflow

#### Fig.2 The pedigrees of complex families

```
plotped(all_fam[all_fam.fid=='25_2'])
```




    
![svg](docs/images/output_48_0.svg)
    



#### Fig.S2 The largest pedigree in ADSP

```
plotped(all_fam[all_fam.fid=='4_649'])
```




    
![svg](docs/images/output_50_0.svg)
    



#### Fig.3 The pedigrees with incorrect information

```
plotped(all_fam[all_fam.fid=='10R_R99'])
```




    
![svg](docs/images/output_52_0.svg)
    



#### Fig.4 The pedigrees with multiple phenotypes

self-defined multiple-trait yaml

```
%%writefile data/self_defined_mutiple_traits.yaml

ad:
    fillcolor:
        1: 'white'
        2: 'dimgrey'
        -9: 'aquamarine3'

vcf:
    style:
        True: filled,setlinewidth(4)
        False: filled
    

trim:
    fontcolor:
        True: darkorange
        False: black
    
```

    Writing data/self_defined_mutiple_traits.yaml


```
attrs=load_attributes('data/self_defined_mutiple_traits.yaml')
ped=readped('data/Fig4_fam_ext.ped',attrs)
```

```
ped
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>fid</th>
      <th>iid</th>
      <th>fathid</th>
      <th>mothid</th>
      <th>sex</th>
      <th>ad</th>
      <th>vcf</th>
      <th>trim</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>10R_R99</td>
      <td>10R_R99_10</td>
      <td>10R_R99_2</td>
      <td>10R_R99_1</td>
      <td>2</td>
      <td>1</td>
      <td>True</td>
      <td>False</td>
    </tr>
    <tr>
      <th>1</th>
      <td>10R_R99</td>
      <td>10R_R99_19</td>
      <td>10R_R99_2</td>
      <td>10R_R99_1</td>
      <td>1</td>
      <td>1</td>
      <td>True</td>
      <td>False</td>
    </tr>
    <tr>
      <th>2</th>
      <td>10R_R99</td>
      <td>10R_R99_20</td>
      <td>10R_R99_2</td>
      <td>10R_R99_1</td>
      <td>1</td>
      <td>1</td>
      <td>False</td>
      <td>False</td>
    </tr>
    <tr>
      <th>3</th>
      <td>10R_R99</td>
      <td>10R_R99_21</td>
      <td>10R_R99_2</td>
      <td>10R_R99_1</td>
      <td>1</td>
      <td>1</td>
      <td>False</td>
      <td>False</td>
    </tr>
    <tr>
      <th>4</th>
      <td>10R_R99</td>
      <td>10R_R99_17</td>
      <td>10R_R99_29</td>
      <td>10R_R99_15</td>
      <td>1</td>
      <td>1</td>
      <td>True</td>
      <td>False</td>
    </tr>
    <tr>
      <th>5</th>
      <td>10R_R99</td>
      <td>10R_R99_22</td>
      <td>10R_R99_29</td>
      <td>10R_R99_15</td>
      <td>1</td>
      <td>1</td>
      <td>False</td>
      <td>False</td>
    </tr>
    <tr>
      <th>6</th>
      <td>10R_R99</td>
      <td>10R_R99_15</td>
      <td>10R_R99_8</td>
      <td>10R_R99_7</td>
      <td>2</td>
      <td>2</td>
      <td>True</td>
      <td>False</td>
    </tr>
    <tr>
      <th>7</th>
      <td>10R_R99</td>
      <td>10R_R99_12</td>
      <td>10R_R99_8</td>
      <td>10R_R99_7</td>
      <td>2</td>
      <td>2</td>
      <td>True</td>
      <td>False</td>
    </tr>
    <tr>
      <th>8</th>
      <td>10R_R99</td>
      <td>10R_R99_1</td>
      <td>10R_R99_8</td>
      <td>10R_R99_7</td>
      <td>2</td>
      <td>2</td>
      <td>True</td>
      <td>False</td>
    </tr>
    <tr>
      <th>9</th>
      <td>10R_R99</td>
      <td>10R_R99_5</td>
      <td>10R_R99_8</td>
      <td>10R_R99_7</td>
      <td>1</td>
      <td>1</td>
      <td>True</td>
      <td>False</td>
    </tr>
    <tr>
      <th>10</th>
      <td>10R_R99</td>
      <td>10R_R99_6</td>
      <td>10R_R99_8</td>
      <td>10R_R99_7</td>
      <td>2</td>
      <td>1</td>
      <td>True</td>
      <td>False</td>
    </tr>
    <tr>
      <th>11</th>
      <td>10R_R99</td>
      <td>10R_R99_2</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>-9</td>
      <td>False</td>
      <td>False</td>
    </tr>
    <tr>
      <th>12</th>
      <td>10R_R99</td>
      <td>10R_R99_29</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>2</td>
      <td>False</td>
      <td>False</td>
    </tr>
    <tr>
      <th>13</th>
      <td>10R_R99</td>
      <td>10R_R99_7</td>
      <td>0</td>
      <td>0</td>
      <td>2</td>
      <td>2</td>
      <td>False</td>
      <td>False</td>
    </tr>
    <tr>
      <th>14</th>
      <td>10R_R99</td>
      <td>10R_R99_8</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
      <td>False</td>
      <td>False</td>
    </tr>
  </tbody>
</table>
</div>



```
plotped(ped,attrs)
```




    
![svg](docs/images/output_58_0.svg)
    



#### Show multiple figures with self-defined attributes

self-defined single-trait yaml

```
%%writefile data/self_defined_single_trait.yaml

ad:
    fillcolor:
        1: 'white'
        2: 'dimgrey'
        -9: 'aquamarine3'
```

    Writing data/self_defined_single_trait.yaml


```
attr=load_attributes('data/self_defined_single_trait.yaml')
all_fam=readped('data/Fig_2_3_fam.ped',attr)
```

```
all_fam
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>fid</th>
      <th>iid</th>
      <th>fathid</th>
      <th>mothid</th>
      <th>sex</th>
      <th>ad</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>25_2</td>
      <td>25_2_33</td>
      <td>25_2_49</td>
      <td>25_2_50</td>
      <td>2</td>
      <td>2</td>
    </tr>
    <tr>
      <th>1</th>
      <td>25_2</td>
      <td>25_2_28c1</td>
      <td>0</td>
      <td>0</td>
      <td>2</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>25_2</td>
      <td>25_2_25</td>
      <td>25_2_49</td>
      <td>25_2_50</td>
      <td>1</td>
      <td>2</td>
    </tr>
    <tr>
      <th>3</th>
      <td>25_2</td>
      <td>25_2_28</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>2</td>
    </tr>
    <tr>
      <th>4</th>
      <td>25_2</td>
      <td>25_2_29</td>
      <td>25_2_49</td>
      <td>25_2_50</td>
      <td>2</td>
      <td>2</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>401</th>
      <td>10R_R99</td>
      <td>10R_R99_22</td>
      <td>10R_R99_29</td>
      <td>10R_R99_15</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>402</th>
      <td>10R_R99</td>
      <td>10R_R99_29</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>2</td>
    </tr>
    <tr>
      <th>403</th>
      <td>10R_R99</td>
      <td>10R_R99_7</td>
      <td>0</td>
      <td>0</td>
      <td>2</td>
      <td>2</td>
    </tr>
    <tr>
      <th>404</th>
      <td>10R_R99</td>
      <td>10R_R99_8</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>405</th>
      <td>10R_R99</td>
      <td>10R_R99_8</td>
      <td>10R_R99_19</td>
      <td>10R_R99_5</td>
      <td>2</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
<p>406 rows × 6 columns</p>
</div>



```
dots=GraphPed(all_fam,attr)
show(dots)
```


    
![svg](docs/images/output_64_0.svg)
    



    
![svg](docs/images/output_64_1.svg)
    



    
![svg](docs/images/output_64_2.svg)
    

