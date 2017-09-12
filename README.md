# guikema_nfl_pool
Python Script to automate the Guikema Family NFL Pool

Based on being elected Commissioner of the Family Football Pool against my will (damn you democratic process!), I
decided to automate the process a bit.

Here is how I use the script:

1. Run the script with the current week, generating a csv with the schedule in the `csv/sched` directory:

   ```python debug.py <week>```

2. Update schedules into Drive account; use `create_form.gs` to create forms from these files
3. Download the results as `Week #.csv` in the `csv/score` directory
4. Once the week is completed, run the script again, which will compare each person's picks against the actual results,
   then output the score for the week and the season's results

```
chrisguikema@ubuntu:~/nfl$ python nfl.py 1
Calculating Score!
----------------------
 2017 Week 1 Results
----------------------
Amy 11
Laura 11
Sam 10
Tyler 10
Chris 10
Troy 9
Katie 9
Curt 7
---------------------
 2017 Season Results
---------------------
Amy 11
Laura 11
Sam 10
Tyler 10
Chris 10
Troy 9
Katie 9
Curt 7
---------------------
```

## Future Developments
* Determine how to use the `go` compiler to use the `skicka` tool in order to grab the csv from Drive automatically.
Information for `skicka` can be found [here](https://github.com/google/skicka/blob/master/README.md)
* Find out how to create a google form from a csv to take all manual work out of things
  * Done in commit `20cb1e6` with `create_form.gs`
