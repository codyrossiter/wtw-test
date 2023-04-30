## Data Engineer - Technical Test

### Format

This is an "open book" short technical test, designed to be a couple of hours at most. It's meant to highlight your skills & experience in designing & implementing a solution to the problem statement below. It does NOT need to be complete, perfectly designed, fully tested or production ready.


### Why am I being asked to do a test?

Your time is precious and you might be wondering why we ask candidates to undertake a short technical test. There are three main reasons:

1. It helps confirm that a candidate actually possess some of the skills they mention on their CV. Unfortunately we've had candidates in the past where they do not possess the technical skills they claim to have. A short test helps filter out unsuitable candidates earlier in the process.

2. It much more accurately reflects the work we do on a daily basis. Being asked in an interview to write algorithms on a white board or put down code on a piece of paper with no reference material is not how we operate in real life.

3. It helps candidates put their best foot forward. There are many good software engineers who don't perform at their best in an interview.

### Technical Direction

In this test, you are asked to write three simple scripts/console applications. You may assume that your scripts will be run locally and all provided data will be stored in a local folder.
We would like the code to be written in Python. You may use any libraries/packages you find useful.

This problem is based on a fictional scenario involving wind turbines. Rest assured, though, that no domain knowledge on wind turbines is required. All data is entirely synthetic.

### Scenario

You have received a batch of time series data from 20 wind turbines across four wind farms in December 2022.
Each turbine has several sensors which monitor important physical properties at different parts of the turbine, such as temperatures, pressures and levels of vibration.
You have been asked to investigate an issue that has been causing these turbines to unexpectedly shut down.
The file "downtime.csv" lists instances of turbine downtime that have been caused by this issue. Each occurrence has a start date and end date, and the four digit ID of the turbine affected.
Additionally, the file "turbine_metadata.csv" contains the ID of each turbine along with which of the four wind farms (Alpha, Bravo, Charlie or Delta) the turbine belongs to.

### Task 1

First, we would like to quantify the impact of this fault mode.
Write a script that prints the total downtime caused by this fault mode across all the turbines in December 2022,
and also a breakdown of total downtime by wind farm.

### Task 2

Since these wind farms are offshore, it can take maintenance engineers up to a day to travel out to a turbine and get it back online after a fault.
If we could detect signs of this fault mode emerging before the turbine shuts down, we could send an engineer out ahead of time, minimising downtime.
Experts have suggested that an abrupt increase in vibration in the turbine (measured by sensors RadialVibX and RadialVibY) might provide a good predictor.
Write a script that will generate a time series chart that illustrates an example of this.

### Task 3

The wind farm owners would like to create a notification system that will alert engineers when signs of an upcoming fault are detected.
For example, when an increase in vibration is detected, as mentioned in Task 2, a notification could be sent out.
In the longer term, they would like to create a web app that lets engineers view historical sensor data, with annotations highlighting previous occurrences of faults and alerts.

For this task, write a console application that, given a timestamp and the name of a wind farm, will print a table summarising the status of each wind turbine on the given farm at the given time.
Possible statuses include:

-  OK: The turbine is up and running normally
-  WARNING: There are signs that a fault might be upcoming
-  DOWN: The turbine is shut down

You may also add other status codes if you think of appropriate ones.
We would like to see one or two examples of automated tests to verify the correctness of your application.

In the next interview, we would expect to talk about decisions you made and your approach to testing.
We would also talk about how your console app could be modified and deployed as part of the notification system and web app described above.
Think about how you might address issues of scale as the system is deployed to an increasing number of turbines and as the historical data log grows.
You may prepare a diagram or a couple of paragraphs on these topics if you wish.