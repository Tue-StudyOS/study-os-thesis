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
    const title = screen.getByText("Settings");
    expect(title).toBeInTheDocument();
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
});
