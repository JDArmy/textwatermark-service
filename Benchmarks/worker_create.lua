-- https://github.com/wg/wrk/blob/master/scripts/

wrk.method                  = "POST"
wrk.headers["Content-Type"] = "application/json"
wrk.body                    = [[{
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
  "use_job_id": true,
  "text": "string",
  "created": "2023-03-11T14:40:44.429172"
}]]
