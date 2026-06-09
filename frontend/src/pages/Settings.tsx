import { useTranslation } from "react-i18next";
import TopBar from "../components/TopBar";
import { useLanguage } from "../i18n/useLanguage";

export default function Settings() {
  const { t } = useTranslation();
  const { language, switchLanguage, availableLanguages } = useLanguage();

  return (
    <div className="flex flex-col h-full bg-background">
      <TopBar title={t("settings.title")} />
      <div className="flex-1 overflow-auto p-6">
        <div className="max-w-2xl">
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
      </div>
    </div>
  );
}
