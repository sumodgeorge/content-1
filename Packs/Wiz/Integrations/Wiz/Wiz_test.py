import pytest
from unittest.mock import patch
import demistomock as demisto

integration_params = {
    'url': 'http://test.io',
    'credentials': {'identifier': 'test', 'password': 'pass'},
    'fetch_time': '7 days',
}


@pytest.fixture(autouse=True)
def set_mocks(mocker):
    mocker.patch.object(demisto, 'params', return_value=integration_params)


test_get_filtered_issues_response = {
    "data": {
        "issues": {
            "nodes": [
                {
                    "id": "12345678-1234-1234-1234-d25e16359c19",
                    "control": {
                        "id": "12345678-4321-4321-4321-3792e8a03318",
                        "name": "test delete",
                    },
                    "createdAt": "2022-01-02T15:46:34Z",
                    "updatedAt": "2022-01-04T10:40:57Z",
                    "status": "OPEN",
                    "severity": "CRITICAL",
                    "entity": {
                        "bla": "lot more blah was here",
                        "name": "virtualMachine",
                        "type": "virtualMachine"
                    }
                }
            ],
            "pageInfo": {
                "hasNextPage": False,
                "endCursor": ""
            }
        }
    }
}


@patch('Wiz.checkAPIerrors', return_value=test_get_filtered_issues_response)
def test_get_filtered_issues(checkAPIerrors):
    from Wiz import get_filtered_issues

    result_response = [
        {
            "id": "12345678-1234-1234-1234-d25e16359c19",
            "control": {
                "id": "12345678-4321-4321-4321-3792e8a03318",
                "name": "test delete",
            },
            "createdAt": "2022-01-02T15:46:34Z",
            "updatedAt": "2022-01-04T10:40:57Z",
            "status": "OPEN",
            "severity": "CRITICAL",
            "entity": {
                "bla": "lot more blah was here",
                "name": "virtualMachine",
                "type": "virtualMachine"
            }
        }
    ]

    res = get_filtered_issues('virtualMachine', '', 'CRITICAL', 500)
    assert res == result_response


test_get_resource_response = {
    "data": {
        "graphSearch": {
            "totalCount": 1,
            "maxCountReached": False,
            "pageInfo": {
                "endCursor": "1",
                "hasNextPage": False,
                "__typename": "PageInfo"
            },
            "nodes": [
                {
                    "entities": [
                        {
                            "id": "12345678-2222-3333-1111-ff5fa2ff7f78",
                            "name": "i_am_an_id",
                            "type": "VIRTUAL_MACHINE",
                            "properties": {
                                "blah": "lots_of_blah_here"
                            }
                        }
                    ]
                }
            ]
        }
    }
}


@patch('Wiz.checkAPIerrors', return_value=test_get_resource_response)
def test_get_resource(checkAPIerrors):
    from Wiz import get_resource
    result_response = {
        "id": "12345678-2222-3333-1111-ff5fa2ff7f78",
        "name": "i_am_an_id",
        "type": "VIRTUAL_MACHINE",
        "properties": {
            "blah": "lots_of_blah_here"
        }
    }

    res = get_resource('i_am_an_id')
    assert res == result_response


test_reject_issue_response = {
    "data": {
        "updateIssue": {
            "issue": {
                "id": "12345678-2222-3333-1111-ff5fa2ff7f78",
                "note": "blah_note",
                "status": "REJECTED",
                "dueAt": "2022-01-14T20:24:20Z",
                "resolutionReason": "WONT_FIX"
            }
        }
    }
}


@patch('Wiz.checkAPIerrors', return_value=test_reject_issue_response)
def test_reject_issue(checkAPIerrors):
    from Wiz import reject_issue

    res = reject_issue('12345678-2222-3333-1111-ff5fa2ff7f78', 'WONT_FIX', 'blah_note')
    assert res == test_reject_issue_response


test_reject_issue_fail_response = {
    "errors": [
        {
            "message": "Resource not found",
            "extensions": {
                "code": "NOT_FOUND",
                "exception": {
                    "message": "Resource not found",
                    "path": [
                        "issue"
                    ]
                }
            }
        }
    ],
    "data": None
}


@patch('Wiz.checkAPIerrors', return_value=test_reject_issue_fail_response)
def test_reject_issue_failed(checkAPIerrors, capfd):
    with capfd.disabled():
        from Wiz import reject_issue

        res = reject_issue('12345678-2222-3333-1111-ff5fa2ff7f78', 'WONT_FIX', 'blah_note')
        assert res == ("Could not find Issue with ID 12345678-2222-3333-1111-ff5fa2ff7f78")


test_reopen_issue_response = {
    "data": {
        "updateIssue": {
            "issue": {
                "id": "12345678-2222-3333-1111-ff5fa2ff7f78",
                "note": "blah_note",
                "status": "OPEN",
                "dueAt": "2022-01-14T20:24:20Z",
                "resolutionReason": ""
            }
        }
    }
}


@patch('Wiz.checkAPIerrors', return_value=test_reopen_issue_response)
def test_reopen_issue(checkAPIerrors):
    from Wiz import reopen_issue

    res = reopen_issue('12345678-2222-3333-1111-ff5fa2ff7f78', 'blah_note')
    assert res == test_reopen_issue_response


test_set_issue_reopen_fail_response = {
    "errors": [
        {
            "message": "Resource not found",
            "extensions": {
                "code": "NOT_FOUND",
                "exception": {
                    "message": "Resource not found",
                    "path": [
                        "issue"
                    ]
                }
            }
        }
    ],
    "data": None
}


@patch('Wiz.checkAPIerrors', return_value=test_set_issue_reopen_fail_response)
def test_set_issue_reopen_failed(checkAPIerrors, capfd):
    with capfd.disabled():
        from Wiz import reopen_issue

        res = reopen_issue('12345678-2222-3333-1111-ff5fa2ff7f78', 'blah_note')
        assert res == ("Could not find Issue with ID 12345678-2222-3333-1111-ff5fa2ff7f78")


test_issue_in_progress_response = {
    "data": {
        "updateIssue": {
            "issue": {
                "id": "12345678-2222-3333-1111-ff5fa2ff7f78",
                "note": "blah_note",
                "status": "IN_PROGRESS",
                "dueAt": "2022-01-14T20:24:20Z",
                "resolutionReason": ""
            }
        }
    }
}


@patch('Wiz.checkAPIerrors', return_value=test_issue_in_progress_response)
def test_issue_in_progress(checkAPIerrors):
    from Wiz import issue_in_progress

    res = issue_in_progress('12345678-2222-3333-1111-ff5fa2ff7f78')
    assert res == test_issue_in_progress_response


test_set_issue_in_progress_fail_response = {
    "errors": [
        {
            "message": "Resource not found",
            "extensions": {
                "code": "NOT_FOUND",
                "exception": {
                    "message": "Resource not found",
                    "path": [
                        "issue"
                    ]
                }
            }
        }
    ],
    "data": None
}


@patch('Wiz.checkAPIerrors', return_value=test_set_issue_in_progress_fail_response)
def test_set_issue_in_progress_failed(checkAPIerrors, capfd):
    with capfd.disabled():
        from Wiz import issue_in_progress

        res = issue_in_progress('12345678-2222-3333-1111-ff5fa2ff7f78')
        assert res == ("Could not find Issue with ID 12345678-2222-3333-1111-ff5fa2ff7f78")


test_set_issue_note_response = {
    "data": {
        "issue": {
            "id": "12345678-1234-1234-1234-d25e16359c19",
            "control": {
                "id": "12345678-4321-4321-4321-3792e8a03318",
                "name": "test delete",
            },
            "createdAt": "2022-01-02T15:46:34Z",
            "updatedAt": "2022-01-04T10:40:57Z",
            "status": "OPEN",
            "note": "blah note",
            "severity": "CRITICAL",
            "entity": {
                "bla": "lot more blah was here",
                "name": "virtualMachine",
                "type": "virtualMachine"
            }
        }
    }
}


@patch('Wiz.checkAPIerrors', return_value=test_set_issue_note_response)
def test_set_issue_note(checkAPIerrors):
    from Wiz import set_issue_note

    res = set_issue_note('12345678-2222-3333-1111-ff5fa2ff7f78', 'blah_note')
    assert res == test_set_issue_note_response


test_set_issue_note_fail_response = {
    "errors": [
        {
            "message": "Resource not found",
            "extensions": {
                "code": "NOT_FOUND",
                "exception": {
                    "message": "Resource not found",
                    "path": [
                        "issue"
                    ]
                }
            }
        }
    ],
    "data": None
}


@patch('Wiz.checkAPIerrors', return_value=test_set_issue_note_fail_response)
def test_set_issue_note_failed(checkAPIerrors, capfd):
    with capfd.disabled():
        from Wiz import set_issue_note

        res = set_issue_note('12345678-2222-3333-1111-ff5fa2ff7f78', "blah")
        assert res == ("Could not find Issue with ID 12345678-2222-3333-1111-ff5fa2ff7f78")


test_clear_issue_note_response = {
    "data": {
        "updateIssue": {
            "issue": {
                "id": "12345678-2222-3333-1111-ff5fa2ff7f78",
                "note": "",
                "status": "REJECTED",
                "dueAt": "2022-01-14T20:24:20Z",
                "resolutionReason": "WONT_FIX"
            }
        }
    }
}


@patch('Wiz.checkAPIerrors', return_value=test_clear_issue_note_response)
def test_clear_issue_note(checkAPIerrors):
    from Wiz import clear_issue_note

    res = clear_issue_note('12345678-2222-3333-1111-ff5fa2ff7f78')
    assert res == test_clear_issue_note_response


test_clear_issue_note_fail_response = {
    "errors": [
        {
            "message": "Resource not found",
            "extensions": {
                "code": "NOT_FOUND",
                "exception": {
                    "message": "Resource not found",
                    "path": [
                        "issue"
                    ]
                }
            }
        }
    ],
    "data": None
}


@patch('Wiz.checkAPIerrors', return_value=test_clear_issue_note_fail_response)
def test_clear_issue_note_failed(checkAPIerrors, capfd):
    with capfd.disabled():
        from Wiz import clear_issue_note

        res = clear_issue_note('12345678-2222-3333-1111-ff5fa2ff7f78')
        assert res == ("Could not find Issue with ID 12345678-2222-3333-1111-ff5fa2ff7f78")


test_get_issue_evidence_fail_response = {
    "errors": [
        {
            "message": "Resource not found",
            "extensions": {
                "code": "NOT_FOUND",
                "exception": {
                    "message": "Resource not found",
                    "path": [
                        "issue"
                    ]
                }
            }
        }
    ],
    "data": {
        "issue": None,
        "issueSettings": {
            "requireNoteOnRejection": True
        }
    }
}


@patch('Wiz.checkAPIerrors', return_value=test_get_issue_evidence_fail_response)
def test_get_issue_evidence_failure(checkAPIerrors, capfd):
    with capfd.disabled():
        from Wiz import get_issue_evidence

        res = get_issue_evidence('12345678-1234-1234-1234-d25e16359c19')
        assert res == ("Could not find Issue with ID 12345678-1234-1234-1234-d25e16359c19")


test_set_issue_due_data_response = {
    "data": {
        "updateIssue": {
            "issue": {
                "id": "12345678-2222-3333-1111-ff5fa2ff7f78",
                "note": "",
                "status": "OPEN",
                "dueAt": "2022-01-20T00:00:00.000Z",
                "resolutionReason": None
            }
        }
    }
}


@patch('Wiz.checkAPIerrors', return_value=test_set_issue_due_data_response)
def test_set_issue_due_date(checkAPIerrors):
    from Wiz import set_issue_due_date

    res = set_issue_due_date('12345678-2222-3333-1111-ff5fa2ff7f78', '2022-01-20')
    assert res == test_set_issue_due_data_response


@patch('Wiz.checkAPIerrors', return_value="The date format is the incorrect. It should be YYYY-MM-DD")
def test_set_issue_due_date_failed(checkAPIerrors, capfd):
    with capfd.disabled():
        from Wiz import set_issue_due_date

        res = set_issue_due_date('12345678-2222-3333-1111-ff5fa2ff7f78', '01-20-2022')
        assert res == "The date format is the incorrect. It should be YYYY-MM-DD"


test_clear_issue_due_data_response = {
    "data": {
        "issue": {
            "id": "12345678-2222-3333-1111-ff5fa2ff7f78",
            "note": "",
            "status": "OPEN",
            "dueAt": None,
            "resolutionReason": None
        }
    }
}


@patch('Wiz.checkAPIerrors', return_value=test_clear_issue_due_data_response)
def test_clear_issue_due_date(checkAPIerrors):
    from Wiz import clear_issue_due_date

    res = clear_issue_due_date('12345678-2222-3333-1111-ff5fa2ff7f78')
    assert res == test_clear_issue_due_data_response


test_clear_issue_due_data_failed_response = {
    "errors": [
        {
            "message": "Resource not found",
            "extensions": {
                "code": "NOT_FOUND",
                "exception": {
                    "message": "Resource not found",
                    "path": [
                        "updateIssue"
                    ]
                }
            }
        }
    ],
    "data": None
}


@patch('Wiz.checkAPIerrors', return_value=test_clear_issue_due_data_failed_response)
def test_clear_issue_due_date_no_issue_id(checkAPIerrors, capfd):
    with capfd.disabled():
        from Wiz import clear_issue_due_date

        res = clear_issue_due_date('12345678-2222-3333-1111-ff5fa2ff7f71')
        assert res == "Could not find Issue with ID 12345678-2222-3333-1111-ff5fa2ff7f71"


test_bad_token_repsonse = {
    "error": "access_denied",
    "error_description": "Unauthorized"
}


def test_bad_get_token(capfd):
    with capfd.disabled():
        with patch('requests.post') as mocked_request:
            with pytest.raises(Exception):
                mocked_request().return_value = test_bad_token_repsonse
                from Wiz import get_token

                res = get_token()
                assert res == test_bad_token_repsonse


test_issue_severity_crit_response = {
    "id": "12345678-2222-3333-1111-ff5fa2ff7f71",
    "note": "",
    "severity": "CRITICAL",
    "status": "OPEN",
    "dueAt": None,
    "resolutionReason": None
}


def test_translate_severity_crit(capfd):
    with capfd.disabled():
        from Wiz import translate_severity

        res = translate_severity(test_issue_severity_crit_response)
        assert res == 4


test_issue_severity_high_response = {
    "id": "12345678-2222-3333-1111-ff5fa2ff7f71",
    "note": "",
    "severity": "HIGH",
    "status": "OPEN",
    "dueAt": None,
    "resolutionReason": None
}


def test_translate_severity_high(capfd):
    with capfd.disabled():
        from Wiz import translate_severity

        res = translate_severity(test_issue_severity_high_response)
        assert res == 3


test_issue_severity_med_response = {
    "id": "12345678-2222-3333-1111-ff5fa2ff7f71",
    "note": "",
    "severity": "MEDIUM",
    "status": "OPEN",
    "dueAt": None,
    "resolutionReason": None
}


def test_translate_severity_med(capfd):
    with capfd.disabled():
        from Wiz import translate_severity

        res = translate_severity(test_issue_severity_med_response)
        assert res == 2


test_issue_severity_low_response = {
    "id": "12345678-2222-3333-1111-ff5fa2ff7f71",
    "note": "",
    "severity": "LOW",
    "status": "OPEN",
    "dueAt": None,
    "resolutionReason": None
}


def test_translate_severity_low(capfd):
    with capfd.disabled():
        from Wiz import translate_severity

        res = translate_severity(test_issue_severity_low_response)
        assert res == 1


test_issue_severity_info_response = {
    "id": "12345678-2222-3333-1111-ff5fa2ff7f71",
    "note": "",
    "severity": "INFORMATIONAL",
    "status": "OPEN",
    "dueAt": None,
    "resolutionReason": None
}


def test_translate_severity_info(capfd):
    with capfd.disabled():
        from Wiz import translate_severity

        res = translate_severity(test_issue_severity_info_response)
        assert res == 0.5


test_build_incidents_response = None


def test_build_incidents_none(capfd):
    with capfd.disabled():
        from Wiz import build_incidents

        res = build_incidents(test_build_incidents_response)
        assert res == {}
