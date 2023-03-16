## wrk -d 30s -t 4 -c 8 -s Benchmarks/worker_create.lua --latency "http://0.0.0.0:8000/worker/create?authorize_key=d0f4ac8c14eae3a992aa574a55099e4f"

```
Running 30s test @ http://0.0.0.0:8000/worker/create?authorize_key=d0f4ac8c14eae3a992aa574a55099e4f
  4 threads and 8 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    18.91ms   14.65ms 242.87ms   92.37%
    Req/Sec   113.03     31.15   170.00     63.36%
  Latency Distribution
     50%   13.50ms
     75%   25.66ms
     90%   31.79ms
     99%   63.22ms
  13536 requests in 30.09s, 1.86MB read
Requests/sec:    449.92
Transfer/sec:     63.27KB
```

## wrk -d 30s -t 4 -c 8 -s Benchmarks/do_job.lua --latency 'http://0.0.0.0:8000/worker/65542/do_job?authorize_key=d0f4ac8c14eae3a992aa574a55099e4f'

最重要的是这个环节，从redo来看，性能瓶颈在数据库上

```
Running 30s test @ http://0.0.0.0:8000/worker/65542/do_job?authorize_key=d0f4ac8c14eae3a992aa574a55099e4f
  4 threads and 8 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    18.44ms   11.68ms 142.55ms   91.47%
    Req/Sec   114.57     35.79   191.00     71.50%
  Latency Distribution
     50%   15.68ms
     75%   22.59ms
     90%   28.73ms
     99%   69.76ms
  13731 requests in 30.08s, 3.21MB read
Requests/sec:    456.54
Transfer/sec:    109.32KB
```

## wrk -d 30s -t 4 -c 8  --latency 'http://0.0.0.0:8000/worker/65542?authorize_key=d0f4ac8c14eae3a992aa574a55099e4f'

```
Running 30s test @ http://0.0.0.0:8000/worker/65542?authorize_key=d0f4ac8c14eae3a992aa574a55099e4f
  4 threads and 8 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     6.95ms    2.18ms  43.09ms   89.87%
    Req/Sec   292.29     29.35   333.00     86.17%
  Latency Distribution
     50%    6.56ms
     75%    7.63ms
     90%    8.73ms
     99%   14.08ms
  34950 requests in 30.04s, 15.63MB read
Requests/sec:   1163.60
Transfer/sec:    532.94KB
```

## wrk -d 30s -t 4 -c 8  --latency 'http://0.0.0.0:8000/worker/65542/job/4904/redo?authorize_key=d0f4ac8c14eae3a992aa574a55099e4f'

```
Running 30s test @ http://0.0.0.0:8000/worker/65542/job/4904/redo?authorize_key=d0f4ac8c14eae3a992aa574a55099e4f
  4 threads and 8 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     2.94ms    2.36ms  54.25ms   93.80%
    Req/Sec   738.03    136.12     1.06k    69.00%
  Latency Distribution
     50%    2.41ms
     75%    3.28ms
     90%    4.55ms
     99%   11.11ms
  88230 requests in 30.04s, 15.57MB read
  Non-2xx or 3xx responses: 88230
Requests/sec:   2937.29
Transfer/sec:    530.66KB
```

## wrk -d 30s -t 4 -c 8  --latency 'http://0.0.0.0:8000/worker/65542/job/4904?authorize_key=d0f4ac8c14eae3a992aa574a55099e4f'

```
Running 30s test @ http://0.0.0.0:8000/worker/65542/job/4904?authorize_key=d0f4ac8c14eae3a992aa574a55099e4f
  4 threads and 8 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    20.87ms   15.47ms 174.27ms   87.23%
    Req/Sec   100.07     34.62   212.00     67.78%
  Latency Distribution
     50%   16.76ms
     75%   24.70ms
     90%   37.48ms
     99%   83.23ms
  11984 requests in 30.09s, 5.42MB read
  Socket errors: connect 0, read 2787, write 0, timeout 0
  Non-2xx or 3xx responses: 2788
Requests/sec:    398.30
Transfer/sec:    184.38KB
```
