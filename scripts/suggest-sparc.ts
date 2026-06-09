#!/usr/bin/env node

/**
 * CLI Tool: Schlägt optimale SPARC-Befehle basierend auf aktuellem Projekt-Zustand vor
 *
 * Usage:
 *   npx ts-node scripts/suggest-sparc.ts [--copy]
 *   npx ts-node scripts/suggest-sparc.ts feature "Feature description"
 *   npx ts-node scripts/suggest-sparc.ts api "API endpoint"
 *   npx ts-node scripts/suggest-sparc.ts ui "Component"
 *
 * Imports project-context.ts und generiert Copy-Paste-Ready Befehle
 */

import * as path from "path";
import * as fs from "fs";

// Einfache Implementation ohne externe Dependencies
interface ProjectContext {
  metadata: {
    branch: string;
    lastCommit: string;
  };
  structure: {
    tests: {
      backend: number;
      frontend: number;
    };
  };
  decisions: Record<string, string>;
}

class SparcSuggester {
  private contextFile: string;
  private context: ProjectContext | null = null;

  constructor() {
    this.contextFile = path.join(process.cwd(), ".claude-flow", "context.json");
    this.loadContext();
  }

  private loadContext(): void {
    try {
      if (fs.existsSync(this.contextFile)) {
        this.context = JSON.parse(fs.readFileSync(this.contextFile, "utf-8"));
      }
    } catch (e) {
      console.warn("⚠️  context.json nicht gefunden. Führe project-context aus:");
      console.warn("   npx ts-node .claude-flow/project-context.ts");
    }
  }

  /**
   * Basierend auf aktuellem Zustand die beste Empfehlung geben
   */
  public suggestOptimal(): string {
    if (!this.context) {
      return this.getDefaultCommand();
    }

    // Analysiere Branch-Name
    const branch = this.context.metadata.branch;

    if (branch.includes("migration") || branch.includes("schema")) {
      return this.generateSchemaCommand(branch);
    } else if (branch.includes("api")) {
      return this.generateAPICommand(branch);
    } else if (branch.includes("ui") || branch.includes("component")) {
      return this.generateUICommand(branch);
    } else if (this.context.structure.tests.backend === 0) {
      return this.generateBackendTestsCommand();
    } else if (this.context.structure.tests.frontend === 0) {
      return this.generateFrontendTestsCommand();
    }

    // Fallback: Generischer Feature-Command
    return this.generateFeatureCommand(branch);
  }

  /**
   * Spezifische Command für Schema/Migration
   */
  private generateSchemaCommand(branch: string): string {
    const featureName = branch.replace(/^feat\/\d+-/, "").replace(/-/g, " ");
    return (
      `claude-flow sparc run dev \\\n` +
      `  "${featureName.charAt(0).toUpperCase() + featureName.slice(1)}: ` +
      `PostgreSQL Schema mit Alembic Migration + SQLAlchemy Entities. ` +
      `Tests für Schema-Validierung und Datenintegrität."`
    );
  }

  /**
   * Command für API-Endpoints
   */
  private generateAPICommand(branch: string): string {
    const featureName = branch.replace(/^feat\/\d+-/, "").replace(/-/g, " ");
    return (
      `claude-flow sparc run api \\\n` +
      `  "${featureName}: REST Endpoints mit FastAPI, Pydantic Validation, ` +
      `pytest Integration Tests und Authentifizierung"`
    );
  }

  /**
   * Command für UI-Komponenten
   */
  private generateUICommand(branch: string): string {
    const featureName = branch.replace(/^feat\/\d+-/, "").replace(/-/g, " ");
    return (
      `claude-flow sparc run ui \\\n` +
      `  "${featureName}: React Component mit TypeScript, Tailwind CSS, ` +
      `React Query Server State, Unit Tests"`
    );
  }

  /**
   * Wenn Backend keine Tests hat
   */
  private generateBackendTestsCommand(): string {
    return (
      `claude-flow sparc run tdd \\\n` +
      `  "Backend-Tests: Schreibe pytest Tests für alle bestehenden FastAPI Endpoints. ` +
      `Nutze fixtures für DB und Auth. Ziel: >80% Coverage"`
    );
  }

  /**
   * Wenn Frontend keine Tests hat
   */
  private generateFrontendTestsCommand(): string {
    return (
      `claude-flow sparc run tdd \\\n` +
      `  "Frontend-Tests: Unit + Integration Tests für alle React-Komponenten. ` +
      `Nutze Vitest + React Testing Library. Ziel: >80% Coverage"`
    );
  }

  /**
   * Generischer Feature-Command
   */
  private generateFeatureCommand(branch: string): string {
    const featureName = branch.replace(/^feat\/\d+-/, "").replace(/-/g, " ");
    return (
      `claude-flow sparc run tdd \\\n` +
      `  "${featureName.charAt(0).toUpperCase() + featureName.slice(1)}: ` +
      `Vollständige Implementation mit Tests von Anfang an. ` +
      `TDD: Fehlende Tests zuerst, dann Implementierung."`
    );
  }

  /**
   * Default wenn kein Context
   */
  private getDefaultCommand(): string {
    return (
      `claude-flow sparc run tdd \\\n` +
      `  "Feature: Beschreibe die Anforderung. Tests zuerst, dann Code."`
    );
  }

  /**
   * Zeige Anleitung an
   */
  public showUsage(): void {
    console.log(`
╔═══════════════════════════════════════════════════════════════╗
║           SPARC Command Generator for study-os-thesis         ║
╚═══════════════════════════════════════════════════════════════╝

USAGE:
  npx ts-node scripts/suggest-sparc.ts              # Auto-suggest
  npx ts-node scripts/suggest-sparc.ts feature      # Feature template
  npx ts-node scripts/suggest-sparc.ts api          # API template
  npx ts-node scripts/suggest-sparc.ts ui           # UI template
  npx ts-node scripts/suggest-sparc.ts refactor     # Refactor template
  npx ts-node scripts/suggest-sparc.ts --copy       # Copy to clipboard

QUICK START:
  1. npx ts-node .claude-flow/project-context.ts    (Laden Context)
  2. npx ts-node scripts/suggest-sparc.ts            (Command anzeigen)
  3. Ctrl+C und command kopieren
  4. Ausführen im Terminal

TEMPLATES:
`);
  }

  /**
   * Zeige verschiedene Templates
   */
  public showTemplates(): void {
    const templates: { [key: string]: string } = {
      feature: this.generateFeatureCommand("feat/00-example-feature"),
      api: this.generateAPICommand("feat/00-api-endpoint"),
      ui: this.generateUICommand("feat/00-ui-component"),
      refactor: `claude-flow sparc run refactor \\
  "Module: Aufteilen, Konsolidieren oder Umstrukturieren. Tests müssen vor und nach grün sein."`,
      migration: this.generateSchemaCommand("feat/00-migration"),
      fullstack: `claude-flow orchestrate \\
  "Full-Stack Feature:
   - Backend: API Endpoints
   - Frontend: React Components
   - Database: Schema + Migration
   - Tests: Unit + Integration" \\
  --agents 8 \\
  --topology hierarchical \\
  --parallel \\
  --memory persistent`,
    };

    Object.entries(templates).forEach(([name, cmd]) => {
      console.log(`\n📋 ${name.toUpperCase()}\n${cmd}\n`);
    });
  }
}

// CLI Main
function main(): void {
  const args = process.argv.slice(2);
  const suggester = new SparcSuggester();

  if (args.length === 0) {
    // Default: Auto-Vorschlag
    const command = suggester.suggestOptimal();
    console.log("\n✨ OPTIMALER SPARC COMMAND FÜR DEIN PROJEKT:\n");
    console.log(command);
    console.log(
      '\n📋 Kopiere den Command oben und führe ihn aus.\n'
    );
  } else if (args[0] === "--help" || args[0] === "-h") {
    suggester.showUsage();
  } else if (args[0] === "--templates") {
    suggester.showTemplates();
  } else if (args[0] === "--copy") {
    const command = suggester.suggestOptimal();
    console.log(command);
    // Versuche zu Clipboard zu kopieren (xclip/pbcopy)
    try {
      require("child_process").execSync("xclip -selection clipboard", {
        input: command,
      });
      console.log("\n✓ Kopiert!");
    } catch {
      // Fallback wenn kein clipboard
      console.log("\n⚠️  Clipboard nicht verfügbar");
    }
  } else {
    // Template anfordern
    const type = args[0];
    const desc = args.slice(1).join(" ") || "Feature";

    const templates: { [key: string]: string } = {
      feature: `claude-flow sparc run tdd \\\n  "${desc}: TDD - fehlende Tests zuerst, dann Code"`,
      api: `claude-flow sparc run api \\\n  "${desc}: REST API mit Pydantic Validation und pytest"`,
      ui: `claude-flow sparc run ui \\\n  "${desc}: React Component mit Tailwind und Unit Tests"`,
      refactor: `claude-flow sparc run refactor \\\n  "${desc}: Tests müssen vor und nach grün sein"`,
      dev: `claude-flow sparc run dev \\\n  "${desc}"`,
    };

    const command = templates[type] || templates.feature;
    console.log("\n✨ COMMAND:\n");
    console.log(command);
  }
}

main();
