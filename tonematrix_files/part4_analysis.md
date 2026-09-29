  When testing the differences between the unoptimized and the optimized code, the results go as follows copied directly from the terminal itself:
  
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
  
  As seen here, the optimized version is better in many cases than the unoptimized version. To be specific, using the linear regression models for the performance while separating the densities 0.05 and 0.25, the optimized version is 1.71x and 1.07x faster than the unoptimized version per sample respectively. This means that the optimized version works faster when the density is lower, while its advantage diminishes as the density increases. Following this trend, the break-even point is expected to be around 0.27, though this is only an estimate as the benchmark only tested densities of 0.05 and 0.25.
  
  In terms of big-$O$ notation, the runtime can be described using the grid size $n$ and the total number of audio samples $N$. In the unoptimized version, every sample processes every string in the grid, giving a runtime of $O(Nn)$. However, $N$ is not independent of $n$, as the program generates 8192 samples per column, which means that $N = 8192n$. Therefore, the runtime can be written as $O((8192n)n)$, which is simplified to $O(n^2)$ because 8192 is a constant. This explains why doubling the grid size results in approximately four times the runtime, since both the number of strings processed per sample and the total number of samples are doubled. Density has little effect on the unoptimized version because every string is processed regardless of whether it is currently producing an audible sound. Thus, increasing the density does not significantly increase the amount of work performed by the algorithm, which is consistent with the runtimes we observed between densities 0.05 and 0.25 in the benchmark.
  
  The optimized version changes this by keeping track of which strings are currently active. Instead of processing all $n$ strings for every sample, it processes only the ringing strings $a$, where \(a \leq n\). Therefore, it would have a runtime of $O(Na)$, and since $N = 8192n$, it becomes $O(8192na)$, which is simplified to $O(na)$. When only a small number of strings are active, $a$ is much smaller than $n$, resulting in less processing than the unoptimized version. However, in the worst case where all the strings are active, $a$ = $n$, the optimized version would have the same worst-case complexity as the unoptimized version, which is $O(n^2)$. The number of lit cells $k$ does not directly determine the mixing cost because multiple lit cells in the same row still correspond to only one string. Instead, $a$, the ringing strings, determines how many strings are mixed for each sample.
  
  Regarding the optimization itself, since option A is implemented here, it performs really well at low density like what was mentioned earlier. Within the code itself, the program checks if the energy of a string goes below a certain threshold. Once that is reached, the string is removed from the set of active strings and is no longer processed. However, this checking also adds a bit to the runtime, since calculating energy requires going through the samples in the ring buffer. Because of this, the energy check is not $O(1)$, although it is only performed once per column. Theoretically, however, it is possible to turn the checking into $O(1)$ directly by calculating the number of steps until the threshold is reached. This idea would mean that each sample would store more data about how long it can play, so it would be a sacrifice of memory for speed.
  
  Exploring the effectiveness of the algorithm further, though the overall $O()$ stays the same in the worst case, the optimization changes what gets actually processed. At a density of 0.05, relatively few strings are active, so the optimized version can avoid processing a large number of inactive strings. However, at a density of 0.25, there are more strings active, so the difference between the optimized and unoptimized algorithm becomes smaller. This explains the observation in the benchmark where the improvement of the optimization decreases as density increases. We do have to note that the overhead produced from checking the energy of the strings is high enough that the optimization may become slower than the unoptimized algorithm when the density is high enough, since most strings still need to be processed while the additional energy checks are also performed. 
