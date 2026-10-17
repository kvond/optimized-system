# Personal Hub provenance — October 12, 2026

The existing successful build is exactly the image currently deployed to Personal Hub API. Metadata-only reads confirm:

- Project/region: `graceful-fold-341018` / `us-east4`.
- Build: `ef6cf407-2dd8-4f76-bd96-2e0282d64656`, SUCCESS, finished September15 at17:47:35 UTC.
- Latest Ready revision: `personal-hub-api-00001-dkz`,100% traffic.
- Build result and revision image digest both equal `sha256:5afd2665237ee5c57eabe435bf8501ed629ac95b2aa01e4537b3e7719960e5d5`.
- Build source provenance identifies bucket `run-sources-graceful-fold-341018-us-east4`, object `services/personal-hub-api/1789494416.870631-f0bc309fd7d846788fb7203c3eff6c22.zip`, generation `1789494417056789`.

The inspected Personal-Hub checkout is commit `180e1174d232418f9fe6521297e053fae4d0e576`. The returned build provenance has no resolved repository/git source or commit linkage. Therefore **build-to-deployed-image equality is verified; inspected-commit-to-build equality is unverified**. Do not infer matching source code from matching service names or a Ready revision. The source ZIP was neither downloaded nor read. No signed URLs, secret reads, data reads, paid calls or cloud changes occurred.

The original reset cloud requirement is a plan or minimal implementation (Task10, success condition7). Existing inventory, staged orchestration plan and tested offline runtime satisfy the plan requirement. A deployed AI-ops service is not necessary to complete that original requirement. A future selected production pilot still needs authenticated source access, actual source/deployed-code linkage, durable transactional state and workflow/output receipt acceptance. These future gates should not be represented as required extra platform work for the original reset handoff.

Evidence commands: one filtered `gcloud builds describe`, filtered service and revision descriptions, and local `git rev-parse HEAD`. The machine-readable companion records exact sanitized metadata and limitations.
