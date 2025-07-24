# HTTP QUEST TEST CHECKLIST

## SQL Model: QUEST (@validates in sql alchemy)

| ID       | Test Description                                                                 |
|----------|-----------------------------------------------------------------------------------|
| QM-001   | When quest is not stateless, `username_loc` must be specified                    |
| QM-002   | Quest must have at least `GET` as an allowed request method                      |
| QM-003   | Only `GET`, `POST`, `PUT`, `DELETE` are valid request methods                    |
| QM-004   | `execution_strategy` must be a valid `ExecutionStrategy` enum                    |
| QM-005   | If not the first quest, a predecessor quest must be specified                    |
| QM-006   | If `solution` is set, `solution_key` and `solution_location` must also be set    |
| QM-007   | If `solution_key` is set, `solution` and `solution_location` must also be set    |
| QM-008   | If `solution_location` is set, `solution_key` and `solution` must also be set    |

---


- [ ] when quest is not stateless, then quest request settings specifies expected username location
- [x] quest must have at least GET as expected method
- [x] expected methods only takes GET, POST, PUT, and DELETE
- [ ] execution_strategy must be valid ExecutionStrategy enum
- [ ] when quest is not the first, it must specify its precessor
- [ ] when quest has a "solution" value, then it also has "solution_key" and "solution_location" values
- [ ] when quest has a "solution_key" values, then it also has "solution" and "solution_location" values
- [ ] when quest has a "solution_location" values, then it also has "solution_key" and "solution" values

## SQL Model: USER QUEST STATE (@validates in sql alchemy)
- [ ] When all precessor quests are CLOSED, then the the state changes to UNLOCKED
- [ ] While all precessor quests are not CLOSED, then the state is LOCKED
- [ ] state value can only be a valid QuestState enum value.

## Class: QUEST PARSER
- [ ] parsed settings must include keys [METHOD_DATA, QUERY_KEYS, AUTH_TYPE]
- [ ] all keys in parsed settings must be valid ParserKey enums.

## Class: REQUEST PARSER
- [ ] when request is parsed, returns a dict[FORMAT_DATA_KEY, dict_data] with all supported formats
- [ ] when a data format has no data in request, then return empty dict in values
- [ ] all keys in parsed are valid ParserKey enums.
### fn: parse_method
- [x] Get method from request
### fn: parse_query
- [x] returns dict format if request has query
- [ ] returns empty dict if not query
- [ ] query data is stored with key == enum.QUERY_DATA

## class: VALIDATOR
- [ ] When input is not dict[REQUEST_KEYS, dict] raise error
- [ ] When input keys does nots include [METHOD, QUERY_DATA], then raise error
### fn: validate_method
- [x] when method is not allowed by quest, then raise validation error
- [x] do nothing is method is allowed
- [ ] when method is not GET, POST, PUT or DELETE, then raise error
### fn: validate_query
- [x] if parsed[QUERY_DATA] is empty but quest expect keys, then raise error
- [x] if keys in parsed[QUERY_DATA] is not the same as expected query keys by quest, then raise error

## class: AUTHENTICATOR
### fn: get_identity
- [ ] when quest has username_loc, then username is in identity 
- [ ] when quest has not username_loc, then username is empty in identity

### fn: authenticate
- [ ] if quest has no authentication, then return True

## class: STATE MANAGER
- [ ] when quest is stateless, then start state COMPLETED 
- [ ] when quest has no authentication, then start state is UNLOCKED 
- [ ] when quest has state, and user has not reached the quest, then the state is LOCKED
- [ ] when the quest has state, and the user has reached the quest, then the initial state is UNLOCKED
- [ ] when the quest has state and is UNLOCKED, when the user completes the quest, the state changes to COMPLETED
- [ ] when the quest has state and is UNLOCKED, when the user fails the quest, the state changes to FAILED
- [ ] when the quest has state and is COMPLETED, then the end state is CLOSED
- [ ] when the quest has state and is FAILED, then the end state is reset to UNLOCKED
- [ ] when state is not a valid QuestState enum, then State Manager raises an error

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