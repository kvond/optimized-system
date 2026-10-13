# Reset hard stop

Absolute cutoff: 2026-10-12T10:00:00Z = October 12, 2026 6:00 AM America/New_York. No reset-specific recurring automation is created. Finish and stop all task-owned work before cutoff; do not kill existing school/other user infrastructure.

Use runtime/reset_guard.py for every reset child operation. It rejects starts after cutoff and runs owned process groups with reserved shutdown time. Process-group denial or escaped children are explicitly unverified and block further dispatch. No cloud/provider background execution is launched tonight. This guard cannot terminate the app's interactive model turn; parent must stop issuing tools before cutoff. No autonomous continuation is scheduled.

Checkpoint reports/status before stopping. Track pending remote calls, wait for or cancel only task-owned operations, never use broad pkill.
