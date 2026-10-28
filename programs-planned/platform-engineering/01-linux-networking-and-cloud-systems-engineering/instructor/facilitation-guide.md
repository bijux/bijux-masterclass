# Facilitation Guide

Teach from the course book. The implementation is used to falsify and verify the chapter model, not to replace explanation.

## Before the cohort

- run core proof, tour, systemd proof, and available environment-backed labs;
- prepare one disposable VM per learner or pair;
- confirm console recovery before firewall work;
- generate fresh local fixture certificates if the cohort will practice rotation;
- establish cloud budget, account boundary, and deletion audit for optional Class D work;
- select planted defects but do not reveal their identifiers in advance.

## During a lab

Ask learners to state a hypothesis and first oracle before commands. When they reach for a broad repair—root, `chmod 777`, `curl -k`, firewall flush, unbounded retry—pause and ask which earlier guarantee would be lost.

Do not rescue an investigation by naming the command. Ask which owner and state transition the learner needs to observe. Permit reference lookup after the causal question is stated.

## Review

Require raw evidence plus interpretation. A screenshot of a green command is insufficient. Check cleanup personally for privileged and cloud labs. Preserve failed attempts when they reveal a useful misconception.
