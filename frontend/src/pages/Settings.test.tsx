import { describe, it, expect, beforeEach, vi } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { I18nextProvider } from "react-i18next";
import { AuthProvider } from "../auth/AuthContext";
import Settings from "./Settings";
import i18n from "../i18n/config";
import * as studentsApi from "../api/students";
import "@testing-library/jest-dom";

describe("Settings page", () => {
  beforeEach(async () => {
    localStorage.clear();
    await i18n.changeLanguage("en");
    vi.clearAllMocks();
    // Mock getStudentProfile to return no profile (404)
    vi.spyOn(studentsApi, "getStudentProfile").mockRejectedValue(new Error("Not found"));
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
    expect(screen.getByText("User Profile")).toBeInTheDocument();
    expect(screen.getByText("Language")).toBeInTheDocument();
  });

  it("renders name field", () => {
    renderSettings();
    expect(screen.getByTestId("name-field")).toBeInTheDocument();
    expect(screen.getByText("Full Name *")).toBeInTheDocument();
  });

  it("renders education level dropdown with Bachelor and Master options", () => {
    renderSettings();
    const select = screen.getByTestId("education-level-select") as HTMLSelectElement;
    expect(select).toBeInTheDocument();
    expect(screen.getByText("Education Level")).toBeInTheDocument();
    expect(select.options?.[0]?.text).toBe("Bachelor");
    expect(select.options?.[1]?.text).toBe("Master");
  });

  it("renders program field", () => {
    renderSettings();
    expect(screen.getByTestId("program-field")).toBeInTheDocument();
    expect(screen.getByText("Program/Field of Study")).toBeInTheDocument();
  });

  it("saves name to localStorage on input", () => {
    renderSettings();
    const nameField = screen.getByTestId("name-field") as HTMLInputElement;
    fireEvent.change(nameField, { target: { value: "John Doe" } });
    expect(localStorage.getItem("settings.name")).toBe("John Doe");
    expect(nameField.value).toBe("John Doe");
  });

  it("saves education level to localStorage on select", () => {
    renderSettings();
    const select = screen.getByTestId("education-level-select") as HTMLSelectElement;
    fireEvent.change(select, { target: { value: "master" } });
    expect(localStorage.getItem("settings.educationLevel")).toBe("master");
    expect(select.value).toBe("master");
  });

  it("saves program to localStorage on input", () => {
    renderSettings();
    const programField = screen.getByTestId("program-field") as HTMLInputElement;
    fireEvent.change(programField, { target: { value: "Computer Science" } });
    expect(localStorage.getItem("settings.program")).toBe("Computer Science");
    expect(programField.value).toBe("Computer Science");
  });

  it("loads values from localStorage on mount", () => {
    localStorage.setItem("settings.name", "Jane Smith");
    localStorage.setItem("settings.educationLevel", "master");
    localStorage.setItem("settings.program", "Physics");

    renderSettings();

    const nameField = screen.getByTestId("name-field") as HTMLInputElement;
    const select = screen.getByTestId("education-level-select") as HTMLSelectElement;
    const programField = screen.getByTestId("program-field") as HTMLInputElement;

    expect(nameField.value).toBe("Jane Smith");
    expect(select.value).toBe("master");
    expect(programField.value).toBe("Physics");
  });

  it("persists values after reload (simulated with localStorage)", () => {
    const { unmount } = renderSettings();

    const nameField = screen.getByTestId("name-field") as HTMLInputElement;
    const select = screen.getByTestId("education-level-select") as HTMLSelectElement;
    const programField = screen.getByTestId("program-field") as HTMLInputElement;

    fireEvent.change(nameField, { target: { value: "Alex Johnson" } });
    fireEvent.change(select, { target: { value: "bachelor" } });
    fireEvent.change(programField, { target: { value: "Mathematics" } });

    // Simulate unmounting
    unmount();

    // Simulate remounting (new render after reload)
    renderSettings();

    const newNameField = screen.getByTestId("name-field") as HTMLInputElement;
    const newSelect = screen.getByTestId("education-level-select") as HTMLSelectElement;
    const newProgramField = screen.getByTestId("program-field") as HTMLInputElement;

    expect(newNameField.value).toBe("Alex Johnson");
    expect(newSelect.value).toBe("bachelor");
    expect(newProgramField.value).toBe("Mathematics");
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

  it("saves profile to database on save button click", async () => {
    const mockUpdate = vi.spyOn(studentsApi, "updateStudentProfile").mockResolvedValue({
      user_id: 1,
      full_name: "John Doe",
      education_level: "master",
      program: "Computer Science",
      semester: null,
      gpa: null,
      updated_at: new Date().toISOString(),
      courses: [],
    });

    renderSettings();

    const nameField = screen.getByTestId("name-field") as HTMLInputElement;
    const select = screen.getByTestId("education-level-select") as HTMLSelectElement;
    const programField = screen.getByTestId("program-field") as HTMLInputElement;

    fireEvent.change(nameField, { target: { value: "John Doe" } });
    fireEvent.change(select, { target: { value: "master" } });
    fireEvent.change(programField, { target: { value: "Computer Science" } });

    const saveButton = screen.getByTestId("save-profile-button");
    fireEvent.click(saveButton);

    await waitFor(() => {
      expect(mockUpdate).toHaveBeenCalledWith("John Doe", "master", "Computer Science");
    });

    expect(localStorage.getItem("settings.name")).toBe("John Doe");
    expect(localStorage.getItem("settings.educationLevel")).toBe("master");
    expect(localStorage.getItem("settings.program")).toBe("Computer Science");
  });

  it("displays success message after save", async () => {
    vi.spyOn(studentsApi, "updateStudentProfile").mockResolvedValue({
      user_id: 1,
      full_name: "Jane Smith",
      education_level: "bachelor",
      program: "Physics",
      semester: null,
      gpa: null,
      updated_at: new Date().toISOString(),
      courses: [],
    });

    renderSettings();

    const nameField = screen.getByTestId("name-field") as HTMLInputElement;
    fireEvent.change(nameField, { target: { value: "Jane Smith" } });

    const saveButton = screen.getByTestId("save-profile-button");
    fireEvent.click(saveButton);

    await waitFor(() => {
      expect(screen.getByText("Saved successfully")).toBeInTheDocument();
    });
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
