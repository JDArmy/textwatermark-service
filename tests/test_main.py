"""pytest"""
import re
from copy import deepcopy

from fastapi.testclient import TestClient
from textwatermark.version import __version__

from textwatermark_service import app

client = TestClient(app)

AUTHORIZE_KEY = "123456"

json_obj = {
    "params": {
        "tpl_type": "HOMOGRAPH_NUMBERS",
        "confusables_chars": [],
        "confusables_chars_key": "",
        "wm_base": 7,
        "method": "FIND_AND_REPLACE",
        "wm_mode": "REAL_NUMBER",
        "wm_len": 11,
        "wm_flag_bit": False,
        "wm_loop": False,
        "wm_max": "1977326742",
        "start_at": 0,
        "version": __version__,
    },
    "use_job_id": False,
    "text": "12345678901",
    # "last_job_id": 0,
    # "created": "2023-03-01T16:49:32.509023",
}


def test_main_simple():
    """test main"""
    # create_worker
    res1 = client.post(
        "/worker/create", params={"authorize_key": AUTHORIZE_KEY}, json=json_obj
    )

    assert res1.status_code == 200
    ret = re.fullmatch(r"\{\'worker_id\'\: \d+\}", str(res1.json()))
    assert ret is not None

    # create_worker: wrong version
    clo_json_obj = deepcopy(json_obj)
    clo_json_obj["params"]["version"] = "0.0.0"
    res2 = client.post(
        "/worker/create", params={"authorize_key": AUTHORIZE_KEY}, json=clo_json_obj
    )
    assert res2.status_code == 400
    assert res2.json() == {"detail": f"Invalid version: 0.0.0, expected {__version__}"}

    # get_worker_info
    worker_id = res1.json()["worker_id"]
    res3 = client.get(f"/worker/{worker_id}", params={"authorize_key": AUTHORIZE_KEY})
    assert res3.status_code == 200
    assert res3.json()["id"] == res1.json()["worker_id"]
    assert res3.json()["params"] == json_obj["params"]

    # do job
    res5 = client.post(
        f"/worker/{worker_id}/do_job",
        params={"authorize_key": AUTHORIZE_KEY},
        data={"wm_str": "12345"},
    )
    assert res5.status_code == 200
    assert res5.json()["wm_text"] == "123456𝟳8𝟿𝟶𝟣"

    # redo job
    res6 = client.post(
        f"/worker/{res5.json()['worker_id']}/job/{res5.json()['job_id']}/redo",
        params={"authorize_key": AUTHORIZE_KEY},
    )
    assert res6.status_code == 200
    assert res6.json()["wm_text"] == "123456𝟳8𝟿𝟶𝟣"

    # get job info
    res7 = client.get(
        f"/worker/{res5.json()['worker_id']}/job/{res5.json()['job_id']}",
        params={"authorize_key": AUTHORIZE_KEY},
    )
    assert res7.status_code == 200
    assert res7.json()["wm_str"] == "12345"

    res8 = client.get(f"/worker/{res5.json()['worker_id']}/job/{res5.json()['job_id']}")
    assert res8.status_code == 401
    assert "Unauthorized" in res8.json()["detail"]


def test_main_use_job_id():
    """test main in use_job_id mode"""

    # create_worker: use_job_id
    clo_json_obj = deepcopy(json_obj)
    clo_json_obj["use_job_id"] = True
    clo_json_obj["text"] = "12345678"
    res1 = client.post(
        "/worker/create", params={"authorize_key": AUTHORIZE_KEY}, json=clo_json_obj
    )
    assert res1.status_code == 200
    ret = re.fullmatch(r"\{\'worker_id\'\: \d+\}", str(res1.json()))
    assert ret is not None

    # get_worker_info
    worker_id = res1.json()["worker_id"]
    # do job
    res5 = client.post(
        f"/worker/{worker_id}/do_job",
        params={"authorize_key": AUTHORIZE_KEY},
        data={"wm_str": "12345"},
    )
    assert res5.status_code == 200
    assert res5.json()["wm_text"] != "123456𝟳8𝟿𝟶𝟣"


def test_main_short_text_exception():
    """test main"""

    # not enough space
    clo_json_obj = deepcopy(json_obj)
    clo_json_obj["text"] = "12345678"
    res1 = client.post(
        "/worker/create", params={"authorize_key": AUTHORIZE_KEY}, json=clo_json_obj
    )
    assert res1.status_code == 400
    assert "Not enough space for watermark" in res1.json()["detail"]

    # raise TextWatermark exception
    clo_json_obj["use_job_id"] = True
    clo_json_obj["params"]["tpl_type"] = "FONT_COLOR"
    # # print(clo_json_obj)
    res2 = client.post(
        "/worker/create", params={"authorize_key": AUTHORIZE_KEY}, json=clo_json_obj
    )
    assert res2.status_code == 500
    assert "confusables_chars_key" in res2.json()["detail"]

    # do job, not enough space
    clo_json_obj["params"]["tpl_type"] = "HOMOGRAPH_NUMBERS"
    clo_json_obj["use_job_id"] = False
    clo_json_obj["text"] = "12345678901"
    res3 = client.post(
        "/worker/create", params={"authorize_key": AUTHORIZE_KEY}, json=clo_json_obj
    )
    worker_id = res3.json()["worker_id"]
    res5 = client.post(
        f"/worker/{worker_id}/do_job",
        params={"authorize_key": AUTHORIZE_KEY},
        data={"wm_str": "12345678901234567890"},
    )
    assert res5.status_code == 500
    assert "There is not enough space to insert a watermark:" in res5.json()["detail"]

    # if text is empty
    clo_json_obj["text"] = ""
    res6 = client.post(
        "/worker/create", params={"authorize_key": AUTHORIZE_KEY}, json=clo_json_obj
    )
    assert res6.status_code == 400
    assert "text is required for watermark" in res6.json()["detail"]


def test_some_not_found():
    """raise exception"""
    # get no exists worker
    res4 = client.get("/worker/9999999999", params={"authorize_key": AUTHORIZE_KEY})
    assert res4.status_code == 404
    assert res4.json() == {"detail": "Worker not found"}

    # do no exists worker job
    res5 = client.post(
        "/worker/9999999999/do_job",
        params={"authorize_key": AUTHORIZE_KEY},
        data={"wm_str": "12345"},
    )
    assert res5.status_code == 404
    assert res5.json() == {"detail": "Worker not found"}

    # redo no exists job
    res6 = client.post(
        "/worker/1/job/9999999999/redo", params={"authorize_key": AUTHORIZE_KEY}
    )
    assert res6.status_code == 404
    assert res6.json() == {"detail": "Job not found"}

    # get not exists job info
    res7 = client.get(
        "/worker/1/job/9999999999", params={"authorize_key": AUTHORIZE_KEY}
    )
    assert res7.status_code == 404
    assert res7.json() == {"detail": "Job not found"}


def test_main_docs():
    """get docs"""
    res = client.get("/docs")
    assert res.status_code == 200
