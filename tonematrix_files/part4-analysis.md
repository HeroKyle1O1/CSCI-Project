When testing the differences between the unoptimized and the optimized code, the results goes as follows copied directly from the terminal itself:

```
(tonematrixenv) chance@192 tonematrix_files % python benchmark.py
  size  density    samples   seconds  μs/sample  x realtime
     8     0.05      65536     0.140      2.140       10.60
     8     0.25      65536     0.140      2.131       10.64
    16     0.05     131072     0.540      4.118        5.51
    16     0.25     131072     0.542      4.135        5.48
    32     0.05     262144     2.174      8.292        2.73
    32     0.25     262144     2.175      8.297        2.73
    64     0.05     524288     8.614     16.429        1.38
    64     0.25     524288     8.756     16.700        1.36
(tonematrixenv) chance@192 tonematrix_files % python benchmark.py --impl optimized
  size  density    samples   seconds  μs/sample  x realtime
     8     0.05      65536     0.014      0.211      107.24
     8     0.25      65536     0.115      1.761       12.88
    16     0.05     131072     0.171      1.302       17.41
    16     0.25     131072     0.511      3.902        5.81
    32     0.05     262144     1.181      4.506        5.03
    32     0.25     262144     1.999      7.626        2.97
    64     0.05     524288     4.452      8.492        2.67
    64     0.25     524288     8.112     15.472        1.47
```

As seen here, the optimized version is better in many cases than the unoptimized version. To be specific, using the linear regression models for the performance while separating the densities 0.05 and 0.25, the optimized version is 1.71x and 1.07x faster than the unoptimized version per sample respectively. This means that the optimized version works faster when the density is lower and vice versa; following this trend, the break-even point is expected to be around 0.27 with a higher density leading to worse outcomes for the optimized version.

In terms of big-$O$ notation, both algorithms run in $O(n^2)$ time based on three independent variables provided above: the size $s$, the density $d$, and the samples $n$. In both cases, when $s$ and $n$ are both increased by a factor of 2, the times increased by a factor of 4 suggesting that both variables have a linear relationship with the time taken. This does not apply with density however since the unoptimized version shows a lack of time difference based on it. With this in mind, the base runtime would be $k(sn) + C$ with $k$ being the time taken to perform the operation and $C$ serving as a constant for other unrelated processes.

As the model runs based on the Karplus-Strong algorithm, the nature of its $O()$ time can be broken down further by analyzing it. Each tone matrix (i.e. the machine that produces a sound) contains a ring buffer with a set of initial samples, which is processed by the algorithm overtime to mimic a guitar string sound. Processing each sample then takes $O(n)$ time beyond the initial "excitement" as the algorithm is applied up to the number of samples present. This only applies to one tone buffer though as it can be increased beyond just a single; as a result, the size is another factor $O(n)$ that serves as a multiplier to the processes present.

Regarding the optimization itself, since option A is implemented here, it performs really well at low density like what was mentioned earlier. Within the code itself, while a for loop with $O(n)$ time is used to check if the sound goes below a threshold, it is possible to turn the checking into O(1) directly by calculating the number of steps until the threshold is reached. This idea would mean that each sample would store more data about how long it can play, so it would be a sacrifice of memory for speed. Once the threshold is reached, the sample itself is discarded such that it isn't rendered by the CPU anymore, saving processing time.

Exploring the effectiveness of the algorithm further, though the overall $O()$ stays the same, it changes what gets actually processed. In the, the base runtime now would be $l[1 + d(k(sn))] + C$ with $l$ being the time taken to check each element's state on whether or not they should be discarded. As this is an upper bound, a more accurate graph is likely lower and more curved as more samples are discarded overtime. Even with this, the overhead produced by $l$ is still high enough that it is only faster when the density is fairly low. In practice, it is much more efficient to do it in this way since most music do not rely on a large barrage of notes.
