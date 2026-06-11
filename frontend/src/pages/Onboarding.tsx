import { useMemo, useState } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";
import {
  getOnboardingProfile,
  clearOnboardingPrefill,
  getOnboardingPrefill,
  inferNameFromEmail,
  isLikelyInTuebingen,
  saveOnboardingProfile,
  type TuebingenResidence,
} from "../onboarding";

export default function Onboarding() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const existingProfile = getOnboardingProfile(user);
  const [prefill] = useState(() => getOnboardingPrefill());
  const inferredName = useMemo(() => (user ? inferNameFromEmail(user.email) : ""), [user]);
  const [displayName, setDisplayName] = useState(existingProfile?.displayName ?? prefill?.displayName ?? inferredName);
  const [degree, setDegree] = useState(existingProfile?.degree ?? "");
  const [semester, setSemester] = useState(existingProfile?.semester ?? "");
  const [livesInTuebingen, setLivesInTuebingen] = useState<TuebingenResidence>(
    existingProfile?.livesInTuebingen ?? "unknown",
  );
  const [locationSource, setLocationSource] = useState<"manual" | "browser" | null>(
    existingProfile?.locationSource ?? null,
  );
  const [locationStatus, setLocationStatus] = useState<string | null>(null);
  const [busyLocation, setBusyLocation] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (!user) return <Navigate to="/login" replace />;
  if (existingProfile) return <Navigate to="/dashboard" replace />;

  function useCurrentLocation() {
    setLocationStatus(null);
    setError(null);

    if (!navigator.geolocation) {
      setLocationStatus("Dein Browser unterstützt Standortfreigabe nicht.");
      return;
    }

    setBusyLocation(true);
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const inTuebingen = isLikelyInTuebingen(
          position.coords.latitude,
          position.coords.longitude,
        );
        setLivesInTuebingen(inTuebingen ? "yes" : "no");
        setLocationSource("browser");
        setLocationStatus(
          inTuebingen
            ? "Standort erkannt: wahrscheinlich in Tübingen."
            : "Standort erkannt: wahrscheinlich nicht in Tübingen.",
        );
        setBusyLocation(false);
      },
      () => {
        setLocationStatus("Standort konnte nicht gelesen werden. Bitte wähle manuell.");
        setBusyLocation(false);
      },
      { enableHighAccuracy: false, maximumAge: 300000, timeout: 8000 },
    );
  }

  function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);

    if (!user) return;

    if (!displayName.trim() || !degree.trim()) {
      setError("Bitte gib deinen Namen und Studiengang an.");
      return;
    }

    if (livesInTuebingen === "unknown") {
      setError("Bitte bestätige, ob du in Tübingen wohnst.");
      return;
    }

    saveOnboardingProfile(user, {
      displayName: displayName.trim(),
      degree: degree.trim(),
      semester: semester.trim(),
      livesInTuebingen,
      locationSource: locationSource ?? "manual",
      completedAt: new Date().toISOString(),
    });
    clearOnboardingPrefill();
    navigate("/dashboard", { replace: true });
  }

  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4">
      <div className="w-full max-w-2xl">
        <div className="flex items-center justify-center gap-3 mb-8">
          <div className="w-10 h-10 rounded-lg bg-primary flex items-center justify-center">
            <span
              className="material-symbols-outlined text-on-primary"
              style={{ fontVariationSettings: "'FILL' 1" }}
            >
              school
            </span>
          </div>
          <div>
            <h1 className="text-headline-md font-headline-md font-bold text-primary tracking-tight">
              ScholarAI
            </h1>
            <p className="font-label-md text-label-md text-on-surface-variant uppercase tracking-widest">
              University Onboarding
            </p>
          </div>
        </div>

        <div className="bg-surface-container-lowest border border-outline-variant rounded-xl p-6 sm:p-8 ambient-shadow">
          <div className="flex items-start gap-4 mb-6">
            <span className="material-symbols-outlined text-primary text-[32px]">badge</span>
            <div>
              <h2 className="font-headline-md text-headline-md text-on-surface font-semibold mb-1">
                Richte dein Profil ein
              </h2>
              <p className="font-body-sm text-body-sm text-on-surface-variant">
                Wir nutzen deine Uni-Anmeldung als Startpunkt und ergänzen die Angaben,
                die ScholarAI für bessere Vorschläge braucht.
              </p>
            </div>
          </div>

          {error && (
            <div className="bg-error-container text-on-error-container border border-error/30 rounded-lg px-4 py-3 mb-4 font-body-sm text-body-sm">
              {error}
            </div>
          )}

          <form onSubmit={onSubmit} className="grid gap-5">
            <div>
              <label className="block font-label-md text-label-md text-on-surface-variant uppercase tracking-wider mb-2">
                Name
              </label>
              <input
                value={displayName}
                onChange={(e) => setDisplayName(e.target.value)}
                required
                placeholder="Max Mustermann"
                className="w-full border border-outline-variant rounded-lg py-3 px-4 font-body-md text-body-md text-on-surface bg-surface focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all placeholder:text-on-surface-variant/60"
              />
            </div>

            <div className="grid sm:grid-cols-[1fr_140px] gap-4">
              <div>
                <label className="block font-label-md text-label-md text-on-surface-variant uppercase tracking-wider mb-2">
                  Studiengang
                </label>
                <input
                  value={degree}
                  onChange={(e) => setDegree(e.target.value)}
                  required
                  placeholder="M.Sc. Machine Learning"
                  className="w-full border border-outline-variant rounded-lg py-3 px-4 font-body-md text-body-md text-on-surface bg-surface focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all placeholder:text-on-surface-variant/60"
                />
              </div>
              <div>
                <label className="block font-label-md text-label-md text-on-surface-variant uppercase tracking-wider mb-2">
                  Semester
                </label>
                <input
                  value={semester}
                  onChange={(e) => setSemester(e.target.value)}
                  inputMode="numeric"
                  placeholder="4"
                  className="w-full border border-outline-variant rounded-lg py-3 px-4 font-body-md text-body-md text-on-surface bg-surface focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all placeholder:text-on-surface-variant/60"
                />
              </div>
            </div>

            <fieldset>
              <legend className="block font-label-md text-label-md text-on-surface-variant uppercase tracking-wider mb-2">
                Wohnst du in Tübingen?
              </legend>
              <div className="grid sm:grid-cols-3 gap-3">
                {[
                  ["yes", "Ja", "home_pin"],
                  ["no", "Nein", "commute"],
                ].map(([value, label, icon]) => (
                  <button
                    key={value}
                    type="button"
                    onClick={() => {
                      setLivesInTuebingen(value as TuebingenResidence);
                      setLocationSource("manual");
                    }}
                    className={`flex items-center justify-center gap-2 rounded-lg border px-4 py-3 font-label-md text-label-md transition-colors ${
                      livesInTuebingen === value
                        ? "bg-primary text-on-primary border-primary"
                        : "bg-surface text-on-surface-variant border-outline-variant hover:border-primary hover:text-primary"
                    }`}
                  >
                    <span className="material-symbols-outlined text-[18px]">{icon}</span>
                    {label}
                  </button>
                ))}
              </div>
            </fieldset>

            <div className="bg-surface-container-low border border-outline-variant rounded-lg p-4 flex flex-col sm:flex-row sm:items-center gap-3 sm:justify-between">
              <div>
                <p className="font-body-sm text-body-sm text-on-surface">
                  Standort optional verwenden
                </p>
                <p className="font-body-sm text-body-sm text-on-surface-variant">
                  Dein Browser fragt vorher nach Erlaubnis.
                </p>
                {locationStatus && (
                  <p className="font-body-sm text-body-sm text-primary mt-2">{locationStatus}</p>
                )}
              </div>
              <button
                type="button"
                onClick={useCurrentLocation}
                disabled={busyLocation}
                className="inline-flex items-center justify-center gap-2 rounded-lg border border-outline-variant bg-surface px-4 py-3 font-label-md text-label-md text-on-surface hover:border-primary hover:text-primary transition-colors disabled:opacity-50"
              >
                <span className="material-symbols-outlined text-[18px]">
                  {busyLocation ? "progress_activity" : "my_location"}
                </span>
                Standort prüfen
              </button>
            </div>

            <button
              type="submit"
              className="w-full bg-primary text-on-primary font-label-md text-label-md py-3 rounded-lg hover:bg-primary/90 transition-colors flex items-center justify-center gap-2"
            >
              <span className="material-symbols-outlined text-[18px]">check</span>
              Onboarding abschließen
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
