
# TextWatermark Service

An HTTP Service for using [TextWatermark](https://github.com/JDArmy/TextWatermark) module to watermark text.

Based on Fastapi.

## Installation

Modify Dockerfile and docker-compose.yml then run
`docker-compose -f docker-compose.yml up`

## Developing and Testing

### Install dependencies

```bash
code .

virtualenv venv
. venv/bin/activate

pip install poetry
poetry lock
poetry install

tox
```

### Run uvicorn

Run `python src/textwatermark_service/run.py`

Or run `uvicorn textwatermark_service.main:app --port 8000 --reload`

## Usage

There are 2 steps for using textwatermark-service

1. Create a worker when you want to watermark some text.
2. Do the watermarking job with the worker you created.

## Use Swagger UI for testing

Visit `http://0.0.0.0:8000/docs` and you will see swagger UI.

## Use Curl for testing

### Create worker

The params JSON string is the same as what you exported by using `TextWatermark` package in the console. see <https://textwatermark.jd.army/cmdline/#export-parameters-example>

```sh
curl -X 'POST' \
  'http://0.0.0.0:8000/worker/create?authorize_key=d0f4ac8c14eae3a992aa574a55099e4f' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "params": {"tpl_type": "HOMOGRAPH_NUMBERS", "confusables_chars": [], "confusables_chars_key": "", "wm_base": 7, "method": 1, "wm_mode": 1, "wm_len": 8, "wm_flag_bit": false, "wm_loop": false, "wm_max": "999999", "start_at": 0, "version": "0.2.1"},
  "use_job_id": false,
  "text": "1234567890123456789012345678901234567890",
  "created": "2023-03-11T14:40:44.429172"
}'
```

Result:

```json
{
  "worker_id": 65542
}
```

### Do job

```sh
curl -X 'POST' \
  'http://0.0.0.0:8000/worker/65542/do_job?authorize_key=d0f4ac8c14eae3a992aa574a55099e4f' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'wm_str=888888'
```

Result:

```json
{
  "use_job_id": false,
  "job_id": 66433,
  "wm_str": "888888",
  "wm_text": "Ӏ2𝟑𝟺Ƽ𝟔𝟩890123456789012345678901234567890"
}
```

### Get worker record

```sh
curl -X 'GET' \
  'http://0.0.0.0:8000/worker/65542?authorize_key=d0f4ac8c14eae3a992aa574a55099e4f' \
  -H 'accept: application/json'
```

Result:

```json
{
  "use_job_id": false,
  "created": "2023-03-11T15:16:02.791571",
  "text": "1234567890123456789012345678901234567890",
  "params": {
    "tpl_type": "HOMOGRAPH_NUMBERS",
    "confusables_chars": [],
    "confusables_chars_key": "",
    "wm_base": 7,
    "method": 1,
    "wm_mode": 1,
    "wm_len": 8,
    "wm_flag_bit": false,
    "wm_loop": false,
    "wm_max": "999999",
    "start_at": 0,
    "version": "0.2.1"
  },
  "id": 65542
}
```

### Redo job

```sh
curl -X 'POST' \
  'http://0.0.0.0:8000/job/4904/redo?authorize_key=d0f4ac8c14eae3a992aa574a55099e4f' \
  -H 'accept: application/json' \
  -d ''
```

Result:

```json
{
  "use_job_id": false,
  "job_id": 4904,
  "wm_str": "888888",
  "wm_text": "Ӏ2𝟑𝟺Ƽ𝟔𝟩890123456789012345678901234567890"
}
```

### Get job record

```sh
curl -X 'GET' \
  'http://0.0.0.0:8000/job/4904?authorize_key=d0f4ac8c14eae3a992aa574a55099e4f' \
  -H 'accept: application/json'
```

Result:

```json
{
  "created": "2023-03-11T15:18:17.792940",
  "id": 4904,
  "worker_id": 65542,
  "wm_str": "888888",
  "worker": {
    "use_job_id": false,
    "created": "2023-03-11T15:16:02.791571",
    "text": "1234567890123456789012345678901234567890",
    "params": {
      "tpl_type": "HOMOGRAPH_NUMBERS",
      "confusables_chars": [],
      "confusables_chars_key": "",
      "wm_base": 7,
      "method": 1,
      "wm_mode": 1,
      "wm_len": 8,
      "wm_flag_bit": false,
      "wm_loop": false,
      "wm_max": "999999",
      "start_at": 0,
      "version": "0.2.1"
    },
    "id": 65542
  }
}
```

## Use wrk for benchmarks

see `wrk.md` in `Benchmarks` Directory.
