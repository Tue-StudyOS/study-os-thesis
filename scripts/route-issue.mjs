#!/usr/bin/env node
/**
 * Route GitHub issues to optimal Claude Code / SPARC commands
 * Usage: node scripts/route-issue.mjs [issue-number]
 *        node scripts/route-issue.mjs  (shows all open issues with suggestions)
 */

import { execSync } from "child_process";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(__dirname, "..");

// ─────────────────────────────────────────────────────────────
// Helpers
// ─────────────────────────────────────────────────────────────

function runCmd(cmd) {
  try {
    return execSync(cmd, { encoding: "utf-8", stdio: "pipe" });
  } catch (e) {
    console.error(`Error running: ${cmd}`);
    console.error(e.message);
    process.exit(1);
  }
}

function getIssue(issueNumber) {
  const json = runCmd(
    `gh issue view ${issueNumber} --json number,title,body,labels`
  );
  return JSON.parse(json);
}

function listOpenIssues() {
  const json = runCmd(
    `gh issue list --state open --json number,title,body,labels --limit 20`
  );
  return JSON.parse(json);
}

// ─────────────────────────────────────────────────────────────
// Complexity Analysis
// ─────────────────────────────────────────────────────────────

function analyzeComplexity(issue) {
  const body = issue.body || "";
  const title = issue.title || "";
  const labels = issue.labels.map((l) => l.name);

  let score = 0;
  let signals = [];

  // Length signals
  const bodyLength = body.length;
  if (bodyLength > 300) {
    score += 2;
    signals.push("✓ detailed body");
  } else if (bodyLength > 100) {
    score += 1;
    signals.push("~ moderate length");
  } else {
    signals.push("✗ short description");
  }

  // Structure signals
  if (
    body.includes("done when") ||
    body.includes("acceptance criteria") ||
    body.includes("Acceptance Criteria") ||
    body.includes("AC:")
  ) {
    score += 3;
    signals.push("✓ has acceptance criteria");
  }

  if (
    body.includes("Given") ||
    body.includes("When") ||
    body.includes("Then")
  ) {
    score += 2;
    signals.push("✓ BDD format");
  }

  if (
    body.includes("Steps") ||
    body.includes("steps") ||
    body.includes("Reproduce") ||
    body.includes("reproduction")
  ) {
    score += 2;
    signals.push("✓ has steps/repro");
  }

  if (body.includes("Test") || body.includes("test")) {
    score += 1;
    signals.push("✓ mentions tests");
  }

  // Label signals
  if (labels.includes("feature")) {
    score += 1;
    signals.push("type: feature");
  } else if (labels.includes("bug")) {
    score += 0;
    signals.push("type: bug");
  } else if (labels.includes("chore")) {
    score -= 1;
    signals.push("type: chore");
  }

  // Multi-part signals
  if (
    (body.match(/-\s/g) || []).length >= 3 ||
    (body.match(/\n/g) || []).length > 5
  ) {
    score += 1;
    signals.push("✓ multiple components");
  }

  return { score, signals, bodyLength };
}

// ─────────────────────────────────────────────────────────────
// Routing Logic
// ─────────────────────────────────────────────────────────────

function routeIssue(issue) {
  const { score, signals, bodyLength } = analyzeComplexity(issue);
  const labels = issue.labels.map((l) => l.name);
  const title = issue.title;

  // Detect issue type
  let issueType = "feature";
  if (labels.includes("bug")) issueType = "bug";
  else if (labels.includes("docs")) issueType = "docs";
  else if (labels.includes("chore")) issueType = "chore";

  // Extract area prefix from title (e.g., "backend: ", "UI: ")
  const areaMatch = title.match(/^([a-zA-Z]+):\s/);
  const area = areaMatch ? areaMatch[1].toLowerCase() : null;

  // Generate branch name
  const titleSlug = title
    .toLowerCase()
    .replace(/^[a-z]+:\s/, "") // remove area prefix
    .replace(/[^a-z0-9]+/g, "-")
    .substring(0, 40)
    .replace(/-+$/, "");

  const prefixMap = {
    bug: "fix",
    docs: "docs",
    chore: "chore",
    feature: "feat",
  };
  const branchPrefix = prefixMap[issueType] || "feat";
  const branchName = `${branchPrefix}/${issue.number}-${titleSlug}`;

  // ─ Decision Logic ─
  let recommendation = {};

  if (score >= 6) {
    // Well-structured, detailed issue → SPARC
    let sparc_mode = "tdd";

    if (issueType === "docs") {
      sparc_mode = "dev"; // Documentation
    } else if (title.match(/api|endpoint|rest|http/i)) {
      sparc_mode = "api"; // REST endpoints
    } else if (title.match(/ui|component|button|form|page|screen/i)) {
      sparc_mode = "ui"; // UI components
    } else if (issueType === "bug") {
      sparc_mode = "tdd"; // TDD for bug fix (test first)
    }

    recommendation = {
      approach: "SPARC",
      mode: sparc_mode,
      confidence: "high",
      reason: `Well-structured issue with clear requirements (score: ${score})`,
    };
  } else if (score >= 3) {
    // Moderate complexity → SPARC or Normal depending on type
    if (issueType === "feature" && bodyLength > 150) {
      recommendation = {
        approach: "SPARC",
        mode: "dev",
        confidence: "medium",
        reason: `Moderate complexity. Could benefit from SPARC structure (score: ${score})`,
      };
    } else {
      recommendation = {
        approach: "CLAUDE",
        command: "/code-review",
        confidence: "medium",
        reason: `Moderate issue. Consider clarifying with acceptance criteria (score: ${score})`,
      };
    }
  } else {
    // Low complexity → Normal Claude Code
    recommendation = {
      approach: "CLAUDE",
      command: issueType === "bug" ? "/verify" : "/code-review",
      confidence: "low",
      reason: `Issue needs more structure. Recommend clarifying with acceptance criteria first (score: ${score})`,
    };
  }

  return {
    issue: {
      number: issue.number,
      title,
      type: issueType,
      area,
    },
    analysis: {
      score,
      signals,
      bodyLength,
    },
    branch: branchName,
    recommendation,
  };
}

// ─────────────────────────────────────────────────────────────
// Output
// ─────────────────────────────────────────────────────────────

function printResult(result) {
  const { issue, analysis, branch, recommendation } = result;

  console.log("\n" + "═".repeat(70));
  console.log(`📌 Issue #${issue.number}: ${issue.title}`);
  console.log("═".repeat(70));

  // Analysis
  console.log(`\n📊 Analysis (complexity score: ${analysis.score}/10):`);
  analysis.signals.forEach((signal) => console.log(`   ${signal}`));

  // Branch
  console.log(`\n🌳 Branch: ${branch}`);

  // Recommendation
  console.log(`\n🎯 Recommendation: ${recommendation.approach}`);
  console.log(`   Confidence: ${recommendation.confidence}`);
  console.log(`   Reason: ${recommendation.reason}`);

  // Suggested command
  if (recommendation.approach === "SPARC") {
    const cmd = `/sparc:${recommendation.mode} "${issue.title}"`;
    console.log(`\n💾 Next steps:`);
    console.log(`   1. git checkout -b ${branch}`);
    console.log(`   2. ${cmd}`);
    console.log(`   3. git add . && git commit -m "feat: ${issue.title}"`);
  } else {
    const cmd = recommendation.command;
    console.log(`\n💾 Next steps:`);
    console.log(`   1. git checkout -b ${branch}`);
    console.log(`   2. ${cmd}`);
    console.log(`   3. Push & create PR with 'Closes #${issue.number}'`);
  }

  console.log("\n" + "═".repeat(70) + "\n");
}

function printSummaryTable(results) {
  console.log("\n" + "═".repeat(90));
  console.log(
    "📋 OPEN ISSUES — Routing Summary".padEnd(90)
  );
  console.log("═".repeat(90));
  console.log(
    "#\tTitle\t\t\t\tComplexity\tApproach\tBranch".padEnd(90)
  );
  console.log(
    "─".repeat(90)
  );

  results.forEach((r) => {
    const title = r.issue.title.substring(0, 25).padEnd(25);
    const complexity = `${r.analysis.score}/10`.padEnd(12);
    const approach = r.recommendation.approach.padEnd(8);
    const branch = r.branch.substring(0, 30);

    console.log(
      `#${r.issue.number}\t${title}\t${complexity}\t${approach}\t${branch}`
    );
  });

  console.log("═".repeat(90));
  console.log("Run: node scripts/route-issue.mjs <number> for detailed view\n");
}

// ─────────────────────────────────────────────────────────────
// Main
// ─────────────────────────────────────────────────────────────

async function main() {
  const issueNumber = process.argv[2];

  if (issueNumber) {
    // Single issue detailed view
    const issue = getIssue(issueNumber);
    const result = routeIssue(issue);
    printResult(result);
  } else {
    // All open issues summary
    const issues = listOpenIssues();
    const results = issues.map(routeIssue);
    printSummaryTable(results);

    // Print top 3 recommendations
    console.log("🚀 Top recommendations:\n");
    results
      .filter((r) => r.recommendation.confidence === "high")
      .slice(0, 3)
      .forEach((r) => {
        if (r.recommendation.approach === "SPARC") {
          console.log(`   ✅ #${r.issue.number}: SPARC ${r.recommendation.mode}`);
          console.log(
            `      $ claude-flow sparc run ${r.recommendation.mode} "${r.issue.title}"`
          );
        } else {
          console.log(`   ⚙️  #${r.issue.number}: ${r.recommendation.command}`);
        }
      });
    console.log();
  }
}

main().catch(console.error);
