import { useState, useCallback } from "react";
import { useTranslation } from "react-i18next";

export function useLanguage() {
  const { i18n } = useTranslation();
  const [language, setLanguage] = useState(i18n.language);

  const switchLanguage = useCallback(
    async (lang: string) => {
      await i18n.changeLanguage(lang);
      setLanguage(lang);
    },
    [i18n]
  );

  return {
    language,
    switchLanguage,
    availableLanguages: ["en", "de"] as const,
  };
}
