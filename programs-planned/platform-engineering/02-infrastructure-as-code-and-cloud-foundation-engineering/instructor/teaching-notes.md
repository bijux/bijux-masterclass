# Instructor Notes

## Teaching posture

Do not begin a module with provider resource syntax. Begin with the failure or
ownership problem, let learners predict the evidence, then introduce HCL as one
implementation of the decision.

## Productive friction

Ask learners to defend:

- why a resource belongs in one state rather than another;
- what a plan cannot know;
- who may read and who may mutate;
- which path a packet or credential follows;
- what is lost during replacement;
- why a successful apply can still be a failed release.

## Avoid

- live console demonstrations without a reproducible transcript;
- presenting the AWS diagram as evidence;
- awarding credit for copying a module interface;
- treating all plan differences as drift;
- giving learners organization-management credentials;
- turning the optional AWS lane into a race to create resources.

The most important instructor task is to preserve the distinction between
semantic evidence, local mechanism evidence, and actual cloud evidence.
