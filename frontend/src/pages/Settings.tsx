import { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";
import TopBar from "../components/TopBar";
import { useLanguage } from "../i18n/useLanguage";
import { getStudentProfile, updateStudentProfile } from "../api/students";

type Tab = "settings" | "help";

export default function Settings() {
  const { t } = useTranslation();
  const { language, switchLanguage, availableLanguages } = useLanguage();
  const [activeTab, setActiveTab] = useState<Tab>("settings");
  const [name, setName] = useState("");
  const [educationLevel, setEducationLevel] = useState<"bachelor" | "master">("bachelor");
  const [program, setProgram] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [isSaving, setIsSaving] = useState(false);

  // Load values from API and localStorage on mount
  useEffect(() => {
    const loadProfile = async () => {
      try {
        const profile = await getStudentProfile();
        if (profile.full_name) setName(profile.full_name);
        if (profile.education_level) setEducationLevel(profile.education_level as "bachelor" | "master");
        if (profile.program) setProgram(profile.program);
      } catch {
        // If profile doesn't exist (404), fall back to localStorage
        const savedName = localStorage.getItem("settings.name");
        const savedEducationLevel = localStorage.getItem("settings.educationLevel");
        const savedProgram = localStorage.getItem("settings.program");

        if (savedName) setName(savedName);
        if (savedEducationLevel) setEducationLevel(savedEducationLevel as "bachelor" | "master");
        if (savedProgram) setProgram(savedProgram);
      } finally {
        setLoading(false);
      }
    };
    setLoading(true);
    void loadProfile();
  }, []);

  // Save to both database and localStorage
  const saveProfile = async () => {
    setIsSaving(true);
    setError(null);
    setSuccess(null);
    try {
      await updateStudentProfile(name, educationLevel, program);
      localStorage.setItem("settings.name", name);
      localStorage.setItem("settings.educationLevel", educationLevel);
      localStorage.setItem("settings.program", program);
      setSuccess(t("settings.saved"));
      setTimeout(() => setSuccess(null), 3000);
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : t("settings.saveFailed");
      setError(errorMsg);
    } finally {
      setIsSaving(false);
    }
  };

  // Save name to database and localStorage
  const handleNameChange = (value: string) => {
    setName(value);
  };

  // Save education level to database and localStorage
  const handleEducationLevelChange = (value: "bachelor" | "master") => {
    setEducationLevel(value);
  };

  // Save program to database and localStorage
  const handleProgramChange = (value: string) => {
    setProgram(value);
  };

  return (
    <div className="flex flex-col h-full bg-background">
      <TopBar title={t("settings.title")} showSearch={false} />
      <div className="flex-1 overflow-auto p-6">
        <div className="max-w-2xl">
          {/* Tab buttons */}
          <div className="flex gap-2 mb-6 border-b border-outline">
            <button
              onClick={() => setActiveTab("settings")}
              className={`px-4 py-3 font-medium text-sm transition-colors relative ${
                activeTab === "settings"
                  ? "text-primary"
                  : "text-on-surface-variant hover:text-on-surface"
              }`}
              data-testid="settings-tab"
            >
              {t("settings.tabs.settings")}
              {activeTab === "settings" && (
                <div className="absolute bottom-0 left-0 right-0 h-1 bg-primary rounded-t" />
              )}
            </button>
            <button
              onClick={() => setActiveTab("help")}
              className={`px-4 py-3 font-medium text-sm transition-colors relative ${
                activeTab === "help"
                  ? "text-primary"
                  : "text-on-surface-variant hover:text-on-surface"
              }`}
              data-testid="help-tab"
            >
              {t("settings.tabs.help")}
              {activeTab === "help" && (
                <div className="absolute bottom-0 left-0 right-0 h-1 bg-primary rounded-t" />
              )}
            </button>
          </div>

          {/* Settings Tab */}
          {activeTab === "settings" && (
            <div className="space-y-6" data-testid="settings-content">
              {/* User Profile Section */}
              <div className="bg-surface rounded-lg p-6 shadow-sm border border-outline">
                <h2 className="text-lg font-semibold text-on-surface mb-6">
                  {t("settings.profile.title")}
                </h2>

                <div className="space-y-5">
                  {/* Name Field */}
                  <div>
                    <label className="block text-sm font-medium text-on-surface mb-2">
                      {t("settings.name.label")} *
                    </label>
                    <input
                      type="text"
                      value={name}
                      onChange={(e) => handleNameChange(e.target.value)}
                      placeholder={t("settings.name.placeholder")}
                      className="w-full px-4 py-3 rounded-lg border border-outline bg-surface text-on-surface placeholder-on-surface-variant focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/20 transition-colors"
                      data-testid="name-field"
                      disabled={isSaving}
                    />
                  </div>

                  {/* Education Level Dropdown */}
                  <div>
                    <label className="block text-sm font-medium text-on-surface mb-2">
                      {t("settings.educationLevel.label")}
                    </label>
                    <select
                      value={educationLevel}
                      onChange={(e) => handleEducationLevelChange(e.target.value as "bachelor" | "master")}
                      className="w-full px-4 py-3 rounded-lg border border-outline bg-surface text-on-surface focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/20 transition-colors"
                      data-testid="education-level-select"
                      disabled={isSaving}
                    >
                      <option value="bachelor">{t("settings.educationLevel.bachelor")}</option>
                      <option value="master">{t("settings.educationLevel.master")}</option>
                    </select>
                  </div>

                  {/* Program Field */}
                  <div>
                    <label className="block text-sm font-medium text-on-surface mb-2">
                      {t("settings.program.label")}
                    </label>
                    <input
                      type="text"
                      value={program}
                      onChange={(e) => handleProgramChange(e.target.value)}
                      placeholder={t("settings.program.placeholder")}
                      className="w-full px-4 py-3 rounded-lg border border-outline bg-surface text-on-surface placeholder-on-surface-variant focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/20 transition-colors"
                      data-testid="program-field"
                      disabled={isSaving}
                    />
                  </div>

                  {/* Status Messages */}
                  {error && (
                    <div className="p-3 rounded-lg bg-error/10 border border-error text-error text-sm">
                      {error}
                    </div>
                  )}
                  {success && (
                    <div className="p-3 rounded-lg bg-tertiary-container/20 border border-tertiary-container text-tertiary-container text-sm">
                      {success}
                    </div>
                  )}

                  {/* Save Button */}
                  <button
                    onClick={() => void saveProfile()}
                    disabled={isSaving || loading}
                    className="w-full px-4 py-3 rounded-lg bg-primary text-on-primary font-medium text-sm hover:bg-primary-dark disabled:bg-outline-variant disabled:text-on-surface-variant transition-colors"
                    data-testid="save-profile-button"
                  >
                    {isSaving ? t("settings.saving") : t("settings.save")}
                  </button>
                </div>
              </div>

              {/* Language Section */}
              <div className="bg-surface rounded-lg p-6 shadow-sm border border-outline">
                <h2 className="text-lg font-semibold text-on-surface mb-4">
                  {t("settings.language")}
                </h2>
                <p className="text-sm text-on-surface-variant mb-6">
                  {t("settings.languageDescription")}
                </p>

                <div className="space-y-3">
                  {availableLanguages.map((lang) => (
                    <button
                      key={lang}
                      onClick={() => switchLanguage(lang)}
                      className={`w-full text-left px-4 py-3 rounded-lg border-2 transition-colors ${
                        language === lang
                          ? "border-primary bg-primary-container text-on-primary-container"
                          : "border-outline bg-surface text-on-surface hover:border-primary hover:bg-primary-container hover:bg-opacity-20"
                      }`}
                    >
                      <span className="font-medium">
                        {lang === "en" ? t("common.english") : t("common.german")}
                      </span>
                      {language === lang && (
                        <span className="ml-2 text-xs">
                          ✓ {t("common.language")}
                        </span>
                      )}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Help Tab */}
          {activeTab === "help" && (
            <div className="space-y-6" data-testid="help-content">
              {/* Features Section */}
              <div className="bg-surface rounded-lg p-6 shadow-sm border border-outline">
                <h2 className="text-lg font-semibold text-on-surface mb-4">
                  {t("settings.help.features.title")}
                </h2>
                <div className="space-y-4">
                  {[
                    { key: "dashboard", icon: "dashboard" },
                    { key: "findThesis", icon: "chat" },
                    { key: "chairExplorer", icon: "school" },
                    { key: "proposals", icon: "description" },
                  ].map(({ key, icon }) => (
                    <div
                      key={key}
                      className="pb-4 border-b border-outline-variant last:pb-0 last:border-b-0"
                    >
                      <div className="flex gap-3">
                        <span className="material-symbols-outlined text-primary mt-1 flex-shrink-0">
                          {icon}
                        </span>
                        <div>
                          <h3 className="font-medium text-on-surface">
                            {t(
                              `settings.help.features.${key}.title` as const
                            )}
                          </h3>
                          <p className="text-sm text-on-surface-variant mt-1">
                            {t(
                              `settings.help.features.${key}.description` as const
                            )}
                          </p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Troubleshooting Section */}
              <div className="bg-surface rounded-lg p-6 shadow-sm border border-outline">
                <h2 className="text-lg font-semibold text-on-surface mb-4">
                  {t("settings.help.troubleshooting.title")}
                </h2>
                <div className="space-y-4">
                  {[
                    "transcriptNotProcessing",
                    "noProposals",
                    "aiResponse",
                  ].map((key) => (
                    <div
                      key={key}
                      className="pb-4 border-b border-outline-variant last:pb-0 last:border-b-0"
                    >
                      <h3 className="font-medium text-on-surface">
                        {t(
                          `settings.help.troubleshooting.${key}.question` as const
                        )}
                      </h3>
                      <p className="text-sm text-on-surface-variant mt-2">
                        {t(
                          `settings.help.troubleshooting.${key}.answer` as const
                        )}
                      </p>
                    </div>
                  ))}
                </div>
              </div>

              {/* FAQ Section */}
              <div className="bg-surface rounded-lg p-6 shadow-sm border border-outline">
                <h2 className="text-lg font-semibold text-on-surface mb-4">
                  {t("settings.help.faq.title")}
                </h2>
                <div className="space-y-4">
                  {[
                    "whatIsCompetency",
                    "howToStartProposal",
                    "changeLanguage",
                    "contactSupport",
                  ].map((key) => (
                    <div
                      key={key}
                      className="pb-4 border-b border-outline-variant last:pb-0 last:border-b-0"
                    >
                      <h3 className="font-medium text-on-surface">
                        {t(`settings.help.faq.${key}.question` as const)}
                      </h3>
                      <p className="text-sm text-on-surface-variant mt-2">
                        {t(`settings.help.faq.${key}.answer` as const)}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
