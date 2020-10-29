# logstash_get_pipelines

Sample output

```
zzz@zzz:~$ ./getpipelines 
http://localhost:9601/_node/stats/pipelines
id                        name              out         in durat°(ms) avg(ms) failures
------------------------- ---------- ---------- ---------- ---------- ------ --------
grok back                 grok           110727     110727      11731 0.1059        0
grok accesslog            grok            91063      91063       9375 0.1030        0
grok solr_server          grok             1690       1690         93 0.0550        0
2a2a6f456bd15437803d6a4f1 mutate            685        685         27 0.0394        -
LogTime_date              date           204165     204165       8003 0.0392        1
Remove ANSI color codes   mutate         204165     204165       3397 0.0166        -
0dd67f2af65286e9bfaacf67a mutate           1690       1690         24 0.0142        -
add logstash hostname for mutate         204165     204165       1799 0.0088        -
ede1e8b139e94c98276a03ec3 mutate          91063      91063        744 0.0082        -
add tag for debug         mutate          93438      93438        492 0.0053        -

```
Help
```
zzz@zzz:~$ ./getpipelines --help
usage: getpipelines [-h] [-m MD] [-c COUNT] [-t] [-f] [-v] [url]

Prints logstash filter time execution

positional arguments:
  url         url to _node/stats/pipeline

optional arguments:
  -h, --help  show this help message and exit
  -m MD       minimum duration_in_millis
  -c COUNT    minimum count (input + output)
  -t          sort by total time (default: average per event)
  -f          ignore events with no failure, except drop
  -v          verbose

```
