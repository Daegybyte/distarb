# Diego's Capstone Project MSD 2022

## Distance Arbitrage aka Distarb

## Licensing
Distance Arbitrage a.k.a. Distarb is offered free of charge under MIT License as free and open source software.

Copyright 2022 Daegybyte

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies
or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.


## Contents:
* ### [distarb.app](https://github.com/UtahMSD/diegoPisciotta/releases/tag/1.1.0).
	
* ### paper

* ### app
	* Contains copies of the source code in `distarb.app/Contents/Resources/app/`.


## Setup:

### A `.zip` of the current release of Distarb can be found [here](https://github.com/UtahMSD/diegoPisciotta/releases/tag/1.1.0).
<br/>


### Why doesn't this work?


#### In the event the executable fails, try:
 
 - Right clicking the application and clicking run. This will circumvent Apple trying to protect you from unidentified developers.

#### If that fails:

 - In your terminal, navigate to where you see '`distarb.app`' and run the script: 
 
 $`bash distarb.app/Contents/MacOS/distarb`
 
 It is worth noting that this may be necessary to get the webscraper to work.
 
 - 

If the above fails and you are having environment issues,  A `.yml` of the conda environement to run the application can be found [here](https://anaconda.org/daegybyte/distarb).

If all else fails and you cannot get distarb to run at all, maybe consider a different field.


## Instructions:

In the program window, select the radio button for what functionality you are interested in. The default button on the left is to figure out the edit distance using the distance calculating algorithm. The results will be ranked by edit and physical distance. The two dropdowns at the top allow you to select a company by either its company name, or its ticker name. The right radio button activates the webscraper.


![app](app_screen.png)

## Class diagram:

![diagram](distance_arbitrage.drawio.png)

### Bug Reporting:

Please report all bugs to [@elonmusk](https://twitter.com/elonmusk/with_replies?lang=en) on Twitter.

### Miscellaneous:
 
No animals were harmed in the making of this program. However one particularly happy corgi did receive many treats fromt the treat jar on my desk. He is becoming a bit of a chunk as a result. 


#### Like keys on a keyboard, your turn signal is not that far from your fingers. Use it.