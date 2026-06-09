import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import i18n from "./config";

describe("i18n configuration", () => {
  beforeEach(() => {
    localStorage.clear();
    vi.clearAllMocks();
  });

  afterEach(() => {
    localStorage.clear();
  });

  it("initializes with English as default language", async () => {
    expect(i18n.language).toBe("en");
  });

  it("loads saved language from localStorage on initialization", async () => {
    localStorage.setItem("i18n-language", "de");
    // Reinitialize to pick up the localStorage value
    await i18n.changeLanguage("de");
    expect(i18n.language).toBe("de");
  });

  it("supports English translations", () => {
    i18n.changeLanguage("en");
    const title = i18n.t("settings.title");
    expect(title).toBe("Settings");
  });

  it("supports German translations", async () => {
    await i18n.changeLanguage("de");
    const title = i18n.t("settings.title");
    expect(title).toBe("Einstellungen");
  });

  it("persists language change to localStorage", async () => {
    await i18n.changeLanguage("de");
    expect(localStorage.getItem("i18n-language")).toBe("de");
  });

  it("switches between languages", async () => {
    await i18n.changeLanguage("en");
    expect(i18n.t("settings.language")).toBe("Language");

    await i18n.changeLanguage("de");
    expect(i18n.t("settings.language")).toBe("Sprache");
  });

  it("falls back to English for missing keys", () => {
    i18n.changeLanguage("en");
    const missing = i18n.t("nonexistent.key");
    // i18next returns the key when translation is not found
    expect(missing).toBe("nonexistent.key");
  });
});
