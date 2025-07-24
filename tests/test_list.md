# ✅ HTTP Quest – Test Checklist

This document outlines the test plan for the `http-quest` project, organized by component. Each test case ensures functional integrity and consistent behavior across models, logic, and state transitions.

---

## 🧩 SQL Model: `Quest` (@validates in SQLAlchemy)

| ID     |  | Test Description                                                                 |
|--------|--|-----------------------------------------------------------------------------------|
| QM-001 |[ ]| When quest is not stateless, `username_loc` must be specified                    |
| QM-002 |[ ]| Quest must have at least `GET` as an allowed request method                      |
| QM-003 |[ ]| Only `GET`, `POST`, `PUT`, `DELETE` are valid request methods                    |
| QM-004 |[ ]| `execution_strategy` must be a valid `ExecutionStrategy` enum                    |
| QM-005 |[ ]| If not the first quest, a predecessor quest must be specified                    |
| QM-006 |[ ]| If `solution` is set, `solution_key` and `solution_location` must also be set    |
| QM-007 |[ ]| If `solution_key` is set, `solution` and `solution_location` must also be set    |
| QM-008 |[ ]| If `solution_location` is set, `solution_key` and `solution` must also be set    |

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
| QP-001 |[ ]| parsed settings must include keys [`METHOD_DATA`, `QUERY_KEYS`, `AUTH_TYPE`]|
| QP-002 |[ ]| all keys in parsed settings must be valid ParserKey enums.|

---

## Class: `REQUEST PARSER`

| ID     |  | Test Description                                                                 |
|--------|--|-----------------------------------------------------------------------------------|
| RP-001 |[ ]| when request is parsed, returns a dict[`FORMAT_DATA_KEY`, dict_data] with all supported formats
| RP-002 |[ ]| when a data format has no data in request, then return empty dict in values
| RP-003 |[ ]| all keys in parsed are valid ParserKey enums.

### fn: `parse_method`
| ID     |  | Test Description                                                                 |
|--------|--|-----------------------------------------------------------------------------------|
| RP_PM-001 |[x]| Get method from request|


### fn: `parse_query`
| ID     |  | Test Description                                                                 |
|--------|--|-----------------------------------------------------------------------------------|
| RP_PQ-001 |[x]| returns dict format if request has query |
| RP_PQ-002 |[ ]| returns empty dict if not query |
| RP_PQ-003 |[ ]| query data is stored with key == enum.QUERY_DATA       |

---

## class: `VALIDATOR`
| ID     |  | Test Description                                                                 |
|--------|--|-----------------------------------------------------------------------------------|
| VA-001 |[x]| When input is not dict[`REQUEST_KEYS`, dict] raise error                       |
| VA-002 |[ ]| When input keys does nots include [`METHOD`, `QUERY_DATA`], then raise error     |


### fn: `validate_method`
| ID     |  | Test Description                                                                 |
|--------|--|-----------------------------------------------------------------------------------|
| VA_VM-001 |[x]|when method is not allowed by quest, then raise validation error               |
| VA_VM-002 |[x]| do nothing is method is allowed                                               |
| VA_VM-003 |[ ]| when method is not `GET`, `POST`, `PUT` or `DELETE`, then raise error                 |


### fn: `validate_query`
| ID     |  | Test Description                                                                 |
|--------|--|-----------------------------------------------------------------------------------|
| VA_VQ-001 |[x]|when parsed[QUERY_DATA] is empty but quest expect keys, then raise error   |
| VA_VQ-002|[x]| when keys in parsed[QUERY_DATA] is not the same as expected query keys by quest, then raise error |

---

## class: `AUTHENTICATOR`

### fn: `get_identity`

| ID     |  | Test Description                                                                 |
|--------|--|-----------------------------------------------------------------------------------|
| AU_GI-001 |[ ]| when quest has username_loc, then username is in identity                 |
| AU_GI-002 |[ ]| when quest has not username_loc, then username is empty in identity       |


### fn: `authenticate`
| ID     |  | Test Description                                                                 |
|--------|--|-----------------------------------------------------------------------------------|
| AU_AU-001 |[ ]| when quest has no authentication, then return True                |

---


## class: `STATE MANAGER`
| ID     |  | Test Description                                                                 |
|--------|--|-----------------------------------------------------------------------------------|
| SM-001 |[ ]| when quest is stateless, then start state COMPLETED                              |
| SM-001 |[ ]| when quest has no authentication, then start state is UNLOCKED                      |
| SM-001 |[ ]| when quest has state, and user has not reached the quest, then the state is LOCKED                     |
| SM-001 |[ ]| when the quest has state, and the user has reached the quest, then the initial state is UNLOCKED    |
| SM-001 |[ ]| when the quest has state and is UNLOCKED, when the user completes the quest, the state changes to COMPLETED  |
| SM-001 |[ ]| when the quest has state and is UNLOCKED, when the user fails the quest, the state changes to FAILED.     |
| SM-001 |[ ]| when the quest has state and is COMPLETED, then the end state is CLOSED.      |
| SM-001 |[ ]| when the quest has state and is FAILED, then the end state is reset to UNLOCKED.   |
| SM-001 |[ ]| when state is not a valid QuestState enum, then State Manager raises an error.     |


## class: GAME MANAGER
- [ ] When a stateless quest begins, the initial state is COMPLETED

### fn: get_response
- [ ] When quest state is LOCKED, then return LOCKED response
- [ ] When quest state is CLOSED, then return CLOSED response
- [ ] When quest state is COMPLETED, then return COMPLETED response
- [ ] When quest state is FAILED, then return FAILED response
- [ ] When quest state is UNLOCKED, then return BASE response

### fn: execute
- [ ] When state is UNLOCKED and request method is valid action method, then quest execution runs
- [ ] When state is not UNLOCKED, then quest execution is skipped
- [ ] when quest execution runs, then state always changes

## class: REQUEST MANAGER (INTEGRATION TEST)
- [ ] When a request parsing fails, then return error to requester with bad request code
- [ ] When a request parses successfully, pass it on to validation
- [ ] when a validation fails, then return the error to the request with bad request code
- [ ] When a parsed request is validated, then pass it on to authentication
- [ ] when an authentication fails, then return the error to the requester with bad request code
- [ ] When an authentication passes, then build context for the game manager
- [ ] When the game manager runs successfully, then return the response to the request with ok request code
- [ ] When the game manager fails, return the error message to the request with game error code
- [ ] When the game manager runs successfully, if the quest has state, update state in db
- [ ] When the game manager runs successfully, if the quest is stateless, do nothing
- [ ] When a response is sent to the request, if the requester is registered, store request in db as latest response