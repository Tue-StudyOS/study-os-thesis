import { describe, it, expect, beforeEach } from "vitest";
import { renderHook, act } from "@testing-library/react";
import { useLanguage } from "./useLanguage";
import { I18nextProvider } from "react-i18next";
import i18n from "./config";

describe("useLanguage hook", () => {
  beforeEach(async () => {
    localStorage.clear();
    await i18n.changeLanguage("en");
  });

  it("returns current language", async () => {
    const wrapper = ({ children }: { children: React.ReactNode }) => (
      <I18nextProvider i18n={i18n}>{children}</I18nextProvider>
    );
    const { result } = renderHook(() => useLanguage(), { wrapper });

    expect(result.current.language).toBe("en");
  });

  it("provides available languages", async () => {
    const wrapper = ({ children }: { children: React.ReactNode }) => (
      <I18nextProvider i18n={i18n}>{children}</I18nextProvider>
    );
    const { result } = renderHook(() => useLanguage(), { wrapper });

    expect(result.current.availableLanguages).toContain("en");
    expect(result.current.availableLanguages).toContain("de");
  });

  it("switches language", async () => {
    const wrapper = ({ children }: { children: React.ReactNode }) => (
      <I18nextProvider i18n={i18n}>{children}</I18nextProvider>
    );
    const { result } = renderHook(() => useLanguage(), { wrapper });

    await act(async () => {
      await result.current.switchLanguage("de");
    });

    expect(result.current.language).toBe("de");
  });

  it("persists language preference to localStorage", async () => {
    const wrapper = ({ children }: { children: React.ReactNode }) => (
      <I18nextProvider i18n={i18n}>{children}</I18nextProvider>
    );
    const { result } = renderHook(() => useLanguage(), { wrapper });

    await act(async () => {
      await result.current.switchLanguage("de");
    });

    expect(localStorage.getItem("i18n-language")).toBe("de");
  });
});
