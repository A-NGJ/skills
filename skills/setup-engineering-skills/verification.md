# Verification

The commands implementation specialists and reviewers run to check a change. Run each in the foreground and wait for it to exit.

## Targeted

How to run the tests for one file, module, or test name while editing:

```sh
<targeted test command, e.g. pytest path/to/test_file.py -k name>
```

## Full suite

Run once before the final `done`, after any change to shared infrastructure or test fixtures, and once per reviewed head.

```sh
<full suite command>
```

Expected duration: <minutes>. Set the shell timeout above this rather than backgrounding the run.

## Static checks

```sh
<lint / type-check / format-check commands, or remove this section>
```

## Environment and gotchas

<Required services, env vars, credentials, fixtures that are slow or interfere when run in parallel, tests known to be flaky. Remove this section when there are none.>
