import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import en from "./en.json";
import de from "./de.json";

const STORAGE_KEY = "i18n-language";

const getSavedLanguage = (): string => {
  if (typeof window === "undefined") return "en";
  return localStorage.getItem(STORAGE_KEY) || "en";
};

const saveLanguage = (lang: string): void => {
  if (typeof window === "undefined") return;
  localStorage.setItem(STORAGE_KEY, lang);
};

i18n.use(initReactI18next).init({
  resources: {
    en: { translation: en },
    de: { translation: de },
  },
  lng: getSavedLanguage(),
  fallbackLng: "en",
  interpolation: {
    escapeValue: false,
  },
});

i18n.on("languageChanged", (lng: string) => {
  saveLanguage(lng);
});

export const changeLanguage = async (lang: string): Promise<void> => {
  await i18n.changeLanguage(lang);
};

export const getLanguage = (): string => {
  return i18n.language;
};

export default i18n;
