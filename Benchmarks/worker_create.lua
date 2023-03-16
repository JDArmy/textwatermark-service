-- https://github.com/wg/wrk/blob/master/scripts/

wrk.method                  = "POST"
wrk.headers["Content-Type"] = "application/json"
wrk.body                    = [[{
  "params": {
    "tpl_type": "INVISIBLE_CHARS",
    "confusables_chars": [],
    "confusables_chars_key": "",
    "wm_base": 29,
    "method": "INSERT_INTO_POSITION",
    "wm_mode": "REAL_NUMBER",
    "wm_len": 5,
    "wm_flag_bit": true,
    "wm_loop": false,
    "wm_max": "99999",
    "start_at": 1,
    "version": "0.3.2"
  },
  "use_job_id": true,
  "text": "12345678901"
}]]
