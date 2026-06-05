const TOKEN_KEY = "study-os-thesis:token";

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(t: string | null): void {
  if (t === null) localStorage.removeItem(TOKEN_KEY);
  else localStorage.setItem(TOKEN_KEY, t);
}

/** Thrown when the LLM provider is unavailable (HTTP 503). */
export class LLMUnavailableError extends Error {
  constructor() {
    super("LLM provider not reachable");
    this.name = "LLMUnavailableError";
  }
}

async function readErrorDetail(res: Response): Promise<string> {
  try {
    const data = await res.json();
    if (typeof data?.detail === "string") return data.detail;
    if (data?.detail !== undefined) return JSON.stringify(data.detail);
  } catch {
    // Response body is not JSON.
  }
  return res.statusText || `Request failed: ${res.status}`;
}

type FetchOpts = RequestInit & {
  json?: unknown;
  form?: Record<string, string>;
  /** Raw multipart FormData — do NOT set Content-Type, the browser handles it. */
  multipart?: FormData;
};

export async function api<T = unknown>(path: string, opts: FetchOpts = {}): Promise<T> {
  const headers: Record<string, string> = {
    Accept: "application/json",
    ...(opts.headers as Record<string, string> | undefined),
  };
  const token = getToken();
  if (token) headers["Authorization"] = `Bearer ${token}`;

  let body: BodyInit | undefined = opts.body as BodyInit | undefined;
  if (opts.json !== undefined) {
    headers["Content-Type"] = "application/json";
    body = JSON.stringify(opts.json);
  } else if (opts.form !== undefined) {
    headers["Content-Type"] = "application/x-www-form-urlencoded";
    body = new URLSearchParams(opts.form).toString();
  } else if (opts.multipart !== undefined) {
    // Let the browser set Content-Type with the correct multipart boundary.
    body = opts.multipart;
  }

  const request: RequestInit = { ...opts, headers };
  if (body !== undefined) {
    request.body = body;
  }

  let res: Response;
  try {
    res = await fetch(path, request);
  } catch (err) {
    // Network-level failure (backend down, no internet, DNS failure).
    if (err instanceof TypeError) {
      throw new Error("Server not reachable. Please check your connection.");
    }
    throw err;
  }

  if (!res.ok) {
    // 503 — LLM provider unavailable, surface as a typed error.
    if (res.status === 503) {
      throw new LLMUnavailableError();
    }

    // 401 — session expired or invalid token; clear local state and redirect to login.
    if (res.status === 401) {
      const isAuthRoute =
        window.location.pathname === "/login" ||
        window.location.pathname === "/register";
      if (!isAuthRoute) {
        setToken(null);
        window.location.href = "/login";
        // Return a pending promise — the redirect will happen before anything resolves.
        return new Promise<never>(() => {});
      }
    }

    throw new Error(await readErrorDetail(res));
  }

  if (res.status === 204) return undefined as T;
  return (await res.json()) as T;
}
