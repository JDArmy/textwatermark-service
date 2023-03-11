-- https://github.com/wg/wrk/blob/master/scripts/

wrk.method                  = "POST"
wrk.headers["Content-Type"] = "application/x-www-form-urlencoded"
wrk.body                    = "wm_str=888888"
