#!/usr/bin/env node

/**
 * Project Context Manager (JavaScript Version)
 * Läuft direkt ohne TypeScript-Compiler
 *
 * Usage: node .claude-flow/project-context.js
 */

const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

class ProjectContextManager {
  constructor(rootPath = process.cwd()) {
    this.rootPath = rootPath;
    this.contextFile = path.join(rootPath, ".claude-flow", "context.json");
    this.memoryCachePath = path.join(rootPath, ".claude-flow", "memory-cache.json");
  }

  analyze() {
    const branch = this.getCurrentBranch();
    const lastCommit = this.getLastCommit();

    const context = {
      metadata: {
        name: "study-os-thesis",
        root: this.rootPath,
        updatedAt: new Date().toISOString(),
        branch,
        lastCommit,
      },
      stack: {
        backend: {
          framework: "FastAPI",
          language: "Python 3.10+",
          orm: "SQLAlchemy 2.0",
          testing: "pytest",
          migrations: "Alembic",
        },
        frontend: {
          framework: "React 19",
          language: "TypeScript",
          bundler: "Vite",
          styling: "Tailwind CSS",
        },
        database: "PostgreSQL",
      },
      structure: {
        backendModules: this.findBackendModules(),
        frontendModules: this.findFrontendModules(),
        migrations: this.findMigrations(),
        tests: {
          backend: this.countTests("backend"),
          frontend: this.countTests("frontend"),
        },
      },
      decisions: this.loadDecisions(),
      openBranch: this.parseOpenBranch(branch),
    };

    this.saveContext(context);
    return context;
  }

  generateSparcCommands() {
    const context = this.loadContext() || this.analyze();
    const commands = new Map();

    const branchType = this.determineBranchType(context.openBranch.name);

    if (branchType === "feature") {
      commands.set("primary", this.generateFeatureCommand(context));
    } else if (branchType === "fix") {
      commands.set("primary", this.generateFixCommand(context));
    } else if (branchType === "refactor") {
      commands.set("primary", this.generateRefactorCommand(context));
    } else {
      commands.set("primary", this.generateDevCommand(context));
    }

    if (this.hasBackendTests(context) && !this.hasFrontendTests(context)) {
      commands.set("nextStep", this.generateUICommand(context));
    } else if (!this.hasBackendTests(context)) {
      commands.set("nextStep", this.generateAPICommand(context));
    }

    return commands;
  }

  getRecommendations() {
    const context = this.loadContext() || this.analyze();
    const recommendations = [];

    const decisions = context.decisions || {};
    if (Object.keys(decisions).length === 0) {
      recommendations.push(
        "💾 Memory ist leer! Speichere Architekturentscheidungen:\n" +
        "   Siehe: .claude-flow/initial-memories.md"
      );
    }

    const testRatio = context.structure.tests.backend / Math.max(context.structure.tests.frontend, 1) || 0;
    if (testRatio > 2) {
      recommendations.push(
        "🧪 Frontend hat weniger Tests als Backend. Nächster Fokus: Unit-Tests für React Components"
      );
    }

    if (context.openBranch.name.includes("22-chair")) {
      recommendations.push(
        "🪑 Chair-Employees Feature erkannt. Start: Architecture Phase für DB Schema"
      );
    }

    return recommendations;
  }

  // Private methods
  getCurrentBranch() {
    try {
      return execSync("git rev-parse --abbrev-ref HEAD", {
        cwd: this.rootPath,
        encoding: "utf-8",
      }).trim();
    } catch {
      return "unknown";
    }
  }

  getLastCommit() {
    try {
      return execSync("git log -1 --pretty=format:%s", {
        cwd: this.rootPath,
        encoding: "utf-8",
      }).trim();
    } catch {
      return "unknown";
    }
  }

  findBackendModules() {
    const appPath = path.join(this.rootPath, "backend", "app");
    try {
      const dirs = fs.readdirSync(appPath, { withFileTypes: true });
      return dirs
        .filter((d) => d.isDirectory() && !d.name.startsWith("_"))
        .map((d) => d.name);
    } catch {
      return [];
    }
  }

  findFrontendModules() {
    const srcPath = path.join(this.rootPath, "frontend", "src");
    try {
      const dirs = fs.readdirSync(srcPath, { withFileTypes: true });
      return dirs
        .filter((d) => d.isDirectory() && !d.name.startsWith("_"))
        .map((d) => d.name);
    } catch {
      return [];
    }
  }

  findMigrations() {
    const migrationsPath = path.join(
      this.rootPath,
      "backend",
      "alembic",
      "versions"
    );
    try {
      return fs
        .readdirSync(migrationsPath)
        .filter((f) => f.endsWith(".py"))
        .sort()
        .reverse()
        .slice(0, 5);
    } catch {
      return [];
    }
  }

  countTests(type) {
    try {
      const testPath =
        type === "backend"
          ? path.join(this.rootPath, "backend", "tests")
          : path.join(this.rootPath, "frontend", "src");

      const output = execSync(
        `find ${testPath} -type f \\( -name "*.test.ts" -o -name "test_*.py" \\) 2>/dev/null | wc -l`,
        { encoding: "utf-8" }
      );
      return parseInt(output.trim()) || 0;
    } catch {
      return 0;
    }
  }

  hasBackendTests(context) {
    return context.structure.tests.backend > 0;
  }

  hasFrontendTests(context) {
    return context.structure.tests.frontend > 0;
  }

  loadDecisions() {
    try {
      if (fs.existsSync(this.memoryCachePath)) {
        return JSON.parse(fs.readFileSync(this.memoryCachePath, "utf-8"));
      }
    } catch {
      // Ignore
    }
    return {};
  }

  parseOpenBranch(branch) {
    const match = branch.match(/^(feat|fix|refactor)\/(\d+)-(.+)/);
    if (match) {
      return {
        name: branch,
        issueName: match[3].replace(/-/g, " "),
        createdAt: new Date().toISOString(),
      };
    }
    return {
      name: branch,
      issueName: "unknown",
      createdAt: new Date().toISOString(),
    };
  }

  saveContext(context) {
    try {
      fs.mkdirSync(path.dirname(this.contextFile), { recursive: true });
      fs.writeFileSync(
        this.contextFile,
        JSON.stringify(context, null, 2),
        "utf-8"
      );
    } catch (error) {
      console.error("Fehler beim Speichern des Contexts:", error.message);
    }
  }

  loadContext() {
    try {
      if (fs.existsSync(this.contextFile)) {
        return JSON.parse(fs.readFileSync(this.contextFile, "utf-8"));
      }
    } catch {
      // Ignore
    }
    return null;
  }

  determineBranchType(branch) {
    if (branch.startsWith("feat/")) return "feature";
    if (branch.startsWith("fix/")) return "fix";
    if (branch.startsWith("refactor/")) return "refactor";
    return "unknown";
  }

  generateFeatureCommand(context) {
    const { issueName } = context.openBranch;
    return (
      `claude-flow sparc run tdd \\\n` +
      `  "${issueName}: Vollständige Implementierung mit Tests von Anfang an. TDD: Fehlende Tests zuerst, dann Code."`
    );
  }

  generateFixCommand(context) {
    const { lastCommit } = context.metadata;
    return (
      `claude-flow sparc run dev \\\n` +
      `  "Fix: ${lastCommit}. Tests zuerst, dann Fix."`
    );
  }

  generateRefactorCommand(context) {
    const { issueName } = context.openBranch;
    return (
      `claude-flow sparc run refactor \\\n` +
      `  "${issueName}: Refactor mit Test-Coverage. Tests müssen vor und nach grün sein."`
    );
  }

  generateDevCommand(context) {
    const { issueName } = context.openBranch;
    return (
      `claude-flow sparc run dev \\\n` +
      `  "${issueName}"`
    );
  }

  generateAPICommand(context) {
    return (
      `claude-flow sparc run api \\\n` +
      `  "REST API: Design Endpoints, Pydantic Schemas, pytest Integration Tests"`
    );
  }

  generateUICommand(context) {
    return (
      `claude-flow sparc run ui \\\n` +
      `  "React Component: TypeScript, Tailwind, React Query, Unit Tests"`
    );
  }
}

// Main
if (require.main === module) {
  const manager = new ProjectContextManager();
  const context = manager.analyze();

  console.log("\n" + "=".repeat(60));
  console.log("📊 PROJECT CONTEXT ANALYSIS");
  console.log("=".repeat(60));

  console.log(`\n📍 Projekt: ${context.metadata.name}`);
  console.log(`🌱 Branch: ${context.metadata.branch}`);
  console.log(`📝 Letzter Commit: ${context.metadata.lastCommit}`);

  console.log("\n📦 Stack:");
  console.log(`   Backend: ${context.stack.backend.framework} + ${context.stack.backend.orm}`);
  console.log(`   Frontend: ${context.stack.frontend.framework} + ${context.stack.frontend.bundler}`);
  console.log(`   Database: ${context.stack.database}`);

  console.log("\n📚 Struktur:");
  console.log(`   Backend-Module: ${context.structure.backendModules.join(", ")}`);
  console.log(`   Frontend-Module: ${context.structure.frontendModules.join(", ")}`);
  console.log(`   Tests: Backend=${context.structure.tests.backend}, Frontend=${context.structure.tests.frontend}`);

  console.log("\n🎯 EMPFOHLENE SPARC COMMANDS:");
  const commands = manager.generateSparcCommands();
  commands.forEach((cmd, key) => {
    console.log(`\n[${key.toUpperCase()}]`);
    console.log(cmd);
  });

  console.log("\n💡 RECOMMENDATIONS:");
  const recs = manager.getRecommendations();
  if (recs.length > 0) {
    recs.forEach((rec) => console.log(`\n${rec}`));
  } else {
    console.log("✓ Alles sieht gut aus!");
  }

  console.log("\n" + "=".repeat(60));
  console.log("✓ Context gespeichert in: .claude-flow/context.json");
  console.log("=".repeat(60) + "\n");
}

module.exports = ProjectContextManager;
