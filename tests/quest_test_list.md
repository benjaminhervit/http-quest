# Quest Test Checklist

This document outlines the test plan for the quests in the `HTTP reQuest` game.
These tests are separated from the other tests as they are not purely game play related.

---

## Quest 1: `Welcome`
Testing for SQL Alchemy models are made with @validates and a custom validate(self) that is triggered by before insert and update.

| ID     |  | Test Description                                                                 |
|--------|--|-----------------------------------------------------------------------------------|
|Q1-001  |[x]| is stateless            |
|Q1-001  |[x]| only accepts GET            |
|Q1-001  |[]| Auto completes                        |
|Q1-001  |[]| Expects no username            |
|Q1-001  |[x]| Expects no authorization            |
|Q1-001  |[x]| Only expects method data and auth_type          |
|Q1-001  |[ ]| accessed by path 'game/welcome'      |