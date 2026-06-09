/**
 * Project Context Manager für study-os-thesis
 * Analysiert Codebase, Git-Zustand und Architekturentscheidungen
 * Generiert optimale SPARC-Befehle basierend auf aktuellem Projekt-Zustand
 *
 * Lädt automatisch via Ruflo Memory System
 * Updatet via Post-Task Hook
 */

import * as fs from "fs";
import * as path from "path";
import { execSync } from "child_process";

interface ProjectContext {
  metadata: {
    name: string;
    root: string;
    updatedAt: string;
    branch: string;
    lastCommit: string;
  };
  stack: {
    backend: {
      framework: string;
      language: string;
      orm: string;
      testing: string;
      migrations: string;
    };
    frontend: {
      framework: string;
      language: string;
      bundler: string;
      styling: string;
    };
    database: string;
  };
  structure: {
    backendModules: string[];
    frontendModules: string[];
    migrations: string[];
    tests: {
      backend: number;
      frontend: number;
    };
  };
  decisions: Record<string, string>;
  openBranch: {
    name: string;
    issueName: string;
    createdAt: string;
  };
}

export class ProjectContextManager {
  private rootPath: string;
  private contextFile: string;
  private memoryCachePath: string;

  constructor(rootPath: string = process.cwd()) {
    this.rootPath = rootPath;
    this.contextFile = path.join(rootPath, ".claude-flow", "context.json");
    this.memoryCachePath = path.join(rootPath, ".claude-flow", "memory-cache.json");
  }

  /**
   * Analyzes the full project and generates current context
   */
  public analyze(): ProjectContext {
    const branch = this.getCurrentBranch();
    const lastCommit = this.getLastCommit();

    const context: ProjectContext = {
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

  /**
   * Generates optimal SPARC commands based on current context
   */
  public generateSparcCommands(): Map<string, string> {
    const context = this.loadContext() || this.analyze();
    const commands = new Map<string, string>();

    // Analyze open branch to determine likely task type
    const branchType = this.determineBranchType(context.openBranch.name);

    // 1. Determine if this is a new feature, fix, or refactor
    if (branchType === "feature") {
      commands.set("primary", this.generateFeatureCommand(context));
      commands.set("alternative", this.generateDevCommand(context));
    } else if (branchType === "fix") {
      commands.set("primary", this.generateFixCommand(context));
      commands.set("alternative", this.generateDevCommand(context));
    } else if (branchType === "refactor") {
      commands.set("primary", this.generateRefactorCommand(context));
      commands.set("alternative", this.generateDevCommand(context));
    }

    // 2. Check what's already implemented
    if (this.hasBackendTests(context) && !this.hasFrontendTests(context)) {
      commands.set("nextStep", this.generateUICommand(context));
    } else if (!this.hasBackendTests(context)) {
      commands.set("nextStep", this.generateAPICommand(context));
    }

    return commands;
  }

  /**
   * Get human-readable recommendations for current work
   */
  public getRecommendations(): string[] {
    const context = this.loadContext() || this.analyze();
    const recommendations: string[] = [];

    // Memory first
    const decisions = context.decisions || {};
    if (Object.keys(decisions).length === 0) {
      recommendations.push(
        "💾 Memory leer! Zuerst Architekturentscheidungen speichern:\n" +
        "   claude-flow memory store --key 'projekt/stack' --value '[Stack Details]' --namespace uni-projekt"
      );
    }

    // Check test coverage
    const testRatio = context.structure.tests.backend / context.structure.tests.frontend || 0;
    if (testRatio < 1) {
      recommendations.push(
        "🧪 Frontend hat weniger Tests als Backend. Nächster Fokus: Unit-Tests für Komponenten"
      );
    }

    // Check branch status
    if (context.openBranch.name.includes("22-chair")) {
      recommendations.push(
        "🪑 Chair-Employees Feature: Likely DB-Schema + API + UI. Start with Architecture phase."
      );
    }

    return recommendations;
  }

  /**
   * --- PRIVATE HELPER METHODS ---
   */

  private getCurrentBranch(): string {
    try {
      return execSync("git rev-parse --abbrev-ref HEAD", {
        cwd: this.rootPath,
        encoding: "utf-8",
      }).trim();
    } catch {
      return "unknown";
    }
  }

  private getLastCommit(): string {
    try {
      return execSync("git log -1 --pretty=format:%s", {
        cwd: this.rootPath,
        encoding: "utf-8",
      }).trim();
    } catch {
      return "unknown";
    }
  }

  private findBackendModules(): string[] {
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

  private findFrontendModules(): string[] {
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

  private findMigrations(): string[] {
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
        .slice(0, 5); // last 5
    } catch {
      return [];
    }
  }

  private countTests(type: "backend" | "frontend"): number {
    const testPath =
      type === "backend"
        ? path.join(this.rootPath, "backend", "tests")
        : path.join(this.rootPath, "frontend", "src");

    try {
      const count = execSync(
        `find ${testPath} -name "*.test.ts" -o -name "test_*.py" | wc -l`,
        { encoding: "utf-8" }
      );
      return parseInt(count.trim()) || 0;
    } catch {
      return 0;
    }
  }

  private hasBackendTests(context: ProjectContext): boolean {
    return context.structure.tests.backend > 0;
  }

  private hasFrontendTests(context: ProjectContext): boolean {
    return context.structure.tests.frontend > 0;
  }

  private loadDecisions(): Record<string, string> {
    try {
      if (fs.existsSync(this.memoryCachePath)) {
        return JSON.parse(fs.readFileSync(this.memoryCachePath, "utf-8"));
      }
    } catch {
      // Ignore if file doesn't exist or is invalid
    }
    return {};
  }

  private parseOpenBranch(
    branch: string
  ): ProjectContext["openBranch"] {
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

  private saveContext(context: ProjectContext): void {
    try {
      fs.mkdirSync(path.dirname(this.contextFile), { recursive: true });
      fs.writeFileSync(
        this.contextFile,
        JSON.stringify(context, null, 2),
        "utf-8"
      );
    } catch (error) {
      console.error("Failed to save context:", error);
    }
  }

  private loadContext(): ProjectContext | null {
    try {
      if (fs.existsSync(this.contextFile)) {
        return JSON.parse(fs.readFileSync(this.contextFile, "utf-8"));
      }
    } catch {
      // Ignore if file doesn't exist or is invalid
    }
    return null;
  }

  private determineBranchType(
    branch: string
  ): "feature" | "fix" | "refactor" | "unknown" {
    if (branch.startsWith("feat/")) return "feature";
    if (branch.startsWith("fix/")) return "fix";
    if (branch.startsWith("refactor/")) return "refactor";
    return "unknown";
  }

  private generateFeatureCommand(context: ProjectContext): string {
    const { issueName } = context.openBranch;
    const { backendModules } = context.structure;

    // Determine if it's full-stack or specific layer
    if (issueName.includes("schema") || issueName.includes("migration")) {
      return `claude-flow sparc run dev \\
  "${issueName}: PostgreSQL Schema + Alembic Migration + SQLAlchemy Entities"`;
    }

    if (backendModules.includes("api")) {
      return `claude-flow sparc run api \\
  "${issueName}: REST API endpoints with pytest integration tests and FastAPI validation"`;
    }

    return `claude-flow sparc run tdd \\
  "${issueName}: Full TDD implementation with unit and integration tests"`;
  }

  private generateFixCommand(context: ProjectContext): string {
    const { lastCommit } = context.metadata;
    return `claude-flow sparc run dev \\
  "Bug Fix: ${lastCommit}. Write failing test first, then fix. Include regression test."`;
  }

  private generateRefactorCommand(context: ProjectContext): string {
    const { issueName } = context.openBranch;
    return `claude-flow sparc run refactor \\
  "${issueName}: Refactor with comprehensive test coverage. Tests must pass before and after."`;
  }

  private generateDevCommand(context: ProjectContext): string {
    const { issueName } = context.openBranch;
    return `claude-flow sparc run dev \\
  "${issueName}. Use context from project decisions: ${Object.keys(context.decisions).join(", ")}"`;
  }

  private generateAPICommand(context: ProjectContext): string {
    return `claude-flow sparc run api \\
  "REST API: Design endpoints, create models, write integration tests. Use SQLAlchemy for ORM."`;
  }

  private generateUICommand(context: ProjectContext): string {
    return `claude-flow sparc run ui \\
  "React Component: TypeScript, Tailwind CSS, React Query for server state. Write unit tests with Vitest."`;
  }
}

// Export instance for CLI usage
if (require.main === module) {
  const manager = new ProjectContextManager();
  const context = manager.analyze();

  console.log("\n=== PROJECT CONTEXT ===");
  console.log(JSON.stringify(context, null, 2));

  console.log("\n=== RECOMMENDED SPARC COMMANDS ===");
  const commands = manager.generateSparcCommands();
  commands.forEach((cmd, key) => {
    console.log(`\n[${key.toUpperCase()}]`);
    console.log(cmd);
  });

  console.log("\n=== RECOMMENDATIONS ===");
  manager.getRecommendations().forEach((rec) => {
    console.log(`\n${rec}`);
  });
}

export default ProjectContextManager;
