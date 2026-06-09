import { describe, it, expect, beforeEach } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { I18nextProvider } from "react-i18next";
import { AuthProvider } from "../auth/AuthContext";
import Settings from "./Settings";
import i18n from "../i18n/config";
import "@testing-library/jest-dom";

describe("Settings page", () => {
  beforeEach(async () => {
    localStorage.clear();
    await i18n.changeLanguage("en");
  });

  const renderSettings = () => {
    return render(
      <I18nextProvider i18n={i18n}>
        <AuthProvider>
          <Settings />
        </AuthProvider>
      </I18nextProvider>
    );
  };

  it("renders settings title", () => {
    renderSettings();
    // Check that settings tab is present
    expect(screen.getByTestId("settings-tab")).toBeInTheDocument();
  });

  it("displays both Settings and Help tabs", () => {
    renderSettings();
    expect(screen.getByTestId("settings-tab")).toBeInTheDocument();
    expect(screen.getByTestId("help-tab")).toBeInTheDocument();
  });

  it("displays Settings tab content by default", () => {
    renderSettings();
    expect(screen.getByTestId("settings-content")).toBeInTheDocument();
    expect(screen.getByText("Language")).toBeInTheDocument();
  });

  it("switches to Help tab when clicked", () => {
    renderSettings();
    const helpTab = screen.getByTestId("help-tab");
    fireEvent.click(helpTab);

    expect(screen.getByTestId("help-content")).toBeInTheDocument();
    expect(screen.getByText("Features")).toBeInTheDocument();
  });

  it("displays all Help sections", () => {
    renderSettings();
    const helpTab = screen.getByTestId("help-tab");
    fireEvent.click(helpTab);

    expect(screen.getByText("Features")).toBeInTheDocument();
    expect(screen.getByText("Troubleshooting")).toBeInTheDocument();
    expect(screen.getByText("Frequently Asked Questions")).toBeInTheDocument();
  });

  it("displays feature items in Help tab", () => {
    renderSettings();
    const helpTab = screen.getByTestId("help-tab");
    fireEvent.click(helpTab);

    expect(screen.getByText("Dashboard")).toBeInTheDocument();
    expect(screen.getByText("Find Thesis")).toBeInTheDocument();
    expect(screen.getByText("Chair Explorer")).toBeInTheDocument();
    expect(screen.getByText("My Proposals")).toBeInTheDocument();
  });

  it("displays troubleshooting items in Help tab", () => {
    renderSettings();
    const helpTab = screen.getByTestId("help-tab");
    fireEvent.click(helpTab);

    expect(
      screen.getByText("Why is my transcript not processing?")
    ).toBeInTheDocument();
    expect(
      screen.getByText("I don't see any proposals. What should I do?")
    ).toBeInTheDocument();
  });

  it("displays FAQ items in Help tab", () => {
    renderSettings();
    const helpTab = screen.getByTestId("help-tab");
    fireEvent.click(helpTab);

    expect(
      screen.getByText("What is my competency profile?")
    ).toBeInTheDocument();
    expect(
      screen.getByText("How do I start developing a thesis proposal?")
    ).toBeInTheDocument();
    expect(
      screen.getByText("Can I switch between languages?")
    ).toBeInTheDocument();
  });

  it("switches back to Settings tab", () => {
    renderSettings();
    const helpTab = screen.getByTestId("help-tab");
    fireEvent.click(helpTab);

    const settingsTab = screen.getByTestId("settings-tab");
    fireEvent.click(settingsTab);

    expect(screen.getByTestId("settings-content")).toBeInTheDocument();
    expect(screen.getByText("Language")).toBeInTheDocument();
  });

  it("displays language selection", () => {
    renderSettings();
    expect(screen.getByText("English")).toBeInTheDocument();
    expect(screen.getByText("Deutsch")).toBeInTheDocument();
  });

  it("marks current language as selected", () => {
    renderSettings();
    const currentLang = screen.getByRole("button", { name: /English/i });
    expect(currentLang).toHaveClass("border-primary");
  });

  it("allows switching to German", async () => {
    const { rerender } = renderSettings();

    const germanButton = screen.getByRole("button", { name: /Deutsch/i });
    fireEvent.click(germanButton);

    // Wait for language to change and rerender
    await i18n.changeLanguage("de");
    rerender(
      <I18nextProvider i18n={i18n}>
        <AuthProvider>
          <Settings />
        </AuthProvider>
      </I18nextProvider>
    );

    expect(localStorage.getItem("i18n-language")).toBe("de");
  });

  it("allows switching back to English", async () => {
    await i18n.changeLanguage("de");
    const { rerender } = renderSettings();

    const englishButton = screen.getByRole("button", { name: /English/i });
    fireEvent.click(englishButton);

    await i18n.changeLanguage("en");
    rerender(
      <I18nextProvider i18n={i18n}>
        <AuthProvider>
          <Settings />
        </AuthProvider>
      </I18nextProvider>
    );

    expect(localStorage.getItem("i18n-language")).toBe("en");
  });

  it("displays Help content in German when language is switched", async () => {
    const { rerender } = renderSettings();

    await i18n.changeLanguage("de");
    rerender(
      <I18nextProvider i18n={i18n}>
        <AuthProvider>
          <Settings />
        </AuthProvider>
      </I18nextProvider>
    );

    const helpTab = screen.getByTestId("help-tab");
    fireEvent.click(helpTab);

    expect(screen.getByText("Funktionen")).toBeInTheDocument();
    expect(screen.getByText("Fehlerbehebung")).toBeInTheDocument();
    expect(screen.getByText("Häufig gestellte Fragen")).toBeInTheDocument();
  });

  it("displays German feature items in Help tab", async () => {
    const { rerender } = renderSettings();

    await i18n.changeLanguage("de");
    rerender(
      <I18nextProvider i18n={i18n}>
        <AuthProvider>
          <Settings />
        </AuthProvider>
      </I18nextProvider>
    );

    const helpTab = screen.getByTestId("help-tab");
    fireEvent.click(helpTab);

    expect(screen.getByText("Übersicht")).toBeInTheDocument();
    expect(screen.getByText("Thesis finden")).toBeInTheDocument();
    expect(screen.getByText("Lehrstuhl-Explorer")).toBeInTheDocument();
    expect(screen.getByText("Meine Anträge")).toBeInTheDocument();
  });
});
