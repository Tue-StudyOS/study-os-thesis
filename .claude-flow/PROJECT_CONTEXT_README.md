# Project Context System mit Ruflo

Intelligentes System zum Verwalten deines Projekt-Kontexts und zur automatischen Generierung optimaler SPARC-Befehle.

## Was dieses System tut

1. **Analysiert** dein Projekt automatisch (Struktur, Tests, Git-Status)
2. **Speichert** Architekturentscheidungen im Memory
3. **Generiert** optimale `claude-flow sparc` Befehle basierend auf aktuellem Zustand
4. **Synchronisiert** zwischen lokalem Filesystem und Ruflo Memory System

## Dateistruktur

```
.claude-flow/
├── project-context.ts          # Core: Projekt-Analyse & SPARC-Generator
├── context.hooks.json          # Hooks für automatische Updates
├── sync-memory.js              # Memory-Synchronisierung
├── context.json                # Aktueller Projekt-Status (auto-generated)
├── memory-cache.json           # Lokaler Entscheidungs-Cache
└── PROJECT_CONTEXT_README.md   # Diese Datei

scripts/
└── suggest-sparc.ts            # CLI: Bekomme beste SPARC-Befehle
```

## Schnelstart

### 1. Project Context laden (beim ersten Mal)

```bash
npx ts-node .claude-flow/project-context.ts
```

Output:
```json
{
  "metadata": {
    "branch": "feat/22-chair-employees-schema",
    "lastCommit": "test: entity shape and migration 0013 integration tests",
    ...
  },
  "structure": {
    "backendModules": ["models", "api", "services", ...],
    "tests": { "backend": 42, "frontend": 15 },
    ...
  },
  "decisions": { ... }
}
```

### 2. Optimale SPARC-Befehle abrufen

```bash
# Auto-Vorschlag basierend auf Branch/Kontext
npx ts-node scripts/suggest-sparc.ts

# Template für spezifischen Typ
npx ts-node scripts/suggest-sparc.ts api "User management endpoints"
npx ts-node scripts/suggest-sparc.ts ui "Dashboard component"
npx ts-node scripts/suggest-sparc.ts refactor "User service cleanup"

# Alle Templates anzeigen
npx ts-node scripts/suggest-sparc.ts --templates
```

Output:
```
✨ OPTIMALER SPARC COMMAND FÜR DEIN PROJEKT:

claude-flow sparc run dev \
  "Chair Employees: PostgreSQL Schema mit Alembic Migration + SQLAlchemy Entities"
```

### 3. Kopiere und führe aus

```bash
# Copy-pasted aus suggest-sparc output:
claude-flow sparc run dev \
  "Chair Employees: PostgreSQL Schema mit Alembic Migration + SQLAlchemy Entities"
```

## Wie Architekturentscheidungen gespeichert werden

### Manuell speichern (einmalig)

```bash
claude-flow memory store \
  --key "entscheidung/auth" \
  --value "JWT mit httpOnly Cookies. Access: 15min, Refresh: 7d" \
  --namespace uni-projekt
```

### Automatisch nach dem Coding

Deine Entscheidungen werden automatisch in `.claude-flow/memory-cache.json` gespeichert und sind dann für alle zukünftigen SPARC-Tasks verfügbar.

## Die Hooks

Drei automatische Hooks halten deinen Kontext aktuell:

### `post-task` Hook
Nach jedem SPARC-Task wird `project-context.ts` ausgeführt:
```bash
npx ts-node .claude-flow/project-context.ts > /dev/null 2>&1
```
→ Updates `context.json` mit neuer Struktur und Tests

### `on-swarm-init` Hook
Bevor ein SPARC-Swarm startet, wird Context geladen:
```bash
npx ts-node .claude-flow/project-context.ts
```
→ Zeigt aktuellen Status

### `pre-task` Hook
Vor jedem Task wird Memory synchronisiert:
```bash
node .claude-flow/sync-memory.js
```
→ Aktualisiert `.claude-flow/memory-cache.json` mit Ruflo Memory

## Typische Workflows

### Workflow 1: Feature in 3 Schritten

```bash
# 1. Context laden (Optional, passiert automatisch)
npx ts-node .claude-flow/project-context.ts

# 2. Bekomme SPARC-Command
npx ts-node scripts/suggest-sparc.ts

# 3. Führe ihn aus
claude-flow sparc run tdd "Feature: Speichere Entscheidung im Memory"
```

### Workflow 2: Memory + SPARC kombiniert

```bash
# 1. Wichtige Entscheidung speichern
claude-flow memory store \
  --key "feature/chair-schema" \
  --value "Universities 1:N Chairs, Chairs 1:N Employees. Cascade delete on University." \
  --namespace uni-projekt

# 2. Get SPARC-Command (dieser hat jetzt Zugriff auf deine Entscheidung)
npx ts-node scripts/suggest-sparc.ts

# 3. Ausführen
<paste command>
```

### Workflow 3: Mehrere Features parallel

```bash
# Alle Entscheidungen ins Memory:
claude-flow memory store --key "projekt/stack" --value "..." --namespace uni-projekt
claude-flow memory store --key "projekt/conventions" --value "..." --namespace uni-projekt

# Full-Stack Feature mit Swarm
claude-flow orchestrate \
  "Full-Stack Chair Management:
   - Backend: API (GET, POST, PUT, DELETE)
   - Frontend: Table + Form Component
   - Database: chair_employees schema
   - Tests: Unit + Integration" \
  --agents 8 --topology hierarchical --parallel --memory persistent
```

## Was project-context alles trackst

```typescript
interface ProjectContext {
  metadata: {
    name: string;           // "study-os-thesis"
    branch: string;         // aktuelle Git-Branch
    lastCommit: string;     // letzter Commit-Message
    updatedAt: string;      // timestamp
  };
  stack: {
    backend: { framework, language, orm, testing, migrations };
    frontend: { framework, language, bundler, styling };
    database: string;
  };
  structure: {
    backendModules: string[];    // gefundene Module in backend/app
    frontendModules: string[];   // gefundene Module in frontend/src
    migrations: string[];        // neueste 5 Migrations
    tests: { backend, frontend }; // Anzahl Tests
  };
  decisions: Record<string, string>; // Gespeicherte Entscheidungen
  openBranch: {
    name: string;          // Z.B. "feat/22-chair-employees-schema"
    issueName: string;     // "chair employees schema"
  };
}
```

## Tipps für optimale Nutzung

### ✅ Bestpraktiken

1. **Nach jeder Architekturentscheid** Memory aktualisieren:
   ```bash
   claude-flow memory store --key "entscheidung/X" --value "..." --namespace uni-projekt
   ```

2. **Vor neuer Session** Context laden:
   ```bash
   npx ts-node .claude-flow/project-context.ts
   ```

3. **Für Tests checken**:
   ```bash
   npx ts-node scripts/suggest-sparc.ts  # Zeigt ob Tests fehlen
   ```

### ❌ Was vermeiden

- **Nicht**: Manuell `context.json` editieren (wird überschrieben)
- **Nicht**: Entscheidungen nur im Kopf behalten (Memory benutzen!)
- **Nicht**: Alte Decisions im Memory lassen die nicht mehr relevant sind (aufräumen)

## Troubleshooting

### Problem: `context.json` ist leer/alt

**Lösung:**
```bash
npx ts-node .claude-flow/project-context.ts --force
```

### Problem: Memory und Context sind nicht synchron

**Lösung:**
```bash
node .claude-flow/sync-memory.js
```

### Problem: `suggest-sparc.ts` schlägt falschen Command vor

**Lösung:** Memory manuell aktualisieren mit Kontext:
```bash
claude-flow memory store \
  --key "feature/current" \
  --value "Was du gerade machst" \
  --namespace uni-projekt
```

## Integration mit Claude Code

Die Hooks sind in `.claude-flow/context.hooks.json` definiert. Sie werden automatisch von Ruflo aufgerufen.

Um sicherzustellen, dass Hooks richtig konfiguriert sind:

```bash
# Check Hooks konfiguration
cat .claude-flow/context.hooks.json

# Check ob context.json existiert und aktuell ist
cat .claude-flow/context.json | jq '.metadata'
```

---

**Erstellt:** 2026-06-09  
**Version:** 1.0  
**Basiert auf:** Ruflo v3.6+, project study-os-thesis
