# HTTP Quest – Test Checklist

This document outlines the test plan for the `http-quest` project, organized by component. Each test case ensures functional integrity and consistent behavior across models, logic, and state transitions.

---

## SQL Model: `Quest`
Testing for SQL Alchemy models are made with @validates and a custom validate(self) that is triggered by before insert and update.

| ID     |  | Test Description                                                                 |
|--------|--|-----------------------------------------------------------------------------------|
| QM-001 |[ ]| When quest is not stateless, `username_loc` must be specified                    |
| QM-002 |[x]| Quest must have at least `GET` as an allowed request method                      |
| QM-003 |[x]| Only `GET`, `POST`, `PUT`, `DELETE` are valid request methods                    |
| QM-004 |[x]| `execution_strategy` must be a valid `ExecutionStrategy` enum                    |
| QM-005 |[ ]| If not the first quest, a predecessor quest must be specified                    |
| QM-006 |[x]| If `solution` is set, `solution_key` and `solution_location` must also be set    |
| QM-007 |[x]| If `solution_key` is set, `solution` and `solution_location` must also be set    |
| QM-008 |[x]| If `solution_location` is set, `solution_key` and `solution` must also be set    |

---

## 🧩 SQL Model: `UserQuestState` (@validates in SQLAlchemy)

| ID     |  | Test Description                                                                 |
|--------|--|-----------------------------------------------------------------------------------|
| UQS-001 |[ ]| When all precessor quests are `CLOSED`, then the the state changes to `UNLOCKED`|
| UQS-002 |[ ]| While all precessor quests are not `CLOSED`, then the state is `LOCKED`|
| UQS-003 |[ ]| state value can only be a valid QuestState enum value.|

---

## Class: `QUEST PARSER`

| ID     |  | Test Description                                                                 |
|--------|--|-----------------------------------------------------------------------------------|
| QP-001 |[x]| parsed settings must include keys [`METHOD_DATA`, `AUTH_TYPE`, `QUERY_KEYS`, `ANSWER_KEY`, `ANSWER_LOC`]|
| QP-002 |[x]| all keys in parsed settings must be valid QuestKey enums.|

---

## Class: `REQUEST PARSER`

| ID     |  | Test Description                                                                 |
|--------|--|-----------------------------------------------------------------------------------|
| RP-001 |[x]| when request is parsed, then key ParserKey.METHOD_DATA is returned dict
| RP-001 |[x]| when request is parsed, then key ParserKey.PATH_DATA is returned dict
| RP-001 |[x]| when request is parsed, then key ParserKey.QUERY_DATA is returned dict
| RP-002 |[x]| when a data format has no data in request, then return empty dict in values
| RP-003 |[x]| all keys in parsed are valid ParserKey enums.

### fn: `parse_method`
| ID     |  | Test Description                                                                 |
|--------|--|-----------------------------------------------------------------------------------|
| RP_PM-001 |[x]| Get method from request|


### fn: `parse_query`
| ID     |  | Test Description                                                                 |
|--------|--|-----------------------------------------------------------------------------------|
| RP_PQ-001 |[x]| returns dict format if request has query |
| RP_PQ-002 |[x]| returns empty dict if not query |
| RP_PQ-003 |[x]| query data is stored with key == enum.QUERY_DATA       |

---

## class: `VALIDATOR`
| ID     |  | Test Description                                                                 |
|--------|--|-----------------------------------------------------------------------------------|
| VA-001 |[x]| When input is not dict[`REQUEST_KEYS`, dict] raise error                       |
| VA-002 |[ ]| When input keys does nots include [`METHOD`, `QUERY_DATA`], then raise error     |
| VA-003 |[x]| When settings keys is not valid, then raise error                    |
| VA-004 |[x]| When parsed keys is not valid, then raise error                    |


### fn: `validate_method`
| ID     |  | Test Description                                                                 |
|--------|--|-----------------------------------------------------------------------------------|
| VA_VM-001 |[x]|when method is not allowed by quest, then raise validation error               |
| VA_VM-002 |[x]| do nothing is method is allowed                                               |
| VA_VM-003 |[x]| when method is not in RequestMethodType enum, then raise error                 |


### fn: `validate_query`
| ID     |  | Test Description                                                                 |
|--------|--|-----------------------------------------------------------------------------------|
| VA_VQ-001 |[x]|when parsed[QUERY_DATA] is empty but quest expect keys, then raise error   |
| VA_VQ-002|[x]| when keys in parsed[QUERY_DATA] is not the same as expected query keys by quest, then raise error |

---

## class: `AUTHENTICATOR`

| ID     |  | Test Description                                                                 |
|--------|--|-----------------------------------------------------------------------------------|
| VA-001 |[]|                                                                       |


### fn: `get_identity`

| ID     |  | Test Description                                                                 |
|--------|--|-----------------------------------------------------------------------------------|
| AU_GI-001 |[x]| when settings has key QuestKey.USERNAME_LOCATION, then data has not-empty value in expected location|
| AU_GI-001 |[x]| when settings expects username but its is missing from data, then raise error     |
| AU_GI-002 |[x]| when quest has not username_loc, then username is empty in identity       |


### fn: `authenticate`
| ID     |  | Test Description                                                                 |
|--------|--|-----------------------------------------------------------------------------------|
| AU_AU-001 |[x]| when quest has no authentication and no user, then return True, None          |
| AU_AU-001 |[x]| when quest has no authentication and user, then return True, temp_user with username only |



---


## class: `STATE MANAGER`
| ID     |  | Test Description                                                                 |
|--------|--|-----------------------------------------------------------------------------------|
| SM-001 |[x]| when quest is stateless, then start state COMPLETED                              |
| SM-001 |[ ]| when quest has state, and user has not reached the quest, then the state is LOCKED                     |
| SM-001 |[ ]| when the quest has state, and the user has reached the quest, then the initial state is UNLOCKED    |
| SM-001 |[ ]| when the quest has state and is UNLOCKED, when the user completes the quest, the state changes to COMPLETED  |
| SM-001 |[ ]| when the quest has state and is UNLOCKED, when the user fails the quest, the state changes to FAILED.     |
| SM-001 |[ ]| when the quest has state and is COMPLETED, then the end state is CLOSED.      |
| SM-001 |[ ]| when the quest has state and is FAILED, then the end state is reset to UNLOCKED.   |
| SM-001 |[x]| when state is not a valid value, then raises an error.     |

---

## class: `GAME MANAGER`
| ID     |  | Test Description                                                                 |
|--------|--|-----------------------------------------------------------------------------------|
| GM-001 |[ ]| When a stateless quest begins, the initial state is COMPLETED    |


### fn: `get_response`
| ID     |  | Test Description                                                                 |
|--------|--|-----------------------------------------------------------------------------------|
| GM_GR-001 |[ ]| When quest state is LOCKED, then return LOCKED response                   |
| GM_GR-002 |[ ]| When quest state is CLOSED, then return CLOSED response       |
| GM_GR-003 |[ ]| When quest state is COMPLETED, then return COMPLETED response       |
| GM_GR-004 |[ ]| When quest state is FAILED, then return FAILED response       |
| GM_GR-005 |[ ]| When quest state is UNLOCKED, then return BASE response       |


### fn: `execute`
| ID     |  | Test Description                                                                 |
|--------|--|-----------------------------------------------------------------------------------|
| GM_EX-001 |[ ]| When state is UNLOCKED and request method is valid action method, then quest execution runs   |
| GM_EX-002 |[ ]| When state is not UNLOCKED, then quest execution is skipped   |
| GM_EX-003 |[ ]| when quest execution runs, then state always changes  |



---

## class: `REQUEST MANAGER` (INTEGRATION TEST)
| ID     |  | Test Description                                                                 |
|--------|--|-----------------------------------------------------------------------------------|
| RM-001 |[ ]| When a request parsing fails, then return error to requester with bad request code   |
| RM-002 |[ ]| When a request parses successfully, pass it on to validation |
| RM-003 |[ ]| when a validation fails, then return the error to the request with bad request code  |
| RM-004 |[ ]| When a parsed request is validated, then pass it on to authentication    |
| RM-005 |[ ]| when an authentication fails, then return the error to the requester with bad request code   |
| RM-006 |[ ]| When an authentication passes, then build context for the game manager   |
| RM-007 |[ ]| When the game manager runs successfully, then return the response to the request with ok request code    |
| RM-008 |[ ]| When the game manager fails, return the error message to the request with game error code    |
| RM-009 |[ ]| When the game manager runs successfully, if the quest has state, update state in db  |
| RM-010 |[ ]| When the game manager runs successfully, if the quest is stateless, do nothing   |
| RM-011 |[ ]| When a response is sent to the request, if the requester is registered, store request in db as latest response   |

## utils: `get_clean_list_from_string`
| ID     |  | Test Description                                                                 |
|--------|--|-----------------------------------------------------------------------------------|
| UT_LS-001 |[x]| When string is empty, then return empty list obj  |
| UT_LS-002 |[x]| When string has empty fields between separators, then they are removed  |
| UT_LS-003 |[x]| When a value is not ' ', then it is its own value

## utils: `get_enum_values_as_list`
| ID     |  | Test Description                                                                 |
|--------|--|-----------------------------------------------------------------------------------|
| UT_EL-001 |[x]| When enum is empty, then return empty list obj  |
| UT_EL-002 |[x]| All values in Enum are returned as list