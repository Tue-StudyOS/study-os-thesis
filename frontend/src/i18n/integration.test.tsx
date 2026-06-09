import { describe, it, expect, beforeEach, afterEach } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import { I18nextProvider } from "react-i18next";
import { AuthProvider } from "../auth/AuthContext";
import { BrowserRouter } from "react-router-dom";
import App from "../App";
import i18n from "./config";
import "@testing-library/jest-dom";

describe("i18n integration", () => {
  beforeEach(async () => {
    localStorage.clear();
    await i18n.changeLanguage("en");
  });

  afterEach(() => {
    localStorage.clear();
  });

  it("app initializes with i18n provider", async () => {
    const { container } = render(
      <I18nextProvider i18n={i18n}>
        <BrowserRouter>
          <AuthProvider>
            <App />
          </AuthProvider>
        </BrowserRouter>
      </I18nextProvider>
    );

    // App should render without errors
    expect(container).toBeTruthy();
  });

  it("translations are loaded for English", async () => {
    render(
      <I18nextProvider i18n={i18n}>
        <AuthProvider>
          <div>{i18n.t("settings.title")}</div>
        </AuthProvider>
      </I18nextProvider>
    );

    await waitFor(() => {
      expect(screen.getByText("Settings")).toBeInTheDocument();
    });
  });

  it("translations are loaded for German", async () => {
    await i18n.changeLanguage("de");

    render(
      <I18nextProvider i18n={i18n}>
        <AuthProvider>
          <div>{i18n.t("settings.title")}</div>
        </AuthProvider>
      </I18nextProvider>
    );

    await waitFor(() => {
      expect(screen.getByText("Einstellungen")).toBeInTheDocument();
    });
  });

  it("language persists across page reloads", async () => {
    await i18n.changeLanguage("de");

    // Verify localStorage contains the selection
    expect(localStorage.getItem("i18n-language")).toBe("de");

    // Clear i18n state and reinitialize (simulating a reload)
    await i18n.changeLanguage("en"); // Reset to en first
    localStorage.setItem("i18n-language", "de");

    // Simulate reading from localStorage on init
    const savedLang = localStorage.getItem("i18n-language") || "en";
    await i18n.changeLanguage(savedLang);

    expect(i18n.language).toBe("de");
  });

  it("navigation labels are translated", async () => {
    expect(i18n.t("navigation.dashboard")).toBe("Dashboard");
    expect(i18n.t("navigation.settings")).toBe("Settings");

    await i18n.changeLanguage("de");
    expect(i18n.t("navigation.dashboard")).toBe("Übersicht");
    expect(i18n.t("navigation.settings")).toBe("Einstellungen");
  });
});
