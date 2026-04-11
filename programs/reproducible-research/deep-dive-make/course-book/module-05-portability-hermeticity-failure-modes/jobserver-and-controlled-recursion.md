# Jobserver and Controlled Recursion

This lesson will explain when recursive Make is acceptable, how GNU Make's jobserver
budget propagates, and how to keep sub-makes observable instead of mysterious. The final
version will keep the focus on bounded recursion rather than folklore about `-j`.
