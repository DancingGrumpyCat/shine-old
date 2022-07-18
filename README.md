# shine
A reactive programming language inspired by spreadsheet programming.

The basic form of the language is defining _value cells_ and _function cells_, both which are allowed to have _unknowns_. Unknowns can be defined relatively, in terms of each other. Here's an example shine program:
``` shine
1 * dm := 0.1 * m
1 * km := 1000 * m
1 * L  := 1 * dm^3
humanvolume := 66 * L
indiaarea := 3287263 * km^2
indiaheight := 8.59 * km
indiapopulation := 1.35e9 * people
print := humanvolume * indiapopulation / (indiaarea * indiaheight)
; 3.16e-9 * people
```

As the comment (the last line, starting with the semicolon) states, the program returns a value in units of people, of about 1 / 3.16 billion. The first three statements declare unit conversions in terms of each other. The units on these three lines are declared in a DAG relationship to each other, with the base case at meters, which is how the interpreter should know to use units of meters (or meters squared or meters cubed).

The next four lines define four cells:
- the volume of a human
- the area of India
- the height of India, based on its tallest mountain
- the population of India

Next, `print` is a predefined output cell targeted to stdout. In this line we calculate the frequency of person by volume in India.
