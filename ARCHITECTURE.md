# Migration Architecture & Flow Diagrams

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        MIGRATION TOOLKIT                             │
│                                                                       │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐      │
│  │  config.json │──────▶│   utils.py   │◀─────│ 9 Migration  │      │
│  │  (Settings)  │      │  (Functions) │      │   Scripts    │      │
│  └──────────────┘      └──────────────┘      └──────────────┘      │
│                               │                                       │
│                               │                                       │
│                        ┌──────▼──────┐                               │
│                        │ validate_   │                               │
│                        │ migration.py│                               │
│                        └──────┬──────┘                               │
│                               │                                       │
│                        ┌──────▼──────────┐                           │
│                        │ run_all_        │                           │
│                        │ migrations.py   │                           │
│                        └─────────────────┘                           │
└─────────────────────────────────────────────────────────────────────┘
                               │
            ┌──────────────────┴──────────────────┐
            │                                     │
            ▼                                     ▼
┌───────────────────────┐              ┌───────────────────────┐
│   SOURCE WORKSPACE    │              │   TARGET WORKSPACE    │
│                       │              │                       │
│  • Users & Groups     │              │  • Users & Groups     │
│  • Clusters           │──Migration──▶│  • Clusters           │
│  • Notebooks          │    Via API   │  • Notebooks          │
│  • Jobs               │              │  • Jobs               │
│  • Secrets            │              │  • Secrets            │
│  • SQL Warehouses     │              │  • SQL Warehouses     │
│  • Git Repos          │              │  • Git Repos          │
│  • Policies           │              │  • Policies           │
└───────────────────────┘              └───────────────────────┘
```

---

## Migration Flow Diagram

```
                    START MIGRATION
                          │
                          ▼
                 ┌────────────────┐
                 │   Validation   │
                 │   (Pre-check)  │
                 └────────┬───────┘
                          │
                    [Pass/Fail?]
                          │
              ┌───────────┴───────────┐
              │                       │
              ▼ FAIL              PASS▼
         [Fix Issues]          ┌──────────────┐
              │                │ PHASE 1      │
              └────────────────│ Enablement   │
                               │ Objects      │
                               └──────┬───────┘
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        │                             │                             │
        ▼                             ▼                             ▼
┌───────────────┐            ┌────────────────┐           ┌─────────────────┐
│ 1. Users &    │            │ 2. Cluster     │           │ 3. SQL          │
│    Groups     │            │    Policies    │           │    Warehouses   │
└───────┬───────┘            └────────┬───────┘           └────────┬────────┘
        │                             │                             │
        └─────────────────────────────┼─────────────────────────────┘
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        │                             │                             │
        ▼                             ▼                             │
┌───────────────┐            ┌────────────────┐                    │
│ 4. Secret     │            │ 5. Workspace   │                    │
│    Scopes     │            │    Folders     │                    │
└───────┬───────┘            └────────┬───────┘                    │
        │                             │                             │
        └─────────────────────────────┼─────────────────────────────┘
                                      │
                                      ▼
                               ┌──────────────┐
                               │ PHASE 2      │
                               │ Content      │
                               │ Objects      │
                               └──────┬───────┘
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        │                             │                             │
        ▼                             ▼                             ▼
┌───────────────┐            ┌────────────────┐           ┌─────────────────┐
│ 6. All-Purpose│            │ 7. Notebooks   │           │ 8. Git Repos    │
│    Clusters   │            │                │           │                 │
└───────┬───────┘            └────────┬───────┘           └────────┬────────┘
        │                             │                             │
        └─────────────────────────────┼─────────────────────────────┘
                                      │
                                      ▼
                               ┌──────────────┐
                               │ PHASE 3      │
                               │ Orchestration│
                               └──────┬───────┘
                                      │
                                      ▼
                              ┌───────────────┐
                              │ 9. Jobs/      │
                              │    Workflows  │
                              └───────┬───────┘
                                      │
                                      ▼
                          ┌───────────────────┐
                          │ Post-Migration    │
                          │ Manual Actions    │
                          └─────────┬─────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
        ▼                           ▼                           ▼
┌───────────────┐          ┌────────────────┐        ┌─────────────────┐
│ Update Secret │          │ Re-auth Git    │        │ Update Job      │
│ Values        │          │ Repos          │        │ Cluster IDs     │
└───────┬───────┘          └────────┬───────┘        └────────┬────────┘
        │                           │                           │
        └───────────────────────────┼───────────────────────────┘
                                    │
                                    ▼
                            ┌───────────────┐
                            │   Testing &   │
                            │  Validation   │
                            └───────┬───────┘
                                    │
                              [All Pass?]
                                    │
                        ┌───────────┴───────────┐
                        │                       │
                        ▼ YES              NO   ▼
                  ┌──────────┐          [Fix Issues]
                  │ GO LIVE  │                 │
                  └────┬─────┘                 │
                       │                       │
                       └───────────────────────┘
                                    │
                                    ▼
                             MIGRATION COMPLETE
```

---

## Object Dependencies

```
                        ┌────────────────┐
                        │ Users & Groups │
                        └────────┬───────┘
                                 │
                    ┌────────────┼────────────┐
                    │            │            │
                    ▼            ▼            ▼
            ┌─────────────┐ ┌─────────┐ ┌──────────┐
            │ Workspace   │ │ Cluster │ │ Secret   │
            │ Folders     │ │ Policies│ │ Scopes   │
            └──────┬──────┘ └────┬────┘ └────┬─────┘
                   │             │            │
                   ▼             ▼            │
            ┌─────────────┐ ┌─────────┐     │
            │ Notebooks   │ │ Clusters│     │
            └──────┬──────┘ └────┬────┘     │
                   │             │            │
                   │      ┌──────┘            │
                   │      │                   │
            ┌──────▼──────▼───────────────────▼────┐
            │            Jobs/Workflows            │
            │  (depends on all above objects)      │
            └──────────────────────────────────────┘

Legend:
  │ = required dependency
  ▼ = migration direction
```

---

## Data Flow per Script

### Users & Groups Migration
```
SOURCE                          TARGET
  │                              │
  ├─── GET /groups/list ────────┐
  │                              │
  ├─── GET /groups/members ─────┤
  │                              │
  │                              ├─── POST /groups/create
  │                              │
  │                              ├─── POST /scim/v2/Users
  │                              │
  │                              └─── POST /groups/add-member
  │
 [Backup Created]
```

### Notebooks Migration
```
SOURCE                          TARGET
  │                              │
  ├─── GET /workspace/list ─────┐
  │    (recursive)               │
  │                              │
  ├─── GET /workspace/export ───┤
  │    (for each notebook)       │
  │                              │
  │                              ├─── POST /workspace/mkdirs
  │                              │    (ensure folders exist)
  │                              │
  │                              └─── POST /workspace/import
  │                                   (for each notebook)
 [Backup Created]
```

### Jobs Migration
```
SOURCE                          TARGET
  │                              │
  ├─── GET /jobs/list ──────────┐
  │    (paginated)               │
  │                              │
  ├─── GET /jobs/get ───────────┤
  │    (for each job)            │
  │                              │
  │                              ├─── POST /jobs/create
  │                              │    (with job clusters)
  │                              │
  │                              └─── [Manual: Update IDs]
  │
 [Backup Created]
```

---

## Error Handling Flow

```
                    ┌─────────────────┐
                    │  Execute Script │
                    └────────┬────────┘
                             │
                      [For Each Object]
                             │
                    ┌────────▼────────┐
                    │  Try Migration  │
                    └────────┬────────┘
                             │
                      [Success/Fail?]
                             │
              ┌──────────────┴──────────────┐
              │                             │
              ▼ SUCCESS                FAIL ▼
    ┌──────────────────┐         ┌──────────────────┐
    │ Log Success      │         │ Log Error        │
    │ Increment Count  │         │ Increment Count  │
    └────────┬─────────┘         │ Continue/Abort?  │
             │                   └────────┬─────────┘
             │                            │
             └────────────┬───────────────┘
                          │
                    [More Objects?]
                          │
                 ┌────────┴────────┐
                 │                 │
            YES  ▼                 │ NO
        [Next Object]              │
                                   ▼
                          ┌─────────────────┐
                          │ Print Summary   │
                          │ Success: X      │
                          │ Failed: Y       │
                          └─────────────────┘
```

---

## Parallel vs Sequential Execution

### Can Run in Parallel (Independent)
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ SQL Warehouses  │     │ Secret Scopes   │     │ Cluster Policies│
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 ▼
                        (After Users & Groups)
```

### Must Run Sequentially (Dependent)
```
┌─────────────────┐
│ Workspace       │
│ Folders         │
└────────┬────────┘
         │
         │ (must exist before)
         │
         ▼
┌─────────────────┐
│ Notebooks       │
└────────┬────────┘
         │
         │ (notebooks must exist before)
         │
         ▼
┌─────────────────┐
│ Jobs            │
│ (reference NBs) │
└─────────────────┘
```

---

## State Transitions

### Cluster State Transition
```
SOURCE WORKSPACE              TARGET WORKSPACE
┌──────────────┐             ┌──────────────┐
│   RUNNING    │             │  TERMINATED  │
│      or      │──Migrate──▶ │              │
│  TERMINATED  │             │ (Created but │
└──────────────┘             │  not started)│
                             └──────┬───────┘
                                    │
                            [Manual: Start]
                                    │
                                    ▼
                             ┌──────────────┐
                             │   RUNNING    │
                             └──────────────┘
```

### Job State Transition
```
SOURCE WORKSPACE              TARGET WORKSPACE
┌──────────────┐             ┌──────────────┐
│   ENABLED    │             │   PAUSED     │
│     with     │──Migrate──▶ │              │
│  Schedule    │             │ (Needs setup)│
└──────────────┘             └──────┬───────┘
                                    │
                         [Manual: Update Clusters]
                                    │
                                    ▼
                             ┌──────────────┐
                             │   ENABLED    │
                             └──────────────┘
```

### Secret State Transition
```
SOURCE WORKSPACE              TARGET WORKSPACE
┌──────────────┐             ┌──────────────────────┐
│  Secret Key  │             │    Secret Key with   │
│    with      │──Migrate──▶ │    PLACEHOLDER       │
│  Real Value  │             │    Value             │
└──────────────┘             └──────┬───────────────┘
  (Can't read)                      │
                            [Manual: Update Value]
                                    │
                                    ▼
                             ┌──────────────────┐
                             │  Secret Key with │
                             │  Real Value      │
                             └──────────────────┘
```

---

## Network Communication

```
┌───────────────────┐                           ┌───────────────────┐
│   Your Machine    │                           │   Your Machine    │
│  (Running Scripts)│                           │  (Running Scripts)│
└─────────┬─────────┘                           └─────────┬─────────┘
          │                                               │
          │ HTTPS API Calls                              │ HTTPS API Calls
          │ (Authorization: Bearer TOKEN)                │ (Authorization: Bearer TOKEN)
          │                                               │
          ▼                                               ▼
┌─────────────────────────┐                   ┌─────────────────────────┐
│  SOURCE WORKSPACE       │                   │  TARGET WORKSPACE       │
│  Databricks REST API    │                   │  Databricks REST API    │
│                         │                   │                         │
│  • GET endpoints        │                   │  • POST endpoints       │
│    (read data)          │                   │    (create objects)     │
│                         │                   │  • PUT endpoints        │
│  • Returns JSON         │                   │    (update objects)     │
│                         │                   │                         │
└─────────────────────────┘                   └─────────────────────────┘
```

---

## Backup Strategy

```
                    ┌─────────────────┐
                    │  Start Script   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Fetch Objects  │
                    │  from Source    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────────────────┐
                    │  Save to Backup File:       │
                    │  backup_<type>_<time>.json  │
                    └────────┬────────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Create Objects │
                    │  in Target      │
                    └─────────────────┘

Backup File Format:
{
  "timestamp": "2026-01-08T10:30:00Z",
  "source_workspace": "...",
  "object_type": "notebooks",
  "count": 42,
  "objects": [ ... ]
}
```

---

## Recommended Execution Timeline

```
TIME    │ ACTIVITY
────────┼──────────────────────────────────────────
00:00   │ Start: Run validation script
00:05   │ Review validation results
00:10   │ Begin Phase 1: Users & Groups
00:30   │ Phase 1: Policies, Warehouses, Secrets, Folders
01:00   │ ─── Checkpoint: Verify Phase 1 ───
01:15   │ Begin Phase 2: Clusters
01:30   │ Phase 2: Notebooks
02:00   │ Phase 2: Git Repos
02:15   │ ─── Checkpoint: Verify Phase 2 ───
02:30   │ Begin Phase 3: Jobs
03:00   │ ─── Checkpoint: Verify Phase 3 ───
03:15   │ Begin Post-Migration: Update Secrets
03:45   │ Post-Migration: Re-auth Git Repos
04:00   │ Post-Migration: Update Job Clusters
05:00   │ Testing: Sample workflows
06:00   │ ─── Checkpoint: Final Verification ───
06:30   │ Go-Live / User Communication
────────┴──────────────────────────────────────────

Total Time: ~6-7 hours for typical workspace
Note: Adjust based on object counts
```

---

## Success Metrics Dashboard

```
╔════════════════════════════════════════════════╗
║        MIGRATION COMPLETION STATUS             ║
╠════════════════════════════════════════════════╣
║                                                ║
║  Phase 1: Enablement Objects                  ║
║  ▓▓▓▓▓▓▓▓▓▓ 100% (5/5 scripts)                ║
║                                                ║
║  Phase 2: Content Objects                     ║
║  ▓▓▓▓▓▓▓▓▓▓ 100% (3/3 scripts)                ║
║                                                ║
║  Phase 3: Orchestration                       ║
║  ▓▓▓▓▓▓▓▓▓▓ 100% (1/1 scripts)                ║
║                                                ║
║  Post-Migration Actions                       ║
║  ▓▓▓▓▓░░░░░  50% (2/4 tasks)                  ║
║                                                ║
║  ✓ Secrets Updated                            ║
║  ✓ Git Re-authenticated                       ║
║  ⏳ Jobs Updated (in progress)                ║
║  ☐ Testing Complete                           ║
║                                                ║
╠════════════════════════════════════════════════╣
║  Objects Migrated:                            ║
║    Users: 45        Notebooks: 123            ║
║    Groups: 12       Git Repos: 3              ║
║    Clusters: 8      Jobs: 28                  ║
║    Policies: 4      Secrets: 15               ║
║    Warehouses: 2    Folders: 87               ║
╚════════════════════════════════════════════════╝
```

---

*These diagrams provide visual representation of the migration architecture and flow. Refer to other documentation for detailed instructions.*
