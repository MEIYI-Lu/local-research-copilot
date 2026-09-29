# Feature Flags

Feature flags decouple deploying code from exposing behaviour to every user. A team can merge and deploy an unfinished or experimental path behind a flag, then enable it for internal users, a percentage of traffic, or a selected cohort.

Flags support gradual rollout and fast disablement, but stale flags create complexity. Mature flag systems therefore track ownership and remove temporary flags after a rollout is complete. A feature flag is a runtime decision mechanism, not a replacement for source control.
