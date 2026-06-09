#!/usr/bin/env node

/**
 * Synchronisiert project-context mit Ruflo Memory System
 * Lädt wichtige Entscheidungen und speichert neue Erkenntnisse
 *
 * Wird automatisch vor jedem Task via Hook aufgerufen
 */

const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

const PROJECT_ROOT = process.cwd();
const CONTEXT_FILE = path.join(PROJECT_ROOT, ".claude-flow", "context.json");
const MEMORY_CACHE = path.join(PROJECT_ROOT, ".claude-flow", "memory-cache.json");

/**
 * Lade gespeicherte project-context
 */
function loadContext() {
  try {
    if (fs.existsSync(CONTEXT_FILE)) {
      return JSON.parse(fs.readFileSync(CONTEXT_FILE, "utf-8"));
    }
  } catch (e) {
    console.warn("Warnung: context.json konnte nicht geladen werden");
  }
  return null;
}

/**
 * Speichere Entscheidungen im Memory-Cache
 */
function syncToMemoryCache(context) {
  try {
    const cache = context.decisions || {};
    fs.writeFileSync(MEMORY_CACHE, JSON.stringify(cache, null, 2), "utf-8");
    console.log("✓ Memory-Cache synchronisiert");
  } catch (e) {
    console.error("Fehler beim Synchronisieren:", e.message);
  }
}

/**
 * Versuche über Ruflo CLI zu synchronisieren (optional)
 */
function syncToRufloMemory(context) {
  try {
    const commands = [
      `claude-flow memory store --key "projekt/stack" --value "Backend: FastAPI + SQLAlchemy + Alembic. Frontend: React 19 + TypeScript + Vite + Tailwind. DB: PostgreSQL" --namespace uni-projekt`,
      `claude-flow memory store --key "projekt/branch" --value "${context.metadata.branch}" --namespace uni-projekt`,
      `claude-flow memory store --key "projekt/lastCommit" --value "${context.metadata.lastCommit}" --namespace uni-projekt`,
    ];

    // Führe aus wenn ruflo verfügbar
    commands.forEach((cmd) => {
      try {
        execSync(cmd, { stdio: "ignore" });
      } catch {
        // Ignoriere wenn ruflo nicht verfügbar
      }
    });

    console.log("✓ Ruflo Memory aktualisiert");
  } catch (e) {
    // Stille Fehlerbehandlung - Ruflo könnte nicht installiert sein
  }
}

/**
 * Main
 */
function main() {
  const context = loadContext();

  if (!context) {
    console.log("⚠️  Kein Context gefunden. Führe project-context.ts aus:");
    console.log("   npx ts-node .claude-flow/project-context.ts");
    return;
  }

  console.log(`📊 Synchronisiere project-context für Branch: ${context.metadata.branch}`);

  syncToMemoryCache(context);
  syncToRufloMemory(context);

  console.log("✓ Synchronisierung abgeschlossen");
}

main();
